#!/usr/bin/env python3
"""39 — mapa no cubo: rho, y, rho-y. Interno."""
from __future__ import annotations
import csv, json, math, struct, time, zlib
from pathlib import Path
import numpy as np

OUT = Path("/workspace/run39/out")
HBAR = 1.0
M = 1.0
LAMBDA = -10.0
ALPHA = 0.15
SIGMA_FRAC = 1.5
GAMMA = 0.05
NU = (10.0, 0.5, 0.05)
LAM = (3.0, 1.0, 0.3)
KT = 1.0
LBOX = 32.0
NGRID = 64
DT = 0.0025
T_PLANT = 0.5
T_FINAL = 2.0
SEED = 0
SIG = 0.5
PLANT = (8.0, 0.0, 0.0)
WIN = 4.0
RECORD = 2
SNAP = {0.0, 0.005, 0.495, 0.5, 0.6, 0.8, 1.085, 2.0}


def min_image(d, box):
    return d - box * np.round(d / box)


def gaussian(X, Y, Z, center, s, dV):
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    psi = np.exp(-(dx * dx + dy * dy + dz * dz) / (2.0 * s * s)).astype(np.complex128)
    return psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)


def strang(psi, y, half, noise_amp, rng, nu, lam, shape):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((3, 1, 1, 1)) * y).sum(axis=0)
    theta = (LAMBDA * rho + V_mem) * DT
    c, s = np.cos(theta), np.sin(theta)
    re, im = np.real(psi), np.imag(psi)
    psi = ((re * c + im * s) + 1j * (im * c - re * s)).astype(np.complex64)
    y = (y + DT * nu.reshape((3, 1, 1, 1)) * (rho - y)).astype(np.float32)
    if noise_amp > 0:
        xi = ((rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2.0)).astype(np.complex64)
        psi = psi + np.complex64(noise_amp) * xi
    psi = np.fft.ifftn(np.fft.fftn(psi) * half).astype(np.complex64)
    return psi, y


def write_png(path, rgb):
    rgb = np.ascontiguousarray(rgb, dtype=np.uint8)
    h, w, _ = rgb.shape
    def chunk(tag, data):
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)
    raw = b"".join(b"\x00" + rgb[i].tobytes() for i in range(h))
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def magma(x):
    x = np.clip(x, 0, 1)
    r = np.clip(1.4 * x - 0.1, 0, 1)
    g = np.clip(1.6 * x * x - 0.15, 0, 1)
    b = np.clip(0.3 + 1.2 * np.sin(np.pi * x) * (1 - x), 0, 1)
    return np.stack((r, g, b), axis=-1)


def field_png(arr, path, log=True):
    a = np.asarray(arr, dtype=np.float64)
    a = np.maximum(a, 0)
    if log:
        a = np.log10(a + 1e-12)
    lo, hi = float(np.percentile(a, 2)), float(np.percentile(a, 99.5))
    if hi <= lo:
        hi = lo + 1e-12
    n = (a - lo) / (hi - lo)
    write_png(path, (magma(n) * 255).astype(np.uint8))


