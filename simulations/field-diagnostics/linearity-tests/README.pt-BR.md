[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Diagnósticos do campo](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Testando a linearidade

Duas sementes comparam A, B e sua superposição sob um banho aditivo comum. O residual ponderado registrado inclui uma contribuição do banho que não se cancela; por isso, não isola a resposta não linear. O desvio de protocolo e a decisão histórica INCONCLUSIVE foram preservados.

Leia a sequência: protocolo → configuração → dados brutos → análise. As classificações abaixo pertencem ao registro histórico; não houve nova execução.

- [protocol.md](notes/protocol.md)
- [linearity-record.md](notes/linearity-record.md)
- [analysis.md](notes/analysis.md)
- [config.json](configuration/config.json)
- [result.json](results/data/result.json)

[Todos os arquivos](FILES.md) · [Dependências](../../../provenance/t-archive/dependencies.pt-BR.md)

![Diagnóstico original](results/figures/rlin-time.png)


## Auditoria da execução

> **Identidade TRIAD: TRIAD completa — termos conjuntos documentados.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-q04) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-q04) · [Español](../../../docs/es/triad-identity-audit.md#study-q04) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-q04) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-q04) · [Norsk](../../../docs/no/triad-identity-audit.md#study-q04) · [Dansk](../../../docs/da/triad-identity-audit.md#study-q04) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-q04)

**Termos conjuntos documentados.** A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. O residual de superposição inclui o banho aditivo comum; não mede somente a resposta não linear.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-q04) · [probe_field_linearity.py](code/probe_field_linearity.py#L54) · [probe_field_linearity.py](code/probe_field_linearity.py#L245) · [probe_field_linearity.py](code/probe_field_linearity.py#L263) · [probe_field_linearity.py](code/probe_field_linearity.py#L324)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O runner inspecionado mantém coeficientes instantâneo, fracionário, de memória e de banho não nulos, com três taxas de memória e `V_ext=0`. O veredito numérico registrado continua ligado à grade, ao passo temporal e ao diagnóstico declarados. Esta é uma inspeção estática, não uma nova execução. [Fonte, linha 34](../spatial-convergence/code/measure_spatial_convergence.py) · [Fonte deste estudo, linha 52](code/probe_field_linearity.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
