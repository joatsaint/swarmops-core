# Milestone 3 — Network Compliance Template
**Status:** ✅ COMPLETE — All 5 acceptance criteria verified live 2026-07-05  
**Gate:** Must be complete and live-demo'd before MONTE-1 posts Jul 14, 2026 ← MET  
**Build window:** Jul 7–13 ← completed early (code 2026-07-04, demo 2026-07-05)  
**Spec author:** Claude Code (Session 35, 2026-07-04)

---

## Objective

Build the second reusable domain template: `templates/network_compliance/`. Follows the same pattern as the AD template (Milestone 2) — own SCOPE.md, domain-tuned triage prompt, sample telemetry generator, README.

Target events: firewall rule violations, unusual port activity, geo-anomaly alerts, unauthorized outbound connections.

---

## What Gets Built

```
templates/network_compliance/
  orchestrator_net.py          ← network-tuned Qwen/Llama pipeline
  generate_net_events.py       ← sample telemetry generator
  SCOPE.md                     ← approved capabilities + value hierarchy
  README.md                    ← 4-step setup, tuning guide
  watch_folder/
    telemetry.log              ← tailed by orchestrator_net.py
  dispatched_drafts/           ← approved ticket archive
```

---

## Network Events to Monitor

| Event Type | Severity | Notes |
|-----------|----------|-------|
| Firewall rule violation — known-bad port | HIGH | Ports: 23 (Telnet), 445 (SMB external), 3389 (RDP external) |
| Unusual outbound connection — new destination | MEDIUM | First-seen external IP for this host |
| Geo-anomaly — traffic from unexpected country | HIGH | Flag if country not in baseline allow-list |
| Port scan detected — multiple ports, single source | HIGH | 5+ ports in 60 seconds from one source |
| DNS over non-standard port | MEDIUM | DNS on port != 53 |
| Excessive failed auth on exposed service | HIGH | 10+ failures in 5 min on SSH/RDP/VPN |

---

## Triage Prompt — Qwen Tier 1

The Tier 1 prompt must instruct Qwen to return JSON with these fields (same structure as AD template, network-specific labels):

```json
{
  "anomaly": true,
  "severity": "LOW|MEDIUM|HIGH",
  "confidence": 0-100,
  "event_type": "firewall_violation|port_scan|geo_anomaly|unusual_outbound|dns_anomaly|auth_storm",
  "source_ip": "x.x.x.x or unknown",
  "dest_port": 0,
  "recommended_action": "one-line plain English",
  "scope_check": "analyze_net_logs"
}
```

Confidence threshold: **70** (same as core engine — network events are less structured than AD event IDs, so keep the bar at 70, not lower).

---

## Telemetry Generator — generate_net_events.py

Must support these flags (mirrors generate_ad_events.py pattern):

```powershell
python .\generate_net_events.py                     # one random event
python .\generate_net_events.py --event firewall    # specific type
python .\generate_net_events.py --storm             # port scan storm (5 rapid events)
python .\generate_net_events.py --all               # one of every type
```

Sample log line format (append to `watch_folder\telemetry.log`):
```
2026-07-10 14:23:01 WARN [NET] Outbound connection to 91.108.4.0:443 (Telegram CDN) from 192.168.1.45 — not in baseline
2026-07-10 14:23:08 ALERT [NET] Port scan detected: 192.168.1.200 probed 192.168.1.1 on ports 22,80,443,3389,8080 in 12s
2026-07-10 14:23:15 ALERT [FIREWALL] Blocked outbound 192.168.1.45:52341 -> 203.0.113.0:23 (Telnet) — rule NET-BLOCK-TELNET
```

---

## New Addition: Receipt Vocabulary (wired in from Nate B Jones — Open Engine pattern)

**What it is:** Standardized audit tokens that turn `audit.log` from a narrative log into a parseable, searchable record. Every event gets a machine-readable status receipt as it moves through the pipeline.

