> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Fontes/TRIAD_reexecucao_integral_2026-08-21.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, dossiê, reexecução]
aliases: [reexecucao_integral, triad_reexecucao_36, dossiê 2026-08-21]
classe: reexecução dossiê Grok, Linux/NumPy fp64
diretório: triad_reexecucao_36
status: completo
run: 36
data: 2026-08-21
```


# TRIAD — Reexecução integral (21 ago 2026)


Figuras da campanha (Linux/NumPy fp64):

![Artefatos/triad_reexecucao_36/A3/figures/peak_vs_t.png](../../source/Artefatos/triad_reexecucao_36/A3/figures/peak_vs_t.png)

![Artefatos/triad_reexecucao_36/A3_N128/figures/peak_vs_t.png](../../source/Artefatos/triad_reexecucao_36/A3_N128/figures/peak_vs_t.png)

![Artefatos/triad_reexecucao_36/A3_N160/figures/peak_vs_t.png](../../source/Artefatos/triad_reexecucao_36/A3_N160/figures/peak_vs_t.png)

![Artefatos/triad_reexecucao_36/QM1D/figures/p1_interference.png](../../source/Artefatos/triad_reexecucao_36/QM1D/figures/p1_interference.png)

![Artefatos/triad_reexecucao_36/CHSH/figures/chsh_bars.png](../../source/Artefatos/triad_reexecucao_36/CHSH/figures/chsh_bars.png)

![Artefatos/triad_reexecucao_36/CHSH/figures/E_vs_delta.png](../../source/Artefatos/triad_reexecucao_36/CHSH/figures/E_vs_delta.png)

![Artefatos/triad_reexecucao_36/sidebands/figures/spectra.png](../../source/Artefatos/triad_reexecucao_36/sidebands/figures/spectra.png)

![Artefatos/triad_reexecucao_36/tunnel_hist/figures/two_pass.png](../../source/Artefatos/triad_reexecucao_36/tunnel_hist/figures/two_pass.png)

![Artefatos/triad_reexecucao_36/hotbath/figures/peak_vs_t.png](../../source/Artefatos/triad_reexecucao_36/hotbath/figures/peak_vs_t.png)

![Artefatos/triad_reexecucao_36/kstar/figures/kL_vs_L.png](../../source/Artefatos/triad_reexecucao_36/kstar/figures/kL_vs_L.png)

![Artefatos/triad_reexecucao_36/bravais/figures/scores.png](../../source/Artefatos/triad_reexecucao_36/bravais/figures/scores.png)


Compilação autónoma a partir dos `result.json` gravados nesta box em 21 ago 2026.
Números são os floats literais do JSON (formato `.16g` após `json.load`).
Falhas e parciais foram **mantidas**. λ **não** foi retocado. Previsões escritas **antes** das integrações.
Isto **não** é uma mudança da leitura operacional full-triad de Leonardo.

## 0 ambiente + PDE

### Ambiente da box

| item | valor |
| --- | --- |
| data local | sexta-feira 21 ago 2026, America/Sao_Paulo (UTC-3) |
| SO / runtime | Linux box partilhada; `/usr/bin/python3` + NumPy 2.2.4; fp64 (`complex128` / `float64`) |
| mlx / triad-lang | não usados |
| numpy A.3 / QM1D / CHSH / hotbath / kstar / bravais | 2.2.4 |
| stepper 3D (A.3, hotbath, kstar, bravais) | 7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713 |
| stepper 1D (QM1D, sidebands, tunnel) | 5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076 |
| A.3 N=64 | N=64, L=20, dt=0.0025, T=6, n_steps=2400, wall_s=180.0158611449988 |
| A.3 N=128 | N=128, dx=0.15625, wall_s=1910.743829617, skipped=['Lambda_ef'] |
| A.3 N=160 | N=160, dx=0.125, wall_s=4001.041219289, skipped=['Lambda_ef'] |
| QM1D | ħ=m=1, fp64=True, t_meas_P1P2=4 |
| CHSH | N=256, L=40, dt=0.002, n_chsh=1400, wall_s=406.3778816360027 |
| sidebands | N=1024, dt=0.01, ic=hermite_(phi0+phi1)/sqrt(2), noise_frac=0.05 |
| tunnel_hist | L=120, N=4096, dt=0.002, V0=4, E=2 |
| hotbath | N=64, L=20, dt=0.0025, T=6, seed=42, wall_s=464.3421608870012 |
| kstar | T=8, dt=0.0025, n_unique_runs=8, wall_s=175.1730860669995 |
| bravais | N=64, L=20, T=8, window=0.15, field_wall_s=100.2937581940023 |

### PDE / protocolo de integração

Equação efetiva 3D (A.3 / hotbath / kstar / campo bravais), stepper Strang autónomo:

- cinética Fourier, potencial multiplicativo real, passo de memória Euler em y;
- cúbico focado Λ|Ψ|² (Λ típico −10 em A.3; −8 no ponto R5 de kstar/bravais);
- memória atrasada V_mem = λ₀ y₀ + λ₁ y₁, λ=(3,1) em A.3 / CHSH / hotbath, λ=(1.125, 0.375) no R5;
- ν=(10, 0.5) ⇒ τ_fast=0.1; Γ=0 e f_FDT=0 salvo hotbath / P2;
- ħ = m = 1, fp64, sem retune.

1D (QM1D P1–P6, sidebands, tunnel_hist, CHSH par): mesmo núcleo Strang 1D.

Diagnóstico de colapso A.3: primeiro t com peak ≥ 8 × peak_ini.
- N=64 limiar = 11.49357581527675
- N=128 limiar = 11.49357581601066
- N=160 limiar = 11.49357581601066
- hotbath limiar = 11.49357581527675

IC gaussiana 3D s=0.5: peak analítico 1/(π s²)^{3/2}.
- A.3 N=64 peak_ini = 1.436696976909594 vs analítico 1.436696977001332
- A.3 N=128 peak_ini = 1.436696977001333 vs analítico 1.436696977001332
- A.3 N=160 peak_ini = 1.436696977001332 vs analítico 1.436696977001332

FDT (hotbath): `f_FDT = 2 Γ dx³ kT / ħ`, `noise_amp = sqrt(f_FDT·dt/dx³)`, ξ=(N+iN)/√2.
Lock gravado: `f_FDT=2*Gamma*dx^3*kT/hbar ; noise_amp=sqrt(f_FDT*dt/dx^3) ; xi=(N+iN)/sqrt(2)`

CHSH: acoplamento de par κ, fase comum e^{iφ} nos dois pacotes, medição sign Re(e^{-iθ} ⟨env|ψ⟩), sem pós-seleção.

## 1 placar

Vereditos de uma linha extraídos de cada `analysis.md` + campo `verdict(s)` do JSON.

| bloco | veredito JSON | uma linha do analysis.md |
| --- | --- | --- |
| A.3 N=64 | IC MATCH; end-state mem MATCH; 8× mem FAIL; no_mem MATCH; Λ_ef MATCH; norma MATCH | ## Protocol / ## Verdicts vs predictions and vs dossier / ### IC — MATCH / **Vs prediction (end-state by T=6): MATCH.** mem peak_end = 3.43e-3 (order 1e-3), PR_end = 2657 (thousands); packet fills the box (R_rms 0.61 → 9.61). no_mem peak_end = 8.10 > 5, PR_end = 0.499 < 1. |
| A.3 N=128 | H_plateau MATCH; H_ramp FAIL; pulso 8× PARTIAL; no_mem MATCH | ## Protocol / ## Verdicts vs predictions (MATCH / PARTIAL / FAIL) / ### IC — MATCH / ### 1. no_mem blow-up grows or stays collapsed — MATCH |
| A.3 N=160 | IC=MATCH; no_mem_sharper_than_128=PARTIAL; mem_H_plateau_vs_H_ramp=MATCH_H_plateau; H_ramp=FAIL; pulse_train_vs_128=MATCH; hypothesis_that_lives=H_plateau; norm=MATCH | ## Protocol / ## Verdicts vs predictions / ### IC — MATCH / ### 1. no_mem sharper than N=128 — PARTIAL |
| QM1D P1–P6 | P1=PARTIAL; P2=MATCH; P3=MATCH; P4=PARTIAL; P5=MATCH; P6=MATCH | **Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_QM1D.md`). No retuning. Failures kept. / ## P1 Interference — PARTIAL / - Prediction “vis ≳ 0.9 in all deterministic regimes”: **held for linear and memory; failed for anti-collapse and cubic**. Kept. / - Memory changes the envelope, does not erase the fringe: mass 0.825 → 0.649 (dossier 0.700 → 0.557). Pattern match. |
| CHSH | MATCH — S saturates the local bound within error; E near triangular CHSH point | ## Verdict — MATCH / ## Surprises / kept failures |
| sidebands | INCONCLUSIVE | **Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_sidebands.md`, SHA `d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47`). No retuning. Failures kept. / **Runner SHA256 (run_sidebands.py, verdict/plot):** `84391c14f8d6d35adeef4fdbf0408e13ef7679f229412d725d99325f7e495661` / ## Verdict: **INCONCLUSIVE** / INCONCLUSIVE = leak, linear-control failure, H_ef (matches Lambda=+2), or extra lines not at the claimed loci. |
| tunnel_hist | protocol-dirty | **Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_tunnel_hist.md`). No retuning of λ, ν, V0. Failures kept. / A is the protocol test. T2/T1 = **1.598**, not ≈1. / Prediction said: if |T2/T1−1| is large, the protocol is dirty and B is unreadable as a barrier-scar test. That is what happened. Not retuned (no narrower s, no higher E, no different V0). / ## Verdict |
| hotbath | PARTIAL | ## Protocol / ## Verdicts vs predictions / ### (a) peak stays finite with mem+bath — **MATCH** / This is "universe" (late field fills), not failure. An early 8× crossing is the known A.3 delay autofocus; it is not a fail of (a). |
| kstar | H_grid | **Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_kstar.md`, SHA `7711f5679cb616a959e3a6cf2b855c6c6303c471c58292cc0fe0f7e822e112b1`). No retuning toward 16.3. Failures kept. / ## Verdict: **H_grid** / - H_invar if A,B,C stay near 16.3 (not a mesh identity), D ≠ πN, and a finite-k peak exists. **Fail** (mesh identity 3π; no peak). / - H_mobile if A or B or C moves k*L by ≳ one shell and D is not Nyquist. **Fail** (Δ(k*L)=0). |
| bravais | no crystal | ## Verdict / **no crystal.** / Prediction match: “R5 unitary at N=64 may or may not crystallize; if / for the verdict. |

### Placar compacto (falhas mantidas)

| item | estado |
| --- | --- |
| A.3 memória impede colapso *duradouro* | MATCH no estado final T=6 (PR milhares); FAIL no diagnóstico 8× (pulso precoce) |
| A.3 no_mem colapsa | MATCH; blow-up mais agudo em N=128; N=160 PARTIAL vs N=128 (peak_end 48.25 < 65.26) |
| A.3 não reduz a Λ_ef | MATCH (N=64); N=128/160 saltaram Λ_ef |
| resolução mem H_plateau | MATCH em N=128 e N=160; H_ramp FAIL |
| P1 interferência vis≳0.9 sob foco | PARTIAL / FAIL em anti-collapse e cubic |
| P2 decoerência padrão | MATCH (decoere mais depressa que o dossiê em f=1e-3) |
| P3 incerteza | MATCH |
| P4 escada linear | MATCH; mem T=80 L=20 vaza — PARTIAL |
| P5 túnel WKB | MATCH |
| P6 Ehrenfest | MATCH (err 1.52e-4 ≪ 1e-3) |
| CHSH S≈2 triangular | MATCH |
| sidebands memória | INCONCLUSIVE (leak_max=0.308 em L=80 no espectro oficial T=251) |
| túnel histérico T2/T1 | protocol-dirty (A já dá 1.598 ≠ 1) |
| hotbath átomo persiste | PARTIAL: pico finito MATCH; resgate tardio = banho; átomo FAIL |
| k*L ≈ 16.3 | FAIL / H_grid: k*L = 3π = 9.42477796076938 em 8/8 runs |
| bravais cristal | no crystal |

Surpresas QM1D (campo `surprises`):
- P1 focusing vis at k=4 is 0.51/0.61, not ~1.0
- P4 Lambda=-2+mem leak 0.642 on L=20
- P2 decoheres faster than dossier at f=1e-3
- P6 err 1.52e-4 vs dossier 1.6e-6 (dt=0.01)

## 2 A.3 N=64 / 128 / 160 (tabelas completas do JSON)

### 2.0 IC comum

| N | peak_ini | peak_ini_analytic | norm_ini | PR_ini | R_rms_ini |
| --- | --- | --- | --- | --- | --- |
| 64 | 1.436696976909594 | 1.436696977001332 | 1 | 1.968662709604115 | 0.6123724353664733 |
| 128 | 1.436696977001333 | 1.436696977001332 | 0.9999999999999998 | 1.968701243215301 | 0.6123724356957948 |
| 160 | 1.436696977001332 | 1.436696977001332 | 0.9999999999999999 | 1.968701243215303 | 0.6123724356957945 |

Veredito IC (analysis N=64): MATCH — origem na grelha; gaussiana contínua; sem bug de IC.
Veredito IC (analysis N=128): MATCH — 15 dígitos iguais ao analítico.
Veredito IC (analysis N=160): MATCH.

### 2.1 Tabela cruzada N=64 / 128 / 160 (campo `table_64_128_160` + JSON N=64/128)

| N | run | peak_end | peak_max | t_peak_max | PR_end | t_collapse |
| --- | --- | --- | --- | --- | --- | --- |
| 64 | mem | 0.003429819606286119 | 13.17367282073293 | 0.1575 | 2656.870317928816 | 0.1425 |
| 64 | no_mem | 8.097538565889609 | 12.67960946296274 | 0.1425 | 0.4988270774697631 | 0.135 |
| 128 | mem | 0.002359459135499595 | 62.48042536203411 | 0.41 | 2444.317743174161 | 0.1275 |
| 128 | no_mem | 65.25968024419336 | 84.57483375811472 | 0.6325 | 0.06155005500212721 | 0.115 |
| 160 | mem | 0.006496378593103867 | 99.7370283653819 | 0.335 | 2345.305542578222 | 0.1275 |
| 160 | no_mem | 48.24539284361922 | 95.41563596626487 | 0.21 | 0.2196431326988974 | 0.115 |

### 2.2 N=64 — todos os campos de run

| campo | mem | no_mem | Lambda_ef |
| --- | --- | --- | --- |
| peak_end | 0.003429819606286119 | 8.097538565889609 | 12.09726775792092 |
| peak_max | 13.17367282073293 | 12.67960946296274 | 16.6750479984777 |
| t_peak_max | 0.1575 | 0.1425 | 0.3125 |
| PR_end | 2656.870317928816 | 0.4988270774697631 | 0.2234719088243859 |
| norm_end | 1.000000000001119 | 1.000000000000789 | 1.000000000000685 |
| t_collapse | 0.1425 | 0.135 | 0.275 |
| wall_s | 59.61499624200042 | 60.59928320499967 | 59.74389844100006 |
| Lambda | -10 | -10 | -6 |
| lam | [3, 1] | [0, 0] | [0, 0] |
| n_samples_above_8x | 12 | — | — |
| t_last_above_8x | 0.17 | — | — |

- wall_seconds total N=64 = 180.0158611449988
- stepper_sha256 = `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`
- n_steps = 2400, collapse_threshold = 11.49357581527675

Vereditos analysis N=64:
- Claim 1 estado final T=6: **MATCH** (mem peak_end ordem 1e-3, PR milhares; no_mem colapsado).
- Claim 1 diagnóstico 8×: **FAIL** (t_collapse mem = 0.1425; previsão t_collapse=inf é falsa). λ não retocado.
- vs tabela do dossiê: **PARTIAL** (direcção ok; 0.00343 / 2657 ≠ 0.00063 / 5005; o par do dossiê está perto de t≈4.5).
- Claim 2 no_mem: **MATCH** (t_collapse=0.135; peak_end=8.0975 vs 8.10; PR_end=0.4988 vs 0.499).
- Claim 3 Λ_ef: **MATCH** (também colapsa; peak_end=12.097 vs 12.1; PR_end=0.2235 vs 0.224).
- Norma: **MATCH** (|norm−1| ~ 10^{-12}).

### 2.3 N=128 — todos os campos de run

| campo | mem | no_mem |
| --- | --- | --- |
| peak_end | 0.002359459135499595 | 65.25968024419336 |
| peak_max | 62.48042536203411 | 84.57483375811472 |
| t_peak_max | 0.41 | 0.6325000000000001 |
| PR_end | 2444.317743174161 | 0.06155005500212721 |
| norm_end | 1.000000000001192 | 1.000000000001121 |
| t_collapse | 0.1275 | 0.115 |
| n_samples_above_8x | 89 | 2326 |
| t_last_above_8x | 0.635 | 6 |
| dt_above_8x | 0.5075000000000001 | 5.885 |
| wall_s | 952.6853576089979 | 957.7015390619999 |
| Lambda | -10 | -10 |
| lam | [3, 1] | [0, 0] |

- wall_seconds total N=128 = 1910.743829617
- runner_sha256 = `e1d5fca10a36b9b593e8c84385d36077358fe59117872175f72eb683d29af4fb`
- skipped = ['Lambda_ef']

Vereditos analysis N=128:
- no_mem blow-up cresce: **MATCH** (peak_end 8.098 → 65.26; PR 0.499 → 0.0616; fica acima de 8× até T=6).
- mem H_plateau: **MATCH** (peak_end=2.359e-3, PR_end=2444).
- H_ramp estado final: **FAIL**.
- pulso 8× resolução-estável: **PARTIAL** (existe e rebound; altura e nº de bursts não estáveis: 1 → 6).

### 2.4 N=160 — todos os campos de run + pulsos

| campo | mem | no_mem |
| --- | --- | --- |
| peak_end | 0.006496378593103867 | 48.24539284361922 |
| peak_max | 99.7370283653819 | 95.41563596626487 |
| t_peak_max | 0.335 | 0.21 |
| PR_end | 2345.305542578222 | 0.2196431326988974 |
| norm_end | 1.000000000001604 | 1.000000000001663 |
| t_collapse | 0.1275 | 0.115 |
| n_samples_above_8x | 108 | 2344 |
| t_last_above_8x | 0.4225 | 6 |
| dt_above_8x | 0.295 | 5.885 |
| n_pulses_above_8x | 9 | 185 |
| n_intervals_above_8x | 4 | 3 |
| wall_s | 2001.199591598001 | 1999.271240703998 |
| Lambda | -10 | -10 |
| lam | [3, 1] | [0, 0] |

- wall_seconds total N=160 = 4001.041219289
- runner_sha256 = `ffa6a5f94288cb9b6b0507f5fc799f11a0fa545aa4218cf85056a7fe8dff89ae`
- dx = 0.125

Vereditos JSON N=160:
- `IC` = **MATCH**
- `no_mem_sharper_than_128` = **PARTIAL**
- `mem_H_plateau_vs_H_ramp` = **MATCH_H_plateau**
- `H_ramp` = **FAIL**
- `pulse_train_vs_128` = **MATCH**
- `hypothesis_that_lives` = **H_plateau**
- `norm` = **MATCH**

#### Pulsos mem N=160 (acima de 8×)

| i | t | peak | PR |
| --- | --- | --- | --- |
| 1 | 0.1475 | 80.5269051647207 | 0.07530684596315937 |
| 2 | 0.195 | 90.55856913465503 | 0.05867646125896675 |
| 3 | 0.2275 | 98.15793137101824 | 0.04870447295987364 |
| 4 | 0.2375 | 16.63034930885511 | 0.1674644722085605 |
| 5 | 0.2525 | 99.36079290524297 | 0.046297268563687 |
| 6 | 0.275 | 98.7600214098688 | 0.04692299791367354 |
| 7 | 0.3 | 99.49717209388565 | 0.04772519153908926 |
| 8 | 0.335 | 99.7370283653819 | 0.04912138053143154 |
| 9 | 0.385 | 95.04950199285469 | 0.05477306757182675 |

#### Intervalos mem N=160 acima de 8×

| t_start | t_end | peak_max | t_peak_max |
| --- | --- | --- | --- |
| 0.1275 | 0.1575 | 80.5269051647207 | 0.1475 |
| 0.18 | 0.2075 | 90.55856913465503 | 0.195 |
| 0.215 | 0.31 | 99.49717209388565 | 0.3 |
| 0.315 | 0.4225 | 99.7370283653819 | 0.335 |

no_mem N=160 tem n_pulses_above_8x = 185 (lista longa no JSON; primeiros 8 abaixo).

| i | t | peak | PR |
| --- | --- | --- | --- |
| 1 | 0.1325 | 78.68152233641999 | 0.07872170223244151 |
| 2 | 0.1675 | 87.95083448600776 | 0.06125374280840926 |
| 3 | 0.1925 | 91.58110944360115 | 0.05330770236891551 |
| 4 | 0.2 | 20.08724981969817 | 0.1306152768684194 |
| 5 | 0.21 | 95.41563596626487 | 0.04741629735341904 |
| 6 | 0.2275 | 94.05919113976914 | 0.04484461390906352 |
| 7 | 0.24 | 91.15380707880095 | 0.04740985366051997 |
| 8 | 0.255 | 76.35248814817422 | 0.07274201886796285 |

#### Intervalos no_mem N=160 acima de 8×

| t_start | t_end | peak_max | t_peak_max |
| --- | --- | --- | --- |
| 0.115 | 0.1425 | 78.68152233641999 | 0.1325 |
| 0.155 | 0.2625 | 95.41563596626487 | 0.21 |
| 0.2825 | 6 | 63.02216600224263 | 0.32 |

## 3 P1–P6 from QM1D/result.json (vis, T, picos, Ehrenfest)

Dossiê: TRIAD — Dossiê unificado dos testes e simulações (2026-08-21)
Âmbito: P1-P6 1D, NOT CHSH
Stepper: `/workspace/dossie_reexec/QM1D/code/stepper1d.py` SHA `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`
Métrica P1/P2: C=2|int rho exp(-i*4*x) dx|/int rho dx  (not max/min)
t_meas_P1P2 = 4

### 3.1 P1 interferência — veredito **PARTIAL**

| regime | vis | vis_sideband | central_mass | norm |
| --- | --- | --- | --- | --- |
| linear | 0.9999999999999989 | 0.9335641846260595 | 0.8254343552674178 | 1.000000000000437 |
| memory_only | 0.9670628135211168 | 0.5557352015635948 | 0.6489201191894274 | 1.000000000000465 |
| anti_collapse | 0.5105687503599642 | -0.6787018619065966 | 0.7682984905856298 | 1.000000000000525 |
| cubic_only | 0.611040819930986 | 0.1380439024456644 | 0.9611764095426462 | 1.000000000000467 |

Referência do dossiê (não é alvo de retune):
| regime | vis_dossiê | mass_dossiê | nota |
| --- | --- | --- | --- |
| linear | 0.998 | 0.7 | rigorous 0.9419999999999999 |
| memory_only | 0.9995000000000001 | 0.5570000000000001 |  |
| anti_collapse | 0.9996 | 0.976 |  |
| cubic_only | 1 | 0.926 |  |

Uma linha analysis: previsão vis≳0.9 **segura em linear e memory; falha em anti-collapse (0.511) e cubic (0.611)**. Mantida.

### 3.2 P2 decoerência — veredito **MATCH** (padrão; números ≠ dossiê)

| f_FDT | shot_mean | shot_std | ensemble_density | shot_mean_wf_sb | ensemble_wf_sb |
| --- | --- | --- | --- | --- | --- |
| 0 | 0.9999999999999979 | 0 | 0.9999999999999979 | 0.9335641846260531 | 0.9335641846260531 |
| 0.001 | 0.1686909574854793 | 0.0365581550922131 | 0.1650910738123847 | 0.6449376012994399 | 0.6460108121319518 |
| 0.01 | 0.05286890517795318 | 0.01431516279209319 | 0.01984752200474882 | 0.1671407464332757 | 0.1764409366733181 |
| 0.03 | 0.04803122835092994 | 0.01969955148669503 | 0.008043820130043434 | 0.06501809773336042 | 0.07561853274216669 |
| 0.1 | 0.04662227619789486 | 0.02190400893591342 | 0.00458179820469069 | 0.02411749466067403 | 0.03449642010551725 |

Dossiê (comparação): f=0 → 0.942/0.942; 1e-3 → 0.50±0.12 / 0.50; 1e-2 → 0.18±0.08 / 0.046; 3e-2 → 0.19 / 0.09; 1e-1 → 0.20 / 0.12.
Uma linha: decoerimos mais depressa em f=1e-3 (0.169 vs 0.50). Não retocado.

### 3.3 P3 incerteza — veredito **MATCH**

| estado | sx | sp | product |
| --- | --- | --- | --- |
| gaussian_s1 | 0.7071067811865476 | 0.7071067811865476 | 0.5000000000000001 |
| gaussian_s04 | 0.282842712474619 | 1.767766952966369 | 0.4999999999999999 |
| p1_linear_tmeas | 2.915475947422814 | 2.121320343559688 | 6.184658438426971 |

Dossiê: [0.5, 0.5, 6.54] (ħ/2 = 0.5).

### 3.4 P4 quantização — veredito **PARTIAL**

#### P4_long linear T=251.33

- label = linear_T251, T_act = 251.33, dt = 0.01, dE = 0.02499874793976123
- leak_max = 2.282705362307901e-27, norm = 1.000000000004779

| E | mag | omega |
| --- | --- | --- |
| 0.4999749587952244 | 12234.94208185194 | -0.4999749587952244 |
| 1.499924876385673 | 8808.492499907939 | -1.499924876385673 |
| 2.499874793976122 | 3170.228739401792 | -2.499874793976122 |
| 3.499824711566571 | 760.1561136944728 | -3.499824711566571 |
| 4.49977462915702 | 136.3068326723275 | -4.49977462915702 |

Dossiê P4_long: [0.5027, 1.508, 2.4881, 3.4935, 4.4988]

#### P4_extras T=80

**linear** — T_act=80, dE=0.07853000008973361, leak_max=6.847989614143249e-28, norm=1.000000000001547

| E | mag | omega |
| --- | --- | --- |
| 0.4711800005384016 | 3103.81601765809 | -0.4711800005384016 |
| 1.492070001704939 | 2690.18189808446 | -1.492070001704939 |
| 2.512960002871476 | 953.0225306851833 | -2.512960002871476 |
| 3.533850004038013 | 208.0705179442423 | -3.533850004038013 |

**Lambda_p2** — T_act=80, dE=0.07853000008973361, leak_max=1.950444299380621e-14, norm=1.000000000001642

| E | mag | omega |
| --- | --- | --- |
| 0.2355900002692008 | 221.7746257931595 | -0.2355900002692008 |
| 1.177950001346004 | 3572.938910815645 | -1.177950001346004 |
| 2.198840002512541 | 2737.803640624022 | -2.198840002512541 |
| 2.905610003320144 | 87.35982420012535 | -2.905610003320144 |

**Lambda_m2** — T_act=80, dE=0.07853000008973361, leak_max=9.865415262727136e-17, norm=1.000000000001679

| E | mag | omega |
| --- | --- | --- |
| 0.5497100006281352 | 2515.85195180462 | -0.5497100006281352 |
| 0.8638300009870696 | 283.9423577527847 | -0.8638300009870696 |
| 1.570600001794672 | 700.2532572471022 | -1.570600001794672 |
| 1.884720002153606 | 170.3193465920629 | -1.884720002153606 |

**Lambda_m2_mem** — T_act=80, dE=0.07853000008973361, leak_max=0.64184519396393, norm=1.00000000000182

| E | mag | omega |
| --- | --- | --- |
| 0.4711800005384016 | 129.6580485616072 | -0.4711800005384016 |
| 0.7067700008076025 | 198.5485866591991 | -0.7067700008076025 |
| 1.020890001166537 | 404.9156290271955 | -1.020890001166537 |
| 2.041780002333074 | 551.7488896870602 | -2.041780002333074 |

Uma linha analysis: escada linear MATCH (mais perto de n+1/2 que o dossiê). **Λ=-2+mem FAIL**: leak_max=0.64184519396393 em L=20. Mantida.

### 3.5 P5 túnel — veredito **MATCH**

| V0 | T | sqrt | dossier_T |
| --- | --- | --- | --- |
| 2.5 | 0.3511231583581099 | 0.7071067811865476 | 0.353 |
| 3 | 0.2303025356559203 | 1 | 0.231 |
| 4 | 0.09506654435165936 | 1.414213562373095 | 0.095 |
| 5 | 0.04111950662586219 | 1.732050807568877 | 0.04 |
| 6 | 0.01991834713379752 | 2 | 0.018 |

- slope = -2.243081349369715 (dossiê -2.33)
- intercept = 0.6794248962705421
- wkb_neg2sqrt2 = -2.82842712474619

### 3.6 P6 Ehrenfest — veredito **MATCH**

- err_max = 0.000152162087353247
- T = 20
- dossiê err = 1.6e-06 (dt menor no dossiê)

Uma linha: max |⟨x⟩ − 2 cos(t)| = 0.000152162087353247 ≪ 1e-3.

## 4 CHSH S, quatro E, scan, hashes

Veredito JSON: **MATCH** — S saturates the local bound within error; E near triangular CHSH point
Uma linha analysis: **Verdict — MATCH**. S satura o bound local dentro do erro; E perto do ponto triangular CHSH.

### 4.1 Protocolo

| campo | valor |
| --- | --- |
| N | 256 |
| L | 40 |
| dt | 0.002 |
| s | 1 |
| x0A | -3 |
| x0B | 3 |
| k0 | 0 |
| Lambda | -2 |
| lam | [3, 1] |
| nu | [10, 0.5] |
| kappa | 0.5 |
| T_couple | 2 |
| T_sep | 2 |
| n_chsh | 1400 |
| n_per_pair | 350 |
| phase_convention | both packets get exp(i phi); fonte de fase comum |
| measurement | sign Re(exp(-i theta) <env|psi>); env = unphased local gaussian of that side |
| settings | balanced shot%4; seed_settings=900000+shot independent of physical 10000+shot |
| post_selection | false |
| all_shots_valid | true |
| downgrade | none (N=256, dt=0.002, T_couple=T_sep=2.0) |
| date_local | 2026-08-21 15:31 UTC-3 (America/Sao_Paulo) |

### 4.2 S

| quantidade | valor |
| --- | --- |
| S | 2.022857142857143 |
| S_se_propagation | 0.09213300058023927 |
| S_bootstrap | 2.023467142857143 |
| S_bootstrap_se | 0.09239369405828873 |
| dossier_S | 2 |
| dossier_S_err | 0.053 |
| near_triangular | true |
| no_signaling_ok | true |
| scan_closer_to_triangle | true |
| mass_err_A | 8.253382104734491e-14 |
| mass_err_B | 1.028525677325222e-13 |
| wall_seconds | 406.3778816360027 |

### 4.3 Quatro correlatores E

| par | E | se | se_1sqrtn | n | E_dossiê |
| --- | --- | --- | --- | --- | --- |
| ab | 0.5657142857142857 | 0.04407679489704874 | 0.05345224838248487 | 350 | 0.486 |
| abp | 0.4685714285714286 | 0.04722108537285105 | 0.05345224838248487 | 350 | 0.511 |
| apb | 0.4742857142857143 | 0.04705780825521155 | 0.05345224838248487 | 350 | 0.51 |
| apbp | -0.5142857142857142 | 0.04584165928440551 | 0.05345224838248487 | 350 | -0.493 |

### 4.4 Marginais

| campo | valor |
| --- | --- |
| P_A_plus_a0 | 0.5114285714285715 |
| P_A_plus_ap | 0.4914285714285714 |
| P_B_plus_b | 0.51 |
| P_B_plus_bp | 0.5328571428571428 |
| n_A_a0 | 700 |
| n_A_ap | 700 |
| n_B_b | 700 |
| n_B_bp | 700 |

### 4.5 No-signaling

| campo | valor |
| --- | --- |
| P_A_plus_a0_b | 0.52 |
| P_A_plus_a0_bp | 0.5028571428571429 |
| P_A_plus_ap_b | 0.4828571428571429 |
| P_A_plus_ap_bp | 0.5 |
| P_B_plus_a_b | 0.52 |
| P_B_plus_ap_b | 0.5 |
| P_B_plus_a_bp | 0.5171428571428571 |
| P_B_plus_ap_bp | 0.5485714285714286 |
| dA_a0 | 0.01714285714285713 |
| dA_ap | -0.01714285714285713 |
| dB_b | 0.02000000000000002 |
| dB_bp | -0.03142857142857147 |
| max_abs_delta | 0.03142857142857147 |

### 4.6 Scan E vs Δ (200 shots / ponto)

| delta | E | se | n | triangle | qm_cos |
| --- | --- | --- | --- | --- | --- |
| 0 | 1 | 0 | 200 | 1 | 1 |
| 0.3926990816987241 | 0.77 | 0.04511651582292232 | 200 | 0.75 | 0.9238795325112867 |
| 0.7853981633974483 | 0.52 | 0.060398675482166 | 200 | 0.5 | 0.7071067811865476 |
| 1.178097245096172 | 0.22 | 0.06897825744392214 | 200 | 0.25 | 0.3826834323650898 |
| 1.570796326794897 | -0.03 | 0.07067885115082163 | 200 | 0 | 6.123233995736766e-17 |
| 2.356194490192345 | -0.55 | 0.05905505905508859 | 200 | -0.5 | -0.7071067811865475 |

runner_sha256 = `5f543afa76927f7c8aee2f39501240b6cc3e1e30038e1d1a92431c0a65700f38`

## 5 sidebands peak tables + leak

Veredito JSON: **INCONCLUSIVE**
- mem leak_max=3.081e-01 >= 1e-06 at L=80.0; spectrum INVALID
- T80_mem (not the scoring spectrum) E=[0.9628, 1.5991, 2.0345, 2.9387] L=40.0 leak=6.77e-13 — confined but official score uses T=251 mem
- verdict_meta: lin_ok=True, new_in_mem=[], side_hits=[]
Uma linha analysis: **Verdict: INCONCLUSIVE** — espectro oficial Λ=-2+mem T=251 vaza em L=80 (leak_max=0.308 ≥ 1e-6); espectro inválido. Não é empate.

IC = hermite_(phi0+phi1)/sqrt(2); noise_frac = 0.05; leak_limit = 1e-06
predictions_sha256 = `d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47`
runner_sha256 = `84391c14f8d6d35adeef4fdbf0408e13ef7679f229412d725d99325f7e495661`
stepper_src_sha256 = `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076` (expected `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`)
go_one_sha256 = `b8a9b3041d74278d186bcc2c2cba6e08f9bdea89f138446576c809a925c43a78`
adopted_from_disk = True
nota: Configs were already finished by go_one.py. This script only loaded raw/ and wrote figures/result/analysis. No config was re-integrated.

### 5.1 Resumo leak / norma / dE

| run | Lambda | lam | L | T | T_act | dE | leak_max | leak_end | norm_end | mag_max | noise_floor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| linear | 0 | [] | 40 | 251 | 251 | 0.02503161351013739 | 1.882777104854143e-27 | 1.824932986627509e-28 | 1.000000000006882 | 6273.562049529743 | 313.6221522208562 |
| Lambda_p2 | 2 | [] | 40 | 80 | 80 | 0.07853000008973361 | 9.27678612704378e-28 | 1.158161727408938e-28 | 1.000000000002124 | 2433.385741046432 | 121.5356484418708 |
| Lambda_m2 | -2 | [] | 40 | 80 | 80 | 0.07853000008973361 | 2.790832673190636e-25 | 2.301172897088491e-25 | 1.000000000002226 | 1121.740026455514 | 55.48533066301074 |
| Lambda_m2_T251 | -2 | [] | 40 | 251 | 251 | 0.02503161351013739 | 1.110930808031761e-22 | 7.542071612708391e-23 | 1.000000000006918 | 3629.217227060447 | 176.949710699363 |
| Lambda_m2_mem | -2 | [3, 1] | 80 | 251 | 251 | 0.02503161351013739 | 0.3080784918807671 | 0.02223710990640824 | 1.000000000006724 | 108.17804117725 | 5.406908533623319 |
| Lambda_m2_mem_T80 | -2 | [3, 1] | 40 | 80 | 80 | 0.07853000008973361 | 6.770050970170906e-13 | 1.622554103073808e-14 | 1.000000000002099 | 195.1741717374206 | 9.750985640775786 |

### 5.2 Picos E = −ω (eixo FFT negativo)

#### linear

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.5001593183031392 | 6273.562049529743 | -0.5001593183031392 | 1.00017840020303 |
| 1.500470717022541 | 6262.050573243737 | -1.500470717022541 | 0.9983431541586278 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 1.000316833409544 | 2660.74278206092 | 1.000715298493466 |
| 2.000619134181012 | 530.6943724563645 | 0.1995961356813762 |
| 3.000891515743614 | 226.4204137639096 | 0.08515756332119488 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 2.000619104673188 | 623.5361317646523 | 1.002888672184941 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 1.203706215242022e-33 |
| n3 | 3.009265538105056e-34 |
| n4 | 7.52316384526264e-35 |
| n5 | 6.770847460736376e-34 |
| sum_P | 1 |

#### Lambda_p2

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.1573128528268163 | 137.5375488088707 | -0.1573128528268163 | 0.0565832126508353 |
| 1.174215977567813 | 2433.385741046432 | -1.174215977567813 | 1.001099583637921 |
| 2.192096124974836 | 912.3033154009424 | -2.192096124974836 | 0.3753233422032907 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 1.017805768616098 | 376.3409312646087 | 1.000807954518542 |
| 2.039729027056551 | 41.00427591788617 | 0.1090431629905274 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 1.881697164863431 | 120.316635028731 | 1.000604898808154 |
| 3.756120065203161 | 45.55193728362398 | 0.3788295075349455 |
| 5.634024950725411 | 14.0120943784074 | 0.1165306050509857 |
| 7.529103636239994 | 8.000124424615288 | 0.06653247648118878 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 1.203706215242022e-33 |
| n3 | 3.009265538105056e-34 |
| n4 | 7.52316384526264e-35 |
| n5 | 6.770847460736376e-34 |
| sum_P | 1 |

#### Lambda_m2

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.5612720737085968 | 1121.740026455514 | -0.5612720737085968 | 1.010843778933556 |
| 0.8927025970709819 | 132.0775070777345 | -0.8927025970709819 | 0.1190202036281491 |
| 1.902166167524159 | 75.27157127929175 | -1.902166167524159 | 0.06783015472724893 |
| 2.976482148420194 | 78.02127127969098 | -2.976482148420194 | 0.0703080168644501 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 0.999333701406627 | 638.4542302416019 | 1.036125846950235 |
| 1.341229035254187 | 62.40416946993993 | 0.1012736228888321 |
| 1.987726297128878 | 62.9247413531111 | 0.1021184414487233 |
| 2.342555878349327 | 31.26457034656705 | 0.05073821723698745 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 2.13426823861186 | 18.24937641136068 | 0.1401988117348898 |
| 2.33904032392122 | 133.1364646776832 | 1.022806134612663 |
| 4.494518665701914 | 97.32185777217995 | 0.747664386329256 |
| 4.699233399267646 | 7.137804222675825 | 0.05483538987077183 |
| 6.849160864882418 | 25.35806533927216 | 0.1948105265804301 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 1.203706215242022e-33 |
| n3 | 3.009265538105056e-34 |
| n4 | 7.52316384526264e-35 |
| n5 | 6.770847460736376e-34 |
| sum_P | 1 |

#### Lambda_m2_T251

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.5698557773672243 | 3629.217227060447 | -0.5698557773672243 | 1.025493970212383 |
| 0.6389143997628103 | 276.373592972113 | -0.6389143997628103 | 0.07809382447696422 |
| 0.900853152694998 | 480.1185854837942 | -0.900853152694998 | 0.1356652643245951 |
| 1.007287121784324 | 376.2955893499556 | -1.007287121784324 | 0.1063283991430991 |
| 1.900500871853691 | 245.3069968273679 | -1.900500871853691 | 0.06931545574667362 |
| 3.008158158016138 | 265.3152713837052 | -3.008158158016138 | 0.07496911702627056 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 1.000419242853415 | 2137.46192795452 | 1.000567414933625 |
| 1.07151104493962 | 165.9923879908908 | 0.07770270542766783 |
| 1.330749733908469 | 225.2157011836205 | 0.1054257336650694 |
| 1.440686832943557 | 149.8192227192392 | 0.07013188418612333 |
| 2.000826466451516 | 221.1987815363712 | 0.1035453731988175 |
| 2.330864570185682 | 119.6256928204238 | 0.05599798932536691 |
| 3.439389480893016 | 128.8277058319346 | 0.06030554411766392 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 2.097139133183302 | 21.8048232655248 | 0.05060039406847312 |
| 2.170433485320944 | 103.4676693386591 | 0.2401076485751841 |
| 2.330038914355713 | 432.4008711204173 | 1.003431864950618 |
| 4.502394484065076 | 327.6450404012474 | 0.7603349019157892 |
| 4.660490671434744 | 21.94722949424276 | 0.05093086275437745 |
| 6.828907072661263 | 59.15120752489527 | 0.1372666209644555 |
| 6.885716055355338 | 46.70150192020158 | 0.1083757649385781 |
| 8.992136979433223 | 33.58004547391457 | 0.07792604017588349 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 1.203706215242022e-33 |
| n3 | 3.009265538105056e-34 |
| n4 | 7.52316384526264e-35 |
| n5 | 6.770847460736376e-34 |
| sum_P | 1 |

#### Lambda_m2_mem

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.5012897204080413 | 108.17804117725 | -0.5012897204080413 | 1.000368699641724 |
| 0.6147868395178306 | 14.6525334137815 | -0.6147868395178306 | 0.1354982548961526 |
| 0.6786753804047747 | 14.22808077532688 | -0.6786753804047747 | 0.1315731594759589 |
| 0.7602612937577649 | 13.9929534860308 | -0.7602612937577649 | 0.1293988366828701 |
| 0.9471190666123355 | 15.75545572309848 | -0.9471190666123355 | 0.1456974500781902 |
| 1.502600339351354 | 88.11999987844494 | -1.502600339351354 | 0.814883397143333 |
| 2.031955767654566 | 22.78364507288268 | -2.031955767654566 | 0.2106901284828535 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 0.9999010075645445 | 37.65125990616413 | 0.1100050198361054 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 1.989797697549625 | 1037.384241056517 | 1.081083977142755 |
| 3.982171977325247 | 274.7736470857784 | 0.2863484670858127 |
| 5.961887098405012 | 161.2913095112831 | 0.1680856942529178 |
| 7.953402045847238 | 114.0098716991057 | 0.1188125292943306 |
| 9.937346502495375 | 67.78670987646584 | 0.07064222012476014 |
| 11.9226958985879 | 51.00555402936173 | 0.05315415930193208 |

V_mem:

| omega | mag | frac |
| --- | --- | --- |
| 1.981794101616216 | 588.8248887278322 | 0.9746579986324845 |
| 3.966062988871038 | 453.7067816125103 | 0.7510024664341823 |
| 5.948582044815791 | 377.1404468833751 | 0.6242653124885421 |
| 7.928838052008796 | 289.3535567970408 | 0.4789552275453338 |
| 9.909016813406735 | 211.8282941266495 | 0.3506307990025263 |
| 11.89125767683235 | 153.7929238573215 | 0.2545672002663938 |
| 13.87682592600106 | 114.9267888881343 | 0.1902336606201823 |
| 15.85987945015647 | 87.73283217172622 | 0.1452206050657935 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 0 |
| n3 | 2.70833898429455e-33 |
| n4 | 3.009265538105056e-34 |
| n5 | 7.52316384526264e-35 |
| sum_P | 1 |

#### Lambda_m2_mem_T80

| E | mag | omega | frac |
| --- | --- | --- | --- |
| 0.9627979385781638 | 128.9027551668615 | -0.9627979385781638 | 0.6609729514308159 |
| 1.599106037272388 | 69.23251680251136 | -1.599106037272388 | 0.3550026600029084 |
| 2.034544153009181 | 195.1741717374206 | -2.034544153009181 | 1.000792016969336 |
| 2.938723320988943 | 10.52041690705891 | -2.938723320988943 | 0.05394540251944165 |

batimento |c(t)|²:

| omega | mag | frac |
| --- | --- | --- |
| 0.05138764323689832 | 403.6787446370851 | 1.048012283033781 |
| 0.9236931776929149 | 68.13549463911194 | 0.1768902530564689 |
| 1.116420460870757 | 52.09234696547821 | 0.1352397672583906 |

ρ²:

| omega | mag | frac |
| --- | --- | --- |
| 0.08291495187110194 | 52.63386069525743 | 0.3713246485798228 |
| 2.01751360306497 | 145.6547146622725 | 1.027573980352842 |
| 3.982445954172634 | 33.6410892271548 | 0.2373332579086544 |
| 4.225929876141823 | 10.23801392349598 | 0.0722277802175363 |
| 5.954188680082881 | 11.97332589655594 | 0.08447016753363361 |

V_mem:

| omega | mag | frac |
| --- | --- | --- |
| 0.08045307298764608 | 388.6720484899318 | 0.6510416367169088 |
| 1.987520777039539 | 620.0708122652152 | 1.038644065262609 |
| 3.971584326018241 | 427.7826893737106 | 0.7165535657402335 |
| 5.95449797248908 | 315.4347871971495 | 0.5283662175660717 |
| 7.927791594305679 | 218.3521507695606 | 0.365748816180576 |
| 9.8940041273736 | 137.2700961251507 | 0.2299330461267284 |
| 10.10612998189691 | 55.4859509169067 | 0.09294124555672223 |
| 11.85659868058477 | 82.00470483832919 | 0.1373612470046603 |

| n | P |
| --- | --- |
| n0 | 0.5000000000000002 |
| n1 | 0.4999999999999999 |
| n2 | 1.203706215242022e-33 |
| n3 | 3.009265538105056e-34 |
| n4 | 7.52316384526264e-35 |
| n5 | 6.770847460736376e-34 |
| sum_P | 1 |

## 6 tunnel T1 T2 dirty

Veredito JSON: **protocol-dirty**
- A T2/T1=1.5981 off by 0.598
- B T2/T1=2.7673 (delta vs A +1.1693)
Uma linha analysis: A é o teste de protocolo. T2/T1 = **1.598**, não ≈1 → **protocol-dirty**.

| campo | valor |
| --- | --- |
| item | pending-6-tunnel-hist |
| L | 120 |
| N | 4096 |
| dt | 0.002 |
| V0 | 4 |
| a | 1 |
| E | 2 |
| s | 2 |
| k0 | 2 |
| x0 | -20 |
| Lambda | 0 |
| alpha | 0 |
| Gamma | 0 |
| f_FDT | 0 |
| reversal | psi <- conj(psi) after Psi(x<0)=0; y untouched |
| T1_def | mass(x>2)/total at t_mid |
| T2_def | mass(x<-2)/mass_sent_back at t_final |
| renormalize_evolved | false |

stepper_sha256 = `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`
runner_sha256 = `b103f6d921de1067ede758da89f17d7d93bacc95549a345ead1c96ee3cc576da`
predictions_sha256 = `5ea1d58c5be2a488c07761da8c55852ecd64728eef3334d115823128112012b4`

### 6.1 Três configs

| campo | A_linear | B_mem | C_freeze |
| --- | --- | --- | --- |
| T1 | 0.08133863831719594 | 0.1863034169517367 | 0.1863034169517367 |
| R1 | 0.9168231506866579 | 0.7534433845762277 | 0.7534433845762277 |
| T1_plus_R1 | 0.9981617890038538 | 0.9397468015279644 | 0.9397468015279644 |
| T2 | 0.1299844288432685 | 0.5155652518327329 | 0.5101966731014173 |
| R2 | 0.8700139124827534 | 0.484422323726383 | 0.4897895717423542 |
| T2_over_T1 | 1.598064972963634 | 2.767341899941074 | 2.738525580739014 |
| mass_sent_raw | 0.08134947816788528 | 0.1868251936426922 | 0.1868251936426922 |
| T2_abs | 0.01057416545635051 | 0.0963205780090937 | 0.0953175922480296 |
| t_mid | 22.3 | 16.4 | 16.4 |
| t_final | 25.35 | 14.2 | 14.2 |
| t_hit_est | 13.35104930314354 | 9.276704058290681 | 9.276704058290681 |
| mass_bar_mid | 3.710161199381395e-05 | 0.001942328635733636 | 0.001942328635733636 |
| mass_mid_mid | 0.001838210996155816 | 0.06025319847223413 | 0.06025319847223413 |
| mass_edge_mid | 9.404890648490705e-05 | 9.806292489513468e-05 | 9.806292489513468e-05 |
| mass_bar_final | 4.363065567235392e-08 | 4.550388299887732e-07 | 5.006434591068916e-07 |
| mass_mid_final | 1.349327079477002e-07 | 2.321199244405842e-06 | 2.569810395897054e-06 |
| mass_edge_final | 1.032892379658445e-06 | 2.338611981216285e-05 | 2.371509705872541e-05 |
| norm_mid | 1.000000000005226 | 1.000000000003295 | 1.000000000003295 |
| norm_final | 0.08134947816833064 | 0.1868251936433626 | 0.1868251936433621 |
| Vmem_bar_mean_mid | 0 | 0.01120329769566924 | 0.01120329769566924 |
| Vmem_bar_max_mid | 0 | 0.04841809094405702 | 0.04841809094405702 |
| Vmem_bar_mean_final | 0 | 0.004407537472100546 | 0.01120329769566924 |
| Vmem_bar_max_final | 0 | 0.006486274767616522 | 0.04841809094405702 |
| y0_bar_mean_mid | 0 | 0.001957216985302522 | 0.001957216985302522 |
| y1_bar_mean_mid | 0 | 0.005331646739761674 | 0.005331646739761674 |
| x_mean_mid | -19.75819540214507 | -6.982222588891008 | -6.982222588891008 |
| k_mean_mid | -1.632944595846114 | -0.9291025627088945 | -0.9291025627088945 |
| E_mid | 2.079446521622663 | 3.035578189690475 | 3.035578189690475 |
| x_sent | 29.99207346689134 | 28.28880562330502 | 28.28880562330502 |
| k_sent | -2.246420695924599 | -3.049445734772906 | -3.049445734772906 |
| E_sent | 2.702076786440188 | 5.382892780390167 | 5.382892780390167 |
| E_ic | 2.0625 | 2.0625 | 2.0625 |
| leak_pass1 | false | false | false |
| leak_pass2 | false | false | false |
| wrap_flag | false | false | false |
| split_dirty | false | true | true |
| flags | ok | pass1_split_incomplete | pass1_split_incomplete |
| wall_s | 12.06163334846497 | 11.28393292427063 | 11.35129356384277 |

### 6.2 Interpretação (JSON)

| campo | valor |
| --- | --- |
| control_dirt | energy filtering of transmitted packet, not wrap |
| A_E_ic | 2.0625 |
| A_E_sent | 2.702076786440188 |
| B_E_sent | 5.382892780390167 |
| Vmem_over_V0_mid_B | 0.00280082442391731 |
| scar_moves_T2 | false |
| C_minus_B_T2 | -0.005368578731315687 |
| T1_B_already_higher_at_t12 | true |
| naive_label_if_ignore_dirt | easier |
| refused_because | A T2/T1 != 1 |

Falhas mantidas: controlo A já é sujo (filtro energético do pacote transmitido, não wrap); B/C `split_dirty=true` (`pass1_split_incomplete`); recusa-se o rótulo ingénuo «easier» porque A T2/T1 ≠ 1.

## 7 hotbath 7 runs

Veredito overall JSON: **PARTIAL**
- (a) pico finito mem+banho: **MATCH** — mem+bath peak stays finite on cool/mid/hot. Early 8× pulse (if present) is the known A.3 delay pulse, not a stuck spike.
- (b) resgate tardio: **MATCH-bath** (hot=bath, mid=bath) — hot 5vs6: BOTH thermal box-fill (mem PR=4283 peak/norm=1.38e-3; no_mem PR=4013 peak/norm=2.05e-3). mid 4vs7: BOTH spread (PR=4011 vs 4002). Late rescue is the bath, not memory. Memory still suppresses extra early pulses.
- (c) átomo persiste: **FAIL** — atom does not persist (box-filling) at hot (PR=4283.1, t_fill=0.0025, n_cells=140348.5) and also not at cooler baths (cool persist=False, mid persist=False). Predicted FAIL at hot; unitary mem already fills by T=6.
- overall_note: (a) MATCH finite peak with mem+bath. (b) MATCH-bath: late rescue is the bath (5 vs 6 and 4 vs 7 both fill). (c) FAIL atom persistence at hot — predicted. Item is PARTIAL: singularity stays finite, atom does not persist in a hot bath.
- scorer_note: Auto is_spread required peak_end<1 and first-marked hot unclear. Corrected: hot peak_end>1 is FDT thermal floor, PR~4000 both sides.
Uma linha analysis: item **PARTIAL** — singularidade fica finita; o átomo **não** persiste num banho quente.

| campo | valor |
| --- | --- |
| peak_ini | 1.436696976909594 |
| peak_ini_analytic | 1.436696977001332 |
| norm_ini | 1 |
| PR_ini | 1.968662709604115 |
| R_rms_ini | 0.6123724353664733 |
| dV | 0.030517578125 |
| dx | 0.3125 |
| box_PR_uniform | 8000 |
| box_n_cells | 262144 |
| collapse_threshold | 11.49357581527675 |
| fill_Rrms | 5 |
| N / L / dt / T / n_steps / seed | 64 / 20 / 0.0025 / 6 / 2400 / 42 |
| lambda_retuned | false |
| wall_seconds | 464.3421608870012 |
| finished_brt | 2026-08-21 17:42 BRT |

### 7.1 Sete runs — tabela completa

| run | source | Lambda | lam | Gamma | kT | f_FDT | noise_amp |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mem_unitary | load | -10 | [3, 1] | 0 | 0 | 0 | 0 |
| nomem_unitary | load | -10 | [0, 0] | 0 | 0 | 0 | 0 |
| mem_bath_cool | integrate | -10 | [3, 1] | 0.01 | 0.001 | 6.103515625e-07 | 0.000223606797749979 |
| mem_bath_mid | integrate | -10 | [3, 1] | 0.05 | 0.1 | 0.00030517578125 | 0.005 |
| mem_bath_hot | integrate | -10 | [3, 1] | 0.05 | 1 | 0.0030517578125 | 0.0158113883008419 |
| nomem_bath_hot | integrate | -10 | [0, 0] | 0.05 | 1 | 0.0030517578125 | 0.0158113883008419 |
| nomem_bath_mid | integrate | -10 | [0, 0] | 0.05 | 0.1 | 0.00030517578125 | 0.005 |

| run | peak_end | peak_max | t_peak_max | PR_end | R_rms_end | norm_end |
| --- | --- | --- | --- | --- | --- | --- |
| mem_unitary | 0.003429819606286119 | 13.17367282073293 | 0.1575 | 2656.870317928816 | 9.612080479106824 | 1.000000000001119 |
| nomem_unitary | 8.097538565889609 | 12.67960946296274 | 0.1425 | 0.4988270774697631 | 6.706517225983717 | 1.000000000000789 |
| mem_bath_cool | 0.004580025893981546 | 13.14725100398445 | 0.1575 | 3562.071168135517 | 9.812850079266902 | 1.794019083929307 |
| mem_bath_mid | 0.5988950796790661 | 12.91513703048579 | 0.155 | 4010.699644089231 | 10.00656964115193 | 362.5242074397553 |
| mem_bath_hot | 4.973991890969456 | 12.83467693401617 | 0.15 | 4283.09743171943 | 9.998644988927284 | 3604.161175006284 |
| nomem_bath_hot | 7.412776249709937 | 12.65070988093987 | 0.14 | 4012.77812391925 | 10.01585859108597 | 3620.609921465132 |
| nomem_bath_mid | 0.6331270920426743 | 12.55668079269137 | 0.1425 | 4001.874657574767 | 10.00119564954041 | 362.5963977950319 |

| run | t_collapse | t_fill | n_above_8x | t_last_8x | n_cells_end | wall_s | peak/norm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| mem_unitary | 0.1425 | 1.6325 | 12 | 0.17 | 87060.32657789145 | 0 | 0.003429819606282282 |
| nomem_unitary | 0.135 | 4.265 | 15 | 0.4025 | 16.3455656745292 | 0 | 8.097538565883218 |
| mem_bath_cool | 0.1425 | 1.085 | 12 | 0.17 | 116721.9480374646 | 99.4174481480004 | 0.002552941568464397 |
| mem_bath_mid | 0.1425 | 0.005 | 12 | 0.17 | 131422.6059375159 | 92.11300940100045 | 0.001652014037651792 |
| mem_bath_hot | 0.14 | 0.0025 | 10 | 0.1625 | 140348.5366425823 | 90.66627872699974 | 0.001380069217065684 |
| nomem_bath_hot | 0.13 | 0.0025 | 9 | 0.15 | 131490.713564586 | 91.37576403099956 | 0.002047383289142138 |
| nomem_bath_mid | 0.1325 | 0.005 | 9 | 0.1525 | 131133.42877941 | 90.64196641000308 | 0.001746093165549228 |

Leitura mantida: o único colapso preso é `nomem_unitary` (n_cells≈16, peak/norm≈8.10). Banhos quentes têm norm_end ~ 3600 (FDT injecta); peak_end 5–7 é chão térmico, não spike de grelha.

## 8 kstar 8 runs all k*L=9.424778

Veredito JSON: **H_grid**
Nota: First-allowed-shell lock: i*=1 and k*L=3*pi=9.42477796076938 on every record of all 8 runs (A,B,C,D). Not 16.3, not pi*N. Spectrum monotonically falling; no finite-k peak; packet spreads. See analysis.md.
kL_late_all_runs = 9.424777960769379
kL_identity = 3*pi = 2*pi*(i+1/2) with i=1
Uma linha analysis: **Verdict: H_grid**. k* é a primeira casca radial permitida (i*=1) em todos os registos de todos os runs. Mediana da janela tardia = **3π = 9.42477796076938**, não 16.3, não πN.

### 8.1 Física e identidades de malha

| campo | valor |
| --- | --- |
| Lambda_baseline | -8 |
| lam | [1.125, 0.375] |
| nu | [10, 0.5] |
| alpha / Gamma / f_FDT / V_ext | 0 / 0 / 0 / 0 |
| init_sigma / seed | 0.5 / 42 |
| T / dt / record_every / late_window | 8 / 0.0025 / 16 / t >= 0.8 T; medians |
| spectral | run_R5_A2.py radial shell-mean power; k_cut=2*pi/L; k*L=k_star*L |
| kL_nyquist_N64 | 201.0619298297468 |
| kL_nyquist_N48 | 150.7964473723101 |
| kL_shell_i1 = 3π | 9.424777960769379 |
| kL_shell_i2 = 5π | 15.70796326794897 |
| kL_shell_i3 | 21.99114857512855 |
| dossier_quote | 16.3 |
| wall_seconds | 175.1730860669995 |

### 8.2 Oito runs — k*L idêntico

| run | tags | L | Lambda | norm_target | N | k_star_L_ini | k_star_L_end | k_star_L_late_median | k_star_L_late_q25 | k_star_L_late_q75 | i_star_late |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A_L15 | A | 15 | -8 | 1 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| A_L20_baseline | A,B,C,D | 20 | -8 | 1 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| A_L25 | A | 25 | -8 | 1 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| B_Lam-6 | B | 20 | -6 | 1 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| B_Lam-10 | B | 20 | -10 | 1 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| C_norm0.5 | C | 20 | -8 | 0.5 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| C_norm2.0 | C | 20 | -8 | 2 | 64 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |
| D_N48 | D | 20 | -8 | 1 | 48 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 9.424777960769379 | 1 |

Confirmado: **todas** as colunas k*L valem 9.42477796076938.

### 8.3 Oito runs — estado e espectro

| run | peak_ini | norm_ini | PR_ini | R_rms_ini | C_ini | i_star_ini |
| --- | --- | --- | --- | --- | --- | --- |
| A_L15 | 1.436696977001332 | 0.9999999999999997 | 1.968701241132808 | 0.6123724356957946 | 0.9888757189667478 | 1 |
| A_L20_baseline | 1.436696976909594 | 1 | 1.968662709604115 | 0.6123724353664733 | 0.9952294968707962 | 1 |
| A_L25 | 1.436696158879071 | 0.9999999999999998 | 1.965068961038376 | 0.6123705560853713 | 0.9975388909537308 | 1 |
| B_Lam-6 | 1.436696976909594 | 1 | 1.968662709604115 | 0.6123724353664733 | 0.9952294968707962 | 1 |
| B_Lam-10 | 1.436696976909594 | 1 | 1.968662709604115 | 0.6123724353664733 | 0.9952294968707962 | 1 |
| C_norm0.5 | 0.7183484884547973 | 0.5000000000000001 | 1.968662709604114 | 0.6123724353664733 | 0.9952294968707961 | 1 |
| C_norm2.0 | 2.873393953819189 | 2 | 1.968662709604114 | 0.6123724353664733 | 0.9952294968707961 | 1 |
| D_N48 | 1.436691179751077 | 0.9999999999999999 | 1.959061850485163 | 0.6123607294342566 | 0.9993039618090037 | 1 |

| run | peak_end | PR_end | norm_end | C_end | i_star_end | peaked | mono_fall6 | wall_s |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A_L15 | 0.002265426747775664 | 1899.752969445845 | 1.000000000001538 | 0.9742804391693617 | 1 | false | true | 88.28949905899935 |
| A_L20_baseline | 0.001147502597989385 | 2225.046404899797 | 1.000000000001448 | 0.991722184710879 | 1 | false | true | 87.35960165500001 |
| A_L25 | 0.0009828622031176552 | 6003.186067765223 | 1.000000000001602 | 0.9965775929326954 | 1 | false | true | 89.17472834200089 |
| B_Lam-6 | 0.0003496827482295713 | 4559.546902036279 | 1.000000000001418 | 0.9898173141662927 | 1 | false | true | 87.88485302999834 |
| B_Lam-10 | 0.001395833702726802 | 3074.703251857741 | 1.000000000001406 | 0.9858209197424709 | 1 | false | true | 85.50662759700208 |
| C_norm0.5 | 0.0006090684151945487 | 1921.978503108485 | 0.5000000000007294 | 0.992769135897596 | 1 | false | true | 85.5861028060026 |
| C_norm2.0 | 0.00317125464483931 | 3859.539465808442 | 2.000000000002804 | 0.9678063340195131 | 1 | false | true | 86.86460753999927 |
| D_N48 | 0.001360777151007969 | 2064.71642206303 | 0.999999999993726 | 0.9990823240270162 | 1 | false | true | 30.55480947199976 |

| run | peak_late_med | PR_late_med | C_late_med | C_late_q25 | C_late_q75 | n_unique_i* |
| --- | --- | --- | --- | --- | --- | --- |
| A_L15 | 0.002635817109639169 | 1404.462285693086 | 0.9742844669772188 | 0.9742679101768943 | 0.9742989526259368 | 1 |
| A_L20_baseline | 0.0008625695445580549 | 3552.670852776767 | 0.9917193439730732 | 0.9917189708643017 | 0.9917201001644914 | 1 |
| A_L25 | 0.0004009272192142873 | 7691.572864096468 | 0.9965775707119862 | 0.9965774969182327 | 0.996577615394232 | 1 |
| B_Lam-6 | 0.0006879025890413828 | 4531.236069277857 | 0.9898155952968307 | 0.9898147667534132 | 0.9898161747586789 | 1 |
| B_Lam-10 | 0.0006276362101727654 | 4446.713359263809 | 0.985819969256716 | 0.9858191596141754 | 0.9858204284513671 | 1 |
| C_norm0.5 | 0.0004217076191527868 | 3463.338772534451 | 0.9927673023140877 | 0.9927667087536796 | 0.9927676130910127 | 1 |
| C_norm2.0 | 0.002920674002097843 | 3395.737905899231 | 0.9678863980432144 | 0.9678426584319736 | 0.9679444238050328 | 1 |
| D_N48 | 0.001028412310339735 | 3003.865931547226 | 0.9990819392438369 | 0.9990818866530751 | 0.999082070659262 | 1 |

| run | dx | dV | dk | k_cut | k_nyquist | kL_nyquist | kL_shell_i1 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A_L15 | 0.234375 | 0.01287460327148438 | 0.4188790204786391 | 0.4188790204786391 | 13.40412865531645 | 201.0619298297468 | 9.424777960769379 |
| A_L20_baseline | 0.3125 | 0.030517578125 | 0.3141592653589793 | 0.3141592653589793 | 10.05309649148734 | 201.0619298297468 | 9.424777960769379 |
| A_L25 | 0.390625 | 0.05960464477539062 | 0.2513274122871835 | 0.2513274122871835 | 8.042477193189871 | 201.0619298297468 | 9.424777960769379 |
| B_Lam-6 | 0.3125 | 0.030517578125 | 0.3141592653589793 | 0.3141592653589793 | 10.05309649148734 | 201.0619298297468 | 9.424777960769379 |
| B_Lam-10 | 0.3125 | 0.030517578125 | 0.3141592653589793 | 0.3141592653589793 | 10.05309649148734 | 201.0619298297468 | 9.424777960769379 |
| C_norm0.5 | 0.3125 | 0.030517578125 | 0.3141592653589793 | 0.3141592653589793 | 10.05309649148734 | 201.0619298297468 | 9.424777960769379 |
| C_norm2.0 | 0.3125 | 0.030517578125 | 0.3141592653589793 | 0.3141592653589793 | 10.05309649148734 | 201.0619298297468 | 9.424777960769379 |
| D_N48 | 0.4166666666666661 | 0.07233796296296266 | 0.3141592653589793 | 0.3141592653589793 | 7.539822368615514 | 150.7964473723101 | 9.424777960769379 |

Falhas mantidas: 16.3 nunca aparece; H_invar FAIL; H_mobile FAIL (Δ(k*L)=0); não é Nyquist (D: N=48 e N=64 dão o mesmo 3π; πN = 150.80 vs 201.06). Sem pico de k finito (`spectrum_peaked=false` nos 8).

## 9 bravais floors vs field

Veredito overall: **no crystal**
verdict_T: no crystal — no isolated finite-k shell and/or n_local_max_prom<=2; field score is not a lattice claim
verdict_maxC: no crystal — no isolated finite-k shell and/or n_local_max_prom<=2; field score is not a lattice claim
cryst_ok_T = false; cryst_ok_maxC = false
Uma linha analysis: **no crystal.** O campo R5 unitário N=64 T=8 nunca formou casca isolada de k finito.

### 9.1 Campo e detector

| campo | valor |
| --- | --- |
| N | 64 |
| L | 20 |
| dt | 0.0025 |
| T | 8 |
| Lambda | -8 |
| lam | [1.125, 0.375] |
| nu | [10, 0.5] |
| Gamma | 0 |
| init_sigma | 0.5 |
| seed | 42 |
| window | 0.15 |
| cos_min | 0.85 |
| angle_max_deg | 31.78833061705162 |
| rule | 1 - max_a(khat·a) < window  (equiv. angle < arccos(1-window)) |
| kstar_T | 0.3141592653589793 |
| kstarL_T | 6.283185307179586 |
| kstarL_resolved_ref | 16.3 |
| M_poisson | 1 |
| M_source | (k*L/2pi)^3 fallback |
| M_from_kstar | 1 |
| M_nodes_localmax | 1179 |
| n_local_max_all_T | 2827 |
| n_local_max_prom_T | 1179 |
| n_local_max_prom_maxC | 2067 |
| peak_T | 0.001147502597989385 |
| PR_T | 2225.046404899797 |
| norm_T | 1.000000000001448 |
| peak_maxC | 0.0007742612103243557 |
| PR_maxC | 4129.710643445787 |
| t_maxC | 6.100000000000001 |
| field_source | integrated |
| field_wall_s | 100.2937581940023 |
| finished_brt | 2026-08-21 17:36:37 -03 |

### 9.2 Scores do campo T e maxC

| família | field_T | field_maxC |
| --- | --- | --- |
| SC | 0.341823810453639 | 0.3418293726208645 |
| BCC | 0.6581761895463608 | 0.6581706273791356 |
| FCC | 0 | 0 |
| HCP | 0.5612158736357618 | 0.561219581747244 |
| best | BCC | BCC |
| best_score | 0.6581761895463608 | 0.6581706273791356 |
| kstar | 0.3141592653589793 | 0.3141592653589793 |
| kstarL | 6.283185307179586 | 6.283185307179586 |
| n_shell | 18 | 18 |
| C | 0.991722184710879 | 0.991718170579337 |
| C_star | 0.0208149835703437 | 0.02082478612074242 |
| contrast | 5553.259554943902 | 5557.873716642361 |

### 9.3 floor_vs_field

| campo | valor |
| --- | --- |
| field_best_T | 0.6581761895463608 |
| field_best_family | BCC |
| field_kstarL | 6.283185307179586 |
| overall_verdict | no crystal |
| note_022_vs_046 | 0.46 < BCC resolved floor 0.931; 0.22 < SC resolved floor 0.331; neither is an excess |

| família | field_scores_T | iso_field_k | iso_mean+2std | iso_std | resolved_iso_16.3 | resolved_iso_std | resolved_poisson_M1179 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SC | 0.341823810453639 | 0.3351051571046079 | 0.5627321303614606 | 0.1138134866284264 | 0.3312140256220921 | 0.03953759830485915 | 0.3403223792475819 |
| BCC | 0.6581761895463608 | 0.664894842895392 | 0.8925218161522448 | 0.1138134866284264 | 0.9307491895431571 | 0.02153047387448479 | 0.9420974560451456 |
| FCC | 0 | 0 | 0 | 0 | 0.5277963756901725 | 0.05481395106998099 | 0.5450433025863783 |
| HCP | 0.5612158736357618 | 0.5491359656853307 | 0.7635892110774098 | 0.1072266226960396 | 0.5091962046203091 | 0.05924879275698738 | 0.5119498291805151 |

### 9.4 Pisos (todas as famílias / todas as redes)

#### piso `isotropic_inj`

| família | valores |
| --- | --- |
| SC | mean=0.3351051571046079; std=0.1138134866284264; mean_plus_2std=0.5627321303614606; n=32 |
| BCC | mean=0.664894842895392; std=0.1138134866284264; mean_plus_2std=0.8925218161522448; n=32 |
| FCC | mean=0; std=0; mean_plus_2std=0; n=32 |
| HCP | mean=0.5491359656853307; std=0.1072266226960396; mean_plus_2std=0.7635892110774098; n=32 |
| BEST | mean=0.6956044855754484; std=0.08678841170468077; mean_plus_2std=0.8691813089848099 |

#### piso `isotropic_ownk`

| família | valores |
| --- | --- |
| SC | mean=0.2014181888964577; std=0.217813228943734; mean_plus_2std=0.6370446467839257; n=32 |
| BCC | mean=0.3799200674524446; std=0.3652030349098176; mean_plus_2std=1.11032613727208; n=32 |
| FCC | mean=0.6176423745772555; std=0.4342644157681449; mean_plus_2std=1.486171206113545; n=32 |
| HCP | mean=0.2790009835500945; std=0.2871420360946867; mean_plus_2std=0.8532850557394679; n=32 |
| BEST | mean=0.8701108206917829; std=0.1420590044430351; mean_plus_2std=1.154228829577853 |

#### piso `poisson_inj`

| família | valores |
| --- | --- |
| SC | mean=0.3333333333333333; std=5.551115123125783e-17; mean_plus_2std=0.3333333333333334; n=32 |
| BCC | mean=0.6666666666666667; std=9.56298117598241e-17; mean_plus_2std=0.666666666666667; n=32 |
| FCC | mean=0; std=0; mean_plus_2std=0; n=32 |
| HCP | mean=0.5555555555555556; std=6.305643054894281e-17; mean_plus_2std=0.5555555555555557; n=32 |
| BEST | mean=0.6666666666666667; std=9.56298117598241e-17; mean_plus_2std=0.666666666666667 |

#### piso `poisson_ownk`

| família | valores |
| --- | --- |
| SC | mean=0.28125; std=0.1229673442094912; mean_plus_2std=0.5271846884189824; n=32 |
| BCC | mean=0.5815972222222222; std=0.209650851868927; mean_plus_2std=1.000898925960076; n=32 |
| FCC | mean=0.15625; std=0.3689020326284735; mean_plus_2std=0.8940540652569471; n=32 |
| HCP | mean=0.4699074074074074; std=0.2022457874856441; mean_plus_2std=0.8743989823786956; n=32 |
| BEST | mean=0.7187499999999999; std=0.1229673442094912; mean_plus_2std=0.9646846884189823 |

#### piso `shellrand`

| família | valores |
| --- | --- |
| SC | mean=0.3328690103658142; std=0.001682132849171752; mean_plus_2std=0.3362332760641578; n=32 |
| BCC | mean=0.6671309896341857; std=0.001682132849171734; mean_plus_2std=0.6704952553325292; n=32 |
| FCC | mean=0; std=0; mean_plus_2std=0; n=32 |
| HCP | mean=0.5555113343205524; std=0.00182335742175532; mean_plus_2std=0.5591580491640631; n=32 |
| BEST | mean=0.6671309896341857; std=0.001682132849171734; mean_plus_2std=0.6704952553325292 |

#### piso `poisson_Mnodes_inj`

| família | valores |
| --- | --- |
| SC | mean=0.3528317992574099; std=0.1666410778270427; mean_plus_2std=0.6861139549114954; n=32 |
| BCC | mean=0.6471682007425902; std=0.1666410778270428; mean_plus_2std=0.9804503563966758; n=32 |
| FCC | mean=0; std=0; mean_plus_2std=0; n=32 |
| HCP | mean=0.5740747941275532; std=0.156196834441579; mean_plus_2std=0.8864684630107112; n=32 |
| BEST | mean=0.739456447407713; std=0.08271174113478647; mean_plus_2std=0.9048799296772859; n=32 |

#### piso `poisson_Mnodes_resolved`

| família | valores |
| --- | --- |
| SC | mean=0.3403223792475819; std=0.07023910879545821; mean_plus_2std=0.4808005968384983; n=32 |
| BCC | mean=0.9420974560451456; std=0.02629181607153677; mean_plus_2std=0.9946810881882191; n=32 |
| FCC | mean=0.5450433025863783; std=0.07741375796038696; mean_plus_2std=0.6998708185071523; n=32 |
| HCP | mean=0.5119498291805151; std=0.06493523117684492; mean_plus_2std=0.6418202915342049; n=32 |
| BEST | mean=0.9420974560451456; std=0.02629181607153677; mean_plus_2std=0.9946810881882191; n=32 |

#### piso `isotropic_resolved`

| família | valores |
| --- | --- |
| SC | mean=0.3312140256220921; std=0.03953759830485915; mean_plus_2std=0.4102892222318104; n=32 |
| BCC | mean=0.9307491895431571; std=0.02153047387448479; mean_plus_2std=0.9738101372921267; n=32 |
| FCC | mean=0.5277963756901725; std=0.05481395106998099; mean_plus_2std=0.6374242778301344; n=32 |
| HCP | mean=0.5091962046203091; std=0.05924879275698738; mean_plus_2std=0.6276937901342838; n=32 |
| BEST | mean=0.9307491895431571; std=0.02153047387448479; mean_plus_2std=0.9738101372921267; n=32 |

### 9.5 verdict_T / verdict_maxC detalhe

| campo | verdict_T | verdict_maxC |
| --- | --- | --- |
| verdict | no crystal | no crystal |
| reason | no isolated finite-k shell and/or n_local_max_prom<=2; field score is not a lattice claim | no isolated finite-k shell and/or n_local_max_prom<=2; field score is not a lattice claim |
| family | BCC | BCC |
| field_best | 0.6581761895463608 | 0.6581706273791356 |
| iso_mean | 0.664894842895392 | 0.664894842895392 |
| iso_mean_plus_2std | 0.8925218161522448 | 0.8925218161522448 |
| poi_mean_plus_2std | 0.666666666666667 | 0.666666666666667 |
| scr_mean_plus_2std | 0.6704952553325292 | 0.6704952553325292 |
| ratio_to_iso_mean | 0.9898951639934914 | 0.9898867985094082 |
| above_iso_2sig | false | false |
| above_poi_2sig | false | false |
| above_shellrand_2sig | false | false |
| low_kstar_bin | true | true |
| few_nodes | false | false |

### 9.6 self_check do detector + continuum

kstar self-check = 1.256637061435917; kstarL = 25.13274122871834; window = 0.15

| rede perfeita | best | SC | BCC | FCC | HCP |
| --- | --- | --- | --- | --- | --- |
| perfect_SC | SC | 1 | 1.937138208166768e-34 | 6.365602480057836e-37 | 1 |
| perfect_BCC | BCC | 0.002735314860192557 | 0.9995681620858058 | 9.557525842371504e-35 | 0.3347729637491286 |
| perfect_FCC | BCC | 0.007282605973831706 | 0.9990786934451675 | 0.9408286938379097 | 0.3371281874127212 |
| perfect_HCP | HCP | 0.7103399499016216 | 0.454450904547875 | 3.614260755326722e-35 | 1 |

isotropic_inj no self_check:
| SC | BCC | FCC | HCP |
| --- | --- | --- | --- |
| 0.4181867997386141 | 0.8439129681196377 | 0.4382092035549399 | 0.6068500999131086 |

| família | n_dirs | no_overlap |
| --- | --- | --- |
| SC | 6 | 0.45 |
| BCC | 12 | 0.8999999999999999 |
| FCC | 8 | 0.6 |
| HCP | 8 | 0.6 |

Nota mantida: 0.46 < piso BCC resolvido 0.931; 0.22 < piso SC resolvido 0.331; nenhum é excesso. Janela 0.15 congelada.

## 10 hashes

SHA256 reportados nos JSON e ficheiros `SHA256` da pasta. Também hashes recalculados agora dos `result.json`.

| objecto | sha256 | origem |
| --- | --- | --- |
| A3 stepper (3D Strang) | `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` | JSON A3/A128/A160/hotbath/kstar/bravais |
| A3_N128 runner | `e1d5fca10a36b9b593e8c84385d36077358fe59117872175f72eb683d29af4fb` | JSON |
| A3_N160 runner | `ffa6a5f94288cb9b6b0507f5fc799f11a0fa545aa4218cf85056a7fe8dff89ae` | JSON |
| QM1D / 1D stepper | `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076` | JSON QM1D; sidebands stepper_src; tunnel stepper |
| CHSH runner | `5f543afa76927f7c8aee2f39501240b6cc3e1e30038e1d1a92431c0a65700f38` | JSON |
| sidebands runner | `84391c14f8d6d35adeef4fdbf0408e13ef7679f229412d725d99325f7e495661` | JSON |
| sidebands predictions | `d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47` | JSON |
| sidebands go_one | `b8a9b3041d74278d186bcc2c2cba6e08f9bdea89f138446576c809a925c43a78` | JSON |
| tunnel runner | `b103f6d921de1067ede758da89f17d7d93bacc95549a345ead1c96ee3cc576da` | JSON |
| tunnel predictions | `5ea1d58c5be2a488c07761da8c55852ecd64728eef3334d115823128112012b4` | JSON |
| hotbath stepper | `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` | JSON |
| hotbath predictions | `b7936bdd039c0ad96cf9cc28d7da226906b276b9e3c353713887115126ea2511` | JSON |
| kstar stepper | `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` | JSON |
| kstar predictions | `7711f5679cb616a959e3a6cf2b855c6c6303c471c58292cc0fe0f7e822e112b1` | JSON |
| bravais detector | `52fcb4151d27e77dc6e794e17f2e45a2aea9a96a47b7e85ea43a8efcc8cd8e8a` | JSON |
| bravais stepper | `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` | JSON |
| bravais predictions | `c8481dd40aac49020cad253f68e424bc0acbb51274892de4feb13388eea309f7` | JSON |

### 10.1 SHA256 recalculados nesta compilação

| ficheiro | sha256 | bytes |
| --- | --- | --- |
| /workspace/dossie_reexec/A3/result.json | `db4b1e191b0144a1ae345ccfd0036228d0eb0a1b0f8e92583ed1dd7abef25ba9` | 1849 |
| /workspace/dossie_reexec/A3_N128/result.json | `c3f1eb7f208ab2171fdad7deff36d31f81f3c47b6b86da6fc56133a2ebc843e1` | 1778 |
| /workspace/dossie_reexec/A3_N160/result.json | `efc2bd8046016101ad5ce192a7edb8db2ec1eb25f2b63db708f51b68ff570cfa` | 25374 |
| /workspace/dossie_reexec/QM1D/result.json | `57b6a6fa73eb98bf7f12c76d518234f3c9352813c98847324a7e5a834d3f9cb1` | 8891 |
| /workspace/dossie_reexec/CHSH/raw/result.json | `c09be35f895a47f0a54a1efdeff0d4a9bccb0e280fc7d4869e73353e9e8de33a` | 4102 |
| /workspace/dossie_reexec/sidebands/result.json | `bb3a5ae57fe0becfd77ae638dc006cd2eb528b291f964e3fbdf878d2be0b6662` | 21623 |
| /workspace/dossie_reexec/tunnel_hist/result.json | `c75f95e6078a07c8abcf701e49988adcb359185d35574e1431a20272347be4a4` | 6386 |
| /workspace/dossie_reexec/hotbath/result.json | `0003b1155d5b4c061efd8c1f31813c6c7467c58fb2081294deb8db96ac261523` | 7415 |
| /workspace/dossie_reexec/kstar/result.json | `98d8829ba5443fe5ae095aefe51f407820973086221872b711d1af21a5e7e8e2` | 17739 |
| /workspace/dossie_reexec/bravais/result.json | `0ed572a5e7b8655ed2ffdb3350e9a36ef5abd34bb96393ed8f2dfaa7acf76f0c` | 15523 |

### 10.2 Ficheiros SHA256 das pastas

#### `/workspace/dossie_reexec/hotbath/SHA256`

```
b7936bdd039c0ad96cf9cc28d7da226906b276b9e3c353713887115126ea2511  predictions_hotbath.md
b7936bdd039c0ad96cf9cc28d7da226906b276b9e3c353713887115126ea2511  hotbath/predictions_hotbath.md
7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713  hotbath/code/stepper.py
58c1344d937c5fc75e5d7a2e67e387071cc6858fda2af1b016d181e78ae18614  hotbath/code/run_hotbath.py
e2b23951b2b7acd03f36de63ddb33225a99975025e9e0a5ae18e659a9f0cf05a  hotbath/code/plot_hotbath.py
c14ca46daf99dd62b6961b9288656e7e92b917708fa1796d009f97688e821030  hotbath/code/launch.py
0003b1155d5b4c061efd8c1f31813c6c7467c58fb2081294deb8db96ac261523  hotbath/result.json
37c8f6583c0e0f2d4e4cc114ec882b6cf46211604baf46a5ace87ce817f1caf8  hotbath/analysis.md
6f45b8dcae2735b7dd10e12fb97e98b08733eeaeefc9ecad80c542ce256d1e87  hotbath/raw/mem_unitary.csv
2ca94de7b186c39ef979890c7558c117b1a68ec44494254bb122ed3520dbd561  hotbath/raw/nomem_unitary.csv
d87a2adc00387eb1cdca98a4cd9fb706bf2064c937fe1908c15171bcd6da981f  hotbath/raw/mem_bath_cool.csv
60a4cbc916f043d23e6549dadb4ce6ae58b01b2380da5d5d867120ad0258c149  hotbath/raw/mem_bath_mid.csv
370023d164bad40060bd73449937fb32a13b447932e4dc45f941fd3cc71ab85b  hotbath/raw/mem_bath_hot.csv
6dada0acec35599e92de29892c876622ca87ec1cb0c11bf5e25aceedb738728f  hotbath/raw/nomem_bath_hot.csv
354fc10ccae223b812ff5aa2c308eb7c4581217e887289dd3af8115f50710847  hotbath/raw/nomem_bath_mid.csv
7dba36e6c3ebbca105233eeed27bfa4c339a20f2d4cbe31f1fa919bc8da472be  hotbath/figures/peak_vs_t.png
60587fc98c3c77d1e9b79166b5220346ffa0517f6ac02f48db6bf31cc086ae3f  hotbath/figures/PR_vs_t.png
42aff30807c1bd881664a1c327cab3868746a6ad049da390ab55a3439cfc8c0a  hotbath/figures/Rrms_vs_t.png
```

#### `/workspace/dossie_reexec/sidebands/SHA256`

```
58577f795878b8939383465b1900689c9e0798e73f1a4b8cbd74617074966a18  /workspace/dossie_reexec/sidebands/analysis.md
e0ac2061160383a8bc140114982fdfeaac34fa3ab5f1953609947921a621cca5  /workspace/dossie_reexec/sidebands/code/__pycache__/run_sidebands.cpython-313.pyc
2c36df18ea0994a1902dc71f94a56f136aed2a44fc84e645e08034d5e284f9d6  /workspace/dossie_reexec/sidebands/code/__pycache__/sb_integ.cpython-313.pyc
2f3782322ff920e632c8f3032aed1ab8e771ac055d272b83afb4c85d85b7550b  /workspace/dossie_reexec/sidebands/code/__pycache__/sb_out.cpython-313.pyc
326bd1c3b6d91e6902f32e987c08fae726da8b33b3adabf008e76aee638adc36  /workspace/dossie_reexec/sidebands/code/__pycache__/sb_peaks.cpython-313.pyc
524d3e757aad3fdc625fbaf7997c19c003831557794529b82fa4f90fc21c8099  /workspace/dossie_reexec/sidebands/code/__pycache__/sb_report.cpython-313.pyc
6adec6c6e68f61030c85894ecc418bda1c5b33c64f7e0cc891dc8680a47d52fe  /workspace/dossie_reexec/sidebands/code/__pycache__/sb_step.cpython-313.pyc
0b784e06fd2c4ace123300ee1269244115751c3a891f0ed6084f9076b611fc02  /workspace/dossie_reexec/sidebands/code/finish_from_raw.py
b8a9b3041d74278d186bcc2c2cba6e08f9bdea89f138446576c809a925c43a78  /workspace/dossie_reexec/sidebands/code/go_one.py
fd8c95b543fee5440e2c7c14b808d4b18062bc39ff0ccefc9ab4c91bd02c3640  /workspace/dossie_reexec/sidebands/code/go_post.py
8aac3e0a7b5a0d63da85a5c9f744721c6b1247bf00eb264a38b1523410ab3939  /workspace/dossie_reexec/sidebands/code/launch.py
bf527af734c54fd45bb86d6a23d6c506c9fce75f69c7934d08ae3da5cc769dbb  /workspace/dossie_reexec/sidebands/code/launch.sh
38cd3eed68376d34c6b854d650b08dad455710606c5b8af6756e98ac495c3ca0  /workspace/dossie_reexec/sidebands/code/patch_report.py
84391c14f8d6d35adeef4fdbf0408e13ef7679f229412d725d99325f7e495661  /workspace/dossie_reexec/sidebands/code/run_sidebands.py
e4d03a77726b9a2165240b1ca33a81b35c53201d82751c41333eb564f957ba17  /workspace/dossie_reexec/sidebands/code/sb_integ.py
22f33c6a0eef8670e13681708e9d1c4343677ef397dd0e59323d375bd5d08a2d  /workspace/dossie_reexec/sidebands/code/sb_out.py
0381e0e14cf6404201abd3d42e016d6f8ad79d15e29e6d98351aa132b86d60bc  /workspace/dossie_reexec/sidebands/code/sb_peaks.py
ed6fed2c241bd8ae169ee14e710d4864308dc65a45afd3cdfb3b42addda7e1f6  /workspace/dossie_reexec/sidebands/code/sb_report.py
fb188a71350e127e69dbae0c91cc1f3d732f559717ef38fcb5a44ee574ae4e5a  /workspace/dossie_reexec/sidebands/code/sb_step.py
1bd0dd9e3f2cf76d3a138951b621393b6c2ebab09c3d2bbc04c0774dfb6a75b3  /workspace/dossie_reexec/sidebands/figures/c_t.png
ce4f77050fa87b3df3ce1a9fb5b66305f839f2f0af6f6bf2e53c05445392603d  /workspace/dossie_reexec/sidebands/figures/spectra.png
cc13d89197b75c00879e197907438940abbe57cf10b5bfd9dba4d2ada539ed7c  /workspace/dossie_reexec/sidebands/raw/Lambda_m2.npz
f719e0fcb3012d11362d59c42282adeb5a17752a44b4fef2384020e631653899  /workspace/dossie_reexec/sidebands/raw/Lambda_m2_T251.npz
1d14854adb463f95d4efd249bcfe40e64ce3ecff3d706b887b5bb0fcce348692  /workspace/dossie_reexec/sidebands/raw/Lambda_m2_mem.npz
9806cc153b909fdeec14b5d0c7e58127763122e9ac0afa7d578c4cbf04e88908  /workspace/dossie_reexec/sidebands/raw/Lambda_m2_mem_T80.npz
43b35fcef5c8cd287c998d7a279b5935bc393dd5b47f91cd5215c35409b3a6fd  /workspace/dossie_reexec/sidebands/raw/Lambda_p2.npz
b0510c48dcca43bf3caad598b5367df83f3b0d87aceb0dd2ae3d396e5639d5e5  /workspace/dossie_reexec/sidebands/raw/c_t_Lambda_m2.csv
38090e3b353199c889c93032e08a5f96110ce6227a6c121d9f94b65fd381a316  /workspace/dossie_reexec/sidebands/raw/c_t_Lambda_m2_T251.csv
36ac768ddc15b33294feb68036621f0d64114fb79ed63ec2d6835ad08b348946  /workspace/dossie_reexec/sidebands/raw/c_t_Lambda_m2_mem.csv
73d0837eebe3fc39d26f7d3589d9f8462f9ddcb0ab65e21dd80bda8c967c8640  /workspace/dossie_reexec/sidebands/raw/c_t_Lambda_m2_mem_T80.csv
14d1d0e2995b37f7f7b8c91bd2f22ef805a9393868ec83c214aea0929d85d4fb  /workspace/dossie_reexec/sidebands/raw/c_t_Lambda_p2.csv
82fa52460f1df20cd8820218e6f7a280bb155fd1d10d8b551604cf79b6f1572f  /workspace/dossie_reexec/sidebands/raw/c_t_linear.csv
cca8c830e0ae9d60eab13292c77e213496912259de96ef5d61aa9d2f59ae5140  /workspace/dossie_reexec/sidebands/raw/diag_Lambda_m2.csv
efc834c15e8ed5e86025f5c12b32ce45c276667b54c52f6cc4cc57aa218deb8a  /workspace/dossie_reexec/sidebands/raw/diag_Lambda_m2_T251.csv
2df03767f8102281a9b3290769a835ed417a3d9e33daafbdee3c0211df0419cb  /workspace/dossie_reexec/sidebands/raw/diag_Lambda_m2_mem.csv
a4bc7a5b0e5fbb16fe4b7652ad4c58a9e75ae9e20403833792b2344f2d1d2a37  /workspace/dossie_reexec/sidebands/raw/diag_Lambda_m2_mem_T80.csv
a798399743bcf9a836539fea7cc36c037f103c3e3916f1748c784245810ffa88  /workspace/dossie_reexec/sidebands/raw/diag_Lambda_p2.csv
ad51a093525b4d9df49d2c7246a4bd852f76dd10b60b787602f943468c1b3fc2  /workspace/dossie_reexec/sidebands/raw/diag_linear.csv
48ab51bbbc091f524742407f0afc281d16383bac472fdb7b24137fc37071ebc8  /workspace/dossie_reexec/sidebands/raw/linear.npz
744c7b7127b14415c268ea98354b22831f9b511ccafbdfaa88a4b3e02a48b999  /workspace/dossie_reexec/sidebands/raw/meta_Lambda_m2.json
75b4bf1299de48a5ab0bf67224e6eac9e5d4fc02dce87b438e37edb7986bd44c  /workspace/dossie_reexec/sidebands/raw/meta_Lambda_m2_T251.json
cf5eb084059e0e1838e423f4f091b9c234315888ea91883166096189fb3a365c  /workspace/dossie_reexec/sidebands/raw/meta_Lambda_m2_mem.json
1dbfd8484f2aed4ca3f6ad408f8d03fbe0ea62757972efc0feccb4876b563a19  /workspace/dossie_reexec/sidebands/raw/meta_Lambda_m2_mem_T80.json
42256c2211c8ee96101b2a63922dfb18b3f409c4b3a3049672602035e822b36f  /workspace/dossie_reexec/sidebands/raw/meta_Lambda_p2.json
f37700a660d25f02cfe82728518c79661908f7d41ee136a6d7ab609d6522d2c5  /workspace/dossie_reexec/sidebands/raw/meta_linear.json
32b9d15616dfa596e0ecb3882f57b125da2c6b344516267d6e5001ac314926fa  /workspace/dossie_reexec/sidebands/raw/peaks_Lambda_m2.csv
35994183e5efeb11fab98465300d4cf0b3fe9616dae106a0bd67b85abdd8fad6  /workspace/dossie_reexec/sidebands/raw/peaks_Lambda_m2_T251.csv
0150cbac86634d3163a207afebcdbf7c698e9b44f6af3a67b306ddf9d780e5b3  /workspace/dossie_reexec/sidebands/raw/peaks_Lambda_m2_mem.csv
6a77c9e84771c72bc3a0336c2135252c7120759fc92c65f0711d7e6110bec29e  /workspace/dossie_reexec/sidebands/raw/peaks_Lambda_m2_mem_T80.csv
57e854adbf5db574cd1375811b2c0b7622b8dcd4dc9dc40dbcb6bacde57dc410  /workspace/dossie_reexec/sidebands/raw/peaks_Lambda_p2.csv
4cfef582cc95b8536ca1a79038d5519df878aecc43c845f06012d07efe4d6999  /workspace/dossie_reexec/sidebands/raw/peaks_linear.csv
bb3a5ae57fe0becfd77ae638dc006cd2eb528b291f964e3fbdf878d2be0b6662  /workspace/dossie_reexec/sidebands/result.json
d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47  /workspace/dossie_reexec/predictions_sidebands.md
```

#### `/workspace/dossie_reexec/tunnel_hist/SHA256`

```
b103f6d921de1067ede758da89f17d7d93bacc95549a345ead1c96ee3cc576da  /workspace/dossie_reexec/tunnel_hist/code/run_tunnel_hist.py
5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076  /workspace/dossie_reexec/tunnel_hist/code/stepper1d.py
750d98256fa251a298429afdaeefce106f52c0b41f19c4dc797ec15cf3752da4  /workspace/dossie_reexec/tunnel_hist/code/launch.py
5ea1d58c5be2a488c07761da8c55852ecd64728eef3334d115823128112012b4  /workspace/dossie_reexec/predictions_tunnel_hist.md
c75f95e6078a07c8abcf701e49988adcb359185d35574e1431a20272347be4a4  /workspace/dossie_reexec/tunnel_hist/result.json
da9e4edf55371655fa231715abb3b131aeba91c5fce2aa1477cebac84d7f9b03  /workspace/dossie_reexec/tunnel_hist/analysis.md
1cea4bca18181a09eaa3ee7b65ffa29d01b7e68a18f51e5c1c44e2ea538eed13  /workspace/dossie_reexec/tunnel_hist/raw/summary.csv
3c7e21e9ef9c6f802e7eff1fba9c674f57e8b551138ab80ca862c717846eb409  /workspace/dossie_reexec/tunnel_hist/raw/timeseries.csv
62fa1aab47094a89d2c83367a2988aab98bac9e88bdc40058b13e9445bc1e848  /workspace/dossie_reexec/tunnel_hist/figures/two_pass.png
```

### 10.3 Hashes de analysis.md / predictions (recalculados)

| ficheiro | sha256 |
| --- | --- |
| /workspace/dossie_reexec/predictions_A3.md | `d67ed66caaa6a17ae9efa82a6450d37beaf77917e188902a4f0fb038a36d4010` |
| /workspace/dossie_reexec/predictions_A3_N128.md | `a445b1a9281fd57939dd3e9fd7aa5f7222e526eedc6f342fce0cd30c2be656f6` |
| /workspace/dossie_reexec/predictions_A3_N160.md | `b7656b1f99aa5143ebc673ebe453c7e15af3e4eb972dfd721c627fbc567dabcc` |
| /workspace/dossie_reexec/predictions_CHSH.md | `2ad5632ebf0855b9f58f23deea7fbf594def156b6780fb13da17798691d16667` |
| /workspace/dossie_reexec/predictions_QM1D.md | `64801a853e9f3290b3f9e3a833eb3655a95cf8498124acb10d226f5077e55bba` |
| /workspace/dossie_reexec/predictions_bravais.md | `c8481dd40aac49020cad253f68e424bc0acbb51274892de4feb13388eea309f7` |
| /workspace/dossie_reexec/predictions_hotbath.md | `b7936bdd039c0ad96cf9cc28d7da226906b276b9e3c353713887115126ea2511` |
| /workspace/dossie_reexec/predictions_kstar.md | `7711f5679cb616a959e3a6cf2b855c6c6303c471c58292cc0fe0f7e822e112b1` |
| /workspace/dossie_reexec/predictions_sidebands.md | `d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47` |
| /workspace/dossie_reexec/predictions_tunnel_hist.md | `5ea1d58c5be2a488c07761da8c55852ecd64728eef3334d115823128112012b4` |
| /workspace/dossie_reexec/A3/analysis.md | `6ac412263f2828497b5d25b35852566f938d5b1457d39fb28e7934cefa4a0200` |
| /workspace/dossie_reexec/A3_N128/analysis.md | `b22b743eb1de44e8a7b0b5f5f6f8827ae6359483749092b1111e5574948b2423` |
| /workspace/dossie_reexec/A3_N160/analysis.md | `57ce966088261efea75e0deb68a230a2434c50cd75768486981a65f7ccd3fdd9` |
| /workspace/dossie_reexec/QM1D/analysis.md | `1a98d160546ebe2298dd97f48984e4ffe6dcb0f9e564321eb046a4bcb15c0058` |
| /workspace/dossie_reexec/CHSH/analysis.md | `227ac7f79cdda78c9b3fc895d0795458a5d92109f738900cad2533d4447df8f9` |
| /workspace/dossie_reexec/sidebands/analysis.md | `58577f795878b8939383465b1900689c9e0798e73f1a4b8cbd74617074966a18` |
| /workspace/dossie_reexec/tunnel_hist/analysis.md | `da9e4edf55371655fa231715abb3b131aeba91c5fce2aa1477cebac84d7f9b03` |
| /workspace/dossie_reexec/hotbath/analysis.md | `37c8f6583c0e0f2d4e4cc114ec882b6cf46211604baf46a5ace87ce817f1caf8` |
| /workspace/dossie_reexec/kstar/analysis.md | `31dbfd68489a7dd0f15d524fd98772df2b9e02837f1405a065e16f15daff6984` |
| /workspace/dossie_reexec/bravais/analysis.md | `d9b5c622053cc114bfbe8ea100650eee24b7ac5fe3a4b0ca1195e25e69ebc662` |
| /workspace/dossie_reexec/A3/code/stepper.py | `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713` |
| /workspace/dossie_reexec/QM1D/code/stepper1d.py | `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076` |

### 10.4 Integridade

- Previsões escritas **antes** das integrações; ficheiros `predictions_*.md` não reescritos depois.
- Stepper 3D único: `7bbc95b990ffa85175826aaa4f054db0a5e233471b63cdb91251308dc9156713`.
- Stepper 1D único: `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`.
- sidebands: `stepper_src_sha256` == `stepper_src_expected` (kernel 1D).
- Falhas mantidas: pulso 8× da memória; vis P1 sob foco; leak P4/sidebands; tunnel dirty; hotbath átomo; k*L=3π≠16.3; bravais sem cristal.
- λ não retocado em lado nenhum.

---

*Fim da compilação. Fonte: JSON em disco, 21 ago 2026. Box `/workspace/dossie_reexec/`.*
