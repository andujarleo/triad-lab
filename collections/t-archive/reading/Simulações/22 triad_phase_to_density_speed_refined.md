> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/22%20triad_phase_to_density_speed_refined.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, solver]
aliases: [triad_phase_to_density_speed_refined]
classe: solver.py real via backend NumPy shim
diretório: triad_phase_to_density_speed_refined
status: completo
run: 22
```


# triad_phase_to_density_speed_refined

Protocolo refinado após a falha de [21 triad_phase_to_density_speed](21%20triad_phase_to_density_speed.md). [Phase-to-density](../Conceitos/Phase-to-density.md) · `[[Solver]]`

## Objetivo

Background T=12, kick só de fase ε=0.15, width=1.25; controle casado (mesma sequência de ruído); probe T=5. L=32, dt=0.0025. `background_kstarL=9.424778`.

## Resultado preservado

| | densidade | fase |
|---|---|---|
| arrival speed | 7.301417 | 7.557409 |
| RMS radius speed | 1.482120 | 1.893955 |
| slope low-k | 0.821417 | 0.235523 |

x–t da densidade: abertura em V/triângulo. Fronts próximos; slopes **não** coincidem.

![Artefatos/triad_phase_to_density_speed_refined/00_montagem.png](../../source/Artefatos/triad_phase_to_density_speed_refined/00_montagem.png)

CSV: [Artefatos/triad_phase_to_density_speed_refined/summary.csv](../../source/Artefatos/triad_phase_to_density_speed_refined/summary.csv)

## Arquivos

`00_montagem.png` · `01_density_xt.png` · `02_phase_xt.png` · `03_response_radii.png` · `04_arrival_times.png` · `05_density_dispersion.png` · `06_phase_dispersion.png` · `07_response_norm.png` · `08_summary.png` · `summary.csv`

→ [Índice de runs](%C3%8Dndice%20de%20runs.md)
