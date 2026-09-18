[Lab](../../../README.md) · [Reference library](../README.md)

# Equation reference · editions

**Current author-supplied edition: [v1.1, dated 2026-09-13](v1.1.md).** It is preserved byte for byte. [Version 1.0](../records/triad-equation-reference.md) remains available as a historical document, in its existing location.

| Edition | Use | SHA-256 of this repository file |
|---|---|---|
| [1.1](v1.1.md) | Current statement of the complete-equation rule and revised reference skeleton | `afb4ac1c7dc391a127e10548b12d0e5eaafd50f2e5093db2f27fcad0ea15d6d8` |
| [1.0](../records/triad-equation-reference.md) | Historical reference for reading the development of the project | `e2e0c39784ba76192b7c14ef31949607c5d15835eb33e27f0ff6c43251b0166a` |

The machine-readable record is [reference-editions.json](../../../provenance/reference-editions.json). The original v1.0 acquisition remains covered by the [layout migration ledger](../../../provenance/layout-migration.json).

## Reading version 1.1

Start at **§1.6**, which states the rule of the complete equation: no ablation mode; memory and bath remain active; raw results, declared parameters and seeds remain as produced. The listed implementation refusals cover non-complete modes, non-positive Γ, f_FDT or k_B T, fewer than three memory time scales, and unequal lengths of ν and λ. This index adds no new refusal rules.

Sections **1.3–1.4** describe the FDT lock and the resulting noise convention. **§7** records the revised validation protocol. **Appendix D** contains the revised 1D skeleton. These are specifications from the supplied document; this import does not claim that every archived script implements them.

### Editorial notes on the supplied edition

The source remains intact, including passages that require reconciliation before implementing a new solver:

- **§4.2 and Appendix D differ.** The initialization excerpt in §4.2 retains `hbar * k**2` and the literal declared `f_FDT`; Appendix D uses `hbar**2 * k**2` and the derived FDT amplitude, explicitly identifying those as v1.1 corrections.
- **§§10.3–10.4 list two memory modes.** The rule in §1.6 requires at least three. Appendix A withdraws the older 3D defaults and leaves a new 3D default unstated. The two-mode tables therefore should not be presented as ready-to-run v1.1 defaults.
- **Historical local paths are source text.** The absolute archive path in the v1.1 introduction records the author’s original location. Use the repository’s [v1.0 link](../records/triad-equation-reference.md) to read that edition here.

## How editions relate to experiments

Adding v1.1 updates the reference library. It does not change historical code, rewrite old parameter sets, replace recorded outputs, or certify older runs against the new edition. An old record retains its own configuration and chronology. A future execution should declare its reference edition, implementation revision and full parameters in the study record.

Read the public introduction in [English](../../en/triad.md) or [Portuguese](../../pt-BR/triad.md).

---

## Português · como usar as edições

A edição fornecida pelo autor e vigente neste índice é a **[v1.1, de 2026-09-13](v1.1.md)**, copiada byte a byte. A **[v1.0](../records/triad-equation-reference.md)** continua preservada como referência histórica.

A **seção 1.6** estabelece a regra da equação completa, com memória e banho ativos e sem modos de ablação. As recusas de parâmetros são as listadas no próprio documento; este índice não acrescenta regras. As seções **1.3–1.4** descrevem o acoplamento FDT, a **seção 7** contém o protocolo revisado e o **Apêndice D** traz o esqueleto 1D atualizado.

Há trechos a conciliar na edição fornecida: a inicialização da **seção 4.2** ainda usa `hbar * k**2` e `f_FDT` literal, enquanto o **Apêndice D** registra suas correções; as tabelas das **seções 10.3–10.4** ainda têm dois modos de memória, embora a **seção 1.6** exija pelo menos três. O Apêndice A retira os antigos padrões 3D e não fornece um novo. Esses trechos foram preservados e não são apresentados aqui como uma configuração 3D pronta para execução.

Importar a edição não modifica nem reclassifica as execuções históricas. Estudos novos devem registrar a edição, a revisão da implementação e os parâmetros usados. Os hashes acima e o [registro de edições](../../../provenance/reference-editions.json) permitem verificar os arquivos.
