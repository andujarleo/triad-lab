> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/%C3%8Dndice%20de%20runs.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, moc]
aliases: [índice, runs, cronologia]
```


# Índice de runs

Antologia com o texto integral de 01–36 + Q00–Q04: [00 registro_completo](00%20registro_completo.md) · [TRIAD_registro_completo_simulacoes_2026-08-21](../Fontes/TRIAD_registro_completo_simulacoes_2026-08-21.md).

36 diretórios, ordem do registro. 36 = reexecução dossiê (Linux box, 21/08/2026). 1–26 = PDF 20/08/2026; 27–28 = noite 20/08/2026, solver real (triad-lang); 29 = noite 20/08/2026, spec §5 Strang standalone; 30 = 21/08/2026, Theta_core I0 dois átomos; 31 = 21/08/2026, Theta_core I0 ninho concêntrico; 32 = 21/08/2026, Theta_core I0 universo-átomo + par +/−; 33 = 21/08/2026, Theta_core I0 ninho +/− concêntrico; 34 = 21/08/2026, mesma IC do 33, T=60. 35 = 21/08/2026, Theta_core I0 singularidade finita (T=1, 1 e 2 pontos). Título da nota = id do diretório. Falhas e vazios entram.

| # | run | classe | status | resultado (PDF) |
|---|---|---|---|---|
| 1 | [triad_sim](01%20triad_sim.md) | Exploratória / pré-referência | completo | visual 2D, duas gaussianas + termo relacional; sem CSV |
| 2 | [triad_nls_fdt](02%20triad_nls_fdt.md) | Exploratória / pré-referência | completo | primeiro NLS+memória+FDT; visual |
| 3 | [triad_nls_fdt_v2](03%20triad_nls_fdt_v2.md) | Exploratória / pré-referência | completo | v2 + trajetórias de picos; visual |
| 4 | [triad_atoms_gaussians](04%20triad_atoms_gaussians.md) | Exploratória / pré-referência | completo | átomos gaussianos; visual |
| 5 | [triad_atoms_individual_fields](05%20triad_atoms_individual_fields.md) | Exploratória / pré-referência | completo | identidades gaussianas separadas; visual |
| 6 | [triad_limit_test](06%20triad_limit_test.md) | Tentativa sem artefatos | vazio | cronologia |
| 7 | [triad_limit_test_fast](07%20triad_limit_test_fast.md) | Exploratória quantitativa | completo | N={2,4,8,12} r={4,6,8}; δR>0 só N=2,r=4 |
| 8 | [triad_observer_observed_consciousness](08%20triad_observer_observed_consciousness.md) | Exploratória | completo | mean_abs_C 0 vs 0.140886; R quase idêntico |
| 9 | [triad_field_consciousness_test](09%20triad_field_consciousness_test.md) | Exploratória | completo | bounce_amplitude=0; C_memory_corr=−0.385509 |
| 10 | [triad_3d_anticollapse_test](10%20triad_3d_anticollapse_test.md) | Exploratória 3D / pré-ref | completo | visual |
| 11 | [triad_3d_longrun](11%20triad_3d_longrun.md) | Tentativa sem artefatos | vazio | cronologia |
| 12 | [triad_3d_longrun_fast](12%20triad_3d_longrun_fast.md) | Exploratória 3D | completo | visual; sem 00_montagem |
| 13 | [triad_3d_longrun_compact](13%20triad_3d_longrun_compact.md) | Exploratória 3D | completo | visual |
| 14 | [triad_R5_reference_run](14%20triad_R5_reference_run.md) | Transição | vazio | preparação R5 |
| 15 | [triad_R5_reference_fast](15%20triad_R5_reference_fast.md) | Transição | vazio | preparação R5 |
| 16 | [triad_R5_reference_N40](16%20triad_R5_reference_N40.md) | Equação de referência | completo | anti-colapso full vs no-memory |
| 17 | [triad_R5_reference_N48_full](17%20triad_R5_reference_N48_full.md) | Equação de referência | completo | scores Bravais; BCC maior, não “perfeito” |
| 18 | [triad_visual_atlas](18%20triad_visual_atlas.md) | Diagnóstico visual | completo | 22 painéis; sem cancelamento local |
| 19 | [triad_bigbang_solver_run](19%20triad_bigbang_solver_run.md) | solver.py NumPy shim | falha-diagnóstica | FDT quente; mass_final=8773.747757 |
| 20 | [triad_bigbang_3d_box](20%20triad_bigbang_3d_box.md) | solver.py NumPy shim | completo | FDT frio; expansão sem teia clara |
| 21 | [triad_phase_to_density_speed](21%20triad_phase_to_density_speed.md) | solver.py | falha-diagnóstica | velocidades ~4.008763e-16 |
| 22 | [triad_phase_to_density_speed_refined](22%20triad_phase_to_density_speed_refined.md) | solver.py | completo | fronts 7.301417 / 7.557409 |
| 23 | [triad_memory_bounce_bigbang](23%20triad_memory_bounce_bigbang.md) | solver.py | completo | R_rms False; raios de massa True |
| 24 | [triad_bravais_map](24%20triad_bravais_map.md) | Pós-processamento bounce | completo | PLANAR_cross=0.221126 (maior) |
| 25 | [triad_bravais_network_map](25%20triad_bravais_network_map.md) | Pós-processamento geométrico | falha-diagnóstica | 2 nós, 1 aresta; threshold severo |
| 26 | [triad_bravais_network_map_v2](26%20triad_bravais_network_map_v2.md) | Pós-processamento geométrico | completo | t=4.4: 39 nós, 25 arestas |
| 27 | [triad_chaos_eq](27%20triad_chaos_eq.md) | solver real (triad-lang), N=32, 2026-08-20 noite | caos-eq | 12 sementes → universo; n_det 12→1238; norm 1→25585.351298 |
| 28 | [triad_atoms_3d](28%20triad_atoms_3d.md) | solver real (triad-lang), N=40 volume 3D, 2026-08-20 noite | caos-eq | 12 sementes 3D → universo no cubo; n_det 12→1007; norm 1→23.275045 |
| 29 | [triad_R5_A2](29%20triad_R5_A2.md) | spec §5 3D Strang standalone, N=96 vs 128, 2026-08-20 noite | R5-FDT | 1 átomo §9.1 A.2 → universo no cubo; peak 1.437→0.004433; PR 1.969→4035.967; R_rms 0.612→10.023 |
| 30 | [triad_dois_atomos](30%20dois_atomos_gravidade.md) | Theta_core I0, 2 gaussianas, N=64, 2026-08-21 | par / pico finito | 2 blobs só até t=0.01 (sep 6.000→6.021); t=0.02 universo (n_raw 30, R_rms 15.88); peak_max=4.770 finito; norm 1→18033 |
| 31 | [triad_nested](31%20nested_gaussians.md) | Theta_core I0, 2 gaussianas aninhadas, N=64, 2026-08-21 | ninho / pico finito | two-scale até t=0.02 (cim 7.89→6.67); t=0.03 universo (R_rms 15.91); peak_max=4.525 finito; norm 1→18022 |
| 32 | [triad_universo_atomo](32%20universo_atomo.md) | Theta_core I0, universo-átomo + par +/−, N=64, 2026-08-21 | ninho 3 / ímã-repele / pico finito | par +/− só em t=0 (sep=5.000); t=0.01 universo (n_raw 8608, R_rms 15.85); peak_max=4.599 finito; norm 1→18029 |
| 33 | [triad_ninho_pm](33%20ninho_pm.md) | Theta_core I0, ninho +/− concêntrico, N=64, 2026-08-21 | ninho sinal / oco / pico finito | oco +/− até t=0.04 (sign até 0.08, flicker t=1.0); t=0.01 universo (R_rms 15.77); peak_max=4.452 finito; norm 1→18022 |
| 34 | [triad_ninho_pm_long](34%20ninho_pm_long.md) | Theta_core I0, ninho +/− T=60, N=64, 2026-08-21 | universo preenchido / sem rebirth | depois de t=1 só universo; sem nest/par/bounce real; peak_max=4.851 em t=10.4 depois platô ~3.31; late norm 32591±72; cryst Δ=2e-6 |
| 35 | [triad_singularidade_35](35%20singularidade_finita.md) | Theta_core I0, 1 e 2 picos, N=64 T=1, 2026-08-21 | singularidade finita | 1atom peak_max=5.3739 t=0.185 n_células 1→1 t_gone=0.005 não aperta; 2atom peak_max=4.76867 t=0.705 n_células 2→1 t_gone=0.005 não aperta |
| 36 | [reexecucao_integral](36%20reexecucao_integral.md) · [TRIAD_reexecucao_integral_2026-08-21](../Fontes/TRIAD_reexecucao_integral_2026-08-21.md) | reexecução dossiê Grok, Linux/NumPy fp64, 21/08/2026 | completo | A.3 64/128/160 H_plateau; P1/P4 PARTIAL; P2/P3/P5/P6 MATCH; CHSH S=2.023±0.092; bandas INCONCLUSIVO; túnel sujo; banho PARTIAL; k*L=3π; Bravais chão |
| 37 | [triad_bolso_37](37%20bolso_no_universo.md) | universo cheio + bolso plantado, N=64 T=2, 21/08/2026 | o bolso apareceu, focou, o cubo comeu | t=0.005 universo; plantio +1.08; pico 4.52 em t=0.8; em t=1.085 já era banho de novo |
| 38 | [triad_dois_bolsos_38](38%20dois_bolsos.md) | dois bolsos +/− no cubo cheio, N=64 T=2, 21/08/2026 | os dois apareceram e apertaram, o cubo comeu | t=0.5 p+=1.60 p−=1.55; t=0.8 p+=4.51 p−=3.41; t=1 o − já foi |
| 39 | [triad_mapa_39](39%20mapa.md) | mapa ρ / y / ρ−y no cubo do 37, 21/08/2026 | a memória soube do bolso e esqueceu | cola 0.52 no plantio, 0.89 em t=0.8, 0.68 no fim |

Classes: [Registro integral](../Fontes/Registro%20integral.md). Equação: `[[Equação de referência]]`. Conceitos: [Anti-colapso](../Conceitos/Anti-colapso.md) · [Bounce](../Conceitos/Bounce.md) · [Rede Bravais](../Conceitos/Rede%20Bravais.md) · [Phase-to-density](../Conceitos/Phase-to-density.md) · [Observador e campo C](../Conceitos/Observador%20e%20campo%20C.md) · [FDT](../Conceitos/FDT.md) · [Memória](../Conceitos/Mem%C3%B3ria.md) · [Leitura operacional](../Conceitos/Leitura%20operacional.md).

Voltar: `[[TRIAD]]`
