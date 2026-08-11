# OCRDb 0.2 Identity-Integrity Remediation — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the shipped 0.1.0 catalog into a clean single-homed identity base (0.2.0) by resolving the 19 same-hazard clusters, adding the disambiguation layer, aligning governance docs, and hardening the validator — following the Codex ordering.

**Architecture:** A clean rewrite (codes mutable pre-1.0): duplicate codes are removed outright and folded into their single home — no deprecation tombstones. Governance docs are reconciled to "freeze at 1.0." The validator gains the checks that mechanize the rules being asserted. Enrichment and gap-growth are explicitly out of scope.

**Tech Stack:** Python 3 stdlib + PyYAML; `unittest` tests in `tests/test_tools.py`; domain content in `domains/*.yml`.

## Global Constraints

- **Mechanism = clean rewrite.** Duplicate codes are removed and folded into the single home named by the audit resolution — **no `status: deprecated`, no `superseded_by`**. The stability freeze activates at **1.0**; the `--baseline` stability check is **not** run across the 0.1.0 → 0.2.0 boundary (the rewrite intentionally breaks it).
- **Source of truth for the 19 clusters:** `reviews/2026-08-11-ocrdb-0.1-catalog-audit.md` §1 (each cluster + advisor resolution). The 9 needs-criteria clusters are §2; the governance census is §3.
- **Severity reconciliation:** where a merged cluster has conflicting severities, set the survivor by the R2 bar — "exploitable now, data loss, or silently wrong at scale." Flag any genuinely-ambiguous case to the maintainer; never guess silently.
- **ARC↔QAL policy:** structural/systemic hazard → ARC, per-instance → QAL, applied to entry **definitions** (this is the `criteria` basis for that border).
- **Tooling stays stdlib + PyYAML.** Test command is **`python3 tests/test_tools.py`** (a machine `.pth` shadows the package-style `-m unittest tests.test_tools`).
- **Entry count drops.** Removing the duplicates lowers the total from 381; the exact new count is computed after Task 3 and threaded into every `== 381` assertion in `tests/test_tools.py`.
- **Out of scope (deferred):** the prior-art budget ruling, the A11Y/I18N grammar ruling, tool-rule enrichment, and all new gap codes (Gemini 45 + tool-mining). This plan is the identity-and-governance base only.
- **All work via PR to `panopticon-scanner/ocrdb`** with `export GH_CONFIG_DIR="$HOME/.config/gh-psyberone"` before any push. Run tooling from the repo root.

## File Structure

- `SCHEMA.md`, `CHANGELOG.md`, `CHARTER.md` — **modify**: governance alignment + provenance vocabulary section.
- `tools/validate.py` — **modify**: `see_also`-target, duplicate-domain, `automated_by`-shape, provenance-vocabulary checks + docstring fix.
- `tests/test_tools.py` — **modify**: tests for the new checks; count-assertion update.
- `domains/*.yml` — **modify**: cluster resolutions, `criteria`, `see_also`, provenance + example repair.
- `reviews/2026-08-11-gate-a-unpinned.md` — **create**: the domain-unpinned Gate A result.
- `build/ocrdb-0.2.0.*` — **create** at release.

---

### Task 1: Governance-doc alignment

**Files:** Modify `SCHEMA.md`, `CHANGELOG.md`, `CHARTER.md`.

- [ ] **Step 1: Correct the immutability language**

In `SCHEMA.md` line ~96 (`Codes are immutable once released — never reused, never renamed, never re-lettered.`), change to state the freeze activates at 1.0:

```markdown
1. **Codes are immutable from the 1.0 release** — never reused, renamed, or
   re-lettered thereafter. Before 1.0 the catalog is incubating and codes may
   change (per CHARTER); 0.x releases are held stable as a courtesy, not a
   contract.
```

- [ ] **Step 2: Fix the CHANGELOG over-promise**

In `CHANGELOG.md`, change "Codes become immutable at each release tag" / "stable from this tag forward" to "Codes are held stable per release but may change before 1.0 (incubating)." Remove the claim that the 0.1 restructure applied `see_also` cross-refs (it did not — audit §3.1).

