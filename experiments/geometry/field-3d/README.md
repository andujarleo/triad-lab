[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md)

# Emergent 3D field

**What spatial and spectral structure emerges from the coupled evolution?**

Evolves a complex field on a periodic 3D grid, with FFTs, a coupled proposal and an implicit fixed point.

## Available material

![Emergent 3D field](results/figures/final-density-slices.png)

- [final-density-slices.png](results/figures/final-density-slices.png)
- [final_state.npz](results/data/final_state.npz)

## Run

[Set up the environment](../../../docs/en/getting-started.md), then run from the repository root.

```sh
MPLBACKEND=Agg python experiments/geometry/field-3d/code/en/bravais_pure_3d.py
```

[English source](code/en/bravais_pure_3d.py) · [Código em português](code/pt-BR/bravais_puro_3d.py)

## Reading and continuation

Defaults are `N=64`, `L=32`, 1,200 steps and `dt=0.025`. Random initialization has no fixed seed. A new run will not recreate the included state exactly. New outputs go to `bravais_outputs_3d/` in the working directory.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

## Preserved implementations

- [Phase checkpoints](variants/phase-checkpoints/README.md)
- [Signed memory and a shorter default run](variants/signed-memory-short-run/README.md)
