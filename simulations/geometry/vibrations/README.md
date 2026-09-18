[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Strings and vibration

**How do field-derived curves change over time?**

One script evolves the field while recording strings and spectral modes; the other reconstructs motion from a saved final state. Their figures retain these distinct origins. Here, strings are curves extracted from the field.

![Preserved historical figure](results/figures/cordas-comprimento.png)



## Execution audit

**Implementation differs.** The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. The separate bravais_vibracoes reader is a kinematic reconstruction.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-vibrations) · [bravais_cordas_vibracoes.py](code/bravais_cordas_vibracoes.py#L93) · [bravais_cordas_vibracoes.py](code/bravais_cordas_vibracoes.py#L173)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

The vibration renderer reconstructs motion from a saved final state and selected spectral modes, using `omega=|k|²/2`. That rendered motion is post-processing, not another integration of the complete dynamics. [Source, line 5](code/bravais_vibracoes.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
