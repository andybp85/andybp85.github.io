---
# andybp85.github.io-t7o4
title: Audit site against modern-web-guidance and code-style rules
status: completed
type: task
priority: normal
created_at: 2026-06-28T15:55:49Z
updated_at: 2026-06-28T15:58:21Z
---

Audit the static site against the rules and skills installed since the code was last touched (general.md, js.md, html.md, css.md, python.md, objects.md, and the modern-web-guidance skill), and bring it into compliance.

## Findings & fixes

- [x] Declare `color-scheme` (modern-web-guidance dark-mode, MANDATORY) — site does manual prefers-color-scheme theming but never told the browser, so native UI (scrollbars/canvas) stayed light and could white-flash. Added `color-scheme: light dark` to styles.css :root + `<meta name="color-scheme">` to all HTML sources.
- [x] charset first in <head> (html.md head order) — was after darkreader-lock; moved to top.
- [x] icon link after stylesheets (html.md head order) — favicon moved after stylesheets in all 4 HTML sources.
- [x] drop semicolons from components.js (js.md: omit optional syntax / ASI).

## Out of scope (pre-existing deferred follow-ups, tracked separately)

- 2016 post inlines a base64 image -> 1.7MB source file.
- Post titles are slug-derived; no `title:` meta override.

## Summary of Changes

- styles.css: added `color-scheme: light dark` to :root.
- index.html, about/index.html, src/post_template.html, src/blog_index_template.html: added `<meta name="color-scheme">`, moved charset first, moved favicon link after stylesheets.
- components.js: removed all semicolons (ASI).
- Blog regenerated from templates; 15 tests pass.
