"""Regression checks for the repository audit; no simulations are imported."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from check_repository import verify_payloads, restore_document, local_links, verify_research, verify_rule_audits

class RepositoryAuditTests(unittest.TestCase):
    def test_changed_numerical_payload_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'state.csv').write_bytes(b'changed\n')
            original = hashlib.sha256(b'original\n').hexdigest()
            errors = verify_payloads(root, [{'path': 'state.csv', 'original_sha256': original, 'current_sha256': original}], [])
            self.assertTrue(errors)

    def test_missing_lfs_payload_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            errors = verify_payloads(Path(directory), [{'path': 'missing.npy', 'original_sha256': 'x', 'current_sha256': 'x'}], [])
            self.assertTrue(errors)

    def test_link_patches_restore_unicode_and_keep_equation(self):
        before = 'Memória: [[campo]]; Ψ=0.2\n'
        patch = {'start': 9, 'end': 18, 'before': '[[campo]]', 'after': '[campo](../field.md)'}
        current = before[:9] + patch['after'] + before[18:]
        self.assertEqual(restore_document(current, [patch]), before)

    def test_unrecorded_document_change_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = b'Value: 0.2\n'
            (root / 'note.md').write_bytes(b'Value: 0.3\n')
            digest = hashlib.sha256(original).hexdigest()
            errors = verify_payloads(root, [{'path': 'note.md', 'original_sha256': digest, 'current_sha256': digest}], [])
            self.assertTrue(errors)

    def test_local_links_ignore_code_and_external_urls(self):
        text = '[yes](folder/a%20b.md)\n`[example](missing.md)`\n```md\n[example](missing.md)\n```\n[web](https://example.com)\n'
        self.assertEqual(list(local_links(text)), ['folder/a%20b.md'])

    def test_html_images_are_checked(self):
        self.assertEqual(list(local_links('<img src="figures/example.png" alt="test">')), ['figures/example.png'])


class ResearchIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'research/sources').mkdir(parents=True)
        (self.root / 'research/README.md').write_text('Reading')
        (self.root / 'research/README.pt-BR.md').write_text('Leitura')
        payload = b'Original source\n'
        (self.root / 'research/sources/source.md').write_bytes(payload)
        self.topic = {'id': 'memory', 'title': {'en': 'Memory', 'pt-BR': 'Memoria'},
                      'summary': {'en': 'History', 'pt-BR': 'Historia'},
                      'docs': {'en': 'research/README.md', 'pt-BR': 'research/README.pt-BR.md'},
                      'study_ids': ['recorded-study'], 'source_ids': ['source']}
        self.source = {'id': 'source', 'path': 'research/sources/source.md',
                       'sha256': hashlib.sha256(payload).hexdigest(), 'bytes': len(payload),
                       'topics': ['memory']}

    def check(self):
        (self.root / 'research/catalog.json').write_text(json.dumps(
            {'languages': ['en', 'pt-BR'], 'topics': [self.topic]}))
        (self.root / 'research/sources/catalog.json').write_text(json.dumps(
            {'sources': [self.source]}))
        return verify_research(self.root, {'recorded-study'})[0]

    def test_related_research_and_original_source_pass(self):
        self.assertEqual(self.check(), [])

    def test_edited_original_cannot_be_published_as_preserved(self):
        (self.root / self.source['path']).write_text('Reinterpreted source')
        self.assertTrue(any('changed research source' in e for e in self.check()))

    def test_unknown_simulation_and_one_sided_relation_are_rejected(self):
        self.topic['study_ids'] = ['invented-study']
        self.source['topics'] = ['another-theme']
        errors = self.check()
        self.assertTrue(any('unknown linked study' in e for e in errors))
        self.assertTrue(any('inconsistent topic/source link' in e for e in errors))
        self.assertTrue(any('inconsistent source/topic link' in e for e in errors))

    def test_missing_translation_is_rejected(self):
        del self.topic['summary']['pt-BR']
        self.assertTrue(any('missing research translation' in e for e in self.check()))

    def test_existing_source_and_symlink_outside_repository_are_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            file = Path(outside) / 'source.md'
            file.write_bytes((self.root / self.source['path']).read_bytes())
            self.source['path'] = str(file)
            self.assertTrue(any('unsafe research source' in e for e in self.check()))
            link = self.root / 'research/sources/link.md'
            link.symlink_to(file)
            self.source['path'] = 'research/sources/link.md'
            self.assertTrue(any('unsafe research source' in e for e in self.check()))

    def test_duplicate_relations_are_rejected(self):
        for record, field in [(self.topic, 'study_ids'), (self.topic, 'source_ids'), (self.source, 'topics')]:
            with self.subTest(field=field):
                record[field].append(record[field][0])
                self.assertTrue(any('duplicate research relation' in e for e in self.check()))
                record[field].pop()

    def test_translations_must_be_nonempty_text(self):
        for field in ['title', 'summary', 'docs']:
            for value in ['   ', 123]:
                with self.subTest(field=field, value=value):
                    previous = self.topic[field]['en']
                    self.topic[field]['en'] = value
                    self.assertTrue(any('missing research translation' in e for e in self.check()))
                    self.topic[field]['en'] = previous

    def test_audit_summary_and_report_must_be_nonempty_text(self):
        study = {'id': 'recorded-study', 'rule_audit': {'status': 'not-established',
                 'summary': {'en': 'Missing run', 'pt-BR': 'Execucao ausente'},
                 'report': dict(self.topic['docs'])}}
        for field in ['summary', 'report']:
            for value in ['   ', 123]:
                with self.subTest(field=field, value=value):
                    previous = study['rule_audit'][field]['en']
                    study['rule_audit'][field]['en'] = value
                    self.assertTrue(verify_rule_audits(self.root, [study]))
                    study['rule_audit'][field]['en'] = previous

    def test_each_study_requires_local_bilingual_audit(self):
        study = {'id': 'recorded-study'}
        self.assertTrue(verify_rule_audits(self.root, [study]))
        study['rule_audit'] = {'status': 'not-established',
                               'summary': {'en': 'Runtime missing', 'pt-BR': 'Runtime ausente'},
                               'report': dict(self.topic['docs'])}
        self.assertEqual(verify_rule_audits(self.root, [study]), [])
        study['rule_audit']['report']['en'] = '../outside.md'
        self.assertTrue(verify_rule_audits(self.root, [study]))

if __name__ == '__main__':
    unittest.main()
