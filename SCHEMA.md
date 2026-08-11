# OCRDb Schema — Normative

**Status:** Draft 0.1 (pre-ratification). The stability contract below **activates at the 1.0 release**; until then, ratification may rename, split, merge, and re-letter freely.

## Code grammar

```
DOMAIN (3 letters) - AREA (letter) CATEGORY (digit) ISSUE (letter)
SEC-A2D
```

- **Domain** — 3-letter, tool-neutral. Seed set: `SEC` security, `COD` correctness, `ARC` architecture, `TST` testing, `QAL` quality/maintainability. Domains are a starting set, not a cap.
- **Area** — a letter (`A`–`Z`) naming a coherent territory within the domain.
- **Category** — a digit (`1`–`9`) within the area.
- **Issue** — a letter naming a **distinct defect type** (not a severity slot). At seeding time, issue letters within a category are assigned in typical-severity order (a mnemonic aid only — the letter's meaning never changes even if severities are later re-graded).
- **Versioned citation form** (outside a pinned context): `ocrdb-v0.1-SEC-A2D`.
- **Domain fallback code**: `<DOM>-X0X` — used by consumers when no specific issue fits. Fallback usage is the catalog-gap signal that feeds curation; `X` is reserved in all three positions and never assigned to real entries.

## Entry schema

Each domain lives in `domains/<dom>.yml`:

```yaml
domain: SEC
name: security
areas:                       # hierarchy naming — areas and categories carry names only
  A:
    name: injection-and-unsafe-execution
    categories:
      1: command-execution
entries:                     # one entry per issue code
  SEC-A1B:
    # ---- required core ----
    name: os-command-injection        # kebab-case, stable once released
    typical_severity: HIGH            # INFO | LOW | MEDIUM | HIGH | CRITICAL
    status: active                    # active | deprecated
    provenance: [corpus]              # where this entry came from — see "Provenance vocabulary" below
    # ---- optional enrichment (any subset, added when needed) ----
    recurrence: 17                    # corpus recurrence count at seeding (importance weight)
    character: defect                 # defect | opportunity (absent = defect)
    definition: "…"                   # one paragraph
    criteria: "qualifies when …; elevate if …"
    superseded_by: SEC-A3B            # required iff status: deprecated
    cwe: [CWE-78]
    iso5055_measure: [security]
    iso25010: [security.integrity]
    odc: {type: checking, trigger: logic-flow}
    owasp: {top10_2025: A03, asvs: [v5.0.0-3.2.1]}
    cert_rule: []
    sonar_rule: []                    # S-ids; mapping only, no content reuse
    codeql: {tags: [security/cwe/cwe-078]}
    semgrep: {category: security}
    mantyla_class: functional         # functional | evolvability
    automated_by: [ruff:E401]         # linter/formatter rule that catches it mechanically;
                                      #   absent/empty = requires human/agent judgment
    see_also: [COD-A1B]               # cross-references to the single home of a related hazard
    examples: ["…"]                   # illustrative finding titles (bad), and/or {bad: …, good: …}
    remediation: "…"
    notes: "…"                        # curation notes, contested classifications
```

### `automated_by` (0.1)

Names the linter/formatter rule that would catch the issue mechanically (e.g. `ruff:E401` for combined-imports). A consumer whose deterministic tool scan ran can instruct reviewers to SKIP `automated_by` entries and disclose the suppression class — the taxonomy encodes *why* a machine-catchable finding is absent, so reviewer-model budget isn't spent re-finding free lints. Empty/absent means the issue needs judgment.

### `see_also` (0.1)

Cross-references the single home of a related hazard (per the single-homing rule in the charter). A `COD` leak entry may `see_also` the `TST` test-code-leak variant; a domain that declines a hazard points at the domain that owns it. `see_also` never creates a second identity for the same hazard — it is a pointer, not a duplicate.

### `character` (from the agentic-skills survey)

The same underlying pattern (duplication, dead code, missing abstraction) is classified as a **defect** by one emitting source and an **opportunity** by another, depending on where in the lifecycle it is caught. `character` carries that distinction on a single issue type without forking the taxonomy:

- `defect` (default when absent) — the entry names something wrong.
- `opportunity` — the entry names an improvement a reviewer/skill may propose; instance severity still applies, but consumers may route these to a different workflow (refactor queue vs. fix queue).

Emitting skills default to `character: opportunity` unless explicitly running in a defect-hunting mode. Where sources disagree (e.g. dead code: YAGNI-defect vs. refactor-opportunity), the entry's `notes` records the contest and ratification picks the default.

## Severity scale

`INFO < LOW < MEDIUM < HIGH < CRITICAL`. `typical_severity` is the *typical* grade for the defect type — never a per-instance verdict. Consumers may override per instance under their own disclosed discipline (panopticon: `severity_override {from, to, reason}`, advisor-checked). Trend lines anchor to the catalog default so overrides never bend history.

## Stability contract (activates at 1.0)

Per CWE discipline:

1. **Codes are immutable from the 1.0 release** — never reused, renamed, or re-lettered thereafter. Before 1.0 the catalog is incubating and codes may change (per CHARTER); 0.x releases are held stable as a courtesy, not a contract.
2. Corrections happen by `status: deprecated` + `superseded_by` + a new code.
3. Releases are semver'd with changelogs; consumers pin a release (`build/ocrdb-<ver>.json`).
4. `tools/validate.py` enforces this mechanically against the previous release bundle: a code that disappears or changes `name` fails the build.

## Provenance vocabulary

`provenance` is a non-empty list drawn from a controlled, vendor-neutral vocabulary. Every entry's evidence tier is one of:

- `corpus` — the hazard was observed in a real code-review corpus (panopticon's self-scan / PR-review runs).
- `tool-observed` — surfaced by automated review tooling or review skills. Deliberately vendor-neutral: the taxonomy is a public, CC-BY-SA-licensed catalog and does not name specific commercial tools or internal run/skill identifiers as provenance values.
- `gap-review` — added by a systematic gap-analysis pass over the taxonomy (e.g. filling a missing precursor/exploited-form pairing).
- `prior-art` — completed from an external taxonomy/standard to fill an obvious asymmetry (e.g. the exploited form of a defect whose precursor was observed). Budget-capped: ≤ 25% of entries per domain.
- `owasp-align` / `asvs-align` / `openssf-align` / `cwe-align` — crosswalk alignment to a named open standard (OWASP Top 10, OWASP ASVS, OpenSSF, CWE respectively). `cwe-align` is reserved for future crosswalk-driven additions.

No other values are permitted. This is a pre-1.0 breaking change from the 0.1 vocabulary, which leaked vendor names (`coderabbit`, `copilot`), internal run/skill identifiers (`pr945`, `skills-class`, `simplify-skill`, `code-simplifier-agent`, `receiving-code-review-skill`), version-qualified corpus tags (`corpus-4x`, `corpus-2.3.0`), and source-specific gap-review tags (`deep-gap-review`, `gemini-gap-review`) into the public catalog; all of these now collapse to the neutral tiers above.
