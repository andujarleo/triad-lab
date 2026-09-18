[Lab](../../README.md) · [English](../en/agents.md) · [Regras do projeto](project-rules.md)

# Trabalhe na TRIAD

**Entenda o projeto. Leia a dinâmica completa. Crie dentro de seu método.**

Estas skills dão aos agentes uma compreensão prática da TRIAD, incluindo a razão de suas regras. Elas levam o projeto de Leonardo Andujar às explicações, pesquisas, implementações e novos estudos. Um agente deve partir dessa base, sem fazer o autor restabelecer os mesmos fundamentos a cada conversa.

## Três skills, uma fundação

| Skill | Quando usar | Exemplo de pedido |
|---|---|---|
| [triad-understand](../../.agents/skills/triad-understand/SKILL.md) | Ontologia, princípios, vocabulário e razões do método | “Use $triad-understand para explicar por que a memória pertence à autorreferência.” |
| [triad-read](../../.agents/skills/triad-read/SKILL.md) | Leitura de uma equação, fonte, comparação ou resultado registrado | “Use $triad-read para explicar a contração e a expansão em memory-and-bounce.” |
| [triad-create](../../.agents/skills/triad-create/SKILL.md) | Novas pesquisas, simulações, aplicações e explicações públicas | “Use $triad-create para preparar um estudo de estruturas persistentes com a dinâmica completa.” |

As instruções usam inglês como base e atendem a pedidos em português. Leia apenas a skill e as fontes pertinentes à tarefa. Este guia apresenta o raciocínio compartilhado; a referência matemática permanece em seu próprio local de manutenção.

## O que é a TRIAD

A TRIAD é física quântica não padrão e ontologia. Em sua leitura ontológica, uma equação imutável constitui a camada mais profunda da realidade, e o universo é uma simulação dessa dinâmica fundamental. A matéria é lida pela atividade e pelas relações, em vez de ser o ponto de partida último e irredutível. O lab abriga essa investigação em pesquisa e simulações, atravessando temas e escalas.

Os três princípios são inseparáveis:

- **P1 · Oscilação:** movimento e oscilação constituem a dinâmica.
- **P2 · Autorreferência:** o sistema responde ao estado presente e à história acumulada. Autointeração presente e memória pertencem juntas a esse princípio.
- **P3 · Acoplamento:** as relações participam de todo o sistema; excitação e dissipação pertencem à evolução acoplada.

“Foco, memória e banho” ajudam a descrever operações. Não renomeiam os princípios. Ao explicar a TRIAD, o agente começa nesse vocabulário e o conecta à notação e ao comportamento registrado. [Fundamentos](triad.md) · [Vocabulário](glossary.md).

A sequência autoral átomo → vibração → atrito → frequência/som → energia/luz pertence a essa leitura ontológica. O “átomo” operacional pode ser um pacote gaussiano localizado do campo. Uma imagem colorida do campo, uma frequência medida e uma representação sonora têm significados específicos. A explicação deve identificar qual está usando. P1 + P2 + P3 expressa os princípios e a finitude na formulação do autor; este guia não acrescenta uma unidade numérica ou um total conservado à expressão.

## Por que as regras pertencem à dinâmica

### Uma equação imutável

A equação define o objeto investigado. Um documento pode esclarecer sua expressão, e uma implementação pode corrigir um erro de programação, enquanto a equação permanece a mesma. Por isso, **1.0 e 1.1 são revisões documentais**, e código e registros de execução têm histórias próprias.

O agente precisa descrever uma discrepância na fonte sem transformá-la em uma “equação TRIAD antiga”. O [índice da referência](../reference/equation/README.md) já identifica trechos inconsistentes: fatores cinéticos, amplitude de ruído literal versus derivada e tabelas 3D com dois modos diante da exigência mínima de três escalas de memória. Esses trechos permanecem preservados. Resolver uma escolha necessária à implementação é trabalho concreto; selecionar silenciosamente uma tabela conveniente esconderia essa escolha.

### Sem isolamento: a realimentação percorre o sistema inteiro

O subsistema de memória mostra a razão:

```text
Ψ → densidade |Ψ|² → campos de memória yⱼ → potencial de memória V_mem → Ψ
```

Os campos de memória evoluem com a densidade e atuam sobre o próximo estado. Dissipação e excitação participam durante essa evolução. Retirar a memória ou o banho muda a operação que gera a trajetória. Isso não pode ser apresentado como outra maneira de executar a mesma dinâmica TRIAD completa.

