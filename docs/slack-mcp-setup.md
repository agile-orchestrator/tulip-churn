# Slack bot MCP server

Claude Code can post to Slack as **Tulip Churn Bot** through the `slack` server in `.mcp.json`
(added in #52, tracked in #53). This is optional: the personal `claude.ai Slack` connector that
`/setup` checks still works on its own. Use the bot when a message should come from the team
app rather than from you.

## How it is configured

`.mcp.json` (committed, no secrets):

```json
{
  "mcpServers": {
    "slack": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-slack"],
      "env": {
        "SLACK_BOT_TOKEN": "${SLACK_BOT_TOKEN}",
        "SLACK_TEAM_ID": "T0C57PPA44S"
      }
    }
  }
}
```

- The team ID only identifies the AgileOrchestrators workspace and is safe to commit.
- The bot token (`xoxb-…`) is a shared secret. It lives in `.env` (gitignored) and is never
  committed, pasted into a chat with Claude or posted in Slack.

The Slack app lives at https://api.slack.com/apps. Its bot token scopes are:

| Scope | Used for |
|---|---|
| `channels:read` | listing channels |
| `chat:write` | posting to channels and DMs |
| `users:read` | looking up user IDs for DMs and @mentions |

## Setting it up

1. Accept the invite to the AgileOrchestrators workspace (ask the PO if you have none).
2. Get the bot token from the PO and add it to `.env` in the repo root:
   ```
   SLACK_BOT_TOKEN=xoxb-…
   ```
3. Start Claude Code with the variable exported. Claude Code does **not** read `.env` itself:
   ```bash
   set -a; source .env; set +a
   claude
   ```
4. Run `/mcp` and check that `slack` shows `✔ Connected`, then ask Claude to list the Slack
   channels. `/setup` runs the same check.

## Channels

The bot only reads and posts in public channels it has been invited to. It is a member of
#tulip-churn and #tasks. To add it to another channel, run this in that channel:

```
/invite @Tulip Churn Bot
```

DMs to workspace members work without an invite.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| Every Slack call returns `invalid_auth` | `SLACK_BOT_TOKEN` was empty when Claude Code started. Export `.env` (step 3) and restart. |
| `not_in_channel` or `channel_not_found` when posting | The bot is not in that channel. `/invite @Tulip Churn Bot` there. |
| `missing_scope` | The app lacks a scope for that call. The workspace admin adds it under **OAuth & Permissions** and reinstalls the app; if the token changes, update `.env`. |
| No `slack` line in `/mcp` | The project server was not approved. Restart Claude Code and accept the `.mcp.json` servers prompt. |
