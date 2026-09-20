[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Memory](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Memory at small amplitude

An N96, seed-42 Gaussian run at the declared R5/FDT parameters; finite peaks in the recorded interval.

Imported historical record; this organization did not rerun the simulation.

[Read the original note](notes/original-record.md) · [Every file](FILES.md)

[Preserved runner](code/simulate_memory_small_amplitude.py) · [Dependencies and portability](../../../provenance/t-archive/dependencies.md)

![Original run figure](results/figures/overview.png)


## Execution audit

> **TRIAD identity: NOT complete TRIAD — documented departure.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-t-29) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-t-29) · [Español](../../../docs/es/triad-identity-audit.md#study-t-29) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-t-29) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-t-29) · [Norsk](../../../docs/no/triad-identity-audit.md#study-t-29) · [Dansk](../../../docs/da/triad-identity-audit.md#study-t-29) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-t-29)

**Implementation differs.** The run sets alpha=0 and uses two memory modes; its bath is active.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-t-29) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L2) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L27) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L189) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L213)

## Available material

10 files associated with this entry: 2 `.csv`, 1 `.json`, 1 `.md`, 6 `.png`.

[Timeline](../../../docs/en/topics/timeline.md) · [← 28](../../structures/3d-atom-trajectories/README.md) · [30 →](../../structures/two-atoms/README.md)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

The runner has `ALPHA=0` and two memory modes, with an active bath (`GAMMA=0.01`, `T_BATH=0.001`). The fractional branch is disabled in this implementation; its historical name does not override those declared values. [Source, line 2](code/simulate_memory_small_amplitude.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
