**English** · [Português](../../pt-BR/topics/quantum.md) · [Collection](../history.md)

# The QM sequence

This is the historical QM diagnostic sequence within TRIAD. Original protocols and verdicts are preserved. The nonstandard quantum-physics proposal is presented through the complete dynamics and the author’s operational reading; these tests do not replace it. [Understand TRIAD](../triad.md).

A sequence with a specification, protocols, configurations, seeds, raw data and analyses. Q00 fixes the starting point; Q01 and Q01b investigate resolution; Q02 expands to an ensemble; Q03 and Q04 examine subspaces and linearity.

| Stage | Study | Record |
|---|---|---|
| Q00 | [Frozen specification](../../../experiments/quantum/reference-specification/README.md) | The canonical Theta_core specification and the starting point for the QM sequence. The hash quoted in Q00 differs from the supplied canonical file; both are preserved. |
| Q01 | [Spatial convergence](../../../experiments/quantum/spatial-convergence/README.md) | N32/N48/N64 at fixed timestep. The recorded convergence decision is INCONCLUSIVE. |
| Q01B | [Resolution and timestep](../../../experiments/quantum/resolution-and-time-step/README.md) | N96 and timestep refinements follow Q01. The record remains INCONCLUSIVE. |
| Q02 | [A 32-seed ensemble](../../../experiments/quantum/seed-ensemble/README.md) | An MLX ensemble with both protocol versions preserved. The recorded QM decision is INCONCLUSIVE. |
| Q03 | [Subspaces and modes](../../../experiments/quantum/field-modes/README.md) | POD/PCA and DMD examine early and late windows across four seeds. The record does not establish a shared low-rank attractor. |
| Q04 | [Linearity probes](../../../experiments/quantum/linearity-tests/README.md) | Two seeds compare A, B and their superposition with matched noise. The protocol deviation and INCONCLUSIVE decision are retained. |

INCONCLUSIVE decisions and protocol deviations are part of the preserved results. The earlier pilots are not relabeled as confirmatory evidence for this sequence.

[Blueprint](../../reference/records/triad-qm-blueprint.md) · [Supplied specification](../../reference/records/triad-qm-canonical-v1.md) · [Integrity note](../../../provenance/t-archive/coverage.md)
