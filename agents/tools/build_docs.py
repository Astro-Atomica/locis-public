"""Build the explicitly selected public Markdown pages; never copy the repository."""
from __future__ import annotations

import hashlib
import html
import json
import re
from pathlib import Path, PurePosixPath
from urllib.parse import quote, unquote, urlsplit, urlunsplit

from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "_build/static-docs"


def public_path(root: Path, relative: str) -> Path:
    parts = PurePosixPath(relative).parts
    if (not parts or "\\" in relative or ":" in relative or
            PurePosixPath(relative).is_absolute() or ".." in parts or
            any(p.startswith(("_", ".")) for p in parts)):
        raise ValueError("nonpublic source path")
    target = root / relative
    if (not target.resolve().is_relative_to(root.resolve()) or target.is_symlink() or
            any(p.is_symlink() for p in target.parents if p != root and p.is_relative_to(root))):
        raise ValueError("source escapes repository")
    if not target.is_file():
        raise ValueError("source file missing")
    return target


def load_site(root: Path) -> dict:
    site = json.loads((root / "docs/site.json").read_text(encoding="utf-8"))
    if site.get("repository") != "https://github.com/Astro-Atomica/locis-public":
        raise ValueError("unexpected public repository")
    seen_sources, seen_outputs = set(), set()
    for page in site["pages"]:
        public_path(root, page["source"])
        if not page["source"].endswith(".md"):
            raise ValueError("only Markdown sources may be exported")
        if not re.fullmatch(r"[a-z][a-z0-9-]*\.html", page["output"]):
            raise ValueError("unsafe output filename")
        if page["source"] in seen_sources or page["output"] in seen_outputs:
            raise ValueError("duplicate source or output")
        seen_sources.add(page["source"])
        seen_outputs.add(page["output"])
    if "index.html" not in seen_outputs:
        raise ValueError("missing index page")
    return site


def heading_ids(tokens) -> dict:
    used = {}
    ids = {}
    for i, token in enumerate(tokens):
        if token.type != "heading_open":
            continue
        label = tokens[i + 1].content
        slug = re.sub(r"[^\w\s-]", "", label.lower()).strip()
        slug = re.sub(r"\s+", "-", slug) or "section"
        count = used.get(slug, 0)
        used[slug] = count + 1
        ident = slug if not count else f"{slug}-{count}"
        token.attrSet("id", ident)
        ids[ident] = label
    return ids


def local_target(root: Path, source: str, href: str) -> tuple[str, str]:
    url = urlsplit(href)
    if url.scheme or url.netloc:
        raise ValueError("external link")
    target = (root / source).parent / unquote(url.path) if url.path else root / source
    target = target.resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError("link escapes repository")
    relative = target.relative_to(root.resolve()).as_posix()
    public_path(root, relative)
    return relative, url.fragment


def render_page(root: Path, site: dict, page: dict) -> str:
    md = MarkdownIt("commonmark", {"html": False}).enable("table")
    text = public_path(root, page["source"]).read_text(encoding="utf-8-sig")
    tokens = md.parse(text)
    heading_ids(tokens)
    outputs = {p["source"]: p["output"] for p in site["pages"]}
    for token in tokens:
        for child in token.children or []:
            if child.type == "image":
                raise ValueError("artwork is not configured for this text-only docs build")
            if child.type != "link_open":
                continue
            href = child.attrGet("href") or ""
            url = urlsplit(href)
            if url.scheme or url.netloc:
                if url.scheme not in ("https", "mailto"):
                    raise ValueError("unsafe link scheme")
                continue
            relative, fragment = local_target(root, page["source"], href)
            new_url = outputs.get(relative)
            if new_url is None:
                new_url = f"{site['repository']}/blob/main/{quote(relative, safe='/')}"
            child.attrSet("href", urlunsplit(("", "", new_url, url.query, fragment)))
    content = md.renderer.render(tokens, md.options, {})
    nav = "".join(
        f'<a href="{p["output"]}"' +
        (' aria-current="page"' if p["source"] == page["source"] else '') +
        f'>{html.escape(p["label"])}</a>' for p in site["pages"]
    )
    return f'''<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(page['label'])} · LOCIS documentation</title>
<link rel="icon" href="data:,">
<link rel="stylesheet" href="style.css"></head>
<body><a class="skip" href="#main">Skip to content</a>
<header><a class="brand" href="index.html">LOCIS <span>public documentation</span></a>
<a href="https://loc.is/">Open loc.is ↗</a></header>
<div class="layout"><nav aria-label="Documentation">{nav}</nav>
<main id="main" tabindex="-1">{content}</main></div>
<footer><a href="{site['repository']}">Documentation repository</a> ·
<a href="{site['repository']}/issues/new/choose">Report a problem</a> ·
<a href="https://loc.is/s/privacy.html">Website privacy</a></footer>
</body></html>
'''


