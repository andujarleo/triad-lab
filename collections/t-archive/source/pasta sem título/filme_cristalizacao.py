#!/usr/bin/env python3
"""
Filme da cristalização
======================
Não roda a dinâmica — só lê os quadros salvos pelo simula_filmes.py
(bravais_outputs_3d/filmes_data.npz) e monta um GIF: o volume 3D da
densidade girando enquanto o tempo passa, com a fatia central e a curva
de ordem ao lado. Você vê o caos inicial se organizando em cristal.

Uso:  python3 filme_cristalizacao.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap
import imageio.v2 as imageio

path = "bravais_outputs_3d/filmes_data.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o simula_filmes.py antes" % path)
dat = np.load(path)
R = dat["rho"].astype(np.float32)          # (quadros, N, N, N)
tempos = dat["tempos"]
order = dat["order"]
L = float(dat["L"])
NF, N = R.shape[0], R.shape[1]
x = np.linspace(-L / 2, L / 2, N, endpoint=False)

cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"]
)
plt.rcParams["figure.facecolor"] = "#0b0e1a"

frames = []
vmax = np.percentile(R, 99.9)
for f in range(NF):
    rho = R[f]
    fig = plt.figure(figsize=(12, 5.2), facecolor="#0b0e1a")

    # ---- volume 3D: voxels do topo da densidade, girando
    ax = fig.add_subplot(1, 2, 1, projection="3d")
    ax.set_facecolor("#0b0e1a")
    thr = np.percentile(rho, 97.0)
    idx = np.argwhere(rho > thr)
    vals = rho[idx[:, 0], idx[:, 1], idx[:, 2]]
    pts = idx * (L / N) - L / 2
    o = np.argsort(vals)
    ax.scatter(pts[o, 0], pts[o, 1], pts[o, 2],
               c=vals[o], cmap=cmap_life, s=6 + 30 * (vals[o] / vmax) ** 2,
               alpha=0.55, linewidths=0)
    ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2)
    ax.set_zlim(-L / 2, L / 2)
    ax.view_init(elev=22, azim=(f * 360.0 / NF) - 60)
    ax.set_axis_off()
    ax.set_title("t = %d" % tempos[f], color="#e6e8f0", fontsize=13)

    # ---- fatia central
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.imshow(rho[:, :, N // 2].T, origin="lower", cmap=cmap_life,
               extent=[-L / 2, L / 2, -L / 2, L / 2], vmin=0, vmax=vmax)
    ax2.set_title("fatia z=0", color="#e6e8f0", fontsize=9)
    ax2.tick_params(colors="#8890a8", labelsize=6)
    for s in ax2.spines.values():
        s.set_color("#2a3050")

    # ---- curva de ordem com cursor
    ax3 = fig.add_subplot(2, 2, 4)
    ax3.set_facecolor("#11152a")
    ax3.plot(order, color="#5bc0be", lw=1.2)
    ax3.axvline(tempos[f], color="#ee6c4d", lw=1.5)
    ax3.set_title("energia de ordem (fora do k=0)", color="#e6e8f0", fontsize=9)
    ax3.tick_params(colors="#8890a8", labelsize=6)
    for s in ax3.spines.values():
        s.set_color("#2a3050")

    fig.suptitle("Cristalização — |Ψ|² pela equação completa (todos os termos juntos)",
                 color="#e6e8f0", fontsize=12)
    fig.tight_layout()
    fig.canvas.draw()
    img = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    frames.append(img)
    plt.close(fig)
    if f % 10 == 0:
        print("quadro %d/%d" % (f + 1, NF))

# congela o último quadro um pouco no fim
frames += [frames[-1]] * 8
imageio.mimsave("bravais_outputs_3d/filme_cristalizacao.gif", frames,
                duration=0.12, loop=0)
print("salvo: bravais_outputs_3d/filme_cristalizacao.gif  (%d quadros)" % NF)
