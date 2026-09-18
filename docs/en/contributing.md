[Lab](../../README.md) · **English** · [Português](../pt-BR/contributing.md)

# Help the lab grow

Start with a question someone can understand before they read an equation. A contribution can be a study, a new run, an explanation, a translation or a correction. Read the [project rules](project-rules.md): TRIAD is nonstandard quantum physics with one immutable, indivisible equation and its own methodology.

## Add or extend a study

1. Choose an existing area in `simulations/`, or describe a new area in both language indexes.
2. Use a descriptive folder: `simulations/<area>/<study>/`. Keep its catalog ID stable even if the title changes.
3. Copy the [study template](../../templates/experiment/README.md). Write the question, what to notice in the representative figure, available evidence and known limits. Add the Portuguese entrance using its template; link to original-language technical material where translation is unavailable.
4. Put implementations in `code/`, explicit inputs in `configuration/`, reports in `notes/` and recorded outputs in `results/`. New runs should use `results/<run-id>/{data,figures,logs}/` so results cannot silently overwrite each other. Create folders only when they contain material.
5. Update `FILES.md`, the area indexes and [catalog.json](../../simulations/catalog.json). Existing entries demonstrate the schema: stable ID, folder, area, titles, docs, material availability and source associations. A shared payload stays in one location, with every association retained.
6. Record the exact command, working directory, code commit, dependencies, hardware, parameters, seeds and input/output hashes in [run.json](../../templates/run.json). Use `null` for unavailable values and explain why.

Catalog availability describes supplied material, not scientific validity. `note-only` and `specification` entries may have no outputs; `recorded` and `recorded-artifacts` indicate preserved outputs. `implementation-available` and `archival` require the page’s execution notes before attempting a run. Explicit `availability` fields say whether code, data, figures and notes are present.

## Preserve the comparison

The equation remains unchanged. A new input, declared configuration, numerical method, solver revision or backend needs its own execution record. Do not disable terms, calibrate toward a desired outcome or rewrite a result to fit an interpretation. Preserve existing records, including failed and inconclusive diagnostics, with their actual configurations and criteria.

The historical files listed in the provenance ledger have fixed original hashes. Do not update those hashes to conceal a change. Add an adapted implementation or a new run separately. A path-only adaptation can still affect file selection or working directories, so verify it explicitly.

## Review a contribution

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/check_repository.py
```

Hydrate Git LFS first when arrays or animations are missing. Review local links, translations and any changed execution command. For navigation changes, check integrity rather than rerunning all simulations. For a numerical change, state the comparison that was actually performed.

Describe the problem, final change, validation and remaining limitations in the commit or pull request. English is the editorial base; update Portuguese in the same change. [Other languages](languages.md) can be added without copying numerical implementations. The repository has no declared license; preserve authorship and do not invent a license.

[Next steps](roadmap.md)

## Preserve the starting point

Present TRIAD as nonstandard quantum physics. Use P1 oscillation, P2 instantaneous self-reference and memory, and P3 coupling together. Read crystallization dynamically, without requiring a fixed lattice. Technical checks inspect faithful implementation and recorded behavior of the complete system. The lab does not adopt Popperian falsification as its method. It does not isolate or remove terms as a TRIAD experiment, and standard-QM agreement is not its identity criterion. Historical controls remain records of their own procedures, not instructions for new TRIAD experiments. [Presentation reference](triad.md).

The public atlas is generated from the same catalog. To add a representative question, image or saved field, follow the [site data contract](../maintenance/site-data.md). For interface changes, run `node --test tools/frontend.test.mjs` and rebuild as described in [web/README.md](../../web/README.md).
