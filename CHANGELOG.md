# Changelog

All notable changes to the OCRDb taxonomy. Codes are held stable per release but may change before 1.0 (pre-1.0); see SCHEMA.md stability contract.

## [0.4.1] - 2026-08-22

Patch release: a severity-grading refinement to one code's `criteria`, plus the domain-lifecycle vocabulary formalization. All 392 codes stay byte-identical on `name`/`default_severity` against 0.4.0 — the stability contract holds.

### Changed — catalog

- `AGT-B1A incomplete-mediation-coverage-gap` `criteria` now grade severity by the **capability of the ungated invocation class**: HIGH when that class can write, execute, or exfiltrate (an ungated Bash/Edit/Write, or any path to un-adjudicated egress); MEDIUM when the ungated class is read-only and its output is adjudicated — e.g. a review scope-fence constraining Read/Grep/Glob only, with no write/exec/egress channel — especially where the gap is disclosed. A read-only, adjudicated, disclosed coverage gap is defense-in-depth, not a directly-exploitable HIGH. `name`/`default_severity` unchanged (the default stays HIGH — the write/exec anchor case).

### Terminology — domain-lifecycle vocabulary formalized

The domain-status vocabulary is unified to the four-stage ladder **provisional → draft → approved → ratified**, now defined canonically in `RATIFICATION.md`. Earlier docs used "active / incubating / ratified" loosely — "incubating" for the whole pre-1.0 catalog, "active" for both the core roster and the per-code `status` flag, and "ratified" for the 0.1 seeding session. Those are now unified:

- The 10 core domains (SEC, COD, ARC, TST, QAL, AGT, DAT, OPS, ACC, LNG) are **approved**; the candidate domains MOC, CMP are **draft** and FRN, LGL are **provisional**.
- **No domain is ratified until 1.0** — the one-time roster-and-code stability freeze. The legacy "incubating" framing (the whole catalog being pre-1.0) is retired in favor of this precise statement.
- Domain **stage** is now described as a **derived** property rolled up from the live catalog (derivation rule to be finalized) — distinct from, and never conflated with, the per-code `status: active | deprecated` field.
- The version history was reconstructed to match the ladder, and the roster-freeze point is corrected from the previously-documented **0.5.0** to **1.0**, with candidate-domain entry points at **0.4.0 / 0.6.0 / 0.8.0**.

This is a **terminology refinement**, not a change to what was done or to any shipped catalog data: no code, `name`, `default_severity`, `status`, or entry was added, removed, or re-graded; `domains/*.yml` data and the build tooling are untouched. Prior release entries below are preserved as-is and retain their original wording. `CHARTER.md`, `SCHEMA.md`, `README.md`, and the domain-file headers now defer to `RATIFICATION.md` for the canonical ladder.

## [0.4.0] - 2026-08-18

