> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Conceitos/Mem%C3%B3ria.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, conceito]
aliases: [V_mem, y_j, memória TRIAD]
```


# Memória

$$V_{\mathrm{mem}}(t,\mathbf{x})=\sum_j\lambda_j y_j(t,\mathbf{x}),\qquad \partial_t y_j=\nu_j\bigl(|\Psi|^2-y_j\bigr)$$

Cada $y_j$ é passa-baixa de $\rho=|\Psi|^2$ com $\tau_j=1/\nu_j$. Coleção $\{(\nu_j,\lambda_j)\}$ = série de Prony de um núcleo (Mori–Zwanzig; spec §2.3). Solver exige ≥3 escalas.

Sinal de $\lambda_j$:

- $>0$ — memória **repulsiva**: suprime retorno a regiões já ocupadas → [Anti-colapso](Anti-colapso.md)
- $<0$ — poços: aprofunda canais já altos

Default de `TriadParams.lam` é (−0.3, −0.2, −0.1) — atrativo. O bounce usou `lam=(3, 1, 0.3)`.

No passo Strang a memória atualiza **duas vezes** por $dt$ (antes e depois do potencial), com decaimento $e^{-\nu dt/2}$. Ver `[[Solver]]`.

## No registro

- Sem memória vs full: R5 N40 — peak_final 3.889202 vs 0.0006409; PR 0.528063 vs 4720.477435. [16 triad_R5_reference_N40](../Simula%C3%A7%C3%B5es/16%20triad_R5_reference_N40.md)
- Atlas: sem regiões de $V_{\mathrm{mem}}\approx|\Lambda\rho|$. [18 triad_visual_atlas](../Simula%C3%A7%C3%B5es/18%20triad_visual_atlas.md)
- Bounce: pico de densidade t=4.1, memória t=4.2, delay=0.1. [23 triad_memory_bounce_bigbang](../Simula%C3%A7%C3%B5es/23%20triad_memory_bounce_bigbang.md) · [Bounce](Bounce.md)
- Campo C: `C_memory_corr_final=-0.3855089487747705` (continuous_C). [09 triad_field_consciousness_test](../Simula%C3%A7%C3%B5es/09%20triad_field_consciousness_test.md) · [Observador e campo C](Observador%20e%20campo%20C.md)

Voltar: `[[Equação de referência]]`
