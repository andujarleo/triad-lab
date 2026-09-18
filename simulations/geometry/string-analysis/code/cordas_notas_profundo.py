#!/usr/bin/env python3
"""
Cordas-nota em profundidade
===========================
Não roda a dinâmica — só lê o estado final salvo pelo bravais_puro_3d.py
e aprofunda o lado espectral das cordas: como as notas fortes do espectro
se relacionam com os filamentos de densidade no espaço real.

Regras respeitadas: nada de dinâmica aqui (nenhum termo tocado, nenhum
termo isolado); toda análise usa o campo completo salvo.

Quatro figuras:

  1. RECONSTRUÇÃO — quantas notas são precisas pra "cantar" os
     filamentos: densidade reconstruída só com as n notas mais fortes,
     comparada com os filamentos reais (topo 3% de |Ψ|²). Curva de
     sobreposição (IoU) vs número de notas.

  2. PEGADA DE CADA NOTA — onde cada uma das 6 notas mais fortes vive
     no espaço real: a onda daquela nota sozinha (só visualização — a
     densidade completa continua sendo a soma de todas), sobreposta
     aos filamentos.

  3. ESPECTRO RADIAL + HARMÔNICOS — potência por casca |k|, notas
     marcadas, razões |k_i|/|k_1| (harmônicos?) e ângulos entre as
     direções das notas fortes.

  4. IMPRESSÃO DIGITAL — matriz filamento × nota: quanto cada filamento
     de densidade "toca" cada nota. Mostra se cada corda tem sua nota
     ou se todas tocam o mesmo acorde.

Uso:
  python3 cordas_notas_profundo.py                     (final_state.npz)
  python3 cordas_notas_profundo.py caminho/arquivo.npz
  L=32 python3 cordas_notas_profundo.py                (caixa diferente)
"""
import sys
import os
import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap

path = sys.argv[1] if len(sys.argv) > 1 else "bravais_outputs_3d/final_state.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o bravais_puro_3d.py antes" % path)
dat = np.load(path)
rho = dat["rho_f"]
N = rho.shape[0]
L = float(os.environ.get("L", 32.0))
dx = L / N
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
X, Y, Zg = np.meshgrid(x, x, x, indexing="ij")
os.makedirs("bravais_outputs_3d", exist_ok=True)

cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"]
)

try:
    from scipy.ndimage import label as cc_label
except ImportError:
    def cc_label(mask):
        lab = np.zeros(mask.shape, dtype=np.int32)
        cur = 0
        idxs = np.argwhere(mask)
        idx_set = set(map(tuple, idxs))
        for seed in map(tuple, idxs):
            if lab[seed] != 0:
                continue
            cur += 1
            stack = [seed]
            lab[seed] = cur
            while stack:
                i, j, k = stack.pop()
                for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0),
                          (0, -1, 0), (0, 0, 1), (0, 0, -1)):
                    nb = (i + d[0], j + d[1], k + d[2])
                    if nb in idx_set and lab[nb] == 0:
                        lab[nb] = cur
                        stack.append(nb)
        return lab, cur

