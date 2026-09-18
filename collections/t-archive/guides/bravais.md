**English** · [Português](bravais.pt-BR.md) · [Collection](../README.md)

# Geometry, strings and visualization

This line brings together material from `pasta sem título`, `lab`, `X` and the nested ZIPs. It includes field evolution, saved-state post-processing, animations and perturbation probes. Repeated names do not always mean identical files: the three versions of `bravais_puro_3d.py` remain separate.

| Path | Reference scripts |
|---|---|
| [2D/3D fields](../files/bravais-root.md) | bravais_emergent_coupled.py, bravais_visual_2d.py, bravais_2d_multi_gaussian.py, bravais_long_2d3d.py, bravais_pure_emerge.py, bravais_puro_3d.py |
| [Strings and modes](../files/bravais-expanded.md) | cordas_arte.py, cordas_notas_profundo.py, bravais_cordas.py, bravais_dimensoes.py, bravais_vibracoes.py, bravais_cordas_vibracoes.py |
| [Movies and readouts](../files/bravais-root.md) | simula_filmes.py, filme_cristalizacao.py, cordas_fase_vivas.py, nebulosa.py, som_e_luz.py, gera_visualizador.py |
| [Perturbations and catalog](../files/bravais-lab.md) | teste_ligacao.py, teste_borboleta.py, teste_pancada.py, teste_musica_batida.py, teste_atomo_corda.py, teste_L_e_A.py, colhe_cordas.py, catalogo_cordas.py |

`bravais_wifi.py` reads measurements from a CSV. `wifi_scans.csv` was not supplied; having the script does not demonstrate a run with real measurements. `filmes_data.npz`, used by several renderers, is also absent. The saved visualization HTML contains its own data.

The `final_state.npz` files differ. The state from `X.zip` includes `psi_f`; another state and the state already in the lab lack that field. This changes which post-processing steps each saved file supports.

![Reconstruction from recorded spectral modes / Reconstrução de modos espectrais](../source/pasta%20sem%20t%C3%ADtulo/cordas_notas_reconstrucao.png)

- [Raiz exploratória / Exploratory root](../files/bravais-root.md)
- [Lab](../files/bravais-lab.md)
- [Resultados / Results](../files/bravais-results.md)
- [ZIPs expandidos / Expanded ZIPs](../files/bravais-expanded.md)
- [Checagens visuais / Visual checks](../files/bravais-check.md)

[Versions and identical copies](../provenance/versions.md) · [HTML preservado / Preserved HTML](../source/pasta%20sem%20t%C3%ADtulo/visualizador.html)