STYLE = """*{box-sizing:border-box}html{color-scheme:light}body{margin:0;background:#fafbf9;color:#202b25;font:17px/1.65 system-ui,sans-serif}a{color:#11683f;text-underline-offset:.18em}a:hover{color:#074527}a:focus-visible{outline:3px solid #258a55;outline-offset:4px}.skip{position:absolute;top:-100px;padding:.6rem;background:white}.skip:focus{top:0}header,footer{max-width:1200px;margin:auto;padding:1.5rem 2rem}header{display:flex;justify-content:space-between;gap:1rem;border-bottom:1px solid #dce5dd}.brand{text-decoration:none;font-weight:800;letter-spacing:.08em}.brand span{display:block;font-size:.8rem;font-weight:400;letter-spacing:0;color:#53675c}.layout{max-width:1200px;margin:auto;display:grid;grid-template-columns:230px minmax(0,1fr);gap:3rem;padding:2.5rem 2rem}nav{display:flex;flex-direction:column;gap:.6rem}nav a{text-decoration:none;padding:.35rem .6rem;border-radius:4px}nav a[aria-current]{background:#e3f0e5;font-weight:700}main{min-width:0;max-width:820px}h1{font-size:clamp(1.75rem,4vw,2.45rem);line-height:1.2;letter-spacing:-.035em;margin:0 0 1.5rem}h2{margin-top:2rem;line-height:1.3}p,li{overflow-wrap:anywhere}pre{overflow-x:auto;padding:1rem;background:#edf1ec;border-radius:4px}code{font-size:.88em}table{border-collapse:collapse;width:100%;font-size:.92em}th,td{padding:.65rem;text-align:left;vertical-align:top;border-bottom:1px solid #dce5dd}footer{border-top:1px solid #dce5dd;font-size:.9rem}li+li{margin-top:.3rem}@media(max-width:760px){header,footer{padding:1.25rem}.layout{display:block;padding:1.25rem}nav{flex-direction:row;flex-wrap:wrap;gap:.3rem;margin-bottom:2rem;font-size:.9rem}nav a{padding:.3rem .45rem}header>a:last-child{white-space:nowrap;font-size:.9rem}table{font-size:.8rem}th,td{padding:.4rem}}
"""


def build(root: Path = ROOT) -> Path:
    from validate_public_repo import validate
    validate(root)
    site = load_site(root)
    # Render and validate every input before touching an existing build.
    pages = {page["output"]: render_page(root, site, page) for page in site["pages"]}
    output = root / "_build/static-docs"
    if output.is_symlink() or not output.resolve().is_relative_to(root.resolve()):
        raise ValueError("output escapes repository")
    output.mkdir(parents=True, exist_ok=True)
    expected = set(pages) | {"style.css", "manifest.json", ".nojekyll"}
    if any(p.name not in expected or not p.is_file() or p.is_symlink() for p in output.iterdir()):
        raise ValueError("unexpected existing output; build into a clean docs folder")
    manifest = {"version": 1, "sources": [
        {"source": p["source"], "sha256": hashlib.sha256(public_path(root, p["source"]).read_bytes()).hexdigest()}
        for p in site["pages"]
    ]}
    for name, content in pages.items():
        (output / name).write_text(content, encoding="utf-8", newline="\n")
    (output / "style.css").write_text(STYLE, encoding="utf-8", newline="\n")
    (output / ".nojekyll").write_text("", encoding="utf-8")
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(pages)} documentation pages in _build/static-docs")
    return output


if __name__ == "__main__":
    build()
