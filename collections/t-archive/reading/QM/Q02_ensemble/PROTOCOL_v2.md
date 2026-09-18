> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q02_ensemble/PROTOCOL_v2.md) · [Collection / Acervo](../../../README.md)

```yaml
tags: [triad, qm, q02, ensemble, protocolo, v2]
aliases: [Q02_v2, Q02_ensemble_v2]
status: frozen-protocol-v2
data: 2026-08-21
canonical: TRIAD_QM_CANONICAL_V1
supersedes: PROTOCOL.md (v1) ONLY for N_num backend/precision
```


# Q02 — Protocolo v2: ensemble caótico de referência (32 seeds, 1 átomo, mlx GPU)

Criado **antes** dos runs (2026-08-21, America/Sao_Paulo). Depois do hash, este arquivo **não é editado**. Correções gerariam `PROTOCOL_v3.md`.

Este v2 **substitui o v1 somente em N_num**: backend e precisão. `Theta_core`, CI, seeds 0–31, L/N/dt/T, passo Strang, convenção FDT, observáveis e regras de veredito são **os mesmos** do v1.

O v1 (`PROTOCOL.md`, numpy/fp64) permanece como congelamento histórico. Não se edita o v1.

Fonte canônica: [TRIAD_QM_CANONICAL_V1](../../Fontes/TRIAD_QM_CANONICAL_V1.md) (Q00, congelado). Blueprint: [TRIAD_QM_BLUEPRINT](../../Fontes/TRIAD_QM_BLUEPRINT.md) §12 / Q02.
Q01a (grade de trabalho N=64): [Q01](../Q01_convergencia/Q01.md) em `QM/Q01_convergencia/`. Q01b: `QM/Q01b_dt_N/`. **Não** se edita o PROTOCOL.md de Q01a/Q01b/Q02 v1.

Q00 permite «numpy ou metal se for o mesmo passo; registrar qual». Isto é **N_num**, não calibração. Lote exploratório (seeds 0–31) pode ser fp32. Lote confirmatório (seeds 1000+) permanece fp64 mais tarde. **Nunca** chamar este lote de SUPPORTED para MQ.

## Pergunta

Qual é a distribuição natural de comportamentos do substrato **sem escolher uma seed bonita**?

Mesmo macroestado físico (1 gaussiana = 1 átomo), tríade **completa** (NLS+memória+FDT), `Theta_core` congelado em Q00, N=64 da célula de trabalho de Q01a. A única diferença entre membros é a seed do gerador FDT.

Esta questão é **apenas** a variabilidade natural do substrato.

- **Não** há comparação com mecânica quântica.
- **Não** se isola termo algum.
- **Não** se altera `Theta_core`.
- **Não** se escolhe seed. Seeds 0,1,2,…,31 **nessa ordem**. Nenhuma seed é dropada por ser feia, por preencher a caixa, ou por “não parecer MQ”.
- Nenhum veredito `SUPPORTED` para MQ é possível neste experimento.

## O que não muda

- `Theta_core` congelado em Q00
- L, N, dt, T, condição inicial, V_ext, modo Strang, lock FDT
- 1 gaussiana = 1 átomo (I0; não é varredura de CI)
- Pilotos 1–34 **não** são confirmatórios e **não** entram como evidência
- Janela tardia = último 20% de T (t ≥ 6.4), já fixada em Q00 — Q02 **mede** se essa janela é empiricamente ok; **não** redesenha a lei nem move a janela depois de olhar “parecença com MQ”
- kT=1 é o banho canônico. Não se retoca.

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

`kT=1.0` é o banho canônico do freeze Q00. O campo que preenche o volume **é o universo**, não ruído a filtrar. Átomos **não** “morreram no banho”.

## Ambiente (N_num, não física — mesma célula de trabalho Q01a N=64, NÃO calibração)

Única mudança vs v1: backend e precisão.

| quantidade | valor |
|---|---|
| L | 32 |
| N | 64 |
| dt | 0.0025 |
| T | 8 |
| seeds | 0,1,2,…,31 (nessa ordem; nenhuma dropada por estética) |
| y_j(0) | 0 |
| V_ext | 0 (caixa livre periódica) |
| CI | 1 gaussiana = 1 átomo, spec §9.1, s=0.5, k0=0, norma=1 |
| precisão campo | complex64 |
| precisão memória | float32 |
| backend | mlx GPU (Device gpu, 0). Neural Engine **não** é usado (inference ML, não FFT). |
| domínio | [-L/2, L/2)³, BC periódicas |

