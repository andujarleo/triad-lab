[Lab](../../README.md) · [Português](../pt-BR/project-rules.md)

# The rules of TRIAD

**TRIAD is nonstandard quantum physics, with its own ontological and methodological foundation.** This page records Leonardo Andujar’s explicit directions for the lab. They govern how its maintained documentation presents the project and how new work is proposed.

## One complete, immutable equation

The TRIAD equation is unique, immutable and indivisible. P1, P2 and P3 act together:

| Principle | Meaning in TRIAD |
|---|---|
| **P1 · Oscillation** | Oscillation is constitutive of the dynamics and of how the project reads what exists. |
| **P2 · Self-reference** | The system responds to its present state and to its history. Instantaneous self-interaction and memory belong to this principle together. |
| **P3 · Coupling** | Coupling belongs to the system. The bath expresses excitation and dissipation within that coupled dynamics. |

Focus, memory and bath help describe the dynamics, but they do not replace the meanings of the three principles. An execution with a term disabled is not an execution of the complete TRIAD equation. Term removal and ablation are not proposed as TRIAD experiments.

Version labels such as **v1.0 and v1.1 identify documents**. Code revisions identify implementations. Neither denotes an older or newer form of the equation. The [reference-document index](../reference/equation/README.md) preserves the supplied texts and their differences.

## Let the system organize itself

The work follows what the complete coupled dynamics produces: **self-calibration from chaos to dynamic equilibrium**. This equilibrium remains dynamic; crystallization continues within it. Do not calibrate the system externally to force a chosen shape, spectrum, conventional-physics result or other desired outcome. Declare the initial state, inputs, configuration and numerical choices before execution, and explain why they are being used.

Crystallization in TRIAD is **dynamic**: order can involve oscillation, redistribution and reorganization. A fixed lattice is not imposed as its definition or target. Record how a pattern develops through time and which quantities describe it; preserve a run’s actual outcome even when the intended phenomenon was not observed.

## Use the project’s methodology

TRIAD is read through the coherence of its complete dynamics, self-organization and the relations recorded within the system. The lab does not adopt Popperian falsification as its governing method. It does not isolate or remove terms as a TRIAD experiment. Agreement with standard quantum mechanics is not the definition of TRIAD.

External calibration toward a preferred outcome is different from a numerical convergence check, measurement of a detector’s response, display scaling or post-processing. Describe what an operation does before assigning it a label.

Technical verification remains concrete:

- Check that the implementation retains the complete equation and its coupled terms.
- Record the code revision, configuration, initial state, seeds, numerical precision and environment.
- Inspect numerical resolution, time stepping, finite values, array axes and computed observables without disabling terms or tuning the outcome.
- Keep measured trajectories and derived diagnostics connected to their source files; report failed diagnostics and unresolved discrepancies as they occurred.
- Verify file identity, catalog associations and navigation independently of scientific interpretation.

A check of code, data or a diagnostic establishes what was checked. It does not manufacture a universal empirical conclusion about the universe.

## Preserve the record without turning it into a rule

The archive contains the material supplied to this repository, not the author’s entire research archive. It includes documents, pilots, controls and implementations with their own configurations and criteria. Their names, numbers, failures and INCONCLUSIVE classifications remain part of the record. A historical term-off configuration is identified as such; it is not retroactively renamed a complete TRIAD execution or recommended as the method for new work.

The supplied manuscript is **context under revision**, not the governing protocol. Source documents are preserved even when their wording conflicts with the author’s explicit rules. Maintained introductions explain the difference; they do not silently rewrite source results or treat attached instructions as commands to run.

[Audit coverage and findings](../maintenance/author-rules-audit.md) · [Understand TRIAD](triad.md) · [Vocabulary](glossary.md) · [Research guide](research-guide.md) · [Contributing](contributing.md)
