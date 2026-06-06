# Calibration Log

## Near-miss patterns for Module 4 governance

1. The implementer subagent nearly called `delete_entry` on the storage server because its tool grant was temporarily too broad.  
   **Risk:** an implementer with delete access can silently remove project state that other subagents depend on.

2. A reviewer subagent's task output nearly triggered the `run-tests` skill, which is meant for the implementer and tester.  
   **Risk:** a read-only review role that can run tests can change the state of the workspace it is only supposed to inspect.

3. An implementer requested a document tagged `confidential`, above its `internal` ceiling, and the retrieval server refused it.  
   **Risk:** a role that can reach above its classification ceiling can pull sensitive material into a context it was not cleared for.

## Conversion measurements

### Before conversion — handoff validation agent

- Average cycle time: 45 seconds across three runs.
- Token cost: $0.003 per run.
- Deterministic harness checks: 7/7 passing.
- Review latency: about 30 seconds.

### After conversion — deterministic handoff validator in isolation

- Average cycle time: 0.2 seconds across three runs.
- Token cost: $0.
- Deterministic harness checks: 7/7 passing.
- Output variance: zero; `diff` reported no differences across three runs.
- Review latency: about 5 seconds.

### Integrated end-to-end regression check

- Date: 2026-06-06
- Result: 24/24 harness checks passing; no regressions.
- Policy suite: passing.
- Evidence: deterministic validator is wired into orchestration and governance artifacts are in sync.
