---
# andybp85.github.io-ef6f
title: Header renders in JS -> title drops on load (CLS)
status: completed
type: bug
priority: normal
created_at: 2026-07-07T11:01:13Z
updated_at: 2026-07-07T11:01:21Z
---

The 'flash' was layout shift, not fonts. <site-header> was an empty custom element that components.js filled at runtime, so the header had zero height at first paint; when JS hydrated it, the header claimed its space and pushed the title/content down.

Fix: server-render the header markup on every page (matching how <sub-nav> already ships static HTML, with current set at build/author time). components.js is demoted to a theme-toggle enhancer that wires the button already in the DOM. Header height is now present at first paint -> no shift, and the nav works with JS off.

- 10 source pages (index, about, 6 projects, 2 blog templates) + 6 rebuilt blog pages: empty <site-header> -> real <header>
- components.js: drop site-header element + navLink; add wireThemeToggle()
- styles.css: site-header off the display:contents rule; reserve .theme-toggle box so the JS-filled icon can't nudge the nav

Verified in Firefox with JS disabled: full header renders in place (previously empty). Build tests pass (15).

## Summary of Changes
Server-rendered the header across all pages; components.js now only enhances the theme button. Kills the title-drop CLS. Verified with JS disabled in Firefox; 15 build tests pass.
