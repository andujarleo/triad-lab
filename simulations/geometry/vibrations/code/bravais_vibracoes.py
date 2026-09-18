#!/usr/bin/env python3
"""
Vibrações das cordas
====================
Não roda a dinâmica completa — lê o estado final salvo (final_state.npz),
extrai as notas (modos fortes do espectro) e TOCA essas notas: cada modo k
oscila com a frequência que a própria equação dá pro seu pedaço linear
(ω = k²/2, o termo cinético que está escrito na equação de base — nenhuma
frequência inventada). O resto é reconstrução e desenho.

Saídas:
  vib_corda_fundamental.png  a corda mais forte vibrando: quadros de um
                             ciclo sobrepostos, como corda dedilhada
  vib_acorde.png             o acorde: amplitude × frequência de cada nota
                             + a relação ω(|k|) que a equação impõe
  vib_filme.png              a superposição das notas evoluindo: fatia
                             central em 8 instantes de um ciclo longo
  vib_batimento.png          a densidade num ponto ao longo do tempo (o
                             "som" do acorde) e seu espectro de frequências
  vib_filme.gif              (opcional, se Pillow disponível) animação

Uso:
  python3 bravais_vibracoes.py                     (usa final_state.npz)
  python3 bravais_vibracoes.py caminho/arquivo.npz
  L=32 NOTAS=24 python3 bravais_vibracoes.py
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.colors import LinearSegmentedColormap

path = sys.argv[1] if len(sys.argv) > 1 else "bravais_outputs_3d/final_state.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o bravais_puro_3d.py antes" % path)
dat = np.load(path)
rho = dat["rho_f"]
psi = dat["psi_f"] if "psi_f" in dat.files else None
N = rho.shape[0]
L = float(os.environ.get("L", 32.0))
M_NOTES = int(os.environ.get("NOTAS", 24))
dx = L / N
os.makedirs("bravais_outputs_3d", exist_ok=True)

cmap_life = LinearSegmentedColormap.from_list(
    "life", ["#0b132b", "#1c2541", "#3a506b", "#5bc0be", "#f4d35e", "#ee6c4d"]
)

# ---------------------------------------------------------------- notas
# usa a FFT de Ψ se disponível (amplitude E fase verdadeiras); senão a de ρ
field_k = np.fft.fftshift(np.fft.fftn(psi)) if psi is not None else \
          np.fft.fftshift(np.fft.fftn(rho))
power = np.abs(field_k) ** 2
power[N // 2, N // 2, N // 2] = 0.0
flat = np.argsort(power.ravel())[::-1]
seen = set()
notes = []  # (kvec, amplitude complexa)
for fi in flat:
    ijk = np.unravel_index(fi, power.shape)
    kvec = (np.array(ijk) - N // 2) * (2 * np.pi / L)
    key = tuple(np.round(np.abs(kvec), 6))
    if key in seen:
        continue
    seen.add(key)
    notes.append((kvec, field_k[ijk] / power.max() ** 0.5))
    if len(notes) >= M_NOTES:
        break

def omega(kvec):
    """Frequência do pedaço linear da própria equação: ω = |k|²/2."""
    return 0.5 * float(np.dot(kvec, kvec))

omegas = np.array([omega(kv) for kv, _ in notes])
amps = np.array([np.abs(a) for _, a in notes])
knorms = np.array([np.linalg.norm(kv) for kv, _ in notes])
T_fund = 2 * np.pi / omegas[np.argmax(amps)]  # período da nota mais forte

print("notas extraídas: %d | fonte: %s" % (len(notes), "Ψ" if psi is not None else "ρ"))
print("nota mais forte: |k|=%.2f  ω=%.2f  T=%.2f" % (knorms[np.argmax(amps)],
      omegas[np.argmax(amps)], T_fund))

# ------------------------------------------- 1) corda fundamental vibrando
i0 = int(np.argmax(amps))
kv0, a0 = notes[i0]
kn0 = np.linalg.norm(kv0)
u = kv0 / kn0
ref = np.array([0.0, 0.0, 1.0]) if abs(u[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
w1 = np.cross(u, ref); w1 /= np.linalg.norm(w1)
s = np.linspace(-L / 2, L / 2, 400)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection="3d")
nframes = 10
for fi in range(nframes):
    t = fi / nframes * (2 * np.pi / omega(kv0))
    prof = np.real(a0 * np.exp(1j * (kn0 * s - omega(kv0) * t)))
    prof = 2.5 * prof / (np.abs(a0) + 1e-30)
    line = np.outer(s, u) + np.outer(prof, w1)
    inside = np.all(np.abs(line) <= L / 2, axis=1)
    col = cmap_life(0.15 + 0.8 * fi / (nframes - 1))
    ax.plot(line[inside, 0], line[inside, 1], line[inside, 2],
            color=col, lw=1.8, alpha=0.85)
ax.set_xlim(-L / 2, L / 2); ax.set_ylim(-L / 2, L / 2); ax.set_zlim(-L / 2, L / 2)
ax.set_title("A corda mais forte vibrando — %d quadros de um ciclo\n"
             "|k|=%.2f, ω=%.2f (do termo cinético da própria equação)"
             % (nframes, kn0, omega(kv0)))
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vib_corda_fundamental.png", dpi=150, bbox_inches="tight")
plt.close()
print("vib_corda_fundamental.png")

# ------------------------------------------- 2) o acorde
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
order = np.argsort(omegas)
axes[0].stem(omegas[order], amps[order] / amps.max(), basefmt=" ")
axes[0].set_xlabel("frequência ω da nota")
axes[0].set_ylabel("amplitude relativa")
axes[0].set_title("o acorde que o sistema está tocando")
axes[0].grid(alpha=0.3)
axes[1].plot(knorms, omegas, "o", color="#ee6c4d", ms=7, alpha=0.8)
kk = np.linspace(0, knorms.max() * 1.05, 100)
axes[1].plot(kk, 0.5 * kk**2, "--", color="#3a506b", alpha=0.7,
             label="ω = |k|²/2 (da equação)")
axes[1].set_xlabel("|k| da nota"); axes[1].set_ylabel("ω")
axes[1].legend(); axes[1].grid(alpha=0.3)
axes[1].set_title("relação nota→frequência usada")
plt.suptitle("2) O acorde — %d notas mais fortes" % len(notes), fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vib_acorde.png", dpi=140, bbox_inches="tight")
plt.close()
print("vib_acorde.png")

# ------------------------------------------- 3) superposição evoluindo
x = np.linspace(-L / 2, L / 2, N, endpoint=False)
X2, Y2 = np.meshgrid(x, x, indexing="ij")  # fatia z=0

def field_slice(t):
    f = np.zeros((N, N), dtype=np.complex128)
    for kv, a in notes:
        phase = kv[0] * X2 + kv[1] * Y2  # z=0
        f += a * np.exp(1j * (phase - omega(kv) * t))
    return np.abs(f) ** 2

T_show = 3.0 * T_fund
frames_t = np.linspace(0, T_show, 8, endpoint=False)
fig, axes = plt.subplots(2, 4, figsize=(14, 7))
snaps = [field_slice(t) for t in frames_t]
vmax = max(sn.max() for sn in snaps)
for ax, t, sn in zip(axes.flat, frames_t, snaps):
    ax.imshow(sn.T, origin="lower", cmap="magma", vmin=0, vmax=vmax,
              extent=[-L / 2, L / 2, -L / 2, L / 2])
    ax.set_title("t = %.2f" % t, fontsize=9)
    ax.set_xticks([]); ax.set_yticks([])
plt.suptitle("3) As notas tocando juntas — fatia z=0 da superposição, um ciclo longo",
             fontsize=13)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vib_filme.png", dpi=140, bbox_inches="tight")
plt.close()
print("vib_filme.png")

# gif opcional
try:
    from matplotlib.animation import FuncAnimation, PillowWriter

    figa, axa = plt.subplots(figsize=(5, 5))
    im = axa.imshow(snaps[0].T, origin="lower", cmap="magma", vmin=0, vmax=vmax,
                    extent=[-L / 2, L / 2, -L / 2, L / 2])
    axa.set_xticks([]); axa.set_yticks([])
    tt = np.linspace(0, T_show, 40, endpoint=False)

    def upd(fi):
        im.set_data(field_slice(tt[fi]).T)
        axa.set_title("t = %.2f" % tt[fi], fontsize=10)
        return [im]

    ani = FuncAnimation(figa, upd, frames=len(tt), blit=False)
    ani.save("bravais_outputs_3d/vib_filme.gif", writer=PillowWriter(fps=10), dpi=90)
    plt.close(figa)
    print("vib_filme.gif")
except Exception as e:
    print("(gif pulado: %s)" % e)

# ------------------------------------------- 4) batimento (o "som")
tt = np.linspace(0, 30.0 * T_fund, 4096)
sig = np.zeros(len(tt), dtype=np.complex128)
for kv, a in notes:  # densidade no ponto central x=0: fases todas zero em x
    sig += a * np.exp(-1j * omega(kv) * tt)
dens_t = np.abs(sig) ** 2
freqs = np.fft.rfftfreq(len(tt), d=tt[1] - tt[0]) * 2 * np.pi
spec = np.abs(np.fft.rfft(dens_t - dens_t.mean()))

fig, axes = plt.subplots(2, 1, figsize=(11, 7))
axes[0].plot(tt / T_fund, dens_t, color="#3a506b", lw=0.8)
axes[0].set_xlabel("tempo (em períodos da nota mais forte)")
axes[0].set_ylabel("densidade no centro")
axes[0].set_title("o som do acorde — batimentos da superposição")
axes[0].grid(alpha=0.3)
axes[1].plot(freqs, spec / spec.max(), color="#ee6c4d", lw=1.2)
axes[1].set_xlim(0, np.percentile(omegas, 95) * 2.5)
axes[1].set_xlabel("frequência ω")
axes[1].set_ylabel("amplitude")
axes[1].set_title("espectro do som — as diferenças entre as notas (ω_i − ω_j)")
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig("bravais_outputs_3d/vib_batimento.png", dpi=140, bbox_inches="tight")
plt.close()
print("vib_batimento.png")

print("\nimagens em bravais_outputs_3d/: vib_corda_fundamental.png, "
      "vib_acorde.png, vib_filme.png, vib_batimento.png (+ vib_filme.gif se Pillow)")
if psi is None:
    print("nota: sem psi_f no npz as fases das notas vêm de ρ (menos fiéis); "
          "rode o bravais_puro_3d.py atualizado pra salvar Ψ")
