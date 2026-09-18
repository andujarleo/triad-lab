#!/usr/bin/env python3
from pathlib import Path
import argparse, math
import numpy as np
import matplotlib.pyplot as plt

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();out=Path(args.out)
    z=np.load(out/'universe_checkpoint.npz');re=z['re'];im=z['im'];y=z['y'];N=len(re)
    side=round(N**(1/3))
    if side**3!=N: raise SystemExit('This renderer expects a perfect-cube active mode count')
    rho=(re.astype(np.float64)**2+im.astype(np.float64)**2).reshape(side,side,side) # z,y,x; x fastest in native map
    phase=np.arctan2(im,re).reshape(side,side,side)
    mem=y.reshape(3,N).reshape(3,side,side,side)
    c=side//2
    fig,axs=plt.subplots(2,3,figsize=(15,9),constrained_layout=True)
    panels=[(rho[c],'rho · kz=0'),(rho[:,c,:],'rho · ky=0'),(rho[:,:,c],'rho · kx=0'),
            (phase[c],'phase · kz=0'),(mem[0,c],'memory fast · kz=0'),(mem[2,c],'memory slow · kz=0')]
    for ax,(a,title) in zip(axs.flat,panels):
        imh=ax.imshow(a,origin='lower',aspect='equal');ax.set_title(title);fig.colorbar(imh,ax=ax,shrink=.75)
    fig.suptitle('TRIAD Universe v0 — final full modal-lattice slices (actual checkpoint)')
    fig.savefig(out/'04_final_full_modal_slices.png',dpi=180);plt.close(fig)

    # Raw shell sums: no Bravais classification or acceptance score.
    coords=np.arange(side)-side//2
    Z,Y,X=np.meshgrid(coords,coords,coords,indexing='ij');kr=np.sqrt(X*X+Y*Y+Z*Z)
    shell=np.rint(kr).astype(int);maxs=shell.max();power=np.bincount(shell.ravel(),weights=rho.ravel(),minlength=maxs+1)
    counts=np.bincount(shell.ravel(),minlength=maxs+1);mean=np.divide(power,counts,out=np.zeros_like(power),where=counts>0)
    fig=plt.figure(figsize=(10,6));ax=fig.add_subplot(111);ax.plot(np.arange(len(mean)),mean);ax.set_yscale('log');ax.set_xlabel('integer k-shell radius');ax.set_ylabel('mean rho');ax.set_title('Raw radial modal density — no family classifier');ax.grid(alpha=.2);fig.tight_layout();fig.savefig(out/'05_final_modal_shells.png',dpi=180);plt.close(fig)
if __name__=='__main__':main()
