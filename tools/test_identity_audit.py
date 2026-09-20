"""Structural checks for the 8-language TRIAD identity audit; reads text only."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LANGS = ["en", "pt-BR", "es", "de", "sv", "no", "da", "zh-CN"]
EXPECTED = {"complete-record": 14, "documented-deviation": 14,
            "not-established": 25, "context-only": 12}


def catalog():
    return json.loads((ROOT / "simulations/catalog.json").read_text(encoding="utf-8"))


class IdentityAuditTests(unittest.TestCase):
    def test_registers_cover_every_study(self):
        ids = [x["id"] for x in catalog()["experiments"]]
        self.assertEqual(len(ids), 65)
        for tag in LANGS:
            with self.subTest(language=tag):
                text = (ROOT / f"docs/{tag}/triad-identity-audit.md").read_text(encoding="utf-8")
                for sid in ids:
                    self.assertIn(f'<a id="study-{sid}"></a>', text)

    def test_identity_classes_keep_their_counts(self):
        counts = {}
        for study in catalog()["experiments"]:
            status = study["rule_audit"]["status"]
            counts[status] = counts.get(status, 0) + 1
        self.assertEqual(counts, EXPECTED)

    def test_audit_summaries_and_reports_cover_eight_languages(self):
        for study in catalog()["experiments"]:
            review = study["rule_audit"]
            with self.subTest(study=study["id"]):
                for tag in LANGS:
                    summary = review["summary"].get(tag, "")
                    self.assertIsInstance(summary, str)
                    self.assertTrue(summary.strip())
                    report = review["report"].get(tag, "")
                    self.assertTrue(report.strip())
                    target = (ROOT / report).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.is_file())

    def test_study_pages_show_the_identity_badge(self):
        for study in catalog()["experiments"]:
            with self.subTest(study=study["id"]):
                en = (ROOT / study["docs"]["en"]).read_text(encoding="utf-8")
                pt = (ROOT / study["docs"]["pt-BR"]).read_text(encoding="utf-8")
                self.assertEqual(en.count("TRIAD identity:"), 1)
                self.assertEqual(pt.count("Identidade TRIAD:"), 1)
                for tag in LANGS:
                    anchor = f"docs/{tag}/triad-identity-audit.md#study-{study['id']}"
                    self.assertIn(anchor, en)
                    self.assertIn(anchor, pt)

    def test_new_language_entrances_link_the_register(self):
        registry = json.loads((ROOT / "docs/languages.json").read_text(encoding="utf-8"))
        tags = [entry["tag"] for entry in registry["languages"]]
        for tag in LANGS:
            self.assertIn(tag, tags)
        for tag in ["es", "de", "sv", "no", "da", "zh-CN"]:
            with self.subTest(language=tag):
                entrance = ROOT / f"docs/{tag}/README.md"
                self.assertTrue(entrance.is_file())
                self.assertIn("(triad-identity-audit.md)", entrance.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
