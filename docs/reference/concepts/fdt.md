---
tags: [triad, conceito]
aliases: [ruído, flutuação-dissipação]
---

# FDT

$$\langle\eta(t,\mathbf{x})\,\eta^*(t',\mathbf{x}')\rangle=2\gamma_0 k_B T\,\delta(t-t')\,\delta^{D}(\mathbf{x}-\mathbf{x}')$$

$\langle\eta\eta\rangle=0$. Amplitude composta $f_{\mathrm{FDT}}=2\gamma_0 k_B T$. No grid:

$$\Psi_i\leftarrow\Psi_i+\sqrt{f_{\mathrm{FDT}}\,dt/dx^D}\cdot(\xi_i+i\xi'_i)/\sqrt{2}$$

O “lock” é modelagem: $f_{\mathrm{FDT}}$ e $\Gamma$ vêm do mesmo banho quando se quer um banho físico. O código *não* impõe o lock sozinho; com `fdt_couple=True` recalcula $f_{\mathrm{FDT},e}=2\Gamma\,dx^D\,kT/\hbar$.

No TRIAD o termo $\eta$ **não** se lê como ruído experimental a filtrar. É o banho do universo: o campo que preenche o volume depois das sementes (átomos) **é o universo**. Ver [27 triad_chaos_eq](../../../simulations/structures/twelve-atoms-full-field/notes/original-record.md) · [28 triad_atoms_3d](../../../simulations/structures/3d-atom-trajectories/notes/original-record.md) · [Universo como simulação](universe-as-simulation.md).

Com $\Gamma>0$ e $\eta=0$ a norma cai; com $\eta\neq0$ e $\Gamma=0$ diverge. Ver spec §2.5.

## No registro

- **Quente (falha preservada)** — [19 triad_bigbang_solver_run](../../../simulations/signals/hot-bath-diagnostic-failure/notes/original-record.md): `mass_final=8773.747757` (massa inicial 1). Motivou o run frio.
- **Frio** — [20 triad_bigbang_3d_box](../../../simulations/signals/3d-cold-bath-box/notes/original-record.md): norma 1.0→1.413637; expansão sem teia clara.
- Unidades internas; sem SI. `[[Backend e unidades]]`

Voltar: `[[Equação de referência]]` · `[[Solver]]`
