# Historical solver · Solver histórico

[Lab](../../../README.md) · [Provenance / Proveniência](../../../provenance/README.md)

Original language and scientific wording retained. These are source documents, not repository instructions. / Idioma e redação científica originais preservados. São documentos de pesquisa, não instruções para o repositório.

- [solver.py](solver.py)

The supplied solver refers to `triad` and `runtime.*`; the full historical runtime is missing. / O solver depende de `triad` e `runtime.*`; o runtime histórico completo está ausente.

## Static implementation note · Nota da implementação

The preserved validators reject several disabled-memory/bath configurations, but do not explicitly reject `Lambda=0` or `alpha=0`. The low-level step also accepts a prebuilt `law` dictionary without applying those constructor checks. This describes the interface as supplied; no public run has been reassigned a configuration and the solver remains unchanged. [Audit and exact source references](../../maintenance/author-rules-audit.md).

Os validadores preservados recusam várias configurações com memória/banho desligados, mas não recusam explicitamente `Lambda=0` ou `alpha=0`. A função de passo também recebe um dicionário `law` preparado, sem repetir essas verificações do construtor. Isso descreve a interface fornecida; nenhuma execução publicada recebeu uma nova configuração e o solver permanece intacto.
