from __future__ import annotations

import json
import os
from pathlib import Path

LIMIT = 200
NOTE = "everyday-wonder line runner"
TAGLINE = "streetlight trust, six fifty-eight"


def source_path() -> Path:
    return Path(__file__).resolve().parent / "entry.txt"


def squeeze(raw: str) -> str:
    body = raw.replace("\r\n", "\n").replace("\r", "\n").strip("\n")
    for candidate in body.split("\n"):
        if candidate.strip():
            return candidate.strip()
    return ""


def evaluate(text: str) -> dict:
    size = len(text)
    if not text.strip():
        return {"state": "empty", "chars": size, "cap": LIMIT}
    if size > LIMIT:
        return {"state": "too-long", "chars": size, "cap": LIMIT}
    return {"state": "ready", "chars": size, "cap": LIMIT}


def main() -> int:
    origin = source_path()
    if not origin.exists():
        print(json.dumps({"state": "missing-source", "note": NOTE}))
        return 1
    verdict = evaluate(squeeze(origin.read_text(encoding="utf-8")))
    if verdict["state"] != "ready":
        print(json.dumps(verdict))
        return 1
    dest = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest.mkdir(parents=True, exist_ok=True)
    with open(dest / "entry.txt", "w", encoding="utf-8", newline="\n") as fh:
        fh.write(squeeze(origin.read_text(encoding="utf-8")))
    print(json.dumps({**verdict, "note": NOTE, "tagline": TAGLINE,
                      "series": "wonder-1930"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
