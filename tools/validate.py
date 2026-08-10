#!/usr/bin/env python3
"""OCRDb domain-file validator: schema + stability contract.

Usage:
    python3 tools/validate.py [--domains-dir domains] [--baseline build/ocrdb-<prev>.json]

Exit codes: 0 = clean (warnings allowed), 1 = schema/stability errors.

Schema checks are hard errors. Cross-domain duplicate names are WARNINGS
until the single-homing rule (RATIFICATION big rock #0) is ratified —
this validator mechanizes that inventory rather than blocking on it.

The stability contract (SCHEMA.md) activates at the 0.1 release tag:
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
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEVERITIES = {"INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"}
STATUSES = {"active", "deprecated"}
CHARACTERS = {"defect", "opportunity"}


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
    for fn, doc in docs.items():
        if not isinstance(doc, dict) or "domain" not in doc:
            errors.append(f"{fn}: missing top-level 'domain'")
            continue
        dom = doc["domain"]
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
            if e.get("typical_severity") not in SEVERITIES:
                errors.append(f"{ctx}: typical_severity {e.get('typical_severity')!r} "
                              f"not in {sorted(SEVERITIES)}")
            if e.get("status") not in STATUSES:
                errors.append(f"{ctx}: status {e.get('status')!r} not in {sorted(STATUSES)}")
            prov = e.get("provenance")
            if not isinstance(prov, list) or not prov:
                errors.append(f"{ctx}: provenance must be a non-empty list")
            if e.get("status") == "deprecated" and not e.get("superseded_by"):
                errors.append(f"{ctx}: deprecated without superseded_by")
            if e.get("status") != "deprecated" and e.get("superseded_by"):
                errors.append(f"{ctx}: superseded_by on a non-deprecated entry")
            if "character" in e and e["character"] not in CHARACTERS:
                errors.append(f"{ctx}: character {e['character']!r} not in {sorted(CHARACTERS)}")
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
    # duplicate names: hard error within a domain, warning across domains
    # (the cross-domain inventory is RATIFICATION big rock #0, pre-ruling)
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
