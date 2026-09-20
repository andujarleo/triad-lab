[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Validação](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Dossiê de reexecução em dez partes

Dossiê histórico com refinamentos A3, QM1D, CHSH, sidebands, banho quente, histórico de tunelamento, k-star e Bravais. Inclui configurações reduzidas e comparações com termos desligados; os resultados registrados pertencem a essas condições declaradas.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

Esta ficha remete às listagens e dependências do registro histórico; não há um script de execução dedicado associado a ela.

![Figura original do run](results/memory-collapse-grid-64/figures/PR-vs-t.png)


## Auditoria da execução

> **Identidade TRIAD: NÃO é TRIAD completa — divergência documentada.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-t-36) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-t-36) · [Español](../../../docs/es/triad-identity-audit.md#study-t-36) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-t-36) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-t-36) · [Norsk](../../../docs/no/triad-identity-audit.md#study-t-36) · [Dansk](../../../docs/da/triad-identity-audit.md#study-t-36) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-t-36)

**Implementação divergente.** O dossiê mistura checagens numéricas/analíticas com comparações registradas de termos desligados, incluindo memória desligada, banho desligado e memória congelada.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-t-36) · [predictions-memory-collapse-grid-64.md](notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md#L10) · [analysis.md](notes/memory-collapse-grid-64/analysis.md#L1) · [predictions-bell-correlation-test.md](notes/predictions/predictions-bell-correlation-test.md#L10)

## Material disponível

122 arquivos associados à ficha: 56 `.csv`, 20 `.json`, 23 `.md`, 22 `.png`, 1 `.txt`.

### Estudos do dossiê

- [Memória e colapso · grade 64](notes/memory-collapse-grid-64/analysis.md)
- [Memória e colapso · grade 128](notes/memory-collapse-grid-128/analysis.md)
- [Memória e colapso · grade 160](notes/memory-collapse-grid-160/analysis.md)
- [Diagnósticos em uma dimensão](notes/one-dimensional-quantum-tests/analysis.md)
- [Correlações de Bell](notes/bell-correlation-test/analysis.md)
- [Memória e bandas espectrais laterais](notes/memory-and-spectral-sidebands/analysis.md)
- [Ruído térmico e colapso](notes/thermal-noise-and-collapse/analysis.md)
- [Barreira, memória e tunelamento](notes/barrier-memory-and-tunneling/analysis.md)
- [Escala espacial dominante](notes/dominant-spatial-scale/analysis.md)
- [Resposta do detector de redes](notes/lattice-detector-calibration/analysis.md)

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 35](../../structures/finite-peak-early-window/README.pt-BR.md) · [37 →](../../structures/a-pocket-in-the-field/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Este dossiê preserva configurações documentadas com `alpha=Gamma=f_FDT=0` e comparações que zeram os acoplamentos de memória. Esses protocolos históricos não são o método para novos experimentos TRIAD. Seus parâmetros, previsões, resultados registrados e vereditos permanecem intactos. [Fonte, linha 10](notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md).

Aqui, calibração do detector significa medir pontuações de templates diante de redes e cascas sintéticas. O relatório registra explicitamente que não houve reajuste dos coeficientes da equação. Esse uso de calibração deve ser distinguido de ajustar o campo para obter um resultado escolhido. [Fonte, linha 1](notes/lattice-detector-calibration/analysis.md).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
