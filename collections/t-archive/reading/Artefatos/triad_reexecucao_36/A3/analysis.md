> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/A3/analysis.md) · [Collection / Acervo](../../../../README.md)

# A.3 re-execution analysis

Label: independent re-execution of dossier **"TRIAD — Dossiê unificado" (2026-08-21) Part I §2.4**, config A.3 real, on this Linux box (NumPy 2.2.4, fp64, N=64). **Not** a change of Leonardo's "full triad" operational reading.

Predictions were written to `/workspace/dossie_reexec/predictions_A3.md` **before** any Strang step (SHA256 `d67ed66caaa6a17ae9efa82a6450d37beaf77917e188902a4f0fb038a36d4010`, 14:56 BRT / 17:56 UTC). Executed stepper SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`. Parameters were **not** retuned.

Wall: 180.0 s total (~60 s/run), finished 15:01 BRT (18:01 UTC) on 2026-08-21.

## Protocol

Same IC, same standalone 3D Strang (`code/stepper.py`, clone of `run_R5_A2.py`; no triad-lang). Only diffs:

| run | Λ | λ |
|---|---|---|
| mem | −10 | (3, 1) |
| no_mem | −10 | (0, 0) |
| Lambda_ef | −6 | (0, 0) |

Collapse diagnostic: first t with peak ≥ 8 × peak_ini (= 11.4936), else inf. After the packet is ≲ dx, post-collapse structure is not interpreted.

## Compact table (this re-execution)

| run | peak_ini | peak_end | peak_max | PR_end | t_collapse | norm_end |
|---|---|---|---|---|---|---|
| mem | 1.436697 | 0.003430 | 13.174 | 2656.87 | **0.1425** | 1 + 1.1e-12 |
| no_mem | 1.436697 | 8.0975 | 12.680 | 0.4988 | 0.1350 | 1 + 7.9e-13 |
| Lambda_ef | 1.436697 | 12.097 | 16.675 | 0.2235 | 0.2750 | 1 + 6.8e-13 |

Dossier table (for comparison, not targets):

| configuração | pico ini → fim | PR fim |
|---|---|---|
| com memória (3,1) | 1.438 → 0.00063 | 5005 |
| controle λ=(0,0) | 1.438 → 8.10 | 0.499 |
| Λ=−6 sem memória | 1.437 → 12.1 | 0.224 |

## Verdicts vs predictions and vs dossier

### IC — MATCH

peak_ini = 1.436697 vs analytic 1 / (π s²)^{3/2} = 1.436697 (s=0.5). Norm = 1. Origin is on the N=64 grid. No IC bug.

### Claim 1 — memory prevents collapse where the no-memory control collapses

**Vs prediction (end-state by T=6): MATCH.** mem peak_end = 3.43e-3 (order 1e-3), PR_end = 2657 (thousands); packet fills the box (R_rms 0.61 → 9.61). no_mem peak_end = 8.10 > 5, PR_end = 0.499 < 1.

**Vs 8× diagnostic: FAIL / not hidden.** mem crosses 8 × peak_ini at t=0.1425, peak_max=13.17 at t=0.1575, stays above threshold only until t=0.17 (12 samples, Δt=0.0275), then the delayed repulsion reverses the spike and the field spreads. The prediction "t_collapse = inf" is **false** under the specified diagnostic. λ was **not** retuned.

**Vs dossier table: PARTIAL.** Direction and order match (spreads; peak ~10^{-3}; PR thousands). At **T=6** our peak_end is 0.00343 not 0.00063, PR 2657 not 5005. The dossier pair (0.00063, 5005) sits on our curve near **t=4.5** (peak=6.10e-4, PR=4809). After t≈4.5 the spread packet oscillates; T=6 is not the PR maximum (PR peaks just above 5000 around t≈5.6, then 2657 at T=6). Spec/dossier T=6 is what we report.

**Reading:** memory does **not** stay collapsed. It does execute a brief autofocus pulse (same early rise as no_mem), then delay reverses it. End-state anti-collapse holds. The 8× first-crossing diagnostic calls that pulse "collapse".

### Claim 2 — no_mem collapses

**MATCH** (prediction and dossier). t_collapse=0.135 < 2. peak_end=8.0975 vs dossier 8.10. PR_end=0.4988 vs dossier 0.499. Bit-level agreement on the end-state. After t≈0.14 the support is a few cells (dx=0.3125); do not interpret the late field beyond "it collapsed and stayed peaked".

### Claim 3 — not reducible to Λ_ef (Lambda_ef also collapses, at least as hard)

**MATCH** for the end-state claim. Lambda_ef t_collapse=0.275 (later than no_mem, as expected for weaker |Λ|), peak_end=12.097 vs dossier 12.1, PR_end=0.2235 vs dossier 0.224. Harder than no_mem at T=6 (higher peak, lower PR). The killing condition — "Lambda_ef does NOT collapse while mem does not" — **did not occur**. Delay, not the shift Λ → Λ+Σλ, is what spreads the mem run.

Caveat on t_collapse alone: mem's first 8× crossing (0.1425) is almost simultaneous with no_mem (0.135). Lambda_ef is later. The **mechanism** claim is carried by the *aftermath*: mem PR→thousands, both controls PR<1.

### Norm conservation — MATCH

Γ=0, no FDT. |norm_end − 1| ~ 10^{-12} on all three (unitary FFT + real multiplicative potential). Better than the predicted ~1e-10.

## What the 8× spike in mem means

The early mem and no_mem trajectories are almost the same until t≈0.14 (y has not had time to catch ρ; ν_fast=10 ⇒ τ=0.1). Then:

- no_mem: first pulse, dip, **re-collapse** and stays at peak~8, PR~0.5 (grid-limited blow-up).
- mem: first pulse (even slightly higher peak_max), then y catches up, V_mem repels, **no second collapse**, PR climbs to thousands.
- Lambda_ef: slower first pulse (weaker cubic), then **stays** collapsed harder (peak_max=16.7, 1515 samples still above 8×, last at T=6).

This is the delay mechanism the dossier argued, seen at high cadence. A run that only stored end-state, or recorded every ≫0.03 time units, would miss mem's 8× crossing and report "never collapsed".

## Parameters / integrity

- N=64, L=20, dt=0.0025, T=6, 2400 steps, ν_max·dt=0.025 < 0.05 (Euler OK).
- numpy 2.2.4, complex128 / float64. No mlx. No triad-lang.
- seed=42 unused (f_FDT=0); kept for protocol lock.
- Failures kept: mem 8× crossing reported; λ not changed; T=6 end-state reported even where it differs from dossier 0.00063 / 5005.

## Files

- predictions: `/workspace/dossie_reexec/predictions_A3.md` (copied at `A3/predictions_A3.md`)
- stepper: `/workspace/dossie_reexec/A3/code/stepper.py`
- runner: `/workspace/dossie_reexec/A3/code/run_A3.py`
- raw: `A3/raw/mem_metrics.csv`, `nomem_metrics.csv`, `lambdaef_metrics.csv`
- figures: `A3/figures/peak_vs_t.png`, `PR_vs_t.png`
- result: `A3/result.json`
