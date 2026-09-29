---
description: Turn a meeting transcript (wiki page or pasted text) into backlog items
argument-hint: <wiki page name or url>
---
Read the meeting transcript: $ARGUMENTS (from the wiki if it is a page reference, or as pasted text).

1. Extract the decisions, requests and open questions.
2. Check the existing board (`gh issue list`) for duplicates or items to update.
3. Propose an epic and/or features and PBIs following the conventions in CLAUDE.md and the
   [Definition of Ready](https://github.com/agile-orchestrator/tulip-churn/wiki/Definition-of-Ready) on the wiki. Show me the proposal as a table before creating anything.
4. After I confirm, create the issues, link them as sub-issues, and add them to the project
   with Status In refinement if they meet the entry bar in `CLAUDE.md`, otherwise Backlog with
   `needs-refinement`. Then list the created issues (number, title, status) in your reply.
