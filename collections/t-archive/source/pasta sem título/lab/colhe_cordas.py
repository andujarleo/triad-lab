#!/usr/bin/env python3
"""
Colheita de cordas — motor: solver.py (TriadParams / integrate_3d)
==================================================================
O motor é o SEU solver, importado como está: nenhum parâmetro
modificado, nenhuma calibração. TriadParams() nasce com os padrões
do seu arquivo; um campo só muda se VOCÊ exportar TRIAD_<CAMPO>
(ex.: TRIAD_N=256 TRIAD_T=40 TRIAD_SEED=3).

Colhe do estado final todas as cordas de densidade (topo 3% conexo,
componentes >= 8 voxels — critério do bravais_cordas.py) com as 14
características fixadas:
  morfológicas: size, elong, atoms, rho_mean, rho_max, vort
  espectrais:   b1..b8 (energia em 8 bandas fixas de |k|, normalizada)
Grava em cordas.csv (incremental por semente).

Coloque este arquivo na MESMA pasta do solver.py e rode:
  python3 colhe_cordas.py
  SEEDS=5 python3 colhe_cordas.py          (sementes 0..4 no mesmo CSV)
Depois:  python3 catalogo_cordas.py
"""
import os
import csv
import time
import dataclasses
import numpy as np
from scipy.ndimage import maximum_filter, label as cc_label

from solver import TriadParams, integrate_3d

SEEDS = int(os.environ.get("SEEDS", 1))
CSV = os.environ.get("CSV", "cordas.csv")


def params_do_ambiente(seed=None):
    """TriadParams puro; sobrescreve APENAS campos que você exportou."""
    kw = {}
    for f in dataclasses.fields(TriadParams):
        v = os.environ.get("TRIAD_" + f.name.upper())
        if v is None:
            continue
        d = f.default
        if isinstance(d, bool):
            kw[f.name] = v.lower() in ("1", "true", "sim")
        elif isinstance(d, int):
            kw[f.name] = int(v)
        elif isinstance(d, float):
            kw[f.name] = float(v)
        elif isinstance(d, tuple):
            kw[f.name] = tuple(float(x) for x in v.split(","))
        else:
            kw[f.name] = v
    if seed is not None and "seed" not in kw:
        kw["seed"] = seed
    return TriadParams(**kw)


# ---------------------------------------------------------------- colheita
def colhe(rho, psi_np, L, N, seed, writer):
    dx = L / N
    thr = np.percentile(rho, 97.0)
    lab, ncomp = cc_label(rho > thr)
    sizes = np.bincount(lab.ravel())
    mxf = maximum_filter(rho, size=5)
    atomos = np.argwhere((rho == mxf) & (rho > np.percentile(rho, 99.0)))
    lab_at = lab[atomos[:, 0], atomos[:, 1], atomos[:, 2]] if len(atomos) else []
    ph = np.angle(psi_np)
    wrapd = lambda d: (d + np.pi) % (2 * np.pi) - np.pi
    a_, b_, c_, d_ = ph[:-1, :-1, :], ph[1:, :-1, :], ph[1:, 1:, :], ph[:-1, 1:, :]
    w = wrapd(b_ - a_) + wrapd(c_ - b_) + wrapd(d_ - c_) + wrapd(a_ - d_)
    vor = np.zeros_like(rho, dtype=bool)
    iz = np.argwhere(np.abs(w) > np.pi)
    if len(iz):
        vor[iz[:, 0], iz[:, 1], iz[:, 2]] = True
    k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
    KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
    Kf = np.sqrt(KX**2 + KY**2 + KZ**2)
    BANDAS = np.linspace(0, np.pi / dx, 9)
    n_cordas = 0
    for cid in range(1, ncomp + 1):
        if sizes[cid] < 8:
            continue
        m = lab == cid
        idx = np.argwhere(m)
        w_ = rho[m]
        P = idx * dx
        Wt = w_ / w_.sum()
        mu = (P * Wt[:, None]).sum(0)
        C = ((P - mu) * Wt[:, None]).T @ (P - mu)
        ev = np.sort(np.linalg.eigvalsh(C))
        elong = float(np.sqrt(ev[2] / max(ev[0], 1e-12)))
        F = np.abs(np.fft.fftn(np.where(m, rho, 0.0))) ** 2
        F[0, 0, 0] = 0.0
        bands = np.array([F[(Kf >= BANDAS[i]) & (Kf < BANDAS[i + 1])].sum()
                          for i in range(8)])
        bands = bands / (bands.sum() + 1e-30)
        writer.writerow([seed, cid, int(sizes[cid]), round(elong, 4),
                         int(np.sum(lab_at == cid)) if len(atomos) else 0,
                         round(float(w_.mean()), 8), round(float(w_.max()), 8),
                         round(float(vor[m].mean()), 5)]
                        + [round(float(b), 6) for b in bands])
        n_cordas += 1
    return n_cordas


novo = not os.path.exists(CSV)
fcsv = open(CSV, "a", newline="")
wr = csv.writer(fcsv)
if novo:
    wr.writerow(["seed", "corda", "size", "elong", "atoms", "rho_mean",
                 "rho_max", "vort"] + ["b%d" % (i + 1) for i in range(8)])
ja = set()
if not novo:
    with open(CSV) as fh:
        ja = {int(r["seed"]) for r in csv.DictReader(fh)}

for seed in range(SEEDS):
    if seed in ja:
        print("semente %d já colhida, pulando" % seed)
        continue
    p = params_do_ambiente(seed=seed)
    print("semente %d | N=%d L=%.1f T=%.1f dt=%g init=%s (parâmetros do solver, intactos)"
          % (p.seed, p.N, p.L, p.T, p.dt, p.init))
    t0 = time.time()
    res = integrate_3d(p)
    psi = np.asarray(res["psi_final"])
    rho = np.abs(psi) ** 2
    n = colhe(rho, psi, p.L, p.N, p.seed, wr)
    fcsv.flush()
    print("semente %d | %d cordas | %.0fs" % (p.seed, n, time.time() - t0))
fcsv.close()
print("colheita completa -> %s" % CSV)
