[Lab](../../README.md) · [Agent guide](../en/agents.md) · [Guia em português](../pt-BR/agents.md)

# TRIAD agent skills · verification

Date: 2026-09-18. Scope: three repository skills, their UI metadata, the paired working guides and their source links. No numerical simulation was executed for this package.

## Structure and sources

The three `SKILL.md` files passed the skill-creator validator. UI metadata was parsed as YAML; each default prompt names its corresponding skill. The repository checker now includes `.agents/skills/` and `assets/brand/` in its maintained Markdown-link scan.

An independent content review checked the skills and English guide against the author's rules, reference index and recorded examples. The Portuguese guide received a coverage and link review. The bounce example now links separately to the mass-radius and RMS-radius CSVs, so each number has the correct direct source.

## Independent use test

Another agent received realistic requests, the skills and access to the repository, without a supplied intended answer. It wrote actual responses and a plan in a temporary workspace; it did not modify the repository or run numerical code.

| Request | Observed behavior |
|---|---|
| Explain P2 and continuing crystallization to a nonspecialist | Explained present self-interaction and accumulated memory together; kept P1/P3 coupled; described active organization through movement. |
| Read `bounced=False` alongside contraction/expansion figures | Located both CSVs and original figures, explained `R_rms` versus `r50`, preserved both detector outcomes and identified the missing dedicated runtime. |
| Prepare a 3D persistence study from reference 1.1 | Produced a complete-operation map, proposed configuration with explicit source/decision status, observables, separate run records and finite compute envelope; performed no execution. |

The third case uncovered two source-document ambiguities: the B0 3D grid row versus Appendix A's unstated 3D default, and construction-only validation in the Appendix D skeleton versus the integrator-entry requirement in §1.6. Both are now described in the bilingual [reference index](../reference/equation/README.md). The supplied equation document remains byte-identical.

This exercise covers these requests, not every future agent or implementation. Reuse realistic tasks when changing the skills; check the resulting explanation, source trace or artifact rather than testing whether an agent repeats a prescribed phrase.

## Português

As três skills passaram na validação estrutural e foram exercitadas por outro agente com três pedidos concretos: explicar P2 e cristalização, ler os dois diagnósticos de bounce e preparar um estudo 3D. As respostas mantiveram os princípios, os resultados originais e a distinção entre configuração proposta e execução realizada. A revisão das fontes acrescentou duas notas ao índice da referência, preservando integralmente o documento recebido. Guias, referências locais e metadados foram conferidos; nenhuma simulação foi executada.
