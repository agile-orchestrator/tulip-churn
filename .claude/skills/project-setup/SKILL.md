---
name: project-setup
description: Change how the Tulip Churn project is set up, such as board columns and fields, labels, the workflow skills and CLAUDE.md, and keep them consistent. Use when asked to add, rename or remove a board status or field, fix board items with missing fields, or change the scrum workflow or the rules for branches and pushing.
argument-hint: <setup change, e.g. "add an In refinement status">
---

Apply the setup change in `$ARGUMENTS` to the GitHub Project **Tulip Churn Board** (org
`agile-orchestrator`, project #1) and the repo, then keep everything that describes the
workflow consistent with it.

Current phase: **project setup**. Commit directly on `main` and push. Do not create
`chore/...` branches or PRs until the user says setup is over, then update this line.

## 1. Read the current state

Never assume the names of columns, fields or labels. Read them:

```bash
gh project view 1 --owner agile-orchestrator --format json --jq .id          # project id
gh project field-list 1 --owner agile-orchestrator --format json             # fields + option ids
gh label list -R agile-orchestrator/tulip-churn
# single-select options with color and description (needed to rewrite them)
gh api graphql -f query='{ node(id:"<field-id>"){ ... on ProjectV2SingleSelectField {
  options { id name color description } } } }'
```

## 2. Change a single-select field (Status, Priority)

`gh` cannot add an option. Use `updateProjectV2Field`, which **replaces the whole list**:

- Pass every existing option **with its `id`**, so items keep their value. An option sent
  without its `id` is recreated, and every item that had it loses its value.
- Keep existing names, colors and descriptions. A new option has no `id`. Its position in
  the list is its column order on the board.
- Take a snapshot before the change and diff it afterwards. Report any difference.

```bash
S=<scratchpad>
gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq '[.items[]|{n:.content.number,status}]' > $S/status_before.json
gh api graphql -f f=<field-id> -f query='mutation($f:ID!){ updateProjectV2Field(input:{
  fieldId:$f, singleSelectOptions:[
    {id:"<existing-id>", name:"Backlog", color:GRAY, description:"..."},
    {name:"<new option>", color:ORANGE, description:"..."},
    ... every other existing option with its id ...
  ]}){ projectV2Field{ ... on ProjectV2SingleSelectField { options{id name} } } } }'
gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq '[.items[]|{n:.content.number,status}]' | diff - $S/status_before.json
```

Removing or renaming an option affects items that use it. List those items and get the
user's OK first.

A new option usually shows up as a board column, but a saved view can hide it. Tell the user
to check the board view.

## 3. Fix board items

Find items with missing fields and set them. Look option ids up by name:

```bash
gh project item-list 1 --owner agile-orchestrator --format json -L 200 \
  --jq '.items[] | select(.status==null) | {n:.content.number, title:.content.title}'
gh project item-edit --project-id <project-id> --id <item-id> --field-id <field-id> \
  --single-select-option-id <option-id>
```

Only fill fields whose value is clear from the workflow, such as the default status. Ask the
user for estimates and priorities instead of guessing them.

## 4. Update everything that describes the workflow

After a setup change, search for the old names and defaults and update each match:

```bash
grep -rn "<old name or default>" CLAUDE.md .claude/ .github/
```

- `CLAUDE.md`: board columns, defaults, and the rules for writing PBIs
- `.claude/skills/*/SKILL.md`, such as `create-pbi`, which sets the default Status
- `.claude/commands/*.md`, such as `transcript-to-board` and `refine-pbi`
- `.github/ISSUE_TEMPLATE/`, for labels and type
- Notion DoR and DoD pages, if the change affects them. Propose the edit and do not change
  Notion without the user's OK.

Skills should look up option ids by name at run time, not hard-code them.

## 5. Commit and report

Use a Conventional Commit (`chore:`), then push as described in "Current phase" above.
Report:

- what changed on the board
- the result of the snapshot diff
- which files changed
- anything left for the user: the board view, fields that need their input, and any Notion
  edits
