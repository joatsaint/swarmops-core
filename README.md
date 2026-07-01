# SwarmOps Core

**A local-first, zero-token agentic governance layer for IT professionals.**

Built by a 25-year IT generalist. Runs on consumer hardware. Costs $0 to operate.

---

## What This Is

SwarmOps Core treats AI models like heavily restricted Junior SysAdmins — the same way
you'd onboard a new hire: scoped access, audit trail, kill switch, and a change-management
approval boundary before anything touches production.

No cloud tokens. No data leaves your machine. No runaway API bills.

---

## The Architecture

```
[ User / Ticket Trigger ]
         │
         ▼
┌─────────────────────────┐
│  SWARMOPS ORCHESTRATOR  │ ◄──► [ IDENTITY & ACCESS REGISTER ]
└───────────┬─────────────┘      (GPO / Driver's License Layer)
            │
            ▼
┌─────────────────────────┐
│    EPHEMERAL SANDBOX    │
│   (Serial VRAM Handoff) │
└───────────┬─────────────┘
            │
    ┌───────┴────────┐
    ▼                ▼
PLAN → EXECUTE → AUDIT
(Local models, zero cloud cost)
```

### The Four Controls (built before anything else)

1. **Scope File** — explicit allow-list of what the agent can touch. Missing = stop.
2. **Kill Switch** — `KILLSWITCH.flag`. If present, exit immediately, touch nothing, log it.
3. **Audit Log** — append-only. Every run recorded: timestamp, sources, output, errors.
4. **Approval Boundary** — agent writes to `draft.txt` or stdout only. No send, no post, no API calls.

---

## Hardware

- Standalone PC, NVIDIA GTX 1660 (6GB VRAM)
- Ollama local inference engine
- Models: `llama3.2:3b`, `qwen2.5-coder:1.5b` (fits in <2GB VRAM)
- Total token cost: **$0.00**

---

## Build Milestones

- [x] **Milestone 1** — Core Engine
  - Four Controls: scope file, kill switch, audit log, approval boundary
  - Dual-model routing: Qwen 2.5-Coder (Tier 1 triage) → Llama 3.2 (Tier 2 escalation)
  - Live telemetry pipeline: lock-free byte-offset log tailer, no file-sharing conflicts
  - Host metrics injection: live Windows disk data via `kernel32.GetDiskFreeSpaceExW`
  - Interactive Command Deck: human A/S approval gate on every anomaly
  - 207 audit log entries across 4 build sessions
- [ ] **Milestone 2** — Domain Templates: Active Directory agent, network compliance agent
- [ ] **Milestone 3** — Hardening Layer: Docker isolation, compliance audit exports

---

## Status

Milestone 1 complete as of 2026-07-01.

The Core Engine is running on local hardware. Dual-model routing is verified: nominal
telemetry stays in Tier 1 (Qwen, fast), anomalies escalate to Tier 2 (Llama, narrative).
The live telemetry pipeline tails a watch folder log without file locks. The Command Deck
prompts the operator for approval on every anomaly before anything is dispatched.

**A real incident from the build:**

During Milestone 1 closeout, the kill switch file on disk was named `KILLSWITCH.flag.txt`
while the code checked for `KILLSWITCH.flag`. The kill switch was silently inoperative for
3 build sessions without anyone knowing.

Cost: one rename command. Risk window: 3 sessions.

This is the exact failure mode SwarmOps is designed to prevent — a control that appears
active but isn't. The fix was simple. The detection was manual. Milestone 2 adds automated
controls verification at session startup so this class of failure surfaces immediately
rather than at closeout.

Full build log: [`docs/BUILD_TRANSPARENCY_LOG.md`](docs/BUILD_TRANSPARENCY_LOG.md)

Follow the build on [LinkedIn](https://www.linkedin.com/in/randy-skiles).

---

*AI assists. Humans approve.*
