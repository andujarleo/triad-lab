[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Estruturas](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Dois bolsos

Bolsos plantados de sinais opostos e suas métricas salvas; a persistência não foi estabelecida no registro.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

[Script preservado](code/simulate_two_field_pockets.py) · [Dependências e portabilidade](../../../provenance/t-archive/dependencies.pt-BR.md)

## Material disponível

3 arquivos associados à ficha: 1 `.csv`, 1 `.json`, 1 `.md`.

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 37](../a-pocket-in-the-field/README.pt-BR.md) · [39 →](../density-memory-maps/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

Alguns protocolos arquivados acrescentam uma entrada durante a evolução: os estudos de bolsos inserem campos gaussianos no instante declarado `T_PLANT=0.5`; o script de impacto aplica uma perturbação declarada no pico do campo. Leia essas operações como intervenções registradas, não apenas condições iniciais nem automaticamente como calibração posterior ao resultado. [Fonte, linha 515](../a-pocket-in-the-field/code/simulate_field_pocket.py) · [Fonte deste estudo, linha 107](code/simulate_two_field_pockets.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
