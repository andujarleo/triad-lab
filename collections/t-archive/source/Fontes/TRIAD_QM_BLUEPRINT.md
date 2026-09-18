# TRIAD → MECÂNICA QUÂNTICA
## Blueprint auto-contido, de ponta a ponta, para investigar se a mecânica quântica pode emergir como leitura efetiva da dinâmica Triad

**Versão:** 1.0  
**Data-base do protocolo:** 2026-08-21  
**Escopo inicial:** mecânica quântica não relativística + sistemas quânticos abertos + informação quântica.  
**Fora do escopo do primeiro ciclo:** provar a Triad como descrição do universo, gravidade quântica, teoria das cordas, QFT relativística e cosmologia. Esses temas só entram depois que a etapa quântica estiver matematicamente fechada.

---

# 0. Objetivo em uma frase

Assumir a **Triad como substrato dinâmico de trabalho** e verificar, de forma quantitativa e reproduzível, até que ponto a matemática e os fenômenos conhecidos como **mecânica quântica** aparecem como descrição efetiva dessa dinâmica, sem modificar a Triad para produzir cada fenômeno.

A pergunta principal é:

> **Se um universo obedecer à dinâmica Triad completa, a mecânica quântica pode ser recuperada como uma descrição matemática efetiva desse universo?**

O objeto deste programa **não é provar que a Triad é verdadeira**.

O objeto é determinar se existe a seta:

\[
\boxed{
\text{Triad completa}
\Longrightarrow
\text{regime efetivo}
\Longrightarrow
\text{mecânica quântica}
}
\]

---

# 1. Hipótese de trabalho

Durante todo este projeto, adotamos provisoriamente:

\[
\boxed{\text{H}_{\mathrm{Triad}}:\;\text{a dinâmica Triad é o substrato físico do universo simulado}.}
\]

Isso é uma **hipótese operacional**, não uma conclusão do paper.

Partindo dela, investigaremos se conceitos que na linguagem quântica recebem nomes como:

- função de onda;
- superposição;
- interferência;
- quantização;
- incerteza;
- tunelamento;
- qubit;
- regra de Born;
- medição;
- decoerência;
- não-separabilidade;
- emaranhamento;
- Bell/CHSH;
- spin;
- estatística de troca;

podem ser reconhecidos como descrições de comportamentos produzidos por uma única dinâmica Triad.

---

# 2. Regra lógica fundamental

O programa inteiro obedece a quatro regras:

\[
\boxed{\text{SEM ISOLAR}}
\]

\[
\boxed{\text{SEM FALSIFICAR}}
\]

\[
\boxed{\text{SEM CALIBRAR}}
\]

\[
\boxed{\text{CAOS}\rightarrow\text{EQUILÍBRIO DINÂMICO}}
\]

Essas expressões precisam ter definições operacionais exatas para não gerar ambiguidade acadêmica.

## 2.1 SEM ISOLAR

Nos **runs que contam como evidência física**, a dinâmica Triad não será decomposta em versões especiais para cada fenômeno.

Não faremos, por exemplo:

- “Triad sem memória para estudar interferência”;
- “Triad sem FDT para estudar qubit”;
- “Triad linearizada para produzir espectro quântico”;
- “Triad com um termo novo para tunelamento”;
- “Triad modificada para Bell”.

A lei permanece inteira.

É permitido separar **observáveis depois da execução**:

\[
\rho=|\Psi|^2,\qquad
\phi=\arg\Psi,\qquad
V_{\rm mem},\qquad
J,\qquad
P(k),\qquad
\text{correlações},\ldots
\]

porque isso não altera a dinâmica. É apenas colocar sensores diferentes olhando para o mesmo universo.

### Importante: teste de software não é experimento físico

Pode ser necessário testar FFT, propagador, precisão numérica ou uma função individual do código. Isso é **engenharia de software**, não evidência sobre a física.

Esses testes ficam numa pasta separada (`solver_validation/`) e nunca são usados para afirmar que um fenômeno quântico emergiu da Triad.

Assim preservamos simultaneamente:

- rigor computacional acadêmico;
- não-isolamento da dinâmica física usada como evidência.

## 2.2 SEM FALSIFICAR

Neste projeto, “sem falsificar” significa:

1. não substituir a dinâmica acoplada por uma aproximação que mude o fenômeno e depois apresentar o resultado como se viesse da dinâmica completa;
2. não apagar runs inconvenientes;
3. não reconstruir retrospectivamente um resultado;
4. não escolher apenas seeds favoráveis;
5. não escolher apenas janelas temporais favoráveis;
6. não alterar a definição do observável depois de olhar o resultado;
7. não chamar de “resultado quântico” algo que foi explicitamente colocado no algoritmo.

**Isso não significa tornar a hipótese impossível de refutar.**

Ao contrário: cada benchmark deve poder retornar **compatível**, **parcial**, **incompatível** ou **inconclusivo**.

## 2.3 SEM CALIBRAR

Nenhum parâmetro da dinâmica será ajustado usando como objetivo “ficar parecido com a mecânica quântica”.

É proibido o loop:

```text
rodar → comparar com QM → mudar parâmetro → rodar → repetir até bater
```

O conjunto central de parâmetros deve ser congelado **antes** dos benchmarks quânticos confirmatórios.

Mudanças numéricas como aumentar resolução ou diminuir `dt` não contam como calibração física. Elas servem para verificar se o computador está resolvendo a mesma equação corretamente.

Mudanças de ambiente físico — por exemplo, adicionar uma barreira, uma caixa ou um potencial harmônico — também não mudam a lei, desde que seus valores sejam definidos previamente pelo protocolo do experimento e não ajustados depois para fazer o resultado bater.

## 2.4 CAOS → EQUILÍBRIO DINÂMICO

A dinâmica não procura um estado congelado.

O padrão esperado da Triad é:

\[
\text{estado inicial / perturbação}
\rightarrow
\text{caos / transiente}
\rightarrow
\text{auto-organização}
\rightarrow
\text{equilíbrio dinâmico}.
\]

Equilíbrio não significa:

\[
\partial_t\Psi=0.
\]

Pode existir:

- movimento residual;
- oscilação;
- troca entre modos;
- memória ativa;
- defeitos topológicos;
- mudanças locais;

com observáveis macroscópicos estabilizados estatisticamente.

---

# 3. A equação Triad usada como substrato

## 3.1 Campo principal

\[
i\hbar\,\partial_t\Psi=
\left[
-\frac{\hbar^2}{2m}\nabla^2
+V_{\rm ext}(\mathbf x)
+\Lambda|\Psi|^2
+V_{\rm mem}(t,\mathbf x)
+\alpha(-\Delta)^{\sigma/2}
-i\Gamma
\right]\Psi
+\eta(t,\mathbf x).
\tag{T1}
\]

## 3.2 Memória multiescala

\[
V_{\rm mem}(t,\mathbf x)=\sum_{j=1}^{M}\lambda_jy_j(t,\mathbf x),
\tag{T2}
\]

\[
\partial_ty_j(t,\mathbf x)
=\nu_j\left(|\Psi(t,\mathbf x)|^2-y_j(t,\mathbf x)\right).
\tag{T3}
\]

Cada modo possui escala temporal:

\[
\tau_j=\frac{1}{\nu_j}.
\]

## 3.3 Ruído ligado ao banho