- [ ] **Step 3: Fix the concurrency drift**

In `CHARTER.md` (the line reading "concurrency in `COD-G`"), change `COD-G` → `COD-F` (concurrency shipped as COD-F; COD-G is data-representation-and-time).

- [ ] **Step 4: Verify internal consistency**

Run: `grep -niE "immutable|stable from|may change|COD-G|see_also" CHARTER.md CHANGELOG.md SCHEMA.md`
Expected: no remaining statement that 0.x codes are immutable-from-tag; no "concurrency in COD-G"; no false see_also credit.

- [ ] **Step 5: Commit**

```bash
git add SCHEMA.md CHANGELOG.md CHARTER.md
git commit -m "docs(governance): freeze at 1.0, fix COD-F + see_also over-promise"
```

---

### Task 2: Validator hardening — structural checks

**Files:** Modify `tools/validate.py`, `tests/test_tools.py`.

**Interfaces:** Produces hard errors for: a `see_also` target that does not exist; two files declaring the same `domain`; a malformed `automated_by` item. These pass on the *current* catalog (no `see_also` populated yet; one file per domain; the 5 QAL `automated_by` conform).

- [ ] **Step 1: Write the failing tests**

Add to `class TestValidateSyntheticErrors` in `tests/test_tools.py`:

```python
    def test_see_also_target_must_exist(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-A1A"]["see_also"] = ["SEC-Z9Z"]
        self.assertTrue(any("see_also" in e and "does not exist" in e
                            for e in self._errs(d)), self._errs(d))

    def test_duplicate_domain_file_is_error(self):
        d = self._base_doc()
        d["y.yml"] = dict(d["x.yml"])  # second file, same domain SEC
        self.assertTrue(any("declared by" in e for e in self._errs(d)),
                        self._errs(d))

    def test_automated_by_shape(self):
        d = self._base_doc()
        e = d["x.yml"]["entries"]["SEC-A1A"]
        e["automated_by"] = ["ruff:B006", "eslint:@typescript-eslint/no-explicit-any"]
        self.assertEqual(self._errs(d), [])
        for bad in ("ruff B006", ":B006", "ruff:", 123):
            e["automated_by"] = [bad]
            self.assertTrue(any("automated_by" in x for x in self._errs(d)), bad)
```

- [ ] **Step 2: Run to verify they fail**

Run: `python3 tests/test_tools.py`
Expected: the three new tests FAIL (checks not present).

- [ ] **Step 3: Implement the checks**

In `tools/validate.py`, add near `CWE_RE` (after line 30):

```python
AUTOMATED_BY_RE = re.compile(r"^[a-z0-9_-]+:[A-Za-z0-9._@/+-]+$")
```

Add a duplicate-domain guard at the top of the `for fn, doc in docs.items():` loop in `validate_schema` (track a `domains_seen` dict keyed by domain → filename):

```python
        dom = doc["domain"]
        if dom in domains_seen:
            errors.append(f"{fn}: domain {dom} already declared by "
                          f"{domains_seen[dom]}")
        domains_seen[dom] = fn
```

(declare `domains_seen = {}` beside `all_codes = {}`.)

Add the `automated_by` block inside the per-entry loop, after the `cwe` loop:

```python
            ab = e.get("automated_by")
            if ab is not None:
                if not isinstance(ab, list):
                    errors.append(f"{ctx}: automated_by must be a list")
                else:
                    for r in ab:
                        if not (isinstance(r, str) and AUTOMATED_BY_RE.match(r)):
                            errors.append(f"{ctx}: automated_by {r!r} must be "
                                          f"'tool:rule-id'")
```

Add a `see_also` target check in the post-loop pass that already validates `superseded_by`:

```python
        for ref in e.get("see_also") or []:
            if ref not in all_codes:
                errors.append(f"{code}: see_also {ref} does not exist")
```

- [ ] **Step 4: Fix the stale docstring**

In `tools/validate.py`, update the module docstring language that calls cross-domain duplicate names "WARNINGS until the single-homing rule … is ratified" — single-homing is now enforced by construction (clean rewrite); state that the check remains a mechanical backstop.

