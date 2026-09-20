[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Memória](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Memória e bounce

A mesma trajetória dá `bounced=False` pelo raio RMS e `bounced=True` pelo raio que contém metade da massa (r50). Esse raio cai de 3,487119 para 1,385641 em t=3,7 e depois sobe para 9,863062. O pico de densidade em t=4,1 antecede o pico de memória em t=4,2; a mudança de diagnóstico não é uma nova execução.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

Esta ficha remete às listagens e dependências do registro histórico; não há um script de execução dedicado associado a ela.

![Figura original do run](results/figures/overview.png)


## Em um minuto

O raio que contém metade da massa se contrai até o mínimo em **t=3,7** e depois se expande — enquanto outro raio não vê mínimo interior algum. A densidade atinge o pico em t=4,1; a memória segue em t=4,2. [Registro de auditoria](../../../docs/pt-BR/execution-audit.md#study-t-23) · [Veredito de identidade](../../../docs/pt-BR/triad-identity-audit.md#study-t-23)

## Auditoria da execução

> **Identidade TRIAD: NÃO estabelecido como TRIAD completa — rastreabilidade incompleta.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-t-23) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-t-23) · [Español](../../../docs/es/triad-identity-audit.md#study-t-23) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-t-23) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-t-23) · [Norsk](../../../docs/no/triad-identity-audit.md#study-t-23) · [Dansk](../../../docs/da/triad-identity-audit.md#study-t-23) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-t-23)

**Execução sem rastreabilidade completa.** Existem métricas de bounce e memória, mas a amplitude efetiva do banho e a fonte executada não estão completamente fixadas.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-t-23) · [original-record.md](notes/original-record.md#L10) · [summary.csv](results/data/summary.csv#L1)

## Material disponível

18 arquivos associados à ficha: 3 `.csv`, 1 `.gif`, 1 `.md`, 13 `.png`.

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 22](../../signals/refined-phase-to-density-diagnostic/README.pt-BR.md) · [24 →](../../geometry/bravais-template-map/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)
