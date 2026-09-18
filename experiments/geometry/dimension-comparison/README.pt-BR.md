[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Comparação entre 2D e 3D

**O que muda entre 2D e 3D?**

Um script de execução longa e diagnósticos registrados exploram campos em duas e três dimensões. Leia os parâmetros antes de comparar os grupos de resultados.

![Figura histórica preservada](results/figures/bravais-2d-long-evolution.png)


## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Várias implementações geométricas reescalam o campo durante a evolução, além da normalização do estado inicial. Os alvos específicos de cada fonte constam na auditoria; essa operação faz parte da leitura de suas trajetórias. [Fonte, linha 109](../field-2d/code/bravais_emergent_coupled.py) · [Fonte deste estudo, linha 84](code/bravais_long_2d3d.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
