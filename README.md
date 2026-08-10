# OCRDb — Open Code Review Database

A hierarchical, severity-graded database of code-review finding types — security,
correctness, architecture, tests, and quality — with stable identifiers
(`SEC-A2D`), CWE/ISO-5055/ASVS crosswalks, and a SARIF taxonomy export.

**Status: INCUBATING.** Private while the schema and seed taxonomy form; public at 1.0.
We start honestly: OCRDb offers the community a solid, evidence-grounded starting
point — not the authoritative answer.

- `CHARTER.md` — founding principles, gap analysis, license posture
- `SCHEMA.md` — entry schema + stability contract (to be extracted from the design spec)
- `domains/` — the taxonomy content (seeding in progress)

First consumer: [panopticon](https://github.com/panopticon-scanner/panopticon) (5.0).
