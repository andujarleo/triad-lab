> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Conceitos/Bounce.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, conceito]
aliases: [bounce de memória, contração-expansão]
```


# Bounce

Nenhum termo explícito de bounce na equação. O run [23 triad_memory_bounce_bigbang](../Simula%C3%A7%C3%B5es/23%20triad_memory_bounce_bigbang.md) parte de gaussiana larga + chirp quadrático radial para dentro e pergunta se a [Memória](Mem%C3%B3ria.md) reexpande o núcleo.

Parâmetros do run (PDF): $\Lambda=-10$, $\nu=(10,0.5,0.05)$, $\lambda=(3,1,0.3)$, 40³, T=12, L=32, dt=0.0025, `initial_sigma=3.2`, `inward_chirp=0.22`.

## Dois diagnósticos, ambos preservados

1. **R_rms** — mínimo em t=0 (`R_min=R_initial=3.919184`); `bounced=False`. O PDF atribui a densidade FDT fraca no volume distante, que infla R_rms.
2. **Raios de massa** (mesma trajetória, sem reintegrar):

| | inicial | mín | t_mín | final | flag |
|---|---|---|---|---|---|
| r50 | 3.487119 | 1.385641 | 3.7 | 9.863062 | True |
| r80 | 4.866210 | 2.884441 | 3.1 | 16.511814 | True |
| r90 | 5.656854 | 5.059644 | 1.3 | 19.0662 | True |

Pico de densidade t=4.1; pico de memória t=4.2; delay=0.1.

Norma 1→1.491662. `R_rms` final=12.272371. peak_density max=0.149575.

Campo C (exploratório, outro solver): `bounce_amplitude=0` em baseline e continuous_C. [09 triad_field_consciousness_test](../Simula%C3%A7%C3%B5es/09%20triad_field_consciousness_test.md)

Pós-processamento: [24 triad_bravais_map](../Simula%C3%A7%C3%B5es/24%20triad_bravais_map.md), [25 triad_bravais_network_map](../Simula%C3%A7%C3%B5es/25%20triad_bravais_network_map.md), [26 triad_bravais_network_map_v2](../Simula%C3%A7%C3%B5es/26%20triad_bravais_network_map_v2.md).


## Run full 27 — caos de átomos → eq (não é ablação)

[27 triad_chaos_eq](../Simula%C3%A7%C3%B5es/27%20triad_chaos_eq.md): equação completa, V_ext=None, N=32, 12 gaussianas (σ=1.2, min_sep=4.8, seed=0). Sem controle sem-memória. Sem isolamento de termos. Não substitui #23.

t=0: n_det=12, ⟨NN⟩=8.857611. t=0.1: n_det=1147, norm=325.919474. Final t=15: norm=25585.351298, n_det=1238, R_rms=16.023042, PR=28851.932841. Raios já nascem na escala da caixa e ficam lá. Os 12 átomos não persistem — FDT default (`fdt_couple=True`, dx=1) inunda a grade, família de [19 triad_bigbang_solver_run](../Simula%C3%A7%C3%B5es/19%20triad_bigbang_solver_run.md).

Não é prova de bounce nem de rede.

Voltar: [Memória](Mem%C3%B3ria.md) · [Anti-colapso](Anti-colapso.md)
