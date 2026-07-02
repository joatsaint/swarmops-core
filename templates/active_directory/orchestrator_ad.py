"""
SwarmOps — Active Directory Agent
Milestone 2 Domain Template

Drop this into any folder with a SCOPE.md and a watch_folder/.
Point your Windows Event Log export at watch_folder\telemetry.log.
Run: python .\\orchestrator_ad.py

AD event IDs monitored:
  4625  Failed logon
  4740  Account lockout
  4728  Member added to global security group
  4732  Member added to local security group
  4756  Member added to universal security group
  4720  User account created
  4726  User account deleted
  4776  NTLM credential validation
  4648  Logon with explicit credentials
  4672  Special privileges assigned (admin logon)
"""
import os
import sys
import time
import json
import logging
import urllib.request
import urllib.error
import ctypes
from datetime import datetime

# ==========================================
# SYSTEM SETUP & DIRECTORIES
# Paths anchored to the script's own location so the agent works
# regardless of which directory PowerShell is sitting in.
# ==========================================
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
WATCH_DIR   = os.path.join(SCRIPT_DIR, "watch_folder")
LOG_FILE    = os.path.join(WATCH_DIR, "telemetry.log")
ARCHIVE_DIR = os.path.join(SCRIPT_DIR, "dispatched_drafts")

# Also change working directory to the script folder so SCOPE.md,
# audit.log, and KILLSWITCH.flag are always found correctly.
os.chdir(SCRIPT_DIR)

for folder in [WATCH_DIR, ARCHIVE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Confidence threshold — AD events are well-structured; 65 is appropriate
# (slightly lower than generic engine because event IDs are unambiguous signals)
CONFIDENCE_THRESHOLD = 65

# AD event severity baseline — Qwen uses this context in its triage prompt
AD_SEVERITY_GUIDE = """
Active Directory Event Severity Reference:
  4625 (Failed logon):            LOW for single event; MEDIUM for 5+ in 10 min; HIGH for 20+ in 10 min
  4740 (Account lockout):         MEDIUM for single; HIGH for 3+ same account in 5 min (lockout storm)
  4728 (Global group membership): HIGH if group is Domain Admins / Enterprise Admins / Schema Admins; MEDIUM otherwise
  4732 (Local group membership):  MEDIUM if group is Administrators; LOW otherwise
  4756 (Universal group change):  HIGH if group is privileged; MEDIUM otherwise
  4720 (Account created):         MEDIUM — requires verification this was authorized
  4726 (Account deleted):         MEDIUM — requires verification this was authorized
  4776 (NTLM validation):         LOW for single; MEDIUM for repeated anonymous attempts
  4648 (Explicit credentials):    MEDIUM — lateral movement indicator if source is unexpected
  4672 (Special privileges):      HIGH if account is not a known admin service account
"""

# ==========================================
# CONTROL 3: Append-Only Audit Logging
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[logging.FileHandler("audit.log", mode="a", encoding="utf-8")]
)

def log_audit(message, level="INFO"):
    if level == "INFO":
        logging.info(message)
        print(f"[*] {message}")
    elif level == "WARNING":
        logging.warning(message)
        print(f"[!] WARNING: {message}")
    elif level == "CRITICAL":
        logging.critical(message)
        print(f"[CRITICAL ERROR] {message}")


