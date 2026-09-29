# ✅ Definition of Ready

A backlog item may move to **Ready** on the board only when all of the following are true. The Product Owner has the final say.

## For every PBI

- [ ] Title is a short imperative sentence ("Make decision threshold configurable")
- [ ] Has a user story: *As a … I want … so that …*
- [ ] Has testable acceptance criteria, ideally Given / When / Then
- [ ] Estimated in story points (1, 2, 3, 5, 8). Anything above 8 must be split
- [ ] Linked to a parent feature (GitHub sub-issue) and labelled `pbi`
- [ ] Dependencies and open questions are listed, none blocking
- [ ] Priority set (P0–P3)

## For bugs

- [ ] Steps to reproduce, expected vs actual behaviour
- [ ] Severity set

## Extra for model or data changes

- [ ] The metric that should improve is named, with the current value
- [ ] Data needed is available at **scoring time** (no information from the future or from the target)
- [ ] Compliance impact considered (personal or sensitive data?)

## Entry bar for In refinement

An item may enter **In refinement** only when it has all of the following. Nothing is invented to meet it.

- [ ] Short imperative title
- [ ] User story (*As a … I want … so that …*)
- [ ] At least one testable acceptance criterion (Given / When / Then)
- [ ] A candidate parent feature, or a note that it is still to be decided
- [ ] Open questions listed

## Not ready signals

Items that miss the entry bar do not go to **In refinement**: the missing points are listed and the item needs more work first. It gets the `needs-refinement` label and stays in **Backlog**. Items in **In refinement** that fail the full checklist above keep the `needs-refinement` label until they are **Ready**.
