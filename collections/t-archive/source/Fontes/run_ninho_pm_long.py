#!/usr/bin/env python3
# Run 34 — ninho +/- LONG (I0 / environment). Mesma IC do run 33, T=60.
# Pergunta: depois que a caixa enche, acontece mais alguma coisa
# (estrutura, rebirth de par, queda de pico, bounce, cristalinidade)
# ou o cubo so senta como universo preenchido?
# Triade completa, Theta_core congelado (Q00). Standalone 3D Strang.
# Mesma IC: Psi = G_out(s=2.0, fase 0) - G_in(s=0.5, fase pi), origem, normalize.
# Volume preenchido = universo, nao ruido.
# NAO isola memoria/FDT. NAO muda Theta_core. NAO retoca kT.
# Nao e prova de nada.
from __future__ import annotations

import csv
import hashlib
import json
import time
import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

VAULT = Path("/Users/leo/Documents/Triad/T")
OUT_VAULT = VAULT / "Artefatos" / "triad_ninho_pm_long"
FALLBACK = Path("/tmp/triad_ninho_pm_long")
RUN_ID = "34"
RUN_NAME = "triad_ninho_pm_long"

# --- Theta_core (Q00 / TRIAD_QM_CANONICAL_V1) — IMUTAVEL ---
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

# --- N_num / caixa (I0, nao scan) ---
LBOX = 32.0
N = 64
DT = 0.0025
T_FINAL = 60.0
SEED = 0
S_IN = 0.5
S_OUT = 2.0
CENTER = (0.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 80
RECORD_EVERY_EARLY = 4
EARLY_T = 0.20
RECORD_EVERY_FILL = 40
FILL_T = 1.0
K_CUT_FACTOR = 1.0
BACKEND = "numpy"
DTYPE_PSI = np.complex128
DTYPE_R = np.float64
ISO_FRAC_IN = 0.35
ISO_FRAC_OUT = 0.08
RE_ISO_FRAC = 0.25
R_CORE = 0.75
R_MID_LO = 1.50
R_MID_HI = 3.00
R_FAR = 8.00
R_SHELL_LO = 0.80
R_SHELL_HI = 2.50
CONTRAST_IM_MIN = 3.0
CONTRAST_MF_MIN = 3.0
CONTRAST_HOLE_MIN = 3.0
SIGN_HOLE_FRAC = 0.40
RE_PLUS_MIN = 1e-8
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
    shell = (r >= R_SHELL_LO) & (r < R_SHELL_HI)
    origin = r <= (r.min() + 1e-15)
    rho_core = float(rho[core].mean()) if np.any(core) else 0.0
    rho_mid = float(rho[mid].mean()) if np.any(mid) else 0.0
    rho_far = float(rho[far].mean()) if np.any(far) else 0.0
    rho_shell = float(rho[shell].mean()) if np.any(shell) else 0.0
    rho_origin = float(rho[origin].mean()) if np.any(origin) else 0.0
    mass_core = float((rho[core] * dV).sum()) if np.any(core) else 0.0
    mass_mid = float((rho[mid] * dV).sum()) if np.any(mid) else 0.0
    mass_far = float((rho[far] * dV).sum()) if np.any(far) else 0.0
    tot = float((rho * dV).sum())
    contrast_im = rho_core / max(rho_mid, 1e-300)
    contrast_mf = rho_mid / max(rho_far, 1e-300)
    contrast_oi = rho_shell / max(rho_origin, 1e-300)
    contrast_sf = rho_shell / max(rho_far, 1e-300)
    two_scale_bright = bool(
        np.isfinite(contrast_im)
        and np.isfinite(contrast_mf)
        and (contrast_im > CONTRAST_IM_MIN)
        and (contrast_mf > CONTRAST_MF_MIN)
        and (rho_mid > 1e-12)
    )
    two_scale_hollow = bool(
        np.isfinite(contrast_oi)
        and np.isfinite(contrast_sf)
        and (contrast_oi > CONTRAST_HOLE_MIN)
        and (contrast_sf > CONTRAST_MF_MIN)
        and (rho_shell > 1e-12)
    )
    two_scale = bool(two_scale_bright or two_scale_hollow)
    return {
        "rho_core": rho_core,
        "rho_mid": rho_mid,
        "rho_far": rho_far,
        "rho_shell": rho_shell,
        "rho_origin": rho_origin,
        "mass_core": mass_core,
        "mass_mid": mass_mid,
        "mass_far": mass_far,
        "mass_core_frac": mass_core / max(tot, 1e-300),
        "mass_mid_frac": mass_mid / max(tot, 1e-300),
        "mass_far_frac": mass_far / max(tot, 1e-300),
        "contrast_im": contrast_im,
        "contrast_mf": contrast_mf,
        "contrast_oi": contrast_oi,
        "contrast_sf": contrast_sf,
        "two_scale_bright": two_scale_bright,
        "two_scale_hollow": two_scale_hollow,
        "two_scale": two_scale,
    }


def sign_nest_metrics(re, r):
    core = r < R_CORE
    mid = (r >= R_MID_LO) & (r < R_MID_HI)
    origin = r <= (r.min() + 1e-15)
    re_core_mean = float(re[core].mean()) if np.any(core) else 0.0
    re_core_min = float(re[core].min()) if np.any(core) else 0.0
    re_mid_mean = float(re[mid].mean()) if np.any(mid) else 0.0
    re_mid_max = float(re[mid].max()) if np.any(mid) else 0.0
    re_origin = float(re[origin].mean()) if np.any(origin) else 0.0
    re_max = float(re.max()) if re.size else 0.0
    re_min = float(re.min()) if re.size else 0.0
    plus_env = bool(re_mid_mean > max(0.05 * max(re_max, 0.0), RE_PLUS_MIN))
    minus_core = bool(re_core_min < 0.0 and re_core_mean < 0.0)
    hole_core = bool(re_origin <= SIGN_HOLE_FRAC * max(re_max, 1e-300) and re_max > RE_PLUS_MIN)
    sign_nest = bool(plus_env and (minus_core or hole_core) and np.isfinite(re_max))
    return {
        "re_core_mean": re_core_mean,
        "re_core_min": re_core_min,
        "re_mid_mean": re_mid_mean,
        "re_mid_max": re_mid_max,
        "re_origin": re_origin,
        "re_max": re_max,
        "re_min": re_min,
        "plus_env": plus_env,
        "minus_core": minus_core,
        "hole_core": hole_core,
        "sign_nest": sign_nest,
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


def add_isosurface(ax, vol, level, dx, box, color, alpha=0.32):
    used = "scatter"
    vmax = float(vol.max()) if vol.size else 0.0
    if HAS_MC and level > 0 and vmax > level:
        try:
            verts, faces, *_ = marching_cubes(vol, level=level, spacing=(dx, dx, dx))
            verts = verts - box / 2.0
            mesh = Poly3DCollection(verts[faces], alpha=alpha, linewidths=0.04)
            mesh.set_facecolor(color)
            mesh.set_edgecolor((0.15, 0.15, 0.2, 0.06))
            ax.add_collection3d(mesh)
            return "marching_cubes"
        except Exception as exc:
            print("marching_cubes_failed", exc, flush=True)
    mask = vol >= level
    ii = np.argwhere(mask)
    if ii.shape[0] == 0:
        return "empty"
    if ii.shape[0] > 8000:
        rng = np.random.default_rng(0)
        ii = ii[rng.choice(ii.shape[0], 8000, replace=False)]
    xyz = ii.astype(np.float64) * dx - box / 2.0
    ax.scatter(xyz[:, 0], xyz[:, 1], xyz[:, 2], s=6, c=color, alpha=0.28, depthshade=False)
    return used



def plot_rho_isosurface(ax, rho, peak, dx, box):
    used_out = "skip"
    used_in = "skip"
    if peak > 0:
        used_out = add_isosurface(ax, rho, ISO_FRAC_OUT * peak, dx, box, "#2b6cb0", alpha=0.18)
        used_in = add_isosurface(ax, rho, ISO_FRAC_IN * peak, dx, box, "#e53e3e", alpha=0.45)
    setup_3d_box(ax, box)
    return {"outer": used_out, "inner": used_in}


def plot_re_isosurface(ax, re, dx, box):
    re_max = float(re.max()) if re.size else 0.0
    re_min = float(re.min()) if re.size else 0.0
    used_p = "skip"
    used_n = "skip"
    if re_max > 0:
        used_p = add_isosurface(ax, re, RE_ISO_FRAC * re_max, dx, box, "#c53030", alpha=0.32)
    if re_min < 0:
        used_n = add_isosurface(ax, -re, RE_ISO_FRAC * (-re_min), dx, box, "#2b6cb0", alpha=0.45)
    setup_3d_box(ax, box)
    return {
        "plus": used_p,
        "minus": used_n,
        "re_max": re_max,
        "re_min": re_min,
        "level_plus": RE_ISO_FRAC * re_max if re_max > 0 else 0.0,
        "level_minus": RE_ISO_FRAC * re_min if re_min < 0 else 0.0,
    }


def save_rho_iso_fig(path, rho, peak, dx, box, title):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    used = plot_rho_isosurface(ax, rho, peak, dx, box)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used


def save_re_iso_fig(path, re, dx, box, title):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    used = plot_re_isosurface(ax, re, dx, box)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used


def save_midplane(path, sl, title, cmap="magma", vmin=None, vmax=None, cbar_label=None):
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    im = ax.imshow(
        sl.T,
        origin="lower",
        extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
        cmap=cmap,
        vmin=vmin,
        vmax=vmax,
    )
    cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if cbar_label:
        cb.set_label(cbar_label)
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
    # I0: ninho concentrico fases opostas. envelope +, inner -. amplitudes cruas iguais.
    g_in = np.exp(-r2 / (2.0 * S_IN * S_IN))
    g_out = np.exp(-r2 / (2.0 * S_OUT * S_OUT))
    psi = (g_out - g_in).astype(DTYPE_PSI)
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
    re = np.real(psi)
    finite = bool(np.isfinite(rho).all() and np.isfinite(y).all() and np.isfinite(re).all())
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
        "rho_shell": float("nan"),
        "rho_origin": float("nan"),
        "mass_core": float("nan"),
        "mass_mid": float("nan"),
        "mass_far": float("nan"),
        "mass_core_frac": float("nan"),
        "mass_mid_frac": float("nan"),
        "mass_far_frac": float("nan"),
        "contrast_im": float("nan"),
        "contrast_mf": float("nan"),
        "contrast_oi": float("nan"),
        "contrast_sf": float("nan"),
        "two_scale_bright": False,
        "two_scale_hollow": False,
        "two_scale": False,
        "r90_over_r50": float("nan"),
        "re_core_mean": float("nan"),
        "re_core_min": float("nan"),
        "re_mid_mean": float("nan"),
        "re_mid_max": float("nan"),
        "re_origin": float("nan"),
        "re_max": float("nan"),
        "re_min": float("nan"),
        "plus_env": False,
        "minus_core": False,
        "hole_core": False,
        "sign_nest": False,
    }
    if not finite:
        return rho, re, nan_rec
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
    sn = sign_nest_metrics(re, r)
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
        "r90_over_r50": (r90 / r50) if r50 > 1e-12 else float("nan"),
    }
    rec.update(struct)
    rec.update(ts)
    rec.update(sn)
    return rho, re, rec


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



