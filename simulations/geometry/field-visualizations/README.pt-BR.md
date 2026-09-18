[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Filmes e leituras visuais do campo

**O que uma imagem em movimento revela sobre o campo?**

Um script de simulação grava snapshots do campo, e cinco leitores/renderizadores transformam dados salvos em filmes e leituras derivadas. O HTML fornecido contém seus dados. Vários leitores precisam de filmes_data.npz, que não foi fornecido.

![Vórtices de fase em regiões densas](../visual-comparisons/results/figures/phase-vortices-final-frame.png)

**Como ler:** rosa marca voltas de fase de +2π; ciano, de −2π. O detector localiza voltas de fase na grade e o renderizador seleciona regiões densas. Os pontos são uma representação desses cruzamentos. O quadro acima mantém os rótulos originais; a animação acompanha os registros com uma câmera girando.

[Ver a animação original](results/figures/cordas-fase-vivas.gif) · [Examinar o renderizador](code/cordas_fase_vivas.py)

A imagem estática é compartilhada com o estudo de comparações visuais; o índice mantém sua associação original. O arquivo de entrada `filmes_data.npz` não veio no acervo: a animação e o código foram preservados, mas esse renderizador não pode ser reproduzido diretamente só com os arquivos fornecidos.



## Auditoria da execução

**Implementação divergente.** A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. Isso se aplica a simula_filmes; os outros cinco arquivos são leitores/renderizadores.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-field-visualizations) · [simula_filmes.py](code/simula_filmes.py#L109) · [simula_filmes.py](code/simula_filmes.py#L234)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O leitor `som_e_luz.py` deriva visualizações de densidade, fase e bandas espectrais de snapshots salvos. O script separado `simula_filmes.py` evolui um campo e grava snapshots. Preserve essa distinção ao apresentar cada imagem ou filme. [Leituras derivadas](code/som_e_luz.py) · [Simulação e gravação](code/simula_filmes.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
