[Início](README.md) · [English](../en/languages.md) · **Português**

# Idiomas

Inglês é a base da nova documentação editorial; português brasileiro é a primeira
tradução mantida. Isso não muda o idioma nem a autoridade das fontes históricas.
As figuras e os dados salvos mantêm seus rótulos originais.

| Idioma | Entrada | Cobertura |
|---|---|---|
| English (`en`) | [Home](../../README.md) | Início, catálogo, sete experimentos, guias e 45 fichas do acervo T |
| Português (`pt-BR`) | [Início](README.md) | Início, catálogo, sete experimentos, guias e 45 fichas do acervo T |

## Acrescentar um idioma

1. Use uma etiqueta como `es` ou `fr`; crie `docs/<tag>/README.md`.
2. Traduza primeiro a entrada e o catálogo; para páginas ausentes, ofereça o inglês.
3. Use `experiments/<id>/README.<tag>.md` para as páginas. Preserve IDs, caminhos,
   equações, unidades e dados. Traduza as explicações, não os resultados registrados.
4. Acrescente idioma e cobertura real a [languages.json](../languages.json), a esta
   tabela e aos seletores. Acrescente as páginas disponíveis ao `catalog.json`.
5. Inclua `<!-- Translation of: path; source commit: SHA -->` nas novas traduções.
   Registre o commit em inglês efetivamente traduzido, sem adivinhar uma revisão.
6. Ao mudar o inglês, atualize as traduções na mesma pull request ou marque-as
   visivelmente como aguardando sincronização. Traduções parciais ligam para a fonte.

A documentação inicial em inglês e português foi escrita em conjunto. Atualizações
posteriores devem registrar a revisão de origem. O README arquivado e as traduções
de código existentes são anteriores a esta convenção.

## Uma implementação para novos experimentos

Os scripts de `en/`, `entre/` e `bravais/` foram mantidos. Novos idiomas acrescentam
documentação e, quando houver suporte, rótulos separados. Não copie implementações
numéricas por idioma. Unificar os scripts existentes é uma mudança separada, que
pode afetar comportamento, e não faz parte de uma tradução.

O acervo T tem apresentação, percursos, 39 fichas cronológicas e seis fichas QM em ambos os idiomas. Os documentos históricos na edição de leitura mantêm o idioma original; não são traduções. Índices de arquivos usam rótulos nos dois idiomas.
