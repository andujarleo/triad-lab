#!/usr/bin/env python3
"""
Mapeando o ambiente com WiFi — mesma equação, mesmo molde
=========================================================
Ideia: em vez de começar o campo com gaussianos sorteados, começar com o
que o ambiente REALMENTE emite — as medições de sinal WiFi — e deixar a
MESMA equação de sempre evoluir esse campo. Depois, aplicar exatamente o
mesmo molde de análise que revelou o triângulo/pirâmide:

  iħ ∂tΨ = [ -ħ²/2m ∇² + V_ext + Λ|Ψ|² + V_mem + α(-Δ)^{σ/2} - iΓ ]Ψ + η

Nada da dinâmica muda. Nada da análise muda. As ÚNICAS coisas declaradas
aqui (e que não vêm da equação) são as duas traduções de entrada, marcadas
com "TRADUÇÃO DECLARADA" no código:

  T1. onde cada medição entra na caixa (posição);
  T2. como RSSI e frequência viram amplitude e fase.

Se a beirada L1 do espectro do campo semeado por WiFi cair no MESMO lugar
(c ≈ 4.9) que nas rodadas semeadas por acaso, a régua é do sistema.
Se cair em outro lugar, o ambiente impôs a sua própria escala — e o
perfil L1 / autocorrelação viram um mapa das dimensões do ambiente.

COMO COLETAR OS DADOS (arquivo wifi_scans.csv, uma linha por medição):
    x,y,z,freq_mhz,rssi_dbm
    0.0,0.0,1.0,2412,-45
    1.5,0.0,1.0,2437,-60
    ...
  - x,y,z em metros: sua posição na sala quando escaneou (passos servem).
  - freq_mhz: canal do AP (ex.: 2412, 5180). rssi_dbm: intensidade (ex.: -45).
  - macOS: airport -s | Linux: nmcli -f FREQ,SIGNAL dev wifi | apps de scan.
  - caminhe pela sala e escaneie em vários pontos; quanto mais pontos, melhor.
  - z pode ser 1.0 fixo se você mediu tudo na mesma altura.

Uso:  python3 bravais_wifi.py                (lê wifi_scans.csv)
      CSV=meuarquivo.csv python3 bravais_wifi.py
      STEPS=400 python3 bravais_wifi.py      (padrão 800)
"""
import numpy as np
import matplotlib.pyplot as plt
import os

np.random.seed(None)
os.makedirs("bravais_outputs_3d", exist_ok=True)

CSV = os.environ.get("CSV", "wifi_scans.csv")
STEPS = int(os.environ.get("STEPS", 800))
DT = 0.025
L = 32.0     # mesma caixa das outras rodadas (comparável com c ≈ 4.9)
N = 64
dx = L / N
dV = dx**3

# ---------------------------------------------------------------- leitura
if not os.path.exists(CSV):
    raise SystemExit(
        "não achei %s\ncrie um CSV com colunas x,y,z,freq_mhz,rssi_dbm "
        "(veja o cabeçalho deste script)" % CSV)
raw = np.genfromtxt(CSV, delimiter=",", names=True)
xs = np.atleast_1d(raw["x"]).astype(float)
ys = np.atleast_1d(raw["y"]).astype(float)
zs = np.atleast_1d(raw["z"]).astype(float)
fq = np.atleast_1d(raw["freq_mhz"]).astype(float)
db = np.atleast_1d(raw["rssi_dbm"]).astype(float)
print("%d medições lidas de %s" % (len(xs), CSV))

# ---------------------------------------------------------------- grid
x1 = np.linspace(-L / 2, L / 2, N, endpoint=False)
X, Y, Zg = np.meshgrid(x1, x1, x1, indexing="ij")
k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1, k1, k1, indexing="ij")
K2 = KX**2 + KY**2 + KZ**2
Kabs = np.sqrt(K2 + 1e-30)

# ---------------------------------------------------------------- Ψ0 do WiFi
# TRADUÇÃO DECLARADA T1 (posição): as posições medidas são centradas e
# escaladas uniformemente para caber em 60% da caixa. Um único fator de
# escala para os três eixos — as proporções do ambiente são preservadas.
pos = np.stack([xs, ys, zs], axis=1)
pos = pos - pos.mean(axis=0)
span = np.abs(pos).max()
metros_por_unidade = span / (0.3 * L) if span > 0 else 1.0
pos = pos / (metros_por_unidade + 1e-30)

