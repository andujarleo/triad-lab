> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../source/Simula%C3%A7%C3%B5es/07%20triad_limit_test_fast.md) · [Collection / Acervo](../../README.md)

```yaml
tags: [triad, simulação, quantitativa]
aliases: [triad_limit_test_fast]
classe: Exploratória quantitativa
diretório: triad_limit_test_fast
status: completo
run: 7
```


# triad_limit_test_fast

Refaz [06 triad_limit_test](06%20triad_limit_test.md). Varredura N={2,4,8,12}, r={4,6,8}. Mede a_R, R0, Rfinal, deltaR.

## Resultado preservado

12 combinações em `limit_results.csv`. a_R tem sinais + e −. **deltaR>0 só em N=2, r=4**; negativo nas demais.

| N | r | a_R | R0 | Rfinal | deltaR |
|---|---|---|---|---|---|
| 2 | 4.0 | 0.0069487159073746 | 2.0 | 2.0180951776059834 | 0.0180951776059836 |
| 2 | 6.0 | 0.0245129493323601 | 3.0 | 2.984787146285002 | −0.0152128537149978 |
| 2 | 8.0 | 0.0038406151472923 | 4.0 | 3.9797465041624513 | −0.0202534958375482 |
| 4 | 4.0 | −0.0125417119295443 | 4.47213595499958 | 4.459549526410244 | −0.0125864285893353 |
| 4 | 6.0 | −0.0114692681920223 | 6.708203932499369 | 6.671005179654979 | −0.0371987528443904 |
| 4 | 8.0 | −0.0066551972554983 | 8.94427190999916 | 8.891641969445779 | −0.0526299405533805 |
| 8 | 4.0 | 0.0029342798044532 | 9.16515138991168 | 9.117765454865182 | −0.0473859350464973 |
| 8 | 6.0 | −0.0056109567203563 | 13.74772708486752 | 13.660728830598003 | −0.0869982542695169 |
| 8 | 8.0 | −0.0170214514185895 | 18.33030277982336 | 18.21883453380261 | −0.111468246020749 |
| 12 | 4.0 | −0.0028163354835267 | 13.808210118138652 | 13.732715217153135 | −0.0754949009855163 |
| 12 | 6.0 | 0.0013605645937609 | 20.71231517720798 | 20.58611413442041 | −0.1262010427875708 |
| 12 | 8.0 | −0.000923292578859 | 27.616420236277303 | 27.36859791533509 | −0.247822320942209 |

Sem `00_montagem`. CSV: [Artefatos/triad_limit_test_fast/limit_results.csv](../../source/Artefatos/triad_limit_test_fast/limit_results.csv)

## Arquivos

`01_heatmap.png` · `02_curves.png` · `03_N_scaling.png` · `04_r_scaling.png` · `05_summary.png` · `limit_results.csv`

![Artefatos/triad_limit_test_fast/01_heatmap.png](../../source/Artefatos/triad_limit_test_fast/01_heatmap.png)

→ [Índice de runs](%C3%8Dndice%20de%20runs.md)
