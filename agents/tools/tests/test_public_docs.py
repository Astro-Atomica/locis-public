import json
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
from build_docs import build, load_site, public_path, render_page
from validate_public_repo import parse_yaml


class PublicDocsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'docs').mkdir()
        (self.root / 'README.md').write_text('# Overview\n\nUpdated October 4, 2026 · Build 1\n\n[Guide](docs/guide.md#start)\n', encoding='utf-8')
        (self.root / 'docs/guide.md').write_text('# Start\n\nUpdated October 4, 2026 · Build 1\n\n[Home](../README.md)\n', encoding='utf-8')
        self.site = {'repository': 'https://github.com/Astro-Atomica/locis-public', 'pages': [
            {'source': 'README.md', 'output': 'index.html', 'label': 'Overview'},
            {'source': 'docs/guide.md', 'output': 'guide.html', 'label': 'Guide'}]}
        (self.root / 'docs/site.json').write_text(json.dumps(self.site), encoding='utf-8')

    def test_private_paths_cannot_be_exported(self):
        (self.root / '_private').mkdir()
        (self.root / '_private/secret.md').write_text('private')
        for path in ('_private/secret.md', '../README.md', '.git/config', r'..\secret.md'):
            with self.subTest(path=path), self.assertRaises(ValueError):
                public_path(self.root, path)

    def test_page_links_and_anchors_survive_project_subdirectory(self):
        page = render_page(self.root, self.site, self.site['pages'][0])
        self.assertIn('href="guide.html#start"', page)
        self.assertIn('href="style.css"', page)
        guide = render_page(self.root, self.site, self.site['pages'][1])
        self.assertIn('id="start"', guide)
        self.assertIn('href="index.html"', guide)

    def test_raw_html_and_script_schemes_are_not_executable(self):
        (self.root / 'README.md').write_text('# Safe\n<script>alert(1)</script>\n\n[bad](javascript:alert(1))', encoding='utf-8')
        page = render_page(self.root, self.site, self.site['pages'][0])
        self.assertNotIn('<script>', page)
        self.assertNotIn('href="javascript:', page)

    def test_private_relative_link_fails(self):
        (self.root / '_private').mkdir()
        (self.root / '_private/note.md').write_text('private')
        (self.root / 'README.md').write_text('# Test\n[Note](_private/note.md)', encoding='utf-8')
        with self.assertRaises(ValueError):
            render_page(self.root, self.site, self.site['pages'][0])

    def test_unselected_files_are_not_in_page(self):
        (self.root / 'extra.md').write_text('UNSELECTED_PRIVATE_TEXT', encoding='utf-8')
        page = render_page(self.root, self.site, self.site['pages'][0])
        self.assertNotIn('UNSELECTED_PRIVATE_TEXT', page)
        self.assertEqual(len(load_site(self.root)['pages']), 2)

    def test_build_emits_only_allowlisted_public_files(self):
        from unittest.mock import patch
        (self.root / '_private').mkdir()
        (self.root / '_private/secret.txt').write_text('PRIVATE_SENTINEL')
        with patch('validate_public_repo.validate'):
            output = build(self.root)
        self.assertEqual({p.name for p in output.iterdir()}, {'index.html', 'guide.html', 'style.css', 'manifest.json', '.nojekyll'})
        self.assertFalse(any('PRIVATE_SENTINEL' in p.read_text(encoding='utf-8') for p in output.iterdir()))

    def test_existing_unexpected_output_is_not_overwritten(self):
        from unittest.mock import patch
        output = self.root / '_build/static-docs'
        output.mkdir(parents=True)
        keep = output / 'unrelated.txt'
        keep.write_text('preserve')
        with patch('validate_public_repo.validate'), self.assertRaises(ValueError):
            build(self.root)
        self.assertEqual(keep.read_text(), 'preserve')

    def test_duplicate_output_is_rejected(self):
        self.site['pages'][1]['output'] = 'index.html'
        (self.root / 'docs/site.json').write_text(json.dumps(self.site), encoding='utf-8')
        with self.assertRaises(ValueError):
            load_site(self.root)

    def test_yaml_workflow_on_key_and_duplicates(self):
        path = self.root / 'workflow.yml'
        path.write_text('on:\n  push:\npermissions:\n  contents: read\n', encoding='utf-8')
        self.assertIn('on', parse_yaml(path))
        path.write_text('name: first\nname: second\n', encoding='utf-8')
        with self.assertRaises(ValueError):
            parse_yaml(path)


if __name__ == '__main__':
    unittest.main()
