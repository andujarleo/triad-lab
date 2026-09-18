> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/kstar/analysis.md) · [Collection / Acervo](../../../../README.md)

# R5 k*L ≈ 16.3 — independent re-execution (pending item 4)

**Date:** 2026-08-21, America/Sao_Paulo (UTC-3). Sweep finished 17:37 -03.
**Dossier:** TRIAD spec §10.4 / A.2 “k*L≈16.3 across calibrations”, pending item 4.
**Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_kstar.md`, SHA `7711f5679cb616a959e3a6cf2b855c6c6303c471c58292cc0fe0f7e822e112b1`). No retuning toward 16.3. Failures kept.
**Stepper:** standalone 3D Strang `/workspace/dossie_reexec/A3/code/stepper.py` SHA `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` (copy also in `kstar/code/stepper.py`).
**Runner SHA256:** `9f6033defed1822b5d2671aac494781ef95facdb66676e943b7bc45d9bed99fb` (`run_kstar.py`).
**Spectral:** same as `/workspace/run_R5_A2.py` — radial *mean-per-mode* shell power of Ψ̂; k* = argmax P(|k|) for k_center > 2π/L; k*L = k* × L; C = voxel power(|k|>2π/L)/total. Shell centers k_i = (i+½)·2π/L ⇒ k_i L = 2π(i+½).
**Runtime:** `/usr/bin/python3` + NumPy 2.2.4, fp64. Plots via `/workspace/.venv` matplotlib. 4 workers. T=8 kept (not dropped to 6). Wall 175.2 s (~88 s per N=64 run, 30.6 s for N=48).
**Physics (unitary R5):** Λ_baseline=−8, lam=(1.125, 0.375), ν=(10, 0.5), α=Γ=f_FDT=0, V_ext=0, s=0.5, seed=42, dt=0.0025. N=64 (D also N=48). Not the Q01 hot-FDT / Nyquist regime.

## Verdict: **H_grid**

k* is the first allowed radial shell (i*=1) on every record of every run. Late-window median k*L is the mesh identity **3π = 9.42477796076938**, not 16.3, not πN.

This is the low-n / first-allowed-shell lock in the written scoring rules, not Nyquist and not a structural invariant of the R5 family.

- **Not H_invar.** 16.3 never appears. No finite-k peak exists (`spectrum_peaked=false` on all 8; first 6 allowed shells monotonically falling). C is *not* a crystal: the IC Gaussian already has C≈0.995 because a narrow packet has a broad Fourier transform. Late C stays 0.968–0.999 for the same reason.
- **Not H_mobile.** Physics knobs that must move a physical scale (Λ ∈ {−6,−8,−10}, norm ∈ {0.5,1,2}, L ∈ {15,20,25}) leave k*L unchanged to machine precision of the bin center. Late IQR of k*L is identically zero (q25=q75=3π).
- **Not Nyquist.** D: N=48 and N=64 at fixed L=20 give the *same* k*L=3π. Nyquist would be πN = 150.80 vs 201.06. Far from both, as predicted for this k* definition.
- **H_grid (first allowed shell).** i*=1 at t=0 and at every later record, including the early focusing pulse (peak_max up to 24 at t≈0.2). After DC is dropped, argmax of a falling P(|k|) is the first bin. k* = 1.5·2π/L, so k*L = 3π independent of L, Λ, norm, and N.

No structure formed by T=8. The packet focuses briefly then **spreads** (late peak ~3e-4–3e-3, PR ~10³–10⁴, R_rms ~ L/2). Same qualitative late state as the A.3 mem re-exec (spread, no collapse). 16.3 is simply not realized on this unitary R5 point. T was not extended to chase it.

## Scoring against the written rules

Predictions file, “Scoring rules”:

- H_invar if A,B,C stay near 16.3 (not a mesh identity), D ≠ πN, and a finite-k peak exists. **Fail** (mesh identity 3π; no peak).
- H_mobile if A or B or C moves k*L by ≳ one shell and D is not Nyquist. **Fail** (Δ(k*L)=0).
- H_grid if k*L = πN **or** k*L = 2π(i+½) for a fixed i on B and C. **Hit:** i=1 fixed on A, B, C, and D; k*L = 2π(1+½) = 3π.
- MIXED if L looks invariant while Λ/norm move, or N tracks πN while B/C move, or no structure so 16.3 is not realized. The last clause is the *situation*, but the measured number is a grid identity, which the same file scores as H_grid. Not MIXED.

Proximity of 16.3 to 5π≈15.708 (shell i=2) is noted and is **not** what was measured.

## IC check (before integration; all passed)

Analytic peak for a unit-norm 3D Gaussian s=0.5: 1/(π s²)^{3/2} = 1.437. Window [1.40, 1.48].

| run | peak_ini | norm_ini | PR_ini | R_rms_ini |
|---|---:|---:|---:|---:|
| all norm=1 (N=64) | 1.43670 | 1 | 1.9687 | 0.61237 |
| C_norm0.5 | 0.71835 = ½×1.43670 | 0.5 | 1.9687 | 0.61237 |
| C_norm2.0 | 2.87339 = 2×1.43670 | 2 | 1.9687 | 0.61237 |
| D_N48 | 1.43669 | 1 | 1.9591 | 0.61236 |

R_rms_ini ≈ √(3/2)·s = 0.61237. Unitary: |norm_end − norm_ini| ~ 1e-12.

## Table — late-window (t ≥ 0.8 T = 6.4) medians

k*L = 9.424778 = 3π on every row. i* = 1 on every row. Late unique i* count = 1.

### A. L sweep (N=64, Λ=−8, norm=1)

| run | L | dx | k* | k*L | C | peak | PR | peaked? | falling? |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| A_L15 | 15 | 0.2344 | 0.62832 | **9.42478** | 0.9743 | 2.64e-3 | 1404 | no | yes |
| A_L20_baseline | 20 | 0.3125 | 0.47124 | **9.42478** | 0.9917 | 8.63e-4 | 3553 | no | yes |
| A_L25 | 25 | 0.3906 | 0.37699 | **9.42478** | 0.9966 | 4.01e-4 | 7692 | no | yes |

k* ∝ 1/L exactly (1.5 · 2π/L). Product is the bin, not a physical length × L.

### B. Λ sweep (L=20, N=64, norm=1)

| run | Λ | k* | k*L | C | peak | PR | peaked? |
|---|---:|---:|---:|---:|---:|---:|---|
| B_Lam-6 | −6 | 0.47124 | **9.42478** | 0.9898 | 6.88e-4 | 4531 | no |
| A_L20_baseline | −8 | 0.47124 | **9.42478** | 0.9917 | 8.63e-4 | 3553 | no |
| B_Lam-10 | −10 | 0.47124 | **9.42478** | 0.9858 | 6.28e-4 | 4447 | no |

Focusing strength changes the early pulse (peak_max 3.32 / 14.55 / 11.63) and not the late k*.

### C. initial-norm sweep (L=20, Λ=−8, N=64)

| run | norm | k* | k*L | C | peak | PR | peaked? |
|---|---:|---:|---:|---:|---:|---:|---|
| C_norm0.5 | 0.5 | 0.47124 | **9.42478** | 0.9928 | 4.22e-4 | 3463 | no |
| A_L20_baseline | 1.0 | 0.47124 | **9.42478** | 0.9917 | 8.63e-4 | 3553 | no |
| C_norm2.0 | 2.0 | 0.47124 | **9.42478** | 0.9679 | 2.92e-3 | 3396 | no |

Amplitude rescales the cubic and the memory source. k*L does not move.

### D. grid check (L=20, Λ=−8, norm=1)

| run | N | dx | k_Nyq | k*L_Nyq=πN | k* | k*L | i* |
|---|---:|---:|---:|---:|---:|---:|---:|
| D_N48 | 48 | 0.4167 | 7.540 | 150.80 | 0.47124 | **9.42478** | 1 |
| A_L20_baseline | 64 | 0.3125 | 10.053 | 201.06 | 0.47124 | **9.42478** | 1 |

dk = 2π/L is N-independent at fixed L, so a low-n lock does not track N. Nyquist is ruled out. This is the same k* as A/B/C, not Q01’s UV lock.

## What the field actually did

Every run: brief focusing (t≈0.12–0.52, peak_max from 0.87 at norm=0.5 up to 24.4 at L=15) then spread to a box-filling packet. Late R_rms is O(L/2). Memory (Σλ=1.5, ν=10) plus the cubic is enough to *prevent collapse* and not enough (or not the right family) to freeze a modulation at finite k. i* never left 1, even at peak_max. The radial spectrum is a falling envelope from DC, so after the k>2π/L cut the “peak” is the cutoff bin.

C as defined in §8.3 / R5-A2 is a poor crystal diagnostic on this IC: a unit-width-s=0.5 Gaussian already puts 99.5% of |Ψ̂|² above one box mode. Late C remaining high does **not** mean a lattice formed.

## Relation to the dossier float 16.3

- 16.3 is **not** Nyquist (201 at N=64).
- 16.3 is **close to shell i=2** (5π≈15.708). A different binning (integer n, voxel-argmax |k|, interpolated shell) could have landed near 16.3 on a falling spectrum that was scored one shell higher. That is a live *measurement* caveat, not evidence that 16.3 is physical.
- On this unitary R5 calibration, with the R5-A2 shell-mean definition, the number that is “constant across knobs” is **3π**, and it is constant because it is a bin. That is the opposite of a structural invariant.

Q01 (hot FDT, different Θ_core) locking at Nyquist is a different regime and was not reproduced here.

## What was not done

- No retune of Λ, λ, ν, s, T, or the IC to manufacture k*L=16.3.
- T was not extended past 8. Predictions: if structure exists it should already be visible; it is not.
- N was 64 (and 48), not spec 128. The lock is at the IR (first shell), so raising N would not move k*L under this definition.
- No FDT / Γ>0 arm. This is the unitary / cool R5 point.

## Paths

| what | path |
|---|---|
| predictions (before any step) | `/workspace/dossie_reexec/predictions_kstar.md` |
| analysis | `/workspace/dossie_reexec/kstar/analysis.md` |
| result | `/workspace/dossie_reexec/kstar/result.json` |
| runner | `/workspace/dossie_reexec/kstar/code/run_kstar.py` |
| launch | `/workspace/dossie_reexec/kstar/code/launch.py` |
| stepper (reused) | `/workspace/dossie_reexec/A3/code/stepper.py` |
| raw CSVs (8 unique) | `/workspace/dossie_reexec/kstar/raw/*_metrics.csv` |
| figures | `/workspace/dossie_reexec/kstar/figures/kL_vs_L.png`, `kL_vs_Lambda.png`, `kL_vs_norm.png` |
