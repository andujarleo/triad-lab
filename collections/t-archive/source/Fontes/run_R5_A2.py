#!/usr/bin/env python3
"""Run 29 triad_R5_A2 — spec v1.0 Appendix A.2 R5-FDT, mode=full.

Standalone 3D Strang (spec §3 + §5). Does NOT use triad-lang TriadParams
(that type rejects 2 memory modes). 1 gaussian = 1 atom, IC §9.1.
N reduced vs spec 128. No §6 ablations. No k*L calibration.
"""
from __future__ import annotations

import csv
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

VAULT = Path("/Users/leo/Documents/Triad/T")
OUT = VAULT / "Artefatos" / "triad_R5_A2"
RUN_ID = "29"
RUN_NAME = "triad_R5_A2"

# --- A.2 + spec "use 0.01 / 0.001 for R5-FDT" ---
HBAR = 1.0
M_MASS = 1.0
LAMBDA = -8.0
SIGMA_FRAC = 1.5
ALPHA = 0.0
GAMMA = 0.01
T_BATH = 0.001
NU = (10.0, 0.5)
LAM = (1.125, 0.375)
LBOX = 20.0
N_SPEC = 128
N = 96
DT = 0.0025
T_FINAL = 15.0
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
SEED = 42
RECORD_EVERY = 40
ISO_FRAC = 0.30
ELEV = 22.0
AZIM = -60.0
N_REASON = "N=64 step ~0.014s < 0.05s; bumped to 96 (still reduced vs spec 128)"
K_CUT_FACTOR = 1.0

try:
    from skimage.measure import marching_cubes
    HAS_MC = True
except Exception:
    HAS_MC = False


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


def setup_3d_box(ax, box):
    h = box / 2.0
    ax.set_xlim(-h, h)
    ax.set_ylim(-h, h)
    ax.set_zlim(-h, h)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.view_init(elev=ELEV, azim=AZIM)
    try:
        ax.set_box_aspect((1, 1, 1))
    except Exception:
        pass
    corners = np.array(
        [
            [-h, -h, -h], [h, -h, -h], [h, h, -h], [-h, h, -h],
            [-h, -h, h], [h, -h, h], [h, h, h], [-h, h, h],
        ]
    )
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),
        (4, 5), (5, 6), (6, 7), (7, 4),
        (0, 4), (1, 5), (2, 6), (3, 7),
    ]
    for a, b in edges:
        p0, q0 = corners[a], corners[b]
        ax.plot([p0[0], q0[0]], [p0[1], q0[1]], [p0[2], q0[2]],
                color="0.35", lw=0.7, alpha=0.7)


def plot_isosurface(ax, rho, level, dx, box, color="#2b6cb0"):
    used = "scatter"
    if HAS_MC and level > 0 and float(rho.max()) > level:
        try:
            verts, faces, *_ = marching_cubes(rho, level=level, spacing=(dx, dx, dx))
            verts = verts - box / 2.0
            mesh = Poly3DCollection(verts[faces], alpha=0.32, linewidths=0.04)
            mesh.set_facecolor(color)
            mesh.set_edgecolor((0.15, 0.15, 0.2, 0.06))
            ax.add_collection3d(mesh)
            used = "marching_cubes"
            setup_3d_box(ax, box)
            return used
        except Exception as exc:
            print("marching_cubes_failed", exc, flush=True)
    mask = rho >= level
    ii = np.argwhere(mask)
    if ii.shape[0] == 0:
        setup_3d_box(ax, box)
        return "empty"
    if ii.shape[0] > 8000:
        rng = np.random.default_rng(0)
        ii = ii[rng.choice(ii.shape[0], 8000, replace=False)]
    xyz = ii.astype(np.float64) * dx - box / 2.0
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=6, c=color, alpha=0.28, depthshade=False)
    setup_3d_box(ax, box)
    return used


def save_isosurface_fig(path, rho, peak, dx, box, title):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    level = ISO_FRAC * peak if peak > 0 else 0.0
    used = plot_isosurface(ax, rho, level, dx, box)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used, level


def spectral_observables(psi, k_mag, dk, k_cut):
    """§8.3 radial power of Psi-hat, k* and crystallinity C."""
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


