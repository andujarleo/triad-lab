[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Strings from a saved state

**How can density, phase and spectral modes be inspected as strings?**

Post-processes a saved state into density threads, phase curves when available, and spectral note strings.

## Available material

![Strings from a saved state](results/figures/cordas-densidade.png)

- [cordas-densidade.png](results/figures/cordas-densidade.png)
- [final_state.npz](../field-3d/results/data/final_state.npz)

## Archived implementation

The command below invokes the preserved implementation. Start with its [execution context](../../../docs/en/getting-started.md) and [implementation audit](../../../docs/maintenance/author-rules-audit.md); keep new output separate from the source record. Run from the repository root in a working copy.

```sh
MPLBACKEND=Agg python simulations/geometry/string-analysis/code/en/bravais_strings.py simulations/geometry/field-3d/results/data/final_state.npz
```

[English source](code/en/bravais_strings.py) · [Código em português](code/pt-BR/bravais_cordas.py)

## Reading and continuation

The included state contains `rho_f`, `v`, `ell`, `order` and `norm`, but no `psi_f`. The script therefore skips phase strings. The box size defaults to `L=32`; for another state, supply its actual size through the `L` environment variable. This step reads the state and writes figures to `bravais_outputs_3d/` without running the dynamics.

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)
