# ADR-002: Convert path-based routing step from agent to deterministic code

## Status

Proposed

## Context

The workflow contains a routing step that assigns work to a role based on changed file paths. The decision is structural: files under `tests/` go to the tester, files under `docs/` go to documentation/project-management work, and source changes go to the implementer. The main edge case is an unmatched path.

## Decision

Replace the agentic routing step with `scripts/route_task_deterministic.py`, which applies explicit ordered path rules and defaults unmatched paths to `implementer`.

## Alternatives considered

- Keep the agentic router. Rejected for the sample because the behavior is a lookup table, not judgment.
- Convert to deterministic code. Preferred, pending integration and full measurement.
- Keep both router and agent as fallback. Rejected because that preserves cost and governance complexity for a structural operation.

## Related decisions

Builds on ADR-001. Two lessons from that conversion shaped this one: identify the input class an agent handled by judgment that a script might miss, and write a test for it; mark model-only rubric dimensions as not applicable rather than failures.

## Evidence

Pending measurement and integration.
