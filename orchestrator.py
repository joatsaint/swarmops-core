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
# ==========================================
WATCH_DIR = "watch_folder"
LOG_FILE = os.path.join(WATCH_DIR, "telemetry.log")
ARCHIVE_DIR = "dispatched_drafts"

for folder in [WATCH_DIR, ARCHIVE_DIR]:
    if not os.path.exists(folder):
        os.makedirs(folder)

# ==========================================
# PROJECT 2: CONFIDENCE CALIBRATION
# Agent must declare certainty before escalating.
# Below this threshold → human decides, not the model.
# ==========================================
CONFIDENCE_THRESHOLD = 70

# ==========================================
# CONTROL 3: Append-Only Audit Logging
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("audit.log", mode="a", encoding="utf-8")
    ]
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
# PROJECT 2: CONTROLS VERIFICATION
# Runs at startup. Catches the class of silent failure where
# a control appears active but isn't (e.g., KILLSWITCH.flag.txt
# was silently inoperative for 3 sessions in Milestone 1).
# ==========================================
def verify_controls():
    """Verify all four controls are present and correctly configured before any run."""
    errors = []

    # Control 1: SCOPE.md must exist and be non-empty
    if not os.path.exists("SCOPE.md"):
        errors.append("SCOPE.md missing — agent has no allow-list. Cannot run.")
    else:
        with open("SCOPE.md", "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]
        if not lines:
            errors.append("SCOPE.md exists but contains no approved actions.")

    # Control 2: Kill switch mechanism verification.
    # The kill switch is TRIGGERED by creating KILLSWITCH.flag — not by it being absent.
    # Normal engine operation: file is NOT present. Emergency stop: create the file.
    # What we verify here: no wrong-named variants exist that would silently disable the mechanism.
    # Use os.listdir() for case-sensitive filename check (os.path.exists is case-insensitive on Windows)
    files_in_dir = os.listdir(".")
    if "KILLSWITCH.flag" in files_in_dir:
        errors.append(
            "KILLSWITCH.flag is present — kill switch is ACTIVE. "
            "Engine will not start. Delete KILLSWITCH.flag to run in monitoring mode."
        )
    wrong_names = {"KILLSWITCH.flag.txt", "KILLSWITCH.Flag", "killswitch.flag", "KILLSWITCH.FLAG"}
    for actual_file in files_in_dir:
        if actual_file in wrong_names:
            errors.append(
                f"Incorrectly named kill switch found: '{actual_file}' "
                f"— rename to exactly 'KILLSWITCH.flag' to arm the kill switch, "
                f"or delete it to run in monitoring mode."
            )

    # Control 3: audit.log must be writable
    try:
        with open("audit.log", "a", encoding="utf-8"):
            pass
    except Exception as e:
        errors.append(f"audit.log not writable: {e}")

    # Control 4: dispatched_drafts/ must exist
    if not os.path.exists(ARCHIVE_DIR):
        errors.append(f"'{ARCHIVE_DIR}' directory missing — approval boundary archive unavailable.")

    if errors:
        print("\n" + "=" * 60)
        print("CONTROLS VERIFICATION FAILED — ENGINE WILL NOT START")
        print("=" * 60)
        for e in errors:
            log_audit(f"CONTROLS VERIFICATION FAILED: {e}", level="CRITICAL")
            print(f"  [X] {e}")
        print("=" * 60)
        sys.exit("Fix the above issues before running SwarmOps.")

    log_audit(
        "Controls verification passed: "
        "SCOPE.md ✓ | KILLSWITCH.flag ✓ | audit.log ✓ | dispatched_drafts/ ✓"
    )

# ==========================================
# CONTROL 1: SCOPE.md (Agent Allow-List)
# ==========================================
def verify_and_parse_scope(requested_action=None):
    scope_file = "SCOPE.md"
    if not os.path.exists(scope_file):
        log_audit(f"Security Alert: '{scope_file}' missing. System failing closed.", level="CRITICAL")
        sys.exit("CRITICAL ERROR: SCOPE.md missing.")

    try:
        with open(scope_file, "r", encoding="utf-8") as f:
            allowed_actions = [line.strip() for line in f if line.strip() and not line.startswith("#")]

        if not allowed_actions:
            log_audit(f"Security Alert: '{scope_file}' is empty. System failing closed.", level="CRITICAL")
            sys.exit("CRITICAL ERROR: SCOPE.md empty.")

        if requested_action:
            if requested_action in allowed_actions:
                return True
            else:
                log_audit(f"Security Violation: Action '{requested_action}' not in SCOPE.md! Failing closed.", level="CRITICAL")
                sys.exit(f"CRITICAL ERROR: Action '{requested_action}' unauthorized.")
        return allowed_actions
    except sys.exit:
        raise
    except Exception as e:
        log_audit(f"Security Alert: SCOPE.md parsing error ({str(e)}). Failing closed.", level="CRITICAL")
        sys.exit(f"CRITICAL ERROR: SCOPE.md failure.")

# ==========================================
# CONTROL 2: KILLSWITCH.flag
# ==========================================
def check_killswitch():
    # Use os.listdir() for case-sensitive check on Windows (os.path.exists is case-insensitive)
    if "KILLSWITCH.flag" in os.listdir("."):
        log_audit("Killswitch triggered via 'KILLSWITCH.flag'. Stopping cleanly.", level="WARNING")
        sys.exit(0)

# ==========================================
# CONTROL 4: Approval Boundary & Rotation
# ==========================================
def write_to_approval_boundary(content_summary, full_output):
    """Writes to draft.txt and archives a timestamped copy in dispatched_drafts."""
    draft_file = "draft.txt"
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_file = os.path.join(ARCHIVE_DIR, f"draft_{timestamp}.txt")

    boundary_text = (
        "==================================================\n"
        "SWARMOPS CORE LIVE DRAFT - HUMAN REVIEW REQUIRED\n"
        f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Context/Summary: {content_summary}\n"
        "==================================================\n\n"
        f"{full_output}\n\n"
        "==================================================\n"
        "END OF ENCLAVE OUTPUT. DO NOT COMMIT TO LIVE STACK.\n"
    )

    try:
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(boundary_text)
        with open(archive_file, "w", encoding="utf-8") as f:
            f.write(boundary_text)
        log_audit(f"Data saved to boundary sandboxes: 'draft.txt' and '{archive_file}'.")
    except Exception as e:
        log_audit(f"Failed writing to safety boundary file: {str(e)}", level="CRITICAL")
        sys.exit("CRITICAL ERROR: Boundary breach prevention failure.")

# ==========================================
# LOCAL MODEL HTTP CLIENT
# ==========================================
def query_local_llm(model_name, prompt):
    url = "http://localhost:11434/api/generate"
    payload = {"model": model_name, "prompt": prompt, "stream": False}
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=45) as response:
            if response.status == 200:
                return json.loads(response.read().decode("utf-8")).get("response", "")
            return f"Error: HTTP Status {response.status}"
    except Exception as e:
        log_audit(f"Ollama integration exception: {str(e)}", level="CRITICAL")
        return f"System Error: {str(e)}"

