[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Diagnósticos do campo](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Um conjunto de condições iniciais

Ensemble MLX com as duas versões do protocolo preservadas. A decisão QM registrada é INCONCLUSIVE.

Leia a sequência: protocolo → configuração → dados brutos → análise. As classificações abaixo pertencem ao registro histórico; não houve nova execução.

- [protocol.md](notes/protocol.md)
- [protocol-revision-2.md](notes/protocol-revision-2.md)
- [ensemble-record.md](notes/ensemble-record.md)
- [analysis.md](notes/analysis.md)
- [config.json](configuration/config.json)
- [result.json](results/data/result.json)
- [seeds.txt](configuration/seeds.txt)

[Todos os arquivos](FILES.md) · [Dependências](../../../provenance/t-archive/dependencies.pt-BR.md)

![Diagnóstico original](results/figures/late-distributions.png)


## Auditoria da execução

> **Identidade TRIAD: TRIAD completa — termos conjuntos documentados.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-q02) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-q02) · [Español](../../../docs/es/triad-identity-audit.md#study-q02) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-q02) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-q02) · [Norsk](../../../docs/no/triad-identity-audit.md#study-q02) · [Dansk](../../../docs/da/triad-identity-audit.md#study-q02) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-q02)

**Termos conjuntos documentados.** A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. As 32 sementes registradas são finitas; o lote usa complex64/float32 e declara a mudança de precisão.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-q02) · [simulate_seed_ensemble.py](code/simulate_seed_ensemble.py#L45) · [simulate_seed_ensemble.py](code/simulate_seed_ensemble.py#L281) · [simulate_seed_ensemble.py](code/simulate_seed_ensemble.py#L242)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O runner inspecionado mantém coeficientes instantâneo, fracionário, de memória e de banho não nulos, com três taxas de memória e `V_ext=0`. O veredito numérico registrado continua ligado à grade, ao passo temporal e ao diagnóstico declarados. Esta é uma inspeção estática, não uma nova execução. [Fonte, linha 34](../spatial-convergence/code/measure_spatial_convergence.py) · [Fonte deste estudo, linha 43](code/simulate_seed_ensemble.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
