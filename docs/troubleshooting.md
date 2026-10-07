# Troubleshooting loc.is

Updated October 7, 2026 · Build 1

Start with a harmless example location. Record the affected URL, what you expected and what happened. Avoid exposing your personal location while investigating a problem.

| Problem | What to check |
| --- | --- |
| Search finds the wrong place | Check the place name and wider region. Try a more specific query and inspect the selected rectangle. Report an incorrect result rather than assuming its label proves accuracy. |
| The homepage location is far away | IP-based location is approximate. If you want a closer match, use the device-location option and inspect the browser's permission setting. Check the result before sharing. |
| A shared link covers too much or too little | Open the link and inspect its rectangle. Select an area suited to the task and copy its URL again. A smaller rectangle does not improve inaccurate source data. |
| A link in a document is not clickable | Publish the complete `https://loc.is/...` URL. Keep bare codes for internal storage, and preserve the correct route for the encoding type. |
| A QR code fails to scan | Preserve the white border, check the payload and scan the final printed proof. Replace the code if it opens the wrong area. |
| A map or control fails to load | Note the browser, device, affected page and visible error text. Say whether it repeats. Include expected and actual results in a website-bug report. |
| A named area's extent looks wrong | Distinguish the named-place source or estimate from the encoded rectangle. Include a reliable source when available and use the location-data form. |
| An integration example does not work | Check whether it is an uncommitted exploration. Use an ordinary full-URL link where possible and consult the current agent guide. |

## Choose a report form

Use the [issue chooser](https://github.com/Astro-Atomica/locis-public/issues/new/choose): website bug for broken behavior, location-data problem for incorrect geographic information, or documentation correction for missing or inaccurate explanations. Search existing issues first.

Include reproduction steps, expected and actual results, browser/device details where relevant, and the document date/build if shown. Say **unknown** rather than guessing a website version. Supporting sources help with location reports but are not required to flag a problem.

See [Reporting issues](reporting-issues.md) for the full process and [SECURITY.md](../SECURITY.md) for private vulnerability reporting. A repository change or closed issue does not establish that a website fix has been deployed.

## Sources

Based on this repository's reporting and support guidance and the public [how-to guide](https://loc.is/s/how-to.html) and [agent guide](https://loc.is/s/for-agents.html), retrieved October 7, 2026. These are diagnostic suggestions, not a claim that each problem has a confirmed cause or fix.
