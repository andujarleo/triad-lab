[English](README.md) · **Português** · [Catalog / Catálogo](../README.pt-BR.md)

# Campo 3D emergente

`bravais-01-field` · bravais

**Que estrutura espacial e espectral emerge da evolução acoplada?**

Evolui um campo complexo em uma grade 3D periódica, com FFTs, uma proposta acoplada e ponto fixo implícito.

## Material disponível

![Campo 3D emergente](../../bravais/resultados/pure_final_slices.png)

- [pure_final_slices.png](../../bravais/resultados/pure_final_slices.png)
- [final_state.npz](../../bravais/final_state.npz)

## Executar

[Prepare o ambiente](../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
MPLBACKEND=Agg python bravais/bravais_puro_3d.py
```

[English source](../../en/bravais/bravais_pure_3d.py) · [Código em português](../../bravais/bravais_puro_3d.py)

## Leitura e continuidade

A configuração padrão usa `N=64`, `L=32`, 1.200 passos e `dt=0.025`. A inicialização aleatória não tem semente fixa. Uma nova execução não recria exatamente o estado incluído. Resultados novos vão para `bravais_outputs_3d/` no diretório de execução.
