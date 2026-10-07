# Speaker notes: expanded presentation

One section per slide, in order. Each starts with the time to spend, then what to say, then the questions to expect.
The 12-minute hand-in deck is `../../Benchmark-Novelty-2-Confidence-Threshold Presentation/defense-slides.html`.

## 1. Cover
*Data Science for Conversational AI · Team project defense · expanded version*
**On the slide:** Reading, Not Asking

This is the long version, for preparation and for questions. The 8-slide version is the hand-in (the course allows at most 8).

Mapping to the 12-minute deck: slides 3-4 = its slide 2; slides 5-10 = its slide 3; slides 11-14 = its slide 4; slides 15-16 = its slide 5; slides 17-18 = its slide 6; slides 19-22 = its slide 7.

Open with the whole story in three sentences: I reproduced a benchmark paper on free resources. My first idea failed completely. My second idea finds a real signal inside the model, but it does not clearly beat the baseline, and I will say exactly what the numbers do and do not prove.

---

## 2. The story in one minute
*Overview*
**On the slide:** The whole story, before the details

About 1 minute. Click through the five rows. This is the map: tell the room what is coming so the details have somewhere to land.

Likely question: "What is your contribution?" Answer: a reproduction on free resources, one documented negative result, and a careful test of whether the model's internal signal can be used.

---

## 3. The problem
*The paper · 1 of 8 · the problem*
**On the slide:** Finding the right passage does not guarantee a good answer

About 1.5 minutes. The example is Figure 1 of the paper. One small change to the question and the passage turns an answerable question into one the model must refuse.

Define the two terms out loud: RAG, and selective refusal.

Likely question: "Why not just always answer?" Because a confident answer from a flawed passage can be wrong and harmful in high-stakes uses. The paper reports models "refusing over 60% of answerable queries" or "confidently answering despite critical information defects".

In the 12-minute deck this is slide 2.

---

## 4. Six reasons to refuse
*The paper · 2 of 8 · the six failure types*
**On the slide:** Six ways the evidence can be bad

About 1.5 minutes. These are the paper's six perturbation classes; the examples are the ones written in the benchmark's own prompt (our file src/prompt_builder.py, copied from the original repository).

The paper calls the last class "epistemic mismatch"; in the reply codes it is REFUSE_NONFACTUAL_QUERY.

Likely question: "How is contradiction different from ambiguity?" Contradiction: two statements cannot both be true. Ambiguity: one statement can be read two ways.

---

## 5. How the benchmark was built
*The paper · 3 of 8 · how the test set was made*
**On the slide:** The benchmark is generated: good evidence is broken on purpose

About 1.75 minutes. Walk the five boxes left to right.

Key idea in your own words: the test is made by changing a good example, so every example has a known correct reply. That is how refusals can be scored without guessing.

"Verify" is unanimous: a broken example is kept only if every model approves it. The paper says this filters out artifacts of one model.

Numbers: 176 levers, 93.1% human pass rate for the NQ set (expert, 180 examples), all from the paper.

Likely question: "Who wrote the examples?" Several strong LLMs. The data file records which one wrote each example (Claude, GPT, DeepSeek, Nova). We did not rerun that part; we used the released test set.

---

## 6. What is inside RefusalBench-NQ
*The paper · 4 of 8 · the data we used*
**On the slide:** RefusalBench-NQ: 1,600 examples from only 100 questions

About 1 minute. These counts are from the released dataset on Hugging Face (aashiqmuhamed/RefusalBench-NQ), checked by us: 536 answerable, 1,064 refusal-required.

The second card is the reason for our cross-fitting later (slide 18): if variants of the same question were in both training and test, a threshold or probe would look better than it is.

Likely question: "Why only 100 questions?" It is the paper's design: a small, clean base set where strong models already answer correctly, so a failure is caused by the break, not by a hard question.

---

## 7. Three kinds of models
*The paper · 5 of 8 · who does what*
**On the slide:** Three different models play three different roles

About 1.5 minutes. This answers the doctor-style question "what is the LLM, what is the benchmark, what is the judge".

Say: the benchmark is the exam paper, the builders wrote it, the target is the student, the judge is the grader. Click through the three cards.

Detail from the paper (Appendix E, Figure 3): models rate their own generations differently from peers; for example Nova Pro and GPT-4o passed 100% of their own, while peers passed 84% and 92%.

Likely question: "Why Gemini instead of Claude?" Cost: the course allows $20, and Gemini has a free tier. It is a documented deviation, and the judge has not yet been hand-checked. That is the main open limit.

---

## 8. What the judge decides
*The paper · 6 of 8 · the judge's job*
**On the slide:** The judge reads a reply and makes three decisions

About 1.5 minutes. Click through the steps.

The judge prompt is Appendix I.1.4 of the paper; our file src/judge.py uses it unchanged. The judge returns three lines: CLASSIFICATION, QUALITY_SCORE, EXPLANATION.

The second example matters: the model did refuse (so the decision to refuse was right) but gave the wrong reason. The paper calls these two skills detection and categorization.

Our shortcut: if a reply is exactly one clean refusal code, we score it by code and do not call the judge ("parse first"). Everything else goes to the judge.

