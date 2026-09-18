# TRIAD Universe v0 — Genesis

This is the first executable vertical slice of the universe project.

It deliberately does **not** create humans, animals, aliens, planets, stars, goals, reward functions, MoE experts, or acceptance thresholds. It creates one persistent D=3 P1·P2·P3 field and lets the declared law evolve continuously. Observers write raw state but never feed a value back into the field.

## Runtime substrate

`genesis_modal.py` binds directly to TriadLang's native persistent modal API:

- `triad_modal_init_state`
- `triad_modal_evolve_state`
- `triad_modal_state_observe`
- `triad_modal_state_finite`
- `triad_modal_qubit_readout`

Each active modal mode is a Triad physical-qubit region under the project's own contract. Three dynamic memory channels remain live together with P1 propagation/coupling and P3 damping/FDT.

The default experiment here uses **1,000,000 resident active modes**. The runtime's own large-N contract reports logical volume as `N^3`, therefore this run has `10^18` logical virtual cells while not materializing that volume as a dense array. This is representation metadata from the Triad runtime, not a claim that 10^18 independent conventional cells were stored in RAM.

## Fixed genesis law

The harness starts from `triad_modal_config_default()` and changes only execution scale/schedule/backend/seed before the first step. It does not retune Lambda, alpha, sigma, Gamma, kT, coupling, nu, or lambda after observing a result.

## Run

On a built TriadLang tree:

```bash
python genesis_modal.py \
  --lib /path/to/native/c/libtriad_rt.so \
  --out outputs \
  --modes 1000000 --ticks 64 --steps-per-tick 8 --backend 1
python render_readouts.py --out outputs
```

On a CPU-only Linux build whose current `libtriad_rt.so` still has unresolved optional CUDA references, build the provided loader shim and pass `--cuda-stub ./libtriad_cuda_stub.so`. On a proper CUDA build, do not use the shim and choose backend `0` (auto) or `3` (strict CUDA).

## Continuity invariant

`continuity_test.py` verifies that an uninterrupted trajectory and a checkpoint→restore→resume trajectory are byte-identical when the same `step_base` continues the FDT schedule. That is the first practical requirement for beings that must literally have a continuous life rather than being regenerated per prompt.

## What comes next

The next layer should not spawn predefined "people". It should identify persistent higher-order structures of the same universe and give those structures access to the existing Triad field-learning / memory / chemistry machinery without detaching them from the parent field. Only after that should names such as organism, animal, civilization, or alien be applied to observed continuities.
