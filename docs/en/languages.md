[Lab home](../../README.md) · **English** · [Português](../pt-BR/languages.md)

# Languages

English is the base for new editorial documentation; Brazilian Portuguese is the
first maintained translation. This does not change the language or authority of
historical source material. Original figures and saved data retain their labels.

| Language | Entry | Coverage |
|---|---|---|
| English (`en`) | [Home](../../README.md) | Home, catalog, seven experiment pages and guides |
| Português (`pt-BR`) | [Início](../pt-BR/README.md) | Início, catálogo, sete páginas de experimentos e guias |

## Add another language

1. Use a language tag such as `es` or `fr`; create `docs/<tag>/README.md`.
2. Translate the home and catalog first, linking to English for pages not yet translated.
3. Use `experiments/<id>/README.<tag>.md` for experiment pages. Keep IDs, code paths,
   equations, units and data unchanged. Translate explanations, not recorded results.
4. Add the language and its real coverage to [languages.json](../languages.json),
   this table and the language switchers. Add available page paths to `catalog.json`.
5. Put `<!-- Translation of: path; source commit: SHA -->` in each new translation.
   Record the English commit that was actually translated, not a guessed revision.
6. In the same pull request as an English change, update its translations or mark
   them visibly as awaiting synchronization. A partial translation links to the source.

The initial English and Portuguese documentation was authored together. Future
translation updates should record their source revision as above. The archived
README and existing code translations predate this convention.

## One implementation for future experiments

The existing `en/`, `entre/` and `bravais/` scripts are retained. New languages
should add documentation and, when supported, separate display labels. Do not
copy numerical implementations for every language. Do not deduplicate the existing
scripts as part of a translation; that would be a separate behavior-sensitive change.
