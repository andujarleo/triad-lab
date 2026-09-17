**English** · [Português](README.pt-BR.md) · [Catalog / Catálogo](../README.md)

# Eight coupled channels

`entre-03-chemistry` · entre

**How does a continuous chemical layer change the relation?**

Adds eight channels named after neurotransmitters, coupled to phase, edge and memory dynamics.

## Available material

![Eight coupled channels](../../entre/resultados/neurotransmissores-mudanca-no-entre.png)

- [neurotransmissores-mudanca-no-entre.png](../../entre/resultados/neurotransmissores-mudanca-no-entre.png)
- [neurotransmissores-mudanca-no-entre.gif](../../entre/resultados/neurotransmissores-mudanca-no-entre.gif)
- [neurotransmitters-between-data.json](../../en/entre/neurotransmitters-between-data.json)
- [neurotransmissores-entre-dados.json](../../entre/dados/neurotransmissores-entre-dados.json)

## Run

[Set up the environment](../../docs/en/getting-started.md), then run from the repository root.

```sh
python en/entre/simulate_neurotransmitters_between.py
```

[English source](../../en/entre/simulate_neurotransmitters_between.py) · [Código em português](../../entre/simulate_neurotransmissores_entre.py)

## Reading and continuation

The scripts use 6,000 steps and `DT=0.02`. New files go to `artifacts/` beside the script. Each included JSON contains 25 samples. Preserve the configuration and record a new run before comparing changes.
