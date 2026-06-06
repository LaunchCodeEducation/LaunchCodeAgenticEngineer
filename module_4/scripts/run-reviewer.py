#!/usr/bin/env python3
"""Sample advisory reviewer entry point.

This intentionally avoids calling a live model. Replace run_reviewer_subagent with
your Module 4 reviewer integration when credentials and infrastructure are ready.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path


def run_reviewer_subagent(changed_files: list[str]) -> str:
    if not changed_files:
        return "No changed files were detected."
    lines = ["### Files reviewed", ""]
    for filename in changed_files:
        lines.append(f"- `{filename}`")
    lines.extend([
        "",
        "### Advisory findings",
        "",
        "No blocking issue was detected by the sample reviewer. Replace this stub with the real reviewer subagent when ready.",
    ])
    return "\n".join(lines)


def main() -> int:
    changed = os.environ.get("CHANGED_FILES", "").split()
    out_dir = Path("/out") if Path("/out").exists() else Path("ci-out")
    out_dir.mkdir(parents=True, exist_ok=True)

    review_text = run_reviewer_subagent(changed)
    (out_dir / "review-output.md").write_text(review_text + "\n", encoding="utf-8")

    audit = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "role": "reviewer",
        "operation": "agent_review",
        "outcome": "success",
        "changed_files": changed,
    }
    with open(out_dir / "audit.log", "a", encoding="utf-8") as handle:
        handle.write(json.dumps(audit) + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
