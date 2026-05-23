#!/bin/bash
set -e

# Register MCP servers via Claude Code CLI
claude mcp add slack \
  node /usr/local/lib/node_modules/@modelcontextprotocol/server-slack/dist/index.js \
  -e SLACK_BOT_TOKEN="$SLACK_BOT_TOKEN" \
  -e SLACK_TEAM_ID="$SLACK_TEAM_ID"

claude mcp add gmail \
  node /usr/local/lib/node_modules/@gongrzhe/server-gmail-autoauth-mcp/build/index.js

exec "$@"
