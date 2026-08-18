# Security Policy

OCRDb is two things: a **data catalog** (the `domains/*.yml` taxonomy and the built
`build/` artifacts) and a small amount of **tooling** (`tools/*.py` — validate, build,
catalog). This policy covers both.

## Reporting a vulnerability

Please report security issues **privately**, not in a public issue:

- Preferred: open a [private security advisory](https://github.com/panopticon-scanner/ocrdb/security/advisories/new)
  on this repository (GitHub's confidential vulnerability reporting).
- Alternatively, contact the maintainer [@psyberone](https://github.com/psyberone).

We aim to acknowledge a report within a few days and to keep you informed as we work
on a fix. Please give us a reasonable window to address the issue before any public
disclosure.

## What is in scope

- **Tooling** (`tools/*.py`): e.g. code injection, unsafe deserialization, path
  traversal, or output-generation issues (the catalog HTML/SARIF generators) that
  could be triggered by a crafted `domains/` file or bundle.
- **Build/release integrity**: anything that could cause the build to ship content it
  did not validate.

## What is *not* a vulnerability

- **The catalog contains vulnerability descriptions, CVE/CWE references, and examples
  by design** — it is a taxonomy *of* code-review findings. A code that describes a
  hazard is data, not a live exploit.
- **`tests/fixtures/` are deliberately vulnerable** (planted dependencies and code)
  used to exercise scanner adapters. Their vulnerabilities are intentional test
  material, not a security issue in OCRDb.

## Supported versions

Only the latest release is supported. Security fixes ship in a new release; see
[`CHANGELOG.md`](CHANGELOG.md).