- [ ] **Step 5: Run tests + real catalog**

Run: `python3 tests/test_tools.py` (new tests PASS) and `python3 tools/validate.py` (real catalog still `0 error(s)`).

- [ ] **Step 6: Commit**

```bash
git add tools/validate.py tests/test_tools.py
git commit -m "feat(validate): see_also-target, duplicate-domain, automated_by checks"
```

---

### Task 3: Resolve the 19 same-hazard clusters (curation)

**Files:** Modify `domains/*.yml`, `tests/test_tools.py` (count assertions).

**Gate (not red-green):** after this task, an independent advisor re-check of the resolved clusters finds **0 surviving same-hazard duplicates**, `python3 tools/validate.py` is clean, and the count assertions match the new total.

- [ ] **Step 1: Apply each resolution from audit §1**

For each of the 19 clusters (17 cross-domain + 2 within-domain in the audit §1 tables), apply the clean-rewrite mechanism: keep the single home named by the advisor resolution, **remove** the duplicate entry from its domain file, fold the removed entry's distinct `examples`/`cwe` and its `recurrence` into the survivor, and set the survivor's severity by the R2 bar (resolving each LOW-vs-HIGH conflict). Remove within-category letter gaps only where the severity-ordering invariant would otherwise break. Record every removal (old code → survivor) in a scratch migration table `scratch/0.2-migration.md` for the CHANGELOG (Task 9) and the Gate A note.

- [ ] **Step 2: Validate + recount**

Run: `python3 tools/validate.py` → expect `0 error(s), 0 warning(s)` at the new (lower) entry count. Note that count.

- [ ] **Step 3: Thread the new count into the tests**

Update every `== 381` / `"381 entries"` assertion in `tests/test_tools.py` (the `TestValidateRealDraft`, `TestBundleBuild`, `TestValidateCli`, `TestCatalog` cases) to the count from Step 2. Also fix the stale `QAL-B2B` comment (audit §8) to match its assertion.

- [ ] **Step 4: Run suite**

Run: `python3 tests/test_tools.py` → all PASS.

- [ ] **Step 5: Independent advisor re-check (gate)**

Dispatch a read-only advisor over the resolved cluster codes: confirm no two surviving entries name the same hazard. Any survivor pair the advisor flags re-enters this task. Record the verdict in `scratch/0.2-migration.md`.

- [ ] **Step 6: Commit**

```bash
git add domains/ tests/test_tools.py
git commit -m "fix(taxonomy): resolve 19 same-hazard clusters (clean rewrite)"
```

---

### Task 4: Criteria for the confusable boundaries (curation)

**Files:** Modify `domains/*.yml`.

**Gate:** each of the 9 needs-criteria clusters (audit §2) has `criteria`; `python3 tools/validate.py` clean.

- [ ] **Step 1: Write criteria**

For each of the 9 clusters in audit §2 (and the highest-priority Appendix-B pairs the audit ranks), add a `criteria` field to each involved entry stating **positive qualification rules and nearest-neighbor exclusions** — never a restatement of the name. Apply the ARC↔QAL policy (Global Constraints) at that border. Example shape:

```yaml
    criteria: >-
      Qualifies when the same physical path is hardcoded independently in two or
      more modules (per-instance duplication). If the hazard is the module
      structure that permits the duplication, that is ARC-A5A (structural) — see_also.
```

- [ ] **Step 2: Validate + commit**

Run: `python3 tools/validate.py` (clean).
```bash
git add domains/
git commit -m "docs(taxonomy): criteria for the 9 confusable boundaries"
```

---

### Task 5: Populate `see_also` (curation)

**Files:** Modify `domains/*.yml`.

**Gate:** every settled near-miss pair from Tasks 3–4 carries `see_also`; the Task 2 target-existence check passes (no dangling references).

- [ ] **Step 1: Add the cross-references**

For each settled pair named in the §1 resolutions and the §2 criteria clusters, add `see_also: [<code>]` on both sides (mutual pointers). These are the routing hints the CHANGELOG promised but 0.1 never delivered.

