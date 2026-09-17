[English](README.md) · **Português** · [Catalog / Catálogo](../README.pt-BR.md)

# Cordas de um estado salvo

`bravais-02-strings` · bravais

**Como inspecionar densidade, fase e modos espectrais como cordas?**

Faz o pós-processamento de um estado salvo em filamentos de densidade, curvas de fase quando disponíveis e cordas-nota espectrais.

## Material disponível

![Cordas de um estado salvo](../../bravais/resultados/cordas_densidade.png)

- [cordas_densidade.png](../../bravais/resultados/cordas_densidade.png)
- [final_state.npz](../../bravais/final_state.npz)

## Executar

[Prepare o ambiente](../../docs/pt-BR/getting-started.md) e execute da raiz do repositório.

```sh
MPLBACKEND=Agg python bravais/bravais_cordas.py bravais/final_state.npz
```

[English source](../../en/bravais/bravais_strings.py) · [Código em português](../../bravais/bravais_cordas.py)

## Leitura e continuidade

O estado incluído contém `rho_f`, `v`, `ell`, `order` e `norm`, mas não `psi_f`. Por isso, o script pula as cordas de fase. O tamanho da caixa é assumido como `L=32`; para outro estado, informe seu tamanho real pela variável `L`. Esta etapa lê o estado e grava figuras em `bravais_outputs_3d/`, sem executar a dinâmica.
