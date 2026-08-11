#!/usr/bin/env python3
"""Tabulate Gate A inter-rater agreement across the 3 advisor passes."""
import json, glob, yaml
from collections import defaultdict

WS = ".superpowers/sdd/2026-08-11-identity-integrity-remediation"
key = json.load(open(f"{WS}/gate-a-key.json"))
adv = [json.load(open(f"{WS}/gate-a-advisor-{i}.json")) for i in (1, 2, 3)]

codes = set()
for f in glob.glob('domains/*.yml'):
    doc = yaml.safe_load(open(f)) or {}
    codes |= set((doc.get('entries') or {}).keys())

fids = sorted(key)
n = len(fids)
pref = lambda c: c[:6] if c and len(c) >= 6 else c   # DOMAIN-AREA-CAT (e.g. SEC-A2)

full3 = cat3 = acc3 = 0
pf = pc = 0
acc = [0, 0, 0]
invalid = []
dis = []
byd = defaultdict(lambda: [0, 0])
pairs = [(0, 1), (0, 2), (1, 2)]

for fid in fids:
    a = [adv[i].get(fid, "?") for i in range(3)]
    tc = key[fid]['true_code']; d = key[fid]['domain']
    for i, c in enumerate(a):
        if c not in codes:
            invalid.append((fid, i + 1, c))
        if c == tc:
            acc[i] += 1
    if a[0] == a[1] == a[2]:
        full3 += 1
    if pref(a[0]) == pref(a[1]) == pref(a[2]):
        cat3 += 1
    if a[0] == a[1] == a[2] == tc:
        acc3 += 1
    pf += sum(1 for x, y in pairs if a[x] == a[y])
    pc += sum(1 for x, y in pairs if pref(a[x]) == pref(a[y]))
    byd[d][1] += 1
    if a[0] == a[1] == a[2]:
        byd[d][0] += 1
    else:
        dis.append((fid, a, tc, d))

print(f"N = {n}")
print(f"FULL-CODE 3-way agreement:     {full3}/{n} = {full3/n:.0%}")
print(f"CATEGORY-PREFIX 3-way agreement: {cat3}/{n} = {cat3/n:.0%}")
print(f"pairwise full-code:            {pf}/{3*n} = {pf/(3*n):.0%}")
print(f"pairwise category-prefix:      {pc}/{3*n} = {pc/(3*n):.0%}")
print(f"accuracy vs home (per advisor): {[f'{x/n:.0%}' for x in acc]}")
print(f"all-3-match-home:              {acc3}/{n} = {acc3/n:.0%}")
print(f"invalid/hallucinated codes:    {len(invalid)} {invalid[:15]}")
print("per-domain full-code 3-way:    " + ", ".join(f"{d} {v[0]}/{v[1]}" for d, v in sorted(byd.items())))
print(f"\n--- {len(dis)} disagreements (fid [domain] home -> [a1,a2,a3]) ---")
for fid, a, tc, d in dis:
    print(f"{fid} [{d}] {tc} -> {a}")
