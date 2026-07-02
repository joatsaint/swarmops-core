"""
Generate realistic Windows Security Event Log lines for Active Directory testing.
Run this in a second PowerShell window while orchestrator_ad.py is watching.

Usage:
    python generate_ad_events.py                  # one random event
    python generate_ad_events.py --event 4740     # specific event ID
    python generate_ad_events.py --storm          # lockout storm (5 rapid lockouts)
    python generate_ad_events.py --all            # one of every event type

Output writes to: watch_folder\telemetry.log
"""
import argparse
import os
import random
import time
from datetime import datetime

# Anchor to the script's own location so it finds the right watch_folder
# regardless of which directory PowerShell is sitting in.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE   = os.path.join(SCRIPT_DIR, "watch_folder", "telemetry.log")

# AD event definitions: ID → (description, default_severity, sample_accounts)
AD_EVENTS = {
    4625: ("An account failed to log on",         "LOW",    ["jsmith", "mrodriguez", "tlee", "UNKNOWN"]),
    4740: ("A user account was locked out",        "HIGH",   ["jsmith", "mrodriguez", "bwilliams"]),
    4728: ("Member added to security-enabled global group", "MEDIUM", ["contractor01", "newuser", "svc_backup"]),
    4732: ("Member added to security-enabled local group",  "MEDIUM", ["contractor01", "newuser"]),
    4756: ("Member added to security-enabled universal group", "HIGH", ["svc_batch", "admin_temp"]),
    4720: ("A user account was created",           "MEDIUM", ["temp_user01", "contractor_ext", "svc_new"]),
    4726: ("A user account was deleted",           "MEDIUM", ["old_employee", "temp_user01"]),
    4776: ("DC attempted to validate credentials (NTLM)", "LOW", ["jsmith", "mrodriguez", "ANONYMOUS"]),
    4648: ("Logon attempted with explicit credentials", "MEDIUM", ["svc_batch", "admin_temp"]),
    4672: ("Special privileges assigned to new logon", "HIGH", ["Administrator", "svc_deploy"]),
}

DOMAIN_CONTROLLERS = ["DC01", "DC02", "DC03"]
WORKSTATIONS      = ["WS-ACCT-01", "WS-IT-14", "WS-MGMT-05", "LAPTOP-FIELD-03"]
PRIVILEGED_GROUPS = ["Domain Admins", "Enterprise Admins", "Schema Admins", "Administrators"]
STANDARD_GROUPS   = ["Helpdesk", "VPN_Users", "FileShare_RW", "Remote_Desktop_Users"]


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _build_line(event_id):
    desc, severity, accounts = AD_EVENTS[event_id]
    account = random.choice(accounts)
    dc      = random.choice(DOMAIN_CONTROLLERS)
    ws      = random.choice(WORKSTATIONS)

    if event_id in (4728, 4732, 4756):
        group = random.choice(PRIVILEGED_GROUPS if event_id in (4728, 4756) else STANDARD_GROUPS)
        return (f"{_timestamp()} {severity} [AD:{event_id}] {desc} | "
                f"Account: {account} | Group: {group} | DC: {dc}")

    if event_id in (4720, 4726):
        return (f"{_timestamp()} {severity} [AD:{event_id}] {desc} | "
                f"New Account: {account} | DC: {dc}")

    if event_id == 4672:
        return (f"{_timestamp()} {severity} [AD:{event_id}] {desc} | "
                f"Account: {account} | Privileges: SeDebugPrivilege, SeTcbPrivilege | DC: {dc}")

    return (f"{_timestamp()} {severity} [AD:{event_id}] {desc} | "
            f"Account: {account} | Source: {ws} | DC: {dc}")


def write_event(line):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"[+] Written: {line}")


def main():
    parser = argparse.ArgumentParser(description="AD event generator for SwarmOps testing")
    parser.add_argument("--event", type=int, choices=AD_EVENTS.keys(),
                        help="Specific AD event ID to generate")
    parser.add_argument("--storm", action="store_true",
                        help="Generate a lockout storm: 5 rapid 4740 events for the same account")
    parser.add_argument("--all", action="store_true",
                        help="Write one event of every type")
    args = parser.parse_args()

    if args.storm:
        account = random.choice(["jsmith", "mrodriguez", "bwilliams"])
        dc      = random.choice(DOMAIN_CONTROLLERS)
        ws      = random.choice(WORKSTATIONS)
        print(f"[!] Generating lockout storm for account: {account}")
        for i in range(5):
            line = (f"{_timestamp()} HIGH [AD:4740] A user account was locked out | "
                    f"Account: {account} | Source: {ws} | DC: {dc} | Count: {i+1}/5")
            write_event(line)
            time.sleep(0.4)
        return

    if args.all:
        for event_id in AD_EVENTS:
            write_event(_build_line(event_id))
            time.sleep(0.3)
        return

    if args.event:
        write_event(_build_line(args.event))
        return

    # Default: one random event weighted toward interesting ones
    weighted = [4625, 4625, 4740, 4740, 4728, 4756, 4672, 4720, 4776, 4648]
    write_event(_build_line(random.choice(weighted)))


if __name__ == "__main__":
    main()
