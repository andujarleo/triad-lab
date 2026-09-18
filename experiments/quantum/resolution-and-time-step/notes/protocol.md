---
tags: [triad, qm, q01, q01b, protocolo]
aliases: [Q01b, Q01b_dt_N]
status: frozen-protocol
data: 2026-08-21
canonical: TRIAD_QM_CANONICAL_V1
---

# Q01b — Protocolo: refino N e dt (convergência numérica)

Criado **antes** dos runs (2026-08-21, America/Sao_Paulo). Depois do hash, este arquivo **não é editado**. Correções gerariam `PROTOCOL_v2.md`.

Fonte canônica: [TRIAD_QM_CANONICAL_V1](../../../../docs/reference/records/triad-qm-canonical-v1.md) (Q00, congelado). Blueprint: [TRIAD_QM_BLUEPRINT](../../../../docs/reference/records/triad-qm-blueprint.md) §12 / Q01.
Q01a (lote espacial grosso): [Q01](../../spatial-convergence/notes/convergence-record.md) em `QM/Q01_convergencia/`. **Não** se edita o PROTOCOL.md de Q01a.

## Pergunta

Os observáveis da dinâmica Triad **completa** convergem quando refinamos a régua computacional além de Q01a — (i) N=96 com o mesmo dt0 e (ii) dt ∈ {dt0/2, dt0/4} em N=64?

Esta questão é **apenas numérica**.

- **Não** há comparação com mecânica quântica.
- **Não** se isola termo algum.
- **Não** se altera `Theta_core`.
- Nenhum veredito `SUPPORTED` para MQ é possível neste experimento.
- Q00 permanece congelado. Q01a permanece INCONCLUSIVE (ε_num≈0.194; k* no Nyquist); este lote não reabre Q01a.

## O que não muda

- `Theta_core` congelado em Q00
- L, T, seed, condição inicial, V_ext, modo Strang, lock FDT
- 1 gaussiana = 1 átomo (I0; não é varredura de CI)
- Pilotos 27–29 **não** são confirmatórios e **não** entram como evidência
- Janela tardia = último 20% de T (t ≥ 6.4), já fixada em Q00 — não se redesenha depois de ver o resultado

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
| T | 8 |
| seed | 0 |
| y_j(0) | 0 |
| V_ext | 0 (caixa livre periódica) |
| CI | 1 gaussiana = 1 átomo, spec §9.1, s=0.5, k0=0, norma=1 |
| precisão | fp64 |
| backend | numpy |
| domínio | [-L/2, L/2)³, BC periódicas |
| dt0 | 0.0025 (canônico Q00 / Q01a) |

Células **deste** lote (ordem de execução):

| célula | N | dt | nota |
|---|---|---|---|
| N96_dt0 | 96 | 0.0025 = dt0 | refino espacial; mesmo dt de Q01a |
| N64_dt0h | 64 | 0.00125 = dt0/2 | refino temporal; mesma grade N=64 de Q01a |
| N64_dt0q | 64 | 0.000625 = dt0/4 | refino temporal mais fino |

Overlay obrigatório contra **Q01a N=64 dt0** (não se re-roda Q01a). Fonte: `QM/Q01_convergencia/result.json` e `metrics.csv`.

Se N=96 passar de 20 min, o run **não** é abandonado e **nenhuma** célula é dropada para “ficar melhor”.

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

Memória: Euler. Em dt0, $\max_j\nu_j\,dt=0.025<0.05$ (spec §3.4). Em dt0/2 e dt0/4 o produto é ainda menor — Euler permanece justificado; **não** se troca o integrador de memória.

## Solver

Dinâmica completa 3D Strang, standalone (spec §3 + §5). Cópia parametrizada de `Fontes/run_q01a.py` (hash `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64`): só N e dt viram argumentos. **Mesmo** passo, mesmos observáveis, mesmo Theta_core. Não usa triad-lang `TriadParams`.

| arquivo | SHA-256 |
|---|---|
| `Fontes/run_q01a.py` (fonte Q01a, não editar) | `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64` |
| canônico Q00 `TRIAD_QM_CANONICAL_V1.md` | `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` |
| `Fontes/run_q01b.py` / `QM/Q01b_dt_N/code/run_q01b.py` | preenchido na gravação do código |

