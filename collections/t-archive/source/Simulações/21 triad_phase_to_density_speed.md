---
tags: [triad, simulação, solver, falha]
aliases: [triad_phase_to_density_speed]
classe: solver.py real via backend NumPy shim
diretório: triad_phase_to_density_speed
status: falha-diagnóstica
run: 21
---

# triad_phase_to_density_speed

Primeira tentativa de kick de fase + frente. T_probe=1.8. **Estimador falhou.** Preservado. [[Phase-to-density]]

## Objetivo

Fundo relaxado T=12, ε=0.07, width=1.3, L=32, dt=0.0025. `background_kstarL=9.424778`.

## Resultado preservado

`density_front_speed≈4.008763e-16`, `phase_front_speed≈4.008763e-16`. Slopes low-k ≈1.045503e-15 e 6.580752e-17. Resultado zero/degenerado. Levou a [[22 triad_phase_to_density_speed_refined]].

![[Artefatos/triad_phase_to_density_speed/00_montagem.png]]

## CSVs

- [[Artefatos/triad_phase_to_density_speed/summary.csv]]
- [[Artefatos/triad_phase_to_density_speed/fronts.csv]]

## Arquivos

`00_montagem.png` · `01_background_density.png` · `02_phase_kick.png` · `03_density_response_xt.png` · `04_phase_response_xt.png` · `05_front_speeds.png` · `06_density_dispersion.png` · `07_phase_dispersion.png` · `08_response_norm.png` · `09_summary.png` + 2 CSVs

→ [[Registro integral]] · [[Solver]]
