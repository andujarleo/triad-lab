# Repository layout audit · Auditoria de organização

## Scope and outcome

The migration starts at `5731b0d3b0f77b7249a7c94ef939edf573a338f3` and accounts for all **1,715 tracked paths** in that tree. It includes **1,384 original content paths**, now represented by **1,169 unique payloads**. **215 exact duplicate paths** were consolidated, including overlap between the initial lab and T.zip. Distinct content was never consolidated by filename or visual similarity.

A migração cobre todos os **1.715 caminhos rastreados** da árvore anterior, incluindo **1.384 caminhos de conteúdo original**. Eles correspondem a **1.169 conteúdos únicos**; **215 caminhos duplicados por bytes idênticos** foram consolidados. Nomes parecidos ou semelhança visual não foram usados para unir conteúdos diferentes.

## Physical structure

- 65 study homes in eight areas. The 39 chronological records retain their IDs and cross-links; the six QM entries retain protocol and outcome context.
- Code, notes, configurations, figures, arrays and logs live with the study that gives them meaning. FILES.md and catalog.json retain cross-study associations when bytes are shared.
- Three distinct Portuguese 3D field implementations remain visible. Descriptive variant names and separate output bundles distinguish colliding filenames; hashes remain in provenance without claiming chronology.
- The old unnamed folders, nested ZIP expansion directories and parallel source/reading trees are removed. Original names remain in acquisition metadata and the migration ledger.
- Original-language concepts, combined records and solver code have a separate reference index. Public navigation has English and Portuguese entrances, a tour, glossary, annotated gallery and research guide.

## Preservation checks

All numerical Python, configuration, table, array, image and binary payloads retain their original bytes. Source Markdown has only link tokens changed outside code. Reversible patches recover every original document hash. Missing or ambiguous references remain visible as text and are indexed; they are not silently redirected.

Every original source path has a canonical destination. All former tracked editorial paths resolve through the migration ledger, including consolidated navigation pages. Original acquisition inspections remain available with their historical path vocabulary.

Todos os códigos numéricos, configurações, tabelas, matrizes, imagens e binários mantêm os bytes originais. Nos documentos Markdown, apenas links fora de código foram alterados. As alterações reversíveis recuperam cada hash original. Referências ausentes ou ambíguas continuam visíveis e registradas.

## Verification and limits

- The maintained checker validates payload hashes, reverses document-link patches, checks catalog membership and translations, and resolves local file links.
- Unit tests exercise changed or missing payloads, Unicode document recovery, unrecorded prose changes and Markdown/HTML link handling.
- Saved-state post-processing was run in an isolated temporary directory with the relocated English string-analysis script. It produced **24 density threads and 40 spectral notes**; phase strings were skipped because the preserved input lacks `psi_f`, as expected.
- The original full field evolutions, archival MLX experiments and incomplete TriadLang runtime were not rerun. Preserved results were not replaced. Historical absolute paths and missing inputs remain documented per dependency family and source script.
- File integrity is not scientific validation. Q00’s hash discrepancy, inconclusive QM outcomes, failed diagnostics and missing runtime components remain explicit.

[Preservation ledger](layout-migration.json) · [Document changes](document-link-changes.json) · [Runtime audit](t-archive/dependencies.md) · [Research guide](../docs/en/research-guide.md)

[Earlier maintenance records](../docs/maintenance/README.md)

## Descriptive naming

Study folders use subjects rather than chronological codes. Entry points describe the action they perform. Dossier comparisons have names such as `memory-collapse-grid-128` and `barrier-memory-and-tunneling`; mode arrays are grouped by seed with descriptive quantities. `code/` and `configuration/` make the study tree readable without knowing internal abbreviations. Historical identifiers and every original filename remain in the ledger.

As pastas usam assuntos, não códigos cronológicos. Scripts de entrada descrevem a ação; comparações do dossiê e matrizes de modos têm nomes descritivos. Valores de resolução, semente e tempo distinguem dados diferentes. Identificadores e nomes originais continuam no registro de proveniência.

## Research identity

The author explicitly identified TRIAD as nonstandard quantum physics. The public entrance and bilingual concept guide now follow the preserved operational-reading and system-overview notes: focus, memory and bath acting together. Historical QM protocols remain diagnostic records with their original outcomes. This editorial framing does not change equations, source code or recorded results.

## Public entrance

The English and Portuguese READMEs feature the preserved phase-vortex still from the visual-comparison study, with a link to the original animation and renderer. Captions identify the opposite directions of phase winding. The first navigation choices distinguish a plain-language tour, annotated gallery and technical guide. No figure was retouched or generated for the cover.
