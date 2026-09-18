[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md)

# Field movies and visual readouts

**What can a moving picture reveal about the field?**

Six renderers and visual readouts turn field data into movies and views. The supplied HTML embeds its data. Several Python renderers require filmes_data.npz, which was not supplied.

![Phase vortices in denser regions](../visual-comparisons/results/figures/phase-vortices-final-frame.png)

**How to read it:** pink marks +2π phase winding; cyan marks −2π. The detector locates phase winding on the grid and the renderer selects denser regions. The points represent these crossings. The frame above retains its original labels; the animation follows the recorded snapshots with a rotating camera.

[Watch the original animation](results/figures/cordas-fase-vivas.gif) · [Inspect the renderer](code/cordas_fase_vivas.py)

The still image is shared with the visual-comparison study; the index retains its original association. The input `filmes_data.npz` was not supplied: the animation and code are preserved, but this renderer cannot be reproduced directly from the supplied files alone.


## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

This page organizes historical records. Code availability does not guarantee a complete execution environment. Paths embedded in source code were preserved; check dependencies before adapting a run.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)
