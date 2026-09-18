---
tags: [triad, conceito]
aliases: [Bravais, rede, cristal]
---

# Rede Bravais

Três detectores distintos no registro. **Não** unificar os scores. **Não** chamar nenhum run de cristal BCC perfeito nem de rede Bravais perfeita.

## Score angular (R5 N48)

Famílias BCC / HCP / FCC / SC. Resultado: BCC=0.462544, HCP=0.393127, FCC=0.298510, SC=0.238946. BCC é o maior *deste* detector *neste* run. [17 triad_R5_reference_N48_full](../../../simulations/memory/memory-grid-48/notes/original-record.md)

## Templates recíprocos (pós-bounce)

FFT 3D da densidade, shell dominante, templates SC_axes, FCC_faces, BCC_body, HEX_basal, PLANAR_cross.

Finais: PLANAR_cross=0.221126, SC_axes=0.214925, HEX_basal=0.182180, FCC_faces=0.159688, BCC_body=0.124794. Melhor match: PLANAR_cross — outro detector, outro regime. [24 triad_bravais_map](../../../simulations/geometry/bravais-template-map/notes/original-record.md)

## Rede geométrica (nós = picos)

Picos de densidade → nós; arestas por kNN + radius_gate.

- v1, threshold 0.992, prune 3 células: **2 nós, 1 aresta**, a0=2.529822, grau médio=1. Threshold “severo demais”; preservado. [25 triad_bravais_network_map](../../../simulations/geometry/first-geometric-network/notes/original-record.md)
- v2, snapshot t=4.4, quantile=0.988, prune 2 células, kNN=6, radius_gate=7.643873: **39 nós, 25 arestas**, a0=4.931531, bond median=5.184593, grau médio=1.282051, grau máx=6. “Rede esparsa, com agrupamentos e conexões locais; não foi rotulada como rede Bravais perfeita.” [26 triad_bravais_network_map_v2](../../../simulations/geometry/refined-geometric-network/notes/original-record.md)

Voltar: [Anti-colapso](anti-collapse.md) · [Bounce](bounce.md)
