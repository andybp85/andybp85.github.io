---
# andybp85.github.io-131t
title: Replace subnav current-post underline with chevron marker
status: completed
type: task
priority: low
created_at: 2026-06-28T20:06:35Z
updated_at: 2026-06-28T20:06:35Z
---

The red underline on the active post in the blog subnav looked rough (3px darkred underline, wrapped awkwardly under two-line titles). Replaced with white text + a '›' ::before chevron in styles.css.

## Summary of Changes

- styles.css: sub-nav nav a.current — dropped text-decoration underline rules; added `&::before { content: "› " }`. Text stays var(--text-color) (white).
