#!/usr/bin/env python3
"""
Teste L e A — todas as possibilidades, segundo as cordas
========================================================
Dinamica IDENTICA ao bravais_puro_3d.py (todos os termos juntos, nada
isolado, nada calibrado). Quatro gemeas identicas ate no ruido.

Traducao (fixada antes de rodar):
  A = uma coisa forte do universo (a cantora)
  L = outra coisa, do outro lado (distancia >= 0.30L)
  nota de A = a nota dominante da impressao digital de A
  cantar    = A emitindo sua nota em compasso proprio, na primeira
              metade da janela; na segunda metade, silencio
  gemeas: G0 silencio | G1 A canta | G2 L emite na chave de A |
          G3 os dois emitem

PERGUNTAS (fixadas antes de rodar; respostas = numeros impressos):
  P1  L sente A?            mudanca local em L (G1) / fundo a mesma distancia
  P2  fica gravado em L?    mudanca em L no fim do silencio / no fim do canto
                            (>1 = persiste e cresce depois que A parou)
  P3  L se afina com A?     variacao da semelhanca numero-L vs numero-A em G1,
                            descontada a variacao natural em G0
  P4  A sente L?            mudanca local em A (G2) / fundo a mesma distancia
  P5  assimetria dos lados  P1 / P4  (>1 = o lado L->recebe e mais forte)
  P6  mao dupla cria canal? afinacao em G3 - afinacao em G1
                            (>0 = reciprocidade afina mais que mao unica)

CONDICOES DE VALIDADE (fixadas antes de rodar; o script imprime o estado):
  V1  o universo oferece >= 30 picos (detector do proprio codigo-base)
  V2  espalhamento das semelhancas entre coisas >= 0.05
  V3  distancia A-L >= 0.30 L

Uso:  python3 teste_L_e_A.py        (N=64, 1200 passos — configuracao do repo)
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
T0 = STEPS // 3                       # nascimento do universo comum
AMP = float(os.environ.get("AMP", 0.05))
dt = 0.025
JAN = STEPS - T0                      # janela do experimento
FIM_CANTO = T0 + JAN // 2             # A canta até aqui; depois, silêncio

def clone_Z(Z):
    return {k: v.copy() for k, v in Z.items()}
def snap_w(w):
    return {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in w.items()}
def load_w(dst, srcw):
    for k, v in srcw.items():
        dst[k] = v.copy() if isinstance(v, np.ndarray) else v

# ---- checkpoint (infraestrutura apenas: salva/retoma a MESMA rodada) ----
import pickle
import time as _time
_t0 = _time.time()
MAXSEC = float(os.environ.get("MAXSEC", 480))
CKPT = os.environ.get("CKPT", "LA_ckpt.pkl")
_state = None
if os.path.exists(CKPT):
    with open(CKPT, "rb") as _fh:
        _state = pickle.load(_fh)
    print("retomando checkpoint em t=%d" % _state["t"])

def _salva_ckpt(t_atual):
    d = dict(t=t_atual, rng=np.random.get_state(), gem=gem, ws=ws,
             serie=serie, sims=sims, t_canto=t_canto, emA=emA, emL=emL,
             bA=bA, bL=bL, anel_de_A=anel_de_A, anel_de_L=anel_de_L,
             cand=cand, A_i=A_i, L_i=L_i, simLA0=simLA0, dLA=dLA,
             n_picos=n_picos, espalh=espalh, V1=V1, V2=V2, V3=V3,
             nota_A=nota_A, T_beat=T_beat, menu=menu)
    with open(CKPT + ".tmp", "wb") as fh:
        pickle.dump(d, fh)
    os.replace(CKPT + ".tmp", CKPT)
    print("checkpoint salvo em t=%d (%.0fs)" % (t_atual, _time.time() - _t0))

if _state is None:
    print("Evoluindo o universo comum até t=%d..." % T0)
    for t in range(T0):
        Z, mets, prop = coupled_step(Z, dt=dt)
        if t % 100 == 0:
            print("t=%4d | order=%.4f" % (t, mets["order"]))

    rho0 = np.abs(Z["psi"]) ** 2

    # cardápio de notas
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

    def pos_de(ijk):
        return np.array(ijk) * dx - L / 2
    def dist_per(p, q):
        d = (p - q + L / 2) % L - L / 2
        return np.linalg.norm(d)

    def digital_em(rho, ijk, raio=3.0):
        c = pos_de(ijk)
        ddx = (X - c[0] + L / 2) % L - L / 2
        ddy = (Y - c[1] + L / 2) % L - L / 2
        ddz = (Zg - c[2] + L / 2) % L - L / 2
        m = (ddx**2 + ddy**2 + ddz**2) < raio**2
        w = rho[m]; xs = ddx[m]; ys = ddy[m]; zs = ddz[m]
        f = np.array([np.abs(np.sum(w * np.exp(-1j * (kv[0] * xs + kv[1] * ys
                                                      + kv[2] * zs)))) for kv in menu])
        return f / (np.linalg.norm(f) + 1e-30)

    # coisas do universo
    mxf = maximum_filter(rho0, size=5)
    picos = np.argwhere((rho0 == mxf) & (rho0 > np.percentile(rho0, 99.0)))
    pvals = rho0[picos[:, 0], picos[:, 1], picos[:, 2]]
    picos = picos[np.argsort(pvals)[::-1]]
    n_picos = len(picos)

    cand = picos[:40]
    digs = [digital_em(rho0, c) for c in cand]
    A_i = 0
    pA = pos_de(cand[A_i])
    sims_all = [float(np.dot(digs[A_i], digs[j])) for j in range(1, len(cand))]
    espalh = (max(sims_all) - min(sims_all)) if sims_all else 0.0

    # L = a coisa afastada (>=0.30L) com MENOR semelhança com A (estranha de
    # verdade — o cenário da história: L não era fã, não era do estilo)
    L_i, simLA0 = None, None
    for j in range(1, len(cand)):
        d = dist_per(pA, pos_de(cand[j]))
        if d < 0.30 * L:
            continue
        s = float(np.dot(digs[A_i], digs[j]))
        if L_i is None or s < simLA0:
            L_i, simLA0, dLA = j, s, d
    pL = pos_de(cand[L_i])

    # validade (fixada antes de rodar)
    V1 = n_picos >= 30
    V2 = espalh >= 0.05
    V3 = dLA >= 0.30 * L
    print("\n----- CONDIÇÕES DE VALIDADE -----")
    print("V1 picos >= 30:              %s  (picos = %d)" %
          ("ATENDIDA" if V1 else "NÃO ATENDIDA", n_picos))
    print("V2 espalhamento >= 0.05:     %s  (espalhamento = %.4f)" %
          ("ATENDIDA" if V2 else "NÃO ATENDIDA", espalh))
    print("V3 distância A-L >= %.1f:    %s  (distância = %.1f)" %
          (0.30 * L, "ATENDIDA" if V3 else "NÃO ATENDIDA", dLA))
    print("semelhança inicial número-L vs número-A: %.4f" % simLA0)

    # nota de A: a mais forte da digital de A cujo período caiba no canto
    ordA = np.argsort(digs[A_i])[::-1]
    cabe = (FIM_CANTO - T0) // 9
    nota_A, T_beat = None, None
    for oi in ordA:
        kv = menu[oi]
        om = 0.5 * np.linalg.norm(kv) ** 2
        Tb = max(2, int(round((2 * np.pi / om) / dt)))
        if Tb <= cabe:
            nota_A, T_beat = kv, Tb
            break
    if nota_A is None:
        nota_A, T_beat = menu[ordA[0]], max(2, cabe)
    t_canto = list(range(T0, FIM_CANTO, T_beat))
    print("nota de A: |k|=%.2f | compasso=%d passos | %d emissões até t=%d, depois silêncio"
          % (np.linalg.norm(nota_A), T_beat, len(t_canto), FIM_CANTO))

    # emissores
    def emissor(centro):
        ddx = (X - centro[0] + L / 2) % L - L / 2
        ddy = (Y - centro[1] + L / 2) % L - L / 2
        ddz = (Zg - centro[2] + L / 2) % L - L / 2
        env = np.exp(-(ddx**2 + ddy**2 + ddz**2) / (2 * 2.0**2))
        onda = np.cos(nota_A[0] * ddx + nota_A[1] * ddy + nota_A[2] * ddz)
        return 1.0 + AMP * onda * env
    emA = emissor(pA)
    emL = emissor(pL)

    # escutas
    def bola(c, r=2.0):
        ddx = (X - c[0] + L / 2) % L - L / 2
        ddy = (Y - c[1] + L / 2) % L - L / 2
        ddz = (Zg - c[2] + L / 2) % L - L / 2
        return (ddx**2 + ddy**2 + ddz**2) < r**2
    bA, bL = bola(pA), bola(pL)
    ddxA = (X - pA[0] + L / 2) % L - L / 2
    ddyA = (Y - pA[1] + L / 2) % L - L / 2
    ddzA = (Zg - pA[2] + L / 2) % L - L / 2
    distA = np.sqrt(ddxA**2 + ddyA**2 + ddzA**2)
    ddxL = (X - pL[0] + L / 2) % L - L / 2
    ddyL = (Y - pL[1] + L / 2) % L - L / 2
    ddzL = (Zg - pL[2] + L / 2) % L - L / 2
    distL = np.sqrt(ddxL**2 + ddyL**2 + ddzL**2)
    anel_de_A = (np.abs(distA - dLA) < 1.0) & ~bA & ~bL   # fundo à distância de L
    anel_de_L = (np.abs(distL - dLA) < 1.0) & ~bA & ~bL   # fundo à distância de A

    nomes = ["G0", "G1", "G2", "G3"]
    gem = {n: clone_Z(Z) for n in nomes}
    ws = {n: snap_w(welford) for n in nomes}

    serie = {"t": [], "L_G1": [], "fundoL_G1": [], "A_G2": [], "fundoA_G2": []}
    sims = {"t": [], "G0": [], "G1": [], "G3": []}

    _salva_ckpt(T0)
else:
    globals().update({k: _state[k] for k in _state if k not in ("t", "rng")})
    np.random.set_state(_state["rng"])
nomes = ["G0", "G1", "G2", "G3"]
T_INI = _state["t"] if _state is not None else T0
FIM_CANTO = T0 + JAN // 2

# funções puras disponíveis também no resume
def pos_de(ijk):
    return np.array(ijk) * dx - L / 2
def dist_per(p, q):
    d = (p - q + L / 2) % L - L / 2
    return np.linalg.norm(d)
def digital_em(rho, ijk, raio=3.0):
    c = pos_de(ijk)
    ddx = (X - c[0] + L / 2) % L - L / 2
    ddy = (Y - c[1] + L / 2) % L - L / 2
    ddz = (Zg - c[2] + L / 2) % L - L / 2
    m = (ddx**2 + ddy**2 + ddz**2) < raio**2
    w = rho[m]; xs = ddx[m]; ys = ddy[m]; zs = ddz[m]
    f = np.array([np.abs(np.sum(w * np.exp(-1j * (kv[0] * xs + kv[1] * ys
                                                  + kv[2] * zs)))) for kv in menu])
    return f / (np.linalg.norm(f) + 1e-30)

for t in range(T_INI, STEPS):
    if _time.time() - _t0 > MAXSEC:
        _salva_ckpt(t)
        print("PAUSA: rode de novo o mesmo comando para continuar")
        raise SystemExit(0)
    st = np.random.get_state()
    for n in nomes:
        np.random.set_state(st)
        load_w(welford, ws[n])
        gem[n], mets, prop = coupled_step(gem[n], dt=dt)
        ws[n] = snap_w(welford)

    if t in t_canto:
        gem["G1"]["psi"] = gem["G1"]["psi"] * emA          # A canta
        gem["G2"]["psi"] = gem["G2"]["psi"] * emL          # L emite na chave de A
        gem["G3"]["psi"] = gem["G3"]["psi"] * emA * emL    # os dois

    serie["t"].append(t)
    D1 = np.abs(gem["G0"]["psi"] - gem["G1"]["psi"]) ** 2
    D2 = np.abs(gem["G0"]["psi"] - gem["G2"]["psi"]) ** 2
    serie["L_G1"].append(np.mean(D1[bL]))
    serie["fundoL_G1"].append(np.mean(D1[anel_de_A]))
    serie["A_G2"].append(np.mean(D2[bA]))
    serie["fundoA_G2"].append(np.mean(D2[anel_de_L]))

    if (t - T0) % 100 == 0 or t == STEPS - 1:
        sims["t"].append(t)
        for n in ["G0", "G1", "G3"]:
            r_ = np.abs(gem[n]["psi"]) ** 2
            dA_ = digital_em(r_, cand[A_i])
            dL_ = digital_em(r_, cand[L_i])
            sims[n].append(float(np.dot(dA_, dL_)))

    if t % 100 == 0:
        print("t=%4d | L sente(G1)=%.2e  A sente(G2)=%.2e" %
              (t, serie["L_G1"][-1], serie["A_G2"][-1]))

os.makedirs("bravais_outputs_3d", exist_ok=True)
cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"])
tt = (np.array(serie["t"]) - T0) * dt
t_fim_canto = (FIM_CANTO - T0) * dt

fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.8))
ax = axes[0]
ax.semilogy(tt, np.array(serie["L_G1"]) + 1e-300, color="#ee6c4d",
            label="L sente (G1: A canta)")
ax.semilogy(tt, np.array(serie["fundoL_G1"]) + 1e-300, color="#aab2c8", ls="--",
            label="fundo à mesma distância")
ax.axvline(t_fim_canto, color="gray", lw=1)
ax.text(t_fim_canto, ax.get_ylim()[0], " A para de cantar", fontsize=7,
        color="gray", va="bottom")
ax.set_title("P1/P2 — o que chega em L e o que fica", fontsize=10)
ax.set_xlabel("tempo"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

ax = axes[1]
ax.semilogy(tt, np.array(serie["A_G2"]) + 1e-300, color="#5bc0be",
            label="A sente (G2: L emite na chave de A)")
ax.semilogy(tt, np.array(serie["fundoA_G2"]) + 1e-300, color="#aab2c8", ls="--",
            label="fundo à mesma distância")
ax.axvline(t_fim_canto, color="gray", lw=1)
ax.set_title("P4 — o caminho de volta: L → A", fontsize=10)
ax.set_xlabel("tempo"); ax.legend(fontsize=8); ax.grid(alpha=0.3)

ax = axes[2]
ts = (np.array(sims["t"]) - T0) * dt
ax.plot(ts, sims["G0"], "o-", color="#aab2c8", label="G0 silêncio (deriva natural)")
ax.plot(ts, sims["G1"], "o-", color="#ee6c4d", label="G1 A canta")
ax.plot(ts, sims["G3"], "o-", color="#f4d35e", label="G3 os dois emitem")
ax.set_title("P3/P6 — semelhança número-L vs número-A no tempo", fontsize=10)
ax.set_xlabel("tempo"); ax.set_ylabel("semelhança")
ax.legend(fontsize=8); ax.grid(alpha=0.3)
plt.suptitle("Teste L e A — todas as possibilidades segundo as cordas "
             "(4 gêmeas, mesma equação, mesmo ruído)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/L_e_A_curvas.png", dpi=150, bbox_inches="tight")
plt.close()
print("L_e_A_curvas.png")

# ================================================================ respostas
i_fim_canto = FIM_CANTO - T0 - 1
q = len(serie["t"]) // 6
P1 = (np.mean(serie["L_G1"][-q:]) / (np.mean(serie["fundoL_G1"][-q:]) + 1e-300))
P2 = (np.mean(serie["L_G1"][-q:]) /
      (np.mean(serie["L_G1"][i_fim_canto - q:i_fim_canto]) + 1e-300))
dsim_G0 = sims["G0"][-1] - sims["G0"][0]
dsim_G1 = sims["G1"][-1] - sims["G1"][0]
dsim_G3 = sims["G3"][-1] - sims["G3"][0]
P3 = dsim_G1 - dsim_G0
P4 = (np.mean(serie["A_G2"][-q:]) / (np.mean(serie["fundoA_G2"][-q:]) + 1e-300))
P5 = P1 / (P4 + 1e-300)
P6 = dsim_G3 - dsim_G1

print("\n===== RESPOSTAS (números; leitura fixada no cabeçalho) =====")
print("P1  L sente A? (L/fundo, terço final)................ %.3f" % P1)
print("P2  fica gravado? (depois do silêncio / fim do canto). %.3f" % P2)
print("P3  L se afina com A? (Δsem G1 - Δsem G0)............ %+.4f" % P3)
print("P4  A sente L? (A/fundo, terço final)................ %.3f" % P4)
print("P5  assimetria (P1/P4)............................... %.3f" % P5)
print("P6  mão dupla afina mais? (Δsem G3 - Δsem G1)........ %+.4f" % P6)
print("\nsemelhança L-A: início %.4f | fim G0 %.4f | fim G1 %.4f | fim G3 %.4f"
      % (simLA0, sims["G0"][-1], sims["G1"][-1], sims["G3"][-1]))
print("validade: V1 %s | V2 %s | V3 %s" %
      tuple("OK" if v else "NÃO" for v in (V1, V2, V3)))
