---
tags: [triad, qm, q04, linearidade]
aliases: [Q04]
status: active
data: 2026-08-21
---

# Q04 — Linearidade efetiva / superposição

Lote **Q04** (este diretório): seeds 0 e 1 (nessa ordem), triple A / B / S, tríade completa, N=64, dt=0.0025, T=8, L=32, Theta_core congelado. Linearidade no campo com ruído FDT idêntico; vazamento do plano Π₀=span{G_A,G_B} (1 gaussiana = 1 átomo). Snapshots são sensores; **não** controlam o solver.

Backend **mlx**, campo complex64, memória float32. N_num, não calibração. **Nunca** SUPPORTED para MQ.

Protocolo: [PROTOCOL](protocol.md). Canônico: [TRIAD_QM_CANONICAL_V1](../../../../docs/reference/records/triad-qm-canonical-v1.md) (Q00).
Q03: `[[Q03]]` — INCONCLUSIVE (atrator sem subespaço compartilhado). Q02: `[[Q02]]` — INCONCLUSIVE.

Pergunta: existe um regime em que F_t(aA+bB) ≈ a F_t(A) + b F_t(B) na dinâmica completa? Por quanto tempo a soma de dois átomos permanece no plano dos dois átomos?
Sem comparação com MQ. Sem isolar termos. Sem cherry-pick. Pilotos 1–34 não confirmatórios.

SHA-256 PROTOCOL: `9b6b2f49352cf458d26c4bc22d36037c6057c52829139a784fa4098c489b51df`
SHA-256 do solver executado `code/run_q04.py`: `c5c271e08e003a3c8a59cc31bdc888d979678c1fad48941daee41db8292eb118`
SHA-256 passo Q02: `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`
SHA-256 PROTOCOL Q03: `f565abde737256058c8c7e7f5a3ce963b89039b0555da908a1563f3c867e8c16`
SHA-256 canônico Q00: `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e`

Desvio: Π = plano dos 2 átomos (CI), **não** POD late de Q03 (EV8=0.409, Rec8=0.769, overlap φ₀=0.047). Ver [PROTOCOL](protocol.md).

Veredito Q04 (oficial = média late de R_lin campo, t≥6.4): **INCONCLUSIVE**. Early só contexto / vida útil (não promove o par a qubit). Q04 **não** é teste de MQ. Nunca SUPPORTED para MQ. Detalhe em [analysis](analysis.md) e `result.json`.

Início 2026-08-21 14:21:11 BRT; fim 2026-08-21 14:22:41 BRT; wall 89.83 s (1 GPU, sequencial).
