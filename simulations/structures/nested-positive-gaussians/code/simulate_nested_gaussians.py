#!/usr/bin/env python3
"""Run 31 — gaussianas aninhadas (I0 / environment). Gravidade / singularidade finita.

Tríade completa, Theta_core congelado (Q00). Standalone 3D Strang.
1 gaussiana = 1 átomo. Aninhadas = dois átomos, um dentro do outro.
Volume preenchido = universo, não ruído.
NÃO isola memória/FDT. NÃO muda Theta_core. NÃO retoca kT.
"""
from __future__ import annotations

import csv
import hashlib
import json
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

VAULT = Path("/Users/leo/Documents/Triad/T")
OUT_VAULT = VAULT / "Artefatos" / "triad_nested"
FALLBACK = Path("/tmp/triad_nested")
RUN_ID = "31"
RUN_NAME = "triad_nested_gaussians"

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

# --- N_num / caixa (I0, não scan) ---
LBOX = 32.0
N = 64
DT = 0.0025
T_FINAL = 8.0
SEED = 0
S_IN = 0.5
S_OUT = 2.0
CENTER = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 40
RECORD_EVERY_EARLY = 4
EARLY_T = 0.40
K_CUT_FACTOR = 1.0
BACKEND = "numpy"
DTYPE_PSI = np.complex128
DTYPE_R = np.float64
ISO_FRAC_IN = 0.35
ISO_FRAC_OUT = 0.08
# duas escalas: núcleo r<R_CORE vs ombro R_MID_LO<r<R_MID_HI vs longe r>R_FAR
R_CORE = 0.75
R_MID_LO = 1.50
R_MID_HI = 3.00
R_FAR = 8.00
CONTRAST_IM_MIN = 3.0
CONTRAST_MF_MIN = 3.0
N_RADIAL_BINS = 48
ELEV = 22.0
AZIM = -60.0

try:
    from skimage.measure import marching_cubes

    HAS_MC = True
except Exception:
    HAS_MC = False


def resolve_out() -> Path:
    try:
        OUT_VAULT.mkdir(parents=True, exist_ok=True)
        test = OUT_VAULT / ".write_test"
        test.write_text("ok", encoding="utf-8")
        test.unlink()
        return OUT_VAULT
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


def radial_profile(rho, r, n_bins=N_RADIAL_BINS, r_max=None):
    r_max = float(r_max if r_max is not None else (LBOX * np.sqrt(3.0) / 2.0))
    bins = np.linspace(0.0, r_max, n_bins + 1)
    idx = np.digitize(r.ravel(), bins) - 1
    idx = np.clip(idx, 0, n_bins - 1)
    sums = np.bincount(idx, weights=rho.ravel().astype(np.float64), minlength=n_bins)
    counts = np.bincount(idx, minlength=n_bins)
    mean = np.divide(sums, counts, out=np.zeros(n_bins), where=counts > 0)
    r_cent = 0.5 * (bins[:-1] + bins[1:])
    return r_cent, mean, counts.astype(np.float64)


def two_scale_metrics(rho, r, dV):
    core = r < R_CORE
    mid = (r >= R_MID_LO) & (r < R_MID_HI)
    far = r > R_FAR
    rho_core = float(rho[core].mean()) if np.any(core) else 0.0
    rho_mid = float(rho[mid].mean()) if np.any(mid) else 0.0
    rho_far = float(rho[far].mean()) if np.any(far) else 0.0
    mass_core = float((rho[core] * dV).sum()) if np.any(core) else 0.0
    mass_mid = float((rho[mid] * dV).sum()) if np.any(mid) else 0.0
    mass_far = float((rho[far] * dV).sum()) if np.any(far) else 0.0
    tot = float((rho * dV).sum())
    contrast_im = rho_core / max(rho_mid, 1e-300)
    contrast_mf = rho_mid / max(rho_far, 1e-300)
    two_scale = bool(
        np.isfinite(contrast_im)
        and np.isfinite(contrast_mf)
        and (contrast_im > CONTRAST_IM_MIN)
        and (contrast_mf > CONTRAST_MF_MIN)
        and (rho_mid > 1e-12)
    )
    return {
        "rho_core": rho_core,
        "rho_mid": rho_mid,
        "rho_far": rho_far,
        "mass_core": mass_core,
        "mass_mid": mass_mid,
        "mass_far": mass_far,
        "mass_core_frac": mass_core / max(tot, 1e-300),
        "mass_mid_frac": mass_mid / max(tot, 1e-300),
        "mass_far_frac": mass_far / max(tot, 1e-300),
        "contrast_im": contrast_im,
        "contrast_mf": contrast_mf,
        "two_scale": two_scale,
    }


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
        p0, q0 = corners[a], corners[b]
        ax.plot(
            [p0[0], q0[0]],
            [p0[1], q0[1]],
            [p0[2], q0[2]],
            color="0.35",
            lw=0.7,
            alpha=0.7,
        )


