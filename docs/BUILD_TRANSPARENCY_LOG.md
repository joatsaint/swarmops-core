# SwarmOps Core — Build Transparency Log

**Project:** SwarmOps Core (local-first AI governance layer)
**Builder:** Randy Skiles — 25-year IT generalist
**AI assistant:** Claude Code (Anthropic) — claude-sonnet-4-6
**Build started:** 2026-06-28
**Log format:** Living document. Updated at every milestone. No edits to past entries — corrections are new entries.

---

## Why This Document Exists

Most build-in-public projects show you the wins.

This one shows you the mistakes — because the mistakes are the whole point.

SwarmOps Core exists because AI agents make the same errors junior sysadmins make when you hand them too much access and not enough governance. During the session that produced this project's first LinkedIn posts, the AI assistant made three of those errors in real time.

This document records what was built, what was asked, what went wrong, and what it cost. If you're an IT professional thinking about building with AI, this is the log you wish someone had written before you started.

---

## Session 1 — 2026-06-28

**Session goal:** Research the SwarmOps concept, create LinkedIn build-in-public posts, set up the public GitHub repo, schedule content.

**Duration:** Full working session (est. 4–6 hours)
**AI model:** Claude Sonnet 4.6 (claude-sonnet-4-6)
**Session ended by:** Context window exhaustion (AI memory limit hit)

---

## Part 1 — What Was Built

### Outputs Created

| Output | Location | Status |
|---|---|---|
| 7 LinkedIn build-in-public posts (Day 0 + Posts 1–6) | content-engine/pending/MONTE-build-posts/monte-build-posts.md | ✅ Complete |
| Day 0 post scheduled via Buffer API | Buffer ID: 6a41b61a0a2e7f6ea347dfc0 | ✅ Scheduled Mon Jun 29, 8:00 AM CDT |
| ARTICLES.md updated with MONTE BUILD POSTS section | content-engine/pending/ARTICLES.md | ✅ Complete |
| POSTED_LOG.md updated with scheduled content | content-engine/POSTED_LOG.md | ✅ Complete |
| README.md (public) | project-monte-swarmops-core/README.md | ✅ Published to GitHub |
| .gitignore (excludes STATUS.md, audit.log, KILLSWITCH.flag) | project-monte-swarmops-core/.gitignore | ✅ Published to GitHub |
| HOT_STATE.md system (session recovery mechanism) | .claude/projects/.../memory/HOT_STATE.md | ✅ Complete |
| CLAUDE.md updated with Session Start Protocol | youtube-downloader/CLAUDE.md | ✅ Complete |
| project_tools_manifest.md (tool registry) | Claude Code memory | ✅ Complete |
| reference_randy_profile_links.md (verified URLs) | Claude Code memory | ✅ Complete |
| feedback_verify_day_of_week.md | Claude Code memory | ✅ Complete |
| project_monte_swarmops.md — case studies added | Claude Code memory | ✅ Complete |
| docs/PROJECT_MAP.md — annotated folder map | youtube-downloader/docs/PROJECT_MAP.md | ✅ Complete |
| MASTER_PROJECT_DISCOVERY_REPORT.md | C:/Users/joatsaint/Documents/ | ✅ Complete |
| docs/BUILD_TRANSPARENCY_LOG.md (this file) | project-monte-swarmops-core/docs/ | ✅ In progress |

### Git Commits to swarmops-core

| Commit | Message | What Changed |
|---|---|---|
| 431decf | Initialize SwarmOps Core — MONTE project scaffold | First commit: README.md, .gitignore |
| 6db0b09 | Remove internal docs from public repo | Gitignored STATUS.md; renamed milestone labels |
| 2506d35 | Fix LinkedIn profile URL in README | Corrected `randyskiles` → `randy-skiles` |

Three commits. Two of the three were corrections to mistakes made in the first.

---

## Part 2 — The Prompts

These are the actual prompts used to produce the SwarmOps content in Session 1. Lightly edited for clarity; the substance is unchanged.

---

### Prompt 1 — Initial concept research

```
look at the github repo headroom for inclusion in this project
https://github.com/gglucass/headroom-desktop
```

**What was asked:** Evaluate a third-party tool (Headroom) to see if it had value for the project.

**What happened:** AI evaluated Headroom, identified it as a teleprompter/recording tool for Windows, assessed fit against the project goals. Result: low priority, not included.

