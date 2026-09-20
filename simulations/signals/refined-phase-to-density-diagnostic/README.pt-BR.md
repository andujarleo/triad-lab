[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Sinais](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Diagnóstico refinado de fase para densidade

A comparação refinada usa controle de ruído pareado e muda tanto o estímulo quanto a medida: epsilon passa de 0,07 para 0,15, a largura de 1,3 para 1,25 e a janela de observação de 1,8 para 5. Velocidades de chegada e RMS são leituras diagnósticas diferentes; devem ser lidas junto ao estimador anterior que falhou.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

Esta ficha remete às listagens e dependências do registro histórico; não há um script de execução dedicado associado a ela.

![Figura original do run](results/figures/overview.png)


## Auditoria da execução

> **Identidade TRIAD: NÃO estabelecido como TRIAD completa — rastreabilidade incompleta.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-t-22) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-t-22) · [Español](../../../docs/es/triad-identity-audit.md#study-t-22) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-t-22) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-t-22) · [Norsk](../../../docs/no/triad-identity-audit.md#study-t-22) · [Dansk](../../../docs/da/triad-identity-audit.md#study-t-22) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-t-22)

**Execução sem rastreabilidade completa.** O detector refinado muda o estímulo e a janela de observação; seu gerador está ausente.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-t-22) · [original-record.md](notes/original-record.md#L10) · [summary.csv](results/data/summary.csv#L1)

## Material disponível

11 arquivo associado à ficha: 1 `.csv`, 1 `.md`, 9 `.png`.

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 21](../first-phase-to-density-diagnostic/README.pt-BR.md) · [23 →](../../memory/memory-and-bounce/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)
