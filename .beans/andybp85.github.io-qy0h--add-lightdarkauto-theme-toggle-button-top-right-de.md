---
# andybp85.github.io-qy0h
title: Add light/dark/auto theme toggle button (top-right, default auto)
status: completed
type: feature
priority: normal
created_at: 2026-06-28T22:58:44Z
updated_at: 2026-06-28T23:14:47Z
---

User wants an explicit theme switcher (light / dark / auto) in the site header, top-right. Default to auto (follow system). Site currently themes via prefers-color-scheme only (styles.css media queries + inline per-page background gradient). Need a manual override that auto falls back to system. Vanilla, no deps.

## Summary of Changes

- Header gains a theme toggle (`components.js`) cycling auto -> light -> dark; sun/moon/contrast SVG icons, default auto.
- "auto" removes `html[data-theme]` (CSS falls back to `prefers-color-scheme`); light/dark pin it. Choice persisted in `localStorage`.
- Inline `<head>` script on every page applies a pinned theme before first paint (no FOUC); added `color-scheme` meta to the 3 projects pages that lacked it.
- `styles.css`: light/dark token pairs + filter vars driven by data-theme with a media-query fallback, so it degrades to system pref if JS fails.
- Verified with Playwright: pins override the system both ways, persist across reload, cycle correctly.
