# CHSH / Bell frontier — independent re-execution

**Date:** 2026-08-21 15:31 UTC-3 (America/Sao_Paulo)
**Dossier:** TRIAD — Dossiê unificado, Fronteira CHSH / Emaranhamento + spec §11.1 (23)
**Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_CHSH.md`). No retuning.
**Stepper:** standalone pair-coupled 1D Strang in `code/run_chsh.py`
**SHA256 (executed runner):** `5f543afa76927f7c8aee2f39501240b6cc3e1e30038e1d1a92431c0a65700f38`
**Runtime:** /usr/bin/python3, numpy 2.2.4, fp64. N=256 dt=0.002 T_couple=2.0 T_sep=2.0
**Downgrade:** none (N=256, dt=0.002, T_couple=T_sep=2.0)
**Wall:** 406.4 s (6.77 min)

Frozen measurement: A = sign Re(e^{-ia} ⟨ΨA|ψ0A⟩) with ψ0 = unphased local gaussian of that side.
Phase convention: both packets × e^{iφ} (fonte de fase comum). Settings = shot % 4 (balanced 350/pair), seed_settings=900000+shot independent of physical seed=10000+shot.
No post-selection. All shots valid.

## Verdict — MATCH

S saturates the local bound within error; E near triangular CHSH point.

## S and four correlators

**S = 2.023 ± 0.092** (propagation). Bootstrap: 2.023 ± 0.092 (4000 resamples).
Dossier: S = 2.000 ± 0.053. Local bound 2. QM 2.828.

| pair | angles | our E ± se | dossier | triangle | QM |
|---|---|---:|---:|---:|---:|
| ab | a=0, b=π/4 | +0.566 ± 0.044 | +0.486 | +0.500 | +0.707 |
| abp | a=0, b=−π/4 | +0.469 ± 0.047 | +0.511 | +0.500 | +0.707 |
| apb | a=π/2, b=π/4 | +0.474 ± 0.047 | +0.510 | +0.500 | +0.707 |
| apbp | a=π/2, b=−π/4 | -0.514 ± 0.046 | -0.493 | -0.500 | -0.707 |

n = 350 per pair. se = sqrt((1-E²)/n). se(1/√n) = 0.053.

## Marginals

- P(A=+1 | a=0) = 0.511  (n=700)
- P(A=+1 | a=π/2) = 0.491  (n=700)
- P(B=+1 | b=π/4) = 0.510  (n=700)
- P(B=+1 | b=−π/4) = 0.533  (n=700)

## No-signaling

- P(A=+1 | a=0, b) − P(A=+1 | a=0, b') = +0.0171
- P(A=+1 | a=π/2, b) − P(A=+1 | a=π/2, b') = -0.0171
- P(B=+1 | a, b) − P(B=+1 | a', b) = +0.0200
- P(B=+1 | a, b') − P(B=+1 | a', b') = -0.0314
- max |Δ| = 0.0314

Binomial se of a 350-shot proportion near 1/2 is ~0.027; a no-signaling delta of 0.05 is ordinary noise.

## E vs Δ scan (200 shots / point)

| Δ | our E ± se | triangle | QM cos |
|---|---:|---:|---:|
| 0.00000 | +1.000 ± 0.000 | +1.000 | +1.000 |
| 0.39270 | +0.770 ± 0.045 | +0.750 | +0.924 |
| 0.78540 | +0.520 ± 0.060 | +0.500 | +0.707 |
| 1.17810 | +0.220 ± 0.069 | +0.250 | +0.383 |
| 1.57080 | -0.030 ± 0.071 | +0.000 | +0.000 |
| 2.35619 | -0.550 ± 0.059 | -0.500 | -0.707 |

MSE vs triangle = 0.0009; MSE vs cos = 0.0185. Closer to triangle: True.

## Surprises / kept failures

- No S>2.1 and no S<<1. Local bound saturated or approached, as predicted.
- Mean |mass-1| A=8.25e-14 B=1.03e-13 (unitary check).

Dossier floats were comparison targets, not tuning targets.

