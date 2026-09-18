[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md)

# Intrinsic scale

**Does the spectral edge follow the system or the size of the box?**

Runs the same equation in boxes L=24, 32 and 48 at fixed dx=0.5, with grids of 48³, 64³ and 96³.

## Available material

The original implementation and archived sweep outputs are included. See the complete file index below.


## Run

[Set up the environment](../../../docs/en/getting-started.md), then run from the repository root.

```sh
MPLBACKEND=Agg python experiments/geometry/scale-sweep/code/en/bravais_sweep_L.py
```

[English source](code/en/bravais_sweep_L.py) · [Código em português](code/pt-BR/bravais_sweep_L.py)

## Reading and continuation

The default is 800 steps per box; the `96³` box is the most demanding. `STEPS` changes the duration of a new run, not the recorded results. Initialization has no fixed seed. Outputs: `bravais_outputs_3d/sweep_L*.npz` and `sweep_verdict.png`.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The archive adds two sweep-verdict figures with different contents. They retain their hashes and origins; they are not outputs from a new run of this script.
