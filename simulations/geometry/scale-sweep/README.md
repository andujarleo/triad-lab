[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Intrinsic scale

**Does the spectral edge follow the system or the size of the box?**

Uses the same preserved implementation across boxes L=24, 32 and 48 at fixed dx=0.5, with grids of 48³, 64³ and 96³. Its kinetic and noise updates differ from the equation reference; this sweep compares that implementation across box sizes.


## Execution audit

**Implementation differs.** The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-bravais-03-scale) · [bravais_sweep_L.py](code/pt-BR/bravais_sweep_L.py#L92) · [bravais_sweep_L.py](code/pt-BR/bravais_sweep_L.py#L175)

## Available material

The original implementation and archived sweep outputs are included. See the complete file index below.


## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
MPLBACKEND=Agg python simulations/geometry/scale-sweep/code/en/bravais_sweep_L.py
```

[English source](code/en/bravais_sweep_L.py) · [Código em português](code/pt-BR/bravais_sweep_L.py)

## Reading and continuation

The default is 800 steps per box; the `96³` box is the most demanding. `STEPS` changes the duration of a new run, not the recorded results. Initialization has no fixed seed. Outputs: `bravais_outputs_3d/sweep_L*.npz` and `sweep_verdict.png`.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The archive adds two sweep-verdict figures with different contents. They retain their hashes and origins; they are not outputs from a new run of this script.
