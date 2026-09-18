---
tags: [triad, simulação, moc]
aliases: [índice, runs, cronologia]
---

# Índice de runs

Antologia com o texto integral de 01–36 + Q00–Q04: [[00 registro_completo]] · [[TRIAD_registro_completo_simulacoes_2026-08-21]].

36 diretórios, ordem do registro. 36 = reexecução dossiê (Linux box, 21/08/2026). 1–26 = PDF 20/08/2026; 27–28 = noite 20/08/2026, solver real (triad-lang); 29 = noite 20/08/2026, spec §5 Strang standalone; 30 = 21/08/2026, Theta_core I0 dois átomos; 31 = 21/08/2026, Theta_core I0 ninho concêntrico; 32 = 21/08/2026, Theta_core I0 universo-átomo + par +/−; 33 = 21/08/2026, Theta_core I0 ninho +/− concêntrico; 34 = 21/08/2026, mesma IC do 33, T=60. 35 = 21/08/2026, Theta_core I0 singularidade finita (T=1, 1 e 2 pontos). Título da nota = id do diretório. Falhas e vazios entram.

| # | run | classe | status | resultado (PDF) |
|---|---|---|---|---|
| 1 | [[01 triad_sim|triad_sim]] | Exploratória / pré-referência | completo | visual 2D, duas gaussianas + termo relacional; sem CSV |
| 2 | [[02 triad_nls_fdt|triad_nls_fdt]] | Exploratória / pré-referência | completo | primeiro NLS+memória+FDT; visual |
| 3 | [[03 triad_nls_fdt_v2|triad_nls_fdt_v2]] | Exploratória / pré-referência | completo | v2 + trajetórias de picos; visual |
| 4 | [[04 triad_atoms_gaussians|triad_atoms_gaussians]] | Exploratória / pré-referência | completo | átomos gaussianos; visual |
| 5 | [[05 triad_atoms_individual_fields|triad_atoms_individual_fields]] | Exploratória / pré-referência | completo | identidades gaussianas separadas; visual |
| 6 | [[06 triad_limit_test|triad_limit_test]] | Tentativa sem artefatos | vazio | cronologia |
| 7 | [[07 triad_limit_test_fast|triad_limit_test_fast]] | Exploratória quantitativa | completo | N={2,4,8,12} r={4,6,8}; δR>0 só N=2,r=4 |
| 8 | [[08 triad_observer_observed_consciousness|triad_observer_observed_consciousness]] | Exploratória | completo | mean_abs_C 0 vs 0.140886; R quase idêntico |
| 9 | [[09 triad_field_consciousness_test|triad_field_consciousness_test]] | Exploratória | completo | bounce_amplitude=0; C_memory_corr=−0.385509 |
| 10 | [[10 triad_3d_anticollapse_test|triad_3d_anticollapse_test]] | Exploratória 3D / pré-ref | completo | visual |
| 11 | [[11 triad_3d_longrun|triad_3d_longrun]] | Tentativa sem artefatos | vazio | cronologia |
| 12 | [[12 triad_3d_longrun_fast|triad_3d_longrun_fast]] | Exploratória 3D | completo | visual; sem 00_montagem |
| 13 | [[13 triad_3d_longrun_compact|triad_3d_longrun_compact]] | Exploratória 3D | completo | visual |
| 14 | [[14 triad_R5_reference_run|triad_R5_reference_run]] | Transição | vazio | preparação R5 |
| 15 | [[15 triad_R5_reference_fast|triad_R5_reference_fast]] | Transição | vazio | preparação R5 |
| 16 | [[16 triad_R5_reference_N40|triad_R5_reference_N40]] | Equação de referência | completo | anti-colapso full vs no-memory |
| 17 | [[17 triad_R5_reference_N48_full|triad_R5_reference_N48_full]] | Equação de referência | completo | scores Bravais; BCC maior, não “perfeito” |
| 18 | [[18 triad_visual_atlas|triad_visual_atlas]] | Diagnóstico visual | completo | 22 painéis; sem cancelamento local |
| 19 | [[19 triad_bigbang_solver_run|triad_bigbang_solver_run]] | solver.py NumPy shim | falha-diagnóstica | FDT quente; mass_final=8773.747757 |
| 20 | [[20 triad_bigbang_3d_box|triad_bigbang_3d_box]] | solver.py NumPy shim | completo | FDT frio; expansão sem teia clara |
| 21 | [[21 triad_phase_to_density_speed|triad_phase_to_density_speed]] | solver.py | falha-diagnóstica | velocidades ~4.008763e-16 |
| 22 | [[22 triad_phase_to_density_speed_refined|triad_phase_to_density_speed_refined]] | solver.py | completo | fronts 7.301417 / 7.557409 |
| 23 | [[23 triad_memory_bounce_bigbang|triad_memory_bounce_bigbang]] | solver.py | completo | R_rms False; raios de massa True |
| 24 | [[24 triad_bravais_map|triad_bravais_map]] | Pós-processamento bounce | completo | PLANAR_cross=0.221126 (maior) |
| 25 | [[25 triad_bravais_network_map|triad_bravais_network_map]] | Pós-processamento geométrico | falha-diagnóstica | 2 nós, 1 aresta; threshold severo |
| 26 | [[26 triad_bravais_network_map_v2|triad_bravais_network_map_v2]] | Pós-processamento geométrico | completo | t=4.4: 39 nós, 25 arestas |
| 27 | [[27 triad_chaos_eq|triad_chaos_eq]] | solver real (triad-lang), N=32, 2026-08-20 noite | caos-eq | 12 sementes → universo; n_det 12→1238; norm 1→25585.351298 |
| 28 | [[28 triad_atoms_3d|triad_atoms_3d]] | solver real (triad-lang), N=40 volume 3D, 2026-08-20 noite | caos-eq | 12 sementes 3D → universo no cubo; n_det 12→1007; norm 1→23.275045 |
| 29 | [[29 triad_R5_A2|triad_R5_A2]] | spec §5 3D Strang standalone, N=96 vs 128, 2026-08-20 noite | R5-FDT | 1 átomo §9.1 A.2 → universo no cubo; peak 1.437→0.004433; PR 1.969→4035.967; R_rms 0.612→10.023 |
| 30 | [[30 dois_atomos_gravidade|triad_dois_atomos]] | Theta_core I0, 2 gaussianas, N=64, 2026-08-21 | par / pico finito | 2 blobs só até t=0.01 (sep 6.000→6.021); t=0.02 universo (n_raw 30, R_rms 15.88); peak_max=4.770 finito; norm 1→18033 |
| 31 | [[31 nested_gaussians|triad_nested]] | Theta_core I0, 2 gaussianas aninhadas, N=64, 2026-08-21 | ninho / pico finito | two-scale até t=0.02 (cim 7.89→6.67); t=0.03 universo (R_rms 15.91); peak_max=4.525 finito; norm 1→18022 |
| 32 | [[32 universo_atomo|triad_universo_atomo]] | Theta_core I0, universo-átomo + par +/−, N=64, 2026-08-21 | ninho 3 / ímã-repele / pico finito | par +/− só em t=0 (sep=5.000); t=0.01 universo (n_raw 8608, R_rms 15.85); peak_max=4.599 finito; norm 1→18029 |
| 33 | [[33 ninho_pm|triad_ninho_pm]] | Theta_core I0, ninho +/− concêntrico, N=64, 2026-08-21 | ninho sinal / oco / pico finito | oco +/− até t=0.04 (sign até 0.08, flicker t=1.0); t=0.01 universo (R_rms 15.77); peak_max=4.452 finito; norm 1→18022 |
| 34 | [[34 ninho_pm_long|triad_ninho_pm_long]] | Theta_core I0, ninho +/− T=60, N=64, 2026-08-21 | universo preenchido / sem rebirth | depois de t=1 só universo; sem nest/par/bounce real; peak_max=4.851 em t=10.4 depois platô ~3.31; late norm 32591±72; cryst Δ=2e-6 |
| 35 | [[35 singularidade_finita|triad_singularidade_35]] | Theta_core I0, 1 e 2 picos, N=64 T=1, 2026-08-21 | singularidade finita | 1atom peak_max=5.3739 t=0.185 n_células 1→1 t_gone=0.005 não aperta; 2atom peak_max=4.76867 t=0.705 n_células 2→1 t_gone=0.005 não aperta |
| 36 | [[36 reexecucao_integral|reexecucao_integral]] · [[TRIAD_reexecucao_integral_2026-08-21]] | reexecução dossiê Grok, Linux/NumPy fp64, 21/08/2026 | completo | A.3 64/128/160 H_plateau; P1/P4 PARTIAL; P2/P3/P5/P6 MATCH; CHSH S=2.023±0.092; bandas INCONCLUSIVO; túnel sujo; banho PARTIAL; k*L=3π; Bravais chão |
| 37 | [[37 bolso_no_universo|triad_bolso_37]] | universo cheio + bolso plantado, N=64 T=2, 21/08/2026 | o bolso apareceu, focou, o cubo comeu | t=0.005 universo; plantio +1.08; pico 4.52 em t=0.8; em t=1.085 já era banho de novo |
| 38 | [[38 dois_bolsos|triad_dois_bolsos_38]] | dois bolsos +/− no cubo cheio, N=64 T=2, 21/08/2026 | os dois apareceram e apertaram, o cubo comeu | t=0.5 p+=1.60 p−=1.55; t=0.8 p+=4.51 p−=3.41; t=1 o − já foi |
| 39 | [[39 mapa|triad_mapa_39]] | mapa ρ / y / ρ−y no cubo do 37, 21/08/2026 | a memória soube do bolso e esqueceu | cola 0.52 no plantio, 0.89 em t=0.8, 0.68 no fim |

Classes: [[Registro integral]]. Equação: [[Equação de referência]]. Conceitos: [[Anti-colapso]] · [[Bounce]] · [[Rede Bravais]] · [[Phase-to-density]] · [[Observador e campo C]] · [[FDT]] · [[Memória]] · [[Leitura operacional]].

Voltar: [[TRIAD]]
