# OCRDb 0.2 — Identity-Integrity & Governance Remediation (Design Spec)

- **Date:** 2026-08-11
- **Status:** Draft (awaiting review)
- **Target:** **0.2.0** — a clean identity-base reset (breaking, pre-1.0)
- **Inputs (committed alongside):**
  - `reviews/2026-08-11-ocrdb-initial-documentation-review.md` (Codex governance/identity review)
  - `reviews/2026-08-11-ocrdb-0.1-catalog-audit.md` (Kimi catalog audit — the 19 clusters, budget census, ambiguity findings)

## 1. Motivation & the governing ruling

The shipped `v0.1.0` promises a stable, single-homed identity layer but does not
yet deliver one. Two independent external reviews converge:

- **Codex (verified):** a P0 governance contradiction (`CHARTER.md:3` "codes may
  change freely until 1.0" vs `SCHEMA.md:96`/`CHANGELOG` "immutable from tag");
  single-homing is "a promise, not a current property"; 0/381 entries carry the
  disambiguation layer; and the tool-rule enrichment "assumes clean identities,"
  so it must follow duplicate resolution, not precede it.
- **Kimi (verified, quantified):** **19 advisor-verified same-hazard clusters**
  (audit §1), 9 needs-criteria clusters + 69 ambiguities, `see_also` 100%
  unpopulated, the prior-art budget breached per-domain (DAT 95 % / AGT 44 % /
  COD 34 % / SEC 26 % vs a 25 % ceiling), a polluted provenance vocabulary, and
  doc drift (`CHARTER` says COD-G, concurrency shipped COD-F).

**Governing ruling (2026-08-11):** 0.x codes are **mutable**; the stability
freeze activates at **1.0**, not at each 0.x tag. Therefore the remediation is a
**clean rewrite** — merge/remove duplicate codes outright, **no deprecation
tombstones** — re-cut as **0.2.0**. There are no real consumers of `v0.1.0`
(the panopticon 5.0 spine is unbuilt), so the pin promise currently protects no
one, and carrying ~19 error-born tombstones into 1.0 is the worse outcome.

**Ordering (Codex, adopted):** identity → criteria → `see_also` → provenance/
budget → Gate A → *then* enrichment → *then* new gap codes. This spec covers the
identity-and-governance half (0.2.0); enrichment and growth are deferred
follow-ons on the clean base.

## 2. Scope

**In (→ 0.2.0):** governance-doc alignment; validator hardening; resolution of
the 19 clusters; `criteria` for the confusable boundaries; `see_also`
population; provenance-vocabulary cleanup + truncated-example repair; a
domain-unpinned Gate A re-run.

**Deferred (post-0.2.0, on the clean base):**
- Tool-rule `automated_by` enrichment — the halted crosswalk (branch
  `feat/tool-rule-crosswalk`, Tasks 1–2 already landed: validator shape check +
  reverse-map build) resumes here.
- New gap codes — the Gemini 45 + the tool-mining gaps, gated by the prior-art
  budget ruling (§6).
- OPS / event-streaming seeding (already parked; dedicated mining pass).

**Separable (any time, independent):** the `build_catalog.py` `</script>`
injection fix; test-suite `ResourceWarning` cleanup; CI `--baseline` wiring.

## 3. Mechanism (from the ruling)

For each cluster in audit §1: keep the **single home** named by the advisor
resolution, **remove** the duplicate code(s), fold the removed entry's
`recurrence` / distinct `examples` / `cwe` into the survivor, and set the
survivor's severity to the calibrated value (resolving the LOW-vs-HIGH conflicts
per the §6 severity rule). Because codes are mutable pre-1.0, removal is
outright — no `status: deprecated`, no `superseded_by`. Prefer minimal
re-lettering; only re-letter within a category when removal would otherwise
strand the severity-ordering invariant.

