[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md) · [Regras do projeto](../../../docs/pt-BR/project-rules.md)

# Escala própria

**A beirada espectral acompanha o sistema ou o tamanho da caixa?**

Usa a mesma implementação preservada em caixas L=24, 32 e 48 com dx=0.5 fixo e grades de 48³, 64³ e 96³. Suas atualizações cinética e de ruído diferem da referência da equação; a varredura compara essa implementação em diferentes tamanhos de caixa.


## Auditoria da execução

**Implementação divergente.** A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação.

[Condições e contrastes registrados](../../../docs/pt-BR/execution-audit.md#study-bravais-03-scale) · [bravais_sweep_L.py](code/pt-BR/bravais_sweep_L.py#L92) · [bravais_sweep_L.py](code/pt-BR/bravais_sweep_L.py#L175)

## Material disponível

A implementação original e saídas históricas da varredura estão incluídas. Consulte o índice completo abaixo.


## Implementação preservada

O comando abaixo chama a implementação preservada. Comece pelas [condições de execução](../../../docs/pt-BR/getting-started.md) e pela [auditoria das implementações](../../../docs/maintenance/author-rules-audit.md#português); mantenha novas saídas separadas do registro original. Execute da raiz do repositório em uma cópia de trabalho.

```sh
MPLBACKEND=Agg python simulations/geometry/scale-sweep/code/pt-BR/bravais_sweep_L.py
```

[English source](code/en/bravais_sweep_L.py) · [Código em português](code/pt-BR/bravais_sweep_L.py)

## Leitura e continuidade

O padrão é 800 passos por caixa; a caixa `96³` é a mais pesada. `STEPS` altera a duração da nova execução, não os resultados registrados. A inicialização não tem semente fixa. Saídas: `bravais_outputs_3d/sweep_L*.npz` e `sweep_verdict.png`.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

O acervo acrescenta duas figuras de veredito de varredura com conteúdos diferentes. Elas mantêm seus hashes e origens; não são saídas de uma nova execução deste script.
