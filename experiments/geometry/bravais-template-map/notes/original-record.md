---
tags: [triad, simulação, pós-processamento]
aliases: [triad_bravais_map]
classe: Pós-processamento do run de bounce
diretório: triad_bravais_map
status: completo
run: 24
---

# triad_bravais_map

Pós-processamento de [23 triad_memory_bounce_bigbang](../../../memory/memory-and-bounce/notes/original-record.md) — sem reintegrar. FFT 3D da densidade, shell dominante, templates angulares. [Rede Bravais](../../../../docs/reference/concepts/bravais-lattice.md)

## Objetivo

Comparar distribuição angular com SC_axes, FCC_faces, BCC_body, HEX_basal, PLANAR_cross.

## Resultado preservado

Scores finais:

| family | final_score |
|---|---|
| PLANAR_cross | 0.2211261477294008 |
| SC_axes | 0.2149247312019548 |
| HEX_basal | 0.1821799060343812 |
| FCC_faces | 0.159688181177609 |
| BCC_body | 0.1247944072953121 |

Melhor match: PLANAR_cross. Diferente do R5 N48, onde BCC foi o maior noutro detector/regime ([17 triad_R5_reference_N48_full](../../../memory/memory-grid-48/notes/original-record.md)). Não unificar.

![Artefatos/triad_bravais_map/00_montagem.png](../results/figures/overview.png)

## CSVs

- [Artefatos/triad_bravais_map/bravais_final_scores.csv](../results/data/bravais_final_scores.csv)
- [Artefatos/triad_bravais_map/bravais_scores_over_time.csv](../results/data/bravais_scores_over_time.csv)

## Arquivos

`00_montagem.png` · `01_final_reciprocal_peaks.png` · `02_template_gallery.png` · `03_bravais_score_heatmap.png` · `04_best_family_over_time.png` · `05_pairwise_angle_comparison.png` · `06_realspace_vs_reciprocal.png` · `07_kstarL_over_time.png` · `08_summary.png` + 2 CSVs

→ [Índice de runs](../../../../docs/reference/records/indice-de-runs.md)
