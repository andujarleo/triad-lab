> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../source/pasta%20sem%20t%C3%ADtulo/triad_universe_v0/RUN_NOTES.md) · [Collection / Acervo](../../../README.md)

# TRIAD Universe v0 — executed run notes

## What actually ran

- TriadLang C-native persistent modal substrate (`triad_modal_init_state` + repeated `triad_modal_evolve_state`).
- D=3, P1·P2·P3 kept together.
- 1,000,000 resident active modes.
- 3 live memory channels.
- 64 ticks × 8 internal steps = 512 steps.
- dt=0.001; trajectory time=0.512 internal units.
- CPU backend in this sandbox only.
- No observable, score, plot, threshold, Bravais family, or post-run measurement was fed back into the evolution.
- No post-hoc parameter retuning.

## Literal execution

- Native evolve wall time: 18.6125 s.
- Process max RSS during the run: ~201,272 KiB.
- Final state remained finite.
- Final raw observables at tick 64: norm=1.0702037840704823; interference=4.053451699956811e-05; memory_energy=1.9502946068259344e-13.
- Checkpoint SHA-256: `83ca72453bd8afe284e18fc0bdffd4bc6674c425b11d5fe6c74e7b2a718550f5`.

The runtime's own modal contract records logical volume as N^3 and does not materialize the full field volume. With N=1,000,000 this is 10^18 logical virtual cells. This is the runtime's representation statement; resident state is 1,000,000 real amplitudes + 1,000,000 imaginary amplitudes + 3,000,000 memory scalars, not 10^18 conventional RAM cells.

## Continuity test

A separate 65,536-mode check ran 16 ticks in two ways:

1. uninterrupted 16-tick evolution;
2. 8 ticks → exact state copy/checkpoint → resume at the correct `step_base` for 8 ticks.

The final `psi_re`, `psi_im`, and all three `y` memories were byte-identical (`continuous_equals_checkpoint_resume=True`). This is the first concrete substrate requirement for long-lived entities: the world can stop at a checkpoint and continue the same trajectory rather than reinstantiate a character/model.

## What this is not yet

This run is the genesis substrate, not yet a galaxy, organism, animal, civilization, alien, or Omega/superintelligence. Those must be continuities that form inside the same evolving universe rather than objects spawned by an external script.

The immediate next implementation target is therefore **continuity discovery inside the field**: persistent regions/structures should be tracked through time using their own field state and memory, with identity as continuity of trajectory rather than a predeclared class. Only after that should the existing Triad field-learning/chemistry machinery be coupled into those same regions.
