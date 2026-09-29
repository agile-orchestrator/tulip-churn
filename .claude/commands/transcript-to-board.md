---
description: Turn a meeting transcript (Notion page or pasted text) into backlog items
argument-hint: <notion page title or url>
---
Read the meeting transcript: $ARGUMENTS (fetch it from Notion if it is a page reference).

1. Extract the decisions, requests and open questions.
2. Check the existing board (`gh issue list`) for duplicates or items to update.
3. Propose an epic and/or features and PBIs following the conventions in CLAUDE.md and the
   Definition of Ready in Notion. Show me the proposal as a table before creating anything.
4. After I confirm, create the issues, link them as sub-issues, add them to the project
   with Status In refinement if they meet the entry bar in `CLAUDE.md`, otherwise Backlog with
   `needs-refinement`, and add a comment on the Notion page listing the created issues.
