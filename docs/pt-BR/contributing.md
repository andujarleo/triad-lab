[Início](README.md) · [English](../en/contributing.md) · **Português**

# Expandir o laboratório

Uma contribuição pode ser um experimento, uma execução adicional, uma explicação,
uma tradução ou uma correção. Mantenha pergunta, implementação, observações e
interpretação do autor conectadas e distinguíveis.

## Adicionar um experimento

1. Escolha uma série existente ou apresente uma nova com uma descrição curta.
2. Dê um ID estável em minúsculas, como `series-01-topic`.
3. Copie os modelos em [inglês](../../templates/experiment/README.md) e
   [português](../../templates/experiment/README.pt-BR.md) para `experiments/<id>/`.
   Substitua os campos; só crie a página traduzida quando ela estiver pronta.
4. Mantenha uma implementação em `src/`, entradas explícitas em `configs/` e
   registros selecionados em `results/<run-id>/` dentro do experimento. Crie pastas
   quando houver conteúdo; uma proposta não precisa de pastas de código vazias.
5. Acrescente ID, série, títulos, documentação, scripts e artefatos ao
   [catalog.json](../../experiments/catalog.json) e atualize os dois catálogos de leitura.
6. Inclua a pergunta e uma imagem representativa no guia pertinente quando útil.

Séries novas não exigem mudar o código numérico do laboratório. Use nomes descritivos;
os caminhos atuais de Entre e Bravais continuam válidos. Os scripts existentes
permanecem nos caminhos históricos, ligados às páginas dos experimentos.

## Registrar uma execução

Use [run.json](../../templates/run.json). Registre commit e comando exatos, ambiente,
parâmetros, caminhos e hashes das entradas, artefatos gerados e resultado. Use `null`
quando um valor não estiver disponível e explique nas notas; não invente semente,
versão ou medida. Guarde resultados negativos, parciais e falhos com seu contexto.
Use IDs de execução distintos e nunca sobrescreva dados publicados para fazer
uma execução posterior concordar com eles.

O `status` do catálogo descreve material disponível: `proposed`,
`implementation-available` ou `recorded`. Não é uma classificação de validade
científica. Use `recorded` quando houver um artefato incluído ou explicitamente ligado.

## Preservar a continuidade

Mudar equação, parâmetro, método numérico ou fonte de dados cria uma comparação
nova a documentar. Mantenha o registro anterior acessível. Separe observações
numéricas da interpretação que sustentam. Traduções editoriais preservam equações,
valores de parâmetros e qualificações.

Confira links relativos, as duas entradas de idioma e os comandos alterados.
Para mudanças apenas na navegação, confira a base preservada sem executar todas
as simulações novamente:

```sh
shasum -a 256 -c docs/archive/SHA256SUMS
```

Não atualize os hashes da base para esconder uma alteração no original. Acrescente
uma versão ou resultado com proveniência própria. O [arquivo](../archive/README.md)
registra a base.

## Pull requests

Descreva a pergunta ou dificuldade de uso, a mudança, a verificação e os limites
da execução. Separe alterações editoriais das mudanças de comportamento experimental.
Atualize traduções ou marque as afetadas como pendentes de sincronização.
O snapshot atual não tem arquivo de licença; preserve a autoria e não invente uma.

## Expandir um estudo do acervo

Mantenha `collections/t-archive/source/` imutável. Crie o novo estudo em `experiments/<id>/`, vincule a ficha de origem e registre os hashes usados. Adaptações de caminhos, dependências ou backend devem ter seu próprio registro de mudança e validação. Documente novos resultados como novos runs; atualize as entradas em inglês e português juntas.
