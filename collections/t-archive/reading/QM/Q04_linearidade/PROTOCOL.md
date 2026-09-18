> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/QM/Q04_linearidade/PROTOCOL.md) · [Collection / Acervo](../../../README.md)

```yaml
tags: [triad, qm, q04, linearidade, protocolo]
aliases: [Q04, Q04_linearidade]
status: frozen-protocol
data: 2026-08-21
canonical: TRIAD_QM_CANONICAL_V1
```


# Q04 — Protocolo: linearidade efetiva / superposição (campo + plano dos 2 átomos)

Criado **antes** dos runs (2026-08-21, America/Sao_Paulo). Depois do hash, este arquivo **não é editado**. Correções gerariam `PROTOCOL_v2.md`.

Fonte canônica: [TRIAD_QM_CANONICAL_V1](../../Fontes/TRIAD_QM_CANONICAL_V1.md) (Q00, congelado). Blueprint: [TRIAD_QM_BLUEPRINT](../../Fontes/TRIAD_QM_BLUEPRINT.md) § Q04 (Linearidade efetiva / superposição).
Q01a/Q01b: `QM/Q01_convergencia/`, `QM/Q01b_dt_N/`. Q02: `QM/Q02_ensemble/` (`PROTOCOL_v2`, backend mlx). Q03: `QM/Q03_subespacos/`.
**Não** se edita o PROTOCOL.md / PROTOCOL_v2.md de Q00/Q01/Q02/Q03.

**Nunca** chamar este lote de SUPPORTED para MQ.

## Pergunta

Existe um regime em que \(F_t(aA+bB) \approx a F_t(A) + b F_t(B)\) na dinâmica completa? Por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?

Esta questão é **apenas** o teste de superposição efetiva no campo completo (tríade NLS+memória+FDT). Sem comparação com mecânica quântica. Sem isolar termo. Sem alterar `Theta_core`. Sem cherry-pick de seed. Sem retocar kT. Sem promover o par visível/morrendo a qubit.

## Desvio explícito do blueprint (não esconder)

O blueprint Q04 ( [TRIAD_QM_BLUEPRINT](../../Fontes/TRIAD_QM_BLUEPRINT.md) § Q04 ) define

\[
R_{\mathrm{lin}}
=
\frac{\|\Pi F_t(aA+bB)-a\Pi F_t(A)-b\Pi F_t(B)\|}
{\|a\Pi F_t(A)\|+\|b\Pi F_t(B)\|}.
\]

depois de projetar no “mesmo subespaço efetivo” Π.

Q03 (atrator late, t ≥ 6.4) **não** entregou um subespaço compartilhado de posto baixo:

- EV8 late = 0.409447 (média seeds 0–3)
- Rec8 late = 0.768507
- overlap pairwise médio de φ₀ late = 0.046794

Π_POD late **não** é um espaço de estados compartilhado. Projetar Q04 nesse POD tornaria \(R_{\mathrm{lin}}\) sem sentido: Π não é um espaço de estados.

Teste **mais válido**, ainda a pergunta do blueprint (“a superposição sobrevive?”):

1. **Linearidade no campo**, com ruído FDT **idêntico** no triple (mesma seed RNG, mesma sequência de chamadas — o ruído do stepper Q02 é independente do campo).
2. **Vazamento do plano das CIs** de dois átomos: \(\Pi_0=\mathrm{span}\{G_A,G_B\}\), as duas gaussianas elas mesmas (1 gaussiana = 1 átomo). Este Π é **declarado antes do run**, não ajustado depois.
3. Também se reporta a fórmula do blueprint com \(\Pi=\Pi_0\) (plano dos átomos), para o rastro de papel ter \(R_{\mathrm{lin}}^{\Pi}\).

**Não** se usa o POD late de Q03 como Π. **Não** se muda `Theta_core`. **Não** se isolam termos. **Não** se retoca kT.

## O que não muda