def add_isosurface(ax, rho, level, dx, box, color, alpha=0.32):
    used = "scatter"
    if HAS_MC and level > 0 and float(rho.max()) > level:
        try:
            verts, faces, *_ = marching_cubes(rho, level=level, spacing=(dx, dx, dx))
            verts = verts - box / 2.0
            mesh = Poly3DCollection(verts[faces], alpha=alpha, linewidths=0.04)
            mesh.set_facecolor(color)
            mesh.set_edgecolor((0.15, 0.15, 0.2, 0.06))
            ax.add_collection3d(mesh)
            return "marching_cubes"
        except Exception as exc:
            print("marching_cubes_failed", exc, flush=True)
    mask = rho >= level
    ii = np.argwhere(mask)
    if ii.shape[0] == 0:
        return "empty"
    if ii.shape[0] > 8000:
        rng = np.random.default_rng(0)
        ii = ii[rng.choice(ii.shape[0], 8000, replace=False)]
    xyz = ii.astype(np.float64) * dx - box / 2.0
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=6, c=color, alpha=0.28, depthshade=False)
    return used


def plot_nested_isosurface(ax, rho, peak, dx, box):
    used_out = "skip"
    used_in = "skip"
    if peak > 0:
        used_out = add_isosurface(ax, rho, ISO_FRAC_OUT * peak, dx, box, "#2b6cb0", alpha=0.18)
        used_in = add_isosurface(ax, rho, ISO_FRAC_IN * peak, dx, box, "#e53e3e", alpha=0.45)
    setup_3d_box(ax, box)
    return {"outer": used_out, "inner": used_in}


def save_isosurface_fig(path, rho, peak, dx, box, title):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    used = plot_nested_isosurface(ax, rho, peak, dx, box)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used, ISO_FRAC_IN * peak if peak > 0 else 0.0, ISO_FRAC_OUT * peak if peak > 0 else 0.0


def save_midplane(path, sl, title):
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    im = ax.imshow(
        sl.T,
        origin="lower",
        extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
        cmap="magma",
    )
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


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
    # I0: duas gaussianas concêntricas, mesma fase 0, amplitude crua igual, depois normaliza
    g_in = np.exp(-r2 / (2.0 * S_IN * S_IN))
    g_out = np.exp(-r2 / (2.0 * S_OUT * S_OUT))
    psi = (g_in + g_out).astype(DTYPE_PSI)
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    return {
        "x": x,
        "X": X,
        "Y": Y,
        "Z": Z,
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
    V_tot = LAMBDA * rho + V_mem
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
    nan_rec = {
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
        "rho_core": float("nan"),
        "rho_mid": float("nan"),
        "rho_far": float("nan"),
        "mass_core": float("nan"),
        "mass_mid": float("nan"),
        "mass_far": float("nan"),
        "mass_core_frac": float("nan"),
        "mass_mid_frac": float("nan"),
        "mass_far_frac": float("nan"),
        "contrast_im": float("nan"),
        "contrast_mf": float("nan"),
        "two_scale": False,
        "r90_over_r50": float("nan"),
    }
    if not finite:
        return rho, nan_rec
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
    ts = two_scale_metrics(rho, r, dV)
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
        "M2": mem_pers[1] if len(mem_pers) else 0.0,
        "M3": mem_pers[2] if len(mem_pers) > 2 else 0.0,
        "finite": True,
        "r90_over_r50": (r90 / r50) if r50 > 1e-12 else float("nan"),
    }
    rec.update(struct)
    rec.update(ts)
    return rho, rec


