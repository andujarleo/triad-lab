#!/usr/bin/env python3
"""
Nebulosa volumétrica
====================
Não roda a dinâmica — lê o último quadro (ou o final_state.npz) e faz um
render volumétrico de emissão: a densidade |Ψ|² desenhada como gás
luminoso translúcido, tipo foto de telescópio. Ray-marching simples:
gira o volume, integra luz ao longo do olhar com absorção.

Uso:
  python3 nebulosa.py            (imagem parada em 3 ângulos, alta resolução)
  GIRAR=1 python3 nebulosa.py    (+ GIF girando 360°)
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import imageio.v2 as imageio
from scipy.ndimage import map_coordinates, gaussian_filter, zoom

if os.path.exists("bravais_outputs_3d/filmes_data.npz"):
    dat = np.load("bravais_outputs_3d/filmes_data.npz")
    rho = dat["rho"][-1].astype(np.float32)
elif os.path.exists("bravais_outputs_3d/final_state.npz"):
    rho = np.load("bravais_outputs_3d/final_state.npz")["rho_f"].astype(np.float32)
else:
    raise SystemExit("rode o simula_filmes.py (ou bravais_puro_3d.py) antes")

N = rho.shape[0]
rho = gaussian_filter(rho, 0.8)            # só suaviza o serrilhado do voxel
alvo = int(os.environ.get("RES", 128))     # resolução do render
if N < alvo:
    rho = zoom(rho, alvo / N, order=3)     # upsample suave (visual apenas)
rho = rho / np.percentile(rho, 99.8)

# paleta de emissão: escuro → azul frio → ciano → dourado → branco quente
stops = np.array([
    [0.00, 0.02, 0.03, 0.08],
    [0.25, 0.05, 0.10, 0.35],
    [0.50, 0.10, 0.55, 0.65],
    [0.75, 0.95, 0.75, 0.30],
    [1.00, 1.00, 0.98, 0.92],
])


def transfer(d):
    d = np.clip(d, 0, 1)
    r = np.interp(d, stops[:, 0], stops[:, 1])
    g = np.interp(d, stops[:, 0], stops[:, 2])
    b = np.interp(d, stops[:, 0], stops[:, 3])
    return np.stack([r, g, b], axis=-1)


def rotate_volume(vol, az, el):
    """Amostra o volume numa grade girada (graus)."""
    c = (np.array(vol.shape) - 1) / 2.0
    az, el = np.radians(az), np.radians(el)
    Rz = np.array([[np.cos(az), -np.sin(az), 0],
                   [np.sin(az), np.cos(az), 0], [0, 0, 1]])
    Ry = np.array([[np.cos(el), 0, np.sin(el)], [0, 1, 0],
                   [-np.sin(el), 0, np.cos(el)]])
    Rm = Ry @ Rz
    idx = np.indices(vol.shape).reshape(3, -1).T - c
    src = (idx @ Rm.T) + c
    out = map_coordinates(vol, src.T, order=1, mode="grid-wrap")
    return out.reshape(vol.shape)


def render(vol, az=30, el=20, gain=2.2, absorb=3.0):
    """Emissão + absorção ao longo do eixo z do volume girado."""
    v = rotate_volume(vol, az, el)
    img = np.zeros(v.shape[:2] + (3,))
    T = np.ones(v.shape[:2])               # transmitância acumulada
    for k in range(v.shape[2]):
        sl = np.clip(v[:, :, k], 0, 1.5)
        emit = transfer(sl) * (sl[..., None] ** 1.5) * gain / v.shape[2]
        img += T[..., None] * emit * v.shape[2] * 0.04
        T *= np.exp(-absorb * sl / v.shape[2])
    img = 1.0 - np.exp(-img * 3.0)         # tone-map suave
    return np.clip(img, 0, 1)


os.makedirs("bravais_outputs_3d", exist_ok=True)

# ---- imagem parada: 3 ângulos
fig, axes = plt.subplots(1, 3, figsize=(16, 5.6), facecolor="black")
for ax, (az, el, nome) in zip(axes, [(25, 15, "diagonal"),
                                     (115, 15, "diagonal oposta"),
                                     (0, 88, "de cima")]):
    print("renderizando %s..." % nome)
    ax.imshow(render(rho, az, el))
    ax.set_axis_off()
    ax.set_title(nome, color="#c8cce0", fontsize=11)
fig.suptitle("Nebulosa — |Ψ|² como gás luminoso (emissão + absorção)",
             color="#e6e8f0", fontsize=14)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/nebulosa.png", dpi=170,
            bbox_inches="tight", facecolor="black")
plt.close()
print("salvo: bravais_outputs_3d/nebulosa.png")

# ---- GIF girando (opcional)
if os.environ.get("GIRAR"):
    frames = []
    nA = 36
    for i in range(nA):
        frames.append((render(rho, az=i * 360.0 / nA, el=18) * 255).astype(np.uint8))
        if i % 6 == 0:
            print("giro %d/%d" % (i + 1, nA))
    imageio.mimsave("bravais_outputs_3d/nebulosa_girando.gif", frames,
                    duration=0.12, loop=0)
    print("salvo: bravais_outputs_3d/nebulosa_girando.gif")
