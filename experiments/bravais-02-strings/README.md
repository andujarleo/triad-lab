**English** · [Português](README.pt-BR.md) · [Catalog / Catálogo](../README.md)

# Strings from a saved state

`bravais-02-strings` · bravais

**How can density, phase and spectral modes be inspected as strings?**

Post-processes a saved state into density threads, phase curves when available, and spectral note strings.

## Available material

![Strings from a saved state](../../bravais/resultados/cordas_densidade.png)

- [cordas_densidade.png](../../bravais/resultados/cordas_densidade.png)
- [final_state.npz](../../bravais/final_state.npz)

## Run

[Set up the environment](../../docs/en/getting-started.md), then run from the repository root.

```sh
MPLBACKEND=Agg python en/bravais/bravais_strings.py bravais/final_state.npz
```

[English source](../../en/bravais/bravais_strings.py) · [Código em português](../../bravais/bravais_cordas.py)

## Reading and continuation

The included state contains `rho_f`, `v`, `ell`, `order` and `norm`, but no `psi_f`. The script therefore skips phase strings. The box size defaults to `L=32`; for another state, supply its actual size through the `L` environment variable. This step reads the state and writes figures to `bravais_outputs_3d/` without running the dynamics.