def now_sp():
    try:
        from zoneinfo import ZoneInfo
        import datetime

        return datetime.datetime.now(ZoneInfo("America/Sao_Paulo")).strftime(
            "%Y-%m-%d %H:%M:%S BRT"
        )
    except Exception:
        return time.strftime("%Y-%m-%d %H:%M:%S UTC")


def nearest_metric(metrics, t_tgt):
    t = np.array([m["t"] for m in metrics], dtype=np.float64)
    i = int(np.argmin(np.abs(t - t_tgt)))
    return metrics[i], i


def jsonable(obj):
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, np.integer):
        return int(obj)
    if isinstance(obj, np.floating):
        return float(obj)
    return obj


def main():
    out = resolve_out()
    out.mkdir(parents=True, exist_ok=True)
    t_wall0 = time.perf_counter()
    started = now_sp()

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

    snap_targets = {
        "ic": 0.0,
        "t002": 0.02,
        "early": 0.10,
        "mid": 0.5 * T_FINAL,
        "late": T_FINAL,
    }
    volumes = {}
    snap_t = {}
    radial_snaps = {}

    print("=== 31 nested_gaussians I0 ===", flush=True)
    print("start", started, "out", out, flush=True)
    print("backend", BACKEND, "dtype", "complex128/float64", flush=True)
    print("L", LBOX, "N", N, "dx", dx, "dt", DT, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("Theta_core Lambda", LAMBDA, "alpha", ALPHA, "sigma", SIGMA_FRAC, flush=True)
    print("Gamma", GAMMA, "kT", KT, "nu", NU, "lam", LAM, flush=True)
    print("fdt_couple", FDT_COUPLE, "f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print("noise_amp_check", float(np.sqrt(2.0 * GAMMA * KT * DT / HBAR)), flush=True)
    print("max_nu_dt", float(max(NU) * DT), "memory_update", "euler", flush=True)
    print("seed", SEED, "IC", f"nested G(s_in={S_IN})+G(s_out={S_OUT}) origin phase=0", flush=True)
    print("center", CENTER, "skimage", HAS_MC, flush=True)

    metrics = []
    blew = False
    blow_t = None
    t_two_lost = None
    last_two_t = 0.0

    for step in range(n_steps + 1):
        t = step * DT
        rec_every = RECORD_EVERY_EARLY if t <= EARLY_T + 1e-12 else RECORD_EVERY
        do_rec = (step % rec_every == 0) or step == n_steps or t in (0.0, T_FINAL)
        for t_tgt in snap_targets.values():
            if abs(t - t_tgt) < 0.5 * DT + 1e-15:
                do_rec = True
        if do_rec:
            rho, rec = record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam)
            rec["N"] = N
            rec["dx"] = dx
            metrics.append(rec)
            if rec.get("two_scale"):
                last_two_t = t
            elif t_two_lost is None and t > 0:
                t_two_lost = t
            for name, t_tgt in snap_targets.items():
                if abs(t - t_tgt) < 0.5 * DT * rec_every + 1e-12 or abs(t - t_tgt) < 0.6 * DT:
                    volumes[name] = rho.copy()
                    snap_t[name] = t
                    rc, rm, _ = radial_profile(rho, r)
                    radial_snaps[name] = (rc, rm, t)
            print(
                f"t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
                f"PR={rec['PR']:.6e} Rrms={rec['R_rms']:.6e} "
                f"r50={rec['r50']:.4f} r90={rec['r90']:.4f} "
                f"cim={rec['contrast_im']:.3e} cmf={rec['contrast_mf']:.3e} "
                f"two={rec['two_scale']} finite={rec['finite']}",
                flush=True,
            )
            if (not rec["finite"]) or (
                np.isfinite(rec["peak"]) and abs(rec["peak"]) > 1.0e30
            ):
                blew = True
                blow_t = t
                print("BLOWUP_OR_NAN", "t", t, flush=True)
                break
        if step == n_steps or blew:
            break
        psi, y = strang_step(psi, y, half_lin, noise_amp, rng, nu, lam)

    wall = time.perf_counter() - t_wall0
    finished = now_sp()
    print("wall_s", wall, "finished", finished, flush=True)

    write_csv(out / "metrics.csv", metrics, list(metrics[0].keys()))

    t_arr = np.array([m["t"] for m in metrics], dtype=np.float64)

    def series(key):
        return np.array([m[key] for m in metrics], dtype=np.float64)

    def stats(key, mask):
        v = series(key)[mask]
        v = v[np.isfinite(v)]
        if v.size == 0:
            return float("nan"), float("nan"), 0
        return float(v.mean()), float(v.std(ddof=0)), int(v.size)

    late_mask = t_arr >= (0.8 * T_FINAL)
    last = metrics[-1]
    first = metrics[0]
    peak_s = series("peak")
    two_s = np.array([bool(m["two_scale"]) for m in metrics])
    n_two = int(two_s.sum())
    if np.any(two_s):
        t_last_two = float(t_arr[two_s][-1])
    else:
        t_last_two = 0.0
    if t_two_lost is None and (not last["two_scale"]):
        lost = np.where(~two_s & (t_arr > 0))[0]
        t_two_lost = float(t_arr[lost[0]]) if lost.size else None

    filled_early = bool(
        (first["two_scale"] and t_last_two < 1.0)
        or (np.isfinite(last["R_rms"]) and last["R_rms"] > 2.0 * max(first["R_rms"], 1e-12))
        or (np.isfinite(last["PR"]) and last["PR"] > 10.0 * max(first["PR"], 1e-12))
    )
    two_scale_readable = bool(t_last_two >= 1.0 and n_two >= 8)
    peak_finite = bool(np.isfinite(peak_s).all() and (not blew) and float(np.nanmax(peak_s)) < 1.0e30)
    peak_max = float(np.nanmax(peak_s)) if peak_s.size else float("nan")
    t_peak = float(t_arr[int(np.nanargmax(peak_s))]) if peak_s.size and np.isfinite(peak_s).any() else None

    # colapso operacional: peak sobe E R_rms cai enquanto ainda há duas escalas
    if n_two >= 2:
        t_two = t_arr[two_s]
        peak_two = peak_s[two_s]
        rrms_two = series("R_rms")[two_s]
        dpeak_two = float(peak_two[-1] - peak_two[0])
        dR_two = float(rrms_two[-1] - rrms_two[0])
        collapse_while_nested = bool(dpeak_two > 0.0 and dR_two < 0.0)
    else:
        dpeak_two = float("nan")
        dR_two = float("nan")
        collapse_while_nested = False

    if blew or not last.get("finite", False):
        verd_scale = "NUMERICAL_FAILURE"
        verd_peak = "NUMERICAL_FAILURE"
        note_scale = "NaN/blowup — exclusão técnica."
        note_peak = "NaN/blowup — exclusão técnica."
    else:
        if not first["two_scale"]:
            verd_scale = "INCONCLUSIVE"
            note_scale = (
                "A IC já não passou no critério operacional de duas escalas "
                f"(contrast_im>{CONTRAST_IM_MIN} e contrast_mf>{CONTRAST_MF_MIN})."
            )
        elif not two_scale_readable:
            verd_scale = "INCONCLUSIVE"
            note_scale = (
                "O perfil radial de duas escalas não durou tempo bastante para ler "
                "colapso/sobreposição como gravidade. Com este banho (kT=1) as "
                "sementes viram universo. kT não foi retocado."
            )
        elif collapse_while_nested:
            verd_scale = "PARTIAL"
            note_scale = (
                "Enquanto as duas escalas existiam, peak subiu e R_rms caiu "
                "(leitura possível de contração). Não é lei 1/r² nem prova."
            )
        else:
            verd_scale = "NOT_SUPPORTED"
            note_scale = (
                "Duas escalas visíveis por tempo, mas sem contração conjunta "
                "(peak↑ e R_rms↓) enquanto o ninho existia."
            )
        if peak_finite:
            verd_peak = "SUPPORTED"
            note_peak = (
                "peak ρ permaneceu finito em todo o T (anti-colapso / singularidade "
                "não foi a infinito neste run)."
            )
        else:
            verd_peak = "NOT_SUPPORTED"
            note_peak = "peak ρ não permaneceu finito."

    mid_m, _ = nearest_metric(metrics, 0.5 * T_FINAL)
    early_m, _ = nearest_metric(metrics, 0.10)
    t002_m, _ = nearest_metric(metrics, 0.02)

    # radial CSV
    rad_rows = []
    for name in ("ic", "t002", "early", "mid", "late"):
        if name not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[name]
        for ri, yi in zip(rc, rm):
            rad_rows.append({"snap": name, "t": tt, "r": float(ri), "rho_shell": float(yi)})
    if rad_rows:
        write_csv(out / "radial_profiles.csv", rad_rows, ["snap", "t", "r", "rho_shell"])

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "question": "I0 gaussianas aninhadas — duas escalas / pico finito (environment, não scan)",
        "leitura": "gravidade emergente / singularidade finita (ninho, não interferência)",
        "theta_core_unchanged": True,
        "terms_isolated": False,
        "kT_retuned": False,
        "solver": "standalone 3D Strang spec §3+§5 (não triad-lang)",
        "backend": BACKEND,
        "fp": "fp64",
        "N": N,
        "L": LBOX,
        "dx": dx,
        "dt": DT,
        "T": T_FINAL,
        "n_steps": n_steps,
        "n_records": len(metrics),
        "record_every": RECORD_EVERY,
        "record_every_early": RECORD_EVERY_EARLY,
        "early_t": EARLY_T,
        "seed": SEED,
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
        "s_in": S_IN,
        "s_out": S_OUT,
        "center": list(CENTER),
        "phases": [0.0, 0.0],
        "raw_amplitudes_equal": True,
        "normalize": "int |Psi|^2 dV = 1",
        "y0": Y0,
        "f_FDT": f_FDT,
        "f_FDT_formula": "2*Gamma*(dx**3)*kT/hbar",
        "noise_amp": noise_amp,
        "noise_amp_formula": "sqrt(f_FDT*dt/dx**3)=sqrt(2*Gamma*kT*dt/hbar)",
        "memory_update": "euler",
        "max_nu_dt": float(max(NU) * DT),
        "iso_frac_in": ISO_FRAC_IN,
        "iso_frac_out": ISO_FRAC_OUT,
        "r_core": R_CORE,
        "r_mid_lo": R_MID_LO,
        "r_mid_hi": R_MID_HI,
        "r_far": R_FAR,
        "contrast_im_min": CONTRAST_IM_MIN,
        "contrast_mf_min": CONTRAST_MF_MIN,
        "has_marching_cubes": HAS_MC,
        "wall_s": wall,
        "started_america_sao_paulo": started,
        "finished_america_sao_paulo": finished,
        "blew_up": blew,
        "blow_t": blow_t,
        "finite_final": bool(last.get("finite", False)),
        "peak_finite_all_t": peak_finite,
        "peak_initial": first["peak"],
        "peak_final": last["peak"],
        "peak_max": peak_max,
        "t_peak": t_peak,
        "norm_initial": first["norm"],
        "norm_final": last["norm"],
        "PR_initial": first["PR"],
        "PR_final": last["PR"],
        "R_rms_initial": first["R_rms"],
        "R_rms_final": last["R_rms"],
        "r50_initial": first["r50"],
        "r50_final": last["r50"],
        "r90_initial": first["r90"],
        "r90_final": last["r90"],
        "r90_over_r50_initial": first["r90_over_r50"],
        "r90_over_r50_final": last["r90_over_r50"],
        "contrast_im_initial": first["contrast_im"],
        "contrast_im_t0.02": t002_m["contrast_im"],
        "contrast_im_t0.1": early_m["contrast_im"],
        "contrast_im_final": last["contrast_im"],
        "contrast_mf_initial": first["contrast_mf"],
        "contrast_mf_t0.02": t002_m["contrast_mf"],
        "contrast_mf_t0.1": early_m["contrast_mf"],
        "contrast_mf_final": last["contrast_mf"],
        "two_scale_t0": bool(first["two_scale"]),
        "two_scale_t0.02": bool(t002_m["two_scale"]),
        "two_scale_t0.1": bool(early_m["two_scale"]),
        "two_scale_mid": bool(mid_m["two_scale"]),
        "two_scale_final": bool(last["two_scale"]),
        "t_last_two_scale": t_last_two,
        "t_two_scale_lost": t_two_lost,
        "n_records_two_scale": n_two,
        "two_scale_readable": two_scale_readable,
        "filled_early": filled_early,
        "bath_ate_nest_before_collapse_read": bool(filled_early and not two_scale_readable),
        "dpeak_while_two_scale": dpeak_two,
        "dR_rms_while_two_scale": dR_two,
        "collapse_while_nested": collapse_while_nested,
        "mass_core_frac_initial": first["mass_core_frac"],
        "mass_core_frac_final": last["mass_core_frac"],
        "Vmem_peak_max": float(np.nanmax(series("Vmem_peak"))),
        "t_Vmem_peak": float(t_arr[int(np.nanargmax(series("Vmem_peak")))]),
        "Vmem_peak_final": last["Vmem_peak"],
        "k_star_final": last["k_star"],
        "k_star_L_final": last["k_star_L"],
        "peak_n_cells_half_final": last["peak_n_cells_half"],
        "peak_width_phys_final": last["peak_width_phys"],
        "verdict_two_scale": verd_scale,
        "verdict_finite_peak": verd_peak,
        "note_scale": note_scale,
        "note_peak": note_peak,
        "snap_t": {k: float(v) for k, v in snap_t.items()},
        "out": str(out),
    }
    for key in ("norm", "peak", "PR", "R_rms", "r50", "r90", "contrast_im", "contrast_mf"):
        lm, ls, ln = stats(key, late_mask)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln

    # --- figures ---
    iso_used = {}
    fig_specs = [
        ("ic", "01_ic_isosurface.png", "31 IC  ninho s=0.5 ⊂ s=2.0  t={t:.2f}"),
        ("early", "01b_isosurface_early.png", "31 isosuperfície early  t={t:.2f}  (banho kT=1)"),
        ("mid", "02_isosurface_mid.png", "31 isosuperfície mid  t={t:.2f}"),
        ("late", "03_isosurface_late.png", "31 isosuperfície late  t={t:.2f}  universo no cubo"),
    ]
    for key, fname, title_tmpl in fig_specs:
        if key not in volumes:
            print("missing_volume", key, flush=True)
            continue
        rho = volumes[key]
        peak = float(rho.max())
        tt = snap_t.get(key, -1.0)
        used, lev_in, lev_out = save_isosurface_fig(
            out / fname,
            rho,
            peak,
            dx,
            LBOX,
            title_tmpl.format(t=tt),
        )
        iso_used[key] = {
            "method": used,
            "level_in": lev_in,
            "level_out": lev_out,
            "peak": peak,
            "t": tt,
        }
        print("iso", key, "t", tt, "method", used, "peak", peak, flush=True)
    if "t002" in volumes:
        rho = volumes["t002"]
        peak = float(rho.max())
        tt = snap_t["t002"]
        used, lev_in, lev_out = save_isosurface_fig(
            out / "01c_isosurface_t002.png",
            rho,
            peak,
            dx,
            LBOX,
            f"31 isosuperfície t={tt:.3f}  (se o ninho já morreu, é isto)",
        )
        iso_used["t002"] = {
            "method": used,
            "level_in": lev_in,
            "level_out": lev_out,
            "peak": peak,
            "t": tt,
        }

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 9.4))
    order = [("ic", "t=0 IC"), ("early", "early"), ("mid", "mid"), ("late", "late")]
    for ax, (key, lab) in zip(axes.ravel(), order):
        if key not in volumes:
            ax.set_title(f"{lab} ausente")
            continue
        rho = volumes[key]
        sl = rho[:, :, rho.shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}  corte z=0")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("31 — midplane xy  (ninho s=0.5⊂s=2, Theta_core, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "04_midplane_xy.png", dpi=150)
    plt.close(fig)

    for key, fname in (
        ("ic", "04a_midplane_t0.png"),
        ("t002", "04e_midplane_t002.png"),
        ("early", "04b_midplane_early.png"),
        ("mid", "04c_midplane_mid.png"),
        ("late", "04d_midplane_late.png"),
    ):
        if key not in volumes:
            continue
        sl = volumes[key][:, :, volumes[key].shape[2] // 2]
        save_midplane(
            out / fname,
            sl,
            f"31 midplane xy  {key}  t={snap_t.get(key, 0):.3f}",
        )

    # MONEY PLOT — perfil radial
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    colors = {
        "ic": "C0",
        "t002": "C1",
        "early": "C3",
        "mid": "C2",
        "late": "0.35",
    }
    labels = {
        "ic": "t=0 IC (duas escalas)",
        "t002": "t=0.02",
        "early": "early t=0.10",
        "mid": "mid t=4",
        "late": "late t=8",
    }
    for key in ("ic", "t002", "early", "mid", "late"):
        if key not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[key]
        ax.semilogy(rc, np.maximum(rm, 1e-20), color=colors[key], lw=1.6, label=labels[key])
    ax.axvline(S_IN, color="C0", ls=":", lw=0.9, alpha=0.7)
    ax.axvline(S_OUT, color="C0", ls="--", lw=0.9, alpha=0.7)
    ax.axvline(R_CORE, color="0.5", ls=":", lw=0.6)
    ax.axvline(R_MID_LO, color="0.5", ls=":", lw=0.6)
    ax.axvline(R_MID_HI, color="0.5", ls=":", lw=0.6)
    ax.set_xlabel("r")
    ax.set_ylabel("ρ(r)  (média em casca)")
    ax.set_title("31 — perfil radial  (duas cascas/larguras em t=0?)")
    ax.set_xlim(0, 16)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06_radial_profiles.png", dpi=150)
    plt.close(fig)

    # radial linear zoom t=0 (ombro visível)
    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    if "ic" in radial_snaps:
        rc, rm, tt = radial_snaps["ic"]
        ax.plot(rc, rm, color="C0", lw=1.8, label="t=0")
    if "t002" in radial_snaps:
        rc, rm, tt = radial_snaps["t002"]
        ax.plot(rc, rm, color="C1", lw=1.3, label=f"t={tt:.3f}")
    if "early" in radial_snaps:
        rc, rm, tt = radial_snaps["early"]
        ax.plot(rc, rm, color="C3", lw=1.1, label=f"t={tt:.2f}")
    ax.axvline(S_IN, color="0.4", ls=":", lw=0.8, label="s_in=0.5")
    ax.axvline(S_OUT, color="0.4", ls="--", lw=0.8, label="s_out=2.0")
    ax.set_xlim(0, 8)
    ax.set_xlabel("r")
    ax.set_ylabel("ρ(r)")
    ax.set_title("31 — perfil radial linear  (ombro externo em t=0)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06b_radial_linear.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, peak_s, color="C3", lw=1.4)
    axes[0, 0].set_title("peak ρ  (fica finito?)")
    axes[0, 1].plot(t_arr, series("PR"), color="C0", lw=1.4)
    axes[0, 1].set_title("PR")
    axes[1, 0].plot(t_arr, series("R_rms"), color="C2", lw=1.4)
    axes[1, 0].set_title("R_rms")
    axes[1, 1].plot(t_arr, series("norm"), color="C4", lw=1.4)
    axes[1, 1].set_title("norma")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("31 ninho — peak / PR / R_rms / norma  (Theta_core, kT=1, sem retune)")
    fig.tight_layout()
    fig.savefig(out / "05_observables.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, series("contrast_im"), color="C0", lw=1.4)
    axes[0, 0].axhline(CONTRAST_IM_MIN, color="0.4", ls="--", lw=0.8)
    axes[0, 0].set_yscale("log")
    axes[0, 0].set_title("contrast núcleo/ombro  ρ_core/ρ_mid")
    axes[0, 1].plot(t_arr, series("contrast_mf"), color="C1", lw=1.4)
    axes[0, 1].axhline(CONTRAST_MF_MIN, color="0.4", ls="--", lw=0.8)
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_title("contrast ombro/longe  ρ_mid/ρ_far")
    axes[1, 0].plot(t_arr, series("r50"), label="r50")
    axes[1, 0].plot(t_arr, series("r80"), label="r80")
    axes[1, 0].plot(t_arr, series("r90"), label="r90")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title("raios de massa")
    two_int = two_s.astype(float)
    axes[1, 1].step(t_arr, two_int, where="post", color="C4", lw=1.4)
    if t_last_two > 0:
        axes[1, 1].axvline(t_last_two, color="C3", ls=":", lw=1.0, label=f"último two-scale t={t_last_two:.3f}")
        axes[1, 1].legend(fontsize=7)
    axes[1, 1].set_ylim(-0.05, 1.15)
    axes[1, 1].set_title("two_scale (critério operacional)")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("31 — duas escalas vs t")
    fig.tight_layout()
    fig.savefig(out / "08_two_scale.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    mask_e = t_arr <= max(EARLY_T, 0.5)
    axes[0].plot(t_arr[mask_e], peak_s[mask_e], "o-", color="C3", ms=3)
    axes[0].set_title("peak ρ  (janela cedo)")
    axes[0].set_xlabel("t")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(t_arr[mask_e], series("contrast_im")[mask_e], "o-", color="C0", ms=3, label="im")
    axes[1].plot(t_arr[mask_e], series("contrast_mf")[mask_e], "s-", color="C1", ms=3, label="mf")
    axes[1].axhline(CONTRAST_IM_MIN, color="0.4", ls="--", lw=0.7)
    axes[1].set_yscale("log")
    axes[1].set_title("contrastes  (janela cedo)")
    axes[1].set_xlabel("t")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("31 — zoom t≤0.4  (o ninho some aqui se kT=1 preencher)")
    fig.tight_layout()
    fig.savefig(out / "07_early_zoom.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(13.0, 8.8))
    gs = fig.add_gridspec(2, 3)
    order = [("ic", "IC t=0  ninho"), ("early", "early"), ("late", "late = universo")]
    positions = [(0, 0), (0, 1), (0, 2)]
    for (key, lab), (ri, ci) in zip(order, positions):
        ax = fig.add_subplot(gs[ri, ci], projection="3d")
        if key in volumes:
            rho = volumes[key]
            plot_nested_isosurface(ax, rho, float(rho.max()), dx, LBOX)
            ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}")
        else:
            setup_3d_box(ax, LBOX)
            ax.set_title(lab)
    ax = fig.add_subplot(gs[1, 0])
    if "ic" in radial_snaps:
        rc, rm, tt = radial_snaps["ic"]
        ax.semilogy(rc, np.maximum(rm, 1e-20), label="t=0")
    if "early" in radial_snaps:
        rc, rm, tt = radial_snaps["early"]
        ax.semilogy(rc, np.maximum(rm, 1e-20), label="early")
    if "late" in radial_snaps:
        rc, rm, tt = radial_snaps["late"]
        ax.semilogy(rc, np.maximum(rm, 1e-20), label="late")
    ax.set_xlim(0, 16)
    ax.legend(fontsize=8)
    ax.set_title("ρ(r)  duas escalas?")
    ax.grid(True, which="both", alpha=0.3)
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(t_arr, peak_s, color="C3", label="peak")
    ax.plot(t_arr, series("R_rms"), color="C2", label="R_rms")
    ax.legend(fontsize=8)
    ax.set_title("peak / R_rms  (pico finito?)")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(t_arr, series("PR"), label="PR")
    ax.plot(t_arr, series("norm"), label="norm")
    ax.legend(fontsize=8)
    ax.set_title("PR / norma")
    ax.grid(True, alpha=0.3)
    fig.suptitle(
        "31 ninho — I0, Theta_core, kT=1, N=64  (duas escalas / singularidade finita)"
    )
    fig.tight_layout()
    fig.savefig(out / "00_montagem.png", dpi=150)
    plt.close(fig)

    summary["iso_used"] = iso_used

    for key in ("ic", "t002", "early", "mid", "late"):
        if key in volumes:
            np.save(out / f"rho_{key}.npy", volumes[key])

    write_csv(out / "summary.csv", [summary], list(summary.keys()))
    js = jsonable(summary)
    with (out / "summary.json").open("w") as f:
        json.dump(js, f, indent=2, default=str)

    paths = [p for p in sorted(out.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.txt"]
    lines = [f"{sha256_file(p)}  {p.relative_to(out).as_posix()}" for p in paths]
    (out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(js, default=str), flush=True)
    print("SUMMARY_JSON_END", flush=True)
    print("wrote", out, flush=True)
    print("VERDICT_SCALE", verd_scale, flush=True)
    print("VERDICT_PEAK", verd_peak, flush=True)
    print("t_last_two_scale", t_last_two, "t_lost", t_two_lost, "peak_max", peak_max, "wall", wall, flush=True)


if __name__ == "__main__":
    main()
