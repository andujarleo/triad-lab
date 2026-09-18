[Lab](../../README.md) · [English](../en/execution-audit.md) · **Português**

# O que as simulações registradas mostram

**O acervo contém diferenças marcantes no comportamento do campo, e as condições dessas diferenças importam.** Uma comparação de memória termina com pico de densidade de aproximadamente **0,000641 contra 3,889202**. Dois registros com doze átomos chegam a normas do campo de **25.585,35 contra 23,28**. Uma mesma trajetória salva recebe tanto a leitura de “bounce” quanto a de “sem bounce”, conforme o raio medido.

Esta auditoria segue esses resultados até os códigos, configurações e medições registrados. A pergunta é concreta: **o que foi evoluído, o que mudou e o que esta comparação permite concluir?** Os **65 itens do catálogo** foram cobertos por inventário de arquivos e classificação fundamentada, com leitura mais próxima das fontes e registros por trás dos achados abaixo. Nenhuma simulação foi reexecutada.

[A equação completa](#the-complete-equation) · [Cinco casos centrais](#five-central-cases) · [Todos os 17 achados](#all-17-findings) · [Cada estudo](#every-study) · [Cobertura](#coverage)

<a id="the-complete-equation"></a>
## Por que a equação completa é o ponto de partida

A TRIAD é apresentada aqui como **física quântica não padrão, com fundamento ontológico**. Seu autor define uma equação única, imutável e indivisível: P1 oscilação, P2 autorreferência pelo estado presente e pela memória, e P3 acoplamento atuam juntos. O comportamento buscado é a auto-organização desse sistema acoplado, incluindo equilíbrio e cristalização dinâmicos. [Regras do projeto](project-rules.md), linhas 5–31.

Um registro produzido com a memória ou o banho desligados não estabelece o que a **equação TRIAD completa** produz. Ele continua documentando o que sua configuração fez. Da mesma forma, uma simulação que redimensiona continuamente o campo ou usa outra equação de atualização precisa declarar essa operação antes de atribuir sua saída à dinâmica de referência. Trata-se da identidade da implementação, não de uma nova versão da equação.

Há diferenças legítimas que não removem termos: uma condição inicial declarada, uma entrada aplicada durante a rodada, uma malha mais fina, um passo temporal menor, a medição de um detector ou uma representação visual. Cada operação precisa ser descrita pelo que faz. Escolher um limiar de detecção é diferente de ajustar a dinâmica para obter uma forma desejada. Alguns registros fornecidos deixam essa distinção em aberto; a auditoria indica onde.

**A metodologia também pertence às regras do autor.** O lab não usa falsificação popperiana nem concordância com a mecânica quântica padrão como critério condutor. Checagens numéricas continuam podendo examinar valores finitos, identidade das fontes, resolução e comportamento do sistema completo. Rótulos históricos como `INCONCLUSIVE`, `SUPPORTED` e outros permanecem ligados aos diagnósticos que os produziram. Eles não são reescritos silenciosamente nem promovidos a vereditos sobre a ontologia. [Método e preservação](project-rules.md), linhas 27–47.

<a id="five-central-cases"></a>
## Cinco casos centrais

<a id="finding-uni-002"></a>
### Memória: uma diferença grande registrada, com um termo removido

O registro N=40 compara um ramo chamado `full` com outro chamado `no-memory`:

| Quantidade registrada | Rótulo `full` | Rótulo `no-memory` |
|---|---:|---:|
| Pico final de densidade | 0,000640882 | 3,889202170 |
| Razão de participação final, PR | 4.720,477435 | 0,528063 |
| Maior pico registrado | 1,651207320 | 4,170131021 |

PR descreve quão amplamente a densidade ocupa o domínio nesse diagnóstico; os dois ramos apresentam concentrações finais muito diferentes. Os números estão preservados no [CSV de resumo](../../simulations/memory/memory-grid-40/results/data/summary.csv), linha 2, e explicados no [registro original](../../simulations/memory/memory-grid-40/notes/original-record.md), linhas 12–26.

**O que a comparação estabelece:** uma diferença grande entre as saídas salvas. **O que não está estabelecido:** a operação da equação indivisível inteira nos dois ramos. Um deles remove expressamente a memória, e o ramo chamado `full` não tem sua fonte/configuração geradora fornecida. O rótulo histórico não supre essa documentação. Por isso, a comparação preservada é identificada como registro com termo desligado; ela não é proposta como método TRIAD. **Achado UNI-002.**

<a id="finding-uni-011"></a>
### Doze átomos: temperatura, malha e observação mudaram

Dois registros usam a mesma receita de posicionamento e semente para doze centros gaussianos. Suas trajetórias diferem visualmente e nos números:

| Condição ou resultado | Campo de doze átomos | Trajetórias 3D dos átomos |
|---|---:|---:|
| Temperatura do banho `kT` | 1 | 0,001 |
| Malha por eixo, N | 32 | 40 |
| Tempo final, T | 15 | 12 |
| Norma final do campo | 25.585,351298 | 23,275045 |
| Sementes detectadas no início | 1.147 máximos em t=0,1 | 12 sementes distintas até t=1 |

O registro mais frio também acrescenta uma separação mínima entre os picos aceitos pelo detector. Sua nota explica que a temperatura escolhida veio de uma configuração da especificação fornecida e manteve as sementes visíveis por mais tempo. Isso é uma escolha declarada de entrada física, não apenas uma mudança de precisão numérica. O material preservado não demonstra uma busca oculta por ajuste; também não permite atribuir toda a diferença somente à temperatura. [Primeiro registro](../../simulations/structures/twelve-atoms-full-field/notes/original-record.md), linhas 19–53; [segundo registro](../../simulations/structures/3d-atom-trajectories/notes/original-record.md), linhas 17–29 e 49–60.

O resultado compara **condições registradas diferentes**, incluindo malha, duração e detector. Os dois runners ainda importam um runtime externo histórico cuja versão executada não está fixada por um hash fornecido. A cópia do solver de referência ajuda a explicar os padrões pretendidos, mas não estabelece a identidade dessa dependência externa. **Achado UNI-011.**

<a id="finding-uni-008"></a>
### Bounce: a mesma trajetória, duas perguntas diferentes

No registro de memória e bounce, o raio quadrático médio, `R_rms`, já começa no seu menor valor. Seu detector retorna `bounced=False`. O raio que contém metade da massa, `r50`, primeiro encolhe e depois aumenta:

| Diagnóstico | Inicial | Mínimo | Final | Leitura registrada |
|---|---:|---:|---:|---|
| `R_rms` | 3,919184 | 3,919184 em t=0 | 12,272371 | Sem mínimo de contração no interior da janela |
| `r50` | 3,487119 | 1,385641 em t=3,7 | 9,863062 | Contração seguida de expansão |

As medidas descrevem partes diferentes da distribuição. Uma cauda externa em expansão pode afetar `R_rms` enquanto a metade central da massa se contrai. Não foi necessária uma nova trajetória para obter os rótulos diferentes. O pico de densidade ocorre em t=4,1 e o de memória em t=4,2, com atraso registrado de 0,1. [Registro original](../../simulations/memory/memory-and-bounce/notes/original-record.md), linhas 16–32; [CSV de resumo](../../simulations/memory/memory-and-bounce/results/data/summary.csv).

A apresentação útil mostra a **trajetória do raio e sua definição**, em vez de um selo binário sem explicação. Esse registro ainda não fixa completamente a fonte executada e a configuração efetiva do banho. **Achado UNI-008.**

<a id="finding-uni-014"></a>
### Q04: o residual ponderado também contém o banho comum

Q04 evolui A, B e sua combinação normalizada S com os termos conjuntos ativos e a mesma sequência aleatória por semente. Seu residual ponderado registrado parte de aproximadamente zero e chega a **0,290717 em t=0,02**, **0,293008 em t=0,1** e média tardia de **0,386410**. A fonte mantém `INCONCLUSIVE`. [Análise registrada](../../simulations/field-diagnostics/linearity-tests/notes/analysis.md), linhas 18–24 e 53–74.

O diagnóstico precisa de uma explicação precisa: somar o mesmo banho às três rodadas **não** o cancela quando os dois pesos da comparação somam mais de um. Portanto, o número não pode ser lido como medida exclusiva da resposta não linear nem como falha universal da superposição.

<details>
<summary>Detalhe técnico: por que a contribuição aditiva comum permanece</summary>

A quantidade implementada é

$$R=\frac{\|S-aA-bB\|}{|a|\,\|A\|+|b|\,\|B\|},\qquad a=b\simeq\frac1{\sqrt2}.$$

No exemplo algébrico de um mapa afim $F(X)=L(X)+W$, com $L$ linear e $W$ uma contribuição aditiva comum, o numerador contém $(1-a-b)W$. Se essa contribuição comum domina, o residual normalizado tende a $1-1/\sqrt2\simeq0{,}292893$ — próximo da escala dos valores iniciais registrados.

Esse cálculo explica uma propriedade do diagnóstico. Ele não decompõe a trajetória não linear real nem atribui ao banho todo o residual tardio. Não exige nem recomenda desligar qualquer termo da equação. Veja a [fonte](../../simulations/field-diagnostics/linearity-tests/code/probe_field_linearity.py), linhas 330–338, 376–386 e 536–541.

</details>

A interpretação mantida é a de **residual ponderado do campo no sistema forçado e acoplado**, preservando valores e veredito originais. **Achado UNI-014.**

<a id="finding-uni-001"></a>
### Geometria: nomear os termos não garante a mesma atualização

A família geométrica contém implementações efetivas, estados de campo salvos e imagens derivadas. A leitura dos kernels que evoluem o campo encontra diferenças da referência além dos guards de normalização registrados anteriormente. Essas diferenças mudam a operação calculada mesmo quando os comentários a chamam de mesma equação.

| Operação examinada | Implementação geométrica fornecida | Operação de referência |
|---|---|---|
| Contribuição cinética em Fourier | `IFFT(-0.5*K2*FFT(psi))`, dentro de contribuição multiplicada por `-1j` | Multiplicador do Hamiltoniano `+hbar²*k²/(2m)` |
| Incremento estocástico | Sorteio gaussiano multiplicado por `dt*eta*0.02` | Amplitude acoplada por FDT proporcional a `sqrt(dt)` |
| Guard de estado | Alguns kernels reduzem norma acima de 100 para 50, corrigem valores não finitos ou injetam um campo pequeno perto de zero | São operações adicionais sobre o estado e precisam ser declaradas |

A fonte também deriva coeficientes e um potencial espacial de memória por uma construção interna de realimentação; chamar esse potencial de `V_mem` não estabelece, por si só, a atualização das memórias auxiliares da referência. Implementações iniciais 1D/2D incluem normalização a cada passo, e algumas expressões chamadas de dissipação atuam como fase. [Propagador e ruído da referência](../reference/equation/v1.1.md), linhas 112–118 e 229–233; [fonte 3D](../../simulations/geometry/field-3d/code/pt-BR/bravais_puro_3d.py), linhas 116–129, 190–218 e 241–253.

A auditoria acompanha esses kernels na varredura de caixa, no runner de evolução de vibrações, no gerador de filmes, nas perturbações, na entrada WiFi e nos testes de estruturas de cordas. Os links próprios de fonte estão no registro de estudos abaixo. A presença de um guard condicional não estabelece quantas vezes ele atuou numa rodada salva. **Nenhuma reexecução pareada mediu o efeito numérico isolado dessas diferenças.** A conclusão é uma divergência demonstrada de implementação, não uma explicação causal inventada para cada figura. **Achado UNI-001.**

Arquivos que apenas leem resultados mantêm sua função distinta: `bravais_vibracoes.py` reconstrói movimento a partir de modos salvos; o outro runner de vibrações evolui um campo. `simula_filmes.py` evolui; os cinco arquivos visuais acompanhantes leem ou renderizam suas saídas. Um pós-processamento não se torna nova execução da equação completa só porque produz uma animação.

<a id="all-17-findings"></a>
## Todos os 17 achados

Os cinco casos acima são **[UNI-001](#finding-uni-001), [UNI-002](#finding-uni-002), [UNI-008](#finding-uni-008), [UNI-011](#finding-uni-011) e [UNI-014](#finding-uni-014)**. Os demais achados conectam outros contrastes numéricos e mudanças de interpretação.

<a id="finding-uni-003"></a>
**UNI-003 · A resolução muda o registro de colapso com memória reduzida.** Em N=64/128/160, o maior pico do ramo com memória é aproximadamente 13,17/62,48/99,74; as contagens de pulsos são 1/6/9. O pico final sem memória sobe de 8,098 para 65,26 e depois cai para 48,25. É um registro dependente da malha, com `alpha=Gamma=FDT=0` e duas memórias, incluindo comparações com termos desligados. Um estado tardio expandido também não apaga a passagem breve pelo limiar inicial. [Análise](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-160/analysis.md), linhas 24–49; [configuração](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md), linhas 10–18.

<a id="finding-uni-004"></a>
**UNI-004 · Um pico térmico precisa vir acompanhado de sua norma.** Condições quentes pareadas do dossiê registram PR=4.283/4.013 e pico=4,974/7,413 com/sem memória, enquanto as normas são aproximadamente 3.604/3.621. Um pico bruto alto nesses campos não é comparável ao mesmo pico num campo de norma unitária. A análise declara a correção de um rótulo diagnóstico depois de considerar a norma; não reexecutou a trajetória para obter essa correção. As configurações continuam reduzidas e incluem remoção da memória. [Análise](../../simulations/numerical-checks/reproduction-dossier/notes/thermal-noise-and-collapse/analysis.md), linhas 17–39 e 60–69.

<a id="finding-uni-005"></a>
**UNI-005 · A razão de retorno na barreira não isola uma cicatriz de memória.** O caso linear já apresenta razão transmissão de retorno/primeira passagem de 1,5981. Os registros com memória e memória congelada dão 2,7673 e 2,7385, com energias diferentes dos pacotes retornados e janela incompleta. Congelar a memória também modifica a dinâmica. A leitura preservada de `protocol-dirty` importa ao apresentar esses números. [Análise](../../simulations/numerical-checks/reproduction-dossier/notes/barrier-memory-and-tunneling/analysis.md), linhas 6–26 e 40–64.

<a id="finding-uni-006"></a>
**UNI-006 · Uma janela espectral curta e limpa não substitui a longa com vazamento.** O registro oficial com memória em T=251, L=80 apresenta vazamento de fronteira de 0,3081; o registro curto em T=80, L=40 tem aproximadamente 6,77×10⁻¹³. São janelas e caixas diferentes. Ampliar a caixa para conferir fronteiras é uma operação técnica; escolher o registro curto mais limpo muda a comparação apresentada. O resultado oficial `INCONCLUSIVE` e suas condições precisam continuar visíveis. [Análise](../../simulations/numerical-checks/reproduction-dossier/notes/memory-and-spectral-sidebands/analysis.md), linhas 10–21 e 98–119.

<a id="finding-uni-007"></a>
**UNI-007 · kL=9,424778 repetido pode vir da definição de uma faixa espectral.** A análise de escala dominante encontra o mesmo valor em oito rodadas porque ele é $3\pi$, o primeiro centro de casca permitido pelo diagnóstico. As oito são marcadas sem pico espectral destacado em k finito. Isso limita a interpretação desse número espectral; não define nem exclui toda cristalização dinâmica. [Análise](../../simulations/numerical-checks/reproduction-dossier/notes/dominant-spatial-scale/analysis.md), linhas 8–23 e 57–59.

<a id="finding-uni-009"></a>
**UNI-009 · A rede reconstruída passa de 2 para 39 nós depois de mudanças na extração.** A primeira usa quantil 0,992 e distância mínima de 3 células; a refinada escolhe t=4,4, quantil 0,988 e distância de 2 células. As arestas passam de 1 para 25. São escolhas de detector/amostra, não uma mudança pareada da dinâmica do campo. Os escores do mapa Bravais separado também usam outro detector e regime em relação ao N=48. [Primeira reconstrução](../../simulations/geometry/first-geometric-network/notes/original-record.md), linhas 12–22; [reconstrução refinada](../../simulations/geometry/refined-geometric-network/notes/original-record.md), linhas 12–24; [mapa de modelos](../../simulations/geometry/bravais-template-map/notes/original-record.md), linhas 12–30.

<a id="finding-uni-010"></a>
**UNI-010 · O par quente/frio anterior também muda malha e duração.** A massa/norma final passa de 8.773,747757 para 1,413637, mas N muda 36→44, T muda 8→10, e os picos iniciais são diferentes. Fonte e configuração são insuficientes para atribuir a diferença somente ao banho. [Registro quente](../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md), linhas 12–29; [registro frio](../../simulations/signals/3d-cold-bath-box/notes/original-record.md), linhas 12–28.

<a id="finding-uni-012"></a>
**UNI-012 · O refino do detector de fase também muda o estímulo.** A primeira estimativa de frente, próxima de zero, aproximadamente 4,01×10⁻¹⁶, é seguida por estimativas refinadas de chegada de 7,301417/7,557409 e RMS de 1,482120/1,893955. A amplitude muda 0,07→0,15, a largura 1,3→1,25 e a duração da sondagem 1,8→5, junto ao estimador/controle. Esses diagnósticos diferentes não estabelecem uma velocidade universal de propagação. [Primeiro registro](../../simulations/signals/first-phase-to-density-diagnostic/notes/original-record.md), linhas 12–26; [registro refinado](../../simulations/signals/refined-phase-to-density-diagnostic/notes/original-record.md), linhas 12–26.

<a id="finding-uni-013"></a>
**UNI-013 · A convergência com termos conjuntos permanece em aberto no espaço.** Com os termos ativos, a média tardia do pico sobe aproximadamente 2,773→3,146→3,905→4,91566 para N=32/48/64/96. A diferença relativa espacial registrada é 0,205642; a temporal é 0,011596. O máximo espectral permanece perto do corte de cada malha. A mesma semente inteira em malhas ou passos distintos não gera uma trajetória comum de ruído. São checagens numéricas legítimas, com classificações `INCONCLUSIVE` preservadas, não ajuste de coeficientes físicos. [Análise espacial](../../simulations/field-diagnostics/spatial-convergence/notes/analysis.md), linhas 31–76; [análise de refino](../../simulations/field-diagnostics/resolution-and-time-step/notes/analysis.md), linhas 34–100. O [conjunto de 32 sementes](../../simulations/field-diagnostics/seed-ensemble/notes/analysis.md), linhas 68–77, documenta variabilidade na malha e precisão declaradas.

<a id="finding-uni-015"></a>
**UNI-015 · O ninho longo reproduz o ponto final curto antes de continuar.** No instante comum t=8, os dois registros apresentam pico 4,336503, PR≈19.557,412 e norma≈18.021,708. Em T=60, o registro longo tem pico 3,372458, PR≈28.301,592 e norma≈32.692,307. É uma continuação com mudança de tempo, não uma réplica independente. A análise original também distingue um indicador automático de bounce baseado no pico de um bounce de raio de massa, preservando as flutuações. [Análise longa](../../simulations/structures/long-nest-trajectory/notes/original-record.md), linhas 13–19 e 37–75.

<a id="finding-uni-016"></a>
**UNI-016 · Os bolsos respondem a entradas declaradas.** Em t=0,5 o runner de um bolso soma uma gaussiana. A massa local muda 12,72→13,80; em t=0,8 a correlação densidade-memória reportada é 0,888 dentro e 0,723 fora. O runner de dois bolsos soma duas entradas com sinais opostos. Essas entradas não removem termos, mas precisam permanecer visíveis em qualquer narrativa sobre o aparecimento de um bolso. O vocabulário de observador do autor é uma interpretação do diagnóstico de campo. [Registro do bolso](../../simulations/structures/a-pocket-in-the-field/notes/original-record.md), linhas 23–31; [mapa](../../simulations/structures/density-memory-maps/notes/original-record.md), linhas 21–29; [fonte da entrada](../../simulations/structures/a-pocket-in-the-field/code/simulate_field_pocket.py), linhas 515–526.

<a id="finding-uni-017"></a>
**UNI-017 · “Sem falsificar” não é evidência de protocolo popperiano.** A documentação atual examinada rejeita expressamente a falsificação popperiana como método condutor. Nos registros históricos, `SEM FALSIFICAR` descreve integridade dos dados: não apagar rodadas, mudar janelas ou reescrever observáveis depois do resultado. Uma busca por palavras isoladas classificaria esse trecho incorretamente. Comparações convencionais e rótulos históricos também precisam de seu contexto original; não substituem as regras do autor. [Regras](project-rules.md), linhas 27–41; [definição histórica](../reference/records/triad-qm-blueprint.md), linhas 127–140.

<a id="every-study"></a>
## Cada estudo

Os status descrevem **o que o registro fornecido estabelece sobre sua operação**. Eles não classificam o valor de um estudo nem certificam uma conclusão científica. Uma entrada com vários arquivos pode reunir implementação que evolui e artefatos que somente leem; a linha explica a distinção relevante.

| Status | Entradas | Significado |
|---|---:|---|
| Termos conjuntos documentados | 14 | Fonte standalone e configuração registrada documentam operadores conjuntos, três memórias, dissipação e ruído FDT. Isso não afirma conformidade absoluta, convergência concluída ou certificação da execução. |
| Divergência de implementação documentada | 14 | Uma fonte/configuração diverge demonstravelmente da referência completa. Os resultados salvos mantêm suas condições efetivas. |
| Operação completa não estabelecida | 25 | A ausência de fonte, configuração, runtime fixado ou associação com a rodada impede estabelecer completude. |
| Contexto ou pós-processamento | 12 | Especificação, modelo conceitual de nós, representação ou leitura derivada, em vez de nova execução do campo completo. |

<details>
<summary>Critérios de “Termos conjuntos documentados”</summary>

Nesses quatorze registros standalone, as constantes examinadas incluem Λ=−10, α=0,15, σ=1,5, Γ=0,05, ν=(10; 0,5; 0,05), λ=(3; 1; 0,3) e kT=1. A atualização examinada inclui propagação cinética/fracionária, autointeração instantânea, três memórias em evolução, dissipação e banho gaussiano complexo acoplado. A normalização da condição inicial/entrada é distinguida da normalização durante a trajetória; esta última não foi encontrada nessas atualizações examinadas.

Os registros de bolsos incluem adições declaradas em t=0,5. Q03 declara uma correção de pós-processamento após a evolução. Q04 tem a questão de interpretação do residual apresentada acima. Precisão numérica, convergência em aberto e limites de vinculação entre fonte e registro continuam valendo. O status registra a operação conjunta documentada; não certifica cada requisito de implementação nem cada execução.

</details>

### Termos conjuntos documentados · 14

| Estudo | Escopo registrado | Fonte |
|---|---|---|
| <a id="study-t-30"></a>[Dois átomos](../../simulations/structures/two-atoms/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Duas sementes gaussianas; o rastreamento do par se perde após t=0,01. | [linhas 33–40](../../simulations/structures/two-atoms/code/simulate_two_atoms.py) |
| <a id="study-t-31"></a>[Gaussianas positivas aninhadas](../../simulations/structures/nested-positive-gaussians/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Sementes positivas concêntricas; o indicador de duas escalas permanece até t=0,02. | [linhas 33–40](../../simulations/structures/nested-positive-gaussians/code/simulate_nested_gaussians.py) |
| <a id="study-t-32"></a>[Átomo dentro de uma gaussiana maior](../../simulations/structures/atom-inside-a-larger-gaussian/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Envelope amplo e duas sementes internas com sinal; somente o quadro inicial preserva o par. | [linhas 39–46](../../simulations/structures/atom-inside-a-larger-gaussian/code/simulate_atom_inside_gaussian.py) |
| <a id="study-t-33"></a>[Ninho concêntrico positivo/negativo](../../simulations/structures/concentric-positive-negative-nest/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Ninho concêntrico com sinal; os indicadores de casca e sinal têm durações registradas distintas. | [linhas 33–40](../../simulations/structures/concentric-positive-negative-nest/code/simulate_signed_gaussian_nest.py) |
| <a id="study-t-34"></a>[Trajetória longa do ninho](../../simulations/structures/long-nest-trajectory/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Mesmo ninho prolongado até T=60; o resultado comum em t=8 coincide com a rodada curta. | [linhas 36–43](../../simulations/structures/long-nest-trajectory/code/simulate_long_gaussian_nest.py) |
| <a id="study-t-35"></a>[Pico finito, janela inicial](../../simulations/structures/finite-peak-early-window/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Janelas iniciais de uma e duas sementes; picos finitos ainda podem ocupar uma célula. | [linhas 51–58](../../simulations/structures/finite-peak-early-window/code/simulate_early_peak.py) |
| <a id="study-t-37"></a>[Um bolso no campo](../../simulations/structures/a-pocket-in-the-field/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Uma entrada gaussiana declarada é somada em t=0,5; trata-se de entrada no campo acoplado. | [linhas 32–39](../../simulations/structures/a-pocket-in-the-field/code/simulate_field_pocket.py) |
| <a id="study-t-38"></a>[Dois bolsos](../../simulations/structures/two-pockets/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Duas entradas gaussianas declaradas, com sinais opostos, são somadas em t=0,5. | [linhas 11–17](../../simulations/structures/two-pockets/code/simulate_two_field_pockets.py) |
| <a id="study-t-39"></a>[Mapas de densidade e memória](../../simulations/structures/density-memory-maps/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. O runner evolui novamente o caso do bolso plantado e registra mapas de densidade/memória; não é só leitor de imagens. | [linhas 11–17](../../simulations/structures/density-memory-maps/code/simulate_density_memory_maps.py) |
| <a id="study-q01"></a>[Convergência espacial](../../simulations/field-diagnostics/spatial-convergence/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. A convergência espacial permanece em aberto; o espectro registrado acompanha o corte da malha. | [linhas 36–43](../../simulations/field-diagnostics/spatial-convergence/code/measure_spatial_convergence.py) |
| <a id="study-q01b"></a>[Resolução e passo temporal](../../simulations/field-diagnostics/resolution-and-time-step/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. Refinos de espaço e passo temporal mantêm os termos conjuntos; a convergência numérica permanece em aberto. | [linhas 38–45](../../simulations/field-diagnostics/resolution-and-time-step/code/compare_grid_and_time_step.py) |
| <a id="study-q02"></a>[Um conjunto de condições iniciais](../../simulations/field-diagnostics/seed-ensemble/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. As 32 sementes registradas são finitas; o lote usa complex64/float32 e declara a mudança de precisão. | [linhas 45–52](../../simulations/field-diagnostics/seed-ensemble/code/simulate_seed_ensemble.py) |
| <a id="study-q03"></a>[Modos e subespaços do campo](../../simulations/field-diagnostics/field-modes/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. A fonte inclui evolução e POD/DMD passivos; a correção de pós-processamento está declarada. | [linhas 52–59](../../simulations/field-diagnostics/field-modes/code/analyze_field_modes.py) |
| <a id="study-q04"></a>[Testando a linearidade](../../simulations/field-diagnostics/linearity-tests/README.pt-BR.md) | A atualização standalone fornecida documenta os termos conjuntos e três modos de memória com FDT ativo. O residual de superposição inclui o banho aditivo comum; não mede somente a resposta não linear. | [linhas 54–61](../../simulations/field-diagnostics/linearity-tests/code/probe_field_linearity.py) |

### Divergência de implementação documentada · 14

| Estudo | Escopo registrado | Fonte |
|---|---|---|
| <a id="study-bravais-01-field"></a>[Campo 3D emergente](../../simulations/geometry/field-3d/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. | [linhas 241–253](../../simulations/geometry/field-3d/code/pt-BR/bravais_puro_3d.py) |
| <a id="study-bravais-03-scale"></a>[Escala própria](../../simulations/geometry/scale-sweep/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. | [linhas 175–185](../../simulations/geometry/scale-sweep/code/pt-BR/bravais_sweep_L.py) |
| <a id="study-t-16"></a>[Memória com resolução 40](../../simulations/memory/memory-grid-40/README.pt-BR.md) | A comparação salva inclui explicitamente um ramo sem memória. A fonte geradora do ramo chamado full está ausente. | [linhas 12–24](../../simulations/memory/memory-grid-40/notes/original-record.md) |
| <a id="study-t-29"></a>[Memória com amplitude pequena](../../simulations/memory/memory-small-amplitude/README.pt-BR.md) | A rodada fixa alpha=0 e usa dois modos de memória; seu banho está ativo. | [linhas 2–6](../../simulations/memory/memory-small-amplitude/code/simulate_memory_small_amplitude.py) |
| <a id="study-t-36"></a>[Dossiê de reexecução em dez partes](../../simulations/numerical-checks/reproduction-dossier/README.pt-BR.md) | O dossiê mistura checagens numéricas/analíticas com comparações registradas de termos desligados, incluindo memória desligada, banho desligado e memória congelada. | [linhas 10–18](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md) |
| <a id="study-field-2d"></a>[Explorações de campo 2D](../../simulations/geometry/field-2d/README.pt-BR.md) | As implementações 1D/2D fornecidas incluem normalização durante a trajetória ou guards e divergem da evolução de referência; a expressão de dissipação do caso 2D puro atua como fase. | [linhas 208–221](../../simulations/geometry/field-2d/code/bravais_pure_emerge.py) |
| <a id="study-dimension-comparison"></a>[Comparação entre 2D e 3D](../../simulations/geometry/dimension-comparison/README.pt-BR.md) | Os dois ramos dimensionais normalizam o campo a cada passo (normas-alvo 3,0 e 2,2) e usam atualização diferente da referência. | [linhas 84–94](../../simulations/geometry/dimension-comparison/code/bravais_long_2d3d.py) |
| <a id="study-vibrations"></a>[Cordas e vibração](../../simulations/geometry/vibrations/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. O leitor separado bravais_vibracoes é uma reconstrução cinemática. | [linhas 173–183](../../simulations/geometry/vibrations/code/bravais_cordas_vibracoes.py) |
| <a id="study-field-visualizations"></a>[Filmes e leituras visuais do campo](../../simulations/geometry/field-visualizations/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. Isso se aplica a simula_filmes; os outros cinco arquivos são leitores/renderizadores. | [linhas 234–246](../../simulations/geometry/field-visualizations/code/simula_filmes.py) |
| <a id="study-perturbation-tests"></a>[Respostas a perturbações](../../simulations/signals/perturbation-tests/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. | [linhas 247–259](../../simulations/signals/perturbation-tests/code/teste_borboleta.py) |
| <a id="study-wifi-input"></a>[Campos iniciados por leituras WiFi](../../simulations/signals/wifi-input/README.pt-BR.md) | A fonte fornecida usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência. As medidas WiFi necessárias não foram fornecidas; esta entrada não documenta uma execução demonstrada com essas medidas. | [linhas 226–235](../../simulations/signals/wifi-input/code/bravais_wifi.py) |
| <a id="study-string-structure-tests"></a>[Cordas, átomos e escala](../../simulations/structures/string-structure-tests/README.pt-BR.md) | A fonte de evolução usa sinal cinético/atualização de ruído e guards condicionais de estado diferentes da referência; as saídas salvas permanecem registros dessa implementação. | [linhas 256–268](../../simulations/structures/string-structure-tests/code/probe_box_size_and_amplitude.py) |
| <a id="study-passive-r5"></a>[Dinâmica passiva da memória](../../simulations/memory/passive-memory-dynamics/README.pt-BR.md) | O runner fixa alpha, Gamma e FDT em zero e mantém dois modos de memória. | [linhas 23–25](../../simulations/memory/passive-memory-dynamics/code/simulate_passive_memory.py) |
| <a id="study-causal-traces"></a>[Rastreamento de efeitos causais](../../simulations/continuity/causal-traces/README.pt-BR.md) | Quatro runners causais usam atualização determinística com duas memórias, sem termos fracionário/banho. | [linhas 22–25](../../simulations/continuity/causal-traces/code/soul_causal_probe_short.py) |

### Operação completa não estabelecida · 25

| Estudo | Escopo registrado | Fonte |
|---|---|---|
| <a id="study-t-01"></a>[Relações iniciais do campo](../../simulations/relations/early-field-relations/README.pt-BR.md) | Restam imagens de relações de campo e descrição isolado/acoplado, sem gerador ou tabela numérica. | [linhas 10–27](../../simulations/relations/early-field-relations/notes/original-record.md) |
| <a id="study-t-02"></a>[Memória e ruído térmico](../../simulations/memory/memory-and-thermal-noise/README.pt-BR.md) | A exploração NLS/memória/banho foi preservada em figuras; não há fonte ou tabela que fixe o operador executado. | [linhas 10–27](../../simulations/memory/memory-and-thermal-noise/notes/original-record.md) |
| <a id="study-t-03"></a>[Rastreamento de picos](../../simulations/memory/tracking-density-peaks/README.pt-BR.md) | Restam figuras de rastreamento de picos, sem o gerador revisto nem amostras numéricas. | [linhas 10–27](../../simulations/memory/tracking-density-peaks/notes/original-record.md) |
| <a id="study-t-04"></a>[Átomos gaussianos em um campo](../../simulations/structures/gaussian-atoms-in-one-field/README.pt-BR.md) | A exploração com múltiplas gaussianas tem figuras, sem fonte salva ou CSV. | [linhas 10–27](../../simulations/structures/gaussian-atoms-in-one-field/notes/original-record.md) |
| <a id="study-t-05"></a>[Campos individuais](../../simulations/structures/individual-fields/README.pt-BR.md) | Campos de identidade separada são descritos visualmente; implementação e CSV estão ausentes. | [linhas 10–27](../../simulations/structures/individual-fields/notes/original-record.md) |
| <a id="study-t-06"></a>[Tentativa de teste de limite](../../simulations/signals/limit-test-attempt/README.pt-BR.md) | Somente nota de preparação; não há artefatos persistidos de execução. | [linhas 10–20](../../simulations/signals/limit-test-attempt/notes/original-record.md) |
| <a id="study-t-07"></a>[Varredura rápida de limite](../../simulations/signals/fast-limit-sweep/README.pt-BR.md) | A varredura N/raio tem valores CSV, mas não há gerador fornecido que estabeleça a dinâmica completa. | [linhas 10–27](../../simulations/signals/fast-limit-sweep/notes/original-record.md) |
| <a id="study-t-08"></a>[Relações de observação em um campo](../../simulations/relations/observer-and-observed/README.pt-BR.md) | Existem CSVs baseline/observador; faltam o solver de campo e o mapeamento de parâmetros. | [linhas 10–27](../../simulations/relations/observer-and-observed/notes/original-record.md) |
| <a id="study-t-09"></a>[Campo contínuo de relações](../../simulations/relations/continuous-relational-field/README.pt-BR.md) | Existem dados baseline/relação contínua sem o solver gerador e a configuração completa. | [linhas 10–27](../../simulations/relations/continuous-relational-field/notes/original-record.md) |
| <a id="study-t-10"></a>[Exploração 3D de anti-colapso](../../simulations/memory/3d-anti-collapse-exploration/README.pt-BR.md) | A exploração inicial em 3D sobrevive apenas em figuras e notas. | [linhas 10–27](../../simulations/memory/3d-anti-collapse-exploration/notes/original-record.md) |
| <a id="study-t-11"></a>[Tentativa de execução longa](../../simulations/structures/long-run-attempt/README.pt-BR.md) | Somente nota de preparação; as saídas efetivas de longo prazo pertencem a outras entradas. | [linhas 10–18](../../simulations/structures/long-run-attempt/notes/original-record.md) |
| <a id="study-t-12"></a>[Execução longa 3D rápida](../../simulations/structures/fast-3d-long-run/README.pt-BR.md) | Cinco diagnósticos de longo prazo foram preservados em imagens, sem CSV ou gerador. | [linhas 10–27](../../simulations/structures/fast-3d-long-run/notes/original-record.md) |
| <a id="study-t-13"></a>[Execução longa 3D compacta](../../simulations/structures/compact-3d-long-run/README.pt-BR.md) | A montagem compacta e os diagnósticos de longo prazo não têm gerador salvo nem tabela numérica. | [linhas 10–24](../../simulations/structures/compact-3d-long-run/notes/original-record.md) |
| <a id="study-t-14"></a>[Tentativa de referência com memória](../../simulations/memory/memory-reference-attempt/README.pt-BR.md) | Somente preparação de rodada de referência; não há artefatos que estabeleçam execução. | [linhas 10–18](../../simulations/memory/memory-reference-attempt/notes/original-record.md) |
| <a id="study-t-15"></a>[Referência acelerada com memória](../../simulations/memory/accelerated-memory-reference/README.pt-BR.md) | Somente nota de preparação acelerada; as saídas começam no registro separado N=40. | [linhas 10–18](../../simulations/memory/accelerated-memory-reference/notes/original-record.md) |
| <a id="study-t-17"></a>[Memória com resolução 48](../../simulations/memory/memory-grid-48/README.pt-BR.md) | Há métricas N=48 e escores Bravais; faltam o gerador e a configuração exata dos termos. | [linhas 10–27](../../simulations/memory/memory-grid-48/notes/original-record.md) |
| <a id="study-t-19"></a>[Falha diagnóstica no banho quente](../../simulations/signals/hot-bath-diagnostic-failure/README.pt-BR.md) | O registro de banho quente tem CSVs, mas não fixa solver/configuração para conferir completude. | [linhas 10–27](../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md) |
| <a id="study-t-20"></a>[Caixa 3D com banho frio](../../simulations/signals/3d-cold-bath-box/README.pt-BR.md) | Os CSVs de banho frio mudam malha, duração e amostras iniciais junto às condições do banho. O gerador está ausente. | [linhas 10–27](../../simulations/signals/3d-cold-bath-box/notes/original-record.md) |
| <a id="study-t-21"></a>[Primeiro diagnóstico de fase para densidade](../../simulations/signals/first-phase-to-density-diagnostic/README.pt-BR.md) | O primeiro detector de fase/densidade registra estimativas próximas de zero; seu gerador está ausente. | [linhas 10–27](../../simulations/signals/first-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-22"></a>[Diagnóstico refinado de fase para densidade](../../simulations/signals/refined-phase-to-density-diagnostic/README.pt-BR.md) | O detector refinado muda o estímulo e a janela de observação; seu gerador está ausente. | [linhas 10–27](../../simulations/signals/refined-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-23"></a>[Memória e bounce](../../simulations/memory/memory-and-bounce/README.pt-BR.md) | Existem métricas de bounce e memória, mas a amplitude efetiva do banho e a fonte executada não estão completamente fixadas. | [linhas 10–27](../../simulations/memory/memory-and-bounce/notes/original-record.md) |
| <a id="study-t-27"></a>[Doze átomos iniciais](../../simulations/structures/twelve-atoms-full-field/README.pt-BR.md) | O runner chama um runtime triad-lang externo em caminho absoluto histórico; essa dependência executada não está fixada por hash. | [linhas 22–31](../../simulations/structures/twelve-atoms-full-field/code/simulate_twelve_atoms.py) |
| <a id="study-t-28"></a>[Trajetórias de átomos em 3D](../../simulations/structures/3d-atom-trajectories/README.pt-BR.md) | O runner de trajetórias 3D mantém três modos de memória e banho, mas importa o runtime histórico não fixado. | [linhas 24–33](../../simulations/structures/3d-atom-trajectories/code/simulate_atom_trajectories.py) |
| <a id="study-string-catalogue"></a>[Catálogo de cordas](../../simulations/geometry/string-catalogue/README.pt-BR.md) | O coletor importa padrões do solver e sobreposições de ambiente; as linhas registradas não fixam todas as configurações geradoras. | [linhas 29–55](../../simulations/geometry/string-catalogue/code/colhe_cordas.py) |
| <a id="study-persistent-universe"></a>[Protótipo de campo persistente](../../simulations/continuity/persistent-universe/README.pt-BR.md) | Há checkpoints modais, leituras e testes de continuidade; a evolução é delegada a uma biblioteca nativa externa ausente das fontes fornecidas. | [linhas 30–40](../../simulations/continuity/persistent-universe/code/genesis_modal.py) |

### Contexto ou pós-processamento · 12

| Estudo | Escopo registrado | Fonte |
|---|---|---|
| <a id="study-entre-01-observer"></a>[Observador e observado](../../simulations/relations/observer/README.pt-BR.md) | Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. | [linhas 116–138](../../simulations/relations/observer/code/en/simulate_observer_observed_relations.py) |
| <a id="study-entre-02-between"></a>[O entre](../../simulations/relations/between/README.pt-BR.md) | Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. | [linhas 88–101](../../simulations/relations/between/code/en/simulate_consciousness_between.py) |
| <a id="study-entre-03-chemistry"></a>[Oito canais acoplados](../../simulations/relations/chemical-channels/README.pt-BR.md) | Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. Camadas opcionais de química/vida são escolhas do modelo, não ablações diretas de P1/P2/P3. | [linhas 113–152](../../simulations/relations/chemical-channels/code/en/simulate_neurotransmitters_between.py) |
| <a id="study-entre-04-life-filter"></a>[Memória e filtro de vida](../../simulations/relations/life-filter/README.pt-BR.md) | Modelo de fases e memória de arestas em nós finitos para relações conceituais, não uma execução da equação de campo completa. Camadas opcionais de química/vida são escolhas do modelo, não ablações diretas de P1/P2/P3. | [linhas 139–184](../../simulations/relations/life-filter/code/en/simulate_life_filter_between.py) |
| <a id="study-bravais-02-strings"></a>[Cordas de um estado salvo](../../simulations/geometry/string-analysis/README.pt-BR.md) | Pós-processamento de estados de campo salvos; esta entrada não evolui a equação completa. | [linhas 1–12](../../simulations/geometry/string-analysis/code/cordas_arte.py) |
| <a id="study-visual-comparisons"></a>[Comparações visuais adicionais](../../simulations/geometry/visual-comparisons/README.pt-BR.md) | Comparações visuais preservadas sem associação estabelecida com uma rodada geradora. | [linhas 5–9](../../simulations/geometry/visual-comparisons/README.md) |
| <a id="study-t-18"></a>[Atlas visual](../../simulations/geometry/visual-atlas/README.pt-BR.md) | Leitura ou reconstrução geométrica de um campo registrado, não uma nova evolução de campo. | [linhas 10–22](../../simulations/geometry/visual-atlas/notes/original-record.md) |
| <a id="study-t-24"></a>[Mapa de templates Bravais](../../simulations/geometry/bravais-template-map/README.pt-BR.md) | Leitura ou reconstrução geométrica de um campo registrado, não uma nova evolução de campo. | [linhas 10–22](../../simulations/geometry/bravais-template-map/notes/original-record.md) |
| <a id="study-t-25"></a>[Primeira rede geométrica](../../simulations/geometry/first-geometric-network/README.pt-BR.md) | Leitura ou reconstrução geométrica de um campo registrado, não uma nova evolução de campo. | [linhas 10–22](../../simulations/geometry/first-geometric-network/notes/original-record.md) |
| <a id="study-t-26"></a>[Rede geométrica refinada](../../simulations/geometry/refined-geometric-network/README.pt-BR.md) | Leitura ou reconstrução geométrica de um campo registrado, não uma nova evolução de campo. | [linhas 10–22](../../simulations/geometry/refined-geometric-network/notes/original-record.md) |
| <a id="study-q00"></a>[Especificação de referência](../../simulations/field-diagnostics/reference-specification/README.pt-BR.md) | Especificação e parâmetros declarados fixados; esta entrada não contém resultado de execução. | [linhas 6–14](../../simulations/field-diagnostics/reference-specification/notes/specification-record.md) |
| <a id="study-dimension-analysis"></a>[Medidas de estrutura espacial](../../simulations/geometry/dimension-analysis/README.pt-BR.md) | Pós-processamento de estados de campo salvos; esta entrada não evolui a equação completa. | [linhas 1–12](../../simulations/geometry/dimension-analysis/code/bravais_dimensoes.py) |


<a id="coverage"></a>
## Cobertura e preservação

O inventário do catálogo cobre **65 entradas e 1.146 caminhos de arquivos associados**. Todos os **165 CSVs e 100 JSONs** foram lidos por parser sem erros de leitura. O inventário inclui **73 arquivos textuais de código**, dos quais **70 são Python, com 33.410 linhas**. O solver de referência e os [19 achados anteriores de fonte](../maintenance/author-rules-audit.md) acrescentam contexto à revisão.

O trabalho combinou inventário, hashes, leitura de arquivos estruturados e exame dirigido de kernels de evolução, configurações, registros numéricos e diagnósticos. **Foi estático e documental: zero reexecuções de simulação, zero edições de fontes científicas.** Arrays e imagens foram inventariados e tiveram seus hashes conferidos; nem todos foram reanalisados numérica ou visualmente. Registros acumulados extensos foram pesquisados e os trechos pertinentes examinados, sem uma nova leitura integral linha a linha.

Todos os **1.062 arquivos do catálogo que não são Markdown** coincidiram com os SHA-256 originais registrados e permaneceram intactos durante esta auditoria. Dos 84 Markdown do catálogo, 51 diferem dos hashes do arquivo original por reescrita documentada de links; isso não é reportado como alteração de conteúdo numérico. Mudanças de navegação e preservação das fontes têm proveniências distintas.

Correções de interpretação pertencem às fichas mantidas e a esta página. Código original, números, diagnósticos que falharam e vereditos históricos continuam disponíveis como registro. Um contraste numérico só é reportado quando medições salvas o sustentam; uma diferença de implementação, sozinha, não é apresentada como mudança medida de resultado.

Atribuição: `codex/equation_context_review` · tarefa `T-2026-0039` · 2026-09-18.

[Regras do projeto](project-rules.md) · [Referência da equação](../reference/equation/README.md) · [Auditoria anterior de implementação](../maintenance/author-rules-audit.md) · [Catálogo de simulações](../../simulations/README.pt-BR.md)