- [ ] **Step 2: Validate + commit**

Run: `python3 tools/validate.py` (clean — the new see_also-target check confirms every reference resolves).
```bash
git add domains/
git commit -m "docs(taxonomy): populate see_also cross-references"
```

---

### Task 6: Provenance-vocabulary cleanup + truncated-example repair (curation)

**Files:** Modify `domains/*.yml`, `SCHEMA.md`.

**Gate:** provenance values are all drawn from the documented vocabulary; the 36 truncated examples are repaired; `python3 tools/validate.py` clean.

- [ ] **Step 1: Clean the provenance data (audit §3.3)**

Strip the 5 annotation-garbage values (`'incl. 1 test-quality-tagged'`, `'incl. 1 correctness-tagged'`, `'1 correctness-tagged'`, `'correctness-tagged'`, `'incl. 1 test-coverage-tagged'` — all QAL); move that information to `notes` if worth keeping. Fix the 2 bare `corpus` → `corpus-4x` (`COD-F1C`, `DAT-C1B`).

- [ ] **Step 2: Document the vocabulary in `SCHEMA.md`**

Add a controlled-vocabulary list to the provenance section: the legitimate values in use (`corpus-4x`, `prior-art`, `deep-gap-review`, `gemini-gap-review`, `code-simplifier-agent`, `receiving-code-review-skill`, `openssf-align`, `owasp-align`, and any others surviving Step 1). This list is what Task 7's validator check enforces.

- [ ] **Step 3: Repair truncated examples (audit §3.2)**

Restore or cleanly trim the 36 clipped examples across 26 entries (the ~110-char clip signature; list in `.panopticon/phase0-sweeps.txt` if present, else grep for examples ending mid-word). Trim to a clean sentence where the corpus original is unavailable.

- [ ] **Step 4: Validate + commit**

Run: `python3 tools/validate.py` (clean).
```bash
git add domains/ SCHEMA.md
git commit -m "docs(taxonomy): clean provenance vocab + repair truncated examples"
```

---

### Task 7: Validator hardening — provenance vocabulary check

**Files:** Modify `tools/validate.py`, `tests/test_tools.py`.

**Interfaces:** Produces a hard error for a provenance item not in the documented vocabulary. Runs *after* Task 6 so the real catalog passes.

- [ ] **Step 1: Write the failing test**

Add to `class TestValidateSyntheticErrors`:

```python
    def test_provenance_vocabulary(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-A1A"]["provenance"] = ["corpus-4x"]
        self.assertEqual(self._errs(d), [])
        d["x.yml"]["entries"]["SEC-A1A"]["provenance"] = ["incl. 1 correctness-tagged"]
        self.assertTrue(any("provenance" in e and "vocabulary" in e
                            for e in self._errs(d)), self._errs(d))
```

- [ ] **Step 2: Run to verify it fails**

Run: `python3 tests/test_tools.py` → new test FAILS.

- [ ] **Step 3: Implement**

In `tools/validate.py`, add the vocabulary set (mirroring the SCHEMA.md list from Task 6):

```python
PROVENANCE_VOCAB = {"corpus-4x", "prior-art", "deep-gap-review",
                    "gemini-gap-review", "code-simplifier-agent",
                    "receiving-code-review-skill", "openssf-align", "owasp-align"}
```

In the per-entry loop, after the existing provenance non-empty check:

```python
            for p in prov if isinstance(prov, list) else []:
                if p not in PROVENANCE_VOCAB:
                    errors.append(f"{ctx}: provenance {p!r} not in vocabulary")
```

- [ ] **Step 4: Run tests + real catalog**

Run: `python3 tests/test_tools.py` (PASS) and `python3 tools/validate.py` (clean — Task 6 made the data conform).

- [ ] **Step 5: Commit**

```bash
git add tools/validate.py tests/test_tools.py
git commit -m "feat(validate): enforce provenance controlled vocabulary"
```

---

### Task 8: Gate A domain-unpinned re-run (eval)

**Files:** Create `reviews/2026-08-11-gate-a-unpinned.md`.

