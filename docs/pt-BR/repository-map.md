[Lab](README.md) · [English](../en/repository-map.md) · **Português**

# Encontre seu caminho

O [lab interativo](https://andujarleo.github.io/triad-lab/?lang=pt-BR) é a entrada pública. O repositório conecta essa apresentação aos arquivos dos estudos, aos documentos de referência e aos registros por trás de cada imagem.

```text
README.md                         Entrada curta para qualquer leitor
experiments/
  relations/ … validation/        Oito áreas, cada uma com índice
    <study>/
      README.md                   Pergunta, contexto e limites conhecidos
      README.pt-BR.md             Apresentação em português
      FILES.md                    Todos os materiais associados
      code/                       Implementações preservadas
      configuration/              Configurações explícitas, quando fornecidas
      notes/                      Relatórios e protocolos históricos
      results/data/               Matrizes, tabelas e medidas registradas
      results/figures/            Gráficos e animações originais
      results/logs/               Registros de execução
      variants/<name>/code/       Implementações diferentes, quando necessário
  catalog.json                    Catálogo completo para ferramentas
docs/en/ · docs/pt-BR/            Visitas, glossário, regras do projeto e guias técnicos
docs/reference/
  equation/                       Documentos de referência v1.0/v1.1 e seu histórico
  concepts/ · records/ · solver/   Fontes originais da pesquisa
provenance/                       Origens, mapa de caminhos, hashes e auditoria
templates/                        Novos estudos e registros de execução
web/                              Interface pública e conteúdo bilíngue
tools/
  build_site.py                   Gera o site a partir do material preservado
  check_repository.py             Verifica integridade e navegação
  test_*.py · frontend.test.mjs    Testes de preservação e interface
_site/                            Site gerado, ignorado pelo Git
```

Pastas só existem quando contêm material. Uma tentativa registrada apenas em nota é um registro válido. Dentro de alguns estudos, subpastas mantêm grupos de diagnósticos ou execuções separados; juntar arquivos de nomes parecidos apagaria distinções.

**Um conteúdo tem um único local de armazenamento.** Se bytes idênticos apareceram em vários conjuntos, os índices dos estudos apontam para o mesmo arquivo. O catálogo mantém cada associação original. Arquivos com o mesmo nome e bytes diferentes continuam separados; nomes descritivos de variantes ou conjuntos de saída separados distinguem os arquivos. Os hashes ficam na proveniência, sem indicar uma ordem de versões.

O código traduzido que já existia permanece em `code/en/` e `code/pt-BR/`. Novas traduções acrescentam documentação, não cópias do código numérico. Os scripts originais ainda contêm seus caminhos históricos de entrada e saída; o [guia de execução](getting-started.md) distingue a consulta aos dados salvos da preparação de uma execução nova conforme as regras do projeto.

[Todos os estudos](../../experiments/README.pt-BR.md) · [Mapa de caminhos antigos e novos](../../provenance/layout-migration.json) · [Contribuir](contributing.md)

## O site público e o arquivo de pesquisa

A [documentação do site](../../web/README.md) explica o build, a prévia e a expansão de idiomas e módulos. A pasta `_site/` contém saídas geradas; a pesquisa original fica em `experiments/`. O [contrato de dados](../maintenance/site-data.md) especifica como matrizes e imagens salvas chegam ao visualizador.

O [índice da documentação de referência](../reference/equation/README.md) conecta os textos identificados como v1.1 e v1.0. São revisões documentais; a equação é imutável. As [regras do projeto](project-rules.md), a [página do autor](author.md), o [vocabulário](glossary.md) e o [diário](journal.md) dão contexto a quem está chegando.

## Exemplo real

```text
experiments/quantum/field-modes/
├── README.md
├── README.pt-BR.md
├── FILES.md
├── code/
│   └── analyze_field_modes.py
├── configuration/
│   └── config.json
├── notes/
│   ├── protocol.md
│   ├── mode-analysis-record.md
│   └── analysis.md
└── results/
    ├── data/
    │   └── seed-00/
    │       ├── leading-mode-early.npy
    │       └── explained-variance-early.npy
    ├── figures/
    └── logs/
```

Os identificadores T01–T39 e Q00–Q04 continuam na cronologia e no catálogo para rastreabilidade. As pastas usam o assunto do estudo. Valores de resolução, semente e tempo continuam nos nomes quando distinguem dados diferentes.
