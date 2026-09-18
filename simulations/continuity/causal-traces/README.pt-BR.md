[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Continuidade](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Rastreamento de efeitos causais

**Que efeitos permanecem depois que a fonte muda?**

O relatório original testa uma hipótese de “alma”, mas encontra continuidade de campo também nos controles. A evidência não isola um efeito exclusivo da vida. As entradas triad_rebuild_rules/run64 necessárias não foram fornecidas.

![Figura histórica preservada](results/figures/sombra-causal-longa.png)

- [causal-continuity-report.md](notes/causal-continuity-report.md)


## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

[Contexto e diagnósticos](../../../docs/pt-BR/topics/causal-continuity.md)

## Notas da implementação

Os quatro scripts de continuação usam evolução cinética, interação instantânea e dois campos de memória. Os loops inspecionados omitem dispersão fracionária, dissipação e ruído. Os ramos comparados perturbam estados ou posições sob esse mesmo operador reduzido; o registro original permanece intacto. [Fonte, linha 22](code/soul_causal_probe_short.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