Likely question: "How do you know the judge is right?" The paper's own check was on the benchmark, not on the judge. For our Gemini judge we have not yet done the planned 30-reply hand check. That is stated as a limit.

---

## 9. The measurements
*The paper · 7 of 8 · what is measured*
**On the slide:** Four rates, with one small worked example

About 1.5 minutes. The first four numbers are the paper's metrics (answer accuracy, refusal accuracy, false refusal rate, missed refusal rate). Balanced accuracy is our own summary; we added it because accuracy alone hides the imbalance (two thirds must be refused).

The numbers on this slide are invented to teach the definitions; they are not results.

Likely question: "Why not plain accuracy?" A model that always refuses would score 66% on plain accuracy but only 50% on balanced accuracy.

---

## 10. What the paper found
*The paper · 8 of 8 · its findings*
**On the slide:** Even the best models are far from good at this

About 1.25 minutes. All numbers are from the paper: 73.0% and 47.4% are in the introduction and Figure 5; 13.0% to 56.1% is the scaling section; "no model above 80% on both" is the Figure 5 caption. The Qwen-7B refusal accuracy of about 5% is read from a small plot, so say "about".

This is where the paper ends and our work begins: the paper measures; it does not propose a way to improve a model.

In the 12-minute deck this is part of slide 3.

---

## 11. The scenario we recreated
*Our baseline · 1 of 4 · the scenario*
**On the slide:** A small open model answering from one passage, on free hardware

About 1.5 minutes. This is the "scenario we recreated": a student-sized deployment of the paper's test. One model, one prompt (sent as a single user message, no system prompt, exactly as in the original code), temperature 1.0 as in the paper.

Why "parse first": it saves judge calls. A reply that is exactly one valid code needs no judge. Careful: a reply with no code is NOT assumed to be an answer, because a small model often refuses in plain words; those go to the judge.

Our data: of 1,560 replies, 528 (34%) were a clean code, 991 (64%) free text.

Likely question: "Why not judge everything like the paper?" Free-tier limit of 500 judge calls per day. Parse first cut the judge's workload by about a third.

---

## 12. How we ran it
*Our baseline · 2 of 4 · for readers who have not done this*
**On the slide:** How a 7B model runs on a free GPU

About 1 minute, no more. This is for classmates who have never run a model on a free GPU. Keep it short and plain.

Numbers: T4 = 15 GB; Qwen1.5-7B-Chat is about 15 GB in 16-bit; 4-bit (NF4) is about 5 GB. Generation is saved after every batch, so a disconnect loses at most one batch. 40 examples ran out of GPU memory in the first run and were set aside (2.5%).

Likely question: "Does 4-bit change the results?" It can, slightly. It is listed as a deviation from the paper; we did not test the effect.

---

## 13. The paper's setup versus ours
*Our baseline · 3 of 4 · every change, written down*
**On the slide:** What we kept and what we changed

About 1.25 minutes. This is the "code and reproduction" part of the rubric: be exact about what is the same and what is not.

Sources: the paper (Qwen served with vLLM on A100s, temperature 1.0, judge Claude-4-Sonnet) and our report. "Likely full precision" is our reading; the paper does not say it outright.

Likely question: "So is it a reproduction?" A close one, with documented deviations. The paper's finding (a 7B model almost never names the right reason) is reproduced; the exact numbers are not expected to match.

---

## 14. Our baseline results
*Our baseline · 4 of 4 · the numbers*
**On the slide:** Same story as the paper: the reason is almost never right

About 1.25 minutes. 770 graded replies: 509 that must be refused, 261 answerable. The grading order was a seeded random shuffle, and our comparison script checks the graded part is representative.

Likely question: "Why is your answer accuracy higher?" Different judge, 4-bit model, different software; I do not claim to beat the paper.

Likely question: "Is the baseline finished?" No: grading is limited to 500 judge calls per day on the free tier. The remaining replies are the next step, plus a 30-reply hand check of the judge.

In the 12-minute deck this is slide 4.

---

## 15. Extension 1: the idea
*Extension 1 · 1 of 2 · the limitation and the idea*
**On the slide:** The limitation: the baseline misses 46% of the refusals it should make

About 1.5 minutes. The control matters: without it, any gain could be blamed on formatting. A control is a version that changes only one thing so we can tell what caused a difference.

The 800 examples are a stratified subset (268 answerable, 532 must refuse) covering all 100 source questions; we compare on the 776 that also exist in the baseline.

Likely question: "Why did you expect this to work?" Because the paper says models are better at detecting than explaining; forcing the explanation first might help the decision. It was a hypothesis, and it failed.

---

## 16. Extension 1: the result
*Extension 1 · 2 of 2 · the result*
**On the slide:** Asking the model to diagnose first made it worse

About 1.75 minutes. Give the failure its full time: a clean negative result is worth marks for honesty and result quality.

Bars show, for each true failure type, how often the model wrote CLEAR. Orange bars are cases that should have been refused: 504 of 532 got CLEAR.