N=64 / dt=0.0025 / T=8 / L=32 é a célula de trabalho de Q01a, **não** uma calibração. Se um membro for lento, o run **não** é abandonado e **nenhuma** seed é dropada para “ficar melhor”.

Lote exploratório (seeds 0–31) em fp32/complex64. Confirmatório (seeds 1000+) fica fp64 mais tarde. Este lote **nunca** é SUPPORTED para MQ.

## Convenção FDT (igual ao v1)

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

`rng = numpy.random.default_rng(seed)` por membro. A seed é a **única** diferença entre membros.

O ruído FDT é **sorteado em numpy** com esse RNG e depois enviado ao GPU (`mx.array`, complex64). A política de seeds não muda. Não se sorteia no gerador do MLX.

## Solver

Dinâmica completa 3D Strang, standalone (spec §3 + §5), **o mesmo passo** que `Fontes/run_q01a.py`, executado em mlx GPU:

1. `psi = ifftn(fftn(psi) * half_lin)`
2. `rho = |psi|^2`
3. `V = Lambda*rho + sum_j lam_j y_j`  (V_ext = 0)
4. `psi *= exp(-i V dt / hbar)`  (cos/sin se `mx.exp` complexo for instável)
5. `y += dt * nu * (rho - y)`  (Euler)
6. `psi += noise_amp * xi`  (xi de numpy rng, upload complex64)
7. `psi = ifftn(fftn(psi) * half_lin)`
8. `mx.eval` após cada passo

Não usa triad-lang `TriadParams` (esse tipo rejeita 3 modos + Gamma).

`half_lin` e a CI são construídos em numpy (mesmas fórmulas do Q01a) e enviados ao GPU em complex64 / float32.

| arquivo | SHA-256 |
|---|---|
| `Fontes/run_q01a.py` (motor Strang de referência) | `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64` |
| canônico Q00 `TRIAD_QM_CANONICAL_V1.md` | `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` |
| Q02 PROTOCOL v1 (histórico numpy/fp64, arquivo completo) | `a2024aff5e29c484ed781f6972d1699f4657997072c528333f1268b95cb648af` |

O runner `run_q02.py` é escrito **depois** deste protocolo. O SHA-256 do arquivo executado entra em `config.json` / `result.json` / `SHA256SUMS.txt`. Este PROTOCOL_v2 **não** é editado para incluir esse hash.

