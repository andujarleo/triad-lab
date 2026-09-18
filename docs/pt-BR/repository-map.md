[Lab](README.md) · [English](../en/repository-map.md) · **Português**

# Encontre seu caminho

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
docs/en/ · docs/pt-BR/            Visitas, glossário e guias técnicos
docs/reference/                   Conceitos, registros e solver originais
provenance/                       Origens, mapa de caminhos, hashes e auditoria
templates/                        Novos estudos e registros de execução
tools/check_repository.py         Checagens de integridade e navegação
```

Pastas só existem quando contêm material. Uma tentativa registrada apenas em nota é um registro válido. Dentro de alguns estudos, subpastas mantêm grupos de diagnósticos ou execuções separados; juntar arquivos de nomes parecidos apagaria distinções.

**Um conteúdo tem um único local de armazenamento.** Se bytes idênticos apareceram em vários conjuntos, os índices dos estudos apontam para o mesmo arquivo. O catálogo mantém cada associação original. Arquivos com o mesmo nome e bytes diferentes continuam separados; nomes descritivos de variantes ou conjuntos de saída separados distinguem os arquivos. Os hashes ficam na proveniência, sem indicar uma ordem de versões.

O código traduzido que já existia permanece em `code/en/` e `code/pt-BR/`. Novas traduções acrescentam documentação, não cópias do código numérico. Os scripts originais ainda contêm seus caminhos históricos de entrada e saída; o [guia de execução](getting-started.md) explica o que pode ser executado diretamente.

[Todos os estudos](../../experiments/README.pt-BR.md) · [Mapa de caminhos antigos e novos](../../provenance/layout-migration.json) · [Contribuir](contributing.md)

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
