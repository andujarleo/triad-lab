[Lab](../../README.md) · **English** · [Português](../pt-BR/execution-audit.md)

# What the recorded simulations actually show

**The archive contains striking differences in field behavior, and the conditions behind those differences matter.** A memory comparison ends with a density peak of about **0.000641 versus 3.889202**. Two twelve-atom records finish with field norms of **25,585.35 versus 23.28**. One saved trajectory receives both a “bounce” and a “no bounce” label, depending on which radius is measured.

This audit follows those results back to their code, configurations and recorded measurements. It asks a practical question: **what was actually evolved, what was changed, and what can this particular comparison tell us?** It covers all **65 catalog entries** through file inventory and a documented status for each, with closer source and record review behind the findings below. No simulation was rerun.

[The complete equation](#the-complete-equation) · [Five central cases](#five-central-cases) · [All 17 findings](#all-17-findings) · [Every study](#every-study) · [Coverage](#coverage) · [Identity audit in eight languages](triad-identity-audit.md)

<a id="the-complete-equation"></a>
## Why the complete equation is the starting point

TRIAD is presented here as **nonstandard quantum physics with an ontological foundation**. Its author defines one immutable, indivisible equation: P1 oscillation, P2 self-reference through both present state and memory, and P3 coupling act together. The intended behavior is the self-organization of that coupled system, including dynamic equilibrium and crystallization. [Project rules](project-rules.md), lines 5–31.

A record produced after disabling memory or the bath cannot establish what the **complete TRIAD equation** produces. It still documents what its recorded configuration did. Likewise, a simulation that continually rescales the field or uses a different update equation needs that operation disclosed before its output is attributed to the reference dynamics. This is a question of implementation identity, not a new version of the equation.

There are also legitimate differences that do not remove terms: a declared initial state, an input applied during a run, a finer grid, a smaller time step, a detector measurement or a visual rendering. Each must be described in its own terms. Choosing a detector threshold is different from tuning the dynamics to obtain a preferred shape. The supplied records sometimes leave that distinction unresolved; the audit says where.

**Methodology also belongs to the author’s rules.** The lab does not use Popperian falsification or agreement with standard quantum mechanics as its governing criterion. Numerical checks can still examine finite values, source identity, resolution and the behavior of the complete system. Historical `INCONCLUSIVE`, `SUPPORTED` and other labels remain attached to the diagnostics that produced them. They are not silently rewritten or promoted into verdicts on the ontology. [Method and preservation rules](project-rules.md), lines 27–47.

<a id="five-central-cases"></a>
## Five central cases

<a id="finding-uni-002"></a>
### Memory: a large recorded difference, with a term removed

The N=40 record compares a branch called `full` with a branch called `no-memory`:

| Recorded quantity | `full` label | `no-memory` label |
|---|---:|---:|
| Final density peak | 0.000640882 | 3.889202170 |
| Final participation ratio, PR | 4,720.477435 | 0.528063 |
| Largest recorded peak | 1.651207320 | 4.170131021 |

PR describes how broadly density occupies the domain under this diagnostic; the two branches have very different final concentration. Those numbers are preserved in the [summary CSV](../../simulations/memory/memory-grid-40/results/data/summary.csv), row 2, and explained in the [original record](../../simulations/memory/memory-grid-40/notes/original-record.md), lines 12–26.

**What the comparison establishes:** a large difference between the saved branch outputs. **What is not established:** the operation of the entire indivisible equation in both branches. Memory is expressly removed in one branch, and the generating source/configuration is absent for the branch labelled `full`. A historical label cannot supply that missing implementation evidence. The retained comparison is therefore identified as a term-off record; it is not a proposed TRIAD method. **Finding UNI-002.**

<a id="finding-uni-011"></a>
### Twelve atoms: temperature, grid and observation all changed

Two records use the same placement recipe and seed for twelve Gaussian centers. Their trajectories differ visibly and numerically:

| Condition or result | Twelve-atom field | 3D atom trajectories |
|---|---:|---:|
| Bath temperature `kT` | 1 | 0.001 |
| Grid per axis, N | 32 | 40 |
| Final time, T | 15 | 12 |
| Final field norm | 25,585.351298 | 23.275045 |
| Early detected seeds | 1,147 maxima at t=0.1 | 12 seeds remain distinct through t=1 |

The colder record also adds distance-based pruning to its peak detector. Its note explains that the chosen temperature came from a supplied specification setting and kept the seeds visible longer. That is a declared physical input choice, not merely a change of numerical precision. The preserved material does not demonstrate a hidden fitting sweep; it also does not support assigning the whole contrast to temperature alone. [First record](../../simulations/structures/twelve-atoms-full-field/notes/original-record.md), lines 19–53; [second record](../../simulations/structures/3d-atom-trajectories/notes/original-record.md), lines 17–29 and 49–60.

The result is a comparison of **different recorded conditions**, including grid, duration and detector. Both runners also import a historical external runtime whose executed version is not bound by a supplied hash. The reference solver copy helps explain their intended defaults, but does not establish the identity of that external dependency. **Finding UNI-011.**

<a id="finding-uni-008"></a>
### Bounce: the same trajectory, two different questions

In the memory-and-bounce record, the root-mean-square radius, `R_rms`, is already smallest at the initial instant. Its detector returns `bounced=False`. The radius containing half the mass, `r50`, first shrinks and then expands:

| Diagnostic | Initial | Minimum | Final | Recorded reading |
|---|---:|---:|---:|---|
| `R_rms` | 3.919184 | 3.919184 at t=0 | 12.272371 | No interior contraction minimum |
| `r50` | 3.487119 | 1.385641 at t=3.7 | 9.863062 | Contraction followed by expansion |

These measurements describe different parts of the distribution. A changing outer tail can affect `R_rms` while the central half of the mass contracts. No new trajectory was needed to obtain the different labels. The density peak occurs at t=4.1 and the memory peak at t=4.2, a recorded lag of 0.1. [Original record](../../simulations/memory/memory-and-bounce/notes/original-record.md), lines 16–32; [summary CSV](../../simulations/memory/memory-and-bounce/results/data/summary.csv).

The useful presentation is the **radius trajectory and its definition**, rather than an unexplained binary badge. This record still lacks a fully bound executed source and effective bath configuration. **Finding UNI-008.**

<a id="finding-uni-014"></a>
### Q04: a weighted residual also contains the common bath

Q04 evolves A, B and their normalized combination S with the coupled terms active and the same random sequence per seed. Its recorded weighted residual rises from about zero to **0.290717 at t=0.02**, **0.293008 at t=0.1**, and a late mean of **0.386410**. The source retains `INCONCLUSIVE`. [Recorded analysis](../../simulations/field-diagnostics/linearity-tests/notes/analysis.md), lines 18–24 and 53–74.

The diagnostic needs a precise explanation: adding the same bath to all three runs does **not** cancel it when the two comparison weights add to more than one. It therefore cannot be read as a pure measure of nonlinear response or a universal failure of superposition.

<details>
<summary>Technical detail: why the common additive contribution remains</summary>

The implemented quantity is

$$R=\frac{\|S-aA-bB\|}{|a|\,\|A\|+|b|\,\|B\|},\qquad a=b\simeq\frac1{\sqrt2}.$$

For the algebraic example of an affine map $F(X)=L(X)+W$, where $L$ is linear and $W$ is a common additive contribution, the numerator contains $(1-a-b)W$. If this common contribution dominates, the normalized residual tends to $1-1/\sqrt2\simeq0.292893$—close to the scale of the early recorded values.

This calculation explains a property of the diagnostic. It neither decomposes the actual nonlinear trajectory nor attributes the entire late residual to the bath. It does not require or recommend disabling any equation term. See the [source](../../simulations/field-diagnostics/linearity-tests/code/probe_field_linearity.py), lines 330–338, 376–386 and 536–541.

</details>

The maintained interpretation is a **weighted field residual in the forced, coupled system**, with its original values and verdict preserved. **Finding UNI-014.**

<a id="finding-uni-001"></a>
### Geometry: named terms do not guarantee the same update

The geometric family contains actual implementations, saved field states and derived images. Reading the evolving kernels reveals differences from the reference beyond the previously recorded normalization guards. These differences affect the operation being computed even when comments call it the same equation.

| Reviewed operation | Supplied geometric implementation | Reference operation |
|---|---|---|
| Fourier kinetic contribution | `IFFT(-0.5*K2*FFT(psi))`, inside a contribution multiplied by `-1j` | Hamiltonian multiplier `+hbar²*k²/(2m)` |
| Stochastic increment | Gaussian draw multiplied by `dt*eta*0.02` | FDT-locked amplitude proportional to `sqrt(dt)` |
| State guard | Some kernels rescale norm above 100 to 50, repair non-finite values or inject a small field near zero | These are additional state operations, requiring disclosure |

The source also derives coefficients and a spatial memory potential through an internal feedback construction; naming that potential `V_mem` does not by itself establish the reference auxiliary-memory update. Early 1D/2D implementations include normalization on every step, and some damping expressions are phase-like. [Reference propagator and noise](../reference/equation/v1.1.md), lines 112–118 and 229–233; [3D source](../../simulations/geometry/field-3d/code/pt-BR/bravais_puro_3d.py), lines 116–129, 190–218 and 241–253.

The audit follows these kernels into the box sweep, evolving vibration runner, movie generator, perturbation tests, WiFi input and string-structure tests. Their own source links appear in the study register below. A conditional guard in code does not establish how often it fired in a saved run. **No matched rerun measured the isolated numerical effect of these differences.** The conclusion is a demonstrated implementation departure, not an invented causal explanation of every figure. **Finding UNI-001.**

Reader-only files retain their different role: `bravais_vibracoes.py` reconstructs motion from saved modes; the other vibration runner evolves a field. `simula_filmes.py` evolves; the five companion visualization files read or render its outputs. Post-processing does not become a new complete-equation execution merely because it animates.

<a id="all-17-findings"></a>
## All 17 findings

The five cases above are **[UNI-001](#finding-uni-001), [UNI-002](#finding-uni-002), [UNI-008](#finding-uni-008), [UNI-011](#finding-uni-011) and [UNI-014](#finding-uni-014)**. The remaining findings connect the other numerical contrasts and interpretation changes.

<a id="finding-uni-003"></a>
**UNI-003 · Resolution changes the reduced-memory collapse record.** At N=64/128/160, the memory-branch maximum peak is about 13.17/62.48/99.74; recorded pulse counts are 1/6/9. The no-memory final peak rises from 8.098 to 65.26, then falls to 48.25. This is a grid-dependent record with `alpha=Gamma=FDT=0` and two memory modes, including term-off comparisons. A late expanded state also does not erase the briefly crossed early threshold. [Analysis](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-160/analysis.md), lines 24–49; [configuration](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md), lines 10–18.

<a id="finding-uni-004"></a>
**UNI-004 · A thermal peak needs its norm alongside it.** Matched hot conditions in the dossier record PR=4,283/4,013 and peak=4.974/7.413 with/without memory, while norms are about 3,604/3,621. A large raw peak in those fields is not comparable to the same peak in a unit-norm field. The analysis discloses a corrected diagnostic label after considering norm; it did not rerun the trajectory to obtain that correction. The underlying configurations remain reduced and include memory removal. [Analysis](../../simulations/numerical-checks/reproduction-dossier/notes/thermal-noise-and-collapse/analysis.md), lines 17–39 and 60–69.

<a id="finding-uni-005"></a>
**UNI-005 · The barrier return ratio does not isolate a memory scar.** The linear case already has return/first-pass transmission ratio 1.5981. Memory and frozen-memory records give 2.7673 and 2.7385, with different returned packet energies and an incomplete observation window. Freezing memory also changes the dynamics. The preserved `protocol-dirty` reading matters when showing these numbers. [Analysis](../../simulations/numerical-checks/reproduction-dossier/notes/barrier-memory-and-tunneling/analysis.md), lines 6–26 and 40–64.

<a id="finding-uni-006"></a>
**UNI-006 · A clean short spectral window cannot replace a leaking long one.** The official memory record at T=251, L=80 has boundary leakage 0.3081; a short T=80, L=40 record has leakage about 6.77×10⁻¹³. They use different windows and boxes. Enlargement to check boundaries is a technical operation; selecting the cleaner short record changes the comparison being reported. Keep the official `INCONCLUSIVE` result and its conditions visible. [Analysis](../../simulations/numerical-checks/reproduction-dossier/notes/memory-and-spectral-sidebands/analysis.md), lines 10–21 and 98–119.

<a id="finding-uni-007"></a>
**UNI-007 · Repeated kL=9.424778 can come from a bin definition.** The dominant-scale analysis reports the same value in eight runs because it is $3\pi$, the first allowed shell center under that diagnostic. All eight are marked without a peaked finite-k spectrum. This constrains the interpretation of that spectral number; it does not define or exclude all dynamic crystallization. [Analysis](../../simulations/numerical-checks/reproduction-dossier/notes/dominant-spatial-scale/analysis.md), lines 8–23 and 57–59.

<a id="finding-uni-009"></a>
**UNI-009 · A reconstructed network grows from 2 to 39 nodes after extraction changes.** The first network uses quantile 0.992 and minimum distance 3 cells; the refined network selects t=4.4, quantile 0.988 and distance 2 cells. Edges change from 1 to 25. These are detector/sample choices, not a paired change of the field dynamics. The template scores in a separate Bravais map also use a different detector and regime from N=48. [First reconstruction](../../simulations/geometry/first-geometric-network/notes/original-record.md), lines 12–22; [refined reconstruction](../../simulations/geometry/refined-geometric-network/notes/original-record.md), lines 12–24; [template map](../../simulations/geometry/bravais-template-map/notes/original-record.md), lines 12–30.

<a id="finding-uni-010"></a>
**UNI-010 · The earlier hot/cold pair also changes grid and duration.** Final mass/norm changes from 8,773.747757 to 1.413637, but N changes 36→44, T changes 8→10, and the initial peaks differ. Source/configuration are insufficient for a one-factor attribution to the bath. [Hot record](../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md), lines 12–29; [cold record](../../simulations/signals/3d-cold-bath-box/notes/original-record.md), lines 12–28.

<a id="finding-uni-012"></a>
**UNI-012 · A phase-detector refinement changes the stimulus too.** The first near-zero front estimate, about 4.01×10⁻¹⁶, is followed by refined arrival estimates 7.301417/7.557409 and RMS estimates 1.482120/1.893955. Amplitude changes 0.07→0.15, width 1.3→1.25 and probe duration 1.8→5, along with the estimator/control. These different diagnostics do not establish one universal propagation speed. [First record](../../simulations/signals/first-phase-to-density-diagnostic/notes/original-record.md), lines 12–26; [refined record](../../simulations/signals/refined-phase-to-density-diagnostic/notes/original-record.md), lines 12–26.

<a id="finding-uni-013"></a>
**UNI-013 · Coupled-term convergence remains unresolved in space.** With the terms active, the late mean peak rises about 2.773→3.146→3.905→4.91566 for N=32/48/64/96. Recorded spatial relative difference is 0.205642; temporal difference is 0.011596. The spectral maximum remains near each grid cutoff. The same integer seed on different grids or time steps does not generate a common noise path. These are legitimate numerical checks, with preserved `INCONCLUSIVE` classifications, not physical coefficient fitting. [Spatial analysis](../../simulations/field-diagnostics/spatial-convergence/notes/analysis.md), lines 31–76; [refinement analysis](../../simulations/field-diagnostics/resolution-and-time-step/notes/analysis.md), lines 34–100. The [32-seed ensemble](../../simulations/field-diagnostics/seed-ensemble/notes/analysis.md), lines 68–77, documents variability at its declared grid and precision.

<a id="finding-uni-015"></a>
**UNI-015 · The long nest matches the short endpoint before continuing.** At the shared t=8, both records give peak 4.336503, PR≈19,557.412 and norm≈18,021.708. At T=60, the longer record has peak 3.372458, PR≈28,301.592 and norm≈32,692.307. This is a continuation with changing time, not an independent replicate. Its source analysis also distinguishes an automatic peak-based bounce flag from a mass-radius bounce and records continuing fluctuations. [Long-run analysis](../../simulations/structures/long-nest-trajectory/notes/original-record.md), lines 13–19 and 37–75.

<a id="finding-uni-016"></a>
**UNI-016 · The pockets are responses to declared inputs.** At t=0.5 the single-pocket runner adds a Gaussian. Local mass changes 12.72→13.80; at t=0.8 the reported density-memory correlation is 0.888 inside versus 0.723 outside. The two-pocket runner adds two signed inputs. These inputs do not remove equation terms, but they must remain visible in any story about the appearance of a pocket. The author’s observer vocabulary is an interpretation of the field diagnostic. [Pocket record](../../simulations/structures/a-pocket-in-the-field/notes/original-record.md), lines 23–31; [map](../../simulations/structures/density-memory-maps/notes/original-record.md), lines 21–29; [input source](../../simulations/structures/a-pocket-in-the-field/code/simulate_field_pocket.py), lines 515–526.

<a id="finding-uni-017"></a>
**UNI-017 · “Sem falsificar” is not evidence of a Popperian protocol.** The scoped current documentation explicitly rejects Popperian falsification as its governing method. In historical records, `SEM FALSIFICAR` describes data integrity: not deleting runs, changing windows or rewriting observables after the result. Keyword matches alone would misclassify that passage. Conventional comparisons and historical verdict labels likewise require their original context; they do not override the author’s rules. [Project rules](project-rules.md), lines 27–41; [historical definition](../reference/records/triad-qm-blueprint.md), lines 127–140.

<a id="every-study"></a>
## Every study

These statuses describe **what the supplied record establishes about its operation**. They do not rank the value of a study or certify a scientific conclusion. A study containing several files can include both an evolving implementation and reader-only artifacts; the row explains the relevant distinction.

| Status | Entries | Meaning |
|---|---:|---|
| Coupled terms documented | 14 | The standalone source and recorded configuration document the coupled operators, three memory fields, dissipation and FDT noise. This is not a claim of complete conformity, successful convergence or runtime certification. |
| Documented implementation departure | 14 | A source/configuration demonstrably departs from the complete reference. Saved results retain their actual conditions. |
| Complete operation not established | 25 | Missing source, configuration, bound runtime or run association prevents establishing completeness. |
| Context or post-processing | 12 | A specification, conceptual node model, representation or derived readout, rather than a new full-field execution. |

<details>
<summary>Criteria behind “Coupled terms documented”</summary>

For these fourteen standalone records, the reviewed constants include Λ=−10, α=0.15, σ=1.5, Γ=0.05, ν=(10, 0.5, 0.05), λ=(3, 1, 0.3), and kT=1. The reviewed update includes kinetic/fractional propagation, instantaneous self-interaction, three evolving memory fields, dissipation and the coupled complex Gaussian bath. Initial state/input normalization is distinguished from normalization during a trajectory; the latter was not found in these reviewed updates.

The pocket records include declared additions at t=0.5. Q03 discloses a post-processing correction after evolution. Q04 has the residual interpretation issue above. Numerical precision, unresolved convergence and source-record linkage limits still apply. This status records the documented joint operation; it does not certify every implementation requirement or every execution.

</details>

### Coupled terms documented · 14

| Study | Recorded scope | Source |
|---|---|---|
| <a id="study-t-30"></a>[Two atoms](../../simulations/structures/two-atoms/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Two Gaussian seeds; pair tracking is lost after t=0.01. | [lines 33–40](../../simulations/structures/two-atoms/code/simulate_two_atoms.py) |
| <a id="study-t-31"></a>[Nested positive Gaussians](../../simulations/structures/nested-positive-gaussians/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Concentric positive seeds; the recorded two-scale flag lasts through t=0.02. | [lines 33–40](../../simulations/structures/nested-positive-gaussians/code/simulate_nested_gaussians.py) |
| <a id="study-t-32"></a>[Atom inside a larger Gaussian](../../simulations/structures/atom-inside-a-larger-gaussian/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Wide envelope and two signed inner seeds; only the initial frame retains the pair. | [lines 39–46](../../simulations/structures/atom-inside-a-larger-gaussian/code/simulate_atom_inside_gaussian.py) |
| <a id="study-t-33"></a>[Concentric positive/negative nest](../../simulations/structures/concentric-positive-negative-nest/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Signed concentric nest; shell and sign flags have different recorded lifetimes. | [lines 33–40](../../simulations/structures/concentric-positive-negative-nest/code/simulate_signed_gaussian_nest.py) |
| <a id="study-t-34"></a>[Long nest trajectory](../../simulations/structures/long-nest-trajectory/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Same nest continued to T=60; the shared t=8 result agrees with the short run. | [lines 36–43](../../simulations/structures/long-nest-trajectory/code/simulate_long_gaussian_nest.py) |
| <a id="study-t-35"></a>[Finite peak, early window](../../simulations/structures/finite-peak-early-window/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. One- and two-seed early windows; finite peaks may still occupy one grid cell. | [lines 51–58](../../simulations/structures/finite-peak-early-window/code/simulate_early_peak.py) |
| <a id="study-t-37"></a>[A pocket in the field](../../simulations/structures/a-pocket-in-the-field/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. A declared Gaussian input is added at t=0.5; it is an input to the coupled field. | [lines 32–39](../../simulations/structures/a-pocket-in-the-field/code/simulate_field_pocket.py) |
| <a id="study-t-38"></a>[Two pockets](../../simulations/structures/two-pockets/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Two declared signed Gaussian inputs are added at t=0.5. | [lines 11–17](../../simulations/structures/two-pockets/code/simulate_two_field_pockets.py) |
| <a id="study-t-39"></a>[Density–memory maps](../../simulations/structures/density-memory-maps/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. The runner re-evolves the planted-pocket case and records density/memory maps; it is not only an image reader. | [lines 11–17](../../simulations/structures/density-memory-maps/code/simulate_density_memory_maps.py) |
| <a id="study-q01"></a>[Spatial convergence](../../simulations/field-diagnostics/spatial-convergence/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Grid convergence is unresolved; the recorded spectrum follows the grid cutoff. | [lines 36–43](../../simulations/field-diagnostics/spatial-convergence/code/measure_spatial_convergence.py) |
| <a id="study-q01b"></a>[Resolution and timestep](../../simulations/field-diagnostics/resolution-and-time-step/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. Spatial and time-step refinements retain the coupled terms; numerical convergence is unresolved. | [lines 38–45](../../simulations/field-diagnostics/resolution-and-time-step/code/compare_grid_and_time_step.py) |
| <a id="study-q02"></a>[An ensemble of initial conditions](../../simulations/field-diagnostics/seed-ensemble/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. All 32 recorded seeds are finite; the batch uses complex64/float32 and records its precision change. | [lines 45–52](../../simulations/field-diagnostics/seed-ensemble/code/simulate_seed_ensemble.py) |
| <a id="study-q03"></a>[Field modes and subspaces](../../simulations/field-diagnostics/field-modes/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. The source includes evolution and passive POD/DMD; its post-processing correction is declared. | [lines 52–59](../../simulations/field-diagnostics/field-modes/code/analyze_field_modes.py) |
| <a id="study-q04"></a>[Testing linearity](../../simulations/field-diagnostics/linearity-tests/README.md) | The supplied standalone update documents the coupled terms and three memory modes with FDT active. The superposition residual includes the common additive bath; it is not a pure measure of nonlinear response. | [lines 54–61](../../simulations/field-diagnostics/linearity-tests/code/probe_field_linearity.py) |

### Documented implementation departure · 14

| Study | Recorded scope | Source |
|---|---|---|
| <a id="study-bravais-01-field"></a>[Emergent 3D field](../../simulations/geometry/field-3d/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. | [lines 241–253](../../simulations/geometry/field-3d/code/pt-BR/bravais_puro_3d.py) |
| <a id="study-bravais-03-scale"></a>[Intrinsic scale](../../simulations/geometry/scale-sweep/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. | [lines 175–185](../../simulations/geometry/scale-sweep/code/pt-BR/bravais_sweep_L.py) |
| <a id="study-t-16"></a>[Memory at resolution 40](../../simulations/memory/memory-grid-40/README.md) | The saved comparison explicitly includes a no-memory branch. The generating source for the branch labelled full is absent. | [lines 12–24](../../simulations/memory/memory-grid-40/notes/original-record.md) |
| <a id="study-t-29"></a>[Memory at small amplitude](../../simulations/memory/memory-small-amplitude/README.md) | The run sets alpha=0 and uses two memory modes; its bath is active. | [lines 2–6](../../simulations/memory/memory-small-amplitude/code/simulate_memory_small_amplitude.py) |
| <a id="study-t-36"></a>[Ten-part rerun dossier](../../simulations/numerical-checks/reproduction-dossier/README.md) | The dossier mixes numerical/analytic checks with recorded term-off comparisons, including memory-off, bath-off and frozen-memory cases. | [lines 10–18](../../simulations/numerical-checks/reproduction-dossier/notes/memory-collapse-grid-64/predictions-memory-collapse-grid-64.md) |
| <a id="study-field-2d"></a>[2D field explorations](../../simulations/geometry/field-2d/README.md) | The supplied 1D/2D implementations include trajectory normalization or guards and differ from the reference evolution; the pure 2D damping expression is phase-like. | [lines 208–221](../../simulations/geometry/field-2d/code/bravais_pure_emerge.py) |
| <a id="study-dimension-comparison"></a>[Comparing 2D and 3D](../../simulations/geometry/dimension-comparison/README.md) | Both dimension branches normalize the field every step (target norms 3.0 and 2.2) and use an update different from the reference. | [lines 84–94](../../simulations/geometry/dimension-comparison/code/bravais_long_2d3d.py) |
| <a id="study-vibrations"></a>[Strings and vibration](../../simulations/geometry/vibrations/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. The separate bravais_vibracoes reader is a kinematic reconstruction. | [lines 173–183](../../simulations/geometry/vibrations/code/bravais_cordas_vibracoes.py) |
| <a id="study-field-visualizations"></a>[Field movies and visual readouts](../../simulations/geometry/field-visualizations/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. This applies to simula_filmes; the other five files are readers/renderers. | [lines 234–246](../../simulations/geometry/field-visualizations/code/simula_filmes.py) |
| <a id="study-perturbation-tests"></a>[Responses to perturbations](../../simulations/signals/perturbation-tests/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. | [lines 247–259](../../simulations/signals/perturbation-tests/code/teste_borboleta.py) |
| <a id="study-wifi-input"></a>[Fields initialized from WiFi scans](../../simulations/signals/wifi-input/README.md) | The supplied source uses a different kinetic sign/noise update and conditional state guards from the reference. The required WiFi measurements were not supplied; this entry does not document a demonstrated run with those measurements. | [lines 226–235](../../simulations/signals/wifi-input/code/bravais_wifi.py) |
| <a id="study-string-structure-tests"></a>[Strings, atoms and scale](../../simulations/structures/string-structure-tests/README.md) | The evolving source uses a different kinetic sign/noise update and conditional state guards from the reference; its saved results remain records of that implementation. | [lines 256–268](../../simulations/structures/string-structure-tests/code/probe_box_size_and_amplitude.py) |
| <a id="study-passive-r5"></a>[Passive memory dynamics](../../simulations/memory/passive-memory-dynamics/README.md) | The runner sets alpha, Gamma and FDT to zero and retains two memory modes. | [lines 23–25](../../simulations/memory/passive-memory-dynamics/code/simulate_passive_memory.py) |
| <a id="study-causal-traces"></a>[Following causal traces](../../simulations/continuity/causal-traces/README.md) | Four causal runners use a deterministic two-memory update with no fractional/bath terms. | [lines 22–25](../../simulations/continuity/causal-traces/code/soul_causal_probe_short.py) |

### Complete operation not established · 25

| Study | Recorded scope | Source |
|---|---|---|
| <a id="study-t-01"></a>[Early field relations](../../simulations/relations/early-field-relations/README.md) | Only field-relation images and an isolated/coupled description remain; no generator or numerical table. | [lines 10–27](../../simulations/relations/early-field-relations/notes/original-record.md) |
| <a id="study-t-02"></a>[Memory and thermal noise](../../simulations/memory/memory-and-thermal-noise/README.md) | NLS/memory/bath exploration survives as figures; no source or numerical table fixes the executed operator. | [lines 10–27](../../simulations/memory/memory-and-thermal-noise/notes/original-record.md) |
| <a id="study-t-03"></a>[Tracking density peaks](../../simulations/memory/tracking-density-peaks/README.md) | Peak-tracking figures survive, but the revised generator and numerical samples are absent. | [lines 10–27](../../simulations/memory/tracking-density-peaks/notes/original-record.md) |
| <a id="study-t-04"></a>[Gaussian atoms in one field](../../simulations/structures/gaussian-atoms-in-one-field/README.md) | Multi-Gaussian exploration has figures but no saved source or CSV. | [lines 10–27](../../simulations/structures/gaussian-atoms-in-one-field/notes/original-record.md) |
| <a id="study-t-05"></a>[Individual fields](../../simulations/structures/individual-fields/README.md) | Separate-identity fields are described visually; the implementation and CSV are absent. | [lines 10–27](../../simulations/structures/individual-fields/notes/original-record.md) |
| <a id="study-t-06"></a>[Limit-test attempt](../../simulations/signals/limit-test-attempt/README.md) | Preparation note only; no persisted execution artifacts. | [lines 10–20](../../simulations/signals/limit-test-attempt/notes/original-record.md) |
| <a id="study-t-07"></a>[Fast limit sweep](../../simulations/signals/fast-limit-sweep/README.md) | The N/radius sweep has CSV values, but no supplied generator establishes the full dynamics. | [lines 10–27](../../simulations/signals/fast-limit-sweep/notes/original-record.md) |
| <a id="study-t-08"></a>[Observer relations in a field](../../simulations/relations/observer-and-observed/README.md) | Baseline/observer CSVs exist; the field solver and parameter mapping are absent. | [lines 10–27](../../simulations/relations/observer-and-observed/notes/original-record.md) |
| <a id="study-t-09"></a>[Continuous relational field](../../simulations/relations/continuous-relational-field/README.md) | Baseline/continuous-relation data exist without the generating solver and complete configuration. | [lines 10–27](../../simulations/relations/continuous-relational-field/notes/original-record.md) |
| <a id="study-t-10"></a>[3D anti-collapse exploration](../../simulations/memory/3d-anti-collapse-exploration/README.md) | The early 3D exploration survives only as figures and notes. | [lines 10–27](../../simulations/memory/3d-anti-collapse-exploration/notes/original-record.md) |
| <a id="study-t-11"></a>[Long-run attempt](../../simulations/structures/long-run-attempt/README.md) | Preparation note only; effective long-run outputs belong to other entries. | [lines 10–18](../../simulations/structures/long-run-attempt/notes/original-record.md) |
| <a id="study-t-12"></a>[Fast 3D long run](../../simulations/structures/fast-3d-long-run/README.md) | Five long-run diagnostics are preserved as images without CSV or generator. | [lines 10–27](../../simulations/structures/fast-3d-long-run/notes/original-record.md) |
| <a id="study-t-13"></a>[Compact 3D long run](../../simulations/structures/compact-3d-long-run/README.md) | Compact long-run montage and diagnostics lack a saved generator and numerical table. | [lines 10–24](../../simulations/structures/compact-3d-long-run/notes/original-record.md) |
| <a id="study-t-14"></a>[Memory reference attempt](../../simulations/memory/memory-reference-attempt/README.md) | Reference-run preparation only; no output artifacts establish an execution. | [lines 10–18](../../simulations/memory/memory-reference-attempt/notes/original-record.md) |
| <a id="study-t-15"></a>[Accelerated memory reference](../../simulations/memory/accelerated-memory-reference/README.md) | Accelerated preparation note only; outputs start in the separate N=40 record. | [lines 10–18](../../simulations/memory/accelerated-memory-reference/notes/original-record.md) |
| <a id="study-t-17"></a>[Memory at resolution 48](../../simulations/memory/memory-grid-48/README.md) | N=48 numerical metrics and Bravais scores are present; the generator and exact term configuration are absent. | [lines 10–27](../../simulations/memory/memory-grid-48/notes/original-record.md) |
| <a id="study-t-19"></a>[Hot-bath diagnostic failure](../../simulations/signals/hot-bath-diagnostic-failure/README.md) | The hot-bath record has CSVs but no bound solver/configuration for a completeness check. | [lines 10–27](../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md) |
| <a id="study-t-20"></a>[3D cold-bath box](../../simulations/signals/3d-cold-bath-box/README.md) | The cold-bath CSVs change grid, duration and initial samples as well as bath conditions. The generator is absent. | [lines 10–27](../../simulations/signals/3d-cold-bath-box/notes/original-record.md) |
| <a id="study-t-21"></a>[First phase-to-density diagnostic](../../simulations/signals/first-phase-to-density-diagnostic/README.md) | The first phase/density detector has recorded near-zero estimates; its generator is absent. | [lines 10–27](../../simulations/signals/first-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-22"></a>[Refined phase-to-density diagnostic](../../simulations/signals/refined-phase-to-density-diagnostic/README.md) | The refined detector changes the stimulus and observation window; its generator is absent. | [lines 10–27](../../simulations/signals/refined-phase-to-density-diagnostic/notes/original-record.md) |
| <a id="study-t-23"></a>[Memory and bounce](../../simulations/memory/memory-and-bounce/README.md) | Bounce metrics and memory records exist, but the executed bath amplitude/source is not fully bound. | [lines 10–27](../../simulations/memory/memory-and-bounce/notes/original-record.md) |
| <a id="study-t-27"></a>[Twelve initial atoms](../../simulations/structures/twelve-atoms-full-field/README.md) | The runner calls an external triad-lang runtime at a historical absolute path; that executed dependency is not bound by hash. | [lines 22–31](../../simulations/structures/twelve-atoms-full-field/code/simulate_twelve_atoms.py) |
| <a id="study-t-28"></a>[3D atom trajectories](../../simulations/structures/3d-atom-trajectories/README.md) | The 3D trajectory runner retains three memory modes and a bath but imports the unbound historical runtime. | [lines 24–33](../../simulations/structures/3d-atom-trajectories/code/simulate_atom_trajectories.py) |
| <a id="study-string-catalogue"></a>[A catalogue of strings](../../simulations/geometry/string-catalogue/README.md) | The collector imports solver defaults/environment overrides; the recorded rows do not bind every generating configuration. | [lines 29–55](../../simulations/geometry/string-catalogue/code/colhe_cordas.py) |
| <a id="study-persistent-universe"></a>[A persistent field prototype](../../simulations/continuity/persistent-universe/README.md) | Modal checkpoints/readouts and continuation tests exist; the evolution is delegated to an external native library absent from the supplied source. | [lines 30–40](../../simulations/continuity/persistent-universe/code/genesis_modal.py) |

### Context or post-processing · 12

| Study | Recorded scope | Source |
|---|---|---|
| <a id="study-entre-01-observer"></a>[Observer and observed](../../simulations/relations/observer/README.md) | Finite-node phase/edge-memory model for conceptual relations, not an execution of the full field equation. | [lines 116–138](../../simulations/relations/observer/code/en/simulate_observer_observed_relations.py) |
| <a id="study-entre-02-between"></a>[The between](../../simulations/relations/between/README.md) | Finite-node phase/edge-memory model for conceptual relations, not an execution of the full field equation. | [lines 88–101](../../simulations/relations/between/code/en/simulate_consciousness_between.py) |
| <a id="study-entre-03-chemistry"></a>[Eight coupled channels](../../simulations/relations/chemical-channels/README.md) | Finite-node phase/edge-memory model for conceptual relations, not an execution of the full field equation. Optional chemistry/life layers are model switches, not direct P1/P2/P3 ablations. | [lines 113–152](../../simulations/relations/chemical-channels/code/en/simulate_neurotransmitters_between.py) |
| <a id="study-entre-04-life-filter"></a>[Memory and life filter](../../simulations/relations/life-filter/README.md) | Finite-node phase/edge-memory model for conceptual relations, not an execution of the full field equation. Optional chemistry/life layers are model switches, not direct P1/P2/P3 ablations. | [lines 139–184](../../simulations/relations/life-filter/code/en/simulate_life_filter_between.py) |
| <a id="study-bravais-02-strings"></a>[Strings from a saved state](../../simulations/geometry/string-analysis/README.md) | Post-processing of saved field states; this item does not evolve the complete equation. | [lines 1–12](../../simulations/geometry/string-analysis/code/cordas_arte.py) |
| <a id="study-visual-comparisons"></a>[Additional visual comparisons](../../simulations/geometry/visual-comparisons/README.md) | Preserved visual comparisons without an established generating-run association. | [lines 5–9](../../simulations/geometry/visual-comparisons/README.md) |
| <a id="study-t-18"></a>[Visual atlas](../../simulations/geometry/visual-atlas/README.md) | Readout or geometric reconstruction from a recorded field, not a new field evolution. | [lines 10–22](../../simulations/geometry/visual-atlas/notes/original-record.md) |
| <a id="study-t-24"></a>[Bravais template map](../../simulations/geometry/bravais-template-map/README.md) | Readout or geometric reconstruction from a recorded field, not a new field evolution. | [lines 10–22](../../simulations/geometry/bravais-template-map/notes/original-record.md) |
| <a id="study-t-25"></a>[First geometric network](../../simulations/geometry/first-geometric-network/README.md) | Readout or geometric reconstruction from a recorded field, not a new field evolution. | [lines 10–22](../../simulations/geometry/first-geometric-network/notes/original-record.md) |
| <a id="study-t-26"></a>[Refined geometric network](../../simulations/geometry/refined-geometric-network/README.md) | Readout or geometric reconstruction from a recorded field, not a new field evolution. | [lines 10–22](../../simulations/geometry/refined-geometric-network/notes/original-record.md) |
| <a id="study-q00"></a>[Reference specification](../../simulations/field-diagnostics/reference-specification/README.md) | Specification and frozen declared parameters; no execution result in this item. | [lines 6–14](../../simulations/field-diagnostics/reference-specification/notes/specification-record.md) |
| <a id="study-dimension-analysis"></a>[Measuring spatial structure](../../simulations/geometry/dimension-analysis/README.md) | Post-processing of saved field states; this item does not evolve the complete equation. | [lines 1–12](../../simulations/geometry/dimension-analysis/code/bravais_dimensoes.py) |


<a id="coverage"></a>
## Coverage and preservation

The catalog inventory covers **65 entries and 1,146 associated file paths**. All **165 CSVs and 100 JSONs** were parsed without parse errors. The inventory includes **73 text source files**, of which **70 are Python files with 33,410 lines**. The reference solver and the earlier [19 source findings](../maintenance/author-rules-audit.md) supply additional context for this review.

The work combined inventory, hashes, structured-file parsing and focused reading of evolution kernels, configurations, numerical records and diagnostics. **It was static and documentary: zero simulation reruns, zero scientific source edits.** Arrays and images were inventoried and hashed; they were not all numerically or visually reanalysed. Large accumulated records were searched and relevant passages examined, rather than newly read line by line in full.

All **1,062 catalog files other than Markdown** matched their recorded original SHA-256 values and remained unchanged during this audit. Of the 84 catalog Markdown files, 51 differ from original archive hashes because of documented link rewriting; that is not reported as a changed numerical payload. Navigation changes and source preservation have separate provenance.

Interpretation corrections belong on the maintained study pages and here. Original code, numbers, failed diagnostics and historical verdicts remain available as the record. A numerical contrast is reported only when saved measurements support it; an implementation difference alone is not presented as a measured change in outcome.

Audit attribution: `codex/equation_context_review` · task `T-2026-0039` · 2026-09-18.

[Project rules](project-rules.md) · [Equation reference](../reference/equation/README.md) · [Previous implementation audit](../maintenance/author-rules-audit.md) · [Simulation catalog](../../simulations/README.md)
