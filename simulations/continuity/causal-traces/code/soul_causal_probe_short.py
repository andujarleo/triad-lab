#!/usr/bin/env python3
from pathlib import Path
import os, json, time, math
import numpy as np
from scipy.fft import fftn, ifftn
from scipy.spatial import cKDTree

ROOT=Path('/mnt/data/triad_rebuild_rules/run64')
OUT=Path('/mnt/data/triad_soul_causal_short'); OUT.mkdir(parents=True,exist_ok=True)
N=64; L=20.; dt=.0025; dx=L/N; dV=dx**3
START=2600; END=2800 # t=6.5 -> 7.0
RUN=int(os.environ.get('RUN',str(END-START)))
EPS=float(os.environ.get('EPS','1e-6'))
workers=int(os.environ.get('FFT_WORKERS','-1'))
# primary static-recurrence case plus matched-duration controls
old_tracks={36037:[6,26,32],36055:[6,32,38],36034:[6,26,26],36119:[13,26,26]}
primary=36037
# half-eps primary linearity branch appended
labels=['base']+[f'track_{k}' for k in old_tracks]+[f'track_{primary}_half']
B=len(labels)

# R5 exact dynamics
hbar=1.; mass=1.; Lambda=-8.; nu=np.array([10.,.5]); lam=np.array([1.125,.375])
k=2*np.pi*np.fft.fftfreq(N,d=dx); KX,KY,KZ=np.meshgrid(k,k,k,indexing='ij'); K2=KX*KX+KY*KY+KZ*KZ
half_lin=np.exp(-1j*(K2/(2*mass))*dt/2)

def F(a): return fftn(a,axes=(-3,-2,-1),workers=workers)
def IF(a): return ifftn(a,axes=(-3,-2,-1),workers=workers)

def periodic_d2_grid(c):
    axes=[]
    for ci in c:
        q=np.arange(N)-ci; q=np.minimum(np.abs(q),N-np.abs(q)); axes.append(q.astype(float))
    A,B,C=np.meshgrid(*axes,indexing='ij'); return A*A+B*B+C*C

def curvature_sigma(rho,c):
    c=tuple(map(int,c)); val=float(rho[c]); lap=sum(np.roll(rho,1,a)+np.roll(rho,-1,a)-2*rho for a in range(3))/(dx*dx)
    curv=max(float(-lap[c]/(val+1e-30)),1e-12)
    return math.sqrt(3.0/curv),curv,val

def aura_weight(rho,c):
    sig_phys,curv,val=curvature_sigma(rho,c); sig_vox=sig_phys/dx
    d2=periodic_d2_grid(c)
    w=np.exp(-0.5*d2/(sig_vox*sig_vox))
    return w,{'sigma_phys':sig_phys,'sigma_vox':sig_vox,'curvature':curv,'rho_peak':val}

psi0=np.load(ROOT/f'psi_{START:05d}.npy').astype(np.complex128)
y0=np.load(ROOT/f'y_{START:05d}.npy').astype(np.float64)
rho0=np.abs(psi0)**2
psi=np.repeat(psi0[None,...],B,axis=0); y=np.repeat(y0[None,...],B,axis=0)
probe_meta={}
bi=1
for tid,c in old_tracks.items():
    w,meta=aura_weight(rho0,c); e=EPS
    psi[bi] *= np.exp(1j*e*w) # exact norm preserving phase tag
    # memory tag: infinitesimal multiplicative perturbation of local historical state
    y[bi] *= (1.0 + e*w[None,...])
    probe_meta[str(tid)]={'coord':c,**meta,'eps':e}
    bi+=1
# half eps branch
w,meta=aura_weight(rho0,old_tracks[primary]); e=EPS/2
psi[bi] *= np.exp(1j*e*w); y[bi] *= (1.0+e*w[None,...])
probe_meta[f'{primary}_half']={'coord':old_tracks[primary],**meta,'eps':e}

# initial norm differences
norm0=np.sum(np.abs(psi)**2,axis=(1,2,3))*dV
record_steps=set([START,2640,2680,2720,2760,2800])
trace=[]
def record(step):
    basep=psi[0]; basey=y[0]
    rec={'step':step,'t':step*dt,'branches':{}}
    for i,label in enumerate(labels[1:],1):
        dp=psi[i]-basep; dy=y[i]-basey
        qp=np.abs(dp)**2; qy=np.sum(dy*dy,axis=0)
        sP=float(qp.sum()); sY=float(qy.sum())
        # effective volume / concentration, no threshold
        iprP=float((qp*qp).sum()/(sP*sP+1e-300)) if sP else 0.
        iprY=float((qy*qy).sum()/(sY*sY+1e-300)) if sY else 0.
        rec['branches'][label]={'delta_psi_l2':float(np.sqrt(sP*dV)),'delta_y_l2':float(np.sqrt(sY*dV)),
            'influence_ipr_psi':iprP,'influence_ipr_y':iprY,'influence_effvox_psi':float(1/iprP) if iprP else None,'influence_effvox_y':float(1/iprY) if iprY else None}
    trace.append(rec)
