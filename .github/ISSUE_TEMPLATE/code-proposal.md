---
name: Code proposal
about: Propose a new finding-type code (or a change to an existing one)
title: "[code] <domain>-<area><cat><issue>? <proposed-name>"
labels: code-proposal
---

<!-- See CONTRIBUTING.md and SCHEMA.md before filing. Homelessness (would_file_as)
     is the deciding evidence — a proposal without it is hard to adjudicate. -->

## Proposed code

- **Domain:** <!-- one of SEC COD ARC TST QAL AGT DAT OPS ACC LNG -->
- **Proposed name (kebab-case):** <!-- e.g. missing-object-level-authorization -->
- **Area / category it belongs under:** <!-- e.g. C1 access-control (or "new area, because…") -->
- **Proposed default_severity:** <!-- INFO | LOW | MEDIUM | HIGH | CRITICAL -->
- **Provenance:** <!-- corpus | tool-observed | gap-review | prior-art | *-align | proof-backed -->

## would_file_as (the deciding evidence)

<!-- The EXISTING OCRDb code or domain you would have used if this proposal did not
     exist, or `none` if nothing in the catalog fits. Be specific. -->

## Evidence

<!-- Where have you seen this? Real-repo occurrences, a tool rule that flags it, a
     standard (CWE/OWASP/…), or — for proof-backed — a passing executable proof.
     Cite paths/links. -->

## Why it is distinct

<!-- What is the nearest existing code, and why does it not cover this? (fix differs,
     trust boundary differs, etc.) This becomes the `criteria` exclusion clause. -->
