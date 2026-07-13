"""
SwarmOps — Dynamic File Categorizer

Discovers categories from file content, classifies every file, and moves them
into folders inside the target directory. No human interaction required.

High confidence → <target>/<Category Name>/
Low confidence  → <target>/_needs_human_review/
No fit          → <target>/_the_junk_drawer/

Results are written to categorizer_results.json for Claude to present in chat.

Usage:
    python file_categorizer.py <target_directory>
    python file_categorizer.py <target_directory> --dry-run
    python file_categorizer.py <target_directory> --voice
"""

import os
import re
import sys
import json
import random
import shutil
import subprocess
import threading
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

SPEAK_PY = Path(__file__).parent.parent / "phigmund" / "speak.py"

def phigmund_speak(text: str = None, event: str = None, mode: str = "standard") -> None:
    if not SPEAK_PY.exists():
        return
    try:
        args = [sys.executable, str(SPEAK_PY), "--mode", mode]
        if event:
            args += ["--event", event]
        else:
            args += [text]
        subprocess.run(args, check=False)
    except Exception:
        pass


# ============================================================
# CONFIG
# ============================================================
CONFIDENCE_THRESHOLD = 70
OLLAMA_MODEL = "llama3.2:3b"
DISCOVERY_SAMPLE_CHARS = 500
MAX_CHARS_PER_FILE = 2000
DISCOVERY_MAX_FILES = 40
NEEDS_REVIEW_FOLDER = "_needs_human_review"
JUNK_DRAWER_FOLDER = "_the_junk_drawer"
RESULTS_FILE = "categorizer_results.json"

RESERVED_FOLDERS = {NEEDS_REVIEW_FOLDER, JUNK_DRAWER_FOLDER}
MAX_SUGGESTED_NAME_LEN = 60
ILLEGAL_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


# ============================================================
# OLLAMA CLIENT
# ============================================================
def query_ollama(prompt: str, timeout: int = 90) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")).get("response", "")
            return f"HTTP_ERROR_{resp.status}"
    except urllib.error.URLError as e:
        return f"CONNECTION_ERROR: {e}"
    except Exception as e:
        return f"EXCEPTION: {e}"


# ============================================================
# FILE READING
# ============================================================
def read_file_sample(file_path: Path, max_chars: int = MAX_CHARS_PER_FILE) -> str:
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read(max_chars)
    except Exception as e:
        return f"[UNREADABLE: {e}]"


# ============================================================
# PHASE 1 — DISCOVER CATEGORIES
# ============================================================
def discover_categories(files: list) -> list:
    sample_files = files if len(files) <= DISCOVERY_MAX_FILES else random.sample(files, DISCOVERY_MAX_FILES)

    print(f"[*] Sampling {len(sample_files)} file(s) to discover categories...")

    file_blocks = []
    for i, fp in enumerate(sample_files, 1):
        sample = read_file_sample(fp, max_chars=DISCOVERY_SAMPLE_CHARS)
        file_blocks.append(f"FILE {i} ({fp.name}):\n{sample}")

    prompt = (
        "You are analyzing a collection of files to determine how to organize them.\n"
        "Here are content samples:\n\n"
        + "\n\n".join(file_blocks) +
        "\n\nSuggest 4 to 8 category names that would organize these files into logical groups.\n"
        "Rules:\n"
        "1. Categories must emerge from what the files ACTUALLY contain.\n"
        "2. Short, clear names — 2 to 5 words max.\n"
        "3. Some files may not fit any category — that is expected.\n"
        "4. Return ONLY a JSON array of strings. No explanation. No markdown.\n\n"
        'Example: ["Category A", "Category B", "Category C"]'
    )

    print("[*] Asking Ollama to derive categories...")
    raw = query_ollama(prompt, timeout=120)

    if raw.startswith(("CONNECTION_ERROR", "HTTP_ERROR", "EXCEPTION")):
        print(f"[ERROR] Ollama error during discovery: {raw}")
        sys.exit(1)

    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        start = clean.find("[")
        end = clean.rfind("]") + 1
        if start == -1 or end == 0:
            raise ValueError("No JSON array in response")
        categories = json.loads(clean[start:end])
        return [str(c).strip() for c in categories if str(c).strip()]
    except (json.JSONDecodeError, ValueError) as e:
        print(f"[ERROR] Could not parse category list: {e}\nRaw: {raw[:300]}")
        sys.exit(1)


def sanitize_suggested_filename(name) -> str | None:
    """Clean up Ollama's suggested filename: strip illegal chars, cap length,
    fall back to None (meaning: keep original name) if nothing usable comes back."""
    if not name or not isinstance(name, str):
        return None
    cleaned = ILLEGAL_FILENAME_CHARS.sub("", name).strip().strip(".")
    cleaned = re.sub(r"\s+", "_", cleaned)
    cleaned = cleaned[:MAX_SUGGESTED_NAME_LEN].strip("_")
    return cleaned or None


