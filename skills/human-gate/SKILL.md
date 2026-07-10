# Skill: human-gate

**Job:** Enforce the review-and-submit boundary in SwarmOps event workflows. The agent organizes, analyzes, drafts, validates, and exports. A human reviews, decides, signs, and executes. This line is written into the workflow — not assumed.

---

## What the agent MAY do

- Ingest and parse Windows Event Log entries, syslog, and structured log files
- Analyze events against the SCOPE.md allow-list
- Score confidence against the CONFIDENCE_THRESHOLD
- Generate a human-readable ticket draft (summary, recommended action, PowerShell command)
- Validate the draft against the scope allow-list (Citation Guard equivalent)
- Write the ticket draft to disk as a Markdown or JSON artifact
- Export a run output packet: ticket draft + confidence score + source event IDs + scope citations
- Flag low-confidence or out-of-scope events for review
- Record verdicts in the audit log

## What the agent MUST NOT do

- Execute any PowerShell command — including commands it wrote in a ticket draft
- Send email, trigger alerts, or push notifications
- Modify Active Directory — unlock accounts, reset passwords, change group membership
- Write to production systems, registry, or file system outside the designated work folder
- Submit or file tickets to ServiceNow, JIRA, or any ITSM without a separate human-initiated workflow
- Authorize, approve, or sign off on access requests
- Transmit event data, log files, or ticket contents outside the local machine
- Take any irreversible action on any system

---

## Review checklist (included in every run output packet)

Before executing any recommended action, the reviewer must confirm:

- [ ] Event source and timestamp reviewed — does this match a real event I recognize?
- [ ] Confidence score is above threshold (default 65) — if below, is the low confidence explained?
- [ ] Recommended PowerShell command reviewed line by line — no unexpected flags or targets
- [ ] Scope check passed — action is within SCOPE.md allow-list for this template
- [ ] Out-of-scope or needs_review flags understood before proceeding
- [ ] Packet exported to work folder — original event log untouched
- [ ] You are the authorized person to take this action on this system

**Reviewer signs off by executing the command manually, not by instructing the agent.**

---

## Workflow stop point

The agent's last step is writing the run output packet to disk:

```
run_outputs/
  YYYY-MM-DD_HHMMSS_<event-id>/
    ticket_draft.md        ← recommended action + cited evidence
    confidence_report.json ← score, threshold, verdict
    source_events.json     ← raw event IDs and fields used
    scope_citations.json   ← SCOPE.md entries that authorized this analysis
    REVIEW_CHECKLIST.md    ← the checklist above, pre-populated for this event
```

The workflow stops here. No downstream step runs automatically. The human opens `ticket_draft.md`, reviews the checklist, and executes the recommended command themselves.

---

## Domain disclaimer

SwarmOps analyzes Windows security and operations events and produces recommended responses. It does not replace a qualified system administrator's judgment. Events involving account lockouts, privilege escalation, or lateral movement may be part of a larger incident — review in context before acting on any single ticket. When in doubt, escalate to your security team before executing.

**Next step after reviewing this packet:** open `ticket_draft.md`, complete the checklist, and run the recommended command in an elevated PowerShell session on the target machine.

---

## Verification

To confirm this gate is enforced: run SwarmOps against a test event batch. Verify that:
1. `run_outputs/` folder contains a packet for each processed event
2. No commands were executed — only written to `ticket_draft.md`
3. `REVIEW_CHECKLIST.md` is present and pre-populated in every packet folder
4. The audit log records each event with confidence score but no execution record

A gate that allows the agent to execute commands, even once, is a failed gate.
