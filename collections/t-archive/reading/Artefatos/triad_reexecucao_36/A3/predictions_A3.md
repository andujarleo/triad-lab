> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/A3/predictions_A3.md) · [Collection / Acervo](../../../../README.md)

# Predictions — TRIAD A.3 re-execution (written BEFORE any time integration)

Status: PREDICTIONS ONLY. No Strang step has been taken. No field has been evolved.
Re-execution label: independent re-run of dossier "TRIAD — Dossiê unificado" (2026-08-21) Part I §2.4, config A.3 real. Not a change of Leonardo's "full triad" operational reading.

Date written: 2026-08-21 (America/Sao_Paulo).
Box: Linux, NumPy 2.2.4, fp64, 8 CPUs.
Scheme: standalone 3D Strang (same as /workspace/run_R5_A2.py). Not triad-lang TriadParams.

## Config (fixed; will not be retuned)

hbar=1, m=1, Lambda=-10, sigma=2, alpha=0, Gamma=0, f_FDT=0, V_ext=0
nu=(10.0, 0.5), L=20, N=64, dt=0.0025, T=6.0, init_sigma=0.5, seed=42
IC: one 3D gaussian Ψ = exp(-r²/(2 s²)), then normalize ∫|Ψ|² dV = 1.
Three runs, same IC, same stepper, only these diffs:
1. mem:      lam=(3.0, 1.0)                 # Σλ=4
2. no_mem:   lam=(0.0, 0.0)
3. Lambda_ef: Lambda=-6.0, lam=(0.0, 0.0)   # Λ_ef = Λ+Σλ = -6, no delay

Collapse diagnostic: t_collapse = first t where peak ≥ 8 * peak_ini (or inf if never).

## IC predictions (must hold before integration; if not, STOP)

- peak_ini ≈ 1.437 = 1 / (π s²)^{3/2} with s=0.5.
  Analytic: (π * 0.25)^{1.5} = (0.785398...)^{1.5} ≈ 0.696... ; 1/0.696 ≈ 1.437.
  Grid N=64, L=20, dx=20/64=0.3125. The continuous peak is sampled near the origin; expect peak_ini in [1.42, 1.45], closest to 1.437.
- norm = 1 (by construction, volume quadrature).
- PR_ini = (norm²) / (∫ ρ² dV). For a 3D gaussian of width s=0.5 this is order-1 (a few units), not thousands.
- R_rms_ini ≈ sqrt(3/2) * s ≈ 0.612.

If peak_ini is not ~1.437, STOP and fix the IC. Do not integrate.

## Qualitative pattern (orders of magnitude, not dossier floats)

These are mechanism predictions, not copies of dossier output numbers.

### 1. mem  (Λ=-10, λ=(3,1), delay present)

- Does NOT collapse by T=6.
- t_collapse = inf (peak never reaches 8*peak_ini ≈ 11.5).
- peak_end << 1, order 1e-3 (packet spreads through the box).
- peak_max remains O(1) — comparable to peak_ini, not an 8× blow-up.
- PR_end in the thousands (volume PR; packet fills a large fraction of the L=20 box).
- Mechanism is DELAY of the repulsive memory, not the mere shift Λ → Λ+Σλ.
- After the packet is well resolved and spreading, the late field is physically meaningful (no collapse).

### 2. no_mem  (Λ=-10, λ=(0,0), focusing cubic only)

- DOES collapse.
- t_collapse finite and < 2.
- peak_end > 5 (well above peak_ini; typically O(1)–O(10) on this grid before the packet is smaller than dx).
- PR_end < 1 (volume PR of a near-grid-point spike).
- After the packet is smaller than dx=0.3125, do NOT interpret the post-collapse field — only t_collapse and that it collapsed. peak_end / PR_end are then grid artifacts of an unresolved blow-up.

### 3. Lambda_ef  (Λ=-6, λ=(0,0); matched Λ_ef = Λ+Σλ, no delay)

- ALSO collapses, at least as hard as no_mem.
- t_collapse finite.
- peak_end large (order similar to or larger than no_mem), PR_end < 1.
- If Lambda_ef does NOT collapse while mem does not, the claim "anti-collapse is not reducible to Λ_ef" DIES.
- The control exists to isolate the delay: same effective cubic strength, no memory ODE. Collapse here + no-collapse in mem ⇒ the delay (the y-dynamics) is the mechanism.

### All three

- Unitary: Γ=0, no FDT. norm conserved to ~1e-10 (fft unitary + real multiplicative potential).
- If a collapse run's late field is unresolved (support ≲ dx), ignore structure of Ψ after t_collapse; keep the diagnostic times and the fact of collapse.

## What would count as FAIL vs this prediction (not vs dossier floats)

- mem collapses (t_collapse finite) — FAIL of the delay-protects claim. Report it; do not retune λ.
- no_mem does not collapse by T=6 — FAIL of the focusing-cubic-collapses claim.
- Lambda_ef does not collapse while mem does not — FAIL of "not reducible to Λ_ef".
- peak_ini far from 1.437 — IC bug; stop.
- |norm_end - 1| ≫ 1e-10 on a non-collapsed run — stepper bug (or interpretation of a collapsed unresolved field).

## What is NOT predicted

Exact dossier floats (mem 1.438→0.00063 PR=5005; no_mem →8.10 PR=0.499; Λ=-6 →12.1 PR=0.224) are NOT copied here as target numbers. They are the comparison table for analysis.md after the runs. This re-execution may differ at the float level and still MATCH the qualitative claims.

## Label

Every number produced after this file is a RE-EXECUTION of the dossier A.3 protocol on this Linux box. It is not a revision of the operational "full triad" reading.
