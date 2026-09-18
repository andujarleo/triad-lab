[Lab](README.md) · [English](../en/contributing.md) · **Português**

# Ajude o lab a crescer

Comece por uma pergunta que alguém consiga entender antes de ler uma equação. Uma contribuição pode ser um estudo, uma execução nova, uma explicação, uma tradução ou uma correção.

## Adicione ou amplie um estudo

1. Escolha uma área existente em `experiments/` ou descreva uma nova nos índices dos dois idiomas.
2. Use uma pasta descritiva: `experiments/<area>/<study>/`. Mantenha estável o ID do catálogo, mesmo que o título mude.
3. Copie o [modelo de estudo](../../templates/experiment/README.pt-BR.md). Escreva a pergunta, o que observar na figura representativa, as evidências disponíveis e os limites conhecidos. Mantenha a entrada em inglês; aponte para o material técnico no idioma original quando não houver tradução.
4. Coloque implementações em `code/`, entradas explícitas em `configuration/`, relatórios em `notes/` e saídas registradas em `results/`. Novas execuções devem usar `results/<run-id>/{data,figures,logs}/`, evitando sobrescrever resultados. Crie pastas apenas quando houver conteúdo.
5. Atualize `FILES.md`, os índices da área e [catalog.json](../../experiments/catalog.json). As entradas existentes mostram o esquema: ID estável, pasta, área, títulos, documentação, disponibilidade e associações de origem. Um conteúdo compartilhado fica em um local, mantendo todas as associações.
6. Registre comando exato, diretório de trabalho, commit do código, dependências, hardware, parâmetros, sementes e hashes das entradas e saídas em [run.json](../../templates/run.json). Use `null` para valores indisponíveis e explique o motivo.

A disponibilidade no catálogo descreve material fornecido, não validade científica. Entradas `note-only` e `specification` podem não ter saídas; `recorded` e `recorded-artifacts` indicam saídas preservadas. `implementation-available` e `archival` exigem consultar as condições de execução da página. Os campos explícitos de `availability` indicam a presença de código, dados, figuras e notas.

## Preserve a comparação

Mudar uma equação, parâmetro, solver, backend ou entrada cria uma nova comparação. Preserve o registro anterior e documente a diferença. Mantenha resultados negativos e inconclusivos com seu contexto. Separe observações numéricas da interpretação que elas podem sustentar.

Os arquivos históricos listados no registro de proveniência têm hashes originais fixos. Não atualize esses hashes para esconder uma mudança. Acrescente uma implementação adaptada ou uma execução nova separadamente. Uma adaptação apenas de caminhos ainda pode mudar a seleção de arquivos ou o diretório de trabalho; verifique isso explicitamente.

## Revise uma contribuição

```sh
python3 -m unittest discover -s tools -p 'test_*.py'
python3 tools/check_repository.py
```

Baixe os arquivos pelo Git LFS antes, quando faltarem matrizes ou animações. Revise links locais, traduções e comandos alterados. Em mudanças de navegação, confira integridade em vez de reexecutar todas as simulações. Em mudanças numéricas, declare qual comparação foi realmente realizada.

Descreva problema, mudança final, validação e limites restantes no commit ou pull request. Inglês é a base editorial; atualize o português na mesma mudança. [Outros idiomas](languages.md) podem ser acrescentados sem duplicar implementações numéricas. O repositório não tem licença declarada; preserve a autoria e não invente uma licença.

[Próximos passos](roadmap.md)

## Preserve o ponto de partida

Apresente a TRIAD como proposta de física quântica não padrão. Vincule novas interpretações à leitura operacional do autor e ao regime realmente executado. Diferencie a tríade completa, os pilotos históricos e os controles; não transforme um diagnóstico de mecânica quântica convencional na definição de todo o projeto. [Referência de apresentação](triad.md).

O atlas público é gerado a partir do mesmo catálogo. Para acrescentar uma pergunta representativa, imagem ou campo salvo, siga o [contrato de dados do site](../maintenance/site-data.md). Ao alterar a interface, execute `node --test tools/frontend.test.mjs` e reconstrua o site conforme [web/README.md](../../web/README.md).
