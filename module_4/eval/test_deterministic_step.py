import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from validate_handoff_deterministic import validate

SCHEMA = {"required": ["task_id", "summary", "owner"]}


def test_holdout_basic_handoff():
    document = {"task_id": "T-1001", "summary": "Add retry logic", "owner": "planner"}
    assert validate(document, SCHEMA) == []


def test_holdout_handoff_with_long_summary():
    document = {"task_id": "T-1002", "summary": "x" * 500, "owner": "reviewer"}
    assert validate(document, SCHEMA) == []


def test_holdout_handoff_with_numeric_owner_id_as_string():
    document = {"task_id": "T-1003", "summary": "Fix flaky test", "owner": "tester"}
    assert validate(document, SCHEMA) == []


def test_extra_fields_are_allowed():
    document = {
        "task_id": "T-1004",
        "summary": "Refactor parser",
        "owner": "implementer",
        "priority": "high",
    }
    assert validate(document, SCHEMA) == []


def test_empty_required_field_is_rejected():
    document = {"task_id": "T-1005", "summary": "", "owner": "planner"}
    problems = validate(document, SCHEMA)
    assert "required field is empty: summary" in problems


def test_whitespace_required_field_is_rejected():
    document = {"task_id": "T-1005", "summary": "   ", "owner": "planner"}
    problems = validate(document, SCHEMA)
    assert "required field is empty: summary" in problems


def test_missing_required_field_is_rejected():
    document = {"task_id": "T-1006", "owner": "reviewer"}
    problems = validate(document, SCHEMA)
    assert "missing required field: summary" in problems
