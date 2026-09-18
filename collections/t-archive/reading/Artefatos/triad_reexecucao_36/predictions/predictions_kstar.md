> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/predictions/predictions_kstar.md) · [Collection / Acervo](../../../../README.md)

# Predictions — R5 k*L ≈ 16.3: invariant vs mobile vs grid (written BEFORE any time integration)

Status: PREDICTIONS ONLY. No Strang step has been taken for this k* sweep.
Three live hypotheses. This file does NOT pick a winner.
Do not calibrate Λ, λ, ν, L, N, dt, s, or the IC toward 16.3. Keep failures.

Date written: 2026-08-21 17:32 -03 (America/Sao_Paulo).
Box: Linux, /usr/bin/python3 + NumPy 2.2.4 fp64 for integration; plots via /workspace/.venv.
Scheme: standalone 3D Strang from /workspace/dossie_reexec/A3/code/stepper.py
SHA256 7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713.
Spectral k* as in /workspace/run_R5_A2.py (radial shell power of Ψ̂, exclude |k|≤2π/L).
Not triad-lang / TriadParams.

Re-execution label: live test of dossier pending item 4 / spec §10.4 / A.2
“k*L≈16.3 across calibrations”. Independent of Q01 (hot FDT, Nyquist-locked).

## What is being tested

k* := peak of radial shell-averaged power P(|k|) for |k| > 2π/L (DC / box mode excluded).
k*L := k* × L.
C := crystallinity = power(|k|>2π/L) / total power. k_cut = 2π/L.

Dossier / spec quotes k*L ≈ 16.3 as if it were a structural number of the R5 family.
This sweep asks whether that number is

- a **structural invariant** of the physics family (H_invar),
- a **movable selection** that just happened to sit near 16.3 in one calibration (H_mobile),
- or a **grid / bin lock** (Nyquist, or 2π n / L with n set by N, or the first allowed shell) (H_grid).

Q01 is a different regime (hot FDT) and found k* at Nyquist. That is NOT this test.
R5 here is structure-forming, unitary / cool: Γ=0, α=0, f_FDT=0.

## Config (fixed; will not be retuned)

hbar=1, m=1, α=0, Γ=0, f_FDT=0, V_ext=0
lam=(1.125, 0.375)   # 0.75/0.25 × Σλ=1.5
ν=(10, 0.5)
s=0.5, seed=42, dt=0.0025
N=64 (not spec 128), T=8 (not spec 15; structure should appear before 15 if it exists)
IC: Ψ = exp(−r²/(2s²)), normalize ∫|Ψ|² dV = 1, then rescale to target norm.
Baseline: L=20, Λ=−8, norm=1, N=64.

Sweep, one change at a time (baseline overlaps → 8 unique runs):

A. L ∈ {15, 20, 25} at N=64, Λ=−8, norm=1   (dx changes)
B. Λ ∈ {−6, −8, −10} at L=20, N=64, norm=1
C. norm ∈ {0.5, 1.0, 2.0} at L=20, Λ=−8, N=64
D. GRID: L=20, Λ=−8, norm=1, N ∈ {48, 64}

Observable per run: late-window (last 20% of [0,T]) **median** of k*, k*L, C, peak, PR.
Also record the shell index i* and the analytic grid numbers below. Do not aim at 16.3.

## Grid numbers (identities; not predictions of the physics)

dk = 2π/L. Shell centers in the R5-A2 binning: k_i = (i + 1/2) dk, so
k_i L = 2π (i + 1/2).

| lock | formula | N=64 | N=48 | L-dependence at fixed N |
|---|---|---|---|---|
| Nyquist k=π/dx | k*L = π N | 201.06 | 150.80 | **constant** (tracks N only) |
| first allowed shell i=1 | k*L = 3π ≈ 9.425 | 9.425 | 9.425 | constant (independent of L and N) |
| shell i=2 | k*L = 5π ≈ 15.708 | 15.708 | 15.708 | constant |
| shell i=3 | k*L = 7π ≈ 21.991 | 21.991 | 21.991 | constant |
| dossier quote | 16.3 | 16.3 | 16.3 | claimed constant |

