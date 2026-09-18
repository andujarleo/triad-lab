---
tags: [triad, simulação, solver, I0]
aliases: [triad_dois_atomos, dois_atomos_gravidade]
classe: spec §5 3D Strang (standalone), Theta_core
diretório: triad_dois_atomos
status: I0 / environment
run: 30
data: 2026-08-21
---

# dois_atomos_gravidade

Equação TRIAD **completa**, Theta_core congelado (Q00 / [[TRIAD_QM_CANONICAL_V1]]). **I0 / environment**, não scan. 1 gaussiana = 1 átomo. Duas sementes, separação 6 ao longo de x. Leitura: par (queda?) e pico finito (singularidade que não vai a infinito). Volume preenchido = universo, não ruído. **Não** é teste de interferência. Sem isolar memória/FDT. Sem mudar Theta_core para o par atrair. [[Leitura operacional]] · [[Anti-colapso]] · [[Universo como simulação]]

Solver: Strang 3D standalone (mesmo passo de [[Fontes/run_q01a.py]] / [[29 triad_R5_A2]]). fp64, numpy. $V_{\mathrm{ext}}=0$, $y_j(0)=0$, caixa periódica $[-L/2,L/2)^3$.

## IC — 2 átomos

Duas gaussianas iguais, $s=1.0$, fases 0, centros $(-3,0,0)$ e $(+3,0,0)$, depois $\int\rho=1$. Pico IC=0.089782, PR=31.506820, R_rms=3.240199, pair_sep=6.000, n_det=2, n_raw=2.

![[Artefatos/triad_dois_atomos/01_ic_isosurface.png]]

![[Artefatos/triad_dois_atomos/04a_midplane_t0.png]]

## Parâmetros (Theta_core, intocado)

$\Lambda=-10$, $\alpha=0.15$, $\sigma=1.5$, $\Gamma=0.05$, $\nu=(10, 0.5, 0.05)$, $\lambda=(3, 1, 0.3)$, `fdt_couple=True`, **kT=1.0**. $L=32$, $N=64$, $dt=0.0025$, $T=8$, seed=0. $f_{\mathrm{FDT}}=0.0125$, noise_amp $=0.015811388300841896=\sqrt{2\Gamma\,kT\,dt}$. Memória Euler ($\max\nu\cdot dt=0.025$).

Não substitui [[27 triad_chaos_eq]] · [[28 triad_atoms_3d]] · [[29 triad_R5_A2]] · Q01a.

## Resultado

Wall: **55.336 s** (12:16:08–12:17:03 BRT, 21/08/2026). 3200 passos, 117 amostras (cedo $\Delta t=0.01$ até $t=0.4$; depois $\Delta t=0.1$).

| | t=0 | t=0.01 (último par) | t=0.02 | t=0.1 | mid t=4 | final t=8 |
|---|---|---|---|---|---|---|
| n_det (par NMS) | 2 | 2 | 29 | — | — | — |
| n_raw máx. local | 2 | 2 | 30 | 3603 | (volume) | 8349 |
| pair_sep | 6.000000 | 6.020797 | — | — | — | — |
| two_blobs | sim | sim | não | não | não | não |
| norm | 1.0 | 33.721971 | 66.256441 | 327.167518 | 10793.88 | 18033.373159 |
| peak | 0.089782 | 0.100767 | 0.090554 | 0.201959 | 3.102430 | 4.187885 |
| PR | 31.506820 | 11004.413 | 14616.525 | 16320.800 | 17833.27 | 19579.930525 |
| R_rms | 3.240199 | 15.758815 | 15.877491 | 15.983788 | 16.01433 | 15.955965 |

Pico de densidade máximo=**4.770362** em t=6.8. Vmem_peak máximo=7.556006 em t=5.7; Vmem_peak final=6.829866. Janela late ($t\ge 6.4$): peak $3.886935\pm 0.343$; PR $19197.382\pm 201$; R_rms $15.982180\pm 0.022$; norm $16771.131\pm 783$. Sem NaN, sem blowup. células½ final=1706 (não 1–2 células).

Os dois átomos **permanecem 2 só até t=0.01**. Em t=0.02 o detector já conta 29–30 máximos e R_rms já é $\approx L/2$. Em t=0.1 n_raw=3603, norm=327 — a mesma família de preenchimento de Q01a / [[27 triad_chaos_eq]] com este banho. **Com kT=1 as duas sementes viram universo antes de um par-órbita poder ser lido.** kT não foi retocado. Isso é o resultado.

pair_sep enquanto ainda havia 2 blobs: $6.000\to 6.021$ ($\Delta=+0.021$ em $\Delta t=0.01$; um passo de grade $dx=0.5$). Não é queda. Depois pair_sep é indefinido (par perdido).

![[Artefatos/triad_dois_atomos/01b_isosurface_early.png]]

![[Artefatos/triad_dois_atomos/02_isosurface_mid.png]]

![[Artefatos/triad_dois_atomos/03_isosurface_late.png]]

![[Artefatos/triad_dois_atomos/04_midplane_xy.png]]

![[Artefatos/triad_dois_atomos/05_observables.png]]

![[Artefatos/triad_dois_atomos/07_early_zoom.png]]

![[Artefatos/triad_dois_atomos/00_montagem.png]]

## O que os números sustentam

**(a) distância do par — INCONCLUSIVE.** Dois blobs só em $t\in\{0, 0.01\}$. Não houve tempo para ler atração. pair_sep 6.000→6.021 e some. Com este banho o par vira universo em $t\ll 1$. Não é evidência de gravidade emergente e não é evidência contra: o par não durou.

**(b) pico finito — SUPPORTED (neste run).** peak ρ máximo=4.770362, final=4.187885, sempre finito, sem blowup. Anti-colapso operacional: a singularidade **não** foi a infinito. Pico late ~3.89 em milhares de células, não artefato de 1–2 células.

Nunca “provou gravidade”. Theta_core intocado.

## CSVs

- [[Artefatos/triad_dois_atomos/summary.csv]]
- [[Artefatos/triad_dois_atomos/metrics.csv]]
- [[Artefatos/triad_dois_atomos/summary.json]]

## Arquivos

`00_montagem.png` · `01_ic_isosurface.png` · `01b_isosurface_early.png` · `02_isosurface_mid.png` · `03_isosurface_late.png` · `04_midplane_xy.png` + midplanes individuais · `05_observables.png` · `06_n_det.png` · `07_early_zoom.png` · metrics.csv · summary.csv · summary.json · `rho_{ic,early,mid,late}.npy`

Script: [[Fontes/run_dois_atomos.py]]

→ [[Índice de runs]] · [[TRIAD]] · [[Leitura operacional]]