\[
\langle\eta(t,\mathbf x)\eta^*(t',\mathbf x')\rangle
=
2\gamma_0k_BT\,
\delta(t-t')\delta^{(D)}(\mathbf x-\mathbf x'),
\tag{T4}
\]

\[
\langle\eta(t,\mathbf x)\eta(t',\mathbf x')\rangle=0.
\tag{T5}
\]

Na implementação atual, quando `fdt_couple=True`, a amplitude efetiva de FDT é ligada a `Gamma`, `kT`, `dx`, dimensão e `hbar`.

## 3.4 Densidade

\[
\rho(t,\mathbf x)=|\Psi(t,\mathbf x)|^2.
\tag{T6}
\]

## 3.5 Fase

\[
\Psi=Ae^{i\phi},
\qquad
\phi=\arg\Psi.
\tag{T7}
\]

## 3.6 Corrente associada ao campo

Como observável diagnóstico:

\[
\mathbf J
=\frac{\hbar}{m}\operatorname{Im}(\Psi^*\nabla\Psi).
\tag{T8}
\]

## 3.7 Operador fracionário

\[
\widehat{(-\Delta)^{\sigma/2}\Psi}(\mathbf k)
=|\mathbf k|^\sigma\hat\Psi(\mathbf k).
\tag{T9}
\]

---

# 4. Significado operacional do anti-colapso

No regime de interesse:

\[
\Lambda<0
\]

tende a concentrar o campo, enquanto memória repulsiva:

\[
\lambda_j>0
\]

responde à densidade histórica e pode contrariar concentração indefinida.

Não haverá `clip()`, teto manual de densidade ou regra “se ficar grande, empurra”.

A condição de finitude precisa ser consequência da própria evolução.

O programa quântico acompanhará continuamente:

\[
\rho_{\max},\qquad
|\nabla\Psi|_{\max},\qquad
|V_{\rm mem}|_{\max},\qquad
\ell_{\min},\qquad
\text{energia local/proxies}.
\]

A pergunta será:

> **Os comportamentos reconhecidos como quânticos continuam existindo enquanto as grandezas físicas convergem para valores finitos quando a resolução aumenta?**

---

# 5. Parâmetros: classificação para impedir calibração escondida

Todo parâmetro deve pertencer a uma das quatro classes abaixo.

## 5.1 Núcleo Triad — `Theta_core`

Parâmetros constitutivos que devem permanecer congelados durante o programa confirmatório:

\[
\Theta_{\rm core}
=
\{\Lambda,\alpha,\sigma,\Gamma,\nu_j,\lambda_j,\text{FDT lock}\}.
\]

### Candidato inicial pré-quântico

Uma escolha defensável é usar um conjunto que **já existia antes deste programa quântico**, por exemplo o regime de bounce/anti-colapso já registrado:

```text
hbar = 1
m = 1
Lambda = -10
alpha = 0.15
sigma = 1.5
Gamma = 0.05
nu = (10.0, 0.5, 0.05)
lambda = (3.0, 1.0, 0.3)
fdt_couple = True
kT = 1.0   # se este for o banho canônico escolhido em Q00
D = 3
bc = periodic
step_mode = strang
```

**Regra:** Q00 deve declarar o conjunto definitivo. Depois disso ele não pode ser alterado porque um benchmark quântico não bateu.

Caso seja escolhido outro conjunto já existente no registro pré-quântico, a decisão e sua origem devem ser documentadas antes de Q01.

## 5.2 Ambiente físico — `Xi_env`

Pode mudar de cenário para cenário porque descreve o experimento, não a lei:

- `V_ext`;
- geometria da caixa;
- barreiras;
- poços;
- separação física;
- orientação de um aparato;
- temperatura do ambiente, **somente se o protocolo definir previamente uma família física de temperaturas**.

Não pode ser ajustado depois de ver o resultado.

## 5.3 Condição inicial — `I0`

Pode variar:

- seed;
- posição;
- fase;
- largura;
- momento inicial;
- distribuição caótica;
- combinação de modos.

O protocolo define previamente a distribuição de condições iniciais.

## 5.4 Parâmetros numéricos — `N_num`

Não são física:

- `N`;
- `L` quando usado apenas para afastar bordas;
- `dt`;
- precisão fp32/fp64;
- backend CPU/CUDA/Metal;
- frequência de gravação.

Eles podem mudar para provar **convergência numérica**, mas a lei física permanece igual.

---

# 6. Auditoria de circularidade — parte obrigatória do paper

Há um ponto que precisa ser explicitado desde o início para que o trabalho seja academicamente correto.

A equação Triad atual já contém:

\[
i\hbar\partial_t
\]

e o termo cinético:

\[
-\frac{\hbar^2}{2m}\nabla^2,
\]

que é a estrutura cinética da equação de Schrödinger.

Portanto **não podemos afirmar que a forma inteira da equação de Schrödinger foi derivada do zero** usando a versão atual da Triad.

Isso cria três classes de evidência.

## 6.1 Evidência herdada — fraca para “derivar QM”

Fenômenos que já são fortemente favorecidos pela estrutura complexa/Schrödinger incorporada:

- propagação ondulatória;
- fase;
- interferência básica;
- dispersão livre;
- parte do comportamento de poços e osciladores.

Esses testes ainda são necessários, mas servem principalmente para verificar **consistência da dinâmica completa**, não para reivindicar derivação independente da QM.

## 6.2 Evidência não trivial — forte

Fenômenos que não entram automaticamente apenas porque existe um termo de Schrödinger:

- recuperação de linearidade efetiva apesar da dinâmica fundamental não linear e com memória;
- regra de Born sem codificá-la como regra de resultado;
- composição de subsistemas;
- tensor product efetivo;
- qubits físicos estáveis;
- dinâmica de Bloch/Rabi;
- medição física sem `collapse()`;
- decoerência emergente;
- não-separabilidade;
- Bell/CHSH;
- no-signaling;
- spin-1/2/SU(2);
- estatística de troca/fermionicidade;
- finitude no limite de resolução.

## 6.3 Derivação forte de primeiros princípios — projeto posterior

Para afirmar que **a própria estrutura de Schrödinger emerge** da Triad, seria necessário um substrato Triad ainda mais profundo no qual `i`, `hbar` e o operador cinético não sejam colocados inicialmente.

Isso é um **Track B posterior**, não deve ser misturado ao primeiro paper.

O primeiro objetivo é mais preciso:

> **Determinar se a dinâmica Triad completa possui um regime efetivo quantitativamente equivalente à mecânica quântica não relativística.**

---

# 7. O que significa “provar a mecânica quântica usando a Triad” neste projeto

Ciência experimental/numerical não usa “prova” no mesmo sentido de um teorema matemático.

Aqui, “provar” operacionalmente significa acumular evidências suficientes para estabelecer uma equivalência quantitativa dentro de um domínio declarado.

A afirmação máxima possível do primeiro ciclo será algo da forma:

> **Sob uma dinâmica Triad fixa, sem ajuste específico por fenômeno, observamos uma classe de estados efetivos cuja evolução, probabilidades, composição e correlações são quantitativamente compatíveis com a mecânica quântica não relativística dentro das incertezas numéricas e estatísticas declaradas.**

Se apenas parte disso funcionar, a conclusão precisa ser menor.

---

# 8. Escada de evidência

## Tier 0 — Integridade computacional

O computador resolve consistentemente a equação.

## Tier 1 — Fenomenologia de onda “quantum-like”

- fase;
- interferência;
- difração;
- tunelamento aparente;
- modos discretos.