# ---------------------------------------------------------------- notas
Fk = np.fft.fftn(rho)                      # FFT completa (com fase!)
power = np.abs(np.fft.fftshift(Fk)) ** 2
power[N // 2, N // 2, N // 2] = 0.0
flat = np.argsort(power.ravel())[::-1]
n_notes = 40
seen = set()
notes = []                                  # (ijk_shifted, kvec, potência)
for fi in flat:
    ijk = np.unravel_index(fi, power.shape)
    kvec = (np.array(ijk) - N // 2) * (2 * np.pi / L)
    key = tuple(np.round(np.abs(kvec), 6))  # junta k e -k (mesma nota)
    if key in seen:
        continue
    seen.add(key)
    notes.append((ijk, kvec, power[ijk]))
    if len(notes) >= n_notes:
        break
pmax = notes[0][2]

# ---------------------------------------------------------------- filamentos
thr = np.percentile(rho, 97.0)
mask_real = rho > thr
lab, ncomp = cc_label(mask_real)
sizes = np.bincount(lab.ravel())[1:]
order_f = np.argsort(sizes)[::-1]
keep = [i + 1 for i in order_f[:24] if sizes[i] >= 8]
print("filamentos (topo 3%%): %d fios | notas: %d" % (len(keep), len(notes)))


def recon_with(n):
    """Densidade reconstruída só com o modo médio + as n notas mais fortes
    (cada nota entra com k e -k, fases originais preservadas)."""
    keep_k = np.zeros((N, N, N), dtype=bool)
    keep_k[0, 0, 0] = True                  # média
    for ijk, kvec, pw in notes[:n]:
        us = tuple((np.array(ijk) - N // 2) % N)   # desfaz o fftshift
        keep_k[us] = True
        keep_k[tuple((-np.array(us)) % N)] = True  # conjugado (-k)
    return np.real(np.fft.ifftn(np.where(keep_k, Fk, 0.0)))


# ================================================================ 1) RECONSTRUÇÃO
ns = [1, 2, 3, 5, 8, 12, 20, 30, 40]
ious = []
for n in ns:
    rc = recon_with(n)
    mask_rc = rc > np.percentile(rc, 97.0)
    inter = np.sum(mask_rc & mask_real)
    union = np.sum(mask_rc | mask_real)
    ious.append(inter / max(union, 1))

fig = plt.figure(figsize=(15, 9))
zc = N // 2
show = [1, 3, 8, 40]
for pi, n in enumerate(show, 1):
    ax = fig.add_subplot(2, 3, pi)
    rc = recon_with(n)
    ax.imshow(rc[:, :, zc].T, origin="lower", cmap=cmap_life,
              extent=[-L / 2, L / 2, -L / 2, L / 2])
    ax.contour(x, x, mask_real[:, :, zc].T, levels=[0.5],
               colors="white", linewidths=0.7)
    ax.set_title("%d nota%s  (IoU=%.2f)" %
                 (n, "s" if n > 1 else "", ious[ns.index(n)]), fontsize=10)
    ax.tick_params(labelsize=6)
ax = fig.add_subplot(2, 3, 5)
ax.imshow(rho[:, :, zc].T, origin="lower", cmap=cmap_life,
          extent=[-L / 2, L / 2, -L / 2, L / 2])
ax.set_title("densidade completa (fatia z=0)", fontsize=10)
ax.tick_params(labelsize=6)
ax = fig.add_subplot(2, 3, 6)
ax.plot(ns, ious, "o-", color="#ee6c4d")
ax.set_xlabel("número de notas"); ax.set_ylabel("IoU com filamentos reais")
ax.set_title("quantas notas cantam os filamentos", fontsize=10)
ax.grid(alpha=0.3)
plt.suptitle("Reconstrução dos filamentos a partir das notas mais fortes\n"
             "(contorno branco = filamentos reais, topo 3% de |Ψ|²)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_notas_reconstrucao.png",
            dpi=140, bbox_inches="tight")
plt.close()
print("cordas_notas_reconstrucao.png  IoU(40 notas)=%.2f" % ious[-1])

# ================================================================ 2) PEGADA DE CADA NOTA
fig = plt.figure(figsize=(15, 10))
for pi, (ijk, kvec, pw) in enumerate(notes[:6], 1):
    us = tuple((np.array(ijk) - N // 2) % N)
    ck = Fk[us]
    wave = 2.0 * np.real(ck * np.exp(1j * (kvec[0] * X + kvec[1] * Y
                                           + kvec[2] * Zg))) / rho.size
    ax = fig.add_subplot(2, 3, pi)
    ax.imshow(wave[:, :, zc].T, origin="lower", cmap="RdBu_r",
              extent=[-L / 2, L / 2, -L / 2, L / 2])
    ax.contour(x, x, mask_real[:, :, zc].T, levels=[0.5],
               colors="black", linewidths=0.8)
    kn = np.linalg.norm(kvec)
    ax.set_title("nota %d  |k|=%.2f  λ=%.1f  P/P₁=%.2f\nk=(%.2f, %.2f, %.2f)"
                 % (pi, kn, 2 * np.pi / max(kn, 1e-9), pw / pmax, *kvec),
                 fontsize=9)
    ax.tick_params(labelsize=6)
plt.suptitle("Pegada real das 6 notas mais fortes (fatia z=0)\n"
             "onda de cada nota sozinha — só visualização; a densidade completa "
             "é a soma de todas — com os filamentos reais em preto", fontsize=12)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_notas_pegada.png",
            dpi=140, bbox_inches="tight")
plt.close()
print("cordas_notas_pegada.png")

# ================================================================ 3) ESPECTRO RADIAL + HARMÔNICOS
k1d = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing="ij")
Kabs = np.sqrt(KX**2 + KY**2 + KZ**2)
Pfull = np.abs(Fk) ** 2
Pfull[0, 0, 0] = 0.0
kmax = np.pi / dx
nb = 60
edges = np.linspace(0, kmax, nb + 1)
which = np.digitize(Kabs.ravel(), edges) - 1
radial = np.zeros(nb)
counts = np.zeros(nb)
np.add.at(radial, np.clip(which, 0, nb - 1), Pfull.ravel())
np.add.at(counts, np.clip(which, 0, nb - 1), 1.0)
radial /= np.maximum(counts, 1)
kcent = 0.5 * (edges[:-1] + edges[1:])

knorms = np.array([np.linalg.norm(kv) for _, kv, _ in notes])
pws = np.array([pw for _, _, pw in notes])
ratios = knorms / knorms[0]

# ângulos entre as direções das 12 notas mais fortes
nd = min(12, len(notes))
dirs = np.array([kv / max(np.linalg.norm(kv), 1e-12)
                 for _, kv, _ in notes[:nd]])
ang = np.degrees(np.arccos(np.clip(np.abs(dirs @ dirs.T), 0, 1)))  # 0–90°

fig = plt.figure(figsize=(15, 5))
ax = fig.add_subplot(1, 3, 1)
ax.semilogy(kcent, radial + 1e-12, color="#3a506b")
for kn, pw in zip(knorms, pws):
    ax.axvline(kn, color="#ee6c4d", alpha=0.15 + 0.6 * pw / pmax, lw=1)
ax.set_xlabel("|k|"); ax.set_ylabel("potência média por casca")
ax.set_title("espectro radial (linhas = notas)", fontsize=10)
ax = fig.add_subplot(1, 3, 2)
ax.stem(ratios, pws / pmax)
for h in (1, np.sqrt(2), np.sqrt(3), 2, np.sqrt(5)):
    ax.axvline(h, color="gray", ls=":", lw=0.8)
ax.set_xlabel("|k| / |k₁|"); ax.set_ylabel("P / P₁")
ax.set_title("razões harmônicas (pontilhado: 1, √2, √3, 2, √5)", fontsize=10)
ax = fig.add_subplot(1, 3, 3)
im = ax.imshow(ang, cmap=cmap_life, vmin=0, vmax=90)
plt.colorbar(im, ax=ax, label="ângulo (°)")
ax.set_title("ângulo entre direções das %d notas fortes" % nd, fontsize=10)
ax.set_xlabel("nota"); ax.set_ylabel("nota")
plt.suptitle("Estrutura do cardápio de notas", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_notas_espectro.png",
            dpi=140, bbox_inches="tight")
plt.close()
print("cordas_notas_espectro.png")

# ================================================================ 4) IMPRESSÃO DIGITAL
nf = len(keep)
nn = min(20, len(notes))
fp = np.zeros((nf, nn))
for fi_, comp in enumerate(keep):
    idx = np.argwhere(lab == comp)
    xs = idx[:, 0] * dx - L / 2
    ys = idx[:, 1] * dx - L / 2
    zs = idx[:, 2] * dx - L / 2
    w = rho[idx[:, 0], idx[:, 1], idx[:, 2]]
    for ni_, (ijk, kvec, pw) in enumerate(notes[:nn]):
        proj = np.sum(w * np.exp(-1j * (kvec[0] * xs + kvec[1] * ys
                                        + kvec[2] * zs)))
        fp[fi_, ni_] = np.abs(proj) / (np.sum(w) + 1e-12)

fig, ax = plt.subplots(figsize=(11, 7))
im = ax.imshow(fp, aspect="auto", cmap=cmap_life)
plt.colorbar(im, ax=ax, label="|projeção| normalizada")
ax.set_xlabel("nota (1 = mais forte)")
ax.set_ylabel("filamento (1 = maior)")
ax.set_xticks(range(nn), [str(i + 1) for i in range(nn)], fontsize=7)
ax.set_yticks(range(nf), [str(i + 1) for i in range(nf)], fontsize=7)
ax.set_title("Impressão digital espectral — quanto cada filamento toca cada nota\n"
             "(linhas parecidas = todas as cordas tocam o mesmo acorde; "
             "linhas distintas = cada corda tem sua nota)", fontsize=11)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_notas_fingerprint.png",
            dpi=140, bbox_inches="tight")
plt.close()
print("cordas_notas_fingerprint.png")

# ---------------------------------------------------------------- dados
out = {
    "n_filamentos": int(nf),
    "notas": [{"k": [float(v) for v in kv], "abs_k": float(np.linalg.norm(kv)),
               "lambda": float(2 * np.pi / max(np.linalg.norm(kv), 1e-9)),
               "P_rel": float(pw / pmax)} for _, kv, pw in notes],
    "iou_por_n_notas": {str(n): float(i) for n, i in zip(ns, ious)},
    "razoes_harmonicas": [float(r) for r in ratios],
}
with open("bravais_outputs_3d/cordas_notas_dados.json", "w") as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print("cordas_notas_dados.json")

print("\nimagens em bravais_outputs_3d/: cordas_notas_reconstrucao.png, "
      "cordas_notas_pegada.png, cordas_notas_espectro.png, "
      "cordas_notas_fingerprint.png")
