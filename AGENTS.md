# LOCIS public repository agent instructions

Updated October 4, 2026 · Build 3

This repository contains public documentation, public issue reporting and public static docs for LOCIS. `locis` is the project HQ and project brain; `locis-website` is the deployable website project. Follow [repository scope](docs/repository-scope.md); SDK and widget source ownership remains undecided.

Read [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md), the [public AI policy](https://loc.is/s/ai-policy.html) and [publication rules](agents/rules/publication.md) before changing content. The policy applies to public docs and support material. Do not weaken it, infer human review from the user's general task instruction or claim that agent validation is human review.

- Keep agent guidance in this entrypoint and `agents/`; avoid duplicate client-specific rule files.
- Keep docs in `docs/` and issue forms in `.github/ISSUE_TEMPLATE/`. Static documentation-site source/build configuration belongs here when selected; its hosting and publication require their own evidence and authorization. Do not copy website application source, internal security audits, host paths, private data or website deployment tools here. Do not assign SDK/widget source to this repo just because their public guides belong here.
- Link to current public website guides for feature details. Verify public URLs and distinguish proposals, local checks and deployed behavior. Do not declare the experimental URL grammar frozen or fully implemented without evidence.
- Preserve sources and uncertainty for geographic claims. Do not treat a code rectangle, named-place estimate or generated illustration as factual boundary evidence.
- Keep contributor correspondence, screenshots, network captures, review evidence and logs in ignored underscore folders. Review artifacts before any public attachment.
- Date and number new/revised documents. Record actual human editorial review in private notes tied to the exact version before publication.
- Follow [the support process](docs/support-process.md) and route sensitive vulnerabilities through [SECURITY.md](SECURITY.md). Never test abuse by generating production traffic or exposing another visitor's data.
- Use `origin/main` as the default Git target and `codex/` for agent branches unless instructed otherwise. Inspect status and preserve unrelated work.
- Read [agents/privacy-policy.json](agents/privacy-policy.json) and use the bundled privacy preflight before committing or publishing. Do not add identity allowances without an existing approved public identity.
- Validate Markdown links, issue-form YAML, required fields and privacy gates. A successful local validation does not establish that GitHub has loaded a form or that the website has been deployed.
- Use [static-docs instructions](docs/static-docs.md): run `python agents/tools/validate_public_repo.py`, the tool tests and `python agents/tools/build_docs.py`. Keep the explicit page allowlist in `docs/site.json`; never publish the repository root or copy ignored folders into the output. Hosting remains undecided. Browser-check rendered pages after changing build templates or styling.

The privacy tool and its tests are reused from the agentic project template; their license is in [agents/tools/LICENSE](agents/tools/LICENSE). This does not assert a new license for unrelated website code, artwork or contributor material.
