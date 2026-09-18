> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/27%20triad_chaos_eq.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, solver]
aliases: [triad_chaos_eq]
classe: solver real (triad-lang)
diretório: triad_chaos_eq
status: caos-eq
run: 27
data: 2026-08-20 noite
```


# triad_chaos_eq

Equação TRIAD **completa** (NLS + memória + FDT) a partir de uma nuvem de **12 átomos gaussianos**. 1 gaussiana = 1 átomo. Caos de átomos → o que assentar. **Não é ablação.** Sem controle sem-memória, sem V_harmônico de comparação, sem fit de k\*L. [Bounce](../Conceitos/Bounce.md) · [FDT](../Conceitos/FDT.md) · [Memória](../Conceitos/Mem%C3%B3ria.md)

N=32 (reduzido vs #23 N=40). Solver: `triad-lang` real, passo `memory_nls_strang_step_3d` (o mesmo Strang de `integrate_3d`). Backend: `triad.ntri` (numpy). Metal disponível (`metal_mlx` / `metal_native`) mas não usado — o loop de diagnóstico precisa de ψ e y a cada amostra.

## IC — 12 átomos

Decisão única, sem scan: `n_atoms=12`, `sigma=1.2`, `min_sep=4.8` (=4σ), seed=0. Posições aleatórias com imagem mínima periódica; fases uniformes em [0, 2π). Superposição, depois norma total = 1. Sem chirp.

Colocação (seed=0): `ic_pair_sep_min=5.130282`, `ic_pair_sep_mean=15.910636`. Detector no t=0 (máximo local 3³ wrap, ρ ≥ 0.20·peak): **n_det=12**, ⟨NN⟩=8.857611, NN mediana=9.103059.

CSV: [Artefatos/triad_chaos_eq/atoms_ic.csv](../../source/Artefatos/triad_chaos_eq/atoms_ic.csv)

## Parâmetros (um conjunto legal)

Λ=−10, ν=(10, 0.5, 0.05), λ=(3, 1, 0.3), Γ=0.05, `fdt_couple=True`, kT=1 (default do solver atual). V_ext=None. L=32, dt=0.0025, T=15, record_every=40 (151 amostras). `noise_amplitude=0.015811388300841896` (f_FDT_e = 2Γ dx³ kT/ℏ com dx=1).

Não é o IC de #23 (uma gaussiana larga σ=3.2 + chirp). Não substitui [23 triad_memory_bounce_bigbang](23%20triad_memory_bounce_bigbang.md).

## Resultado

Wall: **14.124 s** (21:22 BRT, 20/08/2026).

| | t=0 | t=0.1 | final (t=15) |
|---|---|---|---|
| n_átomos det. | 12 | 1147 | 1238 |
| norm | 1.0 | 325.919474 | 25585.351298 |
| peak | 0.008360 | 0.109185 | 2.234612 |
| PR | 327.812738 | 16375.159336 | 28851.932841 |
| R_rms | 15.102938 | 16.049892 | 16.023042 |
| r50 | 14.899664 | 15.779734 | 15.748016 |
| r80 | 18.814888 | 19.287302 | 19.261360 |
| r90 | 20.808652 | 21.0 | 20.928450 |
| ⟨NN⟩ | 8.857611 | 2.287253 | 2.249534 |

Pico de densidade máximo=3.506253 em t=10.6. Vmem_peak máximo=9.386298 em t=4.7; Vmem_peak final=5.141332.

Janela late (t≥12): R_rms mean=16.008579 std=0.040049; peak mean=2.175297 std=0.142540; PR mean=28326.900033 std=394.774018; n_det mean=1204.0 std=23.043; cryst (FFT de ρ, k>2π/L) mean=0.133015 std=0.010882.

Planos xy: em t=0 a fatia z=0 mostra as 12 sementes. De t≈0.1 em diante o volume preenche. O detector passa a contar ~10³ máximos locais — isso **não** é ruído de grade. É o universo emergindo das sementes. Os 12 átomos não “morrem”: deixam de ser o estado inteiro.

Mesma família de [19 triad_bigbang_solver_run](19%20triad_bigbang_solver_run.md) (FDT quente; lá mass_final=8773.747757). Aqui o default `fdt_couple=True` com dx=1 injeta massa ~O(1) por passo; norma 1→25585.351298. #23 no mesmo Λ,ν,λ,Γ teve norma 1→1.491662 (N=40, IC diferente, FDT efetivo não registrado na nota). Este run **não** recalibrou FDT.

![Artefatos/triad_chaos_eq/00_montagem.png](../../source/Artefatos/triad_chaos_eq/00_montagem.png)

## O que os números sustentam

Com o FDT default em N=32, as 12 sementes deixam de ser o estado inteiro em Δt=0.1. O que assenta é o volume preenchido (R_rms~16, n_det~1200). Leitura: **caos → universo**, não “átomos falharam no ruído”. Mesma família de preenchimento que [19 triad_bigbang_solver_run](19%20triad_bigbang_solver_run.md).

## CSVs

- [Artefatos/triad_chaos_eq/summary.csv](../../source/Artefatos/triad_chaos_eq/summary.csv)
- [Artefatos/triad_chaos_eq/metrics.csv](../../source/Artefatos/triad_chaos_eq/metrics.csv)
- [Artefatos/triad_chaos_eq/atoms_ic.csv](../../source/Artefatos/triad_chaos_eq/atoms_ic.csv)

## Arquivos

`00_montagem.png` · `01_radii_vs_t.png` · `02_peak_vs_t.png` · `03_atoms_count_spacing.png` · `04_midplane_snapshots.png` · `05_norm_pr_vmem.png` + 3 CSVs + `summary.json`

Script: [Fontes/run_chaos_eq.py](../../source/Fontes/run_chaos_eq.py)

Não rodados (método corrigido antes): 27b nomem, 27c harmônico, IC `init='chaos'` (campo aleatório).

→ [Índice de runs](%C3%8Dndice%20de%20runs.md) · `[[TRIAD]]`
