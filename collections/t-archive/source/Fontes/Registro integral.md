---
tags: [triad, fonte]
aliases: [PDF, registro, integridade]
---

# Registro integral

Fonte primária deste vault: `TRIAD_registro_integral_simulacoes_2026-08-20.pdf` (82 MB, 88 pp.), na raiz do vault. Autor do PDF: ChatGPT via ReportLab. Data: 20/08/2026.

Objetivo do PDF (p. 1): preservar em ordem cronológica sucessos, falhas, tentativas vazias, diagnósticos depois refinados, números, imagens e brutos. **Nenhum resultado é substituído por um posterior.** Quando um diagnóstico foi corrigido, ambos aparecem.

## Três classes (não misturar)

| | classe | runs |
|---|---|---|
| (a) | ensaios exploratórios anteriores à especificação | #1–#13 |
| (b) | reproduções orientadas pela equação de referência | #14–#18 |
| (c) | runs que chamaram `solver.py` enviado | #19–#23 (+ pós-proc. #24–#26) |

Evita rebatizar os primeiros ensaios como se já fossem o solver final.

## Sem apagamento (p. 2)

- Phase-to-density bruto: velocidades ~0 por diagnóstico inadequado. [[21 triad_phase_to_density_speed]]
- Big Bang FDT quente: `mass_final=8773.747757`. [[19 triad_bigbang_solver_run]]
- Bounce: `R_rms` False e raios de massa True. [[23 triad_memory_bounce_bigbang]]
- Diretórios vazios: #6, #11, #14, #15 — cronologia.

## Como este vault se relaciona ao PDF

- Notas em `Simulações/` = uma por seção do PDF, com os números de lá / dos CSVs.
- `Artefatos/<dir>/` = anexos extraídos, prefixo `triad_*__` removido.
- [[solver.py]] e [[triad_equation_reference]] = anexos #2 e #111, sem edição.
- `Artefatos/conceitual/` = duas imagens **não** geradas pelo solver (p. 56):

![[Artefatos/conceitual/a_large_infographic_cosmic_simulation_montage_on_a.png]]

![[Artefatos/conceitual/evolução_cósmica_da_singularidade_à_teia_cósmica.png]]

Apêndice do PDF: CSVs reimpressos + SHA-256 de cada anexo. Resultados integrados (p. 57) são índice cruzado — não substituem as seções.

Backend dos runs (c): [[Backend e unidades]].

Voltar: [[TRIAD]] · [[Índice de runs]]
