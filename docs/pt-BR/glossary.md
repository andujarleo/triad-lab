[Lab](README.md) · [English](../en/glossary.md)

# Um vocabulário para a TRIAD

Algumas palavras descrevem a leitura de realidade do autor. Outras descrevem matrizes, gráficos e métodos numéricos. Esta página conecta esses usos para que você possa passar da [proposta](triad.md) a um estudo sem precisar adivinhar o significado de um nome.

## Átomo

Na leitura operacional do autor, **um pacote gaussiano é um átomo**: uma forma inicial localizada de Ψ. O mesmo vocabulário se estende a estruturas aninhadas e ao universo-átomo. Leia a [nota original sobre átomo](../reference/concepts/atom.md) e explore [átomos gaussianos em um campo](../../experiments/structures/gaussian-atoms-in-one-field/README.pt-BR.md).

## Matéria e universo

A hipótese ontológica da TRIAD trata a matéria e suas formas como algo que emerge de uma dinâmica mais profunda. “Universo como simulação” nomeia a hipótese ampla do autor; dentro de uma execução, “universo” também nomeia o volume preenchido que está sendo simulado. A [nota original sobre universo](../reference/concepts/universe-as-simulation.md) explica esse uso operacional.

## Vibração e atrito

São etapas da sequência conceitual do autor: **átomo → vibração → atrito → frequência → energia**. Uma simulação precisa declarar uma grandeza observável para associar essas palavras ao resultado. Oscilação, mudança de fase e dissipação já têm descrições numéricas na referência; a sequência conceitual não estabelece uma correspondência individual entre cada palavra e um termo da equação.

## Frequência e som

“Som” é o nome colocado pelo autor ao lado de frequência no mapa conceitual. No lab, um espectro pode descrever variações ao longo do tempo ou estruturas no espaço. Uma conversão para áudio, quando disponível, precisa declarar como esses números foram levados a frequências audíveis. Explore os [estudos de sinais](../../experiments/signals/README.pt-BR.md).

## Energia e luz

“Luz” aparece ao lado de energia no mapa do autor. A cor luminosa de um gráfico representa a grandeza indicada em sua legenda, como densidade ou fase. Conectar uma grandeza registrada à leitura proposta de luz/energia é uma pergunta a ser documentada em um estudo específico.

## Foco, memória e banho

| Palavra | Na dinâmica completa |
|---|---|
| **Foco** | O regime de auto-interação atrativa, Λ < 0, pode concentrar o campo. |
| **Memória / P2** | Os campos yⱼ respondem à densidade em escalas de tempo 1/νⱼ. Sua soma ponderada atua sobre Ψ como V_mem. Valores positivos e negativos de λⱼ produzem respostas diferentes. |
| **Banho / P3** | Dissipação Γ e excitação estocástica η atuam juntas. A versão 1.1 especifica seu acoplamento FDT e mantém o banho ativo. |
| **Anti-colapso** | Nome dado pelo autor à resposta da memória contra a concentração persistente. Um estado final espalhado e picos intensos anteriores podem ocorrer no mesmo registro. |

A [referência versionada da equação](../reference/equation/README.md) apresenta a notação e a regra da equação completa.

## P1, P2, P3 e finitude

**P1 + P2 + P3** registra a formulação do autor para um total finito de base. A referência fornecida chama explicitamente a memória de P2 e o banho de P3. Ela não especifica P1, o que está sendo contado, as unidades da soma ou uma grandeza conservada correspondente. Essas definições seguem em desenvolvimento; o rótulo P1 não é atribuído ao foco por suposição.

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
| **Inconclusivo / Inconclusive** | O teste registrado deixou a conclusão proposta em aberto segundo seus critérios. |
| **Hash / SHA-256** | Uma impressão digital dos bytes de um arquivo, usada aqui para preservar fontes e distinguir edições. |

[Visita de cinco minutos](start-here.md) · [Guia técnico](research-guide.md) · [Diário de pesquisa](journal.md)
