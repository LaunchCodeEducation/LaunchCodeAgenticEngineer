# Routing and Tool Grant Map

| Role | Route condition | Storage operations | Retrieval | Notes |
|---|---|---|---|---|
| orchestrator | Parent workflow coordination | write_entry, read_entry, list_entries, update_entry, delete_entry, audit_read | retrieve, ceiling confidential | Coordinates and audits the run. |
| implementer | Code and implementation tasks | write_entry, read_entry, list_entries, update_entry | retrieve, ceiling internal | No delete access. |
| reviewer | Code review tasks | read_entry, list_entries | retrieve, ceiling internal | Advisory only. |
| tester | Test execution/reporting | read_entry, list_entries | retrieve, ceiling internal | Workspace remains read-only. |
| project-manager | PR description and summaries | read_entry, list_entries | denied | Owns draft-pr-description. |

## Converted steps

- validator: converted to deterministic code (ADR-001). No MCP access required.
- routing: sample deterministic router included as a second decision-history example (ADR-002).
