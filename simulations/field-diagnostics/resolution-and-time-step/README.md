[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Field diagnostics](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Resolution and timestep

N96 and timestep refinements follow Q01. The record remains INCONCLUSIVE.

Read in order: protocol → configuration → raw data → analysis. These classifications belong to the historical record; no new run was performed.

- [protocol.md](notes/protocol.md)
- [refinement-record.md](notes/refinement-record.md)
- [analysis.md](notes/analysis.md)
- [config.json](configuration/config.json)
- [result.json](results/data/result.json)
- [seeds.txt](configuration/seeds.txt)

[Every file](FILES.md) · [Dependencies](../../../provenance/t-archive/dependencies.md)

![Original diagnostic](results/figures/overlay-observables.png)


## Execution audit

> **TRIAD identity: TRIAD complete — coupled terms documented.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-q01b) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-q01b) · [Español](../../../docs/es/triad-identity-audit.md#study-q01b) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-q01b) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-q01b) · [Norsk](../../../docs/no/triad-identity-audit.md#study-q01b) · [Dansk](../../../docs/da/triad-identity-audit.md#study-q01b) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-q01b)

**Coupled terms documented.** The supplied standalone update documents the coupled terms and three memory modes with FDT active. Spatial and time-step refinements retain the coupled terms; numerical convergence is unresolved.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-q01b) · [compare_grid_and_time_step.py](code/compare_grid_and_time_step.py#L38) · [compare_grid_and_time_step.py](code/compare_grid_and_time_step.py#L210) · [compare_grid_and_time_step.py](code/compare_grid_and_time_step.py#L180)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

The inspected runner retains nonzero instantaneous, fractional, memory and bath coefficients, with three memory rates and `V_ext=0`. Its recorded numerical verdict remains attached to its declared grid, timestep and diagnostic. This is static inspection, not a new execution. [Source, line 34](../spatial-convergence/code/measure_spatial_convergence.py) · [This study’s source, line 36](code/compare_grid_and_time_step.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