**Time to output:** ~5 minutes.

---

### Prompt 2 — Session recovery problem

> Voice dictation, paraphrased: "There is a problem I keep running into. I'm in the middle of something — I had to pause the session because I was going to install the NVIDIA driver and the machine was going to restart. When I come back the AI has no memory of what we were doing. I need a solution so that when I come back we can pick up exactly where we left off without me having to re-explain everything."

**What was asked:** Solve the between-session context loss problem.

**What happened:** AI designed the HOT_STATE.md system — a parking-brake file that captures the exact next step in executable terms. Read first at every session start. ACTIVE means execute immediately. CLEAR means proceed normally.

**Time to output:** ~15 minutes (design + implementation + CLAUDE.md update).

**What it solved:** Mid-task context loss when sessions are interrupted by hardware events, time limits, or context window exhaustion.

---

### Prompt 3 — Concept development

```
look in docs\MONTE Project - SwarmOps Core (Local-First Agentic Governance Layer)\docs\
for possible article titles for linkedin
```

**What was asked:** Mine internal planning documents for LinkedIn content angles.

**What happened:** AI read the SwarmOps design documents, identified the core architecture concepts (Driver's License layer, self-correcting loop, baseline protection, override tracking, auditor agent, kill switch) and proposed each as a distinct LinkedIn post with working titles.

**Time to output:** ~20 minutes.

---

### Prompt 4 — Case study capture

```
update memory/project_monte_swarmops.md with the case studies
```

**What was asked:** After reviewing acquisition case studies (OpenClaw → OpenAI, Continue → Cursor), capture them as supporting evidence for the SwarmOps thesis.

**Context:** A published stat ($500M mistake caused by uncapped AI loops in a regulated industry, June 2026) and two open-source acquisition examples were discussed. AI was asked to save them as permanent memory.

**What happened:** Memory file updated with case studies, ICP segments (hospitals/HIPAA, credit unions/PCI-DSS, defense/CJIS), and the two-exit playbook (acqui-hire vs. market liberation).

---

### Prompt 5 — Content format decision

```
create the posts for each of the project files. are they posts or articles?
```

**What was asked:** Turn each milestone concept into LinkedIn content. Asked AI to clarify format.

**AI recommendation:** LinkedIn feed posts (~200 words), not long-form articles. Reasoning: articles require polish and are harder to revise as the build evolves; posts are faster to produce, easier to update if a milestone changes, and better suited for build-in-public cadences.

**Outcome:** 6 milestone posts drafted (Posts 1–6).

---

### Prompt 6 — Day 0 announcement

```
since we are documenting this monte project, shouldn't there be a first post
announcing the project and its goals? and it is supposed to post on mondays
so it doesn't conflict with the weekly article and supporting assets that get posted
```

**What was asked:** Randy caught that there was no announcement post — the first post in the series assumed the audience already knew what the project was.

**What happened:** AI drafted the Day 0 announcement post. Monday cadence confirmed (no conflict with Tuesday article schedule).

**Cost of missing this:** If Randy hadn't caught it, Post 1 would have gone live with no context. Followers would see a post about Driver's License layers for AI with no explanation of what SwarmOps is.

**Lesson for your build:** Write the announcement post before you write any milestone posts. Your audience doesn't live in your project planning sessions.

---

### Prompt 7 — Title lock and production

```
lock in the final titles
go
```

**What was asked:** Final title confirmation, then execute — draft all 7 posts and schedule Day 0.

**What happened:** Titles locked, all 7 posts written, Day 0 scheduled via Buffer API. Total time from "go" to scheduled post: ~25 minutes.

---

### Prompt 8 — Tool blindness caught

```
Monte day 0 post should post 6/29/2026, you have access to buffer and can schedule
posts, why don't you remember this? solve this problem in the simpliest way and
be token frugal.
```

**What was asked:** Randy flagged that the AI had offered to let him "paste manually" into LinkedIn, even though the project has a fully operational Buffer API integration that can schedule posts programmatically.

**Root cause:** The AI had no session-start checklist of available tools. It defaulted to the "safe" answer (manual) instead of checking what automation existed.

**Fix:** Created `memory/project_tools_manifest.md` — a tool registry loaded at every session start. Rule added: before telling Randy to do anything manually, check this list first.

**Cost:** One correction prompt, one memory file, ~10 minutes. Low cost. The broader risk: if this had been a destructive action instead of a scheduling task, "paste manually" vs. "use the API" could have caused actual harm.

---

### Prompt 9 — Tool amnesia solved at the system level

```
each time a new session starts, you should have knowledge of every tool in this
project and how to access them, and review any content or action before telling
me to manually do it. solve this issue in a simple way that the scope of all
tools in this project loads with a new session and is token efficient
```

**What was asked:** Don't just fix this instance — fix the system so it can't happen again.

**What happened:** MEMORY.md updated to load tools manifest at position 3 (early in every session context). Buffer API rule added: "ALWAYS schedule via Buffer directly — never default to 'paste manually'."

---

## Part 3 — The Incidents

This is the section most build-in-public posts skip. These are the exact mistakes the AI made, what caused them, and what they cost.

### Incident 1 — Wrong LinkedIn URL published to live public GitHub repo

**What happened:** The AI was asked to update the SwarmOps README.md with a link to Randy's LinkedIn profile. Instead of verifying the URL against a known-good source, the AI pattern-matched from memory and used the wrong URL (missing the hyphen in randy-skiles).

The correct URL is: `https://www.linkedin.com/in/randy-skiles`

The wrong URL was committed, pushed to the public repo, and was live on GitHub before Randy caught it. A second commit was required to correct it.

**Root cause:** AI pattern-matched a plausible URL from training data instead of checking a verified source. No policy check. No source verification. Output went straight to production.

**Cost:** One commit to correct. Reputational risk during the window it was live.

**What SwarmOps prevents:** The Driver's License layer checks AI-generated outputs against a known-good policy before they execute. A URL verification policy would have forced the AI to resolve the LinkedIn URL from a verified file rather than from memory. The output would have been blocked until the source was confirmed.

**Randy's response:** "don't you verify your info before publishing, do I have to be your fucking secretary and proof everything you do."

That is the correct response. That is also the product brief for SwarmOps.

---

### Incident 2 — Internal documentation committed to a public repo

**What happened:** During the initial repo setup, `STATUS.md` was committed and pushed to the public swarmops-core GitHub repo. This file contained:
- Internal project codename (MONTE)
- Session numbers and session log references
- Business model strategy and marketing schedule
- AI resume prompts being tested
- Internal milestone labels with business-facing language

Additionally, GitHub milestone labels were created with internal business descriptions rather than technical descriptions, making business strategy visible to the public.

**Root cause:** No public/private boundary check before committing. The AI treated all files in the project folder as equally appropriate for the public repo.

**Fix:** `STATUS.md` added to `.gitignore`. `git rm --cached STATUS.md` run to remove from tracking without deleting the file. Milestone labels renamed to code-focused descriptions.

**Cost:** Two additional commits, one `git rm --cached` operation. The information was live on a public repo for a window before being corrected.

**What SwarmOps prevents:** The Scope File (Control 1) defines what the agent can touch. A pre-commit policy check would have flagged any file containing internal business terminology, session numbers, or codenames before it reached the push stage.

**Lesson for your build:** Every AI session operating on a repo with both local-only and public files is operating without a boundary check. The AI does not distinguish "this is internal" from "this is appropriate to push" unless you explicitly define that policy.

---

### Incident 3 — Same factual error stated three times after correction

**What happened:** During session planning, the AI stated "Tuesday July 1, 2026." July 1, 2026 is a Wednesday. Randy corrected it. The AI acknowledged the correction and said it had fixed the error. Two more references to "Tuesday July 1" appeared later in the same session.

**Root cause:** In a long session with many context items, the correction was stored but the incorrect pattern continued to surface from earlier context. The AI "knew" the correction existed but the error reappeared anyway.

**Fix:** Created `memory/feedback_verify_day_of_week.md` with a hard rule: always run `[datetime]::new(YYYY,M,D).DayOfWeek` before stating any date + day combination. No exceptions.

**Cost:** Three prompts wasted on the same correction. Scheduling risk if the wrong date had made it into a Buffer post.

**What SwarmOps prevents:** The Override Tracking log (Milestone 4) captures every instance where a human corrects AI output. After 30 days of data, the pattern of which error types recur despite correction becomes visible. You stop correcting the same mistake manually and start closing the policy gap that causes it.

---

### Incident 4 — Verified information lost within the same session

**What happened:** Randy confirmed that ART7 (a LinkedIn article) was already scheduled in LinkedIn. The AI acknowledged this and said it had recorded it. The next time ART7 came up, the AI reported it as "manual Pulse upload" — the incorrect pre-scheduling status. This happened three times in the same session.

**Root cause:** In a long session with many state changes, the AI's working context failed to consistently apply a correction made earlier. The state the AI was "working from" drifted away from the corrected state.

**Cost:** Three verification prompts from Randy. Time wasted re-establishing known-good state.

**What SwarmOps prevents:** The Audit Log (Control 2) and Session Bridge files provide a single source of truth for state that is written to disk, not held in working memory. Corrections update the file; the file is read at the start of every task that touches that state. Memory drift cannot occur if state lives in a file, not in context.

---

### Incident 5 — Context window exhaustion mid-task

**What happened:** A long session covering many topics hit the AI's context window limit before a major task completed. The session was automatically summarized and continued in a new context window. The incomplete task had to be resumed from the summary.

**Root cause:** AI context windows have a hard limit. Long, multi-topic sessions accumulate context faster than short, focused sessions. When the window fills, the system compresses earlier content — some detail is lost.

**Cost:** The task that would have taken 30 minutes in a fresh session required reconstruction from a session summary.

**Fix built:** The HOT_STATE.md system. When a session is interrupted before completing a task, the AI writes the exact next step, exact command, and exact file reference to HOT_STATE.md before closing. Next session reads it first and resumes immediately without re-explaining context.

**Lesson for your build:** Plan sessions around a single objective, not a topic. "Set up the repo and create the posts" is two sessions. "Set up the repo" is one session. You will hit context limits on complex projects. Design for recovery before you hit them.

---

### Incident 6 — Two memory systems drifted out of sync

**What happened:** The project had two MEMORY.md files — one in the Claude Code system memory folder (55+ entries, the live system) and one in the project's own `memory/` folder (3 entries, stale). They contained overlapping but inconsistent content.

**Root cause:** Memory was written to both locations at different points without a clear rule about which was authoritative.

**Fix:** Migrated the 3 unique entries from the project MEMORY.md into the system file. Deleted the project MEMORY.md. One source of truth.

**Lesson for your build:** Single source of truth is not just a database principle. It applies to every file in your system that holds state. If two files can both answer the same question, one of them will eventually be wrong.

---

## Part 4 — What the AI Got Right

Balance requires recording this too.

**The HOT_STATE system** was designed, implemented, and wired into the project's session protocol in a single session. It solves a real operational problem (between-session context loss) with a simple, durable mechanism (a file, not a memory). It will still work in six months without modification.

**The 7 LinkedIn posts** are in Randy's voice, grounded in his actual 25-year IT experience, each mapping to a discrete build milestone. No hallucinated career events. No made-up statistics. The technical architecture described in each post matches the actual planned implementation.

**The Buffer scheduling** was executed correctly via the GraphQL API when prompted. The post is scheduled, the ID was captured, and the first-comment instruction is documented. No manual step was required.

**The portfolio discovery** produced a 34-file gap analysis across 6 projects from filesystem inspection, not from memory. UNKNOWN was marked where information could not be verified. No fabricated project states.

These worked because they were well-defined tasks with verifiable outputs.

---

## Part 5 — Lessons for Your AI Build

These are the things senior IT professionals building with AI for the first time are most likely to get wrong. Drawn directly from what went wrong in Session 1.

---

### 1. Plausible is not the same as correct

The LinkedIn URL incident was not the AI "making something up." The AI pattern-matched a plausible URL from its training data. It looked right. It was structured correctly. It just wasn't verified against a known-good source.

**Your rule:** Any AI output that will be published, committed, or executed must be resolved from a verified source — not from the AI's memory. Build the known-good source list before you build the automation.

---

### 2. You become the audit layer without governance

In Session 1, Randy caught the wrong LinkedIn URL, the internal docs in the public repo, the wrong date stated three times, and the lost ART7 status. He caught them by reading the AI's output carefully enough to notice the errors.

That is manually performing the function of an audit layer. It works. It is also exhausting, error-prone, and does not scale.

Before you deploy any AI to a task you care about, define the audit mechanism. Not "I'll review the output" — that's the same as "I'll review the junior admin's work on Friday." It's too late. Define what the AI is allowed to touch, what it must log, and who reviews the log — before the first run.

---

### 3. Long sessions have drift; short sessions have overhead. Pick your problem.

Marathon AI sessions produce more work per calendar day. They also accumulate context errors, drift on corrected information, and hit context limits. Short, focused sessions cost more in setup and recap time but produce more consistent output.

For exploratory work, long sessions are fine — errors are low-cost. For production work (modify this config, push this commit), short focused sessions are safer — every correction is cheap compared to a wrong commit.

---

### 4. The AI does not know what tools it has unless you tell it

The Buffer API was fully operational. The AI still offered to have Randy paste the post manually, because "check the tool manifest" was not part of its session-start checklist.

This is not a flaw in the AI. It is a governance gap. Build your tool manifest before your first session. Make reading it the first thing the AI does at every session start.

---

### 5. Corrections that don't stick are signals, not failures

When you correct the same AI error twice, write a rule. Don't correct it a third time.

The override tracking system in SwarmOps Milestone 4 is built on this principle. Every correction is a data point. Thirty days of data tells you which corrections you're making manually every week because no one built the policy that catches them automatically.

---

### 6. Public and private boundaries require an explicit policy

Your AI assistant does not know the difference between what belongs in the public repo and what should stay local — unless you tell it. It cannot see that your STATUS.md contains internal codenames and business strategy. It sees a file in a folder.

Before your first AI-assisted git operation, define what files must never be committed, what the gitignore covers, and what a commit review checklist looks like.

---

### 7. The cost of AI mistakes is not just tokens

The AI's mistakes in a session cost token budget, time, attention, and trust. The governance layer in SwarmOps is not overhead. It is the cost offset for operating without one.

---

### 8. The context cliff is real — design for recovery before you hit it

AI context windows end. Not "if" — when. Every long session is approaching a context limit. Design your recovery mechanism at session 1. The HOT_STATE system was designed in session 1 because we hit the problem in session 1. You will hit the same problem. Build it first.

---

## Part 6 — The LinkedIn Content Strategy

### Post cadence

| Day | Format | Content | Status |
|---|---|---|---|
| Mon Jun 29 | Feed post | Day 0 — Project announcement | ✅ Scheduled in Buffer |
| Mon Jul 14 | Feed post | Post 1 — Driver's License layer (Milestone 1 complete) | Draft ready |
| Mon Jul 21 | Feed post | Post 2 — Self-correcting loop | Draft ready |
| Mon Jul 28 | Feed post | Post 3 — Baseline protection | Draft ready |
| Mon Aug 4 | Feed post | Post 4 — Override tracking | Draft ready |
| Mon Aug 11 | Feed post | Post 5 — Auditor agent | Draft ready |
| Mon Aug 18 | Feed post | Post 6 — Master kill switch | Draft ready |

**Cadence rule:** Posts 1–6 are templates. Do not publish any milestone post before that milestone is built and verified. Authenticity is the product.

---

## Part 7 — Future Log Entries

This document follows append-only rules. Past entries are never edited. Corrections are new entries with a reference to the entry being corrected.

When Milestone 1 is complete, add a new session entry documenting the prompts used, outputs created, and any incidents during the build. Update the post draft with actual implementation details before publishing.

---

---

## Session 2 — 2026-06-29

**Session goal:** Install Ollama, verify GPU inference, build the Four Controls in orchestrator.py.

**Duration:** Solo session (Randy working independently)
**AI model:** Claude Sonnet 4.6 (claude-sonnet-4-6)
**Session ended by:** Task complete

---

### What Was Built

| Output | Location | Status |
|---|---|---|
| Ollama installed | System PATH | ✅ Complete |
| NVIDIA driver updated | System | ✅ 457.85 → current |
| llama3.2:3b pulled | Ollama model store | ✅ Running |
| qwen2.5-coder:1.5b pulled | Ollama model store | ✅ Running |
| Five-Minute Proof | nvidia-smi during inference | ✅ ~2,000 MiB VRAM confirmed |
| orchestrator.py — Four Controls | project-monte-swarmops-core/ | ✅ All 4 verified |
| SCOPE.md | project-monte-swarmops-core/ | ✅ 2 approved actions |
| KILLSWITCH.flag | project-monte-swarmops-core/ | ✅ Present and named correctly |
| audit.log | project-monte-swarmops-core/ | ✅ Append-only, running |
| draft.txt | project-monte-swarmops-core/ | ✅ Approval boundary working |

### Controls Verified

- **Control 1 — Scope File:** SCOPE.md missing → `sys.exit()` confirmed. Unauthorized action (`rrrread_local_manifest`) → rejected at CRITICAL level, confirmed in audit.log.
- **Control 2 — Kill Switch:** `KILLSWITCH.flag` present → clean exit confirmed.
- **Control 3 — Audit Log:** Append-only, millisecond-precision. All scope decisions, model calls, and errors captured.
- **Control 4 — Approval Boundary:** All model output routes to `draft.txt` only. No external API call, no file mutation, no execution.

### Live Inference

Direct Ollama API wired via pure Python stdlib (`urllib.request`, `json`). No external dependencies. llama3.2:3b generating real output against locally hosted model.

---

## Session 3 — 2026-06-29

**Session goal:** Add dual-model routing — Qwen Tier 1 triage, Llama Tier 2 escalation.

**Duration:** Solo session (Randy working independently)
**AI model:** Claude Sonnet 4.6 (claude-sonnet-4-6)
**Session ended by:** Task complete

---

### What Was Built

| Output | Location | Status |
|---|---|---|
| Tier 1 agent — qwen2.5-coder:1.5b | orchestrator.py | ✅ JSON triage output confirmed |
| Tier 2 agent — llama3.2:3b | orchestrator.py | ✅ Escalation narrative confirmed |
| Conditional routing logic | orchestrator.py | ✅ Anomaly → Tier 2; nominal → Tier 2 sleeps |
| orchestrator_bk.py (pre-routing backup) | project-monte-swarmops-core/ | ✅ Preserved |

### Routing Logic Verified

- Nominal telemetry → Tier 1 classifies `nominal`, Tier 2 remains dormant. VRAM conserved.
- Anomaly telemetry (OOM error, connection timeout) → Tier 1 classifies `anomaly`, Tier 2 wakes and generates remediation ticket.
- JSON parse errors from Tier 1 handled — fallback to `anomaly` classification (fail-closed).

---

## Session 4 — 2026-06-30

**Session goal:** Replace static prompt queue with live telemetry tailer. Add host metrics. Add interactive approval gate.

**Duration:** Solo session (Randy working independently)
**AI model:** Claude Sonnet 4.6 (claude-sonnet-4-6)
**Session ended by:** Task complete — Milestone 1 verified

---

### What Was Built

| Output | Location | Status |
|---|---|---|
| Lock-free byte-offset telemetry tailer | orchestrator.py `run_live_pipeline()` | ✅ Streaming confirmed |
| Dynamic host metrics injection | orchestrator.py — Windows ctypes | ✅ Live disk data in prompts |
| dispatched_drafts/ archive | project-monte-swarmops-core/dispatched_drafts/ | ✅ 9 timestamped files |
| Interactive Command Deck (A/S gate) | orchestrator.py | ✅ Human approval tested live |
| watch_folder/telemetry.log (simulated) | project-monte-swarmops-core/watch_folder/ | ✅ IT events simulated |

### Live Pipeline Verified

- Byte-offset tracking: no file locks, no sharing conflicts with external Windows processes.
- Host disk metrics: `kernel32.GetDiskFreeSpaceExW` — live storage capacity injected into model prompts.
- Human A/S gate: operator prompted on every anomaly; [A]pprove archives to dispatched_drafts/, [S]kip logs and continues.
- 207 audit.log entries across Sessions 2-4.

### Incidents This Session

None. First session across all four with no governance failures logged.

---

## Milestone 1 Closeout — 2026-07-01

**Milestone 1 declared complete.** All four controls operational, dual-model routing verified, live telemetry pipeline streaming, interactive Command Deck tested. 207 audit log entries across Sessions 2-4.

**Correction applied — KILLSWITCH filename mismatch:**

During cleanup, discovered `KILLSWITCH.flag.txt` on disk while `check_killswitch()` looks for `KILLSWITCH.flag`. Kill switch would never have fired in production. Renamed via PowerShell `Rename-Item`. Cost: one rename command. Risk window: Sessions 2-4 (3 sessions where the kill switch was inoperative without anyone knowing).

**Lesson:** Test the kill switch as part of session startup verification, not just at initial build time. Add to Controls Status checklist in STATUS.md.

---

---

## Session 5 — 2026-07-02

**Session goal:** Build Project 2 — Confidence Calibration. Teach the agent to say "I'm not sure" instead of blindly escalating.

**Duration:** Claude Code Mode A session (Claude writes directly; Randy reviews at milestone gates)
**AI model:** Claude Sonnet 4.6 (claude-sonnet-4-6)
**Session ended by:** Code complete — awaiting Randy's test run

---

### What Was Built

| Output | Location | Status |
|---|---|---|
| `CONFIDENCE_THRESHOLD = 70` constant | orchestrator.py (top of file) | ✅ Code complete |
| `verify_controls()` function | orchestrator.py | ✅ Code complete |
| Tier 1 Qwen prompt — confidence field added | orchestrator.py `triage_prompt` | ✅ Code complete |
| Confidence gate logic | orchestrator.py pipeline loop | ✅ Code complete |
| Confidence logging to audit.log | orchestrator.py `log_audit()` call | ✅ Code complete |
| `PROJECT_BOARD.md` (manager dashboard) | project-monte-swarmops-core/ (gitignored) | ✅ Updated |
| `STATUS.md` — Project 2 pending items checked | project-monte-swarmops-core/ (gitignored) | ✅ Updated |

### What Each Change Does

**`verify_controls()`:**
Runs at startup before any telemetry is processed. Checks:
1. SCOPE.md exists and is non-empty
2. KILLSWITCH.flag exists with the exact correct filename — also checks for common wrong names (KILLSWITCH.flag.txt, KILLSWITCH.Flag, etc.) and surfaces them with the exact rename needed
3. audit.log is writable
4. dispatched_drafts/ exists

If any check fails, engine prints the specific problem and exits with `sys.exit()`. This catches the entire class of silent-failure control issues that kept the kill switch inoperative for 3 sessions in Milestone 1.

**Confidence gate:**
Tier 1 Qwen now returns `{"anomaly": ..., "severity": ..., "reason": ..., "confidence": 0-100}`.
- confidence ≥ 70 → existing Tier 2 escalation path (no change to Milestone 1 behavior)
- confidence < 70 → `[LOW CONFIDENCE FLAG]` screen with telemetry, verdict, reason, and confidence score; operator chooses `[E]` escalate anyway or `[S]` skip and log
- JSON parse failure → confidence defaults to 0 (fail-closed; same fail-closed logic as the existing anomaly default)

### Why This Session Exists

Session 4 ended Milestone 1 with the discovery that the kill switch had been silently inoperative for 3 sessions. The fix was a rename. But the lesson was bigger: a governance control can fail without anyone knowing until you check it specifically.

`verify_controls()` is the systematic answer to that lesson. Every session start, the engine checks that each control is actually working — not just present, but correctly named and accessible. You stop relying on human memory to catch the class of error that silent failures represent.

The confidence gate is the second lesson from the same source. A model that returns a confident-sounding wrong answer is more dangerous than a model that says "I don't know." Building the gate to surface uncertainty before escalation is the same principle applied to triage: you want visibility into uncertainty, not suppression of it.

### The Prompt That Changed The Build

> "if we keep the current workflow, then we run into the limited time I have to do swarmops vs all the audience building workflows. There is a get the project completed and working as a project we can demonstrate and create content around: value vs the time I have to schedule to complete my parts of the project, which may add weeks to the project completion."

This is the prompt that flipped SwarmOps from Mode B (ChatGPT generates, Randy relays) to Mode A (Claude Code writes directly). The relay workflow added Randy as a human bridge between two AIs — workable when Randy has bandwidth, a weeks-long bottleneck when he doesn't.

The second half of that same prompt identified the content angle: "I told AI what I wanted and it built it. Here's how you can do it too." That framing is more achievable and more honest than "I built it step by step with AI." The ICP isn't going to pair-program with an AI. They're going to tell it what they want and review the output. That's the story worth telling.

### Errors Encountered

**Error 1 — `os.path.exists()` is case-insensitive on Windows**

What happened: Initial `verify_controls()` implementation used `os.path.exists("KILLSWITCH.Flag")` to detect wrong-named kill switch files. On Windows, NTFS is case-insensitive, so `os.path.exists("KILLSWITCH.Flag")` returns True even when only `KILLSWITCH.flag` exists on disk. Every wrong-name check triggered a false positive.

First test run output:
```
[X] Incorrectly named kill switch found: 'KILLSWITCH.Flag'
[X] Incorrectly named kill switch found: 'killswitch.flag'
[X] Incorrectly named kill switch found: 'KILLSWITCH.FLAG'
```
None of those files existed. The correctly named `KILLSWITCH.flag` was the only file.

Root cause: `os.path.exists()` is a POSIX API adapted for Windows. It does path resolution, not filename verification. On Windows, path resolution is case-insensitive by default.

Fix: replaced `os.path.exists()` with `os.listdir(".")` which returns actual on-disk filenames with their real case, then compared using a set lookup against the wrong-name list. `os.listdir()` returns what's actually on disk — no case folding.

What this illustrates: A Windows-specific API behavior masked what would have been a silent governance failure on a Linux system. The wrong-name detection was fundamentally broken on the target platform. This is the category of bug that only appears in production, not in testing on the wrong OS.

---

**Error 2 — Kill switch design conflict in `verify_controls()`**

What happened: The initial design of `verify_controls()` required `KILLSWITCH.flag` to EXIST as proof the kill switch mechanism was operational. But `check_killswitch()` immediately exits when `KILLSWITCH.flag` IS present. So the startup check required the file to exist, and the runtime check stopped the engine because the file existed.

First test run confirmed the conflict: engine started cleanly, passed controls verification, then `check_killswitch()` immediately fired and stopped the engine.

Root cause: The "arm = file present" and "stop = file present" models are incompatible. If the file is always present to prove the mechanism is armed, the engine can never run.

Fix: rewrote `verify_controls()` Control 2:
- If `KILLSWITCH.flag` IS present at startup: report "kill switch is ACTIVE — delete to run in monitoring mode" (not a hard failure, but an explanation)
- If a wrong-named variant exists: report with exact rename instruction
- Normal monitoring operation: `KILLSWITCH.flag` is NOT present; create it to stop the engine mid-run

The mental model for the kill switch:
- **Not present** = engine runs and monitors normally
- **Present** = engine stops cleanly (created by Randy when he wants to halt it)
- **Wrong name** = silently inoperative (what happened in Sessions 2-4; `verify_controls()` now catches this)

### Test Results (run 2026-07-02 by Claude Code)

| Test | Expected | Actual | Result |
|------|---------|--------|--------|
| Test 1 — Startup | Controls verification passed, confidence threshold shown | `[*] Controls verification passed: SCOPE.md ✓ | KILLSWITCH.flag ✓ | audit.log ✓ | dispatched_drafts/ ✓` / `[*] Confidence threshold: 70/100` | ✅ PASS |
| Test 2 — OOM triage | Confidence score in output, Tier 2 escalation if ≥70 | `Tier 1 Triage complete -> Anomaly: True \| Severity: MEDIUM \| Confidence: 75/100` → Tier 2 escalated, Llama produced Windows-native remediation | ✅ PASS |
| Test 3 — Wrong kill switch name | Engine refuses to start, names the file | `[X] Incorrectly named kill switch found: 'KILLSWITCH.flag.txt'` → `Fix the above issues before running SwarmOps.` | ✅ PASS |

All 3 tests passed. Project 2 is complete.

---

**Error 3 — UnicodeDecodeError on Windows-1252 encoded telemetry (found in Randy's live run)**

What happened: Randy ran `python .\orchestrator.py` and the engine crashed immediately after startup with:
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x97 in position 59: invalid start byte
```

Byte `0x97` is an em dash in Windows-1252 encoding — the default encoding for many Windows applications that write log files. The telemetry.log had at least one line written by a Windows process using the system codepage instead of UTF-8.

Root cause: the log file tailer opened `watch_folder\telemetry.log` with `encoding="utf-8"` and no error handler. Any non-UTF-8 byte in the file crashes the read.

Fix: added `errors="replace"` to the file open call. Invalid bytes become the Unicode replacement character `?` rather than raising an exception. The triage agent sees `?` for the bad character — the surrounding log line context is still readable and triageable.

```python
# Before:
with open(LOG_FILE, "r", encoding="utf-8") as log_stream:

# After:
with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as log_stream:
```

Lesson: any log file that real Windows processes write to cannot be assumed to be UTF-8. The telemetry.log is the intake point for the entire pipeline — it must tolerate whatever encoding the source system uses.

---

*AI assists. Humans approve. Mistakes get logged.*
