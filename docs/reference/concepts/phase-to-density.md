---
tags: [triad, conceito]
aliases: [fase-densidade, velocidade de frente]
---

# Phase-to-density

Kick só de fase sobre um fundo relaxado; medir se a densidade responde com uma frente. Dois protocolos, ambos no registro.

## Bruto — falha diagnóstica

[21 triad_phase_to_density_speed](../../../experiments/signals/first-phase-to-density-diagnostic/notes/original-record.md). T_probe=1.8, ε=0.07, width=1.3.

`density_front_speed≈4.008763e-16`, `phase_front_speed≈4.008763e-16`; slopes low-k ≈1.045503e-15 e 6.580752e-17. Estimador degenerado. Preservado.

## Refinado

[22 triad_phase_to_density_speed_refined](../../../experiments/signals/refined-phase-to-density-diagnostic/notes/original-record.md). Background T=12, kick ε=0.15, width=1.25, probe T=5, controle com a mesma sequência de ruído.

| métrica | densidade | fase |
|---|---|---|
| arrival (front) | 7.301417 | 7.557409 |
| RMS radius speed | 1.482120 | 1.893955 |
| slope low-k | 0.821417 | 0.235523 |

Imagem x–t da densidade: abertura em V/triângulo. Fronts de chegada próximos; inclinações espectrais **não** coincidem.

Ambos via `[[Solver]]` / shim NumPy. `[[Backend e unidades]]`

Voltar: [Índice de runs](../records/indice-de-runs.md)
