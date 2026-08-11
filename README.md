# OCRDb — Open Code Review Database

A hierarchical, severity-graded database of code-review finding types — security,
correctness, architecture, tests, and quality — with stable identifiers
(`SEC-A2D`), CWE/ISO-5055/ASVS crosswalks, and a SARIF taxonomy export.

**Status: INCUBATING.** Private while the schema and seed taxonomy form; public at 1.0.
We start honestly: OCRDb offers the community a solid, evidence-grounded starting
point — not the authoritative answer.

## Browse the catalog

- **[`CATALOG.md`](CATALOG.md)** — the whole tree, rendered by GitHub. Browse in-repo, no tooling.
- **`build/ocrdb-<ver>.html`** — a self-contained, searchable/filterable page. Open it locally; drops into a static site or GitHub Pages later, unchanged.

Both are generated from `domains/` by `tools/build_catalog.py` (run at each release) — they never drift from the source.

## Repository layout

- `CHARTER.md` — founding principles, gap analysis, license posture
- `SCHEMA.md` — entry schema + stability contract (normative)
- `domains/` — the taxonomy content (source of truth)
- `build/` — generated per release: JSON bundle, SARIF taxonomy export, Gate C menus, catalog HTML
- `tools/` — `validate.py`, `build_bundle.py`, `build_catalog.py` (Python 3 stdlib + PyYAML)

First consumer: [panopticon](https://github.com/panopticon-scanner/panopticon) (5.0).
