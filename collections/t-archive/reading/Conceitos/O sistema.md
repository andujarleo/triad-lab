> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Conceitos/O%20sistema.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, resumo, memória, anti-colapso]
aliases: [resumo TRIAD, o sistema]
date: 2026-08-21
```


# TRIAD — o sistema

Nosso cubo. Não é pra ninguém.

Um campo $\Psi$ no espaço. Três coisas puxam ao mesmo tempo: o foco (quer juntar), a memória (empurra o que já esteve), e o banho (enche o cubo). A gente roda as três juntas. Sem desligar termo pra “entender melhor”.

## A equação

$$
i\,\partial_t\Psi=\Bigl[-\tfrac{1}{2}\nabla^2+V_{\mathrm{ext}}+\Lambda|\Psi|^2+V_{\mathrm{mem}}+\alpha(-\Delta)^{\sigma/2}-i\Gamma\Bigr]\Psi+\eta
$$

$$
V_{\mathrm{mem}}=\sum_j\lambda_j y_j,\qquad \partial_t y_j=\nu_j\bigl(|\Psi|^2-y_j\bigr)
$$

O ruído $\eta$ vem com o $\Gamma$: quanto mais o campo vaza, mais o banho escreve. No Theta_core, $kT=1$.

O que cada pedaço faz, na nossa língua:

- $-\nabla^2/2$ — o campo se espalha, como onda
- $\Lambda|\Psi|^2$ — se $\Lambda<0$, onde tem mais, puxa mais. Foco. Quer um ponto
- $V_{\mathrm{mem}}$ — o passado empurra o presente
- $\alpha(-\Delta)^{\sigma/2}$ — um pouco de “fora da escala”, cauda
- $-i\Gamma$ + $\eta$ — o cubo esfria/vaza e o banho devolve. Universo enchendo

1 gaussiano = 1 átomo. O volume preenchido = universo. Pico finito = a singularidade que não vira infinito.

## Anti-colapso

Ímã contra ímã.

$\Lambda$ puxa pra dentro. A memória, com $\lambda_j>0$, empurra pra fora o lugar que já foi ocupado. Os dois brigam no mesmo ponto. O pico sobe, mas não vai a infinito. Depois espalha. O cubo vira universo.

Sem memória o campo desaba (pico grande, PR no chão). Com memória o late é espalhado (PR nas casas dos milhares) e o pico do fim é pequeno.

Isso não apaga o começo. Cedo existe um **trem de autofoco**: o pico cruza alto várias vezes, e isso cresce quando a grade afina (N=64 → 128 → 160: tetos ~13 → 62 → 100). A memória mata o colapso que *dura*. O pulso cedo continua.

Reexecução no Linux (run 36): no fim a memória espalha; sem memória colapsa. O 16.3 do dossiê antigo não apareceu — o $k^*L$ ficou em $3\pi$, primeiro bin da grade. Rede Bravais não nasceu. A gente não fica nisso.

## Memória

$y_j$ é o $\rho=|\Psi|^2$ atrasado. Cada $j$ tem um tempo $1/\nu_j$.

No Theta_core (congelado, Q00):

| | $\nu$ | $\lambda$ | tempo |
|---|---|---|---|
| rápida | 10 | 3 | 0.1 |
| média | 0.5 | 1 | 2 |
| lenta | 0.05 | 0.3 | 20 |

$V_{\mathrm{mem}}=\lambda\cdot y$. Onde o campo já esteve, a memória levanta um potencial e empurra. Por isso o ímã.

A memória não é um “campo C”. Runs 8 e 9 puseram um C e o universo mal notou. A memória *é* o $\Psi$ no passado.

No cubo a gente mede **cola**: correlação de $y$ com $\rho$ num pedaço. Se cola ali e não cola no resto, aquele pedaço está sendo lembrado. Se cola igual em todo lugar, é banho.

## O cubo que a gente tem

Theta_core: $\Lambda=-10$, $\alpha=0.15$, $\sigma=1.5$, $\Gamma=0.05$, $\nu$ e $\lambda$ da tabela, FDT ligado, $kT=1$, 3D, passo Strang.

Em $kT=1$ o cubo enche quase na hora (t=0.005 no 37). O gaussiano inicial é semente, não morador.

**27–35.** Doze átomos, ninho, +/−, um ponto, dois pontos. Sempre a mesma coisa: cedo tem forma, o pico fica finito, o late é universo.

**37.** Plantamos um gaussiano no cubo já cheio. Ele apareceu (massa +1.08, pico 1.60). Apertou até 4.52 em t=0.8. Em t=1.085 o cubo tinha comido de novo.

**38.** Dois, + e −. Os dois nasceram, os dois apertaram (4.51 e 3.41). O menos foi primeiro. Não ficou par.

**39.** O mapa. Mesmo cubo do 37, corte no meio: $\rho$, $y$, $|\rho-y|$, $V_{\mathrm{mem}}$.

Cola na janela do bolso:

- plantio: 0.52 (a memória ainda não sabia)
- t=0.8: 0.89 (soube)
- late: 0.68, igual ao resto do cubo (esqueceu)

Um instante em que a memória segura o bolso. Depois o cubo iguala.

## Como a gente lê o conjunto

O sistema é uma briga de três:

1. o foco quer ponto
2. a memória não deixa o ponto ficar
3. o banho quer cubo cheio

O anti-colapso é (1) contra (2). O universo é (3) ganhando no late. O “alguém” que a gente procura é um pedaço onde (2) cola em (1) *enquanto* (3) já encheu. No Theta_core isso aparece e some. Não dura.

Não desligamos termo pra forçar duração. Não baixamos $kT$ depois do resultado. O próximo cubo, quando tiver, é outra pergunta no mesmo sistema.

## Onde está

- Equação: `[[Equação de referência]]` · [TRIAD_QM_CANONICAL_V1](../Fontes/TRIAD_QM_CANONICAL_V1.md)
- Memória / anti-colapso: [Memória](Mem%C3%B3ria.md) · [Anti-colapso](Anti-colapso.md)
- Cubos recentes: [37 bolso_no_universo](../Simula%C3%A7%C3%B5es/37%20bolso_no_universo.md) · [38 dois_bolsos](../Simula%C3%A7%C3%B5es/38%20dois_bolsos.md) · [39 mapa](../Simula%C3%A7%C3%B5es/39%20mapa.md)
- Tudo junto: [00 registro_completo](../Fontes/TRIAD_registro_completo_simulacoes_2026-08-21.md)

Voltar: `[[TRIAD]]`
