#!/usr/bin/env python3
"""
Teste da musica e teste da batida
=================================
Dinamica IDENTICA ao bravais_puro_3d.py (todos os termos juntos, nada
isolado, nada calibrado). Oito gemeas identicas ate no ruido, todas
partindo do mesmo universo em t=T_KICK. So o estado é tocado; a
equacao, nunca.

PARTE 1 — A MUSICA (4 gemeas):
  silencio      referencia, ninguem toca nela
  musica        a nota mais forte do proprio universo, tocada 8 vezes
                NO RITMO dela (intervalo = o periodo da propria nota)
  embaralhada   8 batidas nos MESMOS instantes, mesma forca, mas cada
                vez uma nota sorteada do cardapio, em ordem aleatoria
  sem ritmo     a mesma nota unica da musica, mesma forca, mas em
                instantes sorteados (fora de compasso)
  Pergunta: a musica certa move o universo mais que as mesmas batidas
  sem ordem? (ressonancia: empurrar o balanco na hora certa)

PARTE 2 — A BATIDA NAS COISAS (4 gemeas + a mesma referencia):
  bate-se (bump curto, sem nota) em TRES coisas diferentes do universo
  (tres picos afastados da densidade) e DUAS VEZES na mesma coisa em
  pontos vizinhos. Grava-se o som que cada coisa emite: o espectro da
  diferenca nos primeiros instantes apos a batida.
  Pergunta: cada coisa tem seu numero? (mesma coisa batida em dois
  pontos = mesmo som; coisas diferentes = sons diferentes)

Uso:
  python3 teste_musica_batida.py                 (N=64, 1200 passos)
  N=48 STEPS=400 python3 teste_musica_batida.py  (teste rapido)
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import os

try:
    from scipy.ndimage import maximum_filter
except ImportError:
    def maximum_filter(arr, size=5):
        """Fallback numpy: filtro de máximo separável (bordas periódicas)."""
        r = size // 2
        out = arr
        for axis in range(arr.ndim):
            shifted = [np.roll(out, s, axis=axis) for s in range(-r, r + 1)]
            out = np.max(shifted, axis=0)
        return out

SEED = int(os.environ.get("SEED", 7))
np.random.seed(SEED)
os.makedirs("bravais_outputs_3d", exist_ok=True)

# ---------------------------------------------------------------- grid 3D
L = float(os.environ.get("L", 32.0))
N = int(os.environ.get("N", 64))          # 64^3 = 262144 pontos; suba p/ 96 se tiver paciência
dx = L / N
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
X, Y, Zg = np.meshgrid(x, x, x, indexing="ij")

k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
Kabs = np.sqrt(K2 + 1e-30)

dV = dx**3


def multi_gaussian_field(n_centers=12):
    psi = np.zeros((N, N, N), dtype=np.complex128)
    centers = np.random.uniform(-0.3 * L, 0.3 * L, size=(n_centers, 3))
    widths = np.random.uniform(1.5, 3.5, size=n_centers)
    amps = np.random.uniform(0.3, 1.0, size=n_centers)
    for (cx, cy, cz), w, amp in zip(centers, widths, amps):
        phase = np.exp(1j * np.random.uniform(0, 2 * np.pi))
        psi += amp * phase * np.exp(
            -((X - cx) ** 2 + (Y - cy) ** 2 + (Zg - cz) ** 2) / (2 * w**2)
        )
    psi += 0.05 * (np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))
    return psi


psi0 = multi_gaussian_field(12)

Z = {
    "h": np.zeros(4),
    "b": np.zeros(4),
    "a": np.zeros(4),
    "n": np.zeros(4),
    "g": np.zeros(4),
    "ell": np.zeros(8),
    "v": np.zeros(8),   # 3D: mais graus de liberdade de rede
    "psi": psi0.copy(),
}

welford = {"mean": np.zeros(8), "M2": np.zeros(8), "count": 0}


def welford_update(measures):
    welford["count"] += 1
    c = welford["count"]
    delta = measures - welford["mean"]
    welford["mean"] += delta / c
    welford["M2"] += delta * (measures - welford["mean"])


def welford_z(measures):
    c = max(welford["count"], 1)
    var = welford["M2"] / max(c - 1, 1)
    return (measures - welford["mean"]) / (np.sqrt(var) + 1e-8)


def soft_bound(vec, cap=1.0):
    nrm = np.linalg.norm(vec)
    return vec / (1.0 + nrm / max(cap, 1e-12))


def project_state_vector(vec, radius=2.0):
    nrm = np.linalg.norm(vec)
    if nrm <= radius:
        return vec
    return vec * (radius / nrm)


guard_count = {"n": 0}


def psi_numeric_guard(psi):
    """Só age se a norma explodir ou colapsar numericamente."""
    nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if np.isfinite(nrm2) and nrm2 > 100.0:
        guard_count["n"] += 1
    if not np.isfinite(nrm2) or nrm2 > 1e6:
        psi = np.nan_to_num(psi, nan=0.0, posinf=0.0, neginf=0.0)
        nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if nrm2 < 1e-12:
        psi = psi + 1e-3 * (np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))
        nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if nrm2 > 100.0:
        psi = psi * np.sqrt(50.0 / nrm2)
    return psi


def experience_signature(psi, Z):
    rho = np.abs(psi) ** 2
    mean_rho = np.mean(rho) + 1e-12
    std_rho = np.std(rho)
    fft = np.abs(np.fft.fftn(rho))
    total = np.sum(fft**2)
    order_energy = (total - fft[0, 0, 0] ** 2) / (total + 1e-12)
    gx = np.roll(rho, -1, 0) - np.roll(rho, 1, 0)
    gy = np.roll(rho, -1, 1) - np.roll(rho, 1, 1)
    gz = np.roll(rho, -1, 2) - np.roll(rho, 1, 2)
    rough = np.mean(gx**2 + gy**2 + gz**2)
    measures = np.array(
        [
            mean_rho,
            std_rho,
            order_energy,
            rough,
            np.linalg.norm(Z["ell"]),
            np.linalg.norm(Z["a"]),
            np.linalg.norm(Z["n"]),
            np.linalg.norm(Z["v"]),
        ]
    )
    welford_update(measures)
    z = welford_z(measures)
    chi = np.zeros(16)
    chi[:8] = z
    chi[8:12] = Z["ell"][:4]
    chi[12:16] = 0.5 * (Z["a"] + Z["n"])
    chi = chi / (np.sqrt(np.mean(chi**2)) + 1e-8)
    return chi, {
        "mean_rho": mean_rho,
        "std_rho": std_rho,
        "order": order_energy,
        "rough": rough,
    }


def coupled_proposal(chi, Z_mid):
    ell = Z_mid["ell"]
    a = Z_mid["a"]
    n = Z_mid["n"]
    g = Z_mid["g"]
    v = Z_mid["v"]

    drive = np.tanh(chi[:8] + 0.2 * ell)
    prop_h = drive[:4]
    prop_b = drive[4:8]
    prop_a = np.tanh(chi[:4] + 0.3 * a + 0.1 * n)
    prop_n = np.tanh(chi[4:8] + 0.3 * n + 0.1 * a)
    prop_g = np.tanh(chi[:4] + 0.25 * g + 0.1 * Z_mid["b"])
    prop_ell = np.tanh(chi[:8] + 0.2 * ell + 0.05 * np.concatenate([a, n]))
    prop_v = np.tanh(np.concatenate([chi[2:8], chi[0:2]]) + 0.15 * v)

    radial = np.exp(-(X**2 + Y**2 + Zg**2) / (0.25 * L**2 + 1e-8))
    e0, e1, e2, e3 = ell[0], ell[1], ell[2], ell[3]
    v0, v1, v2, v3, v4, v5, v6, v7 = v

    Lambda_scalar = np.tanh(e0 + 0.3 * chi[0] + 0.2 * a[0])
    alpha_scalar = 0.5 * (1.0 + np.tanh(e1 + 0.3 * chi[1]))
    Gamma_scalar = 0.5 * (1.0 + np.tanh(e2 + 0.3 * chi[2]))
    eta_scalar = 0.5 * (1.0 + np.tanh(e3 + 0.3 * chi[3]))
    sigma_frac = 1.0 + 0.5 * np.tanh(v0 + chi[4])

    # frequências emergentes nas 3 direções + modos cruzados
    fx = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v0))
    fy = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v1))
    fz = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v2))
    fxy = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v3))
    fyz = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v4))
    fzx = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v5))

    # λ_j >= 0: memória repulsiva (anti-colapso), conforme a base
    lam = lambda e: 0.5 * (1.0 + np.tanh(e))
    V_mem = (
        lam(e0) * radial
        + lam(e1) * np.sin(fx * X + np.tanh(v6))
        + lam(e2) * np.sin(fy * Y + np.tanh(v7))
        + lam(e3) * np.sin(fz * Zg + np.tanh(v6 - v7))
        + 0.5 * lam(ell[4]) * np.cos(fxy * (X + Y))
        + 0.5 * lam(ell[5]) * np.cos(fyz * (Y + Zg))
        + 0.5 * lam(ell[6]) * np.cos(fzx * (Zg + X))
        + 0.3 * lam(a[0]) * np.sin(fx * Y - fy * X)
        + 0.3 * lam(a[1]) * np.sin(fy * Zg - fz * Y)
    )
    V_scale = 0.5 * (1.0 + np.tanh(g[0] + chi[5]))
    V_mem = V_scale * V_mem
    V_ext = 0.15 * np.tanh(g[1]) * (
        (X / (L / 2)) ** 2 + (Y / (L / 2)) ** 2 + (Zg / (L / 2)) ** 2
    )

    return {
        "h": prop_h,
        "b": prop_b,
        "a": prop_a,
        "n": prop_n,
        "g": prop_g,
        "ell": prop_ell,
        "v": prop_v,
        "Lambda": Lambda_scalar,
        "alpha": alpha_scalar,
        "Gamma": Gamma_scalar,
        "eta": eta_scalar,
        "sigma": sigma_frac,
        "V_mem": V_mem,
        "V_ext": V_ext,
    }


def psi_flow(psi, prop, dt):
    rho = np.abs(psi) ** 2
    V = prop["V_ext"] + prop["Lambda"] * rho + prop["V_mem"]
    psi_k = np.fft.fftn(psi)
    kinetic = np.fft.ifftn(-0.5 * K2 * psi_k)
    frac = prop["alpha"] * np.fft.ifftn((Kabs ** prop["sigma"]) * psi_k)
    # -iΓ dentro do colchete de iħ∂tΨ  →  contribuição -Γψ em ∂tΨ (dissipação real)
    damp = -prop["Gamma"] * 0.05 * psi
    noise = prop["eta"] * 0.02 * (
        np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N)
    )
    dpsi = -1j * (kinetic + V * psi + frac) + damp + noise
    return psi + dt * dpsi


def coupled_step(Z, dt=0.02, max_iter=5):
    Z0 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}
    Zcur = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}
    metrics = None
    prop = None
    for _ in range(max_iter):
        Zmid = {k: 0.5 * (Z0[k] + Zcur[k]) for k in Z0}
        chi, metrics = experience_signature(Zmid["psi"], Zmid)
        prop = coupled_proposal(chi, Zmid)
        keys = ["h", "b", "a", "n", "g", "ell", "v"]
        raw = {k: prop[k] - Zmid[k] for k in keys}
        stack = soft_bound(np.concatenate([raw[k] for k in keys]), cap=1.0)
        i0 = 0
        for k in keys:
            nsz = raw[k].size
            Zcur[k] = project_state_vector(Z0[k] + stack[i0 : i0 + nsz], radius=2.5)
            i0 += nsz
        psi_new = psi_flow(Zmid["psi"], prop, dt)
        Zcur["psi"] = psi_numeric_guard(psi_new)
        if np.linalg.norm(Zcur["ell"] - Zmid["ell"]) < 1e-3:
            break
    return Zcur, metrics, prop



# ================================================================ preparação
STEPS = int(os.environ.get("STEPS", 1200))
T_KICK = int(os.environ.get("T_KICK", STEPS // 3))
AMP = float(os.environ.get("AMP", 0.05))
N_BAT = 8            # batidas da música
W_SOM = 30           # janela (passos) pra gravar o som emitido
dt = 0.025

def clone_Z(Z):
    return {k: v.copy() for k, v in Z.items()}
def snap_w(w):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in w.items()}
def load_w(dst, srcw):
    for k, v in srcw.items():
        dst[k] = v.copy() if isinstance(v, np.ndarray) else v

print("Evoluindo o universo comum até t=%d..." % T_KICK)
for t in range(T_KICK):
    Z, mets, prop = coupled_step(Z, dt=dt)
    if t % 50 == 0:
        print("t=%4d | order=%.4f" % (t, mets["order"]))

rho0 = np.abs(Z["psi"]) ** 2

# nota mais forte do universo neste instante
F = np.fft.fftshift(np.abs(np.fft.fftn(rho0))) ** 2
F[N // 2, N // 2, N // 2] = 0.0
fl = np.argsort(F.ravel())[::-1]
menu = []
seen = set()
for fi in fl:
    ijk = np.unravel_index(fi, F.shape)
    kv = (np.array(ijk) - N // 2) * (2 * np.pi / L)
    key = tuple(np.round(np.abs(kv), 6))
    if key in seen:
        continue
    seen.add(key)
    menu.append(kv)
    if len(menu) >= N_BAT:
        break
# nota-guia: a mais forte do cardápio CUJO PERÍODO caiba na rodada
# (senão o compasso estoura o tempo da simulação e a música não acontece)
cabe = (STEPS - T_KICK) // (N_BAT + 1)
k_nota, T_beat = None, None
for kv in menu:
    knv = np.linalg.norm(kv)
    om = 0.5 * knv**2
    Tb = max(2, int(round((2 * np.pi / om) / dt)))
    if Tb <= cabe:
        k_nota, T_beat = kv, Tb
        break
if k_nota is None:                        # nenhuma cabe: usa a mais aguda do menu
    k_nota = menu[-1]
    T_beat = max(2, cabe)
kn = np.linalg.norm(k_nota)

# ponto onde a música é tocada: o pico mais forte
pk_m = np.unravel_index(np.argmax(rho0), rho0.shape)

# as "coisas": três picos afastados entre si
mxf = maximum_filter(rho0, size=5)
cand = np.argwhere((rho0 == mxf) & (rho0 > np.percentile(rho0, 90.0)))
cvals = rho0[cand[:, 0], cand[:, 1], cand[:, 2]]
cand = cand[np.argsort(cvals)[::-1]]
coisas = [cand[0]]
for c in cand[1:]:
    d = [np.linalg.norm(((c - o) * dx + L / 2) % L - L / 2) for o in coisas]
    if min(d) > 0.28 * L:
        coisas.append(c)
    if len(coisas) == 3:
        break
while len(coisas) < 3:                     # universo pouco estruturado: completa
    coisas.append(cand[len(coisas)])
# segunda batida na MESMA coisa A, num ponto vizinho (2 voxels ao lado)
coisaA2 = (coisas[0] + np.array([2, 0, 0])) % N

rng2 = np.random.default_rng(SEED + 1)     # sorteios do experimento, fora do ruído
t_beats = [T_KICK + m * T_beat for m in range(N_BAT)]
t_solto = sorted(rng2.integers(T_KICK, T_KICK + (N_BAT - 1) * T_beat + 1,
                               size=N_BAT).tolist())
ordem_emb = rng2.permutation(N_BAT)

def envelope_em(ijk, w=2.5):
    cx, cy, cz = (np.array(ijk) * dx) - L / 2
    ddx = (X - cx + L / 2) % L - L / 2
    ddy = (Y - cy + L / 2) % L - L / 2
    ddz = (Zg - cz + L / 2) % L - L / 2
    return np.exp(-(ddx**2 + ddy**2 + ddz**2) / (2 * w**2)), (ddx, ddy, ddz)

env_m, dd_m = envelope_em(pk_m)
def toca(psi, kv):
    onda = np.cos(kv[0] * dd_m[0] + kv[1] * dd_m[1] + kv[2] * dd_m[2])
    return psi * (1.0 + AMP * onda * env_m)

print("nota-guia: |k|=%.2f (λ=%.1f)  período=%d passos | música em %s"
      % (kn, 2 * np.pi / kn, T_beat, t_beats))
print("coisas batidas: %s + segunda batida em A2=%s"
      % ([tuple(int(v) for v in c) for c in coisas], tuple(int(v) for v in coisaA2)))

# 8 gêmeas
nomes = ["silencio", "musica", "embaralhada", "semritmo",
         "coisaA", "coisaA2", "coisaB", "coisaC"]
gem = {n: clone_Z(Z) for n in nomes}
ws = {n: snap_w(welford) for n in nomes}

# batida seca nas coisas (bump curto, sem nota) — só uma vez, agora
for nome, ijk in [("coisaA", coisas[0]), ("coisaA2", coisaA2),
                  ("coisaB", coisas[1]), ("coisaC", coisas[2])]:
    e_, _ = envelope_em(ijk, w=1.2)
    gem[nome]["psi"] = gem[nome]["psi"] * (1.0 + AMP * e_)

# espectro radial (pra gravar o som emitido)
k1f = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KXf, KYf, KZf = np.meshgrid(k1f, k1f, k1f, indexing="ij")
Kb = np.sqrt(KXf**2 + KYf**2 + KZf**2)
NB = 22
kedges = np.linspace(0, Kb.max(), NB + 1)
kbin = np.clip(np.digitize(Kb.ravel(), kedges) - 1, 0, NB - 1)
kcent = 0.5 * (kedges[:-1] + kedges[1:])
def espectro_radial(dpsi):
    P = (np.abs(np.fft.fftn(dpsi)) ** 2).ravel()
    s = np.zeros(NB); np.add.at(s, kbin, P)
    return s

som = {n: np.zeros(NB) for n in ["coisaA", "coisaA2", "coisaB", "coisaC"]}
hist = {n: [] for n in ["musica", "embaralhada", "semritmo"]}
ht = []
mus_idx = 0

for t in range(T_KICK, STEPS):
    st = np.random.get_state()
    for n in nomes:
        np.random.set_state(st)
        load_w(welford, ws[n])
        gem[n], mets, prop = coupled_step(gem[n], dt=dt)
        ws[n] = snap_w(welford)

    # as batidas da música / embaralhada / sem ritmo
    if t in t_beats:
        m = t_beats.index(t)
        gem["musica"]["psi"] = toca(gem["musica"]["psi"], k_nota)
        gem["embaralhada"]["psi"] = toca(gem["embaralhada"]["psi"],
                                         menu[ordem_emb[m]])
    for _ in range(t_solto.count(t)):
        gem["semritmo"]["psi"] = toca(gem["semritmo"]["psi"], k_nota)

    ht.append(t)
    for n in ["musica", "embaralhada", "semritmo"]:
        D = np.abs(gem["silencio"]["psi"] - gem[n]["psi"]) ** 2
        hist[n].append(np.sum(D) * dV)
    if t - T_KICK < W_SOM:
        for n in som:
            som[n] += espectro_radial(gem["silencio"]["psi"] - gem[n]["psi"])

    if t % 50 == 0:
        print("t=%4d | Δmúsica=%.2e  Δembaralhada=%.2e  Δsem-ritmo=%.2e"
              % (t, hist["musica"][-1], hist["embaralhada"][-1],
                 hist["semritmo"][-1]))

os.makedirs("bravais_outputs_3d", exist_ok=True)
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
htt = (np.array(ht) - T_KICK) * dt

# ================================================================ figura 1: música
fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
cores = {"musica": "#ee6c4d", "embaralhada": "#f4d35e", "semritmo": "#5bc0be"}
rot = {"musica": "música (nota própria, no ritmo próprio)",
       "embaralhada": "embaralhada (notas sorteadas, mesmos instantes)",
       "semritmo": "sem ritmo (mesma nota, instantes sorteados)"}
ax = axes[0]
for n in hist:
    ax.semilogy(htt, np.array(hist[n]) + 1e-300, color=cores[n], label=rot[n])
for tb in t_beats:
    ax.axvline((tb - T_KICK) * dt, color="gray", lw=0.5, alpha=0.4)
ax.set_xlabel("tempo desde a primeira batida")
ax.set_ylabel("quanto o universo mudou (vs silêncio)")
ax.set_title("as 8 batidas (linhas cinzas = compasso da música)", fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)
ax = axes[1]
finais = [hist[n][-1] for n in ["musica", "embaralhada", "semritmo"]]
ax.bar(range(3), finais, color=[cores[n] for n in ["musica", "embaralhada", "semritmo"]])
ax.set_xticks(range(3), ["música", "embaralhada", "sem ritmo"])
ax.set_ylabel("mudança final")
ax.set_title("resultado final de cada jeito de tocar", fontsize=10)
ax.grid(alpha=0.3, axis="y")
plt.suptitle("Teste da música — a ordem e o ritmo importam?", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/musica_curvas.png", dpi=150, bbox_inches="tight")
plt.close()
print("musica_curvas.png")

# ================================================================ figura 2: batida nas coisas
rotb = {"coisaA": "coisa A", "coisaA2": "coisa A (2º ponto)",
        "coisaB": "coisa B", "coisaC": "coisa C"}
coresb = {"coisaA": "#ee6c4d", "coisaA2": "#f4a261",
          "coisaB": "#5bc0be", "coisaC": "#3a506b"}
sn = {n: som[n] / (som[n].sum() + 1e-30) for n in som}
nomes_b = ["coisaA", "coisaA2", "coisaB", "coisaC"]
sim = np.zeros((4, 4))
for i, a in enumerate(nomes_b):
    for j, b in enumerate(nomes_b):
        sim[i, j] = np.dot(sn[a], sn[b]) / (
            np.linalg.norm(sn[a]) * np.linalg.norm(sn[b]) + 1e-30)

fig, axes = plt.subplots(1, 2, figsize=(13.5, 4.8))
ax = axes[0]
for n in nomes_b:
    ax.plot(kcent, sn[n], color=coresb[n], label="%s  (número: |k|≈%.2f)"
            % (rotb[n], kcent[np.argmax(sn[n])]), lw=2 if n != "coisaA2" else 1.2,
            ls="-" if n != "coisaA2" else "--")
ax.set_xlabel("|k| (a nota emitida)"); ax.set_ylabel("fração do som")
ax.set_title("o som que cada coisa emitiu ao ser batida\n"
             "(espectro da resposta nos %d primeiros passos)" % W_SOM, fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)
ax = axes[1]
im = ax.imshow(sim, cmap=cmap_life, vmin=min(0.90, sim.min()), vmax=1.0)
plt.colorbar(im, ax=ax, label="semelhança dos sons")
ax.set_xticks(range(4), [rotb[n] for n in nomes_b], fontsize=8, rotation=20)
ax.set_yticks(range(4), [rotb[n] for n in nomes_b], fontsize=8)
for i in range(4):
    for j in range(4):
        ax.text(j, i, "%.3f" % sim[i, j], ha="center", va="center",
                color="white", fontsize=8)
ax.set_title("cada coisa tem seu número?\n(A vs A-2º ponto deve ser o par "
             "mais parecido)", fontsize=10)
plt.suptitle("Teste da batida — bater na coisa e ouvir o número dela", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/batida_numeros.png", dpi=150, bbox_inches="tight")
plt.close()
print("batida_numeros.png")

# ================================================================ resumo
print("\n===== RESULTADO — MÚSICA =====")
for n in ["musica", "embaralhada", "semritmo"]:
    print("  %-12s mudança final = %.3e" % (n, hist[n][-1]))
print("  música / embaralhada = %.2f×   música / sem-ritmo = %.2f×"
      % (hist["musica"][-1] / (hist["embaralhada"][-1] + 1e-300),
         hist["musica"][-1] / (hist["semritmo"][-1] + 1e-300)))
print("\n===== RESULTADO — BATIDA =====")
for n in nomes_b:
    print("  %-18s número dominante |k| ≈ %.2f" % (rotb[n], kcent[np.argmax(sn[n])]))
print("  semelhança A vs A(2º ponto): %.4f" % sim[0, 1])
print("  semelhança A vs B: %.4f | A vs C: %.4f | B vs C: %.4f"
      % (sim[0, 2], sim[0, 3], sim[2, 3]))
