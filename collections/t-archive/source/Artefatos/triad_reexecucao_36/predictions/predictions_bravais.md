# Predictions — Bravais lattice detector calibration (dossier pending item 5)

Status: PREDICTIONS ONLY. Written BEFORE any detector implementation, any
baseline draw, and any R5 unitary time step. No |Ψ̂|² has been scored.
No window has been (or will be) tuned to separate field from noise.

Date written: 2026-08-21 17:32 -03 (America/Sao_Paulo).
Box: Linux, /usr/bin/python3 + /workspace/.venv for plots, NumPy fp64.
Label: live test of dossier leftover “calibrar com rede aleatória de mesma
densidade de nós (score do ruído como baseline) antes de interpretar
0.22 vs 0.46.” Re-execution of spec §8.4. Not a change of Leonardo's
full-triad operational reading. Not a claim that R5 N48 was BCC.

Dossier numbers this file is *not* targeting: BCC=0.462544, HCP=0.393127,
FCC=0.298510, SC=0.238946 (R5 N48, another detector, another N, another
run). Bounce PLANAR_cross=0.221126 is a third detector. Do not unify.

## Frozen detector (will not be retuned)

On the dominant shell of |Ψ̂|², voxels with ||k| − k*| < 0.5 dk, dk = 2π/L.
k* = argmax of radial power P(|k|) for |k| > dk (DC excluded).

Alignment rule (ONE definition, frozen):

    cos θ = max_{â in family} (k̂ · â)
    voxel counts if 1 − cos θ < 0.15   i.e.  cos θ > 0.85
               iff  θ < arccos(1 − 0.15) ≈ 31.79°

Both ± of each axis are listed, so max-dot equals |k̂ · â_axis|.
Score = (shell power in aligned voxels) / (total shell power).
Best family = argmax score. Window 0.15 is locked. Do not retune it.

Families, box-aligned, no rotation search:

- SC:  6 dirs  ±x, ±y, ±z
- BCC: 12 dirs (1,1,0)/√2 and all sign/axis perms
- FCC: 8 dirs  (1,1,1)/√3 and all sign perms
- HCP: 6 in-plane (xy, every 60°) + 2 axial ±z

A family with more directions covers more of the sphere. That is a
geometric bias of the detector, not evidence of that lattice.

## Why a random shell has a NONZERO score (the noise floor)

Directions always catch some power. Continuum solid-angle estimate,
ignoring cone overlap:

    one cap: Ω = 2π (1 − 0.85) = 0.3 π
    n_dirs caps / 4π  = n_dirs × 0.15 / 2

    SC  (6)  → ~0.45   (cones 90° apart; no overlap)
    FCC (8)  → ~0.60   (angle arccos(1/3)≈70.5°; barely no overlap)
    BCC (12) → ~0.90 before overlap; 60° neighbors + 31.8° half-angle
               overlap heavily, so true continuum BCC floor is lower
               than 0.90 but still ≳ SC
    HCP (8)  → order of FCC; axial pair coincides with SC ±z

Discrete thin-shell sampling (N=64, ~O(10²) voxels if k*L~16, fewer
if k*L is a low bin) will move these numbers, and families will come
out the same *order* (tenths), not the same *value*. THAT scatter —
mean ± std over isotropic / Poisson draws — is the noise floor.

Predictions for baselines (32 seeds, same N=64, L=20 as the field):

1. Isotropic complex-gaussian field: SC / BCC / FCC / HCP scores all
   in the same order of magnitude (roughly 0.15–0.60). BCC and FCC
   likely sit above SC because they have more cones. Std is not tiny:
   a thin shell is a small-N sample of the sphere.
