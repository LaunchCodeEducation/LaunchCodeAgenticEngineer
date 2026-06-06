# ADR-001: Convert JSON schema validation step from agent to deterministic code

## Status

Accepted

## Context

The orchestration includes a step that validates each handoff document against `schemas/handoff.json` before the next subagent consumes it. The step-classification document marks it a strong candidate on all four signals: stable harness scores, identical output on repeated runs, a specification a developer can implement directly, and a run on every workflow invocation. The classification also names the edge case the deterministic version must preserve: a required field that is present but blank must be treated as invalid, not accepted just because the key exists.

## Decision

Replace the agentic validation step with a small script that checks the handoff document against `schemas/handoff.json` and rejects it with a clear error if any required field is missing, null, or empty.

## Alternatives considered

- Keep the agentic step. Rejected. The calibration log before-conversion entry shows this step averaged 45 seconds of cycle time and $0.003 in token cost per run across three runs, while passing all 7 deterministic harness checks. It contributes no language understanding the task requires.
- Convert to deterministic code. Accepted after integration. The after-conversion entry shows the script averaged 0.2 seconds and $0 token cost across three runs, produced identical output on all three, and passed the same 7 deterministic checks with no regression.
- Shrink the agent with a tighter prompt and a smaller model. Rejected. It lowers token cost but keeps inference latency, output variance, and governance overhead.

## Consequences

Cycle time fell from 45 seconds to 0.2 seconds, token cost fell from $0.003 per run to zero, and output variance fell to zero. Known trade-off: the script returns a terse structured result rather than a generated prose explanation. If the structured problem list proves too thin for debugging, enrich the deterministic messages before considering a return to an agent.

## Evidence

- Classification: `docs/step-classification.md`, JSON schema validation marked strong candidate.
- Before-conversion measurement: `docs/calibration-log.md`, before-conversion entry.
- After-conversion measurement in isolation: `docs/calibration-log.md`, after-conversion entry.
- Integrated end-to-end regression check: `docs/calibration-log.md`, integrated end-to-end regression check.
