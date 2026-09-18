---
tags: [triad, simulação, referência]
aliases: [triad_R5_reference_N40, R5 N40]
classe: Equação de referência
diretório: triad_R5_reference_N40
status: completo
run: 16
---

# triad_R5_reference_N40

Regime R5 da [[Equação de referência]]. N=40 em vez de N=128 (custo CPU). Full vs no-memory. Classe (b). Conceito: [[Anti-colapso]] · [[Memória]].

## Objetivo

norm, peak, PR, k\*L, crystallinity. Comparar memória ligada e desligada.

## Resultado preservado

Full: `norm_final=1.0`; `peak_max=1.651207`; `peak_final=0.0006409`; `PR_final=4720.477435`; `k*L late mean=9.424778`; `crystallinity late mean=0.972743`.

No-memory: `peak_max=4.170131`; `peak_final=3.889202`; `PR_final=0.528063`.

`k*L` difere da referência ~16.3 — compatível com resolução reduzida. **Não corrigido nem recalibrado.**

t ∈ [0, 15], dx=0.5. kstar full constante 0.471239 no CSV (k\*L = kstar·L = 9.424778 com L=20 se dx·N=0.5·40).

![[Artefatos/triad_R5_reference_N40/00_montagem.png]]

## CSVs

- [[Artefatos/triad_R5_reference_N40/summary.csv]]
- [[Artefatos/triad_R5_reference_N40/R5_full_metrics.csv]]
- [[Artefatos/triad_R5_reference_N40/R5_no_memory_metrics.csv]]

## Arquivos

`00_montagem.png` · `01_peak.png` · `02_PR.png` · `03_kstarL.png` · `04_cryst.png` · `05_spectra.png` · `06_slices.png` · `07_fourier.png` · `08_summary.png` + 3 CSVs

→ [[17 triad_R5_reference_N48_full]] · [[18 triad_visual_atlas]]
