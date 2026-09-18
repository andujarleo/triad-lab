# A.3 N=160 resolution-check analysis

Label: second resolution check of the N=64 / N=128 re-executions of dossier **"TRIAD — Dossiê unificado" (2026-08-21) Part I §2.4**, config A.3 real, N=160 (dx=0.125). **Not** a change of Leonardo's "full triad" operational reading. λ was **not** retuned. Stepper was **not** rewritten.

Predictions were written to `/workspace/dossie_reexec/predictions_A3_N160.md` **before** any N=160 Strang step (15:42 BRT / 18:42 UTC). That file was **not** rewritten after integration (mtime still 18:42:29 UTC; SHA256 `b7656b1f99aa5143ebc673ebe453c7e15af3e4eb972dfd721c627fbc567dabcc`). Executed stepper SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` (imported from `/workspace/dossie_reexec/A3/code/stepper.py`). Runner SHA256 `ffa6a5f94288cb9b6b0507f5fc799f11a0fa545aa4218cf85056a7fe8dff89ae`.

Both legs were newly integrated this pass (mem wall 2001.2 s, ended 16:16 BRT / 19:16 UTC; no_mem wall 1999.3 s, ended 16:50 BRT / 19:50 UTC). Combined wall 4001.0 s.

## Protocol

Same IC, same standalone 3D Strang (`A3/code/stepper.py`). Only N changes (64 → 128 → 160). Two runs; Lambda_ef skipped.

| run | Λ | λ | N=160 status |
|---|---|---|---|
| mem | −10 | (3, 1) | integrated this pass |
| no_mem | −10 | (0, 0) | integrated this pass |

Collapse diagnostic: first t with peak ≥ 8 × peak_ini (= 11.4936), else inf. Pulse = local maximum of peak(t) at or above 8×. After the packet is ≲ dx, post-collapse structure is not interpreted as continuum physics.

## Compact table — N=64 / 128 / 160

| N | run | peak_ini | peak_end | peak_max (t) | PR_end | t_collapse | 8× window | n_pulses | norm_end |
|---|---|---|---|---|---|---|---|---|---|
| 64 | mem | 1.436697 | 0.003430 | 13.17 (0.1575) | 2657 | 0.1425 | 0.1425–0.170 (Δt=0.0275) | 1 | 1 + 1.1e-12 |
| 64 | no_mem | 1.436697 | 8.098 | 12.68 (0.1425) | 0.499 | 0.135 | stays peaked | — | 1 + 7.9e-13 |
| 128 | mem | 1.436697 | 0.002359 | 62.48 (0.410) | 2444 | 0.1275 | 0.1275–0.635 (Δt=0.5075) | 6 | 1 + 1.2e-12 |
| 128 | no_mem | 1.436697 | 65.26 | 84.57 (0.6325) | 0.0616 | 0.115 | 0.115–6.0 (2326 samples) | — | 1 + 1.1e-12 |
| 160 | mem | 1.436697 | 0.006496 | 99.74 (0.335) | 2345 | 0.1275 | 0.1275–0.4225 (Δt=0.295) | 9 | 1 + 1.6e-12 |
| 160 | no_mem | 1.436697 | 48.25 | 95.42 (0.210) | 0.220 | 0.115 | 0.115–6.0 (2344 samples) | — | 1 + 1.7e-12 |

N=64 anchors from `/workspace/dossie_reexec/A3/result.json`. N=128 from `/workspace/dossie_reexec/A3_N128/result.json`. N=160 from this box.

## Verdicts vs predictions

### IC — MATCH

peak_ini = 1.4366969770 = analytic 1/(π s²)^{3/2}. Norm = 1. Origin on the N=160 grid (even N, endpoint=False). No IC bug. Same continuous gaussian.

### 1. no_mem sharper than N=128 — PARTIAL

Prediction: still collapsed; peak_end **and** peak_max **RISE again** vs N=128 (65.26 / 84.58); PR_end stays < 1 and may drop; stays above 8× through T=6.

- Still collapsed: t_collapse = **0.115** (identical to N=128; N=64 was 0.135). Same early order.
- peak_max = **95.42** at t=0.210 vs 84.57 at t=0.6325. **Rises** (~13%). The early unresolved spike is taller and arrives earlier.
- peak_end = **48.25** vs 65.26. **Falls** (~26%), not rises.
- PR_end = **0.220** vs 0.0616. Stays < 1 but **rises** (late remnant is less of a near-grid-point spike).
- Stays above 8× through T=6 (2344 of 2401 samples). Not a reversible pulse.

The blow-up is still genuine (finite early t_collapse, peak_max still climbing vs N=128, late field still a collapsed remnant). The strict "peak_end and peak_max both rise" clause is only half-true: the early spike sharpened, the late grid-limited plateau did not. After the packet is ≲ dx=0.125 the late numbers are artifacts; the *direction* predicted for peak_end did not hold.

FAIL condition (no collapse by T=6) **did not occur**. peak_max did not fall. So not FAIL. Not a clean MATCH either.

**PARTIAL.**

### 2. mem H_plateau vs H_ramp at N=160 — H_plateau lives (MATCH); H_ramp dies

Prediction: N=128 supported plateau; predict H_plateau still. Score the end-state, not the early train (that is criterion 3).

**H_plateau — MATCH.**

- peak_end = **6.496e-3** (same 10^{-3} decade as N=128 2.359e-3 and N=64 3.43e-3; not O(10^{-1}) or O(1)+).
- PR_end = **2345** (thousands; N=128 was 2444, N=64 was 2657). Packet fills a large fraction of the L=20 box (R_rms 0.612 → 10.15).
- Aftermath still spreads: after t=1 the peak stays O(10^{-3})–O(10^{-2}) (min 7.37e-4 at t=3.87, max 1.09e-2 at t=5.74). By T=6 the field is delocalized. t_collapse is finite (0.1275) but the late state is **not** a collapsed spike.

**H_ramp — FAIL for the end-state.**

- peak_end did **not** leave the 10^{-3} decade.
- PR_end did **not** collapse out of the thousands toward O(1).
- The field does **not** stay above 8× through T=6 (last 8× at 0.4225).
- N=128's rebound is **not** a resolution artifact that N=160 lets run away.

**Hypothesis that lives: H_plateau.** End-state anti-collapse is real at N=160. Early train ramped 62 → 100 and added pulses, then rebound still won. λ=(3,1) is not retuned.

### 3. pulse train vs N=128 — MATCH (taller, more pulses, first-crossing stable)

| | N=64 mem | N=128 mem | N=160 mem |
|---|---|---|---|
| t_first 8× | 0.1425 | 0.1275 | **0.1275** |
| t_peak_max | 0.1575 | 0.410 | 0.335 |
| peak_max | 13.17 | 62.48 | **99.74** |
| t_last 8× | 0.170 | 0.635 | 0.4225 |
| Δt above 8× | 0.0275 | 0.5075 | 0.295 |
| n_samples | 12 | 89 | 108 |
| n_pulses (local max ≥ 8×) | 1 | 6 | **9** |
| n_intervals | 1 | 6 | 4 |

N=160 mem pulses (t, peak): 0.1475/80.5, 0.195/90.6, 0.2275/98.2, 0.2375/16.6 (dip wiggle), 0.2525/99.4, 0.275/98.8, 0.300/99.5, 0.335/99.7, 0.385/95.0.

- First-crossing **identical** to N=128 (0.1275). Stable. Delay still needs a squeeze; y lags ρ (ν_fast=10 ⇒ τ=0.1).
- Taller: 62.48 → 99.74 (~1.60×). MATCH.
- More pulses: 6 → 9. MATCH (even if the 16.6 shoulder is dropped, 8 > 6).
- Train is **compressed** in time (last 8× 0.635 → 0.4225; 6 intervals → 4) — more oscillations packed into a shorter window, not a longer one.
- Train **does rebound** (last 8× at 0.4225; T=6 is spread). Not H_ramp.
- Train does **not** vanish.

**MATCH** of the predicted clause (taller / more pulses / first-crossing stable). Height and count remain resolution-dependent (13 → 62 → 100; 1 → 6 → 9); do not treat any of those as continuum values. First-crossing has now sat at 0.1275 on two grids.

## Reading

Memory still prevents a *lasting* collapse where the no-memory control collapses. H_plateau holds at N=160: peak_end stays O(10^{-3}), PR stays in the thousands. The early mem train continues the N=64→128 trend (taller, more pulses) while the first 8× time has locked at 0.1275. After y catches ρ the repulsion still wins; the train is over by t=0.42.

no_mem is still a genuine blow-up (t_collapse=0.115, stays above 8× to T=6, peak_max rose 84.6 → 95.4). The late peak_end did **not** rise (65 → 48); treat late no_mem numbers as grid artifacts. The early-spike direction is the surviving tell.

λ=(3,1) is **not** retuned. The 8× first-crossing diagnostic still calls the mem train "collapse"; the physics claim is the aftermath.

## Norm conservation — MATCH

Γ=0, no FDT. |norm_end − 1| ~ 10^{-12} on both N=160 runs (unitary FFT + real multiplicative potential).

## Parameters / integrity

- N=160, L=20, dx=0.125, dt=0.0025, T=6, 2400 steps, ν_max·dt=0.025 < 0.05 (Euler OK).
- numpy 2.2.4, complex128 / float64. No mlx. No triad-lang. System python for integrate; `/workspace/.venv/bin/python` for the figure (system python lacks matplotlib).
- seed=42 unused (f_FDT=0); kept for protocol lock.
- predictions file not rewritten after integrating (written 15:42 BRT / 18:42 UTC, before any 160³ field).
- Failures / partials kept: criterion 1 scored PARTIAL because peak_end fell; H_ramp killed on the end-state; λ not changed.

## Files

- predictions: `/workspace/dossie_reexec/predictions_A3_N160.md` (written before any N=160 step; not rewritten)
- stepper: `/workspace/dossie_reexec/A3/code/stepper.py`
- runner: `/workspace/dossie_reexec/A3_N160/code/run_A3_N160.py` (launched via `code/launch.py`)
- raw: `A3_N160/raw/mem_metrics.csv`, `A3_N160/raw/nomem_metrics.csv`
- N=64 / N=128 comparison CSVs: `A3/raw/*.csv`, `A3_N128/raw/*.csv`
- figure: `A3_N160/figures/peak_vs_t.png` (N=64 dashed, N=128 dotted, N=160 solid, mem+no_mem)
- result: `A3_N160/result.json`
