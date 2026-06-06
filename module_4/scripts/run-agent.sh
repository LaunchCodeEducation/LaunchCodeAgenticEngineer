#!/usr/bin/env bash
# run-agent.sh: launch a subagent container with only the permissions its
# governance policy allows. Pass the role name as the first argument.
set -euo pipefail

ROLE="${1:?Usage: run-agent.sh <role-name> [command]}"
shift

IMAGE="${AGENT_IMAGE:-launchcode-agentic:module4}"
WORKSPACE_MODE="ro"
MOUNT_MEMORY=0

case "$ROLE" in
  implementer|orchestrator)
    WORKSPACE_MODE="rw"
    MOUNT_MEMORY=1
    ;;
  reviewer|tester|project-manager)
    WORKSPACE_MODE="ro"
    MOUNT_MEMORY=0
    ;;
  *)
    echo "Unknown role: $ROLE" >&2
    echo "This role has no policy entry, so it cannot be launched." >&2
    exit 1
    ;;
esac

ARGS=( run --rm -it )
ARGS+=( --network agent-internal )
mkdir -p logs
ARGS+=( -v "$(pwd):/workspace:${WORKSPACE_MODE}" )
ARGS+=( -v "$(pwd)/logs:/logs:rw" )
ARGS+=( -e "STORAGE_AUDIT_LOG=/logs/storage-audit-log.jsonl" )
ARGS+=( -e "RETRIEVAL_AUDIT_LOG=/logs/retrieval-audit-log.jsonl" )
if [ "$MOUNT_MEMORY" -eq 1 ]; then
  ARGS+=( -v agent-memory:/memory )
fi
ARGS+=( -e "AGENT_ROLE=${ROLE}" )
ARGS+=( "$IMAGE" "$@" )

MEMORY_STATE=$([ "$MOUNT_MEMORY" -eq 1 ] && echo mounted || echo omitted)
echo "Launching '$ROLE': workspace=${WORKSPACE_MODE}, memory=${MEMORY_STATE}"
exec docker "${ARGS[@]}"
