[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Continuidade](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Rastreamento de efeitos causais

**Que efeitos permanecem depois que a fonte muda?**

O relatório original examina uma hipótese de “alma” por continuações determinísticas com duas memórias, sem dispersão fracionária nem termos de banho. A continuidade de campo também aparece nos controles; esse registro não isola um efeito exclusivo da vida. As entradas triad_rebuild_rules/run64 necessárias não foram fornecidas.

![Figura histórica preservada](results/figures/sombra-causal-longa.png)

- [causal-continuity-report.md](notes/causal-continuity-report.md)



## Auditoria da execução

> **Identidade TRIAD: NÃO é TRIAD completa — divergência documentada.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-causal-traces) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-causal-traces) · [Español](../../../docs/es/triad-identity-audit.md#study-causal-traces) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-causal-traces) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-causal-traces) · [Norsk](../../../docs/no/triad-identity-audit.md#study-causal-traces) · [Dansk](../../../docs/da/triad-identity-audit.md#study-causal-traces) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-causal-traces)

**Implementação divergente.** Quatro runners causais usam atualização determinística com duas memórias, sem termos fracionário/banho.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-causal-traces) · [soul_causal_probe_short.py](code/soul_causal_probe_short.py#L22) · [soul_causal_probe_short.py](code/soul_causal_probe_short.py#L47) · [soul_causal_probe_short.py](code/soul_causal_probe_short.py#L84) · [soul_background_matched.py](code/soul_background_matched.py#L32)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

[Contexto e diagnósticos](../../../docs/pt-BR/topics/causal-continuity.md)

## Notas da implementação

Os quatro scripts de continuação usam evolução cinética, interação instantânea e dois campos de memória. Os loops inspecionados omitem dispersão fracionária, dissipação e ruído. Os ramos comparados perturbam estados ou posições sob esse mesmo operador reduzido; o registro original permanece intacto. [Fonte, linha 22](code/soul_causal_probe_short.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
