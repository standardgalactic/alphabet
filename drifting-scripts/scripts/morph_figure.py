import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
CELL=140; SIZE=110
font=ImageFont.truetype(FONT,SIZE)
def ink(ch):
    im=Image.new("L",(CELL,CELL),0); d=ImageDraw.Draw(im)
    adv=font.getlength(ch)
    d.text(((CELL-adv)/2,CELL*0.80),ch,font=font,fill=255,anchor="ls")
    return np.array(im,dtype=float)/255
def dot(cx,cy,r=9):
    im=Image.new("L",(CELL,CELL),0); d=ImageDraw.Draw(im)
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=255); return np.array(im,dtype=float)/255
B,P=ink("B"),ink("P")
dot_above=dot(CELL*0.5,CELL*0.10)   # offset vector u for the stored-B path
dot_below=dot(CELL*0.5,CELL*0.93)   # opposite offset for the stored-P path
ts=[0,0.25,0.5,0.75,1.0]
def row(start,end,mark=None):
    cells=[]
    for t in ts:
        img=(1-t)*start+t*end
        if mark is not None: img=img+math.sin(math.pi*t)*mark
        cells.append(np.clip(img,0,1))
    return np.hstack(cells)
rows=[row(B,P),row(P,B),row(B,P,dot_above),row(P,B,dot_below)]
gap=np.zeros((14,CELL*len(ts)))
canvas=np.vstack([rows[0],gap,rows[1],gap,rows[2],gap,rows[3]])
img=Image.fromarray(np.round(255*(1-canvas)).astype("uint8"),"L")
img.save("out/morph.png",dpi=(300,300))
print(img.size)
# check: the two linear rows coincide at t=0.5, detour rows do not
c=2*CELL
print("linear rows identical at t=.5:", np.allclose(rows[0][:,c:c+CELL],rows[1][:,c:c+CELL]))
print("detour rows identical at t=.5:", np.allclose(rows[2][:,c:c+CELL],rows[3][:,c:c+CELL]))
d=np.abs(rows[2][:,c:c+CELL]-rows[3][:,c:c+CELL]).sum()
print("L1 difference between detour rows at t=.5: %.1f px-units" % d)
