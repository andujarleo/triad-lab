# Predictions — tunneling with memory in the barrier (pure history)

Date: 2026-08-21 (America/Sao_Paulo)
Label: independent re-execution, dossier pending item 6
Scope: 1D two-pass tunneling. History of the *barrier* (y left on V_ext), not cubic focusing.
Stepper: standalone 1D Strang from `/workspace/dossie_reexec/QM1D/code/stepper1d.py` (copied, not rewritten).
Convention: ħ = m = 1, periodic FFT, fp64, system numpy, Λ=0, α=0, Γ=0, f_FDT=0.

These are pattern predictions written BEFORE any two-pass integration.
Do not treat them as a chosen winner or as the dossier's floats.
Do not retune λ, ν, V0, a, dt, or the reversal protocol to force an effect.
Keep failures.

## Shared equation (what we will integrate)

```
i ∂t Ψ = [ -∂xx/2 + V_ext + V_mem ] Ψ
V_mem = Σ λj yj,   ∂t yj = νj(|Ψ|² − yj)
```

Strang as in stepper1d.py: k-space half linear → real-space V = V_ext + V_mem → Euler memory → k-space half linear.
No Λ|Ψ|², no fractional, no Γ, no FDT.

Barrier: square V0=4, width a=1, on [-0.5, 0.5].
Packet: E=2, s=2, k0=+2, start x=-20.
Box: L=120 (wrap prevention), N=2048 or 4096, dt=0.002.

P5 linear reference (already run, not this experiment): T(V0=4) ≈ 0.095 at L=80, T=20, mass(x>0.5)/total.

## Frozen two-pass protocol (will not be retuned)

Honest, no teleport of the packet onto a fresh barrier.

1. Pass 1: launch from the left. Evolve until t_mid = first time after the collision when mass in |x|<2 is minimal (split complete) and edge mass is still tiny. Store
   T1 = mass(x>2) / total,   R1 = mass(x<-2) / total.
   Residual on barrier = mass(|x|≤0.5). Leak/wrap = mass near periodic edges.
2. Zero the LEFT leftover: Ψ ← 0 for x<0. Keep y everywhere (barrier stain intact). Report mass_sent_back both raw and after renormalizing the remaining right packet.
3. Reverse k of the remaining field only, via FFT: psi_k[i] ↔ psi_k corresponding to −k (Nyquist/DC fixed). Do **not** flip x, do **not** touch y. The transmitted piece on the right becomes left-going and heads back at the same barrier. The reflected piece is already gone (zeroed).
4. Pass 2: evolve to t_final, chosen the same way (mass in |x|<2 minimal after the return collision, no wrap).
   T2 = mass(x<-2 at t_final) / mass_sent_back.
   Also record residual-on-barrier and edge leak.

Configs (λ, ν not retuned):

- A. linear no mem (control): lam=(), nu=()
- B. memory live both passes: lam=(3, 1), nu=(10, 0.5)
- C. if wall time allows: same as B for pass 1, then freeze y during pass 2 (pure static scar; V_mem still applied, ∂t y = 0)

Identical reversal / zeroing / windows for all three. Control dirtiness is diagnosed on A, not fixed by changing B.

## Mechanism (why a history effect could exist)

λj > 0 is repulsive. During pass 1 a small density sits in the barrier (evanescent + whatever tunnels). The memory ODE writes yj > 0 there. After the packet leaves, y decays on timescales 1/ν:

- fast channel ν=10 → τ=0.1 (gone long before the return)
- slow channel ν=0.5 → τ=2

Return travel time after a clean split is several time units (packet must clear |x|<2, then come back from x ~ +O(10) at v=k0=2). Slow-channel remnant at the barrier is then y2 ~ y2(t_mid) · e^{−Δt/τ} with Δt/τ of order 1–3, i.e. a *small* extra potential V_mem = 3 y1 + 1 y2 on top of V0=4.

If that remnant is still positive on the barrier when the returning packet arrives, the barrier is effectively higher where the packet was, so tunneling is harder: T2 < T1.

This is a history-of-the-barrier effect, not a cubic (Λ=0).

## Predicted pattern (not a winner, not dossier floats)

### A. Linear, no memory (control)

