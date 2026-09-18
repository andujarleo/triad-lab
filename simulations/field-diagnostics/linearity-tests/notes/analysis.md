# Q04 — Análise (linearidade efetiva / superposição)

**Desvio (declarado no PROTOCOL, não escondido):** o blueprint Q04 pede R_lin após projetar num subespaço efetivo Π. Q03 late/atrator não tem subespaço compartilhado de posto baixo (EV8=0.409447, Rec8=0.768507, overlap φ₀ entre seeds=0.046794). Π_POD late não é espaço de estados; projetar nele tornaria R_lin sem sentido. Q04 mede linearidade no campo com ruído FDT idêntico no triple, e vazamento do plano pré-declarado Π₀=span{G_A,G_B} (as duas gaussianas; 1 gaussiana = 1 átomo). A fórmula do blueprint é reportada com Π=Π₀. Não se usa o POD late de Q03. Não se muda Theta_core. Não se isolam termos. Não se retoca kT.

Língua: PT. 1 gaussiana = 1 átomo. Volume preenchido = universo, não ruído.
Pilotos 1–34 **não** são confirmatórios. Sem comparação com MQ. Sem isolar termos.
Theta_core intocado (Q00). Sem cherry-pick de seed ou de janela.
Backend **mlx**, campo complex64, memória float32. N_num, não física.
Snapshots são sensores. **Não** controlam o solver.
Este lote **não** é SUPPORTED para MQ.

## Pergunta

Existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B) na dinâmica completa? Por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?

## Setup

- Theta_core: Λ=-10.0, α=0.15, σ=1.5, Γ=0.05, ν=(10.0, 0.5, 0.05), λ=(3.0, 1.0, 0.3), kT=1.0
- L=32.0, N=64, dt=0.0025, T=8.0, y_j(0)=0, V_ext=0
- CI: A gaussiana em x=-3; B em x=+3; s=0.5; k0=0; S=(A+B)/||A+B||; a=b=0.70710678
- ||A+B||_L2 = 1.4142136; checagem R_lin_field(t=0) analítica = 8.476205e-19
- Π₀ = Gram-Schmidt complexo de {A(0), B(0)}; declarado antes; não é POD de Q03
- FDT idêntico no triple: rng = default_rng(seed) independente por membro
- seeds 0, 1 nessa ordem; complex64/float32; Strang Q02
- sensores a cada 8 passos (Δt=0.02), 401/membro; 6 evoluções sequenciais
- PROTOCOL SHA-256: `9b6b2f49352cf458d26c4bc22d36037c6057c52829139a784fa4098c489b51df`
- solver executado SHA-256: `c5c271e08e003a3c8a59cc31bdc888d979678c1fad48941daee41db8292eb118`
- Q02 passo SHA-256: `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`
- Q03 PROTOCOL SHA-256: `f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16`
- canônico Q00: `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e`
- início (America/Sao_Paulo): 2026-08-21 14:21:11 BRT
- fim (America/Sao_Paulo): 2026-08-21 14:22:41 BRT
- wall total: 89.83 s
- device: Device(gpu, 0)
- backend: mlx

## Por seed

| seed | finito | R_lin(0) | R_lin(0.02) | R_lin(0.10) | R_lin(0.20) | R_lin late | t_1/2 | t_leak | leak_S(0.2) | leak_S late |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | True | 6.61993e-09 | 0.290703 | 0.293022 | 0.295138 | 0.386372 | inf | 0.02 | 0.998541 | 0.999998 |
| 1 | True | 6.61993e-09 | 0.290731 | 0.292994 | 0.295155 | 0.386448 | inf | 0.02 | 0.998578 | 0.999997 |

## pair_sep (somente S; espírito run 30)

- seed 0: t=0.00:6, t=0.02:6, t=0.04:6, t=0.06:6, t=0.08:6, t=0.10:6, t=0.12:6, t=0.14:6, t=0.16:6, t=0.18:6, t=0.20:6, t=0.22:6, t=0.26:6
- seed 1: t=0.00:6, t=0.02:6, t=0.04:6, t=0.06:6, t=0.08:6, t=0.10:6, t=0.12:6, t=0.14:6, t=0.16:6

Se os dois blobs não são encontráveis, pair_sep é omitido. Não se inventa.

## Médias sobre seeds finitas (oficial = late)

- n_finite = 2 / 2
- R_lin_field t=0: 6.61993e-09
- R_lin_field t=0.02: 0.290717
- R_lin_field t=0.10: 0.293008
- R_lin_field t=0.20: 0.295147
- R_lin_field late (t≥6.4): 0.38641
- t_half (média das seeds com t finito; inf se nenhuma): inf
- t_leak (idem): 0.02
- leak_S t=0.20: 0.99856
- leak_S late: 0.999997

Números early são CONTEXTO / vida útil. **Não** definem o veredito oficial e **não** promovem o par a qubit.

## Veredito

- n_finite = 2 / 2; seeds não finitas / blowup = 0
- oficial (média late R_lin_field) = 0.38641 → **INCONCLUSIVE**
- supported_for_qm = false (nunca SUPPORTED para MQ)

média late R_lin_field=0.38641 em [0.20, 0.50] (ou não finita de forma útil).

Regras (pré-declaradas, não movidas): late <0.20 → PARTIAL; late >0.50 → NOT_SUPPORTED; senão INCONCLUSIVE; >1/2 blowup → NUMERICAL_FAILURE. Early não define o veredito oficial. Nunca SUPPORTED para MQ.

## Notas

- Sem comparação MQ.
- Theta_core intocado.
- Backend mlx (fallback numpy fp32 só se mlx falhar; registrado).
- Sem Simulações run 35.
- Caixa preenchida = universo.
- Π = plano dos 2 átomos (CI), não POD late de Q03.
- a, b e as janelas não foram movidos depois de ver R_lin.
