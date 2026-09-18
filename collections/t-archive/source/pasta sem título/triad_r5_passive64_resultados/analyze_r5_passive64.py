#!/usr/bin/env python3
from pathlib import Path
import json, numpy as np
import matplotlib.pyplot as plt

ROOT=Path('/mnt/data/triad_r5_passive64')
with open(ROOT/'config.json') as f: cfg=json.load(f)
N=cfg['N']; L=cfg['L']; dx=L/N; dV=dx**3
files=sorted(ROOT.glob('psi_*.npy'))
k1=2*np.pi*np.fft.fftfreq(N,d=dx)
KX,KY,KZ=np.meshgrid(k1,k1,k1,indexing='ij'); K=np.sqrt(KX*KX+KY*KY+KZ*KZ)
dk=2*np.pi/L
shell=np.rint(K/dk).astype(np.int32)
maxshell=shell.max()

def wrap(a): return (a+np.pi)%(2*np.pi)-np.pi

def calc(path,prev_rho=None):
    step=int(path.stem.split('_')[1]); t=step*cfg['dt']
    psi=np.load(path).astype(np.complex128); rho=np.abs(psi)**2; th=np.angle(psi)
    s1=rho.sum(); s2=np.sum(rho*rho)
    pr=float((s1*s1)/(s2+1e-300)); ipr=float(s2/(s1*s1+1e-300))
    mean=float(rho.mean()); std=float(rho.std()); cv=std/(mean+1e-300)
    phase_global=float(np.abs(np.mean(np.exp(1j*th))))
    # nearest-neighbor phase agreement, continuous
    neigh=(np.cos(th-np.roll(th,1,0))+np.cos(th-np.roll(th,1,1))+np.cos(th-np.roll(th,1,2)))/3
    phase_local=float(np.mean(neigh))
    # density fluctuation spectrum
    dr=rho-mean
    P=np.abs(np.fft.fftn(dr))**2
    P[0,0,0]=0.0; total=float(P.sum())
    if total>1e-40:
        q=P.ravel()/total; q=q[q>0]
        entropy=float(-np.sum(q*np.log(q))/np.log(N**3))
        spec_pr=float(1/np.sum(q*q))
        shellpow=np.bincount(shell.ravel(),weights=P.ravel(),minlength=maxshell+1)
        shellpow[0]=0
        dom_shell=int(np.argmax(shellpow)); kdom=dom_shell*dk; kL=kdom*L
        shell_frac=float(shellpow[dom_shell]/(shellpow.sum()+1e-300))
        centroid=float(np.sum(P*K)/total)
    else:
        entropy=spec_pr=kdom=kL=shell_frac=centroid=0.0; dom_shell=0
    # roughness
    gx=np.roll(rho,-1,0)-np.roll(rho,1,0); gy=np.roll(rho,-1,1)-np.roll(rho,1,1); gz=np.roll(rho,-1,2)-np.roll(rho,1,2)
    rough=float(np.mean(gx*gx+gy*gy+gz*gz))
    # winding plaquettes (integer topology, no threshold)
    vort=0
    for a,b in [(0,1),(1,2),(2,0)]:
        t0=th; ta=np.roll(th,-1,a); tab=np.roll(ta,-1,b); tb=np.roll(th,-1,b)
        circ=wrap(ta-t0)+wrap(tab-ta)+wrap(tb-tab)+wrap(t0-tb)
        w=np.rint(circ/(2*np.pi)).astype(np.int8)
        vort += int(np.count_nonzero(w))
    # sound-A from prior lab definition; passive only
    soundA=float(np.mean(np.abs(rho-prev_rho))) if prev_rho is not None else 0.0
    return {'step':step,'t':t,'norm2':float(s1*dV),'rho_mean':mean,'rho_std':std,'cv':cv,'rho_max':float(rho.max()),
            'participation_cells':pr,'ipr_cells':ipr,'phase_global':phase_global,'phase_local_cos':phase_local,
            'spectral_entropy':entropy,'spectral_participation':spec_pr,'dominant_shell':dom_shell,'k_dom':kdom,'kL_dom':kL,
            'dominant_shell_power_fraction':shell_frac,'spectral_centroid':centroid,'roughness':rough,
            'vortex_plaquettes':vort,'soundA_mean_abs_drho':soundA}, rho