**Governance docs:** correct `SCHEMA.md:96` and `CHANGELOG.md` so the freeze is
stated as **activating at 1.0** (0.x explicitly mutable, "held stable but may
change"); `CHARTER.md:3` stands. Fix the `CHARTER.md:33` COD-G → COD-F drift.
`CHANGELOG.md` must stop crediting the 0.1 restructure with `see_also` it never
applied.

**Versioning & stability:** 0.2.0 is an identity-base reset; the `CHANGELOG`
documents the code changes as a sanctioned pre-1.0 restructure. The validator's
`--baseline` stability check is **not** enforced across the 0.1.0 → 0.2.0
boundary (the rewrite intentionally breaks it); it becomes a **1.0-forward**
gate. Wire it into CI from the 0.2.0 baseline onward (§7).

## 4. Phases (Codex order)

1. **Governance alignment + validator hardening** (§5). Docs reconciled; the
   validator gains the checks that mechanize the rules being asserted.
2. **Resolve the 19 clusters** — per audit §1, using the §3 clean-rewrite
   mechanism. This is the P0 core; a post-pass advisor re-check must find 0
   surviving same-hazard duplicates.
3. **Criteria for the 9 needs-criteria clusters** (audit §2) + the
   highest-priority Appendix-B ambiguities. Each `criteria` states positive
   qualification rules **and** nearest-neighbor exclusions — never a restatement
   of the name.
4. **Populate `see_also`** for every settled near-miss pair named in the §2/§3
   resolutions and the criteria clusters.
5. **Provenance-vocabulary cleanup + truncated-example repair** (audit §3.2/§3.3)
   + rule the **prior-art budget** (§6). Strip the 5 annotation-garbage values,
   document the 10 undocumented ones, fix the 2 bare `corpus` → `corpus-4x`;
   restore/trim the 36 clipped examples across 26 entries.
6. **Gate A, domain-UNPINNED re-run** — 3 independent passes over a
   recurrence-weighted sample, now that duplicates are gone and criteria exist.
   This is the deferred 0.1 item, and cleanup gives it its real meaning
   (cross-domain assignment stability). Target ≥ the pinned 91 %/94 %, or explain
   the residual.

## 5. Validator hardening (concrete, `tools/validate.py`)

Each mechanizes a rule the taxonomy already asserts (Codex Appendix E / audit §8):

- **Provenance controlled-vocabulary check** — provenance items must be drawn
  from a documented set (SCHEMA.md vocabulary section); free-text qualifiers
  move to `notes`.
- **`see_also` target-existence check** — every `see_also` code must resolve to
  a real entry (no dangling pointers).
- **Duplicate-domain-file check** — two files declaring the same `domain` is an
  error.
- **`automated_by` format check** — already implemented on
  `feat/tool-rule-crosswalk` (Task 1, commit `594f9c1`); cherry-pick it here so
  0.2.0 carries it independently of the deferred enrichment.
- **Docstring correction** — the "cross-domain duplicate names WARN
  pre-ratification" language is stale post-clean-rewrite.

**A11Y / I18N grammar (OPEN RULING, §6):** the `^[A-Z]{3}-…` grammar cannot
express the 4-character `A11Y`/`I18N` incubating domains. Resolve before either
is seeded.

## 6. Open rulings (for spec review / a short ratification)

These do not block Phases 1–4 (the P0 core); they gate Phases 5–6 and the
deferred growth. Recommendations given; the maintainer rules.

- **Prior-art budget.** The per-domain 25 % cap is breached in four domains and
  conflicts with the catalog-wide figure the CHANGELOG cites. *Recommendation:*
  retire the blunt percentage in favor of a **per-entry evidence requirement** —
  every `prior-art` entry must cite a controlled external source (CWE/OWASP/ISO/
  named guide) — plus a catalog-wide soft advisory. This is more honest than a
  quota and directly gates whether DAT (95 %) / AGT (44 %) gap batches need
  corpus grounding.
- **A11Y / I18N grammar.** *Recommendation:* **rename to three-letter domains**
  (e.g. `ACC`, `INT`) — a grammar widening is a schema-version event and burns
  the compatibility the codes are meant to provide; renaming a not-yet-seeded
  incubating domain is free.
- **ARC↔QAL boundary policy.** *Recommendation:* adopt the audit's implicit rule
  as written policy — **structural/systemic → ARC, per-instance → QAL**, applied
  to entry **definitions**, not just examples — and use it as the `criteria`
  basis for that border (the largest source of cross-domain doubles).
- **Severity-conflict reconciliation.** *Recommendation:* set each survivor's
  severity by the R2 bar — "exploitable now, data loss, or silently wrong at
  scale" — and record the reconciliation in the CHANGELOG.

## 7. Separable bug fixes (independent of the identity work)

- **`build_catalog.py` `</script>` injection (Codex P2 / audit §8, verified at
  `tools/build_catalog.py:236`).** The entries JSON is interpolated into a
  `<script>` block without escaping `</script>`; a `</script>` in a free-text
  `example` breaks out and injects markup. Fix: serialize safely for an HTML
  script context (escape `<`/`/`), or place the JSON in a non-executable
  `<script type="application/json">` element and parse its `textContent`. Also
  drop the `examples` field from the embedded blob (the JS never renders it —
  ~40 % dead payload).
- **Test hygiene:** close files in `tests/test_tools.py` (the `ResourceWarning`s
  are ironic given `TST-D1B`); fix the stale `QAL-B2B` comment.
- **CI:** wire the `--baseline` stability check into `.github/workflows/validate.yml`
  from the 0.2.0 baseline forward.

## 8. Testing & gates

- `python3 tests/test_tools.py` (path-based — a machine `.pth` shadows the
  package-style `-m unittest tests.test_tools`) green after each phase.
- The hardcoded **381-count** assertions in `tests/test_tools.py` must be updated
  to the post-rewrite count (removing the duplicates drops the total; expect
  ~360, exact number set by the resolutions).
- Each validator-hardening check ships with red-before-green unit tests
  (malformed provenance / dangling `see_also` / duplicate domain fail; clean
  passes), extending the existing `unittest` suite.
- No `--baseline` check against `v0.1.0` (intentionally broken); baseline resets
  at 0.2.0.
- Advisor re-check after Phase 2: 0 surviving same-hazard clusters.
- Gate A unpinned result recorded in `reviews/`.

## 9. Success criteria

- 19 clusters resolved (advisor re-check clean); the confusable boundaries carry
  `criteria`; `see_also` populated for every settled pair.
- Provenance vocabulary controlled and validator-enforced; truncated examples
  repaired.
- Governance docs internally consistent (freeze = 1.0; COD-F; no false `see_also`
  credit).
- Domain-unpinned Gate A run recorded.
- `0.2.0` tagged on the clean identity base, artifacts regenerated.

## 10. Deferred / follow-ons (post-0.2.0)

- Resume the tool-rule enrichment (`feat/tool-rule-crosswalk`) on the clean base
  → `automated_by` population + the reverse-map artifact.
- New gap codes: the Gemini 45 (audit §4) + the tool-mining gaps, per the §6
  budget ruling.
- OPS / event-streaming seeding via dedicated mining passes.

## Self-review

- **Input coverage:** every Codex P0/P1 and Kimi §1–§4/§8 finding maps to a phase
  or an open ruling (governance→P1/§3; 19 clusters→P2; criteria→P3; see_also→P4;
  provenance/budget→P5/§6; Gate A→P6; `</script>`/grammar/CI→§5/§7).
- **Mechanism consistency:** the clean-rewrite mechanism (no tombstones) follows
  directly from the immutability ruling and is applied uniformly in §3/§4/§8.
- **No placeholders;** the 19 clusters and their resolutions live in the
  committed audit (§1) — referenced, not duplicated (DRY).
- **Scope discipline:** enrichment and gap growth are explicitly deferred, honoring
  Codex's ordering; this spec is the identity-and-governance half only.
