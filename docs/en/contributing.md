[Lab home](../../README.md) · **English** · [Português](../pt-BR/contributing.md)

# Grow the lab

A contribution can be a new experiment, an additional run, a clearer explanation,
a translation or a correction. Keep the question, implementation, observations
and author's interpretation connected and distinguishable.

## Add an experiment

1. Choose an existing series or introduce a new one with a short description.
2. Give the experiment a stable lowercase ID, such as `series-01-topic`.
3. Copy the [English](../../templates/experiment/README.md) and
   [Portuguese](../../templates/experiment/README.pt-BR.md) templates into
   `experiments/<id>/`. Replace every placeholder; omit untranslated pages until ready.
4. Keep one implementation in `src/`, explicit inputs in `configs/`, and selected
   run records in `results/<run-id>/` inside that experiment. Create folders when
   they contain something; a proposed experiment does not need empty code folders.
5. Add its ID, series, titles, docs, scripts and artifacts to
   [catalog.json](../../experiments/catalog.json), and update both human catalogs.
6. Add the question and a representative artifact to the relevant guide when useful.

New series need no change to the lab's numerical code. Use descriptive series
names; the current Entre and Bravais paths remain supported. Existing scripts
are preserved at their historical locations and linked from their experiment pages.

## Record a run

Use [run.json](../../templates/run.json). Record the exact commit and command,
environment, parameters, input paths and checksums, generated artifacts and outcome.
Use `null` for unavailable values and explain why in notes; do not invent a seed,
version or measurement. Keep negative, partial and failed outcomes with their context.
Use distinct run IDs and never overwrite published data to make a later run agree.

The catalog's `status` describes available material: `proposed`,
`implementation-available`, or `recorded`. It is not a rating of scientific validity.
Only use `recorded` once at least one run artifact is included or explicitly linked.

## Preserve continuity

Changing an equation, parameter, numerical method or data source creates a new
comparison to document. Keep the previous record accessible. Describe numerical
observations separately from the interpretation they support. Editorial translations
must retain equations, parameter values and qualifications.

Check relative links, both language entry points and any command you changed.
For changes limited to navigation, verify the baseline rather than rerunning the
full simulations:

```sh
shasum -a 256 -c docs/archive/SHA256SUMS
```

Do not update baseline hashes to conceal a modified original. Add a new result or
version with its own provenance. [The archive](../archive/README.md) records the baseline.

## Pull requests

State the question or usability problem, what changed, how it was checked and any
execution limits. Keep editorial changes separate from changes to experimental behavior.
Include translation updates, or mark the affected translation as needing synchronization.
The current snapshot has no license file; preserve authorship and do not invent a license.
