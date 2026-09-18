[Lab](../../README.md) · **English** · [Português](../pt-BR/getting-started.md)

# Inspect records and prepare a TRIAD execution

Start with the saved data and the [project rules](project-rules.md). A new TRIAD execution must retain the complete immutable equation, with no disabled terms and no external calibration toward a desired result.

The archived commands below document preserved implementations. Their presence does not certify that they satisfy these rules. Consult each study’s configuration and the [reference-document history](../reference/equation/README.md); do not use a historical term-off setup as a new TRIAD experiment.

Commands use a POSIX shell from the repository root and Python 3.10 or newer. The requirements are an installation starting point, not a recovered lockfile of the original environment.

```sh
git clone https://github.com/andujarleo/triad-lab.git
cd triad-lab
git lfs install
git lfs pull
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-visualization.txt
python tools/check_repository.py
```

Install Git LFS before using `git lfs`. PNG figures can be read on GitHub; arrays and animations use LFS. `requirements.txt` includes NumPy, Matplotlib and Pillow; the visualization list adds SciPy and scikit-image. Their availability can change helper execution paths and which plots are produced.

## Start with a saved state

```sh
MPLBACKEND=Agg python simulations/geometry/string-analysis/code/en/bravais_strings.py simulations/geometry/field-3d/results/data/final_state.npz
```

This command reads the saved state and writes figures into `bravais_outputs_3d/`, without rerunning field evolution. The included state has no `psi_f`, so the phase-string section is skipped. The script assumes `L=32`; for another state, set its actual box size with the `L` environment variable.

## Archived execution commands

These commands are kept for tracing the historical record. The oscillator pilots and the 3D implementations must be assessed against the complete-equation rules before any new TRIAD execution; the source code has not been altered by this editorial audit.

<details>
<summary>Inspect the historical commands and their original defaults</summary>

### Oscillator pilot

```sh
python simulations/relations/observer/code/en/simulate_observer_observed_relations.py
```

This uses 6,000 RK4 steps with `DT=0.02`. New outputs go into `artifacts/` beside the script. The Portuguese version is in `code/pt-BR/` within the same study.

### Historical 3D evolution and sweep

```sh
MPLBACKEND=Agg python simulations/geometry/field-3d/code/en/bravais_pure_3d.py
MPLBACKEND=Agg python simulations/geometry/scale-sweep/code/en/bravais_sweep_L.py
```

Evolution defaults to 1,200 steps on a 64³ grid. The sweep uses 800 steps per box and reaches 96³, requiring more resources. Both accept `STEPS` through the environment, but shortening a run creates a different comparison. Random initialization has no fixed seed; defaults do not exactly reconstruct the included record.

</details>

## Keep each run separate

Scripts use fixed output names and can overwrite generated files. Before the next run, move new outputs to `runs/<study-id>/<run-id>/`, which Git ignores. Record command, working directory, environment, parameters and hashes in the run template. Publish new outputs separately from old ones.

[Run template](../../templates/run.json) · [Historical dependencies](../../provenance/t-archive/dependencies.md)

Many historical scripts execute on import and contain old paths. Do not import them merely to list options. Path or dependency adaptations need their own record; this reorganization preserved the numerical source code.
