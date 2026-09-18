# Provenance · Proveniência

The original numerical record is preserved independently of its old folder names. / O registro numérico original é preservado independentemente dos nomes antigos das pastas.

| Record | Purpose / Finalidade |
|---|---|
| [Universe migration](universe-migration.json) | Previous paths at `d9c4ecb` → Research/Simulations layout; protected before/after hashes |
| [Execution audit](../docs/en/execution-audit.md) · [Português](../docs/pt-BR/execution-audit.md) | 65 study classifications, 17 source-linked findings and comparison limits |
| [Execution audit data](execution-audit.json) | Coverage, structured findings and file inventory with current paths |
| [Research sources](../research/sources/catalog.json) | 21 intact supplied documents, source hashes and reciprocal theme relationships |
| [Migration ledger](layout-migration.json) | Every old tracked path → current destination; original and current content hashes |
| [Document link patches](document-link-changes.json) | Reversible link-only changes; source prose, equations and fenced code preserved |
| [Unresolved references](unresolved-document-links.json) | Missing or ambiguous historical links kept visible as text |
| [Initial lab](initial-lab/README.md) | Baseline from commit `468d66d` |
| [T.zip manifest](t-archive/manifest.json) | All acquisition entries, including excluded metadata and nested ZIP containers |
| [Author-rules audit](../docs/maintenance/author-rules-audit.md) | Author-defined method, editorial corrections and static implementation findings |
| [File coverage](author-rules-audit.json) | Every base-tree file, review method and source-linked findings from the 2026-09-18 audit |
| [Layout audit](layout-audit.md) | Scope, classification, deduplication and verification limits |
| [Runtime dependencies](t-archive/dependencies.md) | Missing inputs, historical paths and incomplete runtime infrastructure |

## Integrity

```sh
git lfs pull
python3 tools/check_repository.py
shasum -a 256 -c provenance/initial-lab/SHA256SUMS
shasum -a 256 -c provenance/t-archive/SHA256SUMS
```

The checksum lists use current repository-root paths and current document bytes. Original hashes remain in the ledger and acquisition manifest. The checker reverses recorded document-link patches in memory and verifies the recovered original hash. Every non-Markdown payload retains its original hash.

As listas usam caminhos atuais relativos à raiz e bytes atuais dos documentos. Os hashes originais permanecem no registro de migração e no manifesto de aquisição. O verificador desfaz as alterações de links em memória e confere o hash original. Todo conteúdo que não é Markdown mantém seu hash original.

## Recovery and scope

The complete pre-migration Git tree is commit `5731b0d3b0f77b7249a7c94ef939edf573a338f3`. The original T.zip SHA-256 is `30276c2f96779ed1923612e82a323b06f88d00b1900272df919799c4791eee26`. A local full-file snapshot and Git bundle were made before migration. The ZIP and that local backup are not required to browse or verify this repository.

Exact-byte consolidation does not merge experiments. Each study keeps all original source associations in `simulations/catalog.json`. Different hashes remain distinct even when filenames match. Existing code translations are preserved; future translations should not fork the numerical implementation.

A consolidação por bytes não une experimentos. Cada estudo mantém suas associações originais em `simulations/catalog.json`. Hashes diferentes continuam separados, mesmo quando os nomes coincidem. Traduções de código já existentes foram preservadas; novas traduções não devem duplicar a implementação numérica.

The acquisition-era inspection and coverage JSON files retain their original path vocabulary. Use `previous_destination` in the format-2 manifest or the migration ledger to resolve those paths. They describe inspection of supplied material, not new simulation runs.

## Universe layout · 2026-09-18

The previous layout is recoverable at commit `d9c4ecbcd7322c569d75f9424005fd6c70da5d4f`. The universe migration records 1,364 tracked path moves. All 1,169 protected payloads remain recoverable; the 1,062 non-Markdown payloads are byte-identical. The preserved Markdown changes are reversible navigation-link patches. The migration changes organization and interpretation, not a numerical execution.

A organização anterior pode ser recuperada no commit acima. A migração registra 1.364 caminhos movidos; os 1.169 conteúdos protegidos continuam recuperáveis, e os 1.062 arquivos que não são Markdown mantêm bytes idênticos. A pesquisa acrescenta 21 fontes fornecidas, com hashes próprios. IDs históricos continuam nos catálogos e filtros; nomes legíveis orientam a árvore pública.

The earlier author-rules audit retains its historical paths. Resolve its `experiments/` paths through the universe migration map; the new execution audit uses current `simulations/` paths. Neither inventory represents a rerun.

The 21 supplied research originals retain their Markdown spacing. A full migration diff reports 318 whitespace diagnostics across seven of those files; these are original bytes, including Markdown hard line breaks. The maintained pages and code pass the whitespace check when that explicitly preserved source directory is excluded. Source integrity remains checked by SHA-256 rather than by reformatting the originals.

Os 21 originais de pesquisa conservam a formatação recebida. Os 318 avisos de espaços em sete fontes foram mantidos para preservar seus bytes; as páginas editadas e o código passam na checagem de espaços. Os hashes verificam a identidade dos originais.
