# Building the public static docs

Updated October 7, 2026 · Build 2

The Markdown files are the documentation source. The portable static build renders only the thirteen pages selected in [site.json](site.json), with local navigation and no runtime JavaScript, analytics, external fonts or application source. Generated output stays in the ignored `_build/static-docs/` folder. The build does not copy private folders, Git data, issue attachments or repository tooling into the site.

## Install and check

Use Python 3.12 or newer and Git. From the repository root:

```text
python -m pip install -r requirements-docs.txt
python agents/tools/validate_public_repo.py
python -m unittest discover -s agents/tools/tests -v
python agents/tools/build_docs.py
```

The validator checks document dates/builds, local links and anchors, issue forms and workflow syntax. The build disables raw Markdown HTML and checks its explicit source list. Relative links to rendered pages become local HTML links; other public repository-file links point to GitHub. Add an approved document to the source list when it needs a standalone page. Artwork is deliberately outside this text-only build's current configuration; adding it requires the project's provenance and permission process.

## Preview

```text
python -m http.server 8100 --bind 127.0.0.1 --directory _build/static-docs
```

Open `http://127.0.0.1:8100/`. Check desktop and mobile navigation, links and readable text. Stop the preview with Ctrl+C. Use another free local port above 8100 if needed. The preview is local; it does not publish the docs.

## Publication

Hosting, the public docs URL and deployment remain undecided. The HTML output can be served under either a domain root or a project subdirectory because its page and stylesheet links are relative. Deploy only the generated static-docs folder, never the repository root. There is no automatic deployment workflow.

Before publication, review the exact generated pages and source versions, record the required human editorial review privately, run the privacy checks described in [CONTRIBUTING.md](../CONTRIBUTING.md), and confirm the intended hosting target. The read-only CI workflow validates changes and builds pages without uploading or deploying them.

The reused privacy scanner and its tests carry their [tool license](../agents/tools/LICENSE). That license does not automatically cover other project documentation, implementation, artwork or contributor material.