def panel4(rho, y0, res, vmem, path):
    def norm(a, log=True):
        a = np.maximum(np.asarray(a, dtype=np.float64), 0)
        if log:
            a = np.log10(a + 1e-12)
        lo, hi = float(np.percentile(a, 2)), float(np.percentile(a, 99.5))
        if hi <= lo:
            hi = lo + 1e-12
        return magma((a - lo) / (hi - lo))
    # residual can be signed
    r = np.asarray(res, dtype=np.float64)
    ra = np.abs(r)
    tiles = [norm(rho), norm(np.maximum(y0, 0)), norm(ra), norm(np.maximum(vmem, 0))]
    # 2x2
    top = np.concatenate(tiles[:2], axis=1)
    bot = np.concatenate(tiles[2:], axis=1)
    grid = np.concatenate([top, bot], axis=0)
    # thin white separators
    h, w, _ = grid.shape
    grid[h // 2 - 1 : h // 2 + 1, :] = 1.0
    grid[:, w // 2 - 1 : w // 2 + 1] = 1.0
    write_png(path, (np.clip(grid, 0, 1) * 255).astype(np.uint8))


def win_corr(a, b, mask):
    aa = a[mask].ravel().astype(np.float64)
    bb = b[mask].ravel().astype(np.float64)
    if aa.size < 8:
        return float("nan")
    aa -= aa.mean()
    bb -= bb.mean()
    den = float(np.sqrt((aa * aa).sum() * (bb * bb).sum()))
    if den <= 0:
        return float("nan")
    return float((aa * bb).sum() / den)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    fig = OUT / "mapas"
    fig.mkdir(exist_ok=True)
    N = NGRID
    x = np.linspace(-LBOX / 2, LBOX / 2, N, endpoint=False)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    H = (HBAR ** 2) * k2 / (2 * M) + ALPHA * np.power(np.sqrt(k2), SIGMA_FRAC)
    half = np.exp(-1j * H * DT / (2 * HBAR) - GAMMA * DT / (2 * HBAR)).astype(np.complex64)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3)))
    g0 = gaussian(X, Y, Z, (0, 0, 0), SIG, dV).astype(np.complex64)
    gp = gaussian(X, Y, Z, PLANT, SIG, dV).astype(np.complex64)
    psi = g0.copy()
    y = np.zeros((3, N, N, N), np.float32)
    nu = np.asarray(NU, np.float32)
    lam = np.asarray(LAM, np.float32)
    rng = np.random.default_rng(SEED)
    n_steps = int(round(T_FINAL / DT))
    plant_step = int(round(T_PLANT / DT))
    snap_steps = {int(round(t / DT)) for t in SNAP}
    dxw = min_image(X - PLANT[0], LBOX)
    dyw = min_image(Y - PLANT[1], LBOX)
    dzw = min_image(Z - PLANT[2], LBOX)
    inside = (dxw * dxw + dyw * dyw + dzw * dzw) <= WIN * WIN
    rows = []
    planted = False
    t0 = time.perf_counter()
    print("39 mapa N=64 T=2", flush=True)
    mid_z = N // 2
    for step in range(n_steps + 1):
        t = step * DT
        if (not planted) and step == plant_step:
            psi = (psi + gp).astype(np.complex64)
            planted = True
            print("PLANTED", t, flush=True)
        if step % RECORD == 0 or step in snap_steps or step == n_steps:
            rho = np.abs(psi) ** 2
            y0 = y[0]
            V_mem = (lam.reshape((3, 1, 1, 1)) * y).sum(axis=0)
            res = rho - y0
            rec = dict(
                t=t,
                planted=planted,
                peak=float(rho.max()),
                glue_in=win_corr(y0, rho, inside),
                glue_out=win_corr(y0, rho, ~inside),
                res_in=float(np.abs(res[inside]).mean()),
                res_out=float(np.abs(res[~inside]).mean()),
            )
            rows.append(rec)
            if step in snap_steps or abs(t - T_PLANT) < 1e-12:
                tag = f"{t:.3f}".replace(".", "p")
                sl = np.s_[:, :, mid_z]
                field_png(rho[sl], fig / f"rho_{tag}.png")
                field_png(np.maximum(y0[sl], 0), fig / f"y_{tag}.png")
                field_png(np.abs(res[sl]), fig / f"res_{tag}.png")
                field_png(np.maximum(V_mem[sl], 0), fig / f"vmem_{tag}.png")
                panel4(rho[sl], y0[sl], res[sl], V_mem[sl], fig / f"mapa_{tag}.png")
                print("SNAP", t, "glue", rec["glue_in"], rec["glue_out"], flush=True)
        if step == n_steps:
            break
        psi, y = strang(psi, y, half, noise_amp, rng, nu, lam, (N, N, N))
    wall = time.perf_counter() - t0
    with (OUT / "metrics.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    (OUT / "summary.json").write_text(json.dumps({"run": 39, "wall_s": wall, "n": len(rows), "snaps": sorted(SNAP)}, indent=2) + "\n")
    print("WALL", wall, flush=True)


if __name__ == "__main__":
    main()
