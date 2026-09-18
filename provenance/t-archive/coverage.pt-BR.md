[English](coverage.md) · **Português** · [Acervo](../../docs/pt-BR/history.md)

# Cobertura e integridade

Fonte: `T.zip`, fornecido pelo autor. A leitura incluiu os dois ZIPs internos. O arquivo original não foi modificado.

- SHA-256: `30276c2f96779ed1923612e82a323b06f88d00b1900272df919799c4791eee26`
- Bytes: `437576946`

| Categoria | Quantidade | Destino |
|---|---:|---|
| Entradas de arquivo / File entries | 2,779 | Indexadas / Indexed |
| Conteúdo / Content | 1,330 | Preservado / Preserved |
| Conteúdos distintos / Distinct contents | 1,140 | SHA-256 |
| Metadados macOS / macOS metadata | 1,445 | Indexados, excluídos / Indexed, excluded |
| Caches Python / Python caches | 2 | Indexados, excluídos / Indexed, excluded |
| ZIPs internos / Nested ZIPs | 2 | Conteúdo expandido / Contents expanded |

Os nomes foram normalizados para UTF-8/NFC; o manifesto mantém também os nomes decodificados originalmente pelo leitor ZIP. Conteúdos idênticos continuam em seus caminhos para preservar relações locais. Git e LFS identificam esses conteúdos por hash.

## O que foi inspecionado

Todos os 1.140 conteúdos distintos passaram por leitura técnica. Os 60 scripts Python foram analisados por AST; documentos e arquivos estruturados foram lidos por completo pelos parsers; os 561 PNGs e 10 GIFs foram decodificados, incluindo todos os frames. A revisão visual percorreu 17 pranchas com todos os PNGs e amostras inicial, intermediária e final dos GIFs. NPY/NPZ foram carregados sem pickle.

Não houve erro de formato nessa inspeção. Os arrays inspecionados não continham NaN ou infinito. Oito CSVs contêm valores não finitos em campos de diagnóstico; eles permanecem intactos e aparecem no relatório técnico. Isso não equivale a reproduzir as simulações, certificar a metodologia ou validar cada conclusão científica.

## Discrepâncias preservadas

Q00 cita SHA-256 `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` para o canônico. O arquivo `TRIAD_QM_CANONICAL_V1.md` recebido tem SHA-256 `f9c23b3d74554beabca7ce8c578b0fb31fdc5b14943ed053596f4962f82273f1`. Não há evidência suficiente neste acervo para explicar a diferença; a referência histórica e o arquivo foram preservados, sem declarar equivalência.

[Q00](../../simulations/field-diagnostics/reference-specification/notes/specification-record.md) · [Canonical](../../docs/reference/records/triad-qm-canonical-v1.md)

[Manifesto completo](manifest.json) · [Inspeção por arquivo](inspection.json) · [SHA-256 dos arquivos](SHA256SUMS) · [Versões](versions.md)

O ZIP também contém 117 entradas de diretório, registradas em [directories.json](directories.json). Diretórios vazios e metadados de diretório ficam representados nesse índice; não precisam de arquivos artificiais para existir no histórico.
