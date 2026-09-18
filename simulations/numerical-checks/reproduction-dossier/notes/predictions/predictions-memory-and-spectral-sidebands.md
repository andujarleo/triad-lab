# Predictions — P4 sidebands / memory vs HO spectrum (re-execution)

Date: 2026-08-21 15:42 -03 (America/Sao_Paulo)
Label: live test of the dossier hypothesis that memory restructures the HO
spectrum via parametric sidebands (TRIAD dossier §3.P4 / pending item 2).
These predictions are written BEFORE any integration of this run.
Do not treat them as forecasts of the dossier's exact floats.
Do not retune Λ, λ, ν, L, dt, or the IC to create sidebands. Keep failures.

## What is being tested

Dossier claim (not confirmed): Λ=−2 + mem(3,1) is NOT Λ_ef=+2.
Claimed extra lines at ~1.99 and 2.99.

Live hypothesis: ρ(t) beats at the system's transition frequencies;
fast memory ν=10 follows those beats → V_mem oscillates at the system's
own frequencies → parametric sidebands in the autocorrelation spectrum.

Previous re-exec of P4 Λ=−2+mem on L=20 leaked (leak=0.642). That
spectrum is INVALID. This run must use a larger box so leak_max < 1e-6.

## Shared equation and stepper (what we will integrate)

```
i ∂t Ψ = [ −∂xx/2 + V_ext + Λ|Ψ|² + V_mem ] Ψ
V_mem = Σ λj yj,   ∂t yj = νj(|Ψ|² − yj)
V_ext = ½ ω² x²,  ω = 1
```

α = Γ = f_FDT = 0. ħ = m = 1.

Strang: k-space half linear (kinetic)
→ real-space V = V_ext + Λρ + V_mem
→ Euler memory
→ k-space half linear.

Standalone runner, same algorithm as
`/workspace/dossie_reexec/QM1D/code/stepper1d.py`
SHA 5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076.
No triad-lang / TriadParams.

Grid: L=40 (L=60 if leak still ≥ 1e-6), N=1024, dt=0.01.
T=80 for extras; T=251 for linear / mem main spectrum if affordable
(bin 2π/T ≈ 0.025 at T=251, ≈ 0.0785 at T=80).

IC (preferred): Hermite 2-level (φ0+φ1)/√2 of the linear HO, built from
physicist's Hermite polynomials (numpy; scipy is not required).
Fallback only if Hermite construction fails: displaced Gaussian s=1, x0=0.8
(mostly n=0+n=1, not a huge n-stack).

c(t) = ∫ Ψ*(0) Ψ(t) dx, sampled every step.
FFT of c(t): look at NEGATIVE ω of numpy (E = −ω).
Report first 8 peaks above a stated noise floor (5% of max on the
negative-ω axis). Also FFT of ∫ρ² dx and of V_mem(x=0), to see whether
memory oscillates at the beat.

Four configs:
1. linear   Λ=0    lam=0
2. Λ=+2     lam=0
3. Λ=−2     lam=0
4. Λ=−2     lam=(3,1)  nu=(10, 0.5)

## Predicted patterns (written before any step)

### Linear Λ=0, no memory

A pure 2-level superposition of linear-HO eigenstates is an exact
solution of the linear Schrödinger equation. Therefore:

- FFT of c(t) shows ONLY the two energies E=0.5 and E=1.5
  (n+1/2 for n=0,1). No other lines above the 5% floor.
- No parametric sidebands. No lines near 2.0, 2.5, 3.0, or E_i ± 10.
- |c(t)| (and |c|²) beats at ω_beat = E1−E0 = 1. That beat may appear
  in FFT(|c|) or FFT(|c|²); it is not a third energy of Ψ.
- leak_max ≪ 1e-6 on L=40 (packet width ~1, well is x²/2).
- This is a Fourier / HO identity. Any extra line here is a stepper
  bug, window artefact, or IC impurity — not new physics.

If the Hermite IC is slightly impure (grid / normalisation), a weak
n=2 (E=2.5) may sit far below 5%. Report it; do not retune.

### Λ=+2, no memory

Repulsive cubic. Dossier: ladder shifts rigidly up (1.20, 2.20, 3.19, 4.19).
Previous leaked-free re-exec (displaced Gaussian x0=1.2, T=80, L=20):
strongest lines at 1.178 and 2.199.

Predicted pattern (not the exact floats):

- Levels shift UP relative to the linear ladder. Spacing stays ~1
  if the shift is approximately rigid.
- With a cleaner 2-level IC we expect fewer visible members than the
  dossier (which used a mixed packet). Two strong lines near ~1.2 and
  ~2.2 would match the dossier's rigid-shift pattern.
- Nonlinear mixing can feed a little n=2, so a third weaker line is
  allowed. That is not a sideband.
- No memory → V_mem ≡ 0. FFT of V_mem is empty.
- leak_max < 1e-6 (repulsive cubic spreads, but the HO well at |x|~20
  is V=200; L=40 should hold).

Missing 3.19 / 4.19 on a 2-level IC is not a failure of the shift claim.

