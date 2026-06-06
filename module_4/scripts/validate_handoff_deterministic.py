#!/usr/bin/env python3
"""Deterministic replacement for the agentic handoff-validation step.

Reads a handoff document, checks it against a schema's required fields, and writes
a result document. No language model is involved.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List


def load_json(path: str | Path) -> Dict[str, Any]:
    """Read a JSON file from disk and return it as a dictionary."""
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate(document: Dict[str, Any], schema: Dict[str, Any]) -> List[str]:
    """Return validation problems. An empty list means valid.

    A required field fails if it is missing, null, an empty string, or a string with
    only whitespace. This preserves the edge case the agent previously caught by
    judgment: present-but-empty is effectively missing.
    """
    problems: List[str] = []
    for field in schema.get("required", []):
        if field not in document:
            problems.append(f"missing required field: {field}")
        elif document[field] is None:
            problems.append(f"required field is empty: {field}")
        elif isinstance(document[field], str) and document[field].strip() == "":
            problems.append(f"required field is empty: {field}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="path to the handoff document")
    parser.add_argument("--schema", default="schemas/handoff.json", help="path to the schema")
    parser.add_argument("--output", required=True, help="path to write the result")
    args = parser.parse_args()

    document = load_json(args.input)
    schema = load_json(args.schema)
    problems = validate(document, schema)
    result = {"valid": len(problems) == 0, "problems": problems}

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
        handle.write("\n")

    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
