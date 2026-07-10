"""
SwarmOps Milestone 4 — Approval Gate

Reads categorizer_results.json (written by file_categorizer.py). High-
confidence files are already moved by file_categorizer.py itself — this
gate is for the files it wasn't sure about: everything sitting in
_needs_human_review/. You review each one (by its title, possibly already
renamed to a descriptive name) and decide: accept the AI's suggested
category as-is, assign a different one, or skip it for now.

Usage:
    python approval_gate.py <target_directory>
    python approval_gate.py <target_directory> --auto-approve   (accept all suggested categories)
    python approval_gate.py <target_directory> --voice
"""

import sys
import json
import shutil
import logging
import subprocess
from datetime import datetime
from pathlib import Path

SPEAK_PY = Path(__file__).parent.parent / "phigmund" / "speak.py"


def phigmund_speak(text: str = None, event: str = None, mode: str = "standard") -> None:
    if not SPEAK_PY.exists():
        return
    try:
        args = [sys.executable, str(SPEAK_PY), "--mode", mode]
        args += ["--event", event] if event else [text]
        subprocess.run(args, check=False)
    except Exception:
        pass


RESULTS_FILE = "categorizer_results.json"
NEEDS_REVIEW_FOLDER = "_needs_human_review"
JUNK_DRAWER_FOLDER = "_the_junk_drawer"
AUDIT_LOG = "audit.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(AUDIT_LOG, mode="a", encoding="utf-8")],
)


def log(msg: str, level: str = "INFO") -> None:
    getattr(logging, level.lower())(msg)
    prefix = {"INFO": "[*]", "WARNING": "[!]", "CRITICAL": "[X]"}.get(level, "[*]")
    print(f"{prefix} {msg}")


