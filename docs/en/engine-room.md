[Lab](../../README.md) · **English** · [Português](../pt-BR/engine-room.md)

# The engine room

The dev door: contracts, commands, and the routes for changing the lab. Public pages stay readable; this page holds the machinery.

## Contracts: what lives where

| Directory | Holds | Never holds |
|---|---|---|
| `research/` | Themes, readings, preserved sources | Numerical executions |
| `simulations/` | Studies: code, configs, recorded outputs | Duplicated sources across themes |
| `docs/` | Guides in English and Portuguese; shared references | New numerical results |
| `provenance/` | Identity, hashes, migrations, audit records | New science |
| `web/` | Public site sources | Generated output (`_site/`) |
| `tools/` | Checks, tests, site build | Simulation code |
| `templates/` | Research, study and run scaffolds | Filled records |
| `assets/brand/` | Symbol and covers, byte-preserved | Result figures |

## The five commands

Run from the repository root:

```sh
git lfs pull
python3 tools/check_repository.py
python3 -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/frontend.test.mjs
python3 tools/build_site.py
python3 -m http.server 8000 --directory _site
```

[Dependencies and preview](../../web/README.md) · [Site data contract](../maintenance/site-data.md)

## Changing the lab

- **New study** — use the [study template](../../templates/experiment/README.md): bilingual pages, `FILES.md`, catalog entry, execution-audit links. [Contributing](contributing.md)
- **New edition** — follow the [edition workflow](editions.md): highlights with records, one-minute narratives, cover in both languages.
- **New language** — follow [Add a language](languages.md); audit translations first, catalog integrity always.
- **New audit verdict** — update the [identity audit](triad-identity-audit.md) and the study's `rule_audit` together.

## Rules that bite

- English and Portuguese move together; the catalog's fully maintained list stays integral-only.
- Preserved bytes are never edited — the checker enforces it. Maintained pages explain; they don't rewrite sources.
- Study intros feed the site build: keep the question and opening summary first. [Reading in layers](reading-layers.md)
- Never duplicate numerical code per language; new code goes beside preserved material, with a change record.

[Repository map](repository-map.md) · [Run guidance](getting-started.md) · [Contributing](contributing.md) · [Back to the cover](../../README.md)
