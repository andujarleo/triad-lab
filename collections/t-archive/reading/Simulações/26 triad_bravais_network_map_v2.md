> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/26%20triad_bravais_network_map_v2.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, pós-processamento]
aliases: [triad_bravais_network_map_v2]
classe: Pós-processamento geométrico
diretório: triad_bravais_network_map_v2
status: completo
run: 26
```


# triad_bravais_network_map_v2

Rede refinada após [25 triad_bravais_network_map](25%20triad_bravais_network_map.md). Snapshot automático “mais estruturado”. [Rede Bravais](../Conceitos/Rede%20Bravais.md)

## Objetivo

quantile=0.988; distância mín=2 células; kNN=6; radius_gate=7.643873.

## Resultado preservado

Snapshot **t=4.4**: nodes=39, edges=25, candidate_spacing_a0=4.931531, median_bond_length=5.184593, mean_degree=1.282051, max_degree=6.

PDF: “A rede é esparsa, com agrupamentos e conexões locais; **não foi rotulada como rede Bravais perfeita.**”

![Artefatos/triad_bravais_network_map_v2/00_montagem.png](../../source/Artefatos/triad_bravais_network_map_v2/00_montagem.png)

## CSVs

- [Artefatos/triad_bravais_network_map_v2/summary.csv](../../source/Artefatos/triad_bravais_network_map_v2/summary.csv)
- [Artefatos/triad_bravais_network_map_v2/nodes.csv](../../source/Artefatos/triad_bravais_network_map_v2/nodes.csv)
- [Artefatos/triad_bravais_network_map_v2/edges.csv](../../source/Artefatos/triad_bravais_network_map_v2/edges.csv)

## Arquivos

`00_montagem.png` · `01_nodes_3d.png` · `02_network_3d.png` · `03_network_xy_projection.png` · `04_nearest_neighbor_histogram.png` · `05_bond_length_histogram.png` · `06_bond_directions.png` · `07_degree_histogram.png` · `08_adjacency_matrix.png` · `09_summary.png` + 3 CSVs

→ [23 triad_memory_bounce_bigbang](23%20triad_memory_bounce_bigbang.md) · [24 triad_bravais_map](24%20triad_bravais_map.md) · `[[TRIAD]]`
