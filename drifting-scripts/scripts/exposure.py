import re, math, json, collections
# Standard English letter frequencies (Lewand 2000), percent
LEW = dict(zip("etaoinshrdlcumwfgypbvkjxqz",
 [12.702, 9.056, 8.167, 7.507, 6.966, 6.749, 6.327, 6.094, 5.987, 4.253, 4.025, 2.782, 2.758, 2.406, 2.360, 2.228, 2.015, 1.974, 1.929, 1.492, 0.978, 0.772, 0.153, 0.150, 0.095, 0.074]))
tot=sum(LEW.values()); print("sum of table: %.3f" % tot)
p={k:v/tot for k,v in LEW.items()}
# book model: 80,000 words, mean 4.7 letters per word (assumption stated in essay)
words=80000; mean_len=4.7
L=int(words*mean_len); print("letters in model book:", L)
S=5; K=40
print("Uniform position schedule: stage length", L//S, "letters")
rows=[]
for ch in "etaoinz":
    pass
for ch in sorted(p, key=lambda c:-p[c]):
    per_stage=p[ch]*L/S
    need=K*S/p[ch]   # letters until K exposures in each of S stages (cumulative K*S)
    rows.append((ch,p[ch],per_stage,need,need/mean_len))
print("letter  freq   exposures/stage(uniform)  letters_for_exposure-driven(K=40,S=5)  words")
for r in rows: print("%s  %.4f  %10.1f  %12.0f  %9.0f" % r)
mx=max(p.values()); mn=min(p.values()); print("ratio most/least frequent: %.1f" % (mx/mn))
# fraction of letters whose exposure-driven finish exceeds book length
over=[r[0] for r in rows if r[3]>L]; print("letters not finishing within book:", over)
# empirical frequencies in the attached text
txt=open("/mnt/user-data/uploads/attachment.txt",encoding="utf-8").read().lower()
cnt=collections.Counter(c for c in txt if 'a'<=c<='z'); n=sum(cnt.values())
print("sample letters:", n)
for ch in "etaoinshrzqxjvk":
    print(ch, cnt[ch], "%.4f"%(cnt[ch]/n), "vs standard %.4f"%p[ch])
json.dump(dict(L=L,S=S,K=K,rows=rows,sample_n=n),open("out/exposure.json","w"))
