[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Memória](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Dinâmica passiva da memória

**Como a memória participa da reorganização espacial contínua?**

O relatório descreve cristalização dinâmica por deslocamentos recorrentes de escala. A norma registrada permanece próxima de um. A estimativa por trajetória gêmea cobre apenas o intervalo curto registrado.

![Figura histórica preservada](results/figures/density-slices-selected.png)

- [passive-memory-report.md](notes/passive-memory-report.md)


## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

[Contexto e diagnósticos](../../../docs/pt-BR/topics/passive-r5.md)

## Notas da implementação

O runner e a configuração preservados usam `alpha=0`, `Gamma=0`, `f_FDT=0` e dois campos de memória. O loop não inclui incremento estocástico. Leia a cristalização dinâmica registrada nessas condições efetivas; este arquivo não implementa todos os termos ativos. [Fonte, linha 23](code/simulate_passive_memory.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
