#!/usr/bin/env python3
"""38 — dois bolsos no cubo cheio. Interno."""
from __future__ import annotations
import csv, json, math, time
from pathlib import Path
import numpy as np

OUT = Path("/workspace/run38/out")
HBAR = 1.0
M_MASS = 1.0
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
PLUS = (8.0, 0.0, 0.0)
MINUS = (-8.0, 0.0, 0.0)
WIN = 4.0
RECORD = 2


def min_image(d, box):
    return d - box * np.round(d / box)


def gaussian(X, Y, Z, center, s, dV):
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    psi = np.exp(-(dx * dx + dy * dy + dz * dz) / (2.0 * s * s)).astype(np.complex128)
    return psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)


def strang(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
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
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin).astype(np.complex64)
    return psi, y


def win_stats(rho, X, Y, Z, center, dV):
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    inside = (dx * dx + dy * dy + dz * dz) <= WIN * WIN
    mass = float(rho[inside].sum() * dV)
    peak = float(rho[inside].max()) if inside.any() else 0.0
    wsum = float(rho[inside].sum())
    if wsum > 0:
        cx = float((rho[inside] * X[inside]).sum() / wsum)
        cy = float((rho[inside] * Y[inside]).sum() / wsum)
        cz = float((rho[inside] * Z[inside]).sum() / wsum)
        dcom = float(np.linalg.norm(min_image(np.array([cx, cy, cz]) - np.array(center), LBOX)))
    else:
        dcom = float("nan")
    return mass, peak, dcom


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    N = NGRID
    x = np.linspace(-LBOX / 2, LBOX / 2, N, endpoint=False)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    k = 2 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    H = (HBAR ** 2) * k2 / (2 * M_MASS) + ALPHA * np.power(np.sqrt(k2), SIGMA_FRAC)
    half = np.exp(-1j * H * DT / (2 * HBAR) - GAMMA * DT / (2 * HBAR)).astype(np.complex64)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3)))
    g0 = gaussian(X, Y, Z, (0, 0, 0), SIG, dV).astype(np.complex64)
    gp = gaussian(X, Y, Z, PLUS, SIG, dV).astype(np.complex64)
    gm = (-gaussian(X, Y, Z, MINUS, SIG, dV)).astype(np.complex64)
    psi = g0.copy()
    y = np.zeros((3, N, N, N), np.float32)
    nu = np.asarray(NU, np.float32)
    lam = np.asarray(LAM, np.float32)
    rng = np.random.default_rng(SEED)
    n_steps = int(round(T_FINAL / DT))
    plant_step = int(round(T_PLANT / DT))
    rows = []
    t_fill = None
    planted = False
    t0 = time.perf_counter()
    print("38 dois bolsos N=64 T=2 plant=0.5", flush=True)
    for step in range(n_steps + 1):
        t = step * DT
        if (not planted) and step == plant_step:
            psi = (psi + gp + gm).astype(np.complex64)
            planted = True
            print("PLANTED", t, flush=True)
        if step % RECORD == 0 or step == n_steps or step == plant_step:
            rho = np.abs(psi) ** 2
            norm = float(rho.sum() * dV)
            peak = float(rho.max())
            pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
            rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
            mp, pp, dp = win_stats(rho, X, Y, Z, PLUS, dV)
            mm, pm, dm = win_stats(rho, X, Y, Z, MINUS, dV)
            rec = dict(t=t, planted=planted, norm=norm, peak=peak, PR=pr, R_rms=rrms,
                       mass_p=mp, peak_p=pp, d_p=dp, mass_m=mm, peak_m=pm, d_m=dm,
                       peak_in_p=peak > 0 and abs(peak - pp) / peak < 1e-6,
                       peak_in_m=peak > 0 and abs(peak - pm) / peak < 1e-6)
            rows.append(rec)
            if t_fill is None and (pr >= 500 or rrms >= 10):
                t_fill = t
                print("FILL", t, pr, rrms, flush=True)
            if step % 80 == 0 or step == plant_step:
                print(f"t={t:.3f} peak={peak:.3g} p+={pp:.3g} p-={pm:.3g} Mp={mp:.3g} Mm={mm:.3g}", flush=True)
        if step == n_steps:
            break
        psi, y = strang(psi, y, half, noise_amp, rng, nu, lam, (N, N, N))
    wall = time.perf_counter() - t0
    fields = list(rows[0].keys())
    with (OUT / "metrics.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    pre = [r for r in rows if not r["planted"]][-1]
    post = [r for r in rows if r["planted"]][0]
    last = rows[-1]
    summary = dict(run=38, wall_s=wall, t_fill=t_fill, t_plant=T_PLANT,
                   pre=pre, post=post, late=last, n=len(rows))
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2, default=float) + "\n")
    print("WALL", wall, "t_fill", t_fill, flush=True)
    print("PRE", pre["peak_p"], pre["peak_m"], pre["mass_p"], pre["mass_m"])
    print("POST", post["peak_p"], post["peak_m"], post["mass_p"], post["mass_m"], "glob", post["peak"])
    print("LATE", last["peak_p"], last["peak_m"], last["mass_p"], last["mass_m"], "glob", last["peak"])


if __name__ == "__main__":
    main()