# ==========================================
# HARDWARE METRIC INJECTION (Windows Native)
# ==========================================
def get_windows_disk_metrics():
    """Retrieves free storage metrics for the local runtime environment context."""
    free_bytes = ctypes.c_ulonglong(0)
    total_bytes = ctypes.c_ulonglong(0)
    total_free_bytes = ctypes.c_ulonglong(0)

    path = os.path.abspath(".")

    success = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p(path) if sys.version_info.major == 3 and sys.version_info.minor >= 12 else path,
        ctypes.byref(free_bytes),
        ctypes.byref(total_bytes),
        ctypes.byref(total_free_bytes)
    )

    if success:
        gb_free = free_bytes.value / (1024**3)
        gb_total = total_bytes.value / (1024**3)
        return f"Host Storage Status: {gb_free:.2f} GB Free out of {gb_total:.2f} GB Total."
    return "Host Storage Status: Telemetry metrics unavailable."

# ==========================================
# LIVE INGESTION RUNTIME ENGINE (Lock-Free)
# ==========================================
def run_live_pipeline():
    log_audit("SwarmOps Core Engine: Initializing...")

    # PROJECT 2: Verify all controls before touching any telemetry
    verify_controls()

    verify_and_parse_scope()

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"2026-06-30 {datetime.now().strftime('%H:%M:%S')} INFO [System] Telemetry stream channel initialized.\n")

    print(f"\n--- SwarmOps Active Log Pipeline Open ---")
    print(f"[*] Confidence threshold: {CONFIDENCE_THRESHOLD}/100 (below this = human decides)")
    print(f"[*] Tailing file: {LOG_FILE}")
    print(f"[*] Awaiting incoming updates...\n")
    active_operation = "analyze_logs"

    last_position = os.path.getsize(LOG_FILE)

    try:
        while True:
            check_killswitch()

            if os.path.exists(LOG_FILE):
                current_size = os.path.getsize(LOG_FILE)
                if current_size > last_position:
                    with open(LOG_FILE, "r", encoding="utf-8") as log_stream:
                        log_stream.seek(last_position)
                        lines = log_stream.readlines()
                        last_position = log_stream.tell()

                    for line in lines:
                        raw_telemetry = line.strip()
                        if not raw_telemetry:
                            continue

                        log_audit(f"Disk read intercept: '{raw_telemetry}'")
                        verify_and_parse_scope(requested_action=active_operation)

                        host_metrics = get_windows_disk_metrics()

                        # --------------------------------------------------
                        # TIER 1: Qwen Triage (now includes confidence score)
                        # --------------------------------------------------
                        triage_prompt = (
                            f"Analyze this telemetry string for any critical infrastructure exceptions.\n"
                            f"Telemetry: '{raw_telemetry}'\n\n"
                            f"Constraint: Return JSON formatting ONLY. No explanation. No markdown.\n"
                            f"JSON Template: "
                            f'{{\"anomaly\": true/false, \"severity\": \"LOW\"/\"MEDIUM\"/\"HIGH\", '
                            f'\"reason\": \"string\", \"confidence\": 0-100}}\n\n'
                            f"confidence is your certainty in this assessment from 0 (no idea) to 100 (certain)."
                        )
                        triage_raw = query_local_llm(model_name="qwen2.5-coder:1.5b", prompt=triage_prompt)

                        try:
                            clean_json = triage_raw.strip().replace("```json", "").replace("```", "").strip()
                            triage_data = json.loads(clean_json)
                            is_anomaly = triage_data.get("anomaly", False)
                            severity = triage_data.get("severity", "LOW")
                            reason = triage_data.get("reason", "No reason provided.")
                            # PROJECT 2: Extract confidence; default 100 preserves existing behavior
                            # if model does not return the field (backward compatible)
                            confidence = int(triage_data.get("confidence", 100))
                        except Exception:
                            log_audit("JSON parsing boundary failed. Escalating safely.", level="WARNING")
                            # Fail-closed: treat parse failure as anomaly but flag zero confidence
                            is_anomaly, severity, reason, confidence = True, "HIGH", "Parsing failure on raw response string.", 0

                        log_audit(
                            f"Tier 1 Triage complete -> "
                            f"Anomaly: {is_anomaly} | Severity: {severity} | Confidence: {confidence}/100"
                        )

                        # --------------------------------------------------
                        # PROJECT 2: CONFIDENCE GATE
                        # If model isn't confident enough, surface to human
                        # before any escalation decision is made.
                        # --------------------------------------------------
                        if confidence < CONFIDENCE_THRESHOLD:
                            log_audit(
                                f"LOW CONFIDENCE ALERT: Model certainty={confidence}/100 "
                                f"(threshold={CONFIDENCE_THRESHOLD}). Human review required.",
                                level="WARNING"
                            )

                            write_to_approval_boundary(
                                f"LOW CONFIDENCE FLAG — confidence={confidence}/100",
                                (
                                    f"LOW CONFIDENCE — HUMAN REVIEW REQUIRED\n\n"
                                    f"Telemetry:  {raw_telemetry}\n"
                                    f"AI Verdict: {severity} anomaly={is_anomaly}\n"
                                    f"AI Reason:  {reason}\n"
                                    f"Confidence: {confidence}/100 (threshold: {CONFIDENCE_THRESHOLD}/100)\n\n"
                                    f"The agent is not confident enough in this assessment to auto-escalate.\n"
                                    f"A human operator must decide whether to escalate to Tier 2."
                                )
                            )

                            print("\n" + "~" * 60)
                            print(f"~~~ LOW CONFIDENCE FLAG ~~~")
                            print("~" * 60)
                            print(f"[~] TELEMETRY    : {raw_telemetry}")
                            print(f"[~] AI VERDICT   : {severity} | anomaly={is_anomaly}")
                            print(f"[~] AI REASON    : {reason}")
                            print(f"[~] CONFIDENCE   : {confidence}/100 (threshold: {CONFIDENCE_THRESHOLD}/100)")
                            print(f"[~] STATUS       : {host_metrics}")
                            print("-" * 60)

                            low_conf_choice = ""
                            while low_conf_choice not in ["e", "s"]:
                                check_killswitch()
                                print("[ACTION REQUIRED] Model is uncertain. You decide:")
                                print("  [E] Escalate to Tier 2 anyway (you override the model)")
                                print("  [S] Skip — log as low-confidence and continue")
                                low_conf_choice = input(">> Enter option (E/S): ").strip().lower()

                            if low_conf_choice == "s":
                                log_audit(
                                    f"Operator Decision: LOW CONFIDENCE SKIPPED. "
                                    f"No escalation (confidence={confidence}).",
                                    level="WARNING"
                                )
                                print("[-] Low-confidence alert skipped by operator.\n")
                                print("[*] Event cycle complete. Re-tailing log path...\n")
                                continue  # skip to next telemetry line

                            # If [E]: fall through to standard Tier 2 escalation below
                            log_audit(
                                f"Operator Decision: MANUAL ESCALATION. "
                                f"Overriding low confidence ({confidence}/100). Proceeding to Tier 2."
                            )

                        # --------------------------------------------------
                        # TIER 2: Llama Executive Escalation & Command Deck
                        # --------------------------------------------------
                        if is_anomaly:
                            log_audit("Escalation sequence triggered. Engaging Tier 2 Executive...")

                            if sys.platform == "win32":
                                ctypes.windll.user32.MessageBeep(0)

                            executive_prompt = (
                                f"Context: An infrastructure exception was identified by Tier 1 processing gates.\n"
                                f"Raw Incident Line: '{raw_telemetry}'\n"
                                f"Triage Assessment: {reason} (Severity Level: {severity})\n"
                                f"Triage Confidence: {confidence}/100\n"
                                f"Host Environment Specs: {host_metrics}\n"
                                f"TARGET OPERATING SYSTEM: Windows Native Environment (CMD/PowerShell execution context).\n\n"
                                f"Task: Generate a precise 3-point IT Admin remediation ticket draft matching this environment context.\n\n"
                                f"CRITICAL SYSTEM RULES (YOU MUST FOLLOW THESE SEVERELY):\n"
                                f"1. ENVIRONMENT CONFORMANCE: The host system is Windows. DO NOT suggest Linux utilities (such as 'df', 'smartctl', 'grep', 'top', or '/dev/sda'). Only recommend Windows-native solutions, commands (e.g., Get-Volume, Get-Process, Get-Service, tasklist), or database configuration adjustments.\n"
                                f"2. DATA ACCURACY: Review free storage vs total storage carefully. Do not invert calculations or misuse percentages (e.g., if ~1800 GB is free out of ~2000 GB, the system has ~12% usage and is mostly empty, NOT 88% usage).\n"
                                f"3. APPLICATION FOCUS: Address the exception's actual root cause. If physical memory metrics on the host are healthy but the database reports an Out Of Memory (OOM) error, acknowledge that this points towards internal process-specific heap/virtual memory allocation caps, not physical disk or physical RAM starvation. Do NOT tell the administrator to check, expand, or adjust storage drives."
                            )

                            final_report = query_local_llm(model_name="llama3.2:3b", prompt=executive_prompt)
                            write_to_approval_boundary(
                                f"ALERT: System Incident Report - {severity} (confidence={confidence}/100)",
                                final_report
                            )

                            print("\n" + "!" * 60)
                            print(f"!!! SWARM ALERT: CRITICAL INFRASTRUCTURE ANOMALY DETECTED !!!")
                            print("!" * 60)
                            print(f"[!] TELEMETRY METRIC : {raw_telemetry}")
                            print(f"[!] TRIAGE REASON    : {reason}")
                            print(f"[!] CONFIDENCE       : {confidence}/100")
                            print(f"[!] LOCAL STATUS     : {host_metrics}")
                            print("-" * 60)
                            print(f"Proposed Remediation Draft Generated by Llama-3B:\n")
                            print(final_report)
                            print("-" * 60)

                            user_choice = ""
                            while user_choice not in ["a", "s"]:
                                check_killswitch()
                                print("[ACTION REQUIRED] Choose an operational option:")
                                print("  [A] Approve & Log Remediation Ticket")
                                print("  [S] Skip / Ignore Alert")
                                user_choice = input(">> Enter option (A/S): ").strip().lower()

                            if user_choice == "a":
                                log_audit("Operator Decision: APPROVED. Remediation ticket committed to dispatch archive.")
                                print("[+] Action authorized! Moving to next telemetry stream frame.\n")
                            else:
                                log_audit("Operator Decision: SKIPPED. Alert bypassed manually.", level="WARNING")
                                print("[-] Action bypassed by operator command.\n")

                        else:
                            write_to_approval_boundary(
                                f"Telemetry Nominal (confidence={confidence}/100)",
                                f"System state checked clean. Log processed:\n{raw_telemetry}\n{host_metrics}"
                            )

                        print("[*] Event cycle complete. Re-tailing log path...\n")

                elif current_size < last_position:
                    log_audit("Telemetry log truncation detected. Resetting byte offset pointer.", level="WARNING")
                    last_position = 0

            time.sleep(1.0)

    except KeyboardInterrupt:
        log_audit("Engine loop interrupted via hardware terminal sign-off.", level="WARNING")
        print("\n[-] Core pipeline deactivated safely.")

if __name__ == "__main__":
    run_live_pipeline()
