**English** · [Português](../../pt-BR/topics/quantum.md) · [Collection](../history.md)

# The QM sequence

This is the historical QM diagnostic sequence within TRIAD. Original protocols and verdicts are preserved. TRIAD is nonstandard quantum physics by its project identity. Its complete dynamics and the author’s operational reading define the approach; agreement with standard QM is not its identity criterion. [Understand TRIAD](../triad.md).

A sequence with a specification, protocols, configurations, seeds, raw data and analyses. Q00 fixes the starting point; Q01 and Q01b investigate resolution; Q02 expands to an ensemble; Q03 and Q04 examine subspaces and linearity.

| Stage | Study | Record |
|---|---|---|
| Q00 | [Frozen specification](../../../simulations/field-diagnostics/reference-specification/README.md) | The canonical Theta_core specification and the starting point for the QM sequence. The hash quoted in Q00 differs from the supplied canonical file; both are preserved. |
| Q01 | [Spatial convergence](../../../simulations/field-diagnostics/spatial-convergence/README.md) | N32/N48/N64 at fixed timestep. The recorded convergence decision is INCONCLUSIVE. |
| Q01B | [Resolution and timestep](../../../simulations/field-diagnostics/resolution-and-time-step/README.md) | N96 and timestep refinements follow Q01. The record remains INCONCLUSIVE. |
| Q02 | [A 32-seed ensemble](../../../simulations/field-diagnostics/seed-ensemble/README.md) | An MLX ensemble with both protocol versions preserved. The recorded QM decision is INCONCLUSIVE. |
| Q03 | [Subspaces and modes](../../../simulations/field-diagnostics/field-modes/README.md) | POD/PCA and DMD examine early and late windows across four seeds. The record does not establish a shared low-rank attractor. |
| Q04 | [Weighted response residual](../../../simulations/field-diagnostics/linearity-tests/README.md) | Two seeds compare A, B and a combined initial state with the same additive-noise realization. That common bath does not cancel from the weighted residual: even an affine linear response retains `(1−a−b)W`. The metric is not a pure superposition test; the original protocol deviation and INCONCLUSIVE decision remain preserved. |

INCONCLUSIVE decisions and protocol deviations are part of the preserved results, attached to the questions and criteria of these records. These protocols are historical material, not the governing methodology for new TRIAD work; see the [project rules](../project-rules.md). The earlier pilots are not relabeled as confirmatory evidence for this sequence.

[Blueprint](../../reference/records/triad-qm-blueprint.md) · [Supplied specification](../../reference/records/triad-qm-canonical-v1.md) · [Integrity note](../../../provenance/t-archive/coverage.md)