rows=[]; prev=None
for p in files:
    r,prev=calc(p,prev); rows.append(r)
with open(ROOT/'posthoc_metrics.json','w') as f: json.dump(rows,f,indent=2)

# automated descriptive extrema / turning points only; no feedback and no stopping
max_peak=max(rows,key=lambda r:r['rho_max']); min_pr=min(rows,key=lambda r:r['participation_cells']); max_cv=max(rows,key=lambda r:r['cv'])
# after initial dispersal, local maxima in rho_max at saved cadence
pulses=[]
for i in range(1,len(rows)-1):
    if rows[i]['rho_max']>rows[i-1]['rho_max'] and rows[i]['rho_max']>rows[i+1]['rho_max']:
        pulses.append({'t':rows[i]['t'],'rho_max':rows[i]['rho_max'],'cv':rows[i]['cv'],'kL_dom':rows[i]['kL_dom']})
summary={'n_snapshots':len(rows),'max_peak':max_peak,'min_spatial_participation':min_pr,'max_cv':max_cv,'pulses':pulses,
         'final':rows[-1], 'norm_drift':rows[-1]['norm2']-rows[0]['norm2']}
with open(ROOT/'posthoc_summary.json','w') as f: json.dump(summary,f,indent=2)

# main time series
fig,axs=plt.subplots(4,2,figsize=(12,15))
series=[('rho_max','max density'),('cv','density CV'),('participation_cells','spatial participation (cells)'),
        ('spectral_entropy','spectral entropy'),('dominant_shell_power_fraction','dominant shell power fraction'),
        ('kL_dom','dominant k × L'),('phase_local_cos','local phase coherence (cos)'),('vortex_plaquettes','phase winding plaquettes')]
for ax,(key,title) in zip(axs.flat,series):
    ax.plot([r['t'] for r in rows],[r[key] for r in rows],marker='o',ms=3)
    ax.set_title(title); ax.set_xlabel('t'); ax.grid(alpha=.25)
    if key in ('rho_max','participation_cells','vortex_plaquettes'): ax.set_yscale('symlog',linthresh=1e-8)
plt.tight_layout(); fig.savefig(ROOT/'posthoc_timeseries.png',dpi=170); plt.close(fig)

# selected density slices at fixed saved times: initial, 5, 10, 13, 15 where available
wanted=[0,2000,4000,5200,6000]
fig,axs=plt.subplots(1,len(wanted),figsize=(18,4))
for ax,st in zip(axs,wanted):
    p=ROOT/f'psi_{st:05d}.npy'; psi=np.load(p); rho=np.abs(psi)**2
    im=ax.imshow(rho[:,:,N//2].T,origin='lower',cmap='magma'); ax.set_title(f't={st*cfg["dt"]:.1f}'); ax.set_xticks([]); ax.set_yticks([])
    fig.colorbar(im,ax=ax,fraction=.046)
plt.tight_layout(); fig.savefig(ROOT/'density_slices_selected.png',dpi=170); plt.close(fig)

# log radial shell power over time as image
shellmat=[]
for p in files:
    psi=np.load(p); rho=np.abs(psi)**2; dr=rho-rho.mean(); P=np.abs(np.fft.fftn(dr))**2; P[0,0,0]=0
    sp=np.bincount(shell.ravel(),weights=P.ravel(),minlength=maxshell+1)
    shellmat.append(sp)
shellmat=np.array(shellmat)
fig,ax=plt.subplots(figsize=(11,6))
im=ax.imshow(np.log10(shellmat[:,1:]+1e-30).T,origin='lower',aspect='auto',extent=[rows[0]['t'],rows[-1]['t'],1,maxshell],cmap='viridis')
ax.set_xlabel('t'); ax.set_ylabel('radial spectral shell n'); ax.set_title('passive radial spectrum evolution: log10 power')
fig.colorbar(im,ax=ax,label='log10 power'); plt.tight_layout(); fig.savefig(ROOT/'spectrum_evolution.png',dpi=170); plt.close(fig)

print(json.dumps(summary,indent=2))
