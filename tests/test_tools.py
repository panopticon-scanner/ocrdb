import copy
import glob
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import build_bundle  # noqa: E402
import validate  # noqa: E402


def _real_docs():
    return validate.load_domains(os.path.join(ROOT, "domains"))


def _codes():
    docs = _real_docs()
    return {c: e for d in docs.values() for c, e in (d.get("entries") or {}).items()}


class TestValidateRealDraft(unittest.TestCase):
    def test_draft_has_no_schema_errors(self):
        errors, warnings, codes = validate.validate_schema(_real_docs())
        self.assertEqual(errors, [])
        self.assertEqual(len(codes), 390)

    def test_single_homing_ratified_no_cross_domain_duplicates(self):
        # Ratified 0.1: single-homing (big rock #0) resolved every cross-domain
        # duplicate, so the validator surfaces NO duplicate-name warnings.
        _, warnings, _ = validate.validate_schema(_real_docs())
        dup = [w for w in warnings if "cross-domain duplicate" in w]
        self.assertEqual(dup, [], dup)

    def test_ops_domain_seeded(self):
        codes = _codes()
        ops = {c: e for c, e in codes.items() if c.startswith("OPS-")}
        self.assertEqual(sorted(ops), [
            "OPS-A1A", "OPS-A1B", "OPS-B1A", "OPS-B1B", "OPS-C1A",
            "OPS-C1B", "OPS-D1A", "OPS-D1B", "OPS-E1A"])
        for e in ops.values():
            self.assertEqual(e["status"], "active")
            self.assertEqual(e["provenance"], ["corpus"])
            self.assertIn(e["default_severity"],
                          {"CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"})

    def test_acc_domain_seeded(self):
        codes = _codes()
        acc = sorted(c for c in codes if c.startswith("ACC-"))
        self.assertEqual(acc, ["ACC-A1A", "ACC-A1B", "ACC-B1A", "ACC-B1B",
                               "ACC-C1A", "ACC-D1A", "ACC-E1A", "ACC-F1A"])
        self.assertEqual(codes["ACC-A1A"]["default_severity"], "HIGH")

    def test_lng_domain_seeded(self):
        codes = _codes()
        lng = sorted(c for c in codes if c.startswith("LNG-"))
        self.assertEqual(lng, ["LNG-A1A", "LNG-A1B", "LNG-B1A", "LNG-B1B",
                               "LNG-C1A", "LNG-D1A", "LNG-E1A", "LNG-F1A"])
        self.assertEqual(codes["LNG-E1A"].get("cwe"), ["CWE-176"])

    def test_new_cross_domain_see_also_reciprocal(self):
        codes = _codes()

        def sa(c):
            return set(codes[c].get("see_also") or [])
        # confirmed edges
        self.assertIn("SEC-F2A", sa("OPS-A1A"))
        self.assertIn("OPS-A1A", sa("SEC-F2A"))
        self.assertIn("COD-B2C", sa("OPS-E1A"))
        self.assertIn("OPS-E1A", sa("COD-B2C"))
        # every see_also target on a new code must be a real code
        for c in [k for k in codes if k[:3] in ("OPS", "ACC", "LNG")]:
            for t in (codes[c].get("see_also") or []):
                self.assertIn(t, codes, f"{c} see_also {t} missing")


