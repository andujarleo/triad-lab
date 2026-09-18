> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q01b_dt_N/analysis.md) · [Collection / Acervo](../../../README.md)

# Q01b — Análise (refino N e dt da tríade completa)

Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
Pilotos 27–29 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.
Theta_core intocado (Q00). PROTOCOL.md de Q01a **não** foi editado.
Q01a permanece INCONCLUSIVE (ε_num≈0.194; k* no Nyquist).

## Pergunta

Os observáveis convergem (ε_num cai) ao ir a N=96 com dt0 e ao refinar dt em N=64?

## Setup

- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0
- L=32.0, T=8.0, seed=0, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0
- FDT: f_FDT_e=2Γ dx³ kT/ℏ ; incremento spec eq. 4
- células: N=96 dt=0.0025; N=64 dt=0.00125; N=64 dt=0.000625
- overlay: Q01a N=64 dt0 (ε_num Q01a = 0.194444)
- fp64; backend numpy; Strang standalone (cópia de run_q01a.py)
- início (America/Sao_Paulo): 2026-08-21 12:10:16 BRT
- fim (America/Sao_Paulo): 2026-08-21 12:18:14 BRT

## Tempos de parede

| célula | N | dt | dx | n_steps | wall_s | wall_min | finito | veredito_célula |
|---|---|---|---|---|---|---|---|---|
| Q01a_N64_dt0 (ref) | 64 | 0.0025 | 0.5 | 3200 | 48.300 | 0.805 | True | INCONCLUSIVE |
| N96_dt0 | 96 | 0.0025 | 0.333333 | 3200 | 181.291 | 3.022 | True | finite |
| N64_dt0h | 64 | 0.00125 | 0.500000 | 6400 | 100.563 | 1.676 | True | finite |
| N64_dt0q | 64 | 0.000625 | 0.500000 | 12800 | 195.825 | 3.264 | True | finite |

Total Q01b ~ 477.7 s (7.96 min). Nenhuma célula dropada.

## Janela tardia (t ≥ 0.8 T = 6.4) — média ± std

| célula | N | dt | norm | peak | PR | R_rms | k* | k*L | Vmem_peak | células½ | largura_fís | 1–2 células |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q01a_N64_dt0 | 64 | 0.0025 | 16764.8 ± 780 | 3.9048 ± 0.281 | 19192.7 ± 195 | 15.9831 ± 0.023 | 10.701 ± 0 | 342.434 ± 0 | 6.62239 ± 0.35 | 2314.06 ± 1.04e+03 | 3.98788 ± 0.701 | não |
| N96_dt0 | 96 | 0.0025 | 16815.7 ± 779 | 4.91566 ± 0.28 | 17873.2 ± 77.7 | 15.9992 ± 0.00237 | 15.7599 ± 0.29 | 504.318 ± 9.28 | 6.78886 ± 0.369 | 3341.41 ± 843 | 3.06722 ± 0.276 | não |
| N64_dt0h | 64 | 0.00125 | 16771.2 ± 782 | 3.83856 ± 0.356 | 19194.7 ± 217 | 15.9792 ± 0.0317 | 10.8165 ± 0.0966 | 346.13 ± 3.09 | 6.67942 ± 0.41 | 2564.47 ± 1.06e+03 | 4.14297 ± 0.684 | não |
| N64_dt0q | 64 | 0.000625 | 16829.2 ± 789 | 3.85952 ± 0.219 | 19201.5 ± 182 | 16.027 ± 0.00724 | 10.8396 ± 0.0895 | 346.869 ± 2.86 | 6.81697 ± 0.451 | 2378.35 ± 718 | 4.0884 ± 0.475 | não |

Norma crescente e R_rms ≈ L/2 significam volume preenchido = universo, não ruído a filtrar.

## ε_num espacial (Q01a N=64 dt0 vs N=96 dt0)

- peak: 0.2056 (20.6%)
- PR: 0.0688 (6.9%)
- R_rms: 0.0010 (0.1%)

ε_num espacial = **0.2056424461832931**
definição: máximo |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms entre Q01a N=64 dt0 e Q01b N=96 dt0

## ε_num temporal (Q01a N=64 dt0 vs N=64 dt0/4)

- peak: 0.0116 (1.2%)
- PR: 0.0005 (0.0%)
- R_rms: 0.0027 (0.3%)

ε_num temporal = **0.011596042823147988**
definição: máximo |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms entre Q01a N=64 dt0 e Q01b N=64 dt0/4

Pares sucessivos de dt (contexto):

dt0 vs dt0/2:
- peak: 0.0170 (1.7%)
- PR: 0.0001 (0.0%)
- R_rms: 0.0002 (0.0%)

dt0/2 vs dt0/4:
- peak: 0.0054 (0.5%)
- PR: 0.0004 (0.0%)
- R_rms: 0.0030 (0.3%)

ε_num Q01a (N=48 vs N=64, dt0) = 0.19444360312773695
melhorou vs Q01a nos dois eixos? False

## k* vs Nyquist

N=96: dx=0.333333, k_Nyq = π√3/dx = 16.324194
k* tardio N=96 = 15.75993814640909 ± 0.28990202127702486
k_max da malha = 16.32419427810793
k* no Nyquist (rel < 5%)? **SIM** (rel=0.03456563442494406)

Q01a (contexto): k* já estava no Nyquist de cada grade
- N=32: k*=5.399612373357457  vs  k_Nyq=5.441398
- N=48: k*=8.148505945248527  vs  k_Nyq=8.162097
- N=64: k*=10.701049976290232  vs  k_Nyq=10.882796

k* e k*L **não** são usados para calibrar Theta. Sem comparação MQ.

## L2 de ρ tardio

Método: RegularGridInterpolator trilinear periódico; N=96→64 contra Q01a N64; N=64 nativo
- N96_dt0_vs_Q01a_N64: L2=103.946  L2_rel=0.806965  (ref Q01a_N64_dt0)
- N64_dt0h_vs_Q01a_N64: L2=115.668  L2_rel=0.897973  (ref Q01a_N64_dt0)
- N64_dt0q_vs_Q01a_N64: L2=115.473  L2_rel=0.896452  (ref Q01a_N64_dt0)
- N64_dt0h_vs_N64_dt0q: L2=115.65  L2_rel=0.895283  (ref N64_dt0q)

L2 alto entre grades/dt diferentes é esperado: seed=0 em malhas ou passos distintos não gera o mesmo campo de ruído. Critério de ε_num usa os escalares da janela tardia.

## Estruturas de 1–2 células

O pico não está preso a 1–2 células em nenhum estado final deste lote.

## Veredito

**INCONCLUSIVE**

Sem falha catastrófica, mas o refino não fechou ε_num abaixo de Q01a nos dois eixos (N e dt), e/ou k* permanece no Nyquist. Nunca SUPPORTED para MQ.

Este experimento **não** compara com mecânica quântica e **não** pode devolver SUPPORTED para MQ.
Exclusão técnica = apenas NaN/blowup. Nenhum run foi descartado por ser feio.
Nenhum termo isolado. Theta_core não mudou. Q00 congelado. Q01a PROTOCOL.md intocado.

## Arquivos

- pasta: `/Users/leo/Documents/Triad/T/QM/Q01b_dt_N`
- PROTOCOL.md, config.json, seeds.txt, Q01b.md, code/run_q01b.py
- raw/{N96_dt0,N64_dt0h,N64_dt0q}_metrics.csv, *_summary.json, *_rho_late.npy
- metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt

