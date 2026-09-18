[Lab](../../README.md) · **English** · [Português](../pt-BR/repository-map.md)

# Find your way around

The [interactive lab](https://andujarleo.github.io/triad-lab/) is the public entrance. The repository connects that view to study files, reference documents and the records behind each image.

```text
README.md                         A short entrance for any reader
simulations/
  relations/ … validation/        Eight areas, each with an index
    <study>/
      README.md                   Question, context and known limits
      README.pt-BR.md             Portuguese entrance
      FILES.md                    Every associated material
      code/                       Preserved implementations
      configuration/              Explicit configurations, when supplied
      notes/                      Historical reports and protocols
      results/data/               Arrays, tables and recorded measurements
      results/figures/            Original plots and animations
      results/logs/               Execution records
      variants/<name>/code/       Distinct implementations, when needed
  catalog.json                    Complete machine-readable catalog
docs/en/ · docs/pt-BR/            Tours, glossary, project rules and technical guides
docs/reference/
  equation/                       Reference documents v1.0/v1.1 and their history
  concepts/ · records/ · solver/   Original research sources
provenance/                       Origins, path map, hashes and audit
templates/                        New studies and run records
web/                              Public interface and bilingual content
tools/
  build_site.py                   Export the site from preserved material
  check_repository.py             Integrity and navigation checks
  test_*.py · frontend.test.mjs    Preservation and interface tests
_site/                            Generated site, ignored by Git
```

Folders are created only when there is material for them. A note-only attempt is a valid record. Inside some studies, subfolders retain separate diagnostic groups or runs; merging files with similar names would erase distinctions.

**A payload has one storage location.** If identical bytes appeared in multiple bundles, their study indexes link to that same file. The catalog retains every original association. Files with the same name but different bytes remain separate; descriptive variant names or separate output bundles distinguish them. Hashes remain in the provenance ledger, without implying a version order.

Existing translated code remains in `code/en/` and `code/pt-BR/`. New translations add documentation, not copies of numerical code. Original scripts still contain their historical input and output paths; [execution guidance](getting-started.md) separates inspecting saved data from preparing a new execution under the project rules.

[All studies](../../simulations/README.md) · [Old-to-new path map](../../provenance/layout-migration.json) · [Contributing](contributing.md)

## The public site and the research archive

[Website source](../../web/README.md) describes the build, preview and language/module extensions. The generated `_site/` folder is disposable output; original research stays under `simulations/`. The [data contract](../maintenance/site-data.md) specifies how saved arrays and images reach the viewer.

The [reference-document index](../reference/equation/README.md) links the texts labeled v1.1 and v1.0. Those are document revisions; the equation is immutable. The [project rules](project-rules.md), [author page](author.md), [vocabulary](glossary.md) and [journal](journal.md) provide the context for new readers.

## A real example

```text
simulations/field-diagnostics/field-modes/
├── README.md
├── README.pt-BR.md
├── FILES.md
├── code/
│   └── analyze_field_modes.py
├── configuration/
│   └── config.json
├── notes/
│   ├── protocol.md
│   ├── mode-analysis-record.md
│   └── analysis.md
└── results/
    ├── data/
    │   └── seed-00/
    │       ├── leading-mode-early.npy
    │       └── explained-variance-early.npy
    ├── figures/
    └── logs/
```

T01–T39 and Q00–Q04 remain in the chronology and catalog for traceability. Folders use the subject of the study. Resolution, seed and time values stay in names when they distinguish different data.
