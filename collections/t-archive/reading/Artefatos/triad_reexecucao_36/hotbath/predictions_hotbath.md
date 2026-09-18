> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/hotbath/predictions_hotbath.md) · [Collection / Acervo](../../../../README.md)

# Predictions — A.3 anti-collapse vs hot FDT bath (written BEFORE any time integration)

Status: PREDICTIONS ONLY. No Strang step has been taken for this item.
No field has been evolved under any bath. Existing unitary A.3 CSVs
(`/workspace/dossie_reexec/A3/raw/mem_metrics.csv`, `nomem_metrics.csv`)
are archival loads, not new integrations. This file is written first.

Re-execution label: pending item 3 of dossier re-exec — does A.3
anti-collapse survive a hot FDT bath? Linux box, /workspace only.
Not a change of Leonardo's "full triad" operational reading.

Date written: 2026-08-21 ~17:31 BRT (America/Sao_Paulo, UTC-3).
Box: Linux, /usr/bin/python3 NumPy 2.2.4, fp64.
Scheme: REUSE `/workspace/dossie_reexec/A3/code/stepper.py`
SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`.
No triad-lang. λ will not be retuned.

These are mechanism predictions. They are not a declaration of which
run "wins". A bath that regularizes a focusing cubic is a physical
outcome, not a software failure. "Universe" (late field fills the box)
is distinct from "collapse" (peak → grid spike and stays).

## Config (fixed; will not be retuned)

hbar=1, m=1, Lambda=-10, sigma=2, alpha=0, V_ext=0
nu=(10.0, 0.5), L=20, N=64, dt=0.0025, T=6.0, init_sigma=0.5, seed=42
IC: one 3D gaussian Ψ = exp(-r²/(2 s²)), then normalize ∫|Ψ|² dV = 1.
Same IC for every run.

FDT lock (R5 / run-28 fdt_couple, already in the reused stepper):
  f_FDT = 2 Γ dx³ kT / ħ
  noise_amp = sqrt(f_FDT * dt / dx³) = sqrt(2 Γ kT dt / ħ)
  ξ = (N + i N) / sqrt(2)   (complex white, unit variance per component)

Collapse diagnostic: t_collapse = first t with peak ≥ 8 * peak_ini
(~11.49), else inf. Also t_fill = first t with R_rms > 5 (box-scale
spread), else inf.

Atom-persistence diagnostics (not retuned):
  PR_volume = (∫ρ dV)² / ∫ρ² dV     (uniform box → L³ = 8000)
  n_cells   = (∑_i ρ_i)² / ∑_i ρ_i² = PR / dx³
  box cells = N³ = 262144
  "atom persists" = late PR stays well below box-filling (≪ 8000)
                    and n_cells is a compact packet, not the whole box.

Seven runs, same IC, same stepper; only (λ, Γ, kT) differ.
Unitary rows 1–2 are LOADED from A.3 raw, not re-integrated.

| # | name            | λ       | Γ    | kT    | source |
|---|-----------------|---------|------|-------|--------|
| 1 | mem_unitary     | (3, 1)  | 0    | 0     | LOAD A3/raw/mem_metrics.csv |
| 2 | nomem_unitary   | (0, 0)  | 0    | 0     | LOAD A3/raw/nomem_metrics.csv |
| 3 | mem_bath_cool   | (3, 1)  | 0.01 | 0.001 | NEW (R5-FDT scale) |
| 4 | mem_bath_mid    | (3, 1)  | 0.05 | 0.1   | NEW |
| 5 | mem_bath_hot    | (3, 1)  | 0.05 | 1.0   | NEW |
| 6 | nomem_bath_hot  | (0, 0)  | 0.05 | 1.0   | NEW (control) |
| 7 | nomem_bath_mid  | (0, 0)  | 0.05 | 0.1   | NEW (control) |

Expected noise_amp (prediction, not a measured value):
  cool: sqrt(2*0.01*0.001*0.0025) = sqrt(5e-8)  ≈ 2.24e-4  (tiny)
  mid:  sqrt(2*0.05*0.1*0.0025)   = sqrt(2.5e-5) ≈ 5.00e-3
  hot:  sqrt(2*0.05*1.0*0.0025)   = sqrt(2.5e-4) ≈ 1.58e-2
Damping-only envelope over T=6 if no noise: exp(-Γ T) on amplitude,
norm ~ exp(-2 Γ T) → cool ≈ 0.887, mid/hot ≈ 0.549. FDT injects
norm, so bath runs will NOT conserve norm=1. That is not a bug.

## Already-known unitary A.3 (N=64) — loaded, not re-run

These numbers already exist. They are the baseline the bath is
tested against, not a new prediction of a winner.

- mem unitary: peak_end ~ 0.00343, PR_end ~ 2657, peak_max ~ 13.17
  at t~0.1575. Early 8× pulse (t_collapse=0.1425, 12 samples above
  8×, last at t=0.17) then spread. R_rms 0.61 → 9.61, t_fill ~ 1.63.
  This is the delay mechanism: first autofocus, then y catches ρ
  and the packet fills the box. End-state is "universe", not a
  stuck grid spike.
- no_mem unitary: peak_end ~ 8.10, PR_end ~ 0.499, t_collapse=0.135,
  peak_max ~ 12.68. Stays collapsed (grid-limited blow-up).

## Qualitative predictions (orders; do not pick a winner as fact)

### 3. mem + bath cool  (λ=(3,1), Γ=0.01, kT=0.001)

R5-FDT scale. noise_amp ~ 2e-4 is a weak kick relative to the O(1)
peak. Expect the unitary mem story almost intact:

- Early 8× pulse still finite and still happens (anti-collapse of
  the *singularity* is the delay, which is already late vs ν_fast=10
  ⇒ τ=0.1; a tiny bath will not cancel the first autofocus).
- Peak stays finite (no second collapse). Late field fills
  (R_rms↑, PR↑). This is "universe", not failure.
- Norm drifts slowly (weak Γ + tiny FDT).
- Atom persistence: same as unitary mem — the packet spreads to
  box scale by T=6. That is already the unitary end-state, not a
  bath-induced death of the atom.

### 4. mem + bath mid  (λ=(3,1), Γ=0.05, kT=0.1)

Stronger damping, moderate noise. Prediction, not a verdict:

- Early pulse still finite. Memory delay should still reverse the
  first autofocus if the cubic focusing is not already washed out.
- Late field: R_rms↑ and PR↑ — dissipation + noise both push the
  field toward filling. Peak stays finite.
- Norm will drop from Γ and be refilled by FDT; |norm_end-1| is
  not a conservation test here.
- Atom: mid bath may already start to dissolve a compact packet
  faster than unitary mem. Persistence of a *localized atom*
  (PR staying O(1)–O(10), not thousands) is not predicted to hold.
  Persistence of a *finite peak* is.

### 5. mem + bath hot  (λ=(3,1), Γ=0.05, kT=1.0)

Very hot (kT order 1, Γ~0.05). Box fills fast. Atoms do not persist.

- Protection of *finite peak* may still hold: the early pulse
  should remain finite (anti-collapse of the singularity). The
  late field is a noisy, damped, box-filling soup, not a grid
  spike. peak_end expected ≪ 8×peak_ini after the pulse, possibly
  small (thermal floor).
- t_fill expected early (R_rms>5 well before T=6), PR climbing
  toward a large fraction of L³=8000. n_cells toward a large
  fraction of N³.
- Claim (c) "atom persists" is predicted to FAIL at hot. That is
  the expected physics of a hot bath, not a code failure, and
  λ will not be retuned to save the atom.

### 6. no_mem + bath hot  (λ=(0,0), Γ=0.05, kT=1.0)  — control

May ALSO stay finite. Dissipation and additive noise can regularize
a focusing-cubic blow-up even with no memory. If no_mem+hot also
spreads (peak_end small, PR large, no stuck spike), then the *late
rescue* is the bath, not the memory — say so. Compare 5 vs 6 on
the late state (peak_end, PR_end, R_rms_end, t_fill).

Possible branches (do not pick one as fact before the run):

- A. no_mem+hot still collapses and stays peaked (PR_end ≲ 1,
  peak_end ≳ few). Then late rescue in mem+hot, if it spreads, is
  still memory (or memory+bath together). Bath alone did not save.
- B. no_mem+hot also spreads / stays finite. Then the bath, not
  the memory, is doing the late rescue. Memory is not uniquely
  responsible for the T=6 end-state. Report that honestly.
- C. both stay finite but mem+hot and no_mem+hot differ in *early*
  pulse (height, duration) or in how fast they fill. Then memory
  still shapes the singularity; the bath owns the late fill.

The early pulse (t ≲ 0.3) is the place to look for memory's
anti-collapse of the singularity, because y has not caught ρ yet
in the unitary case either. If both 5 and 6 show the same early
8× pulse then the same thermal fill, memory is idle at hot.

### 7. no_mem + bath mid  (λ=(0,0), Γ=0.05, kT=0.1)

Intermediate control. Mid noise may or may not be enough to
regularize the cubic. If no_mem+mid still collapses and stays
peaked while mem+mid spreads, memory is still doing work at mid
temperature. If both spread, the mid bath is already the late
rescue. Same three-branch reading as (6), one notch cooler.

## What would count as FAIL / PARTIAL / MATCH (after the runs)

Score three claims separately. Do not retune λ. Do not hide an
8× crossing.

(a) Peak stays finite with mem+bath (runs 3, 4, 5).
    MATCH: after the early pulse, peak does not run away; peak_end
    remains finite (no second unresolved blow-up). An early 8×
    pulse (same as unitary mem) is allowed and is not a fail of
    (a) — that pulse is already the known A.3 delay story.
    FAIL: mem+bath peak_end is a stuck grid spike (PR_end ≲ 1,
    peak comparable to no_mem unitary), or NaNs.

(b) Late rescue is memory vs bath (compare 5 vs 6; also 4 vs 7).
    MATCH-memory: mem+bath spreads, no_mem+same-bath stays
    collapsed. Memory is necessary for the late rescue.
    MATCH-bath: both spread / both stay finite with similar late
    PR and R_rms. The bath, not the memory, is doing the late
    rescue — say so. This is not a hidden fail; it is the
    control working.
    PARTIAL: both finite but late diagnostics differ by a lot
    (PR, t_fill, peak_end), or only one temperature pair agrees.

(c) Atom persists (n_cells / PR not box-filling).
    Predicted: FAIL at hot (run 5). Cool may look like unitary
    mem (already box-filling by T=6, PR~2657). Mid in between.
    A FAIL of (c) at hot is the expected reading of "very hot kT
    (order 1, Γ~0.05): box fills fast; atoms do not persist."
    Do not retune λ to save the atom.

Overall item verdict will be assembled from (a)(b)(c), not from
a single winner. Unitary mem already taught: end-state spread +
early 8× pulse = delay mechanism, reported as PARTIAL vs a
naive "never crosses 8×" claim. Same honesty here.

## What is NOT predicted

- Exact floats for peak_end / PR_end / t_fill on bath runs.
- That the atom remains a compact localized object at kT=1.
- That memory is the unique regularizer once a hot bath is on.
- Norm conservation on Γ>0 or f_FDT>0 runs.

## Label

Every number produced after this file is a RE-EXECUTION of the
A.3 core under an FDT bath on this Linux box. It is not a revision
of the operational "full triad" reading. Failures are kept.