# ==========================================
# CONTROLS VERIFICATION
# ==========================================
def verify_controls():
    errors = []

    # Control 1: SCOPE.md
    if not os.path.exists("SCOPE.md"):
        errors.append("SCOPE.md missing — agent has no allow-list. Cannot run.")
    else:
        with open("SCOPE.md", "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        if not lines:
            errors.append("SCOPE.md exists but contains no approved actions.")

    # Control 2: KILLSWITCH.flag (case-sensitive via os.listdir)
    files_in_dir = os.listdir(".")
    if "KILLSWITCH.flag" in files_in_dir:
        errors.append(
            "KILLSWITCH.flag is present — kill switch is ACTIVE. "
            "Delete KILLSWITCH.flag to run in monitoring mode."
        )
    wrong_names = {"KILLSWITCH.flag.txt", "KILLSWITCH.Flag", "killswitch.flag", "KILLSWITCH.FLAG"}
    for actual_file in files_in_dir:
        if actual_file in wrong_names:
            errors.append(
                f"Incorrectly named kill switch found: '{actual_file}' "
                f"— rename to exactly 'KILLSWITCH.flag' to arm it, or delete to run."
            )

    # Control 3: audit.log writable
    try:
        with open("audit.log", "a", encoding="utf-8"):
            pass
    except Exception as e:
        errors.append(f"audit.log not writable: {e}")

    # Control 4: dispatched_drafts/ exists
    if not os.path.exists(ARCHIVE_DIR):
        errors.append(f"'{ARCHIVE_DIR}' directory missing — approval boundary unavailable.")

    if errors:
        print("\n" + "=" * 60)
        print("CONTROLS VERIFICATION FAILED — ENGINE WILL NOT START")
        print("=" * 60)
        for e in errors:
            log_audit(f"CONTROLS VERIFICATION FAILED: {e}", level="CRITICAL")
            print(f"  [X] {e}")
        print("=" * 60)
        sys.exit("Fix the above issues before running SwarmOps AD Agent.")

    log_audit(
        "Controls verification passed: "
        "SCOPE.md ✓ | KILLSWITCH.flag ✓ | audit.log ✓ | dispatched_drafts/ ✓"
    )


# ==========================================
# CONTROL 1: SCOPE.md
# ==========================================
def verify_and_parse_scope(requested_action=None):
    scope_file = "SCOPE.md"
    if not os.path.exists(scope_file):
        log_audit(f"Security Alert: '{scope_file}' missing. Failing closed.", level="CRITICAL")
        sys.exit("CRITICAL ERROR: SCOPE.md missing.")
    try:
        with open(scope_file, "r", encoding="utf-8") as f:
            allowed_actions = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        if not allowed_actions:
            sys.exit("CRITICAL ERROR: SCOPE.md empty.")
        if requested_action and requested_action not in allowed_actions:
            log_audit(f"Security Violation: Action '{requested_action}' not in SCOPE.md!", level="CRITICAL")
            sys.exit(f"CRITICAL ERROR: Action '{requested_action}' unauthorized.")
        return allowed_actions
    except sys.exit:
        raise
    except Exception as e:
        sys.exit(f"CRITICAL ERROR: SCOPE.md failure: {e}")


# ==========================================
# CONTROL 2: KILLSWITCH.flag
# ==========================================
def check_killswitch():
    if "KILLSWITCH.flag" in os.listdir("."):
        log_audit("Killswitch triggered via 'KILLSWITCH.flag'. Stopping cleanly.", level="WARNING")
        sys.exit(0)


# ==========================================
# CONTROL 4: Approval Boundary
# ==========================================
def write_to_approval_boundary(content_summary, full_output):
    draft_file   = "draft.txt"
    timestamp    = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_file = os.path.join(ARCHIVE_DIR, f"draft_{timestamp}.txt")

    boundary_text = (
        "==================================================\n"
        "SWARMOPS AD AGENT — HUMAN REVIEW REQUIRED\n"
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Context: {content_summary}\n"
        "==================================================\n\n"
        f"{full_output}\n\n"
        "==================================================\n"
        "END OF OUTPUT. DO NOT ACT WITHOUT REVIEW.\n"
    )
    try:
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(boundary_text)
        with open(archive_file, "w", encoding="utf-8") as f:
            f.write(boundary_text)
        log_audit(f"Saved to boundary: 'draft.txt' and '{archive_file}'.")
    except Exception as e:
        log_audit(f"Failed writing to boundary: {str(e)}", level="CRITICAL")
        sys.exit("CRITICAL ERROR: Boundary write failure.")


# ==========================================
# LOCAL MODEL HTTP CLIENT
# ==========================================
def query_local_llm(model_name, prompt):
    url     = "http://localhost:11434/api/generate"
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    try:
        data = json.dumps(payload).encode("utf-8")
        req  = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=45) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8")).get("response", "")
            return f"Error: HTTP Status {response.status}"
    except Exception as e:
        log_audit(f"Ollama exception: {str(e)}", level="CRITICAL")
        return f"System Error: {str(e)}"


# ==========================================
# WINDOWS HOST METRICS
# ==========================================
def get_windows_disk_metrics():
    free_bytes  = ctypes.c_ulonglong(0)
    total_bytes = ctypes.c_ulonglong(0)
    total_free  = ctypes.c_ulonglong(0)
    path        = os.path.abspath(".")
    success     = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p(path),
        ctypes.byref(free_bytes),
        ctypes.byref(total_bytes),
        ctypes.byref(total_free)
    )
    if success:
        return (f"Host Storage: {free_bytes.value/(1024**3):.2f} GB free "
                f"of {total_bytes.value/(1024**3):.2f} GB total")
    return "Host Storage: metrics unavailable"


