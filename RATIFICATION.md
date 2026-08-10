# OCRDb 0.1 — Ratification Agenda

**Status:** Awaiting the owner's ratification session. Nothing in `domains/` is stable until this document's questions are ruled on and the 0.1 tag is cut.

**How the session works** (per the charter's seeding methodology): walk each domain tree — rename / split / merge / re-letter freely, adjust typical severities, rule on the structural questions below. Agents proposed; nothing ships unratified. Rulings can be recorded directly as PR review comments or as edits to the domain files.

## Draft inventory

| Domain | Areas | Entries | Source |
|---|---|---|---|
| SEC | 8 | 65 | corpus (194 deduped types) + 2 prior-art |
| COD | 6 | 44 | corpus (117 deduped types) |
| ARC | 8 | 96 | corpus (181 deduped types) + 2 skills-class |
| TST | 6 | 59 | corpus (250 deduped types) |
| QAL | 6→8 | 56 | corpus (132 deduped types) + 13 skills-class |
| **Total** | | **320** | 1,428 raw findings → 874 deduped types → 6 parallel miners |

Every corpus title landed in an entry's `examples`, in `unplaced`, or in a routing flag — nothing was dropped silently.

## Big rocks — structural rulings needed

1. **SEC-G (ai-agent-trust-boundary): keep in SEC, or spin up a dedicated agentic/LLM domain?** ~20 corpus items (prompt injection, self-asserted trust metadata, single-verifier override authority) recur heavily in agentic-review corpora and map to OWASP LLM Top 10 territory. Draft keeps them in SEC; a future `AGT` domain is the alternative.
2. **SEC-H (security-tooling-and-scan-integrity): SEC, or a meta/process domain?** Heavily represented because this corpus is panopticon reviewing itself; may not generalize. Draft keeps it in SEC with a note.
3. **ARC-H (test-suite-architecture) vs TST.** The ARC miner itself recommended migrating Area H to TST. Draft keeps ARC-H intact; the overlap map: ARC-H1A↔TST-C2B, ARC-H1B/H2C↔TST-C2A, ARC-H2D↔TST-C4A, ARC-H2E↔TST-D2A, ARC-H2F↔TST-C5B, ARC-H3A↔TST-B1B, ARC-H3C↔TST-C1B. Options: (a) migrate ARC-H into TST and re-letter, (b) keep both with cross-references (structural/organizational angle in ARC, per-test quality in TST), (c) draft's default — decide per-pair.
4. **TST "silent non-verification" siblings.** TST-F1C, TST-F1D, TST-A4A, TST-A3C all describe "a test exists but a gate prevents its assertions from running" via different mechanisms. Keep the four distinct mechanisms (draft) or merge into one coarser issue?
5. **QAL areas G (efficiency) and H (complexity-and-simplification)** are new, from the skills-class survey (13 entries folded into QAL total). Confirm placement — the survey suggested `needless-abstraction` might belong in ARC instead; the draft groups the whole simplification cluster in QAL-H for cohesion.
6. **ARC-A5 (canonical-ownership, "altitude")** — the skills survey's strongest novel concept: not "is this logic copied" but "does a constant/regex/derived-value have exactly one canonical owning module, with everyone else aliasing it" (SEV_ORDER, PANELS, AGENT_NAME evidence). Draft: new ARC category A5 beside A3 (duplication). Alternative: merge into A3.
7. **`character: defect|opportunity` field** — adopted in SCHEMA.md as optional enrichment (absent = defect). Ratify the concept and the contested default on `dead-code-unused-function` (QAL-E3A: YAGNI-defect per receiving-code-review vs. refactor-opportunity per TDD/simplify).
8. **Consumer-class charter rule** — quality-only skills MUST NOT emit SEC/COD codes even when a finding brushes against one (added to CHARTER.md §Consumers; the /simplify PR #945 evidence). Includes the "considered-and-declined" self-tag concept so a declined non-fix isn't re-surfaced every run.
9. **Letter-ordering pass.** Miners did not consistently letter issues in typical-severity order. Since ratification will rename/split/merge anyway, the draft preserves miner ordering; a mechanical re-letter pass runs **after** content rulings, immediately before the 0.1 tag (codes are not yet stable, so this is free now and never again).

## Per-domain open questions (miner-raised)

### SEC
- SEC-A1A (unsafe-subprocess-invocation-pattern, LOW, n=96) vs SEC-A1B (os-command-injection, HIGH): the split separates mechanical-heuristic flags from exploitable injection at the same CWE-78 root — keep distinct, or one severity-graduated issue?
- SEC-E1C (known-vulnerable-dependency, n=47) aggregates all ecosystems and MEDIUM→CRITICAL severities. Split by severity tier (e.g. separate critical-RCE-dependency issue) or keep unified with per-instance severity?
- SEC-C3B (weak-prng-for-security-token) merges hand-rolled LCG (HIGH) with System.Random-for-tokens (MEDIUM) — confirm merge.
- SEC-C1D (hardcoded-backdoor-trigger) sits under access-control; could anchor an insecure-design/OWASP-A04 area if more such items accumulate.
- SEC-D2A/D2B SSRF asymmetry: corpus only has the precursor (LOW); the exploited form (HIGH) is prior-art-invented. Confirm inclusion under the invention budget.

### COD
- Severity conflation cluster (area C1): tool-severity/confidence conflation issues were split fine-grained; confirm granularity.
- The COD/QAL boundary was drawn as "demonstrated or plausible runtime behavioral impact → COD; consistency/maintainability debt → QAL" — ratify the rule, not just the instances.
- Doc-drift split: COD-D2 (doc contradicts behavior, functional) vs QAL-C2 (doc merely stale) — confirm.
- COD-F2B (test-defined-after-main-guard, CRITICAL as silent-test-disable) vs QAL-F2A (guard merely misplaced, no functional impact) — confirm the two-entry treatment.
- Recurrence weights on COD entries skew toward adapter-parsing issues because the corpus is a scanner reviewing itself — expect rebalancing from future non-self corpora.

### ARC
- Area H migration (big rock #3).
- ARC-F (enforcement-and-security-boundary) overlaps SEC-G2 (fail-open-controls): ARC-F2B/F2C vs SEC-G2A/G2B describe the same incidents from architecture vs security angles. Cross-reference (draft) or single-home them?
- ARC-B2 (dependency-pinning) vs SEC-E2 (pinning-and-provenance): same defects, two lenses — the draft keeps both; strong CWE-1357/CWE-829/CWE-494 candidates for merge with cross-refs.
- ARC-E1 hardcoded-path severities (E1C CRITICAL) reflect this repo's portability pain more than a universal grade — re-grade candidates.
- ARC-D3C (missing-referenced-file, CRITICAL) — severity driven by one incident class (assigned review target absent from tree); consider MEDIUM typical + criteria note.

### TST
- TST-A1B (uncovered-function-or-method, n=73) is an intentionally broad catch-all — split by target kind (adapter method / helper / CLI) if finer signal is wanted.
- TST-D1C (unclosed-file-handle, n=13) recurrence is inflated by one reviewer pattern repeating across files in one PR — weight with care.
- Silent-non-verification merge question (big rock #4).
- TST/production boundary rule: defect in test code/infrastructure/data → TST; production defect that "also has no test" → coverage angle stays TST, underlying complaint routes out — ratify the rule.

### QAL
- The QAL regex-heuristic split from the code panel means ~10 correctness/security strays were mined into QAL and are now routing-flagged (appendix) — the reverse strays (style items in COD) were routed similarly. Ratify the routing appendix wholesale or item-by-item.
- QAL-C1D (stale-external-url-reference, MEDIUM) — grade reflects broken-link user impact; confirm.
- Whitespace/formatting entries (QAL-B2) are INFO/LOW and arguably linter territory — keep (named types help tools deduplicate against linters) or drop to a single formatting-noncompliance issue?

## Invention budget check

Prior-art-only entries (no corpus grounding): **SEC-C4B, SEC-D2B** — 2 of 65 SEC entries (3%), well under the ≤25% ceiling. All other domains: 0 invented entries. Skills-class entries (15 new + 5 folds) are evidence-grounded in PR #945 / skill definitions, not invention.

## Post-ratification mechanical pass (no rulings needed)

1. Re-letter issues within each category by ratified typical severity (big rock #9).
2. Regenerate `recurrence` sums where entries were merged/split.
3. Truncated `examples` strings (SEC miner clipped some at ~110 chars) — restore from corpus or trim to clean sentences.
4. Build `build/ocrdb-0.1.json` + SARIF export; activate `tools/validate.py` stability baseline.

---

*Appendices below are generated from the miners' own routing flags — each item is currently **absent** from the flagged domain's entries (the miner excluded it) unless marked "kept".*

## Appendix A — Cross-domain routing flags


### Flagged by the SEC miner (4)

- Malformed Finding Schema with Empty Required Fields -> belongs in a Data-Quality/schema-validation domain (DQ), not SEC; it's about required-field integrity in a JSON contract, not an exploitable defect.
- Hardcoded Docker Container Paths in Test Fixtures -> code-quality/test-hygiene domain (portability/maintainability, not security).
- Shallow copy in citation merge without deep copy protection -> code-quality/correctness domain (mutation-aliasing bug, no demonstrated security impact).
- Greedy regex matches from first to last brace in advisor output -> code-quality/correctness domain (parser robustness bug); flagged here because it feeds an agent-trust decision (see SEC-G1B) but the defect itself is a parsing bug, not a named security issue type.

### Flagged by the COD miner (7)

- **→ QAL** — Version/metadata drift across docs and config files — no demonstrated runtime behavioral impact, reads as maintainability/consistency debt
  - Version mismatch between DEVELOPMENT.md and pyproject.toml
  - Version mismatch between DEVELOPMENT.md and canonical project version
  - Project version out of sync with implementation
  - Project version mismatch across configuration sources
- **→ QAL** — Pure documentation staleness/prose issues with no functional or contract impact articulated
  - README documents non-existent docs/ directory
  - Sample model-profiles.yml Claude block is stale relative to the corrected model names shipped later
  - Section structure inconsistency in prose-heavy list
  - Truncated plan document indicates incomplete review scope
  - Misleading documentation in example file header
  - Architecture inventory is stale relative to the file's own 4.3.0 changelog entry
- **→ QAL** — Repo hygiene / VCS metadata noise, not a code defect
  - Stray macOS .DS_Store Finder-metadata file present under skill/
  - macOS system metadata file tracked in version control
- **→ QAL** — Test-file structural convention (missing __main__ block) — distinct from the CRITICAL misplaced-guard defect (kept in COD-F2B); here the block is simply absent, not misordered, so tests still collect/run normally
  - Missing if __name__ == '__main__' block
  - Missing '__main__' guards in test modules
  - *note: n=10 recurrence is a strong convention signal, but no functional impact was described — differs from COD-F2B where a defined-after-guard ordering silently disables tests*
- **→ QAL** — Non-portable/inconsistent path or sys.path handling described as a portability/consistency smell rather than a runtime resolution bug (contrast with COD-F2A, which is a wrong-base-directory resolution defect)
  - Hardcoded absolute path breaks cross-machine portability
  - Hard-coded absolute fixture paths in manifest.json
  - Inconsistent sys.path manipulation depth in dispatch.py
  - Inconsistent sys.path manipulation patterns in test modules
- **→ QAL** — Code organization / complexity / maintainability — module cohesion, function length, cyclomatic complexity, cognitive load; classic QAL territory
  - Module mixes five distinct concerns without separation
  - Module mixes file discovery, grouping, and catalog concerns
  - dedupe() exceeds complexity threshold
  - cross_panel_corroboration() nested closure, high cognitive load
  - main() 147 lines with 6 mode branches
  - _parse_catalog_yaml implicit state machine
  - dispatch.py combines template parsing, rendering, and agent emission
  - Large monolithic synthesize.py file (980+ lines)
  - Large embedded CSS and JS in html_report.py
  - Multiple inconsistent patterns for citations handling across adapters
- **→ TST (test-quality — not COD, arguably not QAL either)** — Findings about the test suite's own ability to catch defects (vacuous assertions, skipped fixtures, missing coverage, unrealistic fixture data) rather than about production-code correctness
  - Test's no-cargo branch ends in a tautological self.assertTrue(True) that can never fail
  - Integration test only checks CargoAuditAdapter.parse()'s raw output, not what survives citation enrichment
  - SpotBugsAdapter.invoke()'s classes-directory fallback logic has no test coverage
  - Malformed Cargo.lock: non-existent dependency in serde package (fixture-realism issue)
  - Inconsistent cargo-audit version between base and fixture Docker images
  - Vacuous/tautological test provides no real verification of cargo-audit skip behavior
  - cargo-audit's hand-rolled CVSS v3.1 score approximation has zero test coverage
  - No test covers malformed/incomplete pip-audit dependency entries, masking an unguarded-indexing crash risk
  - roslyn-secguard hardcodes severity to HIGH for every finding; the only test carrying a SARIF 'level' field never exercises it
  - Fixture-gated integration tests always skip in this checkout, giving false confidence of adapter coverage
  - test_parse_produces_finding never asserts the severity field despite the fixture defining severity: HIGH
  - test_spotbugs.py has no invoke() test, breaking parallel structure with every sibling adapter test module
  - Only the happy-path branch of each conditional is tested
  - Fixture implies category-based filtering that the adapter (and tests) never actually verify
  - Plan's own acceptance test contradicts its own implementation for empty-findings dashboard charts
  - DepthPlanner test expects the wrong lens given its own priority-based selection algorithm
  - Inline test double classes repeated throughout test_run_tools.py
  - Unvalidated manifest fixture keys (fixture-loader safety, not production data flow)

### Flagged by the ARC miner (4)

- F1A/F1C/F1E (policy-not-enforced, inconsistent auth gating, stale-flag trust) - candidate secondary listing under a governance/SEC domain given the security consequence of the architectural gap, even though the defect itself is structural.
- C1E (ci-gate-bypasses-domain-verdict-model) - candidate secondary listing under CI/CD-focused security domain; currently kept solely in ARC since the root cause is pipeline architecture, not a scanner/code vulnerability.
- B2B (unverified-remote-script-execution, curl|sh) - strong CWE-494 match; likely wanted verbatim in any future SEC or supply-chain domain, currently sole-owned by ARC.
- E1A-E1C (hardcoded paths/identifiers) - CWE-547-adjacent; a SEC domain would likely want these too when any of the hardcoded values are security-relevant (e.g. auth-adjacent repo slugs), currently sole-owned by ARC.

### Flagged by the TST miner (9)

- Insufficient error diagnostics in adapter invocation (run_adapters catches all exceptions generically and logs only a simple message)
  - *Production error-handling/observability quality, not a test-code defect. Likely belongs to a diagnostics/observability or reliability domain.*
- Test-file detection regex set is incomplete, so some test files never trigger the 'test' review panel
  - *Defect is in production file-classification heuristics (which files count as tests), not in test code itself. Belongs to a static-analysis/heuristics domain.*
- Silent error handling in verdict loading with minimal diagnostics (load_verdicts skips malformed files with only stderr warnings)
  - *Production error-handling/diagnostics quality issue, not a test-quality defect type.*
- check_writable() conflates probe-cleanup failure with a not-writable directory
  - *Production logic/correctness bug (wraps create+close+unlink in one except clause), not test-specific.*
- Auto-closed 'area clear' issues are closed with GitHub reason 'not planned' instead of 'completed'
  - *Production correctness bug (wrong API enum value used); reviewer's 'no test' remark is incidental and already generically covered by coverage-gap issues.*
- apply() has no resumability/idempotency tracking, so a mid-batch gh failure risks duplicate comments
  - *Production reliability/design gap (idempotency), not a test-taxonomy item.*
- Duplicated LEDGER path constant risks silent drift between reconcile_apply.py and file_issues.py
  - *Production maintainability issue (constant duplication), unrelated to test quality.*
- Assigned review file skill/scripts/codex_runner.py does not exist in the checked-out working tree
  - *Review-process/scan-scoping problem (reviewer assigned a nonexistent target file), not a named test-defect type.*
- Exceptional test fixture documentation for vulnerable dependencies (Cargo.toml comments mapping each dependency to its RUSTSEC advisory)
  - *Not a defect — this corpus entry is a commendation of good fixture documentation practice, included by the miner as a positive observation. Excluded from the defect taxonomy.*

### Flagged by the QAL miner (10)

- idx71/idx28-cat 'CVE ID format placeholder is imprecise' (correctness-tagged) was folded into QAL C2-F (schema-or-example-stricter-than-reality) as a docs/spec-precision issue rather than a real format-validation bug — flag if a human disagrees and wants it purely in COD.
- idx77 'Tuple size mismatch breaks deduplication logic in model collection' (correctness, MEDIUM) — real logic bug, NOT QAL. Route to COD.
- idx94 'pip-audit adapter's positional-target fallback can execute the scanned project's PEP 517 build backend' (security, HIGH) — genuine security vulnerability (arbitrary code execution via build backend), NOT QAL. Route to SEC domain; anomalous severity confirms it doesn't belong in an evolvability-class taxonomy.
- idx108/idx109 'Unvalidated/Unsafe lens["name"] access' (correctness, MEDIUM x2) — same underlying KeyError/robustness defect found twice via different code paths. Route to COD.
- idx122 'Unclosed file handles in json.dump()' (style-tagged but actually a resource-leak defect, MEDIUM) — mistagged by source reviewer; this is a resource-management/correctness concern (CWE-772-adjacent), not a readability/maintainability one. Route to COD, do not treat as QAL despite the 'style' cat label.
- idx123 'apply() has no per-action resumability; a mid-batch gh failure risks duplicate GitHub comments/closes on retry' (reliability, MEDIUM) — idempotency/retry-safety defect, NOT QAL. Route to COD or a dedicated reliability domain.
- idx128 'ScopeProfile lens-name pattern uses \uXXXX escapes that Python's re module does not support' (correctness, MEDIUM) — regex silently fails to match, a functional bug, NOT QAL. Route to COD.
- idx63 'Test asserts a retired, permanently-broken eslint adapter is registered without exercising its failure path' (test-coverage, LOW) — a test-adequacy gap, not a maintainability defect in production code. Route to a TST (test quality/coverage) domain rather than QAL.
- idx64 'base.ID_RE finding-ID format regex is untested and diverges from the canonical validator' (test-coverage, LOW) — dual-homed: the divergence half is captured in QAL E1-B (unused-duplicate-validator-left-in-code); the 'untested' half is a TST-domain concern and has no home here.
- idx65 'Misleadingly named test verifies a static dict lookup, not a CWE-uppercasing transformation' (test-quality, LOW) — included provisionally as an example under QAL A1-B (misleading-identifier-name) since test names are identifiers, but a human may prefer routing this fully to TST instead.

## Appendix B — Unplaced items (4, all from SEC miner)

Currently homeless — each needs a target ruling (likely COD or QAL per the miner's routing flags above, which cover the same four items):

- Malformed Finding Schema with Empty Required Fields
- Hardcoded Docker Container Paths in Test Fixtures
- Shallow copy in citation merge without deep copy protection
- Greedy regex matches from first to last brace in advisor output

---

## Gates (adopted 2026-08-10, from the 5.x roadmap combined review)

**Gate A — assignment-stability eval, run BEFORE the session.** ≥100 run-3 findings sampled across all five domains; the panel-tier model assigns codes 3× independently from the menu one-liners; agreement reported at full-code and category-prefix tier. Sibling entries confused above threshold get merged or coarsened — **taxonomy granularity is bounded by assigner reliability, not conceptual distinctness.** The data also drives the panopticon reconcile-tier ruling.

### Gate A results (run 2026-08-10; 100 findings, recurrence-weighted stratified sample; 3 independent sonnet passes over the Gate-C menu form)

- **Full-code 3/3 agreement: 91/100. Category-prefix 3/3 agreement: 94/100.** Zero invalid codes across 300 assignments; fallback `X0X` used 23/300 (7.7%), concentrated in COD.
- Per-domain full/prefix: SEC 24/24 of 25 · COD 18/18 of 20 · ARC 17/19 of 20 · TST 18/19 of 20 · QAL 14/14 of 15.
- **Ruling-2 read: 91% clears the ~90% bar — full-code identity is defensible**, recommended as the primary reconcile tier with category-prefix as the fallback tier (mirrors the existing exact-fingerprint → coarse-key two-tier design). Prefix-tier identity would rescue only 3 of the 9 disagreements (the within-category letter wobble); the rest are fallback-judgment or cross-area cases no sub-domain tier fixes.
- **The 9 disagreements, classified:**
  - *Within-category sibling wobble (3)* — merge/criteria candidates: ARC-A1A↔A1B (module vs function scale — one finding legitimately spans both; add a scale criterion), ARC-E3A↔E3C (cross-host-config-parity vs asymmetric-domain-coverage — names nearly synonymous, merge candidate), TST-F1A↔F1C (unisolated-external-service vs environment-gated — adjacent mechanisms, criteria line).
  - *Cross-area confusion (3)*: TST-A3A↔A2F (2 of 3 passes missed that the draft's own A2F example IS this finding — "growth-blind-invariant-check" name lacks scent), QAL-F3D↔F1B ("inconsistent mock import style" straddles mocking-idiom vs import-style — boundary rule needed), ARC-A2D↔H3A (doc-regex enforcement straddles hidden-contract vs weak-test-assertion — cross-ref note).
  - *Fallback wobble (3)*: #13 requirements-file selection — SEC-D1B (uncontrolled-search-path-element) lists this exact case as an example, yet 2 of 3 passes chose X0X: **menu one-liner names need more scent** (rename candidates at ratification). #28/#39 — COD strays already routing-flagged to QAL/TST; consistent X0X here is the menu behaving honestly.
- **Menu-clarity lesson (Gate C feedback):** assigner misses correlated with abstract entry names, not taxonomy depth. Ratification renames should optimize for one-line recognizability.

**Gate B — singleton rule.** A `recurrence: 1` entry survives ratification only with a prior-art crosswalk or an explicit invention-budget note; otherwise it parks on an incubation list. The 62 singletons (verified against the draft):
`ARC-C1C ARC-C1D ARC-D1A ARC-D1D ARC-D1F ARC-D2E ARC-E2E ARC-E3C ARC-F1D ARC-F2E ARC-F2F ARC-G1C ARC-G2B COD-B2A COD-B2B COD-B2C COD-B2D COD-B2E COD-C1B COD-C2C COD-C3A COD-D2C COD-D2D COD-D3C COD-E1A COD-E1B COD-E1C COD-E1E COD-E2A COD-E2B COD-F1A COD-F1B QAL-B3C QAL-C1C QAL-C2C QAL-C2D QAL-C2E QAL-F2B QAL-F2C QAL-F3B SEC-B1A SEC-B1B SEC-B1D SEC-B3B SEC-C1A SEC-C1E SEC-G1B SEC-H1A SEC-H2A SEC-H3A TST-B1E TST-B2B TST-B2C TST-B2D TST-C3D TST-C4B TST-C5A TST-C5C TST-C5D TST-D2B TST-E1B TST-F1A`

**Gate C — menu discipline.** The bundle build emits a menu form per entry: one line, `CODE name (SEV)`. Criteria text is advisor-stage only; whole-domain slices render as area/category headers + one-liners. Bounds the permanent per-dispatch tax the identity spine introduces.

**Big rock #10 (added): corpus-blind territories.** Appendix C's gap clusters need three structural placements ruled — concurrency (proposed `COD-G`), resilience (proposed `ARC-I`), observability (proposed `QAL-I`) — plus per-entry adoption of the crosswalk-backed gap candidates.

## Appendix C — external gap analysis (Gemini, 2026-08-10), triaged

An independent Gemini review proposed 33 additions. **Its codes are unusable** — it worked from CHARTER/SCHEMA alone and every proposed code collides with an assigned draft slot (its `SEC-C1A crypto-weak-hash-algorithm` vs. our `SEC-C1A container-runs-as-root`, etc.). Content triaged name-level against all 320 entries:

### Already covered (14 — adopt nothing; convergence evidence)

| Gemini proposal | Draft entry |
|---|---|
| crypto-hardcoded-secret | SEC-B3C (severity note: they say CRITICAL, draft HIGH) |
| auth-missing-rate-limit | SEC-C2B (exact, CWE-307) |
| deps-unpinned-manifest | SEC-E1A/E2B/E2C (manifest-range nuance → examples) |
| error-swallowed-exception | SEC-F1A + COD-B2 |
| error-generic-catch | ARC-F2A |
| logic-off-by-one | COD-A2 |
| resource-unclosed-handle | COD-A1 / SEC-F2A / TST-D1C (already a routing question) |
| concurrency shared-state (partial) | SEC-F2B + ARC-E2A |
| boundary-circular-dependency | ARC-A2E |
| boundary-leaky-abstraction | ARC-A2A |
| flaky-shared-state-bleed | TST-D1 |
| assert-missing-validation | TST-B2 |
| assert-broad-equality | TST-B1B (exact) |
| doc-drift / nested-conditionals / god-class / misleading-identifier | QAL-C2 / QAL-H1B / ARC-A1A+QAL-F2B / QAL-A1B |

### Gap candidates (13 — adopt at ratification, provenance `[prior-art, gemini-gap-review]`, Gate B note each)

All from territories a stdlib-Python self-scan corpus is structurally blind to. Severities to be graded fresh at ratification (Gemini's run hot).

| Candidate | Proposed placement | Crosswalk stub |
|---|---|---|
| weak-standard-crypto-algorithm (MD5/SHA-1) | SEC-C3 (beside C3A ad-hoc checksum) | CWE-327/328, OWASP A02 |
| pii-logged | SEC-B2 | CWE-359, CWE-532 |
| abandoned-unmaintained-dependency | SEC-E1 (distinct from known-vulnerable E1C) | CWE-1104, OpenSSF Scorecard |
| race-condition (production) | **new COD-G concurrency** | CWE-362 |
| blocking-call-on-event-loop | COD-G | async ecosystem guidance |
| stale-cache-read | COD-G (state/caching category) | common prior art |
| unbounded-collection-load | QAL-G (efficiency; `character: defect`) or perf home per big rock #10 | CWE-400/770 |
| missing-timeout-on-remote-call | **new ARC-I resilience** | CWE-1088 |
| missing-retry-transient-failure | ARC-I | resilience patterns |
| missing-trace-propagation | **new QAL-I observability** | OTel; homes the TST miner's routed-out diagnostics strays |
| vague-log-context | QAL-I | CWE-778 adjacent |
| time-dependent-flaky-test | TST-F (new category: timing sensitivity) | flaky-test literature |
| mock-internal-behavior | TST-C4 | "change-detector tests" (Google) |

Also noted, not an entry: n-plus-one placement (QAL-G1D today) feeds the big-rock-#10 performance-home ruling. `doc-missing-why-context` → QAL-C candidate (INFO), weakest of the set — owner's call.

### Declined (1)

`input-missing-sanitization` — generic catch-all duplicating SEC-A's specific injection issues; conflicts with the `<DOM>-X0X` fallback discipline (the "nothing specific fits" signal must stay a counted fallback, not an entry).

### Budget

Adopting all candidates ≈ 15 prior-art entries of ~333 (≈4.5%) — ceiling is 25%.
