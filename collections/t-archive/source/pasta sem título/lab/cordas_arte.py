#!/usr/bin/env python3
"""
Cordas-arte — variações no estilo do cordas_notas.png
=====================================================
Não roda a dinâmica — lê o estado salvo (final_state.npz e, se existir,
filmes_data.npz) e desenha quatro peças no mesmo estilo "fios no espaço":

  1. CORDAS VIBRANDO (GIF) — a mesma estrela de cordas-nota, mas viva:
     cada corda oscila na sua própria frequência (mais aguda = vibra
     mais rápido), com a câmera girando devagar.

  2. HARPA ESPECTRAL — as notas organizadas como harpa: cordas paralelas
     ordenadas por |k|, comprimento = comprimento de onda, cada uma
     desenhada vibrando com sua amplitude. O instrumento inteiro à vista.

  3. TEIA DE PICOS — os picos da rede cristalina ligados aos vizinhos
     por fios curvos que ondulam: a rede de Bravais como teia tecida.

  4. RIOS DE FASE — linhas de fluxo do gradiente da fase de Ψ: os
     "rios" por onde a fase escorre, desenhados como fios finos.
     (pulado com aviso se o npz não tiver psi_f)

Uso:  python3 cordas_arte.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap
import imageio.v2 as imageio

path = "bravais_outputs_3d/final_state.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode a simulação antes" % path)
dat = np.load(path)
rho = dat["rho_f"].astype(np.float32)
psi = dat["psi_f"] if "psi_f" in dat.files else None
N = rho.shape[0]
L = float(os.environ.get("L", 32.0))
dx = L / N
os.makedirs("bravais_outputs_3d", exist_ok=True)

cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"]
)

# ---------------------------------------------------------------- notas (como no bravais_cordas.py)
fft3 = np.fft.fftshift(np.abs(np.fft.fftn(rho)))
power = fft3**2
power[N // 2, N // 2, N // 2] = 0.0
flat = np.argsort(power.ravel())[::-1]
n_notes = 40
seen, notes = set(), []
for fi in flat:
    ijk = np.unravel_index(fi, power.shape)
    kvec = (np.array(ijk) - N // 2) * (2 * np.pi / L)
    key = tuple(np.round(np.abs(kvec), 6))
    if key in seen:
        continue
    seen.add(key)
    notes.append((kvec, power[ijk]))
    if len(notes) >= n_notes:
        break
pmax = notes[0][1]


def base_perp(u):
    ref = np.array([0.0, 0.0, 1.0]) if abs(u[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    w1 = np.cross(u, ref); w1 /= np.linalg.norm(w1)
    w2 = np.cross(u, w1)
    return w1, w2


# ================================================================ 1) CORDAS VIBRANDO
print("1) cordas vibrando...")
s = np.linspace(-L / 2, L / 2, 200)
NFR = 40
frames = []
for f in range(NFR):
    fase_t = 2 * np.pi * f / NFR
    fig = plt.figure(figsize=(9, 8.4))
    ax = fig.add_subplot(111, projection="3d")
    for ni, (kvec, pw) in enumerate(notes):
        kn = np.linalg.norm(kvec)
        if kn < 1e-9:
            continue
        u = kvec / kn
        w1, w2 = base_perp(u)
        amp = 1.8 * (pw / pmax) ** 0.5
        # vibra na sua frequência: notas agudas (|k| alto) oscilam mais rápido
        osc = np.sin(kn * s + fase_t * (1 + 2 * kn * L / (2 * np.pi) / 6))
        bal = np.cos(fase_t * (1 + kn))     # balança entre os dois planos
        line = (np.outer(s, u)
                + np.outer(amp * osc * bal, w1)
                + np.outer(amp * osc * (1 - abs(bal)) * 0.6, w2))
        inside = np.all(np.abs(line) <= L / 2, axis=1)
        col = cmap_life(0.15 + 0.8 * ni / (n_notes - 1))
        ax.plot(line[inside, 0], line[inside, 1], line[inside, 2],
                color=col, lw=1.0 + 2.5 * pw / pmax, alpha=0.8)
    ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2)
    ax.set_zlim(-L / 2, L / 2)
    ax.view_init(elev=20, azim=f * 360.0 / NFR - 60)
    ax.set_axis_off()
    ax.set_title("cordas-nota vibrando — cada uma na sua frequência",
                 fontsize=12)
    fig.tight_layout()
    fig.canvas.draw()
    frames.append(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
imageio.mimsave("bravais_outputs_3d/cordas_vibrando.gif", frames,
                duration=0.09, loop=0)
print("   cordas_vibrando.gif")

# ================================================================ 2) HARPA ESPECTRAL
print("2) harpa espectral...")
fig = plt.figure(figsize=(13, 9))
ax = fig.add_subplot(111, projection="3d")
ordk = sorted(notes, key=lambda nk: np.linalg.norm(nk[0]))
nh = len(ordk)
for ni, (kvec, pw) in enumerate(ordk):
    kn = np.linalg.norm(kvec)
    if kn < 1e-9:
        continue
    lam = 2 * np.pi / kn
    xpos = -L / 2 + L * ni / (nh - 1)          # posição na harpa
    comp = min(lam * 2.2, L * 0.9)             # comprimento da corda
    t = np.linspace(-comp / 2, comp / 2, 160)
    amp = 2.2 * (pw / pmax) ** 0.5
    vib = amp * np.sin(np.pi * (t / comp + 0.5)) * np.sin(kn * t * 2)
    col = cmap_life(0.12 + 0.82 * ni / (nh - 1))
    ax.plot(np.full_like(t, xpos), vib, t,
            color=col, lw=1.0 + 3.0 * pw / pmax, alpha=0.85)
    # sombra no chão da harpa
    ax.plot(np.full_like(t, xpos), vib, np.full_like(t, -L / 2),
            color=col, lw=0.6, alpha=0.15)
ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 4, L / 4)
ax.set_zlim(-L / 2, L / 2)
ax.view_init(elev=14, azim=-72)
ax.set_axis_off()
ax.set_title("Harpa espectral — as %d notas ordenadas por altura\n"
             "(esquerda: graves/longas, direita: agudas/curtas; "
             "espessura ∝ intensidade)" % nh, fontsize=12)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/harpa_espectral.png", dpi=160,
            bbox_inches="tight")
plt.close()
print("   harpa_espectral.png")

# ================================================================ 3) TEIA DE PICOS
print("3) teia de picos...")
try:
    from scipy.ndimage import maximum_filter
except ImportError:
    def maximum_filter(arr, size=5):
        r = size // 2
        out = arr
        for axis in range(arr.ndim):
            sh = [np.roll(out, s, axis=axis) for s in range(-r, r + 1)]
            out = np.max(sh, axis=0)
        return out

mx = maximum_filter(rho, size=5)
# relaxa o corte até ter picos suficientes pra tecer a teia
perc = 99.0
pk = np.argwhere((rho == mx) & (rho > np.percentile(rho, perc)))
while len(pk) < 30 and perc > 85.0:
    perc -= 2.0
    pk = np.argwhere((rho == mx) & (rho > np.percentile(rho, perc)))
pv = rho[pk[:, 0], pk[:, 1], pk[:, 2]]
o = np.argsort(pv)[::-1][:120]
P = pk[o] * dx - L / 2
pv = pv[o]
print("   %d picos" % len(P))

fig = plt.figure(figsize=(11, 10))
ax = fig.add_subplot(111, projection="3d")
vmaxp = pv.max()
# fios: cada pico ligado aos seus 3 vizinhos mais próximos
lig = set()
for i in range(len(P)):
    dd = np.linalg.norm(P - P[i], axis=1)
    for j in np.argsort(dd)[1:4]:
        a, b = min(i, j), max(i, j)
        if (a, b) in lig or dd[j] > 0.35 * L:
            continue
        lig.add((a, b))
        t = np.linspace(0, 1, 60)
        seg = np.outer(1 - t, P[a]) + np.outer(t, P[b])
        # ondulação perpendicular, mais forte no meio do fio
        d = P[b] - P[a]; dn = np.linalg.norm(d)
        w1, _ = base_perp(d / dn)
        forca = 0.5 * (pv[a] + pv[b]) / vmaxp
        seg += np.outer(0.5 * forca * np.sin(np.pi * t) *
                        np.sin(6 * np.pi * t), w1)
        col = cmap_life(0.2 + 0.75 * forca)
        ax.plot(seg[:, 0], seg[:, 1], seg[:, 2], color=col,
                lw=0.7 + 2.2 * forca, alpha=0.65)
ax.scatter(P[:, 0], P[:, 1], P[:, 2], s=14 + 60 * (pv / vmaxp) ** 2,
           c=pv, cmap=cmap_life, alpha=0.95, linewidths=0)
ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2)
ax.set_zlim(-L / 2, L / 2)
ax.view_init(elev=22, azim=40)
ax.set_axis_off()
ax.set_title("Teia de picos — a rede cristalina tecida em fios\n"
             "(%d picos, cada um ligado aos 3 vizinhos; fio mais grosso = "
             "picos mais intensos)" % len(P), fontsize=12)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/teia_de_picos.png", dpi=160,
            bbox_inches="tight")
plt.close()
print("   teia_de_picos.png")

# ================================================================ 4) RIOS DE FASE
if psi is not None:
    print("4) rios de fase...")
    ph = np.angle(psi)
    # gradiente da fase com desenrolamento local (diferença embrulhada)
    def wrap(d):
        return (d + np.pi) % (2 * np.pi) - np.pi
    gx = wrap(np.roll(ph, -1, 0) - np.roll(ph, 1, 0)) / (2 * dx)
    gy = wrap(np.roll(ph, -1, 1) - np.roll(ph, 1, 1)) / (2 * dx)
    gz = wrap(np.roll(ph, -1, 2) - np.roll(ph, 1, 2)) / (2 * dx)

    def veloc(p):
        i = np.clip((p + L / 2) / dx, 0, N - 1.001)
        i0 = i.astype(int)
        return np.array([gx[i0[0], i0[1], i0[2]],
                         gy[i0[0], i0[1], i0[2]],
                         gz[i0[0], i0[1], i0[2]]])

    rng = np.random.default_rng(7)
    # semeia os rios nas regiões densas (é lá que a fase importa)
    thr = np.percentile(rho, 92.0)
    cand = np.argwhere(rho > thr)
    seeds = cand[rng.choice(len(cand), min(220, len(cand)), replace=False)]
    seeds = seeds * dx - L / 2

    fig = plt.figure(figsize=(11, 10))
    ax = fig.add_subplot(111, projection="3d")
    for si, s0 in enumerate(seeds):
        p = s0.astype(float).copy()
        traj = [p.copy()]
        for _ in range(90):
            v = veloc(p)
            nv = np.linalg.norm(v)
            if nv < 1e-6:
                break
            p = p + 0.35 * dx * v / nv
            if np.any(np.abs(p) > L / 2):
                break
            traj.append(p.copy())
        if len(traj) < 8:
            continue
        traj = np.array(traj)
        col = cmap_life(0.15 + 0.8 * si / len(seeds))
        ax.plot(traj[:, 0], traj[:, 1], traj[:, 2], color=col,
                lw=0.8, alpha=0.55)
        ax.scatter(*traj[-1], s=6, color=col, alpha=0.9, linewidths=0)
    ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2)
    ax.set_zlim(-L / 2, L / 2)
    ax.view_init(elev=20, azim=-50)
    ax.set_axis_off()
    ax.set_title("Rios de fase — linhas de fluxo do gradiente da fase de Ψ\n"
                 "(cada fio segue por onde a fase escorre; ponto = foz)",
                 fontsize=12)
    plt.tight_layout()
    plt.savefig("bravais_outputs_3d/rios_de_fase.png", dpi=160,
                bbox_inches="tight")
    plt.close()
    print("   rios_de_fase.png")
else:
    print("4) rios de fase pulados: o npz não tem psi_f — rode o "
          "simula_filmes.py (ou bravais_puro_3d.py atualizado)")

print("\nimagens em bravais_outputs_3d/: cordas_vibrando.gif, "
      "harpa_espectral.png, teia_de_picos.png, rios_de_fase.png")
