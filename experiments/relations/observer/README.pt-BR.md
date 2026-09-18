[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Relações](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md)

# Observador e observado

**Como a direção de uma relação muda a dinâmica acoplada?**

Osciladores de fase com memória contínua nas arestas comparam relações unilaterais, mútuas, aninhadas e pareadas.

## Material disponível

![Observador e observado](results/figures/observador-observado-relacoes.png)

- [observador-observado-relacoes.png](results/figures/observador-observado-relacoes.png)
- [observador-observado-relacoes.gif](results/figures/observador-observado-relacoes.gif)
- [observer-observed-relations-data.json](results/data/observer-observed-relations-data.json)
- [observador-observado-relacoes-dados.json](results/data/observador-observado-relacoes-dados.json)

## Executar

[Prepare o ambiente](../../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
python experiments/relations/observer/code/pt-BR/simulate_observer_observed_relations.py
```

[English source](code/en/simulate_observer_observed_relations.py) · [Código em português](code/pt-BR/simulate_observer_observed_relations.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)
