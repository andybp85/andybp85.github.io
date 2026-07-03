---
# andybp85.github.io-1352
title: Expand token-saving post and teaching-claude page
status: completed
type: task
priority: normal
created_at: 2026-07-03T11:53:22Z
updated_at: 2026-07-03T12:48:04Z
---

Add requested sections to src/posts/cutting-claude-code-token-use.md (superpowers+beans intro section, firecrawl, claude.md brevity, settings.json deny + .claudeignore, language-scoped rules, memory/memsearch in context mgmt, skills+4plus1, statusline, opus 4.8 limits, Fable intro rewrite, sources) and projects/teaching-claude-to-code-like-me/index.html (lang-specific files w/ path-scoping note, semantics-bar-tab quip).

## Tasks

- [x] Rewrite intro (Fable origin)
- [x] Add 'build the right thing' section (Superpowers + beans + bean-gate)
- [x] Add firecrawl beat (clean web input)
- [x] Add 'keep config lean' section (CLAUDE.md brevity + path-scoped rules + deny/.claudeignore)
- [x] Expand context-mgmt section (mydataschool #4, Thariq caption, memory/memsearch)
- [x] Add skills section (firecrawl reasons + 4+1 + repomix + greenfield)
- [x] Add statusline section (dandoescode + GordonBeeming)
- [x] Rewrite close (Opus 4.8 limits)
- [x] Add Sources section
- [x] teaching-claude: add lang-specific files w/ path-scoping intro
- [x] teaching-claude: semantics/bar-tab quip
- [x] Build + test both

## Open
- User instruction "add a section" was truncated — awaiting clarification on what section.
- Post says Opus 4.8 (per instruction); global settings.json model is claude-fable-5[1m] — flagged to user.
- Changes NOT committed/pushed (user did not ask).

## Summary of Changes

Expanded src/posts/cutting-claude-code-token-use.md: Fable-origin intro ending on the search-high-and-low instinct, a category-preview second paragraph, and new sections for build-the-right-thing (Superpowers + beans + bean-gate), firecrawl clean input, keep-config-lean (CLAUDE.md brevity + path-scoped rules + deny/.claudeignore), context management (mydataschool #4, Thariq caption blockquote, memory/memsearch), skills (4+1 + repomix + greenfield), statusline (dandoescode + GordonBeeming), an Opus-4.8 close, and a Sources list. Added a Scoped-by-language section (python.md/ts.md blocks generated via build.py pipeline) and the semantics/bar-tab quip to the teaching-claude project page. Truncated "add a section" instruction skipped per user. 15/15 tests pass.
