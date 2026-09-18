---
tags: [triad, conceito]
aliases: [anticolapso, R5]
---

# Anti-colapso

Regime da referência: $\Lambda<0$ (focusing) com $\lambda_j>0$ (memória repulsiva). Memória opõe o auto-aprisionamento cúbico. Em 3D o NLS focusing é $L^2$-supercrítico; a memória é o termo que o registro testa contra o colapso.

## Evidência numérica (não narrativa)

**R5 N=40** (ref N=128), full vs no-memory, t∈[0,15], norma full = 1.0:

| | peak_max | peak_final | PR_final | k\*L late | cryst late |
|---|---|---|---|---|---|
| full | 1.651207 | 0.0006409 | 4720.477435 | 9.424778 | 0.972743 |
| no-memory | 4.170131 | 3.889202 | 0.528063 | — | — |

`k*L` ≠ referência ~16.3 — compatível com resolução reduzida; o dado **não** foi recalibrado. [16 triad_R5_reference_N40](../../../experiments/memory/memory-grid-40/notes/original-record.md)

**R5 N=48 full** — peak_final=0.0012657, PR=3589.684828, k\*L=9.424778, cryst=0.971880. Scores Bravais: BCC maior (0.462544), sem rótulo de “cristal perfeito”. [17 triad_R5_reference_N48_full](../../../experiments/memory/memory-grid-48/notes/original-record.md)

**Atlas** — 22 painéis. Teste simples de cancelamento local: nenhuma região $V_{\mathrm{mem}}\approx|\Lambda\rho|$. O anti-colapso observado **não** se reduz a igualdade local. [18 triad_visual_atlas](../../../experiments/geometry/visual-atlas/notes/original-record.md)

Runs 3D pré-referência ([10 triad_3d_anticollapse_test](../../../experiments/memory/3d-anti-collapse-exploration/notes/original-record.md), long-runs) são visuais; sem CSV, sem métrica inferida.

Voltar: [Memória](memory.md) · `[[Equação de referência]]`
