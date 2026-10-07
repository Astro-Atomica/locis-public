# Contributing to LOCIS public documentation

Updated October 4, 2026 · Build 2

Report problems through the [issue forms](https://github.com/Astro-Atomica/locis-public/issues/new/choose), or propose a documentation correction in a pull request. Follow the [reporting guide](docs/reporting-issues.md) and [security guidance](SECURITY.md).

Keep changes focused on public documentation and support. Explain the problem, cite sources for factual changes and distinguish observed website behavior from a proposed feature. Do not copy private implementation, deployment configuration, internal security notes or contributor correspondence into this repository.

Each new or revised document needs a visible date and per-document build number. Increment that document's number for each content revision; a build number does not establish approval. Follow the [LOCIS AI policy](https://loc.is/s/ai-policy.html): AI-generated text requires human editorial review before publication, and artwork needs its applicable permission, provenance and disclosure records. Agent checks are not human review.

For maintainers, keep private captures and review notes in ignored underscore folders. Validate Markdown links and GitHub form YAML, and run the privacy checks from the repository root:

Install and run the reproducible [documentation checks and static build](docs/static-docs.md). CI runs these checks on pull requests and updates to `main`; it does not deploy the docs. Public issue forms become available only after the reviewed form files are published on the repository's default branch.

```text
python agents/tools/privacy_preflight.py working
python agents/tools/privacy_preflight.py staged
python agents/tools/privacy_preflight.py push
```

Preserve unrelated work and use a public Git identity approved by the publication policy. Run the staged check before committing and the push check before publishing unpublished commits. Publication also requires review of the exact text/version and authorization for the intended public action.
