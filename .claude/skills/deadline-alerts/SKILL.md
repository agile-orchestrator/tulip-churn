---
name: deadline-alerts
description: Scan the PO's Gmail for emails that ask for something by a date, log them in the Slack List "PO deadline log" and post an alert with a ready-to-paste /create-pbi instruction to #po-deadlines. Used by the daily scheduled routine of issue #29; can also be run by hand.
---

# Daily deadline alerts (PO mailbox → Slack)

Run by the scheduled Claude Code routine of issue #29, or by hand with `/deadline-alerts`.
It runs on the PO's account (Gmail `cedric.sema.gpt@gmail.com`, Slack workspace
AgileOrchestrators) on weekdays at 08:30 Europe/Paris. It only reads email and writes to Slack; it never creates GitHub issues and
never replies to or changes an email beyond adding the scan label.

## Where things live

| What | Where |
|---|---|
| Alerts | private Slack channel `#po-deadlines` (`C0C5DEPA3A8`) |
| Memory of deadline emails and the actions taken | Slack List **PO deadline log** (`F0C5BPTGJ9X`) |
| Which emails were already scanned | Gmail label `claude/deadline-scanned` |

The memory stays in the PO's own Gmail and Slack, not in this repo: no email metadata is
committed.

## Steps

1. **Find new emails.** Search Gmail with
   `in:inbox -label:claude/deadline-scanned -in:sent newer_than:14d`.
   `newer_than:14d` only bounds the first run; the label is what makes runs idempotent.
2. **Decide for each email whether it is a deadline email:** it asks the team or the PO to
   deliver or decide something by a stated date or time, explicit ("by 15 October") or relative
   ("by Friday", "end of next week"). Meeting invites, calendar notifications, newsletters,
   automated notifications and marketing do not count. Read the body only to decide this.
   Convert a relative date to an absolute date from the email's sent date.
3. **Skip duplicates.** Read the PO deadline log. If a row already has this Gmail id, do
   nothing more for this email except step 6.
4. **Log it.** Add a row to the PO deadline log:
   Subject, Sender, Gmail id, Received (sent date), Deadline (absolute date), Ask (one line,
   your own words), Status `New`.
5. **Alert.** Post one message to `#po-deadlines`:

   ```
   📬 *Deadline <YYYY-MM-DD>* — <one-line ask>
   From: <sender> · Subject: "<subject>"

   Turn it into a PBI (paste in Claude Code, in the tulip-churn repo):
   `/create-pbi <one-line ask>, due <YYYY-MM-DD>. Source: email from <sender>, "<subject>" (Gmail id <id>). Afterwards set PO deadline log record <record id> to "PBI created" with the issue link.`
   Not a PBI? Tell Claude: `Set PO deadline log record <record id> to "Ignored" (or "Handled outside board") with a note.`
   ```

   Then write the message link into the row's **Alert link**.
6. **Mark scanned.** Add the label `claude/deadline-scanned` to every email processed in this
   run, deadline or not.

If there are no deadline emails, post nothing.

## Privacy

Only sender, subject, deadline and a one-line summary in your own words go to Slack and the
list. Never copy email body text.
