[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Relações](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Observador e observado

**Como a direção de uma relação muda a dinâmica acoplada?**

Osciladores de fase com memória contínua nas arestas comparam relações unilaterais, mútuas, aninhadas e pareadas.


## Auditoria da execução

> **Identidade TRIAD: NÃO é execução TRIAD — contexto ou pós-processamento.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-entre-01-observer) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-entre-01-observer) · [Español](../../../docs/es/triad-identity-audit.md#study-entre-01-observer) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-entre-01-observer) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-entre-01-observer) · [Norsk](../../../docs/no/triad-identity-audit.md#study-entre-01-observer) · [Dansk](../../../docs/da/triad-identity-audit.md#study-entre-01-observer) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-entre-01-observer)

**Contexto ou pós-processamento.** Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-entre-01-observer) · [simulate_observer_observed_relations.py](code/en/simulate_observer_observed_relations.py#L116)

## Material disponível

![Observador e observado](results/figures/observador-observado-relacoes.png)

- [observador-observado-relacoes.png](results/figures/observador-observado-relacoes.png)
- [observador-observado-relacoes.gif](results/figures/observador-observado-relacoes.gif)
- [observer-observed-relations-data.json](results/data/observer-observed-relations-data.json)
- [observador-observado-relacoes-dados.json](results/data/observador-observado-relacoes-dados.json)

## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
python simulations/relations/observer/code/pt-BR/simulate_observer_observed_relations.py
```

[English source](code/en/simulate_observer_observed_relations.py) · [Código em português](code/pt-BR/simulate_observer_observed_relations.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

## Notas da implementação

Esses scripts relacionais evoluem fases e memória de arestas com RK4. As camadas opcionais de química e filtro de vida pertencem ao sistema relacional declarado. Seus seletores não devem ser descritos como termos nomeados da equação de campo completa da referência. [Fonte, linha 116](code/en/simulate_observer_observed_relations.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
