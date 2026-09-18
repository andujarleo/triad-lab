[Universo](../../README.md) · [English](../en/repository-map.md)

# Mapa do repositório

Pesquisa e simulações têm lugares separados. Os temas as conectam por IDs do catálogo, mantendo um único conjunto de arquivos para cada estudo.

```text
research/
  <theme>/README.md · README.pt-BR.md
  foundations/                    Leitura comum dos princípios TRIAD
  sources/author-supplied/         Documentos recebidos com bytes preservados
  catalog.json · sources/catalog.json
simulations/
  <area>/<study>/
    README.md · README.pt-BR.md    Pergunta, interpretação e auditoria
    FILES.md                      Todo o material associado
    code/ · configuration/        Implementação e entradas preservadas
    notes/                        Relatórios e protocolos de origem
    results/data/                 Arrays e tabelas registrados
    results/figures/ · results/logs/       Imagens, animações e logs de execução
    variants/                     Implementações distintas preservadas
  catalog.json                    Estudos, fontes e auditoria
docs/en/ · docs/pt-BR/             Passeios, método e guias técnicos
docs/reference/                   Documentos da equação e registros autorais
provenance/                       Hashes das fontes e migrações
assets/ · web/                    Apresentação e site público
tools/ · templates/               Verificação, construção e contribuição
```

Cada estudo mantém seu ID existente. As pastas usam nomes descritivos; grade, semente e tempo permanecem quando distinguem dados. Bytes de origem idênticos têm um único lugar de armazenamento e múltiplas associações. Implementações e resultados diferentes continuam distintos.

`docs/reference/` é compartilhado: alguns registros autorais combinam ontologia, algoritmos e resultados. Permanecem íntegros e recebem ligações das duas áreas. Os rótulos v1.0/v1.1 identificam revisões documentais de uma única equação imutável.

A árvore anterior `experiments/` agora é `simulations/`. `quantum/` tornou-se `field-diagnostics/`, e `validation/` tornou-se `numerical-checks/`; os IDs do catálogo continuam estáveis. URLs antigas de arquivos no GitHub podem ser recuperadas pelo mapa de caminhos e seu commit de base. Âncoras do site e filtros de estudos continuam disponíveis.

[Pesquisa](../../research/README.pt-BR.md) · [Simulações](../../simulations/README.pt-BR.md) · [Auditoria](execution-audit.md) · [Mapa de caminhos](../../provenance/universe-migration.json) · [Proveniência](../../provenance/README.md)