**Why it matters:** After 30 days of data, you can `grep audit.log` for `SWARM BLOCKED` to find every out-of-scope event, or `SWARM HUMAN HOLD` to see every time the engine deferred to you. That's a compliance report, not just a log file.

### Receipt tokens — add to `audit.log` at each stage

| Token | When written | Example |
|-------|-------------|---------|
| `SWARM CLAIMED` | Engine starts processing an event | `SWARM CLAIMED evt-00142 2026-07-10T14:23:01` |
| `SWARM DONE` | Analysis complete, packet written to dispatched_drafts/ | `SWARM DONE evt-00142 anomaly=True severity=HIGH confidence=87/100` |
| `SWARM BLOCKED` | Event is out of scope — not in SCOPE.md allow-list | `SWARM BLOCKED evt-00143 reason=out_of_scope action=analyze_host_metrics` |
| `SWARM HUMAN HOLD` | Confidence below threshold — waiting for human decision | `SWARM HUMAN HOLD evt-00144 confidence=52/100 threshold=70` |

### Implementation in orchestrator_net.py

```python
def write_receipt(event_id: str, token: str, detail: str = "") -> None:
    ts = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    line = f"[{ts}] {token} {event_id}"
    if detail:
        line += f" {detail}"
    with open(AUDIT_LOG, "a") as f:
        f.write(line + "\n")
```

Call pattern:
```python
write_receipt(event_id, "SWARM CLAIMED")
# ... run Tier 1 triage ...
if out_of_scope:
    write_receipt(event_id, "SWARM BLOCKED", f"reason=out_of_scope action={action}")
elif confidence < CONFIDENCE_THRESHOLD:
    write_receipt(event_id, "SWARM HUMAN HOLD", f"confidence={confidence}/100 threshold={CONFIDENCE_THRESHOLD}")
else:
    write_receipt(event_id, "SWARM DONE", f"anomaly={anomaly} severity={severity} confidence={confidence}/100")
```

---

## New Addition: Value Hierarchy in SCOPE.md

**What it is:** Every SCOPE.md must answer three questions Nate B Jones identified as the constraint gap in most AI governance specs. Output specs tell the agent where to end up. Constraint specs tell it which paths are off-limits to get there.

**Add this section to `templates/network_compliance/SCOPE.md`:**

```
# SwarmOps — Network Compliance Agent Scope File
# Control 1: This file defines what the agent is authorized to analyze.

analyze_net_logs
read_local_manifest

# --- VALUE HIERARCHY ---
# Q1: What must the agent never do, even to accomplish the goal?
#   - Never execute any command on any system
#   - Never transmit event data outside localhost
#   - Never modify firewall rules, routing tables, or ACLs
#   - Never classify an event as "safe" without a confidence score >= threshold
#
# Q2: When must the agent stop and ask rather than proceed?
#   - Confidence below CONFIDENCE_THRESHOLD (default 70)
#   - Event type not in the monitored list above
#   - Source IP matches internal management subnets (potential lateral movement — escalate, don't auto-ticket)
#   - Any event involving credentials or authentication tokens
#
# Q3: If the goal and a constraint conflict, which wins?
#   CONSTRAINT WINS. Always. The goal is to detect and surface anomalies.
#   The constraint is to never act on them. If the agent cannot surface an
#   anomaly without acting on it, it stops and writes SWARM BLOCKED to audit.log.
```

---

## New Addition: Scope Expansion = Fresh Approval Rule

**Add this to orchestrator_net.py startup output and README:**

> Any addition to SCOPE.md (new action, new event type, new authority) requires a human to edit the file deliberately. The engine does not auto-expand its own scope. A SCOPE.md change is a governance decision — make it consciously, not accidentally.

In `verify_controls()`, add a check that logs the current scope entries at startup:

