#!/usr/bin/env python3
import mlx.core as mx
import numpy as np

print("mlx", mx.__version__)
print("default", mx.default_device())
print("gpu", mx.gpu)
print("has fftn", hasattr(mx.fft, "fftn"), hasattr(mx.fft, "ifftn"))
print("complex64", mx.complex64, "float32", mx.float32)
for name in ["complex128", "float64"]:
    print(name, hasattr(mx, name), getattr(mx, name, None))

a = mx.random.normal((8, 8, 8)) + 1j * mx.random.normal((8, 8, 8))
a = a.astype(mx.complex64)
fa = mx.fft.fftn(a)
ia = mx.fft.ifftn(fa)
mx.eval(ia)
print("fft roundtrip max", float(mx.max(mx.abs(ia - a))))

z = mx.array([0.1 + 0.2j], dtype=mx.complex64)
try:
    e = mx.exp(z)
    mx.eval(e)
    print("mx.exp complex", e)
except Exception as ex:
    print("mx.exp complex FAIL", type(ex), ex)

th = mx.array([0.5], dtype=mx.float32)
c = mx.cos(th)
s = mx.sin(th)
psi = mx.array([1 + 1j], dtype=mx.complex64)
re = mx.real(psi)
im = mx.imag(psi)
nre = re * c + im * s
nim = im * c - re * s
try:
    out = nre.astype(mx.complex64) + (1j * nim.astype(mx.complex64))
    mx.eval(out)
    print("phase mul astype", out)
except Exception as ex:
    print("phase mul astype FAIL", ex)

try:
    out2 = mx.concatenate([nre[..., None], nim[..., None]], axis=-1)
    print("concat shape", out2.shape, out2.dtype)
except Exception as ex:
    print("concat fail", ex)

# numpy check of same formula
psi_np = np.array([1 + 1j], dtype=np.complex64)
theta = 0.5
ref = psi_np * np.exp(-1j * theta)
print("numpy ref", ref)

# half_lin via numpy upload
H = np.array([1.0], dtype=np.float64)
dt = 0.0025
Gamma = 0.05
hl = np.exp(-1j * H * dt / 2.0 - Gamma * dt / 2.0).astype(np.complex64)
hl_mx = mx.array(hl)
print("half_lin uploaded", hl_mx)

# 64^3 fft timing
N = 64
rng = np.random.default_rng(0)
arr = (rng.standard_normal((N, N, N)) + 1j * rng.standard_normal((N, N, N))).astype(np.complex64)
x = mx.array(arr)
mx.eval(x)
import time
t0 = time.perf_counter()
for _ in range(20):
    y = mx.fft.ifftn(mx.fft.fftn(x))
    mx.eval(y)
print("mlx fftn 64^3 x20", time.perf_counter() - t0)
print("done probe")