Python: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`.
mlx 0.32.0, device padrão GPU. Sem complex128 no mlx; campo em complex64, memória em float32.

Se mlx estiver quebrado (não-finito irrecuperável / API ausente), fallback explícito para numpy fp64, registrado como `backend=numpy` em analysis — **não** silencioso.

## Seeds

0, 1, 2, …, 31 **nessa ordem**. Sem descarte estético. Sem cherry-pick. Sem “essa seed não parece MQ”.

Exclusão técnica **apenas**: NaN ou blowup (não-finito / overflow). A seed falha **ainda é registrada** (`finite=false`, `blow_t`).

## Observáveis (passivos, iguais a Q01a / v1)

Registrados ao longo de t (a cada 40 passos = Δt=0.1) e, na **janela tardia** (último 20% de T, t ≥ 6.4, já congelada em Q00): média e desvio **por seed**.

- norma
- peak (ρ_max)
- PR (participação)
- R_rms
- k_*
- k_* L
- Vmem_peak
- crystallinity
- extras de engenharia (não usados para calibrar): r50/r80/r90, M1/M2/M3, peak_n_cells_half, peak_width_phys, finite

Observáveis calculados em CPU numpy após puxar `psi`/`y` do GPU, ou no GPU com `.item()`. Sem ρ-campo obrigatório neste lote.

## Análise pré-declarada (ANTES de ver resultados)

**Iguais ao v1.** Declarada agora. Não se redesenha depois de olhar os números, e **não** se move a janela Q00 por “parecença com MQ”.

### Por seed

Média ± desvio da janela tardia (t ≥ 0.8 T = 6.4) de: peak, PR, R_rms, norm, k*, Vmem_peak, crystallinity.

### Entre seeds (variabilidade natural)

Média, desvio, mínimo, máximo, mediana **das médias tardias** de cada observável acima. Isso é a distribuição natural do substrato neste macroestado.

### Transiente empírico (medição, não lei nova)

Para cada seed finita:

1. `R_rms_late` = média de R_rms na janela tardia.
2. Primeiro t tal que `|R_rms(t) − R_rms_late| < 0.05 · |R_rms_late|` **e permanece** assim até T (todos os registros seguintes satisfazem a desigualdade). Se nunca assenta: declarar `t_settle = never`.
3. Também: primeiro t em que `R_rms > 0.9 · (L/2)` (`t_fill`). Se nunca: `never`.

Reportar mediana / min / max de `t_settle` e de `t_fill` entre seeds finitas. Q00 usou transiente provisório t < 0.8 T; Q02 **mede** se isso é empiricamente ok. **Não** vira lei nova. **Não** se move a janela.

### Caixa preenchida = universo

Fração de seeds finitas com `R_rms_late ≈ L/2 ± 1` (isto é `|R_rms_late − 16| ≤ 1`). Volume preenchido = universo, **não** ruído, **não** “átomos morreram no banho”.

### Fração finita / blowup

`n_finite` / 32 e `n_blowup` / 32. Seeds NaN/blowup listadas, **não** escondidas.

### Distribuição de peak_late

Histograma das médias tardias de peak. Anti-colapso: singularidade finita (peak_max global ao longo de todos os t e seeds). Reportar `peak_max_global`, t e seed.

### k* vs Nyquist

N=64, dx = L/N = 0.5.

$$
k_{\mathrm{Nyq}} = \pi\sqrt{3}/dx \approx 10.8828
$$

Nota se k* está grid-locked como em Q01 (preso ao Nyquist / a um bin espectral). **Não** se recalibra k*. **Não** se compara com MQ.

### Regras de veredito (declaradas agora — iguais ao v1)

- Se ≥ 30/32 finitas **e** as médias tardias de R_rms / peak / PR têm distribuição bem definida (std finito, não-NaN): ensemble OK → **INCONCLUSIVE** para MQ (esperado; Q02 **não** é teste de MQ) e reportar os números empíricos.
- Se > 4 seeds NaN/blowup: **NUMERICAL_FAILURE**.
- **Nunca** `SUPPORTED` para MQ.
- **Nunca** dropar seeds feias.
- Outros casos (p.ex. 28–29 finitas, std finito): **PARTIAL** ou **INCONCLUSIVE**, com a fração finita declarada — ainda **não** é MQ.

Vereditos permitidos neste experimento: `SUPPORTED` / `PARTIAL` / `NOT_SUPPORTED` / `INCONCLUSIVE` / `NUMERICAL_FAILURE` — mas este experimento **não pode** ser `SUPPORTED` para MQ (`supported_for_qm=false` sempre).

## Exclusão técnica

**Apenas** NaN ou blowup (não-finito / overflow). Nenhum run é descartado por ser “feio”, por encher o volume, ou por não parecer MQ. Seed que NaN-ou é guardada (CSV parcial) e marcada `finite=false`.

## Comparação com QM

**Nenhuma.** Este experimento não compara com mecânica quântica. A pergunta é só: qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?

## Linguagem operacional

- 1 gaussiana = 1 átomo
- volume preenchido = universo, NÃO ruído / NÃO “átomos morreram no banho”
- SEM ISOLAR / SEM FALSIFICAR / SEM CALIBRAR
- CAOS → EQUILÍBRIO DINÂMICO (janela tardia = último 20% de T, já fixada em Q00; transiente empírico é medição)
- Pilotos 1–34 não confirmatórios
- kT=1 é o banho canônico
- backend mlx GPU fp32 é N_num, não física

## Hash deste protocolo

Congelado na gravação. Depois disto, o arquivo não muda. Bugs → `PROTOCOL_v3.md`, nunca editar este v2.

SHA-256 (conteúdo acima, antes desta linha): `4f7883f2abf3797d4353d0413138c39d460d7dfcb80bdae591a7bf970ff44f97`
