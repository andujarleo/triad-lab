#!/usr/bin/env python3
"""
Teste: cada atomo e 1 corda?
============================
Dinamica IDENTICA ao bravais_puro_3d.py — a equacao completa
i·hbar·dt Psi = [-hbar²/2m ∇² + V_ext + Λ|Psi|² + V_mem + α(-Δ)^σ/2 - iΓ]Psi + η
todos os termos juntos, nada isolado, nada calibrado, nada inventado.
Uma rodada cheia; a analise usa os criterios DOS SCRIPTS DO REPO:
  atomos          = picos (maximum_filter 5, topo 1%)  [bravais_puro_3d.py]
  cordas densid.  = topo 3%% conexo, componentes >= 8 voxels  [bravais_cordas.py]
  cordas de fase  = voltas de 2π nas plaquetas  [bravais_cordas.py]
  notas           = modos fortes do espectro  [bravais_cordas.py]

PERGUNTAS (fixadas antes de rodar; respostas = numeros impressos):
  P1a  n. de atomos e n. de cordas de densidade
  P1b  %% de cordas com exatamente 1 atomo
  P1c  %% de atomos que moram dentro de alguma corda
  P1d  media de atomos por corda
  P2   alongamento do corpo do atomo (eixo maior/menor; media e %% >= 2)
  P3   %% de atomos com corda de fase a menos de 2 unidades
  P4   numero de participacao das notas por atomo (1 = o atomo e UMA nota;
       12 = acorde espalhado; media sobre 40 atomos mais fortes)

CONDICOES DE VALIDADE: V1 atomos >= 30 | V2 cordas >= 5

Uso:  python3 teste_atomo_corda.py   (N=64, 1200 passos; retoma checkpoint se existir)
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



# ================================================================ rodada (com checkpoint)
import pickle
import time as _time
_t0 = _time.time()
MAXSEC = float(os.environ.get("MAXSEC", 480))
CKPT = os.environ.get("CKPT", "AC_ckpt.pkl")
STEPS = int(os.environ.get("STEPS", 1200))
dt = 0.025

t_ini = 0
if os.path.exists(CKPT):
    with open(CKPT, "rb") as fh:
        _s = pickle.load(fh)
    Z = _s["Z"]
    for k, v in _s["welford"].items():
        welford[k] = v
    np.random.set_state(_s["rng"])
    t_ini = _s["t"]
    print("retomando checkpoint em t=%d" % t_ini)

print("Rodada cheia: N=%d, %d passos" % (N, STEPS))
for t in range(t_ini, STEPS):
    if _time.time() - _t0 > MAXSEC:
        with open(CKPT + ".tmp", "wb") as fh:
            pickle.dump(dict(Z=Z, welford=dict(welford),
                             rng=np.random.get_state(), t=t), fh)
        os.replace(CKPT + ".tmp", CKPT)
        print("checkpoint salvo em t=%d — rode o mesmo comando para continuar" % t)
        raise SystemExit(0)
    Z, mets, prop = coupled_step(Z, dt=dt)
    if t % 100 == 0:
        print("t=%4d | order=%.4f" % (t, mets["order"]))

psi = Z["psi"]
rho = np.abs(psi) ** 2
print("rodada concluída.")

# ================================================================ análise
try:
    from scipy.ndimage import label as cc_label
except ImportError:
    raise SystemExit("scipy necessário para os componentes conexos")

# átomos (critério do bravais_puro_3d.py)
mxf = maximum_filter(rho, size=5)
atomos = np.argwhere((rho == mxf) & (rho > np.percentile(rho, 99.0)))
avals = rho[atomos[:, 0], atomos[:, 1], atomos[:, 2]]
atomos = atomos[np.argsort(avals)[::-1]]
n_at = len(atomos)

# cordas de densidade (critério do bravais_cordas.py)
thr = np.percentile(rho, 97.0)
mask = rho > thr
lab, ncomp = cc_label(mask)
sizes = np.bincount(lab.ravel())
cordas_ids = [i for i in range(1, ncomp + 1) if sizes[i] >= 8]
n_co = len(cordas_ids)

# P1: correspondência
lab_at = lab[atomos[:, 0], atomos[:, 1], atomos[:, 2]]
at_na_corda = np.isin(lab_at, cordas_ids)
p1c = 100.0 * np.mean(at_na_corda) if n_at else 0.0
atomos_por = {c: int(np.sum(lab_at == c)) for c in cordas_ids}
p1b = 100.0 * np.mean([atomos_por[c] == 1 for c in cordas_ids]) if n_co else 0.0
p1d = np.mean(list(atomos_por.values())) if n_co else 0.0

# P2: alongamento do corpo de cada átomo (tensor de forma local, raio 3)
def alonga(ijk):
    c = np.array(ijk) * dx - L / 2
    ddx = (X - c[0] + L / 2) % L - L / 2
    ddy = (Y - c[1] + L / 2) % L - L / 2
    ddz = (Zg - c[2] + L / 2) % L - L / 2
    m = (ddx**2 + ddy**2 + ddz**2) < 3.0**2
    w = rho[m]
    P = np.stack([ddx[m], ddy[m], ddz[m]], axis=1)
    Wt = w / (w.sum() + 1e-30)
    C = (P * Wt[:, None]).T @ P
    ev = np.sort(np.linalg.eigvalsh(C))
    return np.sqrt(ev[2] / max(ev[0], 1e-12))

sub = atomos[:min(60, n_at)]
alongs = np.array([alonga(a) for a in sub])
p2_med = float(np.mean(alongs)) if len(alongs) else 0.0
p2_pct = 100.0 * np.mean(alongs >= 2.0) if len(alongs) else 0.0

# P3: cordas de fase perto dos átomos (plaquetas do bravais_cordas.py)
ph = np.angle(psi)
def wrapd(d):
    return (d + np.pi) % (2 * np.pi) - np.pi
vps = []
a_, b_, c_, d_ = ph[:-1, :-1, :], ph[1:, :-1, :], ph[1:, 1:, :], ph[:-1, 1:, :]
w = wrapd(b_ - a_) + wrapd(c_ - b_) + wrapd(d_ - c_) + wrapd(a_ - d_)
for i, j, k in np.argwhere(np.abs(w) > np.pi):
    vps.append((i + 0.5, j + 0.5, k))
a_, b_, c_, d_ = ph[:-1, :, :-1], ph[1:, :, :-1], ph[1:, :, 1:], ph[:-1, :, 1:]
w = wrapd(b_ - a_) + wrapd(c_ - b_) + wrapd(d_ - c_) + wrapd(a_ - d_)
for i, j, k in np.argwhere(np.abs(w) > np.pi):
    vps.append((i + 0.5, j, k + 0.5))
a_, b_, c_, d_ = ph[:, :-1, :-1], ph[:, 1:, :-1], ph[:, 1:, 1:], ph[:, :-1, 1:]
w = wrapd(b_ - a_) + wrapd(c_ - b_) + wrapd(d_ - c_) + wrapd(a_ - d_)
for i, j, k in np.argwhere(np.abs(w) > np.pi):
    vps.append((i, j + 0.5, k + 0.5))
vps = np.array(vps) if vps else np.zeros((0, 3))
n_vp = len(vps)
if n_vp:
    perto = []
    for a in sub:
        dv = (vps - a + N / 2) % N - N / 2
        perto.append(np.min(np.linalg.norm(dv, axis=1)) * dx < 2.0)
    p3 = 100.0 * np.mean(perto)
else:
    p3 = 0.0

# P4: número de participação das notas (cardápio do bravais_cordas.py)
F = np.fft.fftshift(np.abs(np.fft.fftn(rho))) ** 2
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
def particip(ijk):
    c = np.array(ijk) * dx - L / 2
    ddx = (X - c[0] + L / 2) % L - L / 2
    ddy = (Y - c[1] + L / 2) % L - L / 2
    ddz = (Zg - c[2] + L / 2) % L - L / 2
    m = (ddx**2 + ddy**2 + ddz**2) < 3.0**2
    wgt = rho[m]; xs = ddx[m]; ys = ddy[m]; zs = ddz[m]
    f = np.array([np.abs(np.sum(wgt * np.exp(-1j * (kv[0] * xs + kv[1] * ys
                                                    + kv[2] * zs)))) for kv in menu])
    f = f / (np.linalg.norm(f) + 1e-30)
    return 1.0 / np.sum(f**4)
sub40 = atomos[:min(40, n_at)]
parts = np.array([particip(a) for a in sub40])
p4_med = float(np.mean(parts)) if len(parts) else 0.0

# ================================================================ figura
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
zc = N // 2
ax = axes[0]
ax.imshow(np.where(np.isin(lab[:, :, zc], cordas_ids), rho[:, :, zc], np.nan).T,
          origin="lower", cmap=cmap_life, extent=[-L/2, L/2, -L/2, L/2])
am = atomos[np.abs(atomos[:, 2] - zc) < 3]
ax.scatter(am[:, 0] * dx - L/2, am[:, 1] * dx - L/2, s=20, facecolors="none",
           edgecolors="#43e6e0", linewidths=1.0)
ax.set_title("cordas de densidade (fatia z=0) + átomos (círculos)", fontsize=10)
ax.tick_params(labelsize=7)
ax = axes[1]
ax.hist(alongs, bins=18, color="#5bc0be", edgecolor="#0b132b")
ax.axvline(2.0, color="#ee6c4d", ls="--", label="corpo de fio (≥2)")
ax.set_xlabel("alongamento do átomo (eixo maior/menor)")
ax.set_title("P2 — forma do corpo dos átomos", fontsize=10)
ax.legend(fontsize=8); ax.grid(alpha=0.3)
ax = axes[2]
ax.hist(parts, bins=np.arange(1, 13) - 0.5, color="#f4d35e", edgecolor="#0b132b")
ax.set_xlabel("número de participação (1 = uma nota só)")
ax.set_title("P4 — quantas notas cada átomo toca", fontsize=10)
ax.grid(alpha=0.3)
plt.suptitle("Cada átomo é 1 corda? — critérios dos scripts do repo, equação completa",
             fontsize=13)
plt.tight_layout()
os.makedirs("bravais_outputs_3d", exist_ok=True)
plt.savefig("bravais_outputs_3d/atomo_corda.png", dpi=150, bbox_inches="tight")
plt.close()
print("atomo_corda.png")

# ================================================================ respostas
V1 = n_at >= 30
V2 = n_co >= 5
print("\n===== RESPOSTAS (números; leitura fixada no cabeçalho) =====")
print("P1a  átomos = %d | cordas de densidade = %d" % (n_at, n_co))
print("P1b  cordas com exatamente 1 átomo............ %.1f%%" % p1b)
print("P1c  átomos que moram dentro de alguma corda.. %.1f%%" % p1c)
print("P1d  média de átomos por corda................ %.2f" % p1d)
print("P2   alongamento: média %.2f | com corpo de fio (≥2): %.1f%%"
      % (p2_med, p2_pct))
print("P3   átomos com corda de fase a < 2 unidades.. %.1f%%  (%d pontos de vórtice no volume)"
      % (p3, n_vp))
print("P4   notas por átomo (participação média)..... %.2f  (1 = uma nota; 12 = acorde)"
      % p4_med)
print("validade: V1 %s | V2 %s" % tuple("OK" if v else "NÃO" for v in (V1, V2)))
