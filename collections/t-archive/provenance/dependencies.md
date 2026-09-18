**English** · [Português](dependencies.pt-BR.md) · [Collection](../README.md)

# Dependencies and portability

This archive spans several environments. The root `requirements.txt` serves the initial lab series and does not install the full runtime for these studies. Before running a historical script, copy its bundle to a working directory and check input/output paths, parameters, backend and required data.

| Line | Observed dependencies | Known limit |
|---|---|---|
| Bravais / visualização | NumPy, Matplotlib, SciPy; scikit-image, imageio in some scripts | `filmes_data.npz` missing; state versions differ |
| Catálogo de cordas | scikit-learn, NumPy, Matplotlib | `cordas.csv` referenced, not supplied |
| Solver original | `triad`, `runtime.backend`, `runtime.env`, `runtime.ml.gpu_fused`, CuPy | Runtime TriadLang not supplied in full |
| Q02–Q04 / MLX | `mlx.core`, NumPy, Matplotlib, SciPy as required by the script | Backend Apple/MLX and historical absolute paths |
| R5 passivo | NumPy, SciPy, Matplotlib | Snapshots and checkpoints from this bundle; run outside preserved sources |
| Continuidade causal | NumPy, SciPy | `triad_rebuild_rules/run64` external and missing |
| Universo persistente | NumPy, Matplotlib, native TriadLang API | `libtriad_rt.so` missing; the shim does not replace it |

Scripts containing `/Users/...`, `/mnt/data/...` or `/tmp/...` paths remain intact. Historical paths were not silently rewritten. Making a study runnable should be a separate adaptation with parameter comparison and its own reproduction check.

[Imports and paths by script](code-index.md) · [Technical inspection](inspection.json)
