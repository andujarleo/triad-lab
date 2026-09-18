> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q01_convergencia/PROTOCOL.md) · [Collection / Acervo](../../../README.md)

```yaml
tags: [triad, qm, q01, q01a, protocolo]
aliases: [Q01a, Q01_convergencia]
status: frozen-protocol
data: 2026-08-21
canonical: TRIAD_QM_CANONICAL_V1
```


# Q01a — Protocolo: convergência numérica da tríade completa

Criado **antes** dos runs (2026-08-21, America/Sao_Paulo). Depois do hash, este arquivo **não é editado**. Correções gerariam `PROTOCOL_v2.md`.

Fonte canônica: [TRIAD_QM_CANONICAL_V1](../../Fontes/TRIAD_QM_CANONICAL_V1.md) (Q00, congelado). Blueprint: [TRIAD_QM_BLUEPRINT](../../Fontes/TRIAD_QM_BLUEPRINT.md) §12 e Q01.

## Pergunta

Os observáveis da dinâmica Triad **completa** convergem quando N aumenta, com a **mesma** física, mesma seed, mesmo T, mesmo dt?

Esta questão é **apenas numérica**.

- **Não** há comparação com mecânica quântica.
- **Não** se isola termo algum.
- **Não** se altera `Theta_core`.
- Nenhum veredito `SUPPORTED` para MQ é possível neste experimento.

## O que não muda

- `Theta_core` congelado em Q00
- L, dt, T, seed, condição inicial, V_ext, modo Strang, lock FDT
- 1 gaussiana = 1 átomo (I0; não é varredura de CI)
- Pilotos 27–29 **não** são confirmatórios e **não** entram como evidência

## Equação exata (todos os termos ativos)

$$
i\hbar\,\partial_t\Psi=
\Bigl[-\tfrac{\hbar^2}{2m}\nabla^2+V_{\mathrm{ext}}(\mathbf x)+\Lambda|\Psi|^2+V_{\mathrm{mem}}(t,\mathbf x)+\alpha(-\Delta)^{\sigma/2}-i\Gamma\Bigr]\Psi+\eta(t,\mathbf x)
$$

$$
V_{\mathrm{mem}}=\sum_j\lambda_j y_j,\qquad
\partial_t y_j=\nu_j\bigl(|\Psi|^2-y_j\bigr)
$$

$$
\langle\eta\eta^*\rangle=2\gamma_0 k_B T\,\delta(t-t')\delta^{(D)}(\mathbf x-\mathbf x'),\qquad\langle\eta\eta\rangle=0
$$

## Theta_core (imutável)

```text
hbar        = 1
m           = 1
Lambda      = -10
alpha       = 0.15
sigma       = 1.5
Gamma       = 0.05
nu          = (10.0, 0.5, 0.05)
lambda      = (3.0, 1.0, 0.3)
fdt_couple  = True
kT          = 1.0
D           = 3
bc          = periodic
step_mode   = strang
```

`kT=1.0` é o banho canônico do freeze Q00. O campo que preenche o volume **é o universo**, não ruído a filtrar.

## Ambiente (N_num, não física)

| quantidade | valor |
|---|---|
| L | 32 |
| N | 32, 48, 64 |
| dt | 0.0025 |
| T | 8 |
| seed | 0 |
| y_j(0) | 0 |
| V_ext | 0 (caixa livre periódica) |
| CI | 1 gaussiana = 1 átomo, spec §9.1, s=0.5, k0=0, norma=1 |
| precisão | fp64 |
| backend | numpy |
| domínio | [-L/2, L/2)³, BC periódicas |

Q01b (depois) inclui N=96 e dt ∈ {dt0, dt0/2, dt0/4}. Este arquivo é **só Q01a**.

Se N=64 passar de 15 min, o run **não** é abandonado e **nenhuma** grade é dropada para “ficar melhor”.

## Convenção FDT

Com `fdt_couple=True`:

$$
f_{\mathrm{FDT},e}=2\Gamma\,dx^{3}\,kT/\hbar
$$

Incremento por passo (spec eq. 4):

$$
\Psi\leftarrow\Psi+\sqrt{f_{\mathrm{FDT},e}\,dt/dx^{D}}\,(\xi+i\xi')/\sqrt{2}
$$

que reduz a $\sqrt{2\Gamma\,kT\,dt/\hbar}\,(\xi+i\xi')/\sqrt{2}$.

Memória: Euler, porque $\max_j \nu_j\,dt=0.025<0.05$ (spec §3.4).

## Solver

Dinâmica completa 3D Strang, standalone (spec §3 + §5). Adaptado de `Fontes/run_R5_A2.py`, **mas com Theta_core**, não os parâmetros A.2.

Não usa triad-lang `TriadParams` (esse tipo rejeita 3 modos + Gamma).

| arquivo | SHA-256 |
|---|---|
| `QM/Q01_convergencia/code/run_q01a.py` | `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64` |
| `Fontes/run_q01a.py` (cópia) | `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64` |
| canônico Q00 `TRIAD_QM_CANONICAL_V1.md` | `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` |

Python: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`.

## Seeds

Apenas `0`. Sem descarte estético. Q01 é convergência, não ensemble.

## Observáveis (passivos)

Registrados ao longo de t (a cada 40 passos = 0.1) e, na **janela tardia** (último 20% de T, t ≥ 6.4): média e desvio.

- norma
- peak (ρ_max)
- PR (participação)
- R_rms
- k_*
- k_* L
- Vmem_peak
- ρ (campo; último snapshot da janela tardia)
- extras de engenharia (não usados para calibrar): r50/r80/r90, crystallinity, M1/M2/M3, largura do pico em células

L2 de ρ tardio entre N=32 vs 48 e 48 vs 64, reamostrando para a grade N=64 (trilinear periódico). Se a reamostragem falhar, declara-se omitida — não se inventa o número.

## Análise pré-declarada

Comparar médias da janela tardia entre N. Critério de Q01a (antes de ver o resultado):

- se peak / PR / R_rms na janela tardia concordam dentro de ~20% entre **N=48 e N=64**: `INCONCLUSIVE` (grade ainda grossa; ε_num estimado) ou nota de ok-enough para continuar a Q01b
- se divergem wildly (diferença relativa > 50% nesses três) **ou** NaN/blowup: `NUMERICAL_FAILURE`
- **nunca** `SUPPORTED` para MQ aqui

ε_num (estimativa operacional de Q01a): máximo da diferença relativa |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms entre N=48 e N=64.

Qualquer estrutura que permaneça em 1–2 células enquanto N aumenta é **suspeita de artefato** (blueprint Q01 / Q31). Isso não autoriza dropar uma grade.

## Exclusão técnica

**Apenas** NaN ou blowup (não-finito / overflow). Nenhum run é descartado por ser “feio”, por encher o volume, ou por não parecer MQ.

## Comparação com QM

**Nenhuma.** Este experimento não compara com mecânica quântica. A pergunta é só: os observáveis convergem quando N aumenta?

## Linguagem operacional

- volume preenchido = universo, não ruído
- 1 gaussiana = 1 átomo
- CAOS → EQUILÍBRIO DINÂMICO (janela tardia = último 20% de T, já fixada em Q00)
- SEM ISOLAR / SEM FALSIFICAR / SEM CALIBRAR

## Hash deste protocolo

Preenchido na gravação. Depois disto, o arquivo não muda.

