[Lab](../../README.md) · [Português](../pt-BR/agents.md) · [Project rules](project-rules.md)

# Work in TRIAD

**Understand the project. Read the complete dynamics. Create within its method.**

These skills give agents a working understanding of TRIAD, including why its rules matter. They carry Leonardo Andujar's project into explanations, research, code and new studies. An agent should not make the author reestablish the same foundations in every conversation.

## Three skills, one foundation

| Skill | Use it for | Example request |
|---|---|---|
| [triad-understand](../../.agents/skills/triad-understand/SKILL.md) | Ontology, principles, vocabulary and reasons for the method | “Use $triad-understand to explain why memory belongs to self-reference.” |
| [triad-read](../../.agents/skills/triad-read/SKILL.md) | Reading an equation, source, comparison or recorded outcome | “Use $triad-read to explain the contraction and expansion in memory-and-bounce.” |
| [triad-create](../../.agents/skills/triad-create/SKILL.md) | New research, simulations, applications and public explanations | “Use $triad-create to prepare a study of persistent structures with the complete dynamics.” |

The instructions use English as their base and support Portuguese requests. Read only the skill and sources relevant to the task. This guide supplies the shared reasoning; the mathematical reference remains in its own maintained location.

## What TRIAD is

TRIAD is nonstandard quantum physics and ontology. In its ontological account, one immutable equation forms the deepest layer of reality, and the universe is a simulation of that underlying dynamics. Matter is read through activity and relations rather than as the final, irreducible starting point. The lab gives this investigation a home for research and simulations, across subjects and scales.

The three principles are inseparable:

- **P1 · Oscillation:** movement and oscillation are constitutive of the dynamics.
- **P2 · Self-reference:** the system responds to its current state and its accumulated history. Present self-interaction and memory belong together.
- **P3 · Coupling:** relations participate throughout the system; excitation and dissipation belong to this coupled evolution.

“Focus, memory and bath” help describe operations. They do not rename the principles. An agent explaining TRIAD starts inside this vocabulary, then connects it to the notation and recorded behavior. [Foundations](triad.md) · [Glossary](glossary.md).

The author's sequence atom → vibration → friction → frequency/sound → energy/light belongs to this ontological reading. The operational “atom” can be a localized Gaussian field packet. A colored field plot, a measured frequency and an audible rendering each have a specific meaning. An explanation should say which is being used. P1 + P2 + P3 expresses the author's principles and finitude; this guide adds no numerical unit or conserved total to it.

## Why the rules belong to the dynamics

### One immutable equation

The equation defines the object being investigated. A document can clarify its expression, and an implementation can correct a programming error, while the equation remains the same. This is why **1.0 and 1.1 are document revisions**, and why code and run records have separate histories.

An agent must be able to describe a source discrepancy precisely without turning it into an “old TRIAD equation.” The [reference index](../reference/equation/README.md) already identifies inconsistent excerpts: kinetic factors, literal versus derived noise amplitude, and two-mode 3D tables alongside a minimum of three memory scales. Those passages remain preserved. Resolving a required implementation choice is concrete work; silently choosing a convenient table would hide it.

### No isolation: the feedback continues through the whole system

The memory subsystem illustrates the reason:

```text
Ψ → density |Ψ|² → memory fields yⱼ → memory potential V_mem → Ψ
```

The memory fields evolve with the density and act back on the next state. Dissipation and excitation participate during that evolution. Removing memory or the bath changes the operation generating the trajectory. It cannot be presented as another way of executing the same complete TRIAD dynamics.

