[English](README.md) · **Português** · [Catalog / Catálogo](../README.pt-BR.md)

# Memória e filtro de vida

`entre-04-life-filter` · entre

**Histórias vividas diferentes podem produzir respostas distintas sob a mesma lei?**

Estende o controle químico com quatro horizontes de memória contínua e um vetor de filtro pessoal por entidade.

## Material disponível

![Memória e filtro de vida](../../entre/resultados/memoria-filtro-vida-mudanca.png)

- [memoria-filtro-vida-mudanca.png](../../entre/resultados/memoria-filtro-vida-mudanca.png)
- [memoria-filtro-vida-mudanca.gif](../../entre/resultados/memoria-filtro-vida-mudanca.gif)
- [life-filter-between-data.json](../../en/entre/life-filter-between-data.json)
- [filtro-vida-entre-dados.json](../../entre/dados/filtro-vida-entre-dados.json)

## Executar

[Prepare o ambiente](../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
python entre/simulate_filtro_vida_entre.py
```

[English source](../../en/entre/simulate_life_filter_between.py) · [Código em português](../../entre/simulate_filtro_vida_entre.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.
