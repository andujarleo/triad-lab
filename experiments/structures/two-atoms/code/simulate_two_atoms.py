#!/usr/bin/env python3
"""Run 30 — dois átomos (I0 / environment). Gravidade / singularidade finita.

Tríade completa, Theta_core congelado (Q00). Standalone 3D Strang.
1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
NÃO é teste de interferência. NÃO isola memória/FDT. NÃO muda Theta_core.
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
OUT_VAULT = VAULT / "Artefatos" / "triad_dois_atomos"
FALLBACK = Path("/tmp/triad_dois_atomos")
RUN_ID = "30"
RUN_NAME = "triad_dois_atomos"

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
INIT_SIGMA = 1.0
SEP = 6.0
C1 = (-3.0, 0.0, 0.0)
C2 = (3.0, 0.0, 0.0)
Y0 = 0.0
V_EXT = 0.0
RECORD_EVERY = 40
RECORD_EVERY_EARLY = 4
EARLY_T = 0.40
K_CUT_FACTOR = 1.0
BACKEND = "numpy"
DTYPE_PSI = np.complex128
DTYPE_R = np.float64
ISO_FRAC = 0.30
PEAK_FRAC = 0.20
MIN_DIST_ATOM = 2.0 * INIT_SIGMA
TRACK_RADIUS = 2.5 * INIT_SIGMA
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


def local_atom_peaks(rho, peak, frac, dx, box, min_dist, nms_cap=48):
    """Máximos locais. Se n_raw>nms_cap o volume já não é um par — não faz NMS O(n²)."""
    footprint = maximum_filter(rho, size=3, mode="wrap")
    is_max = (rho == footprint) & (rho >= frac * peak) & (peak > 0)
    coords = np.argwhere(is_max)
    vals = rho[is_max]
    n_raw = int(coords.shape[0])
    if coords.size == 0:
        return coords, vals, n_raw
    if n_raw > nms_cap:
        empty = coords[:0]
        return empty, vals[:0], n_raw
    order = np.argsort(-vals)
    coords, vals = coords[order], vals[order]
    coords, vals = nms_min_dist(coords, vals, dx, box, min_dist)
    return coords, vals, n_raw


def blob_com_near(rho, center, X, Y, Z, dV, box, radius):
    """COM periódico da densidade num raio em torno de um centro rastreado."""
    dx = min_image(X - center[0], box)
    dy = min_image(Y - center[1], box)
    dz = min_image(Z - center[2], box)
    r2 = dx * dx + dy * dy + dz * dz
    w = r2 <= (radius * radius)
    mass = float((rho[w] * dV).sum())
    if mass <= 1e-30:
        return None, 0.0, 0.0
    cx = float((rho[w] * (center[0] + dx[w]) * dV).sum() / mass)
    cy = float((rho[w] * (center[1] + dy[w]) * dV).sum() / mass)
    cz = float((rho[w] * (center[2] + dz[w]) * dV).sum() / mass)
    loc_peak = float(rho[w].max()) if np.any(w) else 0.0
    return wrap_point((cx, cy, cz), box), mass, loc_peak


def assign_two_maxima(coords, vals, dx, box, prev_a, prev_b):
    """Dois máximos mais próximos dos centros rastreados (min-image)."""
    if coords.shape[0] == 0:
        return None, None, float("nan")
    xyz = coords_to_xyz(coords, dx, box)
    if coords.shape[0] == 1:
        d0 = min_image_dist(xyz[0], prev_a, box)
        d1 = min_image_dist(xyz[0], prev_b, box)
        if d0 <= d1:
            return tuple(xyz[0]), None, float("nan")
        return None, tuple(xyz[0]), float("nan")
    da = np.array([min_image_dist(p, prev_a, box) for p in xyz])
    db = np.array([min_image_dist(p, prev_b, box) for p in xyz])
    i_a = int(np.argmin(da))
    i_b = int(np.argmin(db))
    if i_a == i_b:
        # o mesmo máximo ganhou os dois: o segundo vai para o outro tracker
        order_a = np.argsort(da)
        order_b = np.argsort(db)
        if da[i_a] <= db[i_b]:
            i_b = int(order_b[1] if order_b.size > 1 else order_b[0])
            if i_b == i_a and order_b.size > 1:
                i_b = int(order_b[1])
        else:
            i_a = int(order_a[1] if order_a.size > 1 else order_a[0])
            if i_a == i_b and order_a.size > 1:
                i_a = int(order_a[1])
    if i_a == i_b:
        return tuple(xyz[i_a]), None, float("nan")
    pa = tuple(float(v) for v in xyz[i_a])
    pb = tuple(float(v) for v in xyz[i_b])
    return pa, pb, min_image_dist(pa, pb, box)


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


def save_isosurface_fig(path, rho, peak, dx, box, title, marks=None):
    fig = plt.figure(figsize=(6.2, 5.8))
    ax = fig.add_subplot(111, projection="3d")
    level = ISO_FRAC * peak if peak > 0 else 0.0
    used = plot_isosurface(ax, rho, level, dx, box)
    if marks:
        for (p, c, lab) in marks:
            if p is None:
                continue
            ax.scatter([p[0]], [p[1]], [p[2]], s=40, c=c, depthshade=False, label=lab)
        ax.legend(fontsize=7, loc="upper left")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return used, level


def save_midplane(path, sl, title, marks_xy=None):
    fig, ax = plt.subplots(figsize=(5.6, 5.2))
    im = ax.imshow(
        sl.T,
        origin="lower",
        extent=(-LBOX / 2, LBOX / 2, -LBOX / 2, LBOX / 2),
        cmap="magma",
    )
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    if marks_xy:
        for (p, c, lab) in marks_xy:
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
    psi = np.zeros((N, N, N), dtype=DTYPE_PSI)
    for cx, cy, cz in (C1, C2):
        ddx = min_image(X - cx, LBOX)
        ddy = min_image(Y - cy, LBOX)
        ddz = min_image(Z - cz, LBOX)
        rr2 = ddx * ddx + ddy * ddy + ddz * ddz
        psi = psi + np.exp(-rr2 / (2.0 * s * s))
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
        "n_det": 0,
        "n_raw": 0,
        "pair_sep": float("nan"),
        "pair_sep_com": float("nan"),
        "n_blobs_ok": 0,
        "ax": float("nan"),
        "ay": float("nan"),
        "az": float("nan"),
        "bx": float("nan"),
        "by": float("nan"),
        "bz": float("nan"),
        "mass_a": float("nan"),
        "mass_b": float("nan"),
        "peak_a": float("nan"),
        "peak_b": float("nan"),
        "two_blobs": False,
    }
    if not finite:
        return rho, nan_rec, track_a, track_b
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

    coords, vals, n_raw = local_atom_peaks(rho, peak, PEAK_FRAC, dx, LBOX, MIN_DIST_ATOM)
    n_det = int(coords.shape[0])
    pa, pb, pair_sep = assign_two_maxima(coords, vals, dx, LBOX, track_a, track_b)

    com_a, mass_a, peak_a = blob_com_near(rho, track_a, X, Y, Z, dV, LBOX, TRACK_RADIUS)
    com_b, mass_b, peak_b = blob_com_near(rho, track_b, X, Y, Z, dV, LBOX, TRACK_RADIUS)

    # atualiza rastreio: prefere máximo local atribuído; senão COM local
    new_a = pa if pa is not None else (com_a if com_a is not None else track_a)
    new_b = pb if pb is not None else (com_b if com_b is not None else track_b)
    pair_sep_com = (
        min_image_dist(com_a, com_b, LBOX) if (com_a is not None and com_b is not None) else float("nan")
    )
    if not np.isfinite(pair_sep) and com_a is not None and com_b is not None:
        pair_sep = pair_sep_com

    # dois blobs: n_det==2, ou dois COMs com massa local acima de um piso fraco
    mean_rho = float(rho.mean())
    blob_floor = max(5.0 * mean_rho, 1e-8)
    ok_a = (pa is not None) or (com_a is not None and peak_a >= blob_floor)
    ok_b = (pb is not None) or (com_b is not None and peak_b >= blob_floor)
    n_blobs_ok = int(ok_a) + int(ok_b)
    # par só conta se o detector ainda vê 2 máximos (não COM fantasma no banho)
    two_blobs = bool(n_det == 2)
    if not two_blobs:
        pair_sep = float("nan")

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
        "n_det": n_det,
        "n_raw": n_raw,
        "pair_sep": pair_sep,
        "pair_sep_com": pair_sep_com,
        "n_blobs_ok": n_blobs_ok,
        "ax": float(new_a[0]),
        "ay": float(new_a[1]),
        "az": float(new_a[2]),
        "bx": float(new_b[0]),
        "by": float(new_b[1]),
        "bz": float(new_b[2]),
        "mass_a": mass_a,
        "mass_b": mass_b,
        "peak_a": peak_a,
        "peak_b": peak_b,
        "two_blobs": two_blobs,
    }
    rec.update(struct)
    return rho, rec, new_a, new_b


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
    dk = 2.0 * np.pi / LBOX
    k_cut = K_CUT_FACTOR * dk
    nu = np.asarray(NU, dtype=DTYPE_R)
    lam = np.asarray(LAM, dtype=DTYPE_R)
    rng = np.random.default_rng(SEED)

    n_steps = int(round(T_FINAL / DT))
    track_a = C1
    track_b = C2

    snap_targets = {
        "ic": 0.0,
        "early": 0.10,
        "mid": 0.5 * T_FINAL,
        "late": T_FINAL,
    }
    volumes = {}
    snap_t = {}
    snap_marks = {}

    print("=== 30 dois_atomos I0 ===", flush=True)
    print("start", started, "out", out, flush=True)
    print("backend", BACKEND, "dtype", "complex128/float64", flush=True)
    print("L", LBOX, "N", N, "dx", dx, "dt", DT, "T", T_FINAL, "n_steps", n_steps, flush=True)
    print("Theta_core Lambda", LAMBDA, "alpha", ALPHA, "sigma", SIGMA_FRAC, flush=True)
    print("Gamma", GAMMA, "kT", KT, "nu", NU, "lam", LAM, flush=True)
    print("fdt_couple", FDT_COUPLE, "f_FDT", f_FDT, "noise_amp", noise_amp, flush=True)
    print("noise_amp_check", float(np.sqrt(2.0 * GAMMA * KT * DT / HBAR)), flush=True)
    print("max_nu_dt", float(max(NU) * DT), "memory_update", "euler", flush=True)
    print("seed", SEED, "IC", "2 gaussians s=1.0 sep=6.0 phases=0", flush=True)
    print("centers", C1, C2, "skimage", HAS_MC, flush=True)

    metrics = []
    blew = False
    blow_t = None
    t_two_lost = None
    last_two_t = 0.0

    for step in range(n_steps + 1):
        t = step * DT
        rec_every = RECORD_EVERY_EARLY if t <= EARLY_T + 1e-12 else RECORD_EVERY
        do_rec = (step % rec_every == 0) or step == n_steps or t in (0.0, T_FINAL)
        # força snaps
        for t_tgt in snap_targets.values():
            if abs(t - t_tgt) < 0.5 * DT + 1e-15:
                do_rec = True
        if do_rec:
            rho, rec, track_a, track_b = record_metrics(
                psi, y, t, dV, dx, r2, r, k_mag, dk, k_cut, lam, X, Y, Z, track_a, track_b
            )
            rec["N"] = N
            rec["dx"] = dx
            metrics.append(rec)
            if rec.get("two_blobs"):
                last_two_t = t
            elif t_two_lost is None and t > 0:
                t_two_lost = t
            for name, t_tgt in snap_targets.items():
                if abs(t - t_tgt) < 0.5 * DT * rec_every + 1e-12 or abs(t - t_tgt) < 0.6 * DT:
                    volumes[name] = rho.copy()
                    snap_t[name] = t
                    snap_marks[name] = (
                        (track_a, "#4fd1c5", "A"),
                        (track_b, "#f6ad55", "B"),
                    )
            print(
                f"t={t:.4f} norm={rec['norm']:.6e} peak={rec['peak']:.6e} "
                f"PR={rec['PR']:.6e} Rrms={rec['R_rms']:.6e} "
                f"sep={rec['pair_sep']:.6f} n_det={rec['n_det']} "
                f"two={rec['two_blobs']} finite={rec['finite']}",
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
    two_s = np.array([bool(m["two_blobs"]) for m in metrics])
    n_two = int(two_s.sum())
    # último instante com dois blobs
    if np.any(two_s):
        t_last_two = float(t_arr[two_s][-1])
    else:
        t_last_two = 0.0
    # primeiro instante sem dois blobs após t=0
    if t_two_lost is None and (not last["two_blobs"]):
        lost = np.where(~two_s & (t_arr > 0))[0]
        t_two_lost = float(t_arr[lost[0]]) if lost.size else None

    # Δsep enquanto ainda há 2 blobs
    if n_two >= 2:
        sep_two = sep_s[two_s]
        t_two = t_arr[two_s]
        sep0 = float(sep_two[0])
        sep_last_two = float(sep_two[-1])
        dsep_two = sep_last_two - sep0
        # velocidade média de aproximação (negativo = caem juntos)
        dt_two = float(t_two[-1] - t_two[0]) if t_two.size > 1 else float("nan")
        v_sep = dsep_two / dt_two if (np.isfinite(dt_two) and dt_two > 0) else float("nan")
    else:
        sep0 = float(first["pair_sep"])
        sep_last_two = float("nan")
        dsep_two = float("nan")
        v_sep = float("nan")

    filled_early = bool(
        (first["two_blobs"] and t_last_two < 1.0)
        or (np.isfinite(last["R_rms"]) and last["R_rms"] > 2.0 * max(first["R_rms"], 1e-12))
        or (np.isfinite(last["PR"]) and last["PR"] > 10.0 * max(first["PR"], 1e-12))
    )
    pair_readable = bool(t_last_two >= 1.0 and n_two >= 8)
    peak_finite = bool(np.isfinite(peak_s).all() and (not blew) and float(np.nanmax(peak_s)) < 1.0e30)
    peak_max = float(np.nanmax(peak_s)) if peak_s.size else float("nan")
    t_peak = float(t_arr[int(np.nanargmax(peak_s))]) if peak_s.size and np.isfinite(peak_s).any() else None

    # vereditos: o que os números sustentam, sem "provou gravidade"
    if blew or not last.get("finite", False):
        verd_pair = "NUMERICAL_FAILURE"
        verd_peak = "NUMERICAL_FAILURE"
        note_pair = "NaN/blowup — exclusão técnica."
        note_peak = "NaN/blowup — exclusão técnica."
    else:
        if not pair_readable:
            verd_pair = "INCONCLUSIVE"
            note_pair = (
                "Os dois átomos não permaneceram dois blobs tempo bastante para ler "
                "atração/órbita. Com este banho (kT=1) as sementes viram universo "
                "antes de um par ser lido. kT não foi retocado."
            )
        elif np.isfinite(dsep_two) and dsep_two < -0.25:
            verd_pair = "PARTIAL"
            note_pair = (
                "pair_sep caiu enquanto ainda havia dois blobs; leitura possível de "
                "aproximação, sem órbita fechada nem lei 1/r²."
            )
        elif np.isfinite(dsep_two) and abs(dsep_two) <= 0.25:
            verd_pair = "NOT_SUPPORTED"
            note_pair = "Dois blobs visíveis, mas pair_sep não caiu de forma clara."
        else:
            verd_pair = "NOT_SUPPORTED"
            note_pair = "pair_sep não caiu (afastaram-se ou o rastreador perdeu o par)."
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

    summary = {
        "run": RUN_NAME,
        "run_id": RUN_ID,
        "question": "I0 dois átomos — par / pico finito (environment, não scan)",
        "leitura": "gravidade emergente / singularidade finita (não interferência)",
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
        "init_sigma": INIT_SIGMA,
        "sep_ic": SEP,
        "c1": list(C1),
        "c2": list(C2),
        "phases": [0.0, 0.0],
        "y0": Y0,
        "f_FDT": f_FDT,
        "f_FDT_formula": "2*Gamma*(dx**3)*kT/hbar",
        "noise_amp": noise_amp,
        "noise_amp_formula": "sqrt(f_FDT*dt/dx**3)=sqrt(2*Gamma*kT*dt/hbar)",
        "memory_update": "euler",
        "max_nu_dt": float(max(NU) * DT),
        "iso_frac": ISO_FRAC,
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
        "pair_sep_initial": first["pair_sep"],
        "pair_sep_final": last["pair_sep"],
        "pair_sep_last_two_blobs": sep_last_two,
        "dsep_while_two_blobs": dsep_two,
        "v_sep_while_two_blobs": v_sep,
        "n_det_initial": first["n_det"],
        "n_det_final": last["n_det"],
        "n_det_t0.1": early_m["n_det"],
        "two_blobs_t0": bool(first["two_blobs"]),
        "two_blobs_t0.1": bool(early_m["two_blobs"]),
        "two_blobs_final": bool(last["two_blobs"]),
        "t_last_two_blobs": t_last_two,
        "t_two_lost": t_two_lost,
        "n_records_two_blobs": n_two,
        "pair_orbit_readable": pair_readable,
        "filled_early": filled_early,
        "bath_ate_pair_before_orbit": bool(filled_early and not pair_readable),
        "Vmem_peak_max": float(np.nanmax(series("Vmem_peak"))),
        "t_Vmem_peak": float(t_arr[int(np.nanargmax(series("Vmem_peak")))]),
        "Vmem_peak_final": last["Vmem_peak"],
        "k_star_final": last["k_star"],
        "k_star_L_final": last["k_star_L"],
        "peak_n_cells_half_final": last["peak_n_cells_half"],
        "peak_width_phys_final": last["peak_width_phys"],
        "verdict_pair_distance": verd_pair,
        "verdict_finite_peak": verd_peak,
        "note_pair": note_pair,
        "note_peak": note_peak,
        "snap_t": {k: float(v) for k, v in snap_t.items()},
        "out": str(out),
    }
    for key in ("norm", "peak", "PR", "R_rms", "pair_sep", "n_det"):
        lm, ls, ln = stats(key, late_mask)
        summary[f"{key}_late_mean"] = lm
        summary[f"{key}_late_std"] = ls
        summary[f"{key}_late_n"] = ln

    # --- figures ---
    iso_used = {}
    fig_specs = [
        ("ic", "01_ic_isosurface.png", "30 IC  2 átomos s=1 sep=6  t={t:.2f}"),
        ("mid", "02_isosurface_mid.png", "30 isosuperfície mid  t={t:.2f}  ρ={frac:.1f}·peak"),
        ("late", "03_isosurface_late.png", "30 isosuperfície late  t={t:.2f}  universo no cubo"),
    ]
    for key, fname, title_tmpl in fig_specs:
        if key not in volumes:
            print("missing_volume", key, flush=True)
            continue
        rho = volumes[key]
        peak = float(rho.max())
        tt = snap_t.get(key, -1.0)
        used, level = save_isosurface_fig(
            out / fname,
            rho,
            peak,
            dx,
            LBOX,
            title_tmpl.format(t=tt, frac=ISO_FRAC),
            marks=snap_marks.get(key),
        )
        iso_used[key] = {"method": used, "level": level, "peak": peak, "t": tt}
        print("iso", key, "t", tt, "method", used, "level", level, "peak", peak, flush=True)
    if "early" in volumes:
        rho = volumes["early"]
        peak = float(rho.max())
        tt = snap_t["early"]
        used, level = save_isosurface_fig(
            out / "01b_isosurface_early.png",
            rho,
            peak,
            dx,
            LBOX,
            f"30 isosuperfície early  t={tt:.2f}  (banho kT=1)",
            marks=snap_marks.get("early"),
        )
        iso_used["early"] = {"method": used, "level": level, "peak": peak, "t": tt}

    # midplanes 2x2
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
    fig.suptitle("30 — midplane xy  (2 átomos, Theta_core, kT=1)")
    fig.tight_layout()
    fig.savefig(out / "04_midplane_xy.png", dpi=150)
    plt.close(fig)

    # also individual midplanes
    for key, fname in (
        ("ic", "04a_midplane_t0.png"),
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
            f"30 midplane xy  {key}  t={snap_t.get(key, 0):.2f}",
            marks_xy=snap_marks.get(key),
        )

    fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6))
    axes[0, 0].plot(t_arr, sep_s, color="C0", lw=1.4)
    axes[0, 0].axhline(SEP, color="0.5", ls="--", lw=0.8, label="sep IC=6")
    if t_last_two > 0:
        axes[0, 0].axvline(t_last_two, color="C3", ls=":", lw=1.0, label=f"último 2-blobs t={t_last_two:.3f}")
    axes[0, 0].set_title("distância do par (min-image)")
    axes[0, 0].set_ylabel("pair_sep")
    axes[0, 0].legend(fontsize=7)
    axes[0, 1].plot(t_arr, peak_s, color="C3", lw=1.4)
    axes[0, 1].set_title("peak ρ  (fica finito?)")
    axes[1, 0].plot(t_arr, series("PR"), color="C0", lw=1.4)
    axes[1, 0].set_title("PR")
    axes[1, 1].plot(t_arr, series("R_rms"), color="C2", lw=1.4)
    axes[1, 1].set_title("R_rms")
    for a in axes.ravel():
        a.set_xlabel("t")
        a.grid(True, alpha=0.3)
    fig.suptitle("30 dois átomos — par / pico / universo  (Theta_core, kT=1, sem retune)")
    fig.tight_layout()
    fig.savefig(out / "05_observables.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    ax.plot(t_arr, series("n_det"), color="C4", lw=1.3, label="n_det")
    ax.axhline(2, color="0.4", ls="--", lw=0.8, label="2 átomos")
    ax.set_xlabel("t")
    ax.set_ylabel("n_det")
    ax.set_title("detector de blobs vs t")
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out / "06_n_det.png", dpi=150)
    plt.close(fig)

    # zoom early pair
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.0))
    mask_e = t_arr <= max(EARLY_T, 0.5)
    axes[0].plot(t_arr[mask_e], sep_s[mask_e], "o-", color="C0", ms=3)
    axes[0].axhline(SEP, color="0.5", ls="--", lw=0.8)
    axes[0].set_title("pair_sep  (janela cedo)")
    axes[0].set_xlabel("t")
    axes[0].set_ylabel("sep")
    axes[0].grid(True, alpha=0.3)
    axes[1].plot(t_arr[mask_e], peak_s[mask_e], "o-", color="C3", ms=3)
    axes[1].set_title("peak ρ  (janela cedo)")
    axes[1].set_xlabel("t")
    axes[1].grid(True, alpha=0.3)
    fig.suptitle("30 — zoom t≤0.4  (o par some aqui se kT=1 preencher)")
    fig.tight_layout()
    fig.savefig(out / "07_early_zoom.png", dpi=150)
    plt.close(fig)

    # montagem
    fig = plt.figure(figsize=(13.0, 8.8))
    gs = fig.add_gridspec(2, 3)
    order = [("ic", "IC t=0  2 átomos"), ("mid", "mid"), ("late", "late = universo")]
    positions = [(0, 0), (0, 1), (0, 2)]
    for (key, lab), (ri, ci) in zip(order, positions):
        ax = fig.add_subplot(gs[ri, ci], projection="3d")
        if key in volumes:
            rho = volumes[key]
            plot_isosurface(ax, rho, ISO_FRAC * float(rho.max()), dx, LBOX)
            ax.set_title(f"{lab}  t={snap_t.get(key, 0):.2f}")
        else:
            setup_3d_box(ax, LBOX)
            ax.set_title(lab)
    ax = fig.add_subplot(gs[1, 0])
    ax.plot(t_arr, sep_s, label="pair_sep")
    ax.axhline(SEP, color="0.5", ls="--", lw=0.7)
    if t_last_two > 0:
        ax.axvline(t_last_two, color="C3", ls=":", lw=1.0)
    ax.legend(fontsize=8)
    ax.set_title("distância do par")
    ax.grid(True, alpha=0.3)
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
        "30 dois átomos — I0, Theta_core, kT=1, N=64  (par / singularidade finita)"
    )
    fig.tight_layout()
    fig.savefig(out / "00_montagem.png", dpi=150)
    plt.close(fig)

    summary["iso_used"] = iso_used

    # npy snaps
    for key in ("ic", "early", "mid", "late"):
        if key in volumes:
            np.save(out / f"rho_{key}.npy", volumes[key])

    write_csv(out / "summary.csv", [summary], list(summary.keys()))
    # json-friendly
    js = {}
    for k, v in summary.items():
        if isinstance(v, (np.bool_, np.integer)):
            js[k] = int(v) if isinstance(v, np.integer) else bool(v)
        elif isinstance(v, np.floating):
            js[k] = float(v)
        else:
            js[k] = v
    with (out / "summary.json").open("w") as f:
        json.dump(js, f, indent=2, default=str)

    # sha
    paths = [p for p in sorted(out.rglob("*")) if p.is_file() and p.name != "SHA256SUMS.txt"]
    lines = [f"{sha256_file(p)}  {p.relative_to(out).as_posix()}" for p in paths]
    (out / "SHA256SUMS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("SUMMARY_JSON_START", flush=True)
    print(json.dumps(js, default=str), flush=True)
    print("SUMMARY_JSON_END", flush=True)
    print("wrote", out, flush=True)
    print("VERDICT_PAIR", verd_pair, flush=True)
    print("VERDICT_PEAK", verd_peak, flush=True)
    print("t_last_two", t_last_two, "peak_max", peak_max, "wall", wall, flush=True)


if __name__ == "__main__":
    main()
