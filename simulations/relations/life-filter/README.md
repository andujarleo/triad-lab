[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Relations](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Memory and life filter

**Can distinct experienced histories produce distinct responses under the same law?**

Extends the chemical control with four continuous memory horizons and a personal filter vector per entity.


## Execution audit

> **TRIAD identity: NOT a TRIAD execution — context or post-processing.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-entre-04-life-filter) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-entre-04-life-filter) · [Español](../../../docs/es/triad-identity-audit.md#study-entre-04-life-filter) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-entre-04-life-filter) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-entre-04-life-filter) · [Norsk](../../../docs/no/triad-identity-audit.md#study-entre-04-life-filter) · [Dansk](../../../docs/da/triad-identity-audit.md#study-entre-04-life-filter) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-entre-04-life-filter)

**Context or post-processing.** Finite-node phase/edge-memory model for conceptual relations, not an execution of the full field equation. Optional chemistry/life layers are model switches, not direct P1/P2/P3 ablations.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-entre-04-life-filter) · [simulate_life_filter_between.py](code/en/simulate_life_filter_between.py#L139)

## Available material

![Memory and life filter](results/figures/memoria-filtro-vida-mudanca.png)

- [memoria-filtro-vida-mudanca.png](results/figures/memoria-filtro-vida-mudanca.png)
- [memoria-filtro-vida-mudanca.gif](results/figures/memoria-filtro-vida-mudanca.gif)
- [life-filter-between-data.json](results/data/life-filter-between-data.json)
- [filtro-vida-entre-dados.json](results/data/filtro-vida-entre-dados.json)

## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
python simulations/relations/life-filter/code/en/simulate_life_filter_between.py
```

[English source](code/en/simulate_life_filter_between.py) · [Código em português](code/pt-BR/simulate_filtro_vida_entre.py)

## Reading and continuation

The scripts use 6,000 steps and `DT=0.02`. New files go to `artifacts/` beside the script. Each included JSON contains 25 samples. Preserve the configuration and record a new run before comparing changes.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

## Implementation notes

These relational scripts evolve phases and edge memory with RK4. Optional chemistry and life-filter layers belong to their declared relational system. Their switches must not be described as named terms of the complete reference field equation. [Source, line 116](../observer/code/en/simulate_observer_observed_relations.py) · [This study’s source, line 139](code/en/simulate_life_filter_between.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
