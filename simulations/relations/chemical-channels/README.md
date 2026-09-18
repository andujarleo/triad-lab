[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Relations](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Eight coupled channels

**How does a continuous chemical layer change the relation?**

Adds eight channels named after neurotransmitters, coupled to phase, edge and memory dynamics.

## Available material

![Eight coupled channels](results/figures/neurotransmissores-mudanca-no-entre.png)

- [neurotransmissores-mudanca-no-entre.png](results/figures/neurotransmissores-mudanca-no-entre.png)
- [neurotransmissores-mudanca-no-entre.gif](results/figures/neurotransmissores-mudanca-no-entre.gif)
- [neurotransmitters-between-data.json](results/data/neurotransmitters-between-data.json)
- [neurotransmissores-entre-dados.json](results/data/neurotransmissores-entre-dados.json)

## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
python simulations/relations/chemical-channels/code/en/simulate_neurotransmitters_between.py
```

[English source](code/en/simulate_neurotransmitters_between.py) · [Código em português](code/pt-BR/simulate_neurotransmissores_entre.py)

## Reading and continuation

The scripts use 6,000 steps and `DT=0.02`. New files go to `artifacts/` beside the script. Each included JSON contains 25 samples. Preserve the configuration and record a new run before comparing changes.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

## Implementation notes

These relational scripts evolve phases and edge memory with RK4. Optional chemistry and life-filter layers belong to their declared relational system. Their switches must not be described as named terms of the complete reference field equation. [Source, line 116](../observer/code/en/simulate_observer_observed_relations.py) · [This study’s source, line 113](code/en/simulate_neurotransmitters_between.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