2. Shell-randomized |Ψ̂|² (permute voxels on the field's own k* shell):
   scores collapse to the same floor as (1) at that k*. Any excess
   the live field had over the floor is destroyed by the scramble.
   This is the cleanest “same spectrum, no angles” control.
3. Poisson points, M ≈ n_local_max(ρ) or (k*L/2π)³ unit spikes:
   speckle, not a lattice. Family scores again at the floor, maybe
   with fatter tails (small-M shot noise). Same node density as the
   field does *not* produce a Bravais score by itself.

Do not interpret a raw 0.22 or a raw 0.46. Compare to this floor.

## What would count as a real lattice (excess)

A true lattice must beat the *same-family* isotropic mean + 2σ by a
clear margin. The prediction of “clear” is about ×2 above the floor
mean, or at least mean+2σ with the other families not all high too.

- If a run scores 0.22 and random mean is 0.20 (σ~0.03), 0.22 is
  nothing. Verdict: AT floor.
- If a run scores 0.46 and random mean is 0.20 (σ~0.05), 0.46 is a
  real excess (×2.3, well above mean+2σ). Verdict: ABOVE floor.
- If a run scores 0.46 and random mean is 0.40 (σ~0.05), 0.46 is
  not an excess. Verdict: AT floor.
- If all four families rise together, that is extra shell power
  near the coordinate axes / diagonals (anisotropy of the box or
  of the IC), not a Bravais choice.

## Field prediction — one R5 unitary, N=64

Config (locked; will not be retuned):

    N=64, L=20, Λ=−8, lam=(1.125, 0.375), ν=(10, 0.5),
    Γ=0, α=0, T=8, s=0.5, seed=42, dt=0.0025
    IC: one 3D gaussian, ∫|Ψ|² dV = 1
    Stepper: /workspace/dossie_reexec/A3/code/stepper.py (no triad-lang)

This is *not* the R5 N48 dossier run (that was N=48, T=15, and a
different crystallinity / k* estimator). It is the cheapest unitary
R5-like field on which to hang the detector.

May or may not crystallize. Honest branches:

- Memory is weaker than A.3-mem (Σλ=1.5 vs 4) and |Λ| is 8.
  A.3-mem (Λ=−10, λ=(3,1)) spread after a brief 8× pulse.
  A.3 Lambda_ef (Λ=−6, no mem) collapsed and stayed peaked.
  This run sits between those: delay is present but weaker.
  Possible late states: (i) spread, PR thousands, no lattice;
  (ii) unresolved collapse, PR ≲ 1, no lattice; (iii) a resolved
  periodic texture with a real k* shell.
- If it does *not* form a lattice, the field best-score sits at
  the noise floor (within mean+2σ of isotropic / Poisson). That
  is a valid result. Report it. Do not retune Λ, λ, T, N, or the
  window to force a crystal.
- If it *does* form a lattice, the best family beats its own
  floor by ≳×2 and the shell-randomized control falls back to
  the floor. Then, and only then, name the family.
- k*L of a true MI lattice is predicted near the dossier attractor
  ~16 (order-of-magnitude, not the float 16.3). A k* stuck in the
  first radial bin (k*L = 2π or 3π) is “no shell”, not a lattice.
- n_local_max(ρ) of a crystal should be order (k*L/2π)³ (~10–30
  if k*L~16). A handful of maxima, or O(N³) pixel noise, is not
  a Bravais network.
- t of max crystallinity may be t=0 if C(t) is the spec §8.3
  high-k fraction (a narrow gaussian is already broadband). The
  useful clock is concentration of non-DC power onto one shell,
  C_★(t). Report both; use C_★ for “t of max crystallinity” if
  C(t) is uninformative. If even C_★ never rises, there is no
  crystal and late-time scores are the ones that matter.

## What is NOT predicted

- Which family wins on this N=64 run.
- The dossier floats 0.22 vs 0.46. Those are the numbers this
  calibration exists to stop people from reading.
- That R5 “is BCC”. The N48 BCC=0.46 is exactly the kind of raw
  score that might be a floor (SC continuum floor is already ~0.45).

## Fail conditions (vs this file, not vs dossier floats)

- Implementing the detector then changing the window so the field
  separates from random. Window stays 0.15.
- Reporting 0.22 or 0.46 as a lattice without the 32-seed floor.
- Waiting on an empty /workspace/dossie_reexec/kstar/ instead of
  running this field.
- Importing a phantom observables.py.

## Protocol lock (what will be run after this file exists)

1. detector.py in numpy, definition above.
2. Baselines a, b, c at the field's N, L, k*. (a) and (c) × 32 seeds.
   Report mean±std per family.
3. One R5 unitary field. Detector at t=T and at t of max C_★.
   Dump n_local_max(ρ).
4. Compare field best-score to random mean+2σ.
   Verdict: ABOVE floor / AT floor / no crystal.

Every number after this file is a calibration, not a crystal claim.
