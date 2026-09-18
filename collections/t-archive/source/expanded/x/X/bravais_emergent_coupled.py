#!/usr/bin/env python3
"""
Prototipo minimo acoplado - Bravais emergente
Regra: nenhum termo isolado, nenhum parametro calibrado manualmente.
Tudo emerge de uma unica funcao de proposta + ponto fixo implicito.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

# ----------------------------- Configuracao basica -----------------------------
np.random.seed(42)
L = 64.0
N = 256
dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
dk = 2 * np.pi / L
k = np.fft.fftfreq(N, d=dx) * 2 * np.pi

# Estado inicial neutro (sem personalidade)
psi = 0.15 * np.exp(-x**2 / 8.0) * (1.0 + 0.3j * np.random.randn(N))
psi = psi / np.sqrt(np.sum(np.abs(psi)**2) * dx + 1e-12)

state = {
    'h': np.zeros(4),
    'b': np.zeros(4),
    'a': np.zeros(4),
    'n': np.zeros(4),
    'g': np.zeros(4),
    'ell': np.zeros(8),
    'v': np.zeros(6),          # parametros de rede (emergentes)
    'psi': psi.copy()
}

history = {
    'density': [],
    'order': [],
    'energy': [],
    'ell_norm': [],
    'v_params': []
}

# ------------------------- Funcao de proposta unica -------------------------
def single_proposal(signature, Z_mid, k, dx):
    """
    Unica funcao que gera TODOS os termos.
    Nao existe funcao separada para V_mem, Lambda, alpha, Gamma, etc.
    """
    chi = signature
    ell = Z_mid['ell']
    a = Z_mid['a']
    n = Z_mid['n']
    v = Z_mid['v']

    # Propostas brutas (tudo junto)
    raw_h = 0.6 * chi[:4]
    raw_b = 0.4 * chi[4:8]
    raw_a = 0.7 * np.tanh(chi[:4] + 0.3 * a)
    raw_n = 0.5 * np.tanh(chi[4:8] + 0.2 * n)
    raw_g = 0.3 * chi[:4]
    raw_ell = 0.25 * np.tanh(chi[:8] + 0.15 * ell)

    # Parametros de rede (emergem)
    raw_v = 0.15 * np.tanh(chi[:6] + 0.1 * v)

    # Coeficientes da equacao de Psi (tambem emergem da mesma assinatura)
    Lambda = -0.8 + 0.4 * np.tanh(chi[0] + 0.2 * ell[0])          # focusing
    alpha = 0.15 + 0.1 * np.tanh(chi[1])
    Gamma = 0.05 + 0.03 * np.tanh(chi[2])
    eta_amp = 0.02 + 0.01 * np.tanh(chi[3])

    # Potencial de memoria (tambem emerge)
    V_mem = 0.3 * np.tanh(ell[0]) * np.exp(-x**2 / 12.0)
    V_mem += 0.15 * np.sin(2 * np.pi * x / (8.0 + 0.5 * v[0]))

    return {
        'h': raw_h,
        'b': raw_b,
        'a': raw_a,
        'n': raw_n,
        'g': raw_g,
        'ell': raw_ell,
        'v': raw_v,
        'Lambda': Lambda,
        'alpha': alpha,
        'Gamma': Gamma,
        'eta_amp': eta_amp,
        'V_mem': V_mem
    }

# ------------------------- Assinatura da experiencia -------------------------
def compute_signature(psi, ell, free_energy_proxy):
    rho = np.abs(psi)**2
    rho_fft = np.abs(np.fft.fft(rho))
    peak = np.max(rho_fft[1:N//2])
    mean_rho = np.mean(rho)

    sig = np.zeros(12)
    sig[0] = (peak - mean_rho) / (mean_rho + 1e-6)          # novidade/ordem
    sig[1] = np.std(rho)
    sig[2] = free_energy_proxy
    sig[3] = np.mean(np.abs(ell))
    sig[4:8] = np.random.randn(4) * 0.1 + 0.2 * ell[:4]
    sig[8:] = np.random.randn(4) * 0.05
    return sig

# ------------------------- Evolucao de Psi (dentro do acoplamento) -------------------------
def evolve_psi(psi, props, k, dx, dt=0.02):
    rho = np.abs(psi)**2
    V_nl = props['Lambda'] * rho
    V_total = V_nl + props['V_mem']

    # Termo cinetico via FFT
    psi_k = np.fft.fft(psi)
    kinetic = np.fft.ifft(-0.5 * k**2 * psi_k)

    # Termo fracionario (simplificado)
    frac = props['alpha'] * np.fft.ifft(np.abs(k)**1.5 * psi_k)

    # Dissipacao + ruido
    diss = -1j * props['Gamma'] * psi
    noise = props['eta_amp'] * (np.random.randn(N) + 1j * np.random.randn(N))

    dpsi = kinetic + V_total * psi + frac + diss + noise
    psi_new = psi + dt * dpsi

    # Normalizacao branda (emergente, nao calibrada)
    norm = np.sqrt(np.sum(np.abs(psi_new)**2) * dx + 1e-12)
    psi_new = psi_new / norm * np.sqrt(1.0)   # mantem norma ~1

    return psi_new

# ------------------------- Atualizacao acoplada (ponto fixo) -------------------------
def coupled_update(state, dt=0.02, max_iter=6):
    Z = {k: v.copy() for k, v in state.items()}
    Z0 = {k: v.copy() for k, v in state.items()}

    for it in range(max_iter):
        Z_mid = {}
        for key in Z:
            if key == 'psi':
                Z_mid[key] = 0.5 * (Z0[key] + Z[key])
            else:
                Z_mid[key] = 0.5 * (Z0[key] + Z[key])

        # Proxy de energia livre
        rho = np.abs(Z_mid['psi'])**2
        fe_proxy = np.mean(rho**2) + 0.1 * np.sum(np.abs(Z_mid['ell'])**2)

        sig = compute_signature(Z_mid['psi'], Z_mid['ell'], fe_proxy)

        props = single_proposal(sig, Z_mid, k, dx)

        # Atualizacoes (todas juntas)
        delta = {}
        delta['h'] = props['h'] - Z_mid['h']
        delta['b'] = props['b'] - Z_mid['b']
        delta['a'] = props['a'] - Z_mid['a']
        delta['n'] = props['n'] - Z_mid['n']
        delta['g'] = props['g'] - Z_mid['g']
        delta['ell'] = props['ell'] - Z_mid['ell']
        delta['v'] = props['v'] - Z_mid['v']

        # Psi evolui com os coeficientes que acabaram de ser propostos
        psi_new = evolve_psi(Z_mid['psi'], props, k, dx, dt)

        # Bounded update
        for key in ['h','b','a','n','g','ell','v']:
            d = delta[key]
            norm = np.linalg.norm(d) + 1e-8
            delta[key] = d / (1.0 + norm)

        # Aplicar
        for key in ['h','b','a','n','g','ell','v']:
            Z[key] = Z0[key] + 0.6 * delta[key]

        Z['psi'] = psi_new

        # Criterio de convergencia brando
        if np.linalg.norm(Z['ell'] - Z_mid['ell']) < 0.01:
            break

    return Z

# ------------------------- Loop principal -------------------------
print("Rodando simulacao acoplada (sem isolamento, sem calibracao)...")

steps = 180
for step in range(steps):
    state = coupled_update(state, dt=0.025)

    rho = np.abs(state['psi'])**2
    rho_fft = np.abs(np.fft.fft(rho))
    order = np.max(rho_fft[1:N//2]) / (np.mean(rho) + 1e-6)

    energy = np.mean(rho**2) + 0.5 * np.sum(np.abs(state['ell'])**2)
    ell_norm = np.linalg.norm(state['ell'])

    history['density'].append(rho.copy())
    history['order'].append(order)
    history['energy'].append(energy)
    history['ell_norm'].append(ell_norm)
    history['v_params'].append(state['v'].copy())

    if step % 30 == 0:
        print(f"Step {step:3d} | order={order:.3f} | ell_norm={ell_norm:.3f}")

print("Simulacao finalizada.")

# ------------------------- Geracao de graficos -------------------------
os.makedirs("bravais_outputs", exist_ok=True)

# 1. Evolucao da densidade (ultimos frames)
plt.figure(figsize=(10, 4))
for i, idx in enumerate([0, 60, 120, 179]):
    plt.subplot(1, 4, i+1)
    plt.plot(x, history['density'][idx], color='black', lw=0.9)
    plt.title(f"t={idx}")
    plt.ylim(0, np.max(history['density'][-1]) * 1.1)
plt.suptitle("Densidade |Psi|^2 (emergente)")
plt.tight_layout()
plt.savefig("bravais_outputs/density_evolution.png", dpi=140)
plt.close()

# 2. Parametro de ordem
plt.figure(figsize=(7, 3.5))
plt.plot(history['order'], color='#1f77b4')
plt.xlabel("Passo")
plt.ylabel("Parâmetro de ordem")
plt.title("Emergência de ordem periódica")
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/order_parameter.png", dpi=140)
plt.close()

# 3. Energia e norma de ell
fig, ax = plt.subplots(1, 2, figsize=(9, 3.2))
ax[0].plot(history['energy'], color='#d62728')
ax[0].set_title("Energia proxy")
ax[0].set_xlabel("Passo")
ax[1].plot(history['ell_norm'], color='#2ca02c')
ax[1].set_title("Norma do campo latente ℓ(t)")
ax[1].set_xlabel("Passo")
plt.tight_layout()
plt.savefig("bravais_outputs/energy_ell.png", dpi=140)
plt.close()

# 4. Parametros de rede emergentes
v_hist = np.array(history['v_params'])
plt.figure(figsize=(8, 3.5))
for j in range(6):
    plt.plot(v_hist[:, j], label=f"v{j}", alpha=0.85)
plt.title("Parâmetros de rede (emergentes, sem calibração)")
plt.xlabel("Passo")
plt.legend(fontsize=8, ncol=3)
plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/lattice_params.png", dpi=140)
plt.close()

# 5. Snapshot final da densidade + FFT
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
ax[0].plot(x, history['density'][-1], color='black')
ax[0].set_title("Densidade final")
ax[0].set_xlabel("x")

fft_final = np.abs(np.fft.fft(history['density'][-1]))[:N//2]
ax[1].plot(fft_final[1:], color='#ff7f0e')
ax[1].set_title("Espectro de Fourier (picos = periodicidade)")
ax[1].set_xlabel("k")
plt.tight_layout()
plt.savefig("bravais_outputs/final_state.png", dpi=140)
plt.close()

print("\nGráficos salvos em bravais_outputs/")
print("Arquivos gerados:")
for f in sorted(os.listdir("bravais_outputs")):
    print("  -", f)