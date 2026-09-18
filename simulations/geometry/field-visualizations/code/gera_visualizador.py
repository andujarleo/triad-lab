#!/usr/bin/env python3
"""
Gerador do visualizador interativo
==================================
Não roda a dinâmica — lê os quadros do simula_filmes.py e gera um
arquivo ÚNICO, visualizador.html, que abre em qualquer navegador:

  - arraste com o mouse para girar o volume 3D
  - rodinha do mouse para aproximar
  - slider (ou ▶) para andar no tempo
  - camadas ligáveis: densidade, cordas de fase (+ e −), auto-giro

Uso:  python3 gera_visualizador.py
"""
import os
import json
import base64
import numpy as np

path = "bravais_outputs_3d/filmes_data.npz"
if not os.path.exists(path):
    raise SystemExit("não achei %s — rode o simula_filmes.py antes" % path)
dat = np.load(path)
R = dat["rho"].astype(np.float32)
PH = dat["fase"].astype(np.float32)
tempos = dat["tempos"].tolist()
order = dat["order"].astype(float)
L = float(dat["L"])
NF, N = R.shape[0], R.shape[1]

MAX_DENS = 2600    # pontos de densidade por quadro (limite visual)
MAX_VORT = 3200    # pontos de vórtice por quadro


def wrap(d):
    return (d + np.pi) % (2 * np.pi) - np.pi


def vortex_points(ph):
    pts = []
    a = ph[:-1, :-1, :]; b = ph[1:, :-1, :]; c = ph[1:, 1:, :]; d = ph[:-1, 1:, :]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i + 0.5, j + 0.5, k, np.sign(w[i, j, k])))
    a = ph[:-1, :, :-1]; b = ph[1:, :, :-1]; c = ph[1:, :, 1:]; d = ph[:-1, :, 1:]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i + 0.5, j, k + 0.5, np.sign(w[i, j, k])))
    a = ph[:, :-1, :-1]; b = ph[:, 1:, :-1]; c = ph[:, 1:, 1:]; d = ph[:, :-1, 1:]
    w = wrap(b - a) + wrap(c - b) + wrap(d - c) + wrap(a - d)
    for i, j, k in np.argwhere(np.abs(w) > np.pi):
        pts.append((i, j + 0.5, k + 0.5, np.sign(w[i, j, k])))
    return np.array(pts) if pts else np.zeros((0, 4))


dens_frames, vort_frames = [], []
vmax = np.percentile(R, 99.9)
for f in range(NF):
    rho = R[f]
    thr = np.percentile(rho, 97.0)
    idx = np.argwhere(rho > thr)
    vals = rho[idx[:, 0], idx[:, 1], idx[:, 2]]
    o = np.argsort(vals)[::-1][:MAX_DENS]
    dq = np.concatenate([idx[o].astype(np.uint8),
                         np.clip(255 * vals[o] / vmax, 0, 255)
                         .astype(np.uint8)[:, None]], axis=1)
    dens_frames.append(dq)

    vp = vortex_points(PH[f])
    if len(vp):
        thr_d = np.percentile(rho, 75.0)   # filtro visual: só região densa
        ii = np.clip(np.round(vp[:, :3]).astype(int), 0, N - 1)
        vp = vp[rho[ii[:, 0], ii[:, 1], ii[:, 2]] > thr_d]
    if len(vp) > MAX_VORT:
        vp = vp[np.random.choice(len(vp), MAX_VORT, replace=False)]
    vq = np.concatenate([np.round(vp[:, :3] * 2).astype(np.uint8),
                         (vp[:, 3] > 0).astype(np.uint8)[:, None]], axis=1) \
        if len(vp) else np.zeros((0, 4), np.uint8)
    vort_frames.append(vq)
    print("quadro %d/%d: %d densidade, %d vórtices" %
          (f + 1, NF, len(dq), len(vq)))


def pack(frames):
    offs, buf = [0], []
    for fr in frames:
        buf.append(fr.tobytes())
        offs.append(offs[-1] + len(fr))
    return base64.b64encode(b"".join(buf)).decode(), offs


