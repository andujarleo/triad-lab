---
tags: [triad, simulação, solver]
aliases: [triad_phase_to_density_speed_refined]
classe: solver.py real via backend NumPy shim
diretório: triad_phase_to_density_speed_refined
status: completo
run: 22
---

# triad_phase_to_density_speed_refined

Protocolo refinado após a falha de [21 triad_phase_to_density_speed](../../first-phase-to-density-diagnostic/notes/original-record.md). [Phase-to-density](../../../../docs/reference/concepts/phase-to-density.md) · `[[Solver]]`

## Objetivo

Background T=12, kick só de fase ε=0.15, width=1.25; controle casado (mesma sequência de ruído); probe T=5. L=32, dt=0.0025. `background_kstarL=9.424778`.

## Resultado preservado

| | densidade | fase |
|---|---|---|
| arrival speed | 7.301417 | 7.557409 |
| RMS radius speed | 1.482120 | 1.893955 |
| slope low-k | 0.821417 | 0.235523 |

x–t da densidade: abertura em V/triângulo. Fronts próximos; slopes **não** coincidem.

![Artefatos/triad_phase_to_density_speed_refined/00_montagem.png](../results/figures/overview.png)

CSV: [Artefatos/triad_phase_to_density_speed_refined/summary.csv](../results/data/summary.csv)

## Arquivos

`00_montagem.png` · `01_density_xt.png` · `02_phase_xt.png` · `03_response_radii.png` · `04_arrival_times.png` · `05_density_dispersion.png` · `06_phase_dispersion.png` · `07_response_norm.png` · `08_summary.png` · `summary.csv`

→ [Índice de runs](../../../../docs/reference/records/indice-de-runs.md)