T2 ≈ T1. No barrier history, so the second pass is the same Hamiltonian.

Expected T1 near the P5 number ~0.095 (L is larger, measurement window is mass(x>2) not mass(x>0.5); small shift only).

Small differences T2 ≠ T1 are allowed from:

- residual distortion of the transmitted packet (the barrier is a momentum filter: higher-k components transmit more, so the piece we send back is not the original Gaussian)
- incomplete first exit / a little mass still in |x|<2 when we reverse
- wrap-around if the box is not as empty as we think
- the k-flip plus hard cut Ψ(x<0)=0 (spectral ringing)

If |T2/T1 − 1| is only a few percent and leak flags are tiny, the protocol is clean enough to read B.
If |T2/T1 − 1| is large (energy filtering of a Δk~1/s=0.5 packet against V0=4, E=2 can be substantial), the control is dirty: T2≠T1 is then *not* a history effect. Keep that. Do not narrow s, raise E, or change V0 to hide it.

### B. Memory live, λ=(3,1), ν=(10,0.5)

The *prediction the item asks for*: repulsive memory left in the barrier ⇒ T2 < T1 (second pass harder). Ratio T2/T1 < 1.

Competing effects we will not retune away:

1. Stain decay. If Δt ≫ τ_slow, y on the barrier is ~0 at return and B collapses to “no-effect” (T2/T1 ≈ A’s ratio). That is a physical miss of the history window, not a reason to enlarge λ or shrink ν.
2. Live writing on pass 2. B evolves y during the return too. Pass 1 already felt a forming stain, so T1_B may already be below T1_A. The history increment is T2_B vs T1_B, not T1_B vs T1_A.
3. Memory trail *outside* the barrier (y along the transmitted path). The returning packet walks through its own decaying wake. That is extra history, not a protocol bug, and is part of “memory on during both passes.”
4. Same packet-distortion systematics as A. The fair comparison is (T2/T1)_B versus (T2/T1)_A.

If (T2/T1)_B is clearly below (T2/T1)_A and A is clean, that is the repulsive-scar signature.
If both ratios sit at ~1, the stain died or was too weak (no-effect). Keep λ=(3,1).
If A is already far from 1, B is unreadable (protocol-dirty).

### C. Optional frozen scar

Pass-1 y is frozen for pass 2. No decay, no extra writing. This is the cleanest static “scar on V0” test:

- if the stain is repulsive and sits on the barrier, T2 < T1, and the drop should be *at least* as large as in B (B still decays)
- if C also shows T2≈T1, the written y inside the barrier was negligible (packet density in a=1 is small; most of the Gaussian never sits in V0)

Skip only if wall time forces it; record the skip.

## Leak / wrap / residual flags (all configs)

Report at t_mid and t_final:

- mass_bar = mass(|x|≤0.5)
- mass_mid = mass(|x|<2)
- mass_edge = mass(|x| > L/2 − 6)
- norm

Protocol-dirty if any of: mass_edge ≳ 1e-4 at a measurement; mass_mid at t_mid not a post-collision minimum; T1+R1 far from 1; control |T2/T1−1| large compared to the B−A contrast.

## What would count as a verdict (applied after the runs)

- **harder**: A clean (T2/T1 ≈ 1, leaks tiny) AND (T2/T1)_B (and C if run) clearly < (T2/T1)_A. Repulsive scar did what the item guessed.
- **easier**: A clean AND (T2/T1)_B clearly > (T2/T1)_A. Opposite of the repulsive-scar guess (e.g. attractive effective remnant, or spectral reshaping). Keep it.
- **no-effect**: A clean AND B (and C) sit on the same T2/T1 as A within the distortion floor. Stain too weak or too decayed. Keep λ.
- **protocol-dirty**: control T2 not ≈ T1, or wrap/residual flags fail, so the history increment cannot be read. Keep the numbers; do not retune.

Dossier floats are not a target. This item has no published T2/T1 table that we are matching.

## What we will not do

- Will not raise λ or lower ν to keep the stain alive until return.
- Will not teleport a fresh Gaussian onto a prestained barrier (that is not two-pass).
- Will not flip y with the wave (that would move the stain off the barrier).
- Will not drop config A, or diagnose dirtiness on B instead of A.
