#!/usr/bin/env python3
"""Q02 smoke: 80 passos Strang N=64, mlx GPU complex64 vs numpy fp64."""
from __future__ import annotations

import time

import mlx.core as mx
import numpy as np

HBAR = 1.0
M_MASS = 1.0
LAMBDA = -10.0
ALPHA = 0.15
SIGMA_FRAC = 1.5
GAMMA = 0.05
NU = (10.0, 0.5, 0.05)
LAM = (3.0, 1.0, 0.3)
FDT_COUPLE = True
KT = 1.0
LBOX = 32.0
NGRID = 64
DT = 0.0025
N_STEPS = 80
SEED = 0
INIT_SIGMA = 0.5
INIT_K0 = (0.0, 0.0, 0.0)
Y0 = 0.0


def build_state(dtype_psi, dtype_r):
    N = NGRID
    x = np.linspace(-LBOX / 2.0, LBOX / 2.0, N, endpoint=False, dtype=np.float64)
    dx = float(x[1] - x[0])
    dV = dx ** 3
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r2 = X * X + Y * Y + Z * Z
    kvec = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    kx, ky, kz = np.meshgrid(kvec, kvec, kvec, indexing="ij")
    k2 = kx * kx + ky * ky + kz * kz
    k_mag = np.sqrt(k2)
    H_lin = (HBAR * HBAR * k2) / (2.0 * M_MASS)
    if ALPHA != 0.0:
        H_lin = H_lin + ALPHA * np.power(k_mag, SIGMA_FRAC)
    half_lin = np.exp(-1j * H_lin * DT / (2.0 * HBAR) - GAMMA * DT / (2.0 * HBAR))
    s = INIT_SIGMA
    psi = np.exp(-r2 / (2.0 * s * s)).astype(np.complex128)
    k0x, k0y, k0z = INIT_K0
    if k0x != 0.0 or k0y != 0.0 or k0z != 0.0:
        psi = psi * np.exp(1j * (k0x * X + k0y * Y + k0z * Z))
    psi = psi / np.sqrt(np.sum(np.abs(psi) ** 2) * dV)
    y = np.full((len(NU), N, N, N), Y0, dtype=np.float64)
    f_FDT = 2.0 * GAMMA * (dx ** 3) * KT / HBAR if FDT_COUPLE else 0.0
    noise_amp = float(np.sqrt(f_FDT * DT / (dx ** 3))) if f_FDT > 0 else 0.0
    return {
        "dx": dx,
        "dV": dV,
        "half_lin": half_lin.astype(dtype_psi, copy=False),
        "psi": psi.astype(dtype_psi, copy=False),
        "y": y.astype(dtype_r, copy=False),
        "f_FDT": f_FDT,
        "noise_amp": noise_amp,
        "nu": np.asarray(NU, dtype=dtype_r),
        "lam": np.asarray(LAM, dtype=dtype_r),
    }


