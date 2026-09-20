[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Relações](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Memória e filtro de vida

**Histórias vividas diferentes podem produzir respostas distintas sob a mesma lei?**

Estende o controle químico com quatro horizontes de memória contínua e um vetor de filtro pessoal por entidade.


## Auditoria da execução

> **Identidade TRIAD: NÃO é execução TRIAD — contexto ou pós-processamento.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-entre-04-life-filter) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-entre-04-life-filter) · [Español](../../../docs/es/triad-identity-audit.md#study-entre-04-life-filter) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-entre-04-life-filter) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-entre-04-life-filter) · [Norsk](../../../docs/no/triad-identity-audit.md#study-entre-04-life-filter) · [Dansk](../../../docs/da/triad-identity-audit.md#study-entre-04-life-filter) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-entre-04-life-filter)

**Contexto ou pós-processamento.** Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. Camadas opcionais de química/vida são escolhas do modelo, não ablações diretas de P1/P2/P3.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-entre-04-life-filter) · [simulate_life_filter_between.py](code/en/simulate_life_filter_between.py#L139)

## Material disponível

![Memória e filtro de vida](results/figures/memoria-filtro-vida-mudanca.png)

- [memoria-filtro-vida-mudanca.png](results/figures/memoria-filtro-vida-mudanca.png)
- [memoria-filtro-vida-mudanca.gif](results/figures/memoria-filtro-vida-mudanca.gif)
- [life-filter-between-data.json](results/data/life-filter-between-data.json)
- [filtro-vida-entre-dados.json](results/data/filtro-vida-entre-dados.json)

## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
python simulations/relations/life-filter/code/pt-BR/simulate_filtro_vida_entre.py
```

[English source](code/en/simulate_life_filter_between.py) · [Código em português](code/pt-BR/simulate_filtro_vida_entre.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

## Notas da implementação

Esses scripts relacionais evoluem fases e memória de arestas com RK4. As camadas opcionais de química e filtro de vida pertencem ao sistema relacional declarado. Seus seletores não devem ser descritos como termos nomeados da equação de campo completa da referência. [Fonte, linha 116](../observer/code/en/simulate_observer_observed_relations.py) · [Fonte deste estudo, linha 139](code/en/simulate_life_filter_between.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
