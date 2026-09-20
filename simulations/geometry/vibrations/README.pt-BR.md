[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Cordas e vibração

**Como curvas extraídas do campo mudam no tempo?**

Um script evolui o campo enquanto registra cordas e modos espectrais; o outro reconstrói movimento a partir de um estado final salvo. Suas figuras mantêm essas origens distintas. Aqui, cordas são curvas extraídas do campo.

![Figura histórica preservada](results/figures/cordas-comprimento.png)



## Auditoria da execução

> **Identidade TRIAD: NÃO é TRIAD completa — divergência documentada.**
>
> Registro ponto a ponto: [English](../../../docs/en/triad-identity-audit.md#study-vibrations) · [Português](../../../docs/pt-BR/triad-identity-audit.md#study-vibrations) · [Español](../../../docs/es/triad-identity-audit.md#study-vibrations) · [Deutsch](../../../docs/de/triad-identity-audit.md#study-vibrations) · [Svenska](../../../docs/sv/triad-identity-audit.md#study-vibrations) · [Norsk](../../../docs/no/triad-identity-audit.md#study-vibrations) · [Dansk](../../../docs/da/triad-identity-audit.md#study-vibrations) · [中文（简体）](../../../docs/zh-CN/triad-identity-audit.md#study-vibrations)

**Implementação divergente.** A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. O leitor separado bravais_vibracoes é uma reconstrução cinemática.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-vibrations) · [bravais_cordas_vibracoes.py](code/bravais_cordas_vibracoes.py#L93) · [bravais_cordas_vibracoes.py](code/bravais_cordas_vibracoes.py#L173)

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

Os arquivos mantêm a implementação e as condições registradas. Consulte a [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português) para as diferenças documentadas e o registro de dependências abaixo antes de preparar uma nova execução.

[Dependências e entradas ausentes](../../../provenance/t-archive/dependencies.pt-BR.md)

## Notas da implementação

O renderizador de vibrações reconstrói movimento a partir de um estado final salvo e de modos espectrais selecionados, usando `omega=|k|²/2`. Esse movimento renderizado é pós-processamento, não outra integração da dinâmica completa. [Fonte, linha 5](code/bravais_vibracoes.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
