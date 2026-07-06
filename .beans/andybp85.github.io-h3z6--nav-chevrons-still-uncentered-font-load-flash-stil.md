---
# andybp85.github.io-h3z6
title: Nav chevrons still uncentered; font-load flash still visible
status: completed
type: bug
priority: normal
created_at: 2026-07-06T15:28:18Z
updated_at: 2026-07-06T15:28:31Z
---

Follow-up to e7295fe, whose two fixes deployed but did not work:

- Chevron: vertical-align: middle aligns the marker box to x-height/2, which sits low on the cap-height nav text. Replaced with a measured em offset per font (B612 main nav 0.1em, Inter sub-nav 0.06em), derived from each font's cap-height and the guilsinglright glyph center.
- Flash: font-display: optional traded the swap-flash for a FOIT (body text held invisible ~100ms, then popped in). Switched to font-display: swap + font-size-adjust: from-font so the fallback paints immediately and the swap-in is metric-matched (no reflow, no flash).

Verified in Firefox headless against the real built post page: both chevrons center on the caps; font-size-adjust does not regress steady-state layout.

## Summary of Changes

styles.css only:
- 4x @font-face: font-display: optional -> swap
- body: add font-size-adjust: from-font
- main-nav .current::before: vertical-align: middle -> 0.1em
- sub-nav .current::before: vertical-align: middle -> 0.06em
- updated the font-face and both chevron comments to record the measured reasoning