Isso **não basta** para dizer que recuperamos QM.

## Tier 2 — Mecânica quântica efetiva de um sistema

- linearidade aproximada num subespaço;
- operador efetivo aproximadamente Hermitiano ou dinâmica quântica aberta bem definida;
- relações de espectro quantitativas;
- incerteza;
- regra de Born.

## Tier 3 — Estrutura de informação quântica

- sistemas de dois níveis;
- qubits;
- Bloch/Rabi;
- composição de dois subsistemas;
- não-separabilidade.

## Tier 4 — Núcleo forte da QM

- Bell/CHSH;
- no-signaling;
- medição/decoerência;
- spin-1/2;
- estatística de troca.

## Tier 5 — Generalização

- muitos corpos;
- gauge phase/Aharonov–Bohm;
- classes de potenciais não usadas no desenvolvimento;
- previsões cegas.

O título e a conclusão do paper são determinados pelo **maior Tier realmente alcançado**, não pelo objetivo desejado.

---

# 9. Motor numérico único

Todos os experimentos confirmatórios devem chamar o mesmo núcleo.

## 9.1 Passo Strang

Em cada `dt`:

1. meia etapa linear em Fourier;
2. voltar ao espaço real;
3. calcular `rho = |Psi|^2`;
4. atualizar todas as memórias `y_j`;
5. calcular `V_mem`;
6. aplicar simultaneamente `V_ext + Lambda*rho + V_mem`;
7. atualizar memória conforme o integrador definido;
8. aplicar FDT ligado ao banho;
9. segunda meia etapa linear;
10. gravar observáveis passivos.

Pseudocódigo:

```text
state = {Psi, y_1, ..., y_M}
lock Theta_core
initialize scenario I0 + Xi_env

for each time step:
    Psi = linear_half_step(Psi)

    rho = abs(Psi)^2
    y   = update_all_memory_modes(y, rho)
    Vmem = sum(lambda_j * y_j)

    Psi = full_real_space_interaction(
        Psi,
        V_ext + Lambda*rho + Vmem
    )

    y = update_all_memory_modes(y, abs(Psi)^2)
    Psi = inject_FDT(Psi)

    Psi = linear_half_step(Psi)

    record_passive_observables(state)
```

Nenhum observável gravado pode retornar para o solver e controlar o resultado, exceto variáveis que já façam parte explicitamente da equação/protocolo físico.

---

# 10. Observáveis padrão de todos os runs

Todo run deve gravar, no mínimo:

## 10.1 Campo

- `Psi_real` ou snapshots suficientes;
- `Psi_imag`;
- `rho = |Psi|^2`;
- `phase = arg(Psi)`.

## 10.2 Memória

- cada `y_j`;
- `V_mem`;
- overlap densidade–memória;
- atraso temporal entre eventos de densidade e memória.

## 10.3 Espaço

- pico de densidade;
- participação/IPR;
- raios de massa `r50`, `r80`, `r90` quando aplicáveis;
- comprimento de correlação;
- tamanho mínimo das estruturas.

## 10.4 Fourier

- espectro `|Psi_hat(k)|^2`;
- `k_*`;
- largura espectral;
- entropia espectral;
- picos de frequência temporal.

## 10.5 Fase/topologia

- gradiente de fase;
- circulação;
- winding:

\[
n=\frac{1}{2\pi}\oint\nabla\phi\cdot d\mathbf l;
\]

- linhas/loops de vórtice em 3D;
- reconexões topológicas.

## 10.6 Finitude

- `rho_max`;
- `|grad Psi|_max`;
- máximos de memória;
- escala mínima física;
- comportamento dessas quantidades quando `dx -> 0`.

---

# 11. Critério estatístico sem calibração

Não escolheremos uma tolerância porque “o resultado ficou perto”.

A tolerância nasce dos próprios erros independentes.

## 11.1 Erro numérico

Obtido em Q01 por convergência de `dt`, `dx`, precisão e backend:

\[
\epsilon_{\rm num}.
\]

## 11.2 Erro estatístico

Obtido da variação entre seeds:

\[
\epsilon_{\rm stat}.
\]

## 11.3 Erro total

\[
\epsilon_{\rm tot}
=
\sqrt{\epsilon_{\rm num}^2+\epsilon_{\rm stat}^2}.
\]

Uma previsão QM `Q_QM` e uma medida Triad `Q_T` podem ser comparadas por:

\[
z=\frac{Q_T-Q_{QM}}{\epsilon_{\rm tot}}.
\]

Para curvas completas usamos:

- RMSE normalizado;
- `chi^2` reduzido;
- likelihood;
- intervalos de confiança;
- comparação sem parâmetros ajustados ao benchmark sempre que possível.

Se algum mapeamento de unidades for necessário, ele deve ser definido **uma única vez** e aplicado a todos os testes subsequentes.

---

# 12. Registro obrigatório por experimento

Cada experimento gera uma pasta imutável:

```text
Qxx_nome/
├── PROTOCOL.md
├── config.json
├── code/
├── seeds.txt
├── raw/
├── metrics.csv
├── figures/
├── analysis.md
├── result.json
└── SHA256SUMS.txt
```

## `PROTOCOL.md`

Criado **antes do primeiro run confirmatório** e contém:

- pergunta;
- equação;
- hash do solver;
- `Theta_core`;
- variáveis de ambiente permitidas;
- condições iniciais;
- seeds ou regra de geração das seeds;
- número de runs;
- observáveis;
- algoritmo de análise;
- critérios de exclusão técnica;
- regra de comparação com QM.

Depois do hash, esse arquivo não é alterado. Correções geram `PROTOCOL_v2.md`, mantendo a versão original.

---

# 13. Resultados anteriores: como serão tratados

As simulações realizadas antes deste blueprint são **pilotos e evidência de motivação**, não dados confirmatórios do paper quântico.

Entre os comportamentos já observados estão:

- diferença intensa entre dinâmica full e no-memory no regime R5;
- propagação fase → densidade;
- contração → pico de densidade → resposta retardada da memória → expansão;
- organização Bravais/rede;
- dinâmica 3D de anti-colapso;
- windings de fase em um run caótico exploratório recente.

Eles ajudam a desenhar os protocolos, mas os benchmarks quânticos devem ser executados novamente sob o protocolo congelado.

Isso evita usar uma exploração anterior como se tivesse sido uma previsão confirmatória.

---

# 14. MAPA COMPLETO DE SIMULAÇÕES

A execução será dividida em oito fases.

---

# FASE A — Congelamento e integridade

## Q00 — Especificação canônica

### Objetivo

Congelar a versão física usada por todo o programa.

### Fazer

- escolher `Theta_core` usando exclusivamente informação existente antes dos benchmarks quânticos;
- registrar versão/hash de `solver.py`;
- fixar convenção de unidades;
- fixar convenção FDT;
- fixar definição de equilíbrio dinâmico;
- fixar formato de dados;
- fixar política de seeds;
- fixar critérios estatísticos.

### Saída

`TRIAD_QM_CANONICAL_V1.md`

### Regra

Depois de Q00, nenhum benchmark quântico pode alterar `Theta_core`.

---

## Q01 — Convergência numérica da dinâmica completa

### Pergunta

Os mesmos observáveis físicos convergem quando melhoramos a régua computacional?

### Runs

Mesma dinâmica completa em combinações previamente definidas, por exemplo:

```text
N: 32, 48, 64, 96

dt: dt0, dt0/2, dt0/4

fp64 em todos os confirmatórios
```

