"""
Read-only comparison: llama3.2:3b vs qwen2.5-coder:1.5b on the real 346-file
corpus already categorized in docs/test files/. Never moves or renames
anything — reads each file wherever it currently sits (using the real
categorizer_results.json as the location index) and re-classifies with both
models, tracking JSON parse success/failure and agreement with the original
real result.
"""
import json
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from file_categorizer import read_file_sample, CONFIDENCE_THRESHOLD

RESULTS_PATH = Path("../docs/test files/categorizer_results.json")
TARGET_DIR = Path("../docs/test files")
MODELS = ["llama3.2:3b", "qwen2.5-coder:1.5b"]


def query_ollama(model: str, prompt: str, timeout: int = 90) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url, data=data, headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode("utf-8")).get("response", "")
            return f"HTTP_ERROR_{resp.status}"
    except urllib.error.URLError as e:
        return f"CONNECTION_ERROR: {e}"
    except Exception as e:
        return f"EXCEPTION: {e}"


def build_index(results: dict) -> list[dict]:
    """Map each real result entry to its actual current path on disk."""
    index = []
    for entry in results["moved"]:
        name = entry.get("renamed_to") or entry["file"]
        path = TARGET_DIR / entry["category"] / name
        index.append({"path": path, "real_category": entry["category"], "real_confidence": entry["confidence"]})
    for entry in results["needs_review"]:
        name = entry.get("renamed_to") or entry["file"]
        path = TARGET_DIR / "_needs_human_review" / name
        index.append({"path": path, "real_category": entry.get("suggested_category", "no_fit"), "real_confidence": entry["confidence"]})
    for entry in results["junk_drawer"]:
        name = entry.get("renamed_to") or entry["file"]
        path = TARGET_DIR / "_the_junk_drawer" / name
        index.append({"path": path, "real_category": "no_fit", "real_confidence": entry["confidence"]})
    return index


def classify_with_model(model: str, file_path: Path, categories: list) -> dict:
    sample = read_file_sample(file_path)
    category_list = "\n".join(f"- {c}" for c in categories)
    prompt = (
        f"Classify this file into exactly ONE category from the list below, "
        f"or use 'no_fit' if it does not belong in any of them.\n\n"
        f"CATEGORIES:\n{category_list}\n- no_fit\n\n"
        f"FILE NAME: {file_path.name}\n"
        f"FILE CONTENT:\n---\n{sample}\n---\n\n"
        f"Return valid JSON only. No markdown. No explanation.\n"
        f'{{"category": "...", "confidence": 0-100, "reason": "one sentence"}}'
    )
    raw = query_ollama(model, prompt)
    if raw.startswith(("CONNECTION_ERROR", "HTTP_ERROR", "EXCEPTION")):
        return {"parse_ok": False, "category": None, "error": raw}
    try:
        clean = raw.strip().replace("```json", "").replace("```", "").strip()
        start = clean.find("{")
        end = clean.rfind("}") + 1
        if start != -1 and end > 0:
            clean = clean[start:end]
        parsed = json.loads(clean)
        if isinstance(parsed, str):
            parsed = json.loads(parsed)
        return {"parse_ok": True, "category": parsed.get("category") or "no_fit", "confidence": int(parsed.get("confidence") or 0)}
    except (json.JSONDecodeError, ValueError):
        return {"parse_ok": False, "category": None, "raw": raw[:150]}


def main():
    results = json.loads(RESULTS_PATH.read_text(encoding="utf-8"))
    categories = results["categories"]
    index = build_index(results)
    total = len(index)
    print(f"[*] Real corpus: {total} files indexed from categorizer_results.json")
    print(f"[*] Models under test: {MODELS}\n")

    stats = {m: {"parse_ok": 0, "parse_fail": 0, "agrees_with_real": 0} for m in MODELS}

    for i, entry in enumerate(index, 1):
        fp = entry["path"]
        if not fp.exists():
            print(f"[{i}/{total}] MISSING (skipped): {fp}")
            continue
        print(f"[{i}/{total}] {fp.name}", end="  ")
        for model in MODELS:
            r = classify_with_model(model, fp, categories)
            if r["parse_ok"]:
                stats[model]["parse_ok"] += 1
                if r["category"] == entry["real_category"]:
                    stats[model]["agrees_with_real"] += 1
            else:
                stats[model]["parse_fail"] += 1
            print(f"| {model}: {'OK' if r['parse_ok'] else 'PARSE_FAIL'}", end=" ")
        print()

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    for model in MODELS:
        s = stats[model]
        n = s["parse_ok"] + s["parse_fail"]
        parse_rate = (s["parse_ok"] / n * 100) if n else 0
        agree_rate = (s["agrees_with_real"] / s["parse_ok"] * 100) if s["parse_ok"] else 0
        print(f"\n{model}:")
        print(f"  JSON parse success: {s['parse_ok']}/{n} ({parse_rate:.1f}%)")
        print(f"  Agrees with real categorized result: {s['agrees_with_real']}/{s['parse_ok']} ({agree_rate:.1f}%)")

    out_path = Path("model_comparison_results.json")
    out_path.write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(f"\n[*] Saved: {out_path}")


if __name__ == "__main__":
    main()
