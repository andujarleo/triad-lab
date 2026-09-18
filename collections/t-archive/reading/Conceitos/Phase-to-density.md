> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Conceitos/Phase-to-density.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, conceito]
aliases: [fase-densidade, velocidade de frente]
```


# Phase-to-density

Kick só de fase sobre um fundo relaxado; medir se a densidade responde com uma frente. Dois protocolos, ambos no registro.

## Bruto — falha diagnóstica

[21 triad_phase_to_density_speed](../Simula%C3%A7%C3%B5es/21%20triad_phase_to_density_speed.md). T_probe=1.8, ε=0.07, width=1.3.

`density_front_speed≈4.008763e-16`, `phase_front_speed≈4.008763e-16`; slopes low-k ≈1.045503e-15 e 6.580752e-17. Estimador degenerado. Preservado.

## Refinado

[22 triad_phase_to_density_speed_refined](../Simula%C3%A7%C3%B5es/22%20triad_phase_to_density_speed_refined.md). Background T=12, kick ε=0.15, width=1.25, probe T=5, controle com a mesma sequência de ruído.

| métrica | densidade | fase |
|---|---|---|
| arrival (front) | 7.301417 | 7.557409 |
| RMS radius speed | 1.482120 | 1.893955 |
| slope low-k | 0.821417 | 0.235523 |

Imagem x–t da densidade: abertura em V/triângulo. Fronts de chegada próximos; inclinações espectrais **não** coincidem.

Ambos via `[[Solver]]` / shim NumPy. `[[Backend e unidades]]`

Voltar: [Índice de runs](../Simula%C3%A7%C3%B5es/%C3%8Dndice%20de%20runs.md)
