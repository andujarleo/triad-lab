#!/usr/bin/env python3
"""Check preservation, catalog coverage and local Markdown links. Standard library only."""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


def digest(data):
    return hashlib.sha256(data).hexdigest()


def restore_document(current, patches):
    """Reverse link-only edits recorded at offsets in the original Unicode text."""
    parts, cursor, shift = [], 0, 0
    for patch in sorted(patches, key=lambda item: item['start']):
        start = patch['start'] + shift
        end = start + len(patch['after'])
        if start < cursor or current[start:end] != patch['after']:
            raise ValueError('document patch no longer matches its recorded text')
        parts.extend((current[cursor:start], patch['before']))
        cursor = end
        shift += len(patch['after']) - (patch['end'] - patch['start'])
    return ''.join(parts) + current[cursor:]


def verify_payloads(root, records, changes):
    errors, seen = [], set()
    edits = {item['path']: item for item in changes}
    for item in records:
        path = item['path']
        key = (path, item['original_sha256'], item['current_sha256'])
        if key in seen:
            continue
        seen.add(key)
        file = root / path
        if not file.is_file():
            errors.append(f'missing preserved payload: {path}')
            continue
        data = file.read_bytes()
        if digest(data) != item['current_sha256']:
            errors.append(f'changed payload (or unhydrated LFS pointer): {path}')
            continue
        try:
            original = restore_document(data.decode(), edits[path]['replacements']).encode() if path in edits else data
            if digest(original) != item['original_sha256']:
                errors.append(f'original hash cannot be recovered: {path}')
        except (UnicodeError, ValueError) as error:
            errors.append(f'{path}: {error}')
    return errors


def prose(text):
    """Exclude fenced and inline code examples from navigation checks."""
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
            continue
        if fence is None:
            lines.append(re.sub(r'`+[^`]*`+', '', line))
    return '\n'.join(lines)


def local_links(text):
    content = prose(text)
    targets = re.findall(r'!?\[[^\]\n]*\]\((<[^>]+>|[^)\n]+)\)', content)
    targets += re.findall(r'(?:src|href)=["\']([^"\']+)["\']', content)
    for target in targets:
        target = target.strip('<>')
        parsed = urlsplit(target)
        if not parsed.scheme and not target.startswith('//') and parsed.path:
            yield target


def nonempty_text(value):
    return isinstance(value, str) and bool(value.strip())


def verify_research(root, study_ids):
    """Check the two-way research graph and byte-preserved supplied sources."""
    errors = []
    catalog = json.loads((root / 'research/catalog.json').read_text())
    sources = json.loads((root / 'research/sources/catalog.json').read_text())['sources']
    topics = catalog['topics']
    topic_ids = {item['id'] for item in topics}
    source_ids = {item['id'] for item in sources}
    if len(topic_ids) != len(topics) or len(source_ids) != len(sources):
        errors.append('duplicate research topic or source ID')
    languages = catalog['languages']
    if 'en' not in languages or 'pt-BR' not in languages:
        errors.append('research must maintain English and Portuguese')
    source_by_id = {item['id']: item for item in sources}
    topic_by_id = {item['id']: item for item in topics}
    for topic in topics:
        for field in ['title', 'summary', 'docs']:
            if any(not nonempty_text(topic.get(field, {}).get(lang)) for lang in languages):
                errors.append(f"missing research translation: {topic['id']}/{field}")
        for field in ['source_ids', 'study_ids']:
            if len(topic[field]) != len(set(topic[field])):
                errors.append(f"duplicate research relation: {topic['id']}/{field}")
        for path in topic['docs'].values():
            if not nonempty_text(path):
                continue  # Reported above as an invalid translation.
            file = (root / path).resolve()
            if not file.is_relative_to(root.resolve()) or not file.is_file():
                errors.append(f'missing or unsafe research document: {path}')
        if not set(topic['study_ids']) <= study_ids:
            errors.append(f"unknown linked study: {topic['id']}")
        for source_id in topic['source_ids']:
            if source_id not in source_by_id or topic['id'] not in source_by_id[source_id]['topics']:
                errors.append(f"inconsistent topic/source link: {topic['id']} -> {source_id}")
    for source in sources:
        if len(source['topics']) != len(set(source['topics'])):
            errors.append(f"duplicate research relation: {source['id']}/topics")
        file = (root / source['path']).resolve()
        if not file.is_relative_to(root.resolve()) or not file.is_file():
            errors.append(f"missing or unsafe research source: {source['path']}")
            continue
        payload = file.read_bytes()
        if digest(payload) != source['sha256'] or len(payload) != source['bytes']:
            errors.append(f"changed research source: {source['path']}")
        if not source['topics']:
            errors.append(f"unclassified research source: {source['id']}")
        for topic_id in source['topics']:
            if topic_id not in topic_by_id or source['id'] not in topic_by_id[topic_id]['source_ids']:
                errors.append(f"inconsistent source/topic link: {source['id']} -> {topic_id}")
    return errors, {'research_topics': len(topics), 'research_sources': len(sources)}


