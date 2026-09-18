> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/predictions/predictions_CHSH.md) · [Collection / Acervo](../../../../README.md)

# Predictions -- CHSH / Bell frontier (written BEFORE any shot)

Status: PREDICTIONS ONLY. No pair-coupled Strang step has been taken. No shot has been evolved.
Re-execution label: independent re-run of dossier "TRIAD -- Dossie unificado" (2026-08-21) Fronteira CHSH / Emaranhamento + spec 11.1 pair coupling (23).
Date written: 2026-08-21 (America/Sao_Paulo).
Box: Linux, /usr/bin/python3, NumPy 2.2.4, fp64.

These are pattern predictions, not copies of the dossier floats.

## Frozen protocol (will not be retuned)

Two 1D real-line fields PsiA, PsiB, each:

    i dt Psi = [ -dxx/2 + V_ext + Lambda |Psi|^2 + V_mem ] Psi
    V_mem = sum_j lam_j y_j,   dt y_j = nu_j (|Psi|^2 - y_j)

Lambda = -2, lam=(3,1), nu=(10,0.5), alpha=0, Gamma=0, f_FDT=0 (unitary pair).

Pair coupling spec (23) / 11.1, lockstep, V_ext updated every step from partner density:

    V_ext^A(x,t) = kappa |PsiB(x,t)|^2
    V_ext^B(x,t) = kappa |PsiA(x,t)|^2

1D, L=40, N=256, dt=0.002, s=1.0 (downgrade to N=128, dt=0.005, T=1.5 only if wall time forces it; record the downgrade).

Per shot:
1. Physical RNG seed = 10000+shot. Draw phi ~ Uniform[0, 2pi). Frozen phase convention: both packets get e^{i phi} ("fonte de fase comum"). Distinguishability: A centered at -3, B at +3, k0=0 (no kicks).
2. Coupled evolution: kappa=0.5 for T_couple=2.0.
3. Separation: kappa=0 for T_sep=2.0 (keep evolving, drop the cross term).
4. Settings RNG seed = 900000+shot, independent of the physical seed. Angles assigned BEFORE looking at the field. Balanced design: 350 shots per pair of the CHSH set {(0, pi/4), (0, -pi/4), (pi/2, pi/4), (pi/2, -pi/4)}, 1400 total. Pair index = shot % 4 (fixed before any evolution).
5. Local binarized quadrature, frozen:
       A = +1 if Re(e^{-i a} <PsiA | psi0A>) >= 0 else -1
       B = +1 if Re(e^{-i b} <PsiB | psi0B>) >= 0 else -1
   psi0A / psi0B = the unphased local gaussian envelope of that side (shape at the side's center, stored at t=0). The random phase lives in the field, not in the envelope -- otherwise a global phase cancels in the overlap and every shot with the same (a,b) is identical (protocol would fail to sample E). The other side's field is never used in the measurement.

No post-selection. All 1400 shots count. Marginals published.

## Mechanism prediction (why this cannot be a singlet)

Two 1D complex fields coupled only through density are still two single-particle fields on a line. That is a 2-copy 1-body description, not a 3N-dimensional two-body wavefunction. Density coupling is a local real potential: it cannot manufacture the antisymmetric spin singlet of QM.

The only shared randomness is the common phase phi (plus whatever deterministic dynamical phase each side accumulates). The frozen measurement is

    A = sign cos(phi - a + alphaA),   B = sign cos(phi - b + alphaB)

with alphaA, alphaB dynamical phases of each side. If alphaA ~ alphaB (identical envelopes, same Hamiltonian structure), this is the classic continuous-phase local hidden-variable model:

    E(Delta) = 1 - 2|Delta|/pi     for |Delta| <= pi    (triangular, not cos Delta)

and the CHSH combination with a=0, a'=pi/2, b=pi/4, b'=-pi/4 saturates

    S = E(a,b)+E(a,b')+E(a',b)-E(a',b') = 1/2+1/2+1/2-(-1/2) = 2.

Local hidden-variable / single-field realism => |S| <= 2. We predict S <= 2 within sampling error.

Packets at +/-3 with s=1 barely overlap at t=0; they spread and the density cross-term becomes visible later. That coupling can shift alphaA, alphaB and slightly deform the envelopes. It should not create a Tsirelson point.

## Predicted pattern (not dossier floats)

- S <= 2 within sampling error. With 350 shots/pair, se(E) ~ 1/sqrt(350) ~ 0.053 (or sqrt((1-E^2)/n) ~ 0.046 if |E|~0.5). se(S) ~ 0.1 if the four pairs are independent.
- Four correlators near the triangular CHSH point: E(0,pi/4)~E(0,-pi/4)~E(pi/2,pi/4)~+0.5, E(pi/2,-pi/4)~-0.5. Not the QM values 1/sqrt(2).
- E(Delta) closer to triangular (1-2Delta/pi) than to QM cos Delta, if the 6-point scan is run.
- Marginals P(A=+1|a) and P(B=+1|b) near 1/2 (phase is uniform).
- No-signaling: P(A=+1|a,b) ~ P(A=+1|a,b') within binomial noise (settings do not enter the evolution). Same for B.

## What would count as a surprise -- KEEP, do not retune

- S > 2.1: a genuine Bell violation on this pair-density protocol. Keep kappa, angles, measurement. Do not push it back under 2.
- S << 1 (e.g. |E| all near 0): the protocol failed to correlate (phase cancelled, or envelopes orthogonal after evolution). Keep that too.
- S ~ 2 with triangular E: expected saturation of the local bound, matching the dossier pattern (they reported S = 2.000 +/- 0.053, E triangular).

## MATCH / PARTIAL / FAIL vs dossier (applied after the shots)

Dossier: S = 2.000 +/- 0.053; E(a,b)=0.486, E(a,b')=0.511, E(a',b)=0.510, E(a',b')=-0.493; E(Delta) triangular ~1%.

- MATCH: S within ~2 se of 2, |S| not above 2.1, four E values within ~0.15 of the triangular CHSH point, and (if scanned) E(Delta) closer to triangle than to cos.
- PARTIAL: S <= 2 and clearly correlated, but E not triangular, or S near 2 with much larger noise, or scan skipped and correlators only roughly 0.5.
- FAIL: S > 2.1 (QM-like; keep) OR S << 1 (no correlation; keep) OR no-signaling grossly violated (settings leaked into the field).

Dossier floats are comparison targets, not tuning targets.

## Frozen choices (explicit)

- Phase: both packets x e^{i phi} (same sign). Not e^{i phi} / e^{-i phi} -- opposite signs would correlate in (a+b), not in Delta=|a-b|, and would miss the dossier triangle.
- Envelope psi0: unphased local gaussian of that side, stored at t=0. Not the phased field (that cancels phi).
- Settings: balanced 350/pair, pair = shot % 4, assigned from seed_settings before evolution.
- Memory IC: y = 0 (blank) on both sides.
- No discarding.
