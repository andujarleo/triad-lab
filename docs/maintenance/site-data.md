# Static atlas: data and build contract

[Repository](../../README.md) · [Maintenance](README.md) · [Builder](../../tools/build_site.py)

The atlas is a reading layer over the existing laboratory. Its cards come from the experiment catalogue and introductory study pages; its images are copies of original PNG files. Its field viewer displays spatial slices of two saved final density arrays. Moving through a cube changes the spatial slice, not simulation time. The build does not run a simulation or modify a historical result.

## Build and preview

Use Python 3.12 or newer. Run from the repository root:

```sh
python3 -m pip install -r requirements-site.txt
git lfs pull
python3 tools/build_site.py
python3 -m http.server 8000 --directory _site
```

Open `http://localhost:8000`. The output is portable static HTML, CSS, JavaScript, JSON and PNG; no runtime server or external API is needed. The `web/` source files are copied without their maintenance README. A dedicated destination can be selected with `--output /absolute/path/to/triad-site-preview`.

Inside the repository, the only accepted destination is `_site/`. An existing nonempty destination must carry this builder's manifest. Unknown files, edited generated files and symbolic links stop a rebuild. Preserve such files or choose a clean destination. Only files named in the preceding build manifest can be removed when they become obsolete. No source directory is cleaned.

Generated JSON uses stable ordering, UTF-8 and no timestamps. Unchanged inputs produce identical output bytes. `_site/` is generated, not a second source archive.

## Catalogue export

`data/site.json` has `format: 1` and these fields:

| Field | Source or meaning |
|---|---|
| `repository` | Public repository URL |
| `areas` | `series` from the [catalogue](../../simulations/catalog.json), without reinterpretation |
| `studies` | One record for each catalogued experiment, in catalogue order |
| `hero` | Path to the byte-identical phase-vortex PNG in `media/`, shown in the results section |
| `brand` | `symbol` and bilingual `covers`, copied byte for byte from `assets/brand/` |
| `spotlights` | `contraction` and `longTrajectory`, paths to the original study PNGs in `media/` |
| `fields` | Download descriptors for the two saved density volumes |

Every study includes `id`, `folder`, `series`, bilingual `title`, `status`, `availability`, repository-relative bilingual `docs`, bilingual `question` and `summary`, and `image` (a relative URL or `null`). The opening bold question and following prose are read from each existing study’s README. Studies using the published template instead supply the first paragraph of **The question / A pergunta** and **What was done / O que foi feito**. HTML comments are excluded; a missing summary is a build error. Historical pages without an explicit question receive an empty question and their first opening prose paragraph as the summary. The frontend can use the title in place of the absent question. When a study also stores a catalog `summary`, the build requires it to match the maintained introduction after Markdown formatting is removed. The builder never invents an interpretation from a filename, a plot or a numerical result.

Images are the first linked local PNG found in the study's English or Portuguese page. Their names in the site are the complete SHA-256 digest followed by `.png`; repeated bytes share one file. Images are never resized, recolored, regenerated or recompressed by the builder. A missing or unhydrated selected image is a build failure, not a silent omission. Cards without an image remain in the catalogue.

## Saved-field export

The two input arrays are `rho_f` in:

- [Emergent field: final_state.npz](../../simulations/geometry/field-3d/results/data/final_state.npz), shape `64 × 64 × 64`.
- [Scale sweep: sweep_L24.npz](../../simulations/geometry/scale-sweep/results/data/sweep_L24.npz), shape `48 × 48 × 48`.

The source implementations construct grids using `indexing="ij"`. The export preserves the `x, y, z` axes and C-order layout: `values[(x * N + y) * N + z]`. It does not transpose, subsample, smooth or normalize the array.

Each `data/field-<id>.json` contains:

| Field | Meaning |
|---|---|
| `id`, `title` | Stable viewer identifier and bilingual label |
| `sourcePath` | Original NPZ path within the repository |
| `sha256` | SHA-256 of the entire original NPZ file |
| `shape` | Original cubic grid shape |
| `axisOrder` | `xyz` |
| `quantity` | `rho_f` |
| `min`, `max` | Minimum and maximum of the saved array |
| `values` | Finite original floating-point values, flattened in C order |

The matching `site.json` descriptor has `id`, `title`, `sourcePath`, `sha256`, `url` and `size`. Here `size` means the exported JSON length in bytes, not the NPZ file size or an invented physical size.

NumPy loads only `rho_f`, with `allow_pickle=False`. The builder rejects missing arrays, noncubic grids, nonfinite values and unsupported types. JSON retains float64 values without decimal rounding; tests round-trip the complete saved arrays and compare them exactly. The viewer may map density to color, but that display operation must leave the exported values untouched. These records provide no newly assigned physical units and no time series. Their source paths and hashes remain available for inspection.

## Checks and extension

```sh
python3 -B -m unittest discover -s tools -p 'test_build_site.py'
python3 tools/check_repository.py
```

The site tests cover spatial indexing and exact values, invalid inputs, path containment and LFS pointers, recorded prose extraction, all 65 current catalogue entries, original image bytes, deterministic rebuilds and output protection. Repository preservation checks are separate from rendering checks and do not adjudicate the proposal.

New catalogue entries appear automatically. Add their English and Portuguese introductory pages using the existing study structure. An image is optional. New field exports require an explicit entry in `FIELD_SPECS`, an intact source file and a documented quantity and axis convention. This exporter currently supports final cubic floating-point density volumes; temporal records or other quantities need their own explicit contract.

