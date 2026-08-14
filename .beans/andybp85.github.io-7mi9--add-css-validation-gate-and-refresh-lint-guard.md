---
# andybp85.github.io-7mi9
title: Add CSS validation gate and refresh lint guard
status: completed
type: task
priority: normal
created_at: 2026-08-14T18:34:09Z
updated_at: 2026-08-14T18:36:36Z
---

Repo-tooling grew a CSS validity gate (stylelint with declaration-property-value-no-unknown). Bring this repo up to date.

- [x] Run install-css-tooling.sh (.stylelintrc.json + stylelint pinned exact)
- [x] Refresh lint-guard fragment via install-lint-guard.sh
- [x] Prove the CSS gate blocks invalid declarations via a real commit attempt
- [x] Commit config + bean

## Summary of Changes

Installed stylelint (pinned exact) with .stylelintrc.json; refreshed the lint-guard fragment to the version that runs stylelint on staged CSS. Repo-wide check surfaced real issues: fixed three alpha-value notations in projects/projects.css and quoted B612-Regular font names in styles.css. Disabled no-descending-specificity (fires only on the intentional nested/page-order structure) and ignored generated pygments.css, matching .oxfmtrc.json. Proved the gate: a staged file with display: flexx and color: notacolor blocked the commit (exit 1). Documented the gate in README under CSS validity.
