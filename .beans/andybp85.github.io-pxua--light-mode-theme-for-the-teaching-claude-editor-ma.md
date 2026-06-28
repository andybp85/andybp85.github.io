---
# andybp85.github.io-pxua
title: Light-mode theme for the Teaching Claude editor markdown block
status: completed
type: task
priority: normal
created_at: 2026-06-28T23:19:11Z
updated_at: 2026-06-28T23:25:01Z
---

The main > .codehilite editor block in projects/projects.css is hardcoded dark (color-scheme: dark + fixed colors). Now that the site has a light/dark/auto toggle, make the block follow the page theme: light palette in light mode. Reuse --oasis-blue/--text-color where possible; match the value-pair + media/attribute pattern in styles.css.

## Summary of Changes

- `projects/projects.css`: the `main > .codehilite` editor block now follows the page theme instead of forcing dark.
- Dropped `color-scheme: dark` and the fixed colors; editor palette is now custom-property pairs (`--editor-bg/-border/-chip/-emphasis/-gutter/-marker`) defaulting dark, with a light set applied via `:root[data-theme="light"]` and the unpinned `prefers-color-scheme: light` case (mirrors the styles.css pattern).
- Headings reuse `--oasis-blue` and body text `--text-color`, so they track the theme for free.
- Verified light + dark on the Teaching Claude page with Playwright.

## Follow-up: inline-code legibility

Inline-code tokens (.sb) were inheriting monokai's #E6DB74 yellow (only the chip background was themed), unreadable on the light panel. Added a theme-aware --editor-code: dark keeps the yellow (#e6db74), light uses dark amber (#8a5a00).
