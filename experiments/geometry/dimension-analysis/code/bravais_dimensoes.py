#!/usr/bin/env python3
"""
Mapa de dimensões
=================
Não roda a dinâmica — lê o estado final salvo pelo bravais_puro_3d.py
(bravais_outputs_3d/final_state.npz) e mede quantas dimensões cada objeto
do sistema realmente usa, no mesmo molde do teste da pirâmide: cascas,
percentis e inclinações. Nenhuma dimensão é imposta — o número sai da
inclinação medida, em cada escala, e pode ser fracionário ou mudar com a
escala. O dado fala.

A régua usada em tudo: se um conjunto usa D dimensões, a quantidade dele
dentro de um raio r cresce como r^D. Então medimos a contagem N(<r) e a
inclinação local da reta log N × log r É a dimensão naquela escala.

  1. DIMENSÃO DO CARDÁPIO (espaço k): quantas dimensões o conjunto de
     modos ativos usa, em função do raio — nas duas famílias de casca
     (L1 e L2), como no teste da pirâmide.

  2. DIMENSÃO DOS FIOS (espaço real): caixas de tamanhos crescentes
     sobre o topo da densidade (0.5%, 2%, 10%) — a inclinação diz se os
     filamentos vivem como linhas (~1), folhas (~2) ou enchem o volume (~3).

  3. DIMENSÃO DE MASSA (autocorrelação): quanto de correlação cabe
     dentro do raio r, e a inclinação disso por escala.

  4. QUANTAS DIREÇÕES O OBJETO USA: os eixos principais da nuvem de
     modos fortes e da nuvem de densidade alta — os pesos dos eixos
     dizem se o objeto é esticado (1 direção), achatado (2) ou cheio (3),
     resumidos num número contínuo entre 1 e 3.

  5. DIMENSÃO DAS CORDAS DE FASE (se psi_f existir no npz): a mesma
     régua de caixas aplicada às linhas onde a fase dá volta completa —
     teste direto de que as "cordas" são objetos de ~1 dimensão.

Uso:
  python3 bravais_dimensoes.py
  python3 bravais_dimensoes.py caminho/arquivo.npz
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt

path = sys.argv[1] if len(sys.argv) > 1 else "bravais_outputs_3d/final_state.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o bravais_puro_3d.py antes" % path)
dat = np.load(path)
rho = dat["rho_f"]
psi = dat["psi_f"] if "psi_f" in dat.files else None
N = rho.shape[0]
L = float(os.environ.get("L", 32.0))
dx = L / N
os.makedirs("bravais_outputs_3d", exist_ok=True)


def local_slope(logx, logy, win=3):
    """Inclinação local de logy × logx (janela deslizante) = dimensão na escala."""
    slopes = np.full(len(logx), np.nan)
    for i in range(win, len(logx) - win):
        a = np.polyfit(logx[i - win:i + win + 1], logy[i - win:i + win + 1], 1)
        slopes[i] = a[0]
    return slopes


def box_counting(points_ijk, N, sizes=(1, 2, 4, 8, 16)):
    """Contagem de caixas ocupadas por um conjunto de pontos inteiros."""
    counts = []
    for b in sizes:
        boxes = set(map(tuple, (points_ijk // b).astype(int)))
        counts.append(len(boxes))
    return np.array(sizes, float), np.array(counts, float)


def participation_dim(points_xyz):
    """Número contínuo de direções usadas: pesos dos eixos principais
    resumidos em (Σλ)²/Σλ² — 1 se uma direção domina, 3 se as três pesam igual."""
    if len(points_xyz) < 4:
        return np.nan, np.array([np.nan] * 3)
    cov = np.cov((points_xyz - points_xyz.mean(0)).T)
    lam = np.sort(np.linalg.eigvalsh(cov))[::-1]
    lam = np.clip(lam, 0, None)
    pr = (lam.sum() ** 2) / (np.sum(lam**2) + 1e-30)
    return pr, lam / (lam.sum() + 1e-30)


# ================================================================ 1) dimensão do cardápio (espaço k)
fft3 = np.fft.fftshift(np.abs(np.fft.fftn(rho)))
power = fft3**2
power[N // 2, N // 2, N // 2] = 0.0
thr_k = np.percentile(power, 99.0)
kpts = np.argwhere(power > thr_k).astype(float)
kc = (kpts - N // 2) * (2 * np.pi / L)

R1 = np.abs(kc).sum(axis=1)          # raio L1 (família pirâmide)
R2 = np.sqrt((kc**2).sum(axis=1))    # raio L2 (família esfera)

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
for R, nome, cor in [(R1, "casca L1 (pirâmide)", "#3a506b"),
                     (R2, "casca L2 (esfera)", "#ee6c4d")]:
    rr = np.sort(R[R > 0])
    nn = np.arange(1, len(rr) + 1, dtype=float)
    # amostra em grade log pra inclinação estável
    ridx = np.unique(np.geomspace(1, len(rr) - 1, 40).astype(int))
    lr, ln = np.log(rr[ridx]), np.log(nn[ridx])
    axes[0].plot(lr, ln, ".-", ms=4, lw=1, color=cor, label=nome, alpha=0.85)
    sl = local_slope(lr, ln)
    axes[1].plot(np.exp(lr), sl, lw=2, color=cor, label=nome, alpha=0.85)
axes[0].set_xlabel("log raio"); axes[0].set_ylabel("log contagem de modos N(<r)")
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[0].set_title("crescimento da contagem de modos")
for dref in (1, 2, 3):
    axes[1].axhline(dref, ls="--", color="gray", alpha=0.5)
    axes[1].text(axes[1].get_xlim()[0], dref + 0.05, "D=%d" % dref,
                 fontsize=8, color="gray")
axes[1].set_xlabel("raio em k físico"); axes[1].set_ylabel("dimensão local (inclinação)")
axes[1].set_ylim(0, 4); axes[1].legend(); axes[1].grid(alpha=0.3)
axes[1].set_title("dimensão do cardápio por escala")
plt.suptitle("1) Quantas dimensões o conjunto de modos ativos usa", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/dim_cardapio.png", dpi=140, bbox_inches="tight")
plt.close()
print("dim_cardapio.png")

# ================================================================ 2) dimensão dos fios (espaço real)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
dims_fios = {}
for p, cor in [(99.5, "#0b132b"), (98.0, "#3a506b"), (90.0, "#5bc0be")]:
    pts = np.argwhere(rho > np.percentile(rho, p))
    if len(pts) < 8:
        continue
    sizes, counts = box_counting(pts, N)
    lb, lc = np.log(1.0 / sizes), np.log(counts)
    coef = np.polyfit(lb, lc, 1)
    dims_fios[p] = coef[0]
    axes[0].plot(lb, lc, "o-", color=cor, lw=2,
                 label="top %.1f%% → D=%.2f" % (100 - p, coef[0]))
axes[0].set_xlabel("log(1/tamanho da caixa)")
axes[0].set_ylabel("log caixas ocupadas")
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[0].set_title("contagem de caixas sobre o topo da densidade")
axes[1].bar([("top %.1f%%" % (100 - p)) for p in dims_fios],
            list(dims_fios.values()), color="#ee6c4d")
for dref in (1, 2, 3):
    axes[1].axhline(dref, ls="--", color="gray", alpha=0.5)
axes[1].set_ylim(0, 3.5)
axes[1].set_ylabel("dimensão medida")
axes[1].set_title("linha (~1), folha (~2) ou volume (~3)?")
axes[1].grid(alpha=0.3, axis="y")
plt.suptitle("2) Quantas dimensões os fios de densidade usam", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/dim_fios.png", dpi=140, bbox_inches="tight")
plt.close()
print("dim_fios.png")

# ================================================================ 3) dimensão de massa (autocorrelação)
acorr = np.fft.fftshift(np.fft.ifftn(np.abs(np.fft.fftn(rho)) ** 2).real)
acorr = acorr - np.median(acorr)         # tira o fundo, sobra a estrutura
acorr = np.clip(acorr, 0, None)
off = (np.arange(N) - N // 2) * dx
RR = np.sqrt(off[:, None, None] ** 2 + off[None, :, None] ** 2 + off[None, None, :] ** 2)
rs = np.linspace(dx, L / 3, 40)
mass = np.array([acorr[RR <= r].sum() for r in rs])
lr, lm = np.log(rs), np.log(mass + 1e-30)
sl = local_slope(lr, lm)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
axes[0].plot(lr, lm, ".-", color="#3a506b")
axes[0].set_xlabel("log r"); axes[0].set_ylabel("log massa de correlação M(<r)")
axes[0].grid(alpha=0.3); axes[0].set_title("massa de correlação acumulada")
axes[1].plot(rs, sl, lw=2, color="#ee6c4d")
for dref in (1, 2, 3):
    axes[1].axhline(dref, ls="--", color="gray", alpha=0.5)
axes[1].set_xlabel("raio r"); axes[1].set_ylabel("dimensão local")
axes[1].set_ylim(0, 4); axes[1].grid(alpha=0.3)
axes[1].set_title("dimensão de massa por escala")
plt.suptitle("3) Dimensão vista pela autocorrelação", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/dim_massa.png", dpi=140, bbox_inches="tight")
plt.close()
print("dim_massa.png")

# ================================================================ 4) quantas direções o objeto usa
alvo = {
    "modos fortes (k)": (kpts - N // 2) * (2 * np.pi / L),
    "densidade top 2%": (np.argwhere(rho > np.percentile(rho, 98.0)) * dx - L / 2),
}
fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
labels, prs = [], []
for ax, (nome, pts) in zip(axes, alvo.items()):
    pr, lamn = participation_dim(pts)
    labels.append(nome); prs.append(pr)
    ax.bar(["eixo 1", "eixo 2", "eixo 3"], lamn, color=["#0b132b", "#3a506b", "#5bc0be"])
    ax.set_ylim(0, 1)
    ax.set_title("%s\ndireções usadas = %.2f de 3" % (nome, pr))
    ax.grid(alpha=0.3, axis="y")
    ax.set_ylabel("peso do eixo")
plt.suptitle("4) Pesos dos eixos principais — esticado, achatado ou cheio?", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/dim_direcoes.png", dpi=140, bbox_inches="tight")
plt.close()
print("dim_direcoes.png  (%s)" % ", ".join("%s: %.2f" % (l, p) for l, p in zip(labels, prs)))

# ================================================================ 5) dimensão das cordas de fase
if psi is not None:
    ph = np.angle(psi)
    pts_all = []
    # plaquetas nas 3 orientações (mesma medição do bravais_cordas.py)
    for axset in ((0, 1), (0, 2), (1, 2)):
        a = ph
        b = np.roll(a, -1, axis=axset[0])
        c = np.roll(b, -1, axis=axset[1])
        d = np.roll(a, -1, axis=axset[1])
        w = ((b - a + np.pi) % (2 * np.pi) - np.pi) + \
            ((c - b + np.pi) % (2 * np.pi) - np.pi) + \
            ((d - c + np.pi) % (2 * np.pi) - np.pi) + \
            ((a - d + np.pi) % (2 * np.pi) - np.pi)
        pts_all.append(np.argwhere(np.abs(w) > np.pi))
    pts_ph = np.vstack(pts_all)
    if len(pts_ph) >= 8:
        sizes, counts = box_counting(pts_ph, N)
        lb, lc = np.log(1.0 / sizes), np.log(counts)
        coef = np.polyfit(lb, lc, 1)
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.plot(lb, lc, "o-", color="#ee6c4d", lw=2,
                label="cordas de fase → D=%.2f" % coef[0])
        # retas de referência D=1,2,3 partindo do primeiro ponto
        for dref, cor in [(1, "#5bc0be"), (2, "#f4d35e"), (3, "#3a506b")]:
            ax.plot(lb, lc[0] + dref * (lb - lb[0]), "--", color=cor,
                    alpha=0.6, label="referência D=%d" % dref)
        ax.set_xlabel("log(1/tamanho da caixa)")
        ax.set_ylabel("log caixas ocupadas")
        ax.legend(); ax.grid(alpha=0.3)
        ax.set_title("5) Dimensão das cordas de fase\n(linhas puras dariam D≈1)")
        plt.tight_layout()
        plt.savefig("bravais_outputs_3d/dim_cordas_fase.png", dpi=140, bbox_inches="tight")
        plt.close()
        print("dim_cordas_fase.png  (D=%.2f, %d pontos)" % (coef[0], len(pts_ph)))
else:
    print("(dimensão das cordas de fase pulada: npz sem psi_f)")

print("\nimagens em bravais_outputs_3d/: dim_cardapio.png, dim_fios.png, "
      "dim_massa.png, dim_direcoes.png, dim_cordas_fase.png (se houver psi)")
