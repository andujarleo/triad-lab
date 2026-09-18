#!/usr/bin/env python3
"""
Cordas e vibrações — medidas, não desenhadas
============================================
Mesma equação do bravais_puro_3d.py, sem nenhuma alteração na dinâmica.
A diferença é só o que se REGISTRA durante a rodada:

  - as linhas onde a fase de Ψ dá volta completa (as cordas que o próprio
    campo forma), fotografadas em vários tempos;
  - o valor de Ψ em cada modo espacial ao longo do tempo, para medir em
    que frequências temporais cada escala espacial de fato vibra.

Nada é imposto: nenhuma corda é desenhada por fora, nenhuma curva teórica
é sobreposta. No molde do teste da pirâmide: o dado bruto, o dado
binarizado/derivado, e o número — o leitor interpreta.

Saídas (bravais_outputs_3d/):
  cordas_fase_tempo.png    fotos das cordas de fase em 6 tempos
  cordas_comprimento.png   quantidade total de corda vs tempo
  vibracao_dispersao.png   mapa medido: potência em (escala espacial, frequência temporal)
  vibracao_notas.png       espectro temporal dos 10 modos espaciais mais fortes

Uso:  python3 bravais_cordas_vibracoes.py
      STEPS=800 REC=256 python3 bravais_cordas_vibracoes.py
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import os

np.random.seed(None)
os.makedirs("bravais_outputs_3d", exist_ok=True)

# ---------------------------------------------------------------- grid (idêntico)
L = 32.0
N = 64
dx = L / N
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
X, Y, Zg = np.meshgrid(x, x, x, indexing="ij")
k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
Kabs = np.sqrt(K2 + 1e-30)
dV = dx**3

STEPS = int(os.environ.get("STEPS", 800))
REC = int(os.environ.get("REC", 256))      # nº de passos finais registrados
dt = 0.025
SNAP_TIMES = sorted(set(int(s) for s in np.linspace(0, STEPS - 1, 6)))
STRING_EVERY = max(1, STEPS // 30)          # medir comprimento de corda a cada tanto

# ---------------------------------------------------------------- dinâmica (idêntica)
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

Z = {
    "h": np.zeros(4), "b": np.zeros(4), "a": np.zeros(4), "n": np.zeros(4),
    "g": np.zeros(4), "ell": np.zeros(8), "v": np.zeros(8),
    "psi": multi_gaussian_field(12),
}
welford = {"mean": np.zeros(8), "M2": np.zeros(8), "count": 0}

def welford_update(m):
    welford["count"] += 1
    c = welford["count"]
    d = m - welford["mean"]
    welford["mean"] += d / c
    welford["M2"] += d * (m - welford["mean"])

def welford_z(m):
    c = max(welford["count"], 1)
    var = welford["M2"] / max(c - 1, 1)
    return (m - welford["mean"]) / (np.sqrt(var) + 1e-8)

def soft_bound(vec, cap=1.0):
    nrm = np.linalg.norm(vec)
    return vec / (1.0 + nrm / max(cap, 1e-12))

def project_state_vector(vec, radius=2.0):
    nrm = np.linalg.norm(vec)
    return vec if nrm <= radius else vec * (radius / nrm)

def psi_numeric_guard(psi):
    nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if not np.isfinite(nrm2) or nrm2 > 1e6:
        psi = np.nan_to_num(psi, nan=0.0, posinf=0.0, neginf=0.0)
        nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if nrm2 < 1e-12:
        psi = psi + 1e-3 * (np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))
        nrm2 = np.sum(np.abs(psi) ** 2) * dV
    if nrm2 > 100.0:
        psi = psi * np.sqrt(50.0 / nrm2)
    return psi

def experience_signature(psi, Zs):
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
    measures = np.array([
        mean_rho, std_rho, order_energy, rough,
        np.linalg.norm(Zs["ell"]), np.linalg.norm(Zs["a"]),
        np.linalg.norm(Zs["n"]), np.linalg.norm(Zs["v"]),
    ])
    welford_update(measures)
    z = welford_z(measures)
    chi = np.zeros(16)
    chi[:8] = z
    chi[8:12] = Zs["ell"][:4]
    chi[12:16] = 0.5 * (Zs["a"] + Zs["n"])
    return chi / (np.sqrt(np.mean(chi**2)) + 1e-8)

def coupled_proposal(chi, Zm):
    ell = Zm["ell"]; a = Zm["a"]; n = Zm["n"]; g = Zm["g"]; v = Zm["v"]
    drive = np.tanh(chi[:8] + 0.2 * ell)
    prop = {
        "h": drive[:4], "b": drive[4:8],
        "a": np.tanh(chi[:4] + 0.3 * a + 0.1 * n),
        "n": np.tanh(chi[4:8] + 0.3 * n + 0.1 * a),
        "g": np.tanh(chi[:4] + 0.25 * g + 0.1 * Zm["b"]),
        "ell": np.tanh(chi[:8] + 0.2 * ell + 0.05 * np.concatenate([a, n])),
        "v": np.tanh(np.concatenate([chi[2:8], chi[0:2]]) + 0.15 * v),
    }
    radial = np.exp(-(X**2 + Y**2 + Zg**2) / (0.25 * L**2 + 1e-8))
    e0, e1, e2, e3 = ell[0], ell[1], ell[2], ell[3]
    v0, v1, v2, v3, v4, v5, v6, v7 = v
    prop["Lambda"] = np.tanh(e0 + 0.3 * chi[0] + 0.2 * a[0])
    prop["alpha"] = 0.5 * (1.0 + np.tanh(e1 + 0.3 * chi[1]))
    prop["Gamma"] = 0.5 * (1.0 + np.tanh(e2 + 0.3 * chi[2]))
    prop["eta"] = 0.5 * (1.0 + np.tanh(e3 + 0.3 * chi[3]))
    prop["sigma"] = 1.0 + 0.5 * np.tanh(v0 + chi[4])
    fx = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v0))
    fy = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v1))
    fz = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v2))
    fxy = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v3))
    fyz = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v4))
    fzx = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v5))
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
    prop["V_mem"] = V_scale * V_mem
    prop["V_ext"] = 0.15 * np.tanh(g[1]) * (
        (X / (L / 2)) ** 2 + (Y / (L / 2)) ** 2 + (Zg / (L / 2)) ** 2
    )
    return prop

def psi_flow(psi, prop, dt):
    rho = np.abs(psi) ** 2
    V = prop["V_ext"] + prop["Lambda"] * rho + prop["V_mem"]
    psi_k = np.fft.fftn(psi)
    kinetic = np.fft.ifftn(-0.5 * K2 * psi_k)
    frac = prop["alpha"] * np.fft.ifftn((Kabs ** prop["sigma"]) * psi_k)
    damp = -prop["Gamma"] * 0.05 * psi
    noise = prop["eta"] * 0.02 * (
        np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N)
    )
    return psi + dt * (-1j * (kinetic + V * psi + frac) + damp + noise)

def coupled_step(Z, dt=0.02, max_iter=5):
    Z0 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}
    Zc = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}
    for _ in range(max_iter):
        Zm = {k: 0.5 * (Z0[k] + Zc[k]) for k in Z0}
        chi = experience_signature(Zm["psi"], Zm)
        prop = coupled_proposal(chi, Zm)
        keys = ["h", "b", "a", "n", "g", "ell", "v"]
        raw = {k: prop[k] - Zm[k] for k in keys}
        stack = soft_bound(np.concatenate([raw[k] for k in keys]), cap=1.0)
        i0 = 0
        for k in keys:
            nsz = raw[k].size
            Zc[k] = project_state_vector(Z0[k] + stack[i0:i0 + nsz], radius=2.5)
            i0 += nsz
        Zc["psi"] = psi_numeric_guard(psi_flow(Zm["psi"], prop, dt))
        if np.linalg.norm(Zc["ell"] - Zm["ell"]) < 1e-3:
            break
    return Zc

# ---------------------------------------------------------------- cordas de fase
def phase_strings(psi):
    """Pontos onde a fase dá volta de ±2π ao redor de uma plaqueta."""
    ph = np.angle(psi)
    def jump(u, v):
        return (v - u + np.pi) % (2 * np.pi) - np.pi
    out = []
    # plano xy
    a = ph[:-1, :-1, :]; b = ph[1:, :-1, :]; c = ph[1:, 1:, :]; d = ph[:-1, 1:, :]
    w = jump(a, b) + jump(b, c) + jump(c, d) + jump(d, a)
    idx = np.argwhere(np.abs(w) > np.pi)
    if len(idx):
        out.append(np.column_stack([idx[:, 0] + 0.5, idx[:, 1] + 0.5, idx[:, 2],
                                    np.sign(w[idx[:, 0], idx[:, 1], idx[:, 2]])]))
    # plano xz
    a = ph[:-1, :, :-1]; b = ph[1:, :, :-1]; c = ph[1:, :, 1:]; d = ph[:-1, :, 1:]
    w = jump(a, b) + jump(b, c) + jump(c, d) + jump(d, a)
    idx = np.argwhere(np.abs(w) > np.pi)
    if len(idx):
        out.append(np.column_stack([idx[:, 0] + 0.5, idx[:, 1], idx[:, 2] + 0.5,
                                    np.sign(w[idx[:, 0], idx[:, 1], idx[:, 2]])]))
    # plano yz
    a = ph[:, :-1, :-1]; b = ph[:, 1:, :-1]; c = ph[:, 1:, 1:]; d = ph[:, :-1, 1:]
    w = jump(a, b) + jump(b, c) + jump(c, d) + jump(d, a)
    idx = np.argwhere(np.abs(w) > np.pi)
    if len(idx):
        out.append(np.column_stack([idx[:, 0], idx[:, 1] + 0.5, idx[:, 2] + 0.5,
                                    np.sign(w[idx[:, 0], idx[:, 1], idx[:, 2]])]))
    return np.vstack(out) if out else np.zeros((0, 4))

# modos registrados: todos com |k|_L1 até um raio generoso (subamostra o resto)
KL1 = np.abs(KX) + np.abs(KY) + np.abs(KZ)
sel_modes = np.argwhere(np.fft.fftshift(KL1) < 8.0)  # índices na grade shiftada
sel_flat = np.ravel_multi_index(sel_modes.T, (N, N, N))
print("registrando %d modos espaciais por %d passos finais" % (len(sel_flat), REC))

# ---------------------------------------------------------------- rodada
string_len_t = []      # (t, nº de plaquetas com volta)
string_snaps = {}      # t -> pontos
modes_t = np.zeros((REC, len(sel_flat)), dtype=np.complex64)
rec_i = 0

print("rodando %d passos (mesma equação, só registrando mais)" % STEPS)
for t in range(STEPS):
    Z = coupled_step(Z, dt=dt)
    if t % STRING_EVERY == 0 or t in SNAP_TIMES:
        sp = phase_strings(Z["psi"])
        string_len_t.append((t, len(sp)))
        if t in SNAP_TIMES:
            string_snaps[t] = sp
    if t >= STEPS - REC:
        pk = np.fft.fftshift(np.fft.fftn(Z["psi"]))
        modes_t[rec_i] = pk.ravel()[sel_flat].astype(np.complex64)
        rec_i += 1
    if t % 100 == 0:
        print("  t=%4d | cordas=%d plaquetas" % (t, string_len_t[-1][1]))

# ---------------------------------------------------------------- imagens
# 1) fotos das cordas em 6 tempos
fig = plt.figure(figsize=(15, 10))
for pi, t in enumerate(sorted(string_snaps), 1):
    ax = fig.add_subplot(2, 3, pi, projection="3d")
    sp = string_snaps[t]
    if len(sp):
        xyz = sp[:, :3] * dx - L / 2
        pos = sp[:, 3] > 0
        ax.scatter(xyz[pos, 0], xyz[pos, 1], xyz[pos, 2], s=3,
                   color="#ee6c4d", alpha=0.55, linewidths=0)
        ax.scatter(xyz[~pos, 0], xyz[~pos, 1], xyz[~pos, 2], s=3,
                   color="#5bc0be", alpha=0.55, linewidths=0)
    ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2); ax.set_zlim(-L / 2, L / 2)
    ax.set_title("t = %d  (%d pontos)" % (t, len(sp)), fontsize=10)
    ax.view_init(elev=25, azim=45)
    ax.tick_params(labelsize=6)
plt.suptitle("Cordas de fase do próprio campo — voltas de 2π (+ laranja, − azul)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_fase_tempo.png", dpi=140, bbox_inches="tight")
plt.close()

# 2) quantidade total de corda vs tempo
sl = np.array(string_len_t)
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(sl[:, 0], sl[:, 1] * dx, color="#3a506b", lw=2)
ax.set_xlabel("passo")
ax.set_ylabel("comprimento total de corda (unid. de espaço)")
ax.set_title("Quanta corda existe no campo, ao longo do tempo")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/cordas_comprimento.png", dpi=140, bbox_inches="tight")
plt.close()

# 3) mapa medido de vibração: potência em (escala espacial L1, frequência temporal)
win = np.hanning(REC)[:, None]
spec_t = np.fft.fft((modes_t - modes_t.mean(axis=0)) * win, axis=0)
pw = np.abs(spec_t) ** 2
omegas = np.fft.fftfreq(REC, d=dt) * 2 * np.pi
pos_w = omegas >= 0
kl1_sel = np.fft.fftshift(KL1).ravel()[sel_flat]
nkb = 28
kedges = np.linspace(0, kl1_sel.max(), nkb + 1)
kbin = np.digitize(kl1_sel, kedges) - 1
disp = np.zeros((nkb, pos_w.sum()))
for b in range(nkb):
    m = kbin == b
    if m.any():
        disp[b] = pw[pos_w][:, m].mean(axis=1)
fig, ax = plt.subplots(figsize=(9, 6))
im = ax.imshow(
    np.log1p(disp / disp.max()).T, origin="lower", aspect="auto", cmap="viridis",
    extent=[0, kedges[-1], 0, omegas[pos_w].max()],
)
ax.set_xlabel("escala espacial |kx|+|ky|+|kz|")
ax.set_ylabel("frequência temporal ω medida")
ax.set_title("Como cada escala espacial vibra no tempo — mapa medido, nada sobreposto")
plt.colorbar(im, ax=ax, fraction=0.04, label="log potência (norm.)")
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vibracao_dispersao.png", dpi=145, bbox_inches="tight")
plt.close()

# 4) espectro temporal dos 10 modos espaciais mais fortes
strength = np.mean(np.abs(modes_t) ** 2, axis=0)
top10 = np.argsort(strength)[::-1][:10]
fig, ax = plt.subplots(figsize=(9, 5.5))
for rank, mi in enumerate(top10):
    ijk = np.array(np.unravel_index(sel_flat[mi], (N, N, N)))
    kvec = (ijk - N // 2) * (2 * np.pi / L)
    ax.plot(omegas[pos_w], pw[pos_w][:, mi] / pw[pos_w][:, mi].max() + rank * 1.1,
            lw=1.2,
            label="k=(%.1f, %.1f, %.1f)" % tuple(kvec))
ax.set_xlabel("frequência temporal ω")
ax.set_ylabel("potência (normalizada, deslocada por modo)")
ax.set_title("As 10 vibrações mais fortes — espectro temporal de cada modo espacial")
ax.legend(fontsize=7, ncol=2)
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vibracao_notas.png", dpi=145, bbox_inches="tight")
plt.close()

np.savez_compressed(
    "bravais_outputs_3d/cordas_vibracoes.npz",
    string_len_t=sl, omegas=omegas, disp=disp, kedges=kedges,
    top10_k=[(np.array(np.unravel_index(sel_flat[mi], (N, N, N))) - N // 2)
             * (2 * np.pi / L) for mi in top10],
)
print("\nimagens: cordas_fase_tempo.png, cordas_comprimento.png, "
      "vibracao_dispersao.png, vibracao_notas.png")
print("dados: cordas_vibracoes.npz")
