#!/usr/bin/env python3
"""Run 32 — universo-átomo (I0 / environment). Anti-colapso / ímã-repele.

Tríade completa, Theta_core congelado (Q00). Standalone 3D Strang.
1 gaussiana = 1 átomo.
OUTER larga = universo (um átomo gigante).
DENTRO: 2 átomos, observador e observado, fases 0 e π (+ e −).
Força interessante = anti-colapso: memória repulsiva, ímãs mesmo-polo,
impedindo singularidade infinita.
NÃO é MQ. NÃO é colapso-como-gravidade-caindo.
NÃO isola memória/FDT. NÃO muda Theta_core. NÃO retoca kT.
Volume preenchido = universo, não ruído.
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
from scipy.ndimage import maximum_filter

VAULT = Path("/Users/leo/Documents/Triad/T")
OUT_VAULT = VAULT / "Artefatos" / "triad_universo_atomo"
FALLBACK = Path("/tmp/triad_universo_atomo")
RUN_ID = "32"
RUN_NAME = "triad_universo_atomo"

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
S_ENV = 8.0
S_IN = 1.0
C_ENV = (0.0, 0.0, 0.0)
C_OBS = (-2.5, 0.0, 0.0)  # observador, fase 0 (+)
C_OBD = (2.5, 0.0, 0.0)  # observado, fase π (−)
SEP_IC = 5.0
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
RE_ISO_FRAC = 0.25
PEAK_FRAC = 0.20
MIN_DIST_ATOM = 2.0 * S_IN
TRACK_RADIUS = 2.5 * S_IN
INNER_ASSIGN_MAX = 4.0
NMS_CAP = 48
N_RADIAL_BINS = 48
R_CORE = 1.50
R_MID_LO = 4.00
R_MID_HI = 10.00
R_FAR = 14.00
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


def min_image(delta, box):
    return delta - box * np.round(delta / box)


def min_image_dist(a, b, box):
    d = min_image(np.asarray(a, dtype=np.float64) - np.asarray(b, dtype=np.float64), box)
    return float(np.sqrt(np.dot(d, d)))


def wrap_point(p, box):
    h = box / 2.0
    return tuple(float(((x + h) % box) - h) for x in p)


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


def local_extrema(field, frac, dx, box, min_dist, sign=+1, nms_cap=NMS_CAP):
    """Máximos locais de ±field. sign=+1 → max; sign=-1 → min de field (max de -field)."""
    work = field if sign > 0 else -field
    peak = float(work.max())
    footprint = maximum_filter(work, size=3, mode="wrap")
    is_ext = (work == footprint) & (work >= frac * peak) & (peak > 0)
    coords = np.argwhere(is_ext)
    vals = field[is_ext]
    n_raw = int(coords.shape[0])
    if coords.size == 0:
        return coords, vals, n_raw
    if n_raw > nms_cap:
        empty = coords[:0]
        return empty, vals[:0], n_raw
    order = np.argsort(-work[is_ext])
    coords, vals = coords[order], vals[order]
    coords, vals = nms_min_dist(coords, vals, dx, box, min_dist)
    return coords, vals, n_raw


def nearest_xyz(coords, target, dx, box):
    if coords.shape[0] == 0:
        return None, float("nan")
    xyz = coords_to_xyz(coords, dx, box)
    d = np.array([min_image_dist(p, target, box) for p in xyz])
    i = int(np.argmin(d))
    return tuple(float(v) for v in xyz[i]), float(d[i])


def signed_com(field, center, X, Y, Z, dV, box, radius, sign=+1):
    """COM de field_clipped (Re+ ou |Re−|) num raio em torno do centro."""
    dx = min_image(X - center[0], box)
    dy = min_image(Y - center[1], box)
    dz = min_image(Z - center[2], box)
    r2 = dx * dx + dy * dy + dz * dz
    w = r2 <= (radius * radius)
    if sign > 0:
        wgt = np.where(w, np.maximum(field, 0.0), 0.0)
    else:
        wgt = np.where(w, np.maximum(-field, 0.0), 0.0)
    mass = float((wgt * dV).sum())
    if mass <= 1e-30:
        loc = float(field[w].max() if sign > 0 else field[w].min()) if np.any(w) else 0.0
        return None, 0.0, loc
    cx = float((wgt * (center[0] + dx) * dV).sum() / mass)
    cy = float((wgt * (center[1] + dy) * dV).sum() / mass)
    cz = float((wgt * (center[2] + dz) * dV).sum() / mass)
    loc = float(field[w].max() if sign > 0 else field[w].min()) if np.any(w) else 0.0
    return wrap_point((cx, cy, cz), box), mass, loc


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
        used_out = add_isosurface(ax, rho, ISO_FRAC_OUT * peak, dx, box, "#2b6cb0", alpha=0.16)
        used_in = add_isosurface(ax, rho, ISO_FRAC_IN * peak, dx, box, "#e53e3e", alpha=0.45)
    setup_3d_box(ax, box)
    return {"outer": used_out, "inner": used_in}


def plot_re_isosurface(ax, re, dx, box):
    re_max = float(re.max()) if re.size else 0.0
    re_min = float(re.min()) if re.size else 0.0
    used_p = "skip"
    used_n = "skip"
    if re_max > 0:
        used_p = add_isosurface(ax, re, RE_ISO_FRAC * re_max, dx, box, "#c53030", alpha=0.35)
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


def save_midplane(path, sl, title, cmap="magma", vmin=None, vmax=None, marks_xy=None, cbar_label=None):
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
    if marks_xy:
        for p, c, lab in marks_xy:
            if p is None:
                continue
            ax.plot(p[0], p[1], "o", color=c, ms=6, label=lab)
        ax.legend(fontsize=7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def gaussian_at(X, Y, Z, center, sigma, box):
    ddx = min_image(X - center[0], box)
    ddy = min_image(Y - center[1], box)
    ddz = min_image(Z - center[2], box)
    rr2 = ddx * ddx + ddy * ddy + ddz * ddz
    return np.exp(-rr2 / (2.0 * sigma * sigma))


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
    g_env = gaussian_at(X, Y, Z, C_ENV, S_ENV, LBOX)
    g_obs = gaussian_at(X, Y, Z, C_OBS, S_IN, LBOX)
    g_obd = gaussian_at(X, Y, Z, C_OBD, S_IN, LBOX)
    # fase 0 no envelope e no observador; fase π no observado = multiplicar por −1
    psi = (g_env + g_obs - g_obd).astype(DTYPE_PSI)
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


def record_metrics(psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam, X, Y, Z, track_a, track_b):
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
        "n_det_rho": 0,
        "n_raw_rho": 0,
        "n_pos": 0,
        "n_neg": 0,
        "n_raw_pos": 0,
        "n_raw_neg": 0,
        "n_inner": 0,
        "pair_sep": float("nan"),
        "pair_sep_com": float("nan"),
        "ax": float("nan"),
        "ay": float("nan"),
        "az": float("nan"),
        "bx": float("nan"),
        "by": float("nan"),
        "bz": float("nan"),
        "re_plus": float("nan"),
        "re_minus": float("nan"),
        "re_max": float("nan"),
        "re_min": float("nan"),
        "mass_plus": float("nan"),
        "mass_minus": float("nan"),
        "two_inner": False,
        "nest3": False,
    }
    if not finite:
        return rho, re, nan_rec, track_a, track_b
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

    coords_rho, _, n_raw_rho = local_extrema(rho, PEAK_FRAC, dx, LBOX, MIN_DIST_ATOM, sign=+1)
    n_det_rho = int(coords_rho.shape[0])

    coords_pos, vals_pos, n_raw_pos = local_extrema(re, PEAK_FRAC, dx, LBOX, MIN_DIST_ATOM, sign=+1)
    coords_neg, vals_neg, n_raw_neg = local_extrema(re, PEAK_FRAC, dx, LBOX, MIN_DIST_ATOM, sign=-1)
    n_pos = int(coords_pos.shape[0])
    n_neg = int(coords_neg.shape[0])

    pa, da = nearest_xyz(coords_pos, track_a, dx, LBOX)
    pb, db = nearest_xyz(coords_neg, track_b, dx, LBOX)
    ok_pos = pa is not None and np.isfinite(da) and da <= INNER_ASSIGN_MAX
    ok_neg = pb is not None and np.isfinite(db) and db <= INNER_ASSIGN_MAX
    # par interno só conta se o detector ainda vê + e − localizados (não banho)
    bath_like = (n_raw_pos > NMS_CAP) or (n_raw_neg > NMS_CAP) or (n_raw_rho > NMS_CAP)
    two_inner = bool(ok_pos and ok_neg and (not bath_like) and n_pos >= 1 and n_neg >= 1)
    n_inner = int(ok_pos) + int(ok_neg) if (not bath_like) else 0
    if not two_inner:
        n_inner = 0 if bath_like else int(ok_pos) + int(ok_neg)

    com_p, mass_p, re_p = signed_com(re, track_a, X, Y, Z, dV, LBOX, TRACK_RADIUS, sign=+1)
    com_m, mass_m, re_m = signed_com(re, track_b, X, Y, Z, dV, LBOX, TRACK_RADIUS, sign=-1)

    new_a = pa if ok_pos else (com_p if com_p is not None else track_a)
    new_b = pb if ok_neg else (com_m if com_m is not None else track_b)
    pair_sep = min_image_dist(pa, pb, LBOX) if (ok_pos and ok_neg) else float("nan")
    pair_sep_com = (
        min_image_dist(com_p, com_m, LBOX) if (com_p is not None and com_m is not None) else float("nan")
    )
    if not two_inner:
        pair_sep = float("nan")

    nest3 = bool(two_inner)

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
        "n_det_rho": n_det_rho,
        "n_raw_rho": n_raw_rho,
        "n_pos": n_pos,
        "n_neg": n_neg,
        "n_raw_pos": n_raw_pos,
        "n_raw_neg": n_raw_neg,
        "n_inner": n_inner,
        "pair_sep": pair_sep,
        "pair_sep_com": pair_sep_com,
        "ax": float(new_a[0]),
        "ay": float(new_a[1]),
        "az": float(new_a[2]),
        "bx": float(new_b[0]),
        "by": float(new_b[1]),
        "bz": float(new_b[2]),
        "re_plus": re_p,
        "re_minus": re_m,
        "re_max": float(re.max()),
        "re_min": float(re.min()),
        "mass_plus": mass_p,
        "mass_minus": mass_m,
        "two_inner": two_inner,
        "nest3": nest3,
    }
    rec.update(struct)
    return rho, re, rec, new_a, new_b


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


def linecut_re(re, x):
    mid = re.shape[1] // 2
    return x, re[:, mid, mid]


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
    X, Y, Z = st["X"], st["Y"], st["Z"]
    x1d = st["x"]
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    nu = np.asarray(NU, dtype=DTYPE_R)
    lam = np.asarray(LAM, dtype=DTYPE_R)
    rng = np.random.default_rng(SEED)

    n_steps = int(round(T_FINAL / DT))
    track_a = C_OBS
    track_b = C_OBD

    snap_targets = {
        "ic": 0.0,
        "t001": 0.01,
        "t002": 0.02,
        "early": 0.10,
        "mid": 0.5 * T_FINAL,
        "late": T_FINAL,
    }
    volumes_rho = {}
    volumes_re = {}
    snap_t = {}
    snap_marks = {}
    radial_snaps = {}
    linecuts = {}

    print("=== 32 universo_atomo I0 ===", flush=True)
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
        f"G_env(s={S_ENV})@0 phase0 + G_obs(s={S_IN})@{C_OBS} phase0 + G_obd(s={S_IN})@{C_OBD} phase_pi",
        flush=True,
    )
    print("skimage", HAS_MC, flush=True)

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
            rho, re, rec, track_a, track_b = record_metrics(
                psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam, X, Y, Z, track_a, track_b
            )
            rec["N"] = N
            rec["dx"] = dx
            metrics.append(rec)
            if rec.get("two_inner"):
                last_two_t = t
            elif t_two_lost is None and t > 0:
                t_two_lost = t
            for name, t_tgt in snap_targets.items():
                if abs(t - t_tgt) < 0.5 * DT * rec_every + 1e-12 or abs(t - t_tgt) < 0.6 * DT:
                    volumes_rho[name] = rho.copy()
                    volumes_re[name] = re.copy()
                    snap_t[name] = t
                    snap_marks[name] = (
                        (track_a, "#c53030", "obs +"),
                        (track_b, "#2b6cb0", "obd −"),
                    )
                    rc, rm, _ = radial_profile(rho, r)
                    radial_snaps[name] = (rc, rm, t)
                    linecuts[name] = (x1d.copy(), re[:, re.shape[1] // 2, re.shape[2] // 2].copy(), t)
            print(
                f"t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
                f"PR={rec['PR']:.6e} Rrms={rec['R_rms']:.6e} "
                f"sep={rec['pair_sep']:.6f} n_inner={rec['n_inner']} "
                f"n_pos={rec['n_pos']} n_neg={rec['n_neg']} "
                f"re+={rec['re_plus']:.4e} re-={rec['re_minus']:.4e} "
                f"two={rec['two_inner']} nest3={rec['nest3']} finite={rec['finite']}",
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
    sep_s = series("pair_sep")
    two_s = np.array([bool(m["two_inner"]) for m in metrics])
    nest_s = np.array([bool(m["nest3"]) for m in metrics])
    n_two = int(two_s.sum())
    if np.any(two_s):
        t_last_two = float(t_arr[two_s][-1])
    else:
        t_last_two = 0.0
    if t_two_lost is None and (not last["two_inner"]):
        lost = np.where(~two_s & (t_arr > 0))[0]
        t_two_lost = float(t_arr[lost[0]]) if lost.size else None
    if np.any(nest_s):
        t_last_nest3 = float(t_arr[nest_s][-1])
    else:
        t_last_nest3 = 0.0

    if n_two >= 2:
        sep_two = sep_s[two_s]
        t_two = t_arr[two_s]
        sep0 = float(sep_two[0])
        sep_last_two = float(sep_two[-1])
        dsep_two = sep_last_two - sep0
        dt_two = float(t_two[-1] - t_two[0]) if t_two.size > 1 else float("nan")
        v_sep = dsep_two / dt_two if (np.isfinite(dt_two) and dt_two > 0) else float("nan")
    elif n_two == 1:
        sep0 = float(sep_s[two_s][0])
        sep_last_two = sep0
        dsep_two = 0.0
        v_sep = float("nan")
    else:
        sep0 = float(first["pair_sep"])
        sep_last_two = float("nan")
        dsep_two = float("nan")
        v_sep = float("nan")

    filled_early = bool(
        (first["two_inner"] and t_last_two < 1.0)
        or (np.isfinite(last["R_rms"]) and last["R_rms"] > 2.0 * max(first["R_rms"], 1e-12))
        or (np.isfinite(last["PR"]) and last["PR"] > 10.0 * max(first["PR"], 1e-12))
        or (np.isfinite(last["norm"]) and last["norm"] > 10.0 * max(first["norm"], 1e-12))
    )
    pair_readable = bool(t_last_two >= 1.0 and n_two >= 8)
    nest_readable = bool(t_last_nest3 >= 1.0 and int(nest_s.sum()) >= 8)
    peak_finite = bool(np.isfinite(peak_s).all() and (not blew) and float(np.nanmax(peak_s)) < 1.0e30)
    peak_max = float(np.nanmax(peak_s)) if peak_s.size else float("nan")
    t_peak = float(t_arr[int(np.nanargmax(peak_s))]) if peak_s.size and np.isfinite(peak_s).any() else None

    # anti-colapso / ímã-repele: pair_sep sobe enquanto o par +/− ainda existe
    if blew or not last.get("finite", False):
        verd_pair = "NUMERICAL_FAILURE"
        verd_peak = "NUMERICAL_FAILURE"
        verd_nest = "NUMERICAL_FAILURE"
        note_pair = "NaN/blowup — exclusão técnica."
        note_peak = "NaN/blowup — exclusão técnica."
        note_nest = "NaN/blowup — exclusão técnica."
    else:
        if not pair_readable:
            verd_pair = "INCONCLUSIVE"
            note_pair = (
                "O par +/− interno não permaneceu n_inner=2 tempo bastante para ler "
                "repulsão. Com este banho (kT=1) as sementes viram universo "
                "antes de um afastamento ser lido. kT não foi retocado."
            )
        elif np.isfinite(dsep_two) and dsep_two > 0.25:
            verd_pair = "PARTIAL"
            note_pair = (
                "pair_sep subiu enquanto ainda havia n_inner=2; leitura possível de "
                "repulsão (ímã mesmo-polo), sem lei de força nem prova."
            )
        elif np.isfinite(dsep_two) and abs(dsep_two) <= 0.25:
            verd_pair = "NOT_SUPPORTED"
            note_pair = "Par +/− visível, mas pair_sep não subiu de forma clara."
        else:
            verd_pair = "NOT_SUPPORTED"
            note_pair = "pair_sep não subiu (aproximaram-se ou o rastreador perdeu o par)."
        if peak_finite:
            verd_peak = "SUPPORTED"
            note_peak = (
                "peak ρ permaneceu finito em todo o T (anti-colapso / singularidade "
                "não foi a infinito neste run)."
            )
        else:
            verd_peak = "NOT_SUPPORTED"
            note_peak = "peak ρ não permaneceu finito."
        if not first.get("two_inner", False):
            verd_nest = "INCONCLUSIVE"
            note_nest = (
                "A IC já não passou no critério operacional de ninho 3 escalas "
                "(envelope + par +/− interno)."
            )
        elif not nest_readable:
            verd_nest = "INCONCLUSIVE"
            note_nest = (
                "O ninho 3 escalas (universo-átomo + observador + observado) não "
                "durou tempo bastante. Com kT=1 as sementes internas dissolvem; "
                "o volume preenchido continua o universo. kT não foi retocado."
            )
        else:
            verd_nest = "PARTIAL"
            note_nest = "Ninho 3 escalas visível por tempo; ver t_last_nest3."

    mid_m, _ = nearest_metric(metrics, 0.5 * T_FINAL)
    early_m, _ = nearest_metric(metrics, 0.10)
    t001_m, _ = nearest_metric(metrics, 0.01)
    t002_m, _ = nearest_metric(metrics, 0.02)

    rad_rows = []
    for name in ("ic", "t001", "t002", "early", "mid", "late"):
        if name not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[name]
        for ri, yi in zip(rc, rm):
            rad_rows.append({"snap": name, "t": tt, "r": float(ri), "rho_shell": float(yi)})
    if rad_rows:
        write_csv(out / "radial_profiles.csv", rad_rows, ["snap", "t", "r", "rho_shell"])

    lc_rows = []
    for name in ("ic", "t001", "t002", "early", "mid", "late"):
        if name not in linecuts:
            continue
        xx, yy, tt = linecuts[name]
        for xi, yi in zip(xx, yy):
            lc_rows.append({"snap": name, "t": tt, "x": float(xi), "Re_psi": float(yi)})
    if lc_rows:
        write_csv(out / "linecut_re.csv", lc_rows, ["snap", "t", "x", "Re_psi"])

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "question": "I0 universo-átomo — ninho 3 escalas / par +/− / pico finito (environment, não scan)",
        "leitura": "anti-colapso / ímã-repele (não MQ, não colapso-como-gravidade)",
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
        "s_env": S_ENV,
        "s_in": S_IN,
        "c_env": list(C_ENV),
        "c_obs": list(C_OBS),
        "c_obd": list(C_OBD),
        "sep_ic": SEP_IC,
        "phases": [0.0, 0.0, float(np.pi)],
        "phase_labels": ["envelope +", "observador +", "observado −"],
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
        "pair_sep_initial": first["pair_sep"],
        "pair_sep_final": last["pair_sep"],
        "pair_sep_last_two_inner": sep_last_two,
        "dsep_while_two_inner": dsep_two,
        "v_sep_while_two_inner": v_sep,
        "n_inner_initial": first["n_inner"],
        "n_inner_final": last["n_inner"],
        "n_inner_t0.01": t001_m["n_inner"],
        "n_inner_t0.02": t002_m["n_inner"],
        "n_inner_t0.1": early_m["n_inner"],
        "n_det_rho_initial": first["n_det_rho"],
        "n_det_rho_t0.01": t001_m["n_det_rho"],
        "n_det_rho_t0.02": t002_m["n_det_rho"],
        "n_raw_rho_t0.02": t002_m["n_raw_rho"],
        "n_raw_pos_t0.02": t002_m["n_raw_pos"],
        "n_raw_neg_t0.02": t002_m["n_raw_neg"],
        "two_inner_t0": bool(first["two_inner"]),
        "two_inner_t0.01": bool(t001_m["two_inner"]),
        "two_inner_t0.02": bool(t002_m["two_inner"]),
        "two_inner_t0.1": bool(early_m["two_inner"]),
        "two_inner_final": bool(last["two_inner"]),
        "nest3_t0": bool(first["nest3"]),
        "nest3_t0.01": bool(t001_m["nest3"]),
        "nest3_t0.02": bool(t002_m["nest3"]),
        "nest3_final": bool(last["nest3"]),
        "t_last_two_inner": t_last_two,
        "t_two_lost": t_two_lost,
        "t_last_nest3": t_last_nest3,
        "n_records_two_inner": n_two,
        "pair_repel_readable": pair_readable,
        "nest3_readable": nest_readable,
        "filled_early": filled_early,
        "bath_ate_pair_before_repel": bool(filled_early and not pair_readable),
        "re_plus_initial": first["re_plus"],
        "re_minus_initial": first["re_minus"],
        "re_max_initial": first["re_max"],
        "re_min_initial": first["re_min"],
        "Vmem_peak_max": float(np.nanmax(series("Vmem_peak"))),
        "t_Vmem_peak": float(t_arr[int(np.nanargmax(series("Vmem_peak")))]),
        "Vmem_peak_final": last["Vmem_peak"],
        "k_star_final": last["k_star"],
        "k_star_L_final": last["k_star_L"],
        "peak_n_cells_half_final": last["peak_n_cells_half"],
        "peak_width_phys_final": last["peak_width_phys"],
        "verdict_pair_repel": verd_pair,
        "verdict_finite_peak": verd_peak,
        "verdict_nest3": verd_nest,
        "note_pair": note_pair,
        "note_peak": note_peak,
        "note_nest": note_nest,
        "snap_t": {k: float(v) for k, v in snap_t.items()},
        "out": str(out),
    }
    for key in ("norm", "peak", "PR", "R_rms", "pair_sep", "n_inner"):
        lm, ls, ln = stats(key, late_mask)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln

    iso_used = {}
    fig_specs = [
        ("ic", "01_ic_isosurface.png", "32 IC  ρ  envelope s=8 ⊃ par s=1  t={t:.2f}"),
        ("early", "01b_isosurface_early.png", "32 isosuperfície ρ early  t={t:.2f}  (banho kT=1)"),
        ("mid", "02_isosurface_mid.png", "32 isosuperfície ρ mid  t={t:.2f}"),
        ("late", "03_isosurface_late.png", "32 isosuperfície ρ late  t={t:.2f}  universo no cubo"),
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
            f"32 isosuperfície ρ t={tt:.3f}  (se o ninho já morreu, é isto)",
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
            f"32 isosuperfície ρ t={tt:.3f}",
        )
        iso_used["t001"] = {"method": used, "peak": peak, "t": tt}

    if "ic" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01e_ic_re_isosurface.png",
            volumes_re["ic"],
            dx,
            LBOX,
            "32 IC  Re(Ψ)  vermelho + / azul −  t=0",
        )
        iso_used["ic_re"] = used_re
        print("iso_re ic", used_re, flush=True)
    if "t002" in volumes_re:
        used_re = save_re_iso_fig(
            out / "01f_t002_re_isosurface.png",
            volumes_re["t002"],
            dx,
            LBOX,
            f"32 Re(Ψ) t={snap_t['t002']:.3f}  +/−",
        )
        iso_used["t002_re"] = used_re

    # midplane ρ 2x2
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 9.4))
    order = [("ic", "t=0 IC"), ("early", "early"), ("mid", "mid"), ("late", "late")]
    for ax, (key, lab) in zip(axes.ravel(), order):
        if key not in volumes_rho:
            ax.set_title(f"{lab} ausente")
            continue
        sl = volumes_rho[key][:, :, volumes_rho[key].shape[2] // 2]
        im = ax.imshow(
            sl.T,
            origin="lower",
            extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
            cmap="magma",
        )
        fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}  |Ψ|² z=0")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("32 — midplane xy  |Ψ|²  (universo-átomo, Theta_core, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "04_midplane_xy.png", dpi=150)
    plt.close(fig)

    # midplane Re 2x2 — MONEY para +/−
    fig, axes = plt.subplots(2, 2, figsize=(10.4, 9.4))
    for ax, (key, lab) in zip(axes.ravel(), order):
        if key not in volumes_re:
            ax.set_title(f"{lab} ausente")
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
        ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}  Re(Ψ) z=0")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
    fig.suptitle("32 — midplane xy  Re(Ψ)  vermelho + / azul −")
    fig.tight_layout()
    fig.savefig(out / "04r_midplane_re.png", dpi=150)
    plt.close(fig)

    for key, fname in (
        ("ic", "04a_midplane_t0.png"),
        ("t001", "04f_midplane_t001.png"),
        ("t002", "04e_midplane_t002.png"),
        ("early", "04b_midplane_early.png"),
        ("mid", "04c_midplane_mid.png"),
        ("late", "04d_midplane_late.png"),
    ):
        if key not in volumes_rho:
            continue
        sl = volumes_rho[key][:, :, volumes_rho[key].shape[2] // 2]
        save_midplane(
            out / fname,
            sl,
            f"32 midplane xy  |Ψ|²  {key}  t={snap_t.get(key, 0):.3f}",
            cmap="magma",
            marks_xy=snap_marks.get(key),
            cbar_label="|Ψ|²",
        )

    for key, fname in (
        ("ic", "04g_midplane_re_t0.png"),
        ("t001", "04h_midplane_re_t001.png"),
        ("t002", "04i_midplane_re_t002.png"),
        ("early", "04j_midplane_re_early.png"),
        ("mid", "04k_midplane_re_mid.png"),
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
            f"32 midplane xy  Re(Ψ)  {key}  t={snap_t.get(key, 0):.3f}",
            cmap="RdBu_r",
            vmin=-vmax,
            vmax=vmax,
            marks_xy=snap_marks.get(key),
            cbar_label="Re(Ψ)",
        )

    # linecut Re(x)
    fig, ax = plt.subplots(figsize=(8.2, 4.6))
    colors = {"ic": "C0", "t001": "C1", "t002": "C3", "early": "0.4", "mid": "C2", "late": "0.2"}
    for key in ("ic", "t001", "t002", "early"):
        if key not in linecuts:
            continue
        xx, yy, tt = linecuts[key]
        ax.plot(xx, yy, color=colors.get(key, "k"), lw=1.5, label=f"{key} t={tt:.3f}")
    ax.axhline(0.0, color="0.5", ls="--", lw=0.7)
    ax.axvline(C_OBS[0], color="#c53030", ls=":", lw=0.8, label="obs +")
    ax.axvline(C_OBD[0], color="#2b6cb0", ls=":", lw=0.8, label="obd −")
    ax.set_xlabel("x")
    ax.set_ylabel("Re(Ψ)(x,0,0)")
    ax.set_title("32 — corte Re(Ψ) ao longo de x  (+ esquerda / − direita)")
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
    ax.axvline(C_OBS[0], color="#c53030", ls=":", lw=0.8)
    ax.axvline(C_OBD[0], color="#2b6cb0", ls=":", lw=0.8)
    ax.set_xlim(-12, 12)
    ax.set_xlabel("x")
    ax.set_ylabel("Re(Ψ)")
    ax.set_title("32 — Re(Ψ) t=0 zoom  (envelope + par +/−)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "09b_linecut_re_t0.png", dpi=150)
    plt.close(fig)

    # radial
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    colors_r = {"ic": "C0", "t001": "C1", "t002": "C3", "early": "C4", "mid": "C2", "late": "0.35"}
    labels_r = {
        "ic": "t=0 IC",
        "t001": "t=0.01",
        "t002": "t=0.02",
        "early": "early t=0.10",
        "mid": "mid t=4",
        "late": "late t=8",
    }
    for key in ("ic", "t001", "t002", "early", "mid", "late"):
        if key not in radial_snaps:
            continue
        rc, rm, tt = radial_snaps[key]
        ax.semilogy(rc, np.maximum(rm, 1e-20), color=colors_r[key], lw=1.6, label=labels_r[key])
    ax.axvline(S_IN, color="C0", ls=":", lw=0.9, alpha=0.7)
    ax.axvline(S_ENV, color="C0", ls="--", lw=0.9, alpha=0.7)
    ax.axvline(2.5, color="0.5", ls=":", lw=0.6)
    ax.set_xlabel("r")
    ax.set_ylabel("ρ(r)  (média em casca)")
    ax.set_title("32 — perfil radial  (envelope s=8 + par em r≈2.5)")
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
        ax.plot(rc, rm, color="C3", lw=1.3, label=f"t={tt:.3f}")
    ax.axvline(S_IN, color="0.4", ls=":", lw=0.8, label="s_in=1")
    ax.axvline(S_ENV, color="0.4", ls="--", lw=0.8, label="s_env=8")
    ax.axvline(2.5, color="0.5", ls=":", lw=0.6, label="|x|=2.5")
    ax.set_xlim(0, 16)
    ax.set_xlabel("r")
    ax.set_ylabel("ρ(r)")
    ax.set_title("32 — perfil radial linear  (envelope visível em t=0)")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06b_radial_linear.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, sep_s, color="C0", lw=1.4)
    axes[0, 0].axhline(SEP_IC, color="0.5", ls="--", lw=0.8, label="sep IC=5")
    if t_last_two > 0:
        axes[0, 0].axvline(t_last_two, color="C3", ls=":", lw=1.0, label=f"último +/− t={t_last_two:.3f}")
    axes[0, 0].set_title("distância do par interno (min-image)")
    axes[0, 0].set_ylabel("pair_sep")
    axes[0, 0].legend(fontsize=7)
    axes[0, 1].plot(t_arr, peak_s, color="C3", lw=1.4)
    axes[0, 1].set_title("peak ρ  (fica finito?)")
    axes[1, 0].plot(t_arr, series("PR"), color="C0", lw=1.4)
    axes[1, 0].set_title("PR")
    axes[1, 1].plot(t_arr, series("R_rms"), color="C2", lw=1.4)
    axes[1, 1].set_title("R_rms  (envelope / universo)")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("32 universo-átomo — par +/− / pico / envelope  (Theta_core, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "05_observables.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, series("n_inner"), color="C4", lw=1.3, label="n_inner")
    axes[0, 0].axhline(2, color="0.4", ls="--", lw=0.8, label="2 internos")
    axes[0, 0].set_title("n_inner  (extremos Re +/−)")
    axes[0, 0].legend(fontsize=8)
    axes[0, 1].plot(t_arr, series("n_pos"), label="n_pos")
    axes[0, 1].plot(t_arr, series("n_neg"), label="n_neg")
    axes[0, 1].legend(fontsize=8)
    axes[0, 1].set_title("extremos Re atribuídos")
    axes[1, 0].plot(t_arr, series("re_plus"), color="#c53030", label="Re+ local")
    axes[1, 0].plot(t_arr, series("re_minus"), color="#2b6cb0", label="Re− local")
    axes[1, 0].axhline(0.0, color="0.5", ls="--", lw=0.6)
    axes[1, 0].legend(fontsize=8)
    axes[1, 0].set_title("Re local dos dois internos")
    nest_int = nest_s.astype(float)
    axes[1, 1].step(t_arr, nest_int, where="post", color="C4", lw=1.4)
    if t_last_nest3 > 0:
        axes[1, 1].axvline(t_last_nest3, color="C3", ls=":", lw=1.0, label=f"último nest3 t={t_last_nest3:.3f}")
        axes[1, 1].legend(fontsize=7)
    axes[1, 1].set_ylim(-0.05, 1.15)
    axes[1, 1].set_title("nest3 (envelope + par +/−)")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("32 — ninho 3 escalas vs t")
    fig.tight_layout()
    fig.savefig(out / "08_nest3.png", dpi=150)
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    mask_e = t_arr <= max(EARLY_T, 0.5)
    axes[0].plot(t_arr[mask_e], sep_s[mask_e], "o-", color="C0", ms=3)
    axes[0].axhline(SEP_IC, color="0.5", ls="--", lw=0.8)
    axes[0].set_title("pair_sep  (janela cedo)")
    axes[0].set_xlabel("t")
    axes[0].set_ylabel("sep")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(t_arr[mask_e], peak_s[mask_e], "o-", color="C3", ms=3)
    axes[1].set_title("peak ρ  (janela cedo)")
    axes[1].set_xlabel("t")
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("32 — zoom t≤0.4  (o par +/− some aqui se kT=1 preencher)")
    fig.tight_layout()
    fig.savefig(out / "07_early_zoom.png", dpi=150)
    plt.close(fig)

    fig = plt.figure(figsize=(13.0, 8.8))
    gs = fig.add_gridspec(2, 3)
    order3 = [("ic", "IC t=0  ninho 3"), ("early", "early"), ("late", "late = universo")]
    positions = [(0, 0), (0, 1), (0, 2)]
    for (key, lab), (ri, ci) in zip(order3, positions):
        ax = fig.add_subplot(gs[ri, ci], projection="3d")
        if key in volumes_rho:
            plot_rho_isosurface(ax, volumes_rho[key], float(volumes_rho[key].max()), dx, LBOX)
            ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}")
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
    ax.set_title("Re(Ψ) t=0  +/−")
    ax = fig.add_subplot(gs[1, 1])
    ax.plot(t_arr, sep_s, label="pair_sep")
    ax.axhline(SEP_IC, color="0.5", ls="--", lw=0.7)
    if t_last_two > 0:
        ax.axvline(t_last_two, color="C3", ls=":", lw=1.0)
    ax.legend(fontsize=8)
    ax.set_title("distância do par +/−")
    ax.grid(True, alpha=0.3)
    ax = fig.add_subplot(gs[1, 2])
    ax.plot(t_arr, peak_s, color="C3", label="peak")
    ax.plot(t_arr, series("R_rms"), color="C2", label="R_rms")
    ax.legend(fontsize=8)
    ax.set_title("peak / R_rms  (pico finito?)")
    ax.grid(True, alpha=0.3)
    fig.suptitle(
        "32 universo-átomo — I0, Theta_core, kT=1, N=64  (ninho 3 / ímã-repele / pico finito)"
    )
    fig.tight_layout()
    fig.savefig(out / "00_montagem.png", dpi=150)
    plt.close(fig)

    summary["iso_used"] = iso_used

    for key in ("ic", "t001", "t002", "early", "mid", "late"):
        if key in volumes_rho:
            np.save(out / f"rho_{key}.npy", volumes_rho[key])
        if key in volumes_re:
            np.save(out / f"re_{key}.npy", volumes_re[key])

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
    print("VERDICT_PAIR", verd_pair, flush=True)
    print("VERDICT_PEAK", verd_peak, flush=True)
    print("VERDICT_NEST3", verd_nest, flush=True)
    print(
        "t_last_two_inner",
        t_last_two,
        "t_lost",
        t_two_lost,
        "t_last_nest3",
        t_last_nest3,
        "dsep",
        dsep_two,
        "peak_max",
        peak_max,
        "wall",
        wall,
        flush=True,
    )


if __name__ == "__main__":
    main()
