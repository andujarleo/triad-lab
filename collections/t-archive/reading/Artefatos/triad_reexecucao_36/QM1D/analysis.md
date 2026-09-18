> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/QM1D/analysis.md) · [Collection / Acervo](../../../../README.md)

# QM via Triad 1D — independent re-execution (P1–P6)

**Date:** 2026-08-21 15:16 -03 (America/Sao_Paulo)
**Dossier:** TRIAD — Dossiê unificado dos testes e simulações (2026-08-21)
**Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_QM1D.md`). No retuning. Failures kept.
**Stepper:** standalone 1D Strang, no triad-lang / TriadParams
**SHA256 (executed stepper):** `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`
**Runtime:** system python3 + numpy 2.2.4, fp64. Plots via `/workspace/.venv` matplotlib after CSVs existed.

Metric for interference/decoherence: spectral contrast of ρ=|Ψ|² at k=4,
C = 2 |∫ ρ e^{-i 4x} dx| / ∫ ρ dx. Not max/min.

---

## P1 Interference — PARTIAL

Same IC: two Gaussians s=1 at x=±8, k=∓2, L=80, N=1024, dt=0.002, measured at t=4 (overlap).

| regime | our vis (k=4) | our wf sideband | our mass \|x\|<4 | dossier vis | dossier mass |
|---|---:|---:|---:|---:|---:|
| linear | 1.000 | 0.934 | 0.825 | 0.998 (rigorous 0.942) | 0.700 |
| memory only (3,1) | 0.967 | 0.556 | 0.649 | 0.9995 | 0.557 |
| anti-collapse Λ=-10+mem | **0.511** | -0.679 | 0.768 | 0.9996 | 0.976 |
| cubic only Λ=-10 | **0.611** | 0.138 | 0.961 | 1.000 | 0.926 |

- Prediction “vis ≳ 0.9 in all deterministic regimes”: **held for linear and memory; failed for anti-collapse and cubic**. Kept.
- Memory changes the envelope, does not erase the fringe: mass 0.825 → 0.649 (dossier 0.700 → 0.557). Pattern match.
- Cubic pulls mass inward (0.961). Anti-collapse central mass 0.768 is *between* linear and memory — not the dossier’s 0.976 inward pile-up.
- Linear wf-sideband 0.934 is the closest match to their “contraste espectral rigoroso 0.942”.
- Surprise: focusing (Λ=-10) drops the k=4 density contrast well below 0.9. Dossier table ~1.0 was not reproduced with this metric; possible they used a different isolation window or a max/min leftover for the “visibilidade” column.

Norm conserved to 1e-12 in all four (unitary).

## P2 Decoherence — MATCH (pattern)

Γ=0.05, f_FDT sweep, 6 seeds, same t=4, spectral contrast of ρ (not max/min).

| f_FDT | our shot | our ensemble ρ | dossier shot | dossier ensemble |
|---|---|---|---|---|
| 0 | 1.000 ± 0 | 1.000 | 0.942 | 0.942 |
| 1e-3 | 0.169 ± 0.037 | 0.165 | 0.50 ± 0.12 | 0.50 |
| 1e-2 | 0.053 ± 0.014 | 0.020 | 0.18 ± 0.08 | 0.046 |
| 3e-2 | 0.048 ± 0.020 | 0.008 | 0.19 | 0.09* |
| 1e-1 | 0.047 ± 0.022 | 0.005 | 0.20 | 0.12* |

- Ensemble contrast falls as f_FDT rises. Single-shot stays above the ensemble at f≥1e-2 (fringe lives in the shot, dies in the average).
- f=0: shot = ensemble (deterministic).
- Numbers are **not** the dossier’s (we decohere faster at 1e-3). Not retuned.
- Diagnostic |Ψ̂|² carrier-vs-sideband also falls (1e-1: 0.034); it does **not** saturate. Max/min was not used.

## P3 Uncertainty — MATCH

| state | our σx σp | dossier |
|---|---:|---:|
| gaussian s=1 | 0.500000 | 0.5000 |
| gaussian s=0.4 | 0.500000 | 0.5000 |
| P1 linear t=4 (fringed) | 6.185 | 6.54 |

ħ/2 = 0.5 respected. Dynamics cannot violate it. Fringed state > 0.5.

## P4 Quantization — PARTIAL

Harmonic ω=1, L=20, N=512, dt=0.01, IC gaussian s=1 at x0=1.2.
Peaks of FFT(c(t)) on the **negative** numpy-FFT axis, E=-ω.

**Long linear T=251.33 (2π/T=0.025):** leak |Ψ|²_edge/max = 2.3e-27 < 1e-6.

| n | our E | dossier | n+1/2 | our err |
|---|---:|---:|---:|---:|
| 0 | 0.5000 | 0.5027 | 0.5 | 0.0000 |
| 1 | 1.4999 | 1.5080 | 1.5 | 0.0001 |
| 2 | 2.4999 | 2.4881 | 2.5 | 0.0001 |
| 3 | 3.4998 | 3.4935 | 3.5 | 0.0002 |
| 4 | 4.4998 | 4.4988 | 4.5 | 0.0002 |

Linear ladder MATCH (closer to exact n+1/2 than the dossier).

**T=80 extras** (bin 2π/T=0.0785):

| config | our lowest 4 | dossier | leak |
|---|---|---|---:|
| linear | 0.471, 1.492, 2.513, 3.534 | 0.50, 1.50, 2.50, 3.50 | ~0 |
| Λ=+2 | 0.236, **1.178, 2.199**, 2.906 | 1.20, 2.20, 3.19, 4.19 | ~0 |
| Λ=-2 | 0.550, 0.864, 1.571, 1.885 | 0.52, 0.89, 1.52, 2.51 | ~0 |
| Λ=-2+mem(3,1) | 0.471, 0.707, 1.021, 2.042 | 0.52, 1.52, 1.99, 2.99 | **0.642** |

- Λ=+2: two strongest peaks sit at 1.178 / 2.199 (dossier 1.20 / 2.20). Extra weak 0.236; 3.19/4.19 not in our top-4.
- Λ=-2: first three near dossier; fourth 1.885 vs 2.51.
- **Λ=-2+mem FAIL:** boundary leak 0.64. Repulsive memory (λ=3+1) filled the well and pushed mass to the periodic edge of L=20. Spectrum is not a confined HO ladder. Kept. Dossier did not report a leak.

## P5 Tunneling — MATCH

Linear, E=2, a=1 square barrier on [-0.5,0.5], L=80, N=2048, s=2, x0=-20, k0=2, T=20.
T_trans = mass(x>0.5)/total.

| V0 | our T | dossier T | √(V0-E) |
|---|---:|---:|---:|
| 2.5 | 0.351 | 0.353 | 0.707 |
| 3.0 | 0.230 | 0.231 | 1.000 |
| 4.0 | 0.095 | 0.095 | 1.414 |
| 5.0 | 0.041 | 0.040 | 1.732 |
| 6.0 | 0.020 | 0.018 | 2.000 |

ln T vs √(V0-E): slope **-2.24** (dossier -2.33; WKB -2√2 = -2.83). Order -2 to -3. T>0 always.

## P6 Ehrenfest — MATCH

Linear HO ω=1, gaussian x0=2, s=1, k0=0, T=20, dt=0.01, L=20, N=512.
max |⟨x⟩ - 2 cos(t)| = **1.52e-4** ≪ 1e-3 (dossier 1.6e-6). Same identity, larger dt.

---

## Scoreboard

| pillar | verdict | vs dossier |
|---|---|---|
| P1 Interference | PARTIAL | envelope pattern yes; vis ≳0.9 fails under focusing |
| P2 Decoherence | MATCH | pattern; we decohere faster numerically |
| P3 Uncertainty | MATCH | 0.5000 / 0.5000 / 6.19 vs 6.54 |
| P4 Quantization | PARTIAL | linear ladder exact; mem T=80 leaks |
| P5 Tunneling | MATCH | T table and slope |
| P6 Ehrenfest | MATCH | 1.52e-4 ≪ 1e-3 |

CHSH was not run.

## Files

- predictions (before integration): `/workspace/dossie_reexec/predictions_QM1D.md`
- stepper: `/workspace/dossie_reexec/QM1D/code/stepper1d.py`
- runner: `/workspace/dossie_reexec/QM1D/code/run_pillars.py`
- raw CSVs: `/workspace/dossie_reexec/QM1D/raw/`
- figures: `/workspace/dossie_reexec/QM1D/figures/`
- machine result: `/workspace/dossie_reexec/QM1D/result.json`
