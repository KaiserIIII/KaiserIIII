#!/usr/bin/env python3
"""Render the warm, editorial motion cover for the GitHub profile.

Pure Pillow: no external animation APIs, video players, fonts shipped in repo,
analytics or remote assets. The motion is a preview of the hosted SVG explorer.
"""
from __future__ import annotations
import argparse
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 422
COUNT = 48
DURATION_MS = 100
PAPER = (248, 245, 239)
INK = (48, 45, 41)
MUTED = (124, 112, 99)
TERRA = (183, 117, 89)
BLUE = (112, 138, 162)
SAGE = (115, 139, 129)
PALE = (224, 214, 202)
CARD = (253, 250, 246)

def font(path: str, size: int):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
ITALIC = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
LABEL = font(SANS, 13)
CAPTION = font(SANS, 17)
TITLE = font(SERIF, 59)
SUBTITLE = font(ITALIC, 53)
MONOGRAM = font(ITALIC, 43)
SMALL = font(SANS, 11)

def cubic(p, t):
    u = 1 - t
    return (
        (u**3)*p[0][0] + 3*(u**2)*t*p[1][0] + 3*u*(t**2)*p[2][0] + (t**3)*p[3][0],
        (u**3)*p[0][1] + 3*(u**2)*t*p[1][1] + 3*u*(t**2)*p[2][1] + (t**3)*p[3][1],
    )

def interpolate(a, b, t):
    return tuple(int(x*(1-t) + y*t) for x,y in zip(a,b))

def draw_frame(index):
    phase = index / COUNT
    im = Image.new("RGB", (W,H), PAPER)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((23,22,1177,400), radius=15, fill=CARD, outline=PALE, width=2)
    d.rectangle((24,22,30,400),fill=TERRA)
    d.text((62,54),"YUE YU / KAISER  —  PERSONAL NOTEBOOK",font=LABEL,fill=TERRA)
    d.text((60,111),"I like making things.",font=TITLE,fill=INK)
    d.text((60,193),"And understanding them.",font=SUBTITLE,fill=TERRA)
    d.line((62,283,693,283),fill=PALE,width=2)
    d.text((62,307),"SOFTWARE / GAMES / ENGINEERING / EXPERIMENTS",font=CAPTION,fill=MUTED)
    d.text((62,370),"MADE WITH CURIOSITY.   BUILT IN CODE.",font=SMALL,fill=(153,139,124))

    cx,cy = 1010,211
    d.ellipse((cx-168,cy-168,cx+168,cy+168),outline=(224,214,201),width=2)
    d.ellipse((cx-132,cy-132,cx+132,cy+132),outline=(216,202,188),width=2)
    d.ellipse((cx-93,cy-93,cx+93,cy+93),outline=(215,200,185),width=2)
    d.ellipse((cx-53,cy-53,cx+53,cy+53),fill=(239,225,212),outline=(197,164,143),width=2)
    # Curved evidence connections follow one common Bezier formula and loop seamlessly.
    paths=[
        ([(859,124),(950,81),(1043,319),(1155,268)],TERRA,0.0),
        ([(874,306),(938,374),(1074,104),(1160,146)],BLUE,.27),
        ([(928,67),(1050,97),(931,346),(1087,359)],SAGE,.58),
    ]
    for j,(p,color,shift) in enumerate(paths):
        curve=[cubic(p,k/70) for k in range(71)]
        d.line([(round(x),round(y)) for x,y in curve], fill=interpolate(color,CARD,.16),width=2)
        for step in (0,.45):
            t=(phase+shift+step)%1
            x,y=cubic(p,t)
            rr=4 if step==0 else 3
            d.ellipse((x-rr,y-rr,x+rr,y+rr),fill=color)
        for x,y in (p[0],p[-1]):
            d.ellipse((x-4,y-4,x+4,y+4),fill=color)

    # Quiet phase-dependent halo; not a flashing attention trap.
    radius=55+int(7*math.sin(2*math.pi*phase))
    d.ellipse((cx-radius,cy-radius,cx+radius,cy+radius),outline=(213,183,163),width=1)
    d.text((cx,cy+15),"Y.",font=MONOGRAM,fill=(114,83,68),anchor="mm")
    d.text((828,51),"FIG. 001",font=SMALL,fill=(164,150,137))
    d.text((1040,387),"BUILD  /  VERIFY  /  LEARN",font=SMALL,fill=MUTED,anchor="mm")
    return im

def render(path):
    destination=Path(path)
    destination.parent.mkdir(parents=True,exist_ok=True)
    frames=[draw_frame(i).quantize(colors=96,method=Image.Quantize.MEDIANCUT) for i in range(COUNT)]
    frames[0].save(destination,format="GIF",save_all=True,
        append_images=frames[1:],optimize=True,loop=0,
        duration=DURATION_MS,disposal=2)
    output=Image.open(destination)
    if output.n_frames < COUNT//2:
        raise RuntimeError("The motion output collapsed to too few frames")
    print("Rendered",destination,"frames",output.n_frames,"bytes",destination.stat().st_size)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="assets/portrait-motion.gif")
    render(parser.parse_args().output)
