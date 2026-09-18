> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q01_convergencia/analysis.md) · [Collection / Acervo](../../../README.md)

# Q01a — Análise (convergência numérica da tríade completa)

Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
Pilotos 27–29 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.
Theta_core intocado (Q00). PROTOCOL.md não foi editado depois do hash.

## Pergunta

Os observáveis convergem quando N aumenta, com a mesma física, mesma seed, mesmo T, mesmo dt?

## Setup

- Theta_core: Λ=-10, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0
- L=32, dt=0.0025, T=8, seed=0, y_j(0)=0, V_ext=0, CI §9.1 s=0.5 k0=0, norma=1
- FDT: f_FDT_e=2Γ dx³ kT/ℏ ; incremento spec eq. 4
- N ∈ {32, 48, 64}; fp64; backend numpy; Strang standalone
- início (America/Sao_Paulo): 2026-08-21 12:03:01 BRT
- fim (America/Sao_Paulo): 2026-08-21 12:04:13 BRT
- exclusão técnica = apenas NaN/blowup; nenhum run excluído

## Tempos de parede

| N | dx | wall_s | wall_min | finito |
|---|---|---|---|---|
| 32 | 1.000000 | 5.695 | 0.095 | True |
| 48 | 0.666667 | 17.749 | 0.296 | True |
| 64 | 0.500000 | 48.300 | 0.805 | True |

Total ~71.7 s (muito abaixo de 15 min). Nenhuma grade foi dropada.

## Janela tardia (t ≥ 0.8 T = 6.4) — média ± std

| N | norm | peak | PR | R_rms | k* | k*L | Vmem_peak | células½ | largura_fís | 1–2 células |
|---|---|---|---|---|---|---|---|---|---|---|
| 32 | 1.6777e4 ± 775 | 2.773 ± 0.194 | 2.184e4 ± 439 | 16.042 ± 0.014 | 5.400 ± 0 | 172.79 ± 0 | 7.500 ± 0.501 | 768 ± 337 | 5.568 ± 0.795 | não |
| 48 | 1.6860e4 ± 792 | 3.146 ± 0.242 | 2.062e4 ± 419 | 15.988 ± 0.021 | 8.149 ± 0 | 260.75 ± 0 | 6.702 ± 0.466 | 2023 ± 845 | 5.131 ± 0.718 | não |
| 64 | 1.6765e4 ± 780 | 3.905 ± 0.281 | 1.919e4 ± 195 | 15.983 ± 0.023 | 10.701 ± 0 | 342.43 ± 0 | 6.622 ± 0.350 | 2314 ± 1042 | 3.988 ± 0.701 | não |

Norma cresce de ~1 até ~1.7×10⁴ em T=8 (injeção FDT com kT=1). R_rms ≈ 16 ≈ L/2: o volume está preenchido. Isso é o universo, não um ruído a filtrar.

## Diferenças relativas N=48 vs N=64 (critério pré-declarado ~20%)

- peak: 0.1944 (19.4%)
- PR: 0.0692 (6.9%)
- R_rms: 0.0003 (0.03%)

Diferenças N=32 vs N=48 (contexto, não critério):

- peak: 0.1183 (11.8%)
- PR: 0.0557 (5.6%)
- R_rms: 0.0034 (0.34%)

ε_num estimado = **0.1944**
definição: máximo da diferença relativa |A−B|/max(|A|,|B|) das médias da janela tardia (último 20% de T) de peak, PR, R_rms entre N=48 e N=64.

peak está no limiar ~20% e ainda sobe com N (2.77 → 3.15 → 3.90). PR desce. R_rms já está estável. Grade ainda grossa: Q01b (N=96 + dt-refine) é o próximo teste numérico, não um ajuste de Theta.

## k* preso à grade

k* na janela tardia cai no canto de Nyquist de cada grade (k_max ≈ π√3 / dx):

- N=32: k* = 5.400 ≈ 5.441
- N=48: k* = 8.149 ≈ 8.162
- N=64: k* = 10.701 ≈ 10.883

k* e k*L **não** convergem; estão presos ao cutoff da grade. Observável espectral ainda não tem ε_num útil. Não se recalibra k* e não se compara com MQ.

## L2 de ρ tardio (reamostrado para N=64)

Método: RegularGridInterpolator trilinear, periódico, grade comum N=64.

- 32_vs_48: L2=68.84  L2_rel=0.616  (ref N=48)
- 48_vs_64: L2=95.57  L2_rel=0.742  (ref N=64)
- 32_vs_64: L2=94.86  L2_rel=0.736  (ref N=64)

Os campos ρ tardios **não** coincidem ponto a ponto. Seed=0 em grades diferentes não gera o mesmo campo de ruído (o RNG consome N³ amostras por passo). L2 alto não é exclusão técnica; é esperado neste desenho de Q01a. Os escalares da janela tardia é que entram no critério.

## Estruturas de 1–2 células

Não. Na janela tardia o pico ocupa centenas a milhares de células (N=32: ~768; N=48: ~2023; N=64: ~2314). Largura física ~ 5.6 → 5.1 → 4.0 ainda encolhe com N: não é artefato de 1–2 células, mas também não está saturada. Suspeita de core ainda dependente de dx — Q01b.

No t=0 a gaussiana s=0.5 cabe em 1 célula quando dx=1 (N=32): isso é a CI, não o estado tardio.

## Veredito

**INCONCLUSIVE**

peak/PR/R_rms concordam dentro de ~20% entre N=48 e N=64; grade ainda grossa (Q01a sem N=96 / dt-refine). ok-enough para continuar a Q01b. Nunca SUPPORTED para MQ aqui.

ε_num (Q01a, operacional) ≈ 0.19 (dominado pelo peak).

Este experimento **não** compara com mecânica quântica e **não** pode devolver SUPPORTED para MQ.
Exclusão técnica = apenas NaN/blowup. Nenhum run foi descartado por ser feio. Nenhum termo isolado. Theta_core não mudou.

## Arquivos

- pasta: `/Users/leo/Documents/Triad/T/QM/Q01_convergencia/`
- PROTOCOL.md (hash `eb127b7d7948e12e9e097ee2e94379821dc51a157033d11bfd449da2d6b1f550`)
- config.json, seeds.txt, Q01.md
- code/run_q01a.py e Fontes/run_q01a.py (hash `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64`)
- raw/N{32,48,64}_metrics.csv, raw/N*_summary.json, raw/N*_rho_late.npy
- metrics.csv
- figures/overlay_observables.png, late_window_comparison.png, late_rho_midplane.png, peak_structure_vs_N.png
- analysis.md, result.json, SHA256SUMS.txt
