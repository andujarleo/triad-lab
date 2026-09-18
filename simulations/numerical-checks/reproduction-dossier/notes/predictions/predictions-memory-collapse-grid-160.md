# Predictions — TRIAD A.3 anti-collapse at N=160 (written BEFORE any N=160 integration)

Status: PREDICTIONS ONLY. No N=160 Strang step has been taken. No 160³ field has been evolved.
No `/workspace/dossie_reexec/A3_N160/` directory exists yet. This file exists so the
N=160 verdict cannot be fit after the fact.

Re-execution label: second resolution check of the N=64 / N=128 A.3 re-executions
(`/workspace/dossie_reexec/A3/`, `/workspace/dossie_reexec/A3_N128/`). Spec default
is N=128; N=160 (dx=0.125) is a further refinement to test whether the N=128
H_plateau end-state and the unresolved no_mem blow-up continue in the same
direction. Not a change of Leonardo's "full triad" operational reading.
λ is **not** retuned. Stepper is **not** rewritten.

Date written: 2026-08-21 (America/Sao_Paulo, ~15:42 BRT / 18:42 UTC).
Box: Linux, system python3, NumPy 2.2.4, fp64.
Scheme: import the existing standalone stepper
`/workspace/dossie_reexec/A3/code/stepper.py`
SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`.
Not triad-lang.

## Why N=160

N=64 and N=128 re-execs already finished. Anchors (comparison only, not targets):

| N | run | peak_end | PR_end | peak_max (t) | t_collapse | 8× window |
|---|---|---|---|---|---|---|
| 64 | mem | 0.00343 | 2657 | 13.17 (0.1575) | 0.1425 | 0.1425–0.170 (1 pulse) |
| 64 | no_mem | 8.098 | 0.499 | 12.68 (0.1425) | 0.135 | stays peaked |
| 128 | mem | 0.002359 | 2444 | 62.48 (0.41) | 0.1275 | 0.1275–0.635 (6 pulses) |
| 128 | no_mem | 65.26 | 0.0616 | 84.58 (0.6325) | 0.115 | stays above 8× to T=6 |

N=128 supported H_plateau (end-state spread) and showed the no_mem blow-up is
genuine (peak rose 8.1 → 65). The early mem pulse train grew (1 pulse → 6;
13 → 62) and was scored not resolution-stable. N=160 asks whether those
directions continue: no_mem spike still climbs, mem end-state still plateau,
early train still taller / more pulses.

## Config (locked; same A.3 physics; only N changes)

hbar=1, m=1, Lambda=-10, alpha=0, Gamma=0, f_FDT=0, V_ext=0
nu=(10.0, 0.5), L=20, N=160, dx=20/160=0.125, dt=0.0025, T=6.0,
init_sigma=s=0.5, seed=42
IC: one 3D gaussian Ψ = exp(-r²/(2 s²)), then normalize ∫|Ψ|² dV = 1.
Two runs only (save wall time; skip Lambda_ef):
1. mem:    lam=(3.0, 1.0)
2. no_mem: lam=(0.0, 0.0)

Collapse diagnostic: t_collapse = first t where peak ≥ 8 * peak_ini (or inf if never).
Pulse = local maximum of peak(t) that is above 8 × peak_ini (or a contiguous
above-8× interval with its own local max). Print every 200 steps.
2400 steps × 2 FFT3d. 160³ complex128 ≈ 62.5 MB/field.
Expected wall ~25–40 min/run (~2× N=128 by (160/128)³).

## IC prediction

- peak_ini still ≈ 1.437 (same continuous IC). Analytic 1/(π s²)^{3/2} = 1.436696977.
  Origin is on the N=160 grid (even N, endpoint=False, x=-L/2 …). Expect peak_ini
  in [1.42, 1.45], closest to 1.436697 — at or nearer machine equality with
  analytic than N=64 (already 1.4366969769); N=128 already hit 1.4366969770.
- If peak_ini is not ~1.437, STOP. Do not integrate.
- norm = 1. PR_ini ~ O(1). R_rms_ini ≈ √(3/2)·s ≈ 0.612.

## 1. no_mem — still collapsed; peak_end and peak_max RISE again vs N=128

The focusing cubic blow-up is genuine, not a grid artifact of N=64 or N=128.

- Still collapsed: t_collapse finite and of the same early order (~0.11–0.14, certainly < 2).
- peak_end and peak_max **RISE again** vs N=128 (65.26 / 84.58). A finer grid
  (dx=0.125 vs 0.15625) resolves a sharper spike; the unresolved collapse
  can climb higher before dx limits it.
- PR_end stays < 1 and may drop vs 0.0616 if the spike is tighter in physical units.
- After the packet is ≲ dx=0.125, do **not** interpret the late field — only
  t_collapse and that it collapsed. peak_end / PR_end are then grid artifacts of
  an unresolved blow-up, but the *direction* (higher peak than N=128) is the tell
  that the blow-up is real.
- Expect it to stay above 8× through T=6 (not a reversible pulse).

FAIL of this prediction: no_mem does not collapse by T=6, or peak_end / peak_max
fall substantially below the N=128 values (which would suggest N=128 already
saturated the spike and "rise again" is wrong). A modest change is PARTIAL.

## 2. mem end-state — predict H_plateau still (H_ramp stays the rival)

N=128 already supported plateau: peak_end=2.359e-3, PR=2444, late field
delocalized after the 0.1275–0.635 train. Both hypotheses are still named so
analysis can kill one; the **prediction** is that plateau still holds at N=160.
Do not retune λ.

### (H_plateau) — PREDICTED: anti-collapse remains real at N=160

- peak_end stays O(10^{-3}) (same order as 0.002359 / 0.00343; not O(1) or larger).
- PR_end stays in the thousands (packet fills a large fraction of the L=20 box).
- peak_max of the early train may climb further (sharper pulses on a finer grid)
  but the *aftermath* still spreads: by T=6 the field is delocalized.
- t_collapse may still be finite (early train) but the late state is not a
  collapsed spike.

### (H_ramp) — rival, not predicted: late peak climbs toward collapse

- peak_end and/or the late (t ≳ 1) peak grow a lot vs N=128.
  "A lot" means: peak_end leaves the 10^{-3} decade (becomes O(10^{-1}) or O(1)+),
  and/or a late peak climbs toward no_mem-like values, and/or PR_end collapses
  out of the thousands toward O(1) or below, and/or the field stays above 8×
  through T=6 (no rebound).
- That would mean N=128's rebound was still under-resolved: the delayed
  repulsion arrived after a spike the N=128 grid could not fully develop.

N=128 supported plateau. **Predict H_plateau still.** analysis.md will say
which hypothesis actually lives. λ=(3,1) is not retuned either way.

## 3. early pulse train vs N=128 — taller / more pulses; first-crossing stable

Delay still needs a squeeze first: y lags ρ (ν_fast=10 ⇒ τ=0.1), so the early
mem trajectory should still track no_mem until t≈0.12. Therefore an early 8×
train **still happens**.

- First-crossing time stays early and roughly stable (~0.12–0.13; N=128 was
  0.1275, N=64 was 0.1425). Same order, maybe slightly sooner on the finer grid.
- Train is **taller** than N=128 (peak_max > 62.48) and/or has **more pulses**
  than N=128's 6 (local maxima above 8× in the early window). N=64 had 1 pulse;
  N=128 had 6. The trend is more resolved autofocus oscillations before y
  catches ρ.
- Train still **rebounds** (last 8× well before T=6; late state spread). Not
  H_ramp "grows and does not rebound".
- Train does **not** vanish.

FAIL of the "taller / more pulses" clause: peak_max falls below ~62 and pulse
count drops below 6 (N=128 overshot). FAIL of first-crossing stability: first
8× moves by ≳ 0.05 or never happens. PARTIAL: first-crossing stable but only
one of {taller, more pulses} holds, or height/count change is modest.

## What is locked / not predicted

- λ=(3,1) is not retuned regardless of which hypothesis wins.
- Lambda_ef is not re-run (N=64 already isolated delay vs Λ_ef).
- Exact N=64 / N=128 floats are comparison anchors, not targets.
- Unitary: Γ=0, no FDT. norm conserved to ~1e-10 on a non-collapsed run.
- Stepper SHA locked; runner is new but only changes N=160 and output paths.

## What analysis.md must score (MATCH / PARTIAL / FAIL)

1. no_mem sharper than N=128 (peak_end and peak_max rise; still collapsed)
2. mem H_plateau vs H_ramp at N=160 (end-state)
3. pulse train vs N=128 (taller? more pulses? first-crossing time stable?)
