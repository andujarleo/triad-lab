#!/usr/bin/env python3
from pathlib import Path
import os,json,time,math
import numpy as np
from scipy.fft import fftn,ifftn
from scipy.spatial import cKDTree
ROOT=Path('/mnt/data/triad_rebuild_rules/run64'); OUT=Path('/mnt/data/triad_soul_causal_long2'); OUT.mkdir(parents=True,exist_ok=True)
N=64; L=20.; dx=L/N; dV=dx**3; dt=.0025; START=2800; END=4600; CHUNK=int(os.environ.get('CHUNK','600')); EPS=1e-6; workers=int(os.environ.get('FFT_WORKERS','-1'))
hbar=1.; mass=1.; Lambda=-8.; nu=np.array([10.,.5]); lam=np.array([1.125,.375])
k=2*np.pi*np.fft.fftfreq(N,d=dx); KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij'); K2=KX*KX+KY*KY+KZ*KZ; half=np.exp(-1j*K2*dt/4)
def F(a): return fftn(a,axes=(-3,-2,-1),workers=workers)
def IF(a): return ifftn(a,axes=(-3,-2,-1),workers=workers)
def pd2(c):
 ax=[]
 for ci in c:
  q=np.abs(np.arange(N)-ci); q=np.minimum(q,N-q); ax.append(q.astype(float))
 A,B,C=np.meshgrid(*ax,indexing='ij'); return A*A+B*B+C*C
def aura(rho,c):
 c=tuple(c); val=float(rho[c]); lap=sum(np.roll(rho,1,a)+np.roll(rho,-1,a)-2*rho for a in range(3))/(dx*dx); curv=max(float(-lap[c]/(val+1e-30)),1e-12); sig=(3/curv)**.5/dx; return np.exp(-.5*pd2(c)/(sig*sig)),sig
CK=OUT/'checkpoint.npz'; TRACE=OUT/'trace.jsonl'
if CK.exists():
 z=np.load(CK); step=int(z['step']); psi=z['psi'].astype(np.complex128); y=z['y'].astype(np.float64)
else:
 step=START; p=np.load(ROOT/f'psi_{START:05d}.npy').astype(np.complex128); yy=np.load(ROOT/f'y_{START:05d}.npy').astype(np.float64); rho=np.abs(p)**2; w,sig=aura(rho,[35,1,35]);
 psi=np.repeat(p[None],2,axis=0); y=np.repeat(yy[None],2,axis=0)
 psi[1]*=np.exp(1j*EPS*w); y[1]*=(1+EPS*w[None])
 if TRACE.exists(): TRACE.unlink()
 json.dump({'old_track':35479,'coord':[35,1,35],'sigma_vox':sig,'eps':EPS,'start_t':START*dt,'end_t':END*dt},open(OUT/'config.json','w'),indent=2)
def rec(st):
 b=psi[0]; by=y[0]; out={'step':st,'t':st*dt,'branches':{}}
 for i,l in [(1,'full')]:
  q=np.abs(psi[i]-b)**2; qy=np.sum((y[i]-by)**2,axis=0); sp=q.sum(); sy=qy.sum(); ip=(q*q).sum()/(sp*sp+1e-300); iy=(qy*qy).sum()/(sy*sy+1e-300)
  out['branches'][l]={'dpsi_l2':float(np.sqrt(sp*dV)),'dy_l2':float(np.sqrt(sy*dV)),'effvox_psi':float(1/ip),'effvox_y':float(1/iy)}
 with open(TRACE,'a') as f:f.write(json.dumps(out)+'\n')
 print(out,flush=True)
rec(step)
end=min(step+CHUNK,END); t0=time.time()
for st in range(step+1,end+1):
 psi=IF(F(psi)*half); rho=np.abs(psi)**2; vm=lam[0]*y[:,0]+lam[1]*y[:,1]; psi*=np.exp(-1j*(Lambda*rho+vm)*dt); y[:,0]+=dt*nu[0]*(rho-y[:,0]); y[:,1]+=dt*nu[1]*(rho-y[:,1]); psi=IF(F(psi)*half)
 if st%200==0: rec(st)
np.savez(CK,step=end,psi=psi,y=y); print('BLOCK',step,end,'sec',time.time()-t0,flush=True)
if end<END: raise SystemExit
# final natural newborns at t=11.5 persistent >=4 reconstructed

def strict(r):
 mx=None
 for i in (-1,0,1):
  for j in (-1,0,1):
   for z in (-1,0,1):
    if i==j==z==0: continue
    a=np.roll(r,(i,j,z),(0,1,2)); mx=a if mx is None else np.maximum(mx,a)
 return r>mx
steps=list(range(0,6001,200)); frames=[]
for s in steps:
 p=np.load(ROOT/f'psi_{s:05d}.npy').astype(np.complex128); frames.append(np.argwhere(strict(np.abs(p)**2)).astype(float))
tracks={}; nxt=0; prev=None
for fi,B in enumerate(frames):
 ids=np.full(len(B),-1,int)
 if fi==0:
  ids=np.arange(nxt,nxt+len(B)); nxt+=len(B)
  for j,t in enumerate(ids): tracks[int(t)]=[(fi,j)]
 else:
  A=frames[fi-1]
  if len(A) and len(B):
   tb=cKDTree(B,boxsize=N); _,jab=tb.query(A); ta=cKDTree(A,boxsize=N); _,jba=ta.query(B)
   for ai,bj in enumerate(jab):
    if jba[bj]==ai:
     tid=int(prev[ai]); ids[bj]=tid; tracks[tid].append((fi,int(bj)))
  for j in range(len(B)):
   if ids[j]<0: ids[j]=nxt; tracks[nxt]=[(fi,j)]; nxt+=1
 prev=ids
new=[]
for tid,path in tracks.items():
 if path[0][0]==23 and len(path)>=4:
  _,pi=path[0]; new.append((tid,frames[23][pi].astype(int).tolist(),len(path)))
base=psi[0]; br=np.abs(base)**2
for ib,l in [(1,'full')]:
 qp=np.abs(psi[ib]-base)**2; qy=np.sum((y[ib]-y[0])**2,axis=0); sp=qp.sum(); sy=qy.sum(); rows=[]
 for tid,c,ll in new:
  w,s=aura(br,c); rows.append({'track':tid,'coord':c,'length':ll,'cap_psi':float((w*qp).sum()/(sp+1e-300)),'cap_y':float((w*qy).sum()/(sy+1e-300))})
 p=sorted(rows,key=lambda r:r['cap_psi'],reverse=True); m=sorted(rows,key=lambda r:r['cap_y'],reverse=True); rp={r['track']:i+1 for i,r in enumerate(p)}; rm={r['track']:i+1 for i,r in enumerate(m)}
 for r in rows:r['rank_psi']=rp[r['track']];r['rank_y']=rm[r['track']]
 json.dump({'newborn_count':len(new),'top_psi':p[:20],'top_y':m[:20],'target_51782':next((r for r in rows if r['track']==51782),None)},open(OUT/f'captures_{l}.json','w'),indent=2)
print('DONE ANALYSIS',len(new),flush=True)
