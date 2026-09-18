<p align="center"><img src="../../assets/lab-header.svg" alt="TRIAD LAB — laboratório vivo de experimentos numéricos" width="100%" /></p>

[English](../../README.md) · **Português**

# Um laboratório vivo

**Explorar relações, memória e estruturas emergentes — com código, dados e resultados lado a lado.**

TRIAD Lab reúne séries independentes de experimentos numéricos de Leonardo Andujar. Cada entrada do catálogo liga uma pergunta à implementação e aos registros disponíveis. O laboratório cresce por novas séries e execuções, preservando o que já foi registrado.

**[Explorar experimentos](../../experiments/README.pt-BR.md) · [Executar localmente](getting-started.md) · [Ver a galeria](gallery.md) · [Contribuir](contributing.md)**

## Explore o laboratório

| Série | O que explora | Percurso |
|---|---|---|
| **Entre** | Osciladores acoplados, memória nas relações e camadas contínuas | [4 experimentos](../../experiments/entre-01-observer/README.pt-BR.md) |
| **Bravais 3D** | Campo complexo, geometria espacial e estrutura espectral | [3 experimentos](../../experiments/bravais-01-field/README.pt-BR.md) |
| **Acervo T** | 39 runs, sequência QM e explorações de campo, geometria e continuidade | [7 percursos de leitura](../../collections/t-archive/README.pt-BR.md) |

![Cortes do estado Bravais salvo](../../bravais/resultados/pure_final_slices.png)

*Figura original preservada. As imagens existentes mantêm seus rótulos em português.*

## Escolha uma entrada

- **Ler:** abra o [catálogo](../../experiments/README.pt-BR.md); cada página liga pergunta, código, dados e imagens.
- **Executar:** siga o [guia local](getting-started.md), começando pelo pós-processamento de um estado salvo.
- **Expandir:** use o [modelo de experimento](../../templates/experiment/README.pt-BR.md) para registrar uma nova investigação.
- **Traduzir:** consulte o [guia de idiomas](languages.md); inglês é a base editorial, português é a primeira tradução.

## Como o laboratório se organiza

```text
collections/       Acervos históricos, índices e proveniência
experiments/       Catálogo e páginas; novos experimentos crescem aqui
docs/en/           Guias de leitura, execução e contribuição em inglês
docs/pt-BR/        Guias equivalentes em português
templates/         Modelos de experimento e registro de execução
entre/             Scripts originais em português, dados e figuras
bravais/           Scripts originais, estado salvo e figuras
en/                Scripts e dados existentes em inglês
```

Os caminhos históricos continuam válidos. Experimentos novos usam uma implementação compartilhada e documentação por idioma; as traduções existentes são preservadas. [Convenções e evolução](contributing.md).

## Continuidade

Scripts, configurações e resultados originais foram preservados. Confira os hashes com:

```sh
shasum -a 256 -c docs/archive/SHA256SUMS
# Acervo T (após git lfs pull):
shasum -a 256 -c collections/t-archive/SHA256SUMS
```

[Próximos passos](roadmap.md) · [Histórico da organização](../../CHANGELOG.md) · [Registro original](../../docs/archive/README.md)
