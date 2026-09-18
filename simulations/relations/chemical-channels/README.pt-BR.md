[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Relações](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Oito canais acoplados

**Como uma camada química contínua muda a relação?**

Acrescenta oito canais nomeados a partir de neurotransmissores, acoplados às dinâmicas de fase, aresta e memória.


## Auditoria da execução

**Contexto ou pós-processamento.** Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. Camadas opcionais de química/vida são escolhas do modelo, não ablações diretas de P1/P2/P3.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-entre-03-chemistry) · [simulate_neurotransmitters_between.py](code/en/simulate_neurotransmitters_between.py#L113)

## Material disponível

![Oito canais acoplados](results/figures/neurotransmissores-mudanca-no-entre.png)

- [neurotransmissores-mudanca-no-entre.png](results/figures/neurotransmissores-mudanca-no-entre.png)
- [neurotransmissores-mudanca-no-entre.gif](results/figures/neurotransmissores-mudanca-no-entre.gif)
- [neurotransmitters-between-data.json](results/data/neurotransmitters-between-data.json)
- [neurotransmissores-entre-dados.json](results/data/neurotransmissores-entre-dados.json)

## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
python simulations/relations/chemical-channels/code/pt-BR/simulate_neurotransmissores_entre.py
```

[English source](code/en/simulate_neurotransmitters_between.py) · [Código em português](code/pt-BR/simulate_neurotransmissores_entre.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

## Notas da implementação

Esses scripts relacionais evoluem fases e memória de arestas com RK4. As camadas opcionais de química e filtro de vida pertencem ao sistema relacional declarado. Seus seletores não devem ser descritos como termos nomeados da equação de campo completa da referência. [Fonte, linha 116](../observer/code/en/simulate_observer_observed_relations.py) · [Fonte deste estudo, linha 113](code/en/simulate_neurotransmitters_between.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
