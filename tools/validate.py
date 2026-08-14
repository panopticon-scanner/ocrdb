#!/usr/bin/env python3
"""OCRDb domain-file validator: schema + stability contract.

Usage:
    python3 tools/validate.py [--domains-dir domains] [--baseline build/ocrdb-<prev>.json]

Exit codes: 0 = clean (warnings allowed), 1 = schema/stability errors.

Schema checks are hard errors. Single-homing (RATIFICATION big rock #0)
is enforced by construction — the catalog is a clean rewrite with no
cross-domain duplicate names. Cross-domain duplicate names remain a
WARNING here as a mechanical backstop, not a gate on that rule.

The stability contract (SCHEMA.md) activates at the 1.0 release:
with --baseline pointing at the previous release bundle, a code that
disappears or changes `name` is a hard error; `status: deprecated` with
`superseded_by` is the only sanctioned correction path.
"""
import argparse
import json
import os
import re
import sys

try:
    import yaml
except ImportError:  # build tooling fails loudly — no degraded builds
    sys.exit("tools/validate.py requires PyYAML (pip install pyyaml)")

CODE_RE = re.compile(r"^([A-Z]{3})-([A-Z])([1-9])([A-Z])$")
# Active domains carry real entries; incubating domains are declared in the
# CHARTER but seed no codes yet. Both may appear in the <DOM>-X0X gap sentinel.
ACTIVE_DOMAINS = {"SEC", "COD", "ARC", "TST", "QAL", "AGT", "DAT"}
INCUBATING_DOMAINS = {"OPS", "ACC", "LNG"}
SEEDED_INCUBATING = {"OPS", "ACC", "LNG"}  # domains seeded during 0.3.0 phase
ALL_DOMAINS = ACTIVE_DOMAINS | INCUBATING_DOMAINS
# The gap sentinel <DOM>-X0X is a RESERVED NON-ENTRY form: `0` is a reserved
# category digit and `X` a reserved area/issue letter, so it deliberately fails
# the strict entry CODE_RE. It is recognized here, never validated as an entry.
FALLBACK_RE = re.compile(r"^(%s)-X0X$" % "|".join(sorted(ALL_DOMAINS)))


def is_fallback_code(code):
    """True iff `code` is a recognized <DOM>-X0X gap sentinel."""
    return bool(FALLBACK_RE.match(str(code)))


# Flip to False at the 1.0 release: pre-1.0 the prior-art budget over-run is a
# WARNING (visible curation signal); at 1.0 it becomes a hard build error.
INCUBATING = True
PRIOR_ART_BUDGET = 0.25

CWE_RE = re.compile(r"^CWE-\d+$")
AUTOMATED_BY_RE = re.compile(r"^[a-z0-9_-]+:[A-Za-z0-9._@/+-]+$")
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
STATUSES = {"active", "deprecated"}
CHARACTERS = {"defect", "opportunity"}
PROVENANCE_VOCAB = {"corpus", "tool-observed", "gap-review", "prior-art",
                    "owasp-align", "asvs-align", "openssf-align", "cwe-align"}

# Consumer-side finding-field vocabularies (Tier 3). These describe a per-INSTANCE
# judgment a consumer records under its own disclosed discipline (e.g. panopticon's
# advisor-checked severity_override / finding disposition). They are DELIBERATELY
# NOT validated against domains/ entries — OCRDb defines the terms, not their use.
SEVERITY_MODIFIER_VOCAB = {
    "test-or-fixture-scope", "operator-controlled-input", "local-or-offline-context",
    "regenerable-or-recoverable-data", "dev-or-ci-tooling", "intentionally-public-value",
    "documented-accepted-risk", "compensating-control-present"}
DISPOSITION_VOCAB = {
    "defect", "control-present", "not-applicable", "correct-substrate"}


def load_domains(domains_dir):
    docs = {}
    for fn in sorted(os.listdir(domains_dir)):
        if fn.endswith((".yml", ".yaml")):
            with open(os.path.join(domains_dir, fn), encoding="utf-8") as fh:
                docs[fn] = yaml.safe_load(fh)
    return docs


