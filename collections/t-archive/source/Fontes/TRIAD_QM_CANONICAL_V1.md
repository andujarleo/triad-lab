---
tags: [triad, qm, q00, canônico]
aliases: [TRIAD_QM_CANONICAL_V1, Theta_core, Q00]
status: frozen
data: 2026-08-21
---

# TRIAD_QM_CANONICAL_V1

Congelado em Q00, **antes** de qualquer benchmark quântico confirmatório.
Depois deste arquivo, `Theta_core` não muda porque um teste de MQ não bateu.
Fonte do programa: [[TRIAD_QM_BLUEPRINT]]. PDE: [[triad_equation_reference]] · [[Equação de referência]].

Runs 1–29 são **pilotos** (§13 do blueprint), não dados confirmatórios.

## 1. Equação exata

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

Todos os termos ativos em todo run que conta como evidência. Sem ablação.

## 2. Hash do solver

| arquivo | SHA-256 |
|---|---|
| `Fontes/solver.py` | `6cc2c128b135f28ffa7c1a8b37198a9d20e8bf84003765d7f5e80d12311dcf8b` |
| `Fontes/run_R5_A2.py` (Strang 3D da spec, piloto) | `c9dbe725452b3fb9d419d14ed31d0e6c7f8138691f2c2e9c19845448e2ebaeab` |

Motor dos benchmarks: dinâmica completa 3D Strang, fp64, `fdt_couple=True`. Testes de FFT isolados ficam em `solver_validation/` e **não** são evidência física.

## 3. Theta_core — congelado

Origem: candidato pré-quântico do blueprint §5.1, o regime bounce/anti-colapso já no registro (#23 / #27), **não** escolhido para parecer MQ.

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

`kT=1.0` é o banho canônico deste freeze. O campo que preenche o volume **é o universo**, não ruído a filtrar.

## 4. Convenção FDT

Com `fdt_couple=True`:

$$
f_{\mathrm{FDT},e}=2\Gamma\,dx^{D}\,kT/\hbar
$$

Incremento por passo (spec eq. 4):

$$
\Psi\leftarrow\Psi+\sqrt{f_{\mathrm{FDT},e}\,dt/dx^{D}}\,(\xi+i\xi')/\sqrt{2}
$$

que reduz a $\sqrt{2\Gamma\,kT\,dt/\hbar}\,(\xi+i\xi')/\sqrt{2}$.

## 5. Unidades

Internas/naturais. $\hbar=m=1$. Sem conversão SI neste programa. Qualquer mapa de unidades, se um dia existir, é único e posterior a Q00.

## 6. Dimensionalidade

$D=3$, domínio $[-L/2,L/2)^3$, BC periódicas. $L$ é `N_num`/`Xi_env` (caixa), não `Theta_core`. Default de caixa para Q01: $L=32$ (mesmo box do regime bounce pré-quântico).

## 7. Equilíbrio dinâmico

Definição operacional **provisória** (Q02 pode só *medir* transiente/janela, não redesenhar a lei):

- transiente: $t < 0.8\,T$
- janela de equilíbrio: último 20% de $T$
- reportar média e desvio de $\rho_{\max}$, PR, $R_{\mathrm{rms}}$, $k_*$ nessa janela
- equilíbrio = essas médias existem e o desvio na janela é finito; Q02 fixa os números empíricos

Não escolher a janela depois de ver se “parece QM”.

## 8. Política de seeds

- Exploratório (Q01/Q02 lote 1): seeds inteiras $0,1,2,\ldots$ em ordem, sem descarte estético
- Confirmatório: bloco começando em `1000` (`1000, 1001, …`)
- Nenhuma seed é removida porque o resultado é feio
- Seed de Q01: `0` apenas (convergência, não ensemble)

## 9. Resolução / dt

`N_num`, não física.

- `dt0 = 0.0025`
- Q01a (este arquivo): $N\in\{32,48,64\}$, $dt=dt0$, $T=8$, seed=0
- Q01b (depois): inclui $N=96$ e $dt\in\{dt0, dt0/2, dt0/4\}$
- fp64 em confirmatórios
- Backend: numpy ou metal se for o mesmo passo; registrar qual

## 10. Observáveis obrigatórios (passivos)

$\rho$, $\phi=\arg\Psi$, $J$, $V_{\mathrm{mem}}$, $\rho_{\max}$, norma, PR, $R_{\mathrm{rms}}$, r50/r80/r90, $k_*$, $C$ (crystallinity), winding se definido, $|V_{\mathrm{mem}}|_{\max}$.

Comparação com QM **só depois** da saída Triad gerada.

## 11. Regras

- SEM ISOLAR a dinâmica que conta como evidência
- SEM FALSIFICAR (não apagar run, não retocar janela, não mudar observável depois)
- SEM CALIBRAR (proibido o loop rodar→comparar QM→mudar $\Theta$)
- CAOS → EQUILÍBRIO
- 1 gaussiano = 1 átomo
- volume preenchido = universo

Vereditos: `SUPPORTED` / `PARTIAL` / `NOT_SUPPORTED` / `INCONCLUSIVE` / `NUMERICAL_FAILURE`.

## 12. Pastas

```text
T/
  Fontes/TRIAD_QM_BLUEPRINT.md
  Fontes/TRIAD_QM_CANONICAL_V1.md     ← este arquivo
  QM/
    Q00/
    Q01_convergencia/
    Q02_ensemble/
    ...
```

Cada Qxx confirmatório: PROTOCOL.md, config.json, raw/, metrics.csv, figures/, analysis.md, result.json, SHA256SUMS.txt.

## 13. Critério estatístico

Erro total: numérico (Q01, $\varepsilon_{\mathrm{num}}$) + estatístico (Q02, ensemble).
Não reportar “bateu com QM” sem os dois.

## 14. Hash deste protocolo

Preenchido após gravação (SHA-256 deste arquivo).

`SHA-256(TRIAD_QM_CANONICAL_V1.md)` = `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e`
