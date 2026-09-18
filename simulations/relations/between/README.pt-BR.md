[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Relações](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# O entre

**O que pode ser medido na própria relação?**

Acrescenta medidas do “entre” à dinâmica relacional base, sem introduzir uma força nova.

## Material disponível

![O entre](results/figures/consciencia-emergida-no-entre.png)

- [consciencia-emergida-no-entre.png](results/figures/consciencia-emergida-no-entre.png)
- [consciencia-emergida-no-entre.gif](results/figures/consciencia-emergida-no-entre.gif)
- [consciousness-between-data.json](results/data/consciousness-between-data.json)
- [consciencia-entre-dados.json](results/data/consciencia-entre-dados.json)

## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
python simulations/relations/between/code/pt-BR/simulate_consciencia_entre.py
```

[English source](code/en/simulate_consciousness_between.py) · [Código em português](code/pt-BR/simulate_consciencia_entre.py)

## Leitura e continuidade

Os scripts usam 6.000 passos e `DT=0.02`. Novos arquivos vão para `artifacts/` ao lado do script. Os JSONs incluídos têm 25 amostras cada. Preserve a configuração e registre uma nova execução antes de comparar alterações.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

## Notas da implementação

Esses scripts relacionais evoluem fases e memória de arestas com RK4. As camadas opcionais de química e filtro de vida pertencem ao sistema relacional declarado. Seus seletores não devem ser descritos como termos nomeados da equação de campo completa da referência. [Fonte, linha 116](../observer/code/en/simulate_observer_observed_relations.py).

[Auditoria estática completa e referências das fontes](../../../docs/maintenance/author-rules-audit.md).
