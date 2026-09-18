# A.3 hot FDT bath — analysis

Label: pending item 3 of dossier re-exec — does A.3 anti-collapse survive a hot FDT bath? Linux box, /workspace only. **Not** a change of Leonardo's full-triad operational reading.

Predictions written **before** any bath integration: `/workspace/dossie_reexec/predictions_hotbath.md` (SHA256 `b7936bdd039c0ad96cf9cc28d7da226906b276b9e3c353713887115126ea2511`), 17:32 BRT / 20:32 UTC on 2026-08-21.
Executed stepper SHA256 `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` (reuse of `/workspace/dossie_reexec/A3/code/stepper.py`). λ was **not** retuned. NumPy 2.2.4, fp64, N=64.
Wall: 464.3 s total (~90–99 s per new run). Finished 17:42 BRT (20:42 UTC) on 2026-08-21.

## Protocol

Same IC, same standalone 3D Strang. FDT lock: `f_FDT = 2 Γ dx³ kT / ħ`, `noise_amp = sqrt(f_FDT dt / dx³)`, `ξ = (N+iN)/√2`. Collapse: first t with peak ≥ 8 × peak_ini (= 11.4936). Fill: first t with R_rms > 5. n_cells = PR / dx³. Box-uniform PR = L³ = 8000; box cells = N³ = 262144.

Unitary rows 1–2 **loaded** from A.3 raw (not re-integrated). Five new bath runs integrated. λ not retuned.

| # | run | λ | Γ | kT | noise_amp | source |
|---|---|---|---|---|---|---|
| 1 | mem_unitary | (3, 1) | 0 | 0 | 0 | LOAD A3/raw/mem_metrics.csv |
| 2 | nomem_unitary | (0, 0) | 0 | 0 | 0 | LOAD A3/raw/nomem_metrics.csv |
| 3 | mem_bath_cool | (3, 1) | 0.01 | 0.001 | 2.236e-4 | integrate (R5-FDT) |
| 4 | mem_bath_mid | (3, 1) | 0.05 | 0.1 | 5.000e-3 | integrate |
| 5 | mem_bath_hot | (3, 1) | 0.05 | 1.0 | 1.581e-2 | integrate |
| 6 | nomem_bath_hot | (0, 0) | 0.05 | 1.0 | 1.581e-2 | integrate (control) |
| 7 | nomem_bath_mid | (0, 0) | 0.05 | 0.1 | 5.000e-3 | integrate (control) |

## Compact table

| run | peak_end | peak_max | PR_end | R_rms_end | t_collapse | t_fill | n_cells | norm_end | peak/norm |
|---|---|---|---|---|---|---|---|---|---|
| mem_unitary | 0.003430 | 13.17 | 2657 | 9.612 | 0.1425 | 1.6325 | 87060 | 1.000 | 3.43e-3 |
| nomem_unitary | 8.098 | 12.68 | 0.499 | 6.707 | 0.1350 | 4.2650 | 16 | 1.000 | 8.10 |
| mem_bath_cool | 0.004580 | 13.15 | 3562 | 9.813 | 0.1425 | 1.0850 | 116722 | 1.794 | 2.55e-3 |
| mem_bath_mid | 0.5989 | 12.92 | 4011 | 10.01 | 0.1425 | 0.0050 | 131423 | 362.5 | 1.65e-3 |
| mem_bath_hot | 4.974 | 12.83 | 4283 | 9.999 | 0.1400 | 0.0025 | 140349 | 3604 | 1.38e-3 |
| nomem_bath_hot | 7.413 | 12.65 | 4013 | 10.02 | 0.1300 | 0.0025 | 131491 | 3621 | 2.05e-3 |
| nomem_bath_mid | 0.6331 | 12.56 | 4002 | 10.00 | 0.1325 | 0.0050 | 131133 | 362.6 | 1.75e-3 |

IC: peak_ini=1.436697 (analytic 1.436697), PR_ini=1.968663, R_rms_ini=0.612372, norm=1. dx=0.3125, dV=0.03051758.

**Read peak_end on hot with norm.** Hot runs have norm_end ~ 3600 because FDT injects. A uniform box at that mass has ρ = 3600/8000 = 0.45. The raw peak_end of 5–7 is a thermal fluctuation, not a grid spike. The intensive diagnostic peak/norm is ~10⁻³ on every spreading run and **8.1** on the only true stuck collapse (nomem unitary, n_cells=16).

## Verdicts vs predictions

### (a) peak stays finite with mem+bath — **MATCH**

All three mem+bath runs reverse the early 8× pulse and do **not** stay as a grid spike.

- Cool: peak_max=13.15 at t=0.1575 (12 samples above 8×, last at 0.17) — same pulse as unitary mem — then peak_end=0.00458, PR=3562.
- Mid: same first pulse (t_collapse=0.1425, last above 8× at 0.17), then peak_end=0.599, PR=4011.
- Hot: pulse still finite (peak_max=12.83 at t=0.15, 10 samples, last at 0.1625), then thermal floor, peak/norm=1.38e-3.

