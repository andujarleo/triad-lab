> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q03_subespacos/analysis.md) · [Collection / Acervo](../../../README.md)

# Q03 — Análise (subespaços persistentes, POD/DMD passivos)

Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.
Theta_core intocado (Q00). Sem cherry-pick de seed ou de janela.
Backend **mlx GPU**, campo complex64, memória float32. N_num, não física.
Snapshots são sensores. POD/DMD **não** controlam o solver.
Este lote **não** é SUPPORTED para MQ.

## Pergunta

A dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?

## Setup

- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0
- L=32.0, N=64, dt=0.0025, T=8.0, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0
- FDT: spec eq. 4; memória Euler; RNG numpy → upload GPU
- seeds 0,1,2,3 nessa ordem (primeiras quatro de Q02); complex64/float32; backend mlx GPU; Strang Q02
- snapshots a cada 8 passos (Δt=0.02), 401/seed; métricas a cada 40 passos
- janela early t≤0.2 (11 snaps); janela late t≥6.4 (81 snaps); ambas pré-declaradas
- PROTOCOL SHA-256: `f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16`
- solver executado SHA-256: `8a9c1cefd4cc98dc753071a8c7c62dfc8d09240c5d328956388c48a2d8ce4115`
- Q02 passo SHA-256: `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`
- canônico Q00: `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e`
- Q02 PROTOCOL_v2: `bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c`
- início (America/Sao_Paulo): 2026-08-21 14:08:16 BRT
- fim (America/Sao_Paulo): 2026-08-21 14:10:19 BRT
- wall total: 62.62 s
- device: Device(gpu, 0)
- backend: mlx

## Tempos de parede por seed

| seed | wall_s | evo_s | finito | blow_t | peak_late | PR_late | R_rms_late | norm_late |
|---|---|---|---|---|---|---|---|---|
| 0 | 15.54 | 14.1 | True | — | 3.90224 | 19189.1 | 15.9833 | 16740.7 |
| 1 | 15.45 | 14.2 | True | — | 3.83662 | 19227.2 | 15.9895 | 16812.6 |
| 2 | 15.57 | 14.28 | True | — | 3.80785 | 19185.1 | 16.0114 | 16714.6 |
| 3 | 15.71 | 14.47 | True | — | 3.92321 | 19190.9 | 15.9662 | 16780.5 |

## Métricas late vs Q02 (reprodução, não correção)

Q02 já mostrou caixa cheia em t=0.1, peak tardio ~3.89, R_rms=16. Q03 não conserta isso.

| seed | peak Q03 | peak Q02 | PR Q03 | PR Q02 | R_rms Q03 | R_rms Q02 | norm Q03 | norm Q02 |
|---|---|---|---|---|---|---|---|---|
| 0 | 3.90224 | 3.90224 | 19189.1 | 19189.1 | 15.9833 | 15.9833 | 16740.7 | 16740.7 |
| 1 | 3.83662 | 3.83662 | 19227.2 | 19227.2 | 15.9895 | 15.9895 | 16812.6 | 16812.6 |
| 2 | 3.80785 | 3.80785 | 19185.1 | 19185.1 | 16.0114 | 16.0114 | 16714.6 | 16714.6 |
| 3 | 3.92321 | 3.92321 | 19190.9 | 19190.9 | 15.9662 | 15.9662 | 16780.5 | 16780.5 |

## Variância explicada POD (σᵢ²/Σσ², i=1..8 e EV8)

| seed | janela | EV8 | ev1 | ev2 | ev3 | ev4 | ev5 | ev6 | ev7 | ev8 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | early | 0.98576 | 0.509425 | 0.292851 | 0.0875873 | 0.0439499 | 0.0196182 | 0.0138297 | 0.01004 | 0.00845843 |
| 0 | late | 0.407312 | 0.0737954 | 0.0728346 | 0.0521428 | 0.0517144 | 0.0424871 | 0.0420443 | 0.0363618 | 0.0359312 |
| 1 | early | 0.985772 | 0.509617 | 0.29274 | 0.0877195 | 0.0438728 | 0.0195981 | 0.0137895 | 0.00999535 | 0.00843935 |
| 1 | late | 0.414466 | 0.0755679 | 0.0745042 | 0.0535566 | 0.0532347 | 0.0431763 | 0.042726 | 0.0361194 | 0.0355804 |
| 2 | early | 0.985674 | 0.509164 | 0.292697 | 0.0876246 | 0.04388 | 0.0197367 | 0.013931 | 0.0101045 | 0.00853526 |
| 2 | late | 0.40932 | 0.0741235 | 0.0731522 | 0.0523322 | 0.0520017 | 0.0432588 | 0.0428037 | 0.0360922 | 0.0355556 |
| 3 | early | 0.985741 | 0.509469 | 0.292888 | 0.0874913 | 0.0437474 | 0.0197194 | 0.0138738 | 0.010055 | 0.00849707 |
| 3 | late | 0.406692 | 0.0718463 | 0.0711043 | 0.0528026 | 0.0524143 | 0.0432234 | 0.0428239 | 0.0365603 | 0.0359172 |