### Não mudar

`Theta_core`, estado físico e ambiente.

### Medir

- `rho_max`;
- participação;
- espectro;
- `k_*`;
- memória;
- winding;
- equilíbrio tardio;
- diferenças L2 entre resoluções.

### Resultado necessário

Determinar `epsilon_num` e identificar observáveis que ainda estão presos ao grid.

### Regra de segurança científica

Qualquer estrutura que permaneça em 1–2 células enquanto `N` aumenta é tratada como suspeita de artefato.

---

## Q02 — Ensemble caótico de referência

### Pergunta

Qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?

### Runs

Muitas seeds do mesmo macroestado caótico.

Primeiro lote exploratório: `>= 32` seeds.  
Lote confirmatório: `>= 100` seeds ou número determinado por análise de poder estatístico.

### Medir

Todos os observáveis padrão.

### Saída

Definir empiricamente:

- tempo de transiente;
- janela de equilíbrio;
- variabilidade natural;
- estrutura topológica típica;
- distribuição de escalas.

Nenhuma comparação com QM é usada para selecionar seeds.

---

# FASE B — Estrutura efetiva de uma partícula/onda

## Q03 — Identificação de subespaços persistentes

### Pergunta

A dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?

### Método

A partir de snapshots do campo completo, obter modos por métodos passivos como:

- decomposição espectral;
- PCA/POD;
- dynamic mode decomposition;
- eigenmodes de correlação.

Esses métodos **não controlam** o solver.

### Saída

Base efetiva candidata:

\[
\{\varphi_0,\varphi_1,\ldots,\varphi_n\}.
\]

E coeficientes:

\[
c_n(t)=\langle\varphi_n|\Psi(t)\rangle.
\]

---

## Q04 — Linearidade efetiva / superposição

A Triad fundamental é não linear. A QM padrão é linear no vetor de estado.

Portanto este é um teste central.

### Pergunta

Existe um regime macroscópico em que os coeficientes efetivos obedecem aproximadamente à superposição?

### Runs

Todos com a **Triad completa**:

- estado A;
- estado B;
- combinação previamente definida `aA + bB`.

Não se remove termo algum.

### Métrica

Depois de projetar no mesmo subespaço efetivo:

\[
R_{\rm lin}
=
\frac{\|\Pi F_t(aA+bB)-a\Pi F_t(A)-b\Pi F_t(B)\|}
{\|a\Pi F_t(A)\|+\|b\Pi F_t(B)\|}.
\]

### Interpretação

Se `R_lin` fica pequeno e converge com resolução em uma janela física, temos **linearidade emergente**, apesar do substrato não linear.

Se não ficar, a equivalência com QM linear fica limitada.

---

## Q05 — Propagação livre e relação `omega(k)`

### Pergunta

Qual relação dispersiva a dinâmica completa produz para perturbações efetivas?

### Ambiente

Região suficientemente livre, mantendo todos os termos Triad ativos.

### Medir

\[
\omega(k).
\]

Comparar a forma efetiva com:

\[
E=\hbar\omega,\qquad p=\hbar k,
\]

\[
E=\frac{p^2}{2m}
\]

quando aplicável.

### Nota de circularidade

O termo cinético já possui estrutura Schrödinger. Portanto este é um teste de **consistência da dinâmica full**, não uma derivação independente.

---

## Q06 — Fase → densidade

### Motivação

Já houve um piloto mostrando resposta física da densidade a uma perturbação de fase.

### Confirmatório

Definir perturbações de fase com amplitudes/escala espaciais pré-registradas e rodar ensembles completos.

### Medir

- frente de fase;
- frente de densidade;
- velocidade RMS;
- tempo de chegada;
- dispersão espectral;
- relação causal temporal fase→densidade.

### Pergunta

A fase funciona como variável dinâmica física do regime efetivo?

---

## Q07 — Interferência

### Setup

Duas excitações/coerências dentro do mesmo campo global, produzidas por condição inicial previamente definida.

### Não fazer

Não codificar “interference = |A+B|^2” como saída desejada.

### Medir

- densidade real do solver;
- fase relativa;
- posições dos máximos/mínimos;
- visibilidade das franjas;
- dependência com `Delta phi`.

### Benchmark

Comparar quantitativamente com a previsão da teoria quântica correspondente.

### Força da evidência

Baixa/média para derivação, porque interferência já é natural em campos complexos.

---

## Q08 — Difração / dupla abertura

### Setup

Mesmo substrato completo + potencial externo que representa uma parede com aberturas.

O potencial é uma condição ambiental, não uma mudança na lei.

### Medir

- padrão angular;
- espaçamento de franjas;
- dependência com largura/separação das aberturas;
- fase e corrente.

### Regra

Os parâmetros geométricos são definidos no protocolo, não ajustados para fazer a curva coincidir.

---

# FASE C — Quantização e dinâmica quântica efetiva

## Q09 — Poço/caixa

### Pergunta

O campo completo possui estados efetivos discretos quando confinado?

### Setup

Potencial externo de caixa/poço com dimensões pré-definidas.

### Método

Não procurar `n=1,2,3...` durante a evolução.

Depois do run, extrair frequências/modos persistentes.

### Benchmark

Para uma caixa ideal, verificar relações de razão compatíveis com:

\[
E_n\propto n^2.
\]

Usar **razões dimensionless** antes de qualquer conversão de unidade.

---

## Q10 — Oscilador harmônico

### Ambiente

\[
V_{\rm ext}=\frac12m\omega_0^2r^2.
\]

### Pergunta

A dinâmica full produz uma torre efetiva com espaçamento compatível com:

\[
E_n=\hbar\omega_0\left(n+\frac12\right)?
\]

### Observação

Como a estrutura Schrödinger já está parcialmente presente, o valor principal deste teste é verificar se **memória + não linearidade + FDT + anti-colapso** ainda admitem um regime efetivamente quântico, e não “descobrir” o oscilador do zero.

---

## Q11 — Reconstrução do gerador efetivo

Este é um dos testes matematicamente mais fortes.

### Ideia

Projetar a dinâmica full nos modos efetivos:

\[
\mathbf c(t)=(c_0,c_1,\ldots,c_n)^T.
\]

Tentar identificar, sem usar a resposta QM durante o ajuste estrutural:

\[
i\frac{d\mathbf c}{dt}\approx H_{\rm eff}\mathbf c.
\]

### Perguntas

1. `H_eff` é aproximadamente linear?
2. É aproximadamente constante no tempo na janela de equilíbrio?
3. É aproximadamente Hermitiano?
4. Suas previsões fora da janela usada para identificá-lo permanecem corretas?

### Métricas

\[
\epsilon_H
=\frac{\|H_{\rm eff}-H_{\rm eff}^\dagger\|}{\|H_{\rm eff}\|}.
\]

Erro de previsão em holdout temporal.

### Se o sistema efetivo for aberto

Em vez de forçar unitariedade, construir uma matriz de estado de ensemble e testar uma dinâmica efetiva aberta/Lindblad-like.

Não forçar Schrödinger se os dados disserem “sistema aberto”.

---

## Q12 — Relação de incerteza

### Definições

\[
\langle x\rangle
=\frac{\int x|\Psi|^2dx}{\int|\Psi|^2dx},
\]

\[
\Delta x^2=\langle x^2\rangle-\langle x\rangle^2.
\]

Momento diagnosticado em Fourier:

\[
p=\hbar k.
\]

