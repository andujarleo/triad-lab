"""Site export checks; these never import or execute simulation code."""
import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from build_site import BuildError, build, collect_site, extract_intro, load_field, source_file

ROOT = Path(__file__).resolve().parents[1]
PNG = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aD1sAAAAASUVORK5CYII=')


class SiteExportTests(unittest.TestCase):
    def test_saved_density_preserves_values_and_axis_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = np.array([[[0.0, 0.125], [2.0, 3.0]], [[4.0, 5.0], [6.0, 7.0]]])
            np.savez(root / 'state.npz', rho_f=original, other_array=np.array([99]))
            before = (root / 'state.npz').read_bytes()
            result = load_field(root, {'id': 'fixture', 'title': {'en': 'Saved field', 'pt-BR': 'Campo salvo'}, 'sourcePath': 'state.npz'})
            decoded = json.loads(json.dumps(result, allow_nan=False))
            self.assertEqual(decoded['shape'], [2, 2, 2])
            self.assertEqual(decoded['values'], [0.0, 0.125, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0])
            self.assertEqual(decoded['axisOrder'], 'xyz')
            self.assertEqual((decoded['min'], decoded['max']), (0.0, 7.0))
            self.assertEqual(decoded['sha256'], hashlib.sha256(before).hexdigest())
            self.assertEqual((root / 'state.npz').read_bytes(), before)

    def test_field_rejects_missing_nonfinite_and_nonspatial_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            spec = {'id': 'fixture', 'title': {}, 'sourcePath': 'state.npz'}
            for values in (np.array([1, 2]), np.full((2, 2, 2), np.nan), np.zeros((2, 2, 3))):
                np.savez(root / 'state.npz', rho_f=values)
                with self.subTest(shape=values.shape), self.assertRaises(BuildError):
                    load_field(root, spec)
            np.savez(root / 'state.npz', absent=np.zeros((2, 2, 2)))
            with self.assertRaisesRegex(BuildError, 'rho_f'):
                load_field(root, spec)

    def test_source_rejects_missing_escape_symlink_and_lfs_pointer(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = base / 'repository'
            root.mkdir()
            (base / 'outside.png').write_bytes(PNG)
            (root / 'escape.png').symlink_to(base / 'outside.png')
            (root / 'pointer.png').write_text('version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 10\n')
            for relative in ('missing.png', '../outside.png', 'escape.png', 'pointer.png'):
                with self.subTest(path=relative), self.assertRaises(BuildError):
                    source_file(root, relative)

    def test_introduction_uses_recorded_text_without_inventing_question(self):
        question, summary = extract_intro('[Lab](../../../README.md) · **English**\n\n# Field\n\n**What does `rho_f` show?**\n\nRecorded **density** from [this run](note.md).\n\n## Material\n')
        self.assertEqual(question, 'What does rho_f show?')
        self.assertEqual(summary, 'Recorded density from this run.')
        self.assertEqual(extract_intro('# History\n\nRecorded attempt; no new run.\n\n![plot](plot.png)'), ('', 'Recorded attempt; no new run.'))

    def test_catalog_export_includes_every_study_and_byte_exact_images(self):
        catalog = json.loads((ROOT / 'experiments/catalog.json').read_text())
        site, files = collect_site(ROOT)
        self.assertEqual(site['format'], 1)
        self.assertEqual(len(site['studies']), len(catalog['experiments']))
        self.assertGreater(len(site['studies']), 0)
        self.assertEqual([e['id'] for e in site['studies']], [e['id'] for e in catalog['experiments']])
        self.assertEqual(site['areas'], catalog['series'])
        for study in site['studies']:
            self.assertEqual(set(study['question']), {'en', 'pt-BR'})
            self.assertTrue(all(study['summary'].values()))
            self.assertEqual(set(study['docs']), {'en', 'pt-BR'})
            if study['image']:
                payload = files[study['image']]
                self.assertEqual(study['image'], f'media/{hashlib.sha256(payload).hexdigest()}.png')
        hero = ROOT / 'experiments/geometry/visual-comparisons/results/figures/phase-vortices-final-frame.png'
        self.assertEqual(files[site['hero']], hero.read_bytes())
        for field in site['fields']:
            decoded = json.loads(files[field['url']])
            self.assertEqual(field['size'], len(files[field['url']]))
            with np.load(ROOT / field['sourcePath'], allow_pickle=False) as archive:
                np.testing.assert_array_equal(np.array(decoded['values']).reshape(decoded['shape']), archive['rho_f'])

    def test_build_is_repeatable_and_does_not_overwrite_unknown_files(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = self.make_fixture(base / 'repository')
            output = base / 'public'
            build(root, output, field_specs=[])
            first = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            self.assertNotIn('README.md', first)
            self.assertEqual(first['index.html'], b'<h1>Fixture</h1>')
            build(root, output, field_specs=[])
            second = {p.relative_to(output).as_posix(): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            self.assertEqual(first, second)
            (output / 'keep.txt').write_text('user material')
            with self.assertRaisesRegex(BuildError, 'unrecognized'):
                build(root, output, field_specs=[])
            self.assertEqual((output / 'keep.txt').read_text(), 'user material')
            self.assertEqual((root / 'experiments/geometry/visual-comparisons/results/figures/phase-vortices-final-frame.png').read_bytes(), PNG)

    def test_build_refuses_output_over_repository_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            root = self.make_fixture(base / 'repository')
            for output in (root, root / 'web', root / 'experiments', root.parent):
                with self.subTest(output=str(output)), self.assertRaises(BuildError):
                    build(root, output, field_specs=[])
            self.assertEqual((root / 'web/index.html').read_bytes(), b'<h1>Fixture</h1>')

    @staticmethod
    def make_fixture(root):
        (root / 'web').mkdir(parents=True)
        (root / 'web/index.html').write_bytes(b'<h1>Fixture</h1>')
        (root / 'web/README.md').write_text('Maintenance only')
        hero = root / 'experiments/geometry/visual-comparisons/results/figures/phase-vortices-final-frame.png'
        hero.parent.mkdir(parents=True)
        hero.write_bytes(PNG)
        (root / 'experiments/catalog.json').write_text(json.dumps({'series': [], 'experiments': []}))
        return root


if __name__ == '__main__':
    unittest.main()
