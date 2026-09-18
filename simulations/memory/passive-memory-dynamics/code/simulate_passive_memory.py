#!/usr/bin/env python3
from pathlib import Path
import os, json, time
import numpy as np
try:
    from scipy.fft import fftn, ifftn
    FFT_WORKERS=int(os.environ.get('FFT_WORKERS','-1'))
    def F(a): return fftn(a,workers=FFT_WORKERS)
    def IF(a): return ifftn(a,workers=FFT_WORKERS)
except Exception:
    def F(a): return np.fft.fftn(a)
    def IF(a): return np.fft.ifftn(a)

# Exact R5 reference parameters except requested spatial resolution N=64.
N=int(os.environ.get('N','64')); L=20.0; dt=0.0025; T=15.0
TOTAL=int(round(T/dt)) # 6000
RUN=int(os.environ.get('RUN','1000'))
OUT=Path(os.environ.get('OUT','/mnt/data/triad_r5_passive64')); OUT.mkdir(parents=True,exist_ok=True)
CKPT=OUT/'checkpoint.npz'
LOG=OUT/'passive_log.jsonl'
SNAP_EVERY=int(os.environ.get('SNAP_EVERY','200'))

hbar=1.0; mass=1.0; Lambda=-8.0; sigma=1.5; alpha=0.0; Gamma=0.0
nu=np.array([10.0,0.5]); lam=np.array([1.125,0.375])
V_ext=0.0; f_FDT=0.0; init_sigma=0.5; init_k0=(0.0,0.0,0.0)

dx=L/N; dV=dx**3
x=np.linspace(-L/2,L/2,N,endpoint=False)
X,Y,Z=np.meshgrid(x,x,x,indexing='ij')
k=2*np.pi*np.fft.fftfreq(N,d=dx)
KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij'); K2=KX*KX+KY*KY+KZ*KZ; Kabs=np.sqrt(K2)
Hlin=(hbar*hbar*K2/(2*mass)) + alpha*(Kabs**sigma)
half_lin=np.exp(-1j*Hlin*dt/(2*hbar) - Gamma*dt/(2*hbar))

if CKPT.exists():
    z=np.load(CKPT)
    psi=z['psi'].astype(np.complex128); y=z['y'].astype(np.float64); start=int(z['step'])
else:
    r2=X*X+Y*Y+Z*Z
    psi=np.exp(-r2/(2*init_sigma**2)).astype(np.complex128)
    if any(init_k0): psi*=np.exp(1j*(init_k0[0]*X+init_k0[1]*Y+init_k0[2]*Z))
    psi/=np.sqrt(np.sum(np.abs(psi)**2)*dV)
    y=np.zeros((2,N,N,N),dtype=np.float64)
    start=0
    if LOG.exists(): LOG.unlink()
    # config once
    with open(OUT/'config.json','w') as f:
        json.dump({'reference':'triad_equation_reference.md Appendix A.2 R5 default','N':N,'L':L,'dt':dt,'T':T,
          'hbar':hbar,'m':mass,'Lambda':Lambda,'sigma':sigma,'alpha':alpha,'Gamma':Gamma,'f_FDT':f_FDT,
          'nu':nu.tolist(),'lam':lam.tolist(),'V_ext':V_ext,'init_sigma':init_sigma,'init_k0':init_k0,
          'metric_feedback':False,'numeric_guard':False,'renormalization_during_run':False,
          'chaos_imposed':False,'equilibrium_imposed':False,'stopping_on_metric':False},f,indent=2)

end=min(start+RUN,TOTAL)
# fixed snapshots: separate .npy files; saving does not affect state.
def save_snapshot(step,psi):
    np.save(OUT/f'psi_{step:05d}.npy',psi.astype(np.complex64))

def log_passive(step,psi,y):
    rho=np.abs(psi)**2
    rec={'step':step,'t':step*dt,'norm2':float(rho.sum()*dV),'rho_mean':float(rho.mean()),
         'rho_std':float(rho.std()),'rho_max':float(rho.max()),'rho_min':float(rho.min()),
         'mem0_mean':float(y[0].mean()),'mem1_mean':float(y[1].mean()),
         'finite':bool(np.isfinite(psi.real).all() and np.isfinite(psi.imag).all() and np.isfinite(y).all())}
    with open(LOG,'a') as f: f.write(json.dumps(rec)+'\n')
    print(rec,flush=True)

if start % SNAP_EVERY==0:
    if not (OUT/f'psi_{start:05d}.npy').exists(): save_snapshot(start,psi)
    log_passive(start,psi,y)

t0=time.time()
for step in range(start+1,end+1):
    # Strang split reference algorithm; no metrics feed back.
    psi=IF(F(psi)*half_lin)
    rho=np.abs(psi)**2
    V_mem=lam[0]*y[0] + lam[1]*y[1]
    V_tot=Lambda*rho + V_mem  # V_ext=0
    psi *= np.exp(-1j*V_tot*dt/hbar)
    # Reference uses explicit Euler memory update.
    y[0] += dt*nu[0]*(rho-y[0])
    y[1] += dt*nu[1]*(rho-y[1])
    # no noise: f_FDT=0 in reference R5 baseline
    psi=IF(F(psi)*half_lin)
    if not (np.isfinite(psi.real).all() and np.isfinite(psi.imag).all() and np.isfinite(y).all()):
        print('NONFINITE',step,flush=True); end=step; break
    if step % SNAP_EVERY==0 or step==TOTAL:
        save_snapshot(step,psi); log_passive(step,psi,y)

np.savez(CKPT,step=end,psi=psi,y=y)
print('BLOCK_DONE',start,end,'elapsed',time.time()-t0,'TOTAL',TOTAL,flush=True)