\[
\Delta p^2=\langle p^2\rangle-\langle p\rangle^2.
\]

### Pergunta

Que limite inferior a dinâmica full estabelece empiricamente para:

\[
\Delta x\Delta p?
\]

### Comparação posterior

\[
\Delta x\Delta p\geq\frac{\hbar}{2}.
\]

Não selecionar apenas estados que satisfazem a relação; publicar a distribuição inteira.

---

## Q13 — Tunelamento

### Setup

Substrato full + barreira física `V_ext`.

### Medir

Probabilidade/densidade efetiva em cada lado, corrente e atraso temporal.

### Variações pré-registradas

- largura da barreira;
- altura;
- energia/modo inicial.

### Benchmark

Comparar a curva completa de transmissão:

\[
T_{\rm Triad}(E,V_0,a)
\]

com a curva QM correspondente.

### Regra

Nenhum termo `tunnel` é criado.

---

## Q14 — Quantização topológica

### Pergunta

A fase da dinâmica full produz invariantes inteiros persistentes?

### Medir

\[
n=\frac{1}{2\pi}\oint\nabla\phi\cdot d\mathbf l.
\]

Reconstruir em 3D:

- linhas de vórtice;
- loops fechados;
- reconexões;
- vida média;
- modos de vibração.

### Cuidado

Um winding inteiro é uma forma de quantização topológica, mas **não equivale sozinho à mecânica quântica**.

---

## Q15 — Estruturas localizadas persistentes

### Pergunta

O caos da dinâmica completa produz estruturas que podem atuar como objetos/quanta efetivos?

### Não definir “partícula” visualmente

Criar critérios objetivos antes da análise:

- localização relativa;
- persistência temporal;
- conservação aproximada de uma carga/propriedade;
- trajetória rastreável;
- sobrevivência a perturbações;
- colisões.

### Saída

Catálogo de excitações persistentes sem atribuir nomes de partículas conhecidas.

---

# FASE D — Probabilidade e medição

## Q16 — Detector físico Triad

Antes de testar Born, precisamos de um aparato cuja saída não seja simplesmente `abs(Psi)^2` escrito no código.

### Construção

O detector também é uma dinâmica Triad, ou uma região do mesmo campo global, com estados macroscópicos estáveis distinguíveis:

\[
D_0,D_1,\ldots,D_n.
\]

### Requisito

A classificação do resultado usa o estado macroscópico do detector, não a amplitude quântica que queremos testar.

Exemplo:

- qual bacia de memória do detector se estabilizou;
- orientação final de uma estrutura;
- região macroscópica excitada.

---

## Q17 — Regra de Born

Este é um dos testes centrais do programa.

### Preparação

Criar um macroestado efetivo:

\[
|\psi\rangle=\sum_i c_i|i\rangle.
\]

Os coeficientes são obtidos por projeção física nos modos efetivos, não usados para sortear artificialmente a saída.

### Ensemble

Executar muitas realizações com:

- mesmo macroestado;
- mesma lei;
- mesmo aparato;
- microseed diferente segundo protocolo pré-definido.

### Resultado

Contar estados macroscópicos do detector:

\[
f_i=\frac{N_i}{N_{\rm total}}.
\]

### Somente depois comparar

\[
f_i\stackrel{?}{\approx}|c_i|^2.
\]

### Estatística

- teste multinomial;
- `chi^2`;
- likelihood ratio;
- intervalos de confiança binomial/multinomial;
- curva de calibração **diagnóstica**, sem reajuste da dinâmica.

### Proibido

```text
outcome = random_choice(probability=abs(c)^2)
```

Isso colocaria Born por definição e tornaria o teste circular.

---

## Q18 — Medição sem `collapse()`

### Universo simulado

\[
U=S+D+E
\]

onde:

- `S` = sistema;
- `D` = detector;
- `E` = restante do ambiente;

mas tudo evolui dentro da dinâmica Triad completa.

### Pergunta

Uma configuração com múltiplos modos pode evoluir para um estado macroscópico do detector aparentemente definido sem regra externa de colapso?

### Medir

- estado global;
- estado reduzido efetivo de `S`;
- correlação `S-D`;
- memória;
- perda de coerência local;
- informação preservada globalmente.

---

## Q19 — Decoerência

### Pergunta

A perda aparente de interferência pode surgir pela redistribuição de fase/correlação no sistema completo?

### Não fazer

Não adicionar termo artificial “decoherence”.

### Medir

Matriz de coerência efetiva:

\[
C_{ij}(t)=\langle c_i(t)c_j^*(t)\rangle_{\rm ensemble}.
\]

Acompanhar termos fora da diagonal.

### Benchmark

Comparar formas/tempos de decoerência com modelos quânticos abertos apropriados, sem usar esses modelos para ajustar `Theta_core`.

---

# FASE E — Qubits e composição

## Q20 — Sistema físico de dois níveis

### Pergunta

Existem dois modos Triad robustos que formam um subespaço efetivo bidimensional?

\[
|0\rangle,\qquad|1\rangle.
\]

### Requisitos

- estabilidade;
- baixa fuga do subespaço;
- sobreposição controlável;
- fase relativa física;
- transformação contínua entre estados.

### Métrica de leakage

\[
L(t)=1-\sum_{i=0}^{1}|c_i(t)|^2
\]

após normalização apropriada do subespaço efetivo.

---

## Q21 — Geometria de Bloch

Para um estado efetivo de dois níveis:

\[
|\psi\rangle=\alpha|0\rangle+\beta|1\rangle.
\]

Construir observáveis equivalentes às coordenadas:

\[
x=2\operatorname{Re}(\alpha^*\beta),
\]

\[
y=2\operatorname{Im}(\alpha^*\beta),
\]

\[
z=|\alpha|^2-|\beta|^2.
\]

### Pergunta

As trajetórias do subespaço efetivo obedecem uma geometria equivalente à esfera de Bloch ou outra geometria?

Não forçar a esfera de Bloch; medir.

---

## Q22 — Oscilações/Rabi efetivas

### Ambiente

Uma interação externa periódica previamente definida acopla os dois modos, mas a dinâmica Triad inteira continua ativa.

### Pergunta

A ocupação efetiva oscila entre os dois estados com relações compatíveis com dinâmica de dois níveis?

### Medir

- frequência;
- contraste;
- leakage;
- dependência com amplitude/frequência da interação.

---

## Q23 — Composição de dois subsistemas

A QM exige mais do que dois qubits separados: exige uma regra de composição equivalente a tensor product.

### Construção

Dois subespaços efetivos A e B, dentro do universo Triad global.

Base candidata:

\[
|00\rangle,|01\rangle,|10\rangle,|11\rangle.
\]

### Pergunta

O espaço efetivo conjunto possui quatro graus de liberdade coerentes com a composição de dois sistemas de dois níveis?

### Testes

- dimensionalidade efetiva;
- operações locais;
- correlações;
- fatorabilidade de estados independentes.

Se essa estrutura não aparecer, não é legítimo falar em qubits compostos no sentido padrão.

---

# FASE F — Não-separabilidade e Bell

## Q24 — Estados não separáveis

### Pergunta

Existem estados efetivos conjuntos que não podem ser escritos como produto de estados de A e B?

\[
|\Psi_{AB}\rangle\neq|\psi_A\rangle\otimes|\psi_B\rangle.
\]

### Diagnósticos

