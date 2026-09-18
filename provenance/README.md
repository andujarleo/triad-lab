# Provenance · Proveniência

The original numerical record is preserved independently of its old folder names. / O registro numérico original é preservado independentemente dos nomes antigos das pastas.

| Record | Purpose / Finalidade |
|---|---|
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

Exact-byte consolidation does not merge experiments. Each study keeps all original source associations in `experiments/catalog.json`. Different hashes remain distinct even when filenames match. Existing code translations are preserved; future translations should not fork the numerical implementation.

A consolidação por bytes não une experimentos. Cada estudo mantém suas associações originais em `experiments/catalog.json`. Hashes diferentes continuam separados, mesmo quando os nomes coincidem. Traduções de código já existentes foram preservadas; novas traduções não devem duplicar a implementação numérica.

The acquisition-era inspection and coverage JSON files retain their original path vocabulary. Use `previous_destination` in the format-2 manifest or the migration ledger to resolve those paths. They describe inspection of supplied material, not new simulation runs.
