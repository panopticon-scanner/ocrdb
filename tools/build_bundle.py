#!/usr/bin/env python3
"""OCRDb release-bundle builder.

Usage:
    python3 tools/build_bundle.py --version 0.1.0 [--domains-dir domains] [--out build]

Validates first (schema errors abort the build), then emits three
deterministic artifacts (byte-identical across runs — no timestamps):

    build/ocrdb-<ver>.json          full bundle (consumers vendor + pin this)
    build/ocrdb-<ver>.sarif.json    SARIF 2.1.0 toolComponent taxonomy export
    build/ocrdb-<ver>-menus.md      Gate C menu form: one line per entry,
                                    `CODE name (SEV)` under area/category
                                    headers — what reviewer prompts embed

Severity -> SARIF defaultConfiguration.level: CRITICAL/HIGH -> error,
MEDIUM -> warning, LOW/INFO -> note.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate as validate_mod  # noqa: E402

SARIF_LEVEL = {"CRITICAL": "error", "HIGH": "error", "MEDIUM": "warning",
               "LOW": "note", "INFO": "note"}


def build_bundle(docs, version):
    domains = {}
    for doc in docs.values():
        dom = doc["domain"]
        domains[dom] = {
            "name": doc.get("name"),
            "areas": doc.get("areas") or {},
            "entries": dict(sorted((doc.get("entries") or {}).items())),
        }
    return {"$schema": "ocrdb-bundle",
            "schema_version": "1.0",
            "version": version,
            "license": "CC BY-SA 4.0",
            "domains": dict(sorted(domains.items()))}


def build_sarif(bundle):
    taxa = []
    for dom in bundle["domains"].values():
        for code, e in dom["entries"].items():
            taxon = {
                "id": code,
                "name": e["name"],
                "shortDescription": {"text": e["name"].replace("-", " ")},
                "defaultConfiguration": {
                    "level": SARIF_LEVEL[e["default_severity"]]},
            }
            if e.get("definition"):
                taxon["fullDescription"] = {"text": e["definition"]}
            if e.get("status") == "deprecated":
                taxon["properties"] = {"deprecated": True,
                                       "supersededBy": e.get("superseded_by")}
            taxa.append(taxon)
    return {
        "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/"
                   "master/Schemata/sarif-schema-2.1.0.json",
        "version": "2.1.0",
        "runs": [{
            "tool": {"driver": {"name": "ocrdb-export",
                                "version": bundle["version"]}},
            "taxonomies": [{
                "name": "OCRDb",
                "version": bundle["version"],
                "informationUri": "https://github.com/panopticon-scanner/ocrdb",
                "organization": "OCRDb",
                "shortDescription": {"text": "Open Code Review Database"},
                "taxa": taxa,
            }],
            "results": [],
        }],
    }


def build_menus(bundle):
    lines = ["# OCRDb menus — Gate C form (generated; do not edit)",
             f"Version: {bundle['version']}", ""]
    for dom_code, dom in bundle["domains"].items():
        lines.append(f"# MENU {dom_code} ({dom['name']})")
        for ak in sorted(dom["areas"]):
            a = dom["areas"][ak]
            lines.append(f"## {dom_code}-{ak} {a['name']}")
            for ck in sorted(a.get("categories") or {}):
                lines.append(f"### {dom_code}-{ak}{ck} {a['categories'][ck]}")
                for code, e in dom["entries"].items():
                    if code.startswith(f"{dom_code}-{ak}{ck}") \
                            and e.get("status") == "active":
                        lines.append(f"{code} {e['name']} ({e['default_severity']})")
        lines.append("")
    return "\n".join(lines) + "\n"


def _atomic_write(path, text):
    """Write `text` to `path` atomically: a temp file in the same directory
    then os.replace, so an interrupted build (OOM, timeout, Ctrl-C, ENOSPC)
    never leaves a truncated, half-written artifact at a published, vendored
    path (DB-002)."""
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(text)
    os.replace(tmp, path)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", required=True)
    ap.add_argument("--domains-dir", default="domains")
    ap.add_argument("--out", default="build")
    ap.add_argument("--baseline", help="previous release bundle for the "
                                       "stability contract")
    args = ap.parse_args(argv)

    docs = validate_mod.load_domains(args.domains_dir)
    errors, warnings, all_codes = validate_mod.validate_schema(docs)
    errors += validate_mod.domain_parity_errors(docs)
    if args.baseline:
        errors += validate_mod.validate_stability(all_codes, args.baseline)
    for w in warnings:
        print(f"WARN: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        print("build aborted: validation failed", file=sys.stderr)
        return 1

    bundle = build_bundle(docs, args.version)
    os.makedirs(args.out, exist_ok=True)
    paths = {
        "bundle": os.path.join(args.out, f"ocrdb-{args.version}.json"),
        "sarif": os.path.join(args.out, f"ocrdb-{args.version}.sarif.json"),
        "menus": os.path.join(args.out, f"ocrdb-{args.version}-menus.md"),
    }
    _atomic_write(paths["bundle"],
                  json.dumps(bundle, indent=2, sort_keys=True) + "\n")
    _atomic_write(paths["sarif"],
                  json.dumps(build_sarif(bundle), indent=2, sort_keys=True) + "\n")
    _atomic_write(paths["menus"], build_menus(bundle))
    n = sum(len(d["entries"]) for d in bundle["domains"].values())
    print(f"built {n} entries -> {', '.join(sorted(paths.values()))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
