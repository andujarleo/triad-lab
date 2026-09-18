# Triad R5 64³ — dinâmica passiva, sem métricas no loop

## Regra do experimento

A evolução não contém detectores de caos, ordem, Bravais, corda, corpo, luz ou identidade. Nenhuma métrica observada é devolvida à equação. Não existe `numeric_guard`, clipping, rescaling, renormalização durante a trajetória, critério de parada por equilíbrio ou intervenção em tempo escolhido pela aparência do campo.

A única normalização ocorre na condição inicial, como no protocolo de referência, para preparar a Gaussiana inicial com norma unitária.

## Parâmetros

Usada a configuração R5 3D structure-forming do `triad_equation_reference.md`, com apenas a resolução espacial solicitada alterada de 128³ para 64³:

- hbar = 1
- m = 1
- Lambda = -8
- sigma = 1.5
- alpha = 0 (R5 baseline)
- Gamma = 0 (R5 unitary baseline)
- FDT bath = 0
- nu = (10, 0.5)
- lambda_mem = (1.125, 0.375)
- V_ext = 0
- L = 20
- N = 64
- dt = 0.0025
- T = 15
- init_sigma = 0.5
- init_k0 = (0,0,0)

A condição inicial é uma única Gaussiana 3D normalizada, não um campo aleatório nem uma rede pré-construída.

## Resultado bruto

Norma no início: ~1.0.

Norma no final em fp64: 1.0000000000027756.

Drift acumulado: aproximadamente 2.8e-12.

Nenhum NaN/Inf, guard ou renormalização durante os 6000 passos.

### Trajetória observada passivamente

A Gaussiana inicial primeiro se espalha fortemente:

| t | rho_max | sigma_rho | participação espacial (células) |
|---:|---:|---:|---:|
| 0.0 | 1.436697 | 7.967e-3 | 64.5 |
| 0.5 | 0.222518 | 3.275e-3 | 381 |
| 1.0 | 0.044331 | 1.307e-3 | 2,376 |
| 2.0 | 0.005451 | 4.528e-4 | 18,561 |
| 3.0 | 0.002057 | 2.323e-4 | 58,845 |
| 4.0 | 0.000912 | 1.436e-4 | 113,004 |

Depois não converge para um estado fixo. Aparecem pulsos de foco/defoco e reorganização:

- t=6.0: rho_max ~0.001740
- t=10.5: rho_max ~0.001828
- t=12.5: rho_max ~0.003742
- t=13.0: rho_max ~0.023171
- t=13.5: rho_max ~0.001082
- t=15.0: rho_max ~0.000810

O pulso em t=13 aumenta a densidade máxima por ~36x em relação a t=12 e depois é redistribuído novamente sem qualquer intervenção externa.

## Ordem espacial emergente

A inspeção apenas posterior do FFT da densidade mostra uma rede periódica axis-aligned emergindo sem `set_lattice`.

Em t=5, os seis maiores picos não-DC da densidade aparecem em:

- (+/-4.0841, 0, 0)
- (0, +/-4.0841, 0)
- (0, 0, +/-4.0841)

Isso corresponde a uma periodicidade axial de aproximadamente:

    2*pi / 4.0841 = 1.53846

A escala não fica travada. O máximo axial migra ao longo da trajetória:

| t | |k_axis| dominante | escala 2pi/k |
|---:|---:|---:|
| 2.5 | 0.31416 | 20.0 |
| 5.0 | 4.08407 | 1.53846 |
| 7.5 | 2.82743 | 2.22222 |
| 10.0 | 4.08407 | 1.53846 |
| 12.5 | 1.57080 | 4.0 |
| 13.0 | 1.57080 | 4.0 |
| 15.0 | 1.25664 | 5.0 |

Portanto a rodada apresenta ordem periódica, mas não um cristal estático: a escala dominante reorganiza-se continuamente.

## Fase

Coerência local de fase (média do cosseno das diferenças entre vizinhos; leitura posterior):

- t=0: 1.000
- t=0.5: -0.656
- t=1.0: -0.245
- t=2.0: 0.503
- t=3.0: 0.706
- t=4.5: 0.868
- t=15: 0.856

A coerência global em t=15 é somente ~0.035, enquanto a coerência local é ~0.856. Isso mostra organização local forte sem lock de fase global.

A contagem bruta de enrolamentos de fase foi salva, mas não deve ser interpretada como número físico de vórtices sem uma máscara de densidade: a fase é mal condicionada onde |Psi| é quase zero.

## Caos

Esta rodada mostra uma fase inicial de forte perda de coerência local, formação espontânea de ordem periódica e dinâmica intermitente de foco/defoco. Isso não basta, sozinho, para chamar o regime de `caos` no sentido matemático.

Foi iniciado um teste twin com perturbação de fase 1e-12. Nos primeiros tempos calculados em fp64, a separação permanece da ordem de 1e-12; portanto ainda não há evidência de expoente de Lyapunov positivo nessa janela curta. O teste longo precisa ser concluído antes de rotular o regime como caótico matematicamente.

## Resultado epistemológico principal

Esta rodada responde ao problema metodológico das versões anteriores:

- a rede não foi desenhada;
- o caos não foi solicitado;
- o equilíbrio não foi solicitado;
- nenhuma métrica alterou Lambda, memória ou qualquer outro termo;
- não existiu guard forçando a norma para um intervalo;
- a execução terminou porque T=15 foi definido antes, não porque algum detector declarou equilíbrio.

O dado mais claro é que uma entrada simples e localizada evolui para uma estrutura periódica 3D, perde e recupera coerência local, reorganiza sua escala espacial ao longo do tempo e produz pulsos espontâneos de foco/defoco mantendo a norma numericamente estável.

Isso é compatível com a ideia de cristalização dinâmica/contínua dentro desta configuração R5. Não estabelece ainda, por si só, que a fase intermediária seja caos matemático, nem demonstra ontologia física fora da simulação.

## Próximos controles necessários

1. concluir o twin-test para medir sensibilidade a condições iniciais em todo T=15;
2. repetir em 128³, que é a resolução da referência;
3. comparar a escala dominante com a definição exata usada para o k*L~16.3 da referência — a nossa leitura radial/axial de densidade em 64³ não reproduz diretamente esse número;
4. repetir com outros estados iniciais definidos antes da execução, sem selecionar somente os que formam rede;
5. depois disso, somente a posteriori, reconstruir cronologia de frequência, fase/luz, cordas e estruturas persistentes.
