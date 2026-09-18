[Lab](../../../docs/pt-BR/README.md) · [English](README.md) · **Português**

[Geometria](../README.pt-BR.md) · [Glossário](../../../docs/pt-BR/glossary.md)

# Campo 3D emergente

**Que estrutura espacial e espectral emerge da evolução acoplada?**

Evolui um campo complexo em uma grade 3D periódica, com FFTs, uma proposta acoplada e ponto fixo implícito.

## Material disponível

![Campo 3D emergente](results/figures/final-density-slices.png)

- [final-density-slices.png](results/figures/final-density-slices.png)
- [final_state.npz](results/data/final_state.npz)

## Executar

[Prepare o ambiente](../../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
MPLBACKEND=Agg python experiments/geometry/field-3d/code/pt-BR/bravais_puro_3d.py
```

[English source](code/en/bravais_pure_3d.py) · [Código em português](code/pt-BR/bravais_puro_3d.py)

## Leitura e continuidade

A configuração padrão usa `N=64`, `L=32`, 1.200 passos e `dt=0.025`. A inicialização aleatória não tem semente fixa. Uma nova execução não recria exatamente o estado incluído. Resultados novos vão para `bravais_outputs_3d/` no diretório de execução.

## Arquivos e condições de execução

[Índice completo dos materiais](FILES.md) · [Guia técnico](../../../docs/pt-BR/research-guide.md)

## Implementações preservadas

- [Checkpoints com fase](variants/phase-checkpoints/README.pt-BR.md)
- [Memória com sinal e execução padrão mais curta](variants/signed-memory-short-run/README.pt-BR.md)
