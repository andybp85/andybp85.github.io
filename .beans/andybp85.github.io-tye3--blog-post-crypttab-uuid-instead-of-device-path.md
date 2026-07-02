---
# andybp85.github.io-tye3
title: 'Blog post: crypttab UUID instead of device path'
status: completed
type: task
priority: normal
created_at: 2026-07-02T12:55:12Z
updated_at: 2026-07-02T12:56:05Z
---

Write a short blog post crediting the original Medium LUKS tutorial and describing the crypttab change from /dev/sdX to UUID=. Then build and serve for review.

## Summary of Changes

Added src/posts/stop-hardcoding-dev-paths-in-crypttab.md — short post crediting the original Medium LUKS tutorial and describing the one change: reference the LUKS partition by UUID= (from blkid) in /etc/crypttab instead of /dev/sdX; fstab unchanged since it mounts the stable /dev/mapper name. Built via 'uv run build' and served at localhost:5500 (post returns 200).
