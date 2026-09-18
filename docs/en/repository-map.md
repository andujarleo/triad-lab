[Universe](../../README.md) · [Português](../pt-BR/repository-map.md)

# Repository map

Research and simulations have separate homes. Themes connect them through catalog IDs, so a study keeps one canonical set of files.

```text
.agents/skills/                   TRIAD agent skills: understand, read, create
research/
  <theme>/README.md · README.pt-BR.md
  foundations/                    Shared reading of the TRIAD principles
  sources/author-supplied/         Byte-preserved supplied documents
  catalog.json · sources/catalog.json
simulations/
  <area>/<study>/
    README.md · README.pt-BR.md    Question, interpretation and audit
    FILES.md                      All associated material
    code/ · configuration/        Preserved implementation and inputs
    notes/                        Source reports and protocols
    results/data/                 Recorded arrays and tables
    results/figures/ · results/logs/       Images, animations and execution logs
    variants/                     Different preserved implementations
  catalog.json                    Studies, source associations and audit
docs/en/ · docs/pt-BR/             Tours, method and technical guides
docs/reference/                   Equation documents and author records
provenance/                       Source hashes and path migrations
assets/ · web/                    Presentation and public site
tools/ · templates/               Verification, build and contribution tools
```

Every study keeps its existing ID. Folders use descriptive names; grid, seed and time values remain where they distinguish data. Identical source bytes have one storage location and multiple associations. Different implementations and outcomes remain distinct.

`docs/reference/` is shared: some author records combine ontology, algorithms and results. They remain intact and are linked from both wings. The labels v1.0/v1.1 identify document revisions of one immutable equation.

The previous `experiments/` tree is now `simulations/`. `quantum/` became `field-diagnostics/`, and `validation/` became `numerical-checks/`; their catalog IDs stay stable. Old GitHub file URLs are recoverable through the path map and its base commit. Public site anchors and study filters remain supported.

[Research](../../research/README.md) · [Simulations](../../simulations/README.md) · [Audit](execution-audit.md) · [Path map](../../provenance/universe-migration.json) · [Provenance](../../provenance/README.md)
