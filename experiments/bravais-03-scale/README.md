**English** · [Português](README.pt-BR.md) · [Catalog / Catálogo](../README.md)

# Intrinsic scale

`bravais-03-scale` · bravais

**Does the spectral edge follow the system or the size of the box?**

Runs the same equation in boxes L=24, 32 and 48 at fixed dx=0.5, with grids of 48³, 64³ and 96³.

## Available material

The script is included; this snapshot contains no saved sweep output.


## Run

[Set up the environment](../../docs/en/getting-started.md), then run from the repository root.

```sh
MPLBACKEND=Agg python en/bravais/bravais_sweep_L.py
```

[English source](../../en/bravais/bravais_sweep_L.py) · [Código em português](../../bravais/bravais_sweep_L.py)

## Reading and continuation

The default is 800 steps per box; the `96³` box is the most demanding. `STEPS` changes the duration of a new run, not the recorded results. Initialization has no fixed seed. Outputs: `bravais_outputs_3d/sweep_L*.npz` and `sweep_verdict.png`.
