[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Diagnósticos do campo](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Modos e subespaços do campo

POD/PCA e DMD examinam janelas iniciais e tardias em quatro seeds. O registro não estabelece um atrator compartilhado de baixa dimensão.

Leia a sequência: protocolo → configuração → dados brutos → análise. As classificações abaixo pertencem ao registro histórico; não houve nova execução.

- [protocol.md](notes/protocol.md)
- [mode-analysis-record.md](notes/mode-analysis-record.md)
- [analysis.md](notes/analysis.md)
- [config.json](configuration/config.json)
- [result.json](results/data/result.json)

[Todos os arquivos](FILES.md) · [Dependências](../../../provenance/t-archive/dependencies.pt-BR.md)

![Diagnóstico original](results/figures/explained-variance-spectrum.png)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O runner inspecionado mantém coeficientes instantâneo, fracionário, de memória e de banho não nulos, com três taxas de memória e `V_ext=0`. O veredito numérico registrado continua ligado à grade, ao passo temporal e ao diagnóstico declarados. Esta é uma inspeção estática, não uma nova execução. [Fonte, linha 34](../spatial-convergence/code/measure_spatial_convergence.py) · [Fonte deste estudo, linha 50](code/analyze_field_modes.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
