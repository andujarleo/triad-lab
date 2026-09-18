[English](dependencies.md) · **Português** · [Acervo](../README.pt-BR.md)

# Dependências e portabilidade

Este acervo reúne ambientes diferentes. O `requirements.txt` da raiz atende às séries iniciais do lab e não instala o runtime completo destes estudos. Antes de executar um script histórico, copie seu pacote para um diretório de trabalho e confira caminhos de entrada, saída, parâmetros, backend e dados necessários.

| Linha | Dependências observadas | Limite conhecido |
|---|---|---|
| Bravais / visualização | NumPy, Matplotlib, SciPy; scikit-image, imageio em alguns scripts | `filmes_data.npz` ausente; versões de estados diferem |
| Catálogo de cordas | scikit-learn, NumPy, Matplotlib | `cordas.csv` referenciado, não fornecido |
| Solver original | `triad`, `runtime.backend`, `runtime.env`, `runtime.ml.gpu_fused`, CuPy | Runtime TriadLang completo ausente |
| Q02–Q04 / MLX | `mlx.core`, NumPy, Matplotlib, SciPy conforme o script | Backend Apple/MLX e caminhos absolutos históricos |
| R5 passivo | NumPy, SciPy, Matplotlib | Snapshots e checkpoints próprios; executar fora da fonte preservada |
| Continuidade causal | NumPy, SciPy | `triad_rebuild_rules/run64` externo e ausente |
| Universo persistente | NumPy, Matplotlib, native TriadLang API | `libtriad_rt.so` ausente; shim não o substitui |

Scripts com caminhos `/Users/...`, `/mnt/data/...` ou `/tmp/...` continuam intactos. Os caminhos históricos não foram “corrigidos” silenciosamente. O próximo passo para tornar um estudo executável deve ser uma adaptação separada, com comparação dos parâmetros e teste de reprodução próprio.

[Imports e caminhos por script](code-index.md) · [Inspeção técnica](inspection.json)
