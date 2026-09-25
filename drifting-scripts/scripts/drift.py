"""Exposure-driven drift staging for a visual substitution alphabet.
Stage 0 shows a letter in its familiar form; stage S shows its substituted partner.
A letter advances one stage after every K further occurrences, once its own delay
(counted in occurrences of that letter) has passed."""
import sys
PAIRS = ["BP", "UV", "CG", "EF", "MN", "OQ"]
PI = {}
for a, b in PAIRS:
    PI[a] = b; PI[b] = a

def stages(text, K, S, delay):
    seen, out = {}, []
    for ch in text:
        up = ch.upper()
        if up in PI:
            c = seen.get(up, 0); seen[up] = c + 1
            st = max(0, min(S, (c - delay.get(up, 0)) // K))
            out.append((ch, st))
        else:
            out.append((ch, None))
    return out

def show(tokens, S):
    """Discrete rendering: final stage shows the partner letter; earlier stages the original."""
    res = []
    for ch, st in tokens:
        if st == S:
            p = PI[ch.upper()]
            res.append(p if ch.isupper() else p.lower())
        else:
            res.append(ch)
    return "".join(res)

def involution_ok():
    return all(PI[PI[x]] == x for x in PI)

if __name__ == "__main__":
    assert involution_ok()
    text = open(sys.argv[1], encoding="utf-8").read()
    K, S = int(sys.argv[2]), int(sys.argv[3])
    delay = {ch: int(sys.argv[4]) * i for i, ch in enumerate("BPUVCGEFMNOQ")} if len(sys.argv) > 4 else {}
    tok = stages(text, K, S, delay)
    print(show(tok, S)[:0], end="")
    # report, per letter, the character position where stage S is first reached
    first = {}
    for pos, (ch, st) in enumerate(tok):
        if st == S and ch.upper() not in first:
            first[ch.upper()] = pos
    print("first position at final stage:", dict(sorted(first.items(), key=lambda kv: kv[1])))
    print("tokens at final stage in last 1000 chars: %d of %d letters in the alphabet" %
          (sum(1 for _, s in tok[-1000:] if s == S), sum(1 for _, s in tok[-1000:] if s is not None)))
