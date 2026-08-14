---
# andybp85.github.io-fylq
title: Regenerate teaching-claude snippets from source at build time
status: todo
type: feature
priority: normal
created_at: 2026-08-14T19:58:20Z
updated_at: 2026-08-14T19:58:31Z
---

The page's CLAUDE.md and general.md snippet blocks are hand-synced copies of living files in ~/.claude/, and they drift — the Aug 14 resync found ~10 stale lines. Same disease the page diagnoses: when a rule lives in two places, one is already wrong.

Options to explore:
- A build step (or standalone script) that renders the snippet blocks from the rules files through _LineSpanFormatter and splices them between markers in the page HTML
- Or a test that renders and diffs, failing when the page goes stale (detection without auto-rewrite, matching the guard philosophy)

Notes:
- The excerpting is deliberate (CLAUDE.md shows only 4 sections, Workflow trimmed to 2 lines), so the source of truth is a checked-in excerpt spec, not the raw file
- The render half is ~10 lines: import _markdown from builder.build, feed it a fenced md fragment, take the codehilite HTML (run from src/ so the package resolves)

- [ ] Decide: regenerate vs. drift-test
- [ ] Implement, with the excerpt spec committed
- [ ] Prove it fails on a stale snippet before trusting it
