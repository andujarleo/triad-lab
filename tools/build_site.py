#!/usr/bin/env python3
"""Build the public atlas from preserved records; never run a simulation."""
from __future__ import annotations

import argparse
import hashlib
import html
import io
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/andujarleo/triad-lab'
HERO = 'experiments/geometry/visual-comparisons/results/figures/phase-vortices-final-frame.png'
LANGUAGES = ('en', 'pt-BR')
MARKER = '.triad-site-build.json'
FIELD_SPECS = (
    {'id': 'field-3d', 'title': {'en': 'Emergent 3D field · saved density', 'pt-BR': 'Campo 3D emergente · densidade salva'},
     'sourcePath': 'experiments/geometry/field-3d/results/data/final_state.npz'},
    {'id': 'scale-sweep-l24', 'title': {'en': 'Scale sweep · L = 24 · saved density', 'pt-BR': 'Varredura de escala · L = 24 · densidade salva'},
     'sourcePath': 'experiments/geometry/scale-sweep/results/data/sweep_L24.npz'},
)


class BuildError(ValueError):
    """A source or output cannot be safely exported."""


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, separators=(',', ':')) + '\n').encode('utf-8')


def source_file(root: Path, relative: str) -> Path:
    """Resolve an existing, hydrated source without following a path outside root."""
    candidate = Path(relative)
    if candidate.is_absolute():
        raise BuildError(f'Source path must be repository-relative: {relative}')
    path = (root / candidate).resolve()
    if not path.is_relative_to(root.resolve()):
        raise BuildError(f'Source path escapes repository: {relative}')
    if not path.is_file():
        raise BuildError(f'Missing source file: {relative}')
    with path.open('rb') as handle:
        if handle.read(128).startswith(b'version https://git-lfs.github.com/spec/v1'):
            raise BuildError(f'Unhydrated Git LFS source: {relative}. Run git lfs pull before building.')
    return path


def plain_text(value: str) -> str:
    value = re.sub(r'\[([^\]]+)\]\([^\n]*?\)', r'\1', value)
    value = re.sub(r'<[^>]*>', '', value)
    value = value.replace('**', '').replace('`', '')
    value = re.sub(r'(?<!\w)[*_]([^*_]+)[*_](?!\w)', r'\1', value)
    return ' '.join(html.unescape(value).split())


def extract_intro(document: str) -> tuple[str, str]:
    """Use the opening question when explicit; never infer one from a result."""
    heading = re.search(r'^# .+$', document, re.MULTILINE)
    if heading is None:
        return '', ''
    opening = re.split(r'^## ', document[heading.end():], maxsplit=1, flags=re.MULTILINE)[0]
    paragraphs = [part.strip() for part in re.split(r'\n\s*\n', opening) if part.strip()]
    question = ''
    if paragraphs and re.fullmatch(r'\*\*.+\*\*', paragraphs[0], re.DOTALL):
        question = plain_text(paragraphs.pop(0))
    summary = next((plain_text(part) for part in paragraphs if not part.startswith(('#', '![', '[', '-', '|', '```', '<'))), '')
    return question, summary


def load_field(root: Path, spec: dict) -> dict:
    """Read rho_f only and serialize its original values in xyz, C order."""
    path = source_file(root, spec['sourcePath'])
    payload = path.read_bytes()
    try:
        with np.load(io.BytesIO(payload), allow_pickle=False) as archive:
            if 'rho_f' not in archive:
                raise BuildError(f'Missing rho_f array: {spec["sourcePath"]}')
            density = archive['rho_f']
    except (OSError, ValueError, KeyError) as exc:
        raise BuildError(f'Cannot read rho_f in {spec["sourcePath"]}: {exc}') from exc
    if density.ndim != 3 or not density.size or len(set(density.shape)) != 1:
        raise BuildError(f'rho_f must be a nonempty cubic 3D array: {spec["sourcePath"]}')
    if density.dtype.kind != 'f' or density.dtype.itemsize > 8 or not np.isfinite(density).all():
        raise BuildError(f'rho_f must contain finite float32/float64 values: {spec["sourcePath"]}')
    return {
        'id': spec['id'], 'title': spec['title'], 'sourcePath': spec['sourcePath'],
        'sha256': digest(payload), 'shape': list(density.shape), 'axisOrder': 'xyz',
        'quantity': 'rho_f', 'min': float(density.min()), 'max': float(density.max()),
        'values': density.ravel(order='C').tolist(),
    }


def add_image(root: Path, relative: str, files: dict[str, bytes]) -> str:
    payload = source_file(root, relative).read_bytes()
    if not payload.startswith(b'\x89PNG\r\n\x1a\n'):
        raise BuildError(f'Expected an original PNG image: {relative}')
    destination = f'media/{digest(payload)}.png'
    files[destination] = payload
    return destination


def study_image(root: Path, document_path: str, document: str, files: dict[str, bytes]) -> str | None:
    for target in re.findall(r'!\[[^\]]*\]\(([^\n]*?)\)', document):
        target = target.strip().strip('<>')
        url = urlsplit(target)
        if url.scheme or url.netloc or not url.path.lower().endswith('.png'):
            continue
        relative = (Path(document_path).parent / unquote(url.path)).as_posix()
        return add_image(root, relative, files)
    return None


