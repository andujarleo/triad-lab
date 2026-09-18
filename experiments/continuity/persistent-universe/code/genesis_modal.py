#!/usr/bin/env python3
"""TRIAD Universe v0 — persistent P1·P2·P3 genesis field.

This harness does not alter the field from observations.  It binds directly to
TriadLang's C-native persistent modal substrate (`triad_modal_*`).  The Python
layer only declares an a-priori schedule, checkpoints raw state, and renders
post-mortem readouts.
"""
from __future__ import annotations
import argparse, ctypes as ct, csv, hashlib, json, math, os, struct, time
from pathlib import Path
import numpy as np

class Config(ct.Structure):
    _fields_ = [
        ("D", ct.c_int32), ("N", ct.c_int64), ("steps", ct.c_int32),
        ("n_memory", ct.c_int32), ("backend", ct.c_int32),
        ("dt", ct.c_double), ("L", ct.c_double), ("hbar", ct.c_double),
        ("mass", ct.c_double), ("Lambda", ct.c_double), ("alpha", ct.c_double),
        ("sigma", ct.c_double), ("Gamma", ct.c_double), ("kT", ct.c_double),
        ("coupling", ct.c_double), ("nu", ct.c_double * 3),
        ("lambda_", ct.c_double * 3), ("seed", ct.c_uint64),
    ]

class Qubit(ct.Structure):
    _fields_ = [("mode", ct.c_int64), ("kx", ct.c_int32), ("ky", ct.c_int32),
                ("kz", ct.c_int32), ("rho", ct.c_double), ("phase", ct.c_double),
                ("y", ct.c_double * 3)]

def bind(lib_path: str, cuda_stub: str | None = None):
    if cuda_stub and os.path.exists(cuda_stub):
        ct.CDLL(cuda_stub, mode=ct.RTLD_GLOBAL)
    lib = ct.CDLL(lib_path)
    lib.triad_modal_config_default.argtypes = [ct.POINTER(Config)]
    lib.triad_modal_config_default.restype = None
    lib.triad_modal_validate.argtypes = [ct.POINTER(Config)]
    lib.triad_modal_validate.restype = ct.c_int
    lib.triad_modal_init_state.argtypes = [ct.c_int64, ct.c_int32,
        ct.POINTER(ct.c_float), ct.POINTER(ct.c_float), ct.POINTER(ct.c_double)]
    lib.triad_modal_init_state.restype = ct.c_int
    lib.triad_modal_evolve_state.argtypes = [ct.POINTER(Config),
        ct.POINTER(ct.c_float), ct.POINTER(ct.c_float), ct.POINTER(ct.c_double), ct.c_uint32]
    lib.triad_modal_evolve_state.restype = ct.c_int
    lib.triad_modal_last_evolve_backend.argtypes = []
    lib.triad_modal_last_evolve_backend.restype = ct.c_int32
    lib.triad_modal_state_observe.argtypes = [ct.c_int64, ct.c_int32,
        ct.POINTER(ct.c_float), ct.POINTER(ct.c_float), ct.POINTER(ct.c_double),
        ct.POINTER(ct.c_double), ct.POINTER(ct.c_double), ct.POINTER(ct.c_double)]
    lib.triad_modal_state_observe.restype = None
    lib.triad_modal_state_finite.argtypes = [ct.c_int64, ct.c_int32,
        ct.POINTER(ct.c_float), ct.POINTER(ct.c_float), ct.POINTER(ct.c_double)]
    lib.triad_modal_state_finite.restype = ct.c_int
    lib.triad_modal_mode_lattice.argtypes = [ct.c_int64, ct.c_int64,
        ct.POINTER(ct.c_int32), ct.POINTER(ct.c_int32), ct.POINTER(ct.c_int32)]
    lib.triad_modal_mode_lattice.restype = ct.c_int
    lib.triad_modal_qubit_readout.argtypes = [ct.c_int64, ct.c_int32,
        ct.POINTER(ct.c_float), ct.POINTER(ct.c_float), ct.POINTER(ct.c_double),
        ct.c_int64, ct.POINTER(Qubit)]
    lib.triad_modal_qubit_readout.restype = ct.c_int
    return lib

def observe(lib, N, M, re, im, y):
    n = ct.c_double(); inter = ct.c_double(); mem = ct.c_double()
    lib.triad_modal_state_observe(N, M, re, im, y, ct.byref(n), ct.byref(inter), ct.byref(mem))
    return float(n.value), float(inter.value), float(mem.value)

def state_digest(arrays):
    h = hashlib.blake2b(digest_size=8)
    for a in arrays:
        h.update(memoryview(np.ascontiguousarray(a)).cast('B'))
    return h.hexdigest()

