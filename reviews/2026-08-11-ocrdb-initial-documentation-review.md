# OCRDb 0.1 — Initial Documentation Review

**Date:** 2026-08-11  
**Status:** Independent current-state review; no taxonomy rulings are made here.  
**Scope:** All top-level project documentation, domain YAML files, generated catalog artifacts, plans, specifications, and existing reviews.

## Executive assessment

OCRDb has a credible underlying model, but the released taxonomy is not yet dependable as a stable identity layer. The schema, deterministic build, and release mechanics are stronger than the current content curation and governance alignment.

The immediate risk is not missing coverage. It is identity ambiguity: the project promises stable codes and single-homed hazards while the current catalog contains unresolved same-hazard homes, no populated boundary criteria, and no cross-references. Adding more codes or broad automation mappings before resolving those conditions would increase the amount of stable metadata attached to unstable distinctions.

## What is working

### Clear scope and non-goals

The charter correctly separates a taxonomy's typical severity from a finding instance's severity and states that OCRDb is neither a scanner nor a severity oracle. That keeps the project from claiming authority it cannot provide.

### Useful identity mechanics

The following design choices are sound:

- Immutable released codes with correction through deprecation and `superseded_by`.
- A reserved `<DOM>-X0X` fallback that turns failed assignment into gap telemetry.
- Domain, area, category, and issue identifiers that are compact and sortable.
- Deterministic, versioned JSON, SARIF, menu, Markdown, and HTML artifacts.

### Evidence is disclosed

`provenance` and `recurrence` make corpus grounding inspectable. The project generally distinguishes mined evidence from prior-art additions rather than presenting all entries as equally observed.

### Reviews expose material defects

The existing gap analysis and catalog audit are concrete and unusually self-critical. In particular, the catalog audit supplies proposed deprecation paths rather than merely observing that boundaries are untidy.

## Findings

### P0 — The stability contract contradicts the project status

[`CHARTER.md`](../CHARTER.md) says the schema and codes may change freely until 1.0. [`SCHEMA.md`](../SCHEMA.md) says the stability contract activates at the 0.1 release tag, and [`CHANGELOG.md`](../CHANGELOG.md) says 0.1 codes are stable from that tag forward.

These positions cannot all govern the same release. The project needs one explicit answer to:

> Are 0.1 codes and names immutable, or may they still be rewritten before 1.0?

The current validator and changelog implement the first answer. The charter states the second.

### P0 — Single-homing is a promise, not a current property

The changelog says verified cross-domain duplicates were collapsed to one home with `see_also` references. The current catalog audit reports 19 advisor-verified same-hazard clusters in the shipped taxonomy, including several identical incidents under multiple codes and conflicting severities.

The validator still passes because its duplicate check compares exact entry names. It does not and realistically cannot establish semantic single-homing. The test named `test_single_homing_ratified_no_cross_domain_duplicates` therefore proves only that exact names are not reused across domains.

This distinction should be explicit in validation output and documentation. A clean schema validation is not evidence that single-homing holds.

### P0 — Stable assignment lacks its disambiguation layer

Current domain data contains:

- 381 entries
- 0 populated `definition` fields
- 0 populated `criteria` fields
- 0 populated `see_also` fields

Names and corpus examples carry the entire assignment burden. This is insufficient at the ARC/COD/QAL, ARC/SEC, AGT/ARC, and COD/DAT boundaries, where several entries describe the same incident from different perspectives.

The schema already supports the needed enrichment, so this can be corrected without changing the public shape. Criteria should state positive qualification rules and nearest-neighbor exclusions, not merely restate names.

### P0 — The strongest assignment evaluation remains incomplete

The recorded Gate A result achieved 91% full-code agreement, but findings were domain-pinned. The ratification document correctly notes that this does not test cross-domain ambiguity and defers a domain-unpinned rerun.

That rerun is more important after the catalog audit, not less. It should follow duplicate resolution and criteria enrichment; running it against the current catalog would mostly measure already-known ambiguity.

### P1 — The prior-art budget has two incompatible interpretations

