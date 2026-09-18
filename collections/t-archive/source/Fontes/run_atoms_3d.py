#!/usr/bin/env python3
"""Run 28 triad_atoms_3d — equação TRIAD completa, 12 átomos, saídas 3D.

1 gaussiana = 1 átomo. Sem init='chaos'. Sem ablação. Sem calibração.
NLS + memória + FDT juntos. kT=0.001 da spec §A.2 (banho R5-FDT), não fit.
A grade do 27 já era 3D; aqui o ponto são isosuperfície, centros e volume.
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
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
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
OUT = VAULT / "Artefatos" / "triad_atoms_3d"
RUN_ID = "28"
RUN_NAME = "triad_atoms_3d"

N_ATOMS = 12
ATOM_SIGMA = 1.2
MIN_SEP = 4.8
N = 40
L = 32.0
DT = 0.0025
T = 12.0
RECORD_EVERY = 40
SEED = 0
LAMBDA = -10.0
NU = (10.0, 0.5, 0.05)
LAM = (3.0, 1.0, 0.3)
GAMMA = 0.05
KT = 0.001
PEAK_FRAC = 0.20
ISO_FRAC = 0.30
MIN_DIST_ATOM = 2.0 * ATOM_SIGMA
ELEV = 22.0
AZIM = -60.0

try:
    from skimage.measure import marching_cubes

    HAS_MC = True
except Exception:
    HAS_MC = False


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


def coords_to_xyz(coords, dx, box):
    xyz = coords.astype(np.float64) * dx
    return xyz - box / 2.0


def nms_min_dist(coords, vals, dx, box, min_dist):
    if coords.shape[0] == 0 or min_dist <= 0:
        return coords, vals
    xyz = coords_to_xyz(coords, dx, box)
    keep = []
    for i in range(coords.shape[0]):
        ok = True
        for j in keep:
            if np.linalg.norm(min_image(xyz[i] - xyz[j], box)) < min_dist:
                ok = False
                break
        if ok:
            keep.append(i)
    keep = np.asarray(keep, dtype=int)
    return coords[keep], vals[keep]


def local_atom_peaks(rho, peak, frac, dx, box, min_dist):
    footprint = maximum_filter(rho, size=3, mode="wrap")
    is_max = (rho == footprint) & (rho >= frac * peak) & (peak > 0)
    coords = np.argwhere(is_max)
    vals = rho[is_max]
    n_raw = int(coords.shape[0])
    if coords.size == 0:
        return coords, vals, n_raw
    order = np.argsort(-vals)
    coords, vals = coords[order], vals[order]
    coords, vals = nms_min_dist(coords, vals, dx, box, min_dist)
    return coords, vals, n_raw


def nn_spacing(coords, box, dx):
    if coords.shape[0] < 2:
        return float("nan"), float("nan")
    xyz = coords_to_xyz(coords, dx, box)
    n = xyz.shape[0]
    nn = np.empty(n, dtype=np.float64)
    for i in range(n):
        d = min_image(xyz - xyz[i], box)
        dist = np.sqrt((d * d).sum(axis=1))
        dist[i] = np.inf
        nn[i] = dist.min()
    return float(nn.mean()), float(np.median(nn))


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
            [-h, -h, -h],
            [h, -h, -h],
            [h, h, -h],
            [-h, h, -h],
            [-h, -h, h],
            [h, -h, h],
            [h, h, h],
            [-h, h, h],
        ]
    )
    edges = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    for a, b in edges:
        p, q = corners[a], corners[b]
        ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color="0.35", lw=0.7, alpha=0.7)


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
    xyz = coords_to_xyz(ii, dx, box)
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=6, c=color, alpha=0.28, depthshade=False)
    setup_3d_box(ax, box)
    return used


def choose_backend():
    """Metal só se caps disser metal E um xp 3D de fato funcionar. Senão numpy."""
    caps = backend_capabilities()
    print("backend_caps", caps, flush=True)
    if not caps.get("metal"):
        xp = get_xp("numpy")
        name = getattr(xp, "__name__", type(xp).__name__)
        return xp, name, caps, "numpy (metal cap ausente)"
    t0 = time.perf_counter()
    try:
        import mlx.core as mx

        if not (hasattr(mx, "fft") and hasattr(mx.fft, "fftn")):
            raise RuntimeError("mlx sem fft.fftn 3D")
        a = mx.array(np.ones((8, 8, 8), dtype=np.complex64))
        _ = mx.fft.fftn(a)
        # memory_nls_strang_step_3d precisa de API numpy (random, meshgrid, complex128)
        # mlx não é drop-in; não forçar.
        raise RuntimeError("mlx não é drop-in para memory_nls_strang_step_3d")
    except Exception as exc:
        elapsed = time.perf_counter() - t0
        print("metal_probe_failed", exc, "elapsed_s", elapsed, flush=True)
        xp = get_xp("numpy")
        name = getattr(xp, "__name__", type(xp).__name__)
        return xp, name, caps, f"numpy (metal probe: {exc})"


def match_tracks(tracks, curr_xyz, box, max_dist, t):
    """Associa centros atuais a trilhas existentes (NN periódico guloso)."""
    if curr_xyz.shape[0] == 0:
        return tracks
    if not tracks:
        for p in curr_xyz:
            tracks.append({"xyz": [p.copy()], "t": [t]})
        return tracks
    last = np.asarray([tr["xyz"][-1] for tr in tracks], dtype=np.float64)
    pairs = []
    for i, p in enumerate(last):
        for j, q in enumerate(curr_xyz):
            d = float(np.linalg.norm(min_image(q - p, box)))
            pairs.append((d, i, j))
    pairs.sort()
    used_i, used_j = set(), set()
    for d, i, j in pairs:
        if d > max_dist:
            break
        if i in used_i or j in used_j:
            continue
        tracks[i]["xyz"].append(curr_xyz[j].copy())
        tracks[i]["t"].append(t)
        used_i.add(i)
        used_j.add(j)
    for j, q in enumerate(curr_xyz):
        if j not in used_j:
            tracks.append({"xyz": [q.copy()], "t": [t]})
    return tracks


def save_isosurface_fig(path, rho, peak, dx, box, title):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    level = ISO_FRAC * peak
    used = plot_isosurface(ax, rho, level, dx, box)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used, level


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
        backend="numpy",
        bc="periodic",
        fdt_couple=True,
        kT=KT,
        init="gaussian",
    )

    xp, backend_name, caps, backend_reason = choose_backend()
    print("backend_xp", backend_name, flush=True)
    print("backend_reason", backend_reason, flush=True)
    print("params", "N", p.N, "L", p.L, "dt", p.dt, "T", p.T, "V_ext", p.V_ext, flush=True)
    print("Lambda", p.Lambda, "nu", p.nu, "lam", p.lam, "Gamma", p.Gamma, flush=True)
    print("kT", KT, "fdt_couple", True, flush=True)
    print("atoms", N_ATOMS, "sigma", ATOM_SIGMA, "min_sep", MIN_SEP, flush=True)
    print("skimage_marching_cubes", HAS_MC, flush=True)

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
    psi = psi / xp.sqrt(asnumpy((xp.abs(psi) ** 2).sum() * dV))
    y = xp.zeros((len(p.nu), p.N, p.N, p.N), dtype=xp.float64)

    law = prepare_memory_nls_3d(p, xp)
    V_ext = xp.zeros((p.N, p.N, p.N), dtype=xp.float64)
    rng_step = xp.random.default_rng(p.seed)

    n_steps = int(round(p.T / p.dt))
    rec_every = max(1, p.record_every)
    snapshot_times = (0.0, T / 2.0, T)

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
    write_csv(OUT / "atoms_ic.csv", atom_rows, ["atom", "x", "y", "z", "phase", "sigma"])

    seps = []
    for i in range(N_ATOMS):
        for j in range(i + 1, N_ATOMS):
            seps.append(float(np.linalg.norm(min_image(positions[i] - positions[j], L))))
    seps = np.asarray(seps)

    print("n_steps", n_steps, "record_every", rec_every, "dx", dx, flush=True)
    print("f_FDT_e_noise_amp", law["noise_amplitude"], flush=True)
    print(
        "noise_amp_formula_sqrt_2Gamma_kT_dt",
        float(np.sqrt(2.0 * GAMMA * KT * DT)),
        flush=True,
    )
    print("ic_pair_sep_min", float(seps.min()), "mean", float(seps.mean()), flush=True)

    metrics = []
    volumes = {}
    centers_log = []
    tracks = []
    iso_method = None

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
            coords, pvals, n_raw = local_atom_peaks(
                rho, peak, PEAK_FRAC, dx, L, MIN_DIST_ATOM
            )
            n_det = int(coords.shape[0])
            nn_mean, nn_med = nn_spacing(coords, L, dx)
            xyz = coords_to_xyz(coords, dx, L) if n_det else np.zeros((0, 3))
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
                "n_raw_maxima": n_raw,
                "nn_mean": nn_mean,
                "nn_median": nn_med,
            }
            metrics.append(rec)
            for k, (xc, yc, zc) in enumerate(xyz):
                centers_log.append(
                    {
                        "t": t,
                        "idx": k,
                        "x": float(xc),
                        "y": float(yc),
                        "z": float(zc),
                        "rho": float(pvals[k]) if k < len(pvals) else 0.0,
                    }
                )
            tracks = match_tracks(tracks, xyz, L, max_dist=3.0 * ATOM_SIGMA, t=t)
            for st in snapshot_times:
                if abs(t - st) < 0.5 * p.dt * rec_every + 1e-12:
                    volumes[round(t, 6)] = rho.copy()
            print(
                f"t={t:.4f} norm={norm:.6f} peak={peak:.6e} Rrms={rrms:.4f} "
                f"n_at={n_det} n_raw={n_raw} PR={pr:.3f}",
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
    if centers_log:
        write_csv(
            OUT / "centers.csv",
            centers_log,
            ["t", "idx", "x", "y", "z", "rho"],
        )

    t_arr = np.array([m["t"] for m in metrics])
    late = t_arr >= (0.8 * T)
    early = t_arr <= (0.2 * T)
    mid_idx = int(np.argmin(np.abs(t_arr - 0.5 * T)))

    def series(key):
        return np.array([m[key] for m in metrics], dtype=np.float64)

    def stats(key, mask):
        v = series(key)[mask]
        return float(v.mean()), float(v.std())

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "backend_xp": backend_name,
        "backend_reason": backend_reason,
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
        "kT": KT,
        "fdt_couple": True,
        "V_ext": "None",
        "seed": SEED,
        "n_atoms": N_ATOMS,
        "atom_sigma": ATOM_SIGMA,
        "min_sep": MIN_SEP,
        "peak_frac_atom": PEAK_FRAC,
        "min_dist_atom": MIN_DIST_ATOM,
        "iso_frac": ISO_FRAC,
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
        "n_atoms_detected_mid": metrics[mid_idx]["n_atoms_detected"],
        "n_atoms_detected_final": metrics[-1]["n_atoms_detected"],
        "t_mid": float(t_arr[mid_idx]),
        "n_raw_maxima_initial": metrics[0]["n_raw_maxima"],
        "n_raw_maxima_mid": metrics[mid_idx]["n_raw_maxima"],
        "n_raw_maxima_final": metrics[-1]["n_raw_maxima"],
        "nn_mean_initial": metrics[0]["nn_mean"],
        "nn_mean_final": metrics[-1]["nn_mean"],
        "Vmem_peak_max": float(series("Vmem_peak").max()),
        "t_Vmem_peak": float(t_arr[int(series("Vmem_peak").argmax())]),
        "Vmem_peak_final": metrics[-1]["Vmem_peak"],
        "has_marching_cubes": HAS_MC,
    }
    for key in ("peak", "PR", "R_rms", "n_atoms_detected"):
        em, es = stats(key, early)
        lm, ls = stats(key, late)
        summary[f"{key}_early_mean"] = em
        summary[f"{key}_early_std"] = es
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls

    n0 = metrics[0]["n_atoms_detected"]
    nmid = metrics[mid_idx]["n_atoms_detected"]
    nf = metrics[-1]["n_atoms_detected"]
    atoms_remained = (n0 == 12) and (8 <= nmid <= 16) and (8 <= nf <= 16)
    bath_again = (nmid > 40) or (nf > 40) or (metrics[-1]["norm"] > 10.0)
    summary["atoms_remained_atoms"] = bool(atoms_remained)
    summary["bath_again"] = bool(bath_again)

    # --- figures ---
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=80,
        c="#c53030",
        depthshade=True,
        edgecolors="k",
        linewidths=0.4,
    )
    for i, (x0, y0, z0) in enumerate(positions):
        ax.text(x0, y0, z0, f" {i}", fontsize=8)
    setup_3d_box(ax, L)
    ax.set_title("28 IC — 12 centros gaussianos (t=0)")
    fig.tight_layout()
    fig.savefig(OUT / "01_atoms_3d_ic.png", dpi=150)
    plt.close(fig)

    vol_keys = sorted(volumes.keys())
    labels = ["early", "mid", "late"]
    iso_files = [
        "02_isosurface_early.png",
        "03_isosurface_mid.png",
        "04_isosurface_late.png",
    ]
    iso_used = []
    for key, lab, fname in zip(vol_keys[:3], labels, iso_files):
        rho = volumes[key]
        peak = float(rho.max())
        used, level = save_isosurface_fig(
            OUT / fname,
            rho,
            peak,
            dx,
            L,
            f"28 isosuperfície {lab}  t={key:.2f}  ρ={ISO_FRAC:.1f}·peak",
        )
        iso_used.append(used)
        print("iso", lab, "t", key, "method", used, "level", level, "peak", peak, flush=True)
    if iso_used:
        iso_method = iso_used[0]
    summary["iso_method"] = iso_method or "none"

    fig = plt.figure(figsize=(6.4, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    cmap = plt.get_cmap("viridis")
    if atoms_remained and tracks:
        for tr in tracks:
            xyz = np.asarray(tr["xyz"])
            if xyz.shape[0] < 2:
                ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=20, c="#2b6cb0")
                continue
            tt = np.asarray(tr["t"])
            segs = np.stack([xyz[:-1], xyz[1:]], axis=1)
            colors = cmap(0.15 + 0.8 * (tt[:-1] / max(T, 1e-12)))
            lc = Line3DCollection(segs, colors=colors, linewidths=1.4, alpha=0.85)
            ax.add_collection3d(lc)
            ax.scatter(
                xyz[0, 0], xyz[0, 1], xyz[0, 2], s=28, c="#c53030", edgecolors="k", linewidths=0.3
            )
            ax.scatter(
                xyz[-1, 0], xyz[-1, 1], xyz[-1, 2], s=28, c="#2f855a", edgecolors="k", linewidths=0.3
            )
    else:
        snap_xyz = []
        for key, color, m in zip(vol_keys[:3], ("#c53030", "#2b6cb0", "#2f855a"), ("o", "s", "^")):
            rho = volumes[key]
            peak = float(rho.max())
            coords, _, _ = local_atom_peaks(rho, peak, PEAK_FRAC, dx, L, MIN_DIST_ATOM)
            xyz = coords_to_xyz(coords, dx, L) if coords.shape[0] else np.zeros((0, 3))
            if xyz.shape[0]:
                ax.scatter(
                    xyz[:, 0],
                    xyz[:, 1],
                    xyz[:, 2],
                    s=36,
                    c=color,
                    marker=m,
                    label=f"t={key:.2f} n={xyz.shape[0]}",
                    depthshade=False,
                    edgecolors="k",
                    linewidths=0.25,
                )
                snap_xyz.append(xyz.shape[0])
        ax.legend(loc="upper left", fontsize=8)
    setup_3d_box(ax, L)
    ax.set_title("28 trajetórias / centros 3D (máximos locais)")
    fig.tight_layout()
    fig.savefig(OUT / "05_atoms_3d_traj.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.2))
    axes[0, 0].plot(t_arr, series("R_rms"), label="R_rms")
    axes[0, 0].plot(t_arr, series("r50"), label="r50")
    axes[0, 0].plot(t_arr, series("r80"), label="r80")
    axes[0, 0].plot(t_arr, series("r90"), label="r90")
    axes[0, 0].legend()
    axes[0, 0].set_title("raios")
    axes[0, 1].plot(t_arr, series("peak"), color="C3")
    axes[0, 1].set_title("peak ρ")
    axes[1, 0].plot(t_arr, series("n_atoms_detected"), label="n_det (NMS)")
    axes[1, 0].plot(t_arr, series("n_raw_maxima"), label="n_raw máx. local", alpha=0.7)
    axes[1, 0].axhline(N_ATOMS, color="C0", ls="--", alpha=0.5, label="IC=12")
    axes[1, 0].legend()
    axes[1, 0].set_title(f"átomos det. (ρ≥{PEAK_FRAC}·peak, min_dist={MIN_DIST_ATOM})")
    axes[1, 1].plot(t_arr, series("norm"), label="norm")
    axes[1, 1].plot(t_arr, series("PR") / max(series("PR").max(), 1e-12), label="PR/max")
    axes[1, 1].legend()
    axes[1, 1].set_title("norma e PR")
    for ax in axes.ravel():
        ax.set_xlabel("t")
        ax.grid(True, alpha=0.3)
    fig.suptitle("28 triad_atoms_3d — diagnósticos 2D (kT=0.001)")
    fig.tight_layout()
    fig.savefig(OUT / "06_radii_peak.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(12.4, 8.2))
    gs = fig.add_gridspec(2, 3)
    ax = fig.add_subplot(gs[0, 0], projection="3d")
    ax.scatter(
        positions[:, 0],
        positions[:, 1],
        positions[:, 2],
        s=50,
        c="#c53030",
        edgecolors="k",
        linewidths=0.3,
    )
    setup_3d_box(ax, L)
    ax.set_title("IC centros")
    if vol_keys:
        ax = fig.add_subplot(gs[0, 1], projection="3d")
        rho = volumes[vol_keys[min(1, len(vol_keys) - 1)]]
        plot_isosurface(ax, rho, ISO_FRAC * float(rho.max()), dx, L)
        ax.set_title(f"iso t={vol_keys[min(1, len(vol_keys)-1)]:.2f}")
        ax = fig.add_subplot(gs[0, 2], projection="3d")
        rho = volumes[vol_keys[-1]]
        plot_isosurface(ax, rho, ISO_FRAC * float(rho.max()), dx, L)
        ax.set_title(f"iso t={vol_keys[-1]:.2f}")
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(t_arr, series("R_rms"), label="R_rms")
    ax.plot(t_arr, series("r50"), label="r50")
    ax.plot(t_arr, series("r80"), label="r80")
    ax.legend(fontsize=8)
    ax.set_title("raios")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(t_arr, series("peak"), color="C3")
    ax.set_title("peak")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(t_arr, series("n_atoms_detected"))
    ax.axhline(12, ls="--", alpha=0.5)
    ax.set_title("n átomos det.")
    ax.grid(True, alpha=0.3)
    fig.suptitle("28 triad_atoms_3d — tríade completa, 12 átomos, volume 3D, kT=0.001")
    fig.tight_layout()
    fig.savefig(OUT / "00_montagem.png", dpi=150)
    plt.close(fig)

    gif_path = OUT / "07_centers_3d.gif"
    gif_ok = False
    try:
        from PIL import Image

        rec_t = [m["t"] for m in metrics]
        stride = max(1, len(rec_t) // 20)
        picks = list(range(0, len(rec_t), stride))
        if picks[-1] != len(rec_t) - 1:
            picks.append(len(rec_t) - 1)
        frames = []
        by_t = {}
        for row in centers_log:
            by_t.setdefault(row["t"], []).append((row["x"], row["y"], row["z"]))
        for i in picks:
            tt = rec_t[i]
            fig = plt.figure(figsize=(5.2, 4.8))
            ax = fig.add_subplot(111, projection="3d")
            pts = np.asarray(by_t.get(tt, []), dtype=np.float64)
            if pts.size:
                ax.scatter(pts[:, 0], pts[:, 1], pts[:, 2], s=40, c="#2b6cb0", edgecolors="k")
            setup_3d_box(ax, L)
            ax.set_title(f"centros t={tt:.2f}  n={0 if pts.size == 0 else pts.shape[0]}")
            fig.tight_layout()
            tmp = OUT / f"_gif_{i:03d}.png"
            fig.savefig(tmp, dpi=90)
            plt.close(fig)
            frames.append(Image.open(tmp).convert("P"))
        if frames:
            frames[0].save(
                gif_path,
                save_all=True,
                append_images=frames[1:],
                duration=180,
                loop=0,
            )
            gif_ok = True
        for tmp in OUT.glob("_gif_*.png"):
            tmp.unlink()
    except Exception as exc:
        print("gif_skipped", exc, flush=True)
        for tmp in OUT.glob("_gif_*.png"):
            tmp.unlink()
    summary["gif"] = bool(gif_ok)

    write_csv(OUT / "summary.csv", [summary], list(summary.keys()))
    with (OUT / "summary.json").open("w") as f:
        json.dump(summary, f, indent=2)

    print("wrote", OUT, flush=True)
    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(summary), flush=True)
    print("SUMMARY_JSON_END", flush=True)


if __name__ == "__main__":
    main()
