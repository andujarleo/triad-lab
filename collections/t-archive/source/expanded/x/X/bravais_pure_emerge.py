#!/usr/bin/env python3
"""
Bravais puro emergente
======================
Regras rígidas:
  - nenhum termo isolado
  - nenhuma calibração de coeficiente
  - nenhum forçar colapso / norma alvo
  - nenhum set_personality / set_lattice / set_Lambda
  - tudo sai de UMA proposta acoplada + ponto fixo implícito
  - normalização só se a norma explodir numericamente (proteção, não física)

VERSÃO restaurada (antes da troca por split-step / "explosão numérica").
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import maximum_filter
import os

np.random.seed(None)
os.makedirs("bravais_outputs", exist_ok=True)

L = 48.0
N = 160
dx = L / N
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
X, Y = np.meshgrid(x, x, indexing="ij")
k1 = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY = np.meshgrid(k1, k1, indexing="ij")
K2 = KX**2 + KY**2
Kabs = np.sqrt(K2 + 1e-30)


def multi_gaussian_field(n_centers=12):
    psi = np.zeros((N, N), dtype=np.complex128)
    centers = np.random.uniform(-0.3 * L, 0.3 * L, size=(n_centers, 2))
    widths = np.random.uniform(2.0, 4.5, size=n_centers)
    amps = np.random.uniform(0.3, 1.0, size=n_centers)
    for (cx, cy), w, amp in zip(centers, widths, amps):
        phase = np.exp(1j * np.random.uniform(0, 2 * np.pi))
        psi += amp * phase * np.exp(-((X - cx) ** 2 + (Y - cy) ** 2) / (2 * w**2))
    psi += 0.05 * (np.random.randn(N, N) + 1j * np.random.randn(N, N))
    return psi


psi0 = multi_gaussian_field(12)

Z = {
    "h": np.zeros(4),
    "b": np.zeros(4),
    "a": np.zeros(4),
    "n": np.zeros(4),
    "g": np.zeros(4),
    "ell": np.zeros(8),
    "v": np.zeros(6),
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


def psi_numeric_guard(psi):
    """
    Só age se a norma explodir ou colapsar numericamente.
    NÃO impõe norma alvo fixa a cada passo.
    """
    nrm2 = np.sum(np.abs(psi) ** 2) * dx * dx
    if not np.isfinite(nrm2) or nrm2 > 1e6:
        psi = np.nan_to_num(psi, nan=0.0, posinf=0.0, neginf=0.0)
        nrm2 = np.sum(np.abs(psi) ** 2) * dx * dx
    if nrm2 < 1e-12:
        psi = psi + 1e-3 * (np.random.randn(N, N) + 1j * np.random.randn(N, N))
        nrm2 = np.sum(np.abs(psi) ** 2) * dx * dx
    if nrm2 > 100.0:
        psi = psi * np.sqrt(50.0 / nrm2)
    return psi


def experience_signature(psi, Z):
    rho = np.abs(psi) ** 2
    mean_rho = np.mean(rho) + 1e-12
    std_rho = np.std(rho)
    fft = np.abs(np.fft.fft2(rho))
    order_energy = np.sum(fft**2) - fft[0, 0] ** 2
    order_energy = order_energy / (np.sum(fft**2) + 1e-12)

    gx = np.roll(rho, -1, 0) - np.roll(rho, 1, 0)
    gy = np.roll(rho, -1, 1) - np.roll(rho, 1, 1)
    rough = np.mean(gx**2 + gy**2)

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
    h = Z_mid["h"]
    b = Z_mid["b"]

    drive = np.tanh(chi[:8] + 0.2 * ell)
    prop_h = drive[:4]
    prop_b = drive[4:8]
    prop_a = np.tanh(chi[:4] + 0.3 * a + 0.1 * n)
    prop_n = np.tanh(chi[4:8] + 0.3 * n + 0.1 * a)
    prop_g = np.tanh(chi[:4] + 0.25 * g + 0.1 * b)
    prop_ell = np.tanh(chi[:8] + 0.2 * ell + 0.05 * np.concatenate([a, n]))
    prop_v = np.tanh(chi[2:8] + 0.15 * v)

    radial = np.exp(-(X**2 + Y**2) / (0.25 * L**2 + 1e-8))
    e0, e1, e2, e3 = ell[0], ell[1], ell[2], ell[3]
    v0, v1, v2, v3 = v[0], v[1], v[2], v[3]

    Lambda_scalar = np.tanh(e0 + 0.3 * chi[0] + 0.2 * a[0])
    alpha_scalar = 0.5 * (1.0 + np.tanh(e1 + 0.3 * chi[1]))
    Gamma_scalar = 0.5 * (1.0 + np.tanh(e2 + 0.3 * chi[2]))
    eta_scalar = 0.5 * (1.0 + np.tanh(e3 + 0.3 * chi[3]))
    sigma_frac = 1.0 + 0.5 * np.tanh(v0 + chi[4])

    fx = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v0))
    fy = (2.0 * np.pi / L) * (3.0 + 2.0 * np.tanh(v1))
    fxy = (2.0 * np.pi / L) * (2.0 + 2.0 * np.tanh(v2))

    V_mem = (
        np.tanh(e0) * radial
        + np.tanh(e1) * np.sin(fx * X + np.tanh(v3))
        + np.tanh(e2) * np.sin(fy * Y + np.tanh(v[4] if len(v) > 4 else v0))
        + np.tanh(e3) * np.cos(fxy * (X + Y))
        + 0.3 * np.tanh(a[0]) * np.sin(fx * Y - fy * X)
    )
    V_scale = 0.5 * (1.0 + np.tanh(g[0] + chi[5]))
    V_mem = V_scale * V_mem
    V_ext = 0.15 * np.tanh(g[1]) * ((X / (L / 2)) ** 2 + (Y / (L / 2)) ** 2)

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

    psi_k = np.fft.fft2(psi)
    kinetic = np.fft.ifft2(-0.5 * K2 * psi_k)
    frac = prop["alpha"] * np.fft.ifft2((Kabs ** prop["sigma"]) * psi_k)
    damp = -1j * prop["Gamma"] * 0.05 * psi
    noise = prop["eta"] * 0.02 * (
        np.random.randn(N, N) + 1j * np.random.randn(N, N)
    )

    dpsi = -1j * (kinetic + V * psi + frac) + damp + noise
    return psi + dt * dpsi


def coupled_step(Z, dt=0.02, max_iter=5):
    Z0 = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}
    Zcur = {k: (v.copy() if isinstance(v, np.ndarray) else v) for k, v in Z.items()}

    metrics = None
    prop = None
    for _ in range(max_iter):
        Zmid = {}
        for k in Z0:
            Zmid[k] = 0.5 * (Z0[k] + Zcur[k])

        chi, metrics = experience_signature(Zmid["psi"], Zmid)
        prop = coupled_proposal(chi, Zmid)

        keys = ["h", "b", "a", "n", "g", "ell", "v"]
        raw = {}
        for k in keys:
            raw[k] = prop[k] - Zmid[k]

        stack = np.concatenate([raw[k] for k in keys])
        stack = soft_bound(stack, cap=1.0)
        out = {}
        i0 = 0
        for k in keys:
            n = raw[k].size
            out[k] = stack[i0 : i0 + n]
            i0 += n

        for k in keys:
            Zcur[k] = project_state_vector(Z0[k] + out[k], radius=2.5)

        psi_new = psi_flow(Zmid["psi"], prop, dt)
        Zcur["psi"] = psi_numeric_guard(psi_new)

        if np.linalg.norm(Zcur["ell"] - Zmid["ell"]) < 1e-3:
            break

    return Zcur, metrics, prop


print("Iniciando trajetória emergente (versão restaurada pré-split-step)")
print("domínio: %.1f x %.1f | N=%d | multi-gaussianos iniciais" % (L, L, N))

STEPS = 800
dt = 0.025
history = {
    "order": [],
    "mean_rho": [],
    "std_rho": [],
    "ell_norm": [],
    "v": [],
    "Lambda": [],
    "alpha": [],
    "Gamma": [],
    "norm": [],
}
snapshots = {}
snap_at = {0, 100, 200, 400, 600, 799}

for t in range(STEPS):
    Z, metrics, prop = coupled_step(Z, dt=dt)
    rho = np.abs(Z["psi"]) ** 2
    nrm = np.sqrt(np.sum(rho) * dx * dx)

    history["order"].append(metrics["order"])
    history["mean_rho"].append(metrics["mean_rho"])
    history["std_rho"].append(metrics["std_rho"])
    history["ell_norm"].append(np.linalg.norm(Z["ell"]))
    history["v"].append(Z["v"].copy())
    history["Lambda"].append(prop["Lambda"])
    history["alpha"].append(prop["alpha"])
    history["Gamma"].append(prop["Gamma"])
    history["norm"].append(nrm)

    if t in snap_at:
        snapshots[t] = rho.copy()

    if t % 100 == 0:
        print(
            "t=%4d | order=%.4f | |ell|=%.3f | Λ=%.3f | ‖ψ‖=%.3f | ⟨ρ⟩=%.4f"
            % (
                t,
                metrics["order"],
                history["ell_norm"][-1],
                prop["Lambda"],
                nrm,
                metrics["mean_rho"],
            )
        )

print("trajetória concluída.\n")

cmap_life = LinearSegmentedColormap.from_list(
    "life",
    ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"],
)

times = sorted(snapshots.keys())
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
for ax, t in zip(axes.flat, times):
    dens = snapshots[t]
    ax.imshow(
        dens.T,
        extent=[-L / 2, L / 2, -L / 2, L / 2],
        origin="lower",
        cmap="magma",
        interpolation="bilinear",
    )
    ax.set_title("t = %d" % t)
    ax.set_xticks([])
    ax.set_yticks([])
plt.suptitle("Densidade |Ψ|² — versão restaurada (pré-split-step)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs/pure_evolution.png", dpi=150, bbox_inches="tight")
plt.close()

rho_f = snapshots[times[-1]]
thr = np.mean(rho_f) + 1.0 * np.std(rho_f)
local_max = (rho_f == maximum_filter(rho_f, size=5)) & (rho_f > thr)
peaks = np.argwhere(local_max)
pvals = rho_f[peaks[:, 0], peaks[:, 1]] if len(peaks) else np.array([])

fig, ax = plt.subplots(figsize=(9, 8))
im = ax.imshow(
    rho_f.T,
    extent=[-L / 2, L / 2, -L / 2, L / 2],
    origin="lower",
    cmap="magma",
    interpolation="bilinear",
)
if len(peaks):
    sizes = 120 + 200 * (pvals - pvals.min()) / (np.ptp(pvals) + 1e-12)
    colors = cmap_life(np.linspace(0.2, 0.95, len(peaks)))
    ax.scatter(
        peaks[:, 0] * dx - L / 2,
        peaks[:, 1] * dx - L / 2,
        s=sizes,
        c=colors,
        edgecolors="white",
        linewidths=0.4,
        zorder=5,
    )

v = Z["v"]
scale = L / 8.0
a1 = scale * np.array([1.0 + 0.3 * np.tanh(v[0]), 0.3 * np.tanh(v[2])])
a2 = scale * np.array([0.3 * np.tanh(v[3]), 1.0 + 0.3 * np.tanh(v[1])])
ax.annotate(
    "",
    xy=a1,
    xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", color="#5bc0be", lw=2),
)
ax.annotate(
    "",
    xy=a2,
    xytext=(0, 0),
    arrowprops=dict(arrowstyle="->", color="#f4d35e", lw=2),
)
ax.text(a1[0] * 1.05, a1[1] * 1.05, r"$a_1$", color="#5bc0be", fontsize=12)
ax.text(a2[0] * 1.05, a2[1] * 1.05, r"$a_2$", color="#f4d35e", fontsize=12)
ax.set_title(
    "Estado final emergente | picos≈%d | |ℓ|=%.3f | Λ=%.3f"
    % (len(peaks), history["ell_norm"][-1], history["Lambda"][-1])
)
plt.colorbar(im, ax=ax, fraction=0.046, label=r"$|\Psi|^2$")
plt.tight_layout()
plt.savefig("bravais_outputs/pure_final.png", dpi=160, bbox_inches="tight")
plt.close()

fft = np.fft.fftshift(np.abs(np.fft.fft2(rho_f)))
fig, ax = plt.subplots(figsize=(6, 5))
ax.imshow(np.log1p(fft).T, origin="lower", cmap="viridis")
ax.set_title("Espectro log|FFT(ρ)| — periodicidade emergente")
ax.set_xticks([])
ax.set_yticks([])
plt.tight_layout()
plt.savefig("bravais_outputs/pure_fft.png", dpi=140, bbox_inches="tight")
plt.close()

fig, axes = plt.subplots(3, 2, figsize=(11, 9))
axes[0, 0].plot(history["order"], color="#ee6c4d")
axes[0, 0].set_title("ordem (energia modal relativa)")
axes[0, 1].plot(history["norm"], color="#3a506b")
axes[0, 1].set_title(r"norma $\|\psi\|$ (não fixada)")
axes[1, 0].plot(history["Lambda"], color="#5bc0be", label="Λ")
axes[1, 0].plot(history["alpha"], color="#f4d35e", label="α", alpha=0.8)
axes[1, 0].plot(history["Gamma"], color="#ee6c4d", label="Γ", alpha=0.8)
axes[1, 0].legend(fontsize=8)
axes[1, 0].set_title("coeficientes emergentes (mesma proposta)")
axes[1, 1].plot(history["ell_norm"], color="#1c2541")
axes[1, 1].set_title(r"$|\ell(t)|$ campo latente de vida")
v_arr = np.array(history["v"])
for j in range(6):
    axes[2, 0].plot(v_arr[:, j], alpha=0.85, label="v%d" % j)
axes[2, 0].legend(ncol=3, fontsize=7)
axes[2, 0].set_title("parâmetros de rede v (emergentes)")
axes[2, 1].plot(history["mean_rho"], label="⟨ρ⟩")
axes[2, 1].plot(history["std_rho"], label="std ρ")
axes[2, 1].legend(fontsize=8)
axes[2, 1].set_title("densidade média / flutuação")
for ax in axes.flat:
    ax.grid(True, alpha=0.25)
    ax.set_xlabel("passo")
plt.suptitle("Dinâmica acoplada — versão restaurada (pré-split-step)", fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs/pure_timeseries.png", dpi=140, bbox_inches="tight")
plt.close()

print("Imagens salvas em bravais_outputs/:")
for f in [
    "pure_evolution.png",
    "pure_final.png",
    "pure_fft.png",
    "pure_timeseries.png",
]:
    print("  -", f)

print("\nResumo final:")
print("  order     =", history["order"][-1])
print("  |ell|     =", history["ell_norm"][-1])
print("  Lambda    =", history["Lambda"][-1], "(emergiu, pode ser + ou -)")
print("  ||psi||   =", history["norm"][-1], "(não foi forçada a alvo)")
print("  picos     =", len(peaks))
print("  v final   =", np.round(Z["v"], 3))
