# TRIAD Universe Lab · website source

[Public lab](https://andujarleo.github.io/triad-lab/) · [Português](https://andujarleo.github.io/triad-lab/?lang=pt-BR) · [Repository](../README.md) · [Data contract](../docs/maintenance/site-data.md)

The public site has two connected wings: **Research**, with thematic readings and original sources, and **Simulations**, with preserved study records, available files and execution reviews. It presents TRIAD as Leonardo Andujar’s nonstandard quantum physics and ontology, makes every catalogued study searchable and lets readers inspect spatial slices of two saved density volumes. It uses the original research archive as its source. Building or browsing it does not execute the TRIAD equation.

The [project rules](../docs/en/project-rules.md) describe one immutable, indivisible equation and the author’s own methodology. P1 is oscillation; P2 is self-reference, including present self-interaction and memory; P3 is coupling. Present the terms together and self-organization without external calibration. Equilibrium and crystallization name dynamic organization. Revisions of reference documents and implementations describe records of the same equation; historical material remains attached to its actual execution conditions.

## Build locally

Use Python **3.12 or newer**, Git LFS and **Node.js 24** for the frontend tests. Run from the repository root:

```sh
git lfs pull
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-site.txt
python tools/build_site.py
python -m http.server 8000 --directory _site
```

Open `http://localhost:8000` or `http://localhost:8000/?lang=pt-BR`. The build writes portable HTML, CSS, JavaScript, JSON and original PNGs into **`_site/`**, which Git ignores. Serve that generated directory; `web/` alone does not contain the exported data.

Rebuild after changing source files. The builder checks its manifest before replacing generated files and refuses to overwrite unrelated or manually edited output. A separate destination is available through `--output /absolute/path/to/triad-preview`.

## Source map

| File                                    | Responsibility                                                 |
| --------------------------------------- | -------------------------------------------------------------- |
| [index.html](index.html)                | Page structure and semantic controls                           |
| [styles.css](styles.css)                | Responsive presentation, focus states and reduced motion       |
| [content.js](content.js)                | English and Portuguese interface text and concept panels       |
| [app.js](app.js)                        | Startup, language selection, navigation and URL state          |
| [research.js](research.js)              | Theme readings and explicit links to simulation records        |
| [atlas.js](atlas.js)                    | Search, theme/area/material filters and study cards            |
| [field.js](field.js)                    | Saved-density slices, display scales and cell inspection       |
| [build_site.py](../tools/build_site.py) | Export catalog records, source images and saved density arrays |

## Data and provenance

Study cards come from [catalog.json](../simulations/catalog.json) and the text of each study’s bilingual README. The published templates provide the question in **The question / A pergunta** and the summary in the first paragraph of **What was done / O que foi feito**. The builder also retains support for existing opening bold questions followed by prose. Template comments are not exported; a missing summary is a build error. The builder selects an existing PNG linked from those pages, copies its bytes and names it by SHA-256. A card without a selected preview remains searchable.

Research comes from [research/catalog.json](../research/catalog.json). Each topic has a stable `id`, a descriptive `slug` and `folder`, bilingual `title`, `summary` and `docs`, plus `source_ids` and `study_ids`. Source IDs resolve in [research/sources/catalog.json](../research/sources/catalog.json). The builder validates unique IDs, local paths, bilingual pages, SHA-256 and byte size for each source, and reciprocal source/topic links. Study IDs must already exist in the simulations catalog. Source metadata is exported; source texts remain in their original files. A thematic link is a reading connection, not an additional simulation or an equivalence between formalisms.

The generated `data/site.json` retains `format: 1`, `studies`, `areas`, `fields` and `hero`. Its additive `research` object contains `topics` and `sources`. Each study carries `rule_audit: {status, summary: {en, pt-BR}, report: {en, pt-BR}}`. Accepted statuses are `documented-deviation`, `not-established`, `context-only` and `complete-record`. Every record needs an explicit audit; both report paths must exist. The interface translates these into the documented implementation finding and links to its report. Material availability remains separate. The label for `complete-record` is “Coupled terms documented”; it is not a certification of a numerical run or a universal conclusion.

The opening uses the author’s [official TRIAD symbol](../assets/brand/README.md). The additive `brand` object supplies the original symbol and bilingual covers; `spotlights` supplies the contraction and long-trajectory figures. `hero` retains the original phase-vortex PNG, now shown in the results section. Branding and scientific figures are copied unchanged and remain separately identified. `#results` opens the featured records.

The existing anchors `#idea`, `#atlas` and `#field`, and query parameters `q`, `area`, `material` and `lang`, remain available. `#research` opens the thematic wing; `theme=<topic-id>` selects explicitly linked studies. Selecting a theme clears the previous search, area and material filters. Additional filters can then narrow that theme. Reset clears all filters; changing language preserves the current view. Topic links also work in a new tab. Historical GitHub file paths are recorded in the migration ledger; physical directory renaming does not create GitHub redirects.

The field viewer reads `rho_f` from these historical NPZ files:

- [3D field: final_state.npz](../simulations/geometry/field-3d/results/data/final_state.npz), a 64 × 64 × 64 density array.
- [Scale sweep: sweep_L24.npz](../simulations/geometry/scale-sweep/results/data/sweep_L24.npz), a 48 × 48 × 48 density array.

Exports retain their source paths, source-file hashes, axis order and recorded values. Display scales affect color only. The position slider traverses space within each final state, not time; separate color ranges and relative positions do not turn these different runs into a matched comparison. See the [full export contract](../docs/maintenance/site-data.md).

## Verify and publish

```sh
python tools/check_repository.py
python -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/frontend.test.mjs
python tools/build_site.py
```

Also inspect the browser at desktop and narrow widths in both languages: navigation, keyboard operation, filter URLs, empty states, failed downloads and field readouts. The tests cover data preservation and interface logic; they do not replace visual review.

The [Pages workflow](../.github/workflows/pages.yml) runs preservation checks, Python tests, frontend tests and the build. Pull requests receive checks; successful main-branch pushes and manual main-branch runs can publish the verified artifact to GitHub Pages.

## Add studies, languages or modules

**A study:** add its files, bilingual introductions and catalog entry through the [contribution guide](../docs/en/contributing.md). Rebuild; the atlas reads the catalog rather than maintaining a second list in JavaScript.

**A research theme:** add its bilingual pages and one catalog entry, with explicit source and study IDs. Update the source catalog’s reciprocal topic associations. Rebuild to validate the references. Theme counts and simulation-study counts remain separate.

**A language:** add translated study and guide pages and catalog titles, then extend `LANGUAGES` in the builder. Add the corresponding `copy` and `concepts` entries in `content.js`, a language control in `index.html`, and language/URL/document-path handling in `app.js`. Translate the saved-volume labels in `FIELD_SPECS`. Extend tests and verify missing translations and fallback behavior. The current implementation explicitly supports English and Portuguese; an additional language needs these coordinated changes.

**An interactive module:** place interface logic in its own ES module under `web/`, connect it through `app.js` and supply translated labels through `content.js`. Declare what its data represents and how it is exported before adding a new quantity, time series or transformation. New field datasets require an explicit `FIELD_SPECS` entry and checks for their units, axes and recorded values. Keep each new numerical execution in its own study record.

## Português

O Universo TRIAD tem duas alas conectadas: **Pesquisa**, com temas, leituras e fontes, e **Simulações**, com estudos preservados, materiais e análise das execuções. O site apresenta a TRIAD como física quântica não padrão e ontologia de Leonardo Andujar e permite examinar cortes espaciais de dados preservados. O código está dividido entre estrutura, estilo, conteúdo bilíngue, navegação, busca e visualizador. O build gera **`_site/`**, ignorado pelo Git; use essa pasta para a prévia local.

Os cartões vêm do catálogo e dos READMEs dos estudos. Imagens mantêm os bytes originais; volumes mantêm os valores registrados e os hashes dos arquivos de origem. O controle de posição atravessa espaço, não tempo. A [revisão 1.1 do documento de referência](../docs/reference/equation/README.md) registra a mesma equação imutável. Documentos, implementações e execuções históricas mantêm sua proveniência; não são versões da equação. As [regras do projeto](../docs/pt-BR/project-rules.md) orientam a apresentação da dinâmica completa, da auto-organização sem calibração externa e do equilíbrio e cristalização dinâmicos.

Os temas usam ligações explícitas por ID; textos e percursos de pesquisa não aumentam a contagem de estudos. Escolher um tema limpa os filtros anteriores, e trocar o idioma mantém a seleção. A auditoria descreve a implementação e as condições registradas, separadamente da disponibilidade de arquivos. “Termos conjuntos documentados” não é uma certificação de execução.

Para ampliar o site, use os comandos acima e siga os pontos de extensão: novo estudo pelo catálogo, novo idioma nas páginas e nos módulos de conteúdo/navegação, nova interação em módulo próprio com contrato de dados e testes. [Guia de contribuição em português](../docs/pt-BR/contributing.md).
