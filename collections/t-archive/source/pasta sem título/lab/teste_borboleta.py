#!/usr/bin/env python3
"""
Teste da borboleta — uma nota tocada num ponto do universo
==========================================================
Dinamica IDENTICA ao bravais_puro_3d.py (todos os termos juntos, nada
isolado, nada calibrado). Quatro gemeas identicas ate no ruido (mesma
semente, mesmo sorteio a cada passo). Em t=T_KICK, tres delas recebem
uma NOTA: uma ondinha com o comprimento de onda da nota mais forte do
proprio universo, envelopada num ponto, com amplitudes decrescentes
(EPS, EPS/100, EPS/10000). A quarta segue intocada (referencia).

Tres perguntas com numero:
  1. BORBOLETA — a diferenca cresce exponencialmente? (reta no log,
     inclinacao = expoente de Lyapunov deste mundo). A nota mais fraca
     tambem acaba mudando tudo, so mais tarde?
  2. ACAO E REACAO — a diferenca sai do ponto tocado (acao) e o
     universo responde de volta no mesmo ponto (eco/reacao)?
  3. CONTAMINACAO — a diferenca comeca na nota tocada e vaza para o
     acorde inteiro?

Uso:
  python3 teste_borboleta.py                 (N=64, 1200 passos)
  N=48 STEPS=400 python3 teste_borboleta.py  (teste rapido)
  EPS=0.01 T_KICK=... por env se quiser.
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



# ================================================================ gêmeas
STEPS = int(os.environ.get("STEPS", 1200))
T_KICK = int(os.environ.get("T_KICK", STEPS // 3))
EPS = float(os.environ.get("EPS", 1e-2))
dt = 0.025
EPSILONS = [EPS, EPS / 100.0, EPS / 10000.0]
NOMES = ["forte (%.0e)" % EPSILONS[0], "fraca (%.0e)" % EPSILONS[1],
         "quase nada (%.0e)" % EPSILONS[2]]
CORES = ["#ee6c4d", "#f4d35e", "#5bc0be"]

def clone_Z(Z):
    return {k: v.copy() for k, v in Z.items()}

def snap_w(w):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in w.items()}

def load_w(dst, srcw):
    for k, v in srcw.items():
        dst[k] = v.copy() if isinstance(v, np.ndarray) else v

# gêmea 0 = referência; 1..3 = tocadas
gem = [clone_Z(Z) for _ in range(4)]
ws = [snap_w(welford) for _ in range(4)]

print("Teste da borboleta | N=%d  passos=%d  nota em t=%d  amplitudes=%s"
      % (N, STEPS, T_KICK, EPSILONS))

dist = None
kick_ijk = None
k_nota = None
hist = {"t": [], "tot": [[], [], []], "loc": [[], [], []], "pureza": [[], [], []]}
shell = None

for t in range(STEPS):
    st = np.random.get_state()
    for g in range(4):
        np.random.set_state(st)      # todas recebem EXATAMENTE o mesmo sorteio
        load_w(welford, ws[g])
        gem[g], mets, prop = coupled_step(gem[g], dt=dt)
        ws[g] = snap_w(welford)

    if t == T_KICK:
        rho0 = np.abs(gem[0]["psi"]) ** 2
        # a nota mais forte do próprio universo neste instante
        F = np.fft.fftshift(np.abs(np.fft.fftn(rho0))) ** 2
        F[N // 2, N // 2, N // 2] = 0.0
        ijk = np.unravel_index(np.argmax(F), F.shape)
        k_nota = (np.array(ijk) - N // 2) * (2 * np.pi / L)
        kn = np.linalg.norm(k_nota)
        # ponto do universo: o pico de densidade
        kick_ijk = np.unravel_index(np.argmax(rho0), rho0.shape)
        cx, cy, cz = (np.array(kick_ijk) * dx) - L / 2
        ddx = (X - cx + L / 2) % L - L / 2
        ddy = (Y - cy + L / 2) % L - L / 2
        ddz = (Zg - cz + L / 2) % L - L / 2
        dist = np.sqrt(ddx**2 + ddy**2 + ddz**2)
        envelope = np.exp(-dist**2 / (2 * 2.5**2))
        onda = np.cos(k_nota[0] * ddx + k_nota[1] * ddy + k_nota[2] * ddz)
        for g, eps in enumerate(EPSILONS, start=1):
            gem[g]["psi"] = gem[g]["psi"] * (1.0 + eps * onda * envelope)
        # casca espectral da nota (pra medir pureza da diferença)
        k1f = np.fft.fftfreq(N, d=dx) * 2 * np.pi
        KXf, KYf, KZf = np.meshgrid(k1f, k1f, k1f, indexing="ij")
        Kb = np.sqrt(KXf**2 + KYf**2 + KZf**2)
        shell = np.abs(Kb - kn) < (2 * np.pi / L)
        print("t=%4d | NOTA tocada: |k|=%.2f (λ=%.1f) no ponto (%.1f, %.1f, %.1f)"
              % (t, kn, 2 * np.pi / kn, cx, cy, cz))

    if t > T_KICK:
        hist["t"].append(t)
        perto = dist < 3.0
        for g in range(1, 4):
            D = np.abs(gem[0]["psi"] - gem[g]["psi"]) ** 2
            hist["tot"][g - 1].append(np.sum(D) * dV)
            hist["loc"][g - 1].append(np.mean(D[perto]))
            Fd = np.abs(np.fft.fftn(gem[0]["psi"] - gem[g]["psi"])) ** 2
            hist["pureza"][g - 1].append(np.sum(Fd[shell]) / (np.sum(Fd) + 1e-30))

    if t % 50 == 0:
        ex = ""
        if hist["t"]:
            ex = " | Δ: %.1e / %.1e / %.1e" % tuple(h[-1] for h in hist["tot"])
        print("t=%4d | order=%.4f%s" % (t, mets["order"], ex))

os.makedirs("bravais_outputs_3d", exist_ok=True)
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
ht = np.array(hist["t"]) * dt

fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

# ---- 1) borboleta: crescimento em log
ax = axes[0]
lyap = []
for i in range(3):
    tot = np.array(hist["tot"][i]) + 1e-300
    ax.semilogy(ht, tot, color=CORES[i], label="nota " + NOMES[i])
    # ajuste exponencial na fase de crescimento (entre 1% e 60% do máximo)
    lt = np.log(tot)
    m = (tot > tot.max() * 0.01) & (tot < tot.max() * 0.6) & (ht < ht[np.argmax(tot)])
    if m.sum() > 5:
        lyap.append(np.polyfit(ht[m], lt[m], 1)[0])
ax.set_xlabel("tempo desde a nota"); ax.set_ylabel("tamanho da diferença")
ax.set_title("1) borboleta — reta no log = crescimento exponencial\n"
             + ("expoente(s) de Lyapunov ≈ " +
                ", ".join("%.2f" % l for l in lyap) if lyap else ""), fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# ---- 2) ação e reação: eco no ponto tocado
ax = axes[1]
for i in range(3):
    loc = np.array(hist["loc"][i])
    ax.semilogy(ht, loc + 1e-300, color=CORES[i], label=NOMES[i])
ax.set_xlabel("tempo desde a nota")
ax.set_ylabel("diferença NO ponto tocado")
ax.set_title("2) ação e reação — queda = a nota partiu;\n"
             "subida depois = o universo respondeu no mesmo ponto (eco)",
             fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)

# ---- 3) contaminação do acorde
ax = axes[2]
for i in range(3):
    ax.plot(ht, 100 * np.array(hist["pureza"][i]), color=CORES[i], label=NOMES[i])
ax.set_xlabel("tempo desde a nota")
ax.set_ylabel("% da diferença ainda na nota tocada")
ax.set_ylim(0, 105)
ax.set_title("3) contaminação — 100% = diferença pura na nota;\n"
             "caindo = vazou para o acorde inteiro", fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)

plt.suptitle("Teste da borboleta — uma nota tocada num ponto do universo "
             "(4 gêmeas, mesma equação, mesmo ruído)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/borboleta_curvas.png", dpi=150, bbox_inches="tight")
plt.close()
print("borboleta_curvas.png")

# ================================================================ resumo
print("\n===== RESULTADO =====")
for i in range(3):
    tot = np.array(hist["tot"][i])
    loc = np.array(hist["loc"][i])
    ratio = tot[-1] / (tot[0] + 1e-300)
    print("nota %s: diferença cresceu %.1e vezes; final=%.2e" %
          (NOMES[i], ratio, tot[-1]))
if lyap:
    print("expoente de Lyapunov ≈ %s por unidade de tempo" %
          ", ".join("%.2f" % l for l in lyap))
    print("(positivo = caos: efeito borboleta confirmado NESTE mundo)")
print("pureza final da diferença na nota tocada: %s" %
      ", ".join("%.0f%%" % (100 * hist["pureza"][i][-1]) for i in range(3)))
