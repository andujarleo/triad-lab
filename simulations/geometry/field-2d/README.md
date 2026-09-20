[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# 2D field explorations

**How does a field organize itself in two dimensions?**

Four geometric implementations are grouped here: three use 2D fields, while the coupled-emergence script uses a 1D field. Each retains its own parameters and execution history.

![Preserved historical figure](results/figures/bravais-2d-emergent.png)



## Execution audit

> **TRIAD identity: NOT complete TRIAD — documented departure.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-field-2d) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-field-2d) · [Español](../../../docs/es/triad-identity-audit.md#study-field-2d) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-field-2d) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-field-2d) · [Norsk](../../../docs/no/triad-identity-audit.md#study-field-2d) · [Dansk](../../../docs/da/triad-identity-audit.md#study-field-2d) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-field-2d)

**Implementation differs.** The supplied 1D/2D implementations include trajectory normalization or guards and differ from the reference evolution; the pure 2D damping expression is phase-like.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-field-2d) · [bravais_emergent_coupled.py](code/bravais_emergent_coupled.py#L109) · [bravais_pure_emerge.py](code/bravais_pure_emerge.py#L208)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

Several geometric implementations rescale the field during evolution, beyond normalization of the initial state. The source-specific targets are recorded in the audit; keep this operation visible when reading their trajectories. [Source, line 109](code/bravais_emergent_coupled.py).

The geometric implementation uses field-dependent coefficients and a conditional numerical guard. In the inspected 3D source, squared norm above 100 is rescaled to 50, very small squared norm triggers random perturbation, and nonfinite values pass through `nan_to_num`. These are operations in the preserved code; static inspection alone does not show which were triggered in a saved run. [Source, line 116](../field-3d/code/pt-BR/bravais_puro_3d.py) · [This study’s source, line 90](code/bravais_pure_emerge.py).

The archived geometric sources differ in their damping expression: the base 3D source uses a real negative factor, while the pure 2D and signed-memory variant use an imaginary factor in that position. These implementations and their outputs have not been rewritten to harmonize them. [Source, line 208](code/bravais_pure_emerge.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
