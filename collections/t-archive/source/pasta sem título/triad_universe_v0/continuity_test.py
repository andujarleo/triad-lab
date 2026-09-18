#!/usr/bin/env python3
"""Bit-level continuation test for the persistent modal substrate."""
import argparse, ctypes as ct, os, numpy as np
from genesis_modal import Config, bind

def run(lib,cfg,re,im,y,start,ticks):
    for k in range(ticks):
        if not lib.triad_modal_evolve_state(ct.byref(cfg),re,im,y,start+k*cfg.steps):
            raise RuntimeError('evolve failed')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--lib',required=True);ap.add_argument('--cuda-stub');ap.add_argument('--modes',type=int,default=65536);args=ap.parse_args()
    lib=bind(args.lib,args.cuda_stub);cfg=Config();lib.triad_modal_config_default(ct.byref(cfg));cfg.N=args.modes;cfg.steps=8;cfg.backend=1;cfg.seed=77
    N=cfg.N;M=3
    def fresh():
        r=(ct.c_float*N)();i=(ct.c_float*N)();y=(ct.c_double*(N*M))();assert lib.triad_modal_init_state(N,M,r,i,y);return r,i,y
    ar,ai,ay=fresh(); br,bi,by=fresh()
    run(lib,cfg,ar,ai,ay,0,16)
    run(lib,cfg,br,bi,by,0,8)
    # literal checkpoint/restore copy at the midpoint
    rmid=np.ctypeslib.as_array(br).copy(); imid=np.ctypeslib.as_array(bi).copy(); ymid=np.ctypeslib.as_array(by).copy()
    cr=(ct.c_float*N)(*rmid);ci=(ct.c_float*N)(*imid);cy=(ct.c_double*(N*M))(*ymid)
    run(lib,cfg,cr,ci,cy,8*cfg.steps,8)
    ok=(np.array_equal(np.ctypeslib.as_array(ar),np.ctypeslib.as_array(cr)) and
        np.array_equal(np.ctypeslib.as_array(ai),np.ctypeslib.as_array(ci)) and
        np.array_equal(np.ctypeslib.as_array(ay),np.ctypeslib.as_array(cy)))
    print('continuous_equals_checkpoint_resume=',ok)
    if not ok: raise SystemExit(1)
if __name__=='__main__':main()
