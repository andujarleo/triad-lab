**English** · [Português](coverage.pt-BR.md) · [Collection](../../docs/en/history.md)

# Coverage and integrity

Source: the author-supplied `T.zip`. Inspection included both nested ZIPs. The original archive was not modified.

- SHA-256: `30276c2f96779ed1923612e82a323b06f88d00b1900272df919799c4791eee26`
- Bytes: `437576946`

| Category | Count | Disposition |
|---|---:|---|
| Entradas de arquivo / File entries | 2,779 | Indexadas / Indexed |
| Conteúdo / Content | 1,330 | Preservado / Preserved |
| Conteúdos distintos / Distinct contents | 1,140 | SHA-256 |
| Metadados macOS / macOS metadata | 1,445 | Indexados, excluídos / Indexed, excluded |
| Caches Python / Python caches | 2 | Indexados, excluídos / Indexed, excluded |
| ZIPs internos / Nested ZIPs | 2 | Conteúdo expandido / Contents expanded |

Names were normalized to UTF-8/NFC; the manifest also retains the names originally decoded by the ZIP reader. Identical contents remain at their paths to preserve local relationships. Git and LFS identify those contents by hash.

## What was inspected

All 1,140 distinct contents underwent technical inspection. The 60 Python scripts were parsed with AST; documents and structured files were read in full by parsers; all 561 PNGs and 10 GIFs were decoded, including every animation frame. Visual review covered 17 contact sheets with all PNGs and start/middle/end GIF samples. NPY/NPZ files were loaded without pickle.

No format errors were found in that inspection. The inspected arrays contained no NaN or infinity. Eight CSVs contain nonfinite diagnostic values; these remain intact and are recorded in the technical report. This is not a rerun of the simulations, a methodology certification or validation of every scientific conclusion.

## Preserved discrepancies

Q00 quotes SHA-256 `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` for the canonical specification. The supplied `TRIAD_QM_CANONICAL_V1.md` has SHA-256 `f9c23b3d74554beabca7ce8c578b0fb31fdc5b14943ed053596f4962f82273f1`. This archive does not establish why they differ; the historical reference and supplied file are both preserved without declaring equivalence.

[Q00](../../simulations/field-diagnostics/reference-specification/notes/specification-record.md) · [Canonical](../../docs/reference/records/triad-qm-canonical-v1.md)

[Complete manifest](manifest.json) · [Per-file inspection](inspection.json) · [File checksums](SHA256SUMS) · [Versions](versions.md)

The ZIP also contains 117 directory entries, recorded in [directories.json](directories.json). Empty directories and directory metadata are represented in that index; no artificial placeholder files are needed to retain their history.