Table: 776 examples common to all three runs, counted by clean refusal codes only, so the baseline and control are lower bounds (free-text refusals are not counted). The gap to the diagnose-first run is still huge: 1.9% against 43.3%. The differences are significant (paired bootstrap over source questions).

Likely question: "Why did it fail?" I do not know. "Anchoring on clear" would be a guess, not a finding. This failure is what led to extension 2: if the model's written answer to "is the evidence clear" cannot be trusted, read what is inside it.

In the 12-minute deck this is slide 5.

---

## 17. Extension 2: the idea
*Extension 2 · 1 of 4 · the idea*
**On the slide:** Do not ask the model. Read it.

About 1.5 minutes. A probe is just a simple classifier (logistic regression) that looks at the model's internal numbers; "hidden state" means the numbers the model computes on the way to its answer. Higher score always means "refuse".

S1 also counts the wrapped forms the model sometimes uses (for example "**REFUSE..."), about 30% of its coded refusals.

S3 is trained with the benchmark's labels; S1 and S2 at their default thresholds use no labels. Say that out loud: it is why the probe is a diagnostic, not a fair like-for-like replacement for the baseline.

Likely question: "Where is your novelty?" Reading these signals for grounded refusal on this benchmark, with a small open model, tested against the paper's baseline, plus the honest report of the version that did not work.

In the 12-minute deck this is slide 6.

---

## 18. Extension 2: a fair test
*Extension 2 · 2 of 4 · how we kept the test honest*
**On the slide:** Variants of one question never sit on both sides of the test

About 1.5 minutes. This is the part a careful committee member will like, and a tired one will skip: slow down for the first picture.

Our unit test corrupts the labels of one group and checks that the threshold for that group does not change.

Honest limit to state if asked: the intervals resample the held-out predictions; the fitting is not repeated inside each resample, so they do not capture variability of the fitted threshold or probe.

The success rule was written down before the run: signal if the lower end of S1's AUROC interval is above 0.5; gain if the tuned threshold beats the default with its interval above zero.

In the 12-minute deck this is part of slide 6.

---

## 19. Extension 2: results
*Extension 2 · 3 of 4 · the numbers*
**On the slide:** The signal is real, but it does not clearly beat the baseline

About 2 minutes. This is the "result quality" part of the rubric: read the verdict out loud, do not oversell.

The signal column says all three readouts are above 0.5 (their 95% intervals start at 0.70 or higher). The last columns say what a rule would do in practice: thresholding S1 or S2 does not beat letting the model answer. The probe has the best number but its interval is -0.014 to +0.065.

The probe was trained with the benchmark's labels and the baseline was not, so even a clear win would need that caveat.

Earlier in the project we quoted "0.64 versus 0.72"; that used a baseline counted only by clean refusal codes, which understates it. The judged baseline is 0.690.

Hostile question: "Your baseline depends on an unvalidated Gemini judge for 64% of replies, while your rules are scored on labels." Answer: treat the comparison as provisional; I compare on the same 770 examples with question-clustered intervals, I claim no winner, and grading the rest plus the 30-reply judge check are the two next steps.

---

## 20. Extension 2: the trade-off picture
*Extension 2 · 3 of 4 · the same result as a picture*
**On the slide:** The baseline sits about where a simple threshold could put it

About 1.5 minutes. Same 770 examples for every line and for the diamond. Drawn by make_figures.py from the repository's own result files.

What it says in one sentence: the model's own free-text decisions already use about as much of the signal as a global threshold can; the probe's line is slightly lower, which is the small unclear gain in the table.

Likely question: "Why does a good AUROC not give a better decision?" AUROC measures ranking over every possible threshold; a deployed rule needs one operating point, and moving the threshold only slides along the line trading one error for the other.

In the 12-minute deck this is the chart on slide 7.

---

## 21. Extension 2: per failure type
*Extension 2 · 4 of 4 · where each readout helps*
**On the slide:** The probe finds more contradictions, and pays with false alarms

About 1.25 minutes. The overall balanced accuracy hides large trade-offs by type. Contradiction: the baseline misses 71%; the probe misses 19% and S2 23%, but they refuse more answerable questions (0.17 rises to 0.29 and 0.50). Ambiguity improves the same way. False premise is the exception: only the probe lowers false alarms (0.23 against 0.33), but it misses a few more (0.25 against 0.19).

Each cell has only 40 to 93 examples and one seed, so we do not test these differences; we describe them.

Possible next step, not tested: a different threshold per failure type.

---

## 22. Verdict and limits
*Conclusion*
**On the slide:** What we can say, what we cannot, and what a full run needs

About 1.5 minutes. End on the honest statement, then stop talking and invite questions.

"A full run" is the course's term: we ran a smaller-scale version because of the free resources; here is exactly what the full version needs. Cost stays near $0 on the free tiers; it is time (judge quota) that limits us, not money.

Related follow-up work to name if asked: Yin et al. (do models know what they do not know), R-Tuning (training a model to say "I don't know") and Self-RAG (a model that critiques its own retrieval). All three change the model by training; ours keeps the weights fixed and reads signals it already produces.

In the 12-minute deck this is the end of slide 7.

---

## 23. References
*References*

Leave this up during questions. The full list of 20 references is in the IEEE-format report.

---
