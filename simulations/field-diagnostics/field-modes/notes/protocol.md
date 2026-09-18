---
tags: [triad, qm, q03, subespacos, protocolo]
aliases: [Q03, Q03_subespacos]
status: frozen-protocol
data: 2026-08-21
canonical: TRIAD_QM_CANONICAL_V1
---

# Q03 — Protocolo: identificação de subespaços persistentes (POD/PCA + DMD, análise passiva)

Criado **antes** dos runs (2026-08-21, America/Sao_Paulo). Depois do hash, este arquivo **não é editado**. Correções gerariam `PROTOCOL_v2.md`.

Fonte canônica: [TRIAD_QM_CANONICAL_V1](../../../../docs/reference/records/triad-qm-canonical-v1.md) (Q00, congelado). Blueprint: [TRIAD_QM_BLUEPRINT](../../../../docs/reference/records/triad-qm-blueprint.md) § Q03.
Q01a/Q01b: `QM/Q01_convergencia/`, `QM/Q01b_dt_N/`. Q02: `QM/Q02_ensemble/` (`PROTOCOL_v2`, backend mlx).
**Não** se edita o PROTOCOL.md / PROTOCOL_v2.md de Q00/Q01/Q02.

Q02 salvou métricas, **não** snapshots de campo. Q03 precisa de Ψ(t). Mesma física, observação mais densa (N_num), **não** lei nova.

Métodos (POD/PCA + DMD) são **sensores**. **Não** controlam o solver. Snapshots nunca reentram no passo. Modos POD **nunca** são realimentados na dinâmica.

**Nunca** chamar este lote de SUPPORTED para MQ.

## Pergunta

A dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?

Esta questão é **apenas** identificação passiva de estrutura de baixa dimensão no campo completo.

- **Não** há comparação com mecânica quântica.
- **Não** se isola termo algum.
- **Não** se altera `Theta_core`.
- **Não** se escolhe seed. Seeds 0, 1, 2, 3 **nessa ordem** (as quatro primeiras de Q02). Nenhuma seed é dropada por ser feia, por preencher a caixa, por modos “feios”, ou por “não parecer MQ”.
- Nenhum veredito `SUPPORTED` para MQ é possível neste experimento.
- A janela early **não** promove o átomo moribundo a estado de MQ. O veredito oficial de Q03 é o da janela late (atrator).

## O que não muda

- `Theta_core` congelado em Q00 (igual Q02)
- L, N, dt, T, condição inicial, V_ext, modo Strang, lock FDT
- 1 gaussiana = 1 átomo (I0; não é varredura de CI)
- Pilotos 1–34 **não** são confirmatórios e **não** entram como evidência
- Janela tardia Q00 = último 20% de T (t ≥ 6.4) — Q03 **mede** nessa janela; **não** redesenha a lei nem move a janela depois de olhar EV8
- Janela early t ≤ 0.2 pré-declarada (átomo ainda visível / morrendo — medição, não janela “bonita”)
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

`kT=1.0` é o banho canônico do freeze Q00. O campo que preenche o volume **é o universo**, não ruído a filtrar. Átomos **não** “morreram no banho”. Q02 já mostrou: caixa enche em t=0.1 em 32/32, peak tardio ~3.89, R_rms=16. Q03 **não** “conserta” isso.

## Ambiente (N_num, não física — mesma célula de trabalho Q01a N=64, NÃO calibração)

| quantidade | valor |
|---|---|
| L | 32 |
| N | 64 |
| dt | 0.0025 |
| T | 8 |
| seeds | 0, 1, 2, 3 (nessa ordem; primeiras quatro de Q02; nenhuma dropada por estética) |
| y_j(0) | 0 |
| V_ext | 0 (caixa livre periódica) |
| CI | 1 gaussiana = 1 átomo, spec §9.1, s=0.5, k0=0, norma=1 |
| precisão campo | complex64 |
| precisão memória | float32 |
| backend | mlx GPU (Device gpu, 0). Neural Engine **não** é usado. |
| domínio | [-L/2, L/2)³, BC periódicas |

N=64 / dt=0.0025 / T=8 / L=32 é a célula de trabalho de Q01a, **não** uma calibração.

Lote exploratório em fp32/complex64 (igual Q02 PROTOCOL_v2). Este lote **nunca** é SUPPORTED para MQ.

Se mlx estiver quebrado (não-finito irrecuperável / API ausente), fallback explícito para **numpy fp32 / complex64** (mesma classe de precisão; **não** fp64) e registrar `backend=numpy` — **não** silencioso.

## Convenção FDT (igual a Q02)

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

