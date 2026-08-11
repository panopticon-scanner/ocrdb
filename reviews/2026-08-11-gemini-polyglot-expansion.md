# Gemini Pro 3.1 — Polyglot Catalog Expansion (0.2 feeder)

- **Received:** 2026-08-11, external review of OCRDb 0.1.0 by Gemini Pro 3.1
- **Status:** Adjudicated; queued for the 0.2 ratification. **Nothing integrated.**
- **Discipline:** Reviews pass through adjudication; reviewers have no write
  privilege. Gemini's "integrate into `domains/*.yml`" action items are **not**
  executed here — adoption is the ratification's job, with the maintainer's
  rulings. This doc records the proposal, the verification, and the verdicts.

## Provenance of the proposal

Gemini proposed 9 new codes to correct 0.1.0's backend/Python/Docker seeding
bias, spanning frontend/client-side, IaC/cloud-native, non-relational data, and
E2E/UI test flakiness. Full original text retained in the project intake.

## Verification against 0.1.0 (on-disk)

- **All 9 proposed codes are grammar-valid** (`DOM-A1B`).
- **Zero namespace collisions** — every proposed code occupies a free slot
  (Gemini's action-item 1, satisfied).
- **Cited anchors confirmed:** SEC-H *is* web-session-and-browser-boundary
  (CSRF = SEC-H2 cross-site-request); COD-A1A/B, ARC-E1A–C, ARC-E2A–D,
  DAT-A1A–D, TST-F1D/F1E all exist as cited.

## Verdicts

| Proposed | Verdict | Rationale |
|---|---|---|
| `COD-A1C` unclosed-event-listener-leak (MED) | **Adopt, rename** | Legit resource leak; single-homing homes leaks in COD, beside A1A file-handle. Rename framework-neutral → `unremoved-listener-or-subscription-leak` (RxJS/emitters, not just DOM). |
| `COD-F4A` direct-mutation-of-immutable-state (HIGH) | **Adopt hazard; reject placement** | Not a concurrency defect — must not go under COD-F (concurrency). Reframe framework-neutral ("mutation of a value consumers assume immutable"); severity **MED**, not HIGH (UI desync ≠ data loss). Placement → ratification (see unsafe-mutation cluster). |
| `ARC-E2E` client-state-persisted-in-ephemeral-storage (LOW) | **Decline — duplicate** | Same hazard as **ARC-E2A** durable-state-in-ephemeral-scratch-location. Single-homing forbids a second code. Action: enrich E2A with a sessionStorage/in-memory example. *(Maintainer upheld.)* |
| `ARC-E1D` hardcoded-cloud-region-or-zone (LOW) | **Weak / broaden** | Near-duplicate of **ARC-E1C** hardcoded-identifier-scattered. Adding each specific hardcoded thing bloats the area. Prefer one broader `hardcoded-cloud-resource-identifier` (region/account/arn/bucket), or an E1C example. → ratification. |
| `ARC-B4A` missing-resource-allocation-limit (MED) | **Reroute to OPS** | Production-readiness, not architecture. The charter already declared **OPS incubating** (health checks, graceful shutdown, resource governance). This is OPS's first concrete entry, not ARC-B. *(Maintainer upheld.)* |
| `DAT-A1E` missing-partition-or-shard-key (HIGH) | **Adopt** | Real NoSQL modeling hazard; "silently wrong at scale" → HIGH holds. Corrects DAT's relational bias. Fits A1 (integrity-and-modeling). |
| `DAT-A2A` unbounded-document-growth (MED) | **Adopt; placement TBD** | Distinct from DAT-C1C unbounded-*result-set* (storage/model vs query side). New category `A2 document-design` vs a `DAT-A1F` slot → ratification. |
| `DAT-F1A` unmanaged-consumer-offset (HIGH) | **Adopt hazard; caveat** | Real Kafka data-loss/duplication hazard, HIGH. But a whole new **area DAT-F for one entry** repeats the "don't seed a skeleton" discipline — ratification: seed DAT-F now vs. declare event-streaming incubating until a streaming corpus lands. |
| `TST-F3A` arbitrary-sleep-instead-of-state-wait (MED) | **Adopt; generalize** | Classic E2E flake, fits TST-F flakiness-determinism. Generalize beyond Playwright/Cypress (async backend tests sleep too). New category `F3 synchronization`. |
| `TST-F3B` unverified-dom-state-before-interaction (MED) | **Adopt; rename** | Sibling of F3A (act-without-readiness vs wait-wrong). Framework-neutral → `interaction-before-readiness-check`. Ratification may merge with F3A. |

**Tally:** 6 adopts (with naming/severity/placement tweaks), 1 decline-as-duplicate
(`ARC-E2E`), 1 reroute-to-OPS (`ARC-B4A`), 1 broaden (`ARC-E1D`).

### Maintainer rulings (2026-08-11)

- **Both overrides upheld:** `ARC-E2E` declined as a duplicate of `ARC-E2A`
  (enrich E2A instead); `missing-resource-allocation-limit` rerouted to OPS
  seeding rather than a new `ARC-B4`.
- **Record + consolidate:** this feeder is queued for a **single 0.2
  ratification** shared with the tool-rule-mining gap candidates (see
  `docs/specs/2026-08-11-tool-rule-mapping-design.md`).

## Structural findings (beyond the 9 codes)

1. **OPS should graduate incubating → seeded.** The IaC/cloud items are OPS
   content, not ARC gaps. `missing-resource-allocation-limit` is OPS's first
   concrete entry; this review is the corpus signal that OPS's incubation is
   warranted. The 0.2 ratification should decide OPS's seeding scope.
2. **Single-homing earned its keep.** `ARC-E2E` would have been a silent
   cross-domain-style duplicate of `ARC-E2A`; the rule caught it. `DAT-A2A`
   likewise required a check against `DAT-C1C`.
3. **The `unsafe-mutation / aliasing` cluster.** `COD-F4A`
   (mutation-of-assumed-immutable) joins the tool-rule-mining gap candidates
   `mutable-default-argument` and `internal-mutable-representation-exposed` as
   one family — a candidate new COD category, to be shaped at ratification.
4. **`automated_by` overlap.** Several items are linter-catchable (eslint
   `react/no-direct-mutation-state`; testing-library / cypress wait rules), so
   they carry `automated_by` too — confirming this review and the tool-rule
   crosswalk are the **same 0.2 stream**, not two.

## 0.2 ratification rulings (2026-08-11, maintainer)

1. **`COD-F4A` cluster → defer to the tool-mining pass.** Let the mining pass
   surface the full mutation family before shaping the unsafe-mutation/aliasing
   category; `COD-F4A`, `mutable-default-argument`, and
   `internal-mutable-representation-exposed` are held for that pass. `COD-F4A`
   itself: adopt the hazard, framework-neutral name, **MEDIUM** (not HIGH).
2. **`ARC-E1D` → broaden** to `hardcoded-cloud-resource-identifier`
   (region/account/arn/bucket), one entry covering the IaC family.
3. **`DAT-A2A` → `DAT-A1F` slot** under integrity-and-modeling (beside the
   adopted `DAT-A1E` shard-key); no new `DAT-A2` category yet.
4. **`DAT-F1A` → incubate event-streaming.** Declare streaming incubating; the
   offset entry is held until a streaming corpus is mined (no-skeleton).
5. **`TST-F3A` / `TST-F3B` → two codes** under a new `TST-F3 synchronization`
   category (framework-neutral names: arbitrary-sleep; interaction-before-readiness-check).
6. **OPS → dedicated mining pass.** Not seeded in 0.2. The Fable-authored OPS
   payload is adjudicated and parked as the **prior-art seed input** to that
   pass — see `reviews/2026-08-11-ops-seed-input.md`.
7. **`automated_by` tags** for the adopted, linter-catchable candidates are
   confirmed, applied as part of the tool-rule-mining pass.

**Adopts standing as adjudicated (no fork):** `COD-A1C` renamed
`unremoved-listener-or-subscription-leak`; `DAT-A1E` missing-partition-or-shard-key
(HIGH). `ARC-E2E` declined (≡ `ARC-E2A`, enrich with example);
`missing-resource-allocation-limit` → OPS seed input (per §6).

## Non-goals of this doc

- No `domains/*.yml` edits. No new codes minted. No severities finalized.
- Placement/area/issue-letter assignment is deferred to the ratification, per the
  0.1 precedent.
