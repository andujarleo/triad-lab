[English](bravais.md) · **Português** · [Acervo](../README.pt-BR.md)

# Geometria, cordas e visualização

Esta linha reúne o conteúdo que estava em `pasta sem título`, `lab`, `X` e nos ZIPs internos. Há evolução de campo, pós-processamento de estados, animações e testes de perturbação. Nomes repetidos nem sempre significam arquivos iguais: as três versões de `bravais_puro_3d.py` continuam separadas.

| Percurso | Scripts de referência |
|---|---|
| [Campo 2D/3D](../files/bravais-root.md) | bravais_emergent_coupled.py, bravais_visual_2d.py, bravais_2d_multi_gaussian.py, bravais_long_2d3d.py, bravais_pure_emerge.py, bravais_puro_3d.py |
| [Cordas e modos](../files/bravais-expanded.md) | cordas_arte.py, cordas_notas_profundo.py, bravais_cordas.py, bravais_dimensoes.py, bravais_vibracoes.py, bravais_cordas_vibracoes.py |
| [Filmes e leituras](../files/bravais-root.md) | simula_filmes.py, filme_cristalizacao.py, cordas_fase_vivas.py, nebulosa.py, som_e_luz.py, gera_visualizador.py |
| [Perturbações e catálogo](../files/bravais-lab.md) | teste_ligacao.py, teste_borboleta.py, teste_pancada.py, teste_musica_batida.py, teste_atomo_corda.py, teste_L_e_A.py, colhe_cordas.py, catalogo_cordas.py |

`bravais_wifi.py` lê medições de um CSV. `wifi_scans.csv` não veio no arquivo; sua presença como script não demonstra uma execução com dados reais. `filmes_data.npz`, usado por vários renderizadores, também não está no acervo. O HTML de visualização salvo contém seus próprios dados.

Os estados `final_state.npz` têm conteúdos diferentes. O estado do ZIP `X.zip` inclui `psi_f`; outro estado e o estado já presente no lab não incluem esse campo. Isso muda quais pós-processamentos podem ser feitos a partir de cada arquivo.

![Reconstruction from recorded spectral modes / Reconstrução de modos espectrais](../source/pasta%20sem%20t%C3%ADtulo/cordas_notas_reconstrucao.png)

- [Raiz exploratória / Exploratory root](../files/bravais-root.md)
- [Lab](../files/bravais-lab.md)
- [Resultados / Results](../files/bravais-results.md)
- [ZIPs expandidos / Expanded ZIPs](../files/bravais-expanded.md)
- [Checagens visuais / Visual checks](../files/bravais-check.md)

[Versões e cópias idênticas](../provenance/versions.md) · [HTML preservado / Preserved HTML](../source/pasta%20sem%20t%C3%ADtulo/visualizador.html)
