#!/usr/bin/env python3
"""Gate A (domain-unpinned) sample + menu generator. Reproducible (fixed seed)."""
import yaml, glob, json, random
from collections import defaultdict

random.seed(20260811)
WS = ".superpowers/sdd/2026-08-11-identity-integrity-remediation"
DOM_ORDER = ['SEC', 'COD', 'ARC', 'TST', 'QAL', 'AGT', 'DAT']

entries = {}
docs = {}
for f in sorted(glob.glob('domains/*.yml')):
    doc = yaml.safe_load(open(f)) or {}
    dom = doc['domain']
    docs[dom] = doc
    for c, e in (doc.get('entries') or {}).items():
        e['_domain'] = dom
        entries[c] = e

# ---- advisor menu (domain-unpinned; criteria inline where present) ----
menu = ["# OCRDb assignment menu — DOMAIN-UNPINNED",
        "Assign each finding the single best code from ANYWHERE in this menu.",
        "Format: CODE name (SEVERITY). `criteria:` disambiguates confusable boundaries.", ""]
for dom in DOM_ORDER:
    doc = docs.get(dom)
    if not doc:
        continue
    menu.append(f"## {dom} — {doc.get('name', '')}")
    for c in sorted(k for k in entries if entries[k]['_domain'] == dom):
        e = entries[c]
        menu.append(f"- {c} {e.get('name', '')} ({e.get('default_severity', '?')})")
        crit = e.get('criteria')
        if crit:
            menu.append(f"    criteria: {' '.join(crit.split())}")
open(f"{WS}/gate-a-menu.md", "w").write("\n".join(menu) + "\n")

# ---- finding pool ----
pool = []  # (text, code, domain, recurrence)
for c, e in entries.items():
    for ex in (e.get('examples') or []):
        pool.append((ex.strip(), c, e['_domain'], int(e.get('recurrence', 1) or 1)))

bydom = defaultdict(list)
for it in pool:
    bydom[it[2]].append(it)
total = len(pool)

# largest-remainder allocation of 100 across domains proportional to pool size
raw = {d: 100 * len(v) / total for d, v in bydom.items()}
alloc = {d: int(raw[d]) for d in raw}
rem = 100 - sum(alloc.values())
for d in sorted(raw, key=lambda x: raw[x] - int(raw[x]), reverse=True)[:rem]:
    alloc[d] += 1

def weighted_sample(items, n):
    # Efraimidis-Spirakis weighted reservoir (without replacement)
    keyed = sorted(((random.random() ** (1.0 / max(w, 1)), t, c, dm, w)
                    for (t, c, dm, w) in items), reverse=True)
    return [(t, c, dm, w) for _, t, c, dm, w in keyed[:n]]

sample = []
for d, items in bydom.items():
    n = min(alloc.get(d, 0), len(items))
    sample.extend(weighted_sample(items, n))

random.shuffle(sample)
findings = []
key = {}
for i, (text, code, dom, rec) in enumerate(sample, 1):
    fid = f"GA-{i:03d}"
    findings.append(f"- {fid}: {text}")
    key[fid] = {"true_code": code, "domain": dom, "recurrence": rec}

hdr = ["# Gate A findings — assign one code each (domain-unpinned)",
       f"{len(findings)} findings. For EACH, output the single best OCRDb code.", ""]
open(f"{WS}/gate-a-findings.md", "w").write("\n".join(hdr + findings) + "\n")
json.dump(key, open(f"{WS}/gate-a-key.json", "w"), indent=2)

# report
print(f"pool={total} sample={len(sample)}")
print("allocation:", {d: alloc.get(d, 0) for d in DOM_ORDER})
print("sampled by domain:", dict(sorted(defaultdict(int, {d: sum(1 for s in sample if s[2] == d) for d in bydom}).items())))
print("distinct true codes in sample:", len({s[1] for s in sample}))
