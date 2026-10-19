#!/usr/bin/env bash
# PreToolUse hook: run the slopguard checks before Claude runs `git commit`.
# The Stop hook only checks uncommitted files, so work committed within a turn skipped it.
# Exit 2 blocks the commit and shows the findings to Claude.
payload=$(cat)
command=$(jq -r '.tool_input.command // ""' <<<"$payload")
if ! grep -Eq '(^|[;&|[:space:]])git([[:space:]]+-[cC][[:space:]]+[^[:space:]]+)*[[:space:]]+commit' <<<"$command"; then
  exit 0
fi
# Drop stop_hook_active so a second attempt is checked again instead of let through.
jq 'del(.stop_hook_active)' <<<"$payload" | uv run slopguard hook stop
