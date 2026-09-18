---
tags: [triad, simulação, solver]
aliases: [triad_R5_A2]
classe: spec §5 3D Strang (standalone)
diretório: triad_R5_A2
status: R5-FDT
run: 29
data: 2026-08-20 noite
---

# triad_R5_A2

Equação TRIAD **completa** (mode=full) da spec canônica v1.0 [[triad_equation_reference]] **A.2** R5-FDT. IC §9.1: **1 gaussiana = 1 átomo**, $s=0.5$, $k_0=0$, $y_j(0)=0$, $\int|\Psi|^2=1$. **Não é ablação.** Sem §6, sem zerar $\lambda$, sem fit de $k_*L$. [[Memória]] · [[FDT]] · [[Universo como simulação]] · [[Equação de referência]]

N=96 (reduzido vs spec N=128; N=64 deu ~0.014 s/passo < 0.05 s, subiu). Solver: Strang 3D da spec §5 (FFT half linear, $V=\Lambda\rho+V_{\mathrm{mem}}$, Euler memória, FDT, FFT half). **Não** usa `TriadParams` do triad-lang (rejeita 2 modos de memória). Backend: numpy. $V_{\mathrm{ext}}=0$, caixa periódica $[-L/2,L/2)^3$.

## IC — 1 átomo

$\Psi=\mathcal{N}\exp(-|\mathbf{x}|^2/(2s^2))$, $s=0.5$, $k_0=(0,0,0)$. Um blob na origem. Pico IC=1.436697, PR=1.968701, R_rms=0.612372, norma=1.

![[Artefatos/triad_R5_A2/01_ic_isosurface.png]]

![[Artefatos/triad_R5_A2/02_isosurface_early.png]]

## Parâmetros (A.2 R5-FDT)

$\Lambda=-8$, $\sigma=1.5$, $\alpha=0$, $\Gamma=0.01$, $T_{\mathrm{bath}}=0.001$, $\nu=(10, 0.5)$, $\lambda=(1.125, 0.375)$, $L=20$, N=96, $dt=0.0025$, $T=15$, seed=42.

Lock FDT igual ao 28 (`fdt_couple`): $f_{\mathrm{FDT}}=2\Gamma\,dx^3\,T_{\mathrm{bath}}/\hbar=1.808449\times10^{-7}$. **noise_amp = 0.00022360679774997898** $=\sqrt{2\Gamma T_{\mathrm{bath}}dt}$. Memória Euler ($\max\nu\cdot dt=0.025<0.05$).

Não substitui [[27 triad_chaos_eq]] nem [[28 triad_atoms_3d]].

## Resultado

Wall: **313.651 s** (5 min 14 s; 22:00–22:05 BRT, 20/08/2026). 6000 passos, 151 amostras.

| | t=0 | t=0.2 (pico) | early t=2.5 | mid t=7.5 | final t=15 |
|---|---|---|---|---|---|
| norm | 1.0 | 1.028215 | 1.342872 | 1.975632 | 2.815579 |
| peak | 1.436697 | 31.184811 | 0.007653 | 0.002977 | 0.004433 |
| PR | 1.968701 | 0.116987 | 871.949795 | 3994.394322 | 4035.966696 |
| R_rms | 0.612372 | 1.859568 | 6.582178 | 9.798813 | 10.022519 |
| C cryst | 0.995229 | 0.995951 | 0.990987 | 0.994298 | 0.996625 |
| k*L | 9.424778 | 9.424778 | 9.424778 | 9.424778 | 9.424778 |

Pico de densidade máximo=31.184811 em t=0.2 (foco 3D). Vmem_peak máximo=11.261881 em t=0.2; Vmem_peak final=0.001759. r50 0.510310→9.873330; r80 0.779512→12.040153; r90 0.883883→13.113421. Janela late (t≥12): R_rms mean=10.032630 std=0.018685; PR mean=3728.261089 std=404.134198; C mean=0.996281.

O átomo único **sementeia o volume**. t=0: 1 blob na origem. t=2.5: esfera expandida. t=7.5–15: cubo preenchido = **universo**. Não é ruído, não é espuma, não é falha de FDT.

$k_*L$ late=9.424778 (casca não-DC mais baixa; igual ao [[16 triad_R5_reference_N40]]). Spec §10.4 cita ~16.3 em N=128 — **não** calibrado aqui.

![[Artefatos/triad_R5_A2/03_isosurface_mid.png]]

![[Artefatos/triad_R5_A2/04_isosurface_late.png]]

![[Artefatos/triad_R5_A2/05_observables.png]]

![[Artefatos/triad_R5_A2/00_montagem.png]]

## O que os números sustentam

Com A.2 R5-FDT ($\Gamma=0.01$, $T_{\mathrm{bath}}=0.001$) a semente §9.1 permanece 1 átomo visível no t=0 e se espalha até preencher a caixa (R_rms 0.61→10.02, PR 1.97→4036, norma 1→2.816). Leitura: **1 átomo → universo no cubo**. Mesma família de preenchimento que [[27 triad_chaos_eq]] / [[28 triad_atoms_3d]], IC canônico em vez da nuvem de 12. Este run **não** recalibrou FDT nem $k_*L$.

## CSVs

- [[Artefatos/triad_R5_A2/summary.csv]]
- [[Artefatos/triad_R5_A2/metrics.csv]]
- [[Artefatos/triad_R5_A2/summary.json]]

## Arquivos

`00_montagem.png` · `01_ic_isosurface.png` · `02_isosurface_early.png` · `03_isosurface_mid.png` · `04_isosurface_late.png` · `05_observables.png` + metrics.csv + summary.csv + summary.json

Script: [[Fontes/run_R5_A2.py]]

→ [[Índice de runs]] · [[TRIAD]]
