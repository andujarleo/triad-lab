[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Memória](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Memória com amplitude pequena

Run gaussiano N96, seed 42, nos parâmetros R5/FDT declarados; picos finitos no intervalo registrado.

Registro histórico importado; esta organização não reexecutou a simulação.

[Ler a nota original](notes/original-record.md) · [Todos os arquivos](FILES.md)

[Script preservado](code/simulate_memory_small_amplitude.py) · [Dependências e portabilidade](../../../provenance/t-archive/dependencies.pt-BR.md)

![Figura original do run](results/figures/overview.png)


## Auditoria da execução

> **Identidade TRIAD: NÃO é TRIAD completa — divergência documentada.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-t-29) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-t-29) · [Español](../../../docs/es/triad-identity-audit.md#study-t-29) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-t-29) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-t-29) · [Norsk](../../../docs/no/triad-identity-audit.md#study-t-29) · [Dansk](../../../docs/da/triad-identity-audit.md#study-t-29) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-t-29)

**Implementação divergente.** A rodada fixa alpha=0 e usa dois modos de memória; seu banho está ativo.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-t-29) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L2) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L27) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L189) · [simulate_memory_small_amplitude.py](code/simulate_memory_small_amplitude.py#L213)

## Material disponível

10 arquivos associados à ficha: 2 `.csv`, 1 `.json`, 1 `.md`, 6 `.png`.

[Cronologia](../../../docs/pt-BR/topics/timeline.md) · [← 28](../../structures/3d-atom-trajectories/README.pt-BR.md) · [30 →](../../structures/two-atoms/README.pt-BR.md)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O runner tem `ALPHA=0` e dois modos de memória, com banho ativo (`GAMMA=0.01`, `T_BATH=0.001`). O ramo fracionário está desligado nesta implementação; o nome histórico não substitui esses valores declarados. [Fonte, linha 2](code/simulate_memory_small_amplitude.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
