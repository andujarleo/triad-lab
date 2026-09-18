# Audit against the author’s project rules

2026-09-18 · [Project rules](../en/project-rules.md) · [Português](#português) · [File coverage and findings](../../provenance/author-rules-audit.json)

## Scope and result

The audit began at commit `47b21e011dbdc9c4fc95564bd0d792ec147350ea`: **1,491 tracked files, 65 studies and eight areas**. It covers the material published in this repository. Leonardo Andujar has additional research outside this collection.

The maintained presentation now follows the author’s rules: **nonstandard quantum physics and ontology; one immutable, indivisible equation; self-calibration without external adjustment toward a desired outcome; dynamic equilibrium and crystallization; no isolation of terms; no Popperian falsification protocol**. P1 is oscillation, P2 self-reference and P3 coupling.

The audit corrected documentation and publishing infrastructure. Historical scientific files remain preserved. Where an implementation differs from the rules, the difference is attached to its record rather than silently changing the implementation or its result.

## Coverage: what was actually examined

| Material | Coverage and method |
|---|---|
| Complete base tree | Every tracked path inventoried and hashed; the JSON records each file and its review method |
| Preserved research | 1,169 distinct payloads covering 1,384 original paths, plus the author-supplied reference document 1.1; verified against the preservation ledger and document hashes |
| Study navigation | All 65 English and 65 Portuguese entrances reviewed, with the catalog, eight area indexes in both languages and file links |
| Public presentation | Root README, maintained EN/PT guides, site copy, metadata, contribution instructions, templates and agent instructions |
| Scientific code | 76 files in code directories, including 71 Python files (34,783 lines); all Python parsed statically, with targeted manual inspection of parameters, update loops and diagnostics |
| Configurations | Eight dedicated configuration files inspected; parameters embedded in source code and notes also searched |
| Reference and study documents | 110 documents (23,726 lines) scanned; cited contexts read manually |
| Images, arrays and compiled material | Integrity and source associations checked; the viewer’s two exported arrays and selected images checked against original values/bytes. This audit did not reinterpret every image or execute the compiled binary |

A complete file inventory is not a claim that every line received an independent mathematical derivation. Static findings identify actual code and declared conditions; they do not establish which branch generated every historical output. No solver was imported or executed for this audit.

## Corrections delivered

- A bilingual [project-rules page](../en/project-rules.md), [repository instructions](../../AGENTS.md) and [recorded decision](../decisions/002-author-defined-method.md) carry the author’s method into future work.
- Public entrances and reference indexes distinguish **document revisions** from the immutable equation. The P1/P2/P3 definitions now follow the supplied context.
- Descriptions of equilibrium and crystallization reflect continuing organization. Availability labels describe files present in the repository.
- Every study links the methodology. Archived commands retain their execution context; they are not automatically certified as implementations of the complete equation.
- Study summaries and dossier links use descriptive language while retaining original verdicts, quantities and file associations.
- The site exporter now understands the actual English and Portuguese experiment templates. It reads the authored question and summary instead of template-copy instructions; regression tests cover both languages.
- The run template records the reference-document path, SHA-256 and revision separately from the implementation revision. The local-link checker now includes the website source guide.

## Source findings retained for follow-up

The [machine-readable findings](../../provenance/author-rules-audit.json) contain exact paths and line references. These are implementation/document observations, not a judgment of the theory or a change in study membership.

| Source finding | Recorded observation |
|---|---|
| [Passive memory: zero coefficients and two modes](../../experiments/memory/passive-memory-dynamics/code/simulate_passive_memory.py) · line 23 | `alpha=Gamma=f_FDT=0`; two memory fields; no stochastic increment. |
| [Causal continuations: deterministic two-mode operator](../../experiments/continuity/causal-traces/code/soul_causal_probe_short.py) · line 22 | Four continuation loops omit fractional dispersion, dissipation and noise. State/location controls use the same reduced base operator. |
| [Small-amplitude memory: fractional term disabled, bath active](../../experiments/memory/memory-small-amplitude/code/simulate_memory_small_amplitude.py) · line 2 | `ALPHA=0`, two memory modes; `GAMMA=.01` and `T_BATH=.001` keep the bath active. |
| [Reference solver: constructor checks and lower-level entry point](../../docs/reference/solver/solver.py) · line 67 | Validators protect several memory/bath conditions but do not reject `Lambda=0` or `alpha=0`; a low-level step accepts a prebuilt law dictionary. |
| [Field diagnostics: active memory and bath](../../experiments/quantum/spatial-convergence/code/measure_spatial_convergence.py) · line 34 | The five inspected diagnostic runners retain nonzero nonlinear, fractional, memory and bath coefficients, three memory rates and declared `V_ext=0`. |
| [Geometric evolution: repeated normalization](../../experiments/geometry/field-2d/code/bravais_emergent_coupled.py) · line 109 | Normalization occurs after field updates in several 2D/3D implementations, beyond preparation of initial conditions. |
| [Geometric evolution: conditional guards and feedback](../../experiments/geometry/field-3d/code/pt-BR/bravais_puro_3d.py) · line 116 | Field-derived coefficients, finite-value replacement, rescaling and small-norm random perturbations appear in the inspected geometric sources; activation in a saved run was not established. |
| [Geometric sources: different damping expressions](../../experiments/geometry/field-2d/code/bravais_pure_emerge.py) · line 208 | The base 3D source uses a real negative damping factor; pure 2D and the signed-memory variant use an imaginary factor in that position. |
| [Relational scripts: optional layers](../../experiments/relations/observer/code/en/simulate_observer_observed_relations.py) · line 116 | RK4 phase/edge-memory systems include chemistry/life-filter switches. These layers are not named terms of the reference field PDE. |
| [Random initialization without fixed seeds](../../experiments/geometry/field-2d/code/bravais_pure_emerge.py) · line 22 | Ten sources use `np.random.seed(None)`. Source availability alone cannot reconstruct their exact random trajectories. |
| [Backend diagnostics are not term ablations](../../experiments/quantum/seed-ensemble/code/probe_mlx.py) · line 5 | MLX probe/smoke scripts inspect backend operations and precision. Their filenames do not establish term isolation. |
| [Missing runtime and input files](../../docs/reference/solver/solver.py) · line 4 | Several studies still depend on external runtime modules, libraries, snapshots or CSV inputs already identified in the dependency records. |
| [Reconstructed vibration is post-processing](../../experiments/geometry/vibrations/code/bravais_vibracoes.py) · line 5 | A renderer derives motion from a saved state and selected spectral modes; it explicitly does not rerun the complete dynamics. |
| [Recorded dynamic crystallization](../../experiments/memory/passive-memory-dynamics/notes/passive-memory-report.md) · line 55 | The passive-memory report describes recurring focus/defocus and shifting dominant scale. Its declared end time is `T=15`. |
| [Dossier configurations with disabled terms](../../experiments/validation/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md) · line 10 | The dossier records zero fractional/bath coefficients and memory-off comparisons. These are preserved historical protocols, not new-run instructions. |
| [Detector calibration versus coefficient tuning](../../experiments/validation/reproduction-dossier/notes/lattice-detector-calibration/analysis.md) · line 1 | The Bravais record measures detector scores on synthetic structures and states that coefficients were not retuned. |
| [Inputs scheduled during evolution](../../experiments/structures/a-pocket-in-the-field/code/simulate_field_pocket.py) · line 515 | Pocket studies add Gaussian fields at a declared time; the impact script applies a declared kick. These are interventions, not solely initial states. |
| [Author’s operational reading](../../docs/reference/concepts/operational-readings.md) · line 8 | The preserved authorial text calls for joint dynamics and explicitly rejects tuning coefficients to resemble conventional examples. |
| [Document revisions and an immutable equation](../../docs/reference/equation/v1.1.md) · line 3 | The source documents and implementations have histories; the author’s project rule is one immutable equation. |

## What remains separate from this delivery

- The author’s later contextual manuscript and 26 accompanying principle/interface/methodology/result texts were used as context. They have **not** been silently imported as 27 new experiments or treated as commands. The manuscript needs a separate, source-preserving editorial revision.
- The historical code remains as supplied, including reduced configurations, normalizations, guards, missing runtime inputs and recorded failures. A future implementation needs an explicit mapping to the complete-equation specification; it must not overwrite these sources.
- The reference document’s internal differences remain visible in its [index](../reference/equation/README.md). This audit does not resolve them by inventing new defaults.
- The acquisition checker is tied to the current migration ledger. A future source batch needs a new acquisition manifest and an explicit extension of provenance checking; editing the old ledger to disguise new material is not an ingestion workflow.
- File-link checks do not validate external websites or every heading anchor. No numerical reproduction, universal-physics conclusion or certification of all archived runs is claimed.

## Verification

- Preservation and catalog checker: **65 studies, 1,384 original paths, 1,169 distinct payloads and 5,523 local file links** passed. The additional reference document retains its original hash; all **1,170 protected source files** are unchanged.
- **15 Python tests and six frontend tests passed.** The build exports all 65 studies, 56 original PNGs and two saved density volumes.
- Browser review covered English and Portuguese, navigation to the project rules, translated principles, search and both density canvases. Widths 320, 390, 560, 768 and 1440 px were inspected. The longer principle labels exposed a 390 px overflow; the existing stacked layout now applies through 560 px. The inspected preview has no horizontal overflow or console warnings/errors.
- Independent review corrected study-specific source links, a 1D implementation grouped with 2D explorations, and the distinction between simulation and reconstructed vibration. The reviewer confirmed those corrections.
- `git diff --check` passed. No scientific simulation was executed; no historical result was replaced.

## Português

Esta auditoria examinou o material publicado no repositório a partir do commit `47b21e0`: **1.491 arquivos, 65 estudos e oito áreas**. Isso não representa todo o acervo de Leonardo Andujar.

A apresentação mantida passou a seguir as regras do autor: **física quântica não padrão e ontologia; equação única, imutável e indivisível; autocalibração sem ajuste externo para obter um resultado; equilíbrio e cristalização dinâmicos; não isolamento; metodologia própria, sem protocolo popperiano de falsificação**. P1 é oscilação, P2 autorreferência e P3 acoplamento.

A cobertura combina inventário de todos os arquivos, hashes, leitura das entradas e guias bilíngues, inspeção estática de 71 arquivos Python e oito configurações, busca em 110 documentos de referência e dos estudos e leitura contextual dos achados. Os métodos estão identificados por arquivo no [registro da auditoria](../../provenance/author-rules-audit.json). Nenhum solver foi executado. Não se atribui uma reprodução numérica a uma verificação de arquivos.

Foram corrigidos os textos que sugeriam evolução da equação, definições incompletas dos princípios, expectativa de cristal fixo e instruções de contribuição incompatíveis com o projeto. As regras agora estão acessíveis nas fichas dos estudos e nas instruções para agentes. Também foi corrigida a exportação de estudos criados pelo template, com testes em inglês e português.

Os achados nas fontes permanecem documentados: há implementações reduzidas, normalizações e mecanismos de contenção numérica, além de diagnósticos e reconstruções visuais. Cada caso deve ser lido pelas operações que o arquivo realmente executa. Medir a resposta de um detector ou comparar precisão de um backend não equivale automaticamente a calibrar a equação ou remover termos.

**Os resultados originais, parâmetros, fontes, imagens e vereditos foram preservados.** Os textos mantidos explicam diferenças; não reescrevem o passado nem transformam registros incompletos em execuções da dinâmica completa. O manuscrito e os demais textos contextuais continuam como uma etapa separada de incorporação, sem inflar a contagem de estudos. Os detalhes, caminhos e linhas dos achados estão no registro JSON ligado acima e na tabela desta página.
