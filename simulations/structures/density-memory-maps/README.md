[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Structures](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Density–memory maps

Snapshots compare density, memory, residual and memory potential before and after a Gaussian input at t=0.5. The reported local alignment is transient; the record also compares it with the surrounding field.

Imported historical record; this organization did not rerun the simulation.

[Read the original note](notes/original-record.md) · [Every file](FILES.md)

[Preserved runner](code/simulate_density_memory_maps.py) · [Dependencies and portability](../../../provenance/t-archive/dependencies.md)

![Original run figure](results/figures/mapa-0p000.png)


## Execution audit

**Coupled terms documented.** The supplied standalone update documents the coupled terms and three memory modes with FDT active. The runner re-evolves the planted-pocket case and records density/memory maps; it is not only an image reader.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-t-39) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L11) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L43) · [simulate_density_memory_maps.py](code/simulate_density_memory_maps.py#L140)

## Available material

43 files associated with this entry: 1 `.csv`, 1 `.json`, 1 `.md`, 40 `.png`.

[Timeline](../../../docs/en/topics/timeline.md) · [← 38](../two-pockets/README.md)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

Some archived protocols add an input during evolution: the pocket studies plant Gaussian fields at the declared time `T_PLANT=0.5`; the impact script applies a declared kick at the field peak. Read these as recorded interventions, not solely initial conditions or an automatic instance of post-result calibration. [Source, line 515](../a-pocket-in-the-field/code/simulate_field_pocket.py) · [This study’s source, line 163](code/simulate_density_memory_maps.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
