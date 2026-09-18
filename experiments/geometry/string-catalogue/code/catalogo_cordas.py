#!/usr/bin/env python3
"""
Catálogo das cordas — reconhecimento de padrões
===============================================
Lê cordas.csv (colhido pelo colhe_cordas.py) e aprende as ESPÉCIES de
corda sem supervisão. Critérios fixados antes de rodar:
  - características: as 14 do CSV (6 morfológicas + 8 bandas espectrais)
  - normalização: média 0, desvio 1 (StandardScaler)
  - redução: PCA mantendo 95% da variância
  - agrupamento: KMeans, k varrido de 2 a 20, n_init=10, semente 0
  - escolha de k: silhueta máxima
  - saturação: refaz o catálogo usando só os primeiros 1..S universos e
    registra quantas espécies saem em cada prefixo

Imprime: nº de cordas, k escolhido, silhueta, tamanho das famílias,
curva de saturação. Gera catalogo_cordas.png e cordas_rotuladas.csv.

Uso:  python3 catalogo_cordas.py   [cordas.csv]
"""
import sys
import csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

path = sys.argv[1] if len(sys.argv) > 1 else "cordas.csv"
rows = list(csv.DictReader(open(path)))
if len(rows) < 10:
    raise SystemExit("só %d cordas no CSV — colha mais universos" % len(rows))
feats = ["size", "elong", "atoms", "rho_mean", "rho_max", "vort"] + \
        ["b%d" % (i + 1) for i in range(8)]
Xr = np.array([[float(r[f]) for f in feats] for r in rows])
seeds = np.array([int(r["seed"]) for r in rows])
print("cordas: %d | universos: %d | características: %d"
      % (len(rows), len(set(seeds)), len(feats)))

def cataloga(Xsub):
    Xs = StandardScaler().fit_transform(Xsub)
    P = PCA(n_components=0.95, random_state=0).fit_transform(Xs)
    melhor = None
    kmax = min(20, len(Xsub) - 1)
    for k in range(2, kmax + 1):
        km = KMeans(n_clusters=k, n_init=10, random_state=0).fit(P)
        s = silhouette_score(P, km.labels_) if len(set(km.labels_)) > 1 else -1
        if melhor is None or s > melhor[1]:
            melhor = (k, s, km.labels_, P)
    return melhor

k, sil, labels, P = cataloga(Xr)
tam = np.bincount(labels)

# saturação
us = sorted(set(seeds))
sat = []
if len(us) > 1:
    sat_rot = "nº de universos usados"
    for i in range(1, len(us) + 1):
        m = np.isin(seeds, us[:i])
        if m.sum() >= 10:
            sat.append((i, cataloga(Xr[m])[0]))
else:
    sat_rot = "nº de cordas amostradas"
    rng = np.random.default_rng(0)
    ordem = rng.permutation(len(Xr))
    passos = np.unique(np.linspace(10, len(Xr), 12).astype(int))
    for n_ in passos:
        sat.append((int(n_), cataloga(Xr[ordem[:n_]])[0]))

# figura
fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))
ax = axes[0]
sc = ax.scatter(P[:, 0], P[:, 1], c=labels, cmap="turbo", s=14, alpha=0.8)
ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
ax.set_title("as %d espécies de corda (silhueta %.3f)" % (k, sil), fontsize=10)
ax = axes[1]
ax.bar(range(k), tam, color=plt.cm.turbo(np.linspace(0, 1, k)))
ax.set_xlabel("espécie"); ax.set_ylabel("nº de cordas")
ax.set_title("tamanho das famílias", fontsize=10)
ax = axes[2]
if sat:
    ax.plot([s[0] for s in sat], [s[1] for s in sat], "o-", color="#ee6c4d")
ax.set_xlabel(sat_rot); ax.set_ylabel("espécies encontradas")
ax.set_title("saturação do catálogo (achata = alfabeto finito)", fontsize=10)
ax.grid(alpha=0.3)
plt.suptitle("Catálogo das cordas — %d cordas de %d universos"
             % (len(rows), len(us)), fontsize=13)
plt.tight_layout()
plt.savefig("catalogo_cordas.png", dpi=150, bbox_inches="tight")
print("catalogo_cordas.png")

with open("cordas_rotuladas.csv", "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["seed", "corda", "especie"] + feats)
    for r, lb in zip(rows, labels):
        w.writerow([r["seed"], r["corda"], lb] + [r[f] for f in feats])
print("cordas_rotuladas.csv")

print("\n===== CATÁLOGO =====")
print("espécies (k): %d | silhueta: %.3f" % (k, sil))
for i, t in enumerate(tam):
    print("  espécie %2d: %4d cordas (%.1f%%)" % (i, t, 100 * t / len(rows)))
print("saturação:", " ".join("%d->%d esp" % s for s in sat))
