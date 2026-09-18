---
tags: [triad, qm, q02, ensemble]
aliases: [Q02]
status: active
data: 2026-08-21
---

# Q02 — Ensemble caótico de referência (32 seeds, 1 átomo)

Lote **Q02** (este diretório): 32 seeds (0–31, nessa ordem) do mesmo macroestado físico (1 gaussiana = 1 átomo), tríade completa, N=64, dt=0.0025, T=8, L=32, Theta_core congelado.

Backend **mlx GPU**, campo complex64, memória float32 (`PROTOCOL_v2.md`). N_num, não calibração. O v1 (`PROTOCOL.md`, numpy/fp64) fica histórico e **não** foi editado. Lote exploratório; confirmatório (seeds 1000+) permanece fp64 mais tarde. **Nunca** SUPPORTED para MQ.

Protocolo deste lote: [PROTOCOL_v2](protocol-revision-2.md). Canônico: [TRIAD_QM_CANONICAL_V1](../../../../docs/reference/records/triad-qm-canonical-v1.md) (Q00).
Q01a/Q01b: [Q01](../../spatial-convergence/notes/convergence-record.md) / `[[Q01b]]` — INCONCLUSIVE.

Pergunta: qual é a distribuição natural de comportamentos do substrato sem escolher uma seed bonita?
Sem comparação com MQ. Sem isolar termos. Sem cherry-pick. Pilotos 1–34 não confirmatórios.

SHA-256 PROTOCOL v1 (histórico): `a2024aff5e29c484ed781f6972d1699f4657997072c528333f1268b95cb648af`
SHA-256 PROTOCOL v2 (este lote): `bb19a387d2c0b8239b1e360bc9e3b96d246c99d20875a52e5be41617ce75f63c`
SHA-256 do solver executado `code/run_q02.py`: `ef65da9774ff65ac9b781595944f59bc1892f04665370a2de190ad22f94ba365`
SHA-256 canônico Q00: `e7c7d907c7109bbafc73229cb2e1943802feb47df035a7058e71ebec078d9a3e`

Veredito Q02: **INCONCLUSIVE** (32/32 finitas; peak/PR/R_rms tardios com std finito; ensemble OK). Q02 **não** é teste de MQ. Nunca SUPPORTED para MQ. Detalhe em [analysis](analysis.md) e `result.json`.

Início 2026-08-21 13:52:10 BRT; fim 14:00:26 BRT; wall 495.39 s (1 GPU, sequencial).
