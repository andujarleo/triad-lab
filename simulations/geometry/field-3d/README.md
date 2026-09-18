[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Emergent 3D field

**What spatial and spectral structure emerges from the coupled evolution?**

Evolves a complex field on a periodic 3D grid, with FFTs, a coupled proposal and an implicit fixed point.


## Execution audit

**Implementation differs.** The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-bravais-01-field) · [bravais_puro_3d.py](code/pt-BR/bravais_puro_3d.py#L116) · [bravais_puro_3d.py](code/pt-BR/bravais_puro_3d.py#L241) · [bravais_puro_3d.py](variants/phase-checkpoints/code/bravais_puro_3d.py#L116) · [bravais_puro_3d.py](variants/phase-checkpoints/code/bravais_puro_3d.py#L241)

## Available material

![Emergent 3D field](results/figures/final-density-slices.png)

- [final-density-slices.png](results/figures/final-density-slices.png)
- [final_state.npz](results/data/final_state.npz)

## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
MPLBACKEND=Agg python simulations/geometry/field-3d/code/en/bravais_pure_3d.py
```

[English source](code/en/bravais_pure_3d.py) · [Código em português](code/pt-BR/bravais_puro_3d.py)

## Reading and continuation

Defaults are `N=64`, `L=32`, 1,200 steps and `dt=0.025`. Random initialization has no fixed seed. A new run will not recreate the included state exactly. New outputs go to `bravais_outputs_3d/` in the working directory.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

## Preserved implementations

- [Phase checkpoints](variants/phase-checkpoints/README.md)
- [Signed memory and a shorter default run](variants/signed-memory-short-run/README.md)

## Implementation notes

The geometric implementation uses field-dependent coefficients and a conditional numerical guard. In the inspected 3D source, squared norm above 100 is rescaled to 50, very small squared norm triggers random perturbation, and nonfinite values pass through `nan_to_num`. These are operations in the preserved code; static inspection alone does not show which were triggered in a saved run. [Source, line 116](code/pt-BR/bravais_puro_3d.py).

The archived geometric sources differ in their damping expression: the base 3D source uses a real negative factor, while the pure 2D and signed-memory variant use an imaginary factor in that position. These implementations and their outputs have not been rewritten to harmonize them. [Source, line 208](../field-2d/code/bravais_pure_emerge.py) · [This study’s source, line 241](code/pt-BR/bravais_puro_3d.py).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
