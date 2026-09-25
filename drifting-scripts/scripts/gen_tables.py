import json, math
def grp(n): return "{:,}".format(n).replace(",", "\\,")
gs=json.load(open("out/glyph_similarity.json"))
ex=json.load(open("out/exposure.json"))
sch=json.load(open("out/schedule_sim.json"))
gantt=json.load(open("out/gantt_K40_nu25.json"))

# T1 counting
n=26
def df(m):
    r=1
    for j in range(m-1,0,-2): r*=j
    return r
rows=[]
for k in (1,2,3,5,8,10,13):
    rows.append((k,2*k,math.comb(n,2*k)*df(2*k)))
T=[1,1]
for i in range(2,n+1): T.append(T[-1]+(i-1)*T[-2])
D=[1,0]
for i in range(2,n+1): D.append((i-1)*(D[-1]+D[-2]))
with open("tables/counting.tex","w") as f:
    f.write("\\begin{tabular}{rrr}\n\\toprule\nPairs exchanged $k$ & Letters changed $2k$ & Reciprocal alphabets $\\binom{26}{2k}(2k-1)!!$\\\\\n\\midrule\n")
    for k,m,c in rows: f.write(f"{k} & {m} & {grp(c)}\\\\\n")
    f.write("\\midrule\n")
    f.write(f"\\multicolumn{{2}}{{l}}{{All reciprocal alphabets, $I(26)$}} & {grp(T[n])}\\\\\n")
    f.write(f"\\multicolumn{{2}}{{l}}{{All permutations without fixed points, $D(26)$}} & {grp(D[n])}\\\\\n")
    f.write(f"\\multicolumn{{2}}{{l}}{{All permutations, $26!$}} & {grp(math.factorial(26))}\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# T2 resemblance per font
with open("tables/resemblance.tex","w") as f:
    f.write("\\begin{tabular}{lrrrll}\n\\toprule\nFont & Optimal total & Mean per pair & Greedy total & Weakest pair & Strongest pair\\\\\n\\midrule\n")
    for name,v in gs.items():
        pr=sorted(v["pairs"],key=lambda x:x[2])
        w=pr[0]; s=pr[-1]
        f.write(f"{name} & {v['total']:.3f} & {v['mean']:.3f} & {v['greedy_total']:.3f} & {w[0]}{w[1]} ({w[2]:.2f}) & {s[0]}{s[1]} ({s[2]:.2f})\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# T3 named pairs
names=list(gs)
with open("tables/namedpairs.tex","w") as f:
    f.write("\\begin{tabular}{l"+"r"*len(names)+"}\n\\toprule\nPair & "+" & ".join(names)+"\\\\\n\\midrule\n")
    for p in ["OQ","CG","EF","BP","MN","CK","MW","AH","UV","IL"]:
        f.write(p[0]+"/"+p[1]+" & "+" & ".join("%.2f"%gs[k]["named"][p] for k in names)+"\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# T3b optimal pairings per font
with open("tables/pairings.tex","w") as f:
    f.write("\\begin{tabular}{lp{9.2cm}}\n\\toprule\nFont & Optimal reciprocal pairing (overlap in parentheses)\\\\\n\\midrule\n")
    for name,v in gs.items():
        f.write(name+" & "+", ".join(f"{a}{b} ({w:.2f})" for a,b,w in v["pairs"])+"\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# T4 exposure
rows={r[0]:r for r in ex["rows"]}
sel="etandmbkjqz"
with open("tables/exposure.tex","w") as f:
    f.write("\\begin{tabular}{crrrr}\n\\toprule\nLetter & Freq. & Per stage, uniform & To final stage, exposure-driven & In words\\\\\n\\midrule\n")
    for ch in sel:
        r=rows[ch]
        f.write(f"{ch} & {100*r[1]:.2f}\\% & {grp(round(r[2]))} & {grp(round(r[3]))} & {grp(round(r[4]))}\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# T5 schedule
with open("tables/schedule.tex","w") as f:
    f.write("\\begin{tabular}{rrrrrr}\n\\toprule\n$\\kappa$ & $\\nu$ & Capacity bound $n\\kappa/\\nu$ & Rare-letter bound $\\kappa/p_{\\min}$ & Rare-first & Frequent-first\\\\\n\\midrule\n")
    for key,v in sch.items():
        f.write(f"{v['K']} & {v['nu']:.2f} & {grp(round(v['lb_capacity']))} & {grp(round(v['lb_rare']))} & {grp(round(v['rare_first']))} & {grp(round(v['frequent_first']))}\\\\\n")
    f.write("\\bottomrule\n\\end{tabular}\n")
# Gantt (tikz), x in thousands of letters
order=list(gantt.keys())
xmax=60000
with open("tables/gantt.tex","w") as f:
    f.write("\\begin{tikzpicture}[x=0.00022cm,y=0.31cm]\n")
    for i,ch in enumerate(order):
        s,e=gantt[ch]
        y=-i
        f.write(f"\\fill[gray!55] ({s:.0f},{y-0.35:.2f}) rectangle ({e:.0f},{y+0.35:.2f});\n")
        f.write(f"\\node[anchor=east,font=\\footnotesize\\ttfamily] at (-300,{y}) {{{ch}}};\n")
    f.write(f"\\draw[->] (0,{-len(order)+0.2:.1f}) -- ({xmax},{-len(order)+0.2:.1f});\n")
    for x in range(0,60001,10000):
        f.write(f"\\draw ({x},{-len(order)+0.2:.1f}) -- ({x},{-len(order)-0.1:.1f}) node[below,font=\\scriptsize]{{{x//1000}}};\n")
    f.write(f"\\node[font=\\scriptsize] at ({xmax/2:.0f},{-len(order)-2.6:.1f}) {{position in the book (thousands of letters)}};\n")
    f.write("\\end{tikzpicture}\n")
print("ok")
