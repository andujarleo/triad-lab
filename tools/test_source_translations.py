"""Checks for the maintained research-source translations; reads text only."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = re.compile(
    r"^<!-- Translation of: (\S+); source commit: ([0-9a-f]{40}) -->$")
SUFFIX = re.compile(r"^(.+)\.(en|es|de|sv|no|da|zh-CN|ru|ja|pt-BR)\.md$")


def registry():
    return json.loads(
        (ROOT / "research/sources/translations.json").read_text(encoding="utf-8"))


def catalog_ids():
    catalog = json.loads(
        (ROOT / "research/sources/catalog.json").read_text(encoding="utf-8"))
    return {item["id"]: item["path"] for item in catalog["sources"]}


class SourceTranslationTests(unittest.TestCase):
    def test_registered_translations_exist_with_headers(self):
        data = registry()
        known = catalog_ids()
        self.assertEqual(data["source_language"], "pt-BR")
        self.assertEqual(data["total_sources"], len(known))
        for sid, by_lang in data["translations"].items():
            with self.subTest(source=sid):
                self.assertIn(sid, known)
                self.assertEqual(set(by_lang), set(data["target_languages"]))
                for lang, rel in by_lang.items():
                    target = (ROOT / rel).resolve()
                    self.assertTrue(target.is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.is_file())
                    text = target.read_text(encoding="utf-8")
                    self.assertTrue(text.strip())
                    match = HEADER.match(text.split("\n", 1)[0])
                    self.assertIsNotNone(match)
                    self.assertEqual(match.group(1), known[sid])

    def test_no_unregistered_translation_files(self):
        data = registry()
        registered = {path for by_lang in data["translations"].values()
                      for path in by_lang.values()}
        for path in (ROOT / "research/sources/author-supplied").glob("*.md"):
            if SUFFIX.match(path.name):
                self.assertIn(path.relative_to(ROOT).as_posix(), registered)


if __name__ == "__main__":
    unittest.main()