# ==========================================
# ACTIVE DIRECTORY LIVE PIPELINE
# ==========================================
def run_ad_pipeline():
    log_audit("SwarmOps AD Agent: Initializing...")
    verify_controls()
    verify_and_parse_scope()

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO [System] AD telemetry stream initialized.\n")

    print(f"\n--- SwarmOps Active Directory Agent ---")
    print(f"[*] Confidence threshold: {CONFIDENCE_THRESHOLD}/100")
    print(f"[*] Monitoring: {LOG_FILE}")
    print(f"[*] AD event IDs: 4625 4740 4728 4732 4756 4720 4726 4776 4648 4672")
    print(f"[*] Awaiting AD events...\n")

    last_position = os.path.getsize(LOG_FILE)

    try:
        while True:
            check_killswitch()

            if os.path.exists(LOG_FILE):
                current_size = os.path.getsize(LOG_FILE)
                if current_size > last_position:
                    with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
                        f.seek(last_position)
                        lines = f.readlines()
                        last_position = f.tell()

                    for line in lines:
                        raw_event = line.strip()
                        if not raw_event:
                            continue

                        log_audit(f"AD event received: '{raw_event}'")
                        verify_and_parse_scope(requested_action="analyze_ad_logs")

                        host_metrics = get_windows_disk_metrics()

                        # --------------------------------------------------
                        # TIER 1: Qwen AD Triage
                        # --------------------------------------------------
                        triage_prompt = (
                            f"You are an Active Directory security triage agent.\n"
                            f"Analyze this Windows Security Event Log line:\n\n"
                            f"Event: '{raw_event}'\n\n"
                            f"{AD_SEVERITY_GUIDE}\n"
                            f"Return JSON ONLY. No explanation. No markdown.\n"
                            f'Template: {{"anomaly": true/false, "severity": "LOW"/"MEDIUM"/"HIGH", '
                            f'"reason": "string", "confidence": 0-100}}\n\n'
                            f"confidence: your certainty in this assessment (0=no idea, 100=certain).\n"
                            f"anomaly=true means this event requires human review."
                        )
                        triage_raw = query_local_llm("qwen2.5-coder:1.5b", triage_prompt)

                        try:
                            clean_json  = triage_raw.strip().replace("```json", "").replace("```", "").strip()
                            triage_data = json.loads(clean_json)
                            is_anomaly  = triage_data.get("anomaly", False)
                            severity    = triage_data.get("severity", "LOW")
                            reason      = triage_data.get("reason", "No reason provided.")
                            confidence  = int(triage_data.get("confidence", 100))
                        except Exception:
                            log_audit("JSON parse failed. Failing closed.", level="WARNING")
                            is_anomaly, severity, reason, confidence = True, "HIGH", "Parsing failure.", 0

                        log_audit(
                            f"Tier 1 AD Triage -> "
                            f"Anomaly: {is_anomaly} | Severity: {severity} | Confidence: {confidence}/100"
                        )

                        # --------------------------------------------------
                        # CONFIDENCE GATE
                        # --------------------------------------------------
                        if confidence < CONFIDENCE_THRESHOLD:
                            log_audit(
                                f"LOW CONFIDENCE: {confidence}/100 (threshold={CONFIDENCE_THRESHOLD}). "
                                f"Human review required.", level="WARNING"
                            )
                            write_to_approval_boundary(
                                f"LOW CONFIDENCE AD EVENT — confidence={confidence}/100",
                                (f"LOW CONFIDENCE — HUMAN REVIEW REQUIRED\n\n"
                                 f"Event:      {raw_event}\n"
                                 f"Verdict:    {severity} | anomaly={is_anomaly}\n"
                                 f"Reason:     {reason}\n"
                                 f"Confidence: {confidence}/100 (threshold: {CONFIDENCE_THRESHOLD}/100)")
                            )
                            print("\n" + "~" * 60)
                            print("~~~ LOW CONFIDENCE AD ALERT ~~~")
                            print("~" * 60)
                            print(f"[~] EVENT      : {raw_event}")
                            print(f"[~] VERDICT    : {severity} | anomaly={is_anomaly}")
                            print(f"[~] REASON     : {reason}")
                            print(f"[~] CONFIDENCE : {confidence}/100 (threshold: {CONFIDENCE_THRESHOLD}/100)")
                            print(f"[~] HOST       : {host_metrics}")
                            print("-" * 60)

                            low_conf_choice = ""
                            while low_conf_choice not in ["e", "s"]:
                                check_killswitch()
                                print("[ACTION REQUIRED] Agent is uncertain:")
                                print("  [E] Escalate to Tier 2 (you override)")
                                print("  [S] Skip — log and continue")
                                low_conf_choice = input(">> Enter option (E/S): ").strip().lower()

                            if low_conf_choice == "s":
                                log_audit(f"Operator: LOW CONFIDENCE SKIPPED (confidence={confidence}).", level="WARNING")
                                print("[-] Low-confidence event skipped by operator.\n")
                                print("[*] Resuming AD monitoring...\n")
                                continue

                            log_audit(f"Operator: MANUAL ESCALATION (confidence={confidence}/100). Proceeding to Tier 2.")

                        # --------------------------------------------------
                        # TIER 2: Llama AD Remediation
                        # --------------------------------------------------
                        if is_anomaly:
                            log_audit("Escalating to Tier 2 AD Executive...")

                            if sys.platform == "win32":
                                ctypes.windll.user32.MessageBeep(0)

                            executive_prompt = (
                                f"You are an Active Directory incident response specialist.\n"
                                f"An AD security event requires a remediation ticket.\n\n"
                                f"Event:      {raw_event}\n"
                                f"Assessment: {reason} (Severity: {severity})\n"
                                f"Confidence: {confidence}/100\n"
                                f"Host:       {host_metrics}\n\n"
                                f"RULES:\n"
                                f"1. Windows environment only. Use PowerShell AD cmdlets: "
                                f"Get-ADUser, Search-ADAccount, Get-ADGroupMember, Get-ADGroup, "
                                f"Unlock-ADAccount, Disable-ADAccount, Get-EventLog.\n"
                                f"2. Do NOT use Linux tools (grep, tail, awk, net user without /domain).\n"
                                f"3. Write a precise 3-point remediation ticket. "
                                f"Include the specific PowerShell command for each step.\n"
                                f"4. Reference the specific AD event ID in your ticket."
                            )

                            final_report = query_local_llm("llama3.2:3b", executive_prompt)
                            write_to_approval_boundary(
                                f"AD ALERT: {severity} (confidence={confidence}/100)",
                                final_report
                            )

                            print("\n" + "!" * 60)
                            print("!!! AD SECURITY ALERT — HUMAN REVIEW REQUIRED !!!")
                            print("!" * 60)
                            print(f"[!] EVENT      : {raw_event}")
                            print(f"[!] REASON     : {reason}")
                            print(f"[!] CONFIDENCE : {confidence}/100")
                            print(f"[!] HOST       : {host_metrics}")
                            print("-" * 60)
                            print(f"Proposed Remediation (Llama-3B):\n")
                            print(final_report)
                            print("-" * 60)

                            user_choice = ""
                            while user_choice not in ["a", "s"]:
                                check_killswitch()
                                print("[ACTION REQUIRED]:")
                                print("  [A] Approve & archive ticket")
                                print("  [S] Skip / ignore")
                                user_choice = input(">> Enter option (A/S): ").strip().lower()

                            if user_choice == "a":
                                log_audit("Operator: APPROVED. Ticket archived.")
                                print("[+] Ticket approved and archived.\n")
                            else:
                                log_audit("Operator: SKIPPED.", level="WARNING")
                                print("[-] Alert skipped by operator.\n")
                        else:
                            write_to_approval_boundary(
                                f"AD Nominal (confidence={confidence}/100)",
                                f"Event assessed nominal:\n{raw_event}\n{host_metrics}"
                            )

                        print("[*] Resuming AD monitoring...\n")

                elif current_size < last_position:
                    log_audit("Log truncation detected. Resetting offset.", level="WARNING")
                    last_position = 0

            time.sleep(1.0)

    except KeyboardInterrupt:
        log_audit("AD Agent stopped by operator.", level="WARNING")
        print("\n[-] AD Agent deactivated cleanly.")


if __name__ == "__main__":
    run_ad_pipeline()
