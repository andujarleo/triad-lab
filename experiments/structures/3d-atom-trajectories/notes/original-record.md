---
tags: [triad, simulação, solver]
aliases: [triad_atoms_3d]
classe: solver real (triad-lang)
diretório: triad_atoms_3d
status: caos-eq
run: 28
data: 2026-08-20 noite
---

# triad_atoms_3d

Equação TRIAD **completa** (NLS + memória + FDT) a partir da mesma nuvem de **12 átomos gaussianos** do [27 triad_chaos_eq](../../twelve-atoms-full-field/notes/original-record.md). 1 gaussiana = 1 átomo. Caos de átomos → o que assentar. **Não é ablação.** Sem controle sem-memória, sem V_harmônico, sem fit de k\*L. [Memória](../../../../docs/reference/concepts/memory.md) · [FDT](../../../../docs/reference/concepts/fdt.md) · [Universo como simulação](../../../../docs/reference/concepts/universe-as-simulation.md)

A **grade já era 3D no 27** (N=32³, `memory_nls_strang_step_3d`). O 27 só publicou fatias xy do plano médio — por isso parecia 2D. O 28 é o mesmo tríade em **volume**: isosuperfície, centros 3D e trajetórias. N=40 (grade do PDF #23; dx=0.8, σ=1.2 é blob real).

## Por que kT muda (não esconder)

O 27 usou o default do solver `fdt_couple=True, kT=1`. Com Γ=0.05, dt=0.0025, `noise_amp = √(2Γ kT dt) ≈ 0.0158`, enquanto o pico dos 12 átomos era 0.008. Universo já preenchido em t=0.1 (norm 1→326→25585). Mesma família de preenchimento que o PDF #19.

A spec da `[[Equação de referência]]` §A.2 lista `T_bath = 0.001` para R5-FDT. Aqui **kT=0.001**, `fdt_couple=True`, Γ=0.05. É o banho FDT da spec para um átomo continuar átomo em 3D — **não** é calibração de k\*L, **não** isola FDT. Com kT=1 o preenchimento é imediato (ver 27); kT=0.001 deixa as 12 sementes visíveis em 3D no começo.

`noise_amplitude=0.0005` (32× menor que o 27). Pico IC=0.008545.

## IC — 12 átomos

A mesma receita `place_atoms` do 27: `n_atoms=12`, `sigma=1.2`, `min_sep=4.8` (=4σ), seed=0. Posições idênticas (caixa L=32): `ic_pair_sep_min=5.130282`, `ic_pair_sep_mean=15.910636`. Fases uniformes em [0, 2π). Superposição, norma total = 1. Sem chirp.

Detector: máximo local 3³ wrap, ρ ≥ 0.20·peak, NMS min_dist=2σ=2.4. No t=0: **n_det=12**, n_raw=12, ⟨NN⟩=8.922529.

CSV: [Artefatos/triad_atoms_3d/atoms_ic.csv](../results/data/atoms_ic.csv)

![Artefatos/triad_atoms_3d/01_atoms_3d_ic.png](../results/figures/atoms-3d-ic.png)

Isosuperfície t=0 (`skimage.measure.marching_cubes`, ρ=0.3·peak): **12 blobs distintos** na caixa [−L/2, L/2]³. Isto é o que o 27 não mostrou.

![Artefatos/triad_atoms_3d/02_isosurface_early.png](../results/figures/isosurface-early.png)

## Parâmetros (um conjunto legal)

Λ=−10, ν=(10, 0.5, 0.05), λ=(3, 1, 0.3), Γ=0.05, `fdt_couple=True`, **kT=0.001**. V_ext=None. L=32, N=40, dt=0.0025, T=12, record_every=40 (121 amostras). Backend: `triad.ntri` (numpy). Metal disponível (`metal_mlx` / `metal_native`) mas mlx não é drop-in para `memory_nls_strang_step_3d` com IC próprio — probe ~0.01 s, fallback numpy. Solver: `triad-lang` real, passo `memory_nls_strang_step_3d`.

Não substitui [27 triad_chaos_eq](../../twelve-atoms-full-field/notes/original-record.md) nem [23 triad_memory_bounce_bigbang](../../../memory/memory-and-bounce/notes/original-record.md).

## Resultado — trajetória

Wall: **449.406 s** (7 min 29 s; 21:37–21:45 BRT, 20/08/2026).

| | t=0 | t=0.1 | t=1.0 | t=6 (meio) | final (t=12) |
|---|---|---|---|---|---|
| n_átomos det. | 12 | 12 | 12 | 971 | 1007 |
| n_raw máx. local | 12 | 12 | 16 | 2165 | 2205 |
| norm | 1.0 | 1.315725 | 4.033214 | 15.430638 | 23.275045 |
| peak | 0.008545 | 0.008832 | 0.005561 | 0.005544 | 0.008089 |
| PR | 327.458 | 577.229 | 7696.253 | 16475.839 | 16362.984 |
| R_rms | 15.097761 | 15.3182 | 15.7820 | 15.9787 | 16.003210 |

Pico de densidade máximo=0.009249 em t=0.2. Vmem_peak máximo=0.025713 em t=0.3; Vmem_peak final=0.024431. r50 14.902349→15.758172; r80 18.744599→19.266551; r90 20.830747→20.938004. ⟨NN⟩ 8.922529→2.552239.

Os 12 átomos **permanecem 12 até t=1.0** (no 27 o universo já tinha preenchido em t=0.1). Em t=1.1 n_det=22; t=1.3 n_det=162. Depois o detector conta ~10³ máximos: o volume preenchido. Isosuperfície mid/late = universo no cubo, **não** ruído, **não** espuma-falha.

![Artefatos/triad_atoms_3d/03_isosurface_mid.png](../results/figures/isosurface-mid.png)

![Artefatos/triad_atoms_3d/04_isosurface_late.png](../results/figures/isosurface-late.png)

![Artefatos/triad_atoms_3d/05_atoms_3d_traj.png](../results/figures/atoms-3d-traj.png)

![Artefatos/triad_atoms_3d/00_montagem.png](../results/figures/overview.png)

## O que os números sustentam

Com kT=0.001 da spec §A.2 as 12 sementes são **visíveis como blobs 3D no t=0** e seguem distintas ~1 unidade de tempo. O equilíbrio (n_det 12→971→1007, norma 1→23.275045, R_rms→16) é o universo preenchendo o volume — mais lento que [27 triad_chaos_eq](../../twelve-atoms-full-field/notes/original-record.md), mesma leitura. Não é cubo de ruído. Este run **não** recalibrou FDT.

## CSVs

- [Artefatos/triad_atoms_3d/summary.csv](../results/data/summary.csv)
- [Artefatos/triad_atoms_3d/metrics.csv](../results/data/metrics.csv)
- [Artefatos/triad_atoms_3d/atoms_ic.csv](../results/data/atoms_ic.csv)
- [Artefatos/triad_atoms_3d/centers.csv](../results/data/centers.csv)

## Arquivos

`00_montagem.png` · `01_atoms_3d_ic.png` · `02_isosurface_early.png` · `03_isosurface_mid.png` · `04_isosurface_late.png` · `05_atoms_3d_traj.png` · `06_radii_peak.png` · `07_centers_3d.gif` + 4 CSVs + `summary.json`

Script: [Fontes/run_atoms_3d.py](../code/simulate_atom_trajectories.py)

→ [Índice de runs](../../../../docs/reference/records/indice-de-runs.md) · `[[TRIAD]]`
