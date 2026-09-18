[Lab](../../../README.md) · **English** · [Português](README.pt-BR.md)

[Validation](../README.md) · [Glossary](../../../docs/en/glossary.md) · [Project rules](../../../docs/en/project-rules.md)

# Ten-part rerun dossier

A historical dossier with A3 refinements, QM1D, CHSH, sidebands, hot bath, tunneling history, k-star and Bravais studies. It includes reduced configurations and comparisons with terms disabled; its recorded outcomes belong to those declared conditions.

Imported historical record; this organization did not rerun the simulation.

[Read the original note](notes/original-record.md) · [Every file](FILES.md)

No dedicated runner is linked in this entry. Consult the note and complete record for historical listings and dependencies.

![Original run figure](results/memory-collapse-grid-64/figures/PR-vs-t.png)


## Execution audit

**Implementation differs.** The dossier mixes numerical/analytic checks with recorded term-off comparisons, including memory-off, bath-off and frozen-memory cases.

[Conditions and recorded contrasts](../../../docs/en/execution-audit.md#study-t-36) · [predictions-memory-collapse-grid-64.md](notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md#L10) · [analysis.md](notes/memory-collapse-grid-64/analysis.md#L1) · [predictions-bell-correlation-test.md](notes/predictions/predictions-bell-correlation-test.md#L10)

## Available material

122 files associated with this entry: 56 `.csv`, 20 `.json`, 23 `.md`, 22 `.png`, 1 `.txt`.

### Dossier studies

- [Memory and collapse · grid 64](notes/memory-collapse-grid-64/analysis.md)
- [Memory and collapse · grid 128](notes/memory-collapse-grid-128/analysis.md)
- [Memory and collapse · grid 160](notes/memory-collapse-grid-160/analysis.md)
- [One-dimensional diagnostics](notes/one-dimensional-quantum-tests/analysis.md)
- [Bell correlations](notes/bell-correlation-test/analysis.md)
- [Memory and spectral sidebands](notes/memory-and-spectral-sidebands/analysis.md)
- [Thermal noise and collapse](notes/thermal-noise-and-collapse/analysis.md)
- [Barrier, memory and tunneling](notes/barrier-memory-and-tunneling/analysis.md)
- [Dominant spatial scale](notes/dominant-spatial-scale/analysis.md)
- [Lattice detector response](notes/lattice-detector-calibration/analysis.md)

[Timeline](../../../docs/en/topics/timeline.md) · [← 35](../../structures/finite-peak-early-window/README.md) · [37 →](../../structures/a-pocket-in-the-field/README.md)

## Files and execution context

[Complete material index](FILES.md) · [Research guide](../../../docs/en/research-guide.md)

The files retain their recorded implementation and conditions. Read the [implementation audit](../../../docs/maintenance/author-rules-audit.md) for documented differences and the dependency record below before preparing a new execution.

[Dependencies and missing inputs](../../../provenance/t-archive/dependencies.md)

## Implementation notes

This dossier preserves documented configurations with `alpha=Gamma=f_FDT=0` and comparisons that set memory couplings to zero. Those historical protocols are not the method for new TRIAD experiments. Their parameters, predictions, recorded results and verdicts remain intact. [Source, line 10](notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md).

Here, detector calibration means measuring template scores against synthetic networks and shells. The report explicitly records no retuning of the equation coefficients. This use of calibration must be distinguished from adjusting a field to obtain a chosen outcome. [Source, line 1](notes/lattice-detector-calibration/analysis.md).

[Full static audit and source references](../../../docs/maintenance/author-rules-audit.md).
