import sys, json, itertools
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import networkx as nx

FONTS = {
 "DejaVu Sans": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
 "Liberation Sans": "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
 "DejaVu Serif": "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
 "TeX Gyre Pagella": "/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyrepagella-regular.otf",
}
LET = [chr(c) for c in range(ord('A'), ord('Z')+1)]
SIZE = 160   # em size in px
CANVAS = 200

def render(font, ch):
    im = Image.new("L", (CANVAS, CANVAS), 0)
    d = ImageDraw.Draw(im)
    # anchor on baseline, centred horizontally by advance width
    adv = font.getlength(ch)
    d.text(((CANVAS-adv)/2, CANVAS*0.75), ch, font=font, fill=255, anchor="ls")
    a = np.array(im) > 127
    return a

def iou(a, b):
    inter = np.logical_and(a, b).sum()
    uni = np.logical_or(a, b).sum()
    return inter/uni if uni else 0.0

out = {}
for name, path in FONTS.items():
    try:
        font = ImageFont.truetype(path, SIZE)
    except Exception as e:
        print("skip", name, e); continue
    bm = {c: render(font, c) for c in LET}
    W = {}
    for a, b in itertools.combinations(LET, 2):
        W[(a,b)] = iou(bm[a], bm[b])
    G = nx.Graph()
    for (a,b), w in W.items():
        G.add_edge(a, b, weight=w)
    M = nx.max_weight_matching(G, maxcardinality=True)
    pairs = sorted(tuple(sorted(p)) for p in M)
    total = sum(W[p] for p in pairs)
    top = sorted(W.items(), key=lambda kv: -kv[1])[:12]
    # greedy baseline: repeatedly take best remaining pair
    used=set(); greedy=[]
    for (a,b), w in sorted(W.items(), key=lambda kv: -kv[1]):
        if a in used or b in used: continue
        greedy.append(((a,b),w)); used.update([a,b])
    gtotal = sum(w for _, w in greedy)
    named = {f"{a}{b}": W[(a,b)] for a,b in [("B","P"),("U","V"),("C","G"),("E","F"),("M","N"),("O","Q"),("I","L"),("C","K"),("M","W"),("A","H")]}
    out[name] = dict(pairs=[(a,b,W[(a,b)]) for a,b in pairs], total=total,
                     mean=total/13, greedy_total=gtotal, top=[(a,b,w) for (a,b),w in top], named=named)
    print("==", name)
    print(" optimal reciprocal derangement total IoU = %.3f (mean %.3f per pair)" % (total, total/13))
    print(" greedy total = %.3f" % gtotal)
    print(" pairs:", " ".join(f"{a}{b}:{W[(a,b)]:.2f}" for a,b in pairs))
    print(" top12:", " ".join(f"{a}{b}:{w:.2f}" for (a,b),w in top))
    print(" named:", " ".join(f"{k}:{v:.2f}" for k,v in named.items()))
json.dump(out, open("out/glyph_similarity.json","w"), indent=1)
