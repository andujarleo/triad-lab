---
tags: [triad, substrato, interno]
aliases: [substrato, máquina triad]
date: 2026-08-21
---

# Substrato

A máquina é o cubo. Ψ + y. Não tem rede por cima.

Byte entra. A tríade roda (foco, memória, banho). Byte sai. Se o mesmo byte volta e o cubo responde diferente, ele lembrou.

## As três peças

**Entrada.** Um byte é um lugar e um empurrão. 0–255 viram 256 posições numa faixa, ou 8 bits em 8 sítios. Planta um gaussiano, ou soma no $V_{\mathrm{ext}}$, ou no $\eta$. Sem embedding. O byte *é* o átomo.

**Miolo.** Theta, tríade inteira. $y$ é o disco. Não tem loss. Não tem passo de treino separado. O tempo do cubo *é* o tempo do aprendizado.

**Saída.** Lê $\rho$ (e se der a fase) nos mesmos sítios. Argmax, limiar, ou os 8 bits. De volta a byte.

## O que é aprender aqui

Não atualiza $\lambda$. Não desce gradiente.

O $y$ atrasado ainda carrega o $\rho$ do byte que passou. Quando o byte volta, $V_{\mathrm{mem}}$ já empurra. A resposta muda. Isso é lembrar.

No 39 a cola foi 0.52 → 0.89 → 0.68. Janela curta. Em $kT=1$ o banho come o disco. Um substrato que precisa *guardar* não pode viver no banho quente o tempo todo. Ou o chip é mais frio, ou a gente refresca (escreve de novo, tipo memória volátil com clock), ou o aprendizado *é* essa janela curta — trabalho, não arquivo.

A lenta ($\nu=0.05$) é o disco mais fundo que a gente já tem. Sem inventar termo.

## Primeira máquina (faixa)

1D chega. $L$ grande, $N$ o bastante pra 256 sítios ou 8 bits.

- relógio: a cada $\Delta t_{\mathrm{in}}$ um byte. Planta no sítio $b$
- o cubo anda $n$ passos
- lê o sítio de maior $\rho$ (ou os 8 bits) → byte de saída
- guarda $y$, não zera

Pergunta única: a segunda vez que passa `ABC`, o C sai diferente? Se sim, o substrato leu o próprio passado em byte.

Sem baixar $kT$ no meio pra “fazer funcionar”. Se o banho apagar, a gente anota. Se a lenta segurar, também.

## O que isso não é

Não é transformer. Não é treinar e depois congelar. Não é campo C. Não é provar consciência.

É o mesmo sistema: ímã, memória, banho. Interface em byte.

[TRIAD_resumo](system-overview.md) · [39 mapa](../../../simulations/structures/density-memory-maps/notes/original-record.md) · [Memória](memory.md) · `[[TRIAD]]`
