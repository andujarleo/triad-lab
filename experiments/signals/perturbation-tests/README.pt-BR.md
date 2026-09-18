[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Sinais](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Respostas a perturbações

**Como o campo responde quando seu estado inicial é perturbado?**

Quatro protocolos registrados exploram ligação, pequenas perturbações, impactos e excitação rítmica. Cada fonte preserva as entradas, comparações e escolhas de parâmetros usadas na ocasião.

![Figura histórica preservada](results/figures/batida-numeros.png)


## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Alguns protocolos arquivados acrescentam uma entrada durante a evolução: os estudos de bolsos inserem campos gaussianos no instante declarado `T_PLANT=0.5`; o script de impacto aplica uma perturbação declarada no pico do campo. Leia essas operações como intervenções registradas, não apenas condições iniciais nem automaticamente como calibração posterior ao resultado. [Fonte, linha 515](../../structures/a-pocket-in-the-field/code/simulate_field_pocket.py) · [Fonte deste estudo, linha 290](code/teste_pancada.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
