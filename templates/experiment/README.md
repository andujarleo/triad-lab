# Study title

<!--
Copy into experiments/<area>/<study>/README.md and replace every guidance paragraph.
Keep the Portuguese entrance synchronized; link translations only when they exist.
The site reads the first paragraph of "The question" and "What was done" for its card.
These comments are editorial guidance and are not exported into the card.
-->

## The question

State one question about the complete dynamics in language that needs no prerequisites.

## How to read the figure

Include an original figure when available. Explain axes, colors, panels and the part of the recorded evolution it shows. Identify a slice, projection or time series explicitly. If no output is available, state that directly.

## What was done

Summarize the declared initial conditions and recorded evolution in one plain-language paragraph. This paragraph becomes the study card’s summary.

Then identify the reference **document**, implementation revision, initial conditions, parameters, seeds and numerical method. TRIAD has one immutable, indivisible equation. All terms act together: P1 is oscillation; P2 is self-reference, including present self-interaction and memory; P3 is coupling. Follow the project’s rules and methodology for the complete dynamics, preserving self-organization without external calibration or adjustment toward a target result. Describe equilibrium and crystallization as dynamic organization.

## Recorded observations and context

Separate the numerical observations, the author’s interpretation and the files supporting each. Preserve negative, inconclusive and conflicting records. State missing code, inputs or dependencies. Link all supplied material through `FILES.md`. A historical implementation or execution is a record to describe with its conditions; it is not another form of the equation.

## Run or inspect

Give the working directory, environment, exact command, inputs and outputs. State hardware needs and whether outputs can be overwritten. If supplied material cannot be run as received, explain which input or dependency is missing. Keep any adaptation separate from the preserved source.

## Next observation

State what remains to follow in the complete dynamics. Declare any new run’s conditions before execution and retain its raw outputs, including behavior different from what was anticipated.

## Origin

Record authorship, source files and commit. Use `templates/run.json` for the reference-document path, hash and revision, the implementation revision, environment and input/output hashes. A revision number identifies documentation or implementation; it does not version the equation. Share one numerical implementation across languages.
