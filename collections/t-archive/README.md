**English** · [Português](README.pt-BR.md) · [TRIAD Lab](../../README.md)

# A map of the T research archive

**Field → memory → structure → continuity.** A route through the questions, simulations and images that formed this archive.

**39 numbered runs · 6 QM stages · 1,330 files · 1,140 distinct contents**

This material comes from the author-supplied `T.zip`. It now has topic navigation, English and Portuguese entries, and links between notes, code, data and figures. Sources retain their original bytes and language.

| Reading path | What you will find |
|---|---|
| **[39 runs, one chronology](guides/timeline.md)** | From the first field sketches to nested structures, diagnostics and rerun dossiers. |
| **[The QM sequence](guides/quantum.md)** | Frozen specification, convergence, ensembles, subspaces and linearity. |
| **[Geometry, strings and visualization](guides/bravais.md)** | 2D/3D branches, spectral structure, perturbations, animations and saved states. |
| **[Passive R5](guides/passive-r5.md)** | A separate N64 run with snapshots, checkpoints and sensitivity records. |
| **[Causal continuity](guides/causal-continuity.md)** | Field traces, world tubes and matched background controls. |
| **[A persistent universe](guides/persistent-universe.md)** | A modal-state prototype, checkpoint continuity and passive readouts. |
| **[Foundations and provenance](guides/foundations.md)** | Concept notes, the reference equation, source listings and historical records. |

## Start with the figures

| Convergence | Persistent state |
|---|---|
| ![Refinamento temporal / Timestep refinement](source/QM/Q01b_dt_N/figures/dt_refine_N64.png) | ![Estado modal / Modal state](source/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/outputs/04_final_full_modal_slices.png) |

*Preserved original figures. Each belongs to a specific setup and its recorded data.*

## How to read

1. Choose a research line above.
2. Open an entry, then its note, protocol or analysis.
3. Follow the file index to data and code.
4. Check provenance and dependencies before attempting reproduction.

Runs 06, 11, 14 and 15 record attempts without artifacts. Failures, inconclusive results and later-refined diagnostics remain visible. This organization did not rerun or reclassify the studies.

## Download and verify

This collection uses Git LFS for NumPy arrays and animations. From the repository root:

```sh
git lfs install
git lfs pull --include="collections/t-archive/**"
shasum -a 256 -c collections/t-archive/SHA256SUMS
```

[Every file](files/README.md) · [Integrity and coverage](provenance/coverage.md) · [Portability](provenance/dependencies.md) · [Versions](provenance/versions.md) · [JSON catalog](catalog.json)

To expand the lab, create experiments with stable IDs and documentation per language. Use this archive as a preserved reference; put new runs in their own directories. See the [contribution guide](../../docs/en/contributing.md).
