# Bravais detector calibration — analysis

Label: live calibration of spec §8.4 against random networks of the same
node density. **Not** a change of Leonardo's full-triad operational
reading. **Not** a claim that the dossier R5 N48 run was a BCC crystal.

Predictions were written **first** to
`/workspace/dossie_reexec/predictions_bravais.md`
(SHA256 `c8481dd40aac49020cad253f68e424bc0acbb51274892de4feb13388eea309f7`)
at 17:32 -03, before `detector.py` and before any Strang step.
Window **0.15 is frozen**. No `observables.py`. Stepper reused from
`/workspace/dossie_reexec/A3/code/stepper.py`
(SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`).
`/workspace/dossie_reexec/kstar/` had code only, no finished snapshot —
this field was integrated here (wall 100.3 s). Finished 2026-08-21
17:36:37 -03; extra same-density / resolved-shell floors 17:38 -03.

## Frozen rule

```
cos θ = max_{â in family} (k̂ · â)
aligned iff 1 − cos θ < 0.15     (θ < arccos(0.85) ≈ 31.79°)
score = aligned shell power / total shell power
shell: ||k| − k*| < 0.5 dk,  dk = 2π/L,  |k| > 0.5 dk
k* = centre of the radial-mean bin (width dk, n ≥ 1) with max ⟨|Ψ̂|²⟩
```

Families box-aligned, no rotation search. HCP: 6 in-plane in xy every
60° plus axial ±z. A family with more cones covers more of the sphere.
That is a detector bias, not a lattice. Window was not narrowed.

## Verdict

**no crystal.**

The R5 unitary field at N=64, T=8 never formed an isolated finite-k
shell. Its best Bravais score sits on the noise floor of the first
FFT cube (18 voxels). The leftover numbers 0.22 and 0.46 are not
lattice detections under this frozen detector: on a resolved shell
at the dossier attractor k*L=16.3, isotropic BCC already scores
0.931 ± 0.022 and isotropic SC 0.331 ± 0.040. 0.46 is *below* the
BCC floor; 0.22 is *below* the SC floor.

## Noise floor 1 — the field's own k* (first cube, 18 voxels)

k*(T) = 2π/L, k*L = 6.2832. That bin is exactly the 6×(100) + 12×(110)
voxels. (111) is not on this shell, so FCC is identically 0. Equal
power on the 18 voxels gives SC = 6/18 = 0.333, BCC = 12/18 = 0.667,
HCP ≈ 0.556. 32-seed draws confirm it.

### Isotropic complex-gaussian, injected field k* (32 seeds)

| family | mean | std | mean+2σ | min | max |
|---|---|---|---|---|---|
| SC | 0.3351 | 0.1138 | 0.5627 | 0.1063 | 0.6486 |
| BCC | 0.6649 | 0.1138 | 0.8925 | 0.3514 | 0.8937 |
| FCC | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| HCP | 0.5491 | 0.1072 | 0.7636 | 0.2855 | 0.7802 |
| BEST | 0.6956 | 0.0868 | 0.8692 | — | — |

### Poisson M = 1 (= (k*L/2π)³ on this bin)

Deterministic on this 18-voxel shell: SC=0.333, BCC=0.667, FCC=0,
HCP=0.556. A single spike is not a network; it is the geometric
occupancy of the first cube.

### Poisson M = 1179 (= n_local_max_prom of ρ at t=T)

Same *node* density as the field's prominence count (ripples of a
filled box, not crystal sites):

| family | mean | std | mean+2σ |
|---|---|---|---|
| SC | 0.3528 | 0.1666 | 0.6861 |
| BCC | 0.6472 | 0.1666 | 0.9805 |
| FCC | 0.0000 | 0.0000 | 0.0000 |
| HCP | 0.5741 | 0.1562 | 0.8865 |
| BEST | 0.7395 | 0.0827 | 0.9049 |

### Shell-randomized field |Ψ̂|² (32 permutations of the live shell)

| family | mean | std | mean+2σ |
|---|---|---|---|
| SC | 0.3329 | 0.0017 | 0.3362 |
| BCC | 0.6671 | 0.0017 | 0.6705 |
| FCC | 0.0000 | 0.0000 | 0.0000 |
| HCP | 0.5555 | 0.0018 | 0.5592 |
| BEST | 0.6671 | 0.0017 | 0.6705 |

Scrambling the field's own 18 voxels recovers 12/18. The live field
does not beat its scrambled self.

## Noise floor 2 — resolved shell k*L = 16.3 (90 voxels)

This is the shell people have in mind when they quote 0.22 vs 0.46
(dossier MI attractor). Same N, L, window. Not the field's k*.

### Isotropic, injected k*L=16.3 (32 seeds)

| family | mean | std | mean+2σ | min | max |
|---|---|---|---|---|---|
| SC | 0.3312 | 0.0395 | 0.4103 | 0.2609 | 0.4124 |
| BCC | 0.9307 | 0.0215 | 0.9738 | 0.8792 | 0.9699 |
| FCC | 0.5278 | 0.0548 | 0.6374 | 0.4162 | 0.6623 |
| HCP | 0.5092 | 0.0592 | 0.6277 | 0.4189 | 0.6710 |
| BEST | 0.9307 | 0.0215 | 0.9738 | 0.8792 | 0.9699 |

### Poisson M=1179 at the same resolved k*

| family | mean | std | mean+2σ |
|---|---|---|---|
| SC | 0.3403 | 0.0702 | 0.4808 |
| BCC | 0.9421 | 0.0263 | 0.9947 |
| FCC | 0.5450 | 0.0774 | 0.6999 |
| HCP | 0.5119 | 0.0649 | 0.6418 |
| BEST | 0.9421 | 0.0263 | 0.9947 |

Random points at the field's node count score BCC ≈ 0.94 on this
shell. **Same node density is not a Bravais signal.** BCC's floor is
high because 12 cones of half-angle 31.8° cover most of a 90-voxel
shell. Continuum no-overlap estimate was SC=0.45, BCC=0.90, FCC=0.60,
HCP=0.60; discrete draws sit in that order (BCC saturated near 0.93).

### Reading 0.22 vs 0.46 against this floor

| leftover number | claimed as | resolved-shell floor (this detector) | excess? |
|---|---|---|---|
| 0.46 | R5 N48 BCC | BCC 0.931 ± 0.022 (mean+2σ = 0.974) | **no** — below the floor |
| 0.22 | bounce PLANAR/SC | SC 0.331 ± 0.040 (mean+2σ = 0.410) | **no** — below the floor |

If a run scores 0.22 and random is 0.33, 0.22 is nothing.
If a run scores 0.46 and random BCC is 0.93, 0.46 is nothing.
0.46 vs a 0.20 SC floor would have been a real SC excess; it is not
the comparison that was being made. ×2 above the BCC floor is
geometrically impossible (floor ~0.93, ceiling 1). The window was
**not** tightened to manufacture a gap.

Those dossier floats came from other detectors / other N. They are
not re-measured here. What is measured is the floor of *this* §8.4
rule, which is the number you need before anyone reads them.

## Field — one R5 unitary (N=64)

Λ=−8, lam=(1.125, 0.375), ν=(10, 0.5), Γ=0, α=0, L=20, dt=0.0025,
T=8, s=0.5, seed=42. IC: one 3D gaussian, ∫|Ψ|² dV = 1.
peak_ini = 1.436697 (analytic). Norm conserved to ~1e-12.

| t | peak | PR | C | C★ | k*L | n_shell | n_prom | SC | BCC | FCC | HCP |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.437 | 1.97 | 0.995 | 0.012 | 6.283 | 18 | 1 | — | — | — | — |
| T=8 | 1.148e-3 | 2225 | 0.992 | 0.021 | 6.283 | 18 | 1179 | 0.3418 | 0.6582 | 0 | 0.5612 |
| max C★ = 6.10 | 7.743e-4 | 4130 | 0.992 | 0.021 | 6.283 | 18 | 2067 | 0.3418 | 0.6582 | 0 | 0.5612 |

C(t) is the spec §8.3 high-k fraction: a narrow gaussian is already
broadband (~0.99) and stays there. C★ (dominant-shell / non-DC) never
rises above 0.021 — there is no MI pile-up on a finite-k shell.
k* is stuck in the first radial bin for the whole run. R_rms(T) ≈ 9.95
(box half-width = 10): the packet filled the box. n_local_max_prom =
1179 is ripple noise, not (k*L/2π)³ ≈ 1 lattice sites.

Best family at t=T and at t=max C★: **BCC 0.658**.

- vs isotropic BCC mean 0.665 (mean+2σ = 0.893): ratio 0.990, **AT floor**
- vs shell-rand BCC mean 0.667 (mean+2σ = 0.670): **AT floor** (slightly under)
- vs Poisson M=1179 BCC mean 0.647 (mean+2σ = 0.980): **AT floor**

Prediction match: “R5 unitary at N=64 may or may not crystallize; if
it doesn't, the field score is also near the floor — report that
honestly.” It didn't. Score is the floor. Λ, λ, T, N, window were
not retuned.

|ρ̂|² at t=T is a secondary dump only (spec detector is |Ψ̂|²). It
peaked at k*L=50.3 (near Nyquist) with SC≈1 — that is a high-k
artefact of a filled noisy box, not a simple-cubic crystal. Not used
for the verdict.

## Self-check (synthetics, not the PDE)

Perfect box-aligned SC at a grid-commensurate k* scores SC=1 (HCP
also 1: ±z and the xy 60° net catch the axes). Perfect BCC scores
BCC≈1. Isotropic white noise at that k* already scores
SC~0.42 / BCC~0.84 / FCC~0.44 / HCP~0.61. Perfect FCC at a
non-commensurate k* leaks into BCC cones. Limitation of window 0.15
+ 12 BCC directions; window not narrowed.

## What this does to the leftover

Dossier item 5: “calibrar com rede aleatória de mesma densidade de
nós (score do ruído como baseline) antes de interpretar 0.22 vs 0.46.”

Done. The noise score is **not zero**. On the field's shell it is
~0.33 / 0.67 / 0 / 0.55 (SC/BCC/FCC/HCP). On a resolved k*L=16.3
shell it is ~0.33 / 0.93 / 0.53 / 0.51. A random network with the
same node count scores the same. 0.22 and 0.46 sit at or below those
floors. They are not evidence of two different crystals.

## Integrity

- predictions SHA256 `c8481dd40aac49020cad253f68e424bc0acbb51274892de4feb13388eea309f7`
- detector SHA256 `52fcb4151d27e77dc6e794e17f2e45a2aea9a96a47b7e85ea43a8efcc8cd8e8a`
- stepper SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`
- numpy 2.2.4, complex128 / float64, /usr/bin/python3; plots via /workspace/.venv
- no triad-lang; no observables.py; window not retuned
- Γ=0, no FDT; seed=42 locked

## Files

- predictions: `/workspace/dossie_reexec/predictions_bravais.md`
- detector: `/workspace/dossie_reexec/bravais/code/detector.py`
- runner: `/workspace/dossie_reexec/bravais/code/run_bravais.py`
- launch: `/workspace/dossie_reexec/bravais/code/launch.py`
- raw: `/workspace/dossie_reexec/bravais/raw/baseline.csv`, `field.json`, `field_series.csv`
- figure: `/workspace/dossie_reexec/bravais/figures/scores.png`
- result: `/workspace/dossie_reexec/bravais/result.json`

**Verdict: no crystal.** Field BCC=0.658 vs isotropic floor 0.665±0.114
(same 18-voxel shell). Resolved-shell floor for reading 0.22 vs 0.46:
SC 0.331±0.040, BCC 0.931±0.022.
