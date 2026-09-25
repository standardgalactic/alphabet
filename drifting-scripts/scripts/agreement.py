import json
d=json.load(open("out/glyph_similarity.json"))
sets={k:{(a,b) for a,b,_ in v["pairs"]} for k,v in d.items()}
names=list(sets)
core=set.intersection(*sets.values())
print("pairs in all fonts:", sorted(core))
from collections import Counter
c=Counter(p for s in sets.values() for p in s)
print("pair counts:", sorted(c.items(), key=lambda kv:(-kv[1],kv[0])))
for k,v in d.items():
    print(k, "opt %.3f greedy %.3f gap %.3f" % (v["total"], v["greedy_total"], v["total"]-v["greedy_total"]))
# table of named pairs
for p in ["BP","UV","CG","EF","MN","OQ","IL","CK","MW","AH"]:
    print(p, " ".join("%.2f"%d[k]["named"][p] for k in names))
# pairs in at least 2 fonts
print([p for p,n in c.items() if n>=2])
