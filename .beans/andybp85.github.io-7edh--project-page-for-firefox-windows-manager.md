---
# andybp85.github.io-7edh
title: Project page for firefox-windows-manager
status: completed
type: task
priority: normal
created_at: 2026-07-05T12:44:31Z
updated_at: 2026-07-05T13:00:57Z
---

Write projects/firefox-windows-manager/index.html in Andy's voice, with screenshots of the Art-Deco tab overview. Screenshots generated from a standalone harness rendering the real model.js+view.js+dashboard.css with mock window/tab/group data.

## Summary of Changes
- Wrote projects/firefox-windows-manager/index.html in Andy's site voice (situation-first intro, every claim + why, forward-looking close).
- Generated 3 screenshots of the real Art-Deco dashboard by rendering the actual model.js + view.js + dashboard.css against mock window/tab/group data, captured in Playwright Firefox (Gecko): overview-dark.png, overview-light.png (demonstrates light-dark() theming), window-detail.png (single-panel close-up). Quantized with PIL to ~236KB total.
- Added the 'Firefox Tab & Window Manager' sub-nav entry (date 2026-07-05, categories firefox|extension) to all 5 project pages + projects/index.html.
- Verified end-to-end: served locally, Playwright confirmed all images load, sub-nav shows the entry as current, no page errors.
