#!/usr/bin/env python3
"""Run 35 — singularidade finita (janela cedo T=1).

NÃO é Q05. NÃO é teste de MQ. Leitura operacional:
  1 gaussiana = 1 átomo
  volume preenchido = universo
  singularidade = pico finito (o ponto brilhante)
  Anti-colapso: Λ puxa, memória empurra, peak nunca Inf.

Passo Strang idêntico a Q02 code/run_q02.py
  SHA-256 ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365

Pergunta: enquanto o pico é finito, ele aperta (menos células, peak sobe),
espalha (mais células), ou some no universo?

Seed=0 only. Sem cherry-pick. Sem comparação MQ. Sem isolar termos.
Theta_core intocado. kT=1 intocado. T=1 (não estender).
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
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
FONTES = VAULT / "Fontes"
ARTEFATOS = VAULT / "Artefatos" / "triad_singularidade_35"
NOTA_PATH = VAULT / "Simulações" / "35 singularidade_finita.md"
INDEX_PATH = VAULT / "Simulações" / "Índice de runs.md"
TRIAD_MD = VAULT / "TRIAD.md"
TMP_ROOT = Path("/tmp/run35_sing")
OUT = TMP_ROOT / "out"
Q02_PATH = VAULT / "QM" / "Q02_ensemble" / "code" / "run_q02.py"
Q02_SOLVER_SHA = "ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365"
CANONICAL_SHA = "e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e"

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

# --- N_num / caixa ---
LBOX = 32.0
NGRID = 64
DT = 0.0025
T_FINAL = 1.0
SEED = 0
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
CENTER_A = (-3.0, 0.0, 0.0)
CENTER_B = (3.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 2  # Δt = 0.005
K_CUT_FACTOR = 1.0
PRECISION = "complex64"
DTYPE_PSI_NP = np.complex64
DTYPE_R_NP = np.float32
BOX_HALF = LBOX / 2.0
POINT_GONE_NCELLS = 200
POINT_GONE_RRMS = 0.9 * BOX_HALF  # 14.4
PRINT_EVERY_T = 0.2
STRIP_TIMES = (0.0, 0.02, 0.05, 0.10, 0.20, 0.40)
PEAK_FRAC_BLOB = 0.20
MIN_DIST_ATOM = 2.0 * INIT_SIGMA
NMS_CAP = 48
ISO_FRAC = 0.35

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


def gaussian_atom(X, Y, Z, center, s, dV):
    """Uma gaussiana normalizada, como Q04."""
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    rr2 = dx * dx + dy * dy + dz * dz
    psi = np.exp(-rr2 / (2.0 * s * s)).astype(np.complex128)
    nrm = np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    psi = psi / nrm
    return psi


def peak_structure(rho, dx):
    peak = float(rho.max())
    if not np.isfinite(peak) or peak <= 0.0:
        return {
            "peak_n_cells_half": 0,
            "peak_width_phys": 0.0,
            "artifact_1_2_cells": True,
        }
    n_cells = int((rho >= 0.5 * peak).sum())
    r_cells = float((3.0 * n_cells / (4.0 * np.pi)) ** (1.0 / 3.0))
    return {
        "peak_n_cells_half": n_cells,
        "peak_width_phys": r_cells * dx,
        "artifact_1_2_cells": n_cells <= 2,
    }


def find_pair_sep(rho, dx, box):
    """Espírito Q04 / run 30: máximos locais; pair_sep só se n_det==2."""
    try:
        from scipy.ndimage import maximum_filter
    except Exception:
        return None, None
    peak = float(rho.max()) if rho.size else 0.0
    if (not np.isfinite(peak)) or peak <= 0.0:
        return None, None
    footprint = maximum_filter(rho, size=3, mode="wrap")
    is_max = (rho == footprint) & (rho >= PEAK_FRAC_BLOB * peak)
    coords = np.argwhere(is_max)
    n_raw = int(coords.shape[0])
    if n_raw == 0 or n_raw > NMS_CAP:
        return (int(n_raw) if n_raw else 0), None
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
        return int(n_det), None
    p0 = xyz[keep[0]]
    p1 = xyz[keep[1]]
    sep = float(np.linalg.norm(min_image(p0 - p1, box)))
    return int(n_det), sep


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
    """Fallback numpy fp32 / complex64 (mesma classe; NÃO fp64)."""
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


def record_metrics(psi, y, t, dV, dx, r2, want_blobs):
    rho = np.abs(psi) ** 2
    finite = bool(np.isfinite(rho).all() and np.isfinite(y).all())
    if not finite:
        rec = {
            "t": t,
            "norm": float("nan"),
            "peak": float("nan"),
            "PR": float("nan"),
            "R_rms": float("nan"),
            "peak_n_cells_half": 0,
            "peak_width_phys": float("nan"),
            "artifact_1_2_cells": True,
            "finite": False,
        }
        if want_blobs:
            rec["n_det"] = ""
            rec["pair_sep"] = ""
        return rho, rec
    norm = float(rho.sum() * dV)
    peak = float(rho.max())
    pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
    rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
    struct = peak_structure(rho, dx)
    rec = {
        "t": t,
        "norm": norm,
        "peak": peak,
        "PR": pr,
        "R_rms": rrms,
        "finite": True,
    }
    rec.update(struct)
    if want_blobs:
        n_det, sep = find_pair_sep(rho, dx, LBOX)
        rec["n_det"] = n_det if n_det is not None else ""
        rec["pair_sep"] = sep if sep is not None else ""
    return rho, rec


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
    # 1atom: Q00 IC / um ponto no origem
    g1 = gaussian_atom(X, Y, Z, (0.0, 0.0, 0.0), INIT_SIGMA, dV)
    # 2atom: Q04 A, B depois S=(A+B)/||A+B||
    ga = gaussian_atom(X, Y, Z, CENTER_A, INIT_SIGMA, dV)
    gb = gaussian_atom(X, Y, Z, CENTER_B, INIT_SIGMA, dV)
    sab = ga + gb
    gs = sab / l2_norm(sab, dV)
    ics = {
        "1atom": g1.astype(DTYPE_PSI_NP),
        "2atom": gs.astype(DTYPE_PSI_NP),
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
        "y0": np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R_NP),
        "shape": (N, N, N),
        "norm_1atom": l2_norm(g1, dV),
        "norm_2atom": l2_norm(gs, dV),
        "norm_A": l2_norm(ga, dV),
        "norm_B": l2_norm(gb, dV),
    }


def nearest_record_step(t_target):
    step = int(round(t_target / DT))
    # snap to even steps (record every 2) except exact 0
    if step % RECORD_EVERY != 0:
        step = int(round(step / RECORD_EVERY) * RECORD_EVERY)
    return step


def run_ic(name, grid, backend):
    t_wall0 = time.perf_counter()
    N = NGRID
    dx = grid["dx"]
    dV = grid["dV"]
    r2 = grid["r2"]
    noise_amp = grid["noise_amp"]
    f_FDT = grid["f_FDT"]
    shape = grid["shape"]
    psi0 = grid["ics"][name]
    y0 = grid["y0"]
    n_steps = int(round(T_FINAL / DT))
    want_blobs = name == "2atom"
    rng = np.random.default_rng(SEED)
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
        device = str(mx.default_device())
    else:
        half_lin = grid["half_lin"]
        nu = nu_np
        lam = lam_np
        psi = psi0.copy()
        y = y0.copy()
        step_fn = strang_step_np
        device = "cpu"

    print(
        f"=== 35 {name} N={N} backend={backend} {PRECISION} device={device} ===",
        flush=True,
    )
    print(
        f"{name} L {LBOX} dx {dx} dt {DT} T {T_FINAL} n_steps {n_steps} "
        f"record_every {RECORD_EVERY} f_FDT {f_FDT} noise_amp {noise_amp} seed={SEED}",
        flush=True,
    )

    strip_steps = {nearest_record_step(t): t for t in STRIP_TIMES}
    metrics = []
    midplanes = {}
    rho_t0 = None
    rho_at_peak = None
    t_at_saved_peak = None
    blew = False
    blow_t = None
    peak_max = float("-inf")
    peak_max_t = None
    last_print_bucket = -1

    for step in range(n_steps + 1):
        t = step * DT
        if step % RECORD_EVERY == 0 or step == n_steps:
            if backend == "mlx":
                psi_np = np.array(psi)
                y_np = np.array(y)
            else:
                psi_np = np.asarray(psi)
                y_np = np.asarray(y)
            rho, rec = record_metrics(psi_np, y_np, t, dV, dx, r2, want_blobs)
            rec["ic"] = name
            rec["seed"] = SEED
            rec["N"] = N
            rec["dx"] = dx
            rec["backend"] = backend
            metrics.append(rec)
            if rec["finite"] and np.isfinite(rec["peak"]) and rec["peak"] > peak_max:
                peak_max = float(rec["peak"])
                peak_max_t = float(t)
                rho_at_peak = rho.astype(np.float32, copy=True)
                t_at_saved_peak = float(t)
            if step == 0:
                rho_t0 = rho.astype(np.float32, copy=True)
            if step in strip_steps:
                midplanes[float(strip_steps[step])] = np.abs(psi_np[:, :, N // 2]).astype(
                    np.float32
                )
            bucket = int(t // PRINT_EVERY_T)
            if bucket != last_print_bucket or step == n_steps or (not rec["finite"]):
                last_print_bucket = bucket
                extra = ""
                if want_blobs:
                    extra = f" n_det={rec.get('n_det')} sep={rec.get('pair_sep')}"
                print(
                    f"{name} t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
                    f"PR={rec['PR']:.6e} Rrms={rec['R_rms']:.6e} "
                    f"n_cells={rec['peak_n_cells_half']} finite={rec['finite']}{extra}",
                    flush=True,
                )
            if (not rec["finite"]) or (
                np.isfinite(rec.get("peak", float("nan")))
                and abs(rec["peak"]) > 1.0e30
            ):
                blew = True
                blow_t = t
                print("BLOWUP_OR_NAN", name, "t", t, flush=True)
                break
        if step == n_steps or blew:
            break
        psi, y = step_fn(psi, y, half_lin, noise_amp, rng, nu, lam, shape)

    wall = time.perf_counter() - t_wall0
    derived = derive_ic(name, metrics, peak_max, peak_max_t, blew, blow_t, wall, backend, device)
    print(
        f"{name} done wall_s={wall:.3f} finite={derived['finite_all']} "
        f"peak_max={derived['peak_max']} t_at_peak_max={derived['t_at_peak_max']} "
        f"t_point_gone={derived['t_point_gone']} sharpened={derived['sharpened']}",
        flush=True,
    )
    return {
        "name": name,
        "metrics": metrics,
        "derived": derived,
        "midplanes": midplanes,
        "rho_t0": rho_t0,
        "rho_at_peak": rho_at_peak,
        "t_at_saved_peak": t_at_saved_peak,
        "wall_s": wall,
        "backend": backend,
        "device": device,
    }


def derive_ic(name, metrics, peak_max, peak_max_t, blew, blow_t, wall, backend, device):
    if not metrics:
        return {
            "ic": name,
            "finite_all": False,
            "any_nan": True,
            "blew_up": True,
            "blow_t": blow_t,
            "peak_max": None,
            "t_at_peak_max": None,
            "t_point_gone": None,
            "t_point_gone_label": "never in T=1 (sem registros)",
            "sharpened": False,
            "delta_peak": None,
            "delta_n_cells": None,
            "n_cells_t0": None,
            "n_cells_t_peak": None,
            "peak_t0": None,
            "finite_singularity": "NOT_SUPPORTED",
            "wall_s": wall,
            "backend": backend,
            "device": device,
        }
    t0 = metrics[0]
    peak_t0 = t0.get("peak")
    n0 = t0.get("peak_n_cells_half")
    rec_peak = None
    for m in metrics:
        if peak_max_t is not None and abs(float(m["t"]) - float(peak_max_t)) < 1e-12:
            rec_peak = m
            break
    if rec_peak is None:
        rec_peak = max(
            (m for m in metrics if m.get("finite") and np.isfinite(m.get("peak", float("nan")))),
            key=lambda m: m["peak"],
            default=t0,
        )
        peak_max = rec_peak.get("peak")
        peak_max_t = rec_peak.get("t")
    n_peak = rec_peak.get("peak_n_cells_half")
    dpeak = None
    dn = None
    if (
        peak_t0 is not None
        and np.isfinite(peak_t0)
        and peak_max is not None
        and np.isfinite(peak_max)
    ):
        dpeak = float(peak_max) - float(peak_t0)
    if n0 is not None and n_peak is not None:
        dn = int(n_peak) - int(n0)

    t_gone = None
    for m in metrics:
        nc = m.get("peak_n_cells_half")
        rr = m.get("R_rms")
        ok_nc = nc is not None and np.isfinite(nc) and int(nc) > POINT_GONE_NCELLS
        ok_rr = rr is not None and np.isfinite(rr) and float(rr) > POINT_GONE_RRMS
        if ok_nc or ok_rr:
            t_gone = float(m["t"])
            break
    t_gone_label = f"{t_gone:.6g}" if t_gone is not None else "never in T=1"

    # sharpening only inside [0, t_point_gone] (or whole T if never)
    window_end = t_gone if t_gone is not None else T_FINAL
    window = [m for m in metrics if float(m["t"]) <= window_end + 1e-15]
    sharpened = False
    if (
        dpeak is not None
        and dn is not None
        and peak_max_t is not None
        and float(peak_max_t) <= window_end + 1e-15
        and dpeak > 0.0
        and dn < 0
    ):
        sharpened = True
    # also: did peak rise and n_cells fall anywhere 0 → t_at_peak_max
    # (already the definition)

    any_nan = any(not m.get("finite", False) for m in metrics)
    finite_all = (not any_nan) and (not blew) and all(m.get("finite") for m in metrics)
    peak_ok = (
        peak_max is not None
        and np.isfinite(peak_max)
        and peak_t0 is not None
        and np.isfinite(peak_t0)
        and (not any_nan)
        and float(peak_max) > float(peak_t0)
    )
    fs = "SUPPORTED" if peak_ok else "NOT_SUPPORTED"

    last = metrics[-1]
    out = {
        "ic": name,
        "finite_all": bool(finite_all),
        "any_nan": bool(any_nan),
        "blew_up": bool(blew),
        "blow_t": blow_t,
        "peak_max": float(peak_max) if peak_max is not None and np.isfinite(peak_max) else None,
        "t_at_peak_max": float(peak_max_t) if peak_max_t is not None else None,
        "t_point_gone": t_gone,
        "t_point_gone_label": t_gone_label,
        "sharpened": bool(sharpened),
        "delta_peak": dpeak,
        "delta_n_cells": dn,
        "n_cells_t0": int(n0) if n0 is not None else None,
        "n_cells_t_peak": int(n_peak) if n_peak is not None else None,
        "peak_t0": float(peak_t0) if peak_t0 is not None and np.isfinite(peak_t0) else None,
        "peak_width_t0": t0.get("peak_width_phys"),
        "peak_width_t_peak": rec_peak.get("peak_width_phys"),
        "norm_t0": t0.get("norm"),
        "norm_final": last.get("norm"),
        "peak_final": last.get("peak"),
        "PR_t0": t0.get("PR"),
        "PR_final": last.get("PR"),
        "R_rms_t0": t0.get("R_rms"),
        "R_rms_final": last.get("R_rms"),
        "artifact_t0": t0.get("artifact_1_2_cells"),
        "artifact_t_peak": rec_peak.get("artifact_1_2_cells"),
        "finite_singularity": fs,
        "n_records": len(metrics),
        "wall_s": wall,
        "backend": backend,
        "device": device,
        "supported_for_qm": False,
    }
    if name == "2atom":
        # first / last n_det if present
        ndets = []
        seps = []
        for m in metrics:
            nd = m.get("n_det")
            if nd != "" and nd is not None:
                try:
                    ndets.append((float(m["t"]), int(nd)))
                except Exception:
                    pass
            sep = m.get("pair_sep")
            if sep != "" and sep is not None:
                try:
                    seps.append((float(m["t"]), float(sep)))
                except Exception:
                    pass
        out["n_det_t0"] = ndets[0][1] if ndets else None
        out["n_det_series_head"] = ndets[:8] if ndets else []
        out["pair_sep_t0"] = seps[0][1] if seps else None
        out["pair_sep_last"] = seps[-1] if seps else None
        out["n_times_exactly_2"] = sum(1 for _, n in ndets if n == 2)
    return out


def series(metrics, key):
    out = []
    for m in metrics:
        v = m.get(key, "")
        if v == "" or v is None:
            out.append(np.nan)
        else:
            try:
                out.append(float(v))
            except Exception:
                out.append(np.nan)
    return np.asarray(out, dtype=np.float64)


def setup_3d_box(ax, box):
    h = box / 2.0
    ax.set_xlim(-h, h)
    ax.set_ylim(-h, h)
    ax.set_zlim(-h, h)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")


def plot_iso_scatter(ax, rho, level, dx, box, color="#c05621"):
    mask = rho >= level
    ii = np.argwhere(mask)
    if ii.shape[0] == 0:
        setup_3d_box(ax, box)
        return "empty"
    if ii.shape[0] > 8000:
        rng = np.random.default_rng(0)
        ii = ii[rng.choice(ii.shape[0], 8000, replace=False)]
    xyz = ii.astype(np.float64) * dx - box / 2.0
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=6, c=color, alpha=0.35, depthshade=False)
    setup_3d_box(ax, box)
    return "scatter"


def make_figures(out: Path, results: dict, grid: dict):
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    dx = grid["dx"]
    paths = {}

    # --- peak_vs_t ---
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    colors = {"1atom": "#b45309", "2atom": "#1d4ed8"}
    labels = {"1atom": "1 ponto (origem)", "2atom": "2 pontos (x=±3)"}
    for name in ("1atom", "2atom"):
        mets = results[name]["metrics"]
        t = series(mets, "t")
        pk = series(mets, "peak")
        ax.plot(t, pk, color=colors[name], lw=1.7, label=labels[name])
        tp = results[name]["derived"].get("t_at_peak_max")
        pm = results[name]["derived"].get("peak_max")
        if tp is not None and pm is not None:
            ax.axvline(tp, color=colors[name], ls="--", lw=0.9, alpha=0.7)
            ax.scatter([tp], [pm], color=colors[name], s=36, zorder=4)
            ax.annotate(
                f"t_peak={tp:.4g}",
                xy=(tp, pm),
                xytext=(6, 8 if name == "1atom" else -14),
                textcoords="offset points",
                fontsize=8,
                color=colors[name],
            )
    ax.set_xlabel("t")
    ax.set_ylabel("peak ρ  (ρ_max)")
    ax.set_title("singularidade finita — pico vs t  (T=1, seed=0)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    p = fig_dir / "peak_vs_t.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    paths["peak_vs_t"] = p

    # --- width_vs_t ---
    fig, axes = plt.subplots(2, 1, figsize=(9.2, 6.6), sharex=True)
    for name in ("1atom", "2atom"):
        mets = results[name]["metrics"]
        t = series(mets, "t")
        axes[0].plot(
            t, series(mets, "peak_n_cells_half"), color=colors[name], lw=1.6, label=labels[name]
        )
        axes[1].plot(
            t, series(mets, "peak_width_phys"), color=colors[name], lw=1.6, label=labels[name]
        )
        tg = results[name]["derived"].get("t_point_gone")
        if tg is not None:
            axes[0].axvline(tg, color=colors[name], ls=":", lw=0.9, alpha=0.7)
            axes[1].axvline(tg, color=colors[name], ls=":", lw=0.9, alpha=0.7)
    axes[0].axhline(POINT_GONE_NCELLS, color="0.45", ls="--", lw=0.8, label="limiar 200 células")
    axes[0].set_ylabel("n_células (ρ ≥ ½ peak)")
    axes[0].set_title("largura do pico — células acima de ½ peak")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend(fontsize=8)
    axes[1].set_ylabel("largura física  (3n/4π)^{1/3}·dx")
    axes[1].set_xlabel("t")
    axes[1].set_title("largura física do pico")
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("singularidade finita — o ponto no universo  (não estrela)")
    fig.tight_layout()
    p = fig_dir / "width_vs_t.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    paths["width_vs_t"] = p

    # --- peak_vs_width : plano (n_cells, peak) ---
    fig, ax = plt.subplots(figsize=(7.4, 6.2))
    ax.annotate(
        "aperta\n↑ peak, ← células",
        xy=(0.04, 0.96),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=8,
        color="#9a3412",
    )
    ax.annotate(
        "espalha\n↓ peak, → células",
        xy=(0.96, 0.04),
        xycoords="axes fraction",
        ha="right",
        va="bottom",
        fontsize=8,
        color="#1e3a5f",
    )
    for name in ("1atom", "2atom"):
        mets = results[name]["metrics"]
        nc = series(mets, "peak_n_cells_half")
        pk = series(mets, "peak")
        t = series(mets, "t")
        ax.plot(nc, pk, color=colors[name], lw=1.4, alpha=0.85, label=labels[name])
        ax.scatter(nc[0], pk[0], color=colors[name], s=42, marker="o", zorder=4)
        ax.annotate("t=0", xy=(nc[0], pk[0]), fontsize=7, color=colors[name], xytext=(5, 4), textcoords="offset points")
        tp = results[name]["derived"].get("t_at_peak_max")
        if tp is not None:
            i = int(np.argmin(np.abs(t - tp)))
            ax.scatter(nc[i], pk[i], color=colors[name], s=48, marker="*", zorder=5)
            ax.annotate(
                f"t_peak={tp:.4g}",
                xy=(nc[i], pk[i]),
                fontsize=7,
                color=colors[name],
                xytext=(6, -10),
                textcoords="offset points",
            )
    ax.set_xlabel("n_células (ρ ≥ ½ peak)")
    ax.set_ylabel("peak ρ")
    ax.set_title("trajetória (n_células, peak) — esquerda-cima = aperta, direita-baixo = espalha")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8, loc="upper right")
    fig.tight_layout()
    p = fig_dir / "peak_vs_width.png"
    fig.savefig(p, dpi=150)
    plt.close(fig)
    paths["peak_vs_width"] = p

    # --- strips ---
    x = grid["x"]
    extent = [float(x[0]), float(x[-1] + dx), float(x[0]), float(x[-1] + dx)]
    for name in ("1atom", "2atom"):
        mids = results[name]["midplanes"]
        fig, axes = plt.subplots(1, 6, figsize=(14.4, 2.85))
        for ax, tt in zip(axes, STRIP_TIMES):
            sl = mids.get(float(tt))
            if sl is None:
                # nearest
                keys = np.array(sorted(mids.keys()), dtype=np.float64)
                if keys.size:
                    sl = mids[float(keys[np.argmin(np.abs(keys - tt))])]
            if sl is None:
                ax.set_title(f"t={tt:g} (sem)")
                ax.axis("off")
                continue
            im = ax.imshow(
                sl.T,
                origin="lower",
                extent=extent,
                cmap="magma",
                aspect="equal",
            )
            ax.set_title(f"t={tt:g}", fontsize=9)
            ax.set_xlabel("x")
            if ax is axes[0]:
                ax.set_ylabel("y")
            else:
                ax.set_yticklabels([])
            fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        fig.suptitle(
            f"plano médio |Ψ| — {labels[name]}  (singularidade finita no universo)",
            fontsize=11,
        )
        fig.tight_layout()
        p = fig_dir / f"strip_{name}.png"
        fig.savefig(p, dpi=150)
        plt.close(fig)
        paths[f"strip_{name}"] = p

    # --- iso 1atom t=0 e t_peak ---
    r0 = results["1atom"]["rho_t0"]
    rp = results["1atom"]["rho_at_peak"]
    tp = results["1atom"]["derived"].get("t_at_peak_max")
    fig = plt.figure(figsize=(10.4, 5.0))
    for i, (rho, title) in enumerate(
        (
            (r0, "t=0  (IC, 1 ponto)"),
            (rp, f"t={tp:.4g}  (t_at_peak_max)" if tp is not None else "t_peak"),
        )
    ):
        ax = fig.add_subplot(1, 2, i + 1, projection="3d")
        if rho is None:
            ax.set_title(title + " (sem ρ)")
            continue
        peak = float(rho.max()) if rho.size else 0.0
        level = ISO_FRAC * peak if peak > 0 else 0.0
        used = plot_iso_scatter(ax, rho, level, dx, LBOX)
        ax.set_title(f"{title}\nρ≥{ISO_FRAC:.2f}·peak  peak={peak:.4g}  ({used})")
    fig.suptitle("1 ponto — singularidade finita no universo  (não estrela)")
    fig.tight_layout()
    p = fig_dir / "iso_1atom_t0_tpeak.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["iso_1atom_t0_tpeak"] = p
    return paths


def fmt_num(v, spec=".6g"):
    if v is None:
        return "—"
    if isinstance(v, bool):
        return "sim" if v else "não"
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    try:
        fv = float(v)
    except Exception:
        return str(v)
    if not np.isfinite(fv):
        return "—"
    return format(fv, spec)


def write_note(out: Path, results: dict, extra: dict, fig_rel="Artefatos/triad_singularidade_35"):
    d1 = results["1atom"]["derived"]
    d2 = results["2atom"]["derived"]
    m1 = results["1atom"]["metrics"]
    m2 = results["2atom"]["metrics"]

    def row_at(mets, t_want):
        if not mets:
            return None
        ts = np.array([float(m["t"]) for m in mets])
        return mets[int(np.argmin(np.abs(ts - t_want)))]

    times_show = [0.0, 0.02, 0.05, 0.10, 0.20, 0.40, 1.0]
    lines = []
    lines.append("---")
    lines.append("tags: [triad, simulação, solver, I0, singularidade]")
    lines.append("aliases: [triad_singularidade_35, singularidade_finita, run35]")
    lines.append("classe: spec §5 3D Strang (standalone), Theta_core, janela cedo")
    lines.append("diretório: triad_singularidade_35")
    lines.append("status: I0 / environment / singularidade finita")
    lines.append("run: 35")
    lines.append("data: 2026-08-21")
    lines.append("---")
    lines.append("")
    lines.append("# singularidade_finita")
    lines.append("")
    lines.append(
        "Equação TRIAD **completa**, Theta_core congelado (Q00 / [[TRIAD_QM_CANONICAL_V1]]). "
        "**I0 / environment**, não scan, **não** Q05, **não** teste de MQ. "
        "1 gaussiana = 1 [[átomo]]. Volume preenchido = universo. "
        "Leitura: **singularidade = pico finito** (o ponto brilhante). "
        "Anti-colapso: Λ puxa, memória empurra, peak nunca Inf. "
        "Pergunta deste run: **enquanto o pico é finito, ele aperta (menos células, peak sobe), "
        "espalha (mais células), ou some no universo?** "
        "[[Leitura operacional]] · [[Anti-colapso]] · [[átomo]]"
    )
    lines.append("")
    lines.append(
        "Solver: Strang 3D standalone, **mesmo passo** de [[Fontes/run_q02.py]] / Q02 "
        f"(`{Q02_SOLVER_SHA}`). Backend **{extra['backend']}** {PRECISION}. "
        "$V_{\\mathrm{ext}}=0$, $y_j(0)=0$, caixa periódica $[-L/2,L/2)^3$. Seed=0 (única; sem cherry-pick)."
    )
    lines.append("")
    lines.append("## IC — dois casos (seed=0)")
    lines.append("")
    lines.append(
        f"- **1atom**: uma gaussiana $s=0.5$ na origem, $\\int|\\Psi|^2=1$ (IC Q00 / um ponto). "
        f"t=0: peak={fmt_num(d1.get('peak_t0'))}, n_células={fmt_num(d1.get('n_cells_t0'))}, "
        f"PR={fmt_num(d1.get('PR_t0'))}, R_rms={fmt_num(d1.get('R_rms_t0'))}."
    )
    lines.append(
        f"- **2atom**: duas gaussianas $s=0.5$ em $x=\\pm 3$ (cada uma como Q04), "
        f"depois $S=(A+B)/\\|A+B\\|$, $\\int|S|^2=1$ (dois pontos, sep=6). "
        f"t=0: peak={fmt_num(d2.get('peak_t0'))}, n_células={fmt_num(d2.get('n_cells_t0'))}, "
        f"PR={fmt_num(d2.get('PR_t0'))}, R_rms={fmt_num(d2.get('R_rms_t0'))}"
        + (
            f", n_det={fmt_num(d2.get('n_det_t0'))}, pair_sep={fmt_num(d2.get('pair_sep_t0'))}"
            if d2.get("n_det_t0") is not None
            else ""
        )
        + "."
    )
    lines.append("")
    lines.append(f"![[{fig_rel}/strip_1atom.png]]")
    lines.append("")
    lines.append(f"![[{fig_rel}/strip_2atom.png]]")
    lines.append("")
    lines.append("## Parâmetros (Theta_core, intocado)")
    lines.append("")
    lines.append(
        "$\\Lambda=-10$, $\\alpha=0.15$, $\\sigma=1.5$, $\\Gamma=0.05$, "
        "$\\nu=(10, 0.5, 0.05)$, $\\lambda=(3, 1, 0.3)$, `fdt_couple=True`, **kT=1.0**. "
        f"$L=32$, $N=64$, $dt=0.0025$, **$T=1.0$** (janela cedo; pontos somem ~0.3 — "
        f"não estender T para “ver MQ”). seed=0. "
        f"$f_{{\\mathrm{{FDT}}}}={extra['f_FDT']}$, noise_amp $={extra['noise_amp']}$. "
        f"Memória Euler ($\\max\\nu\\cdot dt={extra['max_nu_dt']}$). "
        f"Registro a cada 2 passos ($\\Delta t=0.005$)."
    )
    lines.append("")
    lines.append(
        "Não substitui [[30 dois_atomos_gravidade]] · [[31 nested_gaussians]] · "
        "[[32 universo_atomo]] · [[33 ninho_pm]] · [[34 ninho_pm_long]] · Q00–Q04."
    )
    lines.append("")
    lines.append("## Resultado")
    lines.append("")
    lines.append(
        f"Wall total: **{extra['wall_total_s']:.3f} s** "
        f"({extra['started']} – {extra['finished']}, 21/08/2026). "
        f"Backend {extra['backend']} {extra['device']}. "
        f"{extra['n_steps']} passos × 2 ICs, {d1.get('n_records')} registros/IC. "
        f"Sem NaN, sem blowup."
        if (d1.get("finite_all") and d2.get("finite_all"))
        else f"Wall total: **{extra['wall_total_s']:.3f} s**. "
        f"finite 1atom={d1.get('finite_all')} 2atom={d2.get('finite_all')}."
    )
    lines.append("")
    lines.append("### 1atom — um ponto")
    lines.append("")
    lines.append(
        f"- peak_max = **{fmt_num(d1.get('peak_max'))}** em t_at_peak_max = **{fmt_num(d1.get('t_at_peak_max'))}**"
    )
    lines.append(
        f"- n_células (½ peak): t=0 → **{fmt_num(d1.get('n_cells_t0'))}**; "
        f"t_peak → **{fmt_num(d1.get('n_cells_t_peak'))}** "
        f"(Δn_células = {fmt_num(d1.get('delta_n_cells'))})"
    )
    lines.append(
        f"- Δpeak (t=0 → t_peak) = {fmt_num(d1.get('delta_peak'))}"
    )
    lines.append(
        f"- t_point_gone (n_células>200 ou R_rms>14.4) = **{d1.get('t_point_gone_label')}**"
    )
    lines.append(
        f"- aperta (peak sobe e n_células cai até t_peak, dentro da janela do ponto)? "
        f"**{'sim' if d1.get('sharpened') else 'não'}**"
    )
    lines.append(
        f"- finite_singularity: **{d1.get('finite_singularity')}** "
        f"(peak_max finito, sem NaN, peak_max > peak(t=0)). Nunca SUPPORTED para MQ."
    )
    lines.append("")
    lines.append("### 2atom — dois pontos")
    lines.append("")
    lines.append(
        f"- peak_max = **{fmt_num(d2.get('peak_max'))}** em t_at_peak_max = **{fmt_num(d2.get('t_at_peak_max'))}**"
    )
    lines.append(
        f"- n_células (½ peak): t=0 → **{fmt_num(d2.get('n_cells_t0'))}**; "
        f"t_peak → **{fmt_num(d2.get('n_cells_t_peak'))}** "
        f"(Δn_células = {fmt_num(d2.get('delta_n_cells'))})"
    )
    lines.append(
        f"- Δpeak (t=0 → t_peak) = {fmt_num(d2.get('delta_peak'))}"
    )
    lines.append(
        f"- t_point_gone = **{d2.get('t_point_gone_label')}**"
    )
    lines.append(
        f"- aperta? **{'sim' if d2.get('sharpened') else 'não'}**"
    )
    lines.append(
        f"- finite_singularity: **{d2.get('finite_singularity')}**. Nunca SUPPORTED para MQ."
    )
    if d2.get("n_det_t0") is not None:
        lines.append(
            f"- n_det t=0 = {fmt_num(d2.get('n_det_t0'))}; "
            f"vezes com exatamente 2 blobs = {fmt_num(d2.get('n_times_exactly_2'))}"
            + (
                f"; pair_sep t=0 = {fmt_num(d2.get('pair_sep_t0'))}"
                if d2.get("pair_sep_t0") is not None
                else " (pair_sep omitido quando n_det≠2)"
            )
        )
    lines.append("")
    lines.append("| IC | t | peak | n_células | largura | PR | R_rms | finite |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for ic, mets in (("1atom", m1), ("2atom", m2)):
        for tw in times_show:
            rec = row_at(mets, tw)
            if rec is None:
                continue
            lines.append(
                f"| {ic} | {fmt_num(rec.get('t'))} | {fmt_num(rec.get('peak'))} | "
                f"{fmt_num(rec.get('peak_n_cells_half'))} | {fmt_num(rec.get('peak_width_phys'))} | "
                f"{fmt_num(rec.get('PR'))} | {fmt_num(rec.get('R_rms'))} | "
                f"{'sim' if rec.get('finite') else 'não'} |"
            )
    lines.append("")
    lines.append(f"![[{fig_rel}/peak_vs_t.png]]")
    lines.append("")
    lines.append(f"![[{fig_rel}/width_vs_t.png]]")
    lines.append("")
    lines.append(f"![[{fig_rel}/peak_vs_width.png]]")
    lines.append("")
    lines.append(f"![[{fig_rel}/iso_1atom_t0_tpeak.png]]")
    lines.append("")
    lines.append("## O que os números sustentam")
    lines.append("")
    # reading from numbers only
    def reading(d):
        bits = []
        if d.get("finite_singularity") == "SUPPORTED":
            bits.append(
                f"pico máximo {fmt_num(d.get('peak_max'))} em t={fmt_num(d.get('t_at_peak_max'))}, "
                f"finito, maior que t=0 ({fmt_num(d.get('peak_t0'))})"
            )
        else:
            bits.append("peak_max não excedeu peak(t=0) ou houve NaN — finite_singularity não sustentada neste IC")
        if d.get("sharpened"):
            bits.append(
                f"aperta: Δpeak={fmt_num(d.get('delta_peak'))}, "
                f"Δn_células={fmt_num(d.get('delta_n_cells'))} (t=0 → t_peak)"
            )
        else:
            bits.append(
                f"não aperta no sentido declarado: Δpeak={fmt_num(d.get('delta_peak'))}, "
                f"Δn_células={fmt_num(d.get('delta_n_cells'))} (t=0 → t_peak)"
            )
        bits.append(f"t_point_gone = {d.get('t_point_gone_label')} (ponto perdido no universo preenchido)")
        return "; ".join(bits)

    lines.append(f"**1atom.** {reading(d1)}.")
    lines.append("")
    lines.append(f"**2atom.** {reading(d2)}.")
    lines.append("")
    lines.append(
        "Singularidade = pico finito. O ponto brilhante **não** é estrela nem planeta. "
        "Nunca SUPPORTED para MQ. kT=1 intocado. Theta_core intocado. "
        "Não se estendeu T para “ver MQ”."
    )
    lines.append("")
    lines.append("## CSVs")
    lines.append("")
    lines.append(f"- [[{fig_rel}/metrics_1atom.csv]]")
    lines.append(f"- [[{fig_rel}/metrics_2atom.csv]]")
    lines.append(f"- [[{fig_rel}/summary.json]]")
    lines.append("")
    lines.append("## Arquivos")
    lines.append("")
    lines.append(
        "`peak_vs_t.png` · `width_vs_t.png` · `peak_vs_width.png` · "
        "`strip_1atom.png` · `strip_2atom.png` · `iso_1atom_t0_tpeak.png` · "
        "metrics_1atom.csv · metrics_2atom.csv · summary.json · SHA256SUMS.txt"
    )
    lines.append("")
    lines.append("Script: [[Fontes/run_singularidade_35.py]]")
    lines.append("")
    lines.append("→ [[Índice de runs]] · [[TRIAD]] · [[Leitura operacional]] · [[Anti-colapso]] · [[átomo]]")
    lines.append("")
    text = "\n".join(lines) + "\n"
    (out / "35 singularidade_finita.md").write_text(text, encoding="utf-8")
    return text


def write_sha256sums(folder: Path):
    paths = []
    for p in sorted(folder.rglob("*")):
        if p.is_file() and p.name not in ("SHA256SUMS.txt", ".write_test"):
            paths.append(p)
    lines = []
    for p in paths:
        rel = p.relative_to(folder).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")
    (folder / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def csv_fields(name):
    fields = [
        "t",
        "norm",
        "peak",
        "PR",
        "R_rms",
        "peak_n_cells_half",
        "peak_width_phys",
        "artifact_1_2_cells",
        "finite",
        "ic",
        "seed",
        "N",
        "dx",
        "backend",
    ]
    if name == "2atom":
        fields[8:8] = ["n_det", "pair_sep"]
        # wait that inserts before finite - we want n_det, pair_sep after finite or with blobs
        # rebuild cleanly
        fields = [
            "t",
            "norm",
            "peak",
            "PR",
            "R_rms",
            "peak_n_cells_half",
            "peak_width_phys",
            "artifact_1_2_cells",
            "finite",
            "n_det",
            "pair_sep",
            "ic",
            "seed",
            "N",
            "dx",
            "backend",
        ]
    return fields


def patch_index(d1, d2):
    text = INDEX_PATH.read_text(encoding="utf-8")
    old_head = "34 diretórios, ordem do registro."
    new_head = (
        "35 diretórios, ordem do registro."
    )
    if old_head in text:
        text = text.replace(old_head, new_head, 1)
    extra = (
        " 35 = 21/08/2026, Theta_core I0 singularidade finita (T=1, 1 e 2 pontos)."
    )
    marker = "Título da nota = id do diretório."
    if extra.strip() not in text and marker in text:
        text = text.replace(marker, extra.strip() + " " + marker, 1)
    row34 = (
        "| 34 | [[34 ninho_pm_long|triad_ninho_pm_long]] |"
    )
    row35 = (
        f"| 35 | [[35 singularidade_finita|triad_singularidade_35]] | "
        f"Theta_core I0, 1 e 2 picos, N=64 T=1, 2026-08-21 | "
        f"singularidade finita | "
        f"1atom peak_max={fmt_num(d1.get('peak_max'))} t={fmt_num(d1.get('t_at_peak_max'))} "
        f"n_células {fmt_num(d1.get('n_cells_t0'))}→{fmt_num(d1.get('n_cells_t_peak'))} "
        f"t_gone={d1.get('t_point_gone_label')} "
        f"{'aperta' if d1.get('sharpened') else 'não aperta'}; "
        f"2atom peak_max={fmt_num(d2.get('peak_max'))} t={fmt_num(d2.get('t_at_peak_max'))} "
        f"n_células {fmt_num(d2.get('n_cells_t0'))}→{fmt_num(d2.get('n_cells_t_peak'))} "
        f"t_gone={d2.get('t_point_gone_label')} "
        f"{'aperta' if d2.get('sharpened') else 'não aperta'} |\n"
    )
    if "35 singularidade_finita" not in text and row34 in text:
        # insert after the 34 row (the full line)
        idx = text.find(row34)
        end = text.find("\n", idx)
        text = text[: end + 1] + row35 + text[end + 1 :]
    INDEX_PATH.write_text(text, encoding="utf-8")


def patch_triad_md():
    text = TRIAD_MD.read_text(encoding="utf-8")
    # one-line only if a runs/programa list exists
    if "## Programa TRIAD → MQ" not in text:
        print("TRIAD.md: sem lista de programa/runs — sem patch", flush=True)
        return False
    needle = "Pasta: `QM/Q04_linearidade/`. Sem claim MQ. Ver [[Q04]]."
    add = (
        needle
        + "\n\n"
        + "**35 singularidade_finita** (2026-08-21): leitura operacional do pico finito "
        "(T=1, 1 e 2 pontos). **Não** é Q05. Nunca SUPPORTED para MQ. "
        "Ver [[35 singularidade_finita]]."
    )
    if "35 singularidade_finita" in text:
        print("TRIAD.md: run 35 já citado", flush=True)
        return False
    if needle in text:
        text = text.replace(needle, add, 1)
        TRIAD_MD.write_text(text, encoding="utf-8")
        print("TRIAD.md: uma linha no programa", flush=True)
        return True
    print("TRIAD.md: âncora Q04 não encontrada — sem patch", flush=True)
    return False


def copy_into_vault(out: Path, script_src: Path):
    ARTEFATOS.mkdir(parents=True, exist_ok=True)
    # figures + tables
    for src in (out / "figures").glob("*.png"):
        shutil.copy2(src, ARTEFATOS / src.name)
    for name in (
        "metrics_1atom.csv",
        "metrics_2atom.csv",
        "summary.json",
        "SHA256SUMS.txt",
    ):
        p = out / name
        if p.is_file():
            shutil.copy2(p, ARTEFATOS / name)
    # also copy figures SHA after we rewrite vault SHA?
    note_src = out / "35 singularidade_finita.md"
    if note_src.is_file():
        NOTA_PATH.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(note_src, NOTA_PATH)
    FONTES.mkdir(parents=True, exist_ok=True)
    dst = FONTES / "run_singularidade_35.py"
    if script_src.resolve() != dst.resolve():
        shutil.copy2(script_src, dst)
    # vault artefact SHA (figures + csv + json + script copy not included)
    write_sha256sums(ARTEFATOS)
    shutil.copy2(ARTEFATOS / "SHA256SUMS.txt", out / "SHA256SUMS.txt")


def main():
    started = now_sp()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(parents=True, exist_ok=True)
    executed = Path(__file__).resolve()
    solver_sha = sha256_file(executed)
    q02_sha = sha256_file(Q02_PATH) if Q02_PATH.is_file() else ""
    backend = BACKEND if MLX_OK else "numpy"
    if not MLX_OK:
        print("USING numpy fp32 fallback", flush=True)
    device = str(mx.default_device()) if MLX_OK else "cpu"

    print("35 start", started, "out", OUT, flush=True)
    print("executed", executed, "sha256", solver_sha, flush=True)
    print("q02_sha256", q02_sha, "expected", Q02_SOLVER_SHA, "match", q02_sha == Q02_SOLVER_SHA, flush=True)
    print("backend", backend, "precision", PRECISION, "device", device, flush=True)

    grid = build_grid()
    extra_base = {
        "f_FDT": grid["f_FDT"],
        "noise_amp": grid["noise_amp"],
        "max_nu_dt": float(max(NU) * DT),
        "dx": grid["dx"],
        "dV": grid["dV"],
        "norm_1atom": grid["norm_1atom"],
        "norm_2atom": grid["norm_2atom"],
        "n_steps": int(round(T_FINAL / DT)),
        "backend": backend,
        "device": device,
        "started": started,
    }
    print(
        "grid dx", grid["dx"], "f_FDT", grid["f_FDT"], "noise_amp", grid["noise_amp"],
        "IC norms", grid["norm_1atom"], grid["norm_2atom"],
        flush=True,
    )

    t0 = time.perf_counter()
    results = {}
    for name in ("1atom", "2atom"):
        results[name] = run_ic(name, grid, backend)
    wall_total = time.perf_counter() - t0
    finished = now_sp()
    extra_base["wall_total_s"] = wall_total
    extra_base["finished"] = finished

    for name in ("1atom", "2atom"):
        mets = results[name]["metrics"]
        fields = csv_fields(name)
        write_csv(OUT / f"metrics_{name}.csv", mets, fields)

    fig_paths = make_figures(OUT, results, grid)

    summary = {
        "run": 35,
        "title": "singularidade_finita",
        "question": (
            "enquanto o pico é finito, ele aperta (menos células, peak sobe), "
            "espalha (mais células), ou some no universo?"
        ),
        "not_q05": True,
        "qm_comparison": False,
        "supported_for_qm": False,
        "theta_core_unchanged": True,
        "kT_untouched": True,
        "terms_isolated": False,
        "seed": SEED,
        "T": T_FINAL,
        "L": LBOX,
        "N": NGRID,
        "dt": DT,
        "record_every": RECORD_EVERY,
        "record_dt": DT * RECORD_EVERY,
        "backend": backend,
        "precision": PRECISION,
        "device": device,
        "q02_solver_sha256": q02_sha,
        "q02_solver_sha256_expected": Q02_SOLVER_SHA,
        "q02_sha_match": q02_sha == Q02_SOLVER_SHA,
        "script_sha256": solver_sha,
        "canonical_sha256": CANONICAL_SHA,
        "theta_core": {
            "hbar": HBAR,
            "m": M_MASS,
            "Lambda": LAMBDA,
            "alpha": ALPHA,
            "sigma": SIGMA_FRAC,
            "Gamma": GAMMA,
            "nu": list(NU),
            "lambda": list(LAM),
            "fdt_couple": FDT_COUPLE,
            "kT": KT,
            "D": D_DIM,
            "bc": BC,
            "step_mode": STEP_MODE,
        },
        "ics": {
            "1atom": "one gaussian s=0.5 at origin, norm=1 (Q00)",
            "2atom": "Q04 A,B s=0.5 at x=±3 then S=(A+B)/||A+B||, norm=1",
        },
        "derived": {
            "1atom": results["1atom"]["derived"],
            "2atom": results["2atom"]["derived"],
        },
        "f_FDT": grid["f_FDT"],
        "noise_amp": grid["noise_amp"],
        "started_america_sao_paulo": started,
        "finished_america_sao_paulo": finished,
        "wall_total_s": wall_total,
        "figures": {k: str(v) for k, v in fig_paths.items()},
        "reading": {
            "gaussian_is_atom": True,
            "filled_volume_is_universe": True,
            "singularity_is_finite_peak": True,
            "never_star_or_planet": True,
            "never_supported_for_mq": True,
        },
    }
    with (OUT / "summary.json").open("w") as f:
        json.dump(jsonable(summary), f, indent=2)

    write_note(OUT, results, extra_base)
    write_sha256sums(OUT)
    copy_into_vault(OUT, executed)
    patch_index(results["1atom"]["derived"], results["2atom"]["derived"])
    patch_triad_md()

    print("SUCCESS", flush=True)
    for name in ("1atom", "2atom"):
        d = results[name]["derived"]
        print(
            f"RETURN {name} peak_max={d.get('peak_max')} t={d.get('t_at_peak_max')} "
            f"n_cells_t0={d.get('n_cells_t0')} n_cells_t_peak={d.get('n_cells_t_peak')} "
            f"t_point_gone={d.get('t_point_gone_label')} sharpened={d.get('sharpened')} "
            f"finite_singularity={d.get('finite_singularity')} wall_s={d.get('wall_s')}",
            flush=True,
        )
    print("wall_total_s", wall_total, "backend", backend, "device", device, flush=True)
    print("figures", {k: str(v) for k, v in fig_paths.items()}, flush=True)
    print("script_sha256", solver_sha, flush=True)
    print("q02_sha256", q02_sha, flush=True)
    print("finished", finished, flush=True)


if __name__ == "__main__":
    main()