There is a large recorded contrast in the N=40 memory comparison: final density peaks **0.000640882 and 3.889202170**, with participation ratios **4,720.477435 and 0.528063**. The branches are named `full` and `no-memory`; one expressly removes memory, and the generating source of the other is absent. The numbers are real parts of the record. Their correct role is a documented historical contrast, with those conditions attached—not a recipe for new TRIAD work. [Measurements](../../simulations/memory/memory-grid-40/results/data/summary.csv) · [Reading and conditions](execution-audit.md#finding-uni-002).

### Self-calibration: observe organization from declared conditions

TRIAD follows organization from chaos toward dynamic equilibrium. Choosing an output first and repeatedly adjusting coefficients until it appears would change the investigation into externally forced output selection. The new study therefore declares its inputs and numerical choices, then records what the complete evolution produces.

This does not make every parameter difference prohibited calibration. A different initial state, a declared input, grid refinement, detector measurement and display scaling are different operations. Name the operation and its purpose.

For example, two twelve-atom records finish with norms of **25,585.35 and 23.28**, while temperature, grid, duration and peak detection also differ. The lower-temperature note explains its setting. These records should be read with their complete conditions; the pair neither isolates temperature's contribution nor demonstrates an undocumented tuning search. [Twelve-atom comparison](execution-audit.md#finding-uni-011).

### Dynamic crystallization: read a trajectory

Equilibrium in TRIAD is active. A structure can persist through oscillation, redistribution and reorganization. A fixed lattice is not imposed as the only definition of crystallization. An agent should ask how organization develops over time and which quantities describe it.

The bounce record demonstrates why the observable matters. The radius containing half the mass, `r50`, changes from **3.487119** to **1.385641 at t=3.7**, then **9.863062**. Meanwhile `R_rms` has its minimum at the initial instant and its detector returns `bounced=False`. These are readings of different aspects of the same recorded distribution. Keep both, explain their definitions, and show the trajectory. Replacing one label to obtain agreement would lose information. [Mass-radius measurements](../../simulations/memory/memory-and-bounce/results/data/refined_bounce_summary.csv) · [RMS-radius measurements](../../simulations/memory/memory-and-bounce/results/data/summary.csv) · [Explanation](execution-audit.md#finding-uni-008).

### The TRIAD method: no imposed Popperian protocol

The lab's governing method is the author's structural and ontological reading of the complete system, its self-organization and relations. An agent should not redesign the project around ablation, Popperian falsification or agreement with standard quantum mechanics. Those are not the method the author chose for this work.

Implementation and numerical checks still have clear jobs: establish which operator was computed, whether data are finite, how a diagnostic is defined, which resolution was used and whether files retain their identity. For example, a grid/time-step study with all coupled terms retained is a technical investigation of the execution. It need not remove a physical term or become a verdict on the project's identity. Preserve its actual outcome, including `INCONCLUSIVE`. [Numerical refinement](execution-audit.md#finding-uni-013).

The rules define how TRIAD work is carried out. Saved measurements explain what a particular execution produced. Keeping both explicit lets an agent work confidently within the project and report technical discrepancies accurately.

## How to read a TRIAD record

Follow this chain:

```text
Question → equation → implemented operations → run conditions
         → saved measurements → interpretation → linked sources
```

Start with the study page and `FILES.md`, then inspect the files that support the requested statement. Read code statically before importing it: several archived scripts execute at import, refer to unavailable runtimes or write fixed output names. The label `full` does not establish the full operator; a solver beside an image does not establish which executable generated that image.

A useful reading distinguishes these cases:

| What changed? | What the agent should describe |
|---|---|
| A term or update operator | A different implemented dynamical system; preserve the source and identify the departure |
| Initial state, temperature or an applied input | A declared execution condition, with its rationale and complete configuration |
| Grid or time step | A numerical refinement, retaining the full dynamics and its recorded comparison |
| Radius, threshold or peak detector | A change of observable or detector; identify whether the trajectory changed |
| Color scale, spatial slice or camera | A representation of recorded values; explain what the control means |
| A source interpretation | A maintained reading, linked to the unchanged original |

The shared-bath residual offers another concrete lesson. With weights `a=b≈1/√2`, the common additive contribution does not cancel from `S−aA−bB`. An affine example leaves `(1−a−b)W`, with a bath-dominated normalized scale near **0.292893**. This helps explain the diagnostic's early recorded scale; it does not remove the bath or establish the cause of the entire later residual. [Formula, values and reading](execution-audit.md#finding-uni-014).

For research connections, identify whether the relation is a conceptual analogy, structural comparison, mathematical correspondence or source-reported measurement. A connection can be useful without becoming a new execution. Multiple documents citing the same upstream study do not create additional independent measurements. [Research foundations](../../research/foundations/README.md).

## How to create in TRIAD

**Research:** start with a question, preserve the supplied source, develop the interpretation in the theme page and connect relevant study IDs explicitly. Use [the research template](../../templates/research/README.md), with English and Portuguese pages. Sources remain under `research/`; numerical executions remain under `simulations/`.

**Simulation or application:** first map the full equation to the implementation. Describe state, memory, feedback, bath, initial conditions, boundaries and numerical convention. For an application, identify what introduces an input, what state persists and what the readout measures. Changing the interface does not redefine P1/P2/P3 or make an unrelated architecture the complete equation.

Use [reference revision 1.1](../reference/equation/v1.1.md), especially §§1.3–1.6 and Appendix D, together with the index's reconciliation notes. The listed refusals cover non-complete modes, non-positive Γ, declared f_FDT or k_B T, fewer than three memory scales and unequal ν/λ lengths. The bath's effective noise follows the reference FDT lock; it is not an independent fitting knob. Do not invent extra universal refusals or silently fill the unresolved 3D defaults.

Before execution, record the question, initial state, inputs, parameter rationale, seeds, numerical choices, observables and compute envelope. Check dependencies and output paths. Preserve archived implementations; place adaptations and new runs in separate records. During execution, retain trajectories and unexpected outcomes. Afterward, record the actual environment, command, code revision, reference hash and input/output hashes using [run.json](../../templates/run.json).

A missing scientific choice need only hold up the work that depends on it. An agent can complete the study structure, source map, implementation checklist and reading paths while the choice is resolved. It should ask for the specific missing decision, rather than demand permission to accept TRIAD's foundation again.

**Presentation:** use the [official symbol and covers](../../assets/brand/README.md), original result figures and clear explanations. Preserve the difference between a brand image, a saved spatial slice, reconstructed motion and an actual time series. Make the work visually strong and give every result a route to its record.

## Use the skills in this repository

The skills are versioned in **`.agents/skills/`** and linked from [AGENTS.md](../../AGENTS.md). Work from a full TRIAD Lab checkout so their relative links to rules, sources and templates resolve. They require no separate service or plugin.

Agents with repository-skill discovery can load them normally. For an agent without that mechanism, ask it to read `AGENTS.md` and the relevant `SKILL.md` explicitly. Discovery support differs between agent tools; copying a skill folder alone omits this repository's supporting sources. This change does not install project rules globally or change unrelated agents' configuration.

To extend the package, update the smallest relevant skill and both language guides. Keep domain explanations connected to the current sources. Verify local references and exercise a realistic request with another agent; a valid YAML header alone does not show that an agent applies the method correctly.

[Contribution workflow](contributing.md) · [Repository map](repository-map.md) · [Execution audit](execution-audit.md) · [Source preservation](../../provenance/README.md)

[Skill verification and use test](../maintenance/agent-skills.md).
