#!/usr/bin/env python3
"""Run 27 triad_chaos_eq — equação TRIAD completa, 12 átomos gaussianos.

1 gaussiana = 1 átomo. Sem init='chaos' (campo aleatório). Sem ablação.
Sem calibração. NLS + memória + FDT juntos. seed=0.
"""
from __future__ import annotations

import csv
import json
import sys
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import maximum_filter

SRC = "/Users/leo/Documents/LabX/triad-lang/src"
sys.path.insert(0, SRC)

from runtime.backend import asnumpy, backend_capabilities, get_xp
from runtime.core.solver import (
    TriadParams,
    memory_nls_strang_step_3d,
    prepare_memory_nls_3d,
)

VAULT = Path("/Users/leo/Documents/Triad/T")
OUT = VAULT / "Artefatos" / "triad_chaos_eq"
RUN_ID = "27"
RUN_NAME = "triad_chaos_eq"

# --- decisão única, sem scan ---
N_ATOMS = 12
ATOM_SIGMA = 1.2
MIN_SEP = 4.8  # 4 * sigma; átomos distintos no t=0
N = 32
L = 32.0
DT = 0.0025
T = 15.0
RECORD_EVERY = 40
SEED = 0
LAMBDA = -10.0
NU = (10.0, 0.5, 0.05)
LAM = (3.0, 1.0, 0.3)
GAMMA = 0.05
PEAK_FRAC = 0.20  # máximo local conta como átomo se rho >= PEAK_FRAC * peak


def min_image(delta, box):
    return delta - box * np.round(delta / box)


def place_atoms(n_atoms, box, min_sep, rng, max_tries=50000):
    pos = []
    for i in range(n_atoms):
        placed = False
        for _ in range(max_tries):
            cand = rng.uniform(-box / 2.0, box / 2.0, size=3)
            ok = True
            for p in pos:
                if np.linalg.norm(min_image(cand - p, box)) < min_sep:
                    ok = False
                    break
            if ok:
                pos.append(cand)
                placed = True
                break
        if not placed:
            raise RuntimeError(
                f"falhou posicionar átomo {i + 1}/{n_atoms} com min_sep={min_sep}"
            )
    return np.asarray(pos, dtype=np.float64)


def build_atom_cloud(xs, box, positions, phases, sigma, xp):
    X, Y, Z = xp.meshgrid(xs, xs, xs, indexing="ij")
    psi = xp.zeros(X.shape, dtype=xp.complex128)
    for (x0, y0, z0), ph in zip(positions, phases):
        dx = min_image(X - x0, box)
        dy = min_image(Y - y0, box)
        dz = min_image(Z - z0, box)
        r2 = dx * dx + dy * dy + dz * dz
        psi = psi + xp.exp(-r2 / (2.0 * sigma * sigma)) * xp.exp(1j * ph)
    return psi


def mass_radii(rho, r, dV, fractions=(0.5, 0.8, 0.9)):
    """Menor r com massa acumulada >= f * norma. Células ordenadas por r."""
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


def local_atom_peaks(rho, peak, frac, dx):
    """Máximos locais 3x3x3 com wrap periódico; rho >= frac * peak."""
    footprint = maximum_filter(rho, size=3, mode="wrap")
    is_max = (rho == footprint) & (rho >= frac * peak) & (peak > 0)
    coords = np.argwhere(is_max)
    vals = rho[is_max]
    if coords.size == 0:
        return coords, vals
    order = np.argsort(-vals)
    return coords[order], vals[order]


def nn_spacing(coords, box, dx):
    if coords.shape[0] < 2:
        return float("nan"), float("nan")
    xyz = coords.astype(np.float64) * dx
    xyz = xyz - box / 2.0
    n = xyz.shape[0]
    nn = np.empty(n, dtype=np.float64)
    for i in range(n):
        d = min_image(xyz - xyz[i], box)
        dist = np.sqrt((d * d).sum(axis=1))
        dist[i] = np.inf
        nn[i] = dist.min()
    return float(nn.mean()), float(np.median(nn))


