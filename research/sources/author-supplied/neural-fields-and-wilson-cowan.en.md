<!-- Translation of: research/sources/author-supplied/neural-fields-and-wilson-cowan.md; source commit: 304d75ed6ff646d311fd9df8b4e2db0d4dee277a -->
<!-- convertido de grok_report-67.pdf -->

"Neural field" here is the Wilson-Cowan/Amari/Nunez lineage: activity as a continuous function of cortical space — not NeRF (radiance field). HORN said the right sentence: local oscillation and global wave are the same object at two scales. The field is the continuous scale.

The object

Instead of N neurons, a field u(x, t): mean rate (or potential) at point x of the tissue, at time t. Interaction is not one Wij per pair: it is a spatial kernel w(x, x′) (how much site x′ pulls site x). Canonical form (Amari):

τ∂tu(x,t) = −u(x,t) + ∫ w(x,x′) S(u(x′,t)) dx′ + I(x,t)

S is the sigmoid (rate vs. input). Wilson-Cowan separates E and I populations:

τE∂tE = −E + S(wEE(KEE ∗ E) − wIE(KIE ∗ I) + P)
τI∂tI = −I + S(wEI(KEI ∗ E) − wII(KII ∗ I) + Q)

∗ is convolution in space. The classic Mexican hat — excitation near, inhibition far — is a w yielding a stable bump (spatial working memory), traveling wave, or Turing pattern, depending on gain.

Nunez: the same spirit becomes a brain-wave equation when axonal delay enters. Coombes et al.: the modern field is a generalized "brain-wave equation".

What the field does that the point RNN does not show

Standard repertoire (Bressloff / Coombes, reviews):

- traveling fronts and pulses
- breathers (localized oscillation)
- 2D spirals
- Turing patterns (V1-type geometric hallucination)
- persistent bump (spatial WM, head direction)

The refractoriness Wilson-Cowan already put in the 1972 model changes the physics: a purely excitatory network, which without refractoriness only carries fronts, starts carrying a periodic wave.

Reynolds et al. (ScienceDaily / 2026 framework, awake visual cortex): the traveling wave is not EEG decoration. Four proposed functions — adjusting perception in the moment, turning recent sensory input into representation, predicting the short term, pattern replay. An analogy they write themselves: learned statistics generating the next state, "like an LLM generates text." Here the generator is the wave in the tissue, not the token.

This matches the crow LFP (beta/gamma in NCL) and HORN (interference = representation): three scales, one language.

HORN as discretization of the field

Singer/Effenberger, PNAS 2025, explicit: HORN with local connectivity + geometric stimuli learns a Mexican-hat-like kernel. That graph is the mesh of a field whose associated continuum is a damped wave equation. Supplement movies: different stimulus, different wave direction and shape.

Therefore:

- HORN | neural field
- Space: n nodes | continuous x ∈ Z
- Time: Euler of the 2nd-order ODE | integro-differential equation / wave
- Kernel: Whh (learned) | w(x, x′) (imposed or fitted)
- Representation: transient interference | front, bump, spiral
- Ring parameter: axonal delay, τ, E/I gain

Raising n and localizing W is going from HORN to the field. Lowering the field to a mesh of oscillators is HORN.

From continuum to the real graph (measured brain)

Graph neural fields (PLoS / PMC): the same Wilson-Cowan, but the domain is not the plane — it is the connectome (DTI + MRI). Graph Laplacian in place of the continuum one. Fluctuation at equilibrium reproduces the resting-fMRI harmonic spectrum and predicts functional connectivity. Their appendix: damped wave on the human graph.

Low-dimensional field (Neuron 2025–26): SNN of N LNP neurons, N → ∞, becomes a field vt(z) in circuit space Z. If the embedding z is rank-D, the field collapses to a D-dimensional system — the rigorous bridge between "full net" and "neural mass." Nature Neuroscience (Sep 2026) highlights a single RNN trained on multiarea recordings (fish, mouse, primate, human) to infer current between regions. Field here is a measurement tool, not just theory.

What AI did with the idea (without calling it cortex)

Three branches the name "neural field" mixes today — best not to mix:

1. Trainable classic field. Conv-RNN that learns to emit waves in the hidden state (arXiv 2502.06034): the wave sequence becomes visual representation; effective receptive field grows without a global U-Net; semantic segmentation with fewer parameters. It is HORN/field applied to vision.
2. Neural Field Turing Machine (arXiv 2509.03370): controller + memory as a continuous field + heads reading/writing a local patch. O(N) per neighborhood, Turing-complete under bounded error. Instances: Rule 110, 2D heat, inpainting. Field as differentiable spatial tape.
3. Implicit neural representations / NeRF / SiREN / Functa. "Neural field" in graphics: a network parameterizing f(x), color or SDF. CORDS, ENF, FGN (2026) take this to graphs ("the graph is a sample of an entropy field"). Different family: no Wilson-Cowan wave; a continuous function in place of the mesh.

Whoever comes from HORN wants branches 1–2. Branch 3 only shares the name.

Why it exists (computation, not poetry)

Field/wave solves what the transformer solves with global attention, differently:

- long integration with local weight — the wave carries context; the kernel is short; the effective receptive field is travel time;
- spatial prior in hardware — Mexican hat is WM; no need to learn "hold a bump";
- same language as the LFP — what you measure in crow and V1 is the field;
- scale: continuum or connectome graph, not dense N².

Cost: stability analysis (Turing, Hopf in the field) instead of "stack one more layer." Identifiability: Cremers showed that a plane wave in a rate model and in integrate-and-fire map onto each other, but the kernel inferred from wave speed depends on the microscopic class. Measuring speed ± reading anatomy without a model.

On the thread of the chat

```text
interference
visual NCC
traveling wave / bump
without layer
Y, w, delay
kernel w(x,x')
```

OpenMythos/RDT: loop in layer time. Field/HORN: loop in the wave's physical time. J-space: workspace that interpretability finds in the LLM. Field: workspace that anatomy is (activity become global as it passes). They are not the Mythos. They are — you localize the weights and let the node oscillate; the film that comes out is a field. Neural field networks are this film written [garbled in the converted source] — the mesh from back to front.
