# Routing-and-Tool-Grant Map - CSV Export Workflow

This map uses the plain course tool names from the design sections. The agent definitions in `.agents/` use the corresponding MCP identifiers from Section 4.

| Role | Receives from parent | Produces | Tools granted | Tools denied (reason) | Context isolation reason | Autonomy |
|---|---|---|---|---|---|---|
| `planner` | Feature request and repo path | Numbered plan and file list | `file-read`, `codebase-search` | `file-write` (writes no code); `shell` (runs nothing); `test-runner` (does not test); `task-tracker` (Project Manager owns it); `web-search` (Researcher owns it / not needed for planning) | Planning reads code but never changes it; withholding write and execute tools keeps context lean and blast radius at zero. | High (plans are cheap to correct) |
| `implementer` | Plan and file list | Modified files | `file-read`, `file-write`, `codebase-search` | `shell` (no need to run arbitrary commands); `test-runner` (Tester owns it); `task-tracker` (Project Manager owns it); `web-search` (Researcher owns it) | Needs read and write access to make changes; keeping the test runner out means it cannot grade its own work, and keeping the ticket and web tools out means it cannot move tickets or wander the web on its own. | Medium (writes files; should pause before anything irreversible) |
| `reviewer` | Modified files | Review report | `file-read`, `codebase-search` | `file-write` (proposes, never edits); `shell` (runs nothing); `test-runner` (Tester owns it); `task-tracker` (Project Manager owns it); `web-search` (not a review tool) | Read-only by design; with no write or execute tools it can only propose changes, never make them, so its blast radius is zero even at high autonomy. | High (read-only; proposes, never changes) |
| `tester` | Modified files | Pass or fail report | `file-read`, `test-runner` | `file-write` (must not "fix" code and mask failures); `codebase-search` (not needed to run tests); `shell` (test runner covers the real need); `task-tracker` (Project Manager owns it); `web-search` (not needed) | Owns test execution and nothing else; lacking file-write means it cannot quietly edit code to make a failing test pass. | Medium (executes code, but bounded to the test runner) |
| `project-manager` | Parent's run summary | Ticket-update confirmation | `task-tracker` | `file-read`, `file-write`, `codebase-search`, `shell`, `test-runner`, `web-search` (none are needed to update a ticket) | Sole owner of the ticket tool; because no coding role carries it, the ticket tool's description never enters the Planner's, Implementer's, Reviewer's, or Tester's context. | Medium (changes a shared record; only after the parent confirms the work is done) |
| `researcher` | One research question from a role's blocker | Findings document: answer, key facts, and sources | `web-search` | All other tools (does no code, test, or ticket work) | Sole owner of web-search; isolating it keeps the external-search tool out of the Implementer's context and action space. | Medium (external-facing, but read-only) |

## Tool tally review

- `file-read` appears on four roles (`planner`, `implementer`, `reviewer`, `tester`). Verdict: acceptable, because it is a generic read-only primitive.
- `codebase-search` appears on three roles (`planner`, `implementer`, `reviewer`). Verdict: acceptable, but watch for over-use during runs.
- `file-write` appears on one role (`implementer`) plus the parent orchestrator for handoff/result documents only.
- `test-runner` appears on one role (`tester`).
- `task-tracker` appears on one role (`project-manager`).
- `web-search` appears on one role (`researcher`).
- `shell` appears on no roles.

## Alternatives considered

- Giving the Reviewer the `test-runner` so it could verify its own suggestions. Ruled out: the Tester role owns test execution. A Reviewer that can also run tests blurs the role boundary and creates ambiguous ownership when a test fails, since two roles could each claim or disclaim responsibility.
- Giving the Implementer the `task-tracker` so it could update ticket status as it works. Ruled out: task tracking belongs to the Project Manager. Granting it here would put the ticket tool's description into the Implementer's context for no benefit and would let the Implementer move tickets on its own, outside its actual job.
- Giving the Implementer the `web-search` tool for library documentation. Ruled out: web search belongs to the Researcher. The Implementer should raise a research blocker; the parent routes the single question to the Researcher and relays the findings back.
