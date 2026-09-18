---
tags: [triad, simulação, solver, I0]
aliases: [triad_universo_atomo, universo_atomo]
classe: spec §5 3D Strang (standalone), Theta_core
diretório: triad_universo_atomo
status: I0 / environment
run: 32
data: 2026-08-21
---

# universo_atomo

Equação TRIAD **completa**, Theta_core congelado (Q00 / [[TRIAD_QM_CANONICAL_V1]]). **I0 / environment**, não scan. 1 gaussiana = 1 átomo. **OUTER larga = o universo** (um átomo gigante). **Dentro:** observador e observado, fases 0 e π (+ e −). Leitura: **anti-colapso / ímã-repele** (memória mesmo-polo, singularidade finita) — **não** MQ, **não** colapso-como-gravidade-caindo. Volume preenchido = universo, não ruído. Sem isolar memória/FDT. Sem mudar Theta_core. Sem retocar kT. [[Leitura operacional]] · [[Anti-colapso]] · [[Universo como simulação]]

Solver: Strang 3D standalone (mesmo passo de [[Fontes/run_q01a.py]] / [[30 dois_atomos_gravidade]] / [[31 nested_gaussians]]). fp64, numpy. $V_{\mathrm{ext}}=0$, $y_j(0)=0$, caixa periódica $[-L/2,L/2)^3$.

## IC — ninho 3 escalas (I0, decidido uma vez)

$\Psi = G_{\mathrm{env}}(s=8.0)_{(0,0,0)}^{\mathrm{fase}\,0} + G_{\mathrm{obs}}(s=1.0)_{(-2.5,0,0)}^{\mathrm{fase}\,0} + G_{\mathrm{obd}}(s=1.0)_{(+2.5,0,0)}^{\mathrm{fase}\,\pi\,(=\,\times-1)}$, depois $\int|\Psi|^2\,dV=1$. Pico IC=0.001351, PR=7436.783130, R_rms=9.574362, r50=8.616844, r90=13.829317, pair_sep=5.000, n_inner=2, n_pos=1, n_neg=1, n_det_ρ=1 (só o + é máximo de $|Ψ|^2$; o − é um poço de Re). Re+ = 0.036751, Re− = −0.000897.

![[Artefatos/triad_universo_atomo/01_ic_isosurface.png]]

![[Artefatos/triad_universo_atomo/01e_ic_re_isosurface.png]]

![[Artefatos/triad_universo_atomo/04g_midplane_re_t0.png]]

![[Artefatos/triad_universo_atomo/09b_linecut_re_t0.png]]

![[Artefatos/triad_universo_atomo/06_radial_profiles.png]]

O gráfico de dinheiro é Re(Ψ) no midplane (vermelho + / azul −): envelope largo positivo, blob interno + em $x=-2.5$, dip interno − em $x=+2.5$. O corte Re$(x,0,0)$ mostra o mesmo. $|Ψ|^2$ sozinho esconde o sinal.

## Parâmetros (Theta_core, intocado)

$\Lambda=-10$, $\alpha=0.15$, $\sigma=1.5$, $\Gamma=0.05$, $\nu=(10, 0.5, 0.05)$, $\lambda=(3, 1, 0.3)$, `fdt_couple=True`, **kT=1.0**. $L=32$, $N=64$, $dt=0.0025$, $T=8$, seed=0. $f_{\mathrm{FDT}}=0.0125$, noise_amp $=0.015811388300841896=\sqrt{2\Gamma\,kT\,dt}$. Memória Euler ($\max\nu\cdot dt=0.025$).

Não substitui [[27 triad_chaos_eq]] · [[28 triad_atoms_3d]] · [[29 triad_R5_A2]] · [[30 dois_atomos_gravidade]] · [[31 nested_gaussians]] · Q01a.

## Resultado

Wall: **116.629 s** (12:37:07–12:39:03 BRT, 21/08/2026). 3200 passos, 117 amostras (cedo $\Delta t=0.01$ até $t=0.4$; depois $\Delta t=0.1$).

| | t=0 IC | t=0.01 (perdido) | t=0.02 | t=0.1 | mid t=4 | final t=8 |
|---|---|---|---|---|---|---|
| n_inner (+/− Re) | 2 | 0 | 0 | 0 | 0 | 0 |
| n_pos / n_neg | 1 / 1 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 | 0 / 0 |
| n_raw_ρ | 1 | 8608 | 8636 | 8736 | 9286 | 8358 |
| pair_sep | 5.000000 | — | — | — | — | — |
| two_inner / nest3 | sim | não | não | não | não | não |
| norm | 1.0 | 33.683190 | 66.227634 | 327.040428 | 10793.988 | 18029.079193 |
| peak | 0.001351 | 0.013039 | 0.025565 | 0.124410 | 3.147238 | 3.888902 |
| PR | 7436.783 | 16426.197 | 16382.236 | 16427.905 | 17836.815 | 19568.776 |
| R_rms | 9.574362 | 15.845353 | 15.920024 | 15.994502 | 16.014308 | 15.960909 |

Pico de densidade máximo=**4.598659** em t=7.7. Vmem_peak máximo=7.536641 em t=7.7; Vmem_peak final=6.593055. Janela late ($t\ge 6.4$): peak $3.939050\pm 0.274$; PR $19189.118\pm 193$; R_rms $15.985992\pm 0.019$; norm $16770.970\pm 785$. Sem NaN, sem blowup. células½ final=2830 (não 1–2 células).

O par +/− **existe só em t=0**. Em t=0.01 o detector já conta milhares de extremos (n_raw_ρ=8608, n_raw_pos=9741, n_raw_neg=9250) e R_rms já é $\approx L/2$. Em t=0.02 n_raw_ρ=8636, norm=66.2 — a mesma família de preenchimento de [[30 dois_atomos_gravidade]] / [[31 nested_gaussians]] com este banho. **Com kT=1 o ninho 3 escalas dissolve em $t=0.01$; o volume preenchido continua o universo.** kT não foi retocado. Isso é o resultado.

pair_sep enquanto n_inner=2: só o ponto t=0, sep=5.000. $\Delta$sep $=0$ (um único recorde — não há segundo instante para medir afastamento). Depois pair_sep é indefinido (par perdido). Os dois internos **não** tiveram tempo de se afastar nem de se aproximar.

![[Artefatos/triad_universo_atomo/01d_isosurface_t001.png]]

![[Artefatos/triad_universo_atomo/01c_isosurface_t002.png]]

![[Artefatos/triad_universo_atomo/01b_isosurface_early.png]]

![[Artefatos/triad_universo_atomo/02_isosurface_mid.png]]

![[Artefatos/triad_universo_atomo/03_isosurface_late.png]]

![[Artefatos/triad_universo_atomo/04r_midplane_re.png]]

![[Artefatos/triad_universo_atomo/04_midplane_xy.png]]

![[Artefatos/triad_universo_atomo/05_observables.png]]

![[Artefatos/triad_universo_atomo/07_early_zoom.png]]

![[Artefatos/triad_universo_atomo/08_nest3.png]]

![[Artefatos/triad_universo_atomo/09_linecut_re.png]]

![[Artefatos/triad_universo_atomo/00_montagem.png]]

## O que os números sustentam

**(a) par +/− / ímã-repele — INCONCLUSIVE.** n_inner=2 só em $t=0$. Em t=0.01 o par já morreu. Não houve tempo para ler repulsão. pair_sep=5.000 e some ($\Delta$sep indefinido / 0). Com este banho o ninho vira universo em $t\ll 1$. Não é evidência a favor nem contra: o par não durou.

**(b) ninho 3 escalas — INCONCLUSIVE.** nest3 só em t=0. Envelope $s=8$ + observador + observado visíveis na IC (Re midplane e corte). Depois o banho come as sementes internas. O cubo preenchido **é o universo**, não ruído.

**(c) pico finito — SUPPORTED (neste run).** peak ρ máximo=4.598659, final=3.888902, sempre finito, sem blowup. Anti-colapso operacional: a singularidade **não** foi a infinito. Pico late ~3.94 em 2830 células, não artefato de 1–2 células.

Nunca “provou gravidade”. Nunca “provou MQ”. Theta_core intocado. kT=1.0 intocado.

## CSVs

- [[Artefatos/triad_universo_atomo/summary.csv]]
- [[Artefatos/triad_universo_atomo/metrics.csv]]
- [[Artefatos/triad_universo_atomo/radial_profiles.csv]]
- [[Artefatos/triad_universo_atomo/linecut_re.csv]]
- [[Artefatos/triad_universo_atomo/summary.json]]

## Arquivos

`00_montagem.png` · `01_ic_isosurface.png` · `01e_ic_re_isosurface.png` · `01b`/`01c`/`01d` isos · `04_midplane_xy.png` + midplanes |Ψ|² e Re · `04r_midplane_re.png` · `05_observables.png` · `06_radial_profiles.png` · `06b_radial_linear.png` · `07_early_zoom.png` · `08_nest3.png` · `09_linecut_re.png` · `09b_linecut_re_t0.png` · metrics.csv · radial_profiles.csv · linecut_re.csv · summary.csv · summary.json · `rho_{ic,t001,t002,early,mid,late}.npy` · `re_{ic,t001,t002,early,mid,late}.npy`

Script: [[Fontes/run_universo_atomo.py]]

→ [[Índice de runs]] · [[TRIAD]] · [[Leitura operacional]]
