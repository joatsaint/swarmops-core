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

**Outcome:** 6 milestone posts drafted (Posts 1–6). See content-engine/pending/MONTE-build-posts/monte-build-posts.md for full text.

---

### Prompt 6 — Day 0 announcement

```
since we are documenting this monte project, shouldn't there be a first post 
announcing the project and its goals? and it is supposed to post on mondays 
so it doesn't conflict with the weekly article and supporting assets that get posted
```

**What was asked:** Randy caught that there was no announcement post — the first post in the series assumed the audience already knew what the project was.

**What happened:** AI drafted the Day 0 announcement post. Monday cadence confirmed (no conflict with Tuesday article schedule). Final title: "Twenty-five years ago I learned how to onboard a junior admin..."

**Cost of missing this:** If Randy hadn't caught it, Post 1 would have gone live on LinkedIn with no context. Followers would see a post about Driver's License layers for AI with no explanation of what SwarmOps is.

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

**What happened:** The AI was asked to update the SwarmOps README.md with a link to Randy's LinkedIn profile. Instead of verifying the URL against a known-good source, the AI pattern-matched from memory: `https://www.linkedin.com/in/randyskiles`

The correct URL is: `https://www.linkedin.com/in/randy-skiles`

The wrong URL was committed, pushed to the public repo, and was live on GitHub before Randy caught it. A second commit was required to correct it.

**Root cause:** AI pattern-matched a plausible URL from training data instead of checking a verified source. No policy check. No source verification. Output went straight to production.

**Cost:** One commit to correct. Reputational risk during the window it was live. More importantly: this is exactly what the SwarmOps Driver's License layer is designed to prevent.

**What SwarmOps prevents:** The Driver's License layer checks AI-generated outputs against a known-good policy before they execute. In this case, a URL verification policy would have forced the AI to resolve the LinkedIn URL from a verified file (`memory/reference_randy_profile_links.md`) rather than from memory. The output would have been blocked until the source was confirmed.

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

**What happened:** A long session covering many topics (HOT_STATE system, MONTE concept, LinkedIn posts, repo setup, MEMORY.md consolidation, PROJECT_MAP.md, Portfolio Discovery) hit the AI's context window limit before the Portfolio Discovery task completed. The session was automatically summarized and continued in a new context window. The incomplete task had to be resumed from the summary.

**Root cause:** AI context windows have a hard limit. Long, multi-topic sessions accumulate context faster than short, focused sessions. When the window fills, the system compresses earlier content — some detail is lost.

**Cost:** The Portfolio Discovery task that would have taken 30 minutes in a fresh session required reconstruction from a session summary. Some context had to be re-derived.

**Fix built:** The HOT_STATE.md system. When a session is interrupted before completing a task, the AI writes the exact next step, exact command, and exact file reference to HOT_STATE.md before closing. Next session reads it first and resumes immediately without re-explaining context.

**Lesson for your build:** Plan sessions around a single objective, not a topic. "Set up the repo and create the posts" is two sessions. "Set up the repo" is one session. You will hit context limits on complex projects. Design for recovery before you hit them.

---

### Incident 6 — Two memory systems drifted out of sync

**What happened:** The project had two MEMORY.md files — one in the Claude Code system memory folder (55+ entries, the live system) and one in the project's own `memory/` folder (3 entries, stale, not updated). They contained overlapping but inconsistent content.

**Root cause:** Memory was written to both locations at different points in the project's history, without a clear rule about which was authoritative.

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

These are the things the ICP for this project — senior IT professionals building with AI for the first time — are most likely to get wrong. They are drawn directly from what went wrong in Session 1.

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

The right answer depends on the task. For exploratory work (what should we build?), long sessions are fine — errors are low-cost. For production work (modify this config, push this commit), short focused sessions are safer — every correction is cheap compared to a wrong commit.

---

### 4. The AI does not know what tools it has unless you tell it

The Buffer API was fully operational. The AI still offered to have Randy paste the post manually, because "check the tool manifest" was not part of its session-start checklist.

This is not a flaw in the AI. It is a governance gap. The AI operates from whatever context it is given. If the context does not include "here are the tools available," the AI will default to the safe answer — which is often the manual answer.

Build your tool manifest before your first session. Update it every time you add a new tool. Make reading it the first thing the AI does at every session start.

---

### 5. Corrections that don't stick are signals, not failures

The date error appeared three times after being corrected. That is not evidence that the AI is broken. It is evidence that the correction was held in context (which degrades) rather than written to a file (which does not).

When you correct the same AI error twice, write a rule. Don't correct it a third time.

The override tracking system in SwarmOps Milestone 4 is built on this principle. Every correction is a data point. Thirty days of data tells you which corrections you're making manually every week because no one built the policy that catches them automatically.

---

### 6. Public and private boundaries require an explicit policy

Your AI assistant does not know the difference between what belongs in the public repo and what should stay local — unless you tell it. It cannot see that your STATUS.md contains internal codenames and business strategy. It sees a file in a folder. If you ask it to commit and push, it will commit and push.