# TRADUÇÃO DECLARADA T2 (amplitude e fase): amplitude na escala linear do
# sinal (10^(RSSI/20), normalizada pelo mais forte) e fase proporcional à
# frequência da portadora — mesma banda, mesma fase; bandas distantes,
# fases distantes. Largura do pacote = comprimento de onda físico do WiFi
# reescalado pela mesma régua metros->unidades de T1.
amp = 10.0 ** (db / 20.0)
amp = amp / amp.max()
fase = 2.0 * np.pi * (fq - fq.min()) / (np.ptp(fq) + 1e-30)
c_luz = 299792458.0
lam_m = c_luz / (fq * 1e6)                 # ~0.125 m (2.4G) / ~0.058 m (5G)
w_unid = np.clip(lam_m / (metros_por_unidade + 1e-30), 2 * dx, 0.15 * L)

psi = np.zeros((N, N, N), dtype=np.complex128)
for (px, py, pz), a, ph, w in zip(pos, amp, fase, w_unid):
    psi += a * np.exp(1j * ph) * np.exp(
        -((X - px) ** 2 + (Y - py) ** 2 + (Zg - pz) ** 2) / (2 * w**2))
psi += 0.05 * (np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))

fig, axes = plt.subplots(1, 3, figsize=(13, 4.2))
r0 = np.abs(psi) ** 2
for ax, (sl, lab) in zip(axes, [(r0[:, :, N // 2], "xy"),
                                 (r0[:, N // 2, :], "xz"),
                                 (r0[N // 2, :, :], "yz")]):
    ax.imshow(sl.T, origin="lower", cmap="magma",
              extent=[-L / 2, L / 2, -L / 2, L / 2])
    ax.set_title("plano %s" % lab); ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("Campo inicial semeado pelo WiFi (antes da equação agir)", fontsize=12)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/wifi_campo_inicial.png", dpi=140, bbox_inches="tight")
plt.close()

# ---------------------------------------------------------------- dinâmica
# DAQUI PARA BAIXO: idêntico ao bravais_puro_3d.py. Nada é imposto.
Z = {"h": np.zeros(4), "b": np.zeros(4), "a": np.zeros(4), "n": np.zeros(4),
     "g": np.zeros(4), "ell": np.zeros(8), "v": np.zeros(8), "psi": psi}
welford = {"mean": np.zeros(8), "M2": np.zeros(8), "count": 0}
guard_n = [0]


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


def psi_numeric_guard(p):
    nrm2 = np.sum(np.abs(p) ** 2) * dV
    if np.isfinite(nrm2) and nrm2 > 100.0:
        guard_n[0] += 1
    if not np.isfinite(nrm2) or nrm2 > 1e6:
        p = np.nan_to_num(p, nan=0.0, posinf=0.0, neginf=0.0)
        nrm2 = np.sum(np.abs(p) ** 2) * dV
    if nrm2 < 1e-12:
        p = p + 1e-3 * (np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))
        nrm2 = np.sum(np.abs(p) ** 2) * dV
    if nrm2 > 100.0:
        p = p * np.sqrt(50.0 / nrm2)
    return p


def experience_signature(p, Zs):
    rho = np.abs(p) ** 2
    mean_rho = np.mean(rho) + 1e-12
    std_rho = np.std(rho)
    fft = np.abs(np.fft.fftn(rho))
    total = np.sum(fft**2)
    order_energy = (total - fft[0, 0, 0] ** 2) / (total + 1e-12)
    gx = np.roll(rho, -1, 0) - np.roll(rho, 1, 0)
    gy = np.roll(rho, -1, 1) - np.roll(rho, 1, 1)
    gz = np.roll(rho, -1, 2) - np.roll(rho, 1, 2)
    rough = np.mean(gx**2 + gy**2 + gz**2)
    measures = np.array([mean_rho, std_rho, order_energy, rough,
                         np.linalg.norm(Zs["ell"]), np.linalg.norm(Zs["a"]),
                         np.linalg.norm(Zs["n"]), np.linalg.norm(Zs["v"])])
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
    prop = {"h": drive[:4], "b": drive[4:8],
            "a": np.tanh(chi[:4] + 0.3 * a + 0.1 * n),
            "n": np.tanh(chi[4:8] + 0.3 * n + 0.1 * a),
            "g": np.tanh(chi[:4] + 0.25 * g + 0.1 * Zm["b"]),
            "ell": np.tanh(chi[:8] + 0.2 * ell + 0.05 * np.concatenate([a, n])),
            "v": np.tanh(np.concatenate([chi[2:8], chi[0:2]]) + 0.15 * v)}
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
    V_mem = (lam(e0) * radial
             + lam(e1) * np.sin(fx * X + np.tanh(v6))
             + lam(e2) * np.sin(fy * Y + np.tanh(v7))
             + lam(e3) * np.sin(fz * Zg + np.tanh(v6 - v7))
             + 0.5 * lam(ell[4]) * np.cos(fxy * (X + Y))
             + 0.5 * lam(ell[5]) * np.cos(fyz * (Y + Zg))
             + 0.5 * lam(ell[6]) * np.cos(fzx * (Zg + X))
             + 0.3 * lam(a[0]) * np.sin(fx * Y - fy * X)
             + 0.3 * lam(a[1]) * np.sin(fy * Zg - fz * Y))
    V_scale = 0.5 * (1.0 + np.tanh(g[0] + chi[5]))
    prop["V_mem"] = V_scale * V_mem
    prop["V_ext"] = 0.15 * np.tanh(g[1]) * (
        (X / (L / 2)) ** 2 + (Y / (L / 2)) ** 2 + (Zg / (L / 2)) ** 2)
    return prop


def psi_flow(p, prop, dt):
    rho = np.abs(p) ** 2
    V = prop["V_ext"] + prop["Lambda"] * rho + prop["V_mem"]
    pk = np.fft.fftn(p)
    kinetic = np.fft.ifftn(-0.5 * K2 * pk)
    frac = prop["alpha"] * np.fft.ifftn((Kabs ** prop["sigma"]) * pk)
    damp = -prop["Gamma"] * 0.05 * p
    noise = prop["eta"] * 0.02 * (
        np.random.randn(N, N, N) + 1j * np.random.randn(N, N, N))
    return p + dt * (-1j * (kinetic + V * p + frac) + damp + noise)


def coupled_step(Z, dt, max_iter=5):
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


snap_at = sorted({0, STEPS // 8, STEPS // 4, STEPS // 2, 3 * STEPS // 4, STEPS - 1})
snapshots = {}
for t in range(STEPS):
    Z = coupled_step(Z, dt=DT)
    if t in snap_at:
        snapshots[t] = np.abs(Z["psi"]) ** 2
    if t % 100 == 0:
        nrm = np.sqrt(np.sum(np.abs(Z["psi"]) ** 2) * dV)
        print("t=%4d | ‖ψ‖=%.3f" % (t, nrm))

rho_f = snapshots[max(snapshots)]
np.savez_compressed("bravais_outputs_3d/wifi_final_state.npz",
                    rho_f=rho_f, psi_f=Z["psi"],
                    metros_por_unidade=metros_por_unidade)

# ---------------------------------------------------------------- análise (mesmo molde)
times = sorted(snapshots.keys())
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for ax, t in zip(axes.flat, times):
    ax.imshow(snapshots[t][:, :, N // 2].T, origin="lower", cmap="magma",
              extent=[-L / 2, L / 2, -L / 2, L / 2], interpolation="bilinear")
    ax.set_title("t = %d" % t); ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("Evolução do campo semeado por WiFi (fatia z=0)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/wifi_evolucao.png", dpi=140, bbox_inches="tight")
plt.close()

fft3 = np.fft.fftshift(np.abs(np.fft.fftn(rho_f)))
log_fft3 = np.log1p(fft3)

# molde do triângulo: fatias + binarizado
fig, axes = plt.subplots(1, 4, figsize=(16.8, 4.2))
axes[0].imshow(log_fft3[:, :, N // 2].T, origin="lower", cmap="gray")
axes[0].set_title("log|FFT| kx-ky (cinza)")
power2 = fft3[:, :, N // 2] ** 2
for ax, p in zip(axes[1:], [99.5, 98.0, 90.0]):
    ax.imshow((power2 > np.percentile(power2, p)).T, origin="lower", cmap="gray_r")
    ax.set_title("top %.1f%% da potência" % (100 - p))
for ax in axes:
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("Espectro do campo WiFi — mesmo molde binarizado", fontsize=12)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/wifi_fft_bw.png", dpi=140, bbox_inches="tight")
plt.close()

# molde do triângulo: cascas L1 vs L2 + posição da beirada
k1d = np.fft.fftshift(np.fft.fftfreq(N, d=dx)) * 2 * np.pi
A, B, C = np.meshgrid(k1d, k1d, k1d, indexing="ij")
R_L1 = np.abs(A) + np.abs(B) + np.abs(C)
R_L2 = np.sqrt(A**2 + B**2 + C**2)
nb = 60
prof = {}
for name, R in [("L1 (pirâmide)", R_L1), ("L2 (esfera)", R_L2)]:
    edges = np.linspace(0, R.max(), nb + 1)
    which = np.digitize(R.ravel(), edges) - 1
    sums = np.bincount(which, weights=log_fft3.ravel(), minlength=nb + 1)[:nb]
    cnts = np.bincount(which, minlength=nb + 1)[:nb] + 1e-12
    prof[name] = (0.5 * (edges[:-1] + edges[1:]), sums / cnts)
rmid, p1 = prof["L1 (pirâmide)"]
pn = p1 / (p1.max() + 1e-30)
grad = np.gradient(pn, rmid)
c_edge = rmid[2 + int(np.argmin(grad[2:]))]
fig, ax = plt.subplots(figsize=(8.5, 5))
for name, (rr, pp) in prof.items():
    ax.plot(rr, pp / pp.max(), label=name, lw=2)
ax.axvline(c_edge, ls="--", color="#ee6c4d",
           label="beirada c = %.2f" % c_edge)
ax.axvline(4.9, ls=":", color="#3a506b",
           label="c ≈ 4.9 das rodadas ao acaso")
ax.set_xlabel("raio da casca em k físico")
ax.set_ylabel("intensidade média normalizada")
ax.legend(); ax.grid(alpha=0.3)
ax.set_title("Molde do triângulo, campo WiFi:\n"
             "a beirada fica na régua do sistema ou na do ambiente?")
plt.tight_layout()
plt.savefig("bravais_outputs_3d/wifi_veredito.png", dpi=150, bbox_inches="tight")
plt.close()

# dimensões do ambiente: autocorrelação por eixo, em METROS
acorr = np.fft.fftshift(np.fft.ifftn(np.abs(np.fft.fftn(rho_f)) ** 2).real)
acorr = acorr / acorr.max()
cx = acorr[:, N // 2, N // 2]
cy = acorr[N // 2, :, N // 2]
cz = acorr[N // 2, N // 2, :]
eixo_m = (np.arange(N) - N // 2) * dx * metros_por_unidade
fig, ax = plt.subplots(figsize=(8.5, 5))
ax.plot(eixo_m, cx, label="eixo x", lw=2)
ax.plot(eixo_m, cy, label="eixo y", lw=2)
ax.plot(eixo_m, cz, label="eixo z", lw=2)
ax.set_xlabel("distância (metros do ambiente)")
ax.set_ylabel("autocorrelação")
ax.legend(); ax.grid(alpha=0.3)
ax.set_title("Dimensões do ambiente vistas pelo campo:\n"
             "onde cada curva morre/oscila é a escala daquele eixo, em metros")
plt.tight_layout()
plt.savefig("bravais_outputs_3d/wifi_dimensoes.png", dpi=150, bbox_inches="tight")
plt.close()

print("\nbeirada medida c = %.3f  (rodadas ao acaso: c ≈ 4.9)" % c_edge)
print("guarda ativou %d vezes" % guard_n[0])
print("régua da tradução: 1 unidade da caixa = %.3f m do ambiente" % metros_por_unidade)
print("imagens em bravais_outputs_3d/: wifi_campo_inicial, wifi_evolucao, "
      "wifi_fft_bw, wifi_veredito, wifi_dimensoes (.png) + wifi_final_state.npz")
print("dica: analise o npz com bravais_cordas.py — "
      "python3 bravais_cordas.py bravais_outputs_3d/wifi_final_state.npz")
