[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Geometry](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Strings from a saved state

**How can density, phase and spectral modes be inspected as strings?**

Post-processes a saved state into density threads, phase curves when available, and spectral note strings.


## Execution audit

> **TRIAD identity: NOT a TRIAD execution — context or post-processing.**
>
> Point-to-point record: [English](../../../docs/en/triad-identity-audit.md#study-bravais-02-strings) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-bravais-02-strings) · [Español](../../../docs/es/triad-identity-audit.md#study-bravais-02-strings) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-bravais-02-strings) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-bravais-02-strings) · [Norsk](../../../docs/no/triad-identity-audit.md#study-bravais-02-strings) · [Dansk](../../../docs/da/triad-identity-audit.md#study-bravais-02-strings) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-bravais-02-strings)

**Context or post-processing.** Post-processing of saved field states; this item does not evolve the complete equation.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-bravais-02-strings) · [cordas_arte.py](code/cordas_arte.py#L1)

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