def validate_schema(docs):
    errors, warnings = [], []
    all_codes = {}
    names_by_domain = {}
    domains_seen = {}
    for fn, doc in docs.items():
        if not isinstance(doc, dict) or "domain" not in doc:
            errors.append(f"{fn}: missing top-level 'domain'")
            continue
        dom = doc["domain"]
        if dom in domains_seen:
            errors.append(f"{fn}: domain {dom} already declared by "
                          f"{domains_seen[dom]}")
        domains_seen[dom] = fn
        areas = doc.get("areas") or {}
        entries = doc.get("entries") or {}
        if not doc.get("name"):
            errors.append(f"{fn}: missing domain display 'name'")
        for code, e in entries.items():
            ctx = f"{fn}:{code}"
            m = CODE_RE.match(code)
            if not m:
                errors.append(f"{ctx}: code does not match DOM-A1B grammar")
                continue
            cdom, area, cat, _ = m.groups()
            if cdom != dom:
                errors.append(f"{ctx}: code domain {cdom} != file domain {dom}")
            a = areas.get(area)
            if a is None:
                errors.append(f"{ctx}: area {area} not in areas header")
            elif str(cat) not in {str(k) for k in (a.get("categories") or {})}:
                errors.append(f"{ctx}: category {cat} not under area {area}")
            name = e.get("name")
            if not name or not NAME_RE.match(str(name)):
                errors.append(f"{ctx}: name missing or not kebab-case: {name!r}")
            if e.get("default_severity") not in SEVERITIES:
                errors.append(f"{ctx}: default_severity {e.get('default_severity')!r} "
                              f"not in {sorted(SEVERITIES)}")
            if e.get("status") not in STATUSES:
                errors.append(f"{ctx}: status {e.get('status')!r} not in {sorted(STATUSES)}")
            prov = e.get("provenance")
            if not isinstance(prov, list) or not prov:
                errors.append(f"{ctx}: provenance must be a non-empty list")
            for p in prov if isinstance(prov, list) else []:
                if p not in PROVENANCE_VOCAB:
                    errors.append(f"{ctx}: provenance {p!r} not in vocabulary")
            if e.get("status") == "deprecated" and not e.get("superseded_by"):
                errors.append(f"{ctx}: deprecated without superseded_by")
            if e.get("status") != "deprecated" and e.get("superseded_by"):
                errors.append(f"{ctx}: superseded_by on a non-deprecated entry")
            if "character" in e and e["character"] not in CHARACTERS:
                errors.append(f"{ctx}: character {e['character']!r} not in {sorted(CHARACTERS)}")
            for w in e.get("cwe") or []:
                if not (isinstance(w, str) and CWE_RE.match(w)):
                    errors.append(f"{ctx}: cwe {w!r} must be a 'CWE-<n>' string")
            ab = e.get("automated_by")
            if ab is not None:
                if not isinstance(ab, list):
                    errors.append(f"{ctx}: automated_by must be a list")
                else:
                    for r in ab:
                        if not (isinstance(r, str) and AUTOMATED_BY_RE.match(r)):
                            errors.append(f"{ctx}: automated_by {r!r} must be "
                                          f"'tool:rule-id'")
            if "recurrence" in e and (not isinstance(e["recurrence"], int)
                                      or e["recurrence"] < 1):
                errors.append(f"{ctx}: recurrence must be a positive int")
            all_codes[code] = e
            names_by_domain.setdefault(dom, {}).setdefault(str(name), []).append(code)
    # superseded_by must point at a real code
    for code, e in all_codes.items():
        tgt = e.get("superseded_by")
        if tgt and tgt not in all_codes:
            errors.append(f"{code}: superseded_by {tgt} does not exist")
        for ref in e.get("see_also") or []:
            if ref not in all_codes:
                errors.append(f"{code}: see_also {ref} does not exist")
            elif code not in (all_codes[ref].get("see_also") or []):
                errors.append(f"{code}: see_also {ref} not reciprocal "
                              f"({ref} does not see_also {code})")
    # duplicate names: hard error within a domain, warning across domains
    # (single-homing is enforced by construction post-clean-rewrite; the
    #  cross-domain warning is a mechanical backstop — see module docstring)
    cross = {}
    for dom, names in names_by_domain.items():
        for name, codes in names.items():
            if len(codes) > 1:
                errors.append(f"{dom}: name {name!r} used by {codes}")
            cross.setdefault(name, []).extend(codes)
    for name, codes in sorted(cross.items()):
        if len({c[:3] for c in codes}) > 1:
            warnings.append(f"cross-domain duplicate name {name!r}: {codes} "
                            f"(big rock #0 single-homing)")
    return errors, warnings, all_codes