# ============================================================
# PHASE 2 — CLASSIFY ONE FILE
# ============================================================
def classify_file(file_path: Path, categories: list) -> dict:
    sample = read_file_sample(file_path)
    category_list = "\n".join(f"- {c}" for c in categories)

    prompt = (
        f"Classify this file into exactly ONE category from the list below, "
        f"or use 'no_fit' if it does not belong in any of them.\n\n"
        f"CATEGORIES:\n{category_list}\n- no_fit\n\n"
        f"FILE NAME: {file_path.name}\n"
        f"FILE CONTENT:\n---\n{sample}\n---\n\n"
        f"Also suggest a short, descriptive filename (no extension) based on what the "
        f"file actually contains — this replaces generic names like 'New Text Document "
        f"(247)'. Rules: 3 to 6 words, lowercase, words separated by underscores, no "
        f"special characters, specific enough to identify the file's content at a glance.\n\n"
        f"Return valid JSON only. No markdown. No explanation.\n"
        f'{{"category": "...", "confidence": 0-100, "reason": "one sentence", '
        f'"suggested_filename": "short_descriptive_name"}}'
    )

    raw = query_ollama(prompt)

    if raw.startswith(("CONNECTION_ERROR", "HTTP_ERROR", "EXCEPTION")):
        return {"category": "no_fit", "confidence": 0, "reason": raw, "error": raw, "suggested_filename": None}

    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        # Find the JSON object — Ollama sometimes wraps it in text or double-encodes it
        start = clean.find("{")
        end = clean.rfind("}") + 1
        if start != -1 and end > 0:
            clean = clean[start:end]
        parsed = json.loads(clean)
        # Handle double-encoded JSON (Ollama returns a string instead of a dict)
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
        category = parsed.get("category", "no_fit")
        confidence = int(parsed.get("confidence", 0))
        reason = parsed.get("reason", "")
        suggested_filename = sanitize_suggested_filename(parsed.get("suggested_filename"))

        if category not in categories and category != "no_fit":
            category = "no_fit"
            confidence = max(0, confidence - 20)

        return {
            "category": category,
            "confidence": confidence,
            "reason": reason,
            "error": None,
            "suggested_filename": suggested_filename,
        }

    except (json.JSONDecodeError, ValueError):
        return {
            "category": "no_fit",
            "confidence": 0,
            "reason": f"Parse failure: {raw[:100]}",
            "error": "PARSE_FAILURE",
            "suggested_filename": None,
        }


# ============================================================
# SCREEN-RECORDING HEARTBEAT
# ============================================================
_HEARTBEAT_LINES = [
    "      [*] reading file content...",
    "      [*] querying llama3.2:3b...",
    "      [*] evaluating category fit...",
    "      [*] checking confidence threshold...",
]


def _classify_with_heartbeat(file_path: Path, categories: list) -> dict:
    """Runs classify_file() on a background thread while printing genuinely
    new scrolling status lines on the main thread every ~0.4s. Without this,
    the terminal sits frozen on one line for the several seconds each Ollama
    call takes — looks like a stalled/frozen screen on a recording instead of
    live activity. Purely cosmetic — does not change classification logic."""
    result_box = {}

    def _target():
        result_box["value"] = classify_file(file_path, categories)

    t = threading.Thread(target=_target)
    t.start()
    i = 0
    while t.is_alive():
        print(_HEARTBEAT_LINES[i % len(_HEARTBEAT_LINES)])
        i += 1
        time.sleep(0.4)
    t.join()
    return result_box["value"]


# ============================================================
# PHASE 3 — MOVE FILES
# ============================================================
def resolve_dest_name(dest_folder: Path, base_name: str, extension: str) -> str:
    """Avoid collisions: file.txt -> file (2).txt -> file (3).txt ..."""
    candidate = f"{base_name}{extension}"
    if not (dest_folder / candidate).exists():
        return candidate
    n = 2
    while (dest_folder / f"{base_name} ({n}){extension}").exists():
        n += 1
    return f"{base_name} ({n}){extension}"


def move_file(file_path: Path, dest_folder: Path, dry_run: bool, suggested_filename: str = None) -> tuple[bool, str]:
    """Moves file_path into dest_folder, optionally renaming it to
    suggested_filename (original extension always preserved). Returns
    (success, final_filename_used)."""
    dest_folder.mkdir(parents=True, exist_ok=True)

    if suggested_filename:
        final_name = resolve_dest_name(dest_folder, suggested_filename, file_path.suffix)
    else:
        final_name = file_path.name

    dest = dest_folder / final_name
    if dry_run:
        return True, final_name
    try:
        shutil.move(str(file_path), str(dest))
        return True, final_name
    except Exception as e:
        print(f"  [ERROR] Could not move {file_path.name}: {e}")
        return False, file_path.name


