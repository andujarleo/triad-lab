# Q02 — Análise (ensemble caótico de referência)

Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.
Theta_core intocado (Q00). Sem cherry-pick de seed.
Backend **mlx GPU**, campo complex64, memória float32 (PROTOCOL_v2). N_num, não física.
Este lote exploratório **não** é SUPPORTED para MQ.

## Pergunta

Qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?

## Setup

- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0
- L=32.0, N=64, dt=0.0025, T=8.0, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0
- FDT: f_FDT,e=2Γ dx³ kT/ℏ ; incremento spec eq. 4 (RNG numpy, upload GPU)
- seeds 0–31 nessa ordem; complex64/float32; backend mlx GPU; Strang standalone
- 1 gaussiana = 1 átomo; célula de trabalho Q01a (NÃO calibração)
- PROTOCOL v1 (histórico numpy/fp64): `a2024aff5e29c484ed781f6972d1699f4657997072c528333f1268b95cb648af`
- PROTOCOL v2 (este lote): `bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c`
- início (America/Sao_Paulo): 2026-08-21 13:52:10 BRT
- fim (America/Sao_Paulo): 2026-08-21 14:00:26 BRT
- wall total: 495.388 s (8.256 min)
- device: Device(gpu, 0)

## Tempos de parede por seed

| seed | wall_s | finito | blow_t | box_filled | t_settle | t_fill |
|---|---|---|---|---|---|---|
| 0 | 27.972 | True | — | True | 0.1 | 0.1 |
| 1 | 27.262 | True | — | True | 0.1 | 0.1 |
| 2 | 24.310 | True | — | True | 0.1 | 0.1 |
| 3 | 19.401 | True | — | True | 0.1 | 0.1 |
| 4 | 14.143 | True | — | True | 0.1 | 0.1 |
| 5 | 14.095 | True | — | True | 0.1 | 0.1 |
| 6 | 14.135 | True | — | True | 0.1 | 0.1 |
| 7 | 14.211 | True | — | True | 0.1 | 0.1 |
| 8 | 14.330 | True | — | True | 0.1 | 0.1 |
| 9 | 14.126 | True | — | True | 0.1 | 0.1 |
| 10 | 14.152 | True | — | True | 0.1 | 0.1 |
| 11 | 14.144 | True | — | True | 0.1 | 0.1 |
| 12 | 14.350 | True | — | True | 0.1 | 0.1 |
| 13 | 14.061 | True | — | True | 0.1 | 0.1 |
| 14 | 14.181 | True | — | True | 0.1 | 0.1 |
| 15 | 14.091 | True | — | True | 0.1 | 0.1 |
| 16 | 14.074 | True | — | True | 0.1 | 0.1 |
| 17 | 14.295 | True | — | True | 0.1 | 0.1 |
| 18 | 14.224 | True | — | True | 0.1 | 0.1 |
| 19 | 14.061 | True | — | True | 0.1 | 0.1 |
| 20 | 14.325 | True | — | True | 0.1 | 0.1 |
| 21 | 14.192 | True | — | True | 0.1 | 0.1 |
| 22 | 14.152 | True | — | True | 0.1 | 0.1 |
| 23 | 14.129 | True | — | True | 0.1 | 0.1 |
| 24 | 14.186 | True | — | True | 0.1 | 0.1 |
| 25 | 14.182 | True | — | True | 0.1 | 0.1 |
| 26 | 14.157 | True | — | True | 0.1 | 0.1 |
| 27 | 14.182 | True | — | True | 0.1 | 0.1 |
| 28 | 14.064 | True | — | True | 0.1 | 0.1 |
| 29 | 14.070 | True | — | True | 0.1 | 0.1 |
| 30 | 14.048 | True | — | True | 0.1 | 0.1 |
| 31 | 14.040 | True | — | True | 0.1 | 0.1 |

## Janela tardia entre seeds (t ≥ 0.8 T = 6.4)

Estatística **das médias tardias por seed** (variabilidade natural):

| observável | média ensemble | std | min | max | mediana | n |
|---|---|---|---|---|---|---|
| norm | 16769.7 | 34.094 | 16714.6 | 16846.2 | 16772.1 | 32 |
| peak | 3.8855 | 0.054768 | 3.74995 | 3.97448 | 3.89941 | 32 |
| PR | 19210.3 | 21.3097 | 19176.1 | 19255.2 | 19205.1 | 32 |
| R_rms | 16.0012 | 0.0205258 | 15.9593 | 16.0395 | 15.9992 | 32 |
| k_star | 10.8054 | 0.0808232 | 10.6895 | 10.8974 | 10.7877 | 32 |
| k_star_L | 345.772 | 2.58634 | 342.064 | 348.717 | 345.206 | 32 |
| Vmem_peak | 6.72423 | 0.11714 | 6.45914 | 7.03517 | 6.73414 | 32 |
| crystallinity | 0.999992 | 1.3134e-06 | 0.999989 | 0.999995 | 0.999992 | 32 |

## Transiente empírico (medição, não lei nova)

Primeiro t tal que |R_rms(t) − R_rms_late| < 0.05·|R_rms_late| e permanece até T.
- t_settle: mediana=0.1, min=0.1, max=0.1, n=32, n_never=0
Primeiro t com R_rms > 0.9·(L/2) = 14.4.
- t_fill: mediana=0.1, min=0.1, max=0.1, n=32, n_never=0

Janela Q00 (provisória, já congelada): transiente t < 0.8 T; equilíbrio último 20% (t ≥ 6.4). Q02 mede se isso é empiricamente ok; **não** redesenha a lei.

## Fração caixa preenchida (universo)

- critério: |R_rms_late − L/2| ≤ 1, com L/2 = 16
- n_filled / n_finite = 32 / 32 = 1
- n_filled / 32 = 32 / 32 = 1
Volume preenchido = universo, **não** ruído, **não** “átomos morreram no banho”.

## Anti-colapso (singularidade finita)

- peak_max_global = 5.65613 em t=0.7, seed=14

## k* vs Nyquist

- k_Nyq = π√3 / dx, dx=0.5 → 10.8828
- k*_late média ensemble = 10.8054
- |k* − k_Nyq| / k_Nyq = 0.00711541
- k*_on_nyquist = True
k* médio tardio está a 0.71% do Nyquist (10.8054 vs 10.8828). Espectro ainda pode estar preso à grade. Medição, não calibração.
Não se recalibra k*. Não se compara com MQ.

## Seeds excluídas (apenas NaN/blowup)

Nenhuma. 32/32 tentadas; nenhuma dropada por estética.
- n_finite = 32
- n_blowup = 0

## Veredito

**INCONCLUSIVE**

Ensemble OK: 32/32 finitas e peak/PR/R_rms tardios têm distribuição bem definida (std finito). Q02 não é teste de MQ → INCONCLUSIVE. Backend mlx GPU fp32 (PROTOCOL_v2). Nunca SUPPORTED para MQ.

Sem comparação com MQ. Pilotos 1–34 não confirmatórios. Theta_core intocado.
Backend mlx GPU fp32, PROTOCOL_v2. Este experimento **não** pode devolver SUPPORTED para MQ.
Exclusão técnica = apenas NaN/blowup. Nenhuma seed foi descartada por ser feia.

## Arquivos

- pasta: `/tmp/Q02_ensemble/out`
- PROTOCOL.md (v1 histórico), PROTOCOL_v2.md, config.json, seeds.txt, code/run_q02.py
- raw/seedXX_metrics.csv, metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt

