---
tags: [triad, simulação, solver, I0]
aliases: [triad_ninho_pm, ninho_pm]
classe: spec §5 3D Strang (standalone), Theta_core
diretório: triad_ninho_pm
status: I0 / environment
run: 33
data: 2026-08-21
---

# ninho_pm

Equação TRIAD **completa**, Theta_core congelado (Q00 / [[TRIAD_QM_CANONICAL_V1]]). **I0 / environment**, não scan. 1 gaussiana = 1 átomo. **Inner atom INSIDE the outer atom**, mesmo centro. Outer fase 0 (+), inner fase π (−). Leitura: **ímã / anti-colapso** (ninho de sinal, singularidade finita) — **não** lado-a-lado como [[32 universo_atomo]], **não** ninho mesmo-sinal como [[31 nested_gaussians]]. Volume preenchido = universo, não ruído. Sem isolar memória/FDT. Sem mudar Theta_core. Sem retocar kT. [[Leitura operacional]] · [[Anti-colapso]] · [[Universo como simulação]]

Solver: Strang 3D standalone (mesmo passo de [[Fontes/run_q01a.py]] / [[30 dois_atomos_gravidade]] / [[31 nested_gaussians]]). fp64, numpy. $V_{\mathrm{ext}}=0$, $y_j(0)=0$, caixa periódica $[-L/2,L/2)^3$.

## IC — ninho +/− concêntrico (I0, decidido uma vez)

$\Psi = G_{\mathrm{out}}(s=2.0)_{(0,0,0)}^{\mathrm{fase}\,0} - G_{\mathrm{in}}(s=0.5)_{(0,0,0)}^{\mathrm{fase}\,\pi\,(=\,\times-1)}$, amplitudes cruas iguais, depois $\int|\Psi|^2\,dV=1$. Pico IC=0.014580, PR=141.559784, R_rms=2.522489, r50=2.236068, r90=3.570714, contrast_im=0.952067 (núcleo oco, não brilhante), contrast_mf=$3.287\times10^{8}$, contrast_oi=oco no origem, two_scale=sim (hollow), sign_nest=sim (hole_core, não minus_core). Re origem=0, Re max=0.120747, Re min=0.

![[Artefatos/triad_ninho_pm/01_ic_isosurface.png]]

![[Artefatos/triad_ninho_pm/01e_ic_re_isosurface.png]]

![[Artefatos/triad_ninho_pm/04g_midplane_re_t0.png]]

![[Artefatos/triad_ninho_pm/09b_linecut_re_t0.png]]

![[Artefatos/triad_ninho_pm/06_radial_profiles.png]]

![[Artefatos/triad_ninho_pm/06b_radial_linear.png]]

O gráfico de dinheiro é Re(Ψ) no midplane t=0 (vermelho + / azul −): **halo vermelho (envelope +) com buraco branco no centro** (nó, Re=0). O corte Re$(x,0,0)$ mostra o mesmo. $|Ψ|^2$ sozinho esconde o sinal e mostra o oco/casca. Não é o ninho mesmo-sinal do run 31 (lá o núcleo era brilhante).

## Parâmetros (Theta_core, intocado)

$\Lambda=-10$, $\alpha=0.15$, $\sigma=1.5$, $\Gamma=0.05$, $\nu=(10, 0.5, 0.05)$, $\lambda=(3, 1, 0.3)$, `fdt_couple=True`, **kT=1.0**. $L=32$, $N=64$, $dt=0.0025$, $T=8$, seed=0. $f_{\mathrm{FDT}}=0.0125$, noise_amp $=0.015811388300841896=\sqrt{2\Gamma\,kT\,dt}$. Memória Euler ($\max\nu\cdot dt=0.025$).

Não substitui [[27 triad_chaos_eq]] · [[28 triad_atoms_3d]] · [[29 triad_R5_A2]] · [[30 dois_atomos_gravidade]] · [[31 nested_gaussians]] · [[32 universo_atomo]] · Q01a.

## Resultado

Wall: **46.298 s** (12:51:31–12:52:17 BRT, 21/08/2026). 3200 passos, 117 amostras (cedo $\Delta t=0.01$ até $t=0.4$; depois $\Delta t=0.1$).

| | t=0 IC | t=0.01 | t=0.02 | t=0.04 (último two-scale) | t=0.05 (two perdido) | t=0.09 (1º sign off) | t=0.1 | mid t=4 | final t=8 |
|---|---|---|---|---|---|---|---|---|---|
| two_scale (oco/casca) | sim | sim | sim | sim | não | não | não | não | não |
| sign_nest | sim | sim | sim | sim | sim | não | não | não | não |
| hole_core / minus_core | sim / não | sim / não | sim / não | sim / não | sim / não | não / não | — | — | — |
| Re origem | 0 | −0.034784 | −0.017799 | +0.029837 | +0.033292 | +0.156113 | +0.157547 | −0.067646 | +0.390358 |
| Re max / min | 0.121 / 0 | 0.180 / −0.108 | 0.212 / −0.153 | 0.253 / −0.196 | 0.240 / −0.211 | 0.311 / −0.294 | 0.324 / −0.326 | 1.778 / −1.624 | 1.838 / −1.850 |
| contrast_im | 0.952 | 1.158 | 1.271 | 1.222 | 1.169 | 1.222 | 1.279 | 0.950 | 1.049 |
| contrast_mf | 3.287e8 | 7.139 | 4.149 | 2.593 | 2.284 | 1.730 | 1.650 | 0.975 | 0.888 |
| contrast_oi | oco | 5.076 | 4.642 | 3.936 | 2.220 | 0.534 | 0.742 | 13.587 | 0.513 |
| norm | 1.0 | 33.675405 | 66.236257 | 131.653653 | 164.173819 | 294.527097 | 327.085462 | 10793.588 | 18021.707596 |
| peak | 0.014580 | 0.032350 | 0.045519 | 0.070128 | 0.057509 | 0.106448 | 0.123177 | 3.163439 | 4.336503 |
| PR | 141.559784 | 14978.382 | 15977.150 | 16340.356 | 16357.118 | 16429.534 | 16403.033 | 17834.659 | 19557.411781 |
| R_rms | 2.522489 | 15.765385 | 15.877806 | 15.934619 | 15.948986 | 15.982788 | 15.985310 | 16.014472 | 15.972489 |
| r50 | 2.236068 | 15.580436 | 15.644488 | 15.692355 | 15.700318 | 15.724185 | 15.732133 | 15.763883 | 15.692355 |

Pico de densidade máximo=**4.452033** em t=6.8. Vmem_peak máximo=7.934021 em t=7.1; Vmem_peak final=7.062787. Janela late ($t\ge 6.4$): peak $3.906848\pm 0.261$; PR $19188.898\pm 192$; R_rms $15.990734\pm 0.017$; norm $16769.531\pm 781$. Sem NaN, sem blowup. células½ final=1310 (não 1–2 células).

O ninho **não morreu em t=0.02**. two-scale/oco permanece até **t=0.04**; em t=0.05 contrast_sf/oi caem abaixo do limiar. sign_nest operacional fica ligado até t=0.08 e **cai pela primeira vez em t=0.09**. Depois o flag **pisca** até t=1.0 (36 recordes; último fogo operacional t=1.0) sobre um cubo que **já é universo** desde t=0.01 (R_rms 2.52→15.77, norma 1→33.7 — a mesma família de preenchimento de [[30 dois_atomos_gravidade]] / [[31 nested_gaussians]] / [[32 universo_atomo]]). **Com kT=1 o oco +/− concêntrico dissolve em $t\sim0.05$–$0.09$; o volume preenchido continua o universo.** kT não foi retocado. Isso é o resultado.

