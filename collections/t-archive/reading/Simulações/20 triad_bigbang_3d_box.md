> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/20%20triad_bigbang_3d_box.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, solver]
aliases: [triad_bigbang_3d_box]
classe: solver.py real via backend NumPy shim
diretório: triad_bigbang_3d_box
status: completo
run: 20
```


# triad_bigbang_3d_box

Resposta ao FDT quente de [19 triad_bigbang_solver_run](19%20triad_bigbang_solver_run.md). Grid 44³, L=32, dt=0.0025, T=10; FDT muito frio. `[[Solver]]` via shim. [FDT](../Conceitos/FDT.md)

## Objetivo

Densidade, nós, memória, expansão. Procurar teia — o registro diz que **não** apareceu teia filamentar clara.

## Resultado preservado

norm 1.0 → 1.413637.

| | inicial | mín | máx | final |
|---|---|---|---|---|
| peak | 0.910133 | 0.0004179 | 2.066449 | 0.0005468 |
| Rrms | 0.693459 | | 14.317529 | 14.317529 |
| PR | 2.449071 | | 16780.038 | 16489.834125 |

`memory_mean_final≈6.6e-5` (CSV: 6.58337145e-05). Expansão/anti-colapso visível; sem teia cósmica clara.

![Artefatos/triad_bigbang_3d_box/00_montagem.png](../../source/Artefatos/triad_bigbang_3d_box/00_montagem.png)

GIF 434 KB: ![Artefatos/triad_bigbang_3d_box/06_bigbang_3d_box_animation.gif](../../source/Artefatos/triad_bigbang_3d_box/06_bigbang_3d_box_animation.gif)

## CSVs

- [Artefatos/triad_bigbang_3d_box/summary.csv](../../source/Artefatos/triad_bigbang_3d_box/summary.csv)
- [Artefatos/triad_bigbang_3d_box/metrics.csv](../../source/Artefatos/triad_bigbang_3d_box/metrics.csv)

## Arquivos

`00_montagem.png` · `01_bigbang_3d_box_timeline.png` · `02_density_nodes_3d_timeline.png` · `03_memory_3d_timeline.png` · `04_expansion_observables.png` · `05_peak_memory.png` · `06_bigbang_3d_box_animation.gif` · `07_final_3d_box.png` + 2 CSVs

→ [Anti-colapso](../Conceitos/Anti-colapso.md) · [Índice de runs](%C3%8Dndice%20de%20runs.md)