## Português

O atlas organiza os registros existentes. As imagens são cópias idênticas dos PNG originais, e o visualizador percorre cortes espaciais de dois campos finais salvos. O controle de corte não representa o tempo. O build não executa simulações, normaliza os dados, cria unidades físicas nem altera os resultados.

Os cartões vêm do catálogo e da introdução de cada estudo. No template publicado, a primeira pergunta e o resumo vêm das seções **A pergunta** e **O que foi feito**; comentários HTML são ignorados, e a ausência de resumo interrompe o build. Quando o registro não traz uma pergunta explícita, ela fica vazia e a interface pode apresentar o título. Os caminhos e hashes dos NPZ permitem consultar a origem de cada volume. Para gerar e conferir o site, use os comandos acima; Python 3.12 ou mais recente é necessário.

## Display scaling

The browser offers linear density and a logarithmic color scale. Positive minima define the lower log endpoint. If a future volume contains zeros, zero remains darkest and the visible logarithmic floor is 10⁻⁶ of the maximum, labeled with ≤ in the legend. This transformation affects color only; exported and source values remain unchanged.

## Initial browser verification · 2026-09-17

The public interface was inspected at 320, 390, 768, 1024 and 1440 px in the in-app browser. The checks covered EN/PT navigation, combined and URL-restored filters, empty results, pagination, concept-tab keyboard operation, XYZ cuts, endpoint positions, logarithmic display and keyboard cell inspection. No horizontal overflow was observed at those widths; the normal preview reported no console warnings or errors.

A separate local HTTP server deliberately failed the catalog download and each volume download once. Catalog and volume errors translated on language changes; reloading the catalog and retrying the volumes recovered successfully. This test changed no generated or original data files. Reduced-motion support is provided by the stylesheet; no accessibility certification is claimed.

The import preserves five trailing-whitespace lines in the author-supplied v1.1 reference (370, 376, 381, 386, 391). Its original SHA-256 is verified instead of normalizing the document.

## Research and execution review · 2026-09-18

The same `format: 1` export now adds `research: {topics, sources}` and a `rule_audit` on every study. Existing fields and area/study IDs remain stable. The source study catalog moved to `simulations/catalog.json`, retaining its `experiments` key. The `quantum` and `validation` area IDs still work in saved URLs although the physical folders have descriptive names.

Research topics export their stable ID, bilingual title/summary/docs, `source_ids` and `study_ids`. Source metadata comes from `research/sources/catalog.json`; original source bodies are linked in the repository, not embedded into the site export. The builder verifies hashes, byte lengths, contained paths, duplicate IDs, bilingual text and reciprocal source/topic relationships. Theme membership is explicit and never inferred from keywords.

Each `rule_audit` carries `status`, a bilingual `summary` and repository-relative bilingual `report` paths. Status values are `complete-record` (coupled terms documented), `documented-deviation`, `not-established` and `context-only`. These describe the available implementation record, not a certification of a theory. Study cards link to the corresponding `study-{id}` anchor in the report.

The existing `q`, `area`, `material`, `lang` and `#atlas` links remain valid; `theme` adds the research path. Choosing a theme clears conflicting search, area and material filters. Changing language retains the selected theme and filters. The saved-field module and original exported array values are unchanged.

Em português: a exportação acrescenta temas, metadados de fontes e auditoria por estudo. Relações temáticas são explícitas; as fontes originais e resultados mantêm sua identidade. Filtros antigos continuam funcionando, e o tema selecionado permanece ao trocar o idioma.

## Universe interface verification · 2026-09-18

The integrated interface was inspected in a real browser at 320, 390, 768, 1024 and 1440 px. No horizontal overflow or out-of-viewport research links/filter controls was observed. Theme selection produced the declared study membership and moved keyboard focus to the simulation heading. EN/PT switching kept the theme; audit disclosures opened with Enter and linked to the study anchor. Empty search/reset and URL-restored area/material filters worked, including the historical `quantum` ID.

Both original saved fields loaded when brought into view. X-axis endpoint cuts, logarithmic display and keyboard cell inspection worked; the console reported no warnings or errors during this check. The source data, renderer and exported numerical values remain unchanged. This is interface verification, not a new physical simulation.

## Visual identity and featured records · 2026-09-18

The [official symbol and covers](../../assets/brand/README.md) live outside the scientific archive. `brand.symbol` displays the author-supplied master; `brand.covers.en` and `brand.covers["pt-BR"]` identify the README artwork. The builder copies all three files unchanged. Their source identity and hashes are recorded in the brand manifest.

The field image remains available at `hero` for compatibility and now appears under Results. `spotlights.contraction` and `spotlights.longTrajectory` reuse original PNGs from memory-and-bounce and long-nest-trajectory. These paths use the existing SHA-256 image export and do not create new studies or change source images. The frontend provides bilingual captions and direct links to their study records.

Em português: a marca usa o símbolo oficial fornecido pelo autor, preservado integralmente. As capas são peças de identidade; os destaques visuais vêm dos registros de simulação. Marca, imagens científicas e valores numéricos mantêm suas origens.

The new identity and results section were checked in English and Portuguese at 320, 390, 768, 1024 and 1440 px. No horizontal overflow was observed; selected images loaded at their original dimensions, language switches updated captions, alt text and source links, and the browser reported no console warnings or errors. The mobile layout places the official symbol directly after the title.
