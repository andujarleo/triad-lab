[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Explorações de campo 2D

**Como um campo se organiza em duas dimensões?**

Quatro implementações geométricas estão reunidas aqui: três usam campos 2D, enquanto o script de emergência acoplada usa um campo 1D. Cada uma mantém seus parâmetros e histórico de execução.

![Figura histórica preservada](results/figures/bravais-2d-emergent.png)



## Auditoria da execução

**Implementação divergente.** As implementações 1D/2D fornecidas incluem normalização durante a trajetória ou guards e divergem da evolução de referência; a expressão de dissipação do caso 2D puro atua como fase.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-field-2d) · [bravais_emergent_coupled.py](code/bravais_emergent_coupled.py#L109) · [bravais_pure_emerge.py](code/bravais_pure_emerge.py#L208)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Várias implementações geométricas reescalam o campo durante a evolução, além da normalização do estado inicial. Os alvos específicos de cada fonte constam na auditoria; essa operação faz parte da leitura de suas trajetórias. [Fonte, linha 109](code/bravais_emergent_coupled.py).

A implementação geométrica usa coeficientes dependentes do campo e uma contenção numérica condicional. Na fonte 3D inspecionada, norma ao quadrado acima de 100 é reescalada para 50, valores muito pequenos acionam perturbação aleatória e valores não finitos passam por `nan_to_num`. São operações do código preservado; a inspeção estática não identifica sozinha quais foram acionadas em uma execução salva. [Fonte, linha 116](../field-3d/code/pt-BR/bravais_puro_3d.py) · [Fonte deste estudo, linha 90](code/bravais_pure_emerge.py).

As fontes geométricas arquivadas diferem na expressão de dissipação: a fonte 3D base usa um fator real negativo; a pure 2D e a variante signed-memory usam um fator imaginário nessa posição. As implementações e suas saídas não foram reescritas para uniformizá-las. [Fonte, linha 208](code/bravais_pure_emerge.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
