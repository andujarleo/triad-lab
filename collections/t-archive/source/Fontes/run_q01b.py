#!/usr/bin/env python3
"""Q01b — refino N e dt da tríade COMPLETA (Theta_core, Q00).

Cópia parametrizada de run_q01a.py
(hash abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64).
Só N e dt viram argumentos. Mesmo passo Strang, mesmos observáveis.

Pergunta apenas: ε_num melhora com N=96 e dt ∈ {dt0/2, dt0/4}?
Sem comparação com MQ. Sem isolar termos. Sem mudar Theta_core.
1 gaussiana = 1 átomo. Volume preenchido = universo.
Q01a é INCONCLUSIVE (ε_num≈0.194; k* no Nyquist) — não se reabre.
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
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
Q01B_DIR = VAULT / "QM" / "Q01b_dt_N"
Q01A_DIR = VAULT / "QM" / "Q01_convergencia"
FONTES = VAULT / "Fontes"
FALLBACK = Path("/tmp/Q01b_dt_N")

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

# --- N_num / caixa (não física) ---
LBOX = 32.0
DT0 = 0.0025
T_FINAL = 8.0
SEED = 0
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_DT = 0.1
K_CUT_FACTOR = 1.0
BACKEND = "numpy"
DTYPE_PSI = np.complex128
DTYPE_R = np.float64

CELLS = (
    {"id": "N96_dt0", "N": 96, "dt": 0.0025},
    {"id": "N64_dt0h", "N": 64, "dt": 0.00125},
    {"id": "N64_dt0q", "N": 64, "dt": 0.000625},
)

Q01A_SOLVER_SHA = "abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64"
CANONICAL_SHA = "e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e"
PROTOCOL_SHA = "5bbc8101757a454aefe59c51c40609b35503e805e19740680a7f92ff36e95e1f"
Q01A_EPS_NUM = 0.19444360312773695


def resolve_out() -> Path:
    try:
        Q01B_DIR.mkdir(parents=True, exist_ok=True)
        test = Q01B_DIR / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink()
        return Q01B_DIR
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


def nyquist_corner(dx):
    return math.pi * math.sqrt(3.0) / dx


def build_state(N, dt):
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False, dtype=DTYPE_R)
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
    half_lin = np.exp(-1j * H_lin * dt / (2.0 * HBAR) - GAMMA * dt / (2.0 * HBAR))
    s = INIT_SIGMA
    psi = np.exp(-r2 / (2.0 * s * s)).astype(DTYPE_PSI)
    k0x, k0y, k0z = INIT_K0
    if k0x != 0.0 or k0y != 0.0 or k0z != 0.0:
        psi = psi * np.exp(1j * (k0x * X + k0y * Y + k0z * Z))
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * dt / (dx ** 3))) if f_FDT > 0 else 0.0
    return {
        "x": x,
        "dx": dx,
        "dV": dV,
        "r2": r2,
        "r": r,
        "k_mag": k_mag,
        "half_lin": half_lin,
        "psi": psi,
        "y": y,
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
        "k_nyq": nyquist_corner(dx),
        "k_max_grid": float(k_mag.max()),
    }


def strang_step(psi, y, half_lin, noise_amp, rng, nu, lam, dt):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((-1, 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    psi = psi * np.exp(-1j * V_tot * dt / HBAR)
    y = y + dt * nu.reshape((-1, 1, 1, 1)) * (rho - y)
    if noise_amp > 0.0:
        xi = (rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape)) / np.sqrt(2.0)
        psi = psi + noise_amp * xi
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
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


def resample_rho(rho, N_src, N_dst, L):
    from scipy.interpolate import RegularGridInterpolator

    x_src = np.linspace(-L / 2.0, L / 2.0, N_src, endpoint=False)
    x_dst = np.linspace(-L / 2.0, L / 2.0, N_dst, endpoint=False)
    rho_p = np.pad(rho, ((0, 1), (0, 1), (0, 1)), mode="wrap")
    x_p = np.append(x_src, x_src[0] + L)
    interp = RegularGridInterpolator(
        (x_p, x_p, x_p), rho_p, bounds_error=False, fill_value=None
    )
    X, Y, Z = np.meshgrid(x_dst, x_dst, x_dst, indexing="ij")
    pts = np.stack([X, Y, Z], axis=-1)
    return interp(pts).astype(np.float64)


def run_one(cell, out: Path):
    N = int(cell["N"])
    dt = float(cell["dt"])
    cid = cell["id"]
    t_wall0 = time.perf_counter()
    st = build_state(N, dt)
    dx = st["dx"]
    dV = st["dV"]
    psi = st["psi"]
    y = st["y"]
    half_lin = st["half_lin"]
    noise_amp = st["noise_amp"]
    f_FDT = st["f_FDT"]
    r2 = st["r2"]
    r = st["r"]
    k_mag = st["k_mag"]
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    nu = np.asarray(NU, dtype=DTYPE_R)
    lam = np.asarray(LAM, dtype=DTYPE_R)
    rng = np.random.default_rng(SEED)

    n_steps = int(round(T_FINAL / dt))
    rec_every = max(1, int(round(RECORD_DT / dt)))

    print("=== Q01b %s N=%d dt=%s ===" % (cid, N, dt), flush=True)
    print("backend", BACKEND, "dtype", "complex128/float64", flush=True)
    print("L", LBOX, "dx", dx, "dt", dt, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("record_every", rec_every, "record_dt", rec_every * dt, flush=True)
    print("Theta_core Lambda", LAMBDA, "alpha", ALPHA, "sigma", SIGMA_FRAC, flush=True)
    print("Gamma", GAMMA, "kT", KT, "nu", NU, "lam", LAM, flush=True)
    print("fdt_couple", FDT_COUPLE, "f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print(
        "noise_amp_check",
        float(np.sqrt(2.0 * GAMMA * KT * dt / HBAR)),
        flush=True,
    )
    print("max_nu_dt", float(max(NU) * dt), "memory_update", "euler", flush=True)
    print("k_nyq", st["k_nyq"], "k_max_grid", st["k_max_grid"], flush=True)
    print("seed", SEED, "IC", "§9.1 s=0.5 k0=0 y0=0 V_ext=0", flush=True)

    metrics = []
    late_rho = None
    blew = False
    blow_t = None
    for step in range(n_steps + 1):
        t = step * dt
        if step % rec_every == 0 or step == n_steps:
            rho, rec = record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam)
            rec["N"] = N
            rec["dx"] = dx
            rec["dt"] = dt
            rec["cell"] = cid
            metrics.append(rec)
            if t >= 0.8 * T_FINAL:
                late_rho = rho.copy()
            print(
                f"{cid} t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
                f"PR={rec['PR']:.6e} Rrms={rec['R_rms']:.6e} "
                f"k*={rec['k_star']:.6e} k*L={rec['k_star_L']:.4f} "
                f"Vmem={rec['Vmem_peak']:.6e} cells={rec['peak_n_cells_half']} "
                f"finite={rec['finite']}",
                flush=True,
            )
            if (not rec["finite"]) or (
                np.isfinite(rec["peak"]) and abs(rec["peak"]) > 1.0e30
            ):
                blew = True
                blow_t = t
                print("BLOWUP_OR_NAN", "cell", cid, "N", N, "dt", dt, "t", t, flush=True)
                break
        if step == n_steps or blew:
            break
        psi, y = strang_step(psi, y, half_lin, noise_amp, rng, nu, lam, dt)

    wall = time.perf_counter() - t_wall0
    print("cell", cid, "wall_s", wall, flush=True)

    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    write_csv(raw_dir / f"{cid}_metrics.csv", metrics, list(metrics[0].keys()))

    t_arr = np.array([m["t"] for m in metrics], dtype=np.float64)
    late_mask = t_arr >= (0.8 * T_FINAL)

    def series(key):
        return np.array([m[key] for m in metrics], dtype=np.float64)

    def stats(key, mask):
        v = series(key)[mask]
        v = v[np.isfinite(v)]
        if v.size == 0:
            return float("nan"), float("nan"), 0
        return float(v.mean()), float(v.std(ddof=0)), int(v.size)

    last = metrics[-1]
    k_star_lm, k_star_ls, k_star_ln = stats("k_star", late_mask)
    k_nyq = st["k_nyq"]
    k_on_nyq = bool(
        np.isfinite(k_star_lm) and abs(k_star_lm - k_nyq) / max(k_nyq, 1e-300) < 0.05
    )
    summary = {
        "question": "Q01b",
        "cell": cid,
        "N": N,
        "L": LBOX,
        "dx": dx,
        "dt": dt,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "record_every": rec_every,
        "record_dt": rec_every * dt,
        "seed": SEED,
        "backend": BACKEND,
        "fp": "fp64",
        "solver": "standalone 3D Strang spec §3+§5 (cópia parametrizada de run_q01a.py)",
        "q01a_solver_sha256": Q01A_SOLVER_SHA,
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
        "f_FDT_formula": "2*Gamma*(dx**3)*kT/hbar",
        "noise_amp": noise_amp,
        "noise_amp_formula": "sqrt(f_FDT*dt/dx**3)=sqrt(2*Gamma*kT*dt/hbar)",
        "memory_update": "euler",
        "max_nu_dt": float(max(NU) * dt),
        "k_nyquist": k_nyq,
        "k_nyquist_formula": "pi*sqrt(3)/dx",
        "k_max_grid": st["k_max_grid"],
        "k_star_late_on_nyquist": k_on_nyq,
        "wall_s": wall,
        "blew_up": blew,
        "blow_t": blow_t,
        "finite_final": bool(last.get("finite", False)),
        "norm_initial": metrics[0]["norm"],
        "norm_final": last["norm"],
        "peak_initial": metrics[0]["peak"],
        "peak_final": last["peak"],
        "PR_initial": metrics[0]["PR"],
        "PR_final": last["PR"],
        "R_rms_initial": metrics[0]["R_rms"],
        "R_rms_final": last["R_rms"],
        "k_star_final": last["k_star"],
        "k_star_L_final": last["k_star_L"],
        "Vmem_peak_final": last["Vmem_peak"],
        "peak_n_cells_half_final": last["peak_n_cells_half"],
        "peak_width_phys_final": last["peak_width_phys"],
        "artifact_1_2_cells_final": last["artifact_1_2_cells"],
        "cell_verdict": "NUMERICAL_FAILURE" if (blew or not last.get("finite", False)) else "finite",
    }
    for key in (
        "norm",
        "peak",
        "PR",
        "R_rms",
        "k_star",
        "k_star_L",
        "Vmem_peak",
        "crystallinity",
        "r50",
        "r80",
        "r90",
        "peak_n_cells_half",
        "peak_width_phys",
    ):
        lm, ls, ln = stats(key, late_mask)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln

    if late_rho is not None and np.isfinite(late_rho).all():
        np.save(raw_dir / f"{cid}_rho_late.npy", late_rho)
        summary["rho_late_saved"] = True
        summary["rho_late_t"] = float(t_arr[late_mask][-1]) if np.any(late_mask) else None
    else:
        summary["rho_late_saved"] = False
        summary["rho_late_t"] = None

    with (raw_dir / f"{cid}_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary, metrics, late_rho


def rel_diff(a, b):
    if not (np.isfinite(a) and np.isfinite(b)):
        return float("nan")
    den = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / den


def load_q01a_ref():
    ref = {
        "available": False,
        "late": {},
        "series": {},
        "wall_s": None,
        "k_star_by_N": {},
        "rho_late_N64": None,
    }
    result_p = Q01A_DIR / "result.json"
    metrics_p = Q01A_DIR / "metrics.csv"
    rho_p = Q01A_DIR / "raw" / "N64_rho_late.npy"
    if result_p.is_file():
        with result_p.open() as f:
            q = json.load(f)
        ref["available"] = True
        ref["late"] = q.get("late_window", {}).get("64", {})
        ref["wall_s"] = (q.get("wall_s") or {}).get("64")
        ref["epsilon_num"] = q.get("epsilon_num", Q01A_EPS_NUM)
        ref["verdict"] = q.get("verdict")
        lw = q.get("late_window", {})
        for nkey in ("32", "48", "64"):
            if nkey in lw:
                ref["k_star_by_N"][int(nkey)] = lw[nkey].get("k_star_late_mean")
    if metrics_p.is_file():
        rows = []
        with metrics_p.open() as f:
            r = csv.DictReader(f)
            for row in r:
                if int(float(row["N"])) == 64:
                    rec = {k: (float(row[k]) if k not in ("finite", "artifact_1_2_cells") else row[k]) for k in row}
                    rec["finite"] = str(row.get("finite", "True")).lower() == "true"
                    rows.append(rec)
        ref["series"] = rows
    if rho_p.is_file():
        ref["rho_late_N64"] = np.load(rho_p)
    return ref


def make_figures(out: Path, by_cell: dict, q01a: dict):
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)

    order = [c["id"] for c in CELLS]
    colors = {
        "Q01a_N64_dt0": "0.35",
        "N96_dt0": "C0",
        "N64_dt0h": "C1",
        "N64_dt0q": "C2",
    }
    labels = {
        "Q01a_N64_dt0": "Q01a N=64 dt0",
        "N96_dt0": "N=96 dt0",
        "N64_dt0h": "N=64 dt0/2",
        "N64_dt0q": "N=64 dt0/4",
    }
    keys_panels = [
        ("peak", "peak ρ  (ρ_max)"),
        ("PR", "PR  (participação)"),
        ("R_rms", "R_rms"),
        ("k_star", "k*"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.2))
    for ax, (key, title) in zip(axes.ravel(), keys_panels):
        if q01a.get("series"):
            t = [m["t"] for m in q01a["series"]]
            v = [m[key] for m in q01a["series"]]
            ax.plot(t, v, color=colors["Q01a_N64_dt0"], label=labels["Q01a_N64_dt0"], lw=1.6, ls="--")
        for cid in order:
            mets = by_cell[cid]["metrics"]
            t = [m["t"] for m in mets]
            v = [m[key] for m in mets]
            ax.plot(t, v, color=colors[cid], label=labels[cid], lw=1.4)
        ax.axvspan(
            0.8 * T_FINAL,
            T_FINAL,
            color="0.85",
            alpha=0.5,
            label="janela tardia" if ax is axes[0, 0] else None,
        )
        ax.set_title(title)
        ax.set_xlabel("t")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=7)
    fig.suptitle("Q01b — overlay vs Q01a N=64 dt0  (tríade completa, sem MQ)")
    fig.tight_layout()
    fig.savefig(fig_dir / "overlay_observables.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.2))
    late_keys = ["peak", "PR", "R_rms", "k_star"]
    titles = ["peak tardio", "PR tardio", "R_rms tardio", "k* tardio"]
    ids_bar = ["Q01a_N64_dt0"] + order
    xs = np.arange(len(ids_bar))
    for ax, key, title in zip(axes.ravel(), late_keys, titles):
        means, stds, cols = [], [], []
        for cid in ids_bar:
            if cid == "Q01a_N64_dt0":
                m = q01a.get("late", {}).get(f"{key}_late_mean", float("nan"))
                s = q01a.get("late", {}).get(f"{key}_late_std", 0.0)
            else:
                m = by_cell[cid]["summary"][f"{key}_late_mean"]
                s = by_cell[cid]["summary"][f"{key}_late_std"]
            means.append(m if np.isfinite(m) else 0.0)
            stds.append(s if np.isfinite(s) else 0.0)
            cols.append(colors[cid])
        ax.bar(xs, means, yerr=stds, color=cols, capsize=4, alpha=0.85)
        ax.set_xticks(xs)
        ax.set_xticklabels([labels[i] for i in ids_bar], rotation=20, ha="right", fontsize=8)
        ax.set_title(title + "  (média ± std, último 20%)")
        ax.grid(True, axis="y", alpha=0.3)
    fig.suptitle("Q01b — janela tardia vs Q01a N=64 dt0")
    fig.tight_layout()
    fig.savefig(fig_dir / "late_window_comparison.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(12.8, 4.2))
    for ax, cid in zip(axes, order):
        rho = by_cell[cid]["late_rho"]
        if rho is None:
            ax.set_title(f"{cid} sem ρ tardio")
            continue
        sl = rho[:, :, rho.shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cells = by_cell[cid]["summary"]["peak_n_cells_half_final"]
        ax.set_title(f"{cid}  z=0  células½={cells}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("Q01b — ρ tardio (corte mediano). Volume preenchido = universo")
    fig.tight_layout()
    fig.savefig(fig_dir / "late_rho_midplane.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    Ns_q01a = [32, 48, 64]
    dxs = [LBOX / n for n in Ns_q01a]
    nyqs = [nyquist_corner(dx) for dx in dxs]
    kstars = [q01a.get("k_star_by_N", {}).get(n, float("nan")) for n in Ns_q01a]
    ax.plot(Ns_q01a, nyqs, "k--", label=r"$k_{\mathrm{Nyq}}=\pi\sqrt{3}/dx$")
    ax.plot(Ns_q01a, kstars, "o", color="0.35", label="Q01a k* tardio")
    s96 = by_cell["N96_dt0"]["summary"]
    ax.plot([96], [s96["k_nyquist"]], "ks")
    ax.plot([96], [s96["k_star_late_mean"]], "C0o", ms=8, label="Q01b N=96 k* tardio")
    ax.plot([64], [nyquist_corner(LBOX / 64.0)], "k+")
    ax.set_xlabel("N")
    ax.set_ylabel("k")
    ax.set_title("k* vs Nyquist (canto π√3/dx)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "kstar_vs_nyquist.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.6, 4.4))
    ids_n64 = ["Q01a_N64_dt0", "N64_dt0h", "N64_dt0q"]
    dts = [DT0, 0.00125, 0.000625]
    for key, mk in (("peak", "o-"), ("PR", "s--"), ("R_rms", "^-.")):
        vals = []
        for cid in ids_n64:
            if cid == "Q01a_N64_dt0":
                vals.append(q01a.get("late", {}).get(f"{key}_late_mean", float("nan")))
            else:
                vals.append(by_cell[cid]["summary"][f"{key}_late_mean"])
        # normalizar pelo valor Q01a para caber no mesmo eixo
        refv = vals[0] if (len(vals) and np.isfinite(vals[0]) and abs(vals[0]) > 0) else 1.0
        ax.plot(dts, [v / refv for v in vals], mk, label=f"{key} / {key}_Q01a")
    ax.set_xscale("log")
    ax.set_xlabel("dt")
    ax.set_ylabel("razão à Q01a N=64 dt0")
    ax.set_title("Q01b — refino temporal em N=64")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(fig_dir / "dt_refine_N64.png", dpi=150)
    plt.close(fig)


def l2_compare(by_cell, q01a):
    out = {"method": "RegularGridInterpolator trilinear periódico; N=96→64 contra Q01a N64; N=64 nativo", "pairs": {}}
    try:
        rho_a = q01a.get("rho_late_N64")
        if rho_a is None or not np.isfinite(rho_a).all():
            out["skipped"] = True
            out["reason"] = "ρ tardio Q01a N=64 ausente/não-finito"
            return out
        dx64 = LBOX / 64.0
        dV = dx64 ** 3
        nrm = float(np.sqrt(np.sum(rho_a ** 2) * dV))

        def pack(name, rb):
            if rb is None or not np.isfinite(rb).all():
                return {"skipped": True, "reason": "ρ não-finito"}
            if rb.shape != rho_a.shape:
                rb = resample_rho(rb, rb.shape[0], 64, LBOX)
            diff = rb - rho_a
            l2 = float(np.sqrt(np.sum(diff ** 2) * dV))
            return {"L2": l2, "L2_rel": l2 / max(nrm, 1e-300), "ref": "Q01a_N64_dt0"}

        for cid in ("N96_dt0", "N64_dt0h", "N64_dt0q"):
            out["pairs"][f"{cid}_vs_Q01a_N64"] = pack(cid, by_cell[cid]["late_rho"])
        # pares N=64 nativos
        r_h = by_cell["N64_dt0h"]["late_rho"]
        r_q = by_cell["N64_dt0q"]["late_rho"]
        if r_h is not None and r_q is not None and np.isfinite(r_h).all() and np.isfinite(r_q).all():
            diff = r_h - r_q
            l2 = float(np.sqrt(np.sum(diff ** 2) * dV))
            nrmq = float(np.sqrt(np.sum(r_q ** 2) * dV))
            out["pairs"]["N64_dt0h_vs_N64_dt0q"] = {
                "L2": l2,
                "L2_rel": l2 / max(nrmq, 1e-300),
                "ref": "N64_dt0q",
            }
        out["skipped"] = False
    except Exception as exc:
        out["skipped"] = True
        out["reason"] = f"resample falhou: {exc!r}"
    return out


def classify(by_cell, q01a, l2info):
    reasons = []
    cell_verdicts = {}
    nan_or_blow = False
    for cell in CELLS:
        cid = cell["id"]
        s = by_cell[cid]["summary"]
        if s["blew_up"] or not s["finite_final"]:
            nan_or_blow = True
            cell_verdicts[cid] = "NUMERICAL_FAILURE"
            reasons.append(f"{cid} NaN/blowup t={s['blow_t']}")
        else:
            finite_late = all(
                np.isfinite(s[f"{k}_late_mean"]) for k in ("peak", "PR", "R_rms")
            )
            if not finite_late:
                nan_or_blow = True
                cell_verdicts[cid] = "NUMERICAL_FAILURE"
                reasons.append(f"{cid} médias tardias não-finitas")
            else:
                cell_verdicts[cid] = "finite"

    def late_of(cid, key):
        if cid == "Q01a_N64_dt0":
            return q01a.get("late", {}).get(f"{key}_late_mean", float("nan"))
        return by_cell[cid]["summary"][f"{key}_late_mean"]

    def trio(a, b):
        d = {k: rel_diff(late_of(a, k), late_of(b, k)) for k in ("peak", "PR", "R_rms")}
        finite = [v for v in d.values() if np.isfinite(v)]
        eps = float(max(finite)) if finite else float("nan")
        return d, eps

    d_N, eps_N = trio("Q01a_N64_dt0", "N96_dt0")
    d_dt, eps_dt = trio("Q01a_N64_dt0", "N64_dt0q")
    d_dt_s1, eps_dt_s1 = trio("Q01a_N64_dt0", "N64_dt0h")
    d_dt_s2, eps_dt_s2 = trio("N64_dt0h", "N64_dt0q")

    wild_N = any((np.isfinite(v) and v > 0.50) for v in d_N.values()) or not any(np.isfinite(v) for v in d_N.values())
    wild_dt = any((np.isfinite(v) and v > 0.50) for v in d_dt.values()) or not any(np.isfinite(v) for v in d_dt.values())

    s96 = by_cell["N96_dt0"]["summary"]
    k_on_nyq_96 = bool(s96.get("k_star_late_on_nyquist"))
    k_rel_nyq_96 = rel_diff(s96.get("k_star_late_mean", float("nan")), s96.get("k_nyquist", float("nan")))

    improved = (
        (not nan_or_blow)
        and (not wild_N)
        and (not wild_dt)
        and np.isfinite(eps_N)
        and np.isfinite(eps_dt)
        and eps_N < Q01A_EPS_NUM
        and eps_dt < Q01A_EPS_NUM
    )

    if nan_or_blow or wild_N or wild_dt:
        verdict = "NUMERICAL_FAILURE"
        note = (
            "NaN/blowup ou divergência wild (>50%) no par espacial N=64→96 "
            "ou no par temporal dt0→dt0/4. Células que falharam são guardadas."
        )
    elif improved:
        verdict = "ε_num improved"
        note = (
            "ε_num espacial (N=64 dt0 vs N=96 dt0) e ε_num temporal "
            "(N=64 dt0 vs N=64 dt0/4) ambos menores que ε_num Q01a (0.194). "
            "Ainda não é convergência apertada. Nunca SUPPORTED para MQ."
        )
    else:
        verdict = "INCONCLUSIVE"
        note = (
            "Sem falha catastrófica, mas o refino não fechou ε_num abaixo de Q01a "
            "nos dois eixos (N e dt), e/ou k* permanece no Nyquist. "
            "Nunca SUPPORTED para MQ."
        )

    return {
        "verdict": verdict,
        "note": note,
        "reasons": reasons,
        "cell_verdicts": cell_verdicts,
        "rel_diff_N64_dt0_vs_N96_dt0": d_N,
        "rel_diff_N64_dt0_vs_N64_dt0q": d_dt,
        "rel_diff_N64_dt0_vs_N64_dt0h": d_dt_s1,
        "rel_diff_N64_dt0h_vs_N64_dt0q": d_dt_s2,
        "epsilon_num_spatial": eps_N,
        "epsilon_num_temporal": eps_dt,
        "epsilon_num_dt_successive_dt0_vs_dt0h": eps_dt_s1,
        "epsilon_num_dt_successive_dt0h_vs_dt0q": eps_dt_s2,
        "epsilon_num_q01a": Q01A_EPS_NUM,
        "epsilon_num_spatial_definition": (
            "máximo |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms "
            "entre Q01a N=64 dt0 e Q01b N=96 dt0"
        ),
        "epsilon_num_temporal_definition": (
            "máximo |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms "
            "entre Q01a N=64 dt0 e Q01b N=64 dt0/4"
        ),
        "improved_vs_q01a": improved,
        "diverge_wildly_spatial": wild_N,
        "diverge_wildly_temporal": wild_dt,
        "k_star_N96_late_mean": s96.get("k_star_late_mean"),
        "k_nyquist_N96": s96.get("k_nyquist"),
        "k_star_N96_on_nyquist": k_on_nyq_96,
        "k_star_N96_rel_to_nyquist": k_rel_nyq_96,
        "l2": l2info,
        "qm_comparison": False,
        "supported_for_qm": False,
    }


def fmt_pm(mean, std):
    if not np.isfinite(mean):
        return "NaN"
    return f"{mean:.6g} ± {std:.3g}"


def write_analysis(out: Path, by_cell, q01a, classif, started_iso, finished_iso):
    lines = []
    lines.append("# Q01b — Análise (refino N e dt da tríade completa)")
    lines.append("")
    lines.append("Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.")
    lines.append("Pilotos 27–29 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.")
    lines.append("Theta_core intocado (Q00). PROTOCOL.md de Q01a **não** foi editado.")
    lines.append("Q01a permanece INCONCLUSIVE (ε_num≈0.194; k* no Nyquist).")
    lines.append("")
    lines.append("## Pergunta")
    lines.append("")
    lines.append("Os observáveis convergem (ε_num cai) ao ir a N=96 com dt0 e ao refinar dt em N=64?")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Theta_core: Λ={LAMBDA}, α={ALPHA}, σ={SIGMA_FRAC}, Γ={GAMMA}, ν={NU}, λ={LAM}, kT={KT}")
    lines.append(f"- L={LBOX}, T={T_FINAL}, seed={SEED}, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0")
    lines.append(f"- FDT: f_FDT_e=2Γ dx³ kT/ℏ ; incremento spec eq. 4")
    lines.append("- células: N=96 dt=0.0025; N=64 dt=0.00125; N=64 dt=0.000625")
    lines.append(f"- overlay: Q01a N=64 dt0 (ε_num Q01a = {Q01A_EPS_NUM:.6g})")
    lines.append(f"- fp64; backend {BACKEND}; Strang standalone (cópia de run_q01a.py)")
    lines.append(f"- início (America/Sao_Paulo): {started_iso}")
    lines.append(f"- fim (America/Sao_Paulo): {finished_iso}")
    lines.append("")
    lines.append("## Tempos de parede")
    lines.append("")
    lines.append("| célula | N | dt | dx | n_steps | wall_s | wall_min | finito | veredito_célula |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    if q01a.get("wall_s") is not None:
        lines.append(
            f"| Q01a_N64_dt0 (ref) | 64 | 0.0025 | 0.5 | 3200 | {q01a['wall_s']:.3f} | {q01a['wall_s']/60.0:.3f} | True | INCONCLUSIVE |"
        )
    for cell in CELLS:
        cid = cell["id"]
        s = by_cell[cid]["summary"]
        cv = classif["cell_verdicts"].get(cid, s.get("cell_verdict"))
        lines.append(
            f"| {cid} | {s['N']} | {s['dt']} | {s['dx']:.6f} | {s['n_steps']} | "
            f"{s['wall_s']:.3f} | {s['wall_s']/60.0:.3f} | {s['finite_final']} | {cv} |"
        )
    tot = sum(by_cell[c["id"]]["summary"]["wall_s"] for c in CELLS)
    lines.append("")
    lines.append(f"Total Q01b ~ {tot:.1f} s ({tot/60.0:.2f} min). Nenhuma célula dropada.")
    lines.append("")
    lines.append("## Janela tardia (t ≥ 0.8 T = 6.4) — média ± std")
    lines.append("")
    header = (
        "| célula | N | dt | norm | peak | PR | R_rms | k* | k*L | Vmem_peak | "
        "células½ | largura_fís | 1–2 células |"
    )
    lines.append(header)
    lines.append("|" + "|".join(["---"] * 13) + "|")

    def row_from_late(cid, N, dt, late, artifact):
        def g(key):
            return fmt_pm(late.get(f"{key}_late_mean", float("nan")), late.get(f"{key}_late_std", float("nan")))

        art = "SIM" if artifact else "não"
        return (
            f"| {cid} | {N} | {dt} | {g('norm')} | {g('peak')} | {g('PR')} | {g('R_rms')} | "
            f"{g('k_star')} | {g('k_star_L')} | {g('Vmem_peak')} | "
            f"{g('peak_n_cells_half')} | {g('peak_width_phys')} | {art} |"
        )

    if q01a.get("late"):
        lines.append(row_from_late("Q01a_N64_dt0", 64, 0.0025, q01a["late"], False))
    for cell in CELLS:
        cid = cell["id"]
        s = by_cell[cid]["summary"]
        lines.append(row_from_late(cid, s["N"], s["dt"], s, s["artifact_1_2_cells_final"]))
    lines.append("")
    lines.append(
        "Norma crescente e R_rms ≈ L/2 significam volume preenchido = universo, não ruído a filtrar."
    )
    lines.append("")
    lines.append("## ε_num espacial (Q01a N=64 dt0 vs N=96 dt0)")
    lines.append("")
    for key, val in classif["rel_diff_N64_dt0_vs_N96_dt0"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append(f"")
    lines.append(f"ε_num espacial = **{classif['epsilon_num_spatial']}**")
    lines.append(f"definição: {classif['epsilon_num_spatial_definition']}")
    lines.append("")
    lines.append("## ε_num temporal (Q01a N=64 dt0 vs N=64 dt0/4)")
    lines.append("")
    for key, val in classif["rel_diff_N64_dt0_vs_N64_dt0q"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append("")
    lines.append(f"ε_num temporal = **{classif['epsilon_num_temporal']}**")
    lines.append(f"definição: {classif['epsilon_num_temporal_definition']}")
    lines.append("")
    lines.append("Pares sucessivos de dt (contexto):")
    lines.append("")
    lines.append("dt0 vs dt0/2:")
    for key, val in classif["rel_diff_N64_dt0_vs_N64_dt0h"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append("")
    lines.append("dt0/2 vs dt0/4:")
    for key, val in classif["rel_diff_N64_dt0h_vs_N64_dt0q"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append("")
    lines.append(f"ε_num Q01a (N=48 vs N=64, dt0) = {classif['epsilon_num_q01a']}")
    lines.append(f"melhorou vs Q01a nos dois eixos? {classif['improved_vs_q01a']}")
    lines.append("")
    lines.append("## k* vs Nyquist")
    lines.append("")
    s96 = by_cell["N96_dt0"]["summary"]
    dx96 = LBOX / 96.0
    lines.append(f"N=96: dx={dx96:.6f}, k_Nyq = π√3/dx = {s96['k_nyquist']:.6f}")
    lines.append(f"k* tardio N=96 = {s96.get('k_star_late_mean')} ± {s96.get('k_star_late_std')}")
    lines.append(f"k_max da malha = {s96.get('k_max_grid')}")
    lines.append(
        f"k* no Nyquist (rel < 5%)? **{'SIM' if classif['k_star_N96_on_nyquist'] else 'não'}** "
        f"(rel={classif['k_star_N96_rel_to_nyquist']})"
    )
    lines.append("")
    lines.append("Q01a (contexto): k* já estava no Nyquist de cada grade")
    for n, kval in sorted(q01a.get("k_star_by_N", {}).items()):
        kn = nyquist_corner(LBOX / float(n))
        lines.append(f"- N={n}: k*={kval}  vs  k_Nyq={kn:.6f}")
    lines.append("")
    lines.append("k* e k*L **não** são usados para calibrar Theta. Sem comparação MQ.")
    lines.append("")
    lines.append("## L2 de ρ tardio")
    lines.append("")
    if classif["l2"].get("skipped"):
        lines.append(f"Omitido: {classif['l2'].get('reason', 'não disponível')}.")
    else:
        lines.append(f"Método: {classif['l2']['method']}")
        for pair, d in classif["l2"]["pairs"].items():
            if d.get("skipped"):
                lines.append(f"- {pair}: omitido ({d.get('reason')})")
            else:
                lines.append(f"- {pair}: L2={d['L2']:.6g}  L2_rel={d['L2_rel']:.6g}  (ref {d['ref']})")
    lines.append("")
    lines.append(
        "L2 alto entre grades/dt diferentes é esperado: seed=0 em malhas ou passos distintos "
        "não gera o mesmo campo de ruído. Critério de ε_num usa os escalares da janela tardia."
    )
    lines.append("")
    lines.append("## Estruturas de 1–2 células")
    lines.append("")
    arts = [by_cell[c["id"]]["summary"]["artifact_1_2_cells_final"] for c in CELLS]
    if all(arts):
        lines.append("O pico permanece em 1–2 células em todas as células: suspeita de artefato de grade.")
    elif any(arts):
        lines.append("Pelo menos uma célula tem pico em 1–2 células. Ver tabela. Suspeita parcial.")
    else:
        lines.append("O pico não está preso a 1–2 células em nenhum estado final deste lote.")
    lines.append("")
    lines.append("## Veredito")
    lines.append("")
    lines.append(f"**{classif['verdict']}**")
    lines.append("")
    lines.append(classif["note"])
    lines.append("")
    if classif["reasons"]:
        lines.append("Razões técnicas:")
        for r in classif["reasons"]:
            lines.append(f"- {r}")
        lines.append("")
    lines.append("Este experimento **não** compara com mecânica quântica e **não** pode devolver SUPPORTED para MQ.")
    lines.append("Exclusão técnica = apenas NaN/blowup. Nenhum run foi descartado por ser feio.")
    lines.append("Nenhum termo isolado. Theta_core não mudou. Q00 congelado. Q01a PROTOCOL.md intocado.")
    lines.append("")
    lines.append("## Arquivos")
    lines.append("")
    lines.append(f"- pasta: `{out}`")
    lines.append("- PROTOCOL.md, config.json, seeds.txt, Q01b.md, code/run_q01b.py")
    lines.append("- raw/{N96_dt0,N64_dt0h,N64_dt0q}_metrics.csv, *_summary.json, *_rho_late.npy")
    lines.append("- metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt")
    lines.append("")
    text = "\n".join(lines) + "\n"
    (out / "analysis.md").write_text(text, encoding="utf-8")


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


def now_sp():
    try:
        from zoneinfo import ZoneInfo
        import datetime

        return datetime.datetime.now(ZoneInfo("America/Sao_Paulo")).strftime(
            "%Y-%m-%d %H:%M:%S BRT"
        )
    except Exception:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cells", type=str, nargs="*", default=[c["id"] for c in CELLS])
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()
    wanted = set(args.cells)
    cells = [c for c in CELLS if c["id"] in wanted]
    out = Path(args.out) if args.out else resolve_out()
    out.mkdir(parents=True, exist_ok=True)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    (out / "code").mkdir(parents=True, exist_ok=True)

    started = now_sp()
    print("Q01b start", started, "out", out, flush=True)
    print("protocol_sha256", PROTOCOL_SHA, flush=True)
    print("q01a_solver_sha256", Q01A_SOLVER_SHA, flush=True)

    q01a = load_q01a_ref()
    print("q01a_ref", q01a["available"], "late_keys", list(q01a.get("late", {}).keys())[:6], flush=True)

    by_cell = {}
    all_metrics = []
    for cell in cells:
        summary, metrics, late_rho = run_one(cell, out)
        by_cell[cell["id"]] = {"summary": summary, "metrics": metrics, "late_rho": late_rho}
        all_metrics.extend(metrics)

    if all_metrics:
        write_csv(out / "metrics.csv", all_metrics, list(all_metrics[0].keys()))

    finished = now_sp()
    have_all = set(by_cell.keys()) == {c["id"] for c in CELLS}
    if have_all:
        make_figures(out, by_cell, q01a)
        l2info = l2_compare(by_cell, q01a)
        classif = classify(by_cell, q01a, l2info)
        write_analysis(out, by_cell, q01a, classif, started, finished)
        result = {
            "question": "Q01b",
            "title": "refino N e dt — convergência numérica da tríade completa",
            "qm_comparison": False,
            "theta_core_unchanged": True,
            "terms_isolated": False,
            "pilots_27_29_confirmatory": False,
            "q00_frozen": True,
            "q01a_protocol_untouched": True,
            "q01a_verdict": q01a.get("verdict", "INCONCLUSIVE"),
            "verdict": classif["verdict"],
            "note": classif["note"],
            "cell_verdicts": classif["cell_verdicts"],
            "epsilon_num_spatial": classif["epsilon_num_spatial"],
            "epsilon_num_temporal": classif["epsilon_num_temporal"],
            "epsilon_num_q01a": classif["epsilon_num_q01a"],
            "epsilon_num_spatial_definition": classif["epsilon_num_spatial_definition"],
            "epsilon_num_temporal_definition": classif["epsilon_num_temporal_definition"],
            "rel_diff_N64_dt0_vs_N96_dt0": classif["rel_diff_N64_dt0_vs_N96_dt0"],
            "rel_diff_N64_dt0_vs_N64_dt0q": classif["rel_diff_N64_dt0_vs_N64_dt0q"],
            "rel_diff_N64_dt0_vs_N64_dt0h": classif["rel_diff_N64_dt0_vs_N64_dt0h"],
            "rel_diff_N64_dt0h_vs_N64_dt0q": classif["rel_diff_N64_dt0h_vs_N64_dt0q"],
            "improved_vs_q01a": classif["improved_vs_q01a"],
            "k_star_N96_late_mean": classif["k_star_N96_late_mean"],
            "k_nyquist_N96": classif["k_nyquist_N96"],
            "k_star_N96_on_nyquist": classif["k_star_N96_on_nyquist"],
            "k_star_N96_rel_to_nyquist": classif["k_star_N96_rel_to_nyquist"],
            "l2": classif["l2"],
            "supported_for_qm": False,
            "technical_exclusion": "NaN/blowup only",
            "cells": CELLS,
            "L": LBOX,
            "T": T_FINAL,
            "seed": SEED,
            "backend": BACKEND,
            "fp": "fp64",
            "wall_s": {c["id"]: by_cell[c["id"]]["summary"]["wall_s"] for c in CELLS},
            "late_window": {
                c["id"]: {
                    k: by_cell[c["id"]]["summary"][k]
                    for k in by_cell[c["id"]]["summary"]
                    if k.endswith("_late_mean") or k.endswith("_late_std") or k.endswith("_late_n")
                }
                for c in CELLS
            },
            "q01a_N64_dt0_late": q01a.get("late", {}),
            "started_america_sao_paulo": started,
            "finished_america_sao_paulo": finished,
            "out": str(out),
            "protocol_sha256": PROTOCOL_SHA,
            "canonical_sha256": CANONICAL_SHA,
            "q01a_solver_sha256": Q01A_SOLVER_SHA,
        }
        with (out / "result.json").open("w") as f:
            json.dump(result, f, indent=2)
        print("VERDICT", classif["verdict"], flush=True)
        print("EPS_NUM_SPATIAL", classif["epsilon_num_spatial"], flush=True)
        print("EPS_NUM_TEMPORAL", classif["epsilon_num_temporal"], flush=True)
        print("KSTAR_N96", classif["k_star_N96_late_mean"], "NYQ", classif["k_nyquist_N96"], flush=True)
        print("NOTE", classif["note"], flush=True)
    else:
        print("partial_run", sorted(by_cell.keys()), flush=True)

    write_sha256sums(out)
    print("wrote", out, "finished", finished, flush=True)


if __name__ == "__main__":
    main()