# ============================================================
# LOAD RESULTS
# ============================================================
def load_results(target_dir: Path) -> dict:
    results_path = target_dir / RESULTS_FILE
    if not results_path.exists():
        print(f"\n[ERROR] {RESULTS_FILE} not found in {target_dir}.")
        print(f"        Run file_categorizer.py on this directory first.")
        sys.exit(1)

    with open(results_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    age_seconds = (datetime.now() - datetime.fromisoformat(data["generated"])).total_seconds()
    if age_seconds > 3600:
        print(f"\n[WARNING] Results are {int(age_seconds / 60)} minutes old.")
        print(f"          Consider re-running file_categorizer.py if files have changed.\n")

    return data


# ============================================================
# MOVE FILE (with audit trail) — mirrors file_categorizer.py's
# collision-avoidance behavior so re-runs never silently overwrite
# ============================================================
def resolve_dest_name(dest_folder: Path, file_path: Path) -> str:
    base, ext = file_path.stem, file_path.suffix
    if not (dest_folder / file_path.name).exists():
        return file_path.name
    n = 2
    while (dest_folder / f"{base} ({n}){ext}").exists():
        n += 1
    return f"{base} ({n}){ext}"


def move_file(src: Path, dest_dir: Path) -> bool:
    if not src.exists():
        log(f"Source no longer exists, skipping: {src.name}", "WARNING")
        return False
    try:
        dest_dir.mkdir(parents=True, exist_ok=True)
        final_name = resolve_dest_name(dest_dir, src)
        dest = dest_dir / final_name
        shutil.move(str(src), str(dest))
        log(f"MOVED: {src.name} -> {dest_dir.name}/{final_name}")
        return True
    except Exception as e:
        log(f"MOVE FAILED: {src.name} - {e}", "CRITICAL")
        return False


# ============================================================
# REVIEW: FLAGGED FILES (needs_human_review/)
# ============================================================
def handle_needs_review(entries: list, target_dir: Path, categories: list, auto_approve: bool) -> tuple[int, int]:
    if not entries:
        return 0, 0

    review_folder = target_dir / NEEDS_REVIEW_FOLDER

    print(f"\n{'-' * 70}")
    print(f"[!] NEEDS HUMAN REVIEW — {len(entries)} file(s)")
    print(f"    Model was uncertain. You decide what to do with each one.")
    print(f"{'-' * 70}\n")

    approved = skipped = 0

    for r in sorted(entries, key=lambda x: x["confidence"]):
        current_name = r.get("renamed_to") or r["file"]
        print(f"  File:       {current_name}")
        if r.get("renamed_to"):
            print(f"  (original:  {r['file']})")
        print(f"  Suggested:  {r['suggested_category']}  ({r['confidence']}/100 confidence)")
        print(f"  Reason:     {r['reason']}")
        print()
        print(f"  Options:")
        print(f"    [A] Accept — move to '{r['suggested_category']}' as suggested (recommended)")
        print(f"    [M] Manually assign a different category")
        print(f"    [S] Skip — leave in {NEEDS_REVIEW_FOLDER}/ for now")
        print()

        if auto_approve:
            print("  [auto-approve mode] -> A (accepting suggested category)")
            choice = "a"
        else:
            choice = ""
            while choice not in ["a", "m", "s"]:
                choice = input("  >> Enter option (A/M/S): ").strip().lower()

        src = review_folder / current_name

        if choice == "a":
            dest_dir = target_dir / r["suggested_category"]
            log(f"Operator accepted suggested category: {current_name} -> {r['suggested_category']} ({r['confidence']}/100)")
            if move_file(src, dest_dir):
                approved += 1
            else:
                skipped += 1
            print()

        elif choice == "m":
            print("\n  Available categories:")
            for i, cat in enumerate(categories, 1):
                print(f"    [{i:>2}] {cat}")
            cat_num = ""
            while not cat_num.isdigit() or not (1 <= int(cat_num) <= len(categories)):
                cat_num = input(f"  >> Enter number (1-{len(categories)}): ").strip()
            chosen = categories[int(cat_num) - 1]
            dest_dir = target_dir / chosen
            log(f"Operator manually assigned: {current_name} -> {chosen} (was: {r['suggested_category']} @ {r['confidence']}/100)")
            if move_file(src, dest_dir):
                approved += 1
            else:
                skipped += 1
            print()

        else:
            log(f"Operator skipped: {current_name} (confidence={r['confidence']}/100)", "WARNING")
            print(f"  [-] Skipped.\n")
            skipped += 1

    return approved, skipped


# ============================================================
# MAIN
# ============================================================
def run(target_dir_arg: str, auto_approve: bool = False, voice: bool = False) -> None:
    target_dir = Path(target_dir_arg)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"[ERROR] Directory not found: {target_dir_arg}")
        sys.exit(1)

    data = load_results(target_dir)
    needs_review = data.get("needs_review", [])
    junk = data.get("junk_drawer", [])
    categories = data.get("categories", [])

    print(f"\n{'=' * 70}")
    print(f"SwarmOps Approval Gate")
    print(f"{'=' * 70}")
    print(f"[*] Results from:   {data['generated']}")
    print(f"[*] Target dir:     {target_dir}")
    print(f"[*] Auto-moved:     {len(data.get('moved', []))} file(s) (already done by file_categorizer.py)")
    print(f"[*] Needs review:   {len(needs_review)} file(s)")
    print(f"[*] Junk drawer:    {len(junk)} file(s) (not reviewed here — see {JUNK_DRAWER_FOLDER}/)")
    print(f"[*] Mode:           {'AUTO-APPROVE' if auto_approve else 'INTERACTIVE'}")
    print()

    if not needs_review:
        print("[*] Nothing needs review. All confident files were already moved.\n")
        return

    log("Approval gate session started.")

    if voice:
        phigmund_speak(event="approval_required", mode="grail")

    approved, skipped = handle_needs_review(needs_review, target_dir, categories, auto_approve)

    print(f"\n{'=' * 70}")
    print(f"Session Complete")
    print(f"{'=' * 70}")
    print(f"  Moved:   {approved} file(s)")
    print(f"  Skipped: {skipped} file(s) (left in {NEEDS_REVIEW_FOLDER}/)")
    print(f"  Audit:   {AUDIT_LOG}")
    print(f"{'=' * 70}\n")

    log(f"Approval gate session complete. Moved={approved} Skipped={skipped}")

    if voice:
        phigmund_speak(event="moved" if approved > 0 else "flagged", mode="standard")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python approval_gate.py <target_directory> [--auto-approve] [--voice]")
        sys.exit(1)
    auto = "--auto-approve" in sys.argv
    voice_flag = "--voice" in sys.argv
    target_arg = next(a for a in sys.argv[1:] if not a.startswith("--"))
    run(target_arg, auto_approve=auto, voice=voice_flag)
