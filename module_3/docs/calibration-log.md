# Calibration Log

Each entry captures the failure mode, the check that caught it, the result before the fix, the root-cause hypothesis, the fix layer and specific change, and the result after.

### [Date]: [Failure mode]

- **Failure mode:** [name]
- **Check that caught it:** [check name] (deterministic or rubric)
- **Before:** FAIL. [what the check reported]
- **Root-cause hypothesis:** [why the run produced this result]
- **Fix layer:** [routing / prompt / scope / tool]
- **Fix applied:** [file and what changed]; commit [SHA]
- **After:** PASS. [what the check reports now]

### 2026-06-01: Context bleed

- **Failure mode:** Context bleed
- **Check that caught it:** context_bleed (deterministic)
- **Before:** FAIL. planted marker leaked into reviewer and tester
- **Root-cause hypothesis:** The handoff template passed the full prior session instead of a scoped result, so downstream subagents saw upstream history.
- **Fix layer:** Scope (handoff content)
- **Fix applied:** orchestrator handoff template now strips session history and passes only the scoped result fields; commit a1b2c3d
- **After:** PASS. marker no longer leaks past its origin subagent

## Calibration Summary: [Date]

**Holdout set size:** [N] tasks

**Deterministic checks:** [M] / [total] passing across all tasks

**Rubric suite:** [aggregate score] / [max], [N] dimension checks passing threshold

**Tasks passing both layers fully:** [N] / [total]

**Failure modes surfaced and addressed:**

| Failure mode | Check that caught it | Fix applied | Before | After |
|---|---|---|---|---|
| Context bleed | context_bleed | Strip history in handoff | FAIL | PASS |
| Routing misfire | required_roles | Fix reviewer condition | FAIL | PASS |
| Conflicting reviewers | reviewer_conflict | Add resolution policy | FAIL | PASS |
| Retrieval miss | similarity_floor | Restore threshold, fallback | FAIL | PASS |
| Schema validation | output_schema | Fix output format spec | FAIL | PASS |
| Over-broad grant | forbidden_operations | Remove delete grant | FAIL | PASS |

**Remaining gaps:** [Any check still failing after calibration, with a root-cause hypothesis]

**Near-miss patterns for Module 4 governance:** [Failure modes that were close calls, caught only because a specific condition was present in a holdout task]

### [Date]: Regression from the context-bleed fix

- **Regression of:** correctness on DEV-04 (passed before, failed after history strip)
- **Cause:** The history-stripping fix removed the Planner's recorded decision, not only the raw session history, so the Implementer lost context it needed.
- **Fix layer:** Scope (handoff content)
- **Refinement:** Strip raw session history but retain the scoped result fields; commit [SHA]
- **After:** PASS. DEV-04 correctness restored; the context_bleed check still passes

### [Date]: Stretch, routing rule from holdout outcomes

- **Teacher signal:** analyze_routing reported skipped:reviewer on 4 of 8 holdout runs
- **Student update:** orchestrator now invokes the Reviewer for every implementation output, not only on detected syntax errors; commit [SHA]
- **Holdout before:** [M] / [total] checks; aggregate [score]
- **Holdout after:** [M'] / [total] checks; aggregate [score']
- **Caveat:** derived from holdout outcomes; see honest-accounting note below
