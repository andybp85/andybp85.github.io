# Sub-nav Restyle — Design

**Date:** 2026-06-11
**Branch:** `web-compontents`
**Status:** Approved

## Goal

Restyle the `<sub-nav>` menus (blog index, blog post pages, projects index, vim
project page) so they fit the site theme, handle long titles gracefully, and
visibly mark the current page. Chosen direction: a **ruled list** — thin
darkred rules between entries, echoing the site's header/footer borders. No
dates shown.

## 1. CSS (`styles.css`, the `sub-nav` block)

- Each link in `sub-nav nav` becomes a block entry:
  - `border-top: 1px solid var(--dark-red)` (every entry, including the first —
    a rule sits between the label and the first title).
  - Vertical padding (`0.7rem 0`).
  - `text-wrap: balance` so multi-line titles break evenly instead of leaving a
    dangling word.
- The `text-indent: 1em hanging` rule on `sub-nav nav` is removed (the rules
  replace the hanging indent as the visual grouping for wrapped lines).
- `.current` links inside `sub-nav` get:
  - `color: var(--text-color)` (body text color instead of link blue),
  - the header nav's underline treatment: `text-decoration: underline`,
    `text-decoration-color: darkred`, `text-decoration-thickness: 3px`,
    with `text-underline-offset: 6px` (smaller offset than the header's 10px,
    proportional to the smaller text).
- Light mode needs no additions — everything rides on the existing custom
  properties (`--dark-red`, `--text-color`).
- The medium-breakpoint behavior (sub-nav moves full-width above `main`) is
  unchanged; the ruled entries simply span the full width there.

## 2. Builder: mark the current post (TDD)

Generated post pages currently render the sub-nav with no current marker, so
the `.current` style would never apply on them.

- `_subnav()` in `src/builder/build.py` gains a `current_slug` parameter
  (default `None`). The link whose slug matches gets `class="current"`; with
  `None` (blog index) no link is marked.
- `build_all()` passes each post's slug when rendering that post's page, and
  no slug for the blog index.
- Tests updated/added in `src/test/test_build.py` for: marked link when slug
  matches, no marking with `None`, only the matching link marked.

## 3. Content fix (hand-written pages)

`projects/index.html` and `projects/vim-config-with-YouCompleteMe/index.html`
sub-nav links read "Vim Config With Youcompleteme" (bad casing inherited from
the old slug-derived generation). Correct the link text to
"Vim Config With YouCompleteMe".

## 4. Housekeeping

- Add `.superpowers/` to the root `.gitignore` (visual-companion mockups).
- Regenerate the blog (`uv run build`) and commit the updated generated pages.

## Testing

- Builder: pytest unit tests for `current_slug` marking (TDD).
- Site: visual check of all four sub-nav pages in dark and light schemes via
  `uv run serve` — rules render, titles wrap balanced, current page marked on
  the vim page and the blog post page.

## Out of scope

- Dates or categories in the sub-nav (explicitly declined).
- Any other styling changes.