def collect_site(root: Path, field_specs: tuple | list | None = None) -> tuple[dict, dict[str, bytes]]:
    """Collect data and original media in memory before touching an output folder."""
    root = root.resolve()
    catalog = json.loads(source_file(root, 'experiments/catalog.json').read_text(encoding='utf-8'))
    files: dict[str, bytes] = {}
    studies = []
    ids = set()
    area_ids = {area['id'] for area in catalog['series']}
    for record in catalog['experiments']:
        if record['id'] in ids or record['series'] not in area_ids:
            raise BuildError(f'Duplicate study ID or unknown area: {record["id"]}')
        ids.add(record['id'])
        study = {key: record[key] for key in ('id', 'folder', 'series', 'title', 'status', 'availability', 'docs')}
        study.update(question={}, summary={}, image=None)
        for language in LANGUAGES:
            document_path = record['docs'][language]
            document = source_file(root, document_path).read_text(encoding='utf-8')
            question, summary = extract_intro(document)
            if not summary:
                raise BuildError(f'No opening summary found in {document_path}')
            study['question'][language] = question
            study['summary'][language] = summary
            if study['image'] is None:
                study['image'] = study_image(root, document_path, document, files)
        studies.append(study)
    fields = []
    for spec in FIELD_SPECS if field_specs is None else field_specs:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', spec['id']):
            raise BuildError(f'Invalid field ID: {spec["id"]}')
        field = load_field(root, spec)
        url = f'data/field-{field["id"]}.json'
        if url in files:
            raise BuildError(f'Duplicate field ID: {field["id"]}')
        files[url] = json_bytes(field)
        fields.append({key: field[key] for key in ('id', 'title', 'sourcePath', 'sha256')} | {'url': url, 'size': len(files[url])})
    site = {'format': 1, 'repository': REPOSITORY, 'areas': catalog['series'], 'studies': studies,
            'hero': add_image(root, HERO, files), 'fields': fields}
    files['data/site.json'] = json_bytes(site)
    return site, files


def check_output(root: Path, output: Path) -> tuple[Path, dict[str, str]]:
    """Only a dedicated build folder may be overwritten; never repository sources."""
    if output.is_symlink():
        raise BuildError('Output must not be a symbolic link')
    output = output.resolve()
    root = root.resolve()
    if output == root or root.is_relative_to(output):
        raise BuildError('Output must not be the repository or an ancestor of it')
    if output.is_relative_to(root) and output != root / '_site':
        raise BuildError('Inside the repository, output must be the dedicated _site directory')
    if not output.exists():
        return output, {}
    if not output.is_dir():
        raise BuildError('Output must be a directory')
    entries = list(output.rglob('*'))
    if not entries:
        return output, {}
    if any(path.is_symlink() for path in entries):
        raise BuildError('Output contains symbolic links; choose a clean output directory')
    marker = output / MARKER
    try:
        record = json.loads(marker.read_text(encoding='utf-8'))
        known = record['files']
        if record['generator'] != 'triad-lab-site-v1' or not isinstance(known, dict):
            raise ValueError('Invalid marker')
        for name in known:
            if not isinstance(name, str) or Path(name).is_absolute() or '..' in Path(name).parts or name == MARKER:
                raise ValueError('Invalid output path')
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise BuildError('Output is nonempty and is not a recognized TRIAD site build') from exc
    actual = {path.relative_to(output).as_posix(): path for path in entries if path.is_file() and path != marker}
    if set(actual) - set(known):
        raise BuildError('Output contains unrecognized files; choose a clean output directory')
    for name, path in actual.items():
        if digest(path.read_bytes()) != known[name]:
            raise BuildError(f'Output file was edited after the build: {name}. Preserve it before rebuilding.')
    return output, known


def build(root: Path, output: Path, field_specs: tuple | list | None = None) -> dict:
    output, previous = check_output(root, output)
    site, files = collect_site(root, field_specs)
    source_file(root, 'web/index.html')
    for path in sorted((root / 'web').rglob('*')):
        if path.is_symlink():
            raise BuildError(f'Web source contains a symbolic link: {path}')
        if not path.is_file() or path.name == 'README.md' or any(part.startswith('.') for part in path.relative_to(root / 'web').parts):
            continue
        name = path.relative_to(root / 'web').as_posix()
        if name in files or name == MARKER:
            raise BuildError(f'Web source collides with generated data: {name}')
        files[name] = source_file(root, path.relative_to(root).as_posix()).read_bytes()
    output.mkdir(parents=True, exist_ok=True)
    for name, payload in sorted(files.items()):
        destination = output / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(payload)
    for name in sorted(set(previous) - set(files)):
        (output / name).unlink(missing_ok=True)
    for directory in sorted((p for p in output.rglob('*') if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if not any(directory.iterdir()):
            directory.rmdir()
    (output / MARKER).write_bytes(json_bytes({'generator': 'triad-lab-site-v1', 'files': {name: digest(payload) for name, payload in sorted(files.items())}}))
    return {'studies': len(site['studies']), 'images': len([name for name in files if name.startswith('media/')]),
            'fields': len(site['fields']), 'bytes': sum(map(len, files.values())), 'output': str(output)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT / '_site', help='Dedicated output directory (default: repository _site)')
    args = parser.parse_args()
    try:
        result = build(ROOT, args.output)
    except (BuildError, OSError, KeyError, ValueError) as exc:
        print(f'Site build failed: {exc}', file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
