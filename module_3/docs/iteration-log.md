# Iteration Log

This is the running record for orchestration behavior, failures, fixes, and verification.

## Run 0 - Tool-scope verification (pre-run check)

- Date: `[date]`
- Role tested: `implementer`
- Tool attempted: `mcp__coursetools__task_tracker`
- Expected: denied (`task_tracker` is owned by `project-manager`)
- Result: server returned an authorization error stating the `implementer` is not on the allow-list for `task_tracker`.
- Conclusion: the denial is enforced, not merely declared. The map's intent is confirmed in the running system.

## Run 1 - `[date]`

### Misfire 1: planner output not parseable by implementer

- What happened: the Planner returned its plan as a prose paragraph. The Implementer could not reliably extract the file list and modified a file the plan did not name.
- Roles involved: Planner (produced the output), Implementer (consumed it).
- Cause: neither the Planner definition nor the parent-to-subagent brief pinned a strict output format, so the plan's structure varied from run to run.
- Proposed fix: specify an exact output format in the Planner definition and in the handoff template's required-output-format field.

### Misfire 2: reviewer over-used codebase_search

- What happened: the Reviewer searched unrelated parts of the codebase, enlarging its context well beyond the changed files.
- Roles involved: Reviewer.
- Cause: `codebase_search` was granted to the Reviewer and invited scope creep.
- Proposed fix: remove `codebase_search` from the Reviewer if the next run shows the same pattern; have it rely on `file_read` of the modified files named in its handoff.

### Rerun (planner + implementer only) - `[date]`

- Result: the Planner returned a "Plan" section and a "Files to change" list in the required structure. The Implementer parsed the file list and modified the correct files. Fix holds.
- Watch for: no regression observed in the Reviewer or Tester phases.

## Run 2 - `[date]` - Stretch: isolate web_search in a Researcher role

- Change: removed `web_search` from the Implementer; added a Researcher role that owns `web_search`; updated the diagram, the map, and the orchestrator.
- Context measurement (Implementer role):
  - Before (`web_search` granted to Implementer): `<N1>` tokens
  - After (`web_search` isolated in Researcher): `<N2>` tokens
  - Reduction: `<N1 minus N2>` tokens
- Verification: in the rerun, the Implementer made no `web_search` calls and its context no longer lists the tool. When it needed a library detail it raised a blocker; the parent invoked the Researcher and relayed the findings back. Isolation holds.