`half_lin` e a CI são construídos em numpy (mesmas fórmulas do Q02) e enviados ao GPU em complex64 / float32.

| arquivo | SHA-256 |
|---|---|
| Q02 `code/run_q02.py` (passo Strang reutilizado; **não** se muda) | `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365` |
| canônico Q00 `TRIAD_QM_CANONICAL_V1.md` | `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e` |
| Q02 PROTOCOL_v2 | `bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c` |

O runner `run_q03.py` é escrito **depois** deste protocolo. O SHA-256 do arquivo executado entra em `config.json` / `result.json` / `SHA256SUMS.txt`. Este PROTOCOL **não** é editado para incluir esse hash.

Python: `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3`.
mlx 0.32.0, device padrão GPU. Sem complex128 no mlx; campo em complex64, memória em float32.

## Seeds

0, 1, 2, 3 **nessa ordem**. Primeiras quatro de Q02. Sem descarte estético. Sem cherry-pick. Sem “essa seed não parece MQ”. Sem dropar porque os modos “estão feios”.

Exclusão técnica **apenas**: NaN ou blowup (não-finito / overflow). A seed falha **ainda é registrada** (`finite=false`, `blow_t`).

## Observação (N_num)

- seeds 0–3
- backend mlx GPU complex64
- cadência de snapshot: a cada 8 passos (Δt=0.02) na trajetória **inteira** (t=0..8) → 401 snapshots/seed
  (64³ complex64 ≈ 2 MB × 401 ≈ 800 MB/seed; gravar cada seed em disco como memmap float32/complex64 ou npz comprimido; **não** manter 4 seeds em RAM ao mesmo tempo)
- métricas padrão a cada 40 passos, iguais a Q02
- após POD/DMD da seed, o memmap grande de Ψ **pode** ser apagado se o disco apertar; arrays derivados (valores singulares, c_n(t), φ_0, overlaps) **ficam**

Arquivos brutos por seed (em `/tmp/Q03_subespacos/out/raw/`):

- `seedXX_psi_t.npy` — complex64, shape `(n_snap, N, N, N)` memmap (apagável após análise da seed)
- `seedXX_t.npy` — tempos dos snapshots
- `seedXX_metrics.csv` — métricas estilo Q02

## Análise passiva (não controla o solver)

Duas janelas, **ambas pré-declaradas** (não se escolhe a bonita depois):

- **A. early:** t ≤ 0.2  (átomo ainda visível / morrendo — medição, não janela “bonita”)
- **B. late:** t ≥ 6.4  (universo preenchido; janela Q00)

Com Δt_snap=0.02: early tem 11 snapshots (t=0, 0.02, …, 0.2); late tem 81 snapshots (t=6.4, 6.42, …, 8.0).

### Por janela, por seed

1. Montar a matriz de snapshots do campo empilhado real-imag: [Re Ψ; Im Ψ], shape `(2 N³, n_snap)`, **subtrair a média temporal** da janela.
2. POD econômico via SVD da matriz de Gram `n_snap × n_snap` (G = Xᵀ X). **Não** formar a matriz `2 N³ × 2 N³`.
3. Reportar σᵢ² / Σσ² para i=1..16 (variância explicada). Se n_snap < 16, reportar até n_snap−1 (média já removida).
4. Erro relativo L2 de reconstrução dos snapshots centrados usando r=1, 2, 4, 8 modos: ‖X − X_r‖_F / ‖X‖_F.
5. Coeficientes: a SVD real do empilhamento produz c_n(t) reais, com c_n(t_k) = σ_n V_{k n} = ⟨φ_n^{stack} | x(t_k)⟩ (produto interno real no vetor empilhado). Modos espaciais são reconstituídos como campos complexos φ = φ_re + i φ_im. Produto interno complexo, quando usado (overlaps): ⟨a|b⟩ = Σ conj(a) b · dV, com dV = dx³. Convenção **declarada e consistente**: POD/recon/c_n usam o produto real do empilhamento; overlaps (IC e entre seeds) usam o produto complexo no campo φ normalizado em L2 (∫|φ|² dV = 1).
6. Persistência: std(|c_n|) / mean(|c_n|) na janela para n=0, 1, 2; tempo de autocorrelação de |c_0| (primeiro lag em que acf < 1/e, em unidades de tempo), ou “undefined” se mean(|c_0|) ~ 0 (limiar 1e-30).
7. Overlap do modo líder φ_0 com o átomo gaussiano de t=0 (normalizado |⟨φ_0|Ψ(0)⟩|). Declarado para **as duas** janelas.

