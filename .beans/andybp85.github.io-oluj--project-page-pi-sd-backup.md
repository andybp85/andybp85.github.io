---
# andybp85.github.io-oluj
title: 'Project page: pi-sd-backup'
status: completed
type: task
priority: normal
created_at: 2026-07-02T13:42:06Z
updated_at: 2026-07-02T13:43:59Z
---

Add a hand-written project page for the pi-sd-backup tool (live Pi SD-card dd backup). Anonymize any unsafe info: no real UUIDs (placeholders only), no home-infra/service specifics. Update the shared projects subnav across index + all project pages.

## Summary of Changes

Added projects/pi-sd-backup/index.html — hand-written project page matching existing project-page head/subnav structure, loads pygments.css for code blocks. Covers the live dd clone, crash-consistent snapshot caveat, UUID-pinning to avoid dd hitting the wrong disk (cross-links the crypttab blog post), guard rails, dry-run, and cron.

Anonymization: only placeholder UUIDs; no real UUIDs, IPs, hostnames, or home-infra service specifics. Softened 'serves the home network' to a generic always-on framing.

Updated shared projects subnav (newest-first) across projects/index.html and all three existing project pages via scripted single-match replacement. Verified: new page serves 200, subnav on all 5 files, safety grep clean.
