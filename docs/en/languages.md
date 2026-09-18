[Lab](../../README.md) · **English** · [Português](../pt-BR/languages.md)

# Languages

English is the base for editorial documentation; Brazilian Portuguese is the first maintained translation. All 65 study entrances, eight area indexes and public guides exist in both languages. Historical scientific documents, figures and code retain their original languages and labels.

| Language | Entrance |
|---|---|
| English | [Home](../../README.md) |
| Português | [Início](../pt-BR/README.md) |

## Add a language

1. Use a tag such as `es` or `fr` and create `docs/<tag>/README.md`.
2. Translate the entrance, tour and catalog first. Link to English wherever translation is unavailable.
3. Use `experiments/<area>/<study>/README.<tag>.md` for study pages and area indexes. Preserve IDs, paths, equations, units and values.
4. Record actual coverage in `docs/languages.json` and add only existing pages to the catalog and language switchers. Do not add a partial translation to the catalog’s fully maintained language list.
5. Record the translated revision with `<!-- Translation of: path; source commit: SHA -->`. Do not invent a SHA. The current English and Portuguese pages were authored together.
6. Update translations with their source or mark them visibly as awaiting synchronization.

New languages add explanations. Do not duplicate numerical code per language. Existing translated variants are preserved in `code/en/` and `code/pt-BR/`.
