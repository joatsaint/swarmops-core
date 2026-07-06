# SwarmOps — Network Compliance Agent Template

A governance-first AI agent that monitors network security events and escalates anomalies to a human operator for review.

**Setup time:** under 30 minutes if you already have Ollama running.  
**Requires:** Python 3.10+, Ollama with `qwen2.5-coder:1.5b` and `llama3.2:3b` pulled.

---

## What It Does

Watches a log file for network security events. When it sees a firewall violation, port scan, geo-anomaly, or other suspicious pattern, it:

1. Logs `SWARM CLAIMED` to `audit.log` — the event is now being tracked
2. Qwen (Tier 1, 1.5B model) triages the event and returns a type, severity, and confidence score
3. If confidence is below threshold (70) → logs `SWARM HUMAN HOLD` and asks you to decide (E=escalate, S=skip)
4. If confidence is sufficient and anomaly confirmed → Llama (Tier 2, 3B model) generates a 3-point Windows remediation ticket
5. Logs `SWARM DONE` or `SWARM BLOCKED` to `audit.log` — the receipt closes the event record
6. You approve or skip. Approved tickets are archived in `dispatched_drafts/`.

Nothing executes automatically. The agent writes; you decide.

---

## Network Events Monitored

| Event Type | Default Severity | Notes |
|-----------|-----------------|-------|
| `firewall_violation` | HIGH | Outbound on port 23 (Telnet), 445 (SMB external), 3389 (RDP external) |
| `port_scan` | HIGH | 5+ ports probed from single source in < 60 seconds |
| `geo_anomaly` | HIGH | Traffic to/from country not in baseline allow-list |
| `unusual_outbound` | MEDIUM | First-seen external IP for this host |
| `dns_anomaly` | MEDIUM | DNS traffic on port other than 53 — possible tunneling |
| `auth_storm` | HIGH | 10+ failed auth attempts in 5 min on SSH/RDP/VPN |

---

## Receipt Vocabulary — audit.log Tokens

Every event generates a structured receipt in `audit.log`. These are grep-able after 30 days of operation.

| Token | Meaning |
|-------|---------|
| `SWARM CLAIMED evt-YYYYMMDDHHMMSS-NNNN` | Engine started processing this event |
| `SWARM DONE evt-... anomaly=True severity=HIGH confidence=87/100` | Analysis complete, packet written |
| `SWARM BLOCKED evt-... reason=out_of_scope` | Event not authorized in SCOPE.md |
| `SWARM HUMAN HOLD evt-... confidence=52/100 threshold=70` | Agent deferred to human — confidence too low |

**30-day audit queries (PowerShell):**
```powershell
Select-String -Path audit.log -Pattern "SWARM BLOCKED"      # all out-of-scope events
Select-String -Path audit.log -Pattern "SWARM HUMAN HOLD"   # all human-gate events
Select-String -Path audit.log -Pattern "SWARM DONE.*HIGH"   # all HIGH severity completions
```

---

## Setup — 4 Steps

### Step 1 — Copy this folder

Copy the entire `templates/network_compliance/` folder to wherever you want to run it. It is self-contained.

```
my-net-agent/
  orchestrator_net.py
  generate_net_events.py
  SCOPE.md
  README.md
  watch_folder/
  dispatched_drafts/
```

### Step 2 — Review SCOPE.md

Open `SCOPE.md`. It contains the approved actions and the value hierarchy. The defaults are:
```
analyze_net_logs
read_local_manifest
```

The value hierarchy section answers three governance questions — read it before you change anything. Any addition to SCOPE.md is a governance decision, not a config change.

### Step 3 — Point it at your log source

**Option A — Test with the generator (no live firewall needed):**
```powershell
# Window 2: run while orchestrator_net.py is watching
python .\generate_net_events.py                       # one random event
python .\generate_net_events.py --event firewall      # firewall violation
python .\generate_net_events.py --event port_scan     # port scan
python .\generate_net_events.py --event geo           # geo anomaly
python .\generate_net_events.py --storm               # port scan storm (5 rapid)
python .\generate_net_events.py --all                 # one of every type
```

**Option B — Live Windows Firewall / Event Log:**
Export Windows Firewall or IDS events to `watch_folder\telemetry.log`. The agent tails the file byte-by-byte.

PowerShell to export firewall drop events:
```powershell
Get-WinEvent -LogName "Security" -MaxEvents 100 |
  Where-Object { $_.Id -in @(5152, 5157) } |
  ForEach-Object { "$($_.TimeCreated) ALERT [FIREWALL] $($_.Message.Split([Environment]::NewLine)[0])" } |
  Add-Content "watch_folder\telemetry.log"
```

### Step 4 — Run the agent

**Window 1 (the agent):**
```powershell
python .\orchestrator_net.py
```

**Window 2 (inject test events):**
```powershell
python .\generate_net_events.py --storm
```

---

## The Four Controls

| Control | File/Mechanism | What It Does |
|---------|---------------|--------------|
| 1 — Scope | `SCOPE.md` | Allow-list + value hierarchy. Missing = engine stops. |
| 2 — Kill switch | `KILLSWITCH.flag` | Create this file to stop the engine cleanly mid-run. |
| 3 — Audit log | `audit.log` | Append-only. Every event, every receipt token, every operator choice. |
| 4 — Approval boundary | `draft.txt` + `dispatched_drafts/` | Agent output lands here only. Nothing executes without your approval. |

---

## Scope Expansion Rule

Any new capability (new action in SCOPE.md, new event type, new authority) requires you to edit `SCOPE.md` deliberately. The engine does not expand its own scope.

At startup, the agent logs the exact approved actions currently in SCOPE.md:
```
[*] Approved actions at startup: analyze_net_logs, read_local_manifest
```

This creates an audit record of what the engine was authorized to do at every run.

---

## Tuning the Confidence Threshold

Default `CONFIDENCE_THRESHOLD = 70` in `orchestrator_net.py`. Network events are less structured than AD event IDs, so 70 is appropriate — more human gates than the AD template's 65.

- Raise it (e.g. 85) for more human-gate moments
- Lower it (e.g. 55) if you trust the model's network context more

---

## Kill Switch

```powershell
New-Item -ItemType File KILLSWITCH.flag
```

The engine checks every second and exits cleanly when found. Delete it before your next run.

---

## What Gets Archived

Every approved ticket → `dispatched_drafts/draft_YYYYMMDD_HHMMSS.txt`.  
After 30 days: grep `audit.log` for receipt tokens to get a compliance summary of every event the agent processed and every human decision made.

---

*Built on SwarmOps Core — https://github.com/joatsaint/swarmops-core*
