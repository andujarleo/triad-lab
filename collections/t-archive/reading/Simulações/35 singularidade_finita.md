> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/35%20singularidade_finita.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, solver, I0, singularidade]
aliases: [triad_singularidade_35, singularidade_finita, run35]
classe: spec §5 3D Strang (standalone), Theta_core, janela cedo
diretório: triad_singularidade_35
status: I0 / environment / singularidade finita
run: 35
data: 2026-08-21
```


# singularidade_finita

Equação TRIAD **completa**, Theta_core congelado (Q00 / [TRIAD_QM_CANONICAL_V1](../Fontes/TRIAD_QM_CANONICAL_V1.md)). **I0 / environment**, não scan, **não** Q05, **não** teste de MQ. 1 gaussiana = 1 [átomo](../Conceitos/%C3%A1tomo.md). Volume preenchido = universo. Leitura: **singularidade = pico finito** (o ponto brilhante). Anti-colapso: Λ puxa, memória empurra, peak nunca Inf. Pergunta deste run: **enquanto o pico é finito, ele aperta (menos células, peak sobe), espalha (mais células), ou some no universo?** [Leitura operacional](../Conceitos/Leitura%20operacional.md) · [Anti-colapso](../Conceitos/Anti-colapso.md) · [átomo](../Conceitos/%C3%A1tomo.md)

Solver: Strang 3D standalone, **mesmo passo** de Q02 (`ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`). Backend **mlx** complex64, device `Device(gpu, 0)`. $V_{\mathrm{ext}}=0$, $y_j(0)=0$, caixa periódica $[-L/2,L/2)^3$. Seed=0 (única; sem cherry-pick).

## IC — dois casos (seed=0)

- **1atom**: uma gaussiana $s=0.5$ na origem, $\int|\Psi|^2=1$ (IC Q00 / um ponto). t=0: peak=1.43625, n_células=1, PR=1.88731, R_rms=0.611747. artifact_1_2_cells=sim.
- **2atom**: duas gaussianas $s=0.5$ em $x=\pm 3$ (cada uma como Q04), depois $S=(A+B)/\|A+B\|$, $\int|S|^2=1$ (dois pontos, sep=6). t=0: peak=0.718126, n_células=2, PR=3.77461, R_rms=3.06174, n_det=2, pair_sep=6.

![Artefatos/triad_singularidade_35/strip_1atom.png](../../source/Artefatos/triad_singularidade_35/strip_1atom.png)

![Artefatos/triad_singularidade_35/strip_2atom.png](../../source/Artefatos/triad_singularidade_35/strip_2atom.png)

## Parâmetros (Theta_core, intocado)

$\Lambda=-10$, $\alpha=0.15$, $\sigma=1.5$, $\Gamma=0.05$, $\nu=(10, 0.5, 0.05)$, $\lambda=(3, 1, 0.3)$, `fdt_couple=True`, **kT=1.0**. $L=32$, $N=64$, $dt=0.0025$, **$T=1.0$** (janela cedo). seed=0. $f_{\mathrm{FDT}}=0.0125$, noise_amp $=0.015811388300841896$. Memória Euler ($\max\nu\cdot dt=0.025$). Registro a cada 2 passos ($\Delta t=0.005$).

Não substitui [30 dois_atomos_gravidade](30%20dois_atomos_gravidade.md) · [31 nested_gaussians](31%20nested_gaussians.md) · [32 universo_atomo](32%20universo_atomo.md) · [33 ninho_pm](33%20ninho_pm.md) · [34 ninho_pm_long](34%20ninho_pm_long.md) · Q00–Q04.

## Resultado

Wall total: **4.959 s** (2026-08-21 14:43:45 BRT – 2026-08-21 14:43:50 BRT, 21/08/2026). Backend mlx `Device(gpu, 0)`. 400 passos × 2 ICs, 201 registros/IC. Sem NaN, sem blowup. Ambos ICs finitos.

### 1atom — um ponto

- peak_max = **5.3739** em t_at_peak_max = **0.185**
- n_células (½ peak): t=0 → **1**; t_peak → **1** (Δn_células = 0)
- Δpeak (t=0 → t_peak) = 3.93765
- t_point_gone (n_células>200 **ou** R_rms>14.4) = **0.005** (disparado por R_rms; n_células>200 só em t=0.405)
- aperta em $t\in[0,t_{\mathrm{point\_gone}}]$? **não** (em t=0.005 peak 1.436→1.406, n_células=1→1)
- finite_singularity: **SUPPORTED** (peak_max finito, sem NaN, peak_max > peak(t=0)). Nunca SUPPORTED para MQ.
- artifact_1_2_cells: sim em t=0 e em t_peak (IC s=0.5 já cabe em 1 célula de dx=0.5).

### 2atom — dois pontos

- peak_max = **4.76867** em t_at_peak_max = **0.705**
- n_células (½ peak): t=0 → **2**; t_peak → **1** (Δn_células = -1)
- Δpeak (t=0 → t_peak) = 4.05055
- t_point_gone = **0.005** (R_rms; n_células>200 só em t=0.965)
- aperta em $t\in[0,t_{\mathrm{point\_gone}}]$? **não** (em t=0.005 peak 0.718→0.731, n_células=2→2)
- finite_singularity: **SUPPORTED**. Nunca SUPPORTED para MQ.
- n_det t=0 = 2; pair_sep t=0 = 6; n_det=2 em 62 registros. pair_sep=6.000 até t=0.200; depois o detector oscila (sep omitido quando n_det≠2).

| IC | t | peak | n_células | largura | PR | R_rms | finite |
|---|---|---|---|---|---|---|---|
| 1atom | 0 | 1.43625 | 1 | 0.310175 | 1.88731 | 0.611747 | sim |
| 1atom | 0.005 | 1.40631 | 1 | 0.310175 | 564.086 | 15.5271 | sim |
| 1atom | 0.02 | 1.43434 | 1 | 0.310175 | 5426.05 | 15.8712 | sim |
| 1atom | 0.05 | 1.77444 | 1 | 0.310175 | 11680.2 | 15.9463 | sim |
| 1atom | 0.1 | 2.8926 | 1 | 0.310175 | 13867 | 15.983 | sim |
| 1atom | 0.185 | 5.3739 | 1 | 0.310175 | 14140.1 | 15.9983 | sim |
| 1atom | 0.2 | 5.23208 | 1 | 0.310175 | 14532.4 | 15.9967 | sim |
| 1atom | 0.4 | 0.571455 | 182 | 1.75778 | 16379.5 | 16.0014 | sim |
| 1atom | 0.705 | 0.836735 | 560 | 2.55664 | 16412.3 | 16.0038 | sim |
| 1atom | 1 | 1.23637 | 380 | 2.24665 | 16441.4 | 16.0058 | sim |
| 2atom | 0 | 0.718126 | 2 | 0.390796 | 3.77461 | 3.06174 | sim |
| 2atom | 0.005 | 0.731393 | 2 | 0.390796 | 1035.46 | 15.5315 | sim |
| 2atom | 0.02 | 0.730077 | 2 | 0.390796 | 8296.75 | 15.878 | sim |
| 2atom | 0.05 | 0.729707 | 3 | 0.44735 | 14179 | 15.9491 | sim |
| 2atom | 0.1 | 1.10198 | 2 | 0.390796 | 15615.6 | 15.9842 | sim |
| 2atom | 0.185 | 1.5776 | 1 | 0.310175 | 16128.6 | 15.9991 | sim |
| 2atom | 0.2 | 1.57367 | 1 | 0.310175 | 16176.4 | 15.9966 | sim |
| 2atom | 0.4 | 3.03161 | 1 | 0.310175 | 16213.9 | 16.0004 | sim |
| 2atom | 0.705 | 4.76867 | 1 | 0.310175 | 16267 | 16.0031 | sim |
| 2atom | 1 | 1.23635 | 381 | 2.24862 | 16438.2 | 16.0054 | sim |

![Artefatos/triad_singularidade_35/peak_vs_t.png](../../source/Artefatos/triad_singularidade_35/peak_vs_t.png)

![Artefatos/triad_singularidade_35/width_vs_t.png](../../source/Artefatos/triad_singularidade_35/width_vs_t.png)

![Artefatos/triad_singularidade_35/peak_vs_width.png](../../source/Artefatos/triad_singularidade_35/peak_vs_width.png)

![Artefatos/triad_singularidade_35/iso_1atom_t0_tpeak.png](../../source/Artefatos/triad_singularidade_35/iso_1atom_t0_tpeak.png)

## O que os números sustentam

**1atom.** t_point_gone=0.005: R_rms 0.612→15.53 no primeiro registro. Na janela do ponto, peak cai um pouco (1.436→1.406) e n_células fica 1 — **não aperta**. Depois o universo já está preenchido; o peak sobe até 5.374 em t=0.185 ainda em 1 célula (artifact_1_2_cells), depois n_células cresce (182 em t=0.40; 380 em t=1). finite_singularity SUPPORTED neste run: peak_max finito, sem NaN, maior que t=0.

**2atom.** Mesmo t_point_gone=0.005 (R_rms 3.062→15.53). Na janela do ponto, peak 0.718→0.731 e n_células=2 — **não aperta**. n_det=2 e pair_sep=6.000 até t=0.200. peak_max=4.769 em t=0.705 com n_células=1 (já depois de t_point_gone). Em t=1 n_células=381. finite_singularity SUPPORTED neste run.

Resposta operacional: **o ponto some no universo** (R_rms>14.4 em t=0.005). Não aperta na janela declarada. O pico que sobe depois é 1 célula no universo preenchido, finito (nunca Inf). Singularidade = pico finito. **Não** é estrela nem planeta. Nunca SUPPORTED para MQ. kT=1 intocado. Theta_core intocado.

## CSVs

- [Artefatos/triad_singularidade_35/metrics_1atom.csv](../../source/Artefatos/triad_singularidade_35/metrics_1atom.csv)
- [Artefatos/triad_singularidade_35/metrics_2atom.csv](../../source/Artefatos/triad_singularidade_35/metrics_2atom.csv)
- [Artefatos/triad_singularidade_35/summary.json](../../source/Artefatos/triad_singularidade_35/summary.json)

## Arquivos

`peak_vs_t.png` · `width_vs_t.png` · `peak_vs_width.png` · `strip_1atom.png` · `strip_2atom.png` · `iso_1atom_t0_tpeak.png` · metrics_1atom.csv · metrics_2atom.csv · summary.json · SHA256SUMS.txt

Script: [Fontes/run_singularidade_35.py](../../source/Fontes/run_singularidade_35.py) (sha256 `923ecb0f1c4baf1db7ba2978e3977d3f7050f06c28bf387ddace88ab5c9caff7`)

→ [Índice de runs](%C3%8Dndice%20de%20runs.md) · `[[TRIAD]]` · [Leitura operacional](../Conceitos/Leitura%20operacional.md) · [Anti-colapso](../Conceitos/Anti-colapso.md) · [átomo](../Conceitos/%C3%A1tomo.md)

