# SwarmOps — Active Directory Agent Template

A governance-first AI agent that monitors Active Directory event logs and escalates anomalies to a human operator for review.

**Setup time:** under 30 minutes if you already have Ollama running.
**Requires:** Python 3.10+, Ollama with `qwen2.5-coder:1.5b` and `llama3.2:3b` pulled.

---

## What It Does

Watches a log file for Windows Security Event Log entries. When it sees an AD event (lockout storm, unauthorized group membership change, admin privilege assignment), it:

1. Qwen (Tier 1, 1.5B model) triages the event and returns a severity + confidence score
2. If confidence is below threshold → pauses and asks you to decide (E=escalate, S=skip)
3. If confidence is sufficient and anomaly is confirmed → Llama (Tier 2, 3B model) generates a 3-point PowerShell remediation ticket
4. You approve or skip. Approved tickets are archived in `dispatched_drafts/`.

Nothing executes automatically. The agent writes; you decide.

---

## AD Events Monitored

| Event ID | What It Means | Default Severity |
|----------|--------------|-----------------|
| 4625 | Failed logon | LOW (single) / HIGH (storm) |
| 4740 | Account locked out | MEDIUM (single) / HIGH (storm) |
| 4728 | Added to global security group | HIGH if privileged group |
| 4732 | Added to local security group | MEDIUM if Administrators |
| 4756 | Added to universal security group | HIGH if privileged |
| 4720 | User account created | MEDIUM |
| 4726 | User account deleted | MEDIUM |
| 4776 | NTLM credential validation | LOW (single) |
| 4648 | Logon with explicit credentials | MEDIUM |
| 4672 | Special privileges assigned | HIGH |

---

## Setup — 4 Steps

### Step 1 — Copy this folder

Copy the entire `templates/active_directory/` folder to wherever you want to run it. It is self-contained.

```
my-ad-agent/
  orchestrator_ad.py
  generate_ad_events.py
  SCOPE.md
  README.md
```

### Step 2 — Review SCOPE.md

Open `SCOPE.md`. It contains the approved actions for this agent. The defaults are:
```
analyze_ad_logs
read_local_manifest
```

Add or remove lines to match your environment's policy. The engine will not start if this file is missing or empty.

### Step 3 — Point it at your log source

**Option A — Test with the generator (no live DC needed):**
```powershell
# Window 2: run while orchestrator_ad.py is watching
python .\generate_ad_events.py                  # one random event
python .\generate_ad_events.py --event 4740     # specific event
python .\generate_ad_events.py --storm          # lockout storm (5 rapid lockouts)
python .\generate_ad_events.py --all            # one of every type
```

**Option B — Live Windows Event Log:**
Export your Windows Security log in text format and direct it to `watch_folder\telemetry.log`. The agent tails the file byte-by-byte — new lines appear as they are written.

PowerShell to export AD events to the watch folder:
```powershell
Get-WinEvent -LogName Security -MaxEvents 100 |
  Where-Object { $_.Id -in @(4625,4740,4728,4732,4756,4720,4726,4776,4648,4672) } |
  ForEach-Object { "$($_.TimeCreated) $($_.Id) $($_.Message)" } |
  Add-Content "watch_folder\telemetry.log"
```

### Step 4 — Run the agent

**Window 1 (the agent):**
```powershell
python .\orchestrator_ad.py
```

**Window 2 (inject test events or export real logs):**
```powershell
python .\generate_ad_events.py --storm
```

---

## The Four Controls

Every SwarmOps template includes the same governance layer:

| Control | File/Mechanism | What It Does |
|---------|---------------|--------------|
| 1 — Scope | `SCOPE.md` | Allow-list of what the agent can analyze. Missing = engine stops. |
| 2 — Kill switch | `KILLSWITCH.flag` | Create this file to stop the engine cleanly mid-run. Delete it to restart. |
| 3 — Audit log | `audit.log` | Append-only. Every event, every triage decision, every operator choice. |
| 4 — Approval boundary | `draft.txt` + `dispatched_drafts/` | Agent output lands here only. Nothing executes without your approval. |

---

## Tuning the Confidence Threshold

The default `CONFIDENCE_THRESHOLD = 65` in `orchestrator_ad.py`. AD event IDs are structured and unambiguous, so 65 is appropriate (slightly lower than the generic engine's 70).

- Raise it (e.g. 80) if you want more human-gate moments on borderline events
- Lower it (e.g. 50) if you trust the model's AD context more and want fewer interruptions

Change the constant at the top of `orchestrator_ad.py`.

---

## Kill Switch

To stop the agent mid-run without Ctrl+C:
```powershell
New-Item -ItemType File KILLSWITCH.flag
```

The engine checks for this file every second and exits cleanly when found. Delete it before your next run.

---

## What Gets Archived

Every approved ticket is saved to `dispatched_drafts/draft_YYYYMMDD_HHMMSS.txt`. After 30 days of data, you have a record of every AD anomaly the agent flagged, what the model recommended, and what you approved. That's your override tracking baseline — the data that tells you which events are worth building a policy for.

---

*Built on SwarmOps Core — https://github.com/joatsaint/swarmops-core*
