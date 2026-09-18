#!/usr/bin/env python3
from pathlib import Path
import os,json,time,math
import numpy as np
from scipy.fft import fftn,ifftn
from scipy.spatial import cKDTree
ROOT=Path('/mnt/data/triad_rebuild_rules/run64');OUT=Path('/mnt/data/triad_soul_worldtube');OUT.mkdir(parents=True,exist_ok=True)
N=64;L=20.;dx=L/N;dV=dx**3;dt=.0025;START=1800;END=2800;CHUNK=int(os.environ.get('CHUNK','500'));EPS=1e-6;workers=-1
life=[4,21,32];matched=[28,0,43] # non-max, matched rho/y at t=4.5
sigma_vox=1.412648728389429
labels=['base','life','matched']
k=2*np.pi*np.fft.fftfreq(N,d=dx);KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij');K2=KX*KX+KY*KY+KZ*KZ;half=np.exp(-1j*K2*dt/4)
nu=np.array([10.,.5]);lam=np.array([1.125,.375]);Lambda=-8.
def F(a):return fftn(a,axes=(-3,-2,-1),workers=workers)
def IF(a):return ifftn(a,axes=(-3,-2,-1),workers=workers)
def wgt(c):
 ax=[]
 for ci in c:
  q=np.abs(np.arange(N)-ci);q=np.minimum(q,N-q);ax.append(q.astype(float))
 A,B,C=np.meshgrid(*ax,indexing='ij');return np.exp(-.5*(A*A+B*B+C*C)/(sigma_vox*sigma_vox))
CK=OUT/'checkpoint.npz';TR=OUT/'trace.jsonl'
if CK.exists():
 z=np.load(CK);step=int(z['step']);psi=z['psi'].astype(np.complex128);y=z['y'].astype(float)
else:
 step=START;p=np.load(ROOT/f'psi_{START:05d}.npy').astype(np.complex128);yy=np.load(ROOT/f'y_{START:05d}.npy').astype(float);psi=np.repeat(p[None],3,0);y=np.repeat(yy[None],3,0)
 for i,c in [(1,life),(2,matched)]:
  w=wgt(c);psi[i]*=np.exp(1j*EPS*w);y[i]*=(1+EPS*w[None])
 if TR.exists():TR.unlink()
 json.dump({'life_track':36037,'life_birth_coord':life,'matched_nonlife_coord':matched,'start_t':4.5,'life_death_t':6.5,'end_t':7.0,'sigma_vox':sigma_vox,'eps':EPS},open(OUT/'config.json','w'),indent=2)
def rec(st):
 o={'step':st,'t':st*dt,'branches':{}}
 for i,l in [(1,'life'),(2,'matched')]:
  qp=np.abs(psi[i]-psi[0])**2;qy=np.sum((y[i]-y[0])**2,0);sp=qp.sum();sy=qy.sum();ip=(qp*qp).sum()/(sp*sp+1e-300);iy=(qy*qy).sum()/(sy*sy+1e-300)
  o['branches'][l]={'dpsi_l2':float(np.sqrt(sp*dV)),'dy_l2':float(np.sqrt(sy*dV)),'effvox_psi':float(1/ip),'effvox_y':float(1/iy)}
 with open(TR,'a') as f:f.write(json.dumps(o)+'\n');print(o,flush=True)
rec(step);end=min(step+CHUNK,END);t0=time.time()
for st in range(step+1,end+1):
 psi=IF(F(psi)*half);r=np.abs(psi)**2;vm=lam[0]*y[:,0]+lam[1]*y[:,1];psi*=np.exp(-1j*(Lambda*r+vm)*dt);y[:,0]+=dt*nu[0]*(r-y[:,0]);y[:,1]+=dt*nu[1]*(r-y[:,1]);psi=IF(F(psi)*half)
 if st%200==0:rec(st)
np.savez(CK,step=end,psi=psi,y=y);print('BLOCK',step,end,'sec',time.time()-t0,flush=True)
if end<END:raise SystemExit
# reconstruct persistent newborn tracks at t7

def strict(r):
 mx=None
 for i in (-1,0,1):
  for j in (-1,0,1):
   for z in (-1,0,1):
    if i==j==z==0:continue
    a=np.roll(r,(i,j,z),(0,1,2));mx=a if mx is None else np.maximum(mx,a)
 return r>mx
steps=list(range(0,6001,200));frames=[]
for s in steps:
 p=np.load(ROOT/f'psi_{s:05d}.npy').astype(np.complex128);frames.append(np.argwhere(strict(np.abs(p)**2)).astype(float))
tracks={};nxt=0;prev=None
for fi,B in enumerate(frames):
 ids=np.full(len(B),-1,int)
 if fi==0:
  ids=np.arange(nxt,nxt+len(B));nxt+=len(B)
  for j,t in enumerate(ids):tracks[int(t)]=[(fi,j)]
 else:
  A=frames[fi-1]
  if len(A) and len(B):
   tb=cKDTree(B,boxsize=N);_,jab=tb.query(A);ta=cKDTree(A,boxsize=N);_,jba=ta.query(B)
   for ai,bj in enumerate(jab):
    if jba[bj]==ai:tid=int(prev[ai]);ids[bj]=tid;tracks[tid].append((fi,int(bj)))
  for j in range(len(B)):
   if ids[j]<0:ids[j]=nxt;tracks[nxt]=[(fi,j)];nxt+=1
 prev=ids
new=[]
for tid,path in tracks.items():
 if path[0][0]==14 and len(path)>=4:
  _,pi=path[0];new.append((tid,frames[14][pi].astype(int).tolist(),len(path)))
br=np.abs(psi[0])**2
def aura(c):
 c=tuple(c);val=float(br[c]);lap=sum(np.roll(br,1,a)+np.roll(br,-1,a)-2*br for a in range(3))/(dx*dx);curv=max(float(-lap[c]/(val+1e-30)),1e-12);sig=(3/curv)**.5/dx
 ax=[]
 for ci in c:
  q=np.abs(np.arange(N)-ci);q=np.minimum(q,N-q);ax.append(q.astype(float))
 A,B,C=np.meshgrid(*ax,indexing='ij');return np.exp(-.5*(A*A+B*B+C*C)/(sig*sig))
res={}
for ib,l in [(1,'life'),(2,'matched')]:
 qp=np.abs(psi[ib]-psi[0])**2;qy=np.sum((y[ib]-y[0])**2,0);sp=qp.sum();sy=qy.sum();rows=[]
 for tid,c,ll in new:
  w=aura(c);rows.append({'track':tid,'coord':c,'length':ll,'p':float((w*qp).sum()/(sp+1e-300)),'m':float((w*qy).sum()/(sy+1e-300))})
 P=sorted(rows,key=lambda r:r['p'],reverse=True);M=sorted(rows,key=lambda r:r['m'],reverse=True);rp={r['track']:i+1 for i,r in enumerate(P)};rm={r['track']:i+1 for i,r in enumerate(M)}
 for r in rows:r['rank_p']=rp[r['track']];r['rank_m']=rm[r['track']]
 res[l]={'top_p':P[:20],'top_m':M[:20],'static_target_39300':next((r for r in rows if r['track']==39300),None),'all':rows}
json.dump({'newborn_count':len(new),'results':res},open(OUT/'worldtube_captures.json','w'),indent=2)
print('DONE',len(new),flush=True)
