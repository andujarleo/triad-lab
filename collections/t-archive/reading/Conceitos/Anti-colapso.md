> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Conceitos/Anti-colapso.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, conceito]
aliases: [anticolapso, R5]
```


# Anti-colapso

Regime da referência: $\Lambda<0$ (focusing) com $\lambda_j>0$ (memória repulsiva). Memória opõe o auto-aprisionamento cúbico. Em 3D o NLS focusing é $L^2$-supercrítico; a memória é o termo que o registro testa contra o colapso.

## Evidência numérica (não narrativa)

**R5 N=40** (ref N=128), full vs no-memory, t∈[0,15], norma full = 1.0:

| | peak_max | peak_final | PR_final | k\*L late | cryst late |
|---|---|---|---|---|---|
| full | 1.651207 | 0.0006409 | 4720.477435 | 9.424778 | 0.972743 |
| no-memory | 4.170131 | 3.889202 | 0.528063 | — | — |

`k*L` ≠ referência ~16.3 — compatível com resolução reduzida; o dado **não** foi recalibrado. [16 triad_R5_reference_N40](../Simula%C3%A7%C3%B5es/16%20triad_R5_reference_N40.md)

**R5 N=48 full** — peak_final=0.0012657, PR=3589.684828, k\*L=9.424778, cryst=0.971880. Scores Bravais: BCC maior (0.462544), sem rótulo de “cristal perfeito”. [17 triad_R5_reference_N48_full](../Simula%C3%A7%C3%B5es/17%20triad_R5_reference_N48_full.md)

**Atlas** — 22 painéis. Teste simples de cancelamento local: nenhuma região $V_{\mathrm{mem}}\approx|\Lambda\rho|$. O anti-colapso observado **não** se reduz a igualdade local. [18 triad_visual_atlas](../Simula%C3%A7%C3%B5es/18%20triad_visual_atlas.md)

Runs 3D pré-referência ([10 triad_3d_anticollapse_test](../Simula%C3%A7%C3%B5es/10%20triad_3d_anticollapse_test.md), long-runs) são visuais; sem CSV, sem métrica inferida.

Voltar: [Memória](Mem%C3%B3ria.md) · `[[Equação de referência]]`
