#!/usr/bin/env python3
from pathlib import Path
import argparse, csv, json, re
import numpy as np
import matplotlib.pyplot as plt

def load_npz(path):
    z=np.load(path); ticks=sorted({int(re.match(r't(\d+)_',k).group(1)) for k in z.files})
    return z,ticks

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args()
    out=Path(args.out); z,ticks=load_npz(out/'readout_snapshots.npz')
    # One figure, multiple time panels only for state evolution; no success thresholds.
    fig=plt.figure(figsize=(16,9))
    show=ticks[-6:] if len(ticks)>6 else ticks
    for j,t in enumerate(show,1):
        ax=fig.add_subplot(2,3,j,projection='3d')
        rho=z[f't{t}_rho']; n=min(3500,len(rho)); idx=np.arange(n)
        s=5+55*(rho[:n]/max(rho[0],1e-30))
        ax.scatter(z[f't{t}_kx'][:n],z[f't{t}_ky'][:n],z[f't{t}_kz'][:n],s=s,alpha=.5)
        ax.set_title(f'tick {t}'); ax.set_xlabel('kx');ax.set_ylabel('ky');ax.set_zlabel('kz')
    fig.suptitle('TRIAD Universe v0 — raw strongest modal field regions (observer-only)')
    fig.tight_layout();fig.savefig(out/'01_modal_field_evolution.png',dpi=180);plt.close(fig)

    rows=list(csv.DictReader((out/'trajectory.csv').open()))
    t=np.array([float(r['physical_time']) for r in rows]);
    fig=plt.figure(figsize=(10,6)); ax=fig.add_subplot(111)
    ax.plot(t,[float(r['norm']) for r in rows],label='norm')
    ax.plot(t,[float(r['interference']) for r in rows],label='interference')
    ax.plot(t,[float(r['memory_energy']) for r in rows],label='memory energy')
    ax.set_xlabel('physical time');ax.set_ylabel('raw observable');ax.legend();ax.grid(alpha=.2)
    ax.set_title('Raw trajectory — no observable fed back into dynamics')
    fig.tight_layout();fig.savefig(out/'02_raw_trajectory.png',dpi=180);plt.close(fig)

    last=ticks[-1]; rho=z[f't{last}_rho'];
    fig=plt.figure(figsize=(10,6)); ax=fig.add_subplot(111)
    n=min(12000,len(rho));
    ax.scatter(np.arange(n),rho[:n],s=3,alpha=.4)
    ax.set_yscale('log');ax.set_xlabel('rank among strongest sampled modes');ax.set_ylabel('rho')
    ax.set_title(f'Final modal density rank, tick {last}')
    fig.tight_layout();fig.savefig(out/'03_final_density_rank.png',dpi=180);plt.close(fig)
if __name__=='__main__':main()