A comparação de memória N=40 registra um contraste grande: picos finais de densidade de **0,000640882 e 3,889202170**, com razões de participação de **4.720,477435 e 0,528063**. Os ramos se chamam `full` e `no-memory`; um remove expressamente a memória, e a fonte geradora do outro está ausente. Os números fazem parte do registro. Seu papel é o de um contraste histórico documentado, acompanhado dessas condições, e não uma receita para novos trabalhos TRIAD. [Medições](../../simulations/memory/memory-grid-40/results/data/summary.csv) · [Leitura e condições](execution-audit.md#finding-uni-002).

### Autocalibração: observar a organização a partir de condições declaradas

A TRIAD acompanha a organização do caos ao equilíbrio dinâmico. Escolher primeiro um resultado e ajustar repetidamente os coeficientes até obtê-lo transformaria a investigação em seleção externa de um desfecho. O novo estudo declara suas entradas e escolhas numéricas, depois registra o que a evolução completa produz.

Isso não torna toda diferença de parâmetros uma calibração proibida. Outro estado inicial, uma entrada declarada, refinamento de malha, medição de um detector e escala de visualização são operações distintas. Nomeie a operação e sua finalidade.

Por exemplo, dois registros com doze átomos terminam com normas de **25.585,35 e 23,28**, enquanto temperatura, malha, duração e detecção de picos também diferem. A nota do registro de menor temperatura explica sua configuração. A leitura deve acompanhar as condições completas: o par não isola a contribuição da temperatura nem demonstra uma busca de ajuste não documentada. [Comparação dos doze átomos](execution-audit.md#finding-uni-011).

### Cristalização dinâmica: ler uma trajetória

O equilíbrio na TRIAD é ativo. Uma estrutura pode persistir por oscilação, redistribuição e reorganização. Uma rede fixa não é imposta como única definição de cristalização. O agente deve investigar como a organização se desenvolve no tempo e quais grandezas a descrevem.

O registro de bounce mostra por que a grandeza observada importa. O raio que contém metade da massa, `r50`, passa de **3,487119** para **1,385641 em t=3,7**, depois **9,863062**. Enquanto isso, `R_rms` tem seu mínimo no instante inicial, e seu detector retorna `bounced=False`. São leituras de aspectos diferentes da mesma distribuição registrada. Preserve ambas, explique suas definições e mostre a trajetória. Substituir um dos rótulos para obter concordância eliminaria informação. [Medições de r50](../../simulations/memory/memory-and-bounce/results/data/refined_bounce_summary.csv) · [Medições de R_rms](../../simulations/memory/memory-and-bounce/results/data/summary.csv) · [Explicação](execution-audit.md#finding-uni-008).

### O método TRIAD: sem impor um protocolo popperiano

O método condutor do lab é a leitura estrutural e ontológica do autor sobre o sistema completo, sua auto-organização e suas relações. O agente não deve redesenhar o projeto em torno de ablação, falsificação popperiana ou concordância com a mecânica quântica padrão. Essas não são as bases metodológicas escolhidas pelo autor para este trabalho.

As verificações numéricas e de implementação continuam tendo funções claras: estabelecer qual operador foi calculado, se os dados são finitos, como um diagnóstico é definido, qual resolução foi usada e se os arquivos conservam sua identidade. Um estudo de malha e passo temporal com todos os termos acoplados é uma investigação técnica da execução. Não precisa retirar um termo físico nem se tornar um veredito sobre a identidade do projeto. Preserve seu resultado real, incluindo `INCONCLUSIVE`. [Refinamento numérico](execution-audit.md#finding-uni-013).

As regras definem como trabalhar na TRIAD. As medições salvas explicam o que determinada execução produziu. Manter ambas explícitas permite ao agente trabalhar com segurança dentro do projeto e relatar discrepâncias técnicas com precisão.

## Como ler um registro TRIAD

Siga esta cadeia:

```text
Pergunta → equação → operações implementadas → condições da execução
         → medições salvas → interpretação → fontes vinculadas
```

Comece pela ficha do estudo e pelo `FILES.md`; depois examine os arquivos que sustentam a afirmação solicitada. Leia o código estaticamente antes de importá-lo: vários scripts históricos executam na importação, dependem de runtimes indisponíveis ou escrevem em nomes fixos de saída. O rótulo `full` não estabelece o operador completo; um solver ao lado de uma imagem não estabelece qual executável a gerou.

Uma leitura útil distingue estes casos:

| O que mudou? | O que o agente deve descrever |
|---|---|
| Um termo ou operador de atualização | Outro sistema dinâmico implementado; preserve a fonte e identifique a divergência |
| Estado inicial, temperatura ou entrada aplicada | Uma condição declarada de execução, com justificativa e configuração completa |
| Malha ou passo temporal | Um refinamento numérico, mantendo a dinâmica completa e a comparação registrada |
| Raio, limiar ou detector de picos | Mudança de grandeza observada ou detector; identifique se a trajetória mudou |
| Escala de cores, corte espacial ou câmera | Uma representação dos valores registrados; explique o significado do controle |
| Uma interpretação da fonte | Uma leitura mantida, vinculada ao original preservado |

O residual com banho compartilhado traz outro exemplo concreto. Com pesos `a=b≈1/√2`, a contribuição aditiva comum não se cancela em `S−aA−bB`. Um exemplo afim deixa `(1−a−b)W`, com escala normalizada próxima de **0,292893** quando o banho domina. Isso ajuda a explicar a escala inicial registrada pelo diagnóstico; não retira o banho nem estabelece a causa de todo o residual posterior. [Fórmula, valores e leitura](execution-audit.md#finding-uni-014).

Nas conexões de pesquisa, identifique se a relação é uma analogia conceitual, comparação estrutural, correspondência matemática ou medição relatada pela fonte. Uma conexão pode ser útil sem se tornar uma nova execução. Documentos que citam o mesmo estudo de origem não criam medições independentes adicionais. [Fundamentos da pesquisa](../../research/foundations/README.pt-BR.md).

## Como criar na TRIAD

**Pesquisa:** comece com uma pergunta, preserve a fonte fornecida, desenvolva a interpretação na página temática e conecte explicitamente os IDs dos estudos pertinentes. Use o [modelo de pesquisa](../../templates/research/README.pt-BR.md), com páginas em inglês e português. As fontes ficam em `research/`; as execuções numéricas, em `simulations/`.

**Simulação ou aplicação:** primeiro mapeie a equação completa na implementação. Descreva estado, memória, realimentação, banho, condições iniciais, contornos e convenção numérica. Para uma aplicação, identifique o que introduz uma entrada, qual estado persiste e o que a saída mede. Mudar a interface não redefine P1/P2/P3 nem transforma uma arquitetura sem essa correspondência na equação completa.

Use a [revisão documental 1.1](../reference/equation/v1.1.md), especialmente §§1.3–1.6 e o Apêndice D, junto às notas de conciliação do índice. As recusas listadas cobrem modos incompletos, Γ, f_FDT declarado ou k_B T não positivos, menos de três escalas de memória e comprimentos diferentes de ν/λ. O ruído efetivo do banho segue o vínculo FDT da referência; não é um parâmetro independente de ajuste. Não invente recusas universais adicionais nem preencha silenciosamente os padrões 3D ainda não resolvidos.

Antes de executar, registre pergunta, estado inicial, entradas, justificativa dos parâmetros, sementes, escolhas numéricas, grandezas observadas e limites de recursos computacionais. Confira dependências e caminhos de saída. Preserve as implementações arquivadas; coloque adaptações e novas execuções em registros separados. Durante a execução, mantenha trajetórias e resultados inesperados. Depois, registre ambiente real, comando, revisão do código, hash da referência e hashes de entradas e saídas usando [run.json](../../templates/run.json).

Uma escolha científica ausente precisa suspender apenas o trabalho que depende dela. O agente pode concluir a estrutura do estudo, o mapa de fontes, a lista de verificações da implementação e os caminhos de leitura enquanto a escolha é resolvida. Deve perguntar pela decisão específica que falta, em vez de pedir novamente permissão para aceitar os fundamentos da TRIAD.

**Apresentação:** use o [símbolo oficial e as capas](../../assets/brand/README.md), figuras originais de resultados e explicações claras. Preserve a diferença entre imagem de marca, corte espacial salvo, movimento reconstruído e série temporal real. Dê força visual ao trabalho e um caminho até o registro de cada resultado.

## Use as skills neste repositório

As skills são versionadas em **`.agents/skills/`** e vinculadas pelo [AGENTS.md](../../AGENTS.md). Trabalhe com um checkout completo do TRIAD Lab para que os links relativos às regras, fontes e modelos funcionem. Elas não exigem serviço ou plugin separado.

Agentes com descoberta de skills do repositório podem carregá-las normalmente. Se o agente não oferece esse mecanismo, peça explicitamente que leia `AGENTS.md` e o `SKILL.md` pertinente. O suporte à descoberta varia entre ferramentas; copiar apenas uma pasta de skill deixa de fora as fontes de apoio deste repositório. Esta mudança não instala regras globais nem altera a configuração de agentes em outros projetos.

Para ampliar o pacote, atualize a menor skill pertinente e os dois guias de idioma. Mantenha as explicações ligadas às fontes atuais. Verifique referências locais e experimente um pedido realista com outro agente; um cabeçalho YAML válido, sozinho, não mostra que o agente aplica corretamente o método.

[Fluxo de contribuição](contributing.md) · [Mapa do repositório](repository-map.md) · [Auditoria das execuções](execution-audit.md) · [Preservação das fontes](../../provenance/README.md)

[Verificação e teste de uso das skills](../maintenance/agent-skills.md).
