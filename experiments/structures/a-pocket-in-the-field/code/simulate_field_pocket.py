#!/usr/bin/env python3
"""Run 37 — bolso no universo (identidade / observador).

Theta_core intocado. Tríade inteira. Sem campo C.
1 gaussiana = 1 átomo. Volume preenchido = universo.
Pergunta: um gaussiano plantado DEPOIS do cubo encher continua alguém?
"""
from __future__ import annotations

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
FONTES = VAULT / "Fontes"
ARTEFATOS = VAULT / "Artefatos" / "triad_bolso_37"
NOTA_PATH = VAULT / "Simulações" / "37 bolso_no_universo.md"
INDEX_PATH = VAULT / "Simulações" / "Índice de runs.md"
TRIAD_MD = VAULT / "TRIAD.md"

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
LBOX = 32.0
NGRID = 64
DT = 0.0025
T_PLANT = 0.5
T_FINAL = 2.0
SEED = 0
INIT_SIGMA = 0.5
PLANT_CENTER = (8.0, 0.0, 0.0)
WINDOW_R = 4.0
Y0 = 0.0
RECORD_EVERY = 2
PRECISION = "complex64"
DTYPE_PSI_NP = np.complex64
DTYPE_R_NP = np.float32
PR_FILL = 500.0
RRMS_FILL = 10.0
CONTRAST_ALIVE = 2.0
DCOM_ALIVE = 2.0
NCELLS_ALIVE = 200
CONTRAST_DEAD = 1.5
DCOM_DEAD = 4.0

BACKEND = "mlx"
MLX_OK = False
mx = None
try:
    import mlx.core as mx

    MLX_OK = True
    BACKEND = "mlx"
except Exception as exc:
    MLX_OK = False
    BACKEND = "numpy"
    print("mlx_import_failed", exc, "fallback numpy", flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


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
        return v if math.isfinite(v) else None
    if isinstance(obj, (np.ndarray, list, tuple)):
        return [jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): jsonable(v) for k, v in obj.items()}
    if isinstance(obj, Path):
        return str(obj)
    return obj


def min_image(d, box):
    return d - box * np.round(d / box)


def l2_norm(psi, dV):
    return float(np.sqrt(np.sum(np.abs(psi) ** 2) * dV))


def gaussian_atom(X, Y, Z, center, s, dV):
    dx = min_image(X - center[0], LBOX)
    dy = min_image(Y - center[1], LBOX)
    dz = min_image(Z - center[2], LBOX)
    rr2 = dx * dx + dy * dy + dz * dz
    psi = np.exp(-rr2 / (2.0 * s * s)).astype(np.complex128)
    nrm = np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    return psi / nrm


def mul_phase_mlx(psi, theta):
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