def parse_args():
    ap = argparse.ArgumentParser(description="Run 34 ninho +/- long (same IC as 33)")
    ap.add_argument("--T", type=float, default=None, help="T_final override (default 60)")
    ap.add_argument("--out", type=str, default=None, help="output dir override")
    return ap.parse_args()


def main():
    global T_FINAL
    args = parse_args()
    if args.T is not None:
        T_FINAL = float(args.T)
    out = resolve_out()
    if args.out:
        out = Path(args.out)
        out.mkdir(parents=True, exist_ok=True)
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
    x1d = st["x"]
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    nu = np.asarray(NU, dtype=DTYPE_R)
    lam = np.asarray(LAM, dtype=DTYPE_R)
    rng = np.random.default_rng(SEED)

    n_steps = int(round(T_FINAL / DT))

    snap_targets = {
        "ic": 0.0,
        "t001": 0.01,
        "t002": 0.02,
        "t005": 0.05,
        "early": 0.10,
        "t1": 1.0,
        "t8": 8.0,
        "mid": 8.0,
        "t30": 30.0,
        "late": T_FINAL,
    }
    volumes_rho = {}
    volumes_re = {}
    snap_t = {}
    radial_snaps = {}
    linecuts = {}

    print("=== 34 ninho_pm_long I0 T=%.3f ===" % T_FINAL, flush=True)
    print("start", started, "out", out, flush=True)
    print("backend", BACKEND, "dtype", "complex128/float64", flush=True)
    print("L", LBOX, "N", N, "dx", dx, "dt", DT, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("Theta_core Lambda", LAMBDA, "alpha", ALPHA, "sigma", SIGMA_FRAC, flush=True)
    print("Gamma", GAMMA, "kT", KT, "nu", NU, "lam", LAM, flush=True)
    print("fdt_couple", FDT_COUPLE, "f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print("noise_amp_check", float(np.sqrt(2.0 * GAMMA * KT * DT / HBAR)), flush=True)
    print("max_nu_dt", float(max(NU) * DT), "memory_update", "euler", flush=True)
    print(
        "seed",
        SEED,
        "IC",
        "nested opposite-phase G_out(s=%s) - G_in(s=%s) origin" % (S_OUT, S_IN),
        flush=True,
    )
    print("center", CENTER, "skimage", HAS_MC, flush=True)
    print("phases", "outer=0 (+)", "inner=pi (-)", "Psi = G_out - G_in", flush=True)

    metrics = []
    blew = False
    blow_t = None
    t_two_lost = None
    t_sign_lost = None
    last_two_t = 0.0
    last_sign_t = 0.0

    for step in range(n_steps + 1):
        t = step * DT
        if t <= EARLY_T + 1e-12:
            rec_every = RECORD_EVERY_EARLY
        elif t <= FILL_T + 1e-12:
            rec_every = RECORD_EVERY_FILL
        else:
            rec_every = RECORD_EVERY
        do_rec = (step % rec_every == 0) or step == n_steps or t in (0.0, T_FINAL)
        for t_tgt in snap_targets.values():
            if abs(t - t_tgt) < 0.5 * DT + 1e-15:
                do_rec = True
        if do_rec:
            rho, re, rec = record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam)
            rec["N"] = N
            rec["dx"] = dx
            metrics.append(rec)
            if rec.get("two_scale"):
                last_two_t = t
            elif t_two_lost is None and t > 0:
                t_two_lost = t
            if rec.get("sign_nest"):
                last_sign_t = t
            elif t_sign_lost is None and t > 0:
                t_sign_lost = t
            for name, t_tgt in snap_targets.items():
                if abs(t - t_tgt) < 0.5 * DT * rec_every + 1e-12 or abs(t - t_tgt) < 0.6 * DT:
                    volumes_rho[name] = rho.copy()
                    volumes_re[name] = re.copy()
                    snap_t[name] = t
                    rc, rm, _ = radial_profile(rho, r)
                    radial_snaps[name] = (rc, rm, t)
                    linecuts[name] = (x1d.copy(), re[:, re.shape[1] // 2, re.shape[2] // 2].copy(), t)
            print(
                "t=%.4f norm=%.6e peak=%.6e PR=%.6e Rrms=%.6e r50=%.4f r90=%.4f "
                "cim=%.3e cmf=%.3e coi=%.3e re0=%.3e re+=%.3e re-=%.3e "
                "two=%s hollow=%s sign=%s finite=%s"
                % (
                    t,
                    rec["norm"],
                    rec["peak"],
                    rec["PR"],
                    rec["R_rms"],
                    rec["r50"],
                    rec["r90"],
                    rec["contrast_im"],
                    rec["contrast_mf"],
                    rec["contrast_oi"],
                    rec["re_origin"],
                    rec["re_max"],
                    rec["re_min"],
                    rec["two_scale"],
                    rec["two_scale_hollow"],
                    rec["sign_nest"],
                    rec["finite"],
                ),
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
    sign_s = np.array([bool(m["sign_nest"]) for m in metrics])
    n_two = int(two_s.sum())
    n_sign = int(sign_s.sum())
    if np.any(two_s):
        t_last_two = float(t_arr[two_s][-1])
    else:
        t_last_two = 0.0
    if t_two_lost is None and (not last["two_scale"]):
        lost = np.where(~two_s & (t_arr > 0))[0]
        t_two_lost = float(t_arr[lost[0]]) if lost.size else None
    if np.any(sign_s):
        t_last_sign = float(t_arr[sign_s][-1])
    else:
        t_last_sign = 0.0
    if t_sign_lost is None and (not last["sign_nest"]):
        lost = np.where(~sign_s & (t_arr > 0))[0]
        t_sign_lost = float(t_arr[lost[0]]) if lost.size else None

    filled_early = bool(
        (first["two_scale"] and t_last_two < 1.0)
        or (first["sign_nest"] and t_last_sign < 1.0)
        or (np.isfinite(last["R_rms"]) and last["R_rms"] > 2.0 * max(first["R_rms"], 1e-12))
        or (np.isfinite(last["PR"]) and last["PR"] > 10.0 * max(first["PR"], 1e-12))
    )
    two_scale_readable = bool(t_last_two >= 1.0 and n_two >= 8)
    sign_readable = bool(t_last_sign >= 1.0 and n_sign >= 8)
    peak_finite = bool(np.isfinite(peak_s).all() and (not blew) and float(np.nanmax(peak_s)) < 1.0e30)
    peak_max = float(np.nanmax(peak_s)) if peak_s.size else float("nan")
    t_peak = float(t_arr[int(np.nanargmax(peak_s))]) if peak_s.size and np.isfinite(peak_s).any() else None

    if n_two >= 2:
        peak_two = peak_s[two_s]
        rrms_two = series("R_rms")[two_s]
        dpeak_two = float(peak_two[-1] - peak_two[0])
        dR_two = float(rrms_two[-1] - rrms_two[0])
        collapse_while_nested = bool(dpeak_two > 0.0 and dR_two < 0.0)
    else:
        dpeak_two = float("nan")
        dR_two = float("nan")
        collapse_while_nested = False

    # --- long-run: late (t>=48) vs old-late mid (t=8-12); bounce / rebirth ---
    old_late_mask = (t_arr >= 8.0) & (t_arr <= 12.0)
    after_fill_mask = t_arr >= 1.0
    post1_t = t_arr[after_fill_mask]
    post1_peak = peak_s[after_fill_mask]
    post1_pr = series("PR")[after_fill_mask]
    post1_rrms = series("R_rms")[after_fill_mask]
    post1_norm = series("norm")[after_fill_mask]
    post1_k = series("k_star")[after_fill_mask]
    post1_vmem = series("Vmem_peak")[after_fill_mask]
    post1_cryst = series("crystallinity")[after_fill_mask]
    post1_sign = sign_s[after_fill_mask]
    post1_two = two_s[after_fill_mask]

    def local_extrema(y, t, kind="max", rel=0.08, min_sep=2.0):
        out = []
        if y.size < 3:
            return out
        for i in range(1, y.size - 1):
            if not (np.isfinite(y[i - 1]) and np.isfinite(y[i]) and np.isfinite(y[i + 1])):
                continue
            if kind == "max" and y[i] >= y[i - 1] and y[i] >= y[i + 1]:
                if out and (t[i] - out[-1][0]) < min_sep:
                    if y[i] > out[-1][1]:
                        out[-1] = (float(t[i]), float(y[i]))
                    continue
                out.append((float(t[i]), float(y[i])))
            if kind == "min" and y[i] <= y[i - 1] and y[i] <= y[i + 1]:
                if out and (t[i] - out[-1][0]) < min_sep:
                    if y[i] < out[-1][1]:
                        out[-1] = (float(t[i]), float(y[i]))
                    continue
                out.append((float(t[i]), float(y[i])))
        if rel > 0 and y.size:
            yref = float(np.nanmax(np.abs(y))) if kind == "max" else float(np.nanmax(y) - np.nanmin(y))
            yref = max(yref, 1e-30)
            if kind == "max":
                out = [(tt, vv) for tt, vv in out if vv >= rel * float(np.nanmax(y))]
            else:
                span = max(float(np.nanmax(y) - np.nanmin(y)), 1e-30)
                out = [(tt, vv) for tt, vv in out if (float(np.nanmax(y)) - vv) >= rel * span]
        return out

    peak_maxima = local_extrema(post1_peak, post1_t, kind="max", rel=0.05, min_sep=3.0)
    peak_minima = local_extrema(post1_peak, post1_t, kind="min", rel=0.05, min_sep=3.0)
    second_peak = bool(len(peak_maxima) >= 2)
    t_second_peak = peak_maxima[1][0] if second_peak else None
    val_second_peak = peak_maxima[1][1] if second_peak else None

    bounce = False
    t_bounce_min = None
    t_bounce_rise = None
    bounce_drop = float("nan")
    bounce_rise = float("nan")
    if post1_peak.size >= 4:
        pmax_i = int(np.nanargmax(post1_peak))
        if pmax_i + 2 < post1_peak.size:
            after = post1_peak[pmax_i:]
            after_t = post1_t[pmax_i:]
            imin = int(np.nanargmin(after))
            if imin + 2 < after.size:
                drop = float(after[0] - after[imin])
                rise = float(after[-1] - after[imin])
                span = max(float(np.nanmax(post1_peak) - np.nanmin(post1_peak)), 1e-30)
                if drop > 0.15 * span and rise > 0.10 * span and after_t[imin] > after_t[0] + 1.0:
                    bounce = True
                    t_bounce_min = float(after_t[imin])
                    t_bounce_rise = float(after_t[-1])
                    bounce_drop = drop
                    bounce_rise = rise
        # also: drop then rise anywhere after fill (not only after global max)
        if (not bounce) and peak_minima and peak_maxima:
            for tmin, vmin in peak_minima:
                later_max = [(tt, vv) for tt, vv in peak_maxima if tt > tmin + 1.0]
                earlier_max = [(tt, vv) for tt, vv in peak_maxima if tt < tmin - 1.0]
                if later_max and earlier_max:
                    drop = earlier_max[-1][1] - vmin
                    rise = later_max[0][1] - vmin
                    span = max(float(np.nanmax(post1_peak) - np.nanmin(post1_peak)), 1e-30)
                    if drop > 0.15 * span and rise > 0.10 * span:
                        bounce = True
                        t_bounce_min = tmin
                        t_bounce_rise = later_max[0][0]
                        bounce_drop = float(drop)
                        bounce_rise = float(rise)
                        break

    collapse_after_fill = False
    if post1_peak.size >= 4:
        dpeak_af = float(post1_peak[-1] - post1_peak[0])
        dR_af = float(post1_rrms[-1] - post1_rrms[0])
        collapse_after_fill = bool(dpeak_af > 0.0 and dR_af < 0.0 and abs(dR_af) > 0.05)

    # pair / nest rebirth after first loss
    sign_rebirth = False
    t_sign_rebirth = None
    n_sign_after_fill = int(post1_sign.sum()) if post1_sign.size else 0
    if t_sign_lost is not None:
        later_on = np.where(sign_s & (t_arr > float(t_sign_lost) + 1e-12))[0]
        if later_on.size:
            # only count as rebirth if it happens after the box is already filled
            t_reb = float(t_arr[later_on[0]])
            if t_reb >= 1.0:
                sign_rebirth = True
                t_sign_rebirth = t_reb
    two_rebirth = False
    t_two_rebirth = None
    n_two_after_fill = int(post1_two.sum()) if post1_two.size else 0
    if t_two_lost is not None:
        later_on = np.where(two_s & (t_arr > float(t_two_lost) + 1e-12))[0]
        if later_on.size:
            t_reb = float(t_arr[later_on[0]])
            if t_reb >= 1.0:
                two_rebirth = True
                t_two_rebirth = t_reb

    def rel_change(a, b):
        den = max(abs(a), 1e-30)
        return (b - a) / den

    peak_mid_m, peak_mid_s, peak_mid_n = stats("peak", old_late_mask)
    peak_late_m, peak_late_s, peak_late_n = stats("peak", late_mask)
    pr_mid_m, pr_mid_s, pr_mid_n = stats("PR", old_late_mask)
    pr_late_m, pr_late_s, pr_late_n = stats("PR", late_mask)
    rrms_mid_m, rrms_mid_s, rrms_mid_n = stats("R_rms", old_late_mask)
    rrms_late_m, rrms_late_s, rrms_late_n = stats("R_rms", late_mask)
    norm_mid_m, norm_mid_s, norm_mid_n = stats("norm", old_late_mask)
    norm_late_m, norm_late_s, norm_late_n = stats("norm", late_mask)
    k_mid_m, k_mid_s, k_mid_n = stats("k_star", old_late_mask)
    k_late_m, k_late_s, k_late_n = stats("k_star", late_mask)
    vmem_mid_m, vmem_mid_s, vmem_mid_n = stats("Vmem_peak", old_late_mask)
    vmem_late_m, vmem_late_s, vmem_late_n = stats("Vmem_peak", late_mask)
    cryst_mid_m, cryst_mid_s, cryst_mid_n = stats("crystallinity", old_late_mask)
    cryst_late_m, cryst_late_s, cryst_late_n = stats("crystallinity", late_mask)

    # "sits filled": after t=1, no nest/two rebirth, no bounce, no second peak,
    # and late vs mid (8-12) changes are small on structure observables
    sits_filled = bool(
        (not bounce)
        and (not second_peak)
        and (not sign_rebirth)
        and (not two_rebirth)
        and (not collapse_after_fill)
        and np.isfinite(peak_mid_m)
        and np.isfinite(peak_late_m)
        and abs(rel_change(peak_mid_m, peak_late_m)) < 0.50
        and abs(rel_change(rrms_mid_m, rrms_late_m)) < 0.10
    )
    note_long = (
        "Depois de t~1 a caixa ja e universo preenchido. "
        + (
            "Nao houve segundo pico, bounce, rebirth de ninho/sinal, nem colapso apos o preenchimento. "
            if sits_filled
            else "Houve alguma variacao apos o preenchimento (ver flags bounce/second_peak/rebirth). "
        )
        + "Nao e prova. Volume preenchido = universo, nao ruido."
    )
    print(
        "LONG after_t1 peak_maxima", peak_maxima,
        "second_peak", second_peak,
        "bounce", bounce,
        "sign_rebirth", sign_rebirth,
        "two_rebirth", two_rebirth,
        "collapse_after_fill", collapse_after_fill,
        "sits_filled", sits_filled,
        flush=True,
    )
    print(
        "LONG mid(8-12) peak=%.6f+/-%.6f PR=%.3f+/-%.3f Rrms=%.6f+/-%.6f "
        "norm=%.3f+/-%.3f k*=%.6f+/-%.6f Vmem=%.6f+/-%.6f cryst=%.6e+/-%.6e n=%d"
        % (
            peak_mid_m, peak_mid_s, pr_mid_m, pr_mid_s, rrms_mid_m, rrms_mid_s,
            norm_mid_m, norm_mid_s, k_mid_m, k_mid_s, vmem_mid_m, vmem_mid_s,
            cryst_mid_m, cryst_mid_s, peak_mid_n,
        ),
        flush=True,
    )
    print(
        "LONG late(t>=48) peak=%.6f+/-%.6f PR=%.3f+/-%.3f Rrms=%.6f+/-%.6f "
        "norm=%.3f+/-%.3f k*=%.6f+/-%.6f Vmem=%.6f+/-%.6f cryst=%.6e+/-%.6e n=%d"
        % (
            peak_late_m, peak_late_s, pr_late_m, pr_late_s, rrms_late_m, rrms_late_s,
            norm_late_m, norm_late_s, k_late_m, k_late_s, vmem_late_m, vmem_late_s,
            cryst_late_m, cryst_late_s, peak_late_n,
        ),
        flush=True,
    )

    if blew or not last.get("finite", False):
        verd_scale = "NUMERICAL_FAILURE"
        verd_sign = "NUMERICAL_FAILURE"
        verd_peak = "NUMERICAL_FAILURE"
        note_scale = "NaN/blowup — exclusao tecnica."
        note_sign = "NaN/blowup — exclusao tecnica."
        note_peak = "NaN/blowup — exclusao tecnica."
    else:
        if not first["two_scale"]:
            verd_scale = "INCONCLUSIVE"
            note_scale = (
                "A IC ja nao passou no criterio operacional de duas escalas "
                "(nucleo/ombro ou oco/casca)."
            )
        elif not two_scale_readable:
            verd_scale = "INCONCLUSIVE"
            note_scale = (
                "O perfil radial de duas escalas / oco nao durou tempo bastante. "
                "Com este banho (kT=1) as sementes viram universo. kT nao foi retocado."
            )
        elif collapse_while_nested:
            verd_scale = "PARTIAL"
            note_scale = (
                "Enquanto as duas escalas existiam, peak subiu e R_rms caiu "
                "(leitura possivel de contracao). Nao e lei 1/r2 nem prova."
            )
        else:
            verd_scale = "NOT_SUPPORTED"
            note_scale = (
                "Duas escalas visiveis por tempo, mas sem contracao conjunta "
                "(peak sobe e R_rms cai) enquanto o ninho existia."
            )
        if not first["sign_nest"]:
            verd_sign = "INCONCLUSIVE"
            note_sign = (
                "A IC ja nao passou no criterio operacional de ninho de sinal "
                "(buraco/nucleo - dentro de envelope +)."
            )
        elif not sign_readable:
            verd_sign = "INCONCLUSIVE"
            note_sign = (
                "O ninho de sinal (+ envelope / - ou buraco no nucleo) nao durou "
                "tempo bastante. Com kT=1 as sementes viram universo. kT nao foi retocado."
            )
        else:
            verd_sign = "PARTIAL"
            note_sign = "Ninho de sinal visivel por tempo; ver t_last_sign_nest."
        if peak_finite:
            verd_peak = "SUPPORTED"
            note_peak = (
                "peak rho permaneceu finito em todo o T (anti-colapso / singularidade "
                "nao foi a infinito neste run)."
            )
        else:
            verd_peak = "NOT_SUPPORTED"
            note_peak = "peak rho nao permaneceu finito."

    mid_m, _ = nearest_metric(metrics, 8.0)
    early_m, _ = nearest_metric(metrics, 0.10)
    t001_m, _ = nearest_metric(metrics, 0.01)
    t002_m, _ = nearest_metric(metrics, 0.02)

    rad_rows = []
    for name in ("ic", "t001", "t002", "t005", "early", "t1", "t8", "mid", "t30", "late"):
        if name not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[name]
        for ri, yi in zip(rc, rm):
            rad_rows.append({"snap": name, "t": tt, "r": float(ri), "rho_shell": float(yi)})
    if rad_rows:
        write_csv(out / "radial_profiles.csv", rad_rows, ["snap", "t", "r", "rho_shell"])

    lc_rows = []
    for name in ("ic", "t001", "t002", "t005", "early", "t1", "t8", "mid", "t30", "late"):
        if name not in linecuts:
            continue
        xx, yy, tt = linecuts[name]
        for xi, yi in zip(xx, yy):
            lc_rows.append({"snap": name, "t": tt, "x": float(xi), "Re_psi": float(yi)})
    if lc_rows:
        write_csv(out / "linecut_re.csv", lc_rows, ["snap", "t", "x", "Re_psi"])

    t_last_nest_visible = float(max(t_last_two, t_last_sign))

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "question": "depois que a caixa enche, acontece mais alguma coisa ate T=60 ou so senta como universo preenchido?",
        "leitura": "ima / anti-colapso (ninho de sinal, nao interferencia lado-a-lado, nao ninho mesmo-sinal)",
        "theta_core_unchanged": True,
        "terms_isolated": False,
        "kT_retuned": False,
        "solver": "standalone 3D Strang spec 3+5 (nao triad-lang)",
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
        "record_every_fill": RECORD_EVERY_FILL,
        "early_t": EARLY_T,
        "fill_t": FILL_T,
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
        "phases": [0.0, float(np.pi)],
        "phase_labels": ["envelope +", "inner -"],
        "raw_amplitudes_equal": True,
        "ic_formula": "Psi = G_out - G_in, then int |Psi|^2 dV = 1",
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
        "re_iso_frac": RE_ISO_FRAC,
        "r_core": R_CORE,
        "r_mid_lo": R_MID_LO,
        "r_mid_hi": R_MID_HI,
        "r_far": R_FAR,
        "r_shell_lo": R_SHELL_LO,
        "r_shell_hi": R_SHELL_HI,
        "contrast_im_min": CONTRAST_IM_MIN,
        "contrast_mf_min": CONTRAST_MF_MIN,
        "contrast_hole_min": CONTRAST_HOLE_MIN,
        "sign_hole_frac": SIGN_HOLE_FRAC,
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
        "contrast_im_t0.01": t001_m["contrast_im"],
        "contrast_im_t0.02": t002_m["contrast_im"],
        "contrast_im_t0.1": early_m["contrast_im"],
        "contrast_im_final": last["contrast_im"],
        "contrast_mf_initial": first["contrast_mf"],
        "contrast_mf_t0.01": t001_m["contrast_mf"],
        "contrast_mf_t0.02": t002_m["contrast_mf"],
        "contrast_mf_t0.1": early_m["contrast_mf"],
        "contrast_mf_final": last["contrast_mf"],
        "contrast_oi_initial": first["contrast_oi"],
        "contrast_oi_t0.01": t001_m["contrast_oi"],
        "contrast_oi_t0.02": t002_m["contrast_oi"],
        "contrast_oi_final": last["contrast_oi"],
        "two_scale_t0": bool(first["two_scale"]),
        "two_scale_t0.01": bool(t001_m["two_scale"]),
        "two_scale_t0.02": bool(t002_m["two_scale"]),
        "two_scale_t0.1": bool(early_m["two_scale"]),
        "two_scale_mid": bool(mid_m["two_scale"]),
        "two_scale_final": bool(last["two_scale"]),
        "two_scale_hollow_t0": bool(first["two_scale_hollow"]),
        "two_scale_hollow_t0.02": bool(t002_m["two_scale_hollow"]),
        "sign_nest_t0": bool(first["sign_nest"]),
        "sign_nest_t0.01": bool(t001_m["sign_nest"]),
        "sign_nest_t0.02": bool(t002_m["sign_nest"]),
        "sign_nest_t0.1": bool(early_m["sign_nest"]),
        "sign_nest_mid": bool(mid_m["sign_nest"]),
        "sign_nest_final": bool(last["sign_nest"]),
        "minus_core_t0": bool(first["minus_core"]),
        "hole_core_t0": bool(first["hole_core"]),
        "re_origin_t0": first["re_origin"],
        "re_max_t0": first["re_max"],
        "re_min_t0": first["re_min"],
        "re_origin_t0.02": t002_m["re_origin"],
        "re_max_t0.02": t002_m["re_max"],
        "re_min_t0.02": t002_m["re_min"],
        "t_last_two_scale": t_last_two,
        "t_two_scale_lost": t_two_lost,
        "t_last_sign_nest": t_last_sign,
        "t_sign_nest_lost": t_sign_lost,
        "t_last_nest_visible": t_last_nest_visible,
        "n_records_two_scale": n_two,
        "n_records_sign_nest": n_sign,
        "two_scale_readable": two_scale_readable,
        "sign_nest_readable": sign_readable,
        "filled_early": filled_early,
        "bath_ate_nest_before_read": bool(filled_early and not (two_scale_readable or sign_readable)),
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
        "verdict_sign_nest": verd_sign,
        "verdict_finite_peak": verd_peak,
        "note_scale": note_scale,
        "note_sign": note_sign,
        "note_peak": note_peak,
        "snap_t": {k: float(v) for k, v in snap_t.items()},
        "out": str(out),
        "second_peak": second_peak,
        "t_second_peak": t_second_peak,
        "val_second_peak": val_second_peak,
        "n_peak_maxima_after_t1": len(peak_maxima),
        "peak_maxima_after_t1": peak_maxima,
        "bounce": bounce,
        "t_bounce_min": t_bounce_min,
        "t_bounce_rise": t_bounce_rise,
        "bounce_drop": bounce_drop,
        "bounce_rise": bounce_rise,
        "collapse_after_fill": collapse_after_fill,
        "sign_rebirth": sign_rebirth,
        "t_sign_rebirth": t_sign_rebirth,
        "n_sign_after_fill": n_sign_after_fill,
        "two_rebirth": two_rebirth,
        "t_two_rebirth": t_two_rebirth,
        "n_two_after_fill": n_two_after_fill,
        "sits_filled": sits_filled,
        "note_long": note_long,
        "peak_oldlate_mean": peak_mid_m,
        "peak_oldlate_std": peak_mid_s,
        "peak_oldlate_n": peak_mid_n,
        "PR_oldlate_mean": pr_mid_m,
        "PR_oldlate_std": pr_mid_s,
        "R_rms_oldlate_mean": rrms_mid_m,
        "R_rms_oldlate_std": rrms_mid_s,
        "norm_oldlate_mean": norm_mid_m,
        "norm_oldlate_std": norm_mid_s,
        "k_star_oldlate_mean": k_mid_m,
        "k_star_oldlate_std": k_mid_s,
        "Vmem_peak_oldlate_mean": vmem_mid_m,
        "Vmem_peak_oldlate_std": vmem_mid_s,
        "crystallinity_oldlate_mean": cryst_mid_m,
        "crystallinity_oldlate_std": cryst_mid_s,
        "k_star_late_mean": k_late_m,
        "k_star_late_std": k_late_s,
        "Vmem_peak_late_mean": vmem_late_m,
        "Vmem_peak_late_std": vmem_late_s,
        "crystallinity_late_mean": cryst_late_m,
        "crystallinity_late_std": cryst_late_s,
        "peak_late_over_oldlate": (peak_late_m / peak_mid_m) if peak_mid_m else float("nan"),
        "PR_late_over_oldlate": (pr_late_m / pr_mid_m) if pr_mid_m else float("nan"),
        "norm_late_over_oldlate": (norm_late_m / norm_mid_m) if norm_mid_m else float("nan"),
        "cryst_late_minus_oldlate": (cryst_late_m - cryst_mid_m) if np.isfinite(cryst_late_m) else float("nan"),
    }
    for key in ("norm", "peak", "PR", "R_rms", "r50", "r90", "contrast_im", "contrast_mf", "k_star", "Vmem_peak", "crystallinity"):
        lm, ls, ln = stats(key, late_mask)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln
        om, os, on = stats(key, old_late_mask)
        summary[f"{key}_oldlate_mean"] = om
        summary[f"{key}_oldlate_std"] = os
        summary[f"{key}_oldlate_n"] = on

    iso_used = {}
    fig_specs = [
        ("ic", "01_ic_isosurface.png", "34 IC  rho  ninho +/-  s=0.5 subset s=2.0  t={t:.2f}"),
        ("early", "01b_isosurface_early.png", "34 isosuperficie rho early  t={t:.2f}  (banho kT=1)"),
        ("mid", "02_isosurface_mid.png", "34 isosuperficie rho mid  t={t:.2f}"),
        ("late", "03_isosurface_late.png", "34 isosuperficie rho late  t={t:.2f}  universo no cubo"),
    ]
    for key, fname, title_tmpl in fig_specs:
        if key not in volumes_rho:
            print("missing_volume", key, flush=True)
            continue
        rho = volumes_rho[key]
        peak = float(rho.max())
        tt = snap_t.get(key, -1.0)
        used = save_rho_iso_fig(out / fname, rho, peak, dx, LBOX, title_tmpl.format(t=tt))
        iso_used[key] = {"method": used, "peak": peak, "t": tt}
        print("iso_rho", key, "t", tt, "method", used, "peak", peak, flush=True)
    if "t002" in volumes_rho:
        rho = volumes_rho["t002"]
        peak = float(rho.max())
        tt = snap_t["t002"]
        used = save_rho_iso_fig(
            out / "01c_isosurface_t002.png",
            rho,
            peak,
            dx,
            LBOX,
            "34 isosuperficie rho t=%.3f  (se o ninho ja morreu, e isto)" % tt,
        )
        iso_used["t002"] = {"method": used, "peak": peak, "t": tt}
    if "t001" in volumes_rho:
        rho = volumes_rho["t001"]
        peak = float(rho.max())
        tt = snap_t["t001"]
        used = save_rho_iso_fig(
            out / "01d_isosurface_t001.png",
            rho,
            peak,
            dx,
            LBOX,
            "34 isosuperficie rho t=%.3f" % tt,
        )
        iso_used["t001"] = {"method": used, "peak": peak, "t": tt}

    if "ic" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01e_ic_re_isosurface.png",
            volumes_re["ic"],
            dx,
            LBOX,
            "34 IC  Re(Psi)  vermelho + / azul -  t=0",
        )
        iso_used["ic_re"] = used_re
        print("iso_re ic", used_re, flush=True)
    if "t002" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01f_t002_re_isosurface.png",
            volumes_re["t002"],
            dx,
            LBOX,
            "34 Re(Psi) t=%.3f  +/-" % snap_t["t002"],
        )
        iso_used["t002_re"] = used_re
    if "early" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01g_early_re_isosurface.png",
            volumes_re["early"],
            dx,
            LBOX,
            "34 Re(Psi) early t=%.2f  +/-" % snap_t["early"],
        )
        iso_used["early_re"] = used_re
    if "late" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01h_late_re_isosurface.png",
            volumes_re["late"],
            dx,
            LBOX,
            "34 Re(Psi) late t=%.2f  +/-" % snap_t["late"],
        )
        iso_used["late_re"] = used_re
    extra_rho_iso = (
        ("t005", "01i_isosurface_t005.png", "34 isosuperficie rho t=%.3f  (ninho morre?)"),
        ("t1", "01j_isosurface_t1.png", "34 isosuperficie rho t=%.2f  (caixa cheia)"),
        ("t8", "01k_isosurface_t8.png", "34 isosuperficie rho t=%.2f  (old late run 33)"),
        ("t30", "01l_isosurface_t30.png", "34 isosuperficie rho t=%.2f"),
    )
    for key, fname, tmpl in extra_rho_iso:
        if key not in volumes_rho:
            continue
        rho = volumes_rho[key]
        peak = float(rho.max())
        tt = snap_t[key]
        used = save_rho_iso_fig(out / fname, rho, peak, dx, LBOX, tmpl % tt)
        iso_used[key] = {"method": used, "peak": peak, "t": tt}
        print("iso_rho", key, "t", tt, "method", used, "peak", peak, flush=True)
    extra_re_iso = (
        ("t005", "01m_t005_re_isosurface.png"),
        ("t1", "01n_t1_re_isosurface.png"),
        ("t8", "01o_t8_re_isosurface.png"),
        ("t30", "01p_t30_re_isosurface.png"),
    )
    for key, fname in extra_re_iso:
        if key not in volumes_re:
            continue
        used_re = save_re_iso_fig(
            out / fname,
            volumes_re[key],
            dx,
            LBOX,
            "34 Re(Psi) t=%.3f  +/-" % snap_t[key],
        )
        iso_used[key + "_re"] = used_re


    fig, axes = plt.subplots(2, 2, figsize=(10.4, 9.4))
    order = [("ic", "t=0 IC"), ("early", "early"), ("mid", "mid"), ("late", "late")]
    for ax, (key, lab) in zip(axes.ravel(), order):
        if key not in volumes_rho:
            ax.set_title(lab + " ausente")
            continue
        sl = volumes_rho[key][:, :, volumes_rho[key].shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("%s  t=%.2f  |Psi|^2 z=0" % (lab, snap_t.get(key, 0)))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("34 — midplane xy  |Psi|^2  (ninho +/-, Theta_core, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "04_midplane_xy.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.4, 9.4))
    for ax, (key, lab) in zip(axes.ravel(), order):
        if key not in volumes_re:
            ax.set_title(lab + " ausente")
            continue
        sl = volumes_re[key][:, :, volumes_re[key].shape[2] // 2]
        vmax = float(np.nanmax(np.abs(sl))) if sl.size else 1.0
        vmax = vmax if vmax > 0 else 1.0
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("%s  t=%.2f  Re(Psi) z=0" % (lab, snap_t.get(key, 0)))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("34 — midplane xy  Re(Psi)  vermelho + / azul -  (halo +, buraco no centro)")
    fig.tight_layout()
    fig.savefig(out / "04r_midplane_re.png", dpi=150)
    plt.close(fig)

    watch_order = [
        ("ic", "t=0"),
        ("t005", "t=0.05"),
        ("t1", "t=1"),
        ("t8", "t=8"),
        ("t30", "t=30"),
        ("late", "t=60"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13.6, 8.6))
    for ax, (key, lab) in zip(axes.ravel(), watch_order):
        if key not in volumes_rho:
            ax.set_title(lab + " ausente")
            continue
        sl = volumes_rho[key][:, :, volumes_rho[key].shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("%s  t=%.2f  |Psi|^2 z=0" % (lab, snap_t.get(key, 0)))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("34 — midplane |Psi|^2  t=0, 0.05, 1, 8, 30, 60")
    fig.tight_layout()
    fig.savefig(out / "04x_midplane_watch.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(13.6, 8.6))
    for ax, (key, lab) in zip(axes.ravel(), watch_order):
        if key not in volumes_re:
            ax.set_title(lab + " ausente")
            continue
        sl = volumes_re[key][:, :, volumes_re[key].shape[2] // 2]
        vmax = float(np.nanmax(np.abs(sl))) if sl.size else 1.0
        vmax = vmax if vmax > 0 else 1.0
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title("%s  t=%.2f  Re(Psi) z=0" % (lab, snap_t.get(key, 0)))
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("34 — midplane Re(Psi)  t=0, 0.05, 1, 8, 30, 60")
    fig.tight_layout()
    fig.savefig(out / "04y_midplane_re_watch.png", dpi=150)
    plt.close(fig)

    for key, fname in (
        ("ic", "04a_midplane_t0.png"),
        ("t001", "04f_midplane_t001.png"),
        ("t002", "04e_midplane_t002.png"),
        ("t005", "04m_midplane_t005.png"),
        ("early", "04b_midplane_early.png"),
        ("t1", "04n_midplane_t1.png"),
        ("t8", "04o_midplane_t8.png"),
        ("mid", "04c_midplane_mid.png"),
        ("t30", "04p_midplane_t30.png"),
        ("late", "04d_midplane_late.png"),
    ):
        if key not in volumes_rho:
            continue
        sl = volumes_rho[key][:, :, volumes_rho[key].shape[2] // 2]
        save_midplane(
            out / fname,
            sl,
            "34 midplane xy  |Psi|^2  %s  t=%.3f" % (key, snap_t.get(key, 0)),
            cmap="magma",
            cbar_label="|Psi|^2",
        )

    for key, fname in (
        ("ic", "04g_midplane_re_t0.png"),
        ("t001", "04h_midplane_re_t001.png"),
        ("t002", "04i_midplane_re_t002.png"),
        ("t005", "04q_midplane_re_t005.png"),
        ("early", "04j_midplane_re_early.png"),
        ("t1", "04r_midplane_re_t1.png"),
        ("t8", "04s_midplane_re_t8.png"),
        ("mid", "04k_midplane_re_mid.png"),
        ("t30", "04t_midplane_re_t30.png"),
        ("late", "04l_midplane_re_late.png"),
    ):
        if key not in volumes_re:
            continue
        sl = volumes_re[key][:, :, volumes_re[key].shape[2] // 2]
        vmax = float(np.nanmax(np.abs(sl))) if sl.size else 1.0
        vmax = vmax if vmax > 0 else 1.0
        save_midplane(
            out / fname,
            sl,
            "34 midplane xy  Re(Psi)  %s  t=%.3f" % (key, snap_t.get(key, 0)),
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
            cbar_label="Re(Psi)",
        )

    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    colors = {"ic": "C0", "t001": "C1", "t002": "C3", "early": "0.4", "mid": "C2", "late": "0.2"}
    for key in ("ic", "t001", "t002", "early"):
        if key not in linecuts:
            continue
        xx, yy, tt = linecuts[key]
        ax.plot(xx, yy, color=colors.get(key, "k"), lw=1.5, label="%s t=%.3f" % (key, tt))
    ax.axhline(0.0, color="0.5", ls="--", lw=0.7)
    ax.set_xlabel("x")
    ax.set_ylabel("Re(Psi)(x,0,0)")
    ax.set_title("34 — corte Re(Psi) ao longo de x  (buraco/nucleo no origem, envelope +)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "09_linecut_re.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 4.4))
    if "ic" in linecuts:
        xx, yy, tt = linecuts["ic"]
        ax.plot(xx, yy, color="C0", lw=1.8, label="t=0")
    ax.axhline(0.0, color="0.5", ls="--", lw=0.7)
    ax.set_xlim(-8, 8)
    ax.set_xlabel("x")
    ax.set_ylabel("Re(Psi)")
    ax.set_title("34 — Re(Psi) t=0 zoom  (halo + / buraco no centro)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "09b_linecut_re_t0.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    colors_r = {
        "ic": "C0",
        "t001": "C1",
        "t002": "C3",
        "t005": "C5",
        "early": "C4",
        "t1": "C6",
        "t8": "C8",
        "mid": "C2",
        "t30": "C9",
        "late": "0.20",
    }
    labels_r = {
        "ic": "t=0 IC",
        "t001": "t=0.01",
        "t002": "t=0.02",
        "t005": "t=0.05",
        "early": "early t=0.10",
        "t1": "t=1",
        "t8": "t=8 (old late)",
        "mid": "t=8",
        "t30": "t=30",
        "late": "t=60",
    }
    for key in ("ic", "t001", "t002", "t005", "early", "t1", "t8", "t30", "late"):
        if key not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[key]
        ax.semilogy(rc, np.maximum(rm, 1e-20), color=colors_r[key], lw=1.6, label=labels_r[key])
    ax.axvline(S_IN, color="C0", ls=":", lw=0.9, alpha=0.7)
    ax.axvline(S_OUT, color="C0", ls="--", lw=0.9, alpha=0.7)
    ax.axvline(R_CORE, color="0.5", ls=":", lw=0.6)
    ax.axvline(R_MID_LO, color="0.5", ls=":", lw=0.6)
    ax.axvline(R_MID_HI, color="0.5", ls=":", lw=0.6)
    ax.set_xlabel("r")
    ax.set_ylabel("rho(r)  (media em casca)")
    ax.set_title("34 — perfil radial  |Psi|^2  (oco no origem, casca s~0.5-2)")
    ax.set_xlim(0, 16)
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06_radial_profiles.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.4, 4.4))
    if "ic" in radial_snaps:
        rc, rm, tt = radial_snaps["ic"]
        ax.plot(rc, rm, color="C0", lw=1.8, label="t=0")
    if "t002" in radial_snaps:
        rc, rm, tt = radial_snaps["t002"]
        ax.plot(rc, rm, color="C3", lw=1.3, label="t=%.3f" % tt)
    if "early" in radial_snaps:
        rc, rm, tt = radial_snaps["early"]
        ax.plot(rc, rm, color="C4", lw=1.1, label="t=%.2f" % tt)
    ax.axvline(S_IN, color="0.4", ls=":", lw=0.8, label="s_in=0.5")
    ax.axvline(S_OUT, color="0.4", ls="--", lw=0.8, label="s_out=2.0")
    ax.set_xlim(0, 8)
    ax.set_xlabel("r")
    ax.set_ylabel("rho(r)")
    ax.set_title("34 — perfil radial linear  (oco t=0, early, t=0.02)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06b_radial_linear.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(3, 2, figsize=(10.8, 10.4))
    axes[0, 0].plot(t_arr, peak_s, color="C3", lw=1.4)
    axes[0, 0].axvline(1.0, color="0.5", ls=":", lw=0.8)
    axes[0, 0].axvline(8.0, color="0.6", ls="--", lw=0.7)
    axes[0, 0].axvline(48.0, color="0.3", ls="--", lw=0.7)
    axes[0, 0].set_title("peak rho  (fica finito? segundo pico?)")
    axes[0, 1].plot(t_arr, series("PR"), color="C0", lw=1.4)
    axes[0, 1].set_title("PR")
    axes[1, 0].plot(t_arr, series("R_rms"), color="C2", lw=1.4)
    axes[1, 0].set_title("R_rms")
    axes[1, 1].plot(t_arr, series("norm"), color="C4", lw=1.4)
    axes[1, 1].set_title("norma")
    axes[2, 0].plot(t_arr, series("k_star"), color="C1", lw=1.4)
    axes[2, 0].set_title("k*")
    axes[2, 1].plot(t_arr, series("Vmem_peak"), color="C5", lw=1.4)
    axes[2, 1].set_title("Vmem_peak")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
        a.axvline(1.0, color="0.5", ls=":", lw=0.6)
    fig.suptitle("34 ninho +/- long — peak / PR / R_rms / norma / k* / Vmem  (T=60, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "05_observables.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, series("crystallinity"), color="C6", lw=1.4)
    axes[0, 0].axvline(1.0, color="0.5", ls=":", lw=0.8)
    axes[0, 0].axvline(8.0, color="0.6", ls="--", lw=0.7)
    axes[0, 0].axvline(48.0, color="0.3", ls="--", lw=0.7)
    axes[0, 0].set_title("crystallinity")
    axes[0, 1].plot(t_arr, series("k_star"), color="C1", lw=1.4, label="k*")
    axes[0, 1].plot(t_arr, series("k_star_L"), color="C8", lw=1.1, label="k* L")
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].set_title("k* / k*L")
    axes[1, 0].plot(t_arr, series("Vmem_peak"), color="C5", lw=1.4, label="Vmem_peak")
    axes[1, 0].plot(t_arr, series("Vmem_mean"), color="0.4", lw=1.1, label="Vmem_mean")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title("memoria")
    axes[1, 1].plot(t_arr[after_fill_mask], post1_peak, color="C3", lw=1.4)
    if bounce and t_bounce_min is not None:
        axes[1, 1].axvline(t_bounce_min, color="C0", ls="--", lw=0.9, label="bounce min")
    if second_peak and t_second_peak is not None:
        axes[1, 1].axvline(t_second_peak, color="C2", ls=":", lw=0.9, label="2o pico")
    axes[1, 1].set_title("peak t>=1  (senta ou bounce?)")
    axes[1, 1].legend(fontsize=7)
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("34 — cristalinidade / k* / Vmem / peak apos preenchimento")
    fig.tight_layout()
    fig.savefig(out / "05b_after_fill.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, series("contrast_im"), color="C0", lw=1.4, label="im nucleo/ombro")
    axes[0, 0].plot(t_arr, series("contrast_oi"), color="C2", lw=1.2, label="oi casca/origem")
    axes[0, 0].axhline(CONTRAST_IM_MIN, color="0.4", ls="--", lw=0.8)
    axes[0, 0].set_yscale("log")
    axes[0, 0].legend(fontsize=7)
    axes[0, 0].set_title("contrastes |Psi|^2")
    axes[0, 1].plot(t_arr, series("contrast_mf"), color="C1", lw=1.4)
    axes[0, 1].axhline(CONTRAST_MF_MIN, color="0.4", ls="--", lw=0.8)
    axes[0, 1].set_yscale("log")
    axes[0, 1].set_title("contrast ombro/longe  rho_mid/rho_far")
    axes[1, 0].plot(t_arr, series("r50"), label="r50")
    axes[1, 0].plot(t_arr, series("r80"), label="r80")
    axes[1, 0].plot(t_arr, series("r90"), label="r90")
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title("raios de massa")
    two_int = two_s.astype(float)
    sign_int = sign_s.astype(float)
    axes[1, 1].step(t_arr, two_int, where="post", color="C4", lw=1.4, label="two_scale")
    axes[1, 1].step(t_arr, sign_int, where="post", color="C3", lw=1.1, ls="--", label="sign_nest")
    if t_last_two > 0:
        axes[1, 1].axvline(t_last_two, color="C4", ls=":", lw=1.0)
    if t_last_sign > 0:
        axes[1, 1].axvline(t_last_sign, color="C3", ls=":", lw=1.0)
    axes[1, 1].legend(fontsize=7)
    axes[1, 1].set_ylim(-0.05, 1.15)
    axes[1, 1].set_title("two_scale / sign_nest")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("34 — duas escalas e ninho de sinal vs t")
    fig.tight_layout()
    fig.savefig(out / "08_two_scale.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    mask_e = t_arr <= max(EARLY_T, 0.5)
    axes[0].plot(t_arr[mask_e], peak_s[mask_e], "o-", color="C3", ms=3)
    axes[0].set_title("peak rho  (janela cedo)")
    axes[0].set_xlabel("t")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(t_arr[mask_e], series("re_origin")[mask_e], "o-", color="C0", ms=3, label="Re origem")
    axes[1].plot(t_arr[mask_e], series("re_max")[mask_e], "s-", color="#c53030", ms=3, label="Re max")
    axes[1].plot(t_arr[mask_e], series("re_min")[mask_e], "^-", color="#2b6cb0", ms=3, label="Re min")
    axes[1].axhline(0.0, color="0.5", ls="--", lw=0.6)
    axes[1].set_title("Re  (janela cedo)")
    axes[1].set_xlabel("t")
    axes[1].legend(fontsize=8)
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("34 — zoom t<=0.4  (o ninho +/- some aqui se kT=1 preencher)")
    fig.tight_layout()
    fig.savefig(out / "07_early_zoom.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(13.0, 8.8))
    gs = fig.add_gridspec(2, 3)
    order3 = [("ic", "IC t=0  ninho +/-"), ("early", "early"), ("late", "late = universo")]
    positions = [(0, 0), (0, 1), (0, 2)]
    for (key, lab), (ri, ci) in zip(order3, positions):
        ax = fig.add_subplot(gs[ri, ci], projection="3d")
        if key in volumes_rho:
            plot_rho_isosurface(ax, volumes_rho[key], float(volumes_rho[key].max()), dx, LBOX)
            ax.set_title("%s  t=%.2f" % (lab, snap_t.get(key, 0)))
        else:
            setup_3d_box(ax, LBOX)
            ax.set_title(lab)
    ax = fig.add_subplot(gs[1, 0])
    if "ic" in volumes_re:
        sl = volumes_re["ic"][:, :, volumes_re["ic"].shape[2] // 2]
        vmax = float(np.nanmax(np.abs(sl))) if sl.size else 1.0
        vmax = vmax if vmax > 0 else 1.0
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    ax.set_title("Re(Psi) t=0  halo + / buraco")
    ax = fig.add_subplot(gs[1, 1])
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
    ax.set_title("rho(r)  oco / duas escalas?")
    ax.grid(True, which="both", alpha=0.3)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(t_arr, peak_s, color="C3", label="peak")
    ax.plot(t_arr, series("R_rms"), color="C2", label="R_rms")
    ax.legend(fontsize=8)
    ax.set_title("peak / R_rms  (pico finito?)")
    ax.grid(True, alpha=0.3)
    fig.suptitle("34 ninho +/- long — I0, Theta_core, kT=1, N=64  (sinal / duas escalas / pico finito)")
    fig.tight_layout()
    fig.savefig(out / "00_montagem.png", dpi=150)
    plt.close(fig)

    summary["iso_used"] = iso_used

    for key in ("ic", "t001", "t002", "t005", "early", "t1", "t8", "mid", "t30", "late"):
        if key in volumes_rho:
            np.save(out / ("rho_%s.npy" % key), volumes_rho[key])
        if key in volumes_re:
            np.save(out / ("re_%s.npy" % key), volumes_re[key])

    write_csv(out / "summary.csv", [summary], list(summary.keys()))
    js = jsonable(summary)
    with (out / "summary.json").open("w") as f:
        json.dump(js, f, indent=2, default=str)

    paths = [p for p in sorted(out.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.txt"]
    lines = ["%s  %s" % (sha256_file(p), p.relative_to(out).as_posix()) for p in paths]
    (out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(js, default=str), flush=True)
    print("SUMMARY_JSON_END", flush=True)
    print("wrote", out, flush=True)
    print("VERDICT_SCALE", verd_scale, flush=True)
    print("VERDICT_SIGN", verd_sign, flush=True)
    print("VERDICT_PEAK", verd_peak, flush=True)
    print(
        "t_last_two_scale",
        t_last_two,
        "t_last_sign_nest",
        t_last_sign,
        "t_last_nest_visible",
        t_last_nest_visible,
        "t_lost_two",
        t_two_lost,
        "t_lost_sign",
        t_sign_lost,
        "peak_max",
        peak_max,
        "t_peak",
        t_peak,
        "bounce",
        bounce,
        "second_peak",
        second_peak,
        "sign_rebirth",
        sign_rebirth,
        "sits_filled",
        sits_filled,
        "wall",
        wall,
        flush=True,
    )


if __name__ == "__main__":
    main()
