[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Relations](../README.md) · [Glossary](../../../docs/en/glossary.md)

# Eight coupled channels

**How does a continuous chemical layer change the relation?**

Adds eight channels named after neurotransmitters, coupled to phase, edge and memory dynamics.

## Available material

![Eight coupled channels](results/figures/neurotransmissores-mudanca-no-entre.png)

- [neurotransmissores-mudanca-no-entre.png](results/figures/neurotransmissores-mudanca-no-entre.png)
- [neurotransmissores-mudanca-no-entre.gif](results/figures/neurotransmissores-mudanca-no-entre.gif)
- [neurotransmitters-between-data.json](results/data/neurotransmitters-between-data.json)
- [neurotransmissores-entre-dados.json](results/data/neurotransmissores-entre-dados.json)

## Run

[Set up the environment](../../../docs/en/getting-started.md), then run from the repository root.

```sh
python experiments/relations/chemical-channels/code/en/simulate_neurotransmitters_between.py
```

[English source](code/en/simulate_neurotransmitters_between.py) · [Código em português](code/pt-BR/simulate_neurotransmissores_entre.py)

## Reading and continuation

The scripts use 6,000 steps and `DT=0.02`. New files go to `artifacts/` beside the script. Each included JSON contains 25 samples. Preserve the configuration and record a new run before comparing changes.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)
