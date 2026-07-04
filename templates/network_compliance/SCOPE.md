# SwarmOps — Network Compliance Agent Scope File
# Control 1: This file defines what the agent is authorized to analyze.
# The engine will refuse to start if this file is missing or empty.
# Add or remove actions to match your environment's policy.

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
#   - Source IP matches internal management subnets (potential lateral movement)
#   - Any event involving credentials or authentication tokens
#
# Q3: If the goal and a constraint conflict, which wins?
#   CONSTRAINT WINS. Always. The goal is to detect and surface anomalies.
#   The constraint is to never act on them. If the agent cannot surface an
#   anomaly without acting on it, it writes SWARM BLOCKED to audit.log and stops.
