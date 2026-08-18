<!-- Thanks for contributing to OCRDb! See CONTRIBUTING.md. -->

## What & why

<!-- One or two sentences. Link the code-proposal issue if this lands one. -->

## Checklist

- [ ] `python3 tools/validate.py` passes (**0 errors**).
- [ ] Tests pass (`python3 -m unittest discover -s tests`).
- [ ] **Catalog changes only:** built with `--baseline build/ocrdb-<prev>.json`; the
      prior codes stay byte-identical on `name`/`default_severity` (stability contract).
- [ ] **New codes:** single-homed, carry `criteria` (qualification + nearest-neighbor
      exclusion), valid `provenance` (a `proof-backed` entry carries its proof as an
      `example`).
- [ ] `CHANGELOG.md` updated.
- [ ] **Release PR only:** `build/ocrdb-<X.Y.Z>.{json,sarif.json,-menus.md,html}` and
      `CATALOG.md` regenerated and committed.