def save_checkpoint(path: Path, re_np, im_np, y_np, cfg: Config, step_base: int, tick: int):
    np.savez(path, re=re_np, im=im_np, y=y_np,
             step_base=np.uint64(step_base), tick=np.uint64(tick),
             N=np.int64(cfg.N), D=np.int32(cfg.D), steps=np.int32(cfg.steps),
             dt=np.float64(cfg.dt), L=np.float64(cfg.L), hbar=np.float64(cfg.hbar),
             mass=np.float64(cfg.mass), Lambda=np.float64(cfg.Lambda), alpha=np.float64(cfg.alpha),
             sigma=np.float64(cfg.sigma), Gamma=np.float64(cfg.Gamma), kT=np.float64(cfg.kT),
             coupling=np.float64(cfg.coupling), seed=np.uint64(cfg.seed),
             nu=np.asarray(list(cfg.nu)), lam=np.asarray(list(cfg.lambda_)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lib', required=True)
    ap.add_argument('--cuda-stub', default=None)
    ap.add_argument('--out', required=True)
    ap.add_argument('--modes', type=int, default=1_000_000)
    ap.add_argument('--ticks', type=int, default=64)
    ap.add_argument('--steps-per-tick', type=int, default=8)
    ap.add_argument('--seed', type=int, default=7)
    ap.add_argument('--backend', type=int, default=1, help='1 CPU, 2 Metal, 3 CUDA, 0 auto')
    ap.add_argument('--snapshot-ticks', default='0,1,2,4,8,16,32,64')
    args = ap.parse_args()
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    lib = bind(args.lib, args.cuda_stub)

    cfg = Config(); lib.triad_modal_config_default(ct.byref(cfg))
    cfg.D = 3; cfg.N = args.modes; cfg.steps = args.steps_per_tick
    cfg.n_memory = 3; cfg.backend = args.backend; cfg.seed = args.seed
    if not lib.triad_modal_validate(ct.byref(cfg)):
        raise SystemExit('Triad modal config rejected by native runtime')

    N, M = int(cfg.N), int(cfg.n_memory)
    re = (ct.c_float * N)(); im = (ct.c_float * N)(); y = (ct.c_double * (N*M))()
    if not lib.triad_modal_init_state(N, M, re, im, y):
        raise SystemExit('triad_modal_init_state failed')
    re_np = np.ctypeslib.as_array(re); im_np = np.ctypeslib.as_array(im)
    y_np = np.ctypeslib.as_array(y).reshape(M, N)

    wanted = {int(x) for x in args.snapshot_ticks.split(',') if x.strip()}
    wanted.add(args.ticks)
    rows=[]; snapshots={}

    def snap(tick, wall=0.0):
        norm, interference, memory_energy = observe(lib, N, M, re, im, y)
        rho = re_np.astype(np.float64)**2 + im_np.astype(np.float64)**2
        idx = np.argpartition(rho, -min(12000,N))[-min(12000,N):]
        idx = idx[np.argsort(rho[idx])[::-1]]
        side = int(math.ceil(N ** (1/3)))
        q = idx.astype(np.int64)
        kx = (q % side) - side//2; q//=side
        ky = (q % side) - side//2; q//=side
        kz = (q % side) - side//2
        snapshots[tick] = {
            'idx': idx.astype(np.int64), 'kx': kx.astype(np.int32), 'ky': ky.astype(np.int32),
            'kz': kz.astype(np.int32), 'rho': rho[idx],
            'phase': np.arctan2(im_np[idx], re_np[idx]),
            'y0': y_np[0,idx].copy(), 'y1': y_np[1,idx].copy(), 'y2': y_np[2,idx].copy(),
        }
        row = {'tick': tick, 'step_base': tick*cfg.steps, 'physical_time': tick*cfg.steps*cfg.dt,
               'wall_s': wall, 'norm': norm, 'interference': interference,
               'memory_energy': memory_energy, 'finite': int(lib.triad_modal_state_finite(N,M,re,im,y)),
               'backend_used': int(lib.triad_modal_last_evolve_backend()) if tick else 0,
               'state_digest': state_digest((re_np, im_np, y_np))}
        rows.append(row)
        print(json.dumps(row))

    snap(0)
    total_wall=0.0
    for tick in range(1,args.ticks+1):
        t0=time.perf_counter()
        ok=lib.triad_modal_evolve_state(ct.byref(cfg),re,im,y,(tick-1)*cfg.steps)
        wall=time.perf_counter()-t0; total_wall += wall
        if not ok: raise SystemExit(f'evolution failed at tick {tick}')
        if tick in wanted: snap(tick, wall)

    with (out/'trajectory.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    np.savez_compressed(out/'readout_snapshots.npz', **{
        f't{tick}_{key}': value for tick,s in snapshots.items() for key,value in s.items()
    })
    save_checkpoint(out/'universe_checkpoint.npz', re_np, im_np, y_np, cfg,
                    args.ticks*cfg.steps, args.ticks)
    ck_hash=hashlib.sha256((out/'universe_checkpoint.npz').read_bytes()).hexdigest()
    manifest={
        'engine':'TriadLang C-native persistent modal P1·P2·P3', 'D':3, 'active_modes':N,
        'runtime_reported_virtual_cells_formula':'N^3', 'virtual_cells':N**3,
        'field_volume_materialized':False, 'search_space_materialized':False,
        'resident_state':{'psi_re_f32':N,'psi_im_f32':N,'memory_f64':M*N},
        'ticks':args.ticks,'steps_per_tick':cfg.steps,'total_steps':args.ticks*cfg.steps,
        'dt':cfg.dt,'physical_time':args.ticks*cfg.steps*cfg.dt,'backend_requested':cfg.backend,
        'seed':cfg.seed,'Lambda':cfg.Lambda,'alpha':cfg.alpha,'sigma':cfg.sigma,
        'Gamma':cfg.Gamma,'kT':cfg.kT,'coupling':cfg.coupling,
        'nu':list(cfg.nu),'lambda':list(cfg.lambda_),
        'observer_feedback':False,'post_hoc_retuning':False,'wall_s':total_wall,
        'checkpoint_sha256':ck_hash,
    }
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(json.dumps(manifest,indent=2))

if __name__=='__main__': main()
