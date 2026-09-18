> Reading copy / Cópia de leitura. Obsidian links converted for GitHub; original wording and recorded results retained. Unresolved references stay visible as code. [Original](../../../../source/Artefatos/triad_reexecucao_36/sidebands/analysis.md) · [Collection / Acervo](../../../../README.md)

# P4 sidebands - independent re-execution

**Date:** 2026-08-21, America/Sao_Paulo (UTC-3)
**Dossier:** TRIAD sect 3.P4 / pending item 2 - memory restructures HO spectrum via parametric sidebands?
**Label:** re-execution. Predictions written first (`/workspace/dossie_reexec/predictions_sidebands.md`, SHA `d5f5cffbdb5e8320ecb457db07cc860aaef0bce40a798ba1b59f585a3b2f0c47`). No retuning. Failures kept.
**Stepper kernel:** standalone 1D Strang (algorithm of stepper1d.py SHA `5bddad844ac9a3ae5f393b4f01786e965c5a983beab616034927e078e94d0076`).
**Runner SHA256 (run_sidebands.py, verdict/plot):** `84391c14f8d6d35adeef4fdbf0408e13ef7679f229412d725d99325f7e495661`
**Integrator SHA256 (go_one.py, on-disk runs):** `b8a9b3041d74278d186bcc2c2cba6e08f9bdea89f138446576c809a925c43a78`
**Runtime:** /usr/bin/python3 + numpy, fp64. Plots via /workspace/.venv matplotlib.
**IC:** Hermite 2-level (phi0+phi1)/sqrt(2) of the linear HO. alpha=Gamma=f_FDT=0.
**Noise floor:** 5% of max |FFT[c]| on the negative-omega axis. E=-omega.

Previous P4 Lambda=-2+mem on L=20 had leak=0.642 and is INVALID. This run enlarges L until leak_max < 1e-6 or L=80.

## Verdict: **INCONCLUSIVE**

Adopted finished `go_one.py` outputs under `raw/`. No config was re-integrated. Predictions file not rewritten.

**Why INCONCLUSIVE (protocol, not a tie):** scoring spectrum is `Lambda_m2_mem` T=251. leak_max=0.308 at L=80 (the last box in LTRY=40,60,80). Predictions: if L=80 still leaks, keep the failure and do not score H_side / H_shift on that FFT. Linear control is clean (only 0.500 / 1.500, leak 1.88e-27). Lambda=+2 is a rigid up-shift (1.174, 2.192). Lambda=-2 no-mem is anharmonic and already has weak lines at 1.902 and 2.976 / 3.008, so ~2 and ~3 are **not** absent in Lambda=-2.

T=80 mem is confined (leak 6.77e-13 on L=40) and is reported as an extra, not as the scoring spectrum. Its lines 2.035 / 2.939 sit next to Lambda=-2's own 1.902 / 2.976; they are not new sidebands under the written rule.


- mem leak_max=3.081e-01 >= 1e-06 at L=80.0; spectrum INVALID
- T80_mem (not the scoring spectrum) E=[0.9628, 1.5991, 2.0345, 2.9387] L=40.0 leak=6.77e-13 — confined but official score uses T=251 mem

H_side = extra lines near E_i +/- nu_fast or ~2.0/3.0, absent in Lambda=-2 no-mem.
H_shift = same lines as Lambda=-2, maybe shifted; no new peaks above the floor.
INCONCLUSIVE = leak, linear-control failure, H_ef (matches Lambda=+2), or extra lines not at the claimed loci.

## Peak tables (first 8 above 5% floor)

### linear

Lambda=0.0, lam=[], nu=[], L=40.0, N=1024, dt=0.01, T=251.0, dE=0.02503, leak_max=1.883e-27, leak_end=1.825e-28, norm_end=1.000000000007, wall=2.1s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 0.500159 | 1.0002 | -0.500159 |
| 1 | 1.500471 | 0.9983 | -1.500471 |

FFT(|c|) beat peaks omega: 1.0003(100.1%), 2.0006(20.0%), 3.0009(8.5%)
FFT(int rho^2) peaks omega: 2.0006(100.3%)
FFT(V_mem(x=0)) peaks omega: (none)

### Lambda_p2

Lambda=2.0, lam=[], nu=[], L=40.0, N=1024, dt=0.01, T=80.0, dE=0.07853, leak_max=9.277e-28, leak_end=1.158e-28, norm_end=1.000000000002, wall=0.7s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 1.174216 | 1.0011 | -1.174216 |
| 1 | 2.192096 | 0.3753 | -2.192096 |
| 2 | 0.157313 | 0.0566 | -0.157313 |

FFT(|c|) beat peaks omega: 1.0178(100.1%), 2.0397(10.9%)
FFT(int rho^2) peaks omega: 1.8817(100.1%), 3.7561(37.9%), 5.6340(11.7%), 7.5291(6.7%)
FFT(V_mem(x=0)) peaks omega: (none)

### Lambda_m2

Lambda=-2.0, lam=[], nu=[], L=40.0, N=1024, dt=0.01, T=80.0, dE=0.07853, leak_max=2.791e-25, leak_end=2.301e-25, norm_end=1.000000000002, wall=0.7s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 0.561272 | 1.0108 | -0.561272 |
| 1 | 0.892703 | 0.1190 | -0.892703 |
| 2 | 2.976482 | 0.0703 | -2.976482 |
| 3 | 1.902166 | 0.0678 | -1.902166 |

FFT(|c|) beat peaks omega: 0.9993(103.6%), 1.3412(10.1%), 1.9877(10.2%), 2.3426(5.1%)
FFT(int rho^2) peaks omega: 2.1343(14.0%), 2.3390(102.3%), 4.4945(74.8%), 4.6992(5.5%), 6.8492(19.5%)
FFT(V_mem(x=0)) peaks omega: (none)

