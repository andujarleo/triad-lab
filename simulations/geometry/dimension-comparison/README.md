[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Comparing 2D and 3D

**What changes between 2D and 3D?**

A long-run script and recorded diagnostics explore fields in two and three dimensions. Read the script parameters before comparing the separate output groups.

![Preserved historical figure](results/figures/bravais-2d-long-evolution.png)



## Execution audit

> **TRIAD identity: NOT complete TRIAD — documented departure.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-dimension-comparison) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-dimension-comparison) · [Español](../../../docs/es/triad-identity-audit.md#study-dimension-comparison) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-dimension-comparison) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-dimension-comparison) · [Norsk](../../../docs/no/triad-identity-audit.md#study-dimension-comparison) · [Dansk](../../../docs/da/triad-identity-audit.md#study-dimension-comparison) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-dimension-comparison)

**Implementation differs.** Both dimension branches normalize the field every step (target norms 3.0 and 2.2) and use an update different from the reference.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-dimension-comparison) · [bravais_long_2d3d.py](code/bravais_long_2d3d.py#L84) · [bravais_long_2d3d.py](code/bravais_long_2d3d.py#L255)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

Several geometric implementations rescale the field during evolution, beyond normalization of the initial state. The source-specific targets are recorded in the audit; keep this operation visible when reading their trajectories. [Source, line 109](../field-2d/code/bravais_emergent_coupled.py) · [This study’s source, line 84](code/bravais_long_2d3d.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
