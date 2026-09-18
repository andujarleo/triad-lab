"""Regression checks for the repository audit; no simulations are imported."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from check_repository import verify_payloads, restore_document, local_links

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

if __name__ == '__main__':
    unittest.main()
