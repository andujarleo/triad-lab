# A connected universe of research and simulations

Date: 2026-09-18. Basis: Leonardo Andujar’s request for a deep audit and a physical separation of research and simulations, accessible to general readers and technical contributors.

## Decision

Use `research/` for thematic reading paths and their preserved source library, and `simulations/` for the 65 study records. Themes link to source IDs and stable study IDs. Simulation folders contain their own code, notes, configurations and results. English and Brazilian Portuguese remain complete together. New languages add maintained reading paths without forking original implementations or source documents.

Keep the equation and historical mixed-purpose documents together in `docs/reference/`: splitting a note that contains both ontology and a run would erase its context. Preserve original bytes, historical verdicts and implementation differences. Corrections belong in maintained pages and the [execution audit](../en/execution-audit.md), following the [author-defined method](002-author-defined-method.md).

## Consequences

The site has two entrances and a thematic connection between them. Research links are explicit reading relationships, not claims that a cited theme was simulated. Every study exposes its execution classification and source-linked explanation. The old `quantum` and `validation` area IDs remain for saved URLs; their folders are `field-diagnostics` and `numerical-checks`.

The simulation catalog retains its `experiments` collection key for compatibility. The research and source catalogs use `schema_version: 1`; the public export keeps `format: 1` with additive research and audit fields. Checks reject broken references, missing translations, changed originals and one-sided theme/source relationships.

## Preservation and review

The [migration record](../../provenance/universe-migration.json) maps paths from the previous commit and records protected hashes. The [source catalog](../../research/sources/catalog.json) records the 21 new supplied sources independently. A repository snapshot and Git bundle were taken before the migration. Verification covers preservation, catalog consistency, numerical export identity and browser behavior; it does not represent new simulation runs.

## Português

A árvore passa a ter Pesquisa e Simulações conectadas por temas, com nomes descritivos e percursos para ler, investigar e executar. Referências compartilhadas continuam inteiras. Os originais são preservados; correções de interpretação ficam nas páginas mantidas. IDs antigos permanecem compatíveis, e as verificações cobrem arquivos, traduções, relações e exportação do site.
