[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Cordas de um estado salvo

**Como inspecionar densidade, fase e modos espectrais como cordas?**

Faz o pós-processamento de um estado salvo em filamentos de densidade, curvas de fase quando disponíveis e cordas-nota espectrais.


## Auditoria da execução

**Contexto ou pós-processamento.** Pós-processamento de estados de campo salvos; esta entrada não evolui a equação completa.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-bravais-02-strings) · [cordas_arte.py](code/cordas_arte.py#L1)

## Material disponível

![Cordas de um estado salvo](results/figures/cordas-densidade.png)

- [cordas-densidade.png](results/figures/cordas-densidade.png)
- [final_state.npz](../field-3d/results/data/final_state.npz)

## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
MPLBACKEND=Agg python simulations/geometry/string-analysis/code/pt-BR/bravais_cordas.py simulations/geometry/field-3d/results/data/final_state.npz
```

[English source](code/en/bravais_strings.py) · [Código em português](code/pt-BR/bravais_cordas.py)

## Leitura e continuidade

O estado incluído contém `rho_f`, `v`, `ell`, `order` e `norm`, mas não `psi_f`. Por isso, o script pula as cordas de fase. O tamanho da caixa é assumido como `L=32`; para outro estado, informe seu tamanho real pela variável `L`. Esta etapa lê o estado e grava figuras em `bravais_outputs_3d/`, sem executar a dinâmica.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)
