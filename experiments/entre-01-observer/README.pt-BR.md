[English](README.md) · **Português** · [Catalog / Catálogo](../README.pt-BR.md)

# Observador e observado

`entre-01-observer` · entre

**Como a direção de uma relação muda a dinâmica acoplada?**

Osciladores de fase com memória contínua nas arestas comparam relações unilaterais, mútuas, aninhadas e pareadas.

## Material disponível

![Observador e observado](../../entre/resultados/observador-observado-relacoes.png)

- [observador-observado-relacoes.png](../../entre/resultados/observador-observado-relacoes.png)
- [observador-observado-relacoes.gif](../../entre/resultados/observador-observado-relacoes.gif)
- [observer-observed-relations-data.json](../../en/entre/observer-observed-relations-data.json)
- [observador-observado-relacoes-dados.json](../../entre/dados/observador-observado-relacoes-dados.json)

## Executar

[Prepare o ambiente](../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
python entre/simulate_observer_observed_relations.py
```

[English source](../../en/entre/simulate_observer_observed_relations.py) · [Código em português](../../entre/simulate_observer_observed_relations.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.