def strang_step_np(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((len(NU), 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    theta = V_tot * (DT / HBAR)
    c = np.cos(theta)
    s = np.sin(theta)
    re = np.real(psi)
    im = np.imag(psi)
    psi = ((re * c + im * s) + 1j * (im * c - re * s)).astype(np.complex64, copy=False)
    y = y + DT * nu.reshape((len(NU), 1, 1, 1)) * (rho - y)
    y = y.astype(np.float32, copy=False)
    if noise_amp > 0.0:
        xi_np = (
            (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2.0)
        ).astype(np.complex64, copy=False)
        psi = psi + np.complex64(noise_amp) * xi_np
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin).astype(np.complex64, copy=False)
    return psi, y


def corr_xy(a, b, mask):
    aa = a[mask].ravel().astype(np.float64)
    bb = b[mask].ravel().astype(np.float64)
    if aa.size < 8:
        return float("nan")
    aa = aa - aa.mean()
    bb = bb - bb.mean()
    den = float(np.sqrt((aa * aa).sum() * (bb * bb).sum()))
    if den <= 0:
        return float("nan")
    return float((aa * bb).sum() / den)


def window_metrics(rho, y0, X, Y, Z, dV, dx):
    dxw = min_image(X - PLANT_CENTER[0], LBOX)
    dyw = min_image(Y - PLANT_CENTER[1], LBOX)
    dzw = min_image(Z - PLANT_CENTER[2], LBOX)
    rr = np.sqrt(dxw * dxw + dyw * dyw + dzw * dzw)
    inside = rr <= WINDOW_R
    outside = ~inside
    mass_w = float(rho[inside].sum() * dV)
    mass_out = float(rho[outside].sum() * dV)
    if inside.any():
        peak_w = float(rho[inside].max())
        n_cells_w = int((rho[inside] >= 0.5 * peak_w).sum()) if peak_w > 0 else 0
        wsum = float(rho[inside].sum())
        if wsum > 0:
            cx = float((rho[inside] * X[inside]).sum() / wsum)
            cy = float((rho[inside] * Y[inside]).sum() / wsum)
            cz = float((rho[inside] * Z[inside]).sum() / wsum)
            dvec = min_image(
                np.array([cx, cy, cz]) - np.array(PLANT_CENTER), LBOX
            )
            d_com = float(np.linalg.norm(dvec))
        else:
            cx = cy = cz = d_com = float("nan")
    else:
        peak_w = 0.0
        n_cells_w = 0
        cx = cy = cz = d_com = float("nan")
    med_out = float(np.median(rho[outside])) if outside.any() else 0.0
    contrast = peak_w / max(med_out, 1e-12)
    y_corr_w = corr_xy(y0, rho, inside)
    y_corr_out = corr_xy(y0, rho, outside)
    return {
        "mass_w": mass_w,
        "mass_out": mass_out,
        "peak_w": peak_w,
        "n_cells_w": n_cells_w,
        "com_x": cx,
        "com_y": cy,
        "com_z": cz,
        "d_com": d_com,
        "median_out": med_out,
        "contrast": contrast,
        "y_corr_w": y_corr_w,
        "y_corr_out": y_corr_out,
    }


def global_metrics(psi, y, t, dV, r2):
    rho = np.abs(psi) ** 2
    finite = bool(np.isfinite(rho).all() and np.isfinite(y).all())
    if not finite:
        return rho, {
            "t": t,
            "norm": float("nan"),
            "peak": float("nan"),
            "PR": float("nan"),
            "R_rms": float("nan"),
            "finite": False,
        }
    norm = float(rho.sum() * dV)
    peak = float(rho.max())
    pr = float((norm * norm) / max(float((rho ** 2).sum() * dV), 1e-300))
    rrms = float(np.sqrt((rho * r2).sum() * dV / max(norm, 1e-300)))
    return rho, {
        "t": t,
        "norm": norm,
        "peak": peak,
        "PR": pr,
        "R_rms": rrms,
        "finite": True,
    }


def alive_flag(rec, planted):
    if not planted or not rec.get("finite"):
        return None
    return bool(
        rec["contrast"] > CONTRAST_ALIVE
        and rec["d_com"] < DCOM_ALIVE
        and rec["n_cells_w"] <= NCELLS_ALIVE
    )


def dead_flag(rec, planted):
    if not planted or not rec.get("finite"):
        return False
    dcom = rec.get("d_com")
    dcom = float("inf") if dcom is None or not np.isfinite(dcom) else float(dcom)
    return bool(
        rec["contrast"] < CONTRAST_DEAD
        or dcom > DCOM_DEAD
        or rec["n_cells_w"] > NCELLS_ALIVE
    )


def build_grid():
    N = NGRID
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False, dtype=np.float64)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    kvec = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(kvec, kvec, kvec, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k_mag = np.sqrt(k2)
    H_lin = (HBAR * HBAR * k2) / (2.0 * M_MASS)
    if ALPHA != 0.0:
        H_lin = H_lin + ALPHA * np.power(k_mag, SIGMA_FRAC)
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    g0 = gaussian_atom(X, Y, Z, (0.0, 0.0, 0.0), INIT_SIGMA, dV)
    gplant = gaussian_atom(X, Y, Z, PLANT_CENTER, INIT_SIGMA, dV)
    return {
        "X": X,
        "Y": Y,
        "Z": Z,
        "dx": dx,
        "dV": dV,
        "r2": r2,
        "half_lin": half_lin.astype(DTYPE_PSI_NP),
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
        "psi0": g0.astype(DTYPE_PSI_NP),
        "gplant": gplant.astype(DTYPE_PSI_NP),
        "y0": np.full((len(NU), N, N, N), Y0, dtype=DTYPE_R_NP),
        "shape": (N, N, N),
        "norm_seed": l2_norm(g0, dV),
        "norm_plant": l2_norm(gplant, dV),
    }


def plot_series(rows, outdir):
    t = np.array([r["t"] for r in rows], dtype=np.float64)
    fig, ax = plt.subplots(2, 2, figsize=(10, 7))
    ax[0, 0].plot(t, [r["peak"] for r in rows], label="peak global")
    ax[0, 0].plot(t, [r["peak_w"] for r in rows], label="peak janela")
    ax[0, 0].axvline(T_PLANT, color="k", ls="--", lw=0.8)
    ax[0, 0].set_yscale("log")
    ax[0, 0].legend()
    ax[0, 0].set_title("pico")
    ax[0, 1].plot(t, [r["contrast"] for r in rows])
    ax[0, 1].axvline(T_PLANT, color="k", ls="--", lw=0.8)
    ax[0, 1].axhline(CONTRAST_ALIVE, color="g", ls=":", lw=0.8)
    ax[0, 1].set_title("contraste")
    ax[1, 0].plot(t, [r["d_com"] for r in rows])
    ax[1, 0].axvline(T_PLANT, color="k", ls="--", lw=0.8)
    ax[1, 0].set_title("d_com")
    ax[1, 1].plot(t, [r["y_corr_w"] for r in rows], label="y–ρ janela")
    ax[1, 1].plot(t, [r["y_corr_out"] for r in rows], label="y–ρ fora")
    ax[1, 1].axvline(T_PLANT, color="k", ls="--", lw=0.8)
    ax[1, 1].legend()
    ax[1, 1].set_title("memória")
    for a in ax.ravel():
        a.set_xlabel("t")
    fig.tight_layout()
    fig.savefig(outdir / "identidade_vs_t.png", dpi=140)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, [r["PR"] for r in rows])
    ax.axvline(T_PLANT, color="k", ls="--", lw=0.8)
    ax.set_xlabel("t")
    ax.set_ylabel("PR")
    fig.tight_layout()
    fig.savefig(outdir / "PR_vs_t.png", dpi=140)
    plt.close(fig)


def write_note(summary, arte):
    s = summary
    note = f"""---
tags: [triad, simulação, consciência, identidade, I0]
aliases: [bolso_no_universo, triad_bolso_37, run37]
classe: Theta_core I0, universo cheio + bolso plantado
diretório: triad_bolso_37
status: I0 / identidade / observador
run: 37
data: 2026-08-21
---

# bolso_no_universo

Equação TRIAD **completa**, Theta_core. **Não** é campo C. **Não** é Q05. 1 gaussiana = 1 [[átomo]] = o bolso. Volume preenchido = universo. Pergunta: o cubo já cheio segura um alguém plantado depois, ou come?

Previsões (antes): `Fontes/predictions_37.md`. Protocolo: `Fontes/PROTOCOL_37.md`.

Solver: mesmo passo Strang de Q02/35 (`ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365` no ancestral). Backend **{s['backend']}** `{s['device']}`. seed=0. L=32 N=64 dt=0.0025 T=2 t_plant=0.5. Planta: +1 gaussiana norma 1 em (8,0,0).

Não substitui [[32 universo_atomo]] · [[35 singularidade_finita]] · [[08 triad_observer_observed_consciousness]].

## Previsão (antes)

t_fill ≪ 0.5. Blob no plantio. t_gone − t_plant ≲ 0.05. Identidade FAIL. Plantar depois não salva o átomo.

## Resultado

Wall **{s['wall_s']:.3f} s** ({s['t_start']} – {s['t_end']}). finite={s['finite_all']}.

- t_fill = **{s['t_fill']}** (PR≥500 ou R_rms≥10)
- t_plant = **{T_PLANT}**
- contraste logo após plantio = **{s['contrast_plant']}**
- peak_w logo após plantio = **{s['peak_w_plant']}**
- mass_w logo após plantio = **{s['mass_w_plant']}**
- t_gone = **{s['t_gone']}**
- Δt_identidade = **{s['dt_identity']}**
- late t=2: norm={s['late_norm']} peak={s['late_peak']} PR={s['late_PR']} contrast={s['late_contrast']} d_com={s['late_d_com']} y_corr_w={s['late_y_corr_w']} y_corr_out={s['late_y_corr_out']}
- veredito: **{s['verdict']}**

![[Artefatos/triad_bolso_37/identidade_vs_t.png]]

![[Artefatos/triad_bolso_37/mid_pre_plant.png]]

![[Artefatos/triad_bolso_37/mid_post_plant.png]]

![[Artefatos/triad_bolso_37/mid_end.png]]

## Leitura

{s['reading']}

Voltar: [[TRIAD]] · [[Índice de runs]] · [[Leitura operacional]] · [[Observador e campo C]]
"""
    NOTA_PATH.write_text(note, encoding="utf-8")


def patch_index(summary):
    row = (
        f"| 37 | [[37 bolso_no_universo|triad_bolso_37]] | Theta_core I0, universo cheio + bolso, N=64 T=2, 21/08/2026 | identidade | "
        f"t_fill={summary['t_fill']} t_gone={summary['t_gone']} Δt={summary['dt_identity']} {summary['verdict']} |\n"
    )
    it = INDEX_PATH.read_text(encoding="utf-8")
    if "37 bolso_no_universo" not in it:
        lines = it.splitlines(True)
        last = max(i for i, l in enumerate(lines) if l.startswith("| 36 "))
        lines.insert(last + 1, row)
        INDEX_PATH.write_text("".join(lines), encoding="utf-8")
    t = TRIAD_MD.read_text(encoding="utf-8")
    blob = (
        "\n**37 bolso_no_universo** (2026-08-21): universo cheio + 1 gaussiano plantado. "
        f"t_fill={summary['t_fill']}, t_gone={summary['t_gone']}, {summary['verdict']}. "
        "Sem campo C. Ver [[37 bolso_no_universo]].\n"
    )
    if "37 bolso_no_universo" not in t:
        needle = "[[00 registro_completo]]."
        if needle in t:
            t = t.replace(needle, needle + blob, 1)
        else:
            t = t.rstrip() + blob
        TRIAD_MD.write_text(t, encoding="utf-8")


def midplane(psi):
    N = psi.shape[0]
    return np.abs(np.asarray(psi)[:, :, N // 2]) ** 2


def save_mid(rho2, path, title):
    fig, ax = plt.subplots(figsize=(5, 4))
    im = ax.imshow(np.log10(np.maximum(rho2.T, 1e-12)), origin="lower", cmap="magma")
    ax.set_title(title)
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)


def main():
    t_start = now_sp()
    t_wall0 = time.perf_counter()
    ARTEFATOS.mkdir(parents=True, exist_ok=True)
    grid = build_grid()
    dx, dV, r2 = grid["dx"], grid["dV"], grid["r2"]
    X, Y, Z = grid["X"], grid["Y"], grid["Z"]
    noise_amp = grid["noise_amp"]
    shape = grid["shape"]
    n_steps = int(round(T_FINAL / DT))
    plant_step = int(round(T_PLANT / DT))
    rng = np.random.default_rng(SEED)
    nu_np = np.asarray(NU, dtype=np.float32)
    lam_np = np.asarray(LAM, dtype=np.float32)
    backend = BACKEND
    if backend == "mlx":
        half_lin = mx.array(grid["half_lin"])
        nu = mx.array(nu_np)
        lam = mx.array(lam_np)
        psi = mx.array(grid["psi0"])
        y = mx.array(grid["y0"])
        gplant = mx.array(grid["gplant"])
        mx.eval(psi, y, half_lin, nu, lam, gplant)
        step_fn = strang_step_mlx
        device = str(mx.default_device())
    else:
        half_lin = grid["half_lin"]
        nu = nu_np
        lam = lam_np
        psi = grid["psi0"].copy()
        y = grid["y0"].copy()
        gplant = grid["gplant"]
        step_fn = strang_step_np
        device = "cpu"

    print(
        f"=== 37 bolso backend={backend} device={device} N={NGRID} T={T_FINAL} plant={T_PLANT} ===",
        flush=True,
    )
    print(
        f"f_FDT={grid['f_FDT']} noise_amp={noise_amp} norm_seed={grid['norm_seed']} norm_plant={grid['norm_plant']}",
        flush=True,
    )

    rows = []
    t_fill = None
    t_gone = None
    planted = False
    finite_all = True
    mid_pre = mid_post = mid_end = None
    rec_plant = None

    for step in range(n_steps + 1):
        t = step * DT
        if (not planted) and step == plant_step:
            if backend == "mlx":
                mid_pre = midplane(psi)
                psi = psi + gplant
                mx.eval(psi)
            else:
                mid_pre = midplane(psi)
                psi = (psi + gplant).astype(np.complex64, copy=False)
            planted = True
            print(f"PLANTED t={t}", flush=True)

        if step % RECORD_EVERY == 0 or step == n_steps or step == plant_step:
            if backend == "mlx":
                psi_np = np.array(psi)
                y_np = np.array(y)
            else:
                psi_np = np.asarray(psi)
                y_np = np.asarray(y)
            rho, rec = global_metrics(psi_np, y_np, t, dV, r2)
            rec.update(window_metrics(rho, y_np[0], X, Y, Z, dV, dx))
            rec["planted"] = planted
            rec["alive"] = alive_flag(rec, planted)
            rec["backend"] = backend
            rows.append(rec)
            if rec["finite"] and t_fill is None:
                if rec["PR"] >= PR_FILL or rec["R_rms"] >= RRMS_FILL:
                    t_fill = float(t)
                    print(f"FILL t={t} PR={rec['PR']} Rrms={rec['R_rms']}", flush=True)
            if planted and rec_plant is None:
                rec_plant = rec
                mid_post = np.abs(psi_np[:, :, NGRID // 2]) ** 2
            if planted and t_gone is None and dead_flag(rec, True) and t > T_PLANT + 1e-12:
                t_gone = float(t)
                print(f"GONE t={t} contrast={rec['contrast']} d_com={rec['d_com']}", flush=True)
            if not rec["finite"]:
                finite_all = False
                print("NAN", t, flush=True)
                break
            if step % 80 == 0 or step == plant_step:
                print(
                    f"t={t:.4f} planted={planted} norm={rec['norm']:.4e} peak={rec['peak']:.4e} "
                    f"PR={rec['PR']:.4e} contrast={rec['contrast']:.4g} d_com={rec['d_com']} "
                    f"alive={rec['alive']}",
                    flush=True,
                )
        if step == n_steps:
            if backend == "mlx":
                mid_end = midplane(psi)
            else:
                mid_end = midplane(psi)
            break
        psi, y = step_fn(psi, y, half_lin, noise_amp, rng, nu, lam, shape)

    wall = time.perf_counter() - t_wall0
    t_end = now_sp()
    last = rows[-1]
    dt_id = None if t_gone is None else (t_gone - T_PLANT)
    if t_gone is None and planted and last.get("alive"):
        verdict = "PARTIAL identidade (ainda vivo em T=2)"
        reading = "O bolso ainda passava o critério no fim da janela. Surpresa em relação à previsão. Sem retocar λ. Não promove a consciência."
    elif t_gone is not None and dt_id is not None and dt_id <= 0.05:
        verdict = "FAIL identidade"
        reading = "O universo comeu o bolso na mesma ordem de tempo dos runs 30–35. Plantar depois de encher não criou um alguém. Consciência, neste regime, ainda não tem suporte: não há identidade que dure no cubo preenchido."
    elif t_gone is not None:
        verdict = "PARTIAL identidade (durou mais que 0.05 e depois morreu)"
        reading = "O bolso durou mais que a previsão curta, depois dissolveu. Ainda não é um observador. É um tempo de vida. Sem promover a mente."
    else:
        verdict = "INCONCLUSIVE"
        reading = "Critério não fechou. Ver CSV."

    summary = {
        "run": 37,
        "backend": backend,
        "device": device,
        "wall_s": wall,
        "t_start": t_start,
        "t_end": t_end,
        "finite_all": finite_all,
        "t_fill": t_fill,
        "t_plant": T_PLANT,
        "t_gone": t_gone,
        "dt_identity": dt_id,
        "contrast_plant": None if rec_plant is None else rec_plant.get("contrast"),
        "peak_w_plant": None if rec_plant is None else rec_plant.get("peak_w"),
        "mass_w_plant": None if rec_plant is None else rec_plant.get("mass_w"),
        "late_norm": last.get("norm"),
        "late_peak": last.get("peak"),
        "late_PR": last.get("PR"),
        "late_contrast": last.get("contrast"),
        "late_d_com": last.get("d_com"),
        "late_y_corr_w": last.get("y_corr_w"),
        "late_y_corr_out": last.get("y_corr_out"),
        "verdict": verdict,
        "reading": reading,
        "Theta_core": {
            "Lambda": LAMBDA,
            "alpha": ALPHA,
            "sigma": SIGMA_FRAC,
            "Gamma": GAMMA,
            "nu": NU,
            "lambda": LAM,
            "fdt_couple": FDT_COUPLE,
            "kT": KT,
        },
        "script_sha256": sha256_file(Path(__file__)),
        "n_records": len(rows),
    }
    fields = list(rows[0].keys()) if rows else []
    with (ARTEFATOS / "metrics.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    (ARTEFATOS / "summary.json").write_text(
        json.dumps(jsonable(summary), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    plot_series(rows, ARTEFATOS)
    if mid_pre is not None:
        save_mid(mid_pre, ARTEFATOS / "mid_pre_plant.png", f"pre-plant t={T_PLANT}")
    if mid_post is not None:
        save_mid(mid_post, ARTEFATOS / "mid_post_plant.png", f"post-plant t={T_PLANT}")
    if mid_end is not None:
        save_mid(mid_end, ARTEFATOS / "mid_end.png", f"t={T_FINAL}")
    write_note(summary, ARTEFATOS)
    patch_index(summary)
    print("SUMMARY", json.dumps(jsonable(summary), ensure_ascii=False), flush=True)
    print("wrote", ARTEFATOS, NOTA_PATH, flush=True)


if __name__ == "__main__":
    main()
