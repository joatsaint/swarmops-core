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

- [ ] **Milestone 1** — Core Engine: command whitelist, self-correction loop, audit ledger
- [ ] **Milestone 2** — Domain Templates: Active Directory agent, network compliance agent
- [ ] **Milestone 3** — Hardening Layer: Docker isolation, compliance audit exports

---

## Status

Early build. Core controls not yet implemented. Follow progress on [LinkedIn](https://www.linkedin.com/in/randyskiles/).

---

*AI assists. Humans approve.*