def build_state(N):
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    r = np.sqrt(r2)
    kvec = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(kvec, kvec, kvec, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k_mag = np.sqrt(k2)
    # eq (8): H_lin = hbar^2 |k|^2 / (2m) + alpha |k|^sigma
    H_lin = (HBAR * HBAR * k2) / (2.0 * M_MASS)
    if ALPHA != 0.0:
        H_lin = H_lin + ALPHA * np.power(k_mag, SIGMA_FRAC)
    # eq (9)
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    # §9.1 single Gaussian
    s = INIT_SIGMA
    psi = np.exp(-r2 / (2.0 * s * s)).astype(np.complex128)
    k0x, k0y, k0z = INIT_K0
    if k0x != 0.0 or k0y != 0.0 or k0z != 0.0:
        psi = psi * np.exp(1j * (k0x * X + k0y * Y + k0z * Z))
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.zeros((len(NU), N, N, N), dtype=np.float64)
    # FDT lock same as run 28 fdt_couple: f_FDT = 2 Gamma dx^3 T_bath / hbar
    f_FDT = 2.0 * GAMMA * (dx ** 3) * T_BATH / HBAR
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    return {
        "x": x, "dx": dx, "dV": dV, "r2": r2, "r": r,
        "k_mag": k_mag, "half_lin": half_lin, "psi": psi, "y": y,
        "f_FDT": f_FDT, "noise_amp": noise_amp,
    }


def strang_step(psi, y, half_lin, noise_amp, rng, nu, lam):
    # 1. linear half-step
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    # 2-4. real-space potential
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((-1, 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem  # V_ext = 0
    psi = psi * np.exp(-1j * V_tot * DT / HBAR)
    # 5. memory: Euler because max(nu)*dt = 0.025 < 0.05 (spec §3.4)
    y = y + DT * nu.reshape((-1, 1, 1, 1)) * (rho - y)
    # 6. FDT kick eq (4)/(14)
    if noise_amp > 0.0:
        xi = (rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape)) / np.sqrt(2.0)
        psi = psi + noise_amp * xi
    # 7. linear half-step
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    return psi, y


def record_metrics(psi, y, t, dV, r2, r, k_mag, dk, k_cut, lam):
    rho = np.abs(psi) ** 2
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
    return rho, {
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
    }


def main():
    OUT.mkdir(parents=True, exist_ok=True)
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
    nu = np.asarray(NU, dtype=np.float64)
    lam = np.asarray(LAM, dtype=np.float64)
    rng = np.random.default_rng(SEED)

    n_steps = int(round(T_FINAL / DT))
    rec_every = max(1, RECORD_EVERY)
    snap_targets = {
        "ic": 0.0,
        "early": T_FINAL / 6.0,
        "mid": T_FINAL / 2.0,
        "late": T_FINAL,
    }
    volumes = {}
    snap_t = {}

    print("backend", "numpy", flush=True)
    print("N", N, "N_spec", N_SPEC, "reason", N_REASON, flush=True)
    print("L", LBOX, "dx", dx, "dt", DT, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("Lambda", LAMBDA, "nu", NU, "lam", LAM, "Gamma", GAMMA, "T_bath", T_BATH, flush=True)
    print("alpha", ALPHA, "sigma", SIGMA_FRAC, "V_ext", 0, "seed", SEED, flush=True)
    print("init_sigma", INIT_SIGMA, "init_k0", INIT_K0, flush=True)
    print("f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print("noise_amp_check_sqrt_2Gamma_Tbath_dt", float(np.sqrt(2.0 * GAMMA * T_BATH * DT)), flush=True)
    print("skimage_marching_cubes", HAS_MC, flush=True)
    print("max_nu_dt", float(max(NU) * DT), "memory_update", "euler", flush=True)

    metrics = []
    for step in range(n_steps + 1):
        t = step * DT
        if step % rec_every == 0 or step == n_steps:
            rho, rec = record_metrics(psi, y, t, dV, r2, r, k_mag, dk, k_cut, lam)
            metrics.append(rec)
            for name, t_tgt in snap_targets.items():
                if abs(t - t_tgt) < 0.5 * DT * rec_every + 1e-12:
                    volumes[name] = rho.copy()
                    snap_t[name] = t
            print(
                f"t={t:.4f} norm={rec['norm']:.6f} peak={rec['peak']:.6e} "
                f"PR={rec['PR']:.3f} Rrms={rec['R_rms']:.4f} "
                f"C={rec['crystallinity']:.4f} kL={rec['k_star_L']:.4f}",
                flush=True,
            )
        if step == n_steps:
            break
        psi, y = strang_step(psi, y, half_lin, noise_amp, rng, nu, lam)

    wall = time.perf_counter() - t_wall0
    print("wall_s", wall, flush=True)

    write_csv(OUT / "metrics.csv", metrics, list(metrics[0].keys()))

    t_arr = np.array([m["t"] for m in metrics])
    late = t_arr >= (0.8 * T_FINAL)
    early = t_arr <= (0.2 * T_FINAL)

    def series(key):
        return np.array([m[key] for m in metrics], dtype=np.float64)

    def stats(key, mask):
        v = series(key)[mask]
        return float(v.mean()), float(v.std())

    filled = bool(metrics[-1]["PR"] > 10.0 * metrics[0]["PR"] or metrics[-1]["R_rms"] > 2.0 * metrics[0]["R_rms"])
    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "spec": "triad_equation_reference.md v1.0",
        "appendix": "A.2",
        "ic": "§9.1 single Gaussian",
        "mode": "full",
        "solver": "spec §5 3D Strang (standalone, not triad-lang TriadParams)",
        "backend": "numpy",
        "N": N,
        "N_spec": N_SPEC,
        "N_label": "reduced vs spec N=128",
        "N_reason": N_REASON,
        "L": LBOX,
        "dx": dx,
        "dt": DT,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "record_every": rec_every,
        "hbar": HBAR,
        "m": M_MASS,
        "Lambda": LAMBDA,
        "sigma": SIGMA_FRAC,
        "alpha": ALPHA,
        "Gamma": GAMMA,
        "T_bath": T_BATH,
        "nu": str(NU),
        "lam": str(LAM),
        "V_ext": 0.0,
        "init_sigma": INIT_SIGMA,
        "init_k0": str(INIT_K0),
        "y0": 0.0,
        "seed": SEED,
        "f_FDT": f_FDT,
        "f_FDT_formula": "2*Gamma*(dx**3)*T_bath/hbar  (run-28 fdt_couple lock)",
        "noise_amp": noise_amp,
        "noise_amp_formula": "sqrt(f_FDT*dt/dx**3) = sqrt(2*Gamma*T_bath*dt/hbar)",
        "memory_update": "euler",
        "max_nu_dt": float(max(NU) * DT),
        "iso_frac": ISO_FRAC,
        "has_marching_cubes": HAS_MC,
        "wall_s": wall,
        "norm_initial": metrics[0]["norm"],
        "norm_final": metrics[-1]["norm"],
        "peak_initial": metrics[0]["peak"],
        "peak_final": metrics[-1]["peak"],
        "peak_max": float(series("peak").max()),
        "t_peak": float(t_arr[int(series("peak").argmax())]),
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
        "crystallinity_initial": metrics[0]["crystallinity"],
        "crystallinity_final": metrics[-1]["crystallinity"],
        "k_star_L_initial": metrics[0]["k_star_L"],
        "k_star_L_final": metrics[-1]["k_star_L"],
        "k_star_final": metrics[-1]["k_star"],
        "Vmem_peak_max": float(series("Vmem_peak").max()),
        "t_Vmem_peak": float(t_arr[int(series("Vmem_peak").argmax())]),
        "Vmem_peak_final": metrics[-1]["Vmem_peak"],
        "single_atom_seeds_filled_volume": filled,
        "snap_t": {k: float(v) for k, v in snap_t.items()},
    }
    for key in ("peak", "PR", "R_rms", "crystallinity", "k_star_L", "norm"):
        em, es = stats(key, early)
        lm, ls = stats(key, late)
        summary[f"{key}_early_mean"] = em
        summary[f"{key}_early_std"] = es
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls


    # --- figures, same camera as run 28 ---
    iso_used = {}
    fig_specs = [
        ("ic", "01_ic_isosurface.png", "29 IC isosuperfície  1 gaussiana §9.1  t={t:.2f}"),
        ("early", "02_isosurface_early.png", "29 isosuperfície early  t={t:.2f}  ρ={frac:.1f}·peak"),
        ("mid", "03_isosurface_mid.png", "29 isosuperfície mid  t={t:.2f}  ρ={frac:.1f}·peak"),
        ("late", "04_isosurface_late.png", "29 isosuperfície late  universo no cubo  t={t:.2f}"),
    ]
    for key, fname, title_tmpl in fig_specs:
        if key not in volumes:
            print("missing_volume", key, flush=True)
            continue
        rho = volumes[key]
        peak = float(rho.max())
        tt = snap_t.get(key, -1.0)
        used, level = save_isosurface_fig(
            OUT / fname,
            rho,
            peak,
            dx,
            LBOX,
            title_tmpl.format(t=tt, frac=ISO_FRAC),
        )
        iso_used[key] = {"method": used, "level": level, "peak": peak, "t": tt}
        print("iso", key, "t", tt, "method", used, "level", level, "peak", peak, flush=True)
    summary["iso_used"] = json.dumps(iso_used)

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 7.4))
    axes[0, 0].plot(t_arr, series("peak"), color="C3")
    axes[0, 0].set_title("peak ρ  (§8.1)")
    axes[0, 1].plot(t_arr, series("PR"), color="C0")
    axes[0, 1].set_title("PR  (§8.1)")
    axes[1, 0].plot(t_arr, series("R_rms"), color="C2")
    axes[1, 0].set_title("R_rms")
    ax = axes[1, 1]
    ax.plot(t_arr, series("crystallinity"), color="C4", label="C(t) cryst")
    ax.set_ylabel("C")
    ax2 = ax.twinx()
    ax2.plot(t_arr, series("k_star_L"), color="C5", ls="--", label="k*L")
    ax2.set_ylabel("k*L")
    h1, l1 = ax.get_legend_handles_labels()
    h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, loc="best", fontsize=8)
    ax.set_title("crystallinity / k*L  (§8.3)")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("29 triad_R5_A2 — observáveis §8  (A.2 R5-FDT, N=%d)" % N)
    fig.tight_layout()
    fig.savefig(OUT / "05_observables.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(12.6, 8.4))
    gs = fig.add_gridspec(2, 3)
    order = [("ic", "IC t=0"), ("early", "early"), ("mid", "mid"), ("late", "late = universo")]
    positions = [(0, 0), (0, 1), (0, 2), (1, 0)]
    for (key, lab), (ri, ci) in zip(order, positions):
        ax = fig.add_subplot(gs[ri, ci], projection="3d")
        if key in volumes:
            rho = volumes[key]
            plot_isosurface(ax, rho, ISO_FRAC * float(rho.max()), dx, LBOX)
            ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}")
        else:
            setup_3d_box(ax, LBOX)
            ax.set_title(lab)
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(t_arr, series("peak"), label="peak")
    ax.plot(t_arr, series("R_rms"), label="R_rms")
    ax.legend(fontsize=8)
    ax.set_title("peak / R_rms")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(t_arr, series("PR"), label="PR")
    ax.plot(t_arr, series("crystallinity") * max(series("PR").max(), 1.0), label="C·PRmax")
    ax.legend(fontsize=8)
    ax.set_title("PR / C")
    ax.grid(True, alpha=0.3)
    fig.suptitle("29 triad_R5_A2 — A.2 R5-FDT full, 1 átomo §9.1, N=%d vs spec 128" % N)
    fig.tight_layout()
    fig.savefig(OUT / "00_montagem.png", dpi=150)
    plt.close(fig)

    write_csv(OUT / "summary.csv", [summary], list(summary.keys()))
    with (OUT / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print("wrote", OUT, flush=True)
    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(summary), flush=True)
    print("SUMMARY_JSON_END", flush=True)


if __name__ == "__main__":
    main()