def prior_art_budget_issues(all_codes):
    """Per-domain: entries grounded ONLY by prior-art (provenance has prior-art
    and NEITHER corpus NOR tool-observed) must be <= 25% of the domain. Returns
    over-budget messages (empty if all within budget)."""
    from collections import defaultdict
    total, ungrounded = defaultdict(int), defaultdict(int)
    for code, e in all_codes.items():
        dom = code[:3]
        total[dom] += 1
        prov = set(e.get("provenance") or [])
        if "prior-art" in prov and not (prov & {"corpus", "tool-observed"}):
            ungrounded[dom] += 1
    out = []
    for dom in sorted(total):
        n, u = total[dom], ungrounded[dom]
        if n and u > PRIOR_ART_BUDGET * n:
            out.append(f"prior-art budget: {dom} has {u}/{n} ungrounded "
                       f"prior-art entries ({u / n:.0%} > "
                       f"{PRIOR_ART_BUDGET:.0%})")
    return out


def domain_parity_errors(docs):
    """Full-catalog invariant: the domains present on disk are exactly
    ACTIVE_DOMAINS + SEEDED_INCUBATING. Called from the CLI/build, NOT from validate_schema
    (which also runs on synthetic single-domain fixtures)."""
    present = {d.get("domain") for d in docs.values()
               if isinstance(d, dict) and d.get("domain")}
    expected = ACTIVE_DOMAINS | SEEDED_INCUBATING
    if present == expected:
        return []
    return [f"domain-list parity: on-disk domains {sorted(present)} != "
            f"expected (missing {sorted(expected - present)}, "
            f"unexpected {sorted(present - expected)})"]


def validate_stability(all_codes, baseline_path):
    """Previous-release codes may never disappear or change name."""
    errors = []
    with open(baseline_path, encoding="utf-8") as fh:
        base = json.load(fh)
    base_entries = {}
    for dom in base.get("domains", {}).values():
        base_entries.update(dom.get("entries", {}))
    for code, be in base_entries.items():
        cur = all_codes.get(code)
        if cur is None:
            errors.append(f"stability: {code} existed in baseline and is GONE "
                          f"(deprecate, never delete)")
        elif cur.get("name") != be.get("name"):
            errors.append(f"stability: {code} renamed {be.get('name')!r} -> "
                          f"{cur.get('name')!r} (names are immutable)")
        elif cur.get("default_severity") != be.get("default_severity") \
                and be.get("default_severity") is not None:
            errors.append(f"stability: {code} default_severity "
                          f"{be.get('default_severity')!r} -> "
                          f"{cur.get('default_severity')!r} "
                          f"(severity is immutable post-freeze)")
    return errors


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--domains-dir", default="domains")
    ap.add_argument("--baseline", help="previous release bundle JSON for the "
                                       "stability contract")
    args = ap.parse_args(argv)
    docs = load_domains(args.domains_dir)
    if not docs:
        print(f"no domain files found under {args.domains_dir}", file=sys.stderr)
        return 1
    errors, warnings, all_codes = validate_schema(docs)
    errors += domain_parity_errors(docs)
    budget = prior_art_budget_issues(all_codes)
    if INCUBATING:
        warnings += budget
    else:
        errors += budget
    if args.baseline:
        errors += validate_stability(all_codes, args.baseline)
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    print(f"{len(all_codes)} entries across {len(docs)} domain files: "
          f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
