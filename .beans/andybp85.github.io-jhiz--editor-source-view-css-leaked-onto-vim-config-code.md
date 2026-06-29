---
# andybp85.github.io-jhiz
title: Editor source-view CSS leaked onto vim-config code blocks
status: completed
type: bug
priority: high
created_at: 2026-06-28T23:49:17Z
updated_at: 2026-06-28T23:51:05Z
---

Moving the editor .codehilite rules from blog.css to projects.css (commit 9b6ae79) made main > .codehilite apply to ALL codehilite blocks on projects pages. vim-config uses pygments token-spans (not line-spans), so the editor rules (pre white-space:normal; code>span display:block + line counter) put each token on its own numbered line — broken, and live. Fix: scope the editor rules to the markdown source-view blocks only (.codehilite.source on the Teaching page); let regular code blocks render as pygments monokai.

## Summary of Changes

Scoped the editor source-view CSS to .codehilite.source (Teaching page markdown blocks tagged accordingly); regular .codehilite blocks (vim-config, and the new wedding examples) now render as normal pygments monokai again. Verified: vim-config pre=pre-wrap + monokai bg + inline token spans; Teaching keeps its 29 line-spans.