```python
with open(SCOPE_FILE) as f:
    actions = [line.strip() for line in f if line.strip() and not line.startswith("#")]
print(f"[*] Approved actions: {', '.join(actions)}")
```

This creates an audit record at every startup of exactly what the engine was authorized to do at that moment.

---

## SCOPE.md — Complete File

```
# SwarmOps — Network Compliance Agent Scope File
# Control 1: This file defines what the agent is authorized to analyze.
# The engine will refuse to start if this file is missing or empty.

analyze_net_logs
read_local_manifest

# --- VALUE HIERARCHY ---
# Q1: What must the agent never do, even to accomplish the goal?
#   - Never execute any command on any system
#   - Never transmit event data outside localhost
#   - Never modify firewall rules, routing tables, or ACLs
#   - Never classify an event as "safe" without a confidence score >= threshold
#
# Q2: When must the agent stop and ask rather than proceed?
#   - Confidence below CONFIDENCE_THRESHOLD (default 70)
#   - Event type not in the monitored list above
#   - Source IP matches internal management subnets
#   - Any event involving credentials or authentication tokens
#
# Q3: If the goal and a constraint conflict, which wins?
#   CONSTRAINT WINS. Always.
```

---

## Acceptance Criteria (live demo must pass all 5)

| # | Test | Pass condition |
|---|------|----------------|
| 1 | Startup | `[*] Controls verification passed` + `[*] Approved actions: analyze_net_logs, read_local_manifest` printed |
| 2 | Port scan storm | `python generate_net_events.py --storm` → 5 events processed, SWARM CLAIMED + SWARM DONE tokens in audit.log for each |
| 3 | Out-of-scope event | Inject a non-network event → `SWARM BLOCKED reason=out_of_scope` in audit.log, engine continues |
| 4 | Low confidence | Inject an ambiguous event → `SWARM HUMAN HOLD confidence=XX/100` in audit.log, human gate prompts |
| 5 | Geo-anomaly | HIGH severity geo event → Tier 2 Llama generates Windows-native remediation ticket (netstat/firewall cmdlets only, no Linux tools) |

---

## ChatGPT Build Instructions

Paste the contents of this file + `STATUS.md` to ChatGPT at the start of the session. Tell it:

> "Read both files. Build Milestone 3 exactly as specced. Follow the pattern from `templates/active_directory/orchestrator_ad.py` for the engine structure. Add the receipt vocabulary, value hierarchy, and scope-expansion check as described. Deliver: orchestrator_net.py, generate_net_events.py, SCOPE.md, README.md. After each file, confirm the acceptance criterion it satisfies."

After the build: paste the test results back to Claude Code for the pass/drift check per SwarmOps ChatGPT Protocol.

---

## Build Log

| Date | Step | Result |
|------|------|--------|
| 2026-07-04 | templates/network_compliance/ folder created | ✅ |
| 2026-07-04 | SCOPE.md with value hierarchy written | ✅ — analyze_net_logs + read_local_manifest; 3-question constraint spec |
| 2026-07-04 | orchestrator_net.py with receipt vocabulary | ✅ — SWARM CLAIMED/DONE/BLOCKED/HUMAN HOLD tokens |
| 2026-07-04 | generate_net_events.py working | ✅ — 6 event types; --storm, --all, --event flags |
| 2026-07-04 | README.md written | ✅ — 4-step setup, Option A (generator)/Option B (live), grep queries for each receipt token |
| 2026-07-04 | Tests 1 + 4 verified live | ✅ — startup controls + SWARM HUMAN HOLD on low-confidence unusual_outbound |
| 2026-07-05 | Tests 2, 3, 5 verified live | ✅ — port scan storm; out-of-scope block; geo-anomaly Tier 2 Windows ticket |
| 2026-07-05 | PR opened | ✅ — feat/milestone3-network-compliance |
| 2026-07-05 | STATUS.md + BUILD_TRANSPARENCY_LOG.md updated | ✅ |
