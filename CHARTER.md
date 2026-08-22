# OCRDb — Open Code Review Database

**Status: pre-1.0 (private).** No domain is ratified until the 1.0 release; schema and codes may change freely until then. Each domain carries a derived lifecycle stage (provisional → draft → approved → ratified) — see the canonical ladder in `RATIFICATION.md`.

## Charter

OCRDb is an open, hierarchical, severity-graded database of **code-review finding types** — everything competent review surfaces: security, correctness, architecture, tests, and maintainability/quality. It is to code review what NVD/CWE are to vulnerabilities: a shared vocabulary with stable identifiers, so findings can be named, tracked across runs and tools, trended, and discussed without re-describing them from scratch every time.

**Posture (founding principle):** *We start honestly. OCRDb offers the community a solid, evidence-grounded starting point — not the authoritative answer.* Provenance is transparent (every entry records where it came from), the tree is expected to be reshaped by use, and 1.0's publication is an invitation, not a proclamation.

**Non-goals:** OCRDb is not a scanner, not a rule engine, not a severity oracle for any specific finding instance (instance severity belongs to the reviewing tool/human; OCRDb supplies the *typical* severity and, where enriched, grading criteria). It does not compete with CWE/OWASP/CERT — it maps to them.

**The gap it fills (prior-art survey, 2026-08-10):** No existing source provides a unified, open, cross-domain, hierarchical, graded review-finding taxonomy. CWE is security-first (quality demoted to "indirect security impact" views); ISO/IEC 5055 covers only machine-countable CWE subsets; SonarSource's taxonomy is the closest modern analog but tool-bound and source-available-licensed (as is Semgrep's registry — both moved *away* from open licensing); OWASP's Code Review Guide was archived April 2025; IEEE 1044 is Inactive-Reserved; Google/Microsoft review guides classify nothing. Empirically, ~75% of real review findings are "evolvability" (Mäntylä & Lassenius, IEEE TSE 2009) — precisely the territory existing databases ignore.

**License (decided 2026-08-10):** the taxonomy content is **CC BY-SA 4.0** — attribution + share-alike, deliberately chosen over CC0 so OCRDb and its derivatives stay open, countering the source-available enclosure pattern that closed comparable taxonomies. The `tools/` are MIT. See `LICENSE`. The verbatim CC legal code is embedded there at the 1.0 public release.

## Structure & grammar

Four levels, tool-neutral names (panopticon's panels/lenses *map onto* these; nothing in OCRDb knows panopticon exists):

```
DOMAIN (3 letters)  → AREA (letter) → CATEGORY (digit) → ISSUE (letter)
SEC                 → A (authentication) → 2 (hijack)  → D (named issue)
```

- **Code:** `SEC-A2D` — domain dash area+category+issue. Compact, human-readable, sortable.
- **Issues are named defect types**, not severity slots. Within a category, issue letters are assigned in typical-severity order at seeding time (mnemonic, not semantic — the letter's meaning never changes even if severities are re-graded later).
- Each issue carries a **typical severity** (INFO/LOW/MEDIUM/HIGH/CRITICAL). Consumers may override per-instance under their own disciplines.
- **Versioned citation form** (per ASVS convention): `ocrdb-v0.1-SEC-A2D` when citing outside a pinned context.
- Domains (10 **approved** — the core catalog): `SEC` security, `COD` correctness, `ARC` architecture, `TST` testing, `QAL` quality/maintainability, `AGT` agentic-trust, `DAT` data-and-persistence (in the core catalog since 0.1–0.2); `OPS` production-readiness (retry/backoff/circuit-breaker, graceful shutdown, health checks, idempotent handlers), `ACC` accessibility (WCAG crosswalk), `LNG` language/internationalization (added to the core catalog 0.3.0).
- **Domain-roster lifecycle (canonical ladder in `RATIFICATION.md`):** domains mature through four stages — **provisional → draft → approved → ratified**. The **10 approved** domains form the core catalog; standing candidates are **draft** (`MOC` model-as-code, `CMP` compliance/governance — admitted 0.4.0, cleared round 1) and **provisional** (`FRN`, `LGL` — admitted 0.6.0). New candidate domains are admitted **only at the even-minor entry points 0.4.0 / 0.6.0 / 0.8.0**; between entry points, existing domains are strengthened and candidates calibrated. Each domain's stage is a **derived** property rolled up from the live catalog (derivation rule to be finalized), never a stored field. The roster and codes freeze **once, at 1.0 — the act of ratification**: no domain is added, renamed, or removed after 1.0 without a major version bump. (Domains grow only when the calibration corpus warrants a genuinely new top-level territory, never speculatively.)

**Single-homing (ratified):** each hazard lives in exactly one domain. Other domains may cross-reference it (`see_also:`) but never re-enter the same hazard under a second code — a duplicate home would guarantee a reconcile split for every code-as-identity consumer. Adversary-exploitable classes home in `SEC`; concurrency in `COD-F`; resource leaks in `COD` (a leak *in test code* is a distinct `TST` finding); agentic-trust in `AGT`.

**Stability contract (per CWE discipline):** codes are immutable from the 1.0 release — never reused, renamed, or re-lettered thereafter. Before 1.0 the catalog is pre-1.0 and codes may change (per the status line above); 0.x releases are held stable as a courtesy, not a contract. **The roster and the codes freeze together at 1.0 — the single act of ratification** (see the lifecycle ladder in `RATIFICATION.md`): the set of domains stops growing and every code becomes immutable at the same release. Until then the roster still admits candidate domains at the entry points **0.4.0 / 0.6.0 / 0.8.0**. Corrections after 1.0 happen by `status: deprecated` (with `superseded_by`) plus new codes. Releases are semver'd with changelogs; consumers pin a release.

## Entry schema

Lean core, forward-compatible enrichment — optional fields attach per-entry without schema breakage. The normative schema (required fields, enrichment fields, file format, severity scale, stability mechanics) lives in **`SCHEMA.md`**; domain content lives in `domains/<dom>.yml`.

## Consumers & emitting classes

Two kinds of consumers cite OCRDb codes:

- **Review pipelines** (e.g. panopticon) — grade findings against catalog slices, override typical severity per-instance under their own disclosed discipline, and map their internal panels/lenses onto OCRDb domains via a consumer-side mapping file. Nothing in OCRDb knows any consumer exists.
- **Agentic review & simplification skills** (code-simplification skills, agentic PR-review tools, reviewer subagents) — an emitting class in their own right, and a curation corpus source. Rules for this class:
  1. **Quality-only skills MUST NOT emit `SEC` or `COD` codes**, even when a quality finding brushes against a correctness or security concern. A simplification that is correctness-entangled is declined and deferred to a review pipeline's domain codes — the skill's self-fencing is the boundary.
  2. Findings from this class default to `character: opportunity` (see `SCHEMA.md`) unless the skill is explicitly running in a defect-hunting mode.
  3. Skills should be able to self-tag a finding **considered-and-declined** (with the reason), so a deliberately-not-applied change is not re-surfaced as new on every subsequent run.

