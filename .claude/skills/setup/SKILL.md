---
name: setup
description: Take a newcomer who has Claude Code and a clone of this repo to a working environment. Checks gh, uv, GitHub login and project access, uv sync and the connectors the team uses (GitHub, Gmail, Slack), fixes what it safely can and says exactly what the user still has to do. Safe to run again at any time. Use when asked to set up, onboard or check the dev environment.
---

# Set up the tulip-churn environment

Run every check below, in order, and end with the report table. The skill is idempotent: when
everything is in place it changes nothing and reports all checks green.

Rules:

- **Never ask for, type, print or store a token, password or secret.** Logins and OAuth flows
  are done by the user. Ask them to run the command themselves with the `!` prefix (for
  example `! gh auth login`) so the output lands in this session, then check again.
- Only fix things that need no login and no admin rights (for now only `uv sync`). For
  anything else give the exact command or steps, and do not run installers with `sudo` or
  `curl | sh` yourself.
- Do not depend on Notion: documentation is moving to the GitHub Wiki (#24).
- A failed check does not stop the run. Carry on and report everything at the end.

## 1. Tools

| Check | Command | If missing, tell the user to run |
|---|---|---|
| GitHub CLI | `gh --version` | macOS `brew install gh`; Debian/Ubuntu `sudo apt install gh`; Windows `winget install --id GitHub.cli`; others https://github.com/cli/cli#installation |
| uv | `uv --version` | macOS/Linux `curl -LsSf https://astral.sh/uv/install.sh \| sh`; Windows `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 \| iex"` |

Pick the command for the user's OS (`uname -s`, and `/etc/os-release` on Linux). After an
install, the user may need to open a new shell before the tool is on `PATH`.

## 2. GitHub login and project access

```bash
gh auth status 2>&1 | grep -v -i token          # never echo the token line
gh auth status 2>&1 | grep -i "token scopes"    # scopes only, the token itself is masked
gh repo view agile-orchestrator/tulip-churn --json name --jq .name
gh project view 1 --owner agile-orchestrator --format json --jq .title
```

| Result | What to tell the user |
|---|---|
| Not logged in | `! gh auth login -s project` (choose GitHub.com, then browser login) |
| Logged in, `project` missing from the scopes | `! gh auth refresh -s project` |
| Repo not found or 404 | ask an org owner to add their GitHub account to `agile-orchestrator` with access to `tulip-churn` |
| Project fails ("Could not resolve to a ProjectV2") with the `project` scope present | ask an org owner to give them access to the project **Tulip Churn Board** |

The project check passes when it prints `Tulip Churn Board`.

## 3. Python environment

```bash
uv sync
uv run python -c "import tulip_churn"
```

Run `uv sync` yourself: it only installs into `.venv/` and changes nothing when everything is
already installed. If it fails, show the error and stop this step.

## 4. Connectors

The team works with three services. Check what this Claude Code session can reach:

```bash
claude mcp list
```

| Service | Used for | Connected when |
|---|---|---|
| GitHub | board, issues, PRs | step 2 passed (the team uses the `gh` CLI, not an MCP connector) |
| Gmail | the PO's daily deadline alerts (`/deadline-alerts`) | a `claude.ai Gmail` line shows `✔ Connected` |
| Slack | alerts in `#po-deadlines`, team chat (workspace AgileOrchestrators) | a `claude.ai Slack` line shows `✔ Connected` |

Also list every server in `.mcp.json` with its status from `claude mcp list`, so this report
stays in sync with the repo config. Report `notion` as optional (docs are moving to the
GitHub Wiki); it only needs the user to run `/mcp` and log in if they still read the Notion
docs.

For a missing Gmail or Slack connector, give these steps:

1. Open https://claude.ai/customize/connectors with the same account Claude Code is logged in
   with (`/status` shows it).
2. Click **Connect** on Gmail or Slack and complete the sign-in in the browser. For Gmail use
   the company mailbox; for Slack first accept the invite to the AgileOrchestrators workspace
   (ask the PO if there is none in the mailbox).
3. Restart Claude Code, then run `/setup` again.

Gmail is only needed by the PO. For anyone else, report a missing Gmail as "not needed unless
you run the deadline alerts", not as a failure.

## 5. Report

End with one table, one row per check, and nothing else changed:

| Check | Status | Action |
|---|---|---|
| gh | ✅ 2.x | — |
| uv | ✅ 0.x | — |
| GitHub login | ✅ `<account>`, scope `project` | — |
| Repo access | ✅ | — |
| Project access | ✅ Tulip Churn Board | — |
| uv sync | ✅ | — |
| Gmail | ❌ | steps above |
| Slack | ✅ | — |
| notion (`.mcp.json`, optional) | ⚠️ needs authentication | `/mcp` if you use the Notion docs |

Then one line: "All set" when every required check is ✅, otherwise the number of open
actions and the first one to do. Point the user to `README.md` (Quickstart) and `CLAUDE.md`
(ways of working) as next reads.
