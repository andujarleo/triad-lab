---
tags: [triad, conceito]
aliases: [V_mem, y_j, memória TRIAD]
---

# Memória

$$V_{\mathrm{mem}}(t,\mathbf{x})=\sum_j\lambda_j y_j(t,\mathbf{x}),\qquad \partial_t y_j=\nu_j\bigl(|\Psi|^2-y_j\bigr)$$

Cada $y_j$ é passa-baixa de $\rho=|\Psi|^2$ com $\tau_j=1/\nu_j$. Coleção $\{(\nu_j,\lambda_j)\}$ = série de Prony de um núcleo (Mori–Zwanzig; spec §2.3). Solver exige ≥3 escalas.

Sinal de $\lambda_j$:

- $>0$ — memória **repulsiva**: suprime retorno a regiões já ocupadas → [Anti-colapso](anti-collapse.md)
- $<0$ — poços: aprofunda canais já altos

Default de `TriadParams.lam` é (−0.3, −0.2, −0.1) — atrativo. O bounce usou `lam=(3, 1, 0.3)`.

No passo Strang a memória atualiza **duas vezes** por $dt$ (antes e depois do potencial), com decaimento $e^{-\nu dt/2}$. Ver `[[Solver]]`.

## No registro

- Sem memória vs full: R5 N40 — peak_final 3.889202 vs 0.0006409; PR 0.528063 vs 4720.477435. [16 triad_R5_reference_N40](../../../experiments/memory/memory-grid-40/notes/original-record.md)
- Atlas: sem regiões de $V_{\mathrm{mem}}\approx|\Lambda\rho|$. [18 triad_visual_atlas](../../../experiments/geometry/visual-atlas/notes/original-record.md)
- Bounce: pico de densidade t=4.1, memória t=4.2, delay=0.1. [23 triad_memory_bounce_bigbang](../../../experiments/memory/memory-and-bounce/notes/original-record.md) · [Bounce](bounce.md)
- Campo C: `C_memory_corr_final=-0.3855089487747705` (continuous_C). [09 triad_field_consciousness_test](../../../experiments/relations/continuous-relational-field/notes/original-record.md) · [Observador e campo C](observer-and-c-field.md)

Voltar: `[[Equação de referência]]`
