# Location sharing examples

Updated October 7, 2026 · Build 1

These examples show how to write a location link into everyday material. The example URL is a demonstration area, not an actual event, entrance or findspot. Replace it with the full URL of the area you checked on loc.is.

## A meeting invitation

Fictional invitation template:

```text
Meet at [place name] on [date] at [time and time zone].
Look for [visible landmark or entrance instructions].
Map: https://loc.is/38MC3A
```

A park's general area may help people find the park while leaving the meeting spot ambiguous. Choose a suitable area and retain landmark directions. Do not describe a code as an exact bench location without checking that assignment.

## A public profile or recommendation

```text
A place I recommend: [place name and why it matters].
Location: https://loc.is/38MC3A
```

Use a public venue or broader area when a precise personal location would reveal too much. A short link still discloses geographic information.

## A spreadsheet or research record

Keep a complete HTTPS link in a text cell alongside the place name. Retain the original coordinates, source, observation date and uncertainty in separate fields when those are relevant. A link is convenient access to a map, not a replacement for the underlying evidence.

For internal storage, codes can be stored without a domain. Keep their encoding type, and store longcodes as text to preserve leading zeros. Restore the complete URL and appropriate route before exporting a public link; see [developer guidance](developers.md).

## A poster or printed invitation

Download the QR code from your checked location page. Place it with a readable URL, the venue name and directions. Preserve the white border and scan the final print before distributing it. A QR code contains a link, not the event time, entry instructions or a guarantee of access.

## Several stops

List each checked link with its own description:

```text
Start: [first place name] — [first full HTTPS location URL]
Finish: [second place name] — [second full HTTPS location URL]
```

Describe the journey separately. A collection of location cells does not specify a walking route, accessible path or stop order.

## Sources

Adapted from the public [how-to guide](https://loc.is/s/how-to.html) and [agent guide](https://loc.is/s/for-agents.html), retrieved October 7, 2026. Follow [How to use loc.is](using-locis.md) to select your own area.
