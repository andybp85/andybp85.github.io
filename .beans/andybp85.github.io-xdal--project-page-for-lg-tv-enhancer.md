---
# andybp85.github.io-xdal
title: Project page for lg-tv-enhancer
status: completed
type: task
priority: normal
created_at: 2026-07-08T11:17:48Z
updated_at: 2026-07-08T11:19:17Z
---

Hand-written HTML project page at projects/lg-tv-enhancer/index.html in Andy's voice for the LG C9 Eye Comfort Mode daemon. Standalone — must NOT reference tv-dsp. Sync sub-nav across all project pages.

## Summary of Changes

Created projects/lg-tv-enhancer/index.html — project page in Andy's voice for the LG C9 Eye Comfort Mode daemon (f.lux-for-the-TV framing). Covers the reconcile-loop-not-scheduler design (no missed nights when the TV is off at sunset), the apply-once-per-phase manual-override behavior, and three webOS war stories: eyeComfortMode is write-only (getSystemSettings refuses the read -> blind trusted write), the TV drops off-network without closing TCP (timeout-guard every await), and bscpylgtv saves but never re-reads the pairing key (pin it). Closes on the parked circadian color-temp ramp (fights ISF Dark/Bright switching). Written fully standalone — no reference to tv-dsp, as requested.

Synced the duplicated <sub-nav> across all 7 project files: lg-tv-enhancer entry (raspberry-pi|automation, 2026-07-08) at top, current only on its own page. Verified 1 entry/file, no tv-dsp leak, 200 serving.
