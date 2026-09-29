# 📞 Retention Team Request

**Date:** 2026-09-18
**Type:** Stakeholder meeting
**Attendees:** Tom Verhoeven (Retention lead), Marieke De Vries (PO), Ana Costa (Compliance)

## Transcript

**Marieke:** Tom, thanks for making time. We want to make sure what we build for the pilot actually works for your advisors. Ana joined because some of this touches Compliance.

**Tom:** Sure. So, the basics: I have twelve advisors in the German team, each can do around forty proactive calls a week on top of the inbound work. So roughly five hundred customers a week, max.

**Marieke:** So a weekly list of the top five hundred?

**Tom:** Top five hundred, but per advisor region if possible, and I want to be able to change that number. Some weeks we have campaigns and capacity drops to half.

**Marieke:** Okay. And the API that Youssef built, would you use it?

**Tom:** Yes, in the CRM customer screen. But there's a problem. Right now it says "at risk" when the score is above 50%. That's arbitrary. My people tried it last week and almost nobody was flagged. I need to be able to tune that threshold myself, or at least have the team change it without a new release.

**Marieke:** Noted, configurable threshold.

**Tom:** Also, something weird. We tested the demo with a customer we know is about to leave: 62 years old, German, three products, not active for months. The tool said 0% risk. Zero. That doesn't feel right.

**Marieke:** Hm. I'll pass that to Lotte and Youssef.

**Tom:** Third thing: we must not call people we already called in the last thirty days. Customers hate that. So the list has to exclude recent contacts. We have that in the CRM contact history.

**Ana:** Can I add the Compliance side? Three points. One, logging: I know you're adding audit logs, good, but I don't want names or customer IDs in plain text in the logs. Pseudonymise them.

**Marieke:** Okay.

**Ana:** Two, you use gender and age as inputs. That's not forbidden, but I need a justification and I need to see that the model doesn't perform much worse for one group. That goes in the model card.

**Marieke:** The model card is on the board for this sprint.

**Ana:** Three, if a customer asks why they were contacted, we must be able to explain it. So the reasons per customer are not a nice-to-have for me, they're a requirement.

**Tom:** Same for my advisors, they need something to open the conversation with.

**Marieke:** Clear. So, summarising: weekly list with adjustable size, per region, excluding contacts from the last thirty days; configurable threshold; reasons per customer; pseudonymised logs; fairness analysis in the model card. And Tom's weird zero percent case.

**Tom:** That's it. When can we have the first list?

**Marieke:** I'll come back to you after sprint planning.

## Action items

- [ ] Marieke: turn the requests into backlog items before sprint 3 planning
- [ ] Marieke: forward the 0% risk example to the data team
- [ ] Tom: share CRM contact-history export format
- [ ] Ana: send the fairness checklist for the model card
