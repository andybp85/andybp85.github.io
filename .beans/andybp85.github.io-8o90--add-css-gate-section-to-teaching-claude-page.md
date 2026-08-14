---
# andybp85.github.io-8o90
title: Add CSS-gate section to teaching-claude page
status: completed
type: task
created_at: 2026-08-14T19:48:24Z
updated_at: 2026-08-14T19:48:24Z
---

Rewrite pass covering the latest tooling changes: new "The same argument, one language over" section (stylelint gate, vnu --css trap, proof-of-gate, no-descending-specificity story), CLAUDE.md snippet resynced to current Lint & Format Gates text, updated date bumped to Aug 14.

## Summary of Changes

Added the CSS validity section between the HTML-validator and secrets-guard sections, with two new Pygments-rendered blocks (blocked-commit output, false-positive pair) generated through the site's own _LineSpanFormatter. Page passes oxfmt and vnu.