- rank de Schmidt efetivo;
- entropia de entrelaçamento efetiva, se a construção do espaço permitir;
- mutual information;
- correlações conectadas.

Correlação comum não basta. Precisamos demonstrar **não-fatorabilidade** da descrição efetiva.

---

## Q25 — Bell / CHSH

Este é um dos benchmarks mais importantes.

### Setup

Dois subsistemas efetivos A e B.

Cada lado possui duas configurações locais de medição:

\[
a,a',b,b'.
\]

Cada execução produz resultados binários:

\[
A\in\{-1,+1\},\qquad B\in\{-1,+1\}.
\]

### Correlação

\[
E(a,b)=\langle AB\rangle.
\]

### CHSH

\[
S=E(a,b)+E(a,b')+E(a',b)-E(a',b').
\]

Limite Bell local clássico sob suas hipóteses:

\[
|S|\le2.
\]

Máximo quântico:

\[
|S|\le2\sqrt2.
\]

### Regras críticas

- nenhuma seleção pós-run de eventos favoráveis;
- nenhuma alteração de setting depois de olhar o estado;
- settings gerados independentemente da seed física segundo protocolo;
- todos os eventos válidos entram;
- detector e setting têm implementação local definida antes do run;
- publicar marginais e joint distributions completas.

### Interpretação

O valor produzido pela Triad é o resultado. Não há meta “2.828”.

---

## Q26 — No-signaling

Bell-like correlations não podem ser confundidas com um canal de comunicação superluminal no formalismo QM.

### Teste

Verificar se a distribuição marginal local de A independe da escolha remota de B:

