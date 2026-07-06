"""
Generate realistic network security event log lines for SwarmOps testing.
Run this in a second PowerShell window while orchestrator_net.py is watching.

Usage:
    python generate_net_events.py                      # one random event
    python generate_net_events.py --event firewall     # specific event type
    python generate_net_events.py --storm              # port scan storm (5 rapid events)
    python generate_net_events.py --all                # one of every type

Output writes to: watch_folder\telemetry.log
"""
import argparse
import os
import random
import time
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE   = os.path.join(SCRIPT_DIR, "watch_folder", "telemetry.log")

INTERNAL_HOSTS = [
    "192.168.1.45", "192.168.1.102", "192.168.1.200",
    "10.0.0.15", "10.0.0.88", "10.10.5.22",
]
EXTERNAL_IPS = [
    "91.108.4.0",      # Telegram CDN
    "185.220.101.45",  # Known Tor exit
    "203.0.113.77",    # TEST-NET (documentation range)
    "198.51.100.12",   # TEST-NET-2
    "45.33.32.156",    # Linode VPS (example)
    "104.21.8.153",    # Cloudflare
]
COUNTRIES = ["RU", "CN", "KP", "IR", "BY", "VE", "MM"]
SERVICES  = ["SSH", "RDP", "VPN-Gateway", "Web-Proxy"]
FIREWALLS = ["FW-CORE-01", "FW-EDGE-02", "FW-DMZ-03"]


def _timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _firewall_violation():
    host    = random.choice(INTERNAL_HOSTS)
    ext_ip  = random.choice(EXTERNAL_IPS)
    port    = random.choice([23, 445, 3389])
    fw      = random.choice(FIREWALLS)
    rule    = {23: "NET-BLOCK-TELNET", 445: "NET-BLOCK-SMB-EXT", 3389: "NET-BLOCK-RDP-EXT"}[port]
    svc     = {23: "Telnet", 445: "SMB", 3389: "RDP"}[port]
    src_port = random.randint(49152, 65535)
    return (f"{_timestamp()} ALERT [FIREWALL] Blocked outbound {host}:{src_port} -> "
            f"{ext_ip}:{port} ({svc}) — rule {rule} | fw: {fw}")


def _port_scan():
    src  = random.choice(INTERNAL_HOSTS + EXTERNAL_IPS)
    tgt  = random.choice(INTERNAL_HOSTS)
    count = random.randint(5, 12)
    ports = random.sample([22, 80, 443, 3389, 8080, 8443, 21, 25, 110, 5985, 1433, 3306], count)
    secs  = random.randint(8, 45)
    return (f"{_timestamp()} ALERT [NET] Port scan detected: {src} probed "
            f"{tgt} on ports {','.join(str(p) for p in sorted(ports))} "
            f"in {secs}s | count: {count} ports")


def _geo_anomaly():
    host    = random.choice(INTERNAL_HOSTS)
    ext_ip  = random.choice(EXTERNAL_IPS)
    country = random.choice(COUNTRIES)
    port    = random.choice([443, 80, 8080, 4444])
    bytes_  = random.randint(1024, 512000)
    return (f"{_timestamp()} ALERT [GEO] Outbound traffic to country={country} "
            f"not in baseline allow-list | src: {host} -> dst: {ext_ip}:{port} | "
            f"bytes: {bytes_}")


def _unusual_outbound():
    host   = random.choice(INTERNAL_HOSTS)
    ext_ip = random.choice(EXTERNAL_IPS)
    port   = random.choice([443, 8443, 9001])
    domain = random.choice(["cdn.unknown-vendor.io", "update.newapp.net",
                             "api.thirdparty.com", "telemetry.softwareco.net"])
    return (f"{_timestamp()} WARN [NET] First-seen outbound connection: "
            f"{host} -> {ext_ip}:{port} ({domain}) — not in baseline")


def _dns_anomaly():
    host   = random.choice(INTERNAL_HOSTS)
    ext_ip = random.choice(EXTERNAL_IPS)
    port   = random.choice([5353, 853, 4433, 8053])
    return (f"{_timestamp()} WARN [DNS] DNS traffic on non-standard port: "
            f"{host} -> {ext_ip}:{port} (expected port 53) — possible DNS tunneling")


def _auth_storm():
    host    = random.choice(INTERNAL_HOSTS + EXTERNAL_IPS)
    tgt     = random.choice(INTERNAL_HOSTS)
    service = random.choice(SERVICES)
    count   = random.randint(10, 47)
    mins    = random.randint(2, 5)
    return (f"{_timestamp()} ALERT [AUTH] Excessive failed auth: "
            f"{host} -> {tgt} | service: {service} | "
            f"{count} failures in {mins} min — brute-force pattern")


EVENT_BUILDERS = {
    "firewall":  _firewall_violation,
    "port_scan": _port_scan,
    "geo":       _geo_anomaly,
    "outbound":  _unusual_outbound,
    "dns":       _dns_anomaly,
    "auth":      _auth_storm,
}

WEIGHTED = (
    ["firewall"] * 3 + ["port_scan"] * 3 + ["geo"] * 2 +
    ["outbound"] * 2 + ["dns"] * 1 + ["auth"] * 3
)


def write_event(line):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(f"[+] Written: {line}")


def main():
    parser = argparse.ArgumentParser(description="Network event generator for SwarmOps testing")
    parser.add_argument(
        "--event",
        choices=list(EVENT_BUILDERS.keys()),
        help="Specific event type: firewall | port_scan | geo | outbound | dns | auth"
    )
    parser.add_argument(
        "--storm", action="store_true",
        help="Port scan storm: 5 rapid scan events from the same source"
    )
    parser.add_argument(
        "--all", action="store_true",
        help="Write one event of every type"
    )
    args = parser.parse_args()

    if args.storm:
        src = random.choice(EXTERNAL_IPS)
        tgt = random.choice(INTERNAL_HOSTS)
        print(f"[!] Generating port scan storm from: {src} -> {tgt}")
        for i in range(5):
            port_batch = random.sample([22, 80, 443, 3389, 8080, 8443, 21, 25], 4)
            line = (f"{_timestamp()} ALERT [NET] Port scan storm event {i+1}/5: "
                    f"{src} probed {tgt} on ports {','.join(str(p) for p in sorted(port_batch))} | "
                    f"storm sequence in progress")
            write_event(line)
            time.sleep(0.4)
        return

    if args.all:
        for key, builder in EVENT_BUILDERS.items():
            write_event(builder())
            time.sleep(0.3)
        return

    if args.event:
        write_event(EVENT_BUILDERS[args.event]())
        return

    write_event(EVENT_BUILDERS[random.choice(WEIGHTED)]())


if __name__ == "__main__":
    main()
