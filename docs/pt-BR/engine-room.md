[Lab](README.md) · [English](../en/engine-room.md) · **Português**

# A sala de máquinas

A porta dev: contratos, comandos e os caminhos para modificar o lab. As páginas públicas seguem legíveis; esta página guarda o maquinário.

## Contratos: o que mora onde

| Diretório | Guarda | Jamais guarda |
|---|---|---|
| `research/` | Temas, leituras, fontes preservadas | Execuções numéricas |
| `simulations/` | Estudos: código, configurações, saídas registradas | Fontes duplicadas entre temas |
| `docs/` | Guias em inglês e português; referências comuns | Novos resultados numéricos |
| `provenance/` | Identidade, hashes, migrações, registros de auditoria | Ciência nova |
| `web/` | Fontes do site público | Saída gerada (`_site/`) |
| `tools/` | Checagens, testes, construção do site | Código de simulação |
| `templates/` | Modelos de pesquisa, estudo e execução | Registros preenchidos |
| `assets/brand/` | Símbolo e capas, com bytes preservados | Figuras de resultado |

## Os cinco comandos

Execute da raiz do repositório:

```sh
git lfs pull
python3 tools/check_repository.py
python3 -B -m unittest discover -s tools -p 'test_*.py'
node --test tools/frontend.test.mjs
python3 tools/build_site.py
python3 -m http.server 8000 --directory _site
```

[Dependências e prévia](../../web/README.md) · [Contrato de dados do site](../maintenance/site-data.md)

## Modificando o lab

- **Estudo novo** — use o [modelo de estudo](../../templates/experiment/README.pt-BR.md): páginas bilíngues, `FILES.md`, entrada no catálogo, links de auditoria. [Como contribuir](contributing.md)
- **Edição nova** — siga o [fluxo de edição](editions.md): destaques com registros, narrativas de um minuto, capa nos dois idiomas.
- **Idioma novo** — siga [Adicionar um idioma](languages.md); traduções da auditoria primeiro, integridade do catálogo sempre.
- **Veredito novo** — atualize a [auditoria de identidade](triad-identity-audit.md) e o `rule_audit` do estudo juntos.

## Regras que mordem

- Inglês e português andam juntos; a lista integral do catálogo segue só com idiomas completos.
- Bytes preservados nunca são editados — o verificador impõe. Páginas mantidas explicam; não reescrevem fontes.
- Introduções de estudo alimentam o site: mantenha pergunta e resumo de abertura primeiro. [Leitura em camadas](reading-layers.md)
- Nunca duplique código numérico por idioma; código novo vai ao lado do material preservado, com registro de mudança.

[Mapa do repositório](repository-map.md) · [Orientação de execução](getting-started.md) · [Como contribuir](contributing.md) · [Voltar à capa](README.md)
