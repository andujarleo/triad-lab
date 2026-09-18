[Lab](../../README.md) · [Português](../pt-BR/glossary.md)

# A vocabulary for TRIAD

Some words describe the author’s view of reality. Others describe arrays, plots and numerical methods. This page connects them so you can move from the [proposal](triad.md) to an actual study without guessing what a label means.

## Atom

In the author’s operational reading, **one Gaussian packet is one atom**: a localized initial shape of Ψ. The same vocabulary extends to nested structures and an atom-like universe. Read the [original atom note](../reference/concepts/atom.md) and inspect [Gaussian atoms in one field](../../simulations/structures/gaussian-atoms-in-one-field/README.md).

## Matter and universe

TRIAD’s ontological hypothesis treats matter and its forms as emerging from a deeper dynamics. “Universe as simulation” names the author’s broad hypothesis; within a run, “universe” also names the filled volume being simulated. The [original universe note](../reference/concepts/universe-as-simulation.md) explains that operational use.

## Vibration and friction

These are stages in the author’s conceptual sequence: **atom → vibration → friction → frequency → energy**. A simulation needs a stated observable to attach these words to its output. Oscillation, phase change and dissipation already have numerical descriptions in the reference; the conceptual sequence does not establish a one-to-one mapping between each word and an equation term.

## Frequency and sound

“Sound” is the author’s label beside frequency in the conceptual map. In the lab, a spectrum may describe variation over time or structure across space. An audio rendering, when provided, needs its own mapping from those numbers to audible frequencies. See the [signal studies](../../simulations/signals/README.md).

## Energy and light

“Light” appears beside energy in the author’s map. A luminous color in a plot represents the quantity stated in its legend, such as density or phase. Connecting a recorded quantity to the proposed light/energy reading is a question to document in a particular study.

## Focus, memory and bath

| Word | In the complete dynamics |
|---|---|
| **Focus** | The attractive self-interaction regime, Λ < 0, can concentrate the field. |
| **Memory · part of P2** | The yⱼ fields respond to density on time scales 1/νⱼ. Their weighted sum acts on Ψ as V_mem. Positive and negative λⱼ produce different responses. |
| **Bath · expression of P3** | Dissipation Γ and stochastic excitation η act within the complete coupled dynamics. The reference document describes their FDT coupling. |
| **Anti-collapse** | The author’s name for the memory response opposing persistent concentration. A spread-out final state and intense earlier peaks can occur in the same record. |

The [reference-document index](../reference/equation/README.md) supplies the notation and document history. The equation itself is unique, immutable and indivisible.

## P1, P2, P3 and finitude

| Principle | Meaning |
|---|---|
| **P1 · Oscillation** | Oscillation is part of what constitutes the system. |
| **P2 · Self-reference** | The present state acts on its own dynamics, and memory carries the action of its history. P2 includes both. |
| **P3 · Coupling** | The system exists through coupling; the bath participates in that coupled dynamics. |

**P1 + P2 + P3** expresses the author’s integrated reading of these principles and finitude. The principles are defined. A unit, counted quantity or conserved observable for the sum must not be invented from that notation.

## Dynamic crystallization

TRIAD reads crystallization as dynamic organization. Oscillation, moving scales and reorganization can be part of the ordered state. A fixed lattice is not a required outcome. Read each time window, diagnostic and recorded configuration, without calibrating the field externally to obtain a preferred pattern. [Project rules](project-rules.md).

## Reading a simulation

| Term | What to look for |
|---|---|
| **Field / Campo** | Values represented on spatial locations or through modes. Ψ is the primary complex field in the reference. |
| **Density / Densidade** | ρ = \|Ψ\|² in the field studies. Check whether a figure shows a slice, projection or full volume. |
| **Phase / Fase** | The angle of the complex field. Phase colors do not encode density unless the legend says so. |
| **Grid / Grade** | The sampled locations. A 64³ grid has 64 × 64 × 64 positions. |
| **Time step / Passo de tempo** | The interval used for one numerical update. |
| **Random seed / Semente aleatória** | An input to the random-number generator. Exact replay also depends on code, parameters and environment. A Gaussian “seed” instead names an initial field packet. |
| **Checkpoint** | A saved internal state. Check which arrays were actually stored before trying to resume it. |
| **Spectrum / Espectro** | Distribution across temporal frequencies or spatial scales, depending on the calculation. |
| **Diagnostic / Diagnóstico** | A calculated measurement of a stated property. Its definition and failure conditions belong with the run. |
| **Convergence / Convergência** | Checking how results behave as numerical resolution is refined. The current reference describes ensemble comparisons for the noisy full equation. |
| **R5 / Θ_core** | Names found in historical configurations. Read the actual parameters and implementation attached to each study. |
| **QM / Q00–Q04** | Historical identifiers for field diagnostics, retained for chronology. |
| **Recorded / Registrado** | Material from a run is available; the word describes availability. |
| **Inconclusive / Inconclusivo** | A preserved diagnostic did not settle its question under that record’s criteria. This is not a classification of TRIAD’s identity. |
| **Hash / SHA-256** | A fingerprint of file bytes, used here to preserve source material and distinguish document revisions. |

[Five-minute tour](start-here.md) · [Research guide](research-guide.md) · [Research journal](journal.md)
