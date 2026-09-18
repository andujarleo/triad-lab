[Lab](README.md) · [English](../en/glossary.md)

# Um vocabulário para a TRIAD

Algumas palavras descrevem a leitura de realidade do autor. Outras descrevem matrizes, gráficos e métodos numéricos. Esta página conecta esses usos para que você possa passar da [proposta](triad.md) a um estudo sem precisar adivinhar o significado de um nome.

## Átomo

Na leitura operacional do autor, **um pacote gaussiano é um átomo**: uma forma inicial localizada de Ψ. O mesmo vocabulário se estende a estruturas aninhadas e ao universo-átomo. Leia a [nota original sobre átomo](../reference/concepts/atom.md) e explore [átomos gaussianos em um campo](../../simulations/structures/gaussian-atoms-in-one-field/README.pt-BR.md).

## Matéria e universo

A ontologia da TRIAD trata a matéria e suas formas como algo que emerge de uma dinâmica mais profunda. “Universo como simulação” nomeia a posição ontológica do autor; dentro de uma execução, “universo” também nomeia o volume preenchido que está sendo simulado. A [nota original sobre universo](../reference/concepts/universe-as-simulation.md) explica esse uso operacional.

## Vibração e atrito

São etapas da sequência conceitual do autor: **átomo → vibração → atrito → frequência → energia**. Uma simulação precisa declarar uma grandeza observável para associar essas palavras ao resultado. Oscilação, mudança de fase e dissipação já têm descrições numéricas na referência; a sequência conceitual não estabelece uma correspondência individual entre cada palavra e um termo da equação.

## Frequência e som

“Som” é o nome colocado pelo autor ao lado de frequência no mapa conceitual. No lab, um espectro pode descrever variações ao longo do tempo ou estruturas no espaço. Uma conversão para áudio, quando disponível, precisa declarar como esses números foram levados a frequências audíveis. Explore os [estudos de sinais](../../simulations/signals/README.pt-BR.md).

## Energia e luz

“Luz” aparece ao lado de energia no mapa do autor. A cor luminosa de um gráfico representa a grandeza indicada em sua legenda, como densidade ou fase. Conectar uma grandeza registrada à leitura proposta de luz/energia é uma pergunta a ser documentada em um estudo específico.

## Foco, memória e banho

| Palavra | Na dinâmica completa |
|---|---|
| **Foco** | O regime de auto-interação atrativa, Λ < 0, pode concentrar o campo. |
| **Memória · parte de P2** | Os campos yⱼ respondem à densidade em escalas de tempo 1/νⱼ. Sua soma ponderada atua sobre Ψ como V_mem. Valores positivos e negativos de λⱼ produzem respostas diferentes. |
| **Banho · expressão de P3** | Dissipação Γ e excitação estocástica η atuam dentro da dinâmica completa e acoplada. O documento de referência descreve seu acoplamento FDT. |
| **Anti-colapso** | Nome dado pelo autor à resposta da memória contra a concentração persistente. Um estado final espalhado e picos intensos anteriores podem ocorrer no mesmo registro. |

O [índice da documentação de referência](../reference/equation/README.md) apresenta a notação e o histórico documental. A equação em si é única, imutável e indivisível.

## P1, P2, P3 e finitude

| Princípio | Significado |
|---|---|
| **P1 · Oscilação** | A oscilação faz parte daquilo que constitui o sistema. |
| **P2 · Autorreferência** | O estado presente atua sobre sua própria dinâmica, e a memória carrega a ação de sua história. P2 inclui ambos. |
| **P3 · Acoplamento** | O sistema existe por meio do acoplamento; o banho participa dessa dinâmica acoplada. |

**P1 + P2 + P3** expressa a leitura integrada do autor sobre esses princípios e a finitude. Os princípios estão definidos. Uma unidade, quantidade contada ou grandeza conservada da soma não deve ser inventada a partir dessa notação.

## Cristalização dinâmica

A TRIAD lê a cristalização como organização dinâmica. Oscilação, escalas móveis e reorganização podem fazer parte do estado ordenado. Uma rede fixa não é um resultado obrigatório. Leia cada janela temporal, diagnóstico e configuração registrada, sem calibrar o campo externamente para obter um padrão preferido. [Regras do projeto](project-rules.md).

## Lendo uma simulação

| Termo | O que observar |
|---|---|
| **Campo / Field** | Valores representados em posições espaciais ou por modos. Ψ é o campo complexo principal da referência. |
| **Densidade / Density** | ρ = \|Ψ\|² nos estudos de campo. Observe se a figura mostra um corte, uma projeção ou o volume inteiro. |
| **Fase / Phase** | O ângulo do campo complexo. Cores de fase não representam densidade, a menos que a legenda indique isso. |
| **Grade / Grid** | As posições amostradas. Uma grade 64³ contém 64 × 64 × 64 posições. |
| **Passo de tempo / Time step** | O intervalo usado em uma atualização numérica. |
| **Semente aleatória / Random seed** | Entrada do gerador de números aleatórios. A repetição exata também depende do código, dos parâmetros e do ambiente. Já uma “semente” gaussiana nomeia um pacote inicial do campo. |
| **Checkpoint** | Um estado interno salvo. Confira quais matrizes foram armazenadas antes de tentar retomar a execução. |
| **Espectro / Spectrum** | Distribuição entre frequências temporais ou escalas espaciais, conforme o cálculo. |
| **Diagnóstico / Diagnostic** | Uma medida calculada de uma propriedade declarada. Sua definição e suas condições de falha acompanham a execução. |
| **Convergência / Convergence** | Verificar como os resultados se comportam ao refinar a resolução numérica. A referência vigente descreve comparações entre conjuntos de execuções para a equação completa com ruído. |
| **R5 / Θ_core** | Nomes encontrados em configurações históricas. Leia os parâmetros e a implementação associados a cada estudo. |
| **QM / Q00–Q04** | Identificadores históricos de diagnósticos do campo, mantidos para a cronologia. |
| **Registrado / Recorded** | Há material de uma execução disponível; a palavra descreve disponibilidade. |
| **Inconclusivo / Inconclusive** | Um diagnóstico preservado não resolveu sua pergunta segundo os critérios daquele registro. Isso não classifica a identidade da TRIAD. |
| **Hash / SHA-256** | Uma impressão digital dos bytes de um arquivo, usada aqui para preservar fontes e distinguir revisões documentais. |

[Visita de cinco minutos](start-here.md) · [Guia técnico](research-guide.md) · [Diário de pesquisa](journal.md)
