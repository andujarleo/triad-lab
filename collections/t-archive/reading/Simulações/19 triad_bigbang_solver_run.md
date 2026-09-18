> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/19%20triad_bigbang_solver_run.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, solver, falha]
aliases: [triad_bigbang_solver_run]
classe: solver.py real via backend NumPy shim
diretório: triad_bigbang_solver_run
status: falha-diagnóstica
run: 19
```


# triad_bigbang_solver_run

Primeiro run que carrega [solver.py](../../source/Fontes/solver.py) / `integrate_3d`. `ntri` → NumPy. `[[Backend e unidades]]`. FDT relativamente quente. **Falha de massa preservada.**

## Objetivo

36³, L=32, dt=0.0025, T=8.

## Resultado preservado

| | inicial | mín | máx | final |
|---|---|---|---|---|
| peak | 0.778218 | 0.356994 | 2.253536 | 2.005190 |
| PR | 2.184352 | | 18704.369091 | 18704.369091 |
| Rrms | 0.658873 | | 16.038026 | 16.014047 |
| mass | 1 | | 8773.74776 | **8773.747757** |

k\*L final=21.991149. mem_amp_t final=0.922319. focus_amp_t final=1.606521.

Crescimento de massa/norma associado ao FDT quente. Permanece. Motivou [20 triad_bigbang_3d_box](20%20triad_bigbang_3d_box.md).

![Artefatos/triad_bigbang_solver_run/00_montagem.png](../../source/Artefatos/triad_bigbang_solver_run/00_montagem.png)

Animação 14.34 MB — **não embedada**; arquivo: `Artefatos/triad_bigbang_solver_run/10_bigbang_animation.gif`

## CSVs

- [Artefatos/triad_bigbang_solver_run/summary.csv](../../source/Artefatos/triad_bigbang_solver_run/summary.csv)
- [Artefatos/triad_bigbang_solver_run/metrics.csv](../../source/Artefatos/triad_bigbang_solver_run/metrics.csv)

## Arquivos

`00_montagem.png` · `01_timeline_xy.png` … `09_memory_timeline_xy.png` · `10_bigbang_animation.gif` · `11_summary.png` + 2 CSVs

→ [FDT](../Conceitos/FDT.md) · [Registro integral](../Fontes/Registro%20integral.md)