16.3 is **far from Nyquist** if they measured the same k* (201 vs 16.3).
16.3 is **close to shell i=2** (15.708). Difference 0.6 is one-half of a 2π-wide bin
if someone used a slightly different center (integer n, interpolation, or k of the
max voxel rather than the shell center). That proximity is a live H_grid threat
and is **not** evidence for H_invar until Λ and norm are moved.

At fixed L, dk does not depend on N. So a low-n bin lock and a physical k*L
are **degenerate on the N-sweep** unless k* sits at Nyquist (which tracks N).
The N-sweep is the Nyquist test. The Λ- and norm-sweeps break the degeneracy
between “physical 16.3” and “always the same low-n shell”.

## IC predictions (must hold before integration; if not, STOP that run)

For norm=1: peak_ini ≈ 1.437 = 1/(π s²)^{3/2}, s=0.5.
Grid (N=64, L=20, dx=0.3125): expect peak_ini ∈ [1.42, 1.45].
norm_ini = 1 by construction; after rescale, norm_ini = target.
PR_ini = O(1); R_rms_ini ≈ √(3/2)·s ≈ 0.612 (norm-independent for a Gaussian).
For norm ≠ 1: peak_ini ≈ 1.437 × norm (ρ scales with the rescale).
If peak_ini is not in that window on a norm=1 run, STOP and fix the IC. Do not integrate.

## Three live hypotheses (do not pick a winner)

### H_invar — k*L is a structural invariant of the R5 family

Claim: late median k*L stays near 16.3 when L, Λ, and initial norm change,
at this physics family (same λ, ν, s, unitary). k* itself then scales as 1/L.

What would confirm:
- A, B, C late medians all in a band around 16.3 (say 14–19, not a single bin
  identity and not tracking L or |Λ| or norm).
- D: N=48 and N=64 give the same k*L (not πN). That already kills Nyquist.
- C (crystallinity) is not the IC value: a finite-k peak actually exists
  (P(|k|) is not monotonically falling from DC).
- i* is allowed to move with L (k* ∝ 1/L) so that the product is stable.

What would kill:
- k*L tracks L (physical k* fixed → product ∝ L) — that is H_mobile, not invariant.
- k*L tracks |Λ| or norm (tighter focus, larger k*) — H_mobile.
- k*L = πN on D, or k*L exactly 2π(i+1/2) for the same i on every knob — H_grid.
- No structure by T=8 (C stuck at IC, spectrum monotonically falling) — then
  16.3 was never realized here; do not call that H_invar.

### H_mobile — k*L is a selection, not a constant

Claim: the radial peak is a real (or quasi-real) scale set by the instantaneous
balance of focusing, kinetic energy, and delayed memory. Changing the knobs
moves that scale. 16.3 is one point on a curve, not a constant of the family.

Expected directions if the scale is physical and resolved:
- **L** at fixed N: if the structure does not care about the box (local healing /
  soliton width), k* is independent of L and **k*L ∝ L**. If the structure
  fills the box, k*L can look flat — then B and C must still move it.
- **Λ**: more focusing (|Λ| larger) → tighter real-space support → larger k*
  → larger k*L, at fixed L.
- **norm**: ρ → ν ρ raises the cubic |Λ|ρ and the memory source. norm=2 should
  sit at higher k* than norm=0.5 if a focused object forms.
- **N** at fixed L: a physical k* does **not** track N. D stays put (≠ πN).

What would confirm: late k*L moves by more than one shell (Δ(k*L) ≳ 2π) on
at least one of A/B/C, and D is not Nyquist.
What would kill: all four knobs give the same k*L to within a bin, with a
genuine finite-k peak — that is H_invar or a low-n H_grid, not mobile.

