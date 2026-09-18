[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Relations](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Observer and observed

**How does the direction of a relation change the coupled dynamics?**

Phase oscillators with continuous edge memory compare one-way, mutual, nested and paired relations.

## Available material

![Observer and observed](results/figures/observador-observado-relacoes.png)

- [observador-observado-relacoes.png](results/figures/observador-observado-relacoes.png)
- [observador-observado-relacoes.gif](results/figures/observador-observado-relacoes.gif)
- [observer-observed-relations-data.json](results/data/observer-observed-relations-data.json)
- [observador-observado-relacoes-dados.json](results/data/observador-observado-relacoes-dados.json)

## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
python simulations/relations/observer/code/en/simulate_observer_observed_relations.py
```

[English source](code/en/simulate_observer_observed_relations.py) · [Código em português](code/pt-BR/simulate_observer_observed_relations.py)

## Reading and continuation

The scripts use 6,000 steps and `DT=0.02`. New files go to `artifacts/` beside the script. Each included JSON contains 25 samples. Preserve the configuration and record a new run before comparing changes.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

## Implementation notes

These relational scripts evolve phases and edge memory with RK4. Optional chemistry and life-filter layers belong to their declared relational system. Their switches must not be described as named terms of the complete reference field equation. [Source, line 116](code/en/simulate_observer_observed_relations.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
