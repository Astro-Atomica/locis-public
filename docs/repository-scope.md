# Public repository scope

Updated October 4, 2026 · Build 3

`locis-public` is the LOCIS home for public documentation, public issue reporting and public static docs.

| Project | Role |
| --- | --- |
| **locis** | Project HQ and project brain: project direction, decisions, research and coordination. |
| **locis-public** | Public documentation, public issue reporting and public static docs. |
| **locis-website** | Deployable website project. |

Public guides, reporting forms, reviewed examples and the source/build setup for static documentation belong here. Public docs must work without access to the other repositories. Website implementation and deployment belong to the website project; project planning and cross-project decisions belong to HQ.

The [portable static-docs build](static-docs.md) renders an explicit list of public Markdown pages. The hosting target, public URL and deployment pipeline have not yet been selected. A local build does not establish that a documentation site is deployed. The existing [website guide](https://loc.is/s/how-to.html) remains a reference for current visitor-facing behavior; no guide migration is implied.

SDK and widget source ownership remains undecided. Public guides and reviewed examples for any future components fit this repository's role, but their source, supported API, package releases and delivery targets need separate decisions. Do not describe a documentation example as a supported SDK or widget release.

Public documentation and static-docs releases require the human editorial review described in [CONTRIBUTING.md](../CONTRIBUTING.md) and [publication rules](../agents/rules/publication.md). Dates and build numbers identify versions, not publication approval.
