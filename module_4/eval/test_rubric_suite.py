"""Sample rubric suite.

Replace these placeholders with the Module 4 rubric-as-judge tests when connecting
real model-backed evaluations.
"""

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def test_review_output_has_advisory_label():
    text = (REPO / "docs" / "ci-step-design.md").read_text(encoding="utf-8")
    assert "advisory" in text.lower()


def test_adr_records_tradeoffs():
    text = (REPO / "docs" / "adr" / "ADR-001-json-schema-validation-deterministic-conversion.md").read_text(encoding="utf-8")
    assert "Known trade-off" in text