# ============================================================
# MAIN
# ============================================================
def run(target_dir: str, voice: bool = False, dry_run: bool = False) -> None:
    target = Path(target_dir)
    if not target.exists() or not target.is_dir():
        print(f"[ERROR] Directory not found: {target_dir}")
        sys.exit(1)

    # Only process files in the root — skip any subfolders we may have created
    files = [
        f for f in sorted(target.iterdir())
        if f.is_file() and f.name != RESULTS_FILE
    ]

    if not files:
        print(f"[ERROR] No files found in: {target_dir}")
        sys.exit(1)

    mode_label = "DRY RUN — no files will be moved" if dry_run else "LIVE — files will be moved"

    print(f"\n{'=' * 60}")
    print(f"SwarmOps File Categorizer")
    print(f"{'=' * 60}")
    print(f"Target : {target_dir}")
    print(f"Files  : {len(files)}")
    print(f"Model  : {OLLAMA_MODEL}")
    print(f"Mode   : {mode_label}\n")

    print("[*] Verifying Ollama connection...")
    test = query_ollama("Reply with the single word: ONLINE")
    if "CONNECTION_ERROR" in test or "HTTP_ERROR" in test or "EXCEPTION" in test:
        print(f"[ERROR] Cannot reach Ollama. Start with: ollama serve\n{test}")
        sys.exit(1)
    print("[*] Ollama: connected\n")

    if voice:
        phigmund_speak(event="startup", mode="standard")

    # Phase 1 — discover
    categories = discover_categories(files)
    print(f"\n[*] Discovered {len(categories)} categories:")
    for cat in categories:
        print(f"      - {cat}")
    print()

    # Phase 2 + 3 — classify and move
    moved = []
    needs_review = []
    junk = []

    for i, file_path in enumerate(files, 1):
        print(f"[{i:>3}/{len(files)}] {file_path.name}")
        result = _classify_with_heartbeat(file_path, categories)

        suggested_name = result.get("suggested_filename")

        if result["category"] == "no_fit":
            dest = target / JUNK_DRAWER_FOLDER
            _, final_name = move_file(file_path, dest, dry_run, suggested_name)
            junk.append({
                "file": file_path.name,
                "renamed_to": final_name if final_name != file_path.name else None,
                "reason": result["reason"],
                "confidence": result["confidence"],
            })
            print(f"→ {JUNK_DRAWER_FOLDER}/{final_name}  ({result['confidence']}/100)")

        elif result["confidence"] < CONFIDENCE_THRESHOLD:
            dest = target / NEEDS_REVIEW_FOLDER
            _, final_name = move_file(file_path, dest, dry_run, suggested_name)
            needs_review.append({
                "file": file_path.name,
                "renamed_to": final_name if final_name != file_path.name else None,
                "suggested_category": result["category"],
                "confidence": result["confidence"],
                "reason": result["reason"],
            })
            print(f"→ {NEEDS_REVIEW_FOLDER}/{final_name}  {result['category']} ({result['confidence']}/100)")

        else:
            dest = target / result["category"]
            _, final_name = move_file(file_path, dest, dry_run, suggested_name)
            moved.append({
                "file": file_path.name,
                "renamed_to": final_name if final_name != file_path.name else None,
                "category": result["category"],
                "confidence": result["confidence"],
                "reason": result["reason"],
            })
            print(f"→ {result['category']}/{final_name}  ({result['confidence']}/100)")

    # Write results
    results = {
        "generated": datetime.now().isoformat(),
        "target_dir": str(target),
        "model": OLLAMA_MODEL,
        "dry_run": dry_run,
        "categories": categories,
        "moved": moved,
        "needs_review": needs_review,
        "junk_drawer": junk,
    }
    results_path = target / RESULTS_FILE
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    # Summary
    print(f"\n{'=' * 60}")
    if dry_run:
        print("DRY RUN COMPLETE — nothing was moved")
    else:
        print("DONE")
    print(f"  {len(moved):>3} file(s) moved automatically")
    print(f"  {len(needs_review):>3} file(s) → {NEEDS_REVIEW_FOLDER}/")
    print(f"  {len(junk):>3} file(s) → {JUNK_DRAWER_FOLDER}/")
    print(f"\nResults: {results_path}")
    print(f"{'=' * 60}\n")

    if voice:
        phigmund_speak(event="success", mode="standard")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python file_categorizer.py <target_directory> [--dry-run] [--voice]")
        sys.exit(1)
    dry_run_flag = "--dry-run" in sys.argv
    voice_flag = "--voice" in sys.argv
    target_arg = next(a for a in sys.argv[1:] if not a.startswith("--"))
    run(target_arg, voice=voice_flag, dry_run=dry_run_flag)
