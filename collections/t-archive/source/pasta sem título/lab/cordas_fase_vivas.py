#!/usr/bin/env python3
"""
Cordas de fase vivas
====================
Não roda a dinâmica — lê os quadros de FASE salvos pelo simula_filmes.py
e desenha, quadro a quadro, as linhas onde a fase de Ψ dá uma volta
completa (2π): os vórtices. Estilo neon sobre fundo escuro, câmera
girando. Você vê as cordas nascendo, serpenteando, se reconectando e
morrendo conforme a rede cristaliza.

Uso:  python3 cordas_fase_vivas.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import imageio.v2 as imageio

path = "bravais_outputs_3d/filmes_data.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o simula_filmes.py antes" % path)
dat = np.load(path)
PH = dat["fase"].astype(np.float32)
RH = dat["rho"].astype(np.float32)
tempos = dat["tempos"]
# filtro de VISUALIZAÇÃO: mostra só vórtices em região com densidade
# relevante (acima do percentil FILTRO), senão o ruído do vácuo soterra
# as cordas. Não muda nada da física — só o que aparece na tela.
FILTRO = float(os.environ.get("FILTRO", 75.0))
L = float(dat["L"])
NF, N = PH.shape[0], PH.shape[1]
dx = L / N


def wrap(d):
    return (d + np.pi) % (2 * np.pi) - np.pi


def vortex_points(ph):
    """Atravessamentos de plaqueta (3 orientações), vetorizado."""
    pts = []
    # plano xy
    a = ph[:-1, :-1, :]; b = ph[1:, :-1, :]; c = ph[1:, 1:, :]; d = ph[:-1, 1:, :]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i + 0.5, j + 0.5, k, np.sign(w[i, j, k])))
    # plano xz
    a = ph[:-1, :, :-1]; b = ph[1:, :, :-1]; c = ph[1:, :, 1:]; d = ph[:-1, :, 1:]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i + 0.5, j, k + 0.5, np.sign(w[i, j, k])))
    # plano yz
    a = ph[:, :-1, :-1]; b = ph[:, 1:, :-1]; c = ph[:, 1:, 1:]; d = ph[:, :-1, 1:]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i, j + 0.5, k + 0.5, np.sign(w[i, j, k])))
    return np.array(pts) if pts else np.zeros((0, 4))


frames = []
n_hist = []
for f in range(NF):
    vp = vortex_points(PH[f])
    if len(vp):
        thr = np.percentile(RH[f], FILTRO)
        ii = np.clip(np.round(vp[:, :3]).astype(int), 0, N - 1)
        dens = RH[f][ii[:, 0], ii[:, 1], ii[:, 2]]
        vp = vp[dens > thr]
    n_hist.append(len(vp))
    fig = plt.figure(figsize=(9, 8), facecolor="#05060f")
    ax = fig.add_subplot(111, projection="3d")
    ax.set_facecolor("#05060f")
    if len(vp):
        xyz = vp[:, :3] * dx - L / 2
        pos = vp[:, 3] > 0
        # efeito neon: camada de brilho larga + núcleo pequeno
        for m, cor in ((pos, "#ff5e78"), (~pos, "#43e6e0")):
            ax.scatter(xyz[m, 0], xyz[m, 1], xyz[m, 2], s=40, color=cor,
                       alpha=0.06, linewidths=0)
            ax.scatter(xyz[m, 0], xyz[m, 1], xyz[m, 2], s=3, color=cor,
                       alpha=0.85, linewidths=0)
    ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2)
    ax.set_zlim(-L / 2, L / 2)
    ax.view_init(elev=18, azim=(f * 360.0 / NF) - 45)
    ax.set_axis_off()
    ax.set_title("cordas de fase — t = %d   (%d vórtices em região densa)\n"
                 "rosa: volta +2π   ciano: volta −2π" % (tempos[f], len(vp)),
                 color="#c8cce0", fontsize=11)
    fig.tight_layout()
    fig.canvas.draw()
    frames.append(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
    if f % 10 == 0:
        print("quadro %d/%d  (%d vórtices)" % (f + 1, NF, len(vp)))

frames += [frames[-1]] * 8
imageio.mimsave("bravais_outputs_3d/cordas_fase_vivas.gif", frames,
                duration=0.12, loop=0)
print("salvo: bravais_outputs_3d/cordas_fase_vivas.gif")
print("vórtices por quadro: início=%d  fim=%d  pico=%d"
      % (n_hist[0], n_hist[-1], max(n_hist)))
