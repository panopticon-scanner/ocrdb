#!/usr/bin/env python3
"""Generate build/ocrdb-<to>-migration.json — the machine-readable record of
codes removed/folded in a clean-rewrite release transition.

Usage:
    python3 tools/build_migration.py \
        --source migrations/0.1.0-to-0.2.0.md \
        --from build/ocrdb-0.1.0.json --to build/ocrdb-0.2.0.json \
        --from-version 0.1.0 --to-version 0.2.0 \
        --out build/ocrdb-0.2.0-migration.json

The authoritative set of removed codes is the bundle diff (codes in --from
absent from --to). Each survivor/note comes from the removals table in
--source. The two sets are cross-checked: any code in one but not the other
is a hard error, so a parse drift or a stale source fails loudly.
"""
import argparse
import json
import re
import sys

CODE_TOKEN = re.compile(r"[A-Z]{3}-[A-Z][1-9][A-Z]")


def bundle_codes(path):
    with open(path, encoding="utf-8") as fh:
        b = json.load(fh)
    return {c for dom in b.get("domains", {}).values()
            for c in (dom.get("entries") or {})}


def parse_removals(source_path):
    """Parse the removals table -> {old_code: {"survivors": [...], "note": str}}.

    A data row is `| # | removed_code | survivor | folded... | ... | ... |`.
    Rows whose removed_code cell says 'stays' or 'kept' are annotations
    (e.g. TST-C2B stays, COD-E2B kept) — skipped, not removals.
    """
    out = {}
    with open(source_path, encoding="utf-8") as fh:
        for line in fh:
            if not line.lstrip().startswith("|"):
                continue
            # Split on unescaped pipes only, then unescape \| inside cells, so
            # a literal pipe in a note/survivor cell (GFM-escaped as \|) can no
            # longer shift columns and misassign survivor/note data (DB-003).
            raw = line.strip().strip("|")
            cells = [c.strip().replace("\\|", "|")
                     for c in re.split(r"(?<!\\)\|", raw)]
            if len(cells) < 4:
                continue
            num, removed_cell, survivor_cell, note_cell = cells[:4]
            if num in ("#", "") or set(num) <= {"-", ":"}:
                continue  # header / separator row
            low = removed_cell.lower()
            if "stays" in low or "kept" in low:
                continue  # annotation row, not a removal
            m = CODE_TOKEN.search(removed_cell)
            if not m:
                continue
            out[m.group(0)] = {
                "survivors": CODE_TOKEN.findall(
                    survivor_cell.split("see_also")[0]),
                "note": re.sub(r"\*\*", "", note_cell).strip(),
            }
    return out


def build_migration(source_path, from_path, to_path, from_ver, to_ver):
    removed = bundle_codes(from_path) - bundle_codes(to_path)
    to_codes = bundle_codes(to_path)
    parsed = parse_removals(source_path)

    if set(parsed) != removed:
        raise SystemExit(
            "migration cross-check FAILED: "
            f"in-diff-not-source {sorted(removed - set(parsed))}; "
            f"in-source-not-diff {sorted(set(parsed) - removed)}")

    mappings = []
    for old_code in sorted(removed):
        survivors = parsed[old_code]["survivors"]
        for s in survivors:
            if s not in to_codes:
                raise SystemExit(
                    f"migration: survivor {s} of {old_code} is not a real "
                    f"{to_ver} code")
        mappings.append({
            "old_code": old_code,
            "disposition": "folded" if survivors else "removed",
            "survivors": survivors,
            "note": parsed[old_code]["note"],
        })
    return {"schema_version": "1.0", "from_version": from_ver,
            "to_version": to_ver, "mechanism": "clean-rewrite",
            "mappings": mappings}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--from", dest="from_path", required=True)
    ap.add_argument("--to", dest="to_path", required=True)
    ap.add_argument("--from-version", default="0.1.0")
    ap.add_argument("--to-version", default="0.2.0")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    migration = build_migration(args.source, args.from_path, args.to_path,
                                args.from_version, args.to_version)
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(migration, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print(f"wrote {args.out}: {len(migration['mappings'])} mappings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
