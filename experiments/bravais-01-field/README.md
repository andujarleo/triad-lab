**English** · [Português](README.pt-BR.md) · [Catalog / Catálogo](../README.md)

# Emergent 3D field

`bravais-01-field` · bravais

**What spatial and spectral structure emerges from the coupled evolution?**

Evolves a complex field on a periodic 3D grid, with FFTs, a coupled proposal and an implicit fixed point.

## Available material

![Emergent 3D field](../../bravais/resultados/pure_final_slices.png)

- [pure_final_slices.png](../../bravais/resultados/pure_final_slices.png)
- [final_state.npz](../../bravais/final_state.npz)

## Run

[Set up the environment](../../docs/en/getting-started.md), then run from the repository root.

```sh
MPLBACKEND=Agg python en/bravais/bravais_pure_3d.py
```

[English source](../../en/bravais/bravais_pure_3d.py) · [Código em português](../../bravais/bravais_puro_3d.py)

## Reading and continuation

Defaults are `N=64`, `L=32`, 1,200 steps and `dt=0.025`. Random initialization has no fixed seed. A new run will not recreate the included state exactly. New outputs go to `bravais_outputs_3d/` in the working directory.
