> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/tunnel_hist/analysis.md) · [Collection / Acervo](../../../../README.md)

# Tunneling with memory in the barrier — two-pass history

**Date:** 2026-08-21 15:46 -03 (America/Sao_Paulo)
**Dossier:** pending item 6 (pure history effect)
**Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_tunnel_hist.md`). No retuning of λ, ν, V0. Failures kept.
**Stepper:** standalone 1D Strang, Λ=0, α=0, Γ=0, f_FDT=0. ħ=m=1, fp64, numpy 2.2.4.
**SHA256 stepper:** `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`
**SHA256 runner:** `b103f6d921de1067ede758da89f17d7d93bacc95549a345ead1c96ee3cc576da`
**Grid:** L=120, N=4096, dt=0.002. Barrier V0=4, a=1 on [-0.5,0.5]. Packet E=2, s=2, k0=+2, x0=-20.

Reversal: Ψ ← Ψ* after zeroing x<0 (momentum flip at fixed x; y untouched).
Naive `ψ̂(k)→ψ̂(-k)` is Ψ(x)→Ψ(-x) and would teleport the right packet; it was not used.
T1 = mass(x>2)/total at t_mid. T2 = mass(x<-2)/mass_sent_back at t_final.
Evolution after the cut is **not** renormalized (|Ψ|² drives y).

---

## Numbers

| config | T1 | T2 | T2/T1 | R1 | mass_sent | ⟨E⟩_sent | ⟨k⟩_sent | Vmem_bar mid | t_mid | flags |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A_linear | 0.081339 | 0.129984 | 1.5981 | 0.916823 | 0.081349 | 2.702 | -2.246 | 0 | 22.30 | ok |
| B_mem | 0.186303 | 0.515565 | 2.7673 | 0.753443 | 0.186825 | 5.383 | -3.049 | 1.12e-2 | 16.40 | pass1_split_incomplete |
| C_freeze | 0.186303 | 0.510197 | 2.7385 | 0.753443 | 0.186825 | 5.383 | -3.049 | 1.12e-2 | 16.40 | pass1_split_incomplete |

P5 linear reference (different window, L=80, mass(x>0.5)): T(V0=4)=0.095. Our T1_A=0.081 is mass(x>2) on L=120; the pass-1 plateau of T1_A is 0.0813 from t≈19 onward.

Residual mass on barrier at the measurement times:

| config | mass_bar mid | mass_mid mid | mass_edge mid | mass_bar fin | mass_edge fin |
|---|---:|---:|---:|---:|---:|
| A | 3.71e-5 | 1.84e-3 | 9.40e-5 | 4.4e-8 | 1.0e-6 |
| B | 1.94e-3 | 6.03e-2 | 9.81e-5 | 4.6e-7 | 2.3e-5 |
| C | 1.94e-3 | 6.03e-2 | 9.81e-5 | 5.0e-7 | 2.4e-5 |

---

## Control cleanliness (config A)

A is the protocol test. T2/T1 = **1.598**, not ≈1.

Cause is not wrap and not an incomplete first exit:

- T1+R1 = 0.998, mass_mid=1.8e-3, edge=9.4e-5 at t_mid (flags `ok`).
- Pass-2 left-lobe plateaus by t≈18 and stays there (timeseries); edge at t_final = 1e-6.

Cause **is** residual packet distortion / energy filtering, which the predictions flagged as the thing that would dirty the control:

- IC: ⟨E⟩=2.0625, ⟨k⟩=+2.00
- Sent-back transmitted piece: ⟨E⟩=2.702, ⟨k⟩=-2.246

The square barrier is a high-pass in k. The piece we reverse is hotter than the original Gaussian, so it tunnels more on the way back. T2>T1 of order 60% is that filter, not history.

Prediction said: if |T2/T1−1| is large, the protocol is dirty and B is unreadable as a barrier-scar test. That is what happened. Not retuned (no narrower s, no higher E, no different V0).

---

## Memory configs (B live, C frozen scar)

**Barrier stain is tiny.** At t_mid, mean V_mem on |x|≤0.5 is 0.011 (max 0.048) on top of V0=4. That is +0.3% of the barrier. Slow channel y1_bar=5.3e-3, fast y0_bar=2.0e-3. By t_final of live B, V_mem on the barrier has decayed to 0.004. Frozen C holds 0.011. B and C give T2=0.516 vs 0.510 — the scar does not move T2.

**T1 itself is not the linear T1.** T1_B=0.186 vs T1_A=0.081. This is already visible at t=12, before any wrap (edge 4e-6): T_B=0.181 vs T_A=0.071. Memory during pass 1 *increased* transmission. ⟨E⟩ of the full field at B's t_mid is 3.04 (A: 2.08). The repulsive wake (λ>0 writing y under the incoming packet) heats the packet; a hotter packet tunnels more. The V_mem snapshot is a large stain on the *left* of the barrier (reflected-path trail), not a bump inside V0.

**B's t_mid is earlier (16.4 vs 22.3) because high-k junk from memory hits the periodic edge.** Edge mass for B is 3e-4 at t=17, 1.4e-2 at t=20, 0.16 at t=26. The picker refused those times (wrap). At the kept t_mid, mass in |x|<2 is still 0.060 (flag `pass1_split_incomplete`). T1 at that time has already plateaued (~0.186), so the T1 number is not a mid-collision transient, but the leftover 6% has not chosen a side.

**T2/T1_B=2.77 and T2/T1_C=2.74.** The sent-back packet is very hot (⟨E⟩=5.38, ⟨k⟩=-3.05). Pass-2 transmission ~0.51 is over-barrier physics of that filtered+heated piece, not a lower barrier. C≈B again says the frozen stain is irrelevant next to the spectral change.

---

## Verdict

**protocol-dirty**

- Control A: T2/T1=1.598 (off 0.598). Energy filter of the transmitted packet. Leaks on A are tiny; the dirt is spectral, not wrap.
- B−A contrast of the *ratio* is +1.17, but it is the same filter, amplified by memory heating. It is not a repulsive scar on V0 (V_mem/V0 ~ 0.3%; C≈B).
- The pre-registered “harder if λ>0 stain on the barrier” prediction did not get a clean test. The stain on the barrier was never large enough to matter. The visible memory effect is *easier* first and second passes via heating — opposite of the scar guess, and not isolable from the dirty control.
- λ=(3,1), ν=(10,0.5) not retuned. Failures kept.

If one ignored the dirt and just compared raw ratios, the naive label would be “easier.” That label is refused because A already fails T2≈T1. The honest name is protocol-dirty.

---

## Files

- predictions (before integration): `/workspace/dossie_reexec/predictions_tunnel_hist.md`
- runner: `/workspace/dossie_reexec/tunnel_hist/code/run_tunnel_hist.py`
- stepper: `/workspace/dossie_reexec/tunnel_hist/code/stepper1d.py`
- launch: `/workspace/dossie_reexec/tunnel_hist/code/launch.py`
- raw: `/workspace/dossie_reexec/tunnel_hist/raw/summary.csv`, `timeseries.csv`, `snap_*.npz`
- figure: `/workspace/dossie_reexec/tunnel_hist/figures/two_pass.png`
- machine result: `/workspace/dossie_reexec/tunnel_hist/result.json`
- SHA256: `/workspace/dossie_reexec/tunnel_hist/SHA256`
