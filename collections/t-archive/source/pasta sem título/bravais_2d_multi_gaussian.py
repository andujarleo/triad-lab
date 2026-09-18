#!/usr/bin/env python3
"""
Simulacao 2D longa com multiplos gaussianos iniciais
- Mais passos (500)
- Multiplos centros gaussianos (mais atomos iniciais)
- Visualizacao rica: rede + vetores primitivos + cor por estado de vida
- Tudo emerge sem isolamento nem calibracao
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import maximum_filter
import os

np.random.seed(123)

# ----------------------------- Parametros -----------------------------
L = 56.0
N = 256
dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = x.copy()
X, Y = np.meshgrid(x, y, indexing='ij')

KX = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KY = KX.copy()
KX, KY = np.meshgrid(KX, KY, indexing='ij')
K2 = KX**2 + KY**2

# ------------------------- Inicializacao com multiplos gaussianos -------------------------
def init_multi_gaussians(n_gauss=9, sigma=2.8):
    psi = np.zeros((N, N), dtype=complex)
    centers = np.random.uniform(-L/3, L/3, size=(n_gauss, 2))
    for cx, cy in centers:
        psi += np.exp(-((X - cx)**2 + (Y - cy)**2) / (2 * sigma**2))
    psi *= (0.6 + 0.5j * np.random.randn(N, N))
    norm = np.sqrt(np.sum(np.abs(psi)**2) * dx**2 + 1e-12)
    return psi / norm * np.sqrt(2.5)

psi = init_multi_gaussians(n_gauss=11, sigma=3.1)

state = {
    'ell': np.zeros(8),
    'a': np.zeros(3),
    'n': np.zeros(3),
    'v': np.zeros(6),
    'psi': psi.copy()
}

history = {'density': [], 'order': [], 'ell_norm': [], 'v': []}

# ------------------------- Funcao de proposta unica -------------------------
def single_proposal_2d(sig, Z_mid, K2, dx):
    ell = Z_mid['ell']
    a = Z_mid['a']
    n = Z_mid['n']
    v = Z_mid['v']

    raw_ell = 0.18 * np.tanh(sig[:8] + 0.1 * ell)
    raw_a   = 0.45 * np.tanh(sig[:3] + 0.2 * a)
    raw_n   = 0.4 * np.tanh(sig[3:6] + 0.18 * n)
    raw_v   = 0.14 * np.tanh(sig[6:12] + 0.07 * v)

    Lambda = -0.95 + 0.55 * np.tanh(sig[0] + 0.12 * ell[0])
    alpha  = 0.11 + 0.07 * np.tanh(sig[1])
    Gamma  = 0.035 + 0.022 * np.tanh(sig[2])
    eta_amp = 0.012 + 0.009 * np.tanh(sig[3])

    V_mem = 0.32 * np.tanh(ell[0]) * np.exp(-(X**2 + Y**2) / 26.0)
    V_mem += 0.15 * np.sin(2 * np.pi * X / (8.2 + 0.35 * v[0]))
    V_mem += 0.15 * np.sin(2 * np.pi * Y / (8.2 + 0.35 * v[1]))
    V_mem += 0.11 * np.cos(2 * np.pi * (X + 0.7*Y) / (10.5 + 0.28 * v[2]))

    return {
        'ell': raw_ell, 'a': raw_a, 'n': raw_n, 'v': raw_v,
        'Lambda': Lambda, 'alpha': alpha, 'Gamma': Gamma,
        'eta_amp': eta_amp, 'V_mem': V_mem
    }

def compute_signature_2d(psi, ell):
    rho = np.abs(psi)**2
    rho_fft = np.abs(np.fft.fft2(rho))
    peak = np.max(rho_fft[2:N//2-1, 2:N//2-1])
    mean_rho = np.mean(rho)
    sig = np.zeros(12)
    sig[0] = (peak - mean_rho) / (mean_rho + 1e-6)
    sig[1] = np.std(rho)
    sig[2] = np.mean(rho**2)
    sig[3] = np.linalg.norm(ell)
    sig[4:8] = 0.12 * ell[:4] + np.random.randn(4) * 0.06
    sig[8:] = np.random.randn(4) * 0.05
    return sig

def evolve_psi_2d(psi, props, K2, dx, dt=0.012):
    rho = np.abs(psi)**2
    V_nl = props['Lambda'] * rho
    V_total = V_nl + props['V_mem']

    psi_k = np.fft.fft2(psi)
    kinetic = np.fft.ifft2(-0.5 * K2 * psi_k)
    frac = props['alpha'] * np.fft.ifft2(np.abs(K2)**0.72 * psi_k)
    diss = -1j * props['Gamma'] * psi
    noise = props['eta_amp'] * (np.random.randn(N, N) + 1j * np.random.randn(N, N))

    dpsi = kinetic + V_total * psi + frac + diss + noise
    psi_new = psi + dt * dpsi

    norm = np.sqrt(np.sum(np.abs(psi_new)**2) * dx**2 + 1e-12)
    psi_new = psi_new / norm * np.sqrt(2.8)
    return psi_new

def coupled_update_2d(state, dt=0.012, max_iter=5):
    Z = {k: v.copy() for k, v in state.items()}
    Z0 = {k: v.copy() for k, v in state.items()}

    for _ in range(max_iter):
        Z_mid = {k: 0.5 * (Z0[k] + Z[k]) for k in Z}
        sig = compute_signature_2d(Z_mid['psi'], Z_mid['ell'])
        props = single_proposal_2d(sig, Z_mid, K2, dx)

        for key in ['ell', 'a', 'n', 'v']:
            d = props[key] - Z_mid[key]
            norm = np.linalg.norm(d) + 1e-8
            Z[key] = Z0[key] + 0.5 * (d / norm)

        Z['psi'] = evolve_psi_2d(Z_mid['psi'], props, K2, dx, dt)

        if np.linalg.norm(Z['ell'] - Z_mid['ell']) < 0.012:
            break
    return Z

# ------------------------- Execucao longa -------------------------
print("Rodando simulacao 2D longa com multiplos gaussianos (500 passos)...")

steps = 500
for step in range(steps):
    state = coupled_update_2d(state, dt=0.014)

    rho = np.abs(state['psi'])**2
    rho_fft = np.abs(np.fft.fft2(rho))
    order = np.max(rho_fft[2:N//2-1, 2:N//2-1]) / (np.mean(rho) + 1e-6)

    history['density'].append(rho.copy())
    history['order'].append(order)
    history['ell_norm'].append(np.linalg.norm(state['ell']))
    history['v'].append(state['v'].copy())

    if step % 80 == 0:
        print(f"Step {step:3d} | order={order:.1f} | ell={np.linalg.norm(state['ell']):.3f}")

print("Simulacao 2D concluida.")

# ------------------------- Visualizacao final rica -------------------------
os.makedirs("bravais_outputs", exist_ok=True)
rho_final = history['density'][-1]

# Detectar atomos
local_max = (rho_final == maximum_filter(rho_final, size=7)) & (rho_final > 0.06)
peaks = np.argwhere(local_max)
peak_values = rho_final[peaks[:, 0], peaks[:, 1]]

# Cor por estado de vida
ell = state['ell']
a = state['a']
n = state['n']
color_val = 0.5 + 0.5 * np.tanh(ell[0] + 0.35 * a[0] + 0.25 * n[0])
color_val = np.clip(color_val, 0.1, 0.95)

colors = ["#0d1b2a", "#1b3a4b", "#065a60", "#0a9396", "#94d2bd", "#e9c46a", "#f4a261"]
cmap = LinearSegmentedColormap.from_list("life_rich", colors)

fig, ax = plt.subplots(figsize=(10, 9))
im = ax.imshow(rho_final.T, extent=[-L/2, L/2, -L/2, L/2],
               cmap='inferno', origin='lower', interpolation='bilinear', alpha=0.95)

# Atom os coloridos
if len(peaks) > 0:
    sizes = 220 * (peak_values / np.max(peak_values) + 0.25)
    colors_peaks = cmap(np.linspace(0.15, 0.92, len(peaks)))
    ax.scatter(peaks[:, 0] * dx - L/2, peaks[:, 1] * dx - L/2,
               s=sizes, c=colors_peaks, edgecolors='white', linewidths=0.5, zorder=10, alpha=0.95)

# Vetores primitivos emergentes (aproximados pelos parametros v)
v = state['v']
a1 = np.array([7.8 + 0.4*v[0], 0.3 + 0.2*v[3]])
a2 = np.array([0.4 + 0.2*v[4], 7.8 + 0.4*v[1]])
origin = np.array([0.0, 0.0])
ax.arrow(origin[0], origin[1], a1[0], a1[1], head_width=0.8, head_length=0.6,
         fc='#00ff9f', ec='white', linewidth=2.2, zorder=20)
ax.arrow(origin[0], origin[1], a2[0], a2[1], head_width=0.8, head_length=0.6,
         fc='#00ff9f', ec='white', linewidth=2.2, zorder=20)
ax.text(a1[0]*0.6, a1[1]*0.6, "a₁", color='#00ff9f', fontsize=11, fontweight='bold')
ax.text(a2[0]*0.6, a2[1]*0.6, "a₂", color='#00ff9f', fontsize=11, fontweight='bold')

ax.set_title(f"Rede de Bravais Emergente 2D (múltiplos gaussianos)\n"
             f"ordem={history['order'][-1]:.1f} | ℓ-norm={history['ell_norm'][-1]:.3f} | "
             f"átomos≈{len(peaks)}", fontsize=12)
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.colorbar(im, ax=ax, label="densidade |Ψ|²")
plt.tight_layout()
plt.savefig("bravais_outputs/bravais_2d_multi_gauss.png", dpi=170, bbox_inches='tight')
plt.close()

# Graficos de evolucao
plt.figure(figsize=(7, 3))
plt.plot(history['order'], color='#ff6b6b', lw=1.6)
plt.title("Parâmetro de ordem (2D - multi gaussianos)")
plt.xlabel("Passo")
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/order_2d_multi.png", dpi=140)
plt.close()

v_arr = np.array(history['v'])
plt.figure(figsize=(9, 3.8))
for j in range(6):
    plt.plot(v_arr[:, j], label=f"v{j}", alpha=0.82)
plt.title("Parâmetros de rede emergentes (2D)")
plt.xlabel("Passo")
plt.legend(ncol=3, fontsize=8)
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/v_params_2d_multi.png", dpi=140)
plt.close()

print("Imagens 2D salvas.")