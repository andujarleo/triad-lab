#!/usr/bin/env python3
"""
Teste da ligacao — duas "pessoas" afastadas se sentem?
======================================================
Dinamica IDENTICA ao bravais_puro_3d.py (todos os termos juntos, nada
isolado, nada calibrado). Quatro gemeas identicas ate no ruido.

Traducao da hipotese:
  pessoas  = coisas do universo (estruturas de densidade)
  numero   = impressao digital de notas de cada coisa
  ligacao  = par de coisas AFASTADAS com numeros parecidos (parentes)

No universo evoluido, encontra-se:
  A = a coisa que sera batida
  P = a PARCEIRA: coisa afastada com o numero mais parecido com A
  E = a ESTRANHA: coisa a distancia comparavel com o numero mais
      diferente possivel

Gemeas: silencio | batida seca em A | batida em A chamando o nome de P
        (modulada com a nota dominante de P) | batida chamando o nome de E.

Mede-se, a cada passo, o que cada uma sente (mudanca local vs silencio):
  P, E, e o FUNDO a mesma distancia (o resto do mundo entre elas).

Perguntas:
  1. P sente mais que E e que o fundo?  (ligacao especifica, nao so
     "tudo e ligado")
  2. P sente mais quando a batida chama o nome DELA?  (ligacao
     enderecavel: mensagem para alguem especifico)

Uso:
  python3 teste_ligacao.py                 (N=64, 1200 passos)
  N=48 STEPS=400 python3 teste_ligacao.py  (teste rapido)
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

# cardápio de notas do universo
F = np.fft.fftshift(np.abs(np.fft.fftn(rho0))) ** 2
F[N // 2, N // 2, N // 2] = 0.0
fl = np.argsort(F.ravel())[::-1]
menu, seen = [], set()
for fi in fl:
    ijk = np.unravel_index(fi, F.shape)
    kv = (np.array(ijk) - N // 2) * (2 * np.pi / L)
    key = tuple(np.round(np.abs(kv), 6))
    if key in seen:
        continue
    seen.add(key)
    menu.append(kv)
    if len(menu) >= 12:
        break

# as coisas (picos) e seus números (impressão digital de notas)
mxf = maximum_filter(rho0, size=5)
cand = np.argwhere((rho0 == mxf) & (rho0 > np.percentile(rho0, 88.0)))
cvals = rho0[cand[:, 0], cand[:, 1], cand[:, 2]]
cand = cand[np.argsort(cvals)[::-1]][:40]

def pos_de(ijk):
    return np.array(ijk) * dx - L / 2

def dist_per(p, q):
    d = (p - q + L / 2) % L - L / 2
    return np.linalg.norm(d)

def digital(ijk, raio=3.0):
    """Número da coisa: projeção da vizinhança dela nas 12 notas do menu."""
    c = pos_de(ijk)
    ddx = (X - c[0] + L / 2) % L - L / 2
    ddy = (Y - c[1] + L / 2) % L - L / 2
    ddz = (Zg - c[2] + L / 2) % L - L / 2
    m = (ddx**2 + ddy**2 + ddz**2) < raio**2
    w = rho0[m]; xs = ddx[m]; ys = ddy[m]; zs = ddz[m]
    f = np.array([np.abs(np.sum(w * np.exp(-1j * (kv[0] * xs + kv[1] * ys
                                                  + kv[2] * zs)))) for kv in menu])
    return f / (np.linalg.norm(f) + 1e-30)

digs = [digital(c) for c in cand]

# A = coisa mais forte; P = parceira (parecida e longe); E = estranha
A_i = 0
pA = pos_de(cand[A_i])
melhor, pior = None, None
for j in range(1, len(cand)):
    d = dist_per(pA, pos_de(cand[j]))
    if d < 0.30 * L:
        continue
    s = float(np.dot(digs[A_i], digs[j]))
    if melhor is None or s > melhor[1]:
        melhor = (j, s, d)
    if pior is None or s < pior[1]:
        pior = (j, s, d)
P_i, simP, dP = melhor
E_i, simE, dE = pior
pP, pE = pos_de(cand[P_i]), pos_de(cand[E_i])
nota_P = menu[int(np.argmax(digs[P_i]))]
nota_E = menu[int(np.argmax(digs[E_i]))]
print("A em (%.1f, %.1f, %.1f)" % tuple(pA))
print("P (parceira): distância %.1f, semelhança de número %.3f" % (dP, simP))
print("E (estranha): distância %.1f, semelhança de número %.3f" % (dE, simE))

# máscaras de escuta: bola em P, bola em E, e anéis de fundo às mesmas distâncias
def bola(c, r=2.0):
    ddx = (X - c[0] + L / 2) % L - L / 2
    ddy = (Y - c[1] + L / 2) % L - L / 2
    ddz = (Zg - c[2] + L / 2) % L - L / 2
    return (ddx**2 + ddy**2 + ddz**2) < r**2

ddxA = (X - pA[0] + L / 2) % L - L / 2
ddyA = (Y - pA[1] + L / 2) % L - L / 2
ddzA = (Zg - pA[2] + L / 2) % L - L / 2
distA = np.sqrt(ddxA**2 + ddyA**2 + ddzA**2)
bP, bE = bola(pP), bola(pE)
anelP = (np.abs(distA - dP) < 1.0) & ~bP & ~bE
anelE = (np.abs(distA - dE) < 1.0) & ~bP & ~bE

# batidas em A
envA = np.exp(-distA**2 / (2 * 1.2**2))
def bate(psi, kv=None):
    mod = 1.0 if kv is None else np.cos(kv[0] * ddxA + kv[1] * ddyA + kv[2] * ddzA)
    return psi * (1.0 + AMP * mod * envA)

nomes = ["silencio", "seca", "chamaP", "chamaE"]
gem = {n: clone_Z(Z) for n in nomes}
ws = {n: snap_w(welford) for n in nomes}
gem["seca"]["psi"] = bate(gem["seca"]["psi"])
gem["chamaP"]["psi"] = bate(gem["chamaP"]["psi"], nota_P)
gem["chamaE"]["psi"] = bate(gem["chamaE"]["psi"], nota_E)

sent = {n: {"P": [], "E": [], "fundoP": [], "fundoE": []}
        for n in ["seca", "chamaP", "chamaE"]}
ht = []

for t in range(T_KICK, STEPS):
    st = np.random.get_state()
    for n in nomes:
        np.random.set_state(st)
        load_w(welford, ws[n])
        gem[n], mets, prop = coupled_step(gem[n], dt=dt)
        ws[n] = snap_w(welford)
    ht.append(t)
    for n in ["seca", "chamaP", "chamaE"]:
        D = np.abs(gem["silencio"]["psi"] - gem[n]["psi"]) ** 2
        sent[n]["P"].append(np.mean(D[bP]))
        sent[n]["E"].append(np.mean(D[bE]))
        sent[n]["fundoP"].append(np.mean(D[anelP]))
        sent[n]["fundoE"].append(np.mean(D[anelE]))
    if t % 50 == 0:
        s = sent["seca"]
        print("t=%4d | P sente %.2e (fundo %.2e) | E sente %.2e (fundo %.2e)"
              % (t, s["P"][-1], s["fundoP"][-1], s["E"][-1], s["fundoE"][-1]))

os.makedirs("bravais_outputs_3d", exist_ok=True)
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
htt = (np.array(ht) - T_KICK) * dt

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

ax = axes[0]
s = sent["seca"]
ax.semilogy(htt, np.array(s["P"]) + 1e-300, color="#ee6c4d",
            label="P, a parceira (semelhança %.2f, dist %.1f)" % (simP, dP))
ax.semilogy(htt, np.array(s["E"]) + 1e-300, color="#3a506b",
            label="E, a estranha (semelhança %.2f, dist %.1f)" % (simE, dE))
ax.semilogy(htt, np.array(s["fundoP"]) + 1e-300, color="#aab2c8", ls="--",
            label="fundo à distância de P")
ax.semilogy(htt, np.array(s["fundoE"]) + 1e-300, color="#c9c2a6", ls=":",
            label="fundo à distância de E")
ax.set_xlabel("tempo desde a batida em A")
ax.set_ylabel("quanto cada uma sentiu")
ax.set_title("1) batida seca em A — quem sente do outro lado?", fontsize=10)
ax.legend(fontsize=7); ax.grid(alpha=0.3)

ax = axes[1]
razP = np.array(s["P"]) / (np.array(s["fundoP"]) + 1e-300)
razE = np.array(s["E"]) / (np.array(s["fundoE"]) + 1e-300)
ax.plot(htt, razP, color="#ee6c4d", label="P / fundo à mesma distância")
ax.plot(htt, razE, color="#3a506b", label="E / fundo à mesma distância")
ax.axhline(1.0, color="gray", lw=0.8)
ax.set_xlabel("tempo desde a batida em A")
ax.set_ylabel("sentiu ÷ fundo")
ax.set_title("2) especificidade — acima de 1 = sente mais\n"
             "que o resto do mundo à mesma distância", fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)

ax = axes[2]
pP_seca = np.array(sent["seca"]["P"])
pP_nome = np.array(sent["chamaP"]["P"])
pP_outro = np.array(sent["chamaE"]["P"])
ax.semilogy(htt, pP_nome + 1e-300, color="#ee6c4d",
            label="batida chamando o nome de P")
ax.semilogy(htt, pP_outro + 1e-300, color="#f4d35e",
            label="batida chamando o nome de E")
ax.semilogy(htt, pP_seca + 1e-300, color="#5bc0be", label="batida seca")
ax.set_xlabel("tempo desde a batida em A")
ax.set_ylabel("quanto P sentiu")
ax.set_title("3) endereçamento — P sente mais quando\né o nome DELA na batida?",
             fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)

plt.suptitle("Teste da ligação — A é batida; P (número parecido) e E (número "
             "diferente) escutam do outro lado do universo", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/ligacao_curvas.png", dpi=150, bbox_inches="tight")
plt.close()
print("ligacao_curvas.png")

# ================================================================ resumo
mid = len(htt) // 3
print("\n===== RESULTADO =====")
print("média do terço final (batida seca):")
print("  P sentiu %.2e | fundo à mesma distância %.2e | razão %.2f"
      % (pP_seca[-mid:].mean(), np.array(s["fundoP"])[-mid:].mean(),
         razP[-mid:].mean()))
print("  E sentiu %.2e | fundo à mesma distância %.2e | razão %.2f"
      % (np.array(s["E"])[-mid:].mean(), np.array(s["fundoE"])[-mid:].mean(),
         razE[-mid:].mean()))
print("endereçamento (o que P sentiu, média do terço final):")
print("  chamando o nome de P: %.2e | de E: %.2e | seca: %.2e"
      % (pP_nome[-mid:].mean(), pP_outro[-mid:].mean(), pP_seca[-mid:].mean()))
print("  nome-de-P / nome-de-E = %.2f×" %
      (pP_nome[-mid:].mean() / (pP_outro[-mid:].mean() + 1e-300)))
