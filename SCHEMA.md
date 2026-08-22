# OCRDb Schema — Normative

**Status:** Normative — pre-1.0. No domain is ratified until 1.0; the stability contract below **activates at the 1.0 release**; until then, codes may be renamed, split, merged, and re-lettered freely. Domain lifecycle stages (provisional → draft → approved → ratified) are defined canonically in `RATIFICATION.md`.

## Code grammar

```
DOMAIN (3 letters) - AREA (letter) CATEGORY (digit) ISSUE (letter)
SEC-A2D
```

- **Domain** — 3-letter, tool-neutral. Active set: the 10 **approved** core domains — `SEC` security, `COD` correctness, `ARC` architecture, `TST` testing, `QAL` quality/maintainability, `AGT` agentic, `DAT` data, `OPS` production-readiness, `ACC` accessibility, `LNG` language/internationalization. Candidate domains are admitted only at the entry points 0.4.0 / 0.6.0 / 0.8.0 (`MOC`/`CMP` entered 0.4.0 as draft, `FRN`/`LGL` 0.6.0 as provisional) and the roster freezes once at 1.0 — see the domain-lifecycle ladder in `RATIFICATION.md`.
- **Area** — a letter (`A`–`Z`) naming a coherent territory within the domain.
- **Category** — a digit (`1`–`9`) within the area.
- **Issue** — a letter naming a **distinct defect type** (not a severity slot). At seeding time, issue letters within a category are assigned in typical-severity order (a mnemonic aid only — the letter's meaning never changes even if severities are later re-graded).
- **Versioned citation form** (outside a pinned context): `ocrdb-v0.1-SEC-A2D`.
- **Domain fallback code**: `<DOM>-X0X` — used by consumers when no specific issue fits. It is a **reserved non-entry form** that deliberately sits OUTSIDE the entry grammar above (`0` is a reserved category digit, `X` a reserved area/issue letter), so a real entry code and the sentinel can never collide. Fallback usage is the catalog-gap signal that feeds curation; `X0X` is never assigned to a real entry. Every declared domain has a fallback, e.g. `SEC-X0X`, `OPS-X0X`.

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
    default_severity: HIGH            # INFO | LOW | MEDIUM | HIGH | CRITICAL
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

`character` is an **entry-level** default (the finding-*type*'s nature); it is distinct from a finding's **instance-level** `disposition` (see *Finding disposition vocabulary*), which a consumer sets per finding. A `character: defect` type can still have a `disposition: control-present` instance.

## Severity scale

`INFO < LOW < MEDIUM < HIGH < CRITICAL`. `default_severity` is the *typical* grade for the defect type — never a per-instance verdict. Consumers may override per instance under their own disclosed discipline (panopticon: `severity_override {from, to, reason}`, advisor-checked). Trend lines anchor to the catalog default so overrides never bend history.

**Normative grading rule (R2 bar):** grade `default_severity` against a single bar — *exploitable now, data loss, or silently wrong results at scale*. CRITICAL/HIGH are reserved for hazards meeting the bar; a hazard that is real but does not (dead config, style/metadata drift, hygiene) grades MEDIUM or below. Severity is a property of the defect type, never the instance.

## Stability contract (activates at 1.0)

Per CWE discipline:

1. **Codes are immutable from the 1.0 release** — never reused, renamed, or re-lettered thereafter. Before 1.0 the catalog is pre-1.0 and codes may change (per CHARTER); 0.x releases are held stable as a courtesy, not a contract.
2. Corrections happen by `status: deprecated` + `superseded_by` + a new code.
3. Releases are semver'd with changelogs; consumers pin a release (`build/ocrdb-<ver>.json`).
4. `tools/validate.py` enforces this mechanically against the previous release bundle: a code that disappears or changes `name` fails the build.

## Two axes — domain stage vs. code status

OCRDb tracks two independent maturity properties; do not conflate them.

- **Code status** — the per-entry `status: active | deprecated` field above. It is the inclusion / stability flag the build reads: `tools/build_bundle.py` filters on `status == "active"`, and `superseded_by` is required when `status: deprecated`. It is a property of a single **code**.
- **Domain stage** — `provisional | draft | approved | ratified`, a property of a whole **domain**. It is **derived** (rolled up from the live catalog), not a stored field: there is no `stage:` or `maturity:` key in the YAML, and the roll-up **derivation rule is to be finalized**. The 10 domains in the active set above are **approved**; provisional and draft candidates are calibration skeletons outside `domains/*.yml`; `ratified` is the 1.0 stability-locked state — **no domain is ratified pre-1.0**.

The four-stage ladder, the version history, the promotion gates, and the 0.4.0 / 0.6.0 / 0.8.0 entry-point cadence are defined canonically in `RATIFICATION.md`; this schema documents only the per-code `status` field and the fact that domain `stage` is derived.

## Provenance vocabulary

`provenance` is a non-empty list drawn from a controlled, vendor-neutral vocabulary. Every entry's evidence tier is one of:

- `corpus` — the hazard was observed in a real code-review corpus (panopticon's self-scan / PR-review runs).
- `tool-observed` — surfaced by automated review tooling or review skills. Deliberately vendor-neutral: the taxonomy is a public, CC-BY-SA-licensed catalog and does not name specific commercial tools or internal run/skill identifiers as provenance values.
- `gap-review` — added by a systematic gap-analysis pass over the taxonomy (e.g. filling a missing precursor/exploited-form pairing).
- `prior-art` — completed from an external taxonomy/standard to fill an obvious asymmetry (e.g. the exploited form of a defect whose precursor was observed). Budget-capped: entries grounded ONLY by prior-art (provenance carries `prior-art` and neither `corpus` nor `tool-observed`) must be ≤ 25% of a domain's entries. An entry that later gains a real corpus/tool observation no longer counts against the cap. `tools/validate.py` enforces this — a WARNING while the catalog is pre-1.0, a hard error at 1.0.
- `owasp-align` / `asvs-align` / `openssf-align` / `cwe-align` — crosswalk alignment to a named open standard (OWASP Top 10, OWASP ASVS, OpenSSF, CWE respectively). `cwe-align` is reserved for future crosswalk-driven additions.

No other values are permitted. This is a pre-1.0 breaking change from the 0.1 vocabulary, which leaked vendor names (`coderabbit`, `copilot`), internal run/skill identifiers (`pr945`, `skills-class`, `simplify-skill`, `code-simplifier-agent`, `receiving-code-review-skill`), version-qualified corpus tags (`corpus-4x`, `corpus-2.3.0`), and source-specific gap-review tags (`deep-gap-review`, `gemini-gap-review`) into the public catalog; all of these now collapse to the neutral tiers above.

## Severity-modifier vocabulary

`severity_modifier` is a **consumer finding-field**, not an entry field: OCRDb defines the controlled reasons; a consumer records them per instance under its own disclosed discipline (panopticon: `severity_override {from, to, reason}`, advisor-checked). A modifier records the contextual reason an instance's grade departs from the entry's `default_severity`; it never mutates the catalog default, and trend lines still anchor to that default. The controlled set:

- `test-or-fixture-scope` — the finding is in test, fixture, or example code, not a production path.
- `operator-controlled-input` — the untrusted-input assumption does not hold; the input is operator-, CLI-, env-, or first-party-controlled, not attacker-reachable.
- `local-or-offline-context` — the deployment is LAN, desktop, single-user, or offline, not internet-facing.
- `regenerable-or-recoverable-data` — the affected data or artifact is regenerable (a cache, a derived file), so loss is recoverable.
- `dev-or-ci-tooling` — the artifact is development or CI tooling, not a shipped release artifact.
- `intentionally-public-value` — the value flagged as secret is public by design (an analytics ingest key, an OAuth public client id).
- `documented-accepted-risk` — the hazard is a documented, deliberate trade-off (an acknowledged benign race, a ruled architectural decision).
- `compensating-control-present` — a compensating control reduces the instance's impact (see disposition `control-present`).

## Finding disposition vocabulary

`disposition` is a **consumer finding-field**, not an entry field: it records a specific finding's state relative to the hazard, so a hardened codebase can be credited rather than read as mere absence of findings. It is set per instance by the consumer. The controlled set:

- `defect` — the hazard is present and undefended; the default a finding records.
- `control-present` — the hazard's code path exists but a compensating or mitigating control is in place (out-of-band integrity, SameSite, sandbox/attestation, fencing tokens, a protocol-mandated constraint).
- `not-applicable` — the hazard cannot arise here: a framework default handles it, the architecture precludes it, or the domain does not apply to the target (e.g. `AGT` on a non-agentic codebase).
- `correct-substrate` — the code demonstrates the correct handling of a hazard its code-family is prone to — a positive finding (a "bounded substrate", e.g. a money path that never uses float).

## Instance-disposition rules

- **Both vocabularies are consumer-applied.** OCRDb defines the terms and their meaning; it does not prescribe *when* a consumer assigns them (that is the consumer's disclosed, advisor-checked discipline), and it records no instance state.
- **`character` vs `disposition`.** `character` is **entry-level** — the finding-type's default nature (`defect | opportunity`). `disposition` is **instance-level** — a consumer's judgment about a specific finding. They are orthogonal: a `character: defect` type can have a `disposition: control-present` instance.
- **Neither changes `default_severity` or trends.** Severity is a property of the type; a `severity_modifier`-justified override is the consumer's per-instance verdict; trends anchor to the catalog default.
- **`control-present`, `not-applicable`, and `correct-substrate` are not gate-eligible defects** — they are informational or positive; consumers route them out of the fix queue.

## Domain routing for overlapping hazards

When one observation could be cited under more than one domain, route by *what the finding is about*, not by its phrasing:

- **An instance that breaks a contract or produces a wrong result → the correctness/behavioral home** (COD, or the domain that owns the specific hazard).
- **Two specifications that disagree with each other** — code vs. code, doc vs. doc, schema vs. producer, or documentation vs. the repository's actual structure — **→ the architecture home (ARC).**
- **Inert staleness** — a reference, path, or version out of date but breaking nothing (a drifted pointer, not a structural absence) — **→ the quality/maintainability home (QAL).**

When a hazard could plausibly home in two domains, route by:
- **OPS ↔ SEC** — an externally/maliciously triggered failure homes in SEC; an internal or systemic threshold / self-inflicted failure homes in OPS.
- **OPS ↔ ARC** — a deliberate architectural fail-open *decision* homes in ARC; runtime operational error-swallowing homes in OPS.
- **ACC ownership** — ACC exclusively owns user-facing assistive-technology defects; a UI-regression that is an AT defect routes to ACC, not QAL.
- **LNG ↔ DAT** — LNG owns locale-aware sorting/encoding of user-facing UI text; raw data-layer encoding stays DAT.

An entry's `criteria` may reference this principle to disambiguate a near-neighbour in another domain.
