import math
pi = {}
for a,b in [("B","P"),("U","V")]:
    pi[a]=b; pi[b]=a
def enc(s): return "".join(pi.get(c,c) for c in s)
for w in ["PUBLIC","BLUE","LOVE","PUBLIC BUBBLE","BUPLIC"]:
    print(w, "->", enc(w), "->", enc(enc(w)))
# involution is its own inverse
assert all(enc(enc(w))==w for w in ["PUBLIC","BLUE","LOVE"])
# counting
n=26
T=[1,1]
for i in range(2,n+1): T.append(T[-1]+(i-1)*T[-2])
def df(m):
    r=1
    for j in range(m-1,0,-2): r*=j
    return r
tot=0
rows=[]
for k in range(0,14):
    c=math.comb(n,2*k)*df(2*k) if k>0 else 1
    tot+=c; rows.append((k,2*k,c))
print("sum check", tot==T[n], tot, T[n])
for r in rows: print(r)
print("26!",math.factorial(26))
print("ratio 26!/I(26) =", math.factorial(26)/T[n])
