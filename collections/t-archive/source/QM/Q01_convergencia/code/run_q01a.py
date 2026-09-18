#!/usr/bin/env python3
"""Q01a — convergência numérica da tríade COMPLETA (Theta_core, Q00).

Standalone 3D Strang (spec §3 + §5). Não usa triad-lang TriadParams
(esse tipo rejeita 3 modos + Gamma). Adaptado de run_R5_A2.py, mas
com Theta_core — NÃO os parâmetros A.2.

Pergunta apenas: observáveis convergem quando N aumenta?
Sem comparação com MQ. Sem isolar termos. Sem mudar Theta_core.
1 gaussiana = 1 átomo. Volume preenchido = universo.
Pilotos 27–29 não são confirmatórios.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

VAULT = Path("/Users/leo/Documents/Triad/T")
Q01_DIR = VAULT / "QM" / "Q01_convergencia"
FONTES = VAULT / "Fontes"
FALLBACK = Path("/tmp/Q01_convergencia")

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
DT = 0.0025
T_FINAL = 8.0
SEED = 0
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
NS = (32, 48, 64)
RECORD_EVERY = 40
K_CUT_FACTOR = 1.0
BACKEND = "numpy"
DTYPE_PSI = np.complex128
DTYPE_R = np.float64


def resolve_out() -> Path:
    try:
        Q01_DIR.mkdir(parents=True, exist_ok=True)
        test = Q01_DIR / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink()
        return Q01_DIR
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
    """Largura do pico: células acima de 50% do peak e raio equivalente."""
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
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    s = INIT_SIGMA
    psi = np.exp(-r2 / (2.0 * s * s)).astype(DTYPE_PSI)
    k0x, k0y, k0z = INIT_K0
    if k0x != 0.0 or k0y != 0.0 or k0z != 0.0:
        psi = psi * np.exp(1j * (k0x * X + k0y * Y + k0z * Z))
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
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
    }


def strang_step(psi, y, half_lin, noise_amp, rng, nu, lam):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((-1, 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem  # V_ext = 0
    psi = psi * np.exp(-1j * V_tot * DT / HBAR)
    y = y + DT * nu.reshape((-1, 1, 1, 1)) * (rho - y)
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
    """Reamostra ρ periódica para grade N_dst via interpolação trilinear."""
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


def run_one(N, out: Path):
    t_wall0 = time.perf_counter()
    st = build_state(N)
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

    n_steps = int(round(T_FINAL / DT))
    rec_every = max(1, RECORD_EVERY)

    print("=== Q01a N=%d ===" % N, flush=True)
    print("backend", BACKEND, "dtype", "complex128/float64", flush=True)
    print("L", LBOX, "dx", dx, "dt", DT, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("Theta_core Lambda", LAMBDA, "alpha", ALPHA, "sigma", SIGMA_FRAC, flush=True)
    print("Gamma", GAMMA, "kT", KT, "nu", NU, "lam", LAM, flush=True)
    print("fdt_couple", FDT_COUPLE, "f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print(
        "noise_amp_check",
        float(np.sqrt(2.0 * GAMMA * KT * DT / HBAR)),
        flush=True,
    )
    print("max_nu_dt", float(max(NU) * DT), "memory_update", "euler", flush=True)
    print("seed", SEED, "IC", "§9.1 s=0.5 k0=0 y0=0 V_ext=0", flush=True)

    metrics = []
    late_rho = None
    blew = False
    blow_t = None
    for step in range(n_steps + 1):
        t = step * DT
        if step % rec_every == 0 or step == n_steps:
            rho, rec = record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam)
            rec["N"] = N
            rec["dx"] = dx
            metrics.append(rec)
            if t >= 0.8 * T_FINAL:
                late_rho = rho.copy()
            print(
                f"N={N} t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
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
                print("BLOWUP_OR_NAN", "N", N, "t", t, flush=True)
                break
        if step == n_steps or blew:
            break
        psi, y = strang_step(psi, y, half_lin, noise_amp, rng, nu, lam)

    wall = time.perf_counter() - t_wall0
    print("N", N, "wall_s", wall, flush=True)

    raw_dir = out / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    write_csv(raw_dir / f"N{N}_metrics.csv", metrics, list(metrics[0].keys()))

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
    summary = {
        "question": "Q01a",
        "N": N,
        "L": LBOX,
        "dx": dx,
        "dt": DT,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "record_every": rec_every,
        "seed": SEED,
        "backend": BACKEND,
        "fp": "fp64",
        "solver": "standalone 3D Strang spec §3+§5 (não triad-lang)",
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
        "max_nu_dt": float(max(NU) * DT),
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
        np.save(raw_dir / f"N{N}_rho_late.npy", late_rho)
        summary["rho_late_saved"] = True
        summary["rho_late_t"] = float(t_arr[late_mask][-1]) if np.any(late_mask) else None
    else:
        summary["rho_late_saved"] = False
        summary["rho_late_t"] = None

    with (raw_dir / f"N{N}_summary.json").open("w") as f:
        json.dump(summary, f, indent=2)
    return summary, metrics, late_rho


def rel_diff(a, b):
    if not (np.isfinite(a) and np.isfinite(b)):
        return float("nan")
    den = max(abs(a), abs(b), 1e-300)
    return abs(a - b) / den


def make_figures(out: Path, by_n: dict):
    fig_dir = out / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    colors = {32: "C0", 48: "C1", 64: "C2"}
    keys_panels = [
        ("peak", "peak ρ  (ρ_max)"),
        ("PR", "PR  (participação)"),
        ("R_rms", "R_rms"),
        ("k_star", "k*"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
    for ax, (key, title) in zip(axes.ravel(), keys_panels):
        for N in NS:
            mets = by_n[N]["metrics"]
            t = [m["t"] for m in mets]
            v = [m[key] for m in mets]
            ax.plot(t, v, color=colors[N], label=f"N={N}", lw=1.4)
        ax.axvspan(0.8 * T_FINAL, T_FINAL, color="0.85", alpha=0.5, label="janela tardia" if ax is axes[0, 0] else None)
        ax.set_title(title)
        ax.set_xlabel("t")
        ax.grid(True, alpha=0.3)
        ax.legend(fontsize=8)
    fig.suptitle("Q01a — tríade completa, Theta_core, seed=0  (sem comparação MQ)")
    fig.tight_layout()
    fig.savefig(fig_dir / "overlay_observables.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(11.2, 8.0))
    late_keys = ["peak", "PR", "R_rms", "k_star"]
    titles = ["peak tardio", "PR tardio", "R_rms tardio", "k* tardio"]
    xs = np.arange(len(NS))
    for ax, key, title in zip(axes.ravel(), late_keys, titles):
        means = [by_n[N]["summary"][f"{key}_late_mean"] for N in NS]
        stds = [by_n[N]["summary"][f"{key}_late_std"] for N in NS]
        ax.bar(xs, means, yerr=stds, color=[colors[N] for N in NS], capsize=4, alpha=0.85)
        ax.set_xticks(xs)
        ax.set_xticklabels([f"N={N}" for N in NS])
        ax.set_title(title + "  (média ± std, último 20%)")
        ax.grid(True, axis="y", alpha=0.3)
    fig.suptitle("Q01a — comparação janela tardia entre grades")
    fig.tight_layout()
    fig.savefig(fig_dir / "late_window_comparison.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.2))
    for ax, N in zip(axes, NS):
        rho = by_n[N]["late_rho"]
        if rho is None:
            ax.set_title(f"N={N} sem ρ tardio")
            continue
        sl = rho[:, :, rho.shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        cells = by_n[N]["summary"]["peak_n_cells_half_final"]
        ax.set_title(f"N={N}  corte z=0  células½={cells}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("Q01a — ρ tardio (corte mediano). Volume preenchido = universo")
    fig.tight_layout()
    fig.savefig(fig_dir / "late_rho_midplane.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(6.4, 4.4))
    cells = [by_n[N]["summary"]["peak_n_cells_half_late_mean"] for N in NS]
    widths = [by_n[N]["summary"]["peak_width_phys_late_mean"] for N in NS]
    ax.plot(list(NS), cells, "o-", label="n células (ρ≥½ peak)")
    ax.set_xlabel("N")
    ax.set_ylabel("células")
    ax2 = ax.twinx()
    ax2.plot(list(NS), widths, "s--", color="C3", label="largura física")
    ax2.set_ylabel("largura física")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="best", fontsize=8)
    ax.set_title("Q01a — estrutura do pico vs N  (1–2 células = suspeita)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(fig_dir / "peak_structure_vs_N.png", dpi=150)
    plt.close(fig)


def l2_compare(by_n):
    out = {"method": "RegularGridInterpolator trilinear, periódico, grade comum N=64", "pairs": {}}
    try:
        rhos = {}
        for N in NS:
            rho = by_n[N]["late_rho"]
            if rho is None or not np.isfinite(rho).all():
                out["skipped"] = True
                out["reason"] = f"ρ tardio ausente/não-finito em N={N}"
                return out
            rhos[N] = rho if N == 64 else resample_rho(rho, N, 64, LBOX)
        dx64 = LBOX / 64.0
        dV = dx64 ** 3
        for a, b in ((32, 48), (48, 64), (32, 64)):
            ra, rb = rhos[a], rhos[b]
            # para 32 vs 48, reamostrar ambos a 64 já feito
            if a != 64:
                ra = rhos[a]
            if b != 64:
                rb = rhos[b]
            diff = ra - rb
            l2 = float(np.sqrt(np.sum(diff ** 2) * dV))
            nrm = float(np.sqrt(np.sum(rb ** 2) * dV))
            out["pairs"][f"{a}_vs_{b}"] = {
                "L2": l2,
                "L2_rel": l2 / max(nrm, 1e-300),
                "ref": b,
            }
        out["skipped"] = False
    except Exception as exc:
        out["skipped"] = True
        out["reason"] = f"resample falhou: {exc!r}"
    return out


def classify(by_n, l2info):
    nan_or_blow = False
    reasons = []
    for N in NS:
        s = by_n[N]["summary"]
        if s["blew_up"] or not s["finite_final"]:
            nan_or_blow = True
            reasons.append(f"N={N} NaN/blowup t={s['blow_t']}")
        for key in ("peak_late_mean", "PR_late_mean", "R_rms_late_mean"):
            if not np.isfinite(s[key]):
                nan_or_blow = True
                reasons.append(f"N={N} {key} não-finito")

    diffs = {}
    for key in ("peak", "PR", "R_rms"):
        a = by_n[48]["summary"][f"{key}_late_mean"]
        b = by_n[64]["summary"][f"{key}_late_mean"]
        diffs[key] = rel_diff(a, b)

    # também 32 vs 48 para contexto
    diffs_32_48 = {}
    for key in ("peak", "PR", "R_rms"):
        a = by_n[32]["summary"][f"{key}_late_mean"]
        b = by_n[48]["summary"][f"{key}_late_mean"]
        diffs_32_48[key] = rel_diff(a, b)

    finite_diffs = [v for v in diffs.values() if np.isfinite(v)]
    eps_num = float(max(finite_diffs)) if finite_diffs else float("nan")
    wild = any((np.isfinite(v) and v > 0.50) for v in diffs.values()) or not finite_diffs
    agree20 = all((np.isfinite(v) and v <= 0.20) for v in diffs.values())

    artifact = any(by_n[N]["summary"]["artifact_1_2_cells_final"] for N in NS)
    artifact_persist = all(
        by_n[N]["summary"].get("peak_n_cells_half_late_mean", 99) <= 2.5 for N in NS
    )

    if nan_or_blow:
        verdict = "NUMERICAL_FAILURE"
        note = "NaN ou blowup — exclusão técnica do protocolo."
    elif wild:
        verdict = "NUMERICAL_FAILURE"
        note = "peak/PR/R_rms da janela tardia divergem wildly entre N=48 e N=64 (>50%)."
    elif agree20:
        verdict = "INCONCLUSIVE"
        note = (
            "peak/PR/R_rms concordam dentro de ~20% entre N=48 e N=64; "
            "grade ainda grossa (Q01a sem N=96 / dt-refine). "
            "ok-enough para continuar a Q01b. Nunca SUPPORTED para MQ aqui."
        )
    else:
        verdict = "INCONCLUSIVE"
        note = (
            "Diferenças N=48 vs N=64 entre 20% e 50%; ε_num grosso; "
            "não é falha catastrófica nem convergência apertada."
        )

    return {
        "verdict": verdict,
        "note": note,
        "reasons": reasons,
        "rel_diff_48_vs_64": diffs,
        "rel_diff_32_vs_48": diffs_32_48,
        "epsilon_num_estimate": eps_num,
        "epsilon_num_definition": (
            "máximo da diferença relativa |A-B|/max(|A|,|B|) das médias "
            "da janela tardia (último 20% de T) de peak, PR, R_rms entre N=48 e N=64"
        ),
        "agree_within_20pct_48_64": agree20,
        "diverge_wildly_50pct": wild,
        "artifact_1_2_cells_any": artifact,
        "artifact_1_2_cells_all_N": artifact_persist,
        "l2": l2info,
        "qm_comparison": False,
        "supported_for_qm": False,
    }


def write_analysis(out: Path, by_n, classif, started_iso, finished_iso):
    lines = []
    lines.append("# Q01a — Análise (convergência numérica da tríade completa)")
    lines.append("")
    lines.append("Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.")
    lines.append("Pilotos 27–29 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.")
    lines.append("Theta_core intocado (Q00).")
    lines.append("")
    lines.append("## Pergunta")
    lines.append("")
    lines.append("Os observáveis convergem quando N aumenta, com a mesma física, mesma seed, mesmo T, mesmo dt?")
    lines.append("")
    lines.append("## Setup")
    lines.append("")
    lines.append(f"- Theta_core: Λ={LAMBDA}, α={ALPHA}, σ={SIGMA_FRAC}, Γ={GAMMA}, ν={NU}, λ={LAM}, kT={KT}")
    lines.append(f"- L={LBOX}, dt={DT}, T={T_FINAL}, seed={SEED}, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0")
    lines.append(f"- FDT: f_FDT_e=2Γ dx³ kT/ℏ ; incremento spec eq. 4")
    lines.append(f"- N ∈ {list(NS)}; fp64; backend {BACKEND}; Strang standalone")
    lines.append(f"- início (America/Sao_Paulo): {started_iso}")
    lines.append(f"- fim (America/Sao_Paulo): {finished_iso}")
    lines.append("")
    lines.append("## Tempos de parede")
    lines.append("")
    lines.append("| N | dx | wall_s | wall_min | finito |")
    lines.append("|---|---|---|---|---|")
    for N in NS:
        s = by_n[N]["summary"]
        lines.append(
            f"| {N} | {s['dx']:.6f} | {s['wall_s']:.3f} | {s['wall_s']/60.0:.3f} | {s['finite_final']} |"
        )
    lines.append("")
    lines.append("## Janela tardia (t ≥ 0.8 T = 6.4) — média ± std")
    lines.append("")
    header = (
        "| N | norm | peak | PR | R_rms | k* | k*L | Vmem_peak | "
        "células½ | largura_fís | 1–2 células |"
    )
    lines.append(header)
    lines.append("|" + "|".join(["---"] * 11) + "|")
    for N in NS:
        s = by_n[N]["summary"]

        def fmt(key):
            m, e = s[f"{key}_late_mean"], s[f"{key}_late_std"]
            if not np.isfinite(m):
                return "NaN"
            return f"{m:.6g} ± {e:.3g}"

        art = "SIM" if s["artifact_1_2_cells_final"] else "não"
        lines.append(
            f"| {N} | {fmt('norm')} | {fmt('peak')} | {fmt('PR')} | {fmt('R_rms')} | "
            f"{fmt('k_star')} | {fmt('k_star_L')} | {fmt('Vmem_peak')} | "
            f"{fmt('peak_n_cells_half')} | {fmt('peak_width_phys')} | {art} |"
        )
    lines.append("")
    lines.append("## Diferenças relativas N=48 vs N=64 (critério pré-declarado ~20%)")
    lines.append("")
    for key, val in classif["rel_diff_48_vs_64"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append("")
    lines.append("Diferenças N=32 vs N=48 (contexto, não critério):")
    for key, val in classif["rel_diff_32_vs_48"].items():
        lines.append(f"- {key}: {val:.4f} ({100*val:.1f}%)" if np.isfinite(val) else f"- {key}: NaN")
    lines.append("")
    lines.append(f"ε_num estimado = {classif['epsilon_num_estimate']}")
    lines.append(f"definição: {classif['epsilon_num_definition']}")
    lines.append("")
    lines.append("## L2 de ρ tardio (reamostrado para N=64)")
    lines.append("")
    if classif["l2"].get("skipped"):
        lines.append(f"Omitido: {classif['l2'].get('reason', 'não disponível')}.")
    else:
        lines.append(f"Método: {classif['l2']['method']}")
        for pair, d in classif["l2"]["pairs"].items():
            lines.append(f"- {pair}: L2={d['L2']:.6g}  L2_rel={d['L2_rel']:.6g}  (ref N={d['ref']})")
    lines.append("")
    lines.append("## Estruturas de 1–2 células")
    lines.append("")
    if classif["artifact_1_2_cells_all_N"]:
        lines.append(
            "O pico permanece em 1–2 células em todos os N: **suspeita de artefato de grade** "
            "(blueprint § Q01 / Q31). A largura física ~ dx."
        )
    elif classif["artifact_1_2_cells_any"]:
        lines.append("Pelo menos um N tem pico em 1–2 células. Ver tabela. Suspeita parcial de artefato.")
    else:
        lines.append("O pico não está preso a 1–2 células em nenhum N final.")
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
    lines.append("")
    lines.append("## Arquivos")
    lines.append("")
    lines.append(f"- pasta: `{out}`")
    lines.append("- PROTOCOL.md, config.json, seeds.txt, code/run_q01a.py")
    lines.append("- raw/N{32,48,64}_metrics.csv, raw/N*_summary.json, raw/N*_rho_late.npy")
    lines.append("- metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt")
    lines.append("")
    text = "\n".join(lines) + "\n"
    (out / "analysis.md").write_text(text, encoding="utf-8")


def write_sha256sums(out: Path):
    paths = []
    for p in sorted(out.rglob("*")):
        if p.is_file() and p.name != "SHA256SUMS.txt" and p.name != ".write_test":
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
    parser.add_argument("--N", type=int, nargs="*", default=list(NS))
    parser.add_argument("--out", type=str, default="")
    args = parser.parse_args()
    ns = tuple(args.N) if args.N else NS
    out = Path(args.out) if args.out else resolve_out()
    out.mkdir(parents=True, exist_ok=True)
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "figures").mkdir(parents=True, exist_ok=True)
    (out / "code").mkdir(parents=True, exist_ok=True)

    started = now_sp()
    print("Q01a start", started, "out", out, flush=True)

    by_n = {}
    all_metrics = []
    for N in ns:
        summary, metrics, late_rho = run_one(N, out)
        by_n[N] = {"summary": summary, "metrics": metrics, "late_rho": late_rho}
        all_metrics.extend(metrics)

    # precisa dos 3 N para figures/classificação
    if set(by_n.keys()) != set(NS):
        print("partial_run", sorted(by_n.keys()), flush=True)

    if all_metrics:
        write_csv(out / "metrics.csv", all_metrics, list(all_metrics[0].keys()))

    l2info = {"skipped": True, "reason": "N incompleto"}
    classif = None
    if set(by_n.keys()) == set(NS):
        make_figures(out, by_n)
        l2info = l2_compare(by_n)
        classif = classify(by_n, l2info)
        finished = now_sp()
        write_analysis(out, by_n, classif, started, finished)
        result = {
            "question": "Q01a",
            "title": "convergência numérica da tríade completa",
            "qm_comparison": False,
            "theta_core_unchanged": True,
            "terms_isolated": False,
            "pilots_27_29_confirmatory": False,
            "verdict": classif["verdict"],
            "note": classif["note"],
            "epsilon_num": classif["epsilon_num_estimate"],
            "epsilon_num_definition": classif["epsilon_num_definition"],
            "rel_diff_48_vs_64": classif["rel_diff_48_vs_64"],
            "rel_diff_32_vs_48": classif["rel_diff_32_vs_48"],
            "agree_within_20pct_48_64": classif["agree_within_20pct_48_64"],
            "artifact_1_2_cells_any": classif["artifact_1_2_cells_any"],
            "artifact_1_2_cells_all_N": classif["artifact_1_2_cells_all_N"],
            "l2": classif["l2"],
            "supported_for_qm": False,
            "technical_exclusion": "NaN/blowup only",
            "N": list(NS),
            "L": LBOX,
            "dt": DT,
            "T": T_FINAL,
            "seed": SEED,
            "backend": BACKEND,
            "fp": "fp64",
            "wall_s": {str(N): by_n[N]["summary"]["wall_s"] for N in NS},
            "late_window": {
                str(N): {
                    k: by_n[N]["summary"][k]
                    for k in by_n[N]["summary"]
                    if k.endswith("_late_mean")
                    or k.endswith("_late_std")
                    or k.endswith("_late_n")
                }
                for N in NS
            },
            "started_america_sao_paulo": started,
            "finished_america_sao_paulo": finished,
            "out": str(out),
        }
        with (out / "result.json").open("w") as f:
            json.dump(result, f, indent=2)
        print("VERDICT", classif["verdict"], flush=True)
        print("EPS_NUM", classif["epsilon_num_estimate"], flush=True)
        print("NOTE", classif["note"], flush=True)
    else:
        finished = now_sp()

    write_sha256sums(out)
    print("wrote", out, "finished", finished, flush=True)


if __name__ == "__main__":
    main()