### Lambda_m2_T251

Lambda=-2.0, lam=[], nu=[], L=40.0, N=1024, dt=0.01, T=251.0, dE=0.02503, leak_max=1.111e-22, leak_end=7.542e-23, norm_end=1.000000000007, wall=2.2s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 0.569856 | 1.0255 | -0.569856 |
| 1 | 0.900853 | 0.1357 | -0.900853 |
| 2 | 1.007287 | 0.1063 | -1.007287 |
| 3 | 0.638914 | 0.0781 | -0.638914 |
| 4 | 3.008158 | 0.0750 | -3.008158 |
| 5 | 1.900501 | 0.0693 | -1.900501 |

FFT(|c|) beat peaks omega: 1.0004(100.1%), 1.0715(7.8%), 1.3307(10.5%), 1.4407(7.0%), 2.0008(10.4%), 2.3309(5.6%), 3.4394(6.0%)
FFT(int rho^2) peaks omega: 2.0971(5.1%), 2.1704(24.0%), 2.3300(100.3%), 4.5024(76.0%), 4.6605(5.1%), 6.8289(13.7%), 6.8857(10.8%), 8.9921(7.8%)
FFT(V_mem(x=0)) peaks omega: (none)

### Lambda_m2_mem

Lambda=-2.0, lam=[3.0, 1.0], nu=[10.0, 0.5], L=80.0, N=1024, dt=0.01, T=251.0, dE=0.02503, leak_max=3.081e-01, leak_end=2.224e-02, norm_end=1.000000000007, wall=2.5s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 0.501290 | 1.0004 | -0.501290 |
| 1 | 1.502600 | 0.8149 | -1.502600 |
| 2 | 2.031956 | 0.2107 | -2.031956 |
| 3 | 0.947119 | 0.1457 | -0.947119 |
| 4 | 0.614787 | 0.1355 | -0.614787 |
| 5 | 0.678675 | 0.1316 | -0.678675 |
| 6 | 0.760261 | 0.1294 | -0.760261 |

FFT(|c|) beat peaks omega: 0.9999(11.0%)
FFT(int rho^2) peaks omega: 1.9898(108.1%), 3.9822(28.6%), 5.9619(16.8%), 7.9534(11.9%), 9.9373(7.1%), 11.9227(5.3%)
FFT(V_mem(x=0)) peaks omega: 1.9818(97.5%), 3.9661(75.1%), 5.9486(62.4%), 7.9288(47.9%), 9.9090(35.1%), 11.8913(25.5%), 13.8768(19.0%), 15.8599(14.5%)

### Lambda_m2_mem_T80

Lambda=-2.0, lam=[3.0, 1.0], nu=[10.0, 0.5], L=40.0, N=1024, dt=0.01, T=80.0, dE=0.07853, leak_max=6.770e-13, leak_end=1.623e-14, norm_end=1.000000000002, wall=0.8s
IC overlaps P_n = n=0:0.500000, n=1:0.500000, n=2:0.000000, n=3:0.000000, n=4:0.000000, n=5:0.000000  (sum=1.000000)

| rank | E=-omega | frac of max | omega |
|---:|---:|---:|---:|
| 0 | 2.034544 | 1.0008 | -2.034544 |
| 1 | 0.962798 | 0.6610 | -0.962798 |
| 2 | 1.599106 | 0.3550 | -1.599106 |
| 3 | 2.938723 | 0.0539 | -2.938723 |

FFT(|c|) beat peaks omega: 0.0514(104.8%), 0.9237(17.7%), 1.1164(13.5%)
FFT(int rho^2) peaks omega: 0.0829(37.1%), 2.0175(102.8%), 3.9824(23.7%), 4.2259(7.2%), 5.9542(8.4%)
FFT(V_mem(x=0)) peaks omega: 0.0805(65.1%), 1.9875(103.9%), 3.9716(71.7%), 5.9545(52.8%), 7.9278(36.6%), 9.8940(23.0%), 10.1061(9.3%), 11.8566(13.7%)

## Comparison to dossier T=80 extras

| config | this run (E) | dossier | leak |
|---|---|---|---:|
| linear | 0.500, 1.500 | 0.50, 1.50, 2.50, 3.50 | 1.88e-27 |
| Lambda_p2 | 1.174, 2.192, 0.157 | 1.20, 2.20, 3.19, 4.19 | 9.28e-28 |
| Lambda_m2 | 0.561, 0.893, 2.976, 1.902 | 0.52, 0.89, 1.52 | 2.79e-25 |
| Lambda_m2_mem | 0.501, 1.503, 2.032, 0.947, 0.615, 0.679, 0.760 | 0.52, 1.52, 1.99, 2.99 | 3.08e-01 |
| Lambda_m2_T251 | 0.570, 0.901, 1.007, 0.639, 3.008, 1.901 | 0.52, 0.89, 1.52 | 1.11e-22 |
| Lambda_m2_mem_T80 | 2.035, 0.963, 1.599, 2.939 | 0.52, 1.52, 1.99, 2.99 | 6.77e-13 |

Dossier floats are comparison targets, not tuning targets.

## Files

- predictions (before integration): `/workspace/dossie_reexec/predictions_sidebands.md`
- runner: `/workspace/dossie_reexec/sidebands/code/run_sidebands.py`
- launch: `/workspace/dossie_reexec/sidebands/code/launch.py`
- raw CSVs: `/workspace/dossie_reexec/sidebands/raw/`
- figures: `/workspace/dossie_reexec/sidebands/figures/spectra.png`, `c_t.png`
- machine result: `/workspace/dossie_reexec/sidebands/result.json`

