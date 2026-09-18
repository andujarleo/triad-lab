#!/usr/bin/env python3
"""Q02 — ensemble caótico de referência (32 seeds, 1 átomo, tríade completa).

PROTOCOL_v2: backend mlx GPU, campo complex64, memória float32.
Passo Strang idêntico a Fontes/run_q01a.py
(SHA-256 abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64).
Ruído FDT sorteado com numpy.random.default_rng(seed) e enviado ao GPU.

Pergunta: qual é a distribuição natural de comportamentos do substrato
sem escolher uma seed bonita?
Sem comparação com MQ. Sem isolar termos. Sem mudar Theta_core.
1 gaussiana = 1 átomo. Volume preenchido = universo.
Pilotos 1–34 não são confirmatórios.
Nunca SUPPORTED para MQ.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mlx.core as mx
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
Q02_DIR = VAULT / "QM" / "Q02_ensemble"
FONTES = VAULT / "Fontes"
FALLBACK = Path("/tmp/Q02_ensemble/out")
PROTOCOL_V1_PATH = Q02_DIR / "PROTOCOL.md"
PROTOCOL_V2_PATH = Q02_DIR / "PROTOCOL_v2.md"
PROTOCOL_V1_FALLBACK = Path("/tmp/Q02_ensemble/PROTOCOL.md")
PROTOCOL_V2_FALLBACK = Path("/tmp/Q02_ensemble/PROTOCOL_v2.md")

# --- Theta_core (Q00 / TRIAD_QM_CANONICAL_V1) — IMUTÁVEL ---
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

# --- N_num / caixa (célula de trabalho Q01a N=64, NÃO calibração) ---
LBOX = 32.0
NGRID = 64
DT = 0.0025
T_FINAL = 8.0
SEEDS = tuple(range(32))
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 40
K_CUT_FACTOR = 1.0
BACKEND = "mlx"
PRECISION = "complex64"
DTYPE_PSI_NP = np.complex64
DTYPE_R_NP = np.float32
Q01A_SOLVER_SHA = "abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64"
CANONICAL_SHA = "e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e"
PROTOCOL_V1_SHA_KNOWN = "a2024aff5e29c484ed781f6972d1699f4657997072c528333f1268b95cb648af"
LATE_FRAC = 0.8
BOX_HALF = LBOX / 2.0
FILL_ABS = 1.0
FILL_REL = 0.9
SETTLE_REL = 0.05
PRINT_EVERY_T = 2.0

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


def resolve_out() -> Path:
    try:
        Q02_DIR.mkdir(parents=True, exist_ok=True)
        test = Q02_DIR / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink()
        return Q02_DIR
    except Exception as exc:
        print("vault_blocked", exc, "fallback", FALLBACK, flush=True)
        FALLBACK.mkdir(parents=True, exist_ok=True)
        return FALLBACK


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def find_file(*cands: Path) -> Path | None:
    for p in cands:
        if p.is_file():
            return p
    return None


def protocol_sha(kind: str) -> str:
    if kind == "v1":
        p = find_file(PROTOCOL_V1_PATH, PROTOCOL_V1_FALLBACK)
    else:
        p = find_file(PROTOCOL_V2_PATH, PROTOCOL_V2_FALLBACK)
    return sha256_file(p) if p is not None else ""


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


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def spectral_observables(psi, k_mag, dk, k_cut):
    """§8.3 potência radial de Psi-hat, k* e crystallinity C."""
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
    """psi *= exp(-i * theta); theta real."""
    c = mx.cos(theta)
    s = mx.sin(theta)
    re = mx.real(psi)
    im = mx.imag(psi)
    nre = re * c + im * s
    nim = im * c - re * s
    return nre.astype(mx.complex64) + (1j * nim.astype(mx.complex64))


def strang_step_mlx(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
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


def run_one(seed: int, raw_dir: str, gpu_arrays: dict) -> dict:
    t_wall0 = time.perf_counter()
    N = NGRID
    dx = gpu_arrays["dx"]
    dV = gpu_arrays["dV"]
    r2 = gpu_arrays["r2"]
    r = gpu_arrays["r"]
    k_mag = gpu_arrays["k_mag"]
    half_lin = gpu_arrays["half_lin"]
    nu = gpu_arrays["nu"]
    lam = gpu_arrays["lam"]
    lam_np = gpu_arrays["lam_np"]
    noise_amp = gpu_arrays["noise_amp"]
    f_FDT = gpu_arrays["f_FDT"]
    psi0 = gpu_arrays["psi0"]
    y0 = gpu_arrays["y0"]
    shape = gpu_arrays["shape"]

    psi = mx.array(psi0)
    y = mx.array(y0)
    mx.eval(psi, y)

    rng = np.random.default_rng(seed)
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    n_steps = int(round(T_FINAL / DT))
    rec_every = max(1, RECORD_EVERY)
    raw = Path(raw_dir)
    raw.mkdir(parents=True, exist_ok=True)

    print(f"=== Q02 seed={seed:02d} N={N} start backend={BACKEND} {PRECISION} ===", flush=True)
    print(
        f"seed={seed:02d} device {mx.default_device()} L {LBOX} dx {dx} dt {DT} T {T_FINAL} "
        f"n_steps {n_steps} f_FDT {f_FDT} noise_amp {noise_amp} "
        f"max_nu_dt {float(max(NU) * DT)}",
        flush=True,
    )

    metrics = []
    blew = False
    blow_t = None
    peak_max = float("-inf")
    peak_max_t = None
    last_print_bucket = -1
    for step in range(n_steps + 1):
        t = step * DT
        if step % rec_every == 0 or step == n_steps:
            psi_np = np.array(psi)
            y_np = np.array(y)
            rho, rec = record_metrics(psi_np, y_np, t, dV, dx, r2, r, k_mag, dk, k_cut, lam_np)
            rec["seed"] = seed
            rec["N"] = N
            rec["dx"] = dx
            rec["backend"] = BACKEND
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
                break
        if step == n_steps or blew:
            break
        psi, y = strang_step_mlx(psi, y, half_lin, noise_amp, rng, nu, lam, shape)

    wall = time.perf_counter() - t_wall0
    csv_path = raw / f"seed{seed:02d}_metrics.csv"
    if metrics:
        write_csv(csv_path, metrics, list(metrics[0].keys()))

    t_arr = series_of(metrics, "t") if metrics else np.array([], dtype=np.float64)
    t_late = LATE_FRAC * T_FINAL
    last = metrics[-1] if metrics else {}
    finite_final = bool(last.get("finite", False)) and (not blew)

    summary = {
        "question": "Q02",
        "seed": seed,
        "N": N,
        "L": LBOX,
        "dx": dx,
        "dt": DT,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "record_every": rec_every,
        "backend": BACKEND,
        "precision": PRECISION,
        "fp": "fp32",
        "solver": "standalone 3D Strang mlx GPU (mesmo passo Q01a; não triad-lang)",
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
        "wall_s": wall,
        "blew_up": blew,
        "blow_t": blow_t,
        "finite": finite_final,
        "finite_final": finite_final,
        "csv": str(csv_path),
        "peak_max": peak_max if math.isfinite(peak_max) and peak_max > float("-inf") else float("nan"),
        "peak_max_t": peak_max_t,
    }
    for key in OBS_LATE:
        lm, ls, ln = late_stats(metrics, key, t_arr, t_late) if metrics else (float("nan"), float("nan"), 0)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln

    t_settle, t_fill = empirical_transient(metrics, summary.get("R_rms_late_mean", float("nan")))
    summary["t_settle"] = t_settle
    summary["t_fill"] = t_fill
    rlate = summary.get("R_rms_late_mean", float("nan"))
    summary["box_filled"] = bool(np.isfinite(rlate) and abs(rlate - BOX_HALF) <= FILL_ABS)

    print(
        f"seed={seed:02d} done wall_s={wall:.3f} finite={finite_final} "
        f"blew={blew} blow_t={blow_t} "
        f"peak_late={summary['peak_late_mean']:.6g} "
        f"PR_late={summary['PR_late_mean']:.6g} "
        f"Rrms_late={summary['R_rms_late_mean']:.6g} "
        f"t_settle={t_settle} t_fill={t_fill} box_filled={summary['box_filled']}",
        flush=True,
    )
    with (raw / f"seed{seed:02d}_summary.json").open("w") as f:
        json.dump(jsonable(summary), f, indent=2)
    return summary


def ensemble_of_late(rows, key):
    vals = np.array([r[key] for r in rows], dtype=np.float64)
    vals = vals[np.isfinite(vals)]
    if vals.size == 0:
        return {"mean": None, "std": None, "min": None, "max": None, "median": None, "n": 0}
    return {
        "mean": float(vals.mean()),
        "std": float(vals.std(ddof=0)),
        "min": float(vals.min()),
        "max": float(vals.max()),
        "median": float(np.median(vals)),
        "n": int(vals.size),
    }


def finite_list(vals):
    return [float(v) for v in vals if v is not None and np.isfinite(v)]


def make_figures(out: Path, by_seed: dict, finite_seeds: list):
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    keys_panels = [
        ("norm", "norma"),
        ("peak", "peak ρ  (ρ_max)"),
        ("PR", "PR  (participação)"),
        ("R_rms", "R_rms"),
    ]
    series = {k: [] for k, _ in keys_panels}
    t_ref = None
    for seed in finite_seeds:
        mets = by_seed[seed]["metrics"]
        t = np.array([m["t"] for m in mets], dtype=np.float64)
        if t_ref is None or (t.size > 0 and (t_ref.size == 0 or t.size >= t_ref.size)):
            t_ref = t
        for k, _ in keys_panels:
            series[k].append((t, np.array([m[k] for m in mets], dtype=np.float64)))

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
    for ax, (key, title) in zip(axes.ravel(), keys_panels):
        if t_ref is None or t_ref.size == 0:
            ax.set_title(title + " (sem série)")
            continue
        mat = []
        for t, v in series[key]:
            if t.size == t_ref.size and np.allclose(t, t_ref):
                mat.append(v)
            else:
                vv = np.full(t_ref.shape, np.nan)
                idx = {float(tt): i for i, tt in enumerate(t)}
                for j, tt in enumerate(t_ref):
                    if float(tt) in idx:
                        vv[j] = v[idx[float(tt)]]
                mat.append(vv)
        M = np.vstack(mat) if mat else np.array([[]])
        mean = np.nanmean(M, axis=0)
        std = np.nanstd(M, axis=0, ddof=0)
        ax.plot(t_ref, mean, color="C0", lw=1.6, label="média ensemble")
        ax.fill_between(t_ref, mean - std, mean + std, color="C0", alpha=0.28, label="±1 std")
        ax.axvspan(0.8 * T_FINAL, T_FINAL, color="0.85", alpha=0.5, zorder=0)
        ax.set_title(title)
        ax.set_xlabel("t")
        ax.grid(True, alpha=0.3)
        if ax is axes[0, 0]:
            ax.legend(fontsize=8)
    fig.suptitle(
        "Q02 — ensemble 32 seeds, tríade completa, Theta_core, mlx GPU fp32  (sem comparação MQ)\n"
        "1 gaussiana = 1 átomo; volume preenchido = universo; CAOS → EQUILÍBRIO DINÂMICO"
    )
    fig.tight_layout()
    fig.savefig(fig_dir / "overlay_observables.png", dpi=150)
    plt.close(fig)

    hist_keys = [
        ("peak_late_mean", "peak tardio"),
        ("PR_late_mean", "PR tardio"),
        ("R_rms_late_mean", "R_rms tardio"),
        ("norm_late_mean", "norma tardia"),
        ("k_star_late_mean", "k* tardio"),
        ("Vmem_peak_late_mean", "Vmem_peak tardio"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(12.6, 7.4))
    for ax, (key, title) in zip(axes.ravel(), hist_keys):
        vals = []
        for seed in finite_seeds:
            v = by_seed[seed]["summary"].get(key, float("nan"))
            if v is not None and np.isfinite(v):
                vals.append(float(v))
        if not vals:
            ax.set_title(title + " (vazio)")
            continue
        ax.hist(vals, bins=min(8, max(4, int(np.sqrt(len(vals))))), color="C0", edgecolor="0.2", alpha=0.85)
        ax.axvline(float(np.median(vals)), color="C3", ls="--", lw=1.2, label="mediana")
        ax.set_title(title)
        ax.set_xlabel("média janela tardia")
        ax.set_ylabel("n seeds")
        ax.grid(True, axis="y", alpha=0.3)
        ax.legend(fontsize=7)
    fig.suptitle("Q02 — distribuições das médias tardias (seeds finitas; mlx GPU; sem cherry-pick)")
    fig.tight_layout()
    fig.savefig(fig_dir / "late_distributions.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(3, 1, figsize=(11.0, 8.2), sharex=True)
    xs = np.arange(32)
    strip = [
        ("peak_late_mean", "peak tardio"),
        ("R_rms_late_mean", "R_rms tardio"),
        ("PR_late_mean", "PR tardio"),
    ]
    finite_set = set(finite_seeds)
    for ax, (key, title) in zip(axes, strip):
        ys = []
        colors = []
        for s in xs:
            if int(s) in finite_set:
                v = by_seed[int(s)]["summary"].get(key, float("nan"))
                ys.append(v if v is not None else np.nan)
                colors.append("C0")
            else:
                ys.append(np.nan)
                colors.append("C3")
        ax.scatter(xs, ys, c=colors, s=28, zorder=3)
        ax.plot(xs, ys, color="0.6", lw=0.8, zorder=2)
        ax.set_ylabel(title)
        ax.grid(True, alpha=0.3)
        ax.set_xticks(list(xs))
    axes[-1].set_xlabel("seed (0–31, ordem; nenhuma dropada por estética)")
    axes[0].set_title("Q02 — faixa por seed (mostra ausência de cherry-pick)")
    fig.suptitle("Q02 — 1 gaussiana = 1 átomo; volume preenchido = universo; backend mlx GPU")
    fig.tight_layout()
    fig.savefig(fig_dir / "seed_strip.png", dpi=150)
    plt.close(fig)


def classify(n_finite, n_blowup, ensemble_late):
    reasons = []
    finite_stds = []
    for key in ("peak", "PR", "R_rms"):
        st = ensemble_late.get(key, {})
        std = st.get("std")
        if std is None or not np.isfinite(std):
            reasons.append(f"{key} std da distribuição das médias tardias não-finito")
        else:
            finite_stds.append(float(std))
    well_defined = (len(finite_stds) == 3) and all(math.isfinite(s) for s in finite_stds)
    if n_blowup > 4:
        verdict = "NUMERICAL_FAILURE"
        note = (
            f"{n_blowup} seeds NaN/blowup (>4). Falha numérica do lote. "
            "Nunca SUPPORTED para MQ."
        )
    elif n_finite >= 30 and well_defined:
        verdict = "INCONCLUSIVE"
        note = (
            f"Ensemble OK: {n_finite}/32 finitas e peak/PR/R_rms tardios têm "
            "distribuição bem definida (std finito). Q02 não é teste de MQ → INCONCLUSIVE. "
            "Backend mlx GPU fp32 (PROTOCOL_v2). Nunca SUPPORTED para MQ."
        )
    elif n_finite >= 28 and well_defined:
        verdict = "PARTIAL"
        note = (
            f"{n_finite}/32 finitas com distribuição definida, abaixo do limiar 30/32. "
            "Ainda não é MQ. Backend mlx GPU fp32 (PROTOCOL_v2). Nunca SUPPORTED para MQ."
        )
    else:
        verdict = "INCONCLUSIVE"
        note = (
            f"{n_finite}/32 finitas, n_blowup={n_blowup}. Distribuição "
            f"{'definida' if well_defined else 'incompleta'}. Q02 não é teste de MQ. "
            "Backend mlx GPU fp32 (PROTOCOL_v2). Nunca SUPPORTED para MQ."
        )
    return {
        "verdict": verdict,
        "note": note,
        "reasons": reasons,
        "well_defined_distribution": well_defined,
        "qm_comparison": False,
        "supported_for_qm": False,
    }


def fmt_pm(m, e):
    if m is None or not np.isfinite(m):
        return "omitido"
    if e is None or not np.isfinite(e):
        return f"{m:.6g}"
    return f"{m:.6g} ± {e:.3g}"


def fmt_num(v):
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return "omitido"
    return f"{v:.6g}"


def write_analysis(out, rows, classif, ensemble_late, extra, started, finished):
    n_finite = extra["n_finite"]
    n_blowup = extra["n_blowup"]
    excluded = extra["excluded_seeds"]
    lines = []
    lines.append("# Q02 — Análise (ensemble caótico de referência)")
    lines.append("")
    lines.append("Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.")
    lines.append("Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.")
    lines.append("Theta_core intocado (Q00). Sem cherry-pick de seed.")
    lines.append("Backend **mlx GPU**, campo complex64, memória float32 (PROTOCOL_v2). N_num, não física.")
    lines.append("Este lote exploratório **não** é SUPPORTED para MQ.")
    lines.append("")
    lines.append("## Pergunta")
    lines.append("")
    lines.append("Qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Theta_core: Λ={LAMBDA}, α={ALPHA}, σ={SIGMA_FRAC}, Γ={GAMMA}, ν={NU}, λ={LAM}, kT={KT}")
    lines.append(
        f"- L={LBOX}, N={NGRID}, dt={DT}, T={T_FINAL}, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0"
    )
    lines.append("- FDT: f_FDT,e=2Γ dx³ kT/ℏ ; incremento spec eq. 4 (RNG numpy, upload GPU)")
    lines.append("- seeds 0–31 nessa ordem; complex64/float32; backend mlx GPU; Strang standalone")
    lines.append("- 1 gaussiana = 1 átomo; célula de trabalho Q01a (NÃO calibração)")
    lines.append(f"- PROTOCOL v1 (histórico numpy/fp64): `{extra['protocol_v1_sha256']}`")
    lines.append(f"- PROTOCOL v2 (este lote): `{extra['protocol_v2_sha256']}`")
    lines.append(f"- início (America/Sao_Paulo): {started}")
    lines.append(f"- fim (America/Sao_Paulo): {finished}")
    lines.append(f"- wall total: {extra['wall_total_s']:.3f} s ({extra['wall_total_s']/60.0:.3f} min)")
    lines.append(f"- device: {extra['device']}")
    lines.append("")
    lines.append("## Tempos de parede por seed")
    lines.append("")
    lines.append("| seed | wall_s | finito | blow_t | box_filled | t_settle | t_fill |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        bt = r["blow_t"] if r["blow_t"] is not None else "—"
        ts = fmt_num(r["t_settle"]) if r["t_settle"] is not None else "never"
        tf = fmt_num(r["t_fill"]) if r["t_fill"] is not None else "never"
        lines.append(
            f"| {r['seed']} | {r['wall_s']:.3f} | {r['finite']} | {bt} | "
            f"{r['box_filled']} | {ts} | {tf} |"
        )
    lines.append("")
    lines.append("## Janela tardia entre seeds (t ≥ 0.8 T = 6.4)")
    lines.append("")
    lines.append("Estatística **das médias tardias por seed** (variabilidade natural):")
    lines.append("")
    lines.append("| observável | média ensemble | std | min | max | mediana | n |")
    lines.append("|---|---|---|---|---|---|---|")
    for key in OBS_LATE:
        st = ensemble_late[key]
        lines.append(
            f"| {key} | {fmt_num(st['mean'])} | {fmt_num(st['std'])} | "
            f"{fmt_num(st['min'])} | {fmt_num(st['max'])} | {fmt_num(st['median'])} | {st['n']} |"
        )
    lines.append("")
    lines.append("## Transiente empírico (medição, não lei nova)")
    lines.append("")
    et = extra["empirical_transient"]
    lines.append(
        "Primeiro t tal que |R_rms(t) − R_rms_late| < 0.05·|R_rms_late| e permanece até T."
    )
    lines.append(
        f"- t_settle: mediana={fmt_num(et['t_settle']['median'])}, "
        f"min={fmt_num(et['t_settle']['min'])}, max={fmt_num(et['t_settle']['max'])}, "
        f"n={et['t_settle']['n']}, n_never={et['t_settle']['n_never']}"
    )
    lines.append("Primeiro t com R_rms > 0.9·(L/2) = 14.4.")
    lines.append(
        f"- t_fill: mediana={fmt_num(et['t_fill']['median'])}, "
        f"min={fmt_num(et['t_fill']['min'])}, max={fmt_num(et['t_fill']['max'])}, "
        f"n={et['t_fill']['n']}, n_never={et['t_fill']['n_never']}"
    )
    lines.append("")
    lines.append(
        "Janela Q00 (provisória, já congelada): transiente t < 0.8 T; equilíbrio último 20% "
        "(t ≥ 6.4). Q02 mede se isso é empiricamente ok; **não** redesenha a lei."
    )
    lines.append("")
    lines.append("## Fração caixa preenchida (universo)")
    lines.append("")
    lines.append("- critério: |R_rms_late − L/2| ≤ 1, com L/2 = 16")
    lines.append(
        f"- n_filled / n_finite = {extra['n_filled']} / {n_finite} "
        f"= {fmt_num(extra['fraction_box_filled'])}"
    )
    lines.append(
        f"- n_filled / 32 = {extra['n_filled']} / 32 = {fmt_num(extra['fraction_box_filled_all'])}"
    )
    lines.append("Volume preenchido = universo, **não** ruído, **não** “átomos morreram no banho”.")
    lines.append("")
    lines.append("## Anti-colapso (singularidade finita)")
    lines.append("")
    lines.append(
        f"- peak_max_global = {fmt_num(extra['peak_max_global'])} "
        f"em t={fmt_num(extra['peak_max_t'])}, seed={extra['peak_max_seed']}"
    )
    lines.append("")
    lines.append("## k* vs Nyquist")
    lines.append("")
    kn = extra["k_nyquist"]
    ks = extra["k_star_late_mean"]
    lines.append(f"- k_Nyq = π√3 / dx, dx=0.5 → {fmt_num(kn)}")
    lines.append(f"- k*_late média ensemble = {fmt_num(ks)}")
    lines.append(f"- |k* − k_Nyq| / k_Nyq = {fmt_num(extra['k_star_rel_nyquist'])}")
    lines.append(f"- k*_on_nyquist = {extra['k_star_on_nyquist']}")
    lines.append(extra["k_star_note"])
    lines.append("Não se recalibra k*. Não se compara com MQ.")
    lines.append("")
    lines.append("## Seeds excluídas (apenas NaN/blowup)")
    lines.append("")
    if excluded:
        lines.append(", ".join(str(s) for s in excluded))
    else:
        lines.append("Nenhuma. 32/32 tentadas; nenhuma dropada por estética.")
    lines.append(f"- n_finite = {n_finite}")
    lines.append(f"- n_blowup = {n_blowup}")
    lines.append("")
    lines.append("## Veredito")
    lines.append("")
    lines.append(f"**{classif['verdict']}**")
    lines.append("")
    lines.append(classif["note"])
    lines.append("")
    if classif["reasons"]:
        lines.append("Notas técnicas:")
        for r in classif["reasons"]:
            lines.append(f"- {r}")
        lines.append("")
    lines.append("Sem comparação com MQ. Pilotos 1–34 não confirmatórios. Theta_core intocado.")
    lines.append("Backend mlx GPU fp32, PROTOCOL_v2. Este experimento **não** pode devolver SUPPORTED para MQ.")
    lines.append("Exclusão técnica = apenas NaN/blowup. Nenhuma seed foi descartada por ser feia.")
    lines.append("")
    lines.append("## Arquivos")
    lines.append("")
    lines.append(f"- pasta: `{out}`")
    lines.append("- PROTOCOL.md (v1 histórico), PROTOCOL_v2.md, config.json, seeds.txt, code/run_q02.py")
    lines.append("- raw/seedXX_metrics.csv, metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt")
    lines.append("")
    (out / "analysis.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_sha256sums(out: Path):
    paths = []
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name not in ("SHA256SUMS.txt", ".write_test"):
            paths.append(p)
    lines = []
    for p in paths:
        rel = p.relative_to(out).as_posix()
        lines.append(f"{sha256_file(p)}  {rel}")
    (out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return lines


def load_metrics_csv(path: Path):
    rows = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            rec = {}
            for k, v in row.items():
                if k in ("finite", "artifact_1_2_cells"):
                    rec[k] = str(v).strip().lower() in ("true", "1", "yes")
                else:
                    try:
                        rec[k] = float(v) if v != "" else float("nan")
                    except Exception:
                        rec[k] = v
            if "seed" in rec:
                rec["seed"] = int(rec["seed"])
            if "N" in rec:
                rec["N"] = int(rec["N"])
            rows.append(rec)
    return rows


def summarize_times(vals, n_finite):
    arr = np.array(vals, dtype=np.float64)
    if arr.size == 0:
        return {"mean": None, "std": None, "min": None, "max": None, "median": None, "n": 0, "n_never": n_finite}
    return {
        "mean": float(arr.mean()),
        "std": float(arr.std(ddof=0)),
        "min": float(arr.min()),
        "max": float(arr.max()),
        "median": float(np.median(arr)),
        "n": int(arr.size),
        "n_never": int(n_finite - arr.size),
    }


def prepare_gpu_arrays():
    st = build_state(NGRID)
    half_lin = mx.array(st["half_lin"])
    nu = mx.array(np.asarray(NU, dtype=DTYPE_R_NP))
    lam = mx.array(np.asarray(LAM, dtype=DTYPE_R_NP))
    mx.eval(half_lin, nu, lam)
    return {
        "dx": st["dx"],
        "dV": st["dV"],
        "r2": st["r2"],
        "r": st["r"],
        "k_mag": st["k_mag"],
        "half_lin": half_lin,
        "nu": nu,
        "lam": lam,
        "lam_np": np.asarray(LAM, dtype=np.float64),
        "noise_amp": st["noise_amp"],
        "f_FDT": st["f_FDT"],
        "psi0": st["psi"],
        "y0": st["y"],
        "shape": tuple(st["psi"].shape),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=str, default="")
    parser.add_argument("--seeds", type=int, nargs="*", default=list(SEEDS))
    args = parser.parse_args()
    seeds = tuple(args.seeds) if args.seeds else SEEDS
    out = Path(args.out) if args.out else resolve_out()
    out.mkdir(parents=True, exist_ok=True)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    (out / "code").mkdir(parents=True, exist_ok=True)

    started = now_sp()
    executed = Path(__file__).resolve()
    solver_sha = sha256_file(executed)
    proto_v1 = protocol_sha("v1") or PROTOCOL_V1_SHA_KNOWN
    proto_v2 = protocol_sha("v2")
    dx = LBOX / float(NGRID)
    k_nyq = float(np.pi * np.sqrt(3.0) / dx)
    device = str(mx.default_device())

    print("Q02 start", started, "out", out, flush=True)
    print("executed", executed, "solver_sha256", solver_sha, flush=True)
    print("protocol_v1_sha256", proto_v1, flush=True)
    print("protocol_v2_sha256", proto_v2, flush=True)
    print("backend", BACKEND, "precision", PRECISION, "device", device, flush=True)
    print("seeds", list(seeds), "sequential GPU", flush=True)
    print("k_nyquist", k_nyq, "dx", dx, flush=True)

    src = executed.read_bytes()
    code_dst = out / "code" / "run_q02.py"
    if code_dst.resolve() != executed:
        code_dst.write_bytes(src)
    try:
        fontes_dst = FONTES / "run_q02.py"
        if fontes_dst.resolve() != executed:
            fontes_dst.write_bytes(src)
    except Exception as exc:
        print("fontes_copy_skipped", exc, flush=True)

    (out / "seeds.txt").write_text("\n".join(str(s) for s in seeds) + "\n", encoding="utf-8")

    config = {
        "question": "Q02",
        "title": "ensemble caótico de referência (32 seeds, 1 átomo)",
        "canonical": "TRIAD_QM_CANONICAL_V1",
        "canonical_sha256": CANONICAL_SHA,
        "qm_comparison": False,
        "isolate_terms": False,
        "theta_core_frozen": True,
        "pilots_1_34_confirmatory": False,
        "technical_exclusion": "NaN/blowup only",
        "supported_for_qm": False,
        "protocol": "PROTOCOL_v2",
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
        "box": {
            "L": LBOX,
            "N": NGRID,
            "dt": DT,
            "T": T_FINAL,
            "V_ext": V_EXT,
            "domain": "[-L/2, L/2)^3",
        },
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
            "backend": BACKEND,
            "device": device,
            "solver": "standalone 3D Strang mlx GPU (mesmo passo Q01a)",
            "memory_update": "euler",
            "record_every": RECORD_EVERY,
            "python": "/Library/Frameworks/Python.framework/Versions/3.14/bin/python3",
            "workers": 1,
            "neural_engine": False,
        },
        "seeds": list(seeds),
        "late_window": {"rule": "last 20% of T", "t_min": LATE_FRAC * T_FINAL, "T": T_FINAL},
        "observables": list(OBS_LATE),
        "verdict_rule": {
            "ge_30_of_32_finite_and_finite_std": "INCONCLUSIVE for MQ (expected; Q02 is not a QM test)",
            "gt_4_blowup": "NUMERICAL_FAILURE",
            "supported_for_qm": False,
            "no_aesthetic_drop": True,
        },
        "k_nyquist": k_nyq,
        "k_nyquist_formula": "pi*sqrt(3)/dx",
        "q01a_solver_sha256": Q01A_SOLVER_SHA,
        "solver_sha256": solver_sha,
        "protocol_v1_sha256": proto_v1,
        "protocol_v2_sha256": proto_v2,
        "executed": str(executed),
    }
    with (out / "config.json").open("w") as f:
        json.dump(config, f, indent=2)

    print("preparing GPU arrays", flush=True)
    gpu_arrays = prepare_gpu_arrays()
    print("gpu ready noise_amp", gpu_arrays["noise_amp"], flush=True)

    t0 = time.perf_counter()
    summaries = {}
    raw_dir = str(out / "raw")
    for seed in seeds:
        try:
            summaries[int(seed)] = run_one(int(seed), raw_dir, gpu_arrays)
        except Exception as exc:
            print("SEED_EXCEPTION", "seed", seed, repr(exc), flush=True)
            summaries[int(seed)] = {
                "question": "Q02",
                "seed": int(seed),
                "finite": False,
                "finite_final": False,
                "blew_up": True,
                "blow_t": None,
                "wall_s": float("nan"),
                "box_filled": False,
                "peak_max": float("nan"),
                "peak_max_t": None,
                "t_settle": None,
                "t_fill": None,
                "error": repr(exc),
                "backend": BACKEND,
            }
            for key in OBS_LATE:
                summaries[int(seed)][f"{key}_late_mean"] = float("nan")
                summaries[int(seed)][f"{key}_late_std"] = float("nan")
                summaries[int(seed)][f"{key}_late_n"] = 0

    wall_total = time.perf_counter() - t0
    rows = [summaries[s] for s in seeds]
    fieldnames = [
        "seed",
        "finite",
        "blew_up",
        "blow_t",
        "wall_s",
        "n_records",
        "box_filled",
        "t_settle",
        "t_fill",
        "peak_max",
        "peak_max_t",
        "backend",
    ]
    for key in OBS_LATE:
        fieldnames.extend([f"{key}_late_mean", f"{key}_late_std", f"{key}_late_n"])
    seed_rows = []
    for r in rows:
        row = {k: r.get(k, "") for k in fieldnames}
        seed_rows.append(row)
    write_csv(out / "metrics.csv", seed_rows, fieldnames)

    by_seed = {}
    for s in seeds:
        csvp = out / "raw" / f"seed{int(s):02d}_metrics.csv"
        mets = load_metrics_csv(csvp) if csvp.is_file() else []
        by_seed[int(s)] = {"summary": summaries[s], "metrics": mets}

    finite_seeds = [int(s) for s in seeds if summaries[s].get("finite")]
    excluded = [int(s) for s in seeds if not summaries[s].get("finite")]
    n_finite = len(finite_seeds)
    n_blowup = len(excluded)
    finite_rows = [summaries[s] for s in finite_seeds]

    ensemble_late = {}
    for key in OBS_LATE:
        ensemble_late[key] = ensemble_of_late(finite_rows, f"{key}_late_mean")

    t_settle_vals = finite_list([summaries[s].get("t_settle") for s in finite_seeds])
    t_fill_vals = finite_list([summaries[s].get("t_fill") for s in finite_seeds])
    et = {
        "t_settle": summarize_times(t_settle_vals, n_finite),
        "t_fill": summarize_times(t_fill_vals, n_finite),
        "definition_t_settle": "|R_rms(t)-R_rms_late|<0.05*|R_rms_late| and stays through T",
        "definition_t_fill": "first t with R_rms > 0.9*(L/2)",
    }

    n_filled = sum(1 for s in finite_seeds if summaries[s].get("box_filled"))
    frac_filled = (n_filled / n_finite) if n_finite else None
    frac_filled_all = n_filled / float(len(seeds))

    peak_max_global = None
    peak_max_t = None
    peak_max_seed = None
    for s in seeds:
        pm = summaries[s].get("peak_max")
        if pm is not None and np.isfinite(pm):
            if peak_max_global is None or pm > peak_max_global:
                peak_max_global = float(pm)
                peak_max_t = summaries[s].get("peak_max_t")
                peak_max_seed = int(s)

    k_star_late_mean = ensemble_late["k_star"]["mean"]
    rel_nyq = None
    on_nyq = None
    k_note = "k* omitido (sem médias finitas)."
    if k_star_late_mean is not None and np.isfinite(k_star_late_mean):
        rel_nyq = abs(k_star_late_mean - k_nyq) / k_nyq
        on_nyq = bool(rel_nyq <= 0.10)
        stdk = ensemble_late["k_star"]["std"]
        grid_locked = stdk is not None and np.isfinite(stdk) and stdk < 1e-9
        if on_nyq:
            k_note = (
                f"k* médio tardio está a {100*rel_nyq:.2f}% do Nyquist "
                f"({k_star_late_mean:.6g} vs {k_nyq:.6g}). "
                + ("std≈0 entre seeds: grid-locked a um bin, como em Q01. " if grid_locked else "")
                + "Espectro ainda pode estar preso à grade. Medição, não calibração."
            )
        else:
            k_note = (
                f"k* médio tardio NÃO está no Nyquist (rel={rel_nyq:.4f}). "
                + ("std≈0 entre seeds: um único bin. " if grid_locked else f"std entre seeds = {stdk}. ")
                + "Medição, não calibração."
            )

    extra = {
        "n_finite": n_finite,
        "n_blowup": n_blowup,
        "excluded_seeds": excluded,
        "n_filled": n_filled,
        "fraction_box_filled": frac_filled,
        "fraction_box_filled_all": frac_filled_all,
        "empirical_transient": et,
        "peak_max_global": peak_max_global,
        "peak_max_t": peak_max_t,
        "peak_max_seed": peak_max_seed,
        "k_nyquist": k_nyq,
        "k_star_late_mean": k_star_late_mean,
        "k_star_rel_nyquist": rel_nyq,
        "k_star_on_nyquist": on_nyq,
        "k_star_note": k_note,
        "wall_total_s": wall_total,
        "workers": 1,
        "device": device,
        "protocol_v1_sha256": proto_v1,
        "protocol_v2_sha256": proto_v2,
    }

    classif = classify(n_finite, n_blowup, ensemble_late)
    if finite_seeds:
        make_figures(out, by_seed, finite_seeds)
    finished = now_sp()
    write_analysis(out, rows, classif, ensemble_late, extra, started, finished)

    result = {
        "question": "Qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?",
        "id": "Q02",
        "verdict": classif["verdict"],
        "note": classif["note"],
        "qm_comparison": False,
        "theta_core_unchanged": True,
        "terms_isolated": False,
        "n_seeds": len(seeds),
        "n_finite": n_finite,
        "n_blowup": n_blowup,
        "excluded_seeds": excluded,
        "ensemble_late": ensemble_late,
        "empirical_transient": et,
        "fraction_box_filled": frac_filled,
        "fraction_box_filled_all": frac_filled_all,
        "n_filled": n_filled,
        "peak_max_global": peak_max_global,
        "peak_max_t": peak_max_t,
        "peak_max_seed": peak_max_seed,
        "k_star_late_mean": k_star_late_mean,
        "k_nyquist": k_nyq,
        "k_star_on_nyquist": on_nyq,
        "k_star_rel_nyquist": rel_nyq,
        "k_star_note": k_note,
        "backend": BACKEND,
        "precision": PRECISION,
        "device": device,
        "protocol": "PROTOCOL_v2",
        "protocol_v1_sha256": proto_v1,
        "protocol_v2_sha256": proto_v2,
        "solver_sha256": solver_sha,
        "canonical_sha256": CANONICAL_SHA,
        "q01a_solver_sha256": Q01A_SOLVER_SHA,
        "started_america_sao_paulo": started,
        "finished_america_sao_paulo": finished,
        "supported_for_qm": False,
        "pilots_1_34_confirmatory": False,
        "wall_total_s": wall_total,
        "workers": 1,
        "well_defined_distribution": classif["well_defined_distribution"],
        "out": str(out),
    }
    with (out / "result.json").open("w") as f:
        json.dump(jsonable(result), f, indent=2)

    write_sha256sums(out)
    print("VERDICT", classif["verdict"], flush=True)
    print("NOTE", classif["note"], flush=True)
    print("n_finite", n_finite, "n_blowup", n_blowup, flush=True)
    print("wrote", out, "finished", finished, "wall_total_s", wall_total, flush=True)


if __name__ == "__main__":
    main()
