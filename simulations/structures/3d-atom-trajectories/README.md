[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Structures](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# 3D atom trajectories

Centers and trajectories are saved at N=40, T=12 and kT=0.001, with final norm 23.275045. The preceding twelve-atom run used N=32, T=15 and kT=1; peak pruning also changed. Temperature is a changed physical input, alongside numerical and detector changes, so the contrast does not isolate one parameter.

Imported historical record; this organization did not rerun the simulation.

[Read the original note](notes/original-record.md) · [Every file](FILES.md)

[Preserved runner](code/simulate_atom_trajectories.py) · [Dependencies and portability](../../../provenance/t-archive/dependencies.md)

![Original run figure](results/figures/overview.png)


## Execution audit

**Execution not fully traceable.** The 3D trajectory runner retains three memory modes and a bath but imports the unbound historical runtime.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-t-28) · [simulate_atom_trajectories.py](code/simulate_atom_trajectories.py#L24) · [simulate_atom_trajectories.py](code/simulate_atom_trajectories.py#L328)

## Available material

14 files associated with this entry: 4 `.csv`, 1 `.gif`, 1 `.json`, 1 `.md`, 7 `.png`.

[Timeline](../../../docs/en/topics/timeline.md) · [← 27](../twelve-atoms-full-field/README.md) · [29 →](../../memory/memory-small-amplitude/README.md)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)
