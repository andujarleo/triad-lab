[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Signals](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Responses to perturbations

**How does a field respond when its initial state is disturbed?**

Four recorded protocols explore coupling, small perturbations, impacts and rhythmic forcing. Each source retains the input, comparison and parameter choices used at the time.

![Preserved historical figure](results/figures/batida-numeros.png)


## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

Some archived protocols add an input during evolution: the pocket studies plant Gaussian fields at the declared time `T_PLANT=0.5`; the impact script applies a declared kick at the field peak. Read these as recorded interventions, not solely initial conditions or an automatic instance of post-result calibration. [Source, line 515](../../structures/a-pocket-in-the-field/code/simulate_field_pocket.py) · [This study’s source, line 290](code/teste_pancada.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
