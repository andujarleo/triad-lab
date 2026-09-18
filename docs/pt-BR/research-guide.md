[Lab](README.md) · [English](../en/research-guide.md) · **Português**

# Examine o experimento por trás da figura

Comece pela [identidade e leitura operacional da TRIAD](triad.md) e pelas [regras do projeto](project-rules.md). A TRIAD é física quântica não padrão. Sua metodologia lê a dinâmica completa e acoplada; os diagnósticos históricos não definem essa identidade.

Para novas execuções, declare a [revisão do documento de referência](../reference/equation/README.md), a revisão da implementação e a configuração. A equação é única, imutável e indivisível. Os controles históricos mantêm seu contexto original; configurações com termos desligados não são renomeadas como execuções completas da TRIAD. O índice registra diferenças na escrita recebida, não versões da equação.

Comece pela pergunta do estudo e pelo **FILES.md**, depois siga protocolo → configuração → código → resultado registrado → interpretação. O [catálogo JSON](../../experiments/catalog.json) lista os 65 estudos, suas páginas bilíngues e cada arquivo original associado.

## O que o registro permite afirmar

O repositório preserva código numérico e dados por SHA-256. Nos documentos originais, apenas a sintaxe dos links foi normalizada, com alterações reversíveis. Isso estabelece continuidade do registro recebido. Não estabelece que todas as execuções históricas possam ser repetidas em uma máquina nova.

Os scripts iniciais têm um [guia de execução local](getting-started.md). O material posterior inclui Apple MLX, infraestrutura TriadLang parcial, caminhos absolutos e entradas ausentes. Leia a [auditoria de dependências](../../provenance/t-archive/dependencies.pt-BR.md) antes de escolher um ambiente. Nenhum lockfile do ambiente original foi recuperado.

## Comparações que exigem atenção

- **Três implementações 3D:** `bravais_puro_3d.py` tem três hashes distintos. Continuam separadas no [estudo de campo](../../experiments/geometry/field-3d/FILES.md); o identificador de hash não indica uma versão mais nova ou melhor.
- **Estados salvos diferentes:** o `final_state.npz` inicial não tem `psi_f`; outro estado arquivado inclui esse campo. O pós-processamento de fase depende dele.
- **Inicialização aleatória:** os scripts iniciais de evolução 3D e varredura não fixam a semente por padrão. Os registros não devem ser descritos como exatamente reproduzíveis a partir dos padrões.
- **Resultados QM:** Q01, Q01b, Q02, Q03 e Q04 mantêm a classificação histórica INCONCLUSIVA. Q04 tem um desvio de protocolo registrado. O hash canônico declarado por Q00 difere do documento canônico fornecido; a discrepância foi mantida.
- **Diagnósticos negativos:** T19, T21 e T25 mantêm diagnósticos que falharam. T23 inclui diagnósticos de raio que discordam. Isso faz parte das evidências.
- **Bytes compartilhados:** matrizes ou configurações deduplicadas podem estar associadas a execuções diferentes. A identidade dos bytes não une essas execuções nem suas interpretações.

## Verifique e amplie

```sh
git lfs pull
python3 tools/check_repository.py
```

A checagem valida arquivos preservados, transformações de documentos, associações do catálogo e links locais. Não executa scripts históricos. Registre mudanças de implementação, caminho, dependência ou configuração declarada separadamente e publique suas saídas como novas execuções. A equação não é adaptada para obter um resultado alvo; nenhum termo é desligado. Diagnósticos numéricos examinam a dinâmica completa e permanecem ligados à execução específica.

[Cronologia](topics/timeline.md) · [Inspeção das fontes](../../provenance/t-archive/inspection.json) · [Política de preservação](../../provenance/README.md) · [Modelo de novo estudo](../../templates/experiment/README.pt-BR.md)

[Fundamentos / Foundations](topics/foundations.md)
