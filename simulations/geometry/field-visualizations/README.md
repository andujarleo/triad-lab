[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Field movies and visual readouts

**What can a moving picture reveal about the field?**

A simulation script records field snapshots, and five readers/renderers turn saved data into movies and derived views. The supplied HTML embeds its data. Several readers require filmes_data.npz, which was not supplied.

![Phase vortices in denser regions](../visual-comparisons/results/figures/phase-vortices-final-frame.png)

**How to read it:** pink marks +2π phase winding; cyan marks −2π. The detector locates phase winding on the grid and the renderer selects denser regions. The points represent these crossings. The frame above retains its original labels; the animation follows the recorded snapshots with a rotating camera.

[Watch the original animation](results/figures/cordas-fase-vivas.gif) · [Inspect the renderer](code/cordas_fase_vivas.py)

The still image is shared with the visual-comparison study; the index retains its original association. The input `filmes_data.npz` was not supplied: the animation and code are preserved, but this renderer cannot be reproduced directly from the supplied files alone.



## Execution audit

**Implementation differs.** The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. This applies to simula_filmes; the other five files are readers/renderers.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-field-visualizations) · [simula_filmes.py](code/simula_filmes.py#L109) · [simula_filmes.py](code/simula_filmes.py#L234)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

The `som_e_luz.py` reader derives density, phase and spectral-band displays from saved snapshots. The separate `simula_filmes.py` script evolves a field and records snapshots. Preserve that distinction when presenting each image or movie. [Derived readouts](code/som_e_luz.py) · [Simulation and recording](code/simula_filmes.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