- `Theta_core` congelado em Q00 (igual Q02/Q03)
- L, N, dt, T, V_ext, modo Strang, lock FDT
- 1 gaussiana = 1 átomo
- Pilotos 1–34 **não** são confirmatórios e **não** entram como evidência
- Janela tardia Q00 = último 20% de T (t ≥ 6.4) — Q04 **mede** nessa janela; **não** redesenha a lei nem move a janela depois de olhar \(R_{\mathrm{lin}}\)
- Números early (t=0.02, 0.10, 0.20) são **contexto / vida útil**; **não** definem o veredito oficial e **não** promovem o par moribundo a qubit
- kT=1 é o banho canônico. Não se retoca.
- Passo Strang idêntico ao de Q02 `code/run_q02.py` (SHA-256 `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`). **Não** se muda o passo.

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

`kT=1.0` é o banho canônico do freeze Q00. O campo que preenche o volume **é o universo**, não ruído a filtrar. Átomos **não** “morreram no banho”. Q02/Q03 já mostraram: caixa enche em t=0.1. Q04 **não** “conserta” isso.

## Ambiente (N_num, não física — mesma célula de trabalho Q01a N=64, NÃO calibração)

| quantidade | valor |
|---|---|
| L | 32 |
| N | 64 |
| dt | 0.0025 |
| T | 8 |
| seeds | 0, 1 (nessa ordem; as duas primeiras; nenhuma dropada por estética) |
| y_j(0) | 0 |
| V_ext | 0 (caixa livre periódica) |
| precisão campo | complex64 |
| precisão memória | float32 |
| backend | mlx GPU (Device gpu, 0). Neural Engine **não** é usado. |
| domínio | [-L/2, L/2)³, BC periódicas |

N=64 / dt=0.0025 / T=8 / L=32 é a célula de trabalho de Q01a, **não** uma calibração.

Lote exploratório em fp32/complex64 (igual Q02 PROTOCOL_v2). Este lote **nunca** é SUPPORTED para MQ.

Se mlx estiver quebrado (não-finito irrecuperável / API ausente), fallback explícito para **numpy fp32 / complex64** (mesma classe de precisão; **não** fp64) e registrar `backend=numpy` — **não** silencioso.

## Condição inicial (pré-declarada; ontologia existente / run 30 sep=6; NÃO sintonizada)

s = 0.5 (átomo Q00). k0 = 0. Norma L2 com dV = dx³.

| membro | campo em t=0 | centro | norma |
|---|---|---|---|
| A | gaussiana | x=−3, y=z=0 | 1 |
| B | gaussiana | x=+3, y=z=0 | 1 |
| S | (A+B) / ‖A+B‖_L2 | superposição igual | 1 |

Coeficientes (fixos **antes** do run; não se movem depois de ver \(R_{\mathrm{lin}}\)):

\[
a = b = \frac{1}{\|A+B\|_{L^2}}
\qquad\text{de modo que}\qquad
aA+bB = S \quad\text{em } t=0 \text{ exatamente}.
\]

1 gaussiana = 1 átomo. Isto **não** é varredura de CI. Posições ±3 e s=0.5 vêm da ontologia já usada (run 30, sep=6; átomo Q00). Não se escolhe depois para “ficar linear”.

## Regra de ruído idêntico (obrigatória)

O ruído FDT no stepper Q02 é **independente do campo**: um par `standard_normal` por passo, mesma amplitude.

Para cada membro do triple (A, B, S) de uma seed:

- `rng = numpy.random.default_rng(seed)` **independente** por membro
- mesma seed ⇒ mesma sequência η(t)
- cada membro **consome o RNG do mesmo jeito** (um par `standard_normal` por passo; upload complex64)

Isso é o controle: a diferença A vs B vs S é só a CI, não uma realização diferente do banho.

Seeds 0 e 1, nessa ordem. Sem cherry-pick. Sem “essa seed não parece MQ”.
São 6 evoluções (2 seeds × 3 membros). Sequencial em **um** GPU.

## Convenção FDT (igual a Q02)

Com `fdt_couple=True`:

$$
f_{\mathrm{FDT},e}=2\Gamma\,dx^{3}\,kT/\hbar
$$

Incremento por passo (spec eq. 4):