### Λ=−2, no memory

Attractive cubic. Anharmonic. Dossier first lines: 0.52, 0.89, 1.52
(and 2.51). Previous re-exec (x0=1.2, T=80): 0.550, 0.864, 1.571, 1.885.

Predicted pattern:

- Not a rigid n+1/2 ladder. Spacing is compressed / irregular.
- First lines near the dossier cluster 0.52 / 0.89 / 1.52, within a
  bin or so. We will not predict the exact floats.
- A cleaner 2-level IC may show a subset (the overlap with the
  nonlinear eigenmodes of the cubic HO). Extra weak lines from
  anharmonic mixing are allowed; they are not "memory sidebands".
- leak_max < 1e-6 (attractive cubic is more confined than linear).

### Λ=−2 + mem(3,1), nu=(10, 0.5)  — TWO live outcomes, do not pick a winner

Λ_ef = Λ + Σλ = −2 + 4 = +2 is the static (y=ρ) reduction.
The dossier says this run is NOT that reduction, and claims extra
lines at ~1.99 and 2.99.

Previous re-exec on L=20: leak=0.642, peaks 0.47 / 0.71 / 1.02 / 2.04.
That spectrum is discarded. This run must confine (leak_max < 1e-6).
If L=40 still leaks, enlarge to L=60 and rerun this config only.
If even L=60 (or 80) leaks, the packet is not a confined HO state:
report leak, keep the failure, do not interpret the FFT as a ladder,
verdict INCONCLUSIVE.

Two competing live hypotheses (neither is chosen here):

**H_side (parametric sidebands):**
Extra lines appear that are absent in Λ=−2 no-mem, above the 5% floor,
near E_i ± ν_fast (ν_fast=10 → lines near E_i±10) and/or near 2.0 / 3.0
(the dossier's 1.99 / 2.99). Mechanism: ρ beats → fast y follows →
V_mem oscillates at the system's own frequencies → Floquet / parametric
mixing. FFT of ∫ρ² and/or V_mem(x=0) should then show a peak at the
beat (ω≈1 for a 2-level packet, or at the nonlinear transition
frequencies). The mem spectrum must NOT be the Λ=+2 ladder (1.20, 2.20, …).

**H_shift (no new peaks):**
Same lines as Λ=−2 no-mem, possibly shifted / broadened / reweighted.
No new peaks above the 5% floor. Memory is a delayed potential that
moves existing anharmonic levels; it does not generate parametric
sidebands. A slow-memory (ν=0.5) adiabatic shift is compatible with
this. FFT of V_mem may still show a beat — a beating potential is
necessary but not sufficient for sidebands in c(t).

A spectrum that matches Λ=+2 (rigid +0.7 ladder) would support the
static reduction Λ_ef=+2, which is a *third* outcome, not H_side and
not H_shift. Call that H_ef if it happens. The dossier claims it does
not. We do not predict it; we will report it if the peaks sit there.

We do not pick a winner. The integration decides.

## Memory diagnostic (all configs; empty when lam=0)

- ∫ ρ² dx  and  V_mem(x=0)  sampled every step.
- Linear / no-mem: V_mem ≡ 0; ∫ρ² may still beat at ω=1 for a 2-level
  packet (density breathing), which is ordinary HO interference, not
  a memory effect.
- Mem: if the fast channel tracks ρ, V_mem(x=0) should inherit that
  beat (ν=10 ≫ ω_beat=1). A peak at ω≈1 in FFT(V_mem) supports the
  *premise* of H_side (memory follows the beats). It does not by
  itself confirm sidebands in c(t).

## What would count as FAIL vs MATCH (after the run)

- Linear FAIL if peaks are not only ~0.5 and ~1.5 above 5% (or if
  leak ≥ 1e-6). Extra lines here invalidate the whole sideband reading.
- Λ=+2 FAIL vs the shift pattern if the visible strong lines do not
  move up from 0.5 / 1.5 (rigid-shift pattern broken). Missing high-n
  on a 2-level IC is not a fail.
- Λ=−2 FAIL vs the anharmonic pattern if it is a clean n+1/2 ladder
  or a clean +0.7-shifted ladder.
- Mem spectrum is INVALID if leak_max ≥ 1e-6. Do not score H_side /
  H_shift on an invalid spectrum.
- H_side MATCH if (leak ok) AND extra lines above 5% near 2.0 / 3.0
  or E_i ± 10 that are absent in Λ=−2 no-mem.
- H_shift MATCH if (leak ok) AND the mem lines are the Λ=−2 set
  (within a shift / a bin), with no new peak above 5%.
- INCONCLUSIVE if leak persists, if the floor / window makes the
  extra-line call ambiguous, or if the mem spectrum matches Λ=+2
  (H_ef) rather than either named hypothesis.
- Dossier floats 0.52 / 1.52 / 1.99 / 2.99 are comparison targets,
  not tuning targets.

## Integrity

- Predictions file written first. SHA of this file will be recorded
  before the runner starts.
- No retuning of λ, ν, Λ, dt to manufacture sidebands.
- Failures kept.
