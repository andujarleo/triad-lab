<!-- convertido de grok_report-67.pdf -->

"Camponeural"aquiéa linhagemWilson-Cowan/Amari/Nunezatividade
como funcao continua do espaco cortical  nao NeRF (campo de radiancia).
O HORN disse a frase certa: oscilacao local e onda global sao o mesmo objeto
em duas escalas. O campo é a escala continua.
O objeto
Em vez de N neuronios, um campo u(c, t)  taxa média (ou potencial) no
ponto  do tecido, no tempo t. A interacao nao é um Wij por par: é um kernel
espacial w(α, aα') (o quanto o sitio α' puxa o sitio a). Forma canonica (Amari):
TOtu(a,t) = -u(a,t) + /
w(c,α) S(u(α',t) da' + I(c,t)
S é a sigmoide (taxa vs. input). Wilson-Cowan separa populacoes E e I:
TEOtE = -dEE + S(αEE(KEE *E)-αIE(KIE *I)+P)
TIOtI = -dII + S(αEI(KEI * E) - αII(KII * I) + Q)
O * é convolucao no espaco. O chapéu mexicano classico  excitacao perto,
inibicao longe - é um w que gera bump estavel (memoria de trabalho espacial),
onda viajante, ou padrao de Turing, conforme o ganho.
Nunez: o mesmo espirito vira equacao de onda cerebral quando o atraso axonal
entra. Coombes et al.: o campo moderno é uma "brain-wave equation" generalizada.
O que o campo faz que o RNN pontual nao mostra
Repertorio padrao (Bressloff / Coombes, reviews):
•frente e pulso viajantes
·breathers (oscilacao localizada)
espirais em 2D
·padroes de Turing (alucinacao geométrica tipo V1)
·bump persistente (WM espacial, direcao da cabeca)

A refratariedade que Wilson-Cowan ja punha no modelo de 1972 muda a fisica:
rede so excitatoria, que sem refratariedade so carrega frente, passa a carregar
onda periodica.
Reynolds et al. (ScienceDaily /framework 2026, cortex visual acordado): a onda
viajante nao é enfeite de EEG. Quatro funcoes propostas  ajustar percepcao no
instante, transformar o sensorial recente em representacao, prever o curto prazo,
replay de padrao. Analogia que eles mesmos escrevem: estatistica aprendida
que gera o proximo estado, "como um LLM gera texto." Aqui o gerador é a
onda no tecido, nao o token.
Isso casa com o LFP de corvo (beta/gama no NCL) e com o HORN (interferencia
= representacao): tres escalas, um idioma.
HORN como discretizacao do campo
Singer/Effenberger, PNAs 2025, explicito: HORN com conectividade local + estimulos
geometricos aprende kernel tipo chapéu mexicano. Esse grafo é a malha de um
campo cujo continuo associado é uma equacao de onda amortecida. Oscilacao
filmesdo suplementoestimulo diferente, direcao eforma de onda diferentes.
Portanto:
HORN
Campo neural
Espaco
n nos
 E Z continuo
Tempo
EulerdaODEde2aordem
integro-EDO /onda
Kernel
Whh (aprendido)
w(α, α') (imposto ou fitado)
Representacao
interferenciatransitoria
frente, bump,espiral
Parametro de ring
atraso axonal, T, ganho E/l
Subir n e localizar W éir do HORN ao campo. Descer o campo a uma malha
deosciladoreséoHORN.
Do continuo ao grafo real (cérebro medido)
Graph neural fields (PLos / PMC): o mesmo Wilson-Cowan, mas o dominio nao é

o plano  é o conectoma (DTI + MRI). Laplaciano do grafo no lugar do continuo.
Flutuacao no equilibrio reproduz o espectro harmonico do fMRI de repouso e
preve conectividade funcional. Apendice deles: onda amortecida no grafo humano.
Campo de baixa dimensao (Neuron 2025-26): SNN de N neuronios LNP, N -→
o, vira campo vt(z) no espaco de circuitos Z. Se o embedding z é rank-D,
o campo colapsa para umsistemade Ddimensoesa ponte rigorosaentre
"redefull"e"massa neural."Nature Neuroscience(set 2o26)destaca RNN unico
treinado em gravacao multiarea (peixe, camundongo, primata, humano) para
inferir corrente entre regioes. Campo aqui é ferramenta de medida, nao so teoria.
O que a IA fez com a ideia (sem chamar de cortex)
Tres ramos que o nome "neural field" hoje mistura  convem nao misturar:
1.Campoclassicotreinavel.Conv-RNNqueaprendeaemitirondanoestado
escondido (arXiv 2502.06034): a sequencia de ondas vira representacao visual;
campo receptivo efetivo cresce sem U-Net global; segmentacao semantica
com menos parametros. E HORN/campo aplicado a visao.
2. Neural Field Turing Machine (arXiv 2509.03370): controlador + memoria
como campo continuo + cabecas que leem/escrevem patch local. O(N) por
vizinhanca, Turing-completo sob erro limitado. Instancias: Rule 110, calor 2D,
inpainting. Campo como fita espacial diferenciavel.
3. Implicit neural representations / NeRF / SiREN / Functa. "Neural field" na
grafica: rede que parametriza fe(α), cor ou SDF. CORDS, ENF, FGN (2026)
levam isso a grafo ("o grafo é amostra de um campo de entropia"). Familia
diferente: nao ha onda de Wilson-Cowan; ha funcao continua no lugar da malha.
Quem veio do HORN quer o ramo 1-2. O ramo 3 so compartilha o nome.
Por que existe (computacao, nao poesia)
Campo / onda resolve o que o transformer resolve com atencao global, de outro jeito:
•integracao longa com peso local  a onda carrega o contexto; o kernel é curto; o
receptive field efetiva é o tempo de viagem;
·prior espacial no hardware  chapéu mexicano é WM; nao precisa aprender
"guarde um bump";
•mesmo idioma do LFP  o que vocé mede no corvo e no V1 é o campo;

•escala: continuo ou grafo de conectoma, nao N2 denso.
Custo: analise de estabilidade (Turing, Hopf no campo) no lugar de "stack mais
uma layer." ldentificabilidade: Cremers mostrou que onda plana em rate-model e
em integrate-and-fire se mapeiam, mas o kernel inferido da velocidade da onda
depende da classe microscopica. Medir velocidade ± ler anatomia sem modelo.
No fio do chat
text
interferéncia
Ncc visual
onda viajante / bump
sem lamina
Y, w, delay
kernel w(x,x')
OpenMythos/RDT: loop no tempo de camada. Campo/HORN: loop no tempo fisico da
onda. J-space: workspace que a interpretabilidade acha no LLM. Campo: workspace
que a anatomia é (atividade que se tornou global ao passar). Nao sao o Mythos. Sao
vocé localizaos pesos edeixa onooscilar,o filmeque saiéumcampo.Redes de
camnns nellrais san esse filme escritn cnmn eallacan a malha de tras nara a frente
