---
# andybp85.github.io-yw7n
title: Format project pages to html.md style
status: completed
type: task
priority: normal
created_at: 2026-07-05T17:49:39Z
updated_at: 2026-07-05T17:59:59Z
---

Hand-format all projects/*.html to html.md: 4-space indent, alphabetized attrs, charset first, boolean attrs name-only, void self-closed, long/4+attr elements broken one-per-line with closing on own line. Preserve inline script/style and pre blocks. One commit. Firefox page formatted separately (with popover + lazy).

## Summary of Changes
Reformatted all five existing project pages to html.md style: 4-space indent (html/head/body at col 0), attributes alphabetized, charset meta hoisted first, boolean attrs name-only (crossorigin), void elements self-closed, elements with 4+ attrs or >140-col lines broken one-per-line with the closing bracket on its own line, sub-nav anchors one-per-line. Also alphabetized the two stylesheet links on teaching-claude and vim-config (were rel-before-href). Inline <script>/<style> and every <pre> code block preserved byte-for-byte. Verified: all <pre> blocks byte-identical to HEAD and full tag-stripped text unchanged; all pages render with correct nav/current/code-block counts and no console errors. Firefox page formatted separately (bundled with popover + loading=lazy).