First evidence-graded additions from a ground-truth corpus. Introduces the `proof-backed` provenance value — a finding observed against [BursarBuddy](https://github.com/psyberone/bursarbuddy), a deliberately-vulnerable app where each entry is a *planted* vulnerability with a *passing executable exploit proof*. Distinct from `corpus` (observed in real repos) and `prior-art` (a cited standard): the hazard is proven reachable. `proof-backed` entries are **proof-required** — the validator rejects one that does not carry the proof as an example. **390 → 392 codes.**

### Added
- `SEC-C1F missing-object-level-authorization` (HIGH, CWE-639/566) — object-level authorization (OWASP API1, BOLA/IDOR), the gap the catalog's *function*-level `SEC-C1C` (API5, CWE-862/285) did not cover. The two are now reciprocal `see_also` and their `criteria` split the boundary: a per-record ownership check vs a route/function guard. Proof: BursarBuddy BB-0002.
- `SEC-C2C user-enumeration-via-response-discrepancy` (MEDIUM, CWE-203/204/205) — an observable response oracle (status code, message, or timing) that classifies whether an identifier exists, independent of brute-force protection (`SEC-C2A`). Proofs: BursarBuddy BB-0003 (login) and BB-0004 (signup).
- Provenance value `proof-backed`, plus a validator rule requiring `proof-backed` entries to carry a proof example.

### Changed
- `LNG` area B renamed `plural-format` → `locale-formatting` (incubating pre-1.0 refinement — the area covers locale-aware formatting beyond pluralization). No code or entry-name changes.

Stability contract checked against `build/ocrdb-0.3.1.json`: the 390 prior codes stay byte-identical on `name`/`default_severity`.

## [0.3.1] - 2026-08-14

Criteria pass on the three domains seeded in 0.3.0. Adds a `criteria` disambiguation block — positive qualification plus nearest-neighbor exclusion, in the 0.2.x boundary-consolidation style — to the 18 `OPS`/`ACC`/`LNG` codes that lacked one, so **all 25 seeded codes now carry `criteria`**. No new codes, no renames, no severity re-grades: the 390 codes stay byte-identical on `name`/`default_severity` (stability contract checked against `build/ocrdb-0.3.0.json`, passed clean). This is the first release **built on the 4.x-hardened tooling** — atomic artifact writes, duplicate-key + display-field validation, and script-safe catalog HTML — so the shipped build reflects the corrected build/validate path.

### Changed
- `OPS`/`ACC`/`LNG` — `criteria` added to the 18 codes that lacked it (OPS-A1B, OPS-B1B, OPS-C1A, OPS-C1B, OPS-D1B; ACC-A1B, ACC-B1B, ACC-C1A, ACC-D1A, ACC-E1A, ACC-F1A; LNG-A1B, LNG-B1A, LNG-B1B, LNG-C1A, LNG-D1A, LNG-E1A, LNG-F1A), each citing the governing standard (WCAG SC / 12-Factor / SRE / i18n / Unicode) and excluding its nearest neighbor by code.

## [0.3.0] - 2026-08-14

Seeds and activates the three domains `CHARTER.md` had declared incubating since 0.1: `OPS` production-readiness, `ACC` accessibility, `LNG` language/internationalization. Source grows **365 → 390 codes (25 additions)**, all in the three new domains; no renames, no severity re-grades, no removals — the 365 pre-existing codes are byte-identical on `name`/`default_severity`. The 0.2.0 release bundle stays the frozen stability anchor; this release's stability contract was checked against 0.2.1 (`build_bundle.py --baseline build/ocrdb-0.2.1.json`) and passed clean.

### Added
- `OPS` production-readiness — 9 codes across 5 areas (external-call resilience, lifecycle/shutdown, deployment-config, resource-limits, observability): missing-timeout-on-external-call, retry-without-backoff-or-jitter, no-graceful-shutdown-drain, fake-or-noop-health-check, unvalidated-startup-configuration, unconditional-startup-side-effect, unbounded-resource-consumption, missing-pagination-or-result-cap, silent-failure-without-telemetry.
- `ACC` accessibility — 8 codes across 6 areas (semantics, keyboard, forms, live-regions, contrast, motion), WCAG-crosswalked: icon-only-control-missing-accessible-name, non-text-content-missing-alternative, non-interactive-element-used-as-control, focus-indicator-suppressed, input-missing-programmatic-label, dynamic-status-not-announced, info-conveyed-by-color-alone, motion-ignores-reduced-motion-preference.
- `LNG` language/internationalization — 8 codes across 6 areas (externalization, plural/format, grammar, key-drift, encoding, directionality): hardcoded-user-facing-string, string-assembled-outside-i18n, locale-unaware-number-date-format, naive-pluralization, translation-assembled-by-concatenation, translation-key-drift-or-missing-fallback, byte-vs-codepoint-length-confusion (`CWE-176`), missing-rtl-bidi-support.
- `SCHEMA.md` active domain set grows to **10** (`OPS`/`ACC`/`LNG` move out of "incubating, declared not yet seeded"); a new **"Domain routing for overlapping hazards"** section adds cross-domain tiebreakers: `OPS`↔`SEC` (externally/maliciously triggered failure → SEC; internal/systemic/self-inflicted → OPS), `OPS`↔`ARC` (deliberate architectural fail-open decision → ARC; runtime operational error-swallowing → OPS), `ACC` exclusive ownership of user-facing assistive-technology defects (never QAL), and `LNG`↔`DAT` (locale-aware formatting of user-facing UI text → LNG; raw data-layer encoding stays DAT).
- `CHARTER.md` updated to the 10-domain active roster; the old "Incubating (declared, not yet seeded)" clause for `OPS`/`ACC`/`LNG` is retired.
- Reciprocal cross-domain `see_also`: `OPS-A1A` ↔ `SEC-F2A` (systemic/self-inflicted timeout stall vs. externally-triggered) and `OPS-E1A` ↔ `COD-B2C` (runtime error-swallow-without-telemetry vs. the generic wrong-result home), per the new routing note.

### Deferred (→ 0.3.1)
- A `criteria` pass (positive-qualification + nearest-neighbor exclusion, per the 0.2.x boundary-consolidation style) across the newly seeded domains — only 7 of the 25 new codes carry `criteria` today; the rest currently lean on the SCHEMA routing note alone for disambiguation.
- Two candidate cross-domain `see_also` edges surfaced in planning were dropped rather than inventing a counterpart code: `ACC-A1A` has no QAL near-neighbor (QAL area F is code-convention consistency, not UI/accessibility regression), and `LNG-E1A` has no `DAT` near-neighbor (`domains/dat.yml` has no text-encoding code; its "serialization" entries are DB/ORM query serialization). Revisit if either domain gains a matching code.

## [0.2.1] - 2026-08-13

Accumulated 0.2.x refinement since 0.2.0: catalog self-consistency (Tier 0), DAT durable-file expansion (Tier 2), consumer-side disposition vocabularies (Tier 3), and boundary/criteria consolidation. Source grows 357→365 codes (8 additions, all in the Tier 2 DAT expansion); no renames, no severity re-grades. The 0.2.0 release bundle stays the frozen stability anchor.

### Changed
- Corrected the domain-file banners from the false "0.1 (RATIFIED; codes final at the 0.1 tag)" to an accurate incubating header.
- `SCHEMA.md` domain seed now lists all seven active domains (added `AGT`, `DAT`) and the incubating `OPS`/`ACC`/`LNG`.
- Promoted the R2 severity-grading rubric into `SCHEMA.md` (was only in `RATIFICATION.md`).
- Renamed the two incubating domains whose codes exceeded the three-letter domain grammar to `ACC` (accessibility) and `LNG` (language/internationalization).
- Criteria consolidation (pre-0.3.0): sharpened boundaries + reciprocal see_also across the doc-vs-code drift cluster (ARC-G/D3, QAL-C) and added a normative 'Domain routing for overlapping hazards' rule to SCHEMA.
- Sharpened the error-swallowing boundaries (SEC-F1B=security-relevant / ARC-F2G=overbroad-catch / COD-B2C=generic wrong-result home) with reciprocal see_also.
- Sharpened the assertion-efficacy family (TST-B2A/B1C/B1A/B1E, TST-G3F as residual) with grade-by-consequence criteria + reciprocal see_also.
- Sharpened the duplication/complexity boundary — ARC-A3A vs QAL-D1A (new-module-edge rule) and ARC-A1C (separable concerns) vs QAL-H1A (single-concern complexity) with reciprocal see_also.
- Added the AGT-A1A vs AGT-A1B tiebreaker — demonstrated-injection vs exposure, with an evidentiary bar and mitigation handling — plus reciprocal see_also.
- Sharpened the doc-vs-code drift boundary: reframed ARC-D3B as a documentation-vs-repository structural disagreement (routing note's ARC bullet extended to doc-vs-repo-reality; inert-staleness clarified as pointer drift) with a reciprocal ARC-D3B↔QAL-C1C cross-reference, and aligned SEC-F1B's examples with its security-relevant-only criteria.

### Added
- Two consumer-side finding-field vocabularies in SCHEMA + `tools/validate.py` — `severity_modifier` reasons (×8) and `disposition` (×4: defect/control-present/not-applicable/correct-substrate) — so instance-level severity context and the present-but-defended / correct-substrate cases have shared terms. Not enforced on catalog entries (consumer fields); clarified that `character` is entry-level and `disposition` instance-level.
- `migrations/0.1.0-to-0.2.0.md` — the committed source-of-record for the 0.1→0.2 clean-rewrite folds (previously an untracked working note), so `build/ocrdb-0.2.0-migration.json` is reproducible in any checkout.
- `build/ocrdb-0.2.0-migration.json` — machine-readable record of the 24 codes folded in the 0.1→0.2 rewrite (generated by `tools/build_migration.py`, cross-checked against the release bundle diff).
- DAT area F (durable-file-and-local-state) — 5 codes for non-RDBMS persistence (non-atomic/lost-update/destructive-rewrite file writes, unversioned format, unbounded read); plus DAT-B1E/B1F migration-safety and DAT-E1D mirror-source-divergence. Corpus-grounded from the 2026-08-11 calibration panel.
- `tools/validate.py` now enforces the prior-art budget (≤25% ungrounded-prior-art per domain) — a warning pre-1.0, a hard error at 1.0; SCHEMA wording made precise.

## 0.2.0 — 2026-08-11 (clean identity base, breaking)

A sanctioned **pre-1.0 identity-base reset**. The 0.1 release had duplicate
codes for the same hazard, dead-letter promises (`see_also` declared but never
populated), and vendor names leaked into a public taxonomy. This release fixes
all three. Per the stability contract, codes are held stable *per release* but
free to change *before* 1.0 (CHARTER, SCHEMA.md) — there are no 0.1.0
consumers yet, so the 0.1 pin promise protected no one. **381 → 357 entries**
(24 duplicate codes removed).

**Single-homing (identity):** 19 advisor-verified same-hazard clusters plus
the `TST-G3C` verbatim duplicate resolved by **clean rewrite**: each
duplicate's YAML block is deleted outright and folded into its named
survivor (distinct `examples`/`cwe`/`recurrence` merged; severity set by
the R2 bar — "exploitable now, data loss, or silently wrong at scale"). Four
of these clusters fold two duplicates into one survivor each, so the 20
cluster-groups remove **24 codes** in total. **No `status: deprecated`
tombstones** — this is a rewrite, not a deprecation. `COD-E2B` was flagged as
a same-hazard candidate but **kept and re-scoped** (its production example is
genuine, not a duplicate). Full working notes, severity-reconciliation flags,
and the CWE/recurrence fold policy live in `scratch/0.2-migration.md`
(git-ignored, not shipped); the migration table below is the shareable
summary:

| Removed code | Survivor |
|---|---|
| `COD-D2A` | `ARC-D3A` |
| `SEC-G3A` | `QAL-C1C` |
| `ARC-D3C` | `QAL-C1C` |
| `QAL-A2A` | `ARC-E1A` |
| `ARC-B1B` | `QAL-C1D` |
| `ARC-G3A` | `TST-E1B` |
| `ARC-A4B` | `QAL-E2B` |
| `QAL-D2A` | `TST-G1A` |
| `QAL-D2B` | `TST-G1B` |
| `QAL-E2A` | `TST-C3D` |
| `TST-G2B` | `TST-D2A` |
| `QAL-A1A` | `TST-C3C` |
| `ARC-A2E` | `TST-C3C` |
| `TST-G2C` | `TST-C4B` |
| `QAL-F3A` | `TST-C4B` |
| `TST-G1D` | `TST-C2A` |
| `QAL-F2C` | `TST-C2A` |
| `ARC-F2F` | `AGT-C1A` |
| `COD-B1B` | `ARC-F2C` |
| `SEC-G1A` | `COD-C1A` / `COD-C1B` (split fold) |
| `ARC-E3D` | `COD-C3B` |
| `SEC-C4A` | `SEC-C4B` |
| `COD-A1B` | `COD-F1B` |
| `TST-G3C` | `TST-C1A` |

Per-domain: `ARC` 77→70, `COD` 58→55, `QAL` 58→51, `SEC` 73→70, `TST` 80→76,
`AGT` 16 (unchanged), `DAT` 19 (unchanged).

**Disambiguation:** `criteria` (positive-qualification rule + nearest-neighbor
exclusion, naming the neighbor code in prose) added to 44 entries across the
audit's 9 confusable-boundary clusters plus the top Appendix-B priority pairs
(SEC's four high-priority pairs, the AGT-B1 authority-scope cluster, the
DAT-B1 destructive/irreversible/non-idempotent triangle, and `TST-C2B` vs
`TST-G1B`, the one surviving-pair boundary an independent advisor re-check
flagged post-rewrite). `see_also` — declared in 0.1 but never populated —
is now populated with mutual cross-references across 56 entries (48 pairs): the routing hints 0.1
promised but never delivered.

**Provenance:** normalized to a vendor-neutral controlled vocabulary of 7
active tiers — `corpus`, `tool-observed`, `gap-review`, `prior-art`,
`owasp-align`, `asvs-align`, `openssf-align` (an 8th, `cwe-align`, is defined
in the vocabulary and reserved for future crosswalk-driven additions, not yet
assigned to any entry). Commercial tool names (`coderabbit`, `copilot`),
internal run/skill identifiers (`pr945`, `skills-class`, `simplify-skill`,
`code-simplifier-agent`, `receiving-code-review-skill`), version-qualified
corpus tags (`corpus-4x`, `corpus-2.3.0`), and source-specific gap-review tags
(`deep-gap-review`, `gemini-gap-review`) are stripped — OSS project names and
named standards are retained. **Examples:** 48 examples across 27 entries
(AGT/ARC/COD/SEC), truncated at 0.1's ~110-char signature bug, repaired: 13
completed unambiguously, 35 trimmed to the last complete clause.

**Validator hardening (`tools/validate.py`):** four checks added —
`see_also`-target existence (a `see_also` pointing at a nonexistent code is
now a hard error), duplicate-domain declaration, `automated_by` shape
(`tool:rule-id` pattern), and provenance-controlled-vocabulary membership.

**Schema (breaking):** field `typical_severity` → `default_severity`. Freezes
at 1.0 per the governance change below.

**Governance:** the stability freeze is now stated as activating at **1.0**,
not at each 0.x tag (CHARTER.md, SCHEMA.md) — 0.x releases are held stable as
a courtesy, not a contract, which is what licenses this release to change
codes at all. A `CHARTER.md` concurrency-domain drift (`COD-G` in the
single-homing prose vs the ratified `COD-F`) was fixed. The 0.1.0 changelog
entry's false "+ `see_also` cross-refs" credit — `see_also` was declared in
0.1 but never actually populated — was removed retroactively.

**Gate A (domain-unpinned re-run):** with duplicates removed and `criteria`
present, a 100-finding recurrence-weighted, domain-stratified re-run measured
**85% full-code / 86% category** 3-way advisor agreement (89% / 90%
pairwise), **zero duplicate-driven splits** (the "same hazard under two
codes" wobble that drove 0.1's residual disagreement is gone) and **zero
hallucinated codes** across 300 assignments, on the harder unpinned task (full
357-code menu, not a pinned domain). Below the pinned 0.1 baseline (91% / 94%)
by construction — unpinned assignment is a harder task — but validates the
single-homing rewrite. Full method, per-domain breakdown, and the 15
remaining near-boundary disagreements (mostly ARC/COD/QAL contract-drift; DAT
uncovered, its examples having been re-homed in Task 3-4): see
`reviews/2026-08-11-gate-a-unpinned.md`.

## 0.1.0 — 2026-08-10 (first ratified release, private incubation)

The seeding round: 320 mined draft entries walked in an owner ratification session, restructured per the rulings below, and re-lettered by typical severity into final codes. **381 entries across 7 domains.** Codes are held stable per release but may change before 1.0 (incubating).

**Domains:** `SEC` security (73), `COD` correctness (58), `ARC` architecture (77), `TST` testing (80), `QAL` quality/maintainability (58), **`AGT` agentic-trust (16, new)**, **`DAT` data-and-persistence (19, new)**. Declared incubating (no codes yet): `OPS`, `ACC`, `LNG`.

**Ratification rulings applied:**
- **Single-homing (big rock #0):** verified cross-domain duplicates collapsed to one home each. Adversary-exploitable `COD-E1*` dissolved into `SEC`; thread-safety unified into the new `COD-F`; resource leaks single-homed in `COD` (test-code leak survives distinctly in `TST`).
- **`AGT` promoted** from `SEC-G` to its own domain (prompt-injection, tool/permission scoping, output-trust, autonomy/oversight, cost-safety, data-egress) — includes two corpus incidents `SEC` couldn't express (agent-confabulated-action, secret-materialized-into-agent-output).
- **`DAT` domain added** — the `database` review panel finally has a vocabulary (schema, migrations, query-patterns, transactions, data-lifecycle); `n-plus-one` moved here from `QAL`.
- **`ARC-H` test-suite-architecture migrated into `TST`** as area G.
- **`COD-F` concurrency + `COD-G` data-representation-and-time** added (corpus-blind territories).
- **Gap entries adopted** (crosswalk-backed, ~19% prior-art, under the 25% ceiling): `SEC-I` web-session-and-browser-boundary (CSRF/session/JWT/CORS/ReDoS), `SEC` privacy category (PII-in-logs), weak-standard-crypto, abandoned-dependency, `QAL-I` observability, `TST` flakiness (unseeded-randomness, wall-clock, test-order-coupling).
- **`character: defect|opportunity`** field adopted (absent = defect; dead-code = defect). **`automated_by`** field adopted (linter-rule mapping → consumer skip-rule). **`see_also`** cross-reference field adopted.
- **Severity calibration:** `missing-referenced-file` and `hardcoded-absolute-path-in-source` re-graded CRITICAL → HIGH (single-incident inflation, not universal-CRITICAL).

**License (decided 2026-08-10):** CC BY-SA 4.0 (content) + MIT (tools) — see LICENSE. Post-ratification: re-run Gate A domain-unpinned now that single-homing is resolved (measures cross-domain assignment stability the pinned eval couldn't).
