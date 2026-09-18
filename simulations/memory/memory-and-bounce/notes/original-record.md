---
tags: [triad, simulação, solver]
aliases: [triad_memory_bounce_bigbang]
classe: solver.py real via backend NumPy shim
diretório: triad_memory_bounce_bigbang
status: completo
run: 23
---

# triad_memory_bounce_bigbang

Contração → bounce de memória → expansão. **Nenhum termo explícito de bounce.** [Bounce](../../../../docs/reference/concepts/bounce.md) · [Memória](../../../../docs/reference/concepts/memory.md) · `[[Solver]]`

## Objetivo

Gaussiana larga + chirp quadrático radial para dentro. Λ=−10, ν=(10, 0.5, 0.05), λ=(3, 1, 0.3), 40³, T=12, L=32, dt=0.0025, `initial_sigma=3.2`, `inward_chirp=0.22`.

## Resultado preservado — dois diagnósticos

**R_rms:** mínimo em t=0 (`R_min=R_initial=3.919184`); `bounced=False`; `R_final=12.272371`. PDF: densidade FDT fraca no volume distante infla R_rms.

**Raios de massa** (mesma trajetória):

| | inicial | mín | t_mín | final | refined_bounce |
|---|---|---|---|---|---|
| r50 | 3.487119 | 1.385641 | 3.7 | 9.863062 | True |
| r80 | 4.866210 | 2.884441 | 3.1 | 16.511814 | True |
| r90 | 5.656854 | 5.059644 | 1.3 | 19.0662 | True |

Pico densidade t=4.1; pico memória t=4.2; delay=0.1.

Norma 1→1.491662. peak_density max=0.149575, final=0.001110. PR 516.083→8306.608. Vmem_peak max=0.520074. overlap max=0.999909, final=0.923178.

![Artefatos/triad_memory_bounce_bigbang/00_montagem.png](../results/figures/overview.png)

GIF 5.50 MB (abaixo de 10 MB): ![Artefatos/triad_memory_bounce_bigbang/09_memory_bounce_animation.gif](../results/figures/memory-bounce-animation.gif)

## CSVs

- [Artefatos/triad_memory_bounce_bigbang/summary.csv](../results/data/summary.csv)
- [Artefatos/triad_memory_bounce_bigbang/refined_bounce_summary.csv](../results/data/refined_bounce_summary.csv)
- [Artefatos/triad_memory_bounce_bigbang/metrics.csv](../results/data/metrics.csv)

## Arquivos

`00_montagem.png` · `01_bounce_timeline_xy.png` … `08_radial_spacetime_memory.png` · `09_memory_bounce_animation.gif` · `10_summary.png` · `11_mass_enclosing_radii.png` · `12_central_mass.png` · `13_core_vs_peak.png` + 3 CSVs

Pós-proc: [24 triad_bravais_map](../../../geometry/bravais-template-map/notes/original-record.md) · [25 triad_bravais_network_map](../../../geometry/first-geometric-network/notes/original-record.md) · [26 triad_bravais_network_map_v2](../../../geometry/refined-geometric-network/notes/original-record.md)