EV8 early (média seeds finitas) = 0.985737
EV8 late (média seeds finitas) = 0.409447

## Erro de reconstrução relativo L2

| seed | janela | Rec1 | Rec2 | Rec4 | Rec8 |
|---|---|---|---|---|---|
| 0 | early | 0.700411 | 0.444661 | 0.257268 | 0.119329 |
| 0 | late | 0.962405 | 0.923795 | 0.865766 | 0.769897 |
| 1 | early | 0.700273 | 0.44457 | 0.257005 | 0.119282 |
| 1 | late | 0.961484 | 0.921931 | 0.862077 | 0.765238 |
| 2 | early | 0.700597 | 0.445129 | 0.258135 | 0.119693 |
| 2 | late | 0.962235 | 0.923446 | 0.865118 | 0.768592 |
| 3 | early | 0.70038 | 0.444571 | 0.257689 | 0.119411 |
| 3 | late | 0.963417 | 0.925785 | 0.867105 | 0.7703 |

Rec8 early (média) = 0.119429
Rec8 late (média) = 0.768507

## Overlaps

Produto complexo normalizado. |⟨φᵢ|φⱼ⟩| já maximiza sobre fase global e^{iθ}.

Overlap pairwise médio φ₀ early = 0.00230241
Overlap pairwise médio φ₀ late = 0.0467942

Pares early: {"0-1": 0.0026427993782658426, "0-2": 0.003070346012205576, "0-3": 0.0027484814524526067, "1-2": 0.0023921226176040096, "1-3": 0.0016742537464938792, "2-3": 0.001286440046391809}
Pares late: {"0-1": 0.023990773380732064, "0-2": 0.055388145987838054, "0-3": 0.02836876929936655, "1-2": 0.05405780590805703, "1-3": 0.06740180012325993, "2-3": 0.05155783061835802}

Overlap |⟨φ₀|Ψ(0)⟩| (átomo gaussiano inicial, normalizado):

| seed | IC early | IC late |
|---|---|---|
| 0 | 0.0270029 | 7.22695e-05 |
| 1 | 0.0294921 | 9.1788e-05 |
| 2 | 0.0273225 | 3.71796e-05 |
| 3 | 0.0259065 | 6.73702e-05 |
média IC early = 0.027431
média IC late = 6.71519e-05

## Persistência |c_n| (janela late)

| seed | std/mean |c0| | std/mean |c1| | std/mean |c2| | τ_acf |c0| |
|---|---|---|---|---|
| 0 | 0.857846 | 1.00537 | 0.700114 | 0.32 |
| 1 | 0.835342 | 0.989851 | 0.669829 | 0.26 |
| 2 | 0.833414 | 0.917466 | 0.68234 | 0.26 |
| 3 | 0.871938 | 0.868241 | 0.681804 | 0.16 |

## DMD |λ| (late, r_dmd=8 fixo, seeds 0 e 1)

- seed 0: 1.00448, 1.00448, 0.998177, 0.998177, 0.993827, 0.993827, 0.98417, 0.98417
- seed 1: 1.00498, 1.00498, 0.99798, 0.99798, 0.993718, 0.993718, 0.98337, 0.98337

## Veredito

- n_finite = 4 / 4; n_blowup = 0
- early (contexto, **não** oficial): EV8=0.985737 Rec8=0.119429 Ov=0.00230241 → **INCONCLUSIVE**
- late (oficial, atrator): EV8=0.409447 Rec8=0.768507 Ov=0.0467942 → **INCONCLUSIVE**
- supported_for_qm = false (nunca SUPPORTED para MQ)

Veredito oficial = janela late (atrator). Early é só contexto e não promove o átomo visível/morrendo a estado de MQ. Late: EV8=0.409447 Rec8=0.768507 Ov=0.0467942 com regras EV8≥0.50∧Rec8≤0.30∧Ov≥0.50→PARTIAL; EV8<0.20∧Rec8>0.50→NOT_SUPPORTED; senão INCONCLUSIVE. Nunca SUPPORTED para MQ. Theta_core intocado. Sem comparação MQ.

Regras (pré-declaradas, não movidas): late EV8≥0.50 e Rec8≤0.30 e Ov≥0.50 → PARTIAL;
EV8<0.20 e Rec8>0.50 → NOT_SUPPORTED; senão INCONCLUSIVE; >1 blowup → NUMERICAL_FAILURE.
Janela early não define o veredito oficial.

## Notas

- Sem comparação MQ.
- Theta_core intocado.
- Backend mlx (fallback numpy fp32 só se mlx falhar; registrado).
- Sem Simulações run 35.
- Caixa preenchida = universo.
- Runner: evolução das 4 seeds usou o mesmo passo Strang Q02; depois das 4 seeds um token residual no pós-processamento foi removido sem re-evoluir (resume dos arrays derivados). SHA evolução `7c61d31e3f13db4fad772eac29c10d8ed7ae342ed25f1048190fd46dc41133c2`; SHA runner final `8a9c1cefd4cc98dc753071a8c7c62dfc8d09240c5d328956388c48a2d8ce4115`. PROTOCOL não foi editado.

