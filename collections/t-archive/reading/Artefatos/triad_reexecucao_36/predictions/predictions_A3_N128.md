> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/predictions/predictions_A3_N128.md) · [Collection / Acervo](../../../../README.md)

# Predictions — TRIAD A.3 anti-collapse at N=128 (written BEFORE any N=128 integration)

Status: PREDICTIONS ONLY. No N=128 Strang step has been taken. No 128³ field has been evolved.
This file exists so the N=128 verdict cannot be fit after the fact.

Re-execution label: resolution check of the N=64 A.3 re-execution
(`/workspace/dossie_reexec/A3/`). Spec default is N=128; N=64 was the only failed
criterion of the dossier A.3 protocol. Not a change of Leonardo's "full triad"
operational reading. λ is **not** retuned. Stepper is **not** rewritten.

Date written: 2026-08-21 (America/Sao_Paulo, ~15:04 BRT / 18:04 UTC).
Box: Linux, system python3, NumPy 2.2.4, fp64.
Scheme: import the existing standalone stepper
`/workspace/dossie_reexec/A3/code/stepper.py`
SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`.
Not triad-lang.

## Why N=128

N=64 re-exec already finished. End-state anti-collapse held (mem peak_end=0.00343,
PR_end=2657; no_mem peak_end=8.098, PR_end=0.499, t_collapse=0.135). But mem
crossed 8× peak_ini at t=0.1425, peaked at 13.17 at t=0.1575, then spread. That
early pulse may be under-resolved (dx=0.3125). Spec default is N=128 (dx=0.15625).
This run is the only remaining failed criterion.

N=64 numbers above are comparison anchors, **not** copied as targets.

## Config (locked; same A.3 physics; only N changes)

hbar=1, m=1, Lambda=-10, alpha=0, Gamma=0, f_FDT=0, V_ext=0
nu=(10.0, 0.5), L=20, N=128, dx=20/128=0.15625, dt=0.0025, T=6.0,
init_sigma=s=0.5, seed=42
IC: one 3D gaussian Ψ = exp(-r²/(2 s²)), then normalize ∫|Ψ|² dV = 1.
Two runs only (save wall time; skip Lambda_ef):
1. mem:    lam=(3.0, 1.0)
2. no_mem: lam=(0.0, 0.0)

Collapse diagnostic: t_collapse = first t where peak ≥ 8 * peak_ini (or inf if never).
Print every 200 steps. 2400 steps × 2 FFT3d. 128³ complex128 ≈ 32 MB/field.

## IC prediction

- peak_ini still ≈ 1.437 (same continuous IC). Analytic 1/(π s²)^{3/2} = 1.436696977.
  Origin is on the N=128 grid (even N, endpoint=False, x=-L/2 …). Expect peak_ini
  in [1.42, 1.45], closest to 1.436697 — possibly even closer to analytic than N=64
  (already 1.4366969769).
- If peak_ini is not ~1.437, STOP. Do not integrate.
- norm = 1. PR_ini ~ O(1). R_rms_ini ≈ √(3/2)·s ≈ 0.612.

## no_mem — single prediction

Still collapses. The focusing cubic blow-up is genuine, not a grid artifact of N=64.

- t_collapse finite and of the same early order as N=64 (~0.13–0.14, certainly < 2).
- peak_end should **RISE** vs N=64 (8.098). A finer grid resolves a sharper spike;
  the unresolved collapse can climb higher before dx limits it.
- PR_end stays < 1 (volume PR of a near-grid-point spike). May drop vs 0.499 if
  the spike is tighter in physical units.
- After the packet is ≲ dx=0.15625, do **not** interpret the late field — only
  t_collapse and that it collapsed. peak_end / PR_end are then grid artifacts of
  an unresolved blow-up, but the *direction* (higher peak than N=64) is the tell
  that the blow-up is real.

FAIL of this prediction: no_mem does not collapse by T=6, or peak_end falls
substantially below the N=64 value (which would suggest N=64 was already the
saturated grid-limited spike and "rise" is wrong). A modest change is PARTIAL.

## mem — two live hypotheses (do not pick a winner)

N=64 mem ended spread (peak_end=3.43e-3, PR=2657) after a brief 8× pulse
(peak_max=13.17 at t=0.1575, crossed 8× at t=0.1425 for Δt≈0.028). That end-state
could be real anti-collapse, or delayed / under-resolved collapse that a finer
grid will let run away. Both stay open until the N=128 numbers exist.

### (H_plateau) — anti-collapse is real

- peak_end stays O(10^{-3}) (same order as 0.00343; not O(1) or larger).
- PR_end stays in the thousands (packet fills a large fraction of the L=20 box).
- peak_max may shift (sharper early pulse on a finer grid) but the *aftermath*
  still spreads: by T=6 the field is delocalized.
- t_collapse may still be finite (see early-pulse note) but the late state is
  not a collapsed spike.

### (H_ramp) — N=64 was delayed collapse / under-resolved

- peak_end and/or peak_max grow a lot vs N=64.
  "A lot" means: peak_end leaves the 10^{-3} decade (becomes O(10^{-1}) or O(1)+),
  and/or peak_max climbs well above 13 (say ≳ 2×), and/or PR_end collapses out of
  the thousands toward O(1) or below.
- The N=64 spread would then be a resolution artifact: the delayed repulsion
  arrived after a spike that the coarse grid could not fully develop, so it
  looked like a reversible pulse.

Do **not** pick a winner in this file. analysis.md will say which hypothesis lives.

## Early 8× pulse (resolution-stability, third criterion)

Delay needs a squeeze first: y lags ρ (ν_fast=10 ⇒ τ=0.1), so the early mem
trajectory should still track no_mem until t≈0.14. Therefore the early 8× pulse
in mem **may still happen** at N=128.

- If it happens with similar t_collapse (~0.14) and similar Δt above 8× (~0.03),
  the pulse is resolution-stable (a real delay-then-rebound, not a grid glitch).
- If the pulse vanishes (never reaches 8×), N=64 overshot.
- If the pulse grows and does **not** rebound (stays above 8×, peak_end large),
  that is H_ramp: the pulse was the start of a real collapse that N=64 truncated.

## What is locked / not predicted

- λ=(3,1) is not retuned regardless of which hypothesis wins.
- Lambda_ef is not re-run (N=64 already isolated delay vs Λ_ef).
- Exact N=64 floats are comparison anchors, not targets.
- Unitary: Γ=0, no FDT. norm conserved to ~1e-10 on a non-collapsed run.

## What analysis.md must score (MATCH / PARTIAL / FAIL)

1. no_mem blow-up grows or stays collapsed
2. mem end-state still spread (H_plateau) vs ramps toward collapse (H_ramp)
3. whether the early 8× pulse is resolution-stable