record(START)

t0=time.time(); final=min(START+RUN,END)
for st in range(START+1,final+1):
    psi=IF(F(psi)*half_lin)
    rho=np.abs(psi)**2
    Vmem=lam[0]*y[:,0]+lam[1]*y[:,1]
    psi *= np.exp(-1j*(Lambda*rho+Vmem)*dt)
    y[:,0] += dt*nu[0]*(rho-y[:,0]); y[:,1] += dt*nu[1]*(rho-y[:,1])
    psi=IF(F(psi)*half_lin)
    if st in record_steps: record(st); print('record',st,st*dt,flush=True)
    if not np.isfinite(psi).all() or not np.isfinite(y).all(): raise RuntimeError('nonfinite')
print('evolve seconds',time.time()-t0,flush=True)

# save final batch if complete
np.savez(OUT/'probe_final.npz',step=final,psi=psi,y=y,norm0=norm0,labels=np.array(labels,dtype=object))
json.dump({'labels':labels,'start':START,'end':final,'dt':dt,'eps':EPS,'probe_meta':probe_meta,'trace':trace,'norm0':norm0.tolist()},open(OUT/'probe_trace.json','w'),indent=2)
if final<END:
    print('PARTIAL',final); raise SystemExit

# Reconstruct natural strict-max tracks to identify persistent births at t=11.5.
def strict_max_mask(rho):
    mx=None
    for i in (-1,0,1):
      for j in (-1,0,1):
       for kk in (-1,0,1):
        if i==j==kk==0: continue
        a=np.roll(rho,(i,j,kk),(0,1,2)); mx=a if mx is None else np.maximum(mx,a)
    return rho>mx
steps=list(range(0,6001,200)); frames=[]
for s in steps:
    pp=np.load(ROOT/f'psi_{s:05d}.npy').astype(np.complex128); rr=np.abs(pp)**2
    frames.append(np.argwhere(strict_max_mask(rr)).astype(float))
tracks={}; nextid=0; prev_ids=None
for fi,Bc in enumerate(frames):
    n=len(Bc)
    if fi==0:
        ids=np.arange(nextid,nextid+n); nextid+=n
        for j,tid in enumerate(ids): tracks[int(tid)]=[(fi,j)]
    else:
        Ac=frames[fi-1]; ids=np.full(n,-1,int)
        if len(Ac) and len(Bc):
            tB=cKDTree(Bc,boxsize=N); dAB,jAB=tB.query(Ac,k=1)
            tA=cKDTree(Ac,boxsize=N); _,jBA=tA.query(Bc,k=1)
            for ai,bj in enumerate(jAB):
                if jBA[bj]==ai:
                    tid=int(prev_ids[ai]); ids[bj]=tid; tracks[tid].append((fi,int(bj)))
        for bj in range(n):
            if ids[bj]<0:
                tid=nextid; nextid+=1; ids[bj]=tid; tracks[tid]=[(fi,bj)]
    prev_ids=ids
birth_fi=14 # 7.0
newborn=[]
for tid,path in tracks.items():
    if path[0][0]==birth_fi and len(path)>=4:
        fi,pi=path[0]; newborn.append((tid,frames[fi][pi].astype(int).tolist(),len(path)))
print('persistent newborn',len(newborn),flush=True)
basep=psi[0]; basey=y[0]; base_rho=np.abs(basep)**2
# build target aura weights and attributes
newW=[]; newmeta=[]
for tid,c,ll in newborn:
    ww,mm=aura_weight(base_rho,c); newW.append(ww); newmeta.append({'track':tid,'coord':c,'length':ll,**mm})
# captures per probe
captures={}
for i,label in enumerate(labels[1:],1):
    dp=psi[i]-basep; dy=y[i]-basey
    qp=np.abs(dp)**2; qy=np.sum(dy*dy,axis=0); denp=qp.sum()+1e-300; deny=qy.sum()+1e-300
    rows=[]
    for ww,mm in zip(newW,newmeta):
        rows.append({**mm,'capture_psi':float((ww*qp).sum()/denp),'capture_y':float((ww*qy).sum()/deny)})
    # ranks independent
    rowsP=sorted(rows,key=lambda r:r['capture_psi'],reverse=True)
    rowsY=sorted(rows,key=lambda r:r['capture_y'],reverse=True)
    rankP={r['track']:j+1 for j,r in enumerate(rowsP)}; rankY={r['track']:j+1 for j,r in enumerate(rowsY)}
    for r in rows: r['rank_psi']=rankP[r['track']]; r['rank_y']=rankY[r['track']]
    captures[label]={'top_psi':rowsP[:10],'top_y':rowsY[:10],'rows':rows}
json.dump({'newborn_count':len(newborn),'captures':captures},open(OUT/'causal_captures.json','w'),indent=2)
print('DONE',OUT)
