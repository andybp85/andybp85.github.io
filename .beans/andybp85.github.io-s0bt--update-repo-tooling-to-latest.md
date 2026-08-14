---
# andybp85.github.io-s0bt
title: Update repo tooling to latest
status: completed
type: task
priority: normal
created_at: 2026-08-14T08:20:26Z
updated_at: 2026-08-14T08:23:30Z
---

Bring gates current per repo-tooling skill.

- [x] Refresh stale lint guard fragment (missing vnu/HTML gate)
- [x] Install secrets-commit-guard repo-local copy
- [x] Decline docs guard (.docs-guard-declined)
- [x] Suppress false py-tooling prompt (.py-tooling-declined; config lives in src/)
- [x] Verify vnu installed and gates fire

Skipped by request: docs guard, semver.

## Summary of Changes

Refreshed .git/hooks/pre-commit.d/30-lint-guard to the canonical version (adds the vnu HTML-validity section). Installed 10-secrets-guard repo-local. Touched .docs-guard-declined and .py-tooling-declined (both machine-ignored via ~/.config/git/ignore; py prompt was a false positive — ruff config lives in src/). Proved both gates block via real commits: lint guard caught invalid HTML (oxfmt + vnu), secrets guard caught a fake AKIA key. Note: invoking .git/hooks/pre-commit by hand runs zero fragments because core.hooksPath makes rev-parse --git-path resolve under ~/.claude/git-hooks — only a real git commit exercises the chain.