The schema caps `prior-art` entries at 25% per domain. The changelog justifies the release using an approximately 19% catalog-wide figure. The catalog audit calculates that DAT, AGT, COD, and SEC exceed the per-domain limit under its stated method.

The project must either:

1. Retain the per-domain rule and corpus-ground or defer entries in affected domains.
2. Change the governance rule to a catalog-wide budget and explain why highly prior-art-dependent domains remain acceptable.
3. Replace the fixed percentage with domain-specific evidence requirements.

Until this is ruled, the 45 proposed gap additions cannot be evaluated consistently.

### P1 — Provenance is structured but not controlled

The validator requires a non-empty provenance list but does not validate its vocabulary. Current values include undocumented source labels, bare `corpus`, and annotation text such as `incl. 1 correctness-tagged` stored as if it were a source.

This weakens one of OCRDb's main credibility claims. Provenance values should be controlled identifiers; explanatory qualifiers belong in `notes` or a dedicated structured field.

### P1 — Declared domains do not fit the normative grammar

The code grammar requires a three-letter domain. `A11Y` and `I18N`, both declared as incubating domains, contain four characters and digits. They cannot produce valid OCRDb codes under the current grammar.

This should be resolved before either domain is seeded. Widening the grammar after consumers implement the current regex would be a schema compatibility event; choosing three-letter codes now is cheaper.

### P1 — Planning documents are already stale as progress records

The tool-rule implementation plan leaves all steps unchecked, but the `automated_by` regex validation, schema documentation, and tests are already present. The reverse-map build artifact is not present. The work is therefore partially implemented while the plan presents it as entirely unstarted.

The plan also instructs contributors to run:

```text
python3 -m unittest tests.test_tools -v
```

That command fails because `tests` is not a Python package. The working command is:

```text
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Plans in an actively changing repository should either be maintained as live ledgers or marked historical once execution begins.

### P1 — Tool-rule enrichment assumes clean identities

The tool-rule design maps each tool rule to the OCRDb code naming the same hazard. That assumption is invalid for unresolved duplicate homes. Enrichment performed now could attach rules to codes later deprecated as duplicate identities.

Resolve same-hazard clusters before the broad mapping pass. Mechanical support for the reverse map can proceed independently.

### P2 — Generated HTML treats taxonomy text as executable context

The HTML catalog interpolates serialized entry data into a `<script>` block without escaping the `</script>` sequence. Free-text examples can therefore terminate the script element and inject markup into the generated catalog. The same examples are included in the payload but are not rendered by the current interface.

Serialize for an HTML script context safely, or place JSON in a non-executable data element and parse its text content. Removing fields unused by the catalog would also reduce the generated artifact size.

### P2 — Example quality is uneven

Several corpus examples are clipped mid-word or mid-sentence. DAT is almost entirely prior-art-seeded and lacks concrete examples. These conditions do not invalidate the entries, but they make assignment materially harder in exactly the domains where external validation is weakest.

## Recommended execution order

1. Rule whether 0.1 identities are immutable and align the charter, schema, and changelog.
2. Resolve the 19 verified same-hazard clusters through the existing deprecation mechanism.
3. Add criteria for the highest-confusion sibling and cross-domain boundaries.
4. Populate `see_also` for legitimate adjacent hazards and deprecated homes.
5. Clean and validate the provenance vocabulary; rule the prior-art budget.
6. Rerun Gate A without domain pinning.
7. Complete the tool-rule enrichment and reverse-map artifact.
8. Consider new gap codes only after the identity and evidence rules are stable.

## Verification performed

At the time of this review:

- `python3 tools/validate.py` passes with 381 entries, 0 errors, and 0 warnings.
- Stability validation against `build/ocrdb-0.1.0.json` passes.
- Test discovery runs 19 tests successfully.
- Tests emit existing unclosed-file `ResourceWarning` diagnostics.
- The documented module-style unittest command fails to import `tests.test_tools`.
- The working tree contains an untracked catalog audit and `.panopticon/` review artifacts; audit findings are treated as proposals until ratified.

## Bottom line

OCRDb is a credible curation system and a useful 0.1 research artifact. It is not yet a trustworthy standard for durable finding identity. The next increment should reduce ambiguity and align governance with reality, not maximize entry count.