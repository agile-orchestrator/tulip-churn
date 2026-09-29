# 🎯 Q4 Goals with the PO

**Date:** 2026-09-15
**Type:** Stakeholder meeting
**Attendees:** Marieke De Vries (PO), Lotte Peeters (Data science), Youssef Amrani (ML engineering)

## Transcript

**Marieke:** Okay, thanks both. I want to use this half hour to agree what we commit to for Q4. Management wants to see the churn model used by real advisors before the end of the year, so the headline is a pilot with the Retention team in November.

**Youssef:** November is tight but doable if the scope is small. The API is merged, the container is in progress.

**Marieke:** Good. For the pilot I'd like to start with Germany only. That's where churn is highest and Tom's German team volunteered.

**Lotte:** Makes sense, German customers churn roughly twice as much as French ones in our data.

**Marieke:** Second thing. Tom doesn't want to call an API customer by customer. His team needs a list every Monday morning: the customers most at risk, ranked, so advisors can plan their week. Can we do that?

**Youssef:** Yes, that's a batch job, not the API. We score everyone on Sunday night and export the top N to a CSV or straight into the CRM. We said that in the ADR already.

**Marieke:** How big is N?

**Youssef:** That's a question for Tom, it depends on how many calls his team can make.

**Marieke:** Fine, I'll ask him Thursday. Third: advisors need to know *why* someone is on the list. "This customer has 78% risk" isn't enough to start a conversation. Something like the top three reasons.

**Lotte:** We can do that with SHAP values or at least with the feature contributions. It adds some work, maybe a sprint.

**Marieke:** It's a must for the pilot I think. Ana will ask for it too.

**Lotte:** By the way, good news on the model. After we added the CRM account-closure flag the AUC went to 1.0. Basically perfect.

**Marieke:** That's fantastic! Can we put that in the steering committee slides?

**Youssef:** Hmm, it's almost too good. I haven't looked at it closely yet though.

**Lotte:** The flag is very predictive, it makes sense that people who ask to close their account leave.

**Marieke:** Okay, let's go with it. Next, the model card. Ana won't sign off without it. Who owns it?

**Lotte:** Me, it's in Sprint 2. I haven't started though, the template in Notion is still empty.

**Youssef:** One more thing from my side: training only lives in Lotte's notebook. If Lotte is on holiday nobody can retrain. I'd like to move it into `train.py` before the pilot.

**Marieke:** Agreed, that's in Ready already, right?

**Youssef:** Yes.

**Marieke:** And the "Improve model" ticket, what is that?

**Lotte:** That was me months ago, it's just a placeholder. It needs to be split or closed.

**Marieke:** Let's refine it Wednesday. Okay, to sum up for Q4: pilot in Germany in November, weekly ranked list, reasons per customer, model card signed by Compliance, reproducible training. Thanks!

## Action items

- [ ] Marieke: ask Tom how many customers per week the team can handle
- [ ] Youssef: design the weekly batch scoring export
- [ ] Lotte: explanation of the top reasons per customer
- [ ] Lotte: model card draft before the Compliance review
- [ ] Team: refine "Improve model" on Wednesday
