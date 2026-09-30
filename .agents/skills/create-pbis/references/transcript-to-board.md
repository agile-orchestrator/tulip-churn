# Turn a meeting transcript into backlog items

Read the meeting transcript in `$ARGUMENTS`, from the wiki when it is a page reference or from pasted text otherwise.

1. Extract decisions, requests, and open questions.
2. Check the existing board with `gh issue list` for duplicates or items to update.
3. Propose an epic, features, and PBIs using the conventions in `AGENTS.md` and the [Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready). Show the proposal as a table before creating anything.
4. After the user confirms, create the issues, link them as sub-issues, and add them to the project. Set Status to In refinement when they meet the entry bar in `AGENTS.md`; otherwise set Backlog with `needs-refinement`. List each created issue's number, title, and status.
5. If the source is a wiki page, propose updating its “Processed to backlog” field from “no” to “yes: #n, #m”. Edit and push the wiki only after the user agrees.