def verify_rule_audits(root, studies):
    """Require the interpretation visible in the site to be traceable for every study."""
    errors = []
    statuses = {'documented-deviation', 'not-established', 'context-only', 'complete-record'}
    for study in studies:
        review = study.get('rule_audit', {})
        if review.get('status') not in statuses:
            errors.append(f"missing or unknown rule audit: {study['id']}")
        for lang in ['en', 'pt-BR']:
            if not nonempty_text(review.get('summary', {}).get(lang)):
                errors.append(f"missing audit translation: {study['id']}/{lang}")
            path = review.get('report', {}).get(lang, '')
            if not nonempty_text(path):
                errors.append(f"missing audit report: {study['id']}/{lang}")
                continue
            file = (root / path).resolve()
            if not file.is_relative_to(root.resolve()) or not file.is_file():
                errors.append(f"missing audit report: {study['id']}/{lang}")
    return errors


def audit(root):
    ledger = json.loads((root / 'provenance/layout-migration.json').read_text())
    changes = json.loads((root / 'provenance/document-link-changes.json').read_text())
    catalog = json.loads((root / 'simulations/catalog.json').read_text())
    errors = verify_payloads(root, ledger['content'], changes)
    editions = json.loads((root / 'provenance/reference-editions.json').read_text())
    for edition in editions['editions']:
        file = root / edition['path']
        if not file.is_file() or digest(file.read_bytes()) != edition['sha256']:
            errors.append(f"reference edition changed or missing: {edition['path']}")
    preserved = {(x['old_path'], x['path'], x['original_sha256']) for x in ledger['content']}
    ids, folders, associated = set(), set(), set()
    for study in catalog['experiments']:
        if study['id'] in ids or study['folder'] in folders:
            errors.append(f'duplicate study ID or folder: {study["id"]}')
        ids.add(study['id'])
        folders.add(study['folder'])
        if set(catalog['languages']) - set(study['docs']):
            errors.append(f'missing maintained language: {study["id"]}')
        paths = list(study['docs'].values()) + [study['folder'] + '/FILES.md']
        paths += [item['path'] for item in study['files']]
        for path in paths:
            if not (root / path).is_file():
                errors.append(f'catalog target missing: {path}')
        for item in study['files']:
            associated.add(item['path'])
            for old in item['original_paths']:
                if (old, item['path'], item['original_sha256']) not in preserved:
                    errors.append(f'catalog provenance does not match ledger: {old}')
    for record in ledger['content']:
        if record['path'].startswith('simulations/') and record['path'] not in associated:
            errors.append(f'preserved experiment payload absent from catalog: {record["path"]}')
    for old, path in ledger['path_map'].items():
        if not (root / path).exists():
            errors.append(f'migration target missing for {old}: {path}')
    links = 0
    # Audit only maintained repository trees, excluding generated runs and virtualenvs.
    docs = list(root.glob('*.md'))
    for directory in ['docs', 'research', 'simulations', 'provenance', 'templates', 'web']:
        docs.extend((root / directory).rglob('*.md'))
    for file in docs:
        for target in local_links(file.read_text()):
            links += 1
            path = unquote(urlsplit(target).path)
            destination = (file.parent / path).resolve()
            if not destination.is_relative_to(root.resolve()) or not destination.exists():
                errors.append(f'broken local link: {file.relative_to(root)} -> {target}')
    for directory in folders:
        if any(part in {'pasta sem título', 'expanded'} for part in Path(directory).parts):
            errors.append(f'unclassified directory: {directory}')
    research_errors, research_counts = verify_research(root, ids)
    errors.extend(research_errors)
    errors.extend(verify_rule_audits(root, catalog['experiments']))
    return errors, {**research_counts, 'studies': len(ids), 'original_paths': len(ledger['content']), 'unique_payloads': len({x['path'] for x in ledger['content']}), 'local_links': links}


def main():
    root = Path(__file__).resolve().parents[1]
    errors, counts = audit(root)
    print(json.dumps(counts, indent=2))
    if errors:
        print('\n'.join(errors), file=sys.stderr)
        return 1
    print('PASS: original payloads recoverable; catalog and local file links resolve.')
    print('This check does not validate external URLs, heading anchors or scientific conclusions.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
