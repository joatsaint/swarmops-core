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
    if os.path.exists("KILLSWITCH.flag"):
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
        # Update current review file
        with open(draft_file, "w", encoding="utf-8") as f:
            f.write(boundary_text)
            
        # Write to persistent historical archive
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
    
    # Target current operational partition path
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
# LIVE INGESTION RUNTIME ENGINE (Lock-Free Version)
# ==========================================
def run_live_pipeline():
    log_audit("SwarmOps Core Engine: Initializing Lock-Free Live Storage Pipeline...")
    verify_and_parse_scope()
    
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"2026-06-30 {datetime.now().strftime('%H:%M:%S')} INFO [System] Telemetry stream channel initialized.\n")

    print(f"\n--- SwarmOps Active Log Pipeline Open ---\n[*] Tailing file: {LOG_FILE}\n[*] Awaiting incoming updates...")
    active_operation = "analyze_logs"

    # Track file byte offset persistently across independent open/close cycles
    last_position = os.path.getsize(LOG_FILE)

    try:
        while True:
            check_killswitch()
            
            # Open, read any new contents, and immediately release the file lock
            if os.path.exists(LOG_FILE):
                current_size = os.path.getsize(LOG_FILE)
                if current_size > last_position:
                    with open(LOG_FILE, "r", encoding="utf-8") as log_stream:
                        log_stream.seek(last_position)
                        lines = log_stream.readlines()
                        last_position = log_stream.tell()
                    
                    # Process lines harvested during this interval
                    for line in lines:
                        raw_telemetry = line.strip()
                        if not raw_telemetry:
                            continue
                            
                        log_audit(f"Disk read intercept: '{raw_telemetry}'")
                        verify_and_parse_scope(requested_action=active_operation)
                        
                        host_metrics = get_windows_disk_metrics()
                        
                        # TIER 1: Qwen Triage
                        triage_prompt = (
                            f"Analyze this telemetry string for any critical infrastructure exceptions.\n"
                            f"Telemetry: '{raw_telemetry}'\n\n"
                            f"Constraint: Return JSON formatting ONLY.\n"
                            f"JSON Template: {{\"anomaly\": true/false, \"severity\": \"LOW\"/\"MEDIUM\"/\"HIGH\", \"reason\": \"string\"}}"
                        )
                        triage_raw = query_local_llm(model_name="qwen2.5-coder:1.5b", prompt=triage_prompt)
                        
                        try:
                            clean_json = triage_raw.strip().replace("```json", "").replace("```", "").strip()
                            triage_data = json.loads(clean_json)
                            is_anomaly = triage_data.get("anomaly", False)
                            severity = triage_data.get("severity", "LOW")
                            reason = triage_data.get("reason", "No reason provided.")
                        except Exception:
                            log_audit("JSON parsing boundary failed. Escalating safely.", level="WARNING")
                            is_anomaly, severity, reason = True, "HIGH", "Parsing failure on raw response string."

                        log_audit(f"Tier 1 Triage complete -> Anomaly: {is_anomaly} | Severity: {severity}")
                        
                        # ----------------------------------------------------
                        # TIER 2: Llama Executive Escalation & Command Deck
                        # ----------------------------------------------------
                        if is_anomaly:
                            log_audit("Escalation sequence triggered. Engaging Tier 2 Executive...")
                            
                            # Sound an audio beep alert to wake up the human operator
                            if sys.platform == "win32":
                                import ctypes
                                ctypes.windll.user32.MessageBeep(0)
                            
                            # Hardened executive prompt to prevent memory vs disk hallucinations
                            executive_prompt = (
                                f"Context: An infrastructure exception was identified by Tier 1 processing gates.\n"
                                f"Raw Incident Line: '{raw_telemetry}'\n"
                                f"Triage Assessment: {reason} (Severity Level: {severity})\n"
                                f"Host Environment Specs: {host_metrics}\n"
                                f"TARGET OPERATING SYSTEM: Windows Native Environment (CMD/PowerShell execution context).\n\n"
                                f"Task: Generate a precise 3-point IT Admin remediation ticket draft matching this environment context.\n\n"
                                f"CRITICAL SYSTEM RULES (YOU MUST FOLLOW THESE SEVERELY):\n"
                                f"1. ENVIRONMENT CONFORMANCE: The host system is Windows. DO NOT suggest Linux utilities (such as 'df', 'smartctl', 'grep', 'top', or '/dev/sda'). Only recommend Windows-native solutions, commands (e.g., Get-Volume, Get-Process, Get-Service, tasklist), or database configuration adjustments.\n"
                                f"2. DATA ACCURACY: Review free storage vs total storage carefully. Do not invert calculations or misuse percentages (e.g., if ~1800 GB is free out of ~2000 GB, the system has ~12% usage and is mostly empty, NOT 88% usage).\n"
                                f"3. APPLICATION FOCUS: Address the exception's actual root cause. If physical memory metrics on the host are healthy but the database reports an Out Of Memory (OOM) error, acknowledge that this points towards internal process-specific heap/virtual memory allocation caps, not physical disk or physical RAM starvation. Do NOT tell the administrator to check, expand, or adjust storage drives."
                            )
                            
                            final_report = query_local_llm(model_name="llama3.2:3b", prompt=executive_prompt)
                            write_to_approval_boundary(f"ALERT: System Incident Report - {severity}", final_report)
                            
                            # --- INTERACTIVE COMMAND DECK COMMAND INTERFACE ---
                            print("\n" + "!" * 60)
                            print(f"!!! SWARM ALERT: CRITICAL INFRASTRUCTURE ANOMALY DETECTED !!!")
                            print("!" * 60)
                            print(f"[!] TELEMETRY METRIC : {raw_telemetry}")
                            print(f"[!] TRIAGE REASON    : {reason}")
                            print(f"[!] LOCAL STATUS     : {host_metrics}")
                            print("-" * 60)
                            print(f"Proposed Remediation Draft Generated by Llama-3B:\n")
                            print(final_report)
                            print("-" * 60)
                            
                            # Hold execution thread and force explicit human-in-the-loop validation
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
                            write_to_approval_boundary("Telemetry Nominal", f"System state checked clean. Log processed:\n{raw_telemetry}\n{host_metrics}")
                                
                        print("[*] Event cycle complete. Re-tailing log path...\n")
                        
                elif current_size < last_position:
                    # Handle case where log file is rotated or truncated externally
                    log_audit("Telemetry log truncation detected. Resetting byte offset pointer.", level="WARNING")
                    last_position = 0
            
            time.sleep(1.0)
                
    except KeyboardInterrupt:
        log_audit("Engine loop interrupted via hardware terminal sign-off.", level="WARNING")
        print("\n[-] Core pipeline deactivated safely.")

if __name__ == "__main__":
    run_live_pipeline()