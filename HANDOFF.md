# HANDOFF — project-monte-swarmops-core

**Project:** SwarmOps / MONTE — local-first, zero-token AI governance layer for IT pros
**Status:** ACTIVE
**Last updated:** 2026-07-09

## Where we left off

Milestone 1 + 2 complete. Milestone 4 (Ollama-based dynamic file classifier)
just shipped: `file_categorizer.py` rewritten from scratch with zero
hardcoded categories — it discovers categories from file content via Ollama
(3-phase: discovery → classification → move), plus `approval_gate.py` for
manual review of low-confidence files. Tested live against 11 real files:
8 moved automatically, 1 to `_needs_human_review/`, 2 to `_the_junk_drawer/`.
Committed and merged as **PR #7** in this repo (`github.com/joatsaint/swarmops-core`).

A companion 7-scene HeyGen build-video script documenting this work was
also written (lives in the parent project's memory —
`youtube-downloader/memory/HOT_STATE.md` — since it's a content-pipeline
asset, not SwarmOps code).

## Exact next step

**Milestone 3 — Network Compliance** is next up. Parallel hard deadline:
the Milestone 3 demo (Tests 2, 3, 5 from `PROJECT_BOARD.md`) must be
complete before the **Jul 14** MONTE-1 Buffer post goes out.

Before Milestone 3 work starts, confirm current state against
`PROJECT_BOARD.md` and `STATUS.md` in this folder — they are this repo's
existing tracking files and take precedence over anything summarized here
if they disagree.

## Project boundary

Root: `C:\Users\joatsaint\Desktop\On Desktop HP-CapCut Network Share\Claude Code My Projects\youtube-downloader\project-monte-swarmops-core`

This is an **independent git repo** (`swarmops-core` on GitHub), gitignored
by the parent `youtube-downloader` repo. It is nested inside
`youtube-downloader/` on disk but is not the same project — do not assume
state, decisions, or file conventions from one automatically apply to the
other. Do not write files here that belong to `youtube-downloader`'s
content/publishing pipeline, and vice versa.

This file is a lightweight pointer only. It does not replace
`PROJECT_BOARD.md`, `STATUS.md`, `README.md`, or `scope.md`, which already
exist in this repo and carry the fuller technical detail — read those for
depth. This file exists so a session can reorient in one read even if it
never opens youtube-downloader's memory system.