$$
\Psi\leftarrow\Psi+\sqrt{f_{\mathrm{FDT},e}\,dt/dx^{D}}\,(\xi+i\xi')/\sqrt{2}
$$

que reduz a \(\sqrt{2\Gamma\,kT\,dt/\hbar}\,(\xi+i\xi')/\sqrt{2}\).

Memória: Euler, porque \(\max_j \nu_j\,dt=0.025<0.05\) (spec §3.4).

O ruído FDT é **sorteado em numpy** com esse RNG e depois enviado ao GPU (`mx.array`, complex64). A política de seeds não muda. Não se sorteia no gerador do MLX.

## Solver

Dinâmica completa 3D Strang, standalone, **o mesmo passo** que `QM/Q02_ensemble/code/run_q02.py`:

1. `psi = ifftn(fftn(psi) * half_lin)`
2. `rho = |psi|^2`
3. `V = Lambda*rho + sum_j lam_j y_j`  (V_ext = 0)
4. `psi *= exp(-i V dt / hbar)`  (cos/sin se `mx.exp` complexo for instável)
5. `y += dt * nu * (rho - y)`  (Euler)
6. `psi += noise_amp * xi`  (xi de numpy rng, upload complex64)
7. `psi = ifftn(fftn(psi) * half_lin)`
8. `mx.eval` após cada passo

Não usa triad-lang `TriadParams`. Sequencial em **um** GPU.

`half_lin` e as CIs são construídos em numpy (mesmas fórmulas do Q02) e enviados ao GPU em complex64 / float32.

| arquivo | SHA-256 |
|---|---|
| Q02 `code/run_q02.py` (passo Strang reutilizado; **não** se muda) | `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365` |
| canônico Q00 `TRIAD_QM_CANONICAL_V1.md` | `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` |
| Q03 PROTOCOL.md | `f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16` |
| Q02 PROTOCOL_v2 | `bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c` |

O runner `run_q04.py` é escrito **depois** deste protocolo. O SHA-256 do arquivo executado entra em `config.json` / `result.json` / `SHA256SUMS.txt`. Este PROTOCOL **não** é editado para incluir esse hash.

Python: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`.
mlx 0.32.0, device padrão GPU. Sem complex128 no mlx; campo em complex64, memória em float32.

## Observáveis (sensores; nunca reentram no solver)

Registrados a cada 8 passos (Δt=0.02) em **todo** T=8 (401 instantes: t=0, 0.02, …, 8.0).

Depois que os três membros de uma seed existem:

### Linearidade de campo

\[
R_{\mathrm{lin}}^{\mathrm{field}}(t)
=
\frac{\|\Psi_S(t)-a\Psi_A(t)-b\Psi_B(t)\|_{L^2}}
{|a|\,\|\Psi_A(t)\|_{L^2}+|b|\,\|\Psi_B(t)\|_{L^2}}
\]

L2 com dV = dx³. Em t=0 **deve** ser ~0 (reportar; se não for, é bug).

### Plano Π₀ (declarado antes; Gram-Schmidt)

\(\Pi_0=\mathrm{span}\{A(0),B(0)\}\) ortonormalizado via Gram-Schmidt com produto interno complexo

\[
\langle u|v\rangle=\sum \overline{u}\,v\,dV.
\]

Não se ajusta Π depois do run. Não se usa POD de Q03.

Para \(X\in\{A,B,S\}\):

\[
\mathrm{leak}_X(t)=1-\frac{\|\Pi_0\Psi_X(t)\|^2}{\|\Psi_X(t)\|^2}.
\]

### Fórmula do blueprint com Π = Π₀

\[
R_{\mathrm{lin}}^{\Pi}(t)
=
\frac{\|\Pi_0\Psi_S(t)-a\Pi_0\Psi_A(t)-b\Pi_0\Psi_B(t)\|}
{|a|\,\|\Pi_0\Psi_A(t)\|+|b|\,\|\Pi_0\Psi_B(t)\|}.
\]

### Métricas usuais (por membro)

norma, peak (ρ_max), PR, R_rms — iguais em espírito a Q02. Não controlam o solver.

### pair_sep (somente S)

Separação dos dois picos de densidade em S, **enquanto dois blobs forem encontráveis** (mesmo espírito do run 30: máximos locais + n_det==2). Se não forem encontráveis: **omitido** (NaN). **Não** se inventa pair_sep.

### Vidas úteis (contexto, não veredito)

- \(t_{1/2}\): primeiro t com \(R_{\mathrm{lin}}^{\mathrm{field}}>0.5\). Se nunca: \(t_{1/2}=\infty\).
- \(t_{\mathrm{leak}}\): primeiro t com \(\mathrm{leak}_S>0.5\). Se nunca: \(\infty\).

## Vereditos pré-declarados (não mover depois)

Oficial = média da janela **late** de \(R_{\mathrm{lin}}^{\mathrm{field}}\) (t ≥ 6.4), depois média sobre seeds **finitas**.

- Se >1 de 2 seeds NaN/blowup: **NUMERICAL_FAILURE**
- Média late \(R_{\mathrm{lin}}^{\mathrm{field}} < 0.20\) → **PARTIAL** (linearidade emergente no atrator — inesperado)
- Média late \(R_{\mathrm{lin}}^{\mathrm{field}} > 0.50\) → **NOT_SUPPORTED** (sem superposição efetiva no universo preenchido)
- senão → **INCONCLUSIVE**
- Números early (t=0.02, 0.10, 0.20) são CONTEXTO / vida útil; **não** definem o veredito oficial e **não** promovem o par moribundo a qubit
- **NUNCA** SUPPORTED para MQ
- Não se movem janelas nem a, b depois de ver \(R_{\mathrm{lin}}\)
- Nunca dropar seed por ser “feia”, por encher a caixa, ou por “não parecer MQ”

Vereditos permitidos neste experimento: `PARTIAL` / `NOT_SUPPORTED` / `INCONCLUSIVE` / `NUMERICAL_FAILURE`. Este experimento **não pode** ser `SUPPORTED` para MQ (`supported_for_qm=false` sempre).

## Exclusão técnica

**Apenas** NaN ou blowup (não-finito / overflow). Nenhum run é descartado por ser “feio”, por encher o volume, ou por não parecer MQ. Seed que NaN-ou é guardada (CSV parcial) e marcada `finite=false`.

## Comparação com QM

**Nenhuma.** Este experimento não compara com mecânica quântica. A pergunta é só: existe um regime em que a dinâmica completa respeita aproximadamente a superposição, e por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?

## Linguagem operacional

- 1 gaussiana = 1 átomo
- volume preenchido = universo, NÃO ruído / NÃO “átomos morreram no banho”
- SEM ISOLAR / SEM FALSIFICAR / SEM CALIBRAR
- CAOS → EQUILÍBRIO DINÂMICO (janela tardia = último 20% de T, já fixada em Q00)
- Pilotos 1–34 não confirmatórios
- kT=1 é o banho canônico
- backend mlx GPU fp32 é N_num, não física
- snapshots / sensores nunca controlam o solver
- Π = plano dos 2 átomos (CI), **não** POD late de Q03

## Figuras pré-declaradas (rótulos em PT; sem “ruído/átomos morreram”)

- `rlin_time.png` — \(R_{\mathrm{lin}}^{\mathrm{field}}\) e \(R_{\mathrm{lin}}^{\Pi}\) vs t, ambas as seeds; marcas em t=0.2 e t=6.4
- `leak_time.png` — leak_A, leak_B, leak_S vs t
- `slices_t0_t01.png` — plano médio |Ψ| de A, B, S em t=0 e t=0.1 (2×3)
- `late_rlin_bar.png` — média late de \(R_{\mathrm{lin}}^{\mathrm{field}}\) por seed

## Hash deste protocolo

Congelado na gravação. Depois disto, o arquivo não muda.
O SHA-256 é calculado sobre **este arquivo inteiro** (como Q03). O valor entra em `analysis.md` / `result.json` / `Q04.md`. Este PROTOCOL **não** é editado para incluir esse hash.
