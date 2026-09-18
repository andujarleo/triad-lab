#!/usr/bin/env python3
"""Q03 — identificação de subespaços persistentes (POD/PCA + DMD, análise passiva).

PROTOCOL: /tmp/Q03_subespacos/PROTOCOL.md
  SHA-256 f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16
Passo Strang idêntico a Q02 code/run_q02.py
  SHA-256 ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365

Pergunta: a dinâmica completa produz modos/coordenadas macroscópicas
que mantêm identidade suficiente para serem tratados como estados?

Snapshots são sensores. POD/DMD NÃO controlam o solver.
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
import os
import time
import traceback
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
Q03_DIR = VAULT / "QM" / "Q03_subespacos"
Q02_DIR = VAULT / "QM" / "Q02_ensemble"
TMP_ROOT = Path("/tmp/Q03_subespacos")
OUT = TMP_ROOT / "out"
PROTOCOL_PATHS = (
    TMP_ROOT / "PROTOCOL.md",
    Q03_DIR / "PROTOCOL.md",
)
PROTOCOL_SHA_KNOWN = "f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16"
Q02_SOLVER_SHA = "ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365"
CANONICAL_SHA = "e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e"
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
SEEDS = (0, 1, 2, 3)
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 40
SNAP_EVERY = 8
K_CUT_FACTOR = 1.0
PRECISION = "complex64"
DTYPE_PSI_NP = np.complex64
DTYPE_R_NP = np.float32
LATE_FRAC = 0.8
T_EARLY = 0.2
T_LATE = LATE_FRAC * T_FINAL  # 6.4
BOX_HALF = LBOX / 2.0
FILL_ABS = 1.0
FILL_REL = 0.9
SETTLE_REL = 0.05
PRINT_EVERY_T = 2.0
N_POD_REPORT = 16
RECON_RS = (1, 2, 4, 8)
R_DMD = 8
MEAN_C_EPS = 1e-30
OBS_LATE = (
    "norm",
    "peak",
    "PR",
    "R_rms",
    "k_star",
    "k_star_L",
    "Vmem_peak",
    "crystallinity",
)

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


def mass_radii(rho, r, dV, fractions=(0.5, 0.8, 0.9)):
    mass = (rho * dV).ravel()
    order = np.argsort(r.ravel(), kind="mergesort")
    cum = np.cumsum(mass[order])
    tot = float(cum[-1]) if cum.size else 0.0
    r_sorted = r.ravel()[order]
    out = []
    for f in fractions:
        if tot <= 0.0:
            out.append(0.0)
            continue
        idx = int(np.searchsorted(cum, f * tot, side="left"))
        idx = min(idx, r_sorted.size - 1)
        out.append(float(r_sorted[idx]))
    return out


def spectral_observables(psi, k_mag, dk, k_cut):
    psi_k = np.fft.fftn(psi)
    power = np.abs(psi_k) ** 2
    tot = float(power.sum())
    if tot <= 0.0:
        return 0.0, 0.0, 0.0
    cryst = float(power[k_mag > k_cut].sum() / tot)
    nbins = max(1, int(np.ceil(float(k_mag.max()) / dk)))
    idx = np.minimum((k_mag / dk).astype(np.int64), nbins - 1)
    sums = np.bincount(idx.ravel(), weights=power.ravel(), minlength=nbins)
    counts = np.bincount(idx.ravel(), minlength=nbins)
    shells = np.divide(sums, counts, out=np.zeros(nbins), where=counts > 0)
    k_centers = (np.arange(nbins) + 0.5) * dk
    mask = k_centers > k_cut
    if not np.any(mask):
        return 0.0, 0.0, cryst
    i_star = int(np.argmax(np.where(mask, shells, -np.inf)))
    k_star = float(k_centers[i_star])
    return k_star, k_star * LBOX, cryst


def peak_structure(rho, dx):
    peak = float(rho.max())
    if not np.isfinite(peak) or peak <= 0.0:
        return {
            "peak_n_cells_half": 0,
            "peak_r_cells": 0.0,
            "peak_width_phys": 0.0,
            "artifact_1_2_cells": True,
        }
    n_cells = int((rho >= 0.5 * peak).sum())
    r_cells = float((3.0 * n_cells / (4.0 * np.pi)) ** (1.0 / 3.0))
    return {
        "peak_n_cells_half": n_cells,
        "peak_r_cells": r_cells,
        "peak_width_phys": r_cells * dx,
        "artifact_1_2_cells": n_cells <= 2,
    }


def build_state(N):
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False, dtype=np.float64)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    r = np.sqrt(r2)
    kvec = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(kvec, kvec, kvec, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k_mag = np.sqrt(k2)
    H_lin = (HBAR * HBAR * k2) / (2.0 * M_MASS)
    if ALPHA != 0.0:
        H_lin = H_lin + ALPHA * np.power(k_mag, SIGMA_FRAC)
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    s = INIT_SIGMA
    psi = np.exp(-r2 / (2.0 * s * s)).astype(np.complex128)
    k0x, k0y, k0z = INIT_K0
    if k0x != 0.0 or k0y != 0.0 or k0z != 0.0:
        psi = psi * np.exp(1j * (k0x * X + k0y * Y + k0z * Z))
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.full((len(NU), N, N, N), Y0, dtype=np.float64)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    return {
        "x": x,
        "dx": dx,
        "dV": dV,
        "r2": r2,
        "r": r,
        "k_mag": k_mag,
        "half_lin": half_lin.astype(DTYPE_PSI_NP),
        "psi": psi.astype(DTYPE_PSI_NP),
        "y": y.astype(DTYPE_R_NP),
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
    }


def mul_phase_mlx(psi, theta):
    """psi *= exp(-i * theta); theta real. Idêntico a Q02."""
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


def record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam):
    rho = np.abs(psi) ** 2
    finite = bool(np.isfinite(rho).all() and np.isfinite(y).all())
    if not finite:
        rec = {
            "t": t,
            "norm": float("nan"),
            "peak": float("nan"),
            "PR": float("nan"),
            "R_rms": float("nan"),
            "r50": float("nan"),
            "r80": float("nan"),
            "r90": float("nan"),
            "Vmem_peak": float("nan"),
            "Vmem_mean": float("nan"),
            "k_star": float("nan"),
            "k_star_L": float("nan"),
            "crystallinity": float("nan"),
            "M1": float("nan"),
            "M2": float("nan"),
            "M3": float("nan"),
            "peak_n_cells_half": 0,
            "peak_r_cells": float("nan"),
            "peak_width_phys": float("nan"),
            "artifact_1_2_cells": True,
            "finite": False,
        }
        return rho, rec
    norm = float(rho.sum() * dV)
    peak = float(rho.max())
    pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
    rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
    r50, r80, r90 = mass_radii(rho, r, dV)
    vmem = (lam.reshape((-1, 1, 1, 1)) * y).sum(axis=0)
    k_star, k_star_L, cryst = spectral_observables(psi, k_mag, dk, k_cut)
    rho4 = float((rho ** 2).sum() * dV)
    mem_pers = []
    for j in range(y.shape[0]):
        num = float((y[j] ** 2).sum() * dV)
        mem_pers.append(num / max(rho4, 1e-300))
    struct = peak_structure(rho, dx)
    rec = {
        "t": t,
        "norm": norm,
        "peak": peak,
        "PR": pr,
        "R_rms": rrms,
        "r50": r50,
        "r80": r80,
        "r90": r90,
        "Vmem_peak": float(vmem.max()) if vmem.size else 0.0,
        "Vmem_mean": float(vmem.mean()) if vmem.size else 0.0,
        "k_star": k_star,
        "k_star_L": k_star_L,
        "crystallinity": cryst,
        "M1": mem_pers[0] if mem_pers else 0.0,
        "M2": mem_pers[1] if len(mem_pers) > 1 else 0.0,
        "M3": mem_pers[2] if len(mem_pers) > 2 else 0.0,
        "finite": True,
    }
    rec.update(struct)
    return rho, rec


def series_of(metrics, key):
    return np.array([m[key] for m in metrics], dtype=np.float64)


def late_stats(metrics, key, t_arr, t_late):
    v = series_of(metrics, key)
    mask = t_arr >= t_late
    vv = v[mask]
    vv = vv[np.isfinite(vv)]
    if vv.size == 0:
        return float("nan"), float("nan"), 0
    return float(vv.mean()), float(vv.std(ddof=0)), int(vv.size)


def empirical_transient(metrics, rrms_late):
    t_arr = series_of(metrics, "t")
    rrms = series_of(metrics, "R_rms")
    t_settle = None
    t_fill = None
    fill_thr = FILL_REL * BOX_HALF
    for t, r in zip(t_arr, rrms):
        if t_fill is None and np.isfinite(r) and r > fill_thr:
            t_fill = float(t)
    if np.isfinite(rrms_late) and abs(rrms_late) > 0.0:
        thr = SETTLE_REL * abs(rrms_late)
        ok = np.isfinite(rrms) & (np.abs(rrms - rrms_late) < thr)
        for i in range(len(t_arr)):
            if bool(np.all(ok[i:])):
                t_settle = float(t_arr[i])
                break
    return t_settle, t_fill


def inner_complex(a, b, dV):
    """⟨a|b⟩ = Σ conj(a) b · dV  (complex)."""
    return complex(np.vdot(a.ravel(), b.ravel()) * dV)


def l2_complex(a, dV):
    return float(np.sqrt(np.real(inner_complex(a, a, dV))))


def normalize_complex(a, dV):
    nrm = l2_complex(a, dV)
    if nrm <= 0.0 or not math.isfinite(nrm):
        return a, 0.0
    return a / nrm, nrm


def acf_time(abs_c, dt_snap):
    abs_c = np.asarray(abs_c, dtype=np.float64)
    if abs_c.size < 3:
        return None
    mu = float(np.mean(abs_c))
    if (not math.isfinite(mu)) or abs(mu) < MEAN_C_EPS:
        return None
    x = abs_c - mu
    n = int(x.size)
    for lag in range(1, n):
        a = x[:-lag]
        b = x[lag:]
        da = float(np.dot(a, a))
        db = float(np.dot(b, b))
        if da <= 0.0 or db <= 0.0:
            return None
        rho = float(np.dot(a, b) / math.sqrt(da * db))
        if rho < (1.0 / math.e):
            return float(lag * dt_snap)
    return None


def stacked_from_snaps(snaps):
    """snaps (n, N, N, N) complex -> X (n, 2 N³) float32 centered, mean complex (N3,)."""
    n = int(snaps.shape[0])
    xc = np.asarray(snaps, dtype=np.complex64).reshape(n, -1)
    mean = xc.mean(axis=0)
    xc = xc - mean
    x = np.concatenate(
        [np.real(xc).astype(np.float32, copy=False), np.imag(xc).astype(np.float32, copy=False)],
        axis=1,
    )
    return x, mean


def economy_pod(snaps, dV, n_report=N_POD_REPORT):
    """POD econômico: Gram n_snap × n_snap. NÃO forma 2N³ × 2N³.

    Convenção (PROTOCOL):
    - matriz [Re Ψ; Im Ψ], média temporal da janela subtraída
    - G = X Xᵀ se X é (n_snap, 2 N³)
    - c_n(t_k) = σ_n V_{k n}  (produto real do empilhamento)
    - φ = φ_re + i φ_im
    """
    x, mean = stacked_from_snaps(snaps)
    n, dim = x.shape
    n3 = dim // 2
    shape = snaps.shape[1:]
    G = np.dot(x, x.T).astype(np.float64, copy=False)
    evals, vecs = np.linalg.eigh(G)
    order = np.argsort(evals)[::-1]
    evals = np.maximum(evals[order], 0.0)
    vecs = vecs[:, order]
    sigmas = np.sqrt(evals)
    ev_sum = float(evals.sum())
    ev_frac = (evals / ev_sum) if ev_sum > 0.0 else np.zeros_like(evals)
    n_keep = int(min(n_report, ev_frac.size))
    ev16 = np.zeros(n_report, dtype=np.float64)
    ev16[:n_keep] = ev_frac[:n_keep]
    rec = {}
    x_norm = float(np.linalg.norm(x))
    for r in RECON_RS:
        rr = int(min(r, vecs.shape[1]))
        if rr <= 0 or x_norm == 0.0:
            rec[r] = float("nan")
            continue
        vr = vecs[:, :rr]
        x_approx = vr @ (vr.T @ x)
        rec[r] = float(np.linalg.norm(x - x_approx) / x_norm)
        del x_approx
    n_coeff = int(min(8, vecs.shape[1]))
    # c_n(t) = σ_n V_{k n}
    c = (vecs[:, :n_coeff] * sigmas[:n_coeff].reshape(1, -1)).astype(np.float64)
    # modos complexos unitários no empilhamento real; depois normalizar L2 complexo
    modes = []
    for k in range(n_coeff):
        sig = float(sigmas[k])
        if sig <= 0.0:
            phi = np.zeros(shape, dtype=np.complex64)
        else:
            stack = (x.T @ vecs[:, k]) / sig
            phi = (stack[:n3] + 1j * stack[n3:]).reshape(shape).astype(np.complex64)
        modes.append(phi)
    persist = []
    for k in range(3):
        if k >= c.shape[1]:
            persist.append({"std_over_mean": None, "mean_abs": None, "std_abs": None})
            continue
        ac = np.abs(c[:, k])
        mu = float(np.mean(ac))
        sd = float(np.std(ac, ddof=0))
        ratio = float(sd / mu) if (math.isfinite(mu) and abs(mu) >= MEAN_C_EPS) else None
        persist.append({"std_over_mean": ratio, "mean_abs": mu, "std_abs": sd})
    acf_t = acf_time(np.abs(c[:, 0]), SNAP_EVERY * DT) if c.shape[1] > 0 else None
    ev8 = float(ev_frac[:8].sum()) if ev_frac.size else float("nan")
    return {
        "n_snap": n,
        "mean": mean,
        "sigmas": sigmas,
        "ev_frac": ev_frac,
        "ev16": ev16,
        "ev8": ev8,
        "rec": rec,
        "c": c,
        "modes": modes,
        "persist": persist,
        "acf_time_c0": acf_t,
        "x_frob": x_norm,
    }


def project_full_c0(mm, mean_c, phi_complex, dV):
    """|c_0(t)| na trajetória inteira: produto real empilhado = Re⟨φ|Ψ−mean⟩ sem dV.

    Usa o mesmo produto do POD (empilhamento real). φ aqui é o modo stacked-unit
    reconstruído; equivalente a ⟨φ_stack | x(t)⟩.
    """
    n = int(mm.shape[0])
    n3 = int(np.prod(mm.shape[1:]))
    phi = np.asarray(phi_complex, dtype=np.complex64).ravel()
    # stacked unit from POD: sum(|phi|^2) = 1
    pstack = np.concatenate([np.real(phi), np.imag(phi)]).astype(np.float32, copy=False)
    pn = float(np.linalg.norm(pstack))
    if pn > 0.0:
        pstack = pstack / pn
    mean = np.asarray(mean_c, dtype=np.complex64).ravel()
    c0 = np.empty(n, dtype=np.float64)
    for i in range(n):
        z = np.asarray(mm[i], dtype=np.complex64).ravel() - mean
        x = np.concatenate([np.real(z), np.imag(z)]).astype(np.float32, copy=False)
        c0[i] = float(np.dot(x, pstack))
    return c0


def dmd_abs_lambda(snaps, r_dmd=R_DMD):
    """SVD-DMD padrão, posto r_dmd=8 fixo, snapshots centrados empilhados."""
    x, _mean = stacked_from_snaps(snaps)
    # X columns = snapshots: use (2N3, n)
    # x is (n, 2N3)
    if x.shape[0] < 3:
        return np.full(r_dmd, np.nan)
    x1 = x[:-1]  # (n-1, dim)
    x2 = x[1:]
    # SVD econômico via Gram de X1^T (já é x1 x1^T)
    g = np.dot(x1, x1.T).astype(np.float64, copy=False)
    evals, vecs = np.linalg.eigh(g)
    order = np.argsort(evals)[::-1]
    evals = np.maximum(evals[order], 0.0)
    vecs = vecs[:, order]
    sigmas = np.sqrt(evals)
    r = int(min(r_dmd, int(np.count_nonzero(sigmas > 1e-12)), vecs.shape[1]))
    if r <= 0:
        return np.full(r_dmd, np.nan)
    vr = vecs[:, :r]
    sr = sigmas[:r]
    # U = X1^T V / σ   (dim, r)   — X1 é (n-1, dim), então x1.T @ vr / sr
    # Ã = U^T X2 V Σ^{-1} = (U^T x2^T)^T ... 
    # U^T X2_cols = (x1.T @ vr / sr).T @ x2.T = (vr.T @ x1 @ x2.T) / sr
    # V = vr (temporal left of X1), X2_cols = x2.T
    # Atilde = U.T @ X2 @ V @ inv(S) with V = right singular of X1
    # X1 = U Σ W^T, W = vr (n-1, r) because X1 X1^T = W Σ² W^T
    # Atilde = U.T X2 W / Σ = ((x1.T @ W / Σ).T) @ x2.T @ W / Σ
    #        = (W.T @ x1 @ x2.T @ W) / Σ / Σ  wait no:
    # U = x1.T @ W / Σ   shape (dim, r)
    # U.T @ x2.T = (W.T @ x1 @ x2.T) / Σ     shape (r, n-1)  because x2 is (n-1, dim), x2.T is (dim, n-1)
    ut_x2 = (vr.T @ (x1 @ x2.T).astype(np.float64)) / sr.reshape(-1, 1)
    atilde = (ut_x2 @ vr) / sr.reshape(1, -1)
    w, _ = np.linalg.eig(atilde)
    abs_l = np.abs(w)
    abs_l = np.sort(abs_l)[::-1]
    out = np.full(r_dmd, np.nan, dtype=np.float64)
    out[: abs_l.size] = abs_l
    return out


def window_indices(t_arr, kind):
    if kind == "early":
        return np.nonzero(t_arr <= T_EARLY + 1e-12)[0]
    return np.nonzero(t_arr >= T_LATE - 1e-12)[0]


def run_one(seed, geom, backend):
    t_wall0 = time.perf_counter()
    N = NGRID
    dx = geom["dx"]
    dV = geom["dV"]
    r2 = geom["r2"]
    r = geom["r"]
    k_mag = geom["k_mag"]
    half_lin_np = geom["half_lin"]
    noise_amp = geom["noise_amp"]
    f_FDT = geom["f_FDT"]
    psi0_np = geom["psi"]
    y0_np = geom["y"]
    shape = (N, N, N)
    nu_np = np.array(NU, dtype=DTYPE_R_NP)
    lam_np = np.array(LAM, dtype=DTYPE_R_NP)

    rng = np.random.default_rng(seed)
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    n_steps = int(round(T_FINAL / DT))
    rec_every = max(1, RECORD_EVERY)
    snap_every = max(1, SNAP_EVERY)
    n_snap = n_steps // snap_every + 1
    raw = OUT / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    psi_path = raw / f"seed{seed:02d}_psi_t.npy"
    t_path = raw / f"seed{seed:02d}_t.npy"

    print(
        f"=== Q03 seed={seed:02d} N={N} start backend={backend} {PRECISION} ===",
        flush=True,
    )
    device_s = "numpy-cpu"
    if backend == "mlx":
        device_s = str(mx.default_device())
        psi = mx.array(psi0_np)
        y = mx.array(y0_np)
        half_lin = mx.array(half_lin_np)
        nu = mx.array(nu_np)
        lam = mx.array(lam_np)
        mx.eval(psi, y, half_lin)
    else:
        psi = psi0_np.copy()
        y = y0_np.copy()
        half_lin = half_lin_np
        nu = nu_np
        lam = lam_np

    print(
        f"seed={seed:02d} device {device_s} L {LBOX} dx {dx} dt {DT} T {T_FINAL} "
        f"n_steps {n_steps} n_snap {n_snap} f_FDT {f_FDT} noise_amp {noise_amp} "
        f"max_nu_dt {float(max(NU) * DT)}",
        flush=True,
    )

    mm = np.lib.format.open_memmap(
        psi_path, mode="w+", dtype=np.complex64, shape=(n_snap, N, N, N)
    )
    t_snaps = np.empty(n_snap, dtype=np.float64)
    metrics = []
    blew = False
    blow_t = None
    peak_max = float("-inf")
    peak_max_t = None
    last_print_bucket = -1
    i_snap = 0
    for step in range(n_steps + 1):
        t = step * DT
        need_snap = (step % snap_every == 0) or (step == n_steps)
        need_rec = (step % rec_every == 0) or (step == n_steps)
        if need_snap or need_rec:
            if backend == "mlx":
                psi_np = np.array(psi)
                y_np = np.array(y) if need_rec else None
            else:
                psi_np = np.asarray(psi)
                y_np = np.asarray(y) if need_rec else None
            if need_snap:
                if i_snap < n_snap:
                    mm[i_snap] = psi_np
                    t_snaps[i_snap] = t
                    i_snap += 1
            if need_rec:
                rho, rec = record_metrics(
                    psi_np, y_np, t, dV, dx, r2, r, k_mag, dk, k_cut, lam_np
                )
                rec["seed"] = seed
                rec["N"] = N
                rec["dx"] = dx
                rec["backend"] = backend
                metrics.append(rec)
                if rec["finite"] and np.isfinite(rec["peak"]) and rec["peak"] > peak_max:
                    peak_max = float(rec["peak"])
                    peak_max_t = float(t)
                bucket = int(t // PRINT_EVERY_T)
                if bucket != last_print_bucket or step == n_steps or (not rec["finite"]):
                    last_print_bucket = bucket
                    print(
                        f"seed={seed:02d} t={t:.4f} norm={rec['norm']:.6e} "
                        f"peak={rec['peak']:.6e} PR={rec['PR']:.6e} "
                        f"Rrms={rec['R_rms']:.6e} k*={rec['k_star']:.6e} "
                        f"finite={rec['finite']}",
                        flush=True,
                    )
                if (not rec["finite"]) or (
                    np.isfinite(rec["peak"]) and abs(rec["peak"]) > 1.0e30
                ):
                    blew = True
                    blow_t = t
                    print("BLOWUP_OR_NAN", "seed", seed, "t", t, flush=True)
        if step == n_steps or blew:
            break
        if backend == "mlx":
            psi, y = strang_step_mlx(psi, y, half_lin, noise_amp, rng, nu, lam, shape)
        else:
            psi, y = strang_step_np(psi, y, half_lin, noise_amp, rng, nu, lam, shape)

    mm.flush()
    if i_snap < n_snap:
        # trajetória curta (blowup): truncar visualmente via máscara de t
        t_snaps[i_snap:] = np.nan
    np.save(t_path, t_snaps)
    wall_evo = time.perf_counter() - t_wall0

    csv_path = raw / f"seed{seed:02d}_metrics.csv"
    if metrics:
        write_csv(csv_path, metrics, list(metrics[0].keys()))

    t_arr_m = series_of(metrics, "t") if metrics else np.array([], dtype=np.float64)
    last = metrics[-1] if metrics else {}
    finite_final = bool(last.get("finite", False)) and (not blew)

    summary = {
        "question": "Q03",
        "seed": seed,
        "N": N,
        "L": LBOX,
        "dx": dx,
        "dt": DT,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "n_snap_written": int(i_snap),
        "record_every": rec_every,
        "snap_every": snap_every,
        "backend": backend,
        "precision": PRECISION,
        "fp": "fp32",
        "solver": "standalone 3D Strang (mesmo passo Q02; não triad-lang)",
        "hbar": HBAR,
        "m": M_MASS,
        "Lambda": LAMBDA,
        "alpha": ALPHA,
        "sigma": SIGMA_FRAC,
        "Gamma": GAMMA,
        "nu": list(NU),
        "lam": list(LAM),
        "fdt_couple": FDT_COUPLE,
        "kT": KT,
        "D": D_DIM,
        "bc": BC,
        "step_mode": STEP_MODE,
        "V_ext": V_EXT,
        "init_sigma": INIT_SIGMA,
        "init_k0": list(INIT_K0),
        "y0": Y0,
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
        "memory_update": "euler",
        "max_nu_dt": float(max(NU) * DT),
        "wall_evolve_s": wall_evo,
        "blew_up": blew,
        "blow_t": blow_t,
        "finite": finite_final,
        "finite_final": finite_final,
        "csv": str(csv_path),
        "psi_memmap": str(psi_path),
        "peak_max": peak_max if math.isfinite(peak_max) and peak_max > float("-inf") else float("nan"),
        "peak_max_t": peak_max_t,
    }
    for key in OBS_LATE:
        lm, ls, ln = (
            late_stats(metrics, key, t_arr_m, T_LATE) if metrics else (float("nan"), float("nan"), 0)
        )
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln
    t_settle, t_fill = empirical_transient(metrics, summary.get("R_rms_late_mean", float("nan")))
    summary["t_settle"] = t_settle
    summary["t_fill"] = t_fill
    rlate = summary.get("R_rms_late_mean", float("nan"))
    summary["box_filled"] = bool(np.isfinite(rlate) and abs(rlate - BOX_HALF) <= FILL_ABS)

    # --- POD / DMD (sensores; não realimentam o solver) ---
    t_an0 = time.perf_counter()
    valid = np.isfinite(t_snaps)
    t_use = t_snaps[valid]
    psi0 = np.asarray(psi0_np, dtype=np.complex64)
    pod_out = {}
    dmd_l = None
    c0_full = None
    if finite_final and int(valid.sum()) >= 3:
        mm_ok = mm[: int(valid.sum())]
        for kind in ("early", "late"):
            idx = window_indices(t_use, kind)
            if idx.size < 3:
                pod_out[kind] = {"ok": False, "reason": "too_few_snapshots"}
                continue
            snaps = np.array(mm_ok[idx], dtype=np.complex64)
            pod = economy_pod(snaps, dV)
            phi0 = pod["modes"][0] if pod["modes"] else np.zeros(shape, dtype=np.complex64)
            phi0_n, _ = normalize_complex(phi0, dV)
            ic_ov = abs(inner_complex(phi0_n, psi0, dV)) if l2_complex(phi0_n, dV) > 0 else float("nan")
            rec_map = {int(k): pod["rec"][k] for k in pod["rec"]}
            pod_out[kind] = {
                "ok": True,
                "n_snap": pod["n_snap"],
                "ev16": [float(v) for v in pod["ev16"]],
                "ev8": float(pod["ev8"]),
                "rec": rec_map,
                "persist": pod["persist"],
                "acf_time_c0": pod["acf_time_c0"],
                "ic_overlap": float(ic_ov) if math.isfinite(float(np.real(ic_ov))) else float("nan"),
                "c_n": pod["c"][:, :3].tolist() if pod["c"].size else [],
                "t_window": [float(v) for v in t_use[idx]],
            }
            np.save(raw / f"seed{seed:02d}_phi0_{kind}.npy", phi0_n.astype(np.complex64))
            np.save(raw / f"seed{seed:02d}_ev_{kind}.npy", pod["ev16"])
            np.save(raw / f"seed{seed:02d}_c_{kind}.npy", pod["c"])
            if kind == "late":
                c0_full = project_full_c0(mm_ok, pod["mean"], phi0, dV)
                np.save(raw / f"seed{seed:02d}_c0_full.npy", c0_full)
                np.save(raw / f"seed{seed:02d}_t_use.npy", t_use)
                if seed in (0, 1):
                    dmd_l = dmd_abs_lambda(snaps, R_DMD)
                    np.save(raw / f"seed{seed:02d}_dmd_abs_lambda.npy", dmd_l)
                    pod_out["dmd_abs_lambda"] = [float(v) if np.isfinite(v) else None for v in dmd_l]
                    print(f"seed={seed:02d} DMD |λ| = {dmd_l}", flush=True)
            print(
                f"seed={seed:02d} POD {kind} ev8={pod['ev8']:.6f} rec8={pod['rec'].get(8, float('nan')):.6f} "
                f"ic_ov={float(np.real(ic_ov)):.6f} acf={pod['acf_time_c0']}",
                flush=True,
            )
            del snaps, pod
        # apagar memmap grande; derivados ficam
        del mm
        try:
            os.remove(psi_path)
            summary["psi_memmap_deleted"] = True
        except OSError:
            summary["psi_memmap_deleted"] = False
    else:
        del mm
        pod_out["early"] = {"ok": False, "reason": "nonfinite_or_short"}
        pod_out["late"] = {"ok": False, "reason": "nonfinite_or_short"}
        try:
            os.remove(psi_path)
            summary["psi_memmap_deleted"] = True
        except OSError:
            summary["psi_memmap_deleted"] = False

    summary["wall_s"] = time.perf_counter() - t_wall0
    summary["wall_analyze_s"] = time.perf_counter() - t_an0
    summary["pod"] = pod_out
    if c0_full is not None:
        summary["c0_full_path"] = str(raw / f"seed{seed:02d}_c0_full.npy")
    print(
        f"seed={seed:02d} done wall_s={summary['wall_s']:.3f} evo={wall_evo:.3f} "
        f"finite={finite_final} blew={blew} blow_t={blow_t} "
        f"peak_late={summary['peak_late_mean']:.6g} "
        f"PR_late={summary['PR_late_mean']:.6g} "
        f"Rrms_late={summary['R_rms_late_mean']:.6g}",
        flush=True,
    )
    with (raw / f"seed{seed:02d}_summary.json").open("w") as f:
        json.dump(jsonable(summary), f, indent=2)
    return summary


def load_phi0(seed, kind):
    p = OUT / "raw" / f"seed{seed:02d}_phi0_{kind}.npy"
    if not p.is_file():
        return None
    return np.load(p)


def pairwise_overlaps(seeds, kind, dV):
    phis = {}
    for s in seeds:
        ph = load_phi0(s, kind)
        if ph is None:
            continue
        phis[s] = ph
    pairs = {}
    vals = []
    keys = sorted(phis)
    for i, si in enumerate(keys):
        ai, _ = normalize_complex(phis[si], dV)
        for sj in keys[i + 1 :]:
            bj, _ = normalize_complex(phis[sj], dV)
            ov = abs(inner_complex(ai, bj, dV))
            pairs[f"{si}-{sj}"] = float(ov)
            vals.append(float(ov))
    mean_ov = float(np.mean(vals)) if vals else float("nan")
    return pairs, mean_ov


def apply_verdict(ev8, rec8, ov, n_finite, n_blow):
    if n_blow > 1:
        return "NUMERICAL_FAILURE"
    if (
        ev8 is None
        or rec8 is None
        or ov is None
        or (not math.isfinite(ev8))
        or (not math.isfinite(rec8))
        or (not math.isfinite(ov))
    ):
        return "INCONCLUSIVE"
    if ev8 >= 0.50 and rec8 <= 0.30 and ov >= 0.50:
        return "PARTIAL"
    if ev8 < 0.20 and rec8 > 0.50:
        return "NOT_SUPPORTED"
    return "INCONCLUSIVE"


def mean_of(vals):
    a = np.array([v for v in vals if v is not None and np.isfinite(v)], dtype=np.float64)
    if a.size == 0:
        return float("nan")
    return float(a.mean())


def fmt(v, nd=6):
    if v is None:
        return "omitido"
    try:
        fv = float(v)
    except (TypeError, ValueError):
        return "omitido"
    if not math.isfinite(fv):
        return "omitido"
    return f"{fv:.{nd}g}"


def load_q02_late(seed):
    cands = [
        Q02_DIR / "raw" / f"seed{seed:02d}_summary.json",
        Path("/tmp/Q02_ensemble/out/raw") / f"seed{seed:02d}_summary.json",
    ]
    for p in cands:
        if p.is_file():
            with p.open() as f:
                return json.load(f)
    return None


def make_figures(finite_seeds, by_seed, ov_early, ov_late):
    fig_dir = OUT / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    paths = {}

    # ev_spectrum
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    idx = np.arange(1, N_POD_REPORT + 1)
    for kind, color, lab in (
        ("early", "#1f77b4", "early (t ≤ 0.2)"),
        ("late", "#d62728", "late (t ≥ 6.4)"),
    ):
        mat = []
        for s in finite_seeds:
            pod = by_seed[s]["pod"].get(kind, {})
            if pod.get("ok") and pod.get("ev16"):
                mat.append(pod["ev16"])
        if not mat:
            continue
        mat = np.array(mat, dtype=np.float64)
        mu = mat.mean(axis=0)
        sd = mat.std(axis=0, ddof=0)
        ax.plot(idx, mu, "o-", color=color, label=lab, ms=4)
        ax.fill_between(idx, mu - sd, mu + sd, color=color, alpha=0.18)
    ax.set_xlabel("índice do modo")
    ax.set_ylabel("variância explicada  σᵢ² / Σσ²")
    ax.set_title("Espectro POD — early vs late (média ± desvio entre seeds)")
    ax.set_xticks(idx)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    p = fig_dir / "ev_spectrum.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["ev_spectrum"] = str(p)

    # recon_error
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    rs = list(RECON_RS)
    for kind, color, lab in (
        ("early", "#1f77b4", "early (t ≤ 0.2)"),
        ("late", "#d62728", "late (t ≥ 6.4)"),
    ):
        mat = []
        for s in finite_seeds:
            pod = by_seed[s]["pod"].get(kind, {})
            if pod.get("ok") and pod.get("rec"):
                mat.append([rec_of(pod, r) if rec_of(pod, r) is not None else float("nan") for r in rs])
        if not mat:
            continue
        mat = np.array(mat, dtype=np.float64)
        mu = np.nanmean(mat, axis=0)
        sd = np.nanstd(mat, axis=0, ddof=0)
        ax.errorbar(rs, mu, yerr=sd, fmt="o-", color=color, label=lab, capsize=3)
    ax.set_xlabel("número de modos r")
    ax.set_ylabel("erro L2 relativo de reconstrução")
    ax.set_title("Reconstrução POD dos snapshots centrados")
    ax.set_xticks(rs)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    p = fig_dir / "recon_error.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["recon_error"] = str(p)

    # c0_time
    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    for s in SEEDS:
        fp = OUT / "raw" / f"seed{s:02d}_c0_full.npy"
        tp = OUT / "raw" / f"seed{s:02d}_t_use.npy"
        if fp.is_file() and tp.is_file():
            c0 = np.load(fp)
            tt = np.load(tp)
            n = min(c0.size, tt.size)
            ax.plot(tt[:n], np.abs(c0[:n]), label=f"seed {s}", lw=1.2)
    ax.axvline(T_EARLY, color="0.35", ls="--", lw=1.0, label="t = 0.2")
    ax.axvline(T_LATE, color="0.15", ls=":", lw=1.2, label="t = 6.4")
    ax.set_xlabel("t")
    ax.set_ylabel("|c₀(t)|  (projeção no φ₀ late)")
    ax.set_title("Coordenada do modo líder da janela late ao longo de t")
    ax.grid(True, alpha=0.3)
    ax.legend(ncol=3, fontsize=8)
    fig.tight_layout()
    p = fig_dir / "c0_time.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["c0_time"] = str(p)

    # mode0_slice seed 0
    fig, axes = plt.subplots(1, 2, figsize=(10.4, 4.6))
    for ax, kind, title in (
        (axes[0], "early", "early  t ≤ 0.2"),
        (axes[1], "late", "late  t ≥ 6.4"),
    ):
        ph = load_phi0(0, kind)
        if ph is None:
            ax.set_title(title + " (omitido)")
            continue
        sl = np.abs(ph[:, :, NGRID // 2])
        im = ax.imshow(sl.T, origin="lower", extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2), cmap="viridis")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_title(f"|φ₀| plano médio  seed 0 — {title}")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    p = fig_dir / "mode0_slice.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["mode0_slice"] = str(p)

    # dmd_eigs
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    x = np.arange(1, R_DMD + 1)
    width = 0.35
    plotted = False
    for j, s in enumerate((0, 1)):
        pod = by_seed.get(s, {}).get("pod", {})
        vals = pod.get("dmd_abs_lambda")
        if not vals:
            fp = OUT / "raw" / f"seed{s:02d}_dmd_abs_lambda.npy"
            if fp.is_file():
                vals = [float(v) for v in np.load(fp)]
        if not vals:
            continue
        plotted = True
        ax.bar(x + (j - 0.5) * width, vals, width=width, label=f"seed {s}")
    ax.axhline(1.0, color="0.3", ls="--", lw=1.0, label="|λ| = 1")
    ax.set_xlabel("modo DMD (ordenado por |λ| decrescente)")
    ax.set_ylabel("|λ|")
    ax.set_title("Autovalores DMD da janela late (r_dmd = 8, fixo)")
    ax.set_xticks(x)
    ax.set_ylim(0.0, 1.35)
    ax.grid(True, axis="y", alpha=0.3)
    if plotted:
        ax.legend()
    fig.tight_layout()
    p = fig_dir / "dmd_eigs.png"
    fig.savefig(p, dpi=140)
    plt.close(fig)
    paths["dmd_eigs"] = str(p)
    return paths


def write_analysis(path, payload):
    lines = []
    a = lines.append
    a("# Q03 — Análise (subespaços persistentes, POD/DMD passivos)")
    a("")
    a("Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.")
    a("Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.")
    a("Theta_core intocado (Q00). Sem cherry-pick de seed ou de janela.")
    a("Backend **mlx GPU**, campo complex64, memória float32. N_num, não física.")
    a("Snapshots são sensores. POD/DMD **não** controlam o solver.")
    a("Este lote **não** é SUPPORTED para MQ.")
    a("")
    a("## Pergunta")
    a("")
    a("A dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?")
    a("")
    a("## Setup")
    a("")
    a("- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0")
    a("- L=32.0, N=64, dt=0.0025, T=8.0, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0")
    a("- FDT: spec eq. 4; memória Euler; RNG numpy → upload GPU")
    a("- seeds 0,1,2,3 nessa ordem (primeiras quatro de Q02); complex64/float32; backend mlx GPU; Strang Q02")
    a("- snapshots a cada 8 passos (Δt=0.02), 401/seed; métricas a cada 40 passos")
    a("- janela early t≤0.2 (11 snaps); janela late t≥6.4 (81 snaps); ambas pré-declaradas")
    a(f"- PROTOCOL SHA-256: `{payload['protocol_sha256']}`")
    a(f"- solver executado SHA-256: `{payload['solver_sha256']}`")
    a(f"- Q02 passo SHA-256: `{Q02_SOLVER_SHA}`")
    a(f"- canônico Q00: `{CANONICAL_SHA}`")
    a(f"- Q02 PROTOCOL_v2: `{Q02_PROTOCOL_V2_SHA}`")
    a(f"- início (America/Sao_Paulo): {payload['started_america_sao_paulo']}")
    a(f"- fim (America/Sao_Paulo): {payload['finished_america_sao_paulo']}")
    a(f"- wall total: {fmt(payload['wall_total_s'], 4)} s")
    a(f"- device: {payload.get('device')}")
    a(f"- backend: {payload.get('backend')}")
    a("")
    a("## Tempos de parede por seed")
    a("")
    a("| seed | wall_s | evo_s | finito | blow_t | peak_late | PR_late | R_rms_late | norm_late |")
    a("|---|---|---|---|---|---|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        a(
            f"| {s} | {fmt(row.get('wall_s'), 4)} | {fmt(row.get('wall_evolve_s'), 4)} | "
            f"{row.get('finite')} | {row.get('blow_t') if row.get('blow_t') is not None else '—'} | "
            f"{fmt(row.get('peak_late_mean'))} | {fmt(row.get('PR_late_mean'))} | "
            f"{fmt(row.get('R_rms_late_mean'))} | {fmt(row.get('norm_late_mean'))} |"
        )
    a("")
    a("## Métricas late vs Q02 (reprodução, não correção)")
    a("")
    a("Q02 já mostrou caixa cheia em t=0.1, peak tardio ~3.89, R_rms=16. Q03 não conserta isso.")
    a("")
    a("| seed | peak Q03 | peak Q02 | PR Q03 | PR Q02 | R_rms Q03 | R_rms Q02 | norm Q03 | norm Q02 |")
    a("|---|---|---|---|---|---|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        q2 = row.get("q02") or {}
        a(
            f"| {s} | {fmt(row.get('peak_late_mean'))} | {fmt(q2.get('peak_late_mean'))} | "
            f"{fmt(row.get('PR_late_mean'))} | {fmt(q2.get('PR_late_mean'))} | "
            f"{fmt(row.get('R_rms_late_mean'))} | {fmt(q2.get('R_rms_late_mean'))} | "
            f"{fmt(row.get('norm_late_mean'))} | {fmt(q2.get('norm_late_mean'))} |"
        )
    a("")
    a("## Variância explicada POD (σᵢ²/Σσ², i=1..8 e EV8)")
    a("")
    a("| seed | janela | EV8 | ev1 | ev2 | ev3 | ev4 | ev5 | ev6 | ev7 | ev8 |")
    a("|---|---|---|---|---|---|---|---|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        for kind in ("early", "late"):
            pod = row.get("pod", {}).get(kind, {})
            if not pod.get("ok"):
                a(f"| {s} | {kind} | omitido | — | — | — | — | — | — | — | — |")
                continue
            ev = pod.get("ev16") or []
            cells = [fmt(pod.get("ev8"))] + [fmt(ev[i]) if i < len(ev) else "omitido" for i in range(8)]
            a(f"| {s} | {kind} | " + " | ".join(cells) + " |")
    a("")
    a(f"EV8 early (média seeds finitas) = {fmt(payload['ev8_early'])}")
    a(f"EV8 late (média seeds finitas) = {fmt(payload['ev8_late'])}")
    a("")
    a("## Erro de reconstrução relativo L2")
    a("")
    a("| seed | janela | Rec1 | Rec2 | Rec4 | Rec8 |")
    a("|---|---|---|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        for kind in ("early", "late"):
            pod = row.get("pod", {}).get(kind, {})
            if not pod.get("ok"):
                a(f"| {s} | {kind} | omitido | omitido | omitido | omitido |")
                continue
            a(
                f"| {s} | {kind} | {fmt(rec_of(pod, 1))} | {fmt(rec_of(pod, 2))} | "
                f"{fmt(rec_of(pod, 4))} | {fmt(rec_of(pod, 8))} |"
            )
    a("")
    a(f"Rec8 early (média) = {fmt(payload['rec8_early'])}")
    a(f"Rec8 late (média) = {fmt(payload['rec8_late'])}")
    a("")
    a("## Overlaps")
    a("")
    a("Produto complexo normalizado. |⟨φᵢ|φⱼ⟩| já maximiza sobre fase global e^{iθ}.")
    a("")
    a(f"Overlap pairwise médio φ₀ early = {fmt(payload['ov_phi0_early'])}")
    a(f"Overlap pairwise médio φ₀ late = {fmt(payload['ov_phi0_late'])}")
    a("")
    a("Pares early: " + json.dumps(payload.get("pairwise_early") or {}, ensure_ascii=False))
    a("Pares late: " + json.dumps(payload.get("pairwise_late") or {}, ensure_ascii=False))
    a("")
    a("Overlap |⟨φ₀|Ψ(0)⟩| (átomo gaussiano inicial, normalizado):")
    a("")
    a("| seed | IC early | IC late |")
    a("|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        ie = (row.get("pod") or {}).get("early", {}).get("ic_overlap")
        il = (row.get("pod") or {}).get("late", {}).get("ic_overlap")
        a(f"| {s} | {fmt(ie)} | {fmt(il)} |")
    a(f"média IC early = {fmt(payload['ic_overlap_early'])}")
    a(f"média IC late = {fmt(payload['ic_overlap_late'])}")
    a("")
    a("## Persistência |c_n| (janela late)")
    a("")
    a("| seed | std/mean |c0| | std/mean |c1| | std/mean |c2| | τ_acf |c0| |")
    a("|---|---|---|---|---|")
    for s in SEEDS:
        row = payload["per_seed"][str(s)]
        pod = (row.get("pod") or {}).get("late", {})
        pers = pod.get("persist") or []
        def pr(k):
            if k >= len(pers):
                return "omitido"
            return fmt(pers[k].get("std_over_mean"))
        acf = pod.get("acf_time_c0")
        acf_s = fmt(acf) if acf is not None else "undefined"
        a(f"| {s} | {pr(0)} | {pr(1)} | {pr(2)} | {acf_s} |")
    a("")
    a("## DMD |λ| (late, r_dmd=8 fixo, seeds 0 e 1)")
    a("")
    for s in (0, 1):
        row = payload["per_seed"][str(s)]
        vals = (row.get("pod") or {}).get("dmd_abs_lambda")
        if not vals:
            a(f"- seed {s}: omitido")
        else:
            a("- seed %d: %s" % (s, ", ".join(fmt(v) for v in vals)))
    a("")
    a("## Veredito")
    a("")
    a(f"- n_finite = {payload['n_finite']} / 4; n_blowup = {payload['n_blowup']}")
    a(f"- early (contexto, **não** oficial): EV8={fmt(payload['ev8_early'])} Rec8={fmt(payload['rec8_early'])} Ov={fmt(payload['ov_phi0_early'])} → **{payload['verdict_early_context']}**")
    a(f"- late (oficial, atrator): EV8={fmt(payload['ev8_late'])} Rec8={fmt(payload['rec8_late'])} Ov={fmt(payload['ov_phi0_late'])} → **{payload['verdict']}**")
    a(f"- supported_for_qm = false (nunca SUPPORTED para MQ)")
    a("")
    a(payload.get("verdict_why", ""))
    a("")
    a("Regras (pré-declaradas, não movidas): late EV8≥0.50 e Rec8≤0.30 e Ov≥0.50 → PARTIAL;")
    a("EV8<0.20 e Rec8>0.50 → NOT_SUPPORTED; senão INCONCLUSIVE; >1 blowup → NUMERICAL_FAILURE.")
    a("Janela early não define o veredito oficial.")
    a("")
    a("## Notas")
    a("")
    a("- Sem comparação MQ.")
    a("- Theta_core intocado.")
    a("- Backend mlx (fallback numpy fp32 só se mlx falhar; registrado).")
    a("- Sem Simulações run 35.")
    a("- Caixa preenchida = universo.")
    a("")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def rec_of(pod, r):
    if not pod or not pod.get("ok"):
        return None
    rec = pod.get("rec") or {}
    if r in rec:
        return rec[r]
    if str(r) in rec:
        return rec[str(r)]
    return None


def main():
    started = now_sp()
    t0 = time.perf_counter()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "raw").mkdir(parents=True, exist_ok=True)
    (OUT / "figures").mkdir(parents=True, exist_ok=True)

    proto = None
    for p in PROTOCOL_PATHS:
        if p.is_file():
            proto = p
            break
    protocol_sha = sha256_file(proto) if proto is not None else PROTOCOL_SHA_KNOWN
    solver_sha = sha256_file(Path(__file__))

    backend = BACKEND
    device_s = "numpy-cpu"
    if backend == "mlx" and MLX_OK:
        try:
            mx.set_default_device(mx.gpu)
            device_s = str(mx.default_device())
            _probe = mx.ones((4, 4), dtype=mx.complex64)
            mx.eval(_probe)
            print("mlx_ok", device_s, flush=True)
        except Exception as exc:
            print("mlx_device_failed", exc, "fallback numpy fp32", flush=True)
            backend = "numpy"
            device_s = "numpy-cpu"
    else:
        backend = "numpy"
        print("backend_numpy_fp32", flush=True)

    geom = build_state(NGRID)
    print(
        "Q03 start", started, "backend", backend, "device", device_s,
        "protocol", protocol_sha, "solver", solver_sha, flush=True,
    )

    by_seed = {}
    for seed in SEEDS:
        sp = OUT / "raw" / f"seed{seed:02d}_summary.json"
        phi_ok = (OUT / "raw" / f"seed{seed:02d}_phi0_late.npy").is_file()
        if sp.is_file() and phi_ok:
            with sp.open() as f:
                summary = json.load(f)
            print(f"seed={seed:02d} resume from {sp} finite={summary.get('finite')}", flush=True)
        else:
          try:
            summary = run_one(seed, geom, backend)
          except Exception as exc:
            print("SEED_EXCEPTION", seed, exc, flush=True)
            traceback.print_exc()
            summary = {
                "seed": seed,
                "finite": False,
                "blew_up": True,
                "blow_t": "exception",
                "wall_s": None,
                "wall_evolve_s": None,
                "pod": {"early": {"ok": False}, "late": {"ok": False}},
                "peak_late_mean": float("nan"),
                "PR_late_mean": float("nan"),
                "R_rms_late_mean": float("nan"),
                "norm_late_mean": float("nan"),
                "exception": str(exc),
            }
        q2 = load_q02_late(seed)
        if q2:
            summary["q02"] = {
                "peak_late_mean": q2.get("peak_late_mean"),
                "PR_late_mean": q2.get("PR_late_mean"),
                "R_rms_late_mean": q2.get("R_rms_late_mean"),
                "norm_late_mean": q2.get("norm_late_mean"),
            }
        by_seed[seed] = summary

    n_resumed = sum(
        1
        for s in SEEDS
        if (OUT / "raw" / f"seed{s:02d}_phi0_late.npy").is_file()
        and (OUT / "raw" / f"seed{s:02d}_summary.json").is_file()
    )
    if n_resumed == len(SEEDS):
        started = "2026-08-21 14:08:16 BRT"
        print("resume_all_seeds physics_started", started, flush=True)

    finite_seeds = [s for s in SEEDS if by_seed[s].get("finite")]
    blow_seeds = [s for s in SEEDS if by_seed[s].get("blew_up")]
    n_finite = len(finite_seeds)
    n_blow = len(blow_seeds)

    dV = geom["dV"]
    pairs_early, ov_early = pairwise_overlaps(finite_seeds, "early", dV)
    pairs_late, ov_late = pairwise_overlaps(finite_seeds, "late", dV)

    ev8_early = mean_of(
        [(by_seed[s].get("pod") or {}).get("early", {}).get("ev8") for s in finite_seeds]
    )
    ev8_late = mean_of(
        [(by_seed[s].get("pod") or {}).get("late", {}).get("ev8") for s in finite_seeds]
    )
    rec8_early = mean_of(
        [rec_of((by_seed[s].get("pod") or {}).get("early"), 8) for s in finite_seeds]
    )
    rec8_late = mean_of(
        [rec_of((by_seed[s].get("pod") or {}).get("late"), 8) for s in finite_seeds]
    )
    ic_early = mean_of(
        [
            (by_seed[s].get("pod") or {}).get("early", {}).get("ic_overlap")
            for s in finite_seeds
        ]
    )
    ic_late = mean_of(
        [
            (by_seed[s].get("pod") or {}).get("late", {}).get("ic_overlap")
            for s in finite_seeds
        ]
    )

    verdict = apply_verdict(ev8_late, rec8_late, ov_late, n_finite, n_blow)
    verdict_early = apply_verdict(ev8_early, rec8_early, ov_early, n_finite, n_blow)

    why_bits = []
    if n_blow > 1:
        why_bits.append(
            "Mais de uma seed NaN/blowup → NUMERICAL_FAILURE (regra pré-declarada)."
        )
    else:
        why_bits.append(
            "Veredito oficial = janela late (atrator). Early é só contexto "
            "e não promove o átomo visível/morrendo a estado de MQ."
        )
        why_bits.append(
            f"Late: EV8={fmt(ev8_late)} Rec8={fmt(rec8_late)} Ov={fmt(ov_late)} "
            f"com regras EV8≥0.50∧Rec8≤0.30∧Ov≥0.50→PARTIAL; "
            f"EV8<0.20∧Rec8>0.50→NOT_SUPPORTED; senão INCONCLUSIVE."
        )
        why_bits.append("Nunca SUPPORTED para MQ. Theta_core intocado. Sem comparação MQ.")
    verdict_why = " ".join(why_bits)

    fig_paths = make_figures(finite_seeds, by_seed, ov_early, ov_late)

    dmd_map = {}
    for s in (0, 1):
        vals = (by_seed.get(s, {}).get("pod") or {}).get("dmd_abs_lambda")
        if vals:
            dmd_map[str(s)] = vals

    peaks = [
        by_seed[s].get("peak_max")
        for s in SEEDS
        if by_seed[s].get("peak_max") is not None
    ]
    peak_max_global = None
    peak_max_seed = None
    peak_max_t = None
    best = -1.0
    for s in SEEDS:
        pm = by_seed[s].get("peak_max")
        if pm is not None and np.isfinite(pm) and float(pm) > best:
            best = float(pm)
            peak_max_global = float(pm)
            peak_max_seed = int(s)
            peak_max_t = by_seed[s].get("peak_max_t")

    finished = now_sp()
    analysis_s = time.perf_counter() - t0
    phys_s = 0.0
    for s in SEEDS:
        ws = by_seed[s].get("wall_s")
        if ws is not None and np.isfinite(ws):
            phys_s += float(ws)
    wall_total = phys_s + analysis_s if n_resumed == len(SEEDS) else analysis_s

    per_seed = {str(s): jsonable(by_seed[s]) for s in SEEDS}

    payload = {
        "question": "A dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?",
        "id": "Q03",
        "verdict": verdict,
        "verdict_early_context": verdict_early,
        "verdict_why": verdict_why,
        "qm_comparison": False,
        "theta_core_unchanged": True,
        "terms_isolated": False,
        "n_seeds": 4,
        "n_finite": n_finite,
        "n_blowup": n_blow,
        "excluded_seeds": blow_seeds,
        "ev8_late": ev8_late,
        "rec8_late": rec8_late,
        "ov_phi0_late": ov_late,
        "ev8_early": ev8_early,
        "rec8_early": rec8_early,
        "ov_phi0_early": ov_early,
        "ic_overlap_late": ic_late,
        "ic_overlap_early": ic_early,
        "dmd_abs_lambda": dmd_map,
        "pairwise_early": pairs_early,
        "pairwise_late": pairs_late,
        "peak_max": peak_max_global,
        "peak_max_t": peak_max_t,
        "peak_max_seed": peak_max_seed,
        "backend": backend,
        "precision": PRECISION,
        "device": device_s,
        "protocol_sha256": protocol_sha,
        "solver_sha256": solver_sha,
        "canonical_sha256": CANONICAL_SHA,
        "q02_solver_sha256": Q02_SOLVER_SHA,
        "q02_protocol_v2_sha256": Q02_PROTOCOL_V2_SHA,
        "supported_for_qm": False,
        "pilots_1_34_confirmatory": False,
        "started_america_sao_paulo": started,
        "finished_america_sao_paulo": finished,
        "wall_total_s": wall_total,
        "workers": 1,
        "windows": {"early": "t<=0.2", "late": "t>=6.4"},
        "r_dmd": R_DMD,
        "snap_every": SNAP_EVERY,
        "seeds": list(SEEDS),
        "figures": fig_paths,
        "per_seed": per_seed,
        "out": str(OUT),
    }

    result = {k: jsonable(v) for k, v in payload.items()}
    with (OUT / "result.json").open("w") as f:
        json.dump(result, f, indent=2)
    with (TMP_ROOT / "result.json").open("w") as f:
        json.dump(result, f, indent=2)

    write_analysis(OUT / "analysis.md", payload)
    write_analysis(TMP_ROOT / "analysis.md", payload)

    config = {
        "question": "Q03",
        "title": "identificação de subespaços persistentes (POD/DMD passivos)",
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
        "box": {"L": LBOX, "N": NGRID, "dt": DT, "T": T_FINAL, "V_ext": V_EXT, "domain": "[-L/2, L/2)^3"},
        "initial_condition": {
            "type": "I0_single_gaussian_atom",
            "spec": "§9.1",
            "s": INIT_SIGMA,
            "k0": list(INIT_K0),
            "norm": 1.0,
            "y0": Y0,
            "note": "1 gaussiana = 1 átomo; I0 permitido; não é scan",
        },
        "fdt": {
            "f_FDT_e": "2*Gamma*(dx**3)*kT/hbar",
            "increment": "spec eq 4",
            "rng": "numpy.random.default_rng(seed) then upload mlx complex64",
        },
        "numerics": {
            "fp": "fp32",
            "precision": PRECISION,
            "memory": "float32",
            "backend": backend,
            "device": device_s,
            "solver": "standalone 3D Strang mlx GPU (mesmo passo Q02)",
            "memory_update": "euler",
            "record_every": RECORD_EVERY,
            "snap_every": SNAP_EVERY,
            "n_snap": int(round(T_FINAL / DT)) // SNAP_EVERY + 1,
            "python": "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3",
            "workers": 1,
            "neural_engine": False,
        },
        "seeds": list(SEEDS),
        "windows": {
            "early": {"rule": "t <= 0.2", "t_max": T_EARLY, "note": "átomo ainda visível / morrendo — medição"},
            "late": {"rule": "last 20% of T", "t_min": T_LATE, "T": T_FINAL, "note": "universo preenchido; janela Q00"},
        },
        "analysis": {
            "pod": "economy SVD of n_snap x n_snap Gram of real-imag stacked centered field",
            "dmd": "standard SVD-DMD on centered late snapshots",
            "r_dmd": R_DMD,
            "r_dmd_fixed_before_run": True,
            "modes_fed_to_solver": False,
        },
        "verdict_rule": {
            "gt_1_of_4_blowup": "NUMERICAL_FAILURE",
            "late_ev8_ge_0.50_and_rec8_le_0.30_and_ov_ge_0.50": "PARTIAL",
            "late_ev8_lt_0.20_and_rec8_gt_0.50": "NOT_SUPPORTED",
            "otherwise": "INCONCLUSIVE",
            "early_does_not_set_official_verdict": True,
            "supported_for_qm": False,
            "no_aesthetic_drop": True,
        },
        "q02_solver_sha256": Q02_SOLVER_SHA,
        "q02_protocol_v2_sha256": Q02_PROTOCOL_V2_SHA,
        "solver_sha256": solver_sha,
        "executed": str(Path(__file__).resolve()),
    }
    with (OUT / "config.json").open("w") as f:
        json.dump(config, f, indent=2)
    with (TMP_ROOT / "config.json").open("w") as f:
        json.dump(config, f, indent=2)

    q03md = (
        "---\n"
        "tags: [triad, qm, q03, subespacos]\n"
        "aliases: [Q03]\n"
        "status: active\n"
        "data: 2026-08-21\n"
        "---\n\n"
        "# Q03 — Identificação de subespaços persistentes (POD/DMD passivos)\n\n"
        "Lote **Q03** (este diretório): seeds 0,1,2,3 (nessa ordem; primeiras quatro de Q02), "
        "mesmo macroestado físico (1 gaussiana = 1 átomo), tríade completa, N=64, dt=0.0025, "
        "T=8, L=32, Theta_core congelado. Análise passiva POD/PCA + DMD. "
        "Snapshots são sensores; **não** controlam o solver.\n\n"
        f"Backend **{backend}**, campo complex64, memória float32. N_num, não calibração. "
        "**Nunca** SUPPORTED para MQ.\n\n"
        "Protocolo: [[PROTOCOL]]. Canônico: [[TRIAD_QM_CANONICAL_V1]] (Q00).\n"
        "Q02: [[Q02]] — INCONCLUSIVE. Q01a/Q01b: [[Q01]] / [[Q01b]].\n\n"
        "Pergunta: a dinâmica completa produz modos/coordenadas macroscópicas "
        "que mantêm identidade suficiente para serem tratados como estados?\n"
        "Sem comparação com MQ. Sem isolar termos. Sem cherry-pick. "
        "Pilotos 1–34 não confirmatórios.\n\n"
        f"SHA-256 PROTOCOL: `{protocol_sha}`\n"
        f"SHA-256 do solver executado `code/run_q03.py`: `{solver_sha}`\n"
        f"SHA-256 passo Q02: `{Q02_SOLVER_SHA}`\n"
        f"SHA-256 canônico Q00: `{CANONICAL_SHA}`\n\n"
        f"Veredito Q03 (janela late / atrator): **{verdict}**. "
        f"Early (contexto): **{verdict_early}**. "
        "Q03 **não** é teste de MQ. Nunca SUPPORTED para MQ. "
        "Detalhe em [[analysis]] e `result.json`.\n\n"
        f"Início {started}; fim {finished}; wall {wall_total:.2f} s (1 GPU, sequencial).\n"
    )
    (OUT / "Q03.md").write_text(q03md, encoding="utf-8")
    (TMP_ROOT / "Q03.md").write_text(q03md, encoding="utf-8")

    # SHA256SUMS of artifacts (not the deleted memmaps)
    sum_path = OUT / "SHA256SUMS.txt"
    lines = []
    candidates = []
    for p in (
        proto,
        Path(__file__),
        OUT / "result.json",
        OUT / "analysis.md",
        OUT / "config.json",
        OUT / "Q03.md",
    ):
        if p is not None and p.is_file():
            candidates.append(p)
    for p in sorted((OUT / "figures").glob("*.png")):
        candidates.append(p)
    for p in sorted((OUT / "raw").glob("seed*_summary.json")):
        candidates.append(p)
    for p in sorted((OUT / "raw").glob("seed*_metrics.csv")):
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

    print(
        "Q03_DONE",
        "verdict", verdict,
        "verdict_early", verdict_early,
        "ev8_late", ev8_late,
        "rec8_late", rec8_late,
        "ov_late", ov_late,
        "ev8_early", ev8_early,
        "rec8_early", rec8_early,
        "ov_early", ov_early,
        "n_finite", n_finite,
        "backend", backend,
        "wall", wall_total,
        flush=True,
    )


if __name__ == "__main__":
    main()
