# OCRDb 0.2 — Gate A, domain-unpinned re-run

- **Date:** 2026-08-11
- **Catalog:** 0.2.0-rc, 357 entries (single-homed, `criteria` + `see_also` added), commit `ea2d39a`.
- **Purpose:** Re-measure assigner agreement now **domain-unpinned** — advisors assign each
  finding a code from the whole 357-code menu, not a pinned domain. This is the deferred 0.1
  Gate-A item; with duplicates removed and criteria present it measures cross-domain
  assignment stability.

## Method

- **Sample:** 100 findings drawn from the catalog's 499 example-findings, **recurrence-weighted**
  and **domain-stratified** (Efraimidis–Spirakis weighted reservoir; fixed seed `20260811`,
  reproducible via `reviews/gate-a-0.2.0/gen_gate_a.py`). Allocation: SEC 23, TST 26, ARC 22,
  QAL 15, COD 11, AGT 3, **DAT 0**. Spans 74 distinct home-codes.
- **Menu:** the full domain-unpinned Gate-C menu with each code's `criteria` inline (412 lines).
- **Raters:** 3 independent `sonnet` advisors, one code per finding, no communication.
- **Metrics:** 3-way agreement (all 3 identical) and pairwise agreement, at full-code and
  category-prefix (`DOMAIN-AREA-CAT`, e.g. `SEC-A2`) resolution.

## Results

| Metric | 0.2 unpinned | 0.1 pinned (baseline) |
|---|---|---|
| Full-code, 3-way | **85%** | 91% |
| Category-prefix, 3-way | **86%** | 94% |
| Full-code, pairwise | **89%** | — |
| Category-prefix, pairwise | **90%** | — |
| Accuracy vs home code (per advisor) | 80% / 77% / 81% | — |
| All-3-agree AND match home | 75% | — |
| Hallucinated / invalid codes | **0 / 300** | — |

Per-domain full-code 3-way: AGT 3/3 (100%), SEC 22/23 (96%), QAL 13/15 (87%), TST 22/26 (85%),
COD 9/11 (82%), ARC 16/22 (73%).

## Interpretation

- The unpinned result (85% / 86% 3-way) is **below** the pinned 0.1 baseline (91% / 94%), but the
  conditions differ: unpinned assignment (choose from all 357 codes across 7 domains) is
  materially harder than pinned (choose within a known domain). Pairwise agreement (89% / 90%)
  sits close to the pinned figure despite the harder task.
- **Single-homing worked:** none of the 15 disagreements is a duplicate-driven split — the
  "same hazard under two codes" wobble that drove 0.1's residual is gone (those codes were
  removed in Task 3). Every disagreement is a legitimate near-boundary judgment.
- **Zero hallucinated codes** across 300 assignments — the menu + criteria kept advisors on real
  codes.

## Disagreement analysis (15 findings → criteria follow-ups)

1. **ARC / COD / QAL contract-drift & doc-drift (5/15)** — GA-018, GA-036, GA-042, GA-097, GA-098
   (§2 clusters 1–3: schema-stricter-than-producer / documented-feature-unimplemented /
   contract-vs-schema). Criteria exist, but the "instance breaks the contract → COD vs. documents
   disagree → ARC vs. inert staleness → QAL" call still splits advisors. **Highest-value follow-up.**
2. **ARC area-A structural-duplication granularity (3/15)** — GA-002, GA-046, GA-054:
   ARC-A2 (co-location) vs ARC-A3 (duplicated logic) vs ARC-A5 (non-canonical constant).
3. **TST area-A test-quality sub-boundaries (4/15)** — GA-005, GA-009, GA-028, GA-041:
   TST-A1/A2/A3 (assertion strength / coverage-gap / misleading-name).
4. **Cross-domain edges (3/15)** — QAL-B1C↔TST (GA-066), ARC-A4A↔SEC-A4B (GA-013),
   SEC-B1C↔AGT-A1B (GA-053).

Each becomes a `criteria`/`see_also` follow-up, deferred post-0.2.0 (consistent with the
enrichment deferral).

## Caveats

- **DAT uncovered:** all 19 DAT entries are example-less (their corpus examples were re-homed /
  trimmed in Tasks 3–4), so DAT contributed no sample findings. DAT assignment stability is
  unmeasured here — revisit once DAT gains examples.
- **In-distribution findings:** the sample is the catalog's own examples, so agreement may read
  optimistically vs. novel findings. This matches how 0.1's Gate A was run — apples-to-apples.
- **Reproducible:** seed `20260811`; scripts + the 3 raw advisor outputs + the sample/key in
  `reviews/gate-a-0.2.0/`.

## Verdict

Recorded per the 0.2.0 success criterion. Unpinned agreement of **85% / 86%** (3-way), **89% / 90%**
(pairwise), with **zero duplicate-driven splits** and **zero hallucinations** on the harder
unpinned task — a solid result that validates the single-homing rewrite and localizes remaining
work to a small set of documented boundaries (ARC/COD/QAL contract-drift foremost).