class TestValidateSyntheticErrors(unittest.TestCase):
    def _base_doc(self):
        return {"x.yml": {
            "domain": "SEC", "name": "security",
            "areas": {"A": {"name": "a", "categories": {"1": "c"}}},
            "entries": {"SEC-A1A": {
                "name": "ok-entry", "default_severity": "LOW",
                "status": "active", "provenance": ["corpus"]}}}}

    def _errs(self, docs):
        return validate.validate_schema(docs)[0]

    def test_clean_base(self):
        self.assertEqual(self._errs(self._base_doc()), [])

    def test_bad_grammar_and_wrong_domain(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-11A"] = d["x.yml"]["entries"]["SEC-A1A"]
        d["x.yml"]["entries"]["COD-A1A"] = dict(
            d["x.yml"]["entries"]["SEC-A1A"], name="other-entry")
        errs = self._errs(d)
        self.assertTrue(any("grammar" in e for e in errs), errs)
        self.assertTrue(any("!= file domain" in e for e in errs), errs)

    def test_unknown_area_and_category(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-B1A"] = dict(
            d["x.yml"]["entries"]["SEC-A1A"], name="b-entry")
        d["x.yml"]["entries"]["SEC-A2A"] = dict(
            d["x.yml"]["entries"]["SEC-A1A"], name="a2-entry")
        errs = self._errs(d)
        self.assertTrue(any("area B not in areas header" in e for e in errs), errs)
        self.assertTrue(any("category 2 not under area A" in e for e in errs), errs)

    def test_enum_and_provenance_and_deprecation(self):
        d = self._base_doc()
        e = d["x.yml"]["entries"]["SEC-A1A"]
        e.update(default_severity="SEVERE", status="retired", provenance=[],
                 name="Bad Name")
        errs = self._errs(d)
        for frag in ("default_severity", "status", "provenance", "kebab-case"):
            self.assertTrue(any(frag in x for x in errs), (frag, errs))

    def test_deprecated_requires_existing_superseded_by(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-A1A"].update(status="deprecated")
        errs = self._errs(d)
        self.assertTrue(any("without superseded_by" in e for e in errs), errs)
        d["x.yml"]["entries"]["SEC-A1A"].update(superseded_by="SEC-A9Z")
        errs = self._errs(d)
        self.assertTrue(any("does not exist" in e for e in errs), errs)

    def test_same_domain_duplicate_name_is_error(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-A1B"] = dict(
            d["x.yml"]["entries"]["SEC-A1A"])  # same name, same domain
        errs = self._errs(d)
        self.assertTrue(any("used by" in e for e in errs), errs)

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

    def test_provenance_vocabulary(self):
        d = self._base_doc()
        d["x.yml"]["entries"]["SEC-A1A"]["provenance"] = ["corpus"]
        self.assertEqual(self._errs(d), [])
        d["x.yml"]["entries"]["SEC-A1A"]["provenance"] = ["coderabbit"]
        self.assertTrue(any("provenance" in e and "vocabulary" in e
                            for e in self._errs(d)), self._errs(d))

    def test_automated_by_shape(self):
        d = self._base_doc()
        e = d["x.yml"]["entries"]["SEC-A1A"]
        e["automated_by"] = ["ruff:B006", "eslint:@typescript-eslint/no-explicit-any"]
        self.assertEqual(self._errs(d), [])
        for bad in ("ruff B006", ":B006", "ruff:", 123):
            e["automated_by"] = [bad]
            self.assertTrue(any("automated_by" in x for x in self._errs(d)), bad)


class TestGovernanceDocs(unittest.TestCase):
    def test_domain_banners_not_falsely_ratified(self):
        for f in glob.glob(os.path.join(ROOT, "domains", "*.yml")):
            first = open(f, encoding="utf-8").readline()
            self.assertNotIn("RATIFIED", first, f)
            self.assertIn("INCUBATING", first, f)

    def test_schema_lists_all_active_and_incubating_domains(self):
        # 0.3.0: OPS/ACC/LNG activated — the roster is 10 active, 0 declared-
        # not-seeded. The old "Incubating (declared, not yet seeded):" clause
        # is gone (see test_schema_activates_ten_domains_and_has_routing_note).
        schema = open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8").read()
        self.assertIn("Active set:", schema)
        self.assertNotIn("Incubating (declared, not yet seeded):", schema)
        for dom in ("SEC", "COD", "ARC", "TST", "QAL", "AGT", "DAT",
                    "OPS", "ACC", "LNG"):
            self.assertIn(f"`{dom}`", schema, dom)

    def test_schema_carries_r2_severity_rubric(self):
        schema = open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8").read()
        self.assertIn("exploitable now, data loss, or silently wrong", schema)

    def test_renamed_incubating_domains_everywhere(self):
        for name in ("CHARTER.md", "CHANGELOG.md", "RATIFICATION.md", "SCHEMA.md"):
            text = open(os.path.join(ROOT, name), encoding="utf-8").read()
            self.assertNotIn("A11Y", text, name)
            self.assertNotIn("I18N", text, name)

    def test_schema_activates_ten_domains_and_has_routing_note(self):
        schema = open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8").read()
        self.assertNotIn("Incubating (declared, not yet seeded)", schema)
        self.assertIn("Domain routing for overlapping hazards", schema)
        for rule in ("external", "systemic", "fail-open", "error-swallow",
                     "assistive", "locale"):
            self.assertIn(rule, schema.lower())

    def test_charter_reflects_ops_acc_lng_activation(self):
        # CHARTER<->active parity guard: OPS/ACC/LNG are seeded and active
        # (0.3.0) — the charter must not still call them "not yet seeded".
        charter = open(os.path.join(ROOT, "CHARTER.md"), encoding="utf-8").read()
        self.assertNotIn("not yet seeded", charter)
        for dom in ("OPS", "ACC", "LNG"):
            self.assertIn(f"`{dom}`", charter, dom)


class TestStabilityContract(unittest.TestCase):
    def _baseline(self, tmp, entries):
        path = os.path.join(tmp, "base.json")
        with open(path, "w") as fh:
            json.dump({"domains": {"SEC": {"entries": entries}}}, fh)
        return path

    def test_gone_and_renamed_codes_fail(self):
        cur = {"SEC-A1A": {"name": "kept-entry"},
               "SEC-A1B": {"name": "renamed-now"}}
        with tempfile.TemporaryDirectory() as tmp:
            base = self._baseline(tmp, {
                "SEC-A1A": {"name": "kept-entry"},
                "SEC-A1B": {"name": "original-name"},
                "SEC-A1C": {"name": "vanished-entry"}})
            errs = validate.validate_stability(cur, base)
        self.assertEqual(len(errs), 2)
        self.assertTrue(any("GONE" in e for e in errs), errs)
        self.assertTrue(any("renamed" in e for e in errs), errs)

    def test_deprecation_is_sanctioned(self):
        cur = {"SEC-A1A": {"name": "kept-entry", "status": "deprecated",
                           "superseded_by": "SEC-A1B"},
               "SEC-A1B": {"name": "new-entry"}}
        with tempfile.TemporaryDirectory() as tmp:
            base = self._baseline(tmp, {"SEC-A1A": {"name": "kept-entry"}})
            self.assertEqual(validate.validate_stability(cur, base), [])


class TestBundleBuild(unittest.TestCase):
    def test_build_is_deterministic_and_complete(self):
        with tempfile.TemporaryDirectory() as tmp:
            out1, out2 = os.path.join(tmp, "b1"), os.path.join(tmp, "b2")
            for out in (out1, out2):
                with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                    rc = build_bundle.main(["--version", "0.0.0-test",
                                            "--domains-dir",
                                            os.path.join(ROOT, "domains"),
                                            "--out", out])
                self.assertEqual(rc, 0)
            for fn in os.listdir(out1):
                with open(os.path.join(out1, fn), "rb") as f1, \
                        open(os.path.join(out2, fn), "rb") as f2:
                    self.assertEqual(f1.read(), f2.read(), fn)
            bundle = json.load(open(os.path.join(out1, "ocrdb-0.0.0-test.json")))
            n = sum(len(d["entries"]) for d in bundle["domains"].values())
            self.assertEqual(n, 390)
            self.assertEqual(bundle["license"], "CC BY-SA 4.0")

    def test_sarif_taxa_match_entries_and_levels(self):
        docs = _real_docs()
        bundle = build_bundle.build_bundle(docs, "0.0.0-test")
        sarif = build_bundle.build_sarif(bundle)
        taxa = sarif["runs"][0]["taxonomies"][0]["taxa"]
        self.assertEqual(len(taxa), 390)
        by_id = {t["id"]: t for t in taxa}
        # SEC-A3A is CRITICAL -> error; QAL-B2A is LOW -> note
        self.assertEqual(by_id["SEC-A3A"]["defaultConfiguration"]["level"], "error")
        self.assertEqual(by_id["QAL-B2A"]["defaultConfiguration"]["level"], "note")

    def test_menus_gate_c_form(self):
        bundle = build_bundle.build_bundle(_real_docs(), "0.0.0-test")
        menus = build_bundle.build_menus(bundle)
        self.assertIn("# MENU SEC (security)", menus)
        self.assertIn("SEC-A3A sql-injection-via-string-concatenation (CRITICAL)",
                      menus)
        # criteria/definition text never leaks into menus (Gate C)
        self.assertNotIn("qualifies when", menus)

    def test_menus_exclude_deprecated(self):
        docs = copy.deepcopy(_real_docs())
        for doc in docs.values():
            if doc["domain"] == "SEC":
                doc["entries"]["SEC-A3A"].update(status="deprecated",
                                                 superseded_by="SEC-A1B")
        bundle = build_bundle.build_bundle(docs, "0.0.0-test")
        menus = build_bundle.build_menus(bundle)
        self.assertNotIn("SEC-A3A ", menus)

    def test_build_aborts_on_schema_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            dom_dir = os.path.join(tmp, "domains")
            os.makedirs(dom_dir)
            with open(os.path.join(dom_dir, "bad.yml"), "w") as fh:
                fh.write("domain: SEC\nname: security\nareas: {}\n"
                         "entries:\n  SEC-A1A: {name: x, default_severity: NOPE,"
                         " status: active, provenance: [c]}\n")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                rc = build_bundle.main(["--version", "0.0.0-test",
                                        "--domains-dir", dom_dir,
                                        "--out", os.path.join(tmp, "out")])
            self.assertEqual(rc, 1)
            self.assertFalse(os.path.exists(os.path.join(tmp, "out")))


class TestValidateCli(unittest.TestCase):
    def test_cli_passes_on_real_draft(self):
        proc = subprocess.run(
            [sys.executable, os.path.join(ROOT, "tools", "validate.py"),
             "--domains-dir", os.path.join(ROOT, "domains")],
            capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn("390 entries", proc.stdout)


class TestBundleSchemaVersion(unittest.TestCase):
    def test_bundle_carries_schema_version(self):
        bundle = build_bundle.build_bundle(_real_docs(), "0.0.0-test")
        self.assertEqual(bundle["schema_version"], "1.0")
        # distinct from the catalog version
        self.assertEqual(bundle["version"], "0.0.0-test")

    def test_committed_020_bundle_has_schema_version(self):
        b = json.load(open(os.path.join(ROOT, "build", "ocrdb-0.2.0.json")))
        self.assertEqual(b["schema_version"], "1.0")
        self.assertEqual(b["version"], "0.2.0")


class TestFallbackGrammar(unittest.TestCase):
    def test_fallback_recognizes_all_domains(self):
        for dom in ("SEC", "COD", "ARC", "TST", "QAL", "AGT", "DAT",
                    "OPS", "ACC", "LNG"):
            self.assertTrue(validate.is_fallback_code(f"{dom}-X0X"), dom)

    def test_fallback_rejects_non_sentinels(self):
        for bad in ("SEC-A1A", "SEC-X1X", "SEC-X0A", "ZZZ-X0X", "SEC-X0X-EXTRA"):
            self.assertFalse(validate.is_fallback_code(bad), bad)

    def test_real_code_and_sentinel_are_disjoint(self):
        # A real entry code never matches the fallback grammar, and X0X never
        # matches the strict entry grammar.
        self.assertTrue(validate.CODE_RE.match("SEC-A2D"))
        self.assertIsNone(validate.CODE_RE.match("SEC-X0X"))
        self.assertFalse(validate.is_fallback_code("SEC-A2D"))


class TestCatalog(unittest.TestCase):
    def _bundle(self, tmp):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            build_bundle.main(["--version", "0.0.0-test",
                               "--domains-dir", os.path.join(ROOT, "domains"),
                               "--out", tmp])
        return os.path.join(tmp, "ocrdb-0.0.0-test.json")

    def test_catalog_views_are_complete_and_deterministic(self):
        import build_catalog, json
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self._bundle(tmp)
            a, b = os.path.join(tmp, "a"), os.path.join(tmp, "b")
            os.makedirs(a); os.makedirs(b)
            for d in (a, b):
                with redirect_stdout(io.StringIO()):
                    build_catalog.main(["--bundle", bundle, "--out", d, "--html-out", d])
            md = open(os.path.join(a, "CATALOG.md"), encoding="utf-8").read()
            html = open(os.path.join(a, "ocrdb-0.0.0-test.html"), encoding="utf-8").read()
            codes = [c for dom in json.load(open(bundle))["domains"].values()
                     for c in dom["entries"]]
            self.assertEqual(len(codes), 390)
            for c in codes:
                self.assertIn(c, md, c)
                self.assertIn(c, html, c)
            # byte-identical re-run
            self.assertEqual(open(os.path.join(a, "CATALOG.md"), "rb").read(),
                             open(os.path.join(b, "CATALOG.md"), "rb").read())
            self.assertEqual(open(os.path.join(a, "ocrdb-0.0.0-test.html"), "rb").read(),
                             open(os.path.join(b, "ocrdb-0.0.0-test.html"), "rb").read())

    def test_html_is_self_contained(self):
        import build_catalog
        with tempfile.TemporaryDirectory() as tmp:
            bundle = self._bundle(tmp)
            with redirect_stdout(io.StringIO()):
                build_catalog.main(["--bundle", bundle, "--out", tmp, "--html-out", tmp])
            html = open(os.path.join(tmp, "ocrdb-0.0.0-test.html"), encoding="utf-8").read()
            for external in ("http://", "https://", "src=", "cdn"):
                self.assertNotIn(external, html.lower().replace("initial-scale", ""))


class TestMigrationMap(unittest.TestCase):
    def _codes(self, name):
        b = json.load(open(os.path.join(ROOT, "build", name)))
        return {c for dom in b["domains"].values() for c in dom["entries"]}

    def _build(self):
        import build_migration
        return build_migration.build_migration(
            os.path.join(ROOT, "migrations", "0.1.0-to-0.2.0.md"),
            os.path.join(ROOT, "build", "ocrdb-0.1.0.json"),
            os.path.join(ROOT, "build", "ocrdb-0.2.0.json"),
            "0.1.0", "0.2.0")

    def test_24_mappings_header_and_crosscheck(self):
        m = self._build()
        self.assertEqual(m["schema_version"], "1.0")
        self.assertEqual(m["from_version"], "0.1.0")
        self.assertEqual(m["to_version"], "0.2.0")
        self.assertEqual(len(m["mappings"]), 24)
        old, new = self._codes("ocrdb-0.1.0.json"), self._codes("ocrdb-0.2.0.json")
        self.assertEqual({mp["old_code"] for mp in m["mappings"]}, old - new)
        for mp in m["mappings"]:
            self.assertNotIn(mp["old_code"], new)
            self.assertEqual(mp["disposition"],
                             "folded" if mp["survivors"] else "removed")
            for s in mp["survivors"]:
                self.assertIn(s, new)  # every survivor is a real 0.2.0 code

    def test_multi_survivor_rows_captured(self):
        m = {mp["old_code"]: mp["survivors"] for mp in self._build()["mappings"]}
        self.assertEqual(sorted(m["SEC-G1A"]), ["COD-C1A", "COD-C1B"])
        self.assertEqual(sorted(m["QAL-A1A"]), ["TST-C3B", "TST-C3C"])

    def test_see_also_annotation_not_captured_as_survivor(self):
        m = {mp["old_code"]: mp["survivors"] for mp in self._build()["mappings"]}
        self.assertEqual(m["QAL-F3A"], ["TST-C4B"])

    def test_committed_artifact_matches_generator(self):
        committed = json.load(
            open(os.path.join(ROOT, "build", "ocrdb-0.2.0-migration.json")))
        self.assertEqual(committed, self._build())


class TestNewValidateChecks(unittest.TestCase):
    def _two_entry_doc(self):
        return {"x.yml": {
            "domain": "SEC", "name": "security",
            "areas": {"A": {"name": "a", "categories": {"1": "c"}}},
            "entries": {
                "SEC-A1A": {"name": "e1", "default_severity": "LOW",
                            "status": "active", "provenance": ["corpus"]},
                "SEC-A1B": {"name": "e2", "default_severity": "LOW",
                            "status": "active", "provenance": ["corpus"]}}}}

    def test_real_catalog_passes_symmetry(self):
        errors, _, _ = validate.validate_schema(_real_docs())
        self.assertEqual(errors, [], errors)

    def test_see_also_must_be_reciprocal(self):
        d = self._two_entry_doc()
        d["x.yml"]["entries"]["SEC-A1A"]["see_also"] = ["SEC-A1B"]  # one-way
        errs = validate.validate_schema(d)[0]
        self.assertTrue(any("reciprocal" in e for e in errs), errs)
        # make it mutual -> clean
        d["x.yml"]["entries"]["SEC-A1B"]["see_also"] = ["SEC-A1A"]
        self.assertEqual(validate.validate_schema(d)[0], [])

    def test_domain_parity_clean_on_real_catalog(self):
        self.assertEqual(validate.domain_parity_errors(_real_docs()), [])

    def test_domain_parity_flags_missing_domain(self):
        docs = _real_docs()
        del docs["sec.yml"]  # a whole domain file vanished
        errs = validate.domain_parity_errors(docs)
        self.assertTrue(any("domain-list parity" in e and "SEC" in e
                            for e in errs), errs)

    def test_default_severity_drift_flagged(self):
        cur = {"SEC-A1A": {"name": "kept", "default_severity": "HIGH"}}
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "base.json")
            with open(path, "w") as fh:
                json.dump({"domains": {"SEC": {"entries": {
                    "SEC-A1A": {"name": "kept", "default_severity": "LOW"}}}}}, fh)
            errs = validate.validate_stability(cur, path)
        self.assertTrue(any("default_severity" in e for e in errs), errs)


class TestDatExpansion(unittest.TestCase):
    def _dat(self):
        import validate
        docs = validate.load_domains(os.path.join(ROOT, "domains"))
        return docs["dat.yml"]["entries"]

    def test_new_codes_present_and_corpus(self):
        e = self._dat()
        new = ["DAT-F1A", "DAT-F1B", "DAT-F1C", "DAT-F2A", "DAT-F2B",
               "DAT-B1E", "DAT-B1F", "DAT-E1D"]
        for c in new:
            self.assertIn(c, e, c)
            self.assertIn("corpus", e[c]["provenance"], c)
            self.assertTrue(e[c].get("examples"), f"{c} needs >=1 example")

    def test_area_f_declared(self):
        import validate
        d = validate.load_domains(os.path.join(ROOT, "domains"))["dat.yml"]
        self.assertIn("F", d["areas"])
        self.assertEqual(d["areas"]["F"]["name"], "durable-file-and-local-state")

    def test_area_a_backfilled_from_corpus(self):
        e = self._dat()
        grounded = ["DAT-A1B", "DAT-A1C", "DAT-A1D"]
        for c in grounded:
            self.assertIn("corpus", e[c]["provenance"], c)
            self.assertTrue(e[c].get("examples"), f"{c} needs >=1 example")

    def test_area_b_backfilled_from_corpus(self):
        e = self._dat()
        grounded = ["DAT-B1A", "DAT-B1B", "DAT-B1C", "DAT-B1D"]
        for c in grounded:
            self.assertIn("corpus", e[c]["provenance"], c)
            self.assertTrue(e[c].get("examples"), f"{c} needs >=1 example")

    def test_area_c_backfilled_from_corpus(self):
        e = self._dat()
        grounded = ["DAT-C1A", "DAT-C1B", "DAT-C1C", "DAT-C1D"]
        for c in grounded:
            self.assertIn("corpus", e[c]["provenance"], c)
            self.assertTrue(e[c].get("examples"), f"{c} needs >=1 example")

    def test_areas_d_e_backfilled_from_corpus(self):
        e = self._dat()
        grounded = ["DAT-D1B", "DAT-D1C", "DAT-D1D",
                    "DAT-E1A", "DAT-E1B", "DAT-E1C"]
        for c in grounded:
            self.assertIn("corpus", e[c]["provenance"], c)
            self.assertTrue(e[c].get("examples"), f"{c} needs >=1 example")


class TestPriorArtBudget(unittest.TestCase):
    def test_ungrounded_prior_art_over_25pct_flags(self):
        # 4 entries in a domain, 2 ungrounded prior-art (50%) -> over budget
        codes = {
            "SEC-A1A": {"provenance": ["prior-art"]},
            "SEC-A1B": {"provenance": ["prior-art", "gap-review"]},
            "SEC-A1C": {"provenance": ["prior-art", "corpus"]},   # grounded, excluded
            "SEC-A1D": {"provenance": ["corpus"]},                 # not prior-art
        }
        issues = validate.prior_art_budget_issues(codes)
        self.assertTrue(any("SEC" in i and "budget" in i for i in issues), issues)

    def test_grounded_prior_art_within_budget(self):
        codes = {f"SEC-A1{c}": {"provenance": ["prior-art", "corpus"]}
                 for c in "ABCD"}
        self.assertEqual(validate.prior_art_budget_issues(codes), [])

    def test_real_catalog_dat_within_budget_after_backfill(self):
        import validate
        docs = validate.load_domains(os.path.join(ROOT, "domains"))
        _, _, all_codes = validate.validate_schema(docs)
        issues = validate.prior_art_budget_issues(all_codes)
        self.assertFalse(any("DAT" in i for i in issues), issues)


class TestDispositionVocab(unittest.TestCase):
    def _schema_terms(self, header):
        import re
        text = open(os.path.join(ROOT, "SCHEMA.md"), encoding="utf-8").read()
        start = text.index(header)
        rest = text[start + len(header):]
        m = re.search(r"\n## ", rest)          # slice to the next h2 section
        section = rest[:m.start()] if m else rest
        return set(re.findall(r"^- `([a-z][a-z-]*)`", section, re.M))

    def test_severity_modifier_vocab_matches_schema(self):
        self.assertEqual(
            validate.SEVERITY_MODIFIER_VOCAB,
            self._schema_terms("## Severity-modifier vocabulary"))
        self.assertEqual(len(validate.SEVERITY_MODIFIER_VOCAB), 8)

    def test_disposition_vocab_matches_schema(self):
        self.assertEqual(
            validate.DISPOSITION_VOCAB,
            self._schema_terms("## Finding disposition vocabulary"))

    def test_disposition_default_and_nondefect_set(self):
        self.assertIn("defect", validate.DISPOSITION_VOCAB)
        self.assertEqual(
            validate.DISPOSITION_VOCAB - {"defect"},
            {"control-present", "not-applicable", "correct-substrate"})


class TestCriteriaConsolidation(unittest.TestCase):
    CLUSTER_CODES = [
        "ARC-D3A", "ARC-D3B", "QAL-C1C", "QAL-C1D", "QAL-C2B", "ARC-G1B",
        "ARC-G2A", "ARC-G2B", "ARC-F1E",                       # cluster 1
        "SEC-F1B", "ARC-F2G", "COD-B2C",                       # cluster 2
        "TST-B2A", "TST-B1C", "TST-B1A", "TST-B1E", "TST-G3F", # cluster 3
        "QAL-H1A", "ARC-A1C",                                  # cluster 4
        "AGT-A1A", "AGT-A1B",                                  # cluster 5
    ]
    RECIPROCAL_PAIRS = [
        ("ARC-D3A", "ARC-D3B"), ("QAL-C1C", "QAL-C1D"), ("QAL-C2B", "ARC-G1B"),
        ("ARC-G2A", "ARC-G2B"),
        ("SEC-F1B", "COD-B2C"), ("ARC-F2G", "COD-B2C"), ("SEC-F1B", "ARC-F2E"),
        ("COD-B2C", "COD-B1A"),
        ("TST-G3F", "TST-B2A"), ("TST-G3F", "TST-B1C"), ("TST-G3F", "TST-B1A"),
        ("TST-G3F", "TST-B1E"), ("TST-B1C", "TST-B1E"),
        ("QAL-H1A", "ARC-A1C"), ("AGT-A1A", "AGT-A1B"),
    ]

    def _entries(self):
        import validate
        docs = validate.load_domains(os.path.join(ROOT, "domains"))
        return {c: e for d in docs.values() for c, e in (d.get("entries") or {}).items()}

    def test_cluster_codes_have_criteria(self):
        e = self._entries()
        for c in self.CLUSTER_CODES:
            self.assertTrue((e[c].get("criteria") or "").strip(), f"{c} needs criteria")

    def test_reciprocal_see_also_pairs(self):
        e = self._entries()
        for a, b in self.RECIPROCAL_PAIRS:
            self.assertIn(b, e[a].get("see_also") or [], f"{a} -> {b}")
            self.assertIn(a, e[b].get("see_also") or [], f"{b} -> {a}")

    def test_no_name_or_severity_drift_vs_release(self):
        # criteria/see_also only — a cluster code's name+severity must equal the
        # frozen 0.2.0 release (all cluster codes predate the 0.2.x tiers).
        released = json.load(open(os.path.join(ROOT, "build", "ocrdb-0.2.0.json")))
        rel = {c: v for dom in released["domains"].values()
               for c, v in dom["entries"].items()}
        e = self._entries()
        for c in self.CLUSTER_CODES + ["ARC-A3A", "QAL-D1A", "COD-B1A", "ARC-F2E",
                                       "TST-C2B", "TST-G1B"]:
            self.assertEqual(e[c]["name"], rel[c]["name"], c)
            self.assertEqual(e[c]["default_severity"], rel[c]["default_severity"], c)


if __name__ == "__main__":
    unittest.main()
