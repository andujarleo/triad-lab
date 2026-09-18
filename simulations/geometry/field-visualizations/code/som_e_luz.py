#!/usr/bin/env python3
"""
Som e luz — "sem som não há luz"?
=================================
Não roda a dinâmica — lê os quadros salvos pelo simula_filmes.py
(densidade E fase no tempo) e testa a hipótese em DUAS traduções:

TRADUÇÃO A — densidade e fase (Ψ = √ρ·e^iθ):
  SOM  = vibração local da densidade (quanto ρ muda entre quadros)
  LUZ  = coerência local da fase (vizinhos com θ alinhado = feixe;
         bagunçado = escuro)

TRADUÇÃO B — graves e agudos do espectro:
  SOM  = a parte grave da densidade (modos longos, |k| baixo)
  LUZ  = a parte aguda (modos curtos e rápidos, |k| alto)

Três perguntas, cada uma com número:
  1. Onde não há som, há luz?  (coerência/agudos nas regiões caladas,
     e busca de contraexemplos: luz sem som)
  2. Quem vem primeiro?  (correlação com defasagem entre o nível
     global de som e de luz: quem prevê quem)
  3. Quem carrega mais energia em cada época?

Nada da equação é tocado — só leitura dos quadros completos.

Uso:  python3 som_e_luz.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

path = "bravais_outputs_3d/filmes_data.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o simula_filmes.py antes" % path)
dat = np.load(path)
R = dat["rho"].astype(np.float32)
PH = dat["fase"].astype(np.float32)
tempos = dat["tempos"]
L = float(dat["L"])
NF, N = R.shape[0], R.shape[1]
dx = L / N
os.makedirs("bravais_outputs_3d", exist_ok=True)

cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])


def wrap(d):
    return (d + np.pi) % (2 * np.pi) - np.pi


def coerencia(ph):
    """Coerência local da fase: |média dos fasores e^iθ| no cubo 3³.
    1 = vizinhança marchando junta (feixe); 0 = bagunça (escuro)."""
    ex, ey = np.cos(ph), np.sin(ph)
    sx, sy = ex.copy(), ey.copy()
    nv = 1
    for ax in range(3):
        for s in (-1, 1):
            sx += np.roll(ex, s, axis=ax)
            sy += np.roll(ey, s, axis=ax)
            nv += 1
    return np.sqrt(sx**2 + sy**2) / nv


# filtro espectral grave/agudo (corte no meio geométrico do espectro)
k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
Kabs = np.sqrt(KX**2 + KY**2 + KZ**2)
kc = 0.35 * Kabs.max()
low = Kabs <= kc


def separa_bandas(rho):
    F = np.fft.fftn(rho)
    grave = np.real(np.fft.ifftn(np.where(low, F, 0)))
    agudo = np.real(np.fft.ifftn(np.where(low, 0, F)))
    return grave, agudo


# ================================================================ séries e mapas
print("processando %d quadros..." % NF)
S_A, Luz_A = [], []          # níveis globais, tradução A
S_B, Luz_B = [], []          # tradução B
mapa_som = np.zeros((N, N, N), np.float32)     # vibração média (A)
mapa_luz = np.zeros((N, N, N), np.float32)     # coerência média (A)
E_som, E_luz = [], []        # energias (A): flutuação de ρ vs fluxo de fase

for f in range(NF):
    rho, ph = R[f], PH[f]
    coh = coerencia(ph)
    mapa_luz += coh / NF
    if f > 0:
        vib = np.abs(rho - R[f - 1])
        mapa_som += vib / (NF - 1)
        S_A.append(np.mean(vib))
    Luz_A.append(np.mean(coh))
    # energias
    E_som.append(np.mean((rho - rho.mean()) ** 2))
    gx = wrap(np.roll(ph, -1, 0) - np.roll(ph, 1, 0)) / (2 * dx)
    gy = wrap(np.roll(ph, -1, 1) - np.roll(ph, 1, 1)) / (2 * dx)
    gz = wrap(np.roll(ph, -1, 2) - np.roll(ph, 1, 2)) / (2 * dx)
    E_luz.append(np.mean(rho * (gx**2 + gy**2 + gz**2)))
    # tradução B
    g_, a_ = separa_bandas(rho)
    S_B.append(np.mean(g_**2))
    Luz_B.append(np.mean(a_**2))

S_A = np.array(S_A); Luz_A = np.array(Luz_A)
S_B = np.array(S_B); Luz_B = np.array(Luz_B)
E_som = np.array(E_som); E_luz = np.array(E_luz)

# ================================================================ 1) onde não há som, há luz?
# usa os mapas médios (A): decis de som vs coerência média
q = np.quantile(mapa_som, np.linspace(0, 1, 11))
decis, luz_por_decil = [], []
for i in range(10):
    m = (mapa_som >= q[i]) & (mapa_som <= q[i + 1])
    decis.append(i + 1)
    luz_por_decil.append(mapa_luz[m].mean())

# contraexemplos: luz alta (topo 10%) em lugar calado (fundo 30%)
thr_luz = np.quantile(mapa_luz, 0.90)
thr_som = np.quantile(mapa_som, 0.30)
contra = (mapa_luz > thr_luz) & (mapa_som < thr_som)
frac_contra = contra.mean() / max((mapa_luz > thr_luz).mean(), 1e-12)

# mesmo teste na tradução B, por voxel médio
mapa_gr = np.zeros((N, N, N), np.float32)
mapa_ag = np.zeros((N, N, N), np.float32)
for f in range(NF):
    g_, a_ = separa_bandas(R[f])
    mapa_gr += np.abs(g_ - g_.mean()) / NF
    mapa_ag += np.abs(a_) / NF
qB = np.quantile(mapa_gr, np.linspace(0, 1, 11))
luz_por_decil_B = [mapa_ag[(mapa_gr >= qB[i]) & (mapa_gr <= qB[i + 1])].mean()
                   for i in range(10)]

# ================================================================ 2) quem vem primeiro?
def lidera(s, l, maxlag=8):
    """correlação de s(t) com l(t+lag); lag>0 = som prevê luz."""
    s = (s - s.mean()) / (s.std() + 1e-12)
    l = (l - l.mean()) / (l.std() + 1e-12)
    lags = range(-maxlag, maxlag + 1)
    cc = [np.mean(s[max(0, -g):len(s) - max(0, g)] *
                  l[max(0, g):len(l) - max(0, -g)]) for g in lags]
    return np.array(list(lags)), np.array(cc)

lagsA, ccA = lidera(S_A, Luz_A[1:])
lagsB, ccB = lidera(S_B, Luz_B)

# ================================================================ figura
fig, axes = plt.subplots(2, 3, figsize=(16, 9))

ax = axes[0, 0]
ax.plot(decis, luz_por_decil, "o-", color="#ee6c4d")
ax.set_xlabel("decil de SOM (1 = mais calado)"); ax.set_ylabel("LUZ média (coerência)")
ax.set_title("A: luz por nível de som\n(sobe = sem som, sem luz)", fontsize=10)
ax.grid(alpha=0.3)

ax = axes[0, 1]
ax.plot(lagsA, ccA, "o-", color="#5bc0be")
ax.axvline(0, color="gray", lw=0.8)
best = lagsA[np.argmax(np.abs(ccA))]
ax.set_title("A: quem prevê quem?\n(pico à direita de 0 = SOM lidera; "
             "melhor defasagem: %+d)" % best, fontsize=10)
ax.set_xlabel("defasagem (quadros)"); ax.set_ylabel("correlação")
ax.grid(alpha=0.3)

ax = axes[0, 2]
ax.plot(tempos, E_som / E_som.max(), color="#ee6c4d", label="canal do som (flutuação de ρ)")
ax.plot(tempos, E_luz / E_luz.max(), color="#5bc0be", label="canal da luz (fluxo de fase ρ|∇θ|²)")
ax.set_title("A: energia de cada canal no tempo (normalizada)", fontsize=10)
ax.set_xlabel("passo"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

ax = axes[1, 0]
ax.plot(decis, luz_por_decil_B, "s-", color="#f4d35e")
ax.set_xlabel("decil de GRAVES"); ax.set_ylabel("AGUDOS médios")
ax.set_title("B: agudos por nível de graves", fontsize=10)
ax.grid(alpha=0.3)

ax = axes[1, 1]
ax.plot(lagsB, ccB, "s-", color="#f4d35e")
ax.axvline(0, color="gray", lw=0.8)
bestB = lagsB[np.argmax(np.abs(ccB))]
ax.set_title("B: quem prevê quem?\n(melhor defasagem: %+d)" % bestB, fontsize=10)
ax.set_xlabel("defasagem (quadros)"); ax.set_ylabel("correlação")
ax.grid(alpha=0.3)

ax = axes[1, 2]
zc = N // 2
im = ax.imshow(np.where(contra[:, :, zc], 1.0, np.nan).T, origin="lower",
               cmap="autumn", extent=[-L / 2, L / 2, -L / 2, L / 2])
ax.imshow(mapa_luz[:, :, zc].T, origin="lower", cmap="gray",
          extent=[-L / 2, L / 2, -L / 2, L / 2], alpha=0.6)
ax.set_title("contraexemplos (fatia z=0): luz SEM som\n"
             "%.1f%% da luz forte vive em lugar calado" % (100 * frac_contra),
             fontsize=10)
ax.tick_params(labelsize=7)

plt.suptitle('Teste "sem som não há luz" — duas traduções, três perguntas',
             fontsize=14)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/som_luz_teste.png", dpi=150, bbox_inches="tight")
plt.close()
print("som_luz_teste.png")

# mapas lado a lado
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
for ax, (m, ttl) in zip(axes, [(mapa_som, "mapa do SOM (vibração média de ρ)"),
                               (mapa_luz, "mapa da LUZ (coerência média de θ)"),
                               (mapa_som * mapa_luz, "onde som e luz moram juntos")]):
    ax.imshow(m[:, :, zc].T, origin="lower", cmap=cmap_life,
              extent=[-L / 2, L / 2, -L / 2, L / 2])
    ax.set_title(ttl, fontsize=10); ax.tick_params(labelsize=7)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/som_luz_mapas.png", dpi=150, bbox_inches="tight")
plt.close()
print("som_luz_mapas.png")

# ================================================================ veredito
r_A = np.corrcoef(mapa_som.ravel(), mapa_luz.ravel())[0, 1]
r_B = np.corrcoef(mapa_gr.ravel(), mapa_ag.ravel())[0, 1]
print("\n===== RESULTADO =====")
print("A (densidade/fase):")
print("  correlação som-luz por ponto: r = %+.3f" % r_A)
print("  luz média no decil mais calado: %.3f | no mais vibrante: %.3f"
      % (luz_por_decil[0], luz_por_decil[-1]))
print("  luz forte em lugar calado (contraexemplos): %.1f%%" % (100 * frac_contra))
print("  defasagem que melhor liga som→luz: %+d quadros" % best)
print("B (graves/agudos):")
print("  correlação graves-agudos por ponto: r = %+.3f" % r_B)
print("  defasagem que melhor liga graves→agudos: %+d quadros" % bestB)
print("\nleitura: se a luz cresce com o som, quase não há contraexemplos e a")
print("defasagem fica do lado do som, a hipótese se sustenta NESTE mundo.")
print("Se houver muita luz em lugar calado, o mundo diz que luz vive sem som.")
