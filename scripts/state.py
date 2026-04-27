#!/usr/bin/env python3
"""Read/update a novel's state.json. Pure file IO, no LLM.

Usage:
  python state.py <novel-dir> get [key]
  python state.py <novel-dir> set <key> <value>      # value parsed as JSON
  python state.py <novel-dir> add-debt <trigger> <affected-csv>
  python state.py <novel-dir> init                   # create from template
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TEMPLATE = BASE / "templates" / "state.json"


def load(novel_dir: Path) -> dict:
    p = novel_dir / "state.json"
    return json.loads(p.read_text()) if p.exists() else json.loads(TEMPLATE.read_text())


def save(novel_dir: Path, state: dict):
    (novel_dir / "state.json").write_text(json.dumps(state, indent=2) + "\n")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    novel_dir = Path(sys.argv[1])
    novel_dir.mkdir(parents=True, exist_ok=True)
    cmd = sys.argv[2]
    state = load(novel_dir)

    if cmd == "init":
        save(novel_dir, json.loads(TEMPLATE.read_text()))
        print(f"initialised {novel_dir}/state.json")
    elif cmd == "get":
        if len(sys.argv) > 3:
            print(json.dumps(state.get(sys.argv[3])))
        else:
            print(json.dumps(state, indent=2))
    elif cmd == "set":
        key, val = sys.argv[3], sys.argv[4]
        try:
            state[key] = json.loads(val)
        except json.JSONDecodeError:
            state[key] = val
        save(novel_dir, state)
    elif cmd == "add-debt":
        trigger, affected = sys.argv[3], sys.argv[4].split(",")
        state.setdefault("debts", []).append({
            "trigger": trigger, "affected": affected, "status": "pending"
        })
        save(novel_dir, state)
    else:
        print(f"unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