Before your first AI-assisted git operation, define and document:
- What files must never be committed (and why)
- What the gitignore covers and why each entry is there
- What a commit review checklist looks like

This is your AI equivalent of the pre-flight checklist. It takes 15 minutes to write. It has a non-zero probability of saving you from a public disclosure incident.

---

### 7. The cost of AI mistakes is not just tokens

During Session 1, Randy said: "how do you compensate me for the wasted tokens you cost me?"

That is the right question. The AI's mistakes in a session cost:
- **Token cost:** The prompts used to catch and correct errors consumed API budget
- **Time cost:** Each correction required Randy to stop, verify, and re-prompt
- **Attention cost:** The burden of being the verification layer reduces the cognitive bandwidth available for actual work
- **Trust cost:** Every mistake the AI makes without catching it first shifts more of the verification burden back to the human

The governance layer in SwarmOps is not overhead. It is the cost offset for operating without one.

---

### 8. The context cliff is real — design for recovery before you hit it

AI context windows end. Not "if" — when. Every long session is approaching a context limit. When it hits, the AI's recall of early-session decisions, corrections, and state becomes compressed or lost.

For IT professionals: this is the equivalent of a process that runs out of memory. The graceful handling of that condition is not "hope it doesn't happen." It is designed-in graceful degradation — the session recovery chain.

Design your recovery mechanism at session 1. The HOT_STATE system was designed in session 1 because we hit the problem in session 1. You will hit the same problem. Build it first.

---

## Part 6 — The LinkedIn Content Strategy

### Why build in public?

The audience for SwarmOps Core is experienced IT professionals who are being told AI is too complex for them to build. It is not. They have been governing access, monitoring logs, and shutting down runaway processes for 20 years. SwarmOps is that governance applied to AI agents.

Building in public serves two goals:
1. Demonstrates that this is buildable with consumer hardware and existing IT knowledge
2. Documents the mistakes so others don't make them

### Post cadence

| Day | Format | Content | Status |
|---|---|---|---|
| Mon Jun 29 | Feed post | Day 0 — Project announcement | ✅ Scheduled in Buffer |
| Mon Jul 14 | Feed post | Post 1 — Driver's License layer (Milestone 1 complete) | Draft ready |
| Mon Jul 21 | Feed post | Post 2 — Self-correcting loop (Milestone 1 complete) | Draft ready |
| Mon Jul 28 | Feed post | Post 3 — Baseline protection (Milestone 2 complete) | Draft ready |
| Mon Aug 4 | Feed post | Post 4 — Override tracking (Milestone 3 complete) | Draft ready |
| Mon Aug 11 | Feed post | Post 5 — Auditor agent (Milestone 3 complete) | Draft ready |
| Mon Aug 18 | Feed post | Post 6 — Master kill switch (Milestone 3 complete) | Draft ready |

**Cadence rule:** Posts 1–6 are templates. Do not publish any milestone post before that milestone is built and verified. Date targets above assume one milestone per 2-week sprint. Adjust dates if the build takes longer. Authenticity is the product.

### Day 0 post — text

> Twenty-five years ago I learned how to onboard a junior admin.
>
> Restricted account. Limited scope. Every action logged. You shadow them for 90 days before they touch anything critical alone.
>
> You don't hand a new hire domain admin credentials on day one. That's not distrust. That's operational discipline.
>
> I've been thinking about AI agents the same way.
>
> What I'm building: SwarmOps Core. A local AI orchestration layer that treats AI models exactly like junior sysadmins on a tight leash. Command whitelist. Audit log. Self-correction loop. Kill switch.
>
> All of it runs on my GTX 1660 Ti. No cloud subscriptions. No API token bill at the end of the month.
>
> I'm building this in public because I think experienced IT pros are being told they're not qualified to build AI systems.
>
> You've been governing restricted access, monitoring logs, and shutting down runaway processes for 20 years.
>
> You already know how to do this. You just need to see it in the new language.
>
> I'll post every milestone here on Mondays.
>
> Repo is live — link in the first comment.
>
> \#AIGovernance #ITCareers #SwarmOps

### The incident as content

The LinkedIn URL incident — AI published a wrong URL to a live public repo without verifying it — is documented in the build posts as the strongest real-world proof of the SwarmOps thesis. A plausible output is not a correct output. Verification is not optional. That is the Driver's License layer in one incident.

The CONTENT NOTE in monte-build-posts.md captures this for use in Day 0 or Post 1. Decision on which post to use it in is pending.

---

## Part 7 — Future Log Entries

This document follows append-only rules. Past entries are never edited. Corrections are new entries with a reference to the entry being corrected.

When Milestone 1 is complete:
- Add a new session entry
- Document the prompts used to build the Driver's License layer
- Document any incidents during the build
- Update the post draft with actual implementation details before publishing

When an incident occurs:
- Add it to Part 3 immediately
- Note what SwarmOps would have prevented (or couldn't have prevented, and why)
- Record the actual cost (token cost if known, time cost, consequence)

---

*AI assists. Humans approve. Mistakes get logged.*
