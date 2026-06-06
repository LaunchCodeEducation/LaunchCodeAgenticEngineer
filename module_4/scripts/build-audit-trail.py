#!/usr/bin/env python3
"""Combine per-job reports into one audit trail JSON file."""

import argparse
import glob
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def load_json(path: str | Path, default: Any) -> Any:
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sha", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--touches-policy", default="false")
    parser.add_argument("--artifacts", default="ci-artifacts")
    args = parser.parse_args()

    art = Path(args.artifacts)
    policy = load_json(art / "policy-report.json", {})
    deterministic = load_json(art / "deterministic-report.json", None)
    rubric = load_json(art / "rubric-report.json", None)

    agent_actions = []
    denials = []
    for path in glob.glob(str(art / "audit-*.log")):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    entry = {"raw": line, "outcome": "unparsed"}
                agent_actions.append({
                    "role": entry.get("role"),
                    "operation": entry.get("operation"),
                    "outcome": entry.get("outcome") or entry.get("event"),
                })
                if entry.get("outcome") == "authorization_denied" or entry.get("event") == "authorization_denied":
                    denials.append(entry)

    trail = {
        "metadata": {
            "sha": args.sha,
            "pr": args.pr,
            "event": os.environ.get("GITHUB_EVENT_NAME", "pull_request"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
        "policy": {
            "passed": policy.get("exitcode", 0) == 0 if policy else False,
            "checks": policy.get("tests", []),
        },
        "harness": {
            "triggered": deterministic is not None or rubric is not None,
            "passed": ((deterministic or {}).get("exitcode", 0) == 0 and (rubric or {}).get("exitcode", 0) == 0) if (deterministic or rubric) else True,
            "deterministic": (deterministic or {}).get("tests", []),
            "rubric": (rubric or {}).get("tests", []),
        },
        "agent_actions": agent_actions,
        "authorization_denials": denials,
        "touches_policy": args.touches_policy == "true",
    }

    with open(f"ci-audit-trail-{args.sha}.json", "w", encoding="utf-8") as f:
        json.dump(trail, f, indent=2)
        f.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
