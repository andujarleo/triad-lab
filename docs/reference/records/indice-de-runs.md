---
tags: [triad, simulação, moc]
aliases: [índice, runs, cronologia]
---

# Índice de runs

Antologia com o texto integral de 01–36 + Q00–Q04: [00 registro_completo](00-registro-completo.md) · [TRIAD_registro_completo_simulacoes_2026-08-21](00-registro-completo.md).

36 diretórios, ordem do registro. 36 = reexecução dossiê (Linux box, 21/08/2026). 1–26 = PDF 20/08/2026; 27–28 = noite 20/08/2026, solver real (triad-lang); 29 = noite 20/08/2026, spec §5 Strang standalone; 30 = 21/08/2026, Theta_core I0 dois átomos; 31 = 21/08/2026, Theta_core I0 ninho concêntrico; 32 = 21/08/2026, Theta_core I0 universo-átomo + par +/−; 33 = 21/08/2026, Theta_core I0 ninho +/− concêntrico; 34 = 21/08/2026, mesma IC do 33, T=60. 35 = 21/08/2026, Theta_core I0 singularidade finita (T=1, 1 e 2 pontos). Título da nota = id do diretório. Falhas e vazios entram.

| # | run | classe | status | resultado (PDF) |
|---|---|---|---|---|
| 1 | [triad_sim](../../../experiments/relations/early-field-relations/notes/original-record.md) | Exploratória / pré-referência | completo | visual 2D, duas gaussianas + termo relacional; sem CSV |
| 2 | [triad_nls_fdt](../../../experiments/memory/memory-and-thermal-noise/notes/original-record.md) | Exploratória / pré-referência | completo | primeiro NLS+memória+FDT; visual |
| 3 | [triad_nls_fdt_v2](../../../experiments/memory/tracking-density-peaks/notes/original-record.md) | Exploratória / pré-referência | completo | v2 + trajetórias de picos; visual |
| 4 | [triad_atoms_gaussians](../../../experiments/structures/gaussian-atoms-in-one-field/notes/original-record.md) | Exploratória / pré-referência | completo | átomos gaussianos; visual |
| 5 | [triad_atoms_individual_fields](../../../experiments/structures/individual-fields/notes/original-record.md) | Exploratória / pré-referência | completo | identidades gaussianas separadas; visual |
| 6 | [triad_limit_test](../../../experiments/signals/limit-test-attempt/notes/original-record.md) | Tentativa sem artefatos | vazio | cronologia |
| 7 | [triad_limit_test_fast](../../../experiments/signals/fast-limit-sweep/notes/original-record.md) | Exploratória quantitativa | completo | N={2,4,8,12} r={4,6,8}; δR>0 só N=2,r=4 |
| 8 | [triad_observer_observed_consciousness](../../../experiments/relations/observer-and-observed/notes/original-record.md) | Exploratória | completo | mean_abs_C 0 vs 0.140886; R quase idêntico |
| 9 | [triad_field_consciousness_test](../../../experiments/relations/continuous-relational-field/notes/original-record.md) | Exploratória | completo | bounce_amplitude=0; C_memory_corr=−0.385509 |
| 10 | [triad_3d_anticollapse_test](../../../experiments/memory/3d-anti-collapse-exploration/notes/original-record.md) | Exploratória 3D / pré-ref | completo | visual |
| 11 | [triad_3d_longrun](../../../experiments/structures/long-run-attempt/notes/original-record.md) | Tentativa sem artefatos | vazio | cronologia |
| 12 | [triad_3d_longrun_fast](../../../experiments/structures/fast-3d-long-run/notes/original-record.md) | Exploratória 3D | completo | visual; sem 00_montagem |
| 13 | [triad_3d_longrun_compact](../../../experiments/structures/compact-3d-long-run/notes/original-record.md) | Exploratória 3D | completo | visual |
| 14 | [triad_R5_reference_run](../../../experiments/memory/memory-reference-attempt/notes/original-record.md) | Transição | vazio | preparação R5 |
| 15 | [triad_R5_reference_fast](../../../experiments/memory/accelerated-memory-reference/notes/original-record.md) | Transição | vazio | preparação R5 |
| 16 | [triad_R5_reference_N40](../../../experiments/memory/memory-grid-40/notes/original-record.md) | Equação de referência | completo | anti-colapso full vs no-memory |
| 17 | [triad_R5_reference_N48_full](../../../experiments/memory/memory-grid-48/notes/original-record.md) | Equação de referência | completo | scores Bravais; BCC maior, não “perfeito” |
| 18 | [triad_visual_atlas](../../../experiments/geometry/visual-atlas/notes/original-record.md) | Diagnóstico visual | completo | 22 painéis; sem cancelamento local |
| 19 | [triad_bigbang_solver_run](../../../experiments/signals/hot-bath-diagnostic-failure/notes/original-record.md) | solver.py NumPy shim | falha-diagnóstica | FDT quente; mass_final=8773.747757 |
| 20 | [triad_bigbang_3d_box](../../../experiments/signals/3d-cold-bath-box/notes/original-record.md) | solver.py NumPy shim | completo | FDT frio; expansão sem teia clara |
| 21 | [triad_phase_to_density_speed](../../../experiments/signals/first-phase-to-density-diagnostic/notes/original-record.md) | solver.py | falha-diagnóstica | velocidades ~4.008763e-16 |
| 22 | [triad_phase_to_density_speed_refined](../../../experiments/signals/refined-phase-to-density-diagnostic/notes/original-record.md) | solver.py | completo | fronts 7.301417 / 7.557409 |
| 23 | [triad_memory_bounce_bigbang](../../../experiments/memory/memory-and-bounce/notes/original-record.md) | solver.py | completo | R_rms False; raios de massa True |
| 24 | [triad_bravais_map](../../../experiments/geometry/bravais-template-map/notes/original-record.md) | Pós-processamento bounce | completo | PLANAR_cross=0.221126 (maior) |
| 25 | [triad_bravais_network_map](../../../experiments/geometry/first-geometric-network/notes/original-record.md) | Pós-processamento geométrico | falha-diagnóstica | 2 nós, 1 aresta; threshold severo |
| 26 | [triad_bravais_network_map_v2](../../../experiments/geometry/refined-geometric-network/notes/original-record.md) | Pós-processamento geométrico | completo | t=4.4: 39 nós, 25 arestas |
| 27 | [triad_chaos_eq](../../../experiments/structures/twelve-atoms-full-field/notes/original-record.md) | solver real (triad-lang), N=32, 2026-08-20 noite | caos-eq | 12 sementes → universo; n_det 12→1238; norm 1→25585.351298 |
| 28 | [triad_atoms_3d](../../../experiments/structures/3d-atom-trajectories/notes/original-record.md) | solver real (triad-lang), N=40 volume 3D, 2026-08-20 noite | caos-eq | 12 sementes 3D → universo no cubo; n_det 12→1007; norm 1→23.275045 |
| 29 | [triad_R5_A2](../../../experiments/memory/memory-small-amplitude/notes/original-record.md) | spec §5 3D Strang standalone, N=96 vs 128, 2026-08-20 noite | R5-FDT | 1 átomo §9.1 A.2 → universo no cubo; peak 1.437→0.004433; PR 1.969→4035.967; R_rms 0.612→10.023 |
| 30 | [triad_dois_atomos](../../../experiments/structures/two-atoms/notes/original-record.md) | Theta_core I0, 2 gaussianas, N=64, 2026-08-21 | par / pico finito | 2 blobs só até t=0.01 (sep 6.000→6.021); t=0.02 universo (n_raw 30, R_rms 15.88); peak_max=4.770 finito; norm 1→18033 |
| 31 | [triad_nested](../../../experiments/structures/nested-positive-gaussians/notes/original-record.md) | Theta_core I0, 2 gaussianas aninhadas, N=64, 2026-08-21 | ninho / pico finito | two-scale até t=0.02 (cim 7.89→6.67); t=0.03 universo (R_rms 15.91); peak_max=4.525 finito; norm 1→18022 |
| 32 | [triad_universo_atomo](../../../experiments/structures/atom-inside-a-larger-gaussian/notes/original-record.md) | Theta_core I0, universo-átomo + par +/−, N=64, 2026-08-21 | ninho 3 / ímã-repele / pico finito | par +/− só em t=0 (sep=5.000); t=0.01 universo (n_raw 8608, R_rms 15.85); peak_max=4.599 finito; norm 1→18029 |
| 33 | [triad_ninho_pm](../../../experiments/structures/concentric-positive-negative-nest/notes/original-record.md) | Theta_core I0, ninho +/− concêntrico, N=64, 2026-08-21 | ninho sinal / oco / pico finito | oco +/− até t=0.04 (sign até 0.08, flicker t=1.0); t=0.01 universo (R_rms 15.77); peak_max=4.452 finito; norm 1→18022 |
| 34 | [triad_ninho_pm_long](../../../experiments/structures/long-nest-trajectory/notes/original-record.md) | Theta_core I0, ninho +/− T=60, N=64, 2026-08-21 | universo preenchido / sem rebirth | depois de t=1 só universo; sem nest/par/bounce real; peak_max=4.851 em t=10.4 depois platô ~3.31; late norm 32591±72; cryst Δ=2e-6 |
| 35 | [triad_singularidade_35](../../../experiments/structures/finite-peak-early-window/notes/original-record.md) | Theta_core I0, 1 e 2 picos, N=64 T=1, 2026-08-21 | singularidade finita | 1atom peak_max=5.3739 t=0.185 n_células 1→1 t_gone=0.005 não aperta; 2atom peak_max=4.76867 t=0.705 n_células 2→1 t_gone=0.005 não aperta |
| 36 | [reexecucao_integral](../../../experiments/validation/reproduction-dossier/notes/original-record.md) · [TRIAD_reexecucao_integral_2026-08-21](../../../experiments/validation/reproduction-dossier/notes/original-record.md) | reexecução dossiê Grok, Linux/NumPy fp64, 21/08/2026 | completo | A.3 64/128/160 H_plateau; P1/P4 PARTIAL; P2/P3/P5/P6 MATCH; CHSH S=2.023±0.092; bandas INCONCLUSIVO; túnel sujo; banho PARTIAL; k*L=3π; Bravais chão |
| 37 | [triad_bolso_37](../../../experiments/structures/a-pocket-in-the-field/notes/original-record.md) | universo cheio + bolso plantado, N=64 T=2, 21/08/2026 | o bolso apareceu, focou, o cubo comeu | t=0.005 universo; plantio +1.08; pico 4.52 em t=0.8; em t=1.085 já era banho de novo |
| 38 | [triad_dois_bolsos_38](../../../experiments/structures/two-pockets/notes/original-record.md) | dois bolsos +/− no cubo cheio, N=64 T=2, 21/08/2026 | os dois apareceram e apertaram, o cubo comeu | t=0.5 p+=1.60 p−=1.55; t=0.8 p+=4.51 p−=3.41; t=1 o − já foi |
| 39 | [triad_mapa_39](../../../experiments/structures/density-memory-maps/notes/original-record.md) | mapa ρ / y / ρ−y no cubo do 37, 21/08/2026 | a memória soube do bolso e esqueceu | cola 0.52 no plantio, 0.89 em t=0.8, 0.68 no fim |

Classes: [Registro integral](registro-integral.md). Equação: `[[Equação de referência]]`. Conceitos: [Anti-colapso](../concepts/anti-collapse.md) · [Bounce](../concepts/bounce.md) · [Rede Bravais](../concepts/bravais-lattice.md) · [Phase-to-density](../concepts/phase-to-density.md) · [Observador e campo C](../concepts/observer-and-c-field.md) · [FDT](../concepts/fdt.md) · [Memória](../concepts/memory.md) · [Leitura operacional](../concepts/operational-readings.md).

Voltar: `[[TRIAD]]`