def strang_numpy(psi, y, half_lin, noise_amp, rng, nu, lam):
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    rho = np.abs(psi) ** 2
    V_mem = (lam.reshape((-1, 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    psi = psi * np.exp(-1j * V_tot * DT / HBAR)
    y = y + DT * nu.reshape((-1, 1, 1, 1)) * (rho - y)
    if noise_amp > 0.0:
        xi = (rng.standard_normal(psi.shape) + 1j * rng.standard_normal(psi.shape)) / np.sqrt(2.0)
        psi = psi + noise_amp * xi.astype(psi.dtype, copy=False)
    psi = np.fft.ifftn(np.fft.fftn(psi) * half_lin)
    return psi, y


def mul_phase_mlx(psi, theta):
    """psi *= exp(-i * theta), theta real float32."""
    c = mx.cos(theta)
    s = mx.sin(theta)
    re = mx.real(psi)
    im = mx.imag(psi)
    nre = re * c + im * s
    nim = im * c - re * s
    return nre.astype(mx.complex64) + (1j * nim.astype(mx.complex64))


def strang_mlx(psi, y, half_lin, noise_amp, rng, nu, lam, shape):
    psi = mx.fft.ifftn(mx.fft.fftn(psi) * half_lin)
    rho = mx.abs(psi) ** 2
    V_mem = (lam.reshape((len(NU), 1, 1, 1)) * y).sum(axis=0)
    V_tot = LAMBDA * rho + V_mem
    theta = V_tot * (DT / HBAR)
    psi = mul_phase_mlx(psi, theta)
    y = y + DT * nu.reshape((len(NU), 1, 1, 1)) * (rho - y)
    if noise_amp > 0.0:
        xi_np = (
            (rng.standard_normal(shape) + 1j * rng.standard_normal(shape)) / np.sqrt(2.0)
        ).astype(np.complex64)
        psi = psi + noise_amp * mx.array(xi_np)
    psi = mx.fft.ifftn(mx.fft.fftn(psi) * half_lin)
    mx.eval(psi, y)
    return psi, y


def peaks(psi, dV):
    rho = np.abs(np.asarray(psi)) ** 2
    finite = bool(np.isfinite(rho).all())
    return {
        "finite": finite,
        "norm": float(rho.sum() * dV) if finite else float("nan"),
        "peak": float(rho.max()) if finite else float("nan"),
    }


def main():
    print("=== Q02 smoke mlx vs numpy ===", flush=True)
    print("default_device", mx.default_device(), flush=True)
    print("N", NGRID, "steps", N_STEPS, "dt", DT, "seed", SEED, flush=True)

    st64 = build_state(np.complex128, np.float64)
    st32 = build_state(np.complex64, np.float32)
    dV = st64["dV"]
    noise_amp = st64["noise_amp"]
    print("dx", st64["dx"], "noise_amp", noise_amp, "f_FDT", st64["f_FDT"], flush=True)
    print("noise_amp_check", float(np.sqrt(2.0 * GAMMA * KT * DT / HBAR)), flush=True)

    rng_np = np.random.default_rng(SEED)
    psi_np = st64["psi"].copy()
    y_np = st64["y"].copy()
    t0 = time.perf_counter()
    for step in range(N_STEPS):
        psi_np, y_np = strang_numpy(
            psi_np, y_np, st64["half_lin"], noise_amp, rng_np, st64["nu"], st64["lam"]
        )
    wall_np = time.perf_counter() - t0
    rec_np = peaks(psi_np, dV)
    print(
        f"numpy fp64 wall_s={wall_np:.6f} finite={rec_np['finite']} "
        f"norm={rec_np['norm']:.8e} peak={rec_np['peak']:.8e}",
        flush=True,
    )

    rng_mx = np.random.default_rng(SEED)
    psi_m = mx.array(st32["psi"])
    y_m = mx.array(st32["y"])
    half_m = mx.array(st32["half_lin"])
    nu_m = mx.array(st32["nu"])
    lam_m = mx.array(st32["lam"])
    mx.eval(psi_m, y_m, half_m, nu_m, lam_m)
    # warmup 1 step graph compile, then reset
    shape = tuple(st32["psi"].shape)
    t0 = time.perf_counter()
    for step in range(N_STEPS):
        psi_m, y_m = strang_mlx(psi_m, y_m, half_m, noise_amp, rng_mx, nu_m, lam_m, shape)
    wall_mx = time.perf_counter() - t0
    psi_mx_np = np.array(psi_m)
    y_mx_np = np.array(y_m)
    rec_mx = peaks(psi_mx_np, dV)
    y_finite = bool(np.isfinite(y_mx_np).all())
    print(
        f"mlx gpu c64/f32 wall_s={wall_mx:.6f} finite={rec_mx['finite'] and y_finite} "
        f"norm={rec_mx['norm']:.8e} peak={rec_mx['peak']:.8e}",
        flush=True,
    )
    if rec_np["finite"] and rec_mx["finite"]:
        rel_peak = abs(rec_mx["peak"] - rec_np["peak"]) / max(abs(rec_np["peak"]), 1e-300)
        rel_norm = abs(rec_mx["norm"] - rec_np["norm"]) / max(abs(rec_np["norm"]), 1e-300)
        print(f"rel_diff peak={rel_peak:.6e} norm={rel_norm:.6e}", flush=True)
    print(f"mlx_vs_numpy_wall {wall_mx:.6f} / {wall_np:.6f} = {wall_mx / wall_np:.4f}", flush=True)
    if not (rec_mx["finite"] and y_finite):
        print("SMOKE_FAIL mlx not finite", flush=True)
        raise SystemExit(2)
    print("SMOKE_OK mlx finite", flush=True)
    if wall_mx > wall_np:
        print("NOTE mlx slower than numpy; still using mlx (user asked GPU)", flush=True)


if __name__ == "__main__":
    main()