\[
P(A|a,b)\stackrel{?}{=}P(A|a,b').
\]

E reciprocamente:

\[
P(B|a,b)\stackrel{?}{=}P(B|a',b).
\]

### Estatística

Testes de igualdade de proporções/distribuições com intervalos de confiança pré-definidos.

Bell + no-signaling seria muito mais forte do que correlação isolada.

---

# FASE G — Spin, estatística e benchmarks avançados

## Q27 — Busca por estrutura spinorial / spin-1/2

A Triad atual usa um **campo escalar complexo**.

Isso é um ponto crítico: spin-1/2 não deve ser assumido.

### Pergunta

Pode surgir da dinâmica uma estrutura efetiva de dois componentes com transformação SU(2), incluindo comportamento de rotação característico de spin-1/2?

### Requisitos fortes

- dois componentes efetivos;
- operações de rotação;
- relação SU(2);
- retorno completo após `4π`, não apenas `2π`, se o objeto for realmente spinorial;
- respostas análogas a Stern–Gerlach.

### Regra de escopo

Se isso não aparecer, a conclusão deve ficar limitada a **QM escalar/bosônica não relativística**.

Não adicionar spin manualmente e depois afirmar que emergiu.

---

## Q28 — Estatística de troca

Outro teste forte.

### Pergunta

Duas excitações idênticas apresentam, ao serem trocadas, comportamento efetivo:

- simétrico (bosônico);
- antissimétrico (fermiónico);
- outro/topológico?

### Medir

Fase efetiva sob troca, ocupações e estados de dois objetos.

### Importância

O campo escalar Gross–Pitaevskii-like naturalmente se aproxima de descrição bosônica. Fermionicidade precisa ser demonstrada, não presumida.

Se não houver antisymmetry emergente, não reivindicar recuperação de fermions.

---

## Q29 — Fase de gauge / Aharonov–Bohm-like

Benchmark avançado da importância física da fase.

### Objetivo

Criar uma geometria na qual duas trajetórias efetivas acumulam fase diferente sem força clássica local equivalente na região percorrida.

### Pergunta

A diferença de fase produz deslocamento de interferência compatível com a estrutura quântica de gauge?

Este teste só entra depois dos Tiers anteriores.

---

## Q30 — Muitos corpos

Somente após a composição de dois subsistemas estar fechada.

### Investigar

- 3, 4, 8 ... subsistemas efetivos;
- crescimento do espaço de estados;
- correlações multipartidas;
- GHZ/W-like classes se aplicável;
- estabilidade de qubits dentro do campo global.

Não chamar uma rede de modos de “muitos qubits” sem demonstrar a regra de composição.

---

# FASE H — Finitude, predição cega, reprodução e TriadLang

## Q31 — Limite contínuo e “não infinito”

Este teste atravessa todos os demais, mas recebe análise própria.

### Pergunta

Quando `dx -> 0`, as quantidades físicas convergem ou divergem?

### Resoluções

Usar série crescente de `N` com domínio físico constante.

### Dois modelos concorrentes para uma grandeza como `rho_max`

Modelo finito:

\[
\rho_{\max}(dx)=\rho_\infty+A\,dx^p.
\]

Modelo divergente:

\[
\rho_{\max}(dx)=B\,dx^{-q}.
\]

Comparar qualidade dos modelos sem escolher visualmente.

### Comprimento mínimo

Uma estrutura física deve satisfazer:

\[
\ell_{\rm core}(dx)\rightarrow\ell_0>0
\]

em unidades físicas.

Se permanecer sempre com 1–2 células:

\[
\ell_{\rm core}\sim dx,
\]

é suspeita de artefato da grade.

### Resultado desejado metodologicamente

Não “finitude porque queremos”.

Resultado legítimo é um entre:

- converge para finito;
- diverge;
- inconclusivo na resolução disponível.

---

## Q32 — Benchmark cego / holdout

Para evitar desenho retrospectivo da análise:

1. usar Q03–Q31 para fechar a metodologia;
2. congelar todo o pipeline;
3. escolher fenômenos/sistemas quânticos **não usados** no desenvolvimento;
4. gerar previsões Triad antes de abrir/comparar a solução QM de referência;
5. registrar hash das previsões;
6. somente então comparar.

Exemplos possíveis de holdout:

- outro formato de poço;
- scattering por potencial não usado;
- quench de dois níveis;
- sequência temporal inédita;
- uma relação espectral não usada no desenvolvimento.

Esta é uma das etapas mais importantes para transformar “encaixe” em **poder preditivo**.

---

## Q33 — Reprodução cruzada de backend

Executar os mesmos protocolos em:

- NumPy/CPU;
- implementação nativa TriadLang CPU;
- CUDA no Linux quando disponível;
- Metal/Mac quando suportado.

### Comparar

- observáveis físicos, não bit-a-bit quando a ordem de floating point diferir;
- distribuições em runs estocásticos;
- erros dentro de `epsilon_num`.

Isso evita que o resultado dependa de um único backend.

---

## Q34 — Ponte física → TriadLang

Somente depois de existir um objeto efetivo que realmente satisfaz critérios de qubit.

### Objetivo

Mapear:

\[
|0\rangle_{\rm físico}
\leftrightarrow
\texttt{TriadLang qubit 0},
\]

\[
|1\rangle_{\rm físico}
\leftrightarrow
\texttt{TriadLang qubit 1}.
\]

E:

\[
\alpha|0\rangle+\beta|1\rangle
\leftrightarrow
\text{estado interno da linguagem}.
\]

### Testes

- preparação;
- evolução livre;
- fase;
- operações equivalentes a X/Y/Z;
- rotações;
- dois qubits;
- Bell;
- fidelidade;
- leakage;
- estabilidade temporal.

### Regra

TriadLang não define retroativamente o qubit físico. O objeto físico vem primeiro; a linguagem é validada contra ele depois.

---

## Q35 — Reprodução independente

Preparar um pacote executável por terceiros:

```text
release/
├── README.md
├── equation.md
├── protocols/
├── solver/
├── configs/
├── seeds/
├── raw_subset/
├── analysis/
├── environment.yml / lockfile
├── Dockerfile opcional
└── SHA256SUMS.txt
```

Uma pessoa externa deve conseguir:

1. instalar;
2. rodar;
3. obter os mesmos observáveis dentro da tolerância;
4. executar análise sem intervenção manual.

---

# 15. Testes adicionais que podem virar apêndices

Não são necessários para o primeiro claim, mas ajudam a fechar a estrutura.

## 15.1 Ehrenfest-like relations

Verificar se médias efetivas obedecem relações equivalentes a movimento clássico no limite apropriado.

## 15.2 Correspondência clássico-quântica

Aumentar escala/ocupação e verificar se o comportamento efetivo tende a trajetórias clássicas onde deveria.

## 15.3 Scattering

Calcular amplitudes de reflexão/transmissão para potenciais simples.

## 15.4 Efeito Zeno-like

Somente depois de o detector físico estar definido: verificar se interações repetidas alteram transições sem programar “Zeno”.

## 15.5 Leggett–Garg/contextualidade

Se Bell funcionar, investigar temporal/contextual quantum correlations como benchmarks independentes.

---

# 16. O que NÃO pode ser usado como evidência suficiente

Nenhum item abaixo, sozinho, prova recuperação da QM:

- “a imagem parece quântica”;
- “surgiram ondas”;
- “surgiu interferência”;
- “existem gaussianos”;
- “há windings inteiros”;
- “o campo tunelou visualmente”;
- “a curva lembra Schrödinger”;
- “há correlação entre dois pontos”;
- “existe uma estrutura parecida com corda”;
- “um qubit da TriadLang executa gates”.

O projeto precisa subir a escada quantitativa até probabilidades, composição, não-separabilidade e, idealmente, Bell/no-signaling.

---

# 17. Problemas difíceis que precisamos encarar, não esconder

## 17.1 Não linearidade

QM padrão é linear no estado. Triad é não linear.

Logo precisamos mostrar **linearidade efetiva emergente** em algum subespaço, ou concluir que a equivalência é apenas parcial.

## 17.2 FDT/dissipação

Triad fundamental possui banho/dissipação na implementação atual.

QM fechada é unitária, mas QM de sistemas abertos não é.

Portanto devemos deixar os dados responderem se o regime efetivo é:

- aproximadamente Schrödinger/unitário;
- ou naturalmente quantum-open/Lindblad-like.

Não desligar o banho apenas para obter unitariedade.

## 17.3 Regra de Born

Não vem automaticamente de um campo complexo. Precisa emergir das frequências de resultados de um detector físico.

## 17.4 Tensor product

Não vem automaticamente de uma rede. Precisa existir uma regra efetiva de composição.

## 17.5 Bell

Correlação global comum não basta. Precisamos de protocolo CHSH completo, sem pós-seleção e com marginais.

## 17.6 Spin e fermions

Um campo escalar complexo não contém spin-1/2/fermionicidade por definição.

Ou essas estruturas emergem de topologia/modos internos, ou o escopo da equivalência deve ser reduzido.

## 17.7 “Não infinito”

Um valor finito em grid finito não é prova de finitude física.

A evidência precisa vir da convergência quando `dx -> 0`.

---

# 18. Política de resultados negativos

Cada teste termina com um status padronizado:

```text
SUPPORTED
PARTIAL
NOT_SUPPORTED
INCONCLUSIVE
NUMERICAL_FAILURE
```

## `SUPPORTED`

Compatibilidade quantitativa dentro da incerteza previamente determinada.

## `PARTIAL`

Parte da estrutura aparece, mas uma relação necessária falha.

## `NOT_SUPPORTED`

Resultado converge e é incompatível com o benchmark.

## `INCONCLUSIVE`

Resolução/seeds/tempo ainda não permitem distinguir.

## `NUMERICAL_FAILURE`

A execução não satisfaz integridade computacional; não é interpretada fisicamente.

Nenhum status é removido do registro.

---

# 19. Separação Discovery / Confirmatory sem calibrar

Para evitar que exploração e confirmação sejam confundidas:

## Discovery

- entender observáveis;
- encontrar bugs;
- estimar custo;
- descobrir tempo necessário de run;
- definir algoritmo de extração.

**Não pode otimizar `Theta_core` contra QM.**

## Confirmatory

- protocolo já hashado;
- parâmetros congelados;
- seeds definidas por regra prévia;
- análise congelada;
- comparação executada sem alteração posterior.

Se um problema for encontrado, cria-se uma nova versão e repete-se o conjunto inteiro relevante; o resultado anterior permanece arquivado.

---

# 20. Ordem exata de execução

```text
Q00  congelar especificação
  ↓
Q01  convergência numérica full
  ↓
Q02  ensemble caótico baseline
  ↓
Q03  modos/subespaços efetivos
  ↓
Q04  linearidade emergente
  ↓
Q05  dispersão
Q06  fase→densidade
Q07  interferência
Q08  difração
  ↓
Q09  caixa
Q10  oscilador
Q11  gerador efetivo H_eff
Q12  incerteza
Q13  tunelamento
Q14  topologia
Q15  quanta localizados
  ↓
Q16  detector físico
Q17  Born
Q18  medição
Q19  decoerência
  ↓
Q20  dois níveis
Q21  Bloch
Q22  Rabi
Q23  composição
  ↓
Q24  não-separabilidade
Q25  CHSH
Q26  no-signaling
  ↓
Q27  spin
Q28  troca
Q29  gauge phase
Q30  muitos corpos
  ↓
Q31  análise formal de finitude
Q32  holdout cego
Q33  backends
Q34  TriadLang
Q35  reprodução externa
  ↓
PAPER
```

---

# 21. Critérios de parada

Não precisamos executar todos os testes cegamente se uma condição fundamental falhar de forma convergente.

## Parada A

Se Q01 não converge: corrigir engenharia numérica antes de qualquer interpretação.

## Parada B

Se Q04 mostrar ausência robusta de qualquer linearidade efetiva: a equivalência com QM linear precisa ser reformulada antes de prosseguir para claims fortes.

## Parada C

Se Q17 rejeitar Born de forma robusta: não afirmar equivalência operacional com QM padrão.

## Parada D

Se Q23 não produzir composição de subsistemas: não falar em entanglement/qubits compostos no sentido padrão.

## Parada E

Se Q25/26 falharem: limitar a conclusão ao Tier alcançado.

Isso não “mata” a Triad; apenas delimita o quanto da mecânica quântica a dinâmica reproduz.

---

# 22. Estrutura do paper final

## Título provisório conservador

**Emergent Quantum Mechanics in a Nonlinear Complex Field with Multiscale Memory and Anti-Collapse**

O título deve ser reduzido se os dados alcançarem apenas uma parte da QM.

## Abstract

- problema;
- dinâmica assumida;
- regra de parâmetros fixos;
- benchmarks;
- resultados quantitativos;
- maior claim suportado;
- limitações.

## 1. Introduction

Pergunta:

> Uma dinâmica contínua, não linear, com memória e anti-colapso pode possuir um regime efetivo quantitativamente equivalente à mecânica quântica?

## 2. Triad Dynamics

Equações T1–T9, sem interpretação excessiva.

## 3. Methodological Constraints

Explicar formalmente:

- no phenomenon-specific ablation;
- no target-driven calibration;
- full dynamics active;
- diagnostic separation only;
- preregistration/versioning;
- complete failure retention.

## 4. Numerical Method

- Strang split;
- FFT;
- memória;
- FDT;
- precisão;
- convergência.

## 5. Effective-State Construction

Como modos/subespaços são extraídos sem controlar a dinâmica.

## 6. Single-System Quantum Benchmarks

Q04–Q15.

## 7. Probability and Measurement

Q16–Q19.

## 8. Quantum Information Structure

Q20–Q26.

## 9. Spin/Exchange/Advanced Tests

Somente se suportados.

## 10. Finite Continuum Limit

Q31.

## 11. Blind Holdout

Q32.

## 12. Discussion

O que é herdado da estrutura Schrödinger existente e o que é realmente emergente.

## 13. Limitations

Obrigatório incluir:

- scalar field limitation;
- current use of Schrödinger kinetic structure;
- finite computational resolution;
- stochastic sampling;
- scope nonrelativistic.

## 14. Conclusion

Somente o maior Tier realmente atingido.

---

# 23. Possíveis conclusões e o que cada uma permite dizer

## Cenário A — apenas fenômenos de onda

Dizer:

> “A dinâmica produz comportamento quantum-like em determinados observáveis.”

Não dizer:

> “QM emerge da Triad.”

## Cenário B — Born + linearidade efetiva + espectros

Dizer:

> “Um setor da mecânica quântica não relativística é recuperado como dinâmica efetiva.”

## Cenário C — qubits + composição + Bell + no-signaling

Dizer:

> “A dinâmica recupera estrutura operacional central da mecânica quântica/informação quântica dentro do domínio estudado.”

## Cenário D — spin + troca + holdout + finitude

A afirmação pode ser significativamente mais ampla, sempre lembrando a auditoria de circularidade da equação fundamental atual.

---

# 24. O que ficará para um segundo paper

Se o primeiro programa funcionar, o próximo passo não deve ser imediatamente cosmologia.

O segundo problema seria:

\[
\boxed{
\text{É possível obter a própria estrutura }i\hbar\partial_t
\text{ e o operador cinético a partir de uma Triad mais fundamental?}
}
\]

Esse seria o caminho para remover a principal circularidade atual.

Somente depois faria sentido tentar unificar formalmente:

- QM;
- espaço-tempo emergente;
- gravidade;
- estruturas 1D/“cordas”;
- cosmologia.

---

# 25. Ponte posterior para TriadLang

A TriadLang entra **depois**, não como evidência inicial.

Fluxo correto:

\[
\boxed{
\text{Triad física}
\rightarrow
\text{estado quântico efetivo}
\rightarrow
\text{qubit físico}
\rightarrow
\text{TriadLang}
}
\]

Não:

\[
\text{TriadLang tem um objeto chamado qubit}
\rightarrow
\text{logo a física possui qubits}.
\]

## Etapas TriadLang

1. definir representação binária/numérica do estado físico encontrado;
2. reproduzir dinâmica de um qubit;
3. reproduzir fase e superposição efetiva;
4. medir fidelidade e leakage;
5. implementar operações derivadas do subespaço físico;
6. dois qubits;
7. Bell/CHSH na linguagem;
8. comparar CPU/CUDA/Metal;
9. verificar escalabilidade;
10. somente então escrever um paper/relatório específico de computação.

---

# 26. Checklist mestre

## Antes de rodar

- [ ] Q00 concluído.
- [ ] `Theta_core` congelado.
- [ ] Hash do solver gravado.
- [ ] Versão do protocolo gravada.
- [ ] Ambiente definido.
- [ ] Seeds definidas por regra prévia.
- [ ] Observáveis definidos.
- [ ] Código de análise congelado ou versionado.
- [ ] Critérios de falha técnica definidos.
- [ ] Nenhuma métrica QM usada para ajustar parâmetros.

## Durante o run

- [ ] Todos os termos Triad ativos.
- [ ] Nenhum feedback diagnóstico não previsto entrando no solver.
- [ ] Dados brutos preservados.
- [ ] Logs de erro preservados.
- [ ] Seeds preservadas.
- [ ] Tempo/runtime/backend registrados.

## Depois do run

- [ ] Não remover seeds ruins.
- [ ] Não trocar janela porque ficou mais bonita.
- [ ] Calcular métricas exatamente como pré-definido.
- [ ] Produzir incerteza numérica/estatística.
- [ ] Comparar com QM somente após gerar a saída Triad.
- [ ] Classificar `SUPPORTED/PARTIAL/NOT_SUPPORTED/INCONCLUSIVE/NUMERICAL_FAILURE`.
- [ ] Gerar hashes.
- [ ] Escrever `analysis.md`.

## Antes do paper

- [ ] Q01 converge.
- [ ] Runs confirmatórios separados dos exploratórios.
- [ ] Todos os resultados negativos incluídos.
- [ ] Auditoria de circularidade explícita.
- [ ] Claim limitado ao Tier alcançado.
- [ ] Holdout cego executado.
- [ ] Código reproduzível.
- [ ] Dados suficientes publicados.
- [ ] TriadLang não misturada aos resultados físicos antes da ponte formal.

---

# 27. Primeira ação prática depois deste blueprint

A próxima etapa é **Q00 — TRIAD_QM_CANONICAL_V1**.

Ela deve produzir um arquivo curto e imutável contendo:

```text
1. equação exata
2. solver hash
3. Theta_core exato
4. FDT convention
5. unidades
6. dimensionalidade
7. definição de equilíbrio dinâmico
8. política de seeds
9. política de resolução/dt
10. observáveis obrigatórios
11. regras sem isolar / sem falsificar / sem calibrar
12. estrutura de pastas
13. critério estatístico
14. assinatura/hash do protocolo
```

Depois disso:

\[
\boxed{Q00\rightarrow Q01\rightarrow Q02\rightarrow\cdots}
\]

sem alterar retroativamente a regra por causa do resultado.

---

# 28. Resumo final do programa

A lógica inteira pode ser reduzida a:

\[
\boxed{
\begin{aligned}
&\text{Assumir Triad como substrato}\\
&\downarrow\\
&\text{Congelar uma única dinâmica completa}\\
&\downarrow\\
&\text{Partir de estados físicos/caóticos}\\
&\downarrow\\
&\text{Deixar a dinâmica evoluir para equilíbrio dinâmico}\\
&\downarrow\\
&\text{Medir passivamente o que surgiu}\\
&\downarrow\\
&\text{Extrair estados/modos efetivos}\\
&\downarrow\\
&\text{Comparar quantitativamente com QM}\\
&\downarrow\\
&\text{Testar Born, medição, qubits, Bell, spin, troca}\\
&\downarrow\\
&\text{Verificar finitude no limite de resolução}\\
&\downarrow\\
&\text{Fazer holdout cego}\\
&\downarrow\\
&\text{Reprodução externa}\\
&\downarrow\\
&\text{Paper}\\
&\downarrow\\
&\text{Somente depois: TriadLang formal}
\end{aligned}
}
\]

A regra mais importante de todo o projeto é:

\[
\boxed{
\text{O RESULTADO NUNCA MODIFICA RETROATIVAMENTE A DINÂMICA QUE O PRODUZIU.}
}
\]

E a pergunta que permanece aberta até o último benchmark é apenas:

\[
\boxed{
\text{Quando observamos a Triad da escala correta, vemos a mecânica quântica?}
}
\]
