#!/usr/bin/env python3
"""Render a looping, warm editorial animation for the GitHub profile.

The README itself cannot run interactive JS: this animated GIF is a preview
of the repository-owned interactive HTML graph. No uploaded fonts or tracking.
"""
from __future__ import annotations
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 398
FRAMES, DURATION = 40, 90
BG=(247,243,237); INK=(49,44,39); MUTED=(121,108,97)
TERRA=(185,99,73); SAGE=(104,128,113); BLUE=(110,137,159); PLUM=(141,119,147)
PALETTE=[TERRA,SAGE,BLUE,PLUM]
COLS=[(160,154,147),(225,216,204),(255,252,248)]
FONTS={
    "display": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}
def font(name,size):
    try: return ImageFont.truetype(FONTS[name],size)
    except OSError: return ImageFont.load_default()
F_BOLD=font("sans",15); F_LABEL=font("sans",15); F_TAG=font("sans",12)
F_DISPLAY=font("display",70); F_TITLE=font("display",29)
DOMAINS=["Systems","Data","Verification","Research"]
PROJECTS=["CardCraft","Zhixu","WiFiScope","MigrationWitness","Cost Analyzer","ReproShift"]
LINKS=[(0,0),(0,1),(0,4),(1,1),(1,2),(1,3),(1,4),(2,0),(2,2),(2,3),(3,3),(3,5)]
START=[(728,130+i*64) for i in range(4)]
END=[(1112,100+i*49) for i in range(6)]

def blend(color,base,fraction):
    return tuple(int(c*fraction+b*(1-fraction)) for c,b in zip(color,base))

def cubic(p0,p1,p2,p3,t):
    v=1-t
    return (v**3*p0[0]+3*v*v*t*p1[0]+3*v*t*t*p2[0]+t**3*p3[0],
            v**3*p0[1]+3*v*v*t*p1[1]+3*v*t*t*p2[1]+t**3*p3[1])

def rounded(draw,rect,radius,fill,outline=None,width=1):
    draw.rounded_rectangle(rect,radius=radius,fill=fill,outline=outline,width=width)

def frame(i):
    t=i/FRAMES
    focus=int((i*4)/FRAMES)%4
    phase=(t*4)%1
    canvas=Image.new("RGB",(W,H),BG)
    d=ImageDraw.Draw(canvas)
    rounded(d,(25,20,1175,378),18,(253,250,245),(227,218,208),1)
    d.rectangle((25,20,31,378),fill=TERRA)
    d.text((61,52),"Y U E  Y U    /    K A I S E R",font=F_BOLD,fill=TERRA)
    d.text((58,99),"I build systems.",font=F_DISPLAY,fill=INK)
    d.text((61,184),"that stand up to inspection.",font=F_TITLE,fill=INK)
    d.line((61,247,595,247),fill=(220,207,195),width=2)
    d.text((61,270),"ENGINEERING MANAGEMENT × COMPUTER SCIENCE",font=F_LABEL,fill=MUTED)
    d.text((61,315),"OPEN THE INTERACTIVE EXPERIENCE  →",font=F_BOLD,fill=TERRA)
    # Soft interactive preview on right: a generative, animated bipartite graph.
    rounded(d,(666,49,1142,349),17,(250,247,242),(229,220,211),1)
    d.text((694,68),"LIVE GRAPH / CAPABILITIES × PROJECTS",font=F_TAG,fill=(143,128,115))
    for idx,p in enumerate(START):
        x,y=p
        active=idx==focus
        d.ellipse((x-9,y-9,x+9,y+9),fill=blend(PALETTE[idx],BG,.21),outline=PALETTE[idx] if active else (205,197,187),width=2)
        d.ellipse((x-3,y-3,x+3,y+3),fill=PALETTE[idx])
        d.text((x+15,y-10),DOMAINS[idx],font=F_TAG,fill=INK if active else MUTED)
    for idx,p in enumerate(END):
        x,y=p
        active=idx in [b for a,b in LINKS if a==focus]
        x=981
        rounded(d,(x,y-16,1125,y+15),7,blend(PALETTE[focus],BG,.09) if active else (255,253,249),(223,212,200),1)
        d.text((x+9,y-8),PROJECTS[idx],font=F_TAG,fill=INK if active else (145,137,128))
    for a,b in LINKS:
        x0=875; y0=START[a][1];x3=981;y3=END[b][1]
        p0=(x0,y0);p1=(x0+37,y0);p2=(x3-31,y3);p3=(x3,y3)
        on=a==focus
        points=[cubic(p0,p1,p2,p3,j/20) for j in range(21)]
        line=[(round(x),round(y)) for x,y in points]
        d.line(line,fill=blend(PALETTE[a],BG,.75) if on else (225,217,208),width=2 if on else 1,joint="curve")
        if on:
            local=(phase+(a*0.1)+(b*0.12))%1
            x,y=cubic(p0,p1,p2,p3,local)
            d.ellipse((x-4,y-4,x+4,y+4),fill=PALETTE[a])
    rounded(d,(696,332,827,350),7,blend(PALETTE[focus],BG,.18))
    d.text((703,333),DOMAINS[focus].upper(),font=F_TAG,fill=PALETTE[focus])
    return canvas

def render(path):
    images=[frame(i).quantize(colors=128,method=Image.Quantize.MEDIANCUT) for i in range(FRAMES)]
    dest=Path(path);dest.parent.mkdir(parents=True,exist_ok=True)
    images[0].save(dest,format="GIF",save_all=True,append_images=images[1:],
                   loop=0,duration=DURATION,optimize=True,disposal=2)
    recheck=Image.open(dest)
    if recheck.n_frames<FRAMES//2: raise RuntimeError("Motion output unexpectedly truncated")
    print("Generated",dest,"frames=",recheck.n_frames,"bytes=",dest.stat().st_size)

if __name__=="__main__":
    import argparse
    arg=argparse.ArgumentParser()
    arg.add_argument("--output",default="assets/portrait-motion.gif")
    render(arg.parse_args().output)
