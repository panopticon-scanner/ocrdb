# Contributing to OCRDb

OCRDb is an open, hierarchical, severity-graded database of **code-review finding
types** — the CWE/NVD analogue for everything code review surfaces. Thanks for
helping build it. Please read [`CHARTER.md`](CHARTER.md) (what OCRDb is and is not)
and [`SCHEMA.md`](SCHEMA.md) (the normative entry format and stability contract)
first; this file is the practical how-to.

> **Status: incubating (pre-1.0).** Codes are held stable *within* a release but
> may change between releases until the 1.0 freeze. See the stability contract in
> `SCHEMA.md`.

## The shape of a code

Every code is `DOMAIN-AREA CAT ISSUE`, e.g. `SEC-A2D`:

- **Domain** — one of the ten ratified domains (`SEC COD ARC TST QAL AGT DAT OPS ACC LNG`).
- **Area** (a letter) and **category** (a digit) group related hazards.
- **Issue** (a letter) names one defect type, letter-ordered by typical severity.

A code carries a lean core (`name`, `default_severity`, `status`, `provenance`) plus
optional enrichment (`criteria`, `cwe`, `see_also`, `examples`, `automated_by`, …).
See `SCHEMA.md` for the full field list and rules.

## How codes get added

OCRDb grows through **owner-adjudicated calibration**, not direct edits to the
catalog. Reviewers and tools *cite* codes; they do not have write privilege over the
taxonomy. New codes come from evidence:

1. **Propose** — open an issue using the **Code proposal** template. Give the domain,
   a kebab-case name, the area/category it belongs under, a proposed severity, the
   `provenance`, and — the deciding evidence — **`would_file_as`**: the existing code
   or domain you would have used if your proposal did not exist (`none` if nothing
   fits). Homelessness is what distinguishes a real gap from a duplicate.
2. **Adjudicate** — proposals are triaged and adjudicated against the existing
   catalog (dedup, single-homing, severity calibration, prior-art budget). Accepted
   ones are folded into a release; the rest are absorbed into their named home.
3. **Ship** — accepted codes land in a versioned release with a `CHANGELOG` entry.

Small fixes (typos, a missing `criteria`, a `cwe` correction, an added `example`) can
come as a direct PR without an issue.

## Provenance and evidence

`provenance` records *how a code is grounded* — see the current vocabulary in
`tools/validate.py` (`PROVENANCE_VOCAB`). Two rules to know:

- **Grounding budget.** Each domain must keep entries that rest on `prior-art` alone
  (no `corpus`/`tool-observed` backing) at or below 25%. Over-budget is a warning
  now; it becomes a hard error at 1.0.
- **Proof-required tiers.** A `proof-backed` entry (a ground-truth finding with a
  passing executable exploit proof) **must** carry that proof as an `example`; the
  validator rejects one that does not.

## Invariants the catalog holds

- **Single-homing** — one hazard, one code. Cross-domain duplicate names are flagged.
- **Stability** — within a release, codes never change `name` or reused numbers;
  corrections are `status: deprecated` + `superseded_by`, never deletion (enforced by
  `validate.py --baseline`).
- **Determinism** — the build artifacts are byte-identical across runs.

## Development

```bash
pip install pyyaml
python3 tools/validate.py                       # schema + single-homing + budgets
python3 -m unittest discover -s tests           # or: python3 -m pytest tests/ -q
```

Building a release bundle (maintainers):

```bash
python3 tools/build_bundle.py --version <X.Y.Z> --baseline build/ocrdb-<prev>.json
python3 tools/build_catalog.py --bundle build/ocrdb-<X.Y.Z>.json --out . --html-out build
```

A PR must keep `validate.py` at **0 errors**, the test suite green, and — for catalog
changes — the stability check clean against the previous release bundle. The `validate`
GitHub check runs both on every PR and must pass before merge.

## Licensing

By contributing you agree that catalog content is licensed **CC BY-SA 4.0** and tooling
code **MIT** (see [`LICENSE`](LICENSE)). Contributions must be your own work or
properly attributed.
