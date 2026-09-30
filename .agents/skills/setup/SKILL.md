---
name: setup
description: Take a newcomer who has Claude Code and a clone of this repo to a working environment. Checks gh, uv, GitHub login and project access, uv sync, the local clone of the GitHub Wiki and the connectors the team uses (GitHub, Slack, optionally Miro and Gmail), fixes what it safely can and says exactly what the user still has to do. Safe to run again at any time. Use when asked to set up, onboard or check the dev environment.
---

# Set up the tulip-churn environment

Run every check below, in order, and end with the report table. The skill is idempotent: when
everything is in place it changes nothing and reports all checks green.

Rules:

- **Never ask for, type, print or store a token, password or secret.** Logins and OAuth flows
  are done by the user. Ask them to run the command themselves with the `!` prefix (for
  example `! gh auth login`) so the output lands in this session, then check again.
- Only fix things that need no login and no admin rights (`uv sync` and the wiki clone). For
  anything else give the exact command or steps, and do not run installers with `sudo` or
  `curl | sh` yourself.
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
gh auth status 2>&1 | grep -iE "logged in|token scopes"   # account and scopes lines only
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

## 4. Wiki clone

The docs (Definition of Ready, Definition of Done, ADRs, meeting notes) are in the GitHub Wiki,
a separate git repo. It is cloned next to this repo, never inside it:

```bash
if [ -d ../tulip-churn.wiki/.git ]; then
  git -C ../tulip-churn.wiki pull --ff-only
else
  git clone https://github.com/agile-orchestrator/tulip-churn.wiki.git ../tulip-churn.wiki
fi
ls ../tulip-churn.wiki/Definition-of-Ready.md
gh auth setup-git   # lets `git push` on the HTTPS wiki clone use the gh login
```

Run it yourself. The check passes when `Definition-of-Ready.md` exists. If the pull fails
because of local changes in the wiki clone, do not touch them: report it and let the user
commit or discard them.

## 5. Connectors

Check what this Claude Code session can reach:

```bash
claude mcp list
```

| Service | Used for | Connected when |
|---|---|---|
| GitHub | board, issues, PRs | step 2 passed (the team uses the `gh` CLI, not an MCP connector) |
| Slack | team chat (workspace AgileOrchestrators) | a `claude.ai Slack` line shows `✔ Connected` |
| Miro (optional) | retro boards (`sprint-retrospective` skill) | a `claude.ai Miro` line shows `✔ Connected` |
| Gmail (optional) | the PO's personal tools only | a `claude.ai Gmail` line shows `✔ Connected` |

Also list every server in `.mcp.json` with its status from `claude mcp list`, so this report
stays in sync with the repo config.

Notion is no longer needed: the docs moved to the GitHub Wiki (#24), which step 4 clones. Do
not report a missing Notion connector.

For a missing Gmail, Slack or Miro connector, give these steps:

1. Open https://claude.ai/customize/connectors with the same account Claude Code is logged in
   with (`/status` shows it).
2. Click **Connect** on Gmail, Slack or Miro and complete the sign-in in the browser. For Gmail use
   the company mailbox; for Slack first accept the invite to the AgileOrchestrators workspace
   (ask the PO if there is none in the mailbox).
3. Restart Claude Code, then run `/setup` again.

A connector that is listed but needs authentication is fixed in this session: run `/mcp`,
select it (for example **claude.ai Miro**) and log in in the browser.

Gmail is only needed by the PO, and Miro only by whoever prepares the retro. For anyone else,
report a missing Gmail or Miro as "not needed", not as a failure.

## 6. Report

End with one table, one row per check, and nothing else changed:

| Check | Status | Action |
|---|---|---|
| gh | ✅ 2.x | — |
| uv | ✅ 0.x | — |
| GitHub login | ✅ `<account>`, scope `project` | — |
| Repo access | ✅ | — |
| Project access | ✅ Tulip Churn Board | — |
| uv sync | ✅ | — |
| Wiki clone | ✅ `../tulip-churn.wiki` | — |
| Slack | ✅ | — |
| Miro (optional) | ✅ | — |
| Gmail (optional) | — not needed | — |

Then one line: "All set" when every required check is ✅, otherwise the number of open
actions and the first one to do. Point the user to `README.md` (Quickstart) and `CLAUDE.md`
(ways of working) as next reads.
