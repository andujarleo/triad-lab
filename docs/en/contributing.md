[Lab](../../README.md) · **English** · [Português](../pt-BR/contributing.md)

# Help the lab grow

Start with a question someone can understand before they read an equation. A contribution can be a study, a new run, an explanation, a translation or a correction.

## Add or extend a study

1. Choose an existing area in `experiments/`, or describe a new area in both language indexes.
2. Use a descriptive folder: `experiments/<area>/<study>/`. Keep its catalog ID stable even if the title changes.
3. Copy the [study template](../../templates/experiment/README.md). Write the question, what to notice in the representative figure, available evidence and known limits. Add the Portuguese entrance using its template; link to original-language technical material where translation is unavailable.
4. Put implementations in `code/`, explicit inputs in `configuration/`, reports in `notes/` and recorded outputs in `results/`. New runs should use `results/<run-id>/{data,figures,logs}/` so results cannot silently overwrite each other. Create folders only when they contain material.
5. Update `FILES.md`, the area indexes and [catalog.json](../../experiments/catalog.json). Existing entries demonstrate the schema: stable ID, folder, area, titles, docs, material availability and source associations. A shared payload stays in one location, with every association retained.
6. Record the exact command, working directory, code commit, dependencies, hardware, parameters, seeds and input/output hashes in [run.json](../../templates/run.json). Use `null` for unavailable values and explain why.

Catalog availability describes supplied material, not scientific validity. `note-only` and `specification` entries may have no outputs; `recorded` and `recorded-artifacts` indicate preserved outputs. `implementation-available` and `archival` require the page’s execution notes before attempting a run. Explicit `availability` fields say whether code, data, figures and notes are present.

## Preserve the comparison

Changing an equation, parameter, solver, backend or input creates a new comparison. Preserve the old record and document the difference. Keep negative and inconclusive outcomes with their context. Separate numerical observations from the interpretation they may support.

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

Present TRIAD as a proposal for nonstandard quantum physics. Connect new interpretations to the author’s operational reading and the regime actually executed. Distinguish the complete triad, historical pilots and controls; do not make a conventional quantum-mechanical diagnostic the definition of the entire project. [Presentation reference](triad.md).

The public atlas is generated from the same catalog. To add a representative question, image or saved field, follow the [site data contract](../maintenance/site-data.md). For interface changes, run `node --test tools/frontend.test.mjs` and rebuild as described in [web/README.md](../../web/README.md).
