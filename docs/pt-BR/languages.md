[Lab](README.md) · [English](../en/languages.md) · **Português**

# Idiomas

Inglês é a base da documentação editorial; português brasileiro é a primeira tradução mantida. As 65 apresentações de estudos, os oito índices de área e os guias públicos existem nos dois idiomas. Documentos científicos, figuras e código históricos mantêm seus idiomas e rótulos originais.

| Idioma | Entrada |
|---|---|
| English | [Home](../../README.md) |
| Português | [Início](README.md) |

As traduções preservam as [regras do projeto](project-rules.md): física quântica não padrão, equação imutável e indivisível, os três princípios e auto-organização dinâmica. Descreva v1.0/v1.1 como revisões documentais. Mantenha resultados históricos e seu contexto em todos os idiomas.

## Acrescente um idioma

1. Use uma tag como `es` ou `fr` e crie `docs/<tag>/README.md`.
2. Traduza a entrada, a visita e o catálogo primeiro. Aponte para o inglês onde ainda faltar tradução.
3. Use `simulations/<area>/<study>/README.<tag>.md` nas páginas dos estudos e índices das áreas. Preserve IDs, caminhos, equações, unidades e valores.
4. Registre a cobertura real em `docs/languages.json` e acrescente apenas as páginas existentes ao catálogo e aos seletores de idioma. Não acrescente uma tradução parcial à lista de idiomas integralmente mantidos do catálogo.
5. Registre a revisão traduzida com `<!-- Translation of: path; source commit: SHA -->`. Não invente o SHA. As páginas atuais em inglês e português foram escritas juntas.
6. Atualize traduções junto da base ou sinalize visivelmente que aguardam sincronização.

Novos idiomas acrescentam explicações. Não duplique o código numérico para cada idioma. As variantes traduzidas que já existiam foram preservadas em `code/en/` e `code/pt-BR/`.

O site interativo possui [pontos próprios de tradução](../../web/README.md). Amplie em conjunto os textos da interface, conceitos, alternativas do catálogo e seletor de idioma; verifique rótulos longos e URLs compartilhadas no novo idioma.