d64, doffs = pack(dens_frames)
v64, voffs = pack(vort_frames)
meta = {"N": N, "L": L, "NF": NF, "tempos": tempos,
        "order": [round(float(o), 4) for o in order],
        "doffs": doffs, "voffs": voffs}

HTML = r"""<title>Cristal da Triade</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root { --bg:#070914; --panel:#11152a; --line:#232a4a; --tx:#dfe3f4;
          --dim:#8890ab; --hot:#ee6c4d; --cool:#5bc0be; }
  * { margin:0; box-sizing:border-box; }
  body { background:var(--bg); color:var(--tx);
         font:14px/1.5 "Segoe UI", system-ui, sans-serif;
         display:flex; flex-direction:column; height:100vh; overflow:hidden; }
  header { padding:10px 16px 6px; }
  header h1 { font-size:17px; font-weight:600; }
  header p { font-size:12px; color:var(--dim); }
  #wrap { flex:1; position:relative; min-height:0; }
  canvas { width:100%; height:100%; display:block; cursor:grab; }
  #hud { position:absolute; top:10px; left:12px; font-size:12px;
         color:var(--dim); pointer-events:none; }
  #controls { padding:10px 16px 14px; background:var(--panel);
              border-top:1px solid var(--line);
              display:flex; gap:14px; align-items:center; flex-wrap:wrap; }
  button { background:var(--line); color:var(--tx); border:0; border-radius:6px;
           padding:6px 14px; font-size:14px; cursor:pointer; }
  button:hover { background:#313a63; }
  input[type=range] { flex:1; min-width:140px; accent-color:var(--hot); }
  label { font-size:12.5px; color:var(--dim); display:flex; gap:5px;
          align-items:center; cursor:pointer; white-space:nowrap; }
  input[type=checkbox] { accent-color:var(--cool); }
  #tlabel { font-variant-numeric:tabular-nums; min-width:88px; font-size:12.5px; }
</style>
<header>
  <h1>Cristal da Tríade — visualizador</h1>
  <p>arraste para girar · rodinha aproxima · a equação completa rodou antes; aqui você só passeia pelos quadros salvos</p>
</header>
<div id="wrap">
  <canvas id="cv"></canvas>
  <div id="hud"></div>
</div>
<div id="controls">
  <button id="play">▶</button>
  <input type="range" id="tslider" min="0" value="0" step="1">
  <span id="tlabel"></span>
  <label><input type="checkbox" id="ldens" checked> densidade</label>
  <label><input type="checkbox" id="lvp" checked> cordas +2π</label>
  <label><input type="checkbox" id="lvm" checked> cordas −2π</label>
  <label><input type="checkbox" id="lauto" checked> auto-giro</label>
</div>
<script>
const META = __META__;
const DENS = Uint8Array.from(atob("__D64__"), c=>c.charCodeAt(0));
const VORT = Uint8Array.from(atob("__V64__"), c=>c.charCodeAt(0));
const N=META.N, NF=META.NF;
const cv=document.getElementById('cv'), ctx=cv.getContext('2d');
const hud=document.getElementById('hud');
const sl=document.getElementById('tslider'); sl.max=NF-1;
const tl=document.getElementById('tlabel');
let frame=0, playing=true, auto=true;
let rx=-0.45, ry=0.7, zoom=1.0, drag=null;

// paleta "vida" para densidade
const pal=[[11,19,43],[28,37,65],[58,80,107],[91,192,190],[244,211,94],[238,108,77]];
function col(v){ const t=v/255*(pal.length-1), i=Math.min(pal.length-2,Math.floor(t)),
  f=t-i, a=pal[i], b=pal[i+1];
  return [a[0]+f*(b[0]-a[0]), a[1]+f*(b[1]-a[1]), a[2]+f*(b[2]-a[2])]; }

function draw(){
  const W=cv.width=cv.clientWidth*devicePixelRatio,
        H=cv.height=cv.clientHeight*devicePixelRatio;
  ctx.fillStyle='#070914'; ctx.fillRect(0,0,W,H);
  const ca=Math.cos(ry), sa=Math.sin(ry), cb=Math.cos(rx), sb=Math.sin(rx);
  const S=Math.min(W,H)/(N*1.45)*zoom, cx=W/2, cy=H/2, h=N/2;
  const pts=[];
  if(document.getElementById('ldens').checked){
    const o0=META.doffs[frame]*4, o1=META.doffs[frame+1]*4;
    for(let o=o0;o<o1;o+=4){
      const x=DENS[o]-h, y=DENS[o+1]-h, z=DENS[o+2]-h, v=DENS[o+3];
      const X= ca*x+sa*z, Z=-sa*x+ca*z, Y= cb*y-sb*Z, Zd= sb*y+cb*Z;
      const c=col(v);
      pts.push([Zd, cx+X*S, cy-Y*S, c[0],c[1],c[2], 1.2+3.2*v/255, 0.75]);
    }
  }
  const wp=document.getElementById('lvp').checked,
        wm=document.getElementById('lvm').checked;
  if(wp||wm){
    const o0=META.voffs[frame]*4, o1=META.voffs[frame+1]*4;
    for(let o=o0;o<o1;o+=4){
      const s=VORT[o+3];
      if(s&&!wp || !s&&!wm) continue;
      const x=VORT[o]/2-h, y=VORT[o+1]/2-h, z=VORT[o+2]/2-h;
      const X= ca*x+sa*z, Z=-sa*x+ca*z, Y= cb*y-sb*Z, Zd= sb*y+cb*Z;
      const c=s?[255,94,120]:[67,230,224];
      pts.push([Zd, cx+X*S, cy-Y*S, c[0],c[1],c[2], 1.6, 0.85]);
    }
  }
  pts.sort((a,b)=>a[0]-b[0]);
  for(const p of pts){
    const depth=0.55+0.45*(p[0]/N+0.5);
    ctx.fillStyle=`rgba(${p[3]|0},${p[4]|0},${p[5]|0},${(p[7]*depth).toFixed(3)})`;
    ctx.beginPath(); ctx.arc(p[1],p[2],p[6]*devicePixelRatio*depth,0,6.283);
    ctx.fill();
  }
  const nd=META.doffs[frame+1]-META.doffs[frame],
        nv=META.voffs[frame+1]-META.voffs[frame];
  hud.textContent=`t = ${META.tempos[frame]}  ·  ordem ${META.order[META.tempos[frame]].toFixed(3)}  ·  ${nd} pontos de densidade, ${nv} vórtices`;
  tl.textContent=`quadro ${frame+1}/${NF}`;
  sl.value=frame;
}

let acc=0;
function tick(ts){
  if(auto && !drag) ry+=0.004;
  if(playing){ acc++; if(acc%9===0){ frame=(frame+1)%NF; } }
  draw(); requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

cv.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY];cv.style.cursor='grabbing';});
window.addEventListener('pointermove',e=>{ if(!drag) return;
  ry+=(e.clientX-drag[0])*0.008; rx+=(e.clientY-drag[1])*0.008;
  rx=Math.max(-1.5,Math.min(1.5,rx)); drag=[e.clientX,e.clientY]; });
window.addEventListener('pointerup',()=>{drag=null;cv.style.cursor='grab';});
cv.addEventListener('wheel',e=>{e.preventDefault();
  zoom=Math.max(0.4,Math.min(3.5,zoom*(e.deltaY<0?1.1:0.9)));},{passive:false});
sl.addEventListener('input',()=>{frame=+sl.value; playing=false;
  document.getElementById('play').textContent='▶';});
document.getElementById('play').addEventListener('click',e=>{
  playing=!playing; e.target.textContent=playing?'⏸':'▶';});
document.getElementById('play').textContent='⏸';
document.getElementById('lauto').addEventListener('change',e=>auto=e.target.checked);
</script>
"""

html = (HTML.replace("__META__", json.dumps(meta))
        .replace("__D64__", d64).replace("__V64__", v64))
out = "bravais_outputs_3d/visualizador.html"
with open(out, "w") as f:
    f.write(html)
print("salvo: %s  (%.1f MB) — abra no navegador" %
      (out, os.path.getsize(out) / 1e6))
