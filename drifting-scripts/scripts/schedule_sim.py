import json
LEW = dict(zip("etaoinshrdlcumwfgypbvkjxqz",
 [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987, 4.253, 4.025, 2.782, 2.758, 2.406, 2.360, 2.228, 2.015, 1.974, 1.929, 1.492, 0.978, 0.772, 0.153, 0.150, 0.095, 0.074]))
tot=sum(LEW.values()); p={k:v/tot for k,v in LEW.items()}
n=26
def simulate(order, K, nu):
    """Fluid model: letter l is in transition for K/p_l letters, adding load p_l.
    Start each letter, in the given order, at the earliest time at which total load
    stays <= nu for its whole interval. Returns makespan (letters) and intervals."""
    ivs=[]  # (start,end,load)
    def load_ok(s,e,pl):
        pts=sorted({s}|{a for a,b,_ in ivs if s<=a<e}|{b for a,b,_ in ivs if s<b<=e})
        for t in pts:
            cur=sum(l for a,b,l in ivs if a<=t<b)
            if cur+pl>nu+1e-12: return False
        return True
    out={}
    for ch in order:
        d=K/p[ch]; pl=p[ch]
        cands=sorted({0.0}|{b for a,b,_ in ivs})
        for s in cands:
            if load_ok(s,s+d,pl):
                ivs.append((s,s+d,pl)); out[ch]=(s,s+d); break
        else:
            raise RuntimeError("no slot for "+ch)
    return max(e for s,e in out.values()), out
def main():
    freq_desc=sorted(p,key=lambda c:-p[c]); freq_asc=freq_desc[::-1]
    res={}
    print("lower bounds: n*K/nu and K/pmin")
    for K in (20,40,80):
        for nu in (0.15,0.25,0.40):
            lb1=n*K/nu; lb2=K/min(p.values())
            h_asc,_=simulate(freq_asc,K,nu); h_desc,_=simulate(freq_desc,K,nu)
            print("K=%2d nu=%.2f  LB nK/nu=%8.0f  LB K/pmin=%8.0f  rare-first=%8.0f  frequent-first=%8.0f  (letters)" % (K,nu,lb1,lb2,h_asc,h_desc))
            res[f"{K}_{nu}"]=dict(K=K,nu=nu,lb_capacity=lb1,lb_rare=lb2,rare_first=h_asc,frequent_first=h_desc)
    json.dump(res,open("out/schedule_sim.json","w"),indent=1)
    # detail for K=40, nu=0.2 rare-first: starts
    h,iv=simulate(freq_asc,40,0.25)
    print("detail K=40 nu=0.25 rare-first:")
    for ch in freq_asc: print(ch, "start %8.0f end %8.0f" % iv[ch])
    json.dump({ch:iv[ch] for ch in freq_asc},open('out/gantt_K40_nu25.json','w'))

if __name__=='__main__':
    main()
