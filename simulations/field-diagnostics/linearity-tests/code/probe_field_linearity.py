#!/usr/bin/env python3
"""Q04 — linearidade efetiva / superposição (campo + plano dos 2 átomos).

PROTOCOL: /tmp/Q04_linearidade/PROTOCOL.md
  SHA-256 9b6b2f49352cf458d26c4bc22d36037c6057c52829139a784fa4098c489b51df
Passo Strang idêntico a Q02 code/run_q02.py
  SHA-256 ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365

Pergunta: existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B)
na dinâmica completa? Por quanto tempo a soma de dois átomos
permanece no plano dos dois átomos?

Π = plano das CIs {G_A, G_B}, declarado antes. NÃO é o POD late de Q03.
Ruído FDT idêntico no triple (mesma seed, mesma sequência de chamadas).
Sem comparação com MQ. Sem isolar termos. Sem mudar Theta_core.
1 gaussiana = 1 átomo. Volume preenchido = universo.
Pilotos 1–34 não são confirmatórios.
Nunca SUPPORTED para MQ.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import shutil
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
Q04_DIR = VAULT / "QM" / "Q04_linearidade"
FONTES = VAULT / "Fontes"
TMP_ROOT = Path("/tmp/Q04_linearidade")
OUT = TMP_ROOT / "out"
PROTOCOL_PATHS = (
    TMP_ROOT / "PROTOCOL.md",
    Q04_DIR / "PROTOCOL.md",
)
PROTOCOL_SHA_KNOWN = "9b6b2f49352cf458d26c4bc22d36037c6057c52829139a784fa4098c489b51df"
Q02_SOLVER_SHA = "ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365"
CANONICAL_SHA = "e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e"
Q03_PROTOCOL_SHA = "f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16"
Q02_PROTOCOL_V2_SHA = "bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c"

# --- Theta_core (Q00) — IMUTÁVEL ---
HBAR = 1.0
M_MASS = 1.0
LAMBDA = -10.0
ALPHA = 0.15
SIGMA_FRAC = 1.5
GAMMA = 0.05
NU = (10.0, 0.5, 0.05)
LAM = (3.0, 1.0, 0.3)
FDT_COUPLE = True
KT = 1.0
D_DIM = 3
BC = "periodic"
STEP_MODE = "strang"

# --- N_num / caixa (célula Q01a N=64, NÃO calibração) ---
LBOX = 32.0
NGRID = 64
DT = 0.0025
T_FINAL = 8.0
SEEDS = (0, 1)
MEMBERS = ("A", "B", "S")
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
CENTER_A = (-3.0, 0.0, 0.0)
CENTER_B = (3.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
SNAP_EVERY = 8
K_CUT_FACTOR = 1.0
PRECISION = "complex64"
DTYPE_PSI_NP = np.complex64
DTYPE_R_NP = np.float32
LATE_FRAC = 0.8
T_LATE = LATE_FRAC * T_FINAL  # 6.4
T_MARK_EARLY = 0.2
BOX_HALF = LBOX / 2.0
PRINT_EVERY_T = 2.0
PEAK_FRAC_BLOB = 0.20
MIN_DIST_ATOM = 2.0 * INIT_SIGMA
NMS_CAP = 48

BACKEND = "mlx"
MLX_OK = False
mx = None
try:
    import mlx.core as mx

    MLX_OK = True
    BACKEND = "mlx"
except Exception as _exc:
    MLX_OK = False
    BACKEND = "numpy"
    print("mlx_import_failed", _exc, "fallback numpy fp32", flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def now_sp() -> str:
    try:
        from zoneinfo import ZoneInfo
        import datetime

        return datetime.datetime.now(ZoneInfo("America/Sao_Paulo")).strftime(
            "%Y-%m-%d %H:%M:%S BRT"
        )
    except Exception:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC")


def jsonable(obj):
    if obj is None:
        return None
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating, float)):
        v = float(obj)
        if not math.isfinite(v):
            return None
        return v
    if isinstance(obj, (np.ndarray, list, tuple)):
        return [jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, Path):
        return str(obj)
    return obj


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def min_image(d, box):
    return d - box * np.round(d / box)


def l2_norm(psi, dV):
    return float(np.sqrt(np.sum(np.abs(psi) ** 2) * dV))


def inner(u, v, dV):
    return complex(np.vdot(np.asarray(u).ravel(), np.asarray(v).ravel()) * dV)


def gaussian_atom(X, Y, Z, center, s, dV):
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    rr2 = dx * dx + dy * dy + dz * dz
    psi = np.exp(-rr2 / (2.0 * s * s)).astype(np.complex128)
    nrm = np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    psi = psi / nrm
    return psi


def gram_schmidt_plane(ga, gb, dV):
    """Π0 = span{G_A, G_B} orthonormalizado. Declarado antes do run."""
    n0 = l2_norm(ga, dV)
    u0 = (ga / n0).astype(np.complex64, copy=False)
    proj = inner(u0, gb, dV)
    w = gb - proj * u0
    n1 = l2_norm(w, dV)
    u1 = (w / n1).astype(np.complex64, copy=False)
    return u0, u1


def pi0_proj_norm2(psi, u0, u1, dV):
    c0 = inner(u0, psi, dV)
    c1 = inner(u1, psi, dV)
    return float(abs(c0) ** 2 + abs(c1) ** 2)


def find_pair_sep(rho, dx, box):
    """Espírito run 30: máximos locais; pair_sep só se n_det==2. Senão omitido."""
    try:
        from scipy.ndimage import maximum_filter
    except Exception:
        return float("nan"), 0, False
    peak = float(rho.max()) if rho.size else 0.0
    if (not np.isfinite(peak)) or peak <= 0.0:
        return float("nan"), 0, False
    footprint = maximum_filter(rho, size=3, mode="wrap")
    is_max = (rho == footprint) & (rho >= PEAK_FRAC_BLOB * peak)
    coords = np.argwhere(is_max)
    n_raw = int(coords.shape[0])
    if n_raw == 0 or n_raw > NMS_CAP:
        return float("nan"), int(n_raw), False
    vals = rho[is_max]
    order = np.argsort(-vals)
    coords = coords[order]
    xyz = coords.astype(np.float64) * dx - box / 2.0
    keep = []
    for i in range(xyz.shape[0]):
        ok = True
        for j in keep:
            d = min_image(xyz[i] - xyz[j], box)
            if float(np.linalg.norm(d)) < MIN_DIST_ATOM:
                ok = False
                break
        if ok:
            keep.append(i)
    n_det = len(keep)
    if n_det != 2:
        return float("nan"), int(n_det), False
    p0 = xyz[keep[0]]
    p1 = xyz[keep[1]]
    sep = float(np.linalg.norm(min_image(p0 - p1, box)))
    return sep, int(n_det), True


def mul_phase_mlx(psi, theta):
    c = mx.cos(theta)
    s = mx.sin(theta)
    re = mx.real(psi)
    im = mx.imag(psi)
    nre = re * c + im * s
    nim = im * c - re * s
    return nre.astype(mx.complex64) + (1j * nim.astype(mx.complex64))


def strang_step_mlx(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
    """Passo Strang Q02 — NÃO alterar."""
    psi = mx.fft.ifftn(mx.fft.fftn(psi) * half_lin)
    rho = mx.abs(psi) ** 2
    V_mem = (lam.reshape((len(NU), 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    psi = mul_phase_mlx(psi, V_tot * (DT / HBAR))
    y = y + DT * nu.reshape((len(NU), 1, 1, 1)) * (rho - y)
    if noise_amp > 0.0:
        xi_np = (
            (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2.0)
        ).astype(np.complex64, copy=False)
        psi = psi + noise_amp * mx.array(xi_np)
    psi = mx.fft.ifftn(mx.fft.fftn(psi) * half_lin)
    mx.eval(psi, y)
    return psi, y


def strang_step_np(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
    """Fallback numpy fp32 / complex64 (mesma classe de precisão; NÃO fp64)."""
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((len(NU), 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    theta = V_tot * (DT / HBAR)
    c = np.cos(theta)
    s = np.sin(theta)
    re = np.real(psi)
    im = np.imag(psi)
    psi = (re * c + im * s) + 1j * (im * c - re * s)
    psi = psi.astype(np.complex64, copy=False)
    y = y + DT * nu.reshape((len(NU), 1, 1, 1)) * (rho - y)
    y = y.astype(np.float32, copy=False)
    if noise_amp > 0.0:
        xi_np = (
            (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2.0)
        ).astype(np.complex64, copy=False)
        psi = psi + np.complex64(noise_amp) * xi_np
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin).astype(np.complex64, copy=False)
    return psi, y


def record_member(psi, t, dV, r2):
    rho = np.abs(psi) ** 2
    finite = bool(np.isfinite(rho).all())
    if not finite:
        return {
            "t": t,
            "norm": float("nan"),
            "peak": float("nan"),
            "PR": float("nan"),
            "R_rms": float("nan"),
            "finite": False,
        }
    norm = float(rho.sum() * dV)
    peak = float(rho.max())
    pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
    rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
    return {
        "t": t,
        "norm": norm,
        "peak": peak,
        "PR": pr,
        "R_rms": rrms,
        "finite": True,
    }


def build_grid():
    N = NGRID
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False, dtype=np.float64)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    kvec = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(kvec, kvec, kvec, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k_mag = np.sqrt(k2)
    H_lin = (HBAR * HBAR * k2) / (2.0 * M_MASS)
    if ALPHA != 0.0:
        H_lin = H_lin + ALPHA * np.power(k_mag, SIGMA_FRAC)
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    ga = gaussian_atom(X, Y, Z, CENTER_A, INIT_SIGMA, dV)
    gb = gaussian_atom(X, Y, Z, CENTER_B, INIT_SIGMA, dV)
    sab = ga + gb
    norm_ab = l2_norm(sab, dV)
    a_coef = 1.0 / norm_ab
    b_coef = 1.0 / norm_ab
    gs = (sab / norm_ab)
    r0 = l2_norm(gs - a_coef * ga - b_coef * gb, dV)
    u0, u1 = gram_schmidt_plane(ga, gb, dV)
    ics = {
        "A": ga.astype(DTYPE_PSI_NP),
        "B": gb.astype(DTYPE_PSI_NP),
        "S": gs.astype(DTYPE_PSI_NP),
    }
    return {
        "x": x,
        "X": X,
        "Y": Y,
        "Z": Z,
        "dx": dx,
        "dV": dV,
        "r2": r2.astype(np.float64, copy=False),
        "half_lin": half_lin.astype(DTYPE_PSI_NP),
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
        "ics": ics,
        "a": float(a_coef),
        "b": float(b_coef),
        "norm_ab": float(norm_ab),
        "rlin0_check": float(r0),
        "u0": u0,
        "u1": u1,
        "y0": np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R_NP),
        "shape": (N, N, N),
    }


def evolve_member(member, seed, grid, backend, snap_path, mid_dir):
    t_wall0 = time.perf_counter()
    N = NGRID
    dx = grid["dx"]
    dV = grid["dV"]
    r2 = grid["r2"]
    noise_amp = grid["noise_amp"]
    f_FDT = grid["f_FDT"]
    shape = grid["shape"]
    psi0 = grid["ics"][member]
    y0 = grid["y0"]
    n_steps = int(round(T_FINAL / DT))
    n_snap = n_steps // SNAP_EVERY + 1
    snap_path.parent.mkdir(parents=True, exist_ok=True)
    snaps = np.lib.format.open_memmap(
        snap_path, mode="w+", dtype=np.complex64, shape=(n_snap, N, N, N)
    )
    rng = np.random.default_rng(seed)
    nu_np = np.asarray(NU, dtype=np.float32)
    lam_np = np.asarray(LAM, dtype=np.float32)

    if backend == "mlx":
        half_lin = mx.array(grid["half_lin"])
        nu = mx.array(nu_np)
        lam = mx.array(lam_np)
        psi = mx.array(psi0)
        y = mx.array(y0)
        mx.eval(psi, y, half_lin, nu, lam)
        step_fn = strang_step_mlx
    else:
        half_lin = grid["half_lin"]
        nu = nu_np
        lam = lam_np
        psi = psi0.copy()
        y = y0.copy()
        step_fn = strang_step_np

    print(
        f"=== Q04 seed={seed:02d} member={member} N={N} backend={backend} {PRECISION} ===",
        flush=True,
    )
    print(
        f"seed={seed:02d} {member} L {LBOX} dx {dx} dt {DT} T {T_FINAL} "
        f"n_steps {n_steps} n_snap {n_snap} f_FDT {f_FDT} noise_amp {noise_amp}",
        flush=True,
    )

    metrics = []
    midplanes = {}
    blew = False
    blow_t = None
    last_print_bucket = -1
    i_snap = 0
    for step in range(n_steps + 1):
        t = step * DT
        if step % SNAP_EVERY == 0 or step == n_steps:
            if backend == "mlx":
                psi_np = np.array(psi)
            else:
                psi_np = np.asarray(psi)
            if i_snap < n_snap:
                snaps[i_snap] = psi_np
                i_snap += 1
            rec = record_member(psi_np, t, dV, r2)
            rec["seed"] = seed
            rec["member"] = member
            rec["backend"] = backend
            metrics.append(rec)
            if abs(t - 0.0) < 1e-12:
                midplanes[0.0] = np.abs(psi_np[:, :, N // 2]).astype(np.float32)
            elif abs(t - 0.1) < 1e-9:
                midplanes[0.1] = np.abs(psi_np[:, :, N // 2]).astype(np.float32)
            bucket = int(t // PRINT_EVERY_T)
            if bucket != last_print_bucket or step == n_steps or (not rec["finite"]):
                last_print_bucket = bucket
                print(
                    f"seed={seed:02d} {member} t={t:.4f} norm={rec['norm']:.6e} "
                    f"peak={rec['peak']:.6e} PR={rec['PR']:.6e} "
                    f"Rrms={rec['R_rms']:.6e} finite={rec['finite']}",
                    flush=True,
                )
            if (not rec["finite"]) or (
                np.isfinite(rec["peak"]) and abs(rec["peak"]) > 1.0e30
            ):
                blew = True
                blow_t = t
                print("BLOWUP_OR_NAN", "seed", seed, "member", member, "t", t, flush=True)
                break
        if step == n_steps or blew:
            break
        psi, y = step_fn(psi, y, half_lin, noise_amp, rng, nu, lam, shape)

    snaps.flush()
    del snaps
    wall = time.perf_counter() - t_wall0
    mid_dir.mkdir(parents=True, exist_ok=True)
    for tk, sl in midplanes.items():
        tag = f"{tk:.2f}".replace(".", "p")
        np.save(mid_dir / f"seed{seed:02d}_{member}_mid_t{tag}.npy", sl)
    finite_final = bool(metrics and metrics[-1]["finite"] and (not blew))
    print(
        f"seed={seed:02d} {member} done wall_s={wall:.3f} finite={finite_final} "
        f"blew={blew} blow_t={blow_t} n_rec={len(metrics)}",
        flush=True,
    )
    return {
        "member": member,
        "seed": seed,
        "metrics": metrics,
        "blew": blew,
        "blow_t": blow_t,
        "finite": finite_final,
        "wall_s": wall,
        "n_snap_written": i_snap,
        "snap_path": str(snap_path),
        "midplanes": {str(k): True for k in midplanes},
    }


def nearest_idx(t_arr, t_target):
    return int(np.argmin(np.abs(t_arr - t_target)))


def first_exceed(t_arr, vals, thr):
    for t, v in zip(t_arr, vals):
        if np.isfinite(v) and v > thr:
            return float(t)
    return float("inf")


def analyze_seed(seed, grid, member_runs, raw_dir):
    dV = grid["dV"]
    dx = grid["dx"]
    a = grid["a"]
    b = grid["b"]
    u0 = grid["u0"]
    u1 = grid["u1"]
    n_steps = int(round(T_FINAL / DT))
    n_snap = n_steps // SNAP_EVERY + 1
    t_arr = np.arange(n_snap, dtype=np.float64) * (SNAP_EVERY * DT)
    mmaps = {}
    for mem in MEMBERS:
        p = Path(member_runs[mem]["snap_path"])
        mmaps[mem] = np.lib.format.open_memmap(p, mode="r", dtype=np.complex64, shape=(n_snap, NGRID, NGRID, NGRID))
    rows = []
    finite_all = all(member_runs[m]["finite"] for m in MEMBERS)
    n_ok = min(member_runs[m]["n_snap_written"] for m in MEMBERS)
    for i in range(n_ok):
        t = float(t_arr[i])
        psi_a = np.asarray(mmaps["A"][i])
        psi_b = np.asarray(mmaps["B"][i])
        psi_s = np.asarray(mmaps["S"][i])
        if not (np.isfinite(psi_a).all() and np.isfinite(psi_b).all() and np.isfinite(psi_s).all()):
            rows.append({
                "t": t,
                "R_lin_field": float("nan"),
                "R_lin_Pi": float("nan"),
                "leak_A": float("nan"),
                "leak_B": float("nan"),
                "leak_S": float("nan"),
                "pair_sep": float("nan"),
                "n_det": 0,
                "two_blobs": False,
                "norm_A": float("nan"),
                "norm_B": float("nan"),
                "norm_S": float("nan"),
                "finite": False,
            })
            continue
        na = l2_norm(psi_a, dV)
        nb = l2_norm(psi_b, dV)
        ns = l2_norm(psi_s, dV)
        resid = psi_s - a * psi_a - b * psi_b
        den_f = abs(a) * na + abs(b) * nb
        rlin_f = (l2_norm(resid, dV) / den_f) if den_f > 0 else float("nan")
        npi_a = math.sqrt(max(pi0_proj_norm2(psi_a, u0, u1, dV), 0.0))
        npi_b = math.sqrt(max(pi0_proj_norm2(psi_b, u0, u1, dV), 0.0))
        npi_s = math.sqrt(max(pi0_proj_norm2(psi_s, u0, u1, dV), 0.0))
        npi_r = math.sqrt(max(pi0_proj_norm2(resid, u0, u1, dV), 0.0))
        den_p = abs(a) * npi_a + abs(b) * npi_b
        rlin_p = (npi_r / den_p) if den_p > 0 else float("nan")
        leak_a = 1.0 - (npi_a * npi_a) / max(na * na, 1e-300)
        leak_b = 1.0 - (npi_b * npi_b) / max(nb * nb, 1e-300)
        leak_s = 1.0 - (npi_s * npi_s) / max(ns * ns, 1e-300)
        rho_s = np.abs(psi_s) ** 2
        sep, n_det, two = find_pair_sep(rho_s, dx, LBOX)
        rows.append({
            "t": t,
            "R_lin_field": float(rlin_f),
            "R_lin_Pi": float(rlin_p),
            "leak_A": float(leak_a),
            "leak_B": float(leak_b),
            "leak_S": float(leak_s),
            "pair_sep": float(sep) if two else float("nan"),
            "n_det": int(n_det),
            "two_blobs": bool(two),
            "norm_A": float(na),
            "norm_B": float(nb),
            "norm_S": float(ns),
            "finite": True,
        })
    for mem in MEMBERS:
        del mmaps[mem]
    csv_path = raw_dir / f"seed{seed:02d}_rlin.csv"
    write_csv(csv_path, rows, list(rows[0].keys()) if rows else [
        "t", "R_lin_field", "R_lin_Pi", "leak_A", "leak_B", "leak_S",
        "pair_sep", "n_det", "two_blobs", "norm_A", "norm_B", "norm_S", "finite",
    ])
    t_np = np.array([r["t"] for r in rows], dtype=np.float64)
    rlin = np.array([r["R_lin_field"] for r in rows], dtype=np.float64)
    rpi = np.array([r["R_lin_Pi"] for r in rows], dtype=np.float64)
    leak_s = np.array([r["leak_S"] for r in rows], dtype=np.float64)

    def at_t(arr, t_target):
        if arr.size == 0:
            return float("nan")
        return float(arr[nearest_idx(t_np, t_target)])

    late_mask = t_np >= T_LATE
    late_vals = rlin[late_mask]
    late_vals = late_vals[np.isfinite(late_vals)]
    late_leak = leak_s[late_mask]
    late_leak = late_leak[np.isfinite(late_leak)]
    t_half = first_exceed(t_np, rlin, 0.5)
    t_leak = first_exceed(t_np, leak_s, 0.5)
    pair_vals = [(r["t"], r["pair_sep"]) for r in rows if r.get("two_blobs")]
    pair_note = "omitido (blobs não encontráveis)" if not pair_vals else None
    summary = {
        "seed": seed,
        "finite": bool(finite_all and rows and rows[-1]["finite"]),
        "blew": any(member_runs[m]["blew"] for m in MEMBERS),
        "blow_t": {m: member_runs[m]["blow_t"] for m in MEMBERS},
        "wall_s": {m: member_runs[m]["wall_s"] for m in MEMBERS},
        "R_lin_field_t0": at_t(rlin, 0.0),
        "R_lin_field_t002": at_t(rlin, 0.02),
        "R_lin_field_t01": at_t(rlin, 0.10),
        "R_lin_field_t02": at_t(rlin, 0.20),
        "R_lin_field_late_mean": float(late_vals.mean()) if late_vals.size else float("nan"),
        "R_lin_Pi_t0": at_t(rpi, 0.0),
        "R_lin_Pi_late_mean": float(rpi[late_mask][np.isfinite(rpi[late_mask])].mean()) if np.any(late_mask & np.isfinite(rpi)) else float("nan"),
        "leak_S_t02": at_t(leak_s, 0.20),
        "leak_S_late_mean": float(late_leak.mean()) if late_leak.size else float("nan"),
        "t_half": t_half,
        "t_leak": t_leak,
        "pair_sep_available": bool(pair_vals),
        "pair_sep_times": [p[0] for p in pair_vals],
        "pair_sep_values": [p[1] for p in pair_vals],
        "pair_sep_note": pair_note,
        "n_records": len(rows),
        "csv": str(csv_path),
    }
    with (raw_dir / f"seed{seed:02d}_summary.json").open("w") as f:
        json.dump(jsonable(summary), f, indent=2)
    for mem in MEMBERS:
        mets = member_runs[mem]["metrics"]
        if mets:
            write_csv(raw_dir / f"seed{seed:02d}_{mem}_metrics.csv", mets, list(mets[0].keys()))
    return summary, rows


def make_figures(fig_dir, by_seed, grid):
    fig_dir.mkdir(parents=True, exist_ok=True)
    colors = {0: "#1f4e79", 1: "#c45911"}
    # rlin_time
    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    for seed, pack in by_seed.items():
        rows = pack["rows"]
        t = np.array([r["t"] for r in rows])
        rf = np.array([r["R_lin_field"] for r in rows])
        rp = np.array([r["R_lin_Pi"] for r in rows])
        ax.plot(t, rf, color=colors.get(seed, "k"), lw=1.6, label=f"R_lin campo  seed {seed}")
        ax.plot(t, rp, color=colors.get(seed, "k"), lw=1.2, ls="--", label=f"R_lin Π₀  seed {seed}")
    ax.axvline(T_MARK_EARLY, color="0.45", ls=":", lw=1.0)
    ax.axvline(T_LATE, color="0.45", ls=":", lw=1.0)
    ax.text(T_MARK_EARLY, ax.get_ylim()[1] if False else 0.02, " t=0.2", color="0.35", fontsize=8)
    ax.text(T_LATE, 0.02, " t=6.4", color="0.35", fontsize=8)
    ax.set_xlabel("tempo t")
    ax.set_ylabel("R_lin")
    ax.set_title("Linearidade: campo e projeção no plano dos 2 átomos")
    ax.legend(fontsize=8, loc="best")
    ax.set_xlim(0, T_FINAL)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(fig_dir / "rlin_time.png", dpi=150)
    plt.close(fig)

    # leak_time
    fig, ax = plt.subplots(figsize=(10.2, 5.6))
    leak_styles = {"A": "-", "B": "--", "S": "-"}
    leak_colors = {"A": "#2b6cb0", "B": "#c05621", "S": "#276749"}
    for seed, pack in by_seed.items():
        rows = pack["rows"]
        t = np.array([r["t"] for r in rows])
        for key, lab in (("leak_A", "A"), ("leak_B", "B"), ("leak_S", "S")):
            v = np.array([r[key] for r in rows])
            alpha = 1.0 if seed == 0 else 0.55
            ax.plot(
                t, v,
                color=leak_colors[lab],
                ls=leak_styles[lab],
                lw=1.5 if seed == 0 else 1.1,
                alpha=alpha,
                label=f"vazamento {lab}  seed {seed}",
            )
    ax.axvline(T_MARK_EARLY, color="0.45", ls=":", lw=1.0)
    ax.axvline(T_LATE, color="0.45", ls=":", lw=1.0)
    ax.set_xlabel("tempo t")
    ax.set_ylabel("vazamento do plano Π₀")
    ax.set_title("Vazamento do plano dos dois átomos")
    ax.legend(fontsize=7, ncol=2, loc="best")
    ax.set_xlim(0, T_FINAL)
    ax.set_ylim(-0.02, 1.02)
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    fig.savefig(fig_dir / "leak_time.png", dpi=150)
    plt.close(fig)

    # slices 2x3
    seed_fig = 0 if 0 in by_seed else (next(iter(by_seed)) if by_seed else 0)
    mid_dir = OUT / "raw"
    fig, axes = plt.subplots(2, 3, figsize=(12.0, 7.6))
    times = (0.0, 0.1)
    members = ("A", "B", "S")
    extent = (-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2)
    for i, tt in enumerate(times):
        tag = f"{tt:.2f}".replace(".", "p")
        for j, mem in enumerate(members):
            ax = axes[i, j]
            p = mid_dir / f"seed{seed_fig:02d}_{mem}_mid_t{tag}.npy"
            if p.is_file():
                sl = np.load(p)
                im = ax.imshow(sl.T, origin="lower", extent=extent, cmap="magma")
                fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            else:
                ax.text(0.5, 0.5, "ausente", ha="center", va="center", transform=ax.transAxes)
            ax.set_title(f"|Ψ|  {mem}   t={tt}")
            ax.set_xlabel("x")
            ax.set_ylabel("y")
    fig.suptitle(f"Plano médio |Ψ| (seed {seed_fig})", fontsize=12)
    fig.tight_layout()
    fig.savefig(fig_dir / "slices_t0_t01.png", dpi=150)
    plt.close(fig)

    # late bar
    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    seeds = sorted(by_seed)
    vals = [by_seed[s]["summary"].get("R_lin_field_late_mean", float("nan")) for s in seeds]
    xpos = np.arange(len(seeds))
    ax.bar(xpos, [v if np.isfinite(v) else 0.0 for v in vals], color=["#1f4e79", "#c45911"][: len(seeds)])
    ax.set_xticks(xpos)
    ax.set_xticklabels([f"seed {s}" for s in seeds])
    ax.set_ylabel("R_lin campo  (média tardia, t≥6.4)")
    ax.set_title("Linearidade tardia por seed")
    ax.axhline(0.20, color="0.4", ls="--", lw=0.9)
    ax.axhline(0.50, color="0.4", ls="--", lw=0.9)
    ax.set_ylim(0, max(1.05, max([v for v in vals if np.isfinite(v)] + [0.6]) * 1.15))
    for i, v in enumerate(vals):
        if np.isfinite(v):
            ax.text(i, v + 0.02, f"{v:.3f}", ha="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(fig_dir / "late_rlin_bar.png", dpi=150)
    plt.close(fig)


def fmt_inf(x):
    if x is None:
        return "None"
    if isinstance(x, float) and not math.isfinite(x):
        return "inf"
    if isinstance(x, float):
        return f"{x:.6g}"
    return str(x)


def mean_over(vals):
    arr = np.array([v for v in vals if v is not None and np.isfinite(v)], dtype=np.float64)
    if arr.size == 0:
        return float("nan")
    return float(arr.mean())


def copy_into_vault(solver_src: Path):
    try:
        Q04_DIR.mkdir(parents=True, exist_ok=True)
        (Q04_DIR / "code").mkdir(parents=True, exist_ok=True)
        (Q04_DIR / "figures").mkdir(parents=True, exist_ok=True)
        (Q04_DIR / "raw").mkdir(parents=True, exist_ok=True)
        FONTES.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        print("vault_mkdir_failed", exc, flush=True)
        return False
    mapping = [
        (TMP_ROOT / "PROTOCOL.md", Q04_DIR / "PROTOCOL.md"),
        (OUT / "Q04.md", Q04_DIR / "Q04.md"),
        (OUT / "analysis.md", Q04_DIR / "analysis.md"),
        (OUT / "result.json", Q04_DIR / "result.json"),
        (OUT / "config.json", Q04_DIR / "config.json"),
        (OUT / "SHA256SUMS.txt", Q04_DIR / "SHA256SUMS.txt"),
        (solver_src, Q04_DIR / "code" / "run_q04.py"),
        (solver_src, FONTES / "run_q04.py"),
        (solver_src, TMP_ROOT / "run_q04.py"),
    ]
    for src, dst in mapping:
        if src.is_file():
            try:
                if src.resolve() != dst.resolve():
                    shutil.copy2(src, dst)
            except Exception as exc:
                print("copy_failed", src, dst, exc, flush=True)
    for p in (OUT / "figures").glob("*.png"):
        try:
            shutil.copy2(p, Q04_DIR / "figures" / p.name)
        except Exception as exc:
            print("copy_fig_failed", p, exc, flush=True)
    for p in (OUT / "raw").iterdir():
        if p.suffix in {".csv", ".json", ".npy"} and p.is_file():
            try:
                shutil.copy2(p, Q04_DIR / "raw" / p.name)
            except Exception as exc:
                print("copy_raw_failed", p, exc, flush=True)
    return True


def main():
    started = now_sp()
    t0 = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    raw_dir = OUT / "raw"
    fig_dir = OUT / "figures"
    raw_dir.mkdir(parents=True, exist_ok=True)
    fig_dir.mkdir(parents=True, exist_ok=True)

    proto = None
    for p in PROTOCOL_PATHS:
        if p.is_file():
            proto = p
            break
    protocol_sha = sha256_file(proto) if proto is not None else ""
    solver_src = Path(__file__).resolve()
    solver_sha = sha256_file(solver_src)
    print("PROTOCOL_SHA", protocol_sha, "known", PROTOCOL_SHA_KNOWN, flush=True)
    print("SOLVER_SHA", solver_sha, flush=True)
    if protocol_sha and protocol_sha != PROTOCOL_SHA_KNOWN:
        print("WARNING protocol hash differs from frozen known", flush=True)

    backend = BACKEND
    device_s = "numpy"
    if MLX_OK:
        try:
            device_s = str(mx.default_device())
            print("device", device_s, flush=True)
        except Exception as exc:
            print("mlx_device_failed", exc, "fallback numpy fp32", flush=True)
            backend = "numpy"
    else:
        backend = "numpy"

    grid = build_grid()
    print(
        "IC a", grid["a"], "b", grid["b"], "||A+B||", grid["norm_ab"],
        "R_lin_field(t=0) check", grid["rlin0_check"],
        flush=True,
    )

    by_seed = {}
    member_walls = []
    n_blowup = 0
    for seed in SEEDS:
        member_runs = {}
        for mem in MEMBERS:
            snap_path = raw_dir / f"seed{seed:02d}_{mem}_psi_t.npy"
            rec = evolve_member(mem, seed, grid, backend, snap_path, raw_dir)
            member_runs[mem] = rec
            member_walls.append(rec["wall_s"])
            if rec["blew"]:
                n_blowup += 1
        summary, rows = analyze_seed(seed, grid, member_runs, raw_dir)
        by_seed[seed] = {"summary": summary, "rows": rows, "members": member_runs}
        # apagar memmaps grandes depois da análise da seed
        for mem in MEMBERS:
            p = Path(member_runs[mem]["snap_path"])
            if p.is_file():
                try:
                    p.unlink()
                    print("deleted_memmap", p, flush=True)
                except Exception as exc:
                    print("memmap_delete_failed", p, exc, flush=True)

    finite_seeds = [s for s, pack in by_seed.items() if pack["summary"]["finite"]]
    n_finite = len(finite_seeds)
    # blowup counted per seed (if any member blew)
    n_seed_blow = sum(1 for s, pack in by_seed.items() if pack["summary"]["blew"] or (not pack["summary"]["finite"]))

    late_means = [by_seed[s]["summary"]["R_lin_field_late_mean"] for s in finite_seeds]
    rlin_late = mean_over(late_means)
    rlin_t0 = mean_over([by_seed[s]["summary"]["R_lin_field_t0"] for s in finite_seeds])
    rlin_t002 = mean_over([by_seed[s]["summary"]["R_lin_field_t002"] for s in finite_seeds])
    rlin_t01 = mean_over([by_seed[s]["summary"]["R_lin_field_t01"] for s in finite_seeds])
    rlin_t02 = mean_over([by_seed[s]["summary"]["R_lin_field_t02"] for s in finite_seeds])
    leak_s_late = mean_over([by_seed[s]["summary"]["leak_S_late_mean"] for s in finite_seeds])
    leak_s_t02 = mean_over([by_seed[s]["summary"]["leak_S_t02"] for s in finite_seeds])

    def mean_or_inf(key):
        vals = [by_seed[s]["summary"][key] for s in finite_seeds]
        if not vals:
            return float("inf")
        if any((isinstance(v, float) and not math.isfinite(v)) for v in vals):
            # if any is inf, and we need a representative: report per-seed; official mean of finite t_half
            fin = [v for v in vals if isinstance(v, float) and math.isfinite(v)]
            if not fin:
                return float("inf")
            return float(np.mean(fin))
        return float(np.mean(vals))

    t_half_mean = mean_or_inf("t_half")
    t_leak_mean = mean_or_inf("t_leak")

    if n_seed_blow > 1:
        verdict = "NUMERICAL_FAILURE"
        verdict_why = f">1 de 2 seeds NaN/blowup (n_seed_blow={n_seed_blow})."
    elif n_finite == 0:
        verdict = "NUMERICAL_FAILURE"
        verdict_why = "nenhuma seed finita."
    elif np.isfinite(rlin_late) and rlin_late < 0.20:
        verdict = "PARTIAL"
        verdict_why = (
            f"média late R_lin_field={rlin_late:.6g} < 0.20 "
            "(linearidade emergente no atrator — inesperado)."
        )
    elif np.isfinite(rlin_late) and rlin_late > 0.50:
        verdict = "NOT_SUPPORTED"
        verdict_why = (
            f"média late R_lin_field={rlin_late:.6g} > 0.50 "
            "(sem superposição efetiva no universo preenchido)."
        )
    else:
        verdict = "INCONCLUSIVE"
        verdict_why = (
            f"média late R_lin_field={rlin_late:.6g} em [0.20, 0.50] "
            "(ou não finita de forma útil)."
        )

    make_figures(fig_dir, by_seed, grid)
    finished = now_sp()
    wall_total = time.perf_counter() - t0

    # per-seed tables for analysis
    seed_lines = []
    for s in SEEDS:
        sm = by_seed[s]["summary"]
        seed_lines.append(
            f"| {s} | {sm['finite']} | {fmt_inf(sm['R_lin_field_t0'])} | "
            f"{fmt_inf(sm['R_lin_field_t002'])} | {fmt_inf(sm['R_lin_field_t01'])} | "
            f"{fmt_inf(sm['R_lin_field_t02'])} | {fmt_inf(sm['R_lin_field_late_mean'])} | "
            f"{fmt_inf(sm['t_half'])} | {fmt_inf(sm['t_leak'])} | "
            f"{fmt_inf(sm['leak_S_t02'])} | {fmt_inf(sm['leak_S_late_mean'])} |"
        )

    pair_lines = []
    for s in SEEDS:
        sm = by_seed[s]["summary"]
        if sm.get("pair_sep_available"):
            pairs = ", ".join(
                f"t={t:.2f}:{v:.4g}" for t, v in zip(sm["pair_sep_times"], sm["pair_sep_values"])
            )
            pair_lines.append(f"- seed {s}: {pairs}")
        else:
            pair_lines.append(f"- seed {s}: omitido (blobs não encontráveis após o critério run 30)")

    analysis = (
        "# Q04 — Análise (linearidade efetiva / superposição)\n\n"
        "**Desvio (declarado no PROTOCOL, não escondido):** o blueprint Q04 pede "
        "R_lin após projetar num subespaço efetivo Π. Q03 late/atrator não tem "
        "subespaço compartilhado de posto baixo "
        "(EV8=0.409447, Rec8=0.768507, overlap φ₀ entre seeds=0.046794). "
        "Π_POD late não é espaço de estados; projetar nele tornaria R_lin sem sentido. "
        "Q04 mede linearidade no campo com ruído FDT idêntico no triple, e vazamento "
        "do plano pré-declarado Π₀=span{G_A,G_B} (as duas gaussianas; 1 gaussiana = 1 átomo). "
        "A fórmula do blueprint é reportada com Π=Π₀. "
        "Não se usa o POD late de Q03. Não se muda Theta_core. Não se isolam termos. "
        "Não se retoca kT.\n\n"
        "Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.\n"
        "Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.\n"
        "Theta_core intocado (Q00). Sem cherry-pick de seed ou de janela.\n"
        f"Backend **{backend}**, campo complex64, memória float32. N_num, não física.\n"
        "Snapshots são sensores. **Não** controlam o solver.\n"
        "Este lote **não** é SUPPORTED para MQ.\n\n"
        "## Pergunta\n\n"
        "Existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B) na dinâmica completa? "
        "Por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?\n\n"
        "## Setup\n\n"
        "- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0\n"
        "- L=32.0, N=64, dt=0.0025, T=8.0, y_j(0)=0, V_ext=0\n"
        f"- CI: A gaussiana em x=-3; B em x=+3; s=0.5; k0=0; S=(A+B)/||A+B||; a=b={grid['a']:.8g}\n"
        f"- ||A+B||_L2 = {grid['norm_ab']:.8g}; checagem R_lin_field(t=0) analítica = {grid['rlin0_check']:.6e}\n"
        "- Π₀ = Gram-Schmidt complexo de {A(0), B(0)}; declarado antes; não é POD de Q03\n"
        "- FDT idêntico no triple: rng = default_rng(seed) independente por membro\n"
        "- seeds 0, 1 nessa ordem; complex64/float32; Strang Q02\n"
        "- sensores a cada 8 passos (Δt=0.02), 401/membro; 6 evoluções sequenciais\n"
        f"- PROTOCOL SHA-256: `{protocol_sha}`\n"
        f"- solver executado SHA-256: `{solver_sha}`\n"
        f"- Q02 passo SHA-256: `{Q02_SOLVER_SHA}`\n"
        f"- Q03 PROTOCOL SHA-256: `{Q03_PROTOCOL_SHA}`\n"
        f"- canônico Q00: `{CANONICAL_SHA}`\n"
        f"- início (America/Sao_Paulo): {started}\n"
        f"- fim (America/Sao_Paulo): {finished}\n"
        f"- wall total: {wall_total:.2f} s\n"
        f"- device: {device_s}\n"
        f"- backend: {backend}\n\n"
        "## Por seed\n\n"
        "| seed | finito | R_lin(0) | R_lin(0.02) | R_lin(0.10) | R_lin(0.20) | R_lin late | t_1/2 | t_leak | leak_S(0.2) | leak_S late |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        + "\n".join(seed_lines)
        + "\n\n"
        "## pair_sep (somente S; espírito run 30)\n\n"
        + "\n".join(pair_lines)
        + "\n\n"
        "Se os dois blobs não são encontráveis, pair_sep é omitido. Não se inventa.\n\n"
        "## Médias sobre seeds finitas (oficial = late)\n\n"
        f"- n_finite = {n_finite} / 2\n"
        f"- R_lin_field t=0: {fmt_inf(rlin_t0)}\n"
        f"- R_lin_field t=0.02: {fmt_inf(rlin_t002)}\n"
        f"- R_lin_field t=0.10: {fmt_inf(rlin_t01)}\n"
        f"- R_lin_field t=0.20: {fmt_inf(rlin_t02)}\n"
        f"- R_lin_field late (t≥6.4): {fmt_inf(rlin_late)}\n"
        f"- t_half (média das seeds com t finito; inf se nenhuma): {fmt_inf(t_half_mean)}\n"
        f"- t_leak (idem): {fmt_inf(t_leak_mean)}\n"
        f"- leak_S t=0.20: {fmt_inf(leak_s_t02)}\n"
        f"- leak_S late: {fmt_inf(leak_s_late)}\n\n"
        "Números early são CONTEXTO / vida útil. **Não** definem o veredito oficial "
        "e **não** promovem o par a qubit.\n\n"
        "## Veredito\n\n"
        f"- n_finite = {n_finite} / 2; seeds não finitas / blowup = {n_seed_blow}\n"
        f"- oficial (média late R_lin_field) = {fmt_inf(rlin_late)} → **{verdict}**\n"
        f"- supported_for_qm = false (nunca SUPPORTED para MQ)\n\n"
        f"{verdict_why}\n\n"
        "Regras (pré-declaradas, não movidas): late <0.20 → PARTIAL; late >0.50 → "
        "NOT_SUPPORTED; senão INCONCLUSIVE; >1/2 blowup → NUMERICAL_FAILURE. "
        "Early não define o veredito oficial. Nunca SUPPORTED para MQ.\n\n"
        "## Notas\n\n"
        "- Sem comparação MQ.\n"
        "- Theta_core intocado.\n"
        f"- Backend {backend} (fallback numpy fp32 só se mlx falhar; registrado).\n"
        "- Sem Simulações run 35.\n"
        "- Caixa preenchida = universo.\n"
        "- Π = plano dos 2 átomos (CI), não POD late de Q03.\n"
        "- a, b e as janelas não foram movidos depois de ver R_lin.\n"
    )
    (OUT / "analysis.md").write_text(analysis, encoding="utf-8")
    (TMP_ROOT / "analysis.md").write_text(analysis, encoding="utf-8")

    result = {
        "question": "Existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B) na dinâmica completa? Por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?",
        "id": "Q04",
        "verdict": verdict,
        "verdict_why": verdict_why,
        "qm_comparison": False,
        "theta_core_unchanged": True,
        "terms_isolated": False,
        "deviation": True,
        "pi": "IC_atom_plane_not_Q03_POD",
        "n_seeds": 2,
        "n_finite": n_finite,
        "n_blowup": n_seed_blow,
        "excluded_seeds": [s for s in SEEDS if s not in finite_seeds],
        "R_lin_field_late_mean": jsonable(rlin_late),
        "R_lin_field": {
            "t0": jsonable(rlin_t0),
            "t0.02": jsonable(rlin_t002),
            "t0.10": jsonable(rlin_t01),
            "t0.20": jsonable(rlin_t02),
            "late": jsonable(rlin_late),
        },
        "t_half": jsonable(t_half_mean) if math.isfinite(t_half_mean) else None,
        "t_half_raw": {str(s): jsonable(by_seed[s]["summary"]["t_half"]) if math.isfinite(by_seed[s]["summary"]["t_half"]) else None for s in SEEDS},
        "t_leak": jsonable(t_leak_mean) if math.isfinite(t_leak_mean) else None,
        "t_leak_raw": {str(s): jsonable(by_seed[s]["summary"]["t_leak"]) if math.isfinite(by_seed[s]["summary"]["t_leak"]) else None for s in SEEDS},
        "leak_S_late": jsonable(leak_s_late),
        "leak_S_t0.20": jsonable(leak_s_t02),
        "a": grid["a"],
        "b": grid["b"],
        "norm_AB": grid["norm_ab"],
        "R_lin_field_t0_analytic_check": grid["rlin0_check"],
        "per_seed": {str(s): jsonable(by_seed[s]["summary"]) for s in SEEDS},
        "backend": backend,
        "precision": PRECISION,
        "device": device_s,
        "protocol_sha256": protocol_sha,
        "solver_sha256": solver_sha,
        "canonical_sha256": CANONICAL_SHA,
        "q02_solver_sha256": Q02_SOLVER_SHA,
        "q03_protocol_sha256": Q03_PROTOCOL_SHA,
        "q02_protocol_v2_sha256": Q02_PROTOCOL_V2_SHA,
        "supported_for_qm": False,
        "pilots_1_34_confirmatory": False,
        "started_america_sao_paulo": started,
        "finished_america_sao_paulo": finished,
        "wall_total_s": wall_total,
        "workers": 1,
        "windows": {"early_context": "t=0.02,0.10,0.20", "late": "t>=6.4"},
        "identical_noise": True,
        "theta_core": {
            "hbar": HBAR, "m": M_MASS, "Lambda": LAMBDA, "alpha": ALPHA,
            "sigma": SIGMA_FRAC, "Gamma": GAMMA, "nu": list(NU), "lambda": list(LAM),
            "fdt_couple": FDT_COUPLE, "kT": KT, "D": D_DIM, "bc": BC, "step_mode": STEP_MODE,
        },
    }
    with (OUT / "result.json").open("w") as f:
        json.dump(jsonable(result), f, indent=2)
    with (TMP_ROOT / "result.json").open("w") as f:
        json.dump(jsonable(result), f, indent=2)

    config = {
        "question": "Q04",
        "title": "linearidade efetiva / superposição (campo + plano dos 2 átomos)",
        "canonical": "TRIAD_QM_CANONICAL_V1",
        "canonical_sha256": CANONICAL_SHA,
        "qm_comparison": False,
        "isolate_terms": False,
        "theta_core_frozen": True,
        "pilots_1_34_confirmatory": False,
        "technical_exclusion": "NaN/blowup only",
        "supported_for_qm": False,
        "protocol": "PROTOCOL.md",
        "protocol_sha256": protocol_sha,
        "deviation": True,
        "pi": "IC_atom_plane_not_Q03_POD",
        "theta_core": result["theta_core"],
        "box": {"L": LBOX, "N": NGRID, "dt": DT, "T": T_FINAL, "V_ext": V_EXT, "domain": "[-L/2, L/2)^3"},
        "initial_condition": {
            "type": "two_atom_gaussians_and_equal_superposition",
            "s": INIT_SIGMA,
            "A": {"center": list(CENTER_A), "k0": list(INIT_K0), "norm": 1.0},
            "B": {"center": list(CENTER_B), "k0": list(INIT_K0), "norm": 1.0},
            "S": "(A+B)/||A+B||_L2",
            "a": grid["a"],
            "b": grid["b"],
            "y0": Y0,
            "note": "1 gaussiana = 1 átomo; posições ±3 e s=0.5 da ontologia / run 30; não é scan",
        },
        "fdt": {
            "f_FDT_e": "2*Gamma*(dx**3)*kT/hbar",
            "increment": "spec eq 4",
            "rng": "numpy.random.default_rng(seed) independently per member; identical eta in the triple",
            "identical_noise": True,
        },
        "numerics": {
            "fp": "fp32",
            "precision": PRECISION,
            "memory": "float32",
            "backend": backend,
            "device": device_s,
            "solver": "standalone 3D Strang mlx GPU (mesmo passo Q02)",
            "memory_update": "euler",
            "snap_every": SNAP_EVERY,
            "n_snap": int(round(T_FINAL / DT)) // SNAP_EVERY + 1,
            "python": "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3",
            "workers": 1,
            "neural_engine": False,
        },
        "seeds": list(SEEDS),
        "members": list(MEMBERS),
        "windows": {
            "early_context": {"times": [0.02, 0.10, 0.20], "note": "contexto / vida útil; não veredito"},
            "late": {"rule": "last 20% of T", "t_min": T_LATE, "T": T_FINAL, "note": "oficial"},
        },
        "verdict_rule": {
            "gt_1_of_2_blowup": "NUMERICAL_FAILURE",
            "late_R_lin_field_lt_0.20": "PARTIAL",
            "late_R_lin_field_gt_0.50": "NOT_SUPPORTED",
            "otherwise": "INCONCLUSIVE",
            "early_does_not_set_official_verdict": True,
            "supported_for_qm": False,
            "no_aesthetic_drop": True,
        },
        "q02_solver_sha256": Q02_SOLVER_SHA,
        "q03_protocol_sha256": Q03_PROTOCOL_SHA,
        "q02_protocol_v2_sha256": Q02_PROTOCOL_V2_SHA,
        "solver_sha256": solver_sha,
        "executed": str(solver_src),
    }
    with (OUT / "config.json").open("w") as f:
        json.dump(config, f, indent=2)
    with (TMP_ROOT / "config.json").open("w") as f:
        json.dump(config, f, indent=2)

    q04md = (
        "---\n"
        "tags: [triad, qm, q04, linearidade]\n"
        "aliases: [Q04]\n"
        "status: active\n"
        "data: 2026-08-21\n"
        "---\n\n"
        "# Q04 — Linearidade efetiva / superposição\n\n"
        "Lote **Q04** (este diretório): seeds 0 e 1 (nessa ordem), triple A / B / S, "
        "tríade completa, N=64, dt=0.0025, T=8, L=32, Theta_core congelado. "
        "Linearidade no campo com ruído FDT idêntico; vazamento do plano "
        "Π₀=span{G_A,G_B} (1 gaussiana = 1 átomo). "
        "Snapshots são sensores; **não** controlam o solver.\n\n"
        f"Backend **{backend}**, campo complex64, memória float32. N_num, não calibração. "
        "**Nunca** SUPPORTED para MQ.\n\n"
        "Protocolo: [[PROTOCOL]]. Canônico: [[TRIAD_QM_CANONICAL_V1]] (Q00).\n"
        "Q03: [[Q03]] — INCONCLUSIVE (atrator sem subespaço compartilhado). "
        "Q02: [[Q02]] — INCONCLUSIVE.\n\n"
        "Pergunta: existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B) "
        "na dinâmica completa? Por quanto tempo a soma de dois átomos permanece "
        "no plano dos dois átomos?\n"
        "Sem comparação com MQ. Sem isolar termos. Sem cherry-pick. "
        "Pilotos 1–34 não confirmatórios.\n\n"
        f"SHA-256 PROTOCOL: `{protocol_sha}`\n"
        f"SHA-256 do solver executado `code/run_q04.py`: `{solver_sha}`\n"
        f"SHA-256 passo Q02: `{Q02_SOLVER_SHA}`\n"
        f"SHA-256 PROTOCOL Q03: `{Q03_PROTOCOL_SHA}`\n"
        f"SHA-256 canônico Q00: `{CANONICAL_SHA}`\n\n"
        f"Desvio: Π = plano dos 2 átomos (CI), **não** POD late de Q03 "
        "(EV8=0.409, Rec8=0.769, overlap φ₀=0.047). Ver [[PROTOCOL]].\n\n"
        f"Veredito Q04 (oficial = média late de R_lin campo, t≥6.4): **{verdict}**. "
        "Early só contexto / vida útil (não promove o par a qubit). "
        "Q04 **não** é teste de MQ. Nunca SUPPORTED para MQ. "
        "Detalhe em [[analysis]] e `result.json`.\n\n"
        f"Início {started}; fim {finished}; wall {wall_total:.2f} s (1 GPU, sequencial).\n"
    )
    (OUT / "Q04.md").write_text(q04md, encoding="utf-8")
    (TMP_ROOT / "Q04.md").write_text(q04md, encoding="utf-8")

    sum_path = OUT / "SHA256SUMS.txt"
    lines = []
    candidates = []
    for p in (
        proto,
        solver_src,
        OUT / "result.json",
        OUT / "analysis.md",
        OUT / "config.json",
        OUT / "Q04.md",
    ):
        if p is not None and p.is_file():
            candidates.append(p)
    for p in sorted((OUT / "figures").glob("*.png")):
        candidates.append(p)
    for p in sorted(raw_dir.glob("seed*_summary.json")):
        candidates.append(p)
    for p in sorted(raw_dir.glob("seed*_rlin.csv")):
        candidates.append(p)
    for p in sorted(raw_dir.glob("seed*_metrics.csv")):
        candidates.append(p)
    seen = set()
    for p in candidates:
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        lines.append(f"{sha256_file(p)}  {p}")
    sum_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (TMP_ROOT / "SHA256SUMS.txt").write_text(sum_path.read_text(encoding="utf-8"), encoding="utf-8")

    copy_into_vault(solver_src)

    print(
        "Q04_DONE",
        "verdict", verdict,
        "R_lin_late", rlin_late,
        "R_lin_0", rlin_t0,
        "R_lin_0.02", rlin_t002,
        "R_lin_0.10", rlin_t01,
        "R_lin_0.20", rlin_t02,
        "t_half", t_half_mean,
        "t_leak", t_leak_mean,
        "leak_S_late", leak_s_late,
        "n_finite", n_finite,
        "backend", backend,
        "wall", wall_total,
        flush=True,
    )


if __name__ == "__main__":
    main()
