#!/usr/bin/env python3
from pathlib import Path
import json,math,time,os
import numpy as np
from scipy.fft import fftn,ifftn
from scipy.spatial import cKDTree
ROOT=Path('/mnt/data/triad_rebuild_rules/run64'); OUT=Path('/mnt/data/triad_soul_background_matched'); OUT.mkdir(exist_ok=True)
N=64;L=20.;dx=L/N;dV=dx**3;dt=.0025;START=2600;END=2800;EPS=1e-6;workers=-1
old_life=[6,26,32]; sigma_vox=1.2338802034935676
# pick non-peak controls
controls={'life':old_life,'matched1':[13,39,32],'matched2':[32,25,13],'matched3':[51,39,32]}
k=2*np.pi*np.fft.fftfreq(N,d=dx);KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij');K2=KX*KX+KY*KY+KZ*KZ;half=np.exp(-1j*K2*dt/4)
nu=np.array([10.,.5]);lam=np.array([1.125,.375]);Lambda=-8.
def F(a):return fftn(a,axes=(-3,-2,-1),workers=workers)
def IF(a):return ifftn(a,axes=(-3,-2,-1),workers=workers)
def wgt(c):
 ax=[]
 for ci in c:
  q=np.abs(np.arange(N)-ci);q=np.minimum(q,N-q);ax.append(q.astype(float))
 A,B,C=np.meshgrid(*ax,indexing='ij');return np.exp(-.5*(A*A+B*B+C*C)/(sigma_vox*sigma_vox))
p=np.load(ROOT/f'psi_{START:05d}.npy').astype(np.complex128);yy=np.load(ROOT/f'y_{START:05d}.npy').astype(float);rho=np.abs(p)**2
# check whether background coords are strict maxima
def strict(r):
 mx=None
 for i in (-1,0,1):
  for j in (-1,0,1):
   for z in (-1,0,1):
    if i==j==z==0:continue
    a=np.roll(r,(i,j,z),(0,1,2));mx=a if mx is None else np.maximum(mx,a)
 return r>mx
mm=strict(rho); print({k:bool(mm[tuple(c)]) for k,c in controls.items()},flush=True)
labels=['base']+list(controls);B=len(labels);psi=np.repeat(p[None],B,0);y=np.repeat(yy[None],B,0)
for bi,(lab,c) in enumerate(controls.items(),1):
 w=wgt(c);psi[bi]*=np.exp(1j*EPS*w);y[bi]*=(1+EPS*w[None])
for st in range(START+1,END+1):
 psi=IF(F(psi)*half);r=np.abs(psi)**2;vm=lam[0]*y[:,0]+lam[1]*y[:,1];psi*=np.exp(-1j*(Lambda*r+vm)*dt);y[:,0]+=dt*nu[0]*(r-y[:,0]);y[:,1]+=dt*nu[1]*(r-y[:,1]);psi=IF(F(psi)*half)
# newborn persistent tracks reconstructed
steps=list(range(0,6001,200));frames=[]
for s in steps:
 pp=np.load(ROOT/f'psi_{s:05d}.npy').astype(np.complex128);frames.append(np.argwhere(strict(np.abs(pp)**2)).astype(float))
tracks={};nxt=0;prev=None
for fi,Bc in enumerate(frames):
 ids=np.full(len(Bc),-1,int)
 if fi==0:
  ids=np.arange(nxt,nxt+len(Bc));nxt+=len(Bc)
  for j,t in enumerate(ids):tracks[int(t)]=[(fi,j)]
 else:
  A=frames[fi-1]
  if len(A) and len(Bc):
   tb=cKDTree(Bc,boxsize=N);_,jab=tb.query(A);ta=cKDTree(A,boxsize=N);_,jba=ta.query(Bc)
   for ai,bj in enumerate(jab):
    if jba[bj]==ai:
     tid=int(prev[ai]);ids[bj]=tid;tracks[tid].append((fi,int(bj)))
  for j in range(len(Bc)):
   if ids[j]<0:ids[j]=nxt;tracks[nxt]=[(fi,j)];nxt+=1
 prev=ids
new=[]
for tid,path in tracks.items():
 if path[0][0]==14 and len(path)>=4:
  _,pi=path[0];new.append((tid,frames[14][pi].astype(int).tolist(),len(path)))
br=np.abs(psi[0])**2
# target aura widths use natural curvature independently
def aura(c):
 c=tuple(c);val=float(br[c]);lap=sum(np.roll(br,1,a)+np.roll(br,-1,a)-2*br for a in range(3))/(dx*dx);curv=max(float(-lap[c]/(val+1e-30)),1e-12);sig=(3/curv)**.5/dx
 ax=[]
 for ci in c:
  q=np.abs(np.arange(N)-ci);q=np.minimum(q,N-q);ax.append(q.astype(float))
 A,B,C=np.meshgrid(*ax,indexing='ij');return np.exp(-.5*(A*A+B*B+C*C)/(sig*sig))
res={}
for bi,lab in enumerate(labels[1:],1):
 qp=np.abs(psi[bi]-psi[0])**2;qy=np.sum((y[bi]-y[0])**2,0);sp=qp.sum();sy=qy.sum();rows=[]
 for tid,c,ll in new:
  w=aura(c);rows.append({'track':tid,'coord':c,'length':ll,'p':float((w*qp).sum()/sp),'m':float((w*qy).sum()/sy)})
 P=sorted(rows,key=lambda r:r['p'],reverse=True);M=sorted(rows,key=lambda r:r['m'],reverse=True)
 ip=(qp*qp).sum()/(sp*sp);iy=(qy*qy).sum()/(sy*sy)
 res[lab]={'coord':controls[lab],'max_p':P[0],'max_m':M[0],'top5_p':P[:5],'top5_m':M[:5],'effvox_p':float(1/ip),'effvox_m':float(1/iy),'dpsi_l2':float(np.sqrt(sp*dV))}
json.dump({'strict_max_start':{k:bool(mm[tuple(c)]) for k,c in controls.items()},'sigma_vox_matched':sigma_vox,'newborn_count':len(new),'results':res},open(OUT/'background_control.json','w'),indent=2)
print(json.dumps(res,indent=2),flush=True)
