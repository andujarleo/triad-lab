[English](README.md) · **Português** · [Catalog / Catálogo](../README.pt-BR.md)

# Escala própria

`bravais-03-scale` · bravais

**A beirada espectral acompanha o sistema ou o tamanho da caixa?**

Executa a mesma equação em caixas L=24, 32 e 48 com dx=0.5 fixo e grades de 48³, 64³ e 96³.

## Material disponível

O script está incluído; este snapshot não contém uma saída da varredura.


## Executar

[Prepare o ambiente](../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
MPLBACKEND=Agg python bravais/bravais_sweep_L.py
```

[English source](../../en/bravais/bravais_sweep_L.py) · [Código em português](../../bravais/bravais_sweep_L.py)

## Leitura e continuidade

O padrão é 800 passos por caixa; a caixa `96³` é a mais pesada. `STEPS` altera a duração da nova execução, não os resultados registrados. A inicialização não tem semente fixa. Saídas: `bravais_outputs_3d/sweep_L*.npz` e `sweep_verdict.png`.
