![TRIAD — oscilação, autorreferência e acoplamento](../../assets/lab-header.pt-BR.svg)

<p align="center"><a href="../../README.md">English</a> · <strong>Português</strong><br />
<a href="https://andujarleo.github.io/triad-lab/?lang=pt-BR"><strong>ENTRE NO UNIVERSO ↗</strong></a> · <a href="../../research/README.pt-BR.md">Pesquisa</a> · <a href="../../simulations/README.pt-BR.md">Simulações</a> · <a href="start-here.md">Comece aqui</a></p>

# Universo TRIAD

**Física quântica não padrão. Uma ontologia de movimento, memória e relação.**

A TRIAD é o projeto de Leonardo Andujar. Sua ontologia coloca uma **equação imutável e indivisível** na base da realidade. **P1 oscilação, P2 autorreferência e P3 acoplamento atuam juntos.** O lab acompanha a dinâmica completa: autocalibração do caos ao equilíbrio dinâmico, com a cristalização continuando nesse equilíbrio.

Este é um universo vivo de pesquisa e simulações. Entre por uma imagem, acompanhe uma pergunta e alcance as fontes, a equação, o código e as trajetórias registradas.

<p align="center"><a href="../../simulations/geometry/field-visualizations/README.pt-BR.md"><img src="../../simulations/geometry/visual-comparisons/results/figures/phase-vortices-final-frame.png" width="760" alt="Visualização 3D original de vórtices de fase: ciano e rosa indicam sentidos opostos do enrolamento da fase nas regiões mais densas." /></a></p>

**Um campo, visto por dentro.** Um quadro original registrado, com seus rótulos preservados. [Veja a animação](../../simulations/geometry/field-visualizations/results/figures/cordas-fase-vivas.gif) · [Acompanhe sua origem](../../simulations/geometry/field-visualizations/README.pt-BR.md).

## Dois caminhos para explorar

| Pesquisa | Simulações |
|---|---|
| **Entenda as conexões.** Ontologia, memória, som, geometria, cognição e leituras culturais, com fontes e interpretação lado a lado. | **Acompanhe o que acontece.** Resultados visuais, trajetórias, implementações e condições registradas de 65 estudos em oito áreas. |
| [Abra a biblioteca de pesquisa →](../../research/README.pt-BR.md) | [Explore o acervo de simulações →](../../simulations/README.pt-BR.md) |

O [atlas interativo](https://andujarleo.github.io/triad-lab/?lang=pt-BR) conecta essas duas áreas por tema. O visualizador de campo mostra cortes espaciais de estados salvos; seu controle percorre o **espaço**.

## Comece pela sua curiosidade

| Quero entender | Quero investigar | Quero desenvolver ou executar |
|---|---|---|
| [Um passeio de cinco minutos](start-here.md), [fundamentos da TRIAD](triad.md) e [vocabulário acessível](glossary.md). | [Temas de pesquisa](../../research/README.pt-BR.md), [comparações registradas](execution-audit.md) e [referência da equação](../reference/equation/README.md). | [Mapa do repositório](repository-map.md), [orientação de execução](getting-started.md) e [como contribuir](contributing.md). |

## A dinâmica completa importa

Retirar um termo muda o sistema implementado. O acervo preserva essas configurações históricas e as identifica junto dos resultados. A [auditoria das execuções](execution-audit.md) liga cada estudo às suas condições e distingue mudanças registradas no comportamento de mudanças na medição ou na interpretação.

Trabalhos TRIAD novos seguem as [regras do projeto](project-rules.md): equação completa, ausência de calibração externa para obter um resultado desejado, ausência de isolamento de termos e de protocolo de falsificação popperiana. Números originais e resultados divergentes continuam visíveis. Documentos e implementações têm revisões; a equação é imutável.

## Dentro do universo

```text
research/       Temas, leituras, conexões e fontes de pesquisa preservadas
simulations/    Perguntas, código, configurações e resultados registrados
docs/           Guias em inglês e português; referências comuns da equação
provenance/     Origem, histórico de caminhos, integridade e auditoria
web/            A experiência pública
tools/          Catálogo, checagens de preservação e construção do site
templates/      Pesquisas, estudos e registros de execução
```

[Diário do lab](journal.md) · [Sobre Leonardo](author.md) · [Preservação das fontes](../../provenance/README.md) · [Adicionar um idioma](languages.md)

<details><summary>Verificar e explorar localmente</summary>

```sh
git lfs pull
python3 tools/check_repository.py
python3 -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/frontend.test.mjs
python3 tools/build_site.py
```

[Dependências e prévia](../../web/README.md) · [Mapa atual do repositório](repository-map.md) · [Caminhos anteriores](../../provenance/universe-migration.json)

</details>
