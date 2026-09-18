---
tags: [triad, qm, q01, q01a]
aliases: [Q01]
status: active
data: 2026-08-21
---

# Q01 — Convergência numérica da tríade completa

Lote **Q01a** (este diretório): N ∈ {32, 48, 64}, dt=0.0025, T=8, seed=0, Theta_core congelado.

Protocolo imutável: [PROTOCOL](protocol.md) (`Q01_convergencia/PROTOCOL.md`).
Canônico: [TRIAD_QM_CANONICAL_V1](../../../../docs/reference/records/triad-qm-canonical-v1.md) (Q00).

Pergunta só numérica: os observáveis convergem quando N aumenta?
Sem comparação com MQ. Sem isolar termos. Pilotos 27–29 não confirmatórios.

SHA-256 do PROTOCOL.md: `eb127b7d7948e12e9e097ee2e94379821dc51a157033d11bfd449da2d6b1f550`
SHA-256 do solver `code/run_q01a.py`: `abcacbacae3010e1b0e2858dbb96c63410387cb8674286dca8da3958d12e5f64`

Veredito Q01a: **INCONCLUSIVE** (ε_num ≈ 0.19; ok-enough para Q01b). Nunca SUPPORTED para MQ. Detalhe em [analysis](analysis.md) e `result.json`.
