#!/usr/bin/env python3
"""
Teste da pancada — "tudo e um"?
===============================
Duas simulacoes GEMEAS, identicas ate no ruido (mesma semente, mesmo
sorteio a cada passo). A dinamica e IDENTICA ao bravais_puro_3d.py:
mesma proposta acoplada, todos os termos juntos, nada isolado, nada
calibrado. A UNICA diferenca entre as gemeas: num instante escolhido,
a gemea B leva um beliscao de amplitude num unico filamento (o pico
mais forte da densidade). Nada na equacao muda — so o estado, uma vez.

Dai em diante mede-se |Psi_A - Psi_B|^2: a onda de influencia.

Perguntas que o teste responde com numero:
  - a influencia se espalha pelo volume inteiro ou fica presa perto
    do beliscao?  (fracao do volume tocada ao final)
  - com que velocidade a frente avanca?  (raio R90 vs tempo)
  - quanto do campo distante sente?  (perfil radial da diferenca)

Uso:
  python3 teste_pancada.py                          (N=64, 1200 passos)
  N=48 STEPS=400 python3 teste_pancada.py           (teste rapido)
  AMP=0.3 T_KICK=um_terco_dos_passos por padrao; ajuste por env se quiser.
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
import copy
import imageio.v2 as imageio

STEPS = int(os.environ.get("STEPS", 1200))
T_KICK = int(os.environ.get("T_KICK", STEPS // 3))
AMP = float(os.environ.get("AMP", 0.3))
dt = 0.025
N_SNAP = 40

def clone_Z(Z):
    return {k: v.copy() for k, v in Z.items()}

def snap_w(w):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in w.items()}

def load_w(dst, srcw):
    for k, v in srcw.items():
        dst[k] = v.copy() if isinstance(v, np.ndarray) else v

Z_A = clone_Z(Z)
Z_B = clone_Z(Z)
w_A = snap_w(welford)
w_B = snap_w(welford)

print("Teste da pancada | N=%d  passos=%d  beliscão em t=%d  amp=%.2f  semente=%d"
      % (N, STEPS, T_KICK, AMP, SEED))

# distância ao ponto do beliscão (imagem mínima periódica) — definida no kick
dist = None
kick_ijk = None

hist = {"t": [], "total": [], "r90": [], "frac": []}
snaps, snap_t = [], []
snap_at = set(np.linspace(T_KICK, STEPS - 1, N_SNAP).astype(int))

for t in range(STEPS):
    st = np.random.get_state()
    load_w(welford, w_A)
    Z_A, mA, pA = coupled_step(Z_A, dt=dt)
    w_A = snap_w(welford)

    np.random.set_state(st)          # gêmea B recebe EXATAMENTE o mesmo sorteio
    load_w(welford, w_B)
    Z_B, mB, pB = coupled_step(Z_B, dt=dt)
    w_B = snap_w(welford)

    if t == T_KICK:
        rho_B = np.abs(Z_B["psi"]) ** 2
        kick_ijk = np.unravel_index(np.argmax(rho_B), rho_B.shape)
        cx, cy, cz = (np.array(kick_ijk) * dx) - L / 2
        # imagem mínima periódica
        ddx = (X - cx + L / 2) % L - L / 2
        ddy = (Y - cy + L / 2) % L - L / 2
        ddz = (Zg - cz + L / 2) % L - L / 2
        dist = np.sqrt(ddx**2 + ddy**2 + ddz**2)
        bump = 1.0 + AMP * np.exp(-dist**2 / (2 * 1.5**2))
        Z_B["psi"] = Z_B["psi"] * bump
        print("t=%4d | BELISCÃO no pico em (%.1f, %.1f, %.1f)" % (t, cx, cy, cz))

    if t >= T_KICK and dist is not None:
        D = np.abs(Z_A["psi"] - Z_B["psi"]) ** 2
        total = np.sum(D) * dV
        # raio que contém 90% da diferença
        o = np.argsort(dist.ravel())
        cum = np.cumsum(D.ravel()[o])
        r90 = dist.ravel()[o][np.searchsorted(cum, 0.90 * cum[-1])] if cum[-1] > 0 else 0.0
        ref = np.mean(np.abs(Z_A["psi"]) ** 2)
        frac = np.mean(D > 1e-4 * ref)
        hist["t"].append(t); hist["total"].append(total)
        hist["r90"].append(r90); hist["frac"].append(frac)
        if t in snap_at:
            snaps.append(D[:, :, kick_ijk[2]].astype(np.float32))
            snap_t.append(t)

    if t % 50 == 0:
        extra = ""
        if hist["t"]:
            extra = " | Δtotal=%.2e  R90=%.1f  vol.tocado=%.0f%%" % (
                hist["total"][-1], hist["r90"][-1], 100 * hist["frac"][-1])
        print("t=%4d | order=%.4f%s" % (t, mA["order"], extra))

os.makedirs("bravais_outputs_3d", exist_ok=True)

# ================================================================ gráficos
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
ht = np.array(hist["t"]); tot = np.array(hist["total"])
r90 = np.array(hist["r90"]); frac = np.array(hist["frac"])

fig, axes = plt.subplots(1, 3, figsize=(15, 4.6))
axes[0].semilogy(ht, tot + 1e-30, color="#ee6c4d")
axes[0].set_title("tamanho total da diferença entre as gêmeas")
axes[0].set_xlabel("passo"); axes[0].grid(alpha=0.3)
axes[1].plot(ht, r90, color="#5bc0be")
axes[1].axhline(L / 2 * np.sqrt(3) * 0.9, ls=":", color="gray",
                label="≈ alcance máximo na caixa")
axes[1].set_title("R90 — raio que contém 90% da diferença")
axes[1].set_xlabel("passo"); axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)
axes[2].plot(ht, 100 * frac, color="#f4d35e")
axes[2].set_ylim(0, 105)
axes[2].set_title("%% do volume que já sentiu o beliscão")
axes[2].set_xlabel("passo"); axes[2].grid(alpha=0.3)
plt.suptitle("Teste da pancada — a influência de UM filamento sobre o resto "
             "(gêmeas idênticas até no ruído)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/pancada_curvas.png", dpi=150, bbox_inches="tight")
plt.close()
print("pancada_curvas.png")

# filme da onda de influência (fatia no plano do beliscão)
frames = []
vmax = max(np.percentile(s, 99.5) for s in snaps) + 1e-30
for s_, t_ in zip(snaps, snap_t):
    fig, ax = plt.subplots(figsize=(6.6, 6.2))
    ax.imshow(np.log10(s_.T + 1e-12), origin="lower", cmap="inferno",
              extent=[-L / 2, L / 2, -L / 2, L / 2],
              vmin=np.log10(1e-12), vmax=np.log10(vmax))
    ax.plot((kick_ijk[0] * dx) - L / 2, (kick_ijk[1] * dx) - L / 2,
            "o", ms=10, mfc="none", mec="#43e6e0", mew=2)
    ax.set_title("onda de influência — t = %d  (log da diferença; "
                 "círculo = beliscão)" % t_, fontsize=10)
    ax.tick_params(labelsize=7)
    fig.tight_layout()
    fig.canvas.draw()
    frames.append(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
frames += [frames[-1]] * 6
imageio.mimsave("bravais_outputs_3d/pancada_onda.gif", frames,
                duration=0.15, loop=0)
print("pancada_onda.gif")

# ================================================================ resumo
print("\n===== RESULTADO =====")
print("volume tocado ao final: %.1f%%" % (100 * frac[-1]))
print("R90 final: %.1f  (máximo possível ≈ %.1f)" % (r90[-1], L / 2 * np.sqrt(3)))
if len(r90) > 10:
    vel = np.polyfit(ht[:len(ht)//2] * dt, r90[:len(ht)//2], 1)[0]
    print("velocidade média da frente (primeira metade): %.2f unidades de espaço "
          "por unidade de tempo" % vel)
print("interpretação: se o volume tocado se aproxima de 100%% e o R90 satura no")
print("tamanho da caixa, a influência de um filamento alcançou tudo — dentro")
print("deste mundo simulado, 'um toca todos'. Se ficou local, não alcançou.")