def spectral_from_rho(rho, dx, box):
    """k* e C a partir de FFT(rho). Barato; não é |hat Psi|^2."""
    pwr = np.abs(np.fft.fftn(rho)) ** 2
    k = 2.0 * np.pi * np.fft.fftfreq(rho.shape[0], d=dx)
    kx, ky, kz = np.meshgrid(k, k, k, indexing="ij")
    kabs = np.sqrt(kx * kx + ky * ky + kz * kz)
    k_min = 2.0 * np.pi / box
    total = float(pwr.sum())
    cryst = float(pwr[kabs > k_min].sum() / total) if total > 0 else 0.0
    mask = kabs > k_min
    if not np.any(mask) or total <= 0:
        return 0.0, cryst
    kb = kabs[mask].ravel()
    pb = pwr[mask].ravel()
    n_bins = 24
    bins = np.linspace(k_min, float(kb.max()) + 1e-12, n_bins + 1)
    idx = np.clip(np.digitize(kb, bins) - 1, 0, n_bins - 1)
    shell = np.bincount(idx, weights=pb, minlength=n_bins)
    j = int(np.argmax(shell))
    kstar = 0.5 * (bins[j] + bins[j + 1])
    return float(kstar), cryst


def write_csv(path, rows, fieldnames):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    t_wall0 = time.perf_counter()

    p = TriadParams(
        L=L,
        N=N,
        dt=DT,
        T=T,
        V_ext=None,
        omega=0.05,
        Lambda=LAMBDA,
        Gamma=GAMMA,
        nu=NU,
        lam=LAM,
        seed=SEED,
        record_every=RECORD_EVERY,
        D=3,
        backend="auto",
        bc="periodic",
        fdt_couple=True,
        kT=1.0,
        init="gaussian",
    )

    xp = get_xp(getattr(p, "backend", "auto"))
    backend_name = getattr(xp, "__name__", type(xp).__name__)
    caps = backend_capabilities()
    print("backend_xp", backend_name, flush=True)
    print("backend_caps", caps, flush=True)
    print("params", "N", p.N, "L", p.L, "dt", p.dt, "T", p.T, "V_ext", p.V_ext, flush=True)
    print("Lambda", p.Lambda, "nu", p.nu, "lam", p.lam, "Gamma", p.Gamma, flush=True)
    print("atoms", N_ATOMS, "sigma", ATOM_SIGMA, "min_sep", MIN_SEP, flush=True)

    rng_np = np.random.default_rng(SEED)
    positions = place_atoms(N_ATOMS, L, MIN_SEP, rng_np)
    phases = rng_np.uniform(0.0, 2.0 * np.pi, size=N_ATOMS)

    xs_np = np.linspace(-L / 2.0, L / 2.0, N, endpoint=False)
    dx = float(xs_np[1] - xs_np[0])
    dV = dx ** 3
    Xn, Yn, Zn = np.meshgrid(xs_np, xs_np, xs_np, indexing="ij")
    r2 = Xn * Xn + Yn * Yn + Zn * Zn
    r = np.sqrt(r2)

    xs = xp.asarray(xs_np)
    psi = build_atom_cloud(xs, L, positions, phases, ATOM_SIGMA, xp)
    norm0 = float(asnumpy((xp.abs(psi) ** 2).sum() * dV))
    psi = psi / xp.sqrt(asnumpy((xp.abs(psi) ** 2).sum() * dV))
    y = xp.zeros((len(p.nu), p.N, p.N, p.N), dtype=xp.float64)

    law = prepare_memory_nls_3d(p, xp)
    V_ext = xp.zeros((p.N, p.N, p.N), dtype=xp.float64)
    rng_step = xp.random.default_rng(p.seed)

    # mesmo gerador de ruído FDT que integrate_3d (seed=0), IC próprio
    n_steps = int(round(p.T / p.dt))
    rec_every = max(1, p.record_every)
    mid_z = p.N // 2

    atom_rows = []
    for i, ((x0, y0, z0), ph) in enumerate(zip(positions, phases)):
        atom_rows.append(
            {
                "atom": i,
                "x": float(x0),
                "y": float(y0),
                "z": float(z0),
                "phase": float(ph),
                "sigma": ATOM_SIGMA,
            }
        )
    write_csv(
        OUT / "atoms_ic.csv",
        atom_rows,
        ["atom", "x", "y", "z", "phase", "sigma"],
    )

    seps = []
    for i in range(N_ATOMS):
        for j in range(i + 1, N_ATOMS):
            seps.append(float(np.linalg.norm(min_image(positions[i] - positions[j], L))))
    seps = np.asarray(seps)

    metrics = []
    midplanes = {}
    snapshot_times = {0.0, 3.75, 7.5, 11.25, 15.0}

    print("n_steps", n_steps, "record_every", rec_every, "dx", dx, flush=True)
    print("f_FDT_e_noise_amp", law["noise_amplitude"], flush=True)
    print("ic_pair_sep_min", float(seps.min()), "mean", float(seps.mean()), flush=True)

    for step in range(n_steps + 1):
        t = step * p.dt
        rho_xp = xp.abs(psi) ** 2
        if step % rec_every == 0 or step == n_steps:
            rho = np.asarray(asnumpy(rho_xp), dtype=np.float64)
            y_np = np.asarray(asnumpy(y), dtype=np.float64)
            vmem = (np.asarray(LAM, dtype=np.float64).reshape(-1, 1, 1, 1) * y_np).sum(axis=0)
            norm = float(rho.sum() * dV)
            peak = float(rho.max())
            rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
            r50, r80, r90 = mass_radii(rho, r, dV)
            pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
            coords, pvals = local_atom_peaks(rho, peak, PEAK_FRAC, dx)
            n_det = int(coords.shape[0])
            nn_mean, nn_med = nn_spacing(coords, L, dx)
            kstar, cryst = spectral_from_rho(rho, dx, L)
            rec = {
                "t": t,
                "norm": norm,
                "peak": peak,
                "R_rms": rrms,
                "r50": r50,
                "r80": r80,
                "r90": r90,
                "PR": pr,
                "Vmem_peak": float(vmem.max()) if vmem.size else 0.0,
                "Vmem_mean": float(vmem.mean()) if vmem.size else 0.0,
                "n_atoms_detected": n_det,
                "nn_mean": nn_mean,
                "nn_median": nn_med,
                "kstar": kstar,
                "kstarL": kstar * L,
                "cryst": cryst,
            }
            metrics.append(rec)
            t_key = round(t, 6)
            if any(abs(t - s) < 0.5 * p.dt * rec_every + 1e-12 for s in snapshot_times):
                midplanes[t_key] = rho[:, :, mid_z].copy()
            print(
                f"t={t:.4f} norm={norm:.6f} peak={peak:.6e} Rrms={rrms:.4f} "
                f"n_at={n_det} PR={pr:.3f}",
                flush=True,
            )
        if step == n_steps:
            break
        psi, y, _ = memory_nls_strang_step_3d(
            psi,
            y,
            xp=xp,
            law=law,
            external_potential=V_ext,
            dt=p.dt,
            hbar=p.hbar,
            normal_provider=rng_step.standard_normal,
            bc_mask=None,
        )

    wall = time.perf_counter() - t_wall0
    print("wall_s", wall, flush=True)

    fields = list(metrics[0].keys())
    write_csv(OUT / "metrics.csv", metrics, fields)

    t_arr = np.array([m["t"] for m in metrics])
    late = t_arr >= (0.8 * T)
    early = t_arr <= (0.2 * T)

    def series(key):
        return np.array([m[key] for m in metrics], dtype=np.float64)

    def stats(key, mask):
        v = series(key)[mask]
        return float(v.mean()), float(v.std()), float(v[0]) if v.size else float("nan")

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "backend_xp": backend_name,
        "backend_caps": json.dumps(caps),
        "stepper": "memory_nls_strang_step_3d",
        "N": N,
        "L": L,
        "dt": DT,
        "T": T,
        "record_every": RECORD_EVERY,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "dx": dx,
        "Lambda": LAMBDA,
        "nu": str(NU),
        "lam": str(LAM),
        "Gamma": GAMMA,
        "V_ext": "None",
        "seed": SEED,
        "n_atoms": N_ATOMS,
        "atom_sigma": ATOM_SIGMA,
        "min_sep": MIN_SEP,
        "peak_frac_atom": PEAK_FRAC,
        "ic_pair_sep_min": float(seps.min()),
        "ic_pair_sep_mean": float(seps.mean()),
        "noise_amplitude": float(law["noise_amplitude"]),
        "wall_s": wall,
        "norm_initial": metrics[0]["norm"],
        "norm_final": metrics[-1]["norm"],
        "peak_initial": metrics[0]["peak"],
        "peak_max": float(series("peak").max()),
        "t_peak": float(t_arr[int(series("peak").argmax())]),
        "peak_final": metrics[-1]["peak"],
        "PR_initial": metrics[0]["PR"],
        "PR_final": metrics[-1]["PR"],
        "R_rms_initial": metrics[0]["R_rms"],
        "R_rms_final": metrics[-1]["R_rms"],
        "r50_initial": metrics[0]["r50"],
        "r50_final": metrics[-1]["r50"],
        "r80_initial": metrics[0]["r80"],
        "r80_final": metrics[-1]["r80"],
        "r90_initial": metrics[0]["r90"],
        "r90_final": metrics[-1]["r90"],
        "n_atoms_detected_initial": metrics[0]["n_atoms_detected"],
        "n_atoms_detected_final": metrics[-1]["n_atoms_detected"],
        "nn_mean_initial": metrics[0]["nn_mean"],
        "nn_mean_final": metrics[-1]["nn_mean"],
        "Vmem_peak_max": float(series("Vmem_peak").max()),
        "t_Vmem_peak": float(t_arr[int(series("Vmem_peak").argmax())]),
        "Vmem_peak_final": metrics[-1]["Vmem_peak"],
    }
    for key in ("peak", "PR", "R_rms", "n_atoms_detected", "kstarL", "cryst", "nn_mean"):
        em, es, _ = stats(key, early)
        lm, ls, _ = stats(key, late)
        summary[f"{key}_early_mean"] = em
        summary[f"{key}_early_std"] = es
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls

    write_csv(OUT / "summary.csv", [summary], list(summary.keys()))
    with (OUT / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    # figures
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(t_arr, series("R_rms"), label="R_rms")
    ax.plot(t_arr, series("r50"), label="r50")
    ax.plot(t_arr, series("r80"), label="r80")
    ax.plot(t_arr, series("r90"), label="r90")
    ax.set_xlabel("t")
    ax.set_ylabel("raio")
    ax.set_title("27 triad_chaos_eq — raios (12 átomos, N=32)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "01_radii_vs_t.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.plot(t_arr, series("peak"), color="C3")
    ax.set_xlabel("t")
    ax.set_ylabel("peak ρ")
    ax.set_title("pico de densidade")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "02_peak_vs_t.png", dpi=140)
    plt.close(fig)

    fig, ax1 = plt.subplots(figsize=(8, 4.2))
    ax1.plot(t_arr, series("n_atoms_detected"), color="C0", label="n_átomos detectados")
    ax1.axhline(N_ATOMS, color="C0", ls="--", alpha=0.5, label="n_atoms IC=12")
    ax1.set_xlabel("t")
    ax1.set_ylabel("contagem")
    ax2 = ax1.twinx()
    ax2.plot(t_arr, series("nn_mean"), color="C1", label="⟨NN⟩")
    ax2.set_ylabel("espaçamento NN")
    h1, l1 = ax1.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax1.legend(h1 + h2, l1 + l2, loc="best")
    ax1.set_title(f"átomos detectados (máx. local, ρ≥{PEAK_FRAC}·peak)")
    ax1.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "03_atoms_count_spacing.png", dpi=140)
    plt.close(fig)

    keys_sorted = sorted(midplanes.keys())
    nsnap = max(1, len(keys_sorted))
    fig, axes = plt.subplots(1, nsnap, figsize=(3.2 * nsnap, 3.2))
    if nsnap == 1:
        axes = [axes]
    for ax, tk in zip(axes, keys_sorted):
        im = ax.imshow(midplanes[tk].T, origin="lower", extent=[-L / 2, L / 2, -L / 2, L / 2])
        ax.set_title(f"xy z=0  t={tk:.2f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.suptitle("planos médios — 12 átomos gaussianos")
    fig.tight_layout()
    fig.savefig(OUT / "04_midplane_snapshots.png", dpi=140)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5))
    axes[0, 0].plot(t_arr, series("norm"))
    axes[0, 0].set_title("norma")
    axes[0, 1].plot(t_arr, series("PR"))
    axes[0, 1].set_title("PR")
    axes[1, 0].plot(t_arr, series("Vmem_peak"), label="Vmem_peak")
    axes[1, 0].plot(t_arr, series("Vmem_mean"), label="Vmem_mean")
    axes[1, 0].legend()
    axes[1, 0].set_title("V_mem")
    axes[1, 1].plot(t_arr, series("cryst"), label="C (FFT ρ)")
    axes[1, 1].plot(t_arr, series("kstarL") / max(series("kstarL").max(), 1e-12), label="k*L / max")
    axes[1, 1].legend()
    axes[1, 1].set_title("espectro barato (de ρ)")
    for ax in axes.ravel():
        ax.set_xlabel("t")
        ax.grid(True, alpha=0.3)
    fig.suptitle("27 triad_chaos_eq — norma, PR, memória, espectro")
    fig.tight_layout()
    fig.savefig(OUT / "05_norm_pr_vmem.png", dpi=140)
    plt.close(fig)

    fig = plt.figure(figsize=(11, 8))
    gs = fig.add_gridspec(2, 3)
    ax = fig.add_subplot(gs[0, :2])
    ax.plot(t_arr, series("R_rms"), label="R_rms")
    ax.plot(t_arr, series("r50"), label="r50")
    ax.plot(t_arr, series("r80"), label="r80")
    ax.plot(t_arr, series("r90"), label="r90")
    ax.legend()
    ax.set_title("raios")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(t_arr, series("n_atoms_detected"))
    ax.axhline(12, ls="--", alpha=0.5)
    ax.set_title("n átomos det.")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(t_arr, series("peak"), color="C3")
    ax.set_title("peak")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 1])
    if keys_sorted:
        ax.imshow(midplanes[keys_sorted[0]].T, origin="lower")
        ax.set_title(f"xy t={keys_sorted[0]:.2f}")
    ax = fig.add_subplot(gs[1, 2])
    if keys_sorted:
        ax.imshow(midplanes[keys_sorted[-1]].T, origin="lower")
        ax.set_title(f"xy t={keys_sorted[-1]:.2f}")
    fig.suptitle("27 triad_chaos_eq — 12 átomos, equação completa, N=32")
    fig.tight_layout()
    fig.savefig(OUT / "00_montagem.png", dpi=140)
    plt.close(fig)

    print("wrote", OUT, flush=True)
    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(summary), flush=True)
    print("SUMMARY_JSON_END", flush=True)


if __name__ == "__main__":
    main()
