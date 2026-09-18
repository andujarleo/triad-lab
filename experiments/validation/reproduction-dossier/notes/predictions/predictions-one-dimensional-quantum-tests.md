# Predictions — QM via Triad 1D pillars (re-execution)

Date: 2026-08-21
Label: independent re-execution of dossier "TRIAD — Dossiê unificado dos testes e simulações"
Scope: pillars P1–P6 only (NOT CHSH)
Stepper: standalone 1D Strang (no triad-lang TriadParams)
Convention: ħ = m = 1, periodic FFT, fp64, system numpy 2.2.4

These are pattern predictions written BEFORE any integration.
Do not treat them as forecasts of the dossier's exact floats.

## Shared equation and stepper (what we will integrate)

```
i ∂t Ψ = [ -∂xx/2 + V_ext + Λ|Ψ|² + V_mem + α(-Δ)^{σ/2} - iΓ ] Ψ + η
V_mem = Σ λj yj,   ∂t yj = νj(|Ψ|² − yj)
```

Strang: k-space half linear (kinetic + fractional + Γ drain)
→ real-space potential V = V_ext + Λρ + V_mem
→ Euler memory
→ optional FDT kick
→ k-space half linear.

FDT: noise_amp = sqrt(f_FDT * dt / dx);
ξ = (rng.standard_normal + 1j*rng.standard_normal)/sqrt(2);
Ψ += noise_amp * ξ.

Regime switches:
- linear: Λ=0, lam=0, α=0, Γ=0, f_FDT=0
- memory only: Λ=0, lam=(3,1), nu=(10,0.5), rest off
- anti-collapse: Λ=-10, lam=(3,1), nu=(10,0.5)
- cubic only: Λ=-10, lam=0

## P1 Interference

Setup: two Gaussians, s=1, centers ±8, k0=∓2, L=80, N=1024, dt=0.002, T=8, V_ext=0.
Measure at packet overlap: spectral contrast at fringe k=±4 vs carrier k=±2; also central mass |x|<4.

Predicted pattern:
- Spectral visibility at 2k0 stays ≳ 0.9 in all four deterministic regimes.
- Memory does not erase nodes; it changes the envelope (less mass in the center).
- Cubic / anti-collapse (attractive Λ<0) may pull mass inward (higher central mass than linear).
- Linear is the reference: high visibility, nodes intact.
- We will not predict the exact visibilities or central-mass floats of the dossier.

## P2 Decoherence

Same two-packet IC as P1. Γ=0.05. Sweep f_FDT ∈ {0, 1e-3, 1e-2, 3e-2, 1e-1}, 6 seeds (0..5).
Metric MUST be spectral contrast at the fringe k, not max/min (max/min saturates on rough fields).
Fixed t = same measurement time as P1.

Predicted pattern:
- Single-shot spectral contrast survives better than the ensemble-average contrast.
- Ensemble contrast falls as f_FDT rises (fringe lives in the shot, dies in the average).
- At f_FDT=0 the two contrasts should be close (deterministic + only Γ).
- If a metric saturates, report saturation rather than retuning.
- Do not predict the dossier's exact contrast table.

## P3 Uncertainty

σx σp for (1) normalized Gaussian s=1; (2) compressed s=0.4; (3) post-collision field from P1 linear.
ħ=1 so ħ/2 = 0.5.

Predicted pattern:
- Any normalized Ψ satisfies σx σp ≥ 0.5 (Fourier theorem). Dynamics cannot violate this.
- Ground / minimum-uncertainty Gaussian (s=1, vacuum width of free packet in ħ=m=1) gives 0.5000.
- Compressed Gaussian s=0.4 is still a minimum-uncertainty packet → also 0.5000.
- Fringed post-collision field is not a Gaussian coherent packet → product > 0.5.
- Exact 0.5000 is a numerical check of the σx/σp estimator, not a dynamics result.

## P4 Quantization

Harmonic V = (1/2) ω² x², ω=1. L=20, N=512, asymmetric Gaussian s=1.0 at x0=1.2.
Long run: T≈251 so 2π/T ≈ 0.025, dt=0.01. Autocorrelation c(t)=∫ Ψ*(0) Ψ(t) dx.
FFT of c(t): peaks sit at E_n = n+1/2 on the NEGATIVE frequency side of numpy FFT (E = −ω).
Also extra configs with T=80: linear; Λ=+2 no mem; Λ=-2 no mem; Λ=-2 + mem(3,1). Lowest 4 levels.

Predicted pattern:
- Linear: first peaks at 0.5, 1.5, 2.5, 3.5, 4.5 (spacing ≈ 1).
- Boundary leak |Ψ|²_edge / max < 1e-6 if the well is well-resolved.
- Attractive cubic (Λ<0) should shift levels (typically downward / compressed spacing) vs linear.
- Repulsive cubic (Λ>0) should shift the other way.
- Memory is a delayed potential; lowest levels remain near the harmonic ladder but can shift / broaden.
- We will not predict the dossier's exact peak frequencies.

## P5 Tunneling

Linear. Packet E=2, k0=√(2E)=2, s=2, start x=-20, square barrier a=1 on [-0.5,0.5],
V0 ∈ {2.5, 3, 4, 5, 6}, L=80, N=2048, T~20.
T_trans = mass with x>0.5 / total after interaction, before wrap-around.
Fit ln T vs √(V0−E). WKB for a rectangular barrier of width a=1 is order −2.

Predicted pattern:
- T > 0 for every V0 > E (finite barrier, finite width).
- ln T is roughly linear in √(V0−E).
- Fitted slope is order −2 to −3 (WKB reference −2).
- T decreases as V0 increases. We will not predict the dossier's exact T(V0) table.

## P6 Ehrenfest

Linear harmonic ω=1, Gaussian at x0=2, s=1, k0=0, T=20 (≥3 periods of 2π).
Compare ⟨x⟩(t) to x0 cos(ωt) = 2 cos(t).

Predicted pattern:
- |⟨x⟩(t) − 2 cos(t)| stays tiny (≪ 1e-3) over ≥3 periods.
- This is a pure Fourier / harmonic-oscillator identity for a coherent state in a quadratic well.
- Any large deviation is a stepper bug (dt, aliasing, or potential discretization), not new physics.

## What would count as FAIL vs MATCH

- P1 FAIL if any deterministic regime erases the 2k0 sideband (visibility << 0.9) without a numerical cause.
- P2 FAIL if ensemble contrast does not fall with f_FDT, or if we used max/min instead of spectral contrast.
- P3 FAIL if any normalized state gives σx σp < 0.5 beyond roundoff.
- P4 FAIL if linear peaks are not near n+1/2 on the negative numpy-FFT axis.
- P5 FAIL if T=0 for finite V0, or ln T vs √(V0−E) is not roughly linear with slope O(−2).
- P6 FAIL if max |⟨x⟩−2 cos(t)| is not ≪ 1e-3.

Dossier floats are comparison targets, not tuning targets. Keep failures.
