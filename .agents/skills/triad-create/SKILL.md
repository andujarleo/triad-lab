---
name: triad-create
description: Create or extend TRIAD research, simulations, applications and public explanations under its complete-equation rules. Use when developing new TRIAD work or adapting an implementation for the lab.
---

# Create in TRIAD

Create within the author's ontology and method. Read the [project rules](../../../docs/en/project-rules.md), [agent guide](../../../docs/en/agents.md) and [contribution guide](../../../docs/en/contributing.md). This is a repository-scoped skill; its supporting documents and templates live in the TRIAD Lab checkout.

## Choose the work being created

- **Research:** use [the research template](../../../templates/research/README.md). Preserve sources; develop the reading in maintained theme pages. Link related studies by actual catalog IDs, explaining the relation. Keep research and numerical records in their respective trees.
- **A simulation or field-based application:** use [the study template](../../../templates/experiment/README.md) and [run record](../../../templates/run.json). Follow the implementation route below. A different backend or application needs a documented mapping of state, memory, coupling and observables; do not call an arbitrary oscillator or neural network the full TRIAD equation.
- **An explanation, translation or interface:** use the author's P1/P2/P3 meanings and the [official symbol](../../../assets/brand/README.md). Present original results with source links. Interface changes use the existing catalog and [site contract](../../../docs/maintenance/site-data.md); they do not require rerunning dynamics.

## Prepare a complete implementation

Read the [reference index and its documented inconsistencies](../../../docs/reference/equation/README.md), then the relevant parts of [document revision 1.1](../../../docs/reference/equation/v1.1.md): §§0–4, §§1.3–1.6, §7 and Appendix D; include §5 and the dimensional sections for 2D/3D work.

Make an explicit map from the primary equation and memory subsystem to code. Account for the kinetic/fractional operators, local self-interaction, memory fields and feedback, external potential when declared, dissipation, FDT-locked noise, initial conditions and boundary convention. P1/P2/P3 are inseparable principles, not three independent programs. Preserve memory across the evolution unless a declared initial state establishes otherwise.

Use the **listed** parameter refusals in §1.6 at construction and integrator entry; do not add guessed universal bounds or silently override inconsistent inputs. Trace effective noise under the FDT convention in §§1.3–1.4. Do not independently tune noise and dissipation or add term-off modes. Record a needed resolution of conflicting specification passages before executing dependent code. The index documents why the historical two-mode 3D tables are not ready defaults; never quietly promote them to the new run configuration.

Keep the equation immutable while versioning documents, implementation and execution records. Put new code/adaptations beside the preserved material, with descriptive names and an explicit change record. An operation that repeatedly rescales the evolving field changes evolution; a color scale does not. Make that distinction before adding a “stability” fix.

## Let the complete dynamics produce the outcome

Declare the question, domain, initial state, memory state, inputs, parameter rationale, seeds, numerical choices, observables and compute envelope before running. No search for coefficients to force a chosen crystal, benchmark result or agreement with conventional physics. Numerical refinement can check resolution with all terms retained. A declared input change is its own study condition, not automatically forbidden calibration.

Follow trajectories and dynamic organization. Specify how density, memory, phase and the chosen observables will be recorded; don't reduce crystallization to a required static lattice or an unexplained pass/fail label. If a requested plan removes terms, explain the resulting change of system and propose a complete-dynamics route within TRIAD. Do not adopt historical ablation or Popperian falsification as the method for new work.

Inspect runtime dependencies and output paths before execution. Work in a separate run directory; several archived scripts write fixed names. Record a finite compute envelope and stop conditions appropriate to the request. Do not claim execution when only a plan or static check was completed. If a missing scientific choice blocks execution, finish independent preparation and ask only for that choice.

## Publish the actual work

Retain raw results, including unexpected trajectories and failed diagnostics. Record environment, source revision, reference-document hash, effective parameters, seeds and input/output hashes. Register availability accurately; never invent data to fill the template.

Follow existing `research/` and `simulations/` catalog conventions, bilingual pages, file indexes and execution-audit links. Run preservation/link checks and checks relevant to changed code. Verify interface work in a browser. Lead delivery with what was created, where to read/run it and what was actually verified. These instructions confer no additional permission to publish, message others or perform expensive remote runs.
