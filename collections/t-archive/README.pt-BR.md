[English](README.md) · **Português** · [TRIAD Lab](../../docs/pt-BR/README.md)

# Um mapa para o acervo T

**Campo → memória → estrutura → continuidade.** Um percurso pelas perguntas, simulações e imagens que formaram este acervo.

**39 runs numerados · 6 etapas QM · 1.330 arquivos · 1.140 conteúdos distintos**

O material veio do `T.zip` entregue pelo autor. Aqui ele ganha navegação por assunto, fichas em inglês e português e ligações entre notas, código, dados e figuras. As fontes mantêm seus bytes e seu idioma original.

| Percurso | O que você encontra |
|---|---|
| **[39 runs, uma cronologia](guides/timeline.pt-BR.md)** | Dos primeiros campos a estruturas aninhadas, diagnósticos e dossiês de reexecução. |
| **[A sequência QM](guides/quantum.pt-BR.md)** | Especificação congelada, convergência, ensembles, subespaços e linearidade. |
| **[Geometria, cordas e visualização](guides/bravais.pt-BR.md)** | Ramificações 2D/3D, estrutura espectral, perturbações, animações e estados salvos. |
| **[R5 passivo](guides/passive-r5.pt-BR.md)** | Run N64 separado, com snapshots, checkpoints e registros de sensibilidade. |
| **[Continuidade causal](guides/causal-continuity.pt-BR.md)** | Rastros de campo, tubos de mundo e controles de fundo pareados. |
| **[Um universo persistente](guides/persistent-universe.pt-BR.md)** | Protótipo de estado modal, continuidade por checkpoint e leituras passivas. |
| **[Fundamentos e proveniência](guides/foundations.pt-BR.md)** | Notas conceituais, equação de referência, fontes e registros históricos. |

## Comece pelas figuras

| Convergência | Estado persistente |
|---|---|
| ![Refinamento temporal / Timestep refinement](source/QM/Q01b_dt_N/figures/dt_refine_N64.png) | ![Estado modal / Modal state](source/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/outputs/04_final_full_modal_slices.png) |

*Figuras originais preservadas. O valor está no vínculo com a montagem e os dados de cada estudo.*

## Como ler

1. Escolha uma linha de pesquisa acima.
2. Abra a ficha do run e depois sua nota, protocolo ou análise.
3. Consulte dados e código pelo índice de arquivos.
4. Confira proveniência e dependências antes de tentar reproduzir.

Os runs 06, 11, 14 e 15 registram tentativas sem artefatos. Falhas, resultados inconclusivos e diagnósticos posteriormente refinados continuam visíveis. A organização não reexecutou nem reclassificou os estudos.

## Baixar e verificar

Os arrays NumPy e as animações deste acervo usam Git LFS. Na raiz do repositório:

```sh
git lfs install
git lfs pull --include="collections/t-archive/**"
shasum -a 256 -c collections/t-archive/SHA256SUMS
```

[Todos os arquivos](files/README.md) · [Integridade e cobertura](provenance/coverage.pt-BR.md) · [Portabilidade](provenance/dependencies.pt-BR.md) · [Versões](provenance/versions.md) · [Catálogo JSON](catalog.json)

Para expandir o lab, crie novos experimentos com IDs estáveis e documentos por idioma. Use este acervo como referência preservada; registre novos runs em seus próprios diretórios. Veja o [guia de contribuição](../../docs/pt-BR/contributing.md).
