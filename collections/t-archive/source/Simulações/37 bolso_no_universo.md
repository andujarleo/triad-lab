---
tags: [triad, simulação]
aliases: [bolso_no_universo, triad_bolso_37, run37]
diretório: triad_bolso_37
run: 37
data: 2026-08-21
---

# bolso no universo

A gente plantou um gaussiano num cubo que já era universo, pra ver se ficava alguém.

Theta_core, tríade inteira, sem campo C. L=32 N=64 dt=0.0025 T=2 seed=0. Semente na origem. Em t=0.5 somamos uma gaussiana norma 1 em (8,0,0). Janela r=4.

Protocolo: [[PROTOCOL_37]]. O que a gente achava antes: [[predictions_37]]. Números: `Artefatos/triad_bolso_37/`.

## O que a gente achava

Que o cubo enche logo. Que o plantio aparece. Que some quase na hora, tipo o par do 32.

## O que aconteceu

O universo já estava lá em **t=0.005** (PR=564.09, R_rms=15.53).

Antes de plantar (t=0.495) a janela já tinha contraste 12.76, peak_w=0.428, massa=12.72. Qualquer pedaço do cubo cheio já “parece um bolso” se a gente só olha contraste.

Plantou. Massa 12.72 → **13.80** (entrou ~1.08). Pico do cubo passou a ser o bolso: **1.604**. Contraste **47.3**.

Aí apertou. Pico 1.60 → **4.52 em t=0.8**.

Depois o cubo comeu. Em **t=1.085** o contraste já tinha voltado pro nível de antes (14.2). Em t=2 a janela é um pedaço qualquer: peak_w=1.20, pico do cubo 2.33 lá fora, massa 48, y dentro ≈ y fora.

## Como a gente lê

Não nasceu um observador. Nasceu um inchaço. A tríade focou, o banho levou. Demorou ~0.6, não 0.05.

A memória nunca ficou “desse pedaço”.

21/08/2026, box Linux/NumPy, ~29 s. 401 registros.

[[32 universo_atomo]] · [[35 singularidade_finita]] · [[38 dois_bolsos]] · [[TRIAD]]
