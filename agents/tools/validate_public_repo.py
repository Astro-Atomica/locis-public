"""Validate public documents, local links, GitHub forms and workflow syntax."""
from __future__ import annotations

import copy
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

import yaml
from markdown_it import MarkdownIt
from build_docs import ROOT, heading_ids, load_site, local_target


class StrictLoader(yaml.SafeLoader):
    pass


# GitHub uses YAML 1.2: the workflow key 'on' is not a boolean.
StrictLoader.yaml_implicit_resolvers = copy.deepcopy(yaml.SafeLoader.yaml_implicit_resolvers)
for key, entries in StrictLoader.yaml_implicit_resolvers.items():
    StrictLoader.yaml_implicit_resolvers[key] = [(tag, rule) for tag, rule in entries if tag != 'tag:yaml.org,2002:bool']
StrictLoader.add_implicit_resolver('tag:yaml.org,2002:bool', re.compile(r'^(?:true|false)$', re.I), list('tTfF'))


def unique_mapping(loader, node, deep=False):
    values = {}
    for key, value in node.value:
        name = loader.construct_object(key, deep=deep)
        if name in values:
            raise ValueError("duplicate YAML key")
        values[name] = loader.construct_object(value, deep=deep)
    return values


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def parse_yaml(path: Path):
    return yaml.load(path.read_text(encoding='utf-8-sig'), Loader=StrictLoader)


def require(ok: bool, message: str):
    if not ok:
        raise ValueError(message)


def public_files(root: Path) -> list[Path]:
    names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z', '--cached', '--others', '--exclude-standard'])
    return sorted({root / n.decode('utf-8') for n in names.split(b'\x00') if n and (root / n.decode('utf-8')).is_file()})


def validate(root: Path = ROOT) -> dict:
    md = MarkdownIt('commonmark', {'html': False}).enable('table')
    documents = [p for p in public_files(root) if p.suffix == '.md']
    link_count = 0
    for path in documents:
        source = path.relative_to(root).as_posix()
        text = path.read_text(encoding='utf-8-sig')
        require(bool(re.search(r'(?:Updated|updated) [A-Z][a-z]+ \d{1,2}, \d{4}.*Build [1-9]\d*', text)), f'{source}: missing date/build')
        require(not re.search(r'[A-Z]:[/\\](?:Data|Users)[/\\]', text), f'{source}: private machine path')
        for token in md.parse(text):
            for child in token.children or []:
                if child.type not in ('link_open', 'image'):
                    continue
                href = child.attrGet('href' if child.type == 'link_open' else 'src') or ''
                url = urlsplit(href)
                if url.scheme or url.netloc:
                    require(url.scheme in ('https', 'mailto'), f'{source}: unsafe external link')
                    continue
                target, fragment = local_target(root, source, href)
                if fragment and target.endswith('.md'):
                    ids = heading_ids(md.parse((root / target).read_text(encoding='utf-8-sig')))
                    require(fragment in ids, f'{source}: missing local anchor')
                link_count += 1
    names = set()
    forms = list((root / '.github/ISSUE_TEMPLATE').glob('*.yml'))
    for path in forms:
        data = parse_yaml(path)
        if path.name == 'config.yml':
            require(data['blank_issues_enabled'] is False, 'blank issues must be disabled')
            for contact in data['contact_links']:
                require(all(contact.get(k) for k in ('name', 'url', 'about')), 'incomplete contact')
                require(contact['url'].startswith('https://'), 'contact must use HTTPS')
            continue
        require(all(isinstance(data.get(k), str) and data[k] for k in ('name', 'description', 'title')), 'incomplete issue form')
        require(data['name'] not in names, 'duplicate form name')
        names.add(data['name'])
        ids = set()
        for field in data['body']:
            require(field['type'] in ('markdown', 'input', 'textarea', 'dropdown', 'checkboxes'), 'invalid form field')
            attrs = field['attributes']
            if field['type'] == 'markdown':
                require(bool(re.search(r'updated .*Build [1-9]\d*', attrs['value'])), 'form needs visible revision')
                continue
            ident = field['id']
            require(bool(re.fullmatch(r'[A-Za-z0-9_-]+', ident)) and ident not in ids, 'invalid/duplicate field ID')
            ids.add(ident)
            require(bool(attrs.get('label')), 'missing field label')
            if field['type'] == 'dropdown':
                options = attrs['options']
                require(len(options) >= 2 and len(set(options)) == len(options), 'invalid dropdown')
            if 'validations' in field:
                require(isinstance(field['validations'].get('required'), bool), 'invalid required flag')
            if ident == 'privacy':
                require(field['type'] == 'checkboxes' and any(o.get('required') is True for o in attrs['options']), 'privacy acknowledgement must be required')
        require('privacy' in ids, 'missing public-report privacy check')
    require(len(names) == 3, 'expected bug, location and docs forms')
    for path in (root / '.github/workflows').glob('*.yml'):
        workflow = parse_yaml(path)
        require('on' in workflow and workflow.get('jobs'), 'invalid workflow')
        require(workflow.get('permissions') == {'contents': 'read'}, 'validation workflow must be read-only')
    site = load_site(root)
    result = {'documents': len(documents), 'localLinks': link_count, 'issueForms': len(names), 'staticPages': len(site['pages'])}
    print('Public repository validation:', result)
    return result


if __name__ == '__main__':
    validate()
