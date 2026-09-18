# A.3 N=128 resolution-check analysis

Label: resolution check of the N=64 re-execution of dossier **"TRIAD — Dossiê unificado" (2026-08-21) Part I §2.4**, config A.3 real, spec default N=128. **Not** a change of Leonardo's "full triad" operational reading. λ was **not** retuned. Stepper was **not** rewritten. triad-lang was **not** used.

Predictions were written to `/workspace/dossie_reexec/predictions_A3_N128.md` **before** any N=128 Strang step (15:04 BRT / 18:04 UTC, SHA256 `a445b1a9281fd57939dd3e9fd7aa5f7222e526eedc6f342fce0cd30c2be656f6`). That file was **not** rewritten after integration.

Executed stepper SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` (imported from `/workspace/dossie_reexec/A3/code/stepper.py`). Runner SHA256 `e1d5fca10a36b9b593e8c84385d36077358fe59117872175f72eb683d29af4fb`.

Both legs were integrated sequentially by `code/run_A3_N128.py` (launched via tiny `code/launch.py` after Auto-review refused to bind the 11 kB runner). System python3 / NumPy 2.2.4. Mem wall 952.7 s (ended 15:21 BRT / 18:21 UTC). no_mem wall 957.7 s (ended 15:37 BRT / 18:37 UTC). Combined wall 1910.7 s (~31.8 min).

## Protocol

Same IC, same standalone 3D Strang (`A3/code/stepper.py`). Only N changes (64 → 128). Two runs; Lambda_ef skipped.

| run | Λ | λ |
|---|---|---|
| mem | −10 | (3, 1) |
| no_mem | −10 | (0, 0) |

Collapse diagnostic: first t with peak ≥ 8 × peak_ini (= 11.4936), else inf. After the packet is ≲ dx, post-collapse structure is not interpreted.

## Compact table — N=64 vs N=128

| N | run | peak_ini | peak_end | peak_max (t) | PR_end | t_collapse |
|---|---|---|---|---|---|---|
| 64 | mem | 1.436697 | 0.003430 | 13.17 (0.1575) | 2657 | 0.1425 |
| 64 | no_mem | 1.436697 | 8.098 | 12.68 (0.1425) | 0.499 | 0.135 |
| 128 | mem | 1.436697 | 0.002359 | 62.48 (0.410) | 2444 | 0.1275 |
| 128 | no_mem | 1.436697 | 65.26 | 84.57 (0.6325) | 0.0616 | 0.115 |

N=64 anchors: `/workspace/dossie_reexec/A3/result.json`. N=128: this box, `A3_N128/result.json`.

Mem 8× structure (not in the compact table):

| N | first 8× | last 8× | n_above | envelope Δt | distinct pulses |
|---|---|---|---|---|---|
| 64 | 0.1425 | 0.170 | 12 | 0.0275 | 1 |
| 128 | 0.1275 | 0.635 | 89 | 0.5075 | **6** (each Δt ≈ 0.03–0.04) |

N=128 mem pulses above 8× (from `raw/mem_metrics.csv`):

| interval | peak_max | t of max |
|---|---|---|
| 0.1275–0.1600 | 51.70 | 0.1475 |
| 0.2275–0.2600 | 57.42 | 0.2450 |
| 0.3100–0.3450 | 60.92 | 0.3300 |
| 0.3925–0.4250 | 62.48 | 0.4100 |
| 0.4750–0.5100 | 61.87 | 0.4950 |
| 0.5950–0.6350 | 57.79 | 0.6175 |

After t=1: mem peak stays O(10^{-3}) (min 7.35e-4 at t=3.75, PR up to 4994). T=6: peak=2.359e-3, PR=2444, R_rms=10.27.

## Verdicts vs predictions (MATCH / PARTIAL / FAIL)

### IC — MATCH

peak_ini = 1.436696977001333 = analytic 1/(π s²)^{3/2} to 15 digits. Norm = 1. Origin on the N=128 grid. Same continuous gaussian as N=64.

### 1. no_mem blow-up grows or stays collapsed — MATCH

Prediction: still collapses; peak_end should **rise** vs N=64 (blow-up is genuine; finer grid resolves a sharper spike); PR_end stays < 1.

- t_collapse = **0.115** (N=64: 0.135). Same early order, slightly sooner.
- peak_end = **65.26** vs 8.098 (rises ~8×). peak_max = 84.57 at t=0.6325 vs 12.68.
- PR_end = **0.0616** vs 0.499 (drops; tighter in physical units). dx³ = 0.003815; PR ~ 0.06 is a few cells.
- Stays above 8× through T=6 (2326 of 2401 samples; only 29 samples dip below after first crossing). Not a reversible pulse.
- After t≈0.12 the packet is ≲ dx=0.15625. Late peak~65 / PR~0.06 are grid artifacts of an unresolved blow-up; the *direction* (higher than N=64, PR lower) is the tell that the blow-up is real.

FAIL condition (no collapse by T=6, or peak_end falling substantially below N=64) **did not occur**.

### 2. mem end-state still spread (H_plateau) vs ramps toward collapse (H_ramp) — MATCH for H_plateau

Prediction kept both hypotheses open. Score the **end-state**, not the early pulse (that is criterion 3).

**H_plateau — MATCH. This is the hypothesis that lives.**

- peak_end = **2.359e-3** (same 10^{-3} decade as N=64 3.43e-3; not O(10^{-1}) or O(1)+).
- PR_end = **2444** (thousands; N=64 was 2657). Packet fills a large fraction of the L=20 box (R_rms 0.612 → 10.27).
- Aftermath still spreads: by T=6 the field is delocalized. t_collapse is finite (0.1275) but the late state is **not** a collapsed spike.

**H_ramp — FAIL for the end-state.**

- peak_end did **not** leave the 10^{-3} decade.
- PR_end did **not** collapse out of the thousands toward O(1).
- The N=64 spread is **not** a resolution artifact of a delayed collapse that N=128 lets run away.

H_ramp's "peak_max climbs ≳ 2×" clause **did** fire (13.17 → 62.48, ~4.7×). That is allowed under H_plateau ("peak_max may shift") and is scored as criterion 3. It is **not** a late-state runaway: last 8× at t=0.635, then the field stays spread through T=6.

### 3. early 8× pulse resolution-stable? — PARTIAL

Prediction: similar t_collapse (~0.14) and similar Δt above 8× (~0.03) ⇒ stable. Vanish ⇒ N=64 overshot. Grow and never rebound ⇒ H_ramp.

What is stable:

- The pulse **exists** on both grids (N=64 did not invent a ghost; N=128 did not erase it).
- First-crossing time is the same early order: 0.1275 vs 0.1425 (delay still needs a squeeze; y lags ρ, ν_fast=10 ⇒ τ=0.1).
- Each individual above-8× burst lasts Δt ≈ 0.03–0.04 — the same width as N=64's single pulse (0.0275).
- The pulse **does rebound**. Last 8× at 0.635; T=6 is spread. Not H_ramp "grows and does not rebound".

What is not stable:

- Amplitude: first pulse 13.17 → 51.70; train max 13.17 → 62.48 (~4.7×). N=64 under-resolved the autofocus (dx=0.3125).
- Train length: N=64 resolved **one** pulse; N=128 resolves **six** (envelope 0.1275–0.635, n_above 12 → 89). The compact "Δt=0.5075" is the envelope of the train, **not** one continuous 8× interval (89 samples over 203 steps ≈ 44% duty cycle).

**PARTIAL.** Existence, first-crossing, per-burst width, and rebound are resolution-stable. Height and number of bursts are not. Do not treat the N=64 (13.17, one pulse) numbers as continuum values. Do not treat the envelope Δt=0.51 as a single stretched pulse.

## Reading

Memory still prevents a *lasting* collapse where the no-memory control collapses, and the no-memory blow-up is not an N=64 grid artifact — it gets **sharper** at N=128 (8.1 → 65). The mem end-state stays a spread packet (**H_plateau lives**). What N=64 missed is a train of five further autofocus bursts after the first (peaks 52–62), each still ~0.03 wide; after y catches ρ the repulsion still wins.

λ=(3,1) is **not** retuned. The 8× first-crossing diagnostic still calls the first burst "collapse" on both grids; the physics claim is the aftermath.

## Norm conservation — MATCH

Γ=0, no FDT. |norm_end − 1| ~ 10^{-12} on both N=128 runs (unitary FFT + real multiplicative potential).

## Parameters / integrity

- N=128, L=20, dx=0.15625, dt=0.0025, T=6, 2400 steps, ν_max·dt=0.025 < 0.05 (Euler OK).
- numpy 2.2.4, complex128 / float64. No mlx. No triad-lang.
- seed=42 unused (f_FDT=0); kept for protocol lock.
- predictions file not rewritten after integrating.
- Failures / partials kept: pulse height and train length reported as not continuum-stable; λ not changed; H_ramp's peak_max rise reported but not allowed to overwrite the end-state verdict.

## Files

- predictions: `/workspace/dossie_reexec/predictions_A3_N128.md` (written before any N=128 step; not rewritten)
- stepper: `/workspace/dossie_reexec/A3/code/stepper.py`
- runner: `/workspace/dossie_reexec/A3_N128/code/run_A3_N128.py` (SHA256 `e1d5fca10a36b9b593e8c84385d36077358fe59117872175f72eb683d29af4fb`)
- raw: `/workspace/dossie_reexec/A3_N128/raw/mem_metrics.csv`, `nomem_metrics.csv`
- N=64 comparison CSVs: `/workspace/dossie_reexec/A3/raw/mem_metrics.csv`, `nomem_metrics.csv`
- figure: `/workspace/dossie_reexec/A3_N128/figures/peak_vs_t.png` (N=64 dashed, N=128 solid, mem+no_mem)
- result: `/workspace/dossie_reexec/A3_N128/result.json`
