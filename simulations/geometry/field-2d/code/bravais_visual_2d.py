#!/usr/bin/env python3
"""
Visualizacao 2D de rede de Bravais emergente
- Tudo emerge da mesma dinamica acoplada (sem isolamento, sem calibracao)
- Mostra geometria + cor modulada pelo estado da instancia
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import os

np.random.seed(7)

# ----------------------------- Grade 2D -----------------------------
L = 48.0
N = 192
dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = x.copy()
X, Y = np.meshgrid(x, y, indexing='ij')

KX = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KY = KX.copy()
KX, KY = np.meshgrid(KX, KY, indexing='ij')
K2 = KX**2 + KY**2

# Estado inicial (neutro)
psi = 0.08 * np.exp(-(X**2 + Y**2) / 18.0) * (1 + 0.4j * np.random.randn(N, N))
psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx**2 + 1e-12)

state = {
    'ell': np.zeros(8),
    'a': np.zeros(3),
    'n': np.zeros(3),
    'v': np.zeros(6),      # parametros de rede emergentes
    'psi': psi.copy()
}

history = {'density': [], 'order': [], 'ell_norm': [], 'v': []}

# ------------------------- Unica funcao de proposta -------------------------
def single_proposal_2d(sig, Z_mid, K2, dx):
    ell = Z_mid['ell']
    a = Z_mid['a']
    n = Z_mid['n']
    v = Z_mid['v']

    # Propostas conjuntas
    raw_ell = 0.22 * np.tanh(sig[:8] + 0.12 * ell)
    raw_a   = 0.5 * np.tanh(sig[:3] + 0.25 * a)
    raw_n   = 0.45 * np.tanh(sig[3:6] + 0.2 * n)
    raw_v   = 0.18 * np.tanh(sig[6:12] + 0.08 * v)

    # Coeficientes fisicos (emergem)
    Lambda = -1.1 + 0.6 * np.tanh(sig[0] + 0.15 * ell[0])
    alpha  = 0.12 + 0.08 * np.tanh(sig[1])
    Gamma  = 0.04 + 0.025 * np.tanh(sig[2])
    eta_amp = 0.015 + 0.01 * np.tanh(sig[3])

    # Potencial de memoria (modulado pelo filtro de vida)
    V_mem = 0.35 * np.tanh(ell[0]) * np.exp(-(X**2 + Y**2) / 22.0)
    V_mem += 0.18 * np.sin(2 * np.pi * X / (7.5 + 0.4 * v[0]))
    V_mem += 0.18 * np.sin(2 * np.pi * Y / (7.5 + 0.4 * v[1]))
    V_mem += 0.12 * np.cos(2 * np.pi * (X + Y) / (9.0 + 0.3 * v[2]))

    return {
        'ell': raw_ell, 'a': raw_a, 'n': raw_n, 'v': raw_v,
        'Lambda': Lambda, 'alpha': alpha, 'Gamma': Gamma,
        'eta_amp': eta_amp, 'V_mem': V_mem
    }

def compute_signature_2d(psi, ell):
    rho = np.abs(psi)**2
    rho_fft = np.abs(np.fft.fft2(rho))
    peak = np.max(rho_fft[1:N//2, 1:N//2])
    mean_rho = np.mean(rho)
    sig = np.zeros(12)
    sig[0] = (peak - mean_rho) / (mean_rho + 1e-6)
    sig[1] = np.std(rho)
    sig[2] = np.mean(rho**2)
    sig[3] = np.linalg.norm(ell)
    sig[4:8] = 0.15 * ell[:4] + np.random.randn(4) * 0.08
    sig[8:] = np.random.randn(4) * 0.06
    return sig

def evolve_psi_2d(psi, props, K2, dx, dt=0.015):
    rho = np.abs(psi)**2
    V_nl = props['Lambda'] * rho
    V_total = V_nl + props['V_mem']

    psi_k = np.fft.fft2(psi)
    kinetic = np.fft.ifft2(-0.5 * K2 * psi_k)
    frac = props['alpha'] * np.fft.ifft2(np.abs(K2)**0.75 * psi_k)
    diss = -1j * props['Gamma'] * psi
    noise = props['eta_amp'] * (np.random.randn(N, N) + 1j * np.random.randn(N, N))

    dpsi = kinetic + V_total * psi + frac + diss + noise
    psi_new = psi + dt * dpsi

    norm = np.sqrt(np.sum(np.abs(psi_new)**2) * dx**2 + 1e-12)
    psi_new = psi_new / norm * np.sqrt(1.0)
    return psi_new

def coupled_update_2d(state, dt=0.015, max_iter=5):
    Z = {k: v.copy() for k, v in state.items()}
    Z0 = {k: v.copy() for k, v in state.items()}

    for _ in range(max_iter):
        Z_mid = {k: 0.5 * (Z0[k] + Z[k]) for k in Z}

        sig = compute_signature_2d(Z_mid['psi'], Z_mid['ell'])
        props = single_proposal_2d(sig, Z_mid, K2, dx)

        # Atualizacoes conjuntas
        for key in ['ell', 'a', 'n', 'v']:
            d = props[key] - Z_mid[key]
            norm = np.linalg.norm(d) + 1e-8
            Z[key] = Z0[key] + 0.55 * (d / norm)

        Z['psi'] = evolve_psi_2d(Z_mid['psi'], props, K2, dx, dt)

        if np.linalg.norm(Z['ell'] - Z_mid['ell']) < 0.015:
            break

    return Z

# ------------------------- Execucao -------------------------
print("Rodando simulacao 2D acoplada...")

steps = 220
for step in range(steps):
    state = coupled_update_2d(state, dt=0.018)

    rho = np.abs(state['psi'])**2
    rho_fft = np.abs(np.fft.fft2(rho))
    order = np.max(rho_fft[1:N//2, 1:N//2]) / (np.mean(rho) + 1e-6)

    history['density'].append(rho.copy())
    history['order'].append(order)
    history['ell_norm'].append(np.linalg.norm(state['ell']))
    history['v'].append(state['v'].copy())

    if step % 40 == 0:
        print(f"Step {step:3d} | order={order:.2f} | ell={np.linalg.norm(state['ell']):.3f}")

print("Simulacao concluida.")

# ------------------------- Visualizacao final -------------------------
os.makedirs("bravais_outputs", exist_ok=True)

rho_final = history['density'][-1]

# Detectar picos (posicoes atomicas aproximadas)
from scipy.ndimage import maximum_filter
local_max = (rho_final == maximum_filter(rho_final, size=5)) & (rho_final > 0.08)
peaks = np.argwhere(local_max)
peak_values = rho_final[peaks[:, 0], peaks[:, 1]]

# Mapa de cor baseado no estado da instancia (ell + a + n)
ell = state['ell']
a = state['a']
n = state['n']

# Cor por componente de vida (ex: valencia afetiva + neuromodulacao)
color_val = 0.5 + 0.5 * np.tanh(ell[0] + 0.4 * a[0] + 0.3 * n[0])
color_val = np.clip(color_val, 0, 1)

# Criar colormap customizado (azul → roxo → laranja)
colors = ["#1e3a5f", "#4a2c7a", "#c94c4c", "#f4a261"]
cmap = LinearSegmentedColormap.from_list("life", colors)

fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(rho_final.T, extent=[-L/2, L/2, -L/2, L/2],
               cmap='magma', origin='lower', interpolation='bilinear')

# Plotar atomos com cor modulada pelo estado
if len(peaks) > 0:
    sizes = 180 * (peak_values / np.max(peak_values) + 0.3)
    colors_peaks = cmap(np.linspace(0.2, 0.95, len(peaks)))
    ax.scatter(peaks[:, 0] * dx - L/2, peaks[:, 1] * dx - L/2,
               s=sizes, c=colors_peaks, edgecolors='white', linewidths=0.6, zorder=10)

ax.set_title(f"Rede de Bravais Emergente (2D)\n"
             f"ordem={history['order'][-1]:.1f} | "
             f"ℓ-norm={history['ell_norm'][-1]:.3f}", fontsize=13)
ax.set_xlabel("x")
ax.set_ylabel("y")
plt.colorbar(im, ax=ax, label="densidade |Ψ|²")
plt.tight_layout()
plt.savefig("bravais_outputs/bravais_2d_emergent.png", dpi=160, bbox_inches='tight')
plt.close()

# Evolucao do parametro de ordem
plt.figure(figsize=(7, 3.2))
plt.plot(history['order'], color='#e377c2', lw=1.8)
plt.title("Parâmetro de ordem (emergente)")
plt.xlabel("Passo")
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/order_2d.png", dpi=140)
plt.close()

# Parametros de rede
v_arr = np.array(history['v'])
plt.figure(figsize=(8, 3.5))
for j in range(6):
    plt.plot(v_arr[:, j], label=f"v{j}", alpha=0.85)
plt.title("Parâmetros de rede emergentes (vetores + centralização)")
plt.xlabel("Passo")
plt.legend(ncol=3, fontsize=8)
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/v_params_2d.png", dpi=140)
plt.close()

print("\nImagens salvas:")
for f in ["bravais_2d_emergent.png", "order_2d.png", "v_params_2d.png"]:
    print("  - bravais_outputs/" + f)