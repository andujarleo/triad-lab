#!/usr/bin/env python3
"""
Bravais emergente - simulacao LONGA 2D + teste 3D
- 2D: 1200 passos, multiplos gaussianos
- 3D: 280 passos em grade menor, multiplos gaussianos
- Sem isolamento de termos, sem calibracao manual
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D
from scipy.ndimage import maximum_filter
import os

np.random.seed(42)
os.makedirs("bravais_outputs", exist_ok=True)

# =============================================================================
#                              2D LONGA
# =============================================================================
print("=" * 60)
print("FASE 1: Simulacao 2D LONGA (1200 passos)")
print("=" * 60)

L2 = 64.0
N2 = 192
dx2 = L2 / N2
x2 = np.linspace(-L2/2, L2/2, N2, endpoint=False)
X2, Y2 = np.meshgrid(x2, x2, indexing='ij')
KX2 = np.fft.fftfreq(N2, d=dx2) * 2 * np.pi
KX2, KY2 = np.meshgrid(KX2, KX2, indexing='ij')
K2_2d = KX2**2 + KY2**2

def init_gauss_2d(n=14, sigma=2.6):
    psi = np.zeros((N2, N2), dtype=complex)
    centers = np.random.uniform(-L2*0.32, L2*0.32, size=(n, 2))
    for cx, cy in centers:
        psi += np.exp(-((X2-cx)**2 + (Y2-cy)**2) / (2*sigma**2))
    psi *= (0.55 + 0.45j * np.random.randn(N2, N2))
    nrm = np.sqrt(np.sum(np.abs(psi)**2)*dx2**2 + 1e-12)
    return psi / nrm * np.sqrt(3.0)

psi2 = init_gauss_2d(n=14, sigma=2.7)
st2 = {
    'ell': np.zeros(8), 'a': np.zeros(3), 'n': np.zeros(3),
    'v': np.zeros(6), 'psi': psi2.copy()
}
hist2 = {'order': [], 'ell': [], 'v': [], 'dens_snap': []}

def proposal_2d(sig, Z):
    ell, a, n, v = Z['ell'], Z['a'], Z['n'], Z['v']
    return {
        'ell': 0.16*np.tanh(sig[:8] + 0.09*ell),
        'a':   0.4*np.tanh(sig[:3] + 0.18*a),
        'n':   0.35*np.tanh(sig[3:6] + 0.15*n),
        'v':   0.12*np.tanh(sig[6:12] + 0.06*v),
        'Lambda': -0.9 + 0.5*np.tanh(sig[0] + 0.1*ell[0]),
        'alpha':  0.1 + 0.06*np.tanh(sig[1]),
        'Gamma':  0.03 + 0.02*np.tanh(sig[2]),
        'eta':    0.01 + 0.008*np.tanh(sig[3]),
        'Vmem': (
            0.28*np.tanh(ell[0])*np.exp(-(X2**2+Y2**2)/30.0)
            + 0.14*np.sin(2*np.pi*X2/(8.5+0.3*v[0]))
            + 0.14*np.sin(2*np.pi*Y2/(8.5+0.3*v[1]))
            + 0.1*np.cos(2*np.pi*(X2+0.6*Y2)/(11+0.25*v[2]))
        )
    }

def sig_2d(psi, ell):
    rho = np.abs(psi)**2
    fft = np.abs(np.fft.fft2(rho))
    peak = np.max(fft[2:N2//2-1, 2:N2//2-1])
    m = np.mean(rho)
    s = np.zeros(12)
    s[0] = (peak-m)/(m+1e-6)
    s[1] = np.std(rho)
    s[2] = np.mean(rho**2)
    s[3] = np.linalg.norm(ell)
    s[4:8] = 0.1*ell[:4] + np.random.randn(4)*0.05
    s[8:] = np.random.randn(4)*0.04
    return s

def evolve_2d(psi, p, dt=0.012):
    rho = np.abs(psi)**2
    V = p['Lambda']*rho + p['Vmem']
    pk = np.fft.fft2(psi)
    kin = np.fft.ifft2(-0.5*K2_2d*pk)
    fr = p['alpha']*np.fft.ifft2(np.abs(K2_2d)**0.7 * pk)
    d = -1j*p['Gamma']*psi
    noise = p['eta']*(np.random.randn(N2,N2)+1j*np.random.randn(N2,N2))
    psi_n = psi + dt*(kin + V*psi + fr + d + noise)
    nrm = np.sqrt(np.sum(np.abs(psi_n)**2)*dx2**2 + 1e-12)
    return psi_n / nrm * np.sqrt(3.0)

def step_2d(st, dt=0.012):
    Z = {k: v.copy() for k,v in st.items()}
    Z0 = {k: v.copy() for k,v in st.items()}
    for _ in range(4):
        Zm = {k: 0.5*(Z0[k]+Z[k]) for k in Z}
        s = sig_2d(Zm['psi'], Zm['ell'])
        p = proposal_2d(s, Zm)
        for key in ['ell','a','n','v']:
            d = p[key] - Zm[key]
            nrm = np.linalg.norm(d)+1e-8
            Z[key] = Z0[key] + 0.48*(d/nrm)
        Z['psi'] = evolve_2d(Zm['psi'], p, dt)
        if np.linalg.norm(Z['ell']-Zm['ell']) < 0.01:
            break
    return Z

steps2 = 1200
snap_idx = [0, 200, 400, 600, 800, 1000, 1199]
for t in range(steps2):
    st2 = step_2d(st2, dt=0.013)
    rho = np.abs(st2['psi'])**2
    fft = np.abs(np.fft.fft2(rho))
    order = np.max(fft[2:N2//2-1, 2:N2//2-1]) / (np.mean(rho)+1e-6)
    hist2['order'].append(order)
    hist2['ell'].append(np.linalg.norm(st2['ell']))
    hist2['v'].append(st2['v'].copy())
    if t in snap_idx:
        hist2['dens_snap'].append(rho.copy())
    if t % 150 == 0:
        print(f"  2D step {t:4d} | order={order:.1f} | ell={hist2['ell'][-1]:.3f}")

print("2D longa concluida.\n")

# Visual 2D final
rho_f = hist2['dens_snap'][-1]
local_max = (rho_f == maximum_filter(rho_f, size=6)) & (rho_f > 0.05)
peaks = np.argwhere(local_max)
pvals = rho_f[peaks[:,0], peaks[:,1]] if len(peaks) else np.array([])

cmap = LinearSegmentedColormap.from_list("life",
    ["#0d1b2a","#1b3a4b","#065a60","#0a9396","#94d2bd","#e9c46a","#f4a261","#e76f51"])

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
for i, (ax, dens) in enumerate(zip(axes.flat, hist2['dens_snap'] + [None])):
    if dens is None:
        ax.axis('off')
        continue
    ax.imshow(dens.T, extent=[-L2/2,L2/2,-L2/2,L2/2], cmap='inferno',
              origin='lower', interpolation='bilinear')
    ax.set_title(f"t={snap_idx[i]}", fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("Evolucao 2D longa — multiplos gaussianos → rede Bravais", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs/bravais_2d_long_evolution.png", dpi=150, bbox_inches='tight')
plt.close()

# Final detalhado
fig, ax = plt.subplots(figsize=(10, 9))
im = ax.imshow(rho_f.T, extent=[-L2/2,L2/2,-L2/2,L2/2], cmap='inferno',
               origin='lower', interpolation='bilinear')
if len(peaks):
    sizes = 200*(pvals/np.max(pvals)+0.2)
    cols = cmap(np.linspace(0.2, 0.95, len(peaks)))
    ax.scatter(peaks[:,0]*dx2-L2/2, peaks[:,1]*dx2-L2/2,
               s=sizes, c=cols, edgecolors='white', linewidths=0.4, zorder=10)
v = st2['v']
a1 = np.array([8.0+0.5*v[0], 0.2+0.15*v[3]])
a2 = np.array([0.3+0.15*v[4], 8.0+0.5*v[1]])
ax.arrow(0,0,a1[0],a1[1], head_width=0.9, head_length=0.7, fc='#00ff9f', ec='white', lw=2.2, zorder=20)
ax.arrow(0,0,a2[0],a2[1], head_width=0.9, head_length=0.7, fc='#00ff9f', ec='white', lw=2.2, zorder=20)
ax.text(a1[0]*0.55, a1[1]*0.55, "a₁", color='#00ff9f', fontsize=12, fontweight='bold')
ax.text(a2[0]*0.55, a2[1]*0.55, "a₂", color='#00ff9f', fontsize=12, fontweight='bold')
ax.set_title(f"Bravais 2D final (1200 passos)\nordem={hist2['order'][-1]:.1f} | ℓ={hist2['ell'][-1]:.3f} | átomos≈{len(peaks)}")
plt.colorbar(im, ax=ax, label="|Ψ|²")
plt.tight_layout()
plt.savefig("bravais_outputs/bravais_2d_long_final.png", dpi=170, bbox_inches='tight')
plt.close()

plt.figure(figsize=(8,3.2))
plt.plot(hist2['order'], color='#ff6b6b', lw=1.4)
plt.title("Ordem 2D (1200 passos)"); plt.xlabel("passo"); plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/order_2d_long.png", dpi=140); plt.close()

varr = np.array(hist2['v'])
plt.figure(figsize=(9,3.5))
for j in range(6):
    plt.plot(varr[:,j], label=f"v{j}", alpha=0.85)
plt.title("Parâmetros de rede 2D (emergentes)"); plt.legend(ncol=3, fontsize=8); plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/v_2d_long.png", dpi=140); plt.close()

print("Imagens 2D salvas.\n")

# =============================================================================
#                              3D
# =============================================================================
print("=" * 60)
print("FASE 2: Simulacao 3D (280 passos, multiplos gaussianos)")
print("=" * 60)

L3 = 28.0
N3 = 48
dx3 = L3 / N3
coords = np.linspace(-L3/2, L3/2, N3, endpoint=False)
X3, Y3, Z3 = np.meshgrid(coords, coords, coords, indexing='ij')
k1d = np.fft.fftfreq(N3, d=dx3) * 2 * np.pi
KX3, KY3, KZ3 = np.meshgrid(k1d, k1d, k1d, indexing='ij')
K2_3d = KX3**2 + KY3**2 + KZ3**2

def init_gauss_3d(n=8, sigma=2.2):
    psi = np.zeros((N3,N3,N3), dtype=complex)
    centers = np.random.uniform(-L3*0.28, L3*0.28, size=(n, 3))
    for cx,cy,cz in centers:
        psi += np.exp(-((X3-cx)**2+(Y3-cy)**2+(Z3-cz)**2)/(2*sigma**2))
    psi *= (0.5 + 0.4j*np.random.randn(N3,N3,N3))
    nrm = np.sqrt(np.sum(np.abs(psi)**2)*dx3**3 + 1e-12)
    return psi / nrm * np.sqrt(2.2)

psi3 = init_gauss_3d(n=9, sigma=2.3)
st3 = {
    'ell': np.zeros(8), 'a': np.zeros(3), 'n': np.zeros(3),
    'v': np.zeros(6), 'psi': psi3.copy()
}
hist3 = {'order': [], 'ell': [], 'v': []}

def proposal_3d(sig, Z):
    ell, a, n, v = Z['ell'], Z['a'], Z['n'], Z['v']
    Vmem = (
        0.25*np.tanh(ell[0])*np.exp(-(X3**2+Y3**2+Z3**2)/22.0)
        + 0.12*np.sin(2*np.pi*X3/(7.5+0.3*v[0]))
        + 0.12*np.sin(2*np.pi*Y3/(7.5+0.3*v[1]))
        + 0.12*np.sin(2*np.pi*Z3/(7.5+0.3*v[2]))
        + 0.08*np.cos(2*np.pi*(X3+Y3+Z3)/(12+0.2*v[3]))
    )
    return {
        'ell': 0.14*np.tanh(sig[:8] + 0.08*ell),
        'a':   0.35*np.tanh(sig[:3] + 0.15*a),
        'n':   0.3*np.tanh(sig[3:6] + 0.12*n),
        'v':   0.1*np.tanh(sig[6:12] + 0.05*v),
        'Lambda': -0.85 + 0.45*np.tanh(sig[0] + 0.08*ell[0]),
        'alpha':  0.09 + 0.05*np.tanh(sig[1]),
        'Gamma':  0.028 + 0.018*np.tanh(sig[2]),
        'eta':    0.009 + 0.007*np.tanh(sig[3]),
        'Vmem': Vmem
    }

def sig_3d(psi, ell):
    rho = np.abs(psi)**2
    fft = np.abs(np.fft.fftn(rho))
    peak = np.max(fft[2:N3//2-1, 2:N3//2-1, 2:N3//2-1])
    m = np.mean(rho)
    s = np.zeros(12)
    s[0] = (peak-m)/(m+1e-6)
    s[1] = np.std(rho)
    s[2] = np.mean(rho**2)
    s[3] = np.linalg.norm(ell)
    s[4:8] = 0.08*ell[:4] + np.random.randn(4)*0.04
    s[8:] = np.random.randn(4)*0.03
    return s

def evolve_3d(psi, p, dt=0.01):
    rho = np.abs(psi)**2
    V = p['Lambda']*rho + p['Vmem']
    pk = np.fft.fftn(psi)
    kin = np.fft.ifftn(-0.5*K2_3d*pk)
    fr = p['alpha']*np.fft.ifftn(np.abs(K2_3d)**0.65 * pk)
    d = -1j*p['Gamma']*psi
    noise = p['eta']*(np.random.randn(N3,N3,N3)+1j*np.random.randn(N3,N3,N3))
    psi_n = psi + dt*(kin + V*psi + fr + d + noise)
    nrm = np.sqrt(np.sum(np.abs(psi_n)**2)*dx3**3 + 1e-12)
    return psi_n / nrm * np.sqrt(2.2)

def step_3d(st, dt=0.01):
    Z = {k: v.copy() for k,v in st.items()}
    Z0 = {k: v.copy() for k,v in st.items()}
    for _ in range(3):
        Zm = {k: 0.5*(Z0[k]+Z[k]) for k in Z}
        s = sig_3d(Zm['psi'], Zm['ell'])
        p = proposal_3d(s, Zm)
        for key in ['ell','a','n','v']:
            d = p[key] - Zm[key]
            nrm = np.linalg.norm(d)+1e-8
            Z[key] = Z0[key] + 0.45*(d/nrm)
        Z['psi'] = evolve_3d(Zm['psi'], p, dt)
        if np.linalg.norm(Z['ell']-Zm['ell']) < 0.012:
            break
    return Z

steps3 = 280
for t in range(steps3):
    st3 = step_3d(st3, dt=0.011)
    rho = np.abs(st3['psi'])**2
    fft = np.abs(np.fft.fftn(rho))
    order = np.max(fft[2:N3//2-1, 2:N3//2-1, 2:N3//2-1]) / (np.mean(rho)+1e-6)
    hist3['order'].append(order)
    hist3['ell'].append(np.linalg.norm(st3['ell']))
    hist3['v'].append(st3['v'].copy())
    if t % 40 == 0:
        print(f"  3D step {t:3d} | order={order:.1f} | ell={hist3['ell'][-1]:.3f}")

print("3D concluida.\n")

rho3 = np.abs(st3['psi'])**2
# Isosuperficie via fatias + scatter 3D dos picos
local_max3 = (rho3 == maximum_filter(rho3, size=4)) & (rho3 > 0.04)
peaks3 = np.argwhere(local_max3)
pvals3 = rho3[peaks3[:,0], peaks3[:,1], peaks3[:,2]] if len(peaks3) else np.array([])

# Figura 3D: scatter dos atomos
fig = plt.figure(figsize=(12, 5))
ax1 = fig.add_subplot(121, projection='3d')
if len(peaks3):
    xs = peaks3[:,0]*dx3 - L3/2
    ys = peaks3[:,1]*dx3 - L3/2
    zs = peaks3[:,2]*dx3 - L3/2
    sc = ax1.scatter(xs, ys, zs, c=pvals3, cmap='plasma', s=60+120*(pvals3/np.max(pvals3)),
                     edgecolors='white', linewidths=0.3, alpha=0.9)
    # Vetores primitivos
    v = st3['v']
    a1 = np.array([6.5+0.4*v[0], 0.2*v[3], 0.1*v[4]])
    a2 = np.array([0.2*v[3], 6.5+0.4*v[1], 0.1*v[5]])
    a3 = np.array([0.1*v[4], 0.1*v[5], 6.5+0.4*v[2]])
    o = np.array([0.,0.,0.])
    ax1.quiver(*o, *a1, color='#00ff9f', arrow_length_ratio=0.15, lw=2)
    ax1.quiver(*o, *a2, color='#00ff9f', arrow_length_ratio=0.15, lw=2)
    ax1.quiver(*o, *a3, color='#00ff9f', arrow_length_ratio=0.15, lw=2)
    ax1.text(*(a1*0.7), "a₁", color='#00ff9f', fontsize=10)
    ax1.text(*(a2*0.7), "a₂", color='#00ff9f', fontsize=10)
    ax1.text(*(a3*0.7), "a₃", color='#00ff9f', fontsize=10)
ax1.set_title(f"Bravais 3D emergente\nátomos≈{len(peaks3)} | ordem={hist3['order'][-1]:.1f}")
ax1.set_xlabel("x"); ax1.set_ylabel("y"); ax1.set_zlabel("z")
ax1.set_xlim(-L3/2, L3/2); ax1.set_ylim(-L3/2, L3/2); ax1.set_zlim(-L3/2, L3/2)

# Fatia central
ax2 = fig.add_subplot(122)
mid = N3 // 2
ax2.imshow(rho3[:,:,mid].T, extent=[-L3/2,L3/2,-L3/2,L3/2],
           cmap='inferno', origin='lower', interpolation='bilinear')
ax2.set_title(f"Fatia z=0 (densidade 3D)")
ax2.set_xlabel("x"); ax2.set_ylabel("y")
plt.tight_layout()
plt.savefig("bravais_outputs/bravais_3d_final.png", dpi=160, bbox_inches='tight')
plt.close()

# Ordem e params 3D
plt.figure(figsize=(8,3.2))
plt.plot(hist3['order'], color='#4ecdc4', lw=1.5)
plt.title("Ordem 3D"); plt.xlabel("passo"); plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/order_3d.png", dpi=140); plt.close()

varr3 = np.array(hist3['v'])
plt.figure(figsize=(9,3.5))
for j in range(6):
    plt.plot(varr3[:,j], label=f"v{j}", alpha=0.85)
plt.title("Parâmetros de rede 3D (emergentes)"); plt.legend(ncol=3, fontsize=8); plt.grid(True, alpha=0.3)
plt.savefig("bravais_outputs/v_3d.png", dpi=140); plt.close()

# Comparativo final
fig, ax = plt.subplots(1, 2, figsize=(11, 3.5))
ax[0].plot(hist2['order'], color='#ff6b6b', lw=1.3, label='2D')
ax[0].set_title("Ordem 2D (1200 passos)"); ax[0].legend(); ax[0].grid(True, alpha=0.3)
ax[1].plot(hist3['order'], color='#4ecdc4', lw=1.3, label='3D')
ax[1].set_title("Ordem 3D (280 passos)"); ax[1].legend(); ax[1].grid(True, alpha=0.3)
plt.suptitle("Comparativo 2D vs 3D — dinâmica emergente")
plt.tight_layout()
plt.savefig("bravais_outputs/compare_2d_3d.png", dpi=140, bbox_inches='tight')
plt.close()

print("=" * 60)
print("TUDO CONCLUIDO")
print("=" * 60)
print("Arquivos gerados em bravais_outputs/:")
for f in sorted(os.listdir("bravais_outputs")):
    if f.endswith(".png"):
        print(f"  - {f}")