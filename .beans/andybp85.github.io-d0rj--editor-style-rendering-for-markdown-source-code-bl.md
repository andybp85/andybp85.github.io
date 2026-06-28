---
# andybp85.github.io-d0rj
title: Editor-style rendering for markdown source code blocks
status: completed
type: feature
priority: normal
created_at: 2026-06-28T20:27:01Z
updated_at: 2026-06-28T22:53:11Z
---

Render fenced markdown code blocks as an editor view (line numbers + syntax highlighting) themed with the site palette, for the On Writing Readable Code post which embeds general.md verbatim.

- src/post_template.html: load blog.css after pygments.css so editor token colors beat monokai.
- blog/blog.css: .codehilitetable editor theme — dark panel, line-number gutter, Berkeley Mono, oasis-blue headings, indianred list markers, italic emphasis, inline-code chips. Scoped to line-numbered blocks; stays dark in both page themes.

## Open
- [x] long lines soft-wrap with hanging indent; no horizontal scroll. Switched from Pygments table line-numbers to per-line spans (build.py linespans) + CSS counter; blog.css wraps each line as a block.

## Summary of Changes

- build.py: Pygments `linespans='line'` wraps each source line in a `<span>`, so a CSS counter numbers lines and soft-wraps them with a hanging indent (no horizontal scroll).
- Editor theming (line numbers, site-palette markdown tokens) lives in `projects/projects.css`.
- Rendered view ships at `/projects/teaching-claude-to-code-like-me/` (moved out of `/blog/`).
