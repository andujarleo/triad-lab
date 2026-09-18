[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Structures](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# A pocket in the field

A Gaussian pocket is added at t=0.5 to an evolving coupled field. The record follows its identity and memory diagnostics after this declared input.

Imported historical record; this organization did not rerun the simulation.

[Read the original note](notes/original-record.md) · [Every file](FILES.md)

[Preserved runner](code/simulate_field_pocket.py) · [Dependencies and portability](../../../provenance/t-archive/dependencies.md)

![Original run figure](results/figures/PR-vs-t.png)


## Execution audit

**Coupled terms documented.** The supplied standalone update documents the coupled terms and three memory modes with FDT active. A declared Gaussian input is added at t=0.5; it is an input to the coupled field.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-t-37) · [simulate_field_pocket.py](code/simulate_field_pocket.py#L32) · [simulate_field_pocket.py](code/simulate_field_pocket.py#L143) · [simulate_field_pocket.py](code/simulate_field_pocket.py#L160) · [simulate_field_pocket.py](code/simulate_field_pocket.py#L301)

## Available material

5 files associated with this entry: 1 `.csv`, 1 `.json`, 1 `.md`, 2 `.png`.

[Timeline](../../../docs/en/topics/timeline.md) · [← 36](../../numerical-checks/reproduction-dossier/README.md) · [38 →](../two-pockets/README.md)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

Some archived protocols add an input during evolution: the pocket studies plant Gaussian fields at the declared time `T_PLANT=0.5`; the impact script applies a declared kick at the field peak. Read these as recorded interventions, not solely initial conditions or an automatic instance of post-result calibration. [Source, line 515](code/simulate_field_pocket.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