**Gate:** three independent passes recorded; agreement reported against the pinned 91%/94% baseline.

- [ ] **Step 1: Build the sample**

Regenerate the Gate-C menu form from the cleaned catalog (`python3 tools/build_bundle.py --version 0.2.0-rc`) and draw a recurrence-weighted stratified sample of 100 findings, domain-**unpinned** (assigners see the whole menu, not a pinned domain).

- [ ] **Step 2: Run three independent passes**

Dispatch three independent sonnet advisors, each assigning a full OCRDb code to every sample finding from the whole menu. Collect the three code lists.

- [ ] **Step 3: Tabulate and record**

Compute full-code and category-prefix agreement across the three passes. Write `reviews/2026-08-11-gate-a-unpinned.md`: method, sample, the two agreement figures, disagreement analysis, and a comparison to the pinned 91%/94%. Any boundary still driving disagreement becomes a criteria follow-up (noted, not fixed here).

- [ ] **Step 4: Commit**

```bash
git add reviews/2026-08-11-gate-a-unpinned.md
git commit -m "docs(gate-a): domain-unpinned re-run on the clean base"
```

---

### Task 9: 0.2.0 release

**Files:** Create `build/ocrdb-0.2.0.*`; modify `CHANGELOG.md`, `.gitignore`.

- [ ] **Step 1: Ignore scratch**

Add `.panopticon/` and `.DS_Store` to `.gitignore`.

- [ ] **Step 2: Build the 0.2.0 artifacts (no cross-version baseline)**

Run: `python3 tools/build_bundle.py --version 0.2.0` (NO `--baseline` — the clean rewrite intentionally breaks 0.1.0 stability). Expect the new entry count, `0 errors`.

- [ ] **Step 3: Write the CHANGELOG 0.2.0 section**

Add `## 0.2.0`: the identity-base reset — 19 clusters resolved (with the migration table from `scratch/0.2-migration.md`), criteria + see_also added, provenance vocabulary controlled, governance aligned (freeze at 1.0), validator hardened, Gate A re-run recorded. State plainly that codes changed under the pre-1.0 mutability rule.

- [ ] **Step 4: Full suite + commit**

Run: `python3 tests/test_tools.py` (all PASS).
```bash
git add build/ CHANGELOG.md .gitignore
git commit -m "chore(release): 0.2.0 — clean identity base"
```

- [ ] **Step 5: Tag prep (maintainer performs the tag/PR)**

Branch ready for the 0.2.0 PR. The maintainer merges, then tags `v0.2.0` and cuts the release (attaching `build/ocrdb-0.2.0.*`), consistent with the 0.1.0 flow.

---

## Self-Review

**Spec coverage:** Phase 1 (governance)→Task 1; validator hardening (§5)→Tasks 2,7; Phase 2 (19 clusters)→Task 3; Phase 3 (criteria)→Task 4; Phase 4 (see_also)→Task 5; Phase 5 (provenance/examples)→Task 6; Phase 6 (Gate A)→Task 8; release→Task 9. The §6 open rulings (prior-art budget, A11Y/I18N grammar) and the deferred growth are correctly excluded per Global Constraints. The separable `build_catalog.py` `</script>` fix is NOT in this plan — tracked in the spec §7 as independent.

**Placeholder scan:** validator tasks carry real code; curation tasks reference the audit's concrete resolutions (§1/§2/§3) as their source of truth rather than restating them (DRY); the severity rule and ARC↔QAL policy are stated in Global Constraints. No "TBD"/"handle appropriately".

**Type/name consistency:** `AUTOMATED_BY_RE`, `PROVENANCE_VOCAB`, `domains_seen`, and the `see_also`/`superseded_by` post-loop pass all reference real `validate.py` structures; the test command is `python3 tests/test_tools.py` throughout; the count-assertion update (Task 3) is threaded before any later task re-runs the suite.

**Ordering check:** the provenance-vocabulary *enforcement* (Task 7) follows the provenance *data cleanup* (Task 6), so the validator never fails on un-cleaned data; the `see_also` *target check* (Task 2) precedes `see_also` *population* (Task 5), so typos are caught on write.