|c_0(t)| na trajetória **inteira** é a projeção de Ψ(t) − mean_late sobre o φ_0 da janela late da mesma seed (coordenada no atrator). Isso é sensor, não controle.

### Entre seeds (mesma janela)

- Overlap absoluto |⟨φ_0^{seed i}|φ_0^{seed j}⟩| para todos os pares. Fase/sinal global: tomar o máximo sobre a fase global e^{iθ} — o módulo do produto complexo já realiza esse máximo.
- Média dos overlaps pairwise de φ_0 (pares i<j).

### DMD (somente janela late, seed 0 e seed 1 — suficiente, pré-declarado)

- SVD-DMD padrão nos **mesmos** snapshots late centrados (empilhamento real-imag).
- Reportar |λ| dos 8 autovalores DMD líderes (persistência se |λ|≈1; decaimento se |λ|≪1).
- **Não** sintonizar o posto depois de ver resultados: `r_dmd=8` fixo **antes** de rodar.
- Ordenar os 8 autovalores por |λ| decrescente para o relatório.

### Reprodução Q02

Reportar peak / PR / R_rms / norm da janela late (média por seed, t ≥ 6.4) para checar reprodutibilidade Q02 nestas 4 seeds. Q03 **não** “conserta” o preenchimento da caixa.

## Vereditos pré-declarados (não mover depois)

Aplicar **SEPARADAMENTE** à janela A (early) e à janela B (late). O veredito oficial de Q03 é o da janela late (o atrator); early entra só como contexto.

Seja EV8 = fração de variância nos 8 primeiros modos POD (média entre seeds finitas).
Seja Rec8 = erro relativo L2 de reconstrução com r=8 (média entre seeds).
Seja Ov = overlap pairwise médio de |⟨φ_0^i|φ_0^j⟩| entre seeds.

- Se >1 de 4 seeds NaN/blowup: **NUMERICAL_FAILURE**
- Janela late:
  * EV8 ≥ 0.50 AND Rec8 ≤ 0.30 AND Ov ≥ 0.50 → **PARTIAL** (subespaço candidato no atrator)
  * EV8 < 0.20 AND Rec8 > 0.50 → **NOT_SUPPORTED** (o atrator não tem estrutura de “estado” de posto baixo; universo preenchido é alta dimensão)
  * caso contrário → **INCONCLUSIVE**
- A janela early reporta os mesmos números mas **NÃO** define o veredito oficial (não se promove o átomo moribundo a estado de MQ).
- **NUNCA** SUPPORTED para MQ.
- Nunca dropar uma seed porque os modos parecem feios.
- Nunca mudar Theta_core nem mover janelas depois de ver EV8.

Vereditos permitidos neste experimento: `PARTIAL` / `NOT_SUPPORTED` / `INCONCLUSIVE` / `NUMERICAL_FAILURE`. Este experimento **não pode** ser `SUPPORTED` para MQ (`supported_for_qm=false` sempre).

## Exclusão técnica

**Apenas** NaN ou blowup (não-finito / overflow). Nenhum run é descartado por ser “feio”, por encher o volume, por modos feios, ou por não parecer MQ. Seed que NaN-ou é guardada (CSV parcial) e marcada `finite=false`.

## Comparação com QM

**Nenhuma.** Este experimento não compara com mecânica quântica. A pergunta é só: a dinâmica completa produz modos/coordenadas macroscópicas que mantêm identidade suficiente para serem tratados como estados?

## Linguagem operacional

- 1 gaussiana = 1 átomo
- volume preenchido = universo, NÃO ruído / NÃO “átomos morreram no banho”
- SEM ISOLAR / SEM FALSIFICAR / SEM CALIBRAR
- CAOS → EQUILÍBRIO DINÂMICO (janela tardia = último 20% de T, já fixada em Q00)
- Pilotos 1–34 não confirmatórios
- kT=1 é o banho canônico
- backend mlx GPU fp32 é N_num, não física
- snapshots são sensores; POD/DMD não controlam o solver

## Figuras pré-declaradas (rótulos em PT; sem “ruído/átomos morreram”)

- `ev_spectrum.png` — variância explicada vs índice do modo, early vs late, média±std entre seeds
- `recon_error.png` — Rec(r) vs r para early vs late
- `c0_time.png` — |c_0(t)| das 4 seeds (t completo), marcas em t=0.2 e t=6.4
- `mode0_slice.png` — plano médio |φ_0| da seed 0, janela early E late (2 painéis)
- `dmd_eigs.png` — |λ| dos 8 modos DMD, seeds 0 e 1