This is "universe" (late field fills), not failure. An early 8× crossing is the known A.3 delay autofocus; it is not a fail of (a).

### (b) late rescue is memory vs bath (5 vs 6, 4 vs 7) — **MATCH-bath**

Prediction branch B happened. Say so: **the bath, not the memory, is doing the late rescue.**

| pair | mem late | no_mem late |
|---|---|---|
| hot 5 vs 6 | PR=4283, R_rms=10.00, n_cells=140k, peak/norm=1.38e-3 | PR=4013, R_rms=10.02, n_cells=131k, peak/norm=2.05e-3 |
| mid 4 vs 7 | PR=4011, R_rms=10.01, n_cells=131k, peak/norm=1.65e-3 | PR=4002, R_rms=10.00, n_cells=131k, peak/norm=1.75e-3 |

Both controls spread. Contrast with unitary no_mem: PR=0.499, n_cells=16, peak/norm=8.10 — that is the stuck spike the bath removes even without λ.

The auto-scorer first tagged hot as "unclear" because raw peak_end (4.97 vs 7.41) is > 1. That cut is wrong once FDT has grown the norm to 3600. Intensive and participation diagnostics say both are thermal box-fill.

Memory is **not idle on the early pulse**:
- mem+hot t_peak_max=0.150, t_last_above_8×=0.1625, 10 samples.
- no_mem+hot t_peak_max=0.140, t_last_above_8×=0.150, 9 samples, then several extra high pulses between t≈0.2–1.3 (visible on peak_vs_t) that memory suppresses.
- Same pattern at mid: no_mem+mid re-attempts at t=0.5 (peak=7.77, PR=688) then the bath washes it; mem+mid does not re-spike.

So: delay still shapes the singularity; the bath owns the T=6 end-state. Without a bath, memory is still necessary (unitary pair). With a mid/hot bath, memory is not necessary for late finiteness.

### (c) atom persists (n_cells / PR not box-filling) — **FAIL**

Predicted. Do not retune λ to save the atom.

- Hot: t_fill=0.0025 (first step). PR_end=4283 (half the uniform box). n_cells=140k / 262k. Atoms do not persist.
- Mid: t_fill=0.005. Same thermal fill (norm_end=363, PR=4011).
- Cool: t_fill=1.085, PR=3562 — already the unitary-mem "universe" (unitary t_fill=1.63, PR=2657), plus a slow FDT norm drift to 1.79. Not a compact atom at T=6.

A compact atom would be PR ≪ 200 and t_fill=inf. None of the mem+bath runs meet that. Unitary mem already did not.

### Overall item — **PARTIAL**

(a) MATCH: finite peak with mem+bath; early 8× pulse reverses; no stuck spike.
(b) MATCH-bath: late rescue at mid and hot is the bath (5≈6, 4≈7). Memory still kills the extra early pulses.
(c) FAIL: atom does not persist at hot (also mid; cool is already universe). Predicted.

Anti-collapse of the *singularity* survives a hot FDT bath. Persistence of a *localized atom* does not. λ was not changed.

## Reading vs predictions

- Unitary A.3 mem (loaded): peak_end=0.00343, PR=2657, early 8× then spread. Matches the stated baseline.
- Mem+bath: early pulse still finite. Late field fills (R_rms↑, PR↑). Peak stays finite. "Universe", not failure. **Holds.**
- No-mem + same bath: ALSO stays finite. Mid and hot no_mem both go to PR~4000. **The bath, not the memory, does the late rescue.** Reported.
- Very hot kT~1, Γ=0.05: box fills on the first step; atoms do not persist. Protection of finite peak (and of peak/norm) still holds.
- Cool (R5-FDT) sits on top of unitary mem through the pulse and only slowly diverges (more PR, earlier t_fill, norm 1.79). Tiny bath.

Norm is **not** conserved on bath runs (FDT injects). Cool +0.79; mid ×363; hot ×3604. That is the lock, not a stepper bug. Unitary |norm−1| ~ 10⁻¹².

## Parameters / integrity

- N=64, L=20, dt=0.0025, T=6, 2400 steps, ν_max·dt=0.025 < 0.05 (Euler OK).
- numpy 2.2.4, complex128 / float64. No mlx. No triad-lang.
- seed=42 on every bath run (independent rng per run).
- stepper SHA locked. λ not retuned. Failures kept (c; 8× crossings reported).
- Predictions file mtime 17:32 BRT; first bath step after that (mem_bath_cool started ~17:35 BRT).

## Files

- predictions: `/workspace/dossie_reexec/predictions_hotbath.md` (copy at `hotbath/predictions_hotbath.md`)
- stepper: `/workspace/dossie_reexec/A3/code/stepper.py` (byte-identical copy in `hotbath/code/`)
- runner: `/workspace/dossie_reexec/hotbath/code/run_hotbath.py`
- binder: `/workspace/dossie_reexec/hotbath/code/launch.py`
- raw: `hotbath/raw/*.csv`
- figures: `hotbath/figures/peak_vs_t.png` (also PR_vs_t.png, Rrms_vs_t.png)
- result: `hotbath/result.json`