Python: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`.

Registro temporal: Δt_rec = 0.1 (igual a Q01a: 40 passos × dt0). Em dt menor, `record_every = round(0.1/dt)` para a janela tardia ter a mesma cadência física.

## Seeds

Apenas `0`. Sem descarte estético. Q01 é convergência, não ensemble.

## Observáveis (passivos)

Iguais a Q01a. Registrados ao longo de t (Δt_rec = 0.1) e, na **janela tardia** (último 20% de T, t ≥ 6.4): média e desvio.

- norma
- peak (ρ_max)
- PR (participação)
- R_rms
- k_*
- k_* L
- Vmem_peak
- ρ (campo; último snapshot da janela tardia)
- extras de engenharia (não usados para calibrar): r50/r80/r90, crystallinity, M1/M2/M3, largura do pico em células

L2 de ρ tardio: N=96 reamostrado para N=64 (trilinear periódico) contra o ρ tardio de Q01a N=64, se ambos finitos. Entre células N=64 (só dt muda) o L2 é na grade nativa. Se a reamostragem falhar, declara-se omitida — não se inventa o número.

## k* vs Nyquist (pré-declarado)

Q01a deixou k* no canto de Nyquist de cada grade: $k_{\mathrm{Nyq}}=\pi\sqrt{3}/dx$.

Para N=96: $dx=32/96=1/3$, $k_{\mathrm{Nyq}}=3\pi\sqrt{3}\approx 16.3246$.

Medir k* tardio de N96_dt0 e declarar se ainda está no Nyquist (diferença relativa a $k_{\mathrm{Nyq}}$ < 5%, ou máximo da malha radial). Isso **não** autoriza mudar Theta nem dropar a célula.

## Análise pré-declarada

Comparar médias da janela tardia. Overlay obrigatório contra Q01a N=64 dt0.

Definições operacionais (antes de ver o resultado):

- ε_num espacial (Q01b): máximo da diferença relativa |A−B|/max(|A|,|B|) das médias tardias de peak, PR, R_rms entre **Q01a N=64 dt0** e **N96_dt0**
- ε_num temporal (Q01b): máximo da mesma diferença entre **Q01a N=64 dt0** e **N64_dt0q** (dt0/4); reportar também os pares sucessivos dt0 vs dt0/2 e dt0/2 vs dt0/4
- ε_num Q01a (já medido, não se recalcula a regra): 0.1944 (N=48 vs N=64, dt0)

Critério de veredito (só numérico; **nunca** SUPPORTED para MQ):

- NaN ou blowup em uma célula: essa célula = `NUMERICAL_FAILURE`; o run é **guardado**. Se qualquer célula requerida falha assim, o lote = `NUMERICAL_FAILURE`
- divergência wild (diferença relativa > 50% em peak/PR/R_rms no par espacial ou no par temporal dt0 vs dt0/4): `NUMERICAL_FAILURE`
- se ε_num espacial **e** ε_num temporal são ambos **menores** que ε_num Q01a (0.194) e nenhum dos dois pares diverge wildly: veredito textual **ε_num improved** (ainda não é convergência apertada; ainda não é MQ)
- caso contrário, sem falha catastrófica: `INCONCLUSIVE` (grade/dt ainda não fecharam; k* no Nyquist em N=96 pesa para inconclusivo mesmo se os escalares melhorarem só de um lado)

k* preso ao Nyquist em N=96 é evidência de espectro ainda grid-locked. Não se recalibra k*. Não se compara com MQ.

Qualquer estrutura que permaneça em 1–2 células enquanto N aumenta é **suspeita de artefato** (blueprint Q01 / Q31). Isso não autoriza dropar uma grade.

## Exclusão técnica

**Apenas** NaN ou blowup (não-finito / overflow). Nenhum run é descartado por ser “feio”, por encher o volume, ou por não parecer MQ. Célula que NaN-ou é guardada e marcada `NUMERICAL_FAILURE`.

## Comparação com QM

**Nenhuma.** Este experimento não compara com mecânica quântica. A pergunta é só: o erro numérico melhorou ao refinar N e dt?

## Linguagem operacional

- volume preenchido = universo, não ruído
- 1 gaussiana = 1 átomo
- CAOS → EQUILÍBRIO DINÂMICO (janela tardia = último 20% de T, já fixada em Q00)
- SEM ISOLAR / SEM FALSIFICAR / SEM CALIBRAR

## Hash deste protocolo

Preenchido na gravação. Depois disto, o arquivo não muda.
