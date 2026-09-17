[Lab home](../../README.md) · **English** · [Português](../pt-BR/getting-started.md)

# Run an experiment

## Set up

Commands below use a POSIX shell, from the repository root. Use Python 3.10 or newer
(the scripts use modern type annotations). Dependencies here are installation
requirements, not a recovered lockfile of the original environment.

```sh
git clone https://github.com/andujarleo/triad-lab.git
cd triad-lab
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-visualization.txt
```

`requirements.txt` supplies NumPy, Matplotlib and Pillow. The visualization list
also installs SciPy and scikit-image. The Bravais scripts have NumPy fallbacks
for SciPy helpers; isosurface plots require scikit-image. Installing or removing
these packages can change which plots are available and which helper path runs.

## Start with a saved state

Generate density and spectral strings without running the 3D evolution:

```sh
MPLBACKEND=Agg python en/bravais/bravais_strings.py bravais/final_state.npz
```

Outputs go to `bravais_outputs_3d/`. The bundled state has no `psi_f`, so the phase
strings section is skipped by the script. This is expected for that saved file.
The script assumes `L=32`; set `L` to the actual box size for a different state.

## Run a simulation

```sh
python en/entre/simulate_observer_observed_relations.py
```

The base experiment uses 6,000 RK4 steps with `DT=0.02`. It writes new PNG, GIF,
JSON and NPZ files into `en/entre/artifacts/`. Other Entre entry points are listed
in the [catalog](../../experiments/README.md). Portuguese scripts write to
`entre/artifacts/` instead.

For the Bravais evolution or box sweep:

```sh
MPLBACKEND=Agg python en/bravais/bravais_pure_3d.py
MPLBACKEND=Agg python en/bravais/bravais_sweep_L.py
```

The evolution defaults to 1,200 steps on a `64³` grid. The sweep defaults to 800
steps per box and reaches `96³`; resource needs are higher. Both accept `STEPS`
through the environment, but a shorter run is a different run. Both initialize
randomly without a fixed seed. Saved figures are available without rerunning.

## Keep runs separate

Scripts use fixed output names and can overwrite earlier generated files. After
each run, move its generated output directory into `runs/<experiment-id>/<run-id>/`
before starting another run. Keep a copy of [run.json](../../templates/run.json)
with the command, commit, environment, parameters and outcome. `runs/` is ignored
by Git; selectively publish a reviewed record under its experiment folder.

Many historical scripts execute at import time. Run them as scripts; importing
a module is not a harmless way to list its options.

## What is preserved

```sh
shasum -a 256 -c docs/archive/SHA256SUMS
```

This verifies the supplied files. It does not assert exact replay of a historical
execution. The included arrays, plots and script defaults are the available
record; capture dependency versions and hardware for each new run.
