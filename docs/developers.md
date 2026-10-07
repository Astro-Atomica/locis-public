# Developer guidance

Updated October 7, 2026 · Build 1

The documented integration is an ordinary HTTPS link. Geocode on the [loc.is website](https://loc.is/), inspect the selected rectangle and copy its URL. No public geocoding API or SDK is available according to the current agent guide.

## Link from HTML or Markdown

These snippets use a demonstration area. Replace it with a checked location and a meaningful link label.

```html
<a href="https://loc.is/38MC3A">View the selected area on loc.is</a>
```

```markdown
[View the selected area on loc.is](https://loc.is/38MC3A)
```

A standard link does not install an embed, hovercard or metadata reader. Keep place names, directions and event details in your own content. There is no need to invent a custom URI scheme or endpoint.

## Store codes and export links

A bare code can be an internal data value. Preserve the encoding type so a shortcode and a longcode remain distinguishable. Store longcodes as text, retaining leading zeros. Keep original geographic sources, coordinate precision and version context when needed.

The public agent guide provides these format examples:

| Encoding | Stored text | Public link |
| --- | --- | --- |
| Shortcode | `683M` | `https://loc.is/683M` |
| Longcode | `06080314` | `https://loc.is/h/06080314` |

These are source examples, not locations selected for your application. Always include the protocol and domain in a publicly presented location or QR payload. Do not prepend the shortcode route to a stored longcode.

## Compound expressions and experimental interfaces

Use individually checked links when they meet the need. If you use a compound expression, consult the current public format guidance and check the resulting combined map. Do not assume an area set defines an itinerary.

Hovercards, widgets, custom metadata readers, geocoding APIs and SDKs are uncommitted explorations. A prototype does not establish a supported interface or third-party integration. The URL grammar is experimental; this document is not a frozen standard. Keep the ordinary full-URL link usable if an experiment changes or disappears.

## Automated access

Follow the [agent guide](https://loc.is/s/for-agents.html). Identify automated requests as agent traffic through the HTTP `User-Agent` header. Navigate slowly and only as needed for the user's task. Reuse retrieved information, respect crawl rules and back off when asked.

Do not enumerate location codes, manufacture visits, evade blocks or disguise automated requests as human traffic. If tooling cannot identify agent traffic, do not use it to generate automated visits. The public guide does not establish a traffic-reporting API.

## Verify and report

Check the copied URL and geographic meaning. Distinguish a local test, a live website check and a physical QR print test. Use the [reporting guide](reporting-issues.md) for bugs; use [security guidance](../SECURITY.md) for sensitive vulnerabilities.

## Sources and status

Based on the [web developer section](https://loc.is/s/how-to.html#web-developers) and [agent guide](https://loc.is/s/for-agents.html), retrieved October 7, 2026. Check those current guides before depending on an integration. SDK and widget source ownership remains undecided; see [repository scope](repository-scope.md).