Em t=0.01 o origem já é Re=−0.0348 (buraco azul de verdade, não só nó branco). Em t=0.02 Re origem=−0.0178, two e sign ainda vivos. Enquanto two_scale existia: $\Delta$peak $= +0.0555$, $\Delta$R_rms $= +13.412$ (expandiu, não contraiu). Sem leitura de queda.

![[Artefatos/triad_ninho_pm/01d_isosurface_t001.png]]

![[Artefatos/triad_ninho_pm/01c_isosurface_t002.png]]

![[Artefatos/triad_ninho_pm/01f_t002_re_isosurface.png]]

![[Artefatos/triad_ninho_pm/01b_isosurface_early.png]]

![[Artefatos/triad_ninho_pm/02_isosurface_mid.png]]

![[Artefatos/triad_ninho_pm/03_isosurface_late.png]]

![[Artefatos/triad_ninho_pm/04r_midplane_re.png]]

![[Artefatos/triad_ninho_pm/04_midplane_xy.png]]

![[Artefatos/triad_ninho_pm/05_observables.png]]

![[Artefatos/triad_ninho_pm/07_early_zoom.png]]

![[Artefatos/triad_ninho_pm/08_two_scale.png]]

![[Artefatos/triad_ninho_pm/09_linecut_re.png]]

![[Artefatos/triad_ninho_pm/00_montagem.png]]

## O que os números sustentam

**(a) duas escalas / oco — INCONCLUSIVE.** two_scale (hollow) em $t\in\{0, 0.01, 0.02, 0.03, 0.04\}$. Em t=0 o perfil radial tem oco no origem e casca $s\sim0.5$–$2$ (é o ponto da IC +/−). Depois o banho come o oco: R_rms 2.52→15.77 já em t=0.01, flag morta em t=0.05. Não houve tempo para ler colapso/sobreposição. Não é evidência a favor nem contra: o oco não durou.

**(b) ninho de sinal +/− — INCONCLUSIVE como ímã; o flag operacional pisca até t=1.** sign_nest limpo (halo + / buraco no centro, plus_env) até t=0.08; primeiro off em t=0.09. O último fogo operacional é t=1.0, mas isso é flicker sobre universo preenchido, não o ninho concêntrico da IC. Com este banho o ninho vira universo em $t\ll 1$. Não é evidência a favor nem contra de ímã-repele: o ninho de sinal não durou como estrutura.

**(c) pico finito — SUPPORTED (neste run).** peak ρ máximo=4.452033, final=4.336503, sempre finito, sem blowup. Anti-colapso operacional: a singularidade **não** foi a infinito. Pico late ~3.91 em 1310 células, não artefato de 1–2 células.

Nunca “provou gravidade”. Nunca “provou ímã”. Theta_core intocado. kT=1.0 intocado.

## CSVs

- [[Artefatos/triad_ninho_pm/summary.csv]]
- [[Artefatos/triad_ninho_pm/metrics.csv]]
- [[Artefatos/triad_ninho_pm/radial_profiles.csv]]
- [[Artefatos/triad_ninho_pm/linecut_re.csv]]
- [[Artefatos/triad_ninho_pm/summary.json]]

## Arquivos

`00_montagem.png` · `01_ic_isosurface.png` · `01e_ic_re_isosurface.png` · `01b`/`01c`/`01d` isos ρ · `01f`/`01g`/`01h` isos Re · `04_midplane_xy.png` + midplanes |Ψ|² e Re · `04r_midplane_re.png` · `05_observables.png` · `06_radial_profiles.png` · `06b_radial_linear.png` · `07_early_zoom.png` · `08_two_scale.png` · `09_linecut_re.png` · `09b_linecut_re_t0.png` · metrics.csv · radial_profiles.csv · linecut_re.csv · summary.csv · summary.json · `rho_{ic,t001,t002,early,mid,late}.npy` · `re_{ic,t001,t002,early,mid,late}.npy`

Script: [[Fontes/run_ninho_pm.py]]

→ [[Índice de runs]] · [[TRIAD]] · [[Leitura operacional]]
