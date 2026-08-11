# Changelog

All notable changes to the OCRDb taxonomy. Codes are held stable per release but may change before 1.0 (incubating); see SCHEMA.md stability contract.

<!-- TODO(0.2.0): Renamed `typical_severity` → `default_severity` (breaking, pre-1.0). Full 0.2.0 changelog entry is written in Task 9. -->

## 0.1.0 — 2026-08-10 (first ratified release, private incubation)

The seeding round: 320 mined draft entries walked in an owner ratification session, restructured per the rulings below, and re-lettered by typical severity into final codes. **381 entries across 7 domains.** Codes are held stable per release but may change before 1.0 (incubating).

**Domains:** `SEC` security (73), `COD` correctness (58), `ARC` architecture (77), `TST` testing (80), `QAL` quality/maintainability (58), **`AGT` agentic-trust (16, new)**, **`DAT` data-and-persistence (19, new)**. Declared incubating (no codes yet): `OPS`, `A11Y`, `I18N`.

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