### H_grid — k* is a bin locked to the mesh

Claim: k* is not a physical scale. It sits on a mesh identity.

Two concrete locks, both live:

1. **Nyquist.** k* = π/dx = π N/L. Then k*L = πN.
   - A (fixed N): k*L ≈ 201 for all three L.
   - D: N=48 → 150.8, N=64 → 201.1.
   - B, C: still 201 if the lock is the grid, independent of physics.
   User already noted 16.3 ≪ 201. If this lock appears, the measured k* is
   **not** the dossier’s k*, or this unitary R5 is in a different (UV) regime
   than the quoted calibration. Report it. Do not retune.

2. **Low-n / first-allowed shell.** A smooth blob (spread packet, no crystal)
   has P(|k|) decreasing in k. After dropping DC, argmax is the first bin
   with k > 2π/L. In the R5-A2 centering that is i=1, k*L = 3π ≈ 9.425,
   **independent of L, Λ, norm, and N**. A slightly different center, or a
   peak that sits on i=2, gives 15.708 — numerically next to 16.3.
   - D does **not** move (dk = 2π/L is N-independent at fixed L).
   - A does **not** move.
   - B, C do **not** move if the spectrum stays monotonic.
   - Diagnostic: C stays near the IC value; i* is the same integer on every run;
     the shell profile is falling, not peaked.

What would confirm: k*L equals πN (Nyquist) or equals 2π(i+1/2) for one
fixed i across the knobs that should have moved a physical scale (B and C).
What would kill: k*L moves with Λ or norm by more than one bin, or k*L tracks
L while i* changes so as to hold a physical k* (not a bin identity).

## Structure-or-not (gate, not a fourth hypothesis)

T=8 is shorter than spec T=15. Prediction: if a finite-k structure exists in
this family it should already be visible in the late window (C risen vs IC,
P(|k|) peaked at k*>2π/L, peak/PR not a pure spread-to-the-box). If it is
not, say so and do **not** treat a first-bin k*L as “the R5 invariant”.
Do not extend T to chase 16.3.

A.3 re-exec (Λ=−10, λ=(3,1), same stepper, N=64) spread without collapse.
This R5 point is weaker memory (Σλ=1.5 vs 4) and slightly weaker focusing
(|Λ|=8 vs 10). Possible late states, all live:
- spread blob → H_grid first-bin is the default measurement;
- arrested compact object / modulation → a real k* (then H_invar vs H_mobile);
- collapse toward the grid → UV / Nyquist (H_grid), ignore post-collapse structure.

Unitary: norm conserved to ~1e-10 on non-collapsed runs.

## Scoring rules (written before the runs)

Score on late-window **medians**, not on a single final snapshot.
Do not average the three hypotheses. Verdict is one of:
H_invar / H_mobile / H_grid / MIXED.

- **H_invar** if A,B,C stay near 16.3 (not a mesh identity), D ≠ πN, and
  a finite-k peak exists (C up, spectrum not monotonic).
- **H_mobile** if A or B or C moves k*L by ≳ one shell and D is not Nyquist.
- **H_grid** if k*L = πN (and D tracks N) **or** k*L = 2π(i+1/2) for a
  fixed i on B and C (physics knobs that must move a physical scale).
- **MIXED** if L looks invariant while Λ/norm move, or N tracks πN while
  B/C move, or no structure forms so 16.3 is simply not realized.

Proximity of 16.3 to 5π≈15.708 is **not** scored as H_invar by itself.

## What is NOT predicted

The dossier float 16.3 is not a target. No run will be retuned so that
k*L lands on 16.3. Exact late peak/PR/C are not predicted as numbers.

## Label

Every number produced after this file is a RE-EXECUTION of the R5 k* protocol
on this Linux box. It is not a revision of the operational “full triad” reading.
