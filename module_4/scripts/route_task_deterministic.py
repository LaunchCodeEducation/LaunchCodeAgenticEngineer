#!/usr/bin/env python3
"""Deterministically route changed files to a role."""

import argparse
import json
from pathlib import Path
from typing import Iterable


def route_for_path(path: str) -> str:
    if path.startswith("tests/") or path.startswith("eval/"):
        return "tester"
    if path.startswith("docs/") or path.endswith(".md"):
        return "project-manager"
    if path.startswith(".github/") or path.startswith("scripts/check-pipeline-integrity.py"):
        return "orchestrator"
    return "implementer"


def route_files(paths: Iterable[str]) -> dict:
    routes: dict[str, list[str]] = {}
    for path in paths:
        role = route_for_path(path)
        routes.setdefault(role, []).append(path)
    return routes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-files", nargs="*", default=[])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    result = {"routes": route_files(args.changed_files)}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
