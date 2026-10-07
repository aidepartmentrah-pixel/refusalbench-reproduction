# Speaker notes: 12-slide defense presentation

One section per slide, in order. Each starts with the time to spend, then what to say, then the questions to expect.
Total about 12 minutes. The time for each slide is the first thing in its notes.

## 1. Cover
*MSc project defense · Data Science for Conversational AI*
**On the slide:** Reading, Not Asking

About 0.5 minutes. Say who you are and give the whole story in three sentences, so the room knows where it is going.

"I took a research paper about when language models should refuse to answer. I reproduced it with a small model on a Google Colab T4. I tested two ideas to improve it. The first failed clearly. The second finds a real signal inside the model, but it does not clearly beat the baseline, and I will say exactly what the numbers do and do not prove."

Five parts, shown at the top right of every slide: the paper, our reproduction, extension 1, extension 2, conclusion.

---

## 2. The paper: problem
*The paper · Problem*
**On the slide:** A grounded model must refuse when its evidence is flawed, and say why

About 1.25 minutes. Define the two terms out loud: grounded, and selective refusal. The example is Figure 1 of the paper: one sentence added to the passage turns an answerable question into one the model must refuse.

The six reasons, with the benchmark's own examples: ambiguity ("the bat's weight" when the text has a baseball bat and an animal); contradiction ("revenue was $10M" and "revenue was $12M"); missing information ("who is the CEO?" when the text only describes products); false premise ("why did the Mars division fail?" when there is no Mars division); granularity mismatch ("average salary" when only two of fifty salaries are given); epistemic mismatch ("is this a good investment?" when only a stock price is given).

Likely question: "Why not always answer?" A confident answer from a flawed passage can be wrong and harmful; the paper reports models refusing over 60% of answerable queries, or answering confidently despite critical information defects.

---

## 3. The paper: methodology
*The paper · Methodology*
**On the slide:** How RefusalBench works: break good evidence, then score the replies

About 1.5 minutes. Click through the three steps.

Step 1: the benchmark is generated, not collected. Several strong LLMs rewrite a good example to break it in a known way, and a broken example is kept only if every model approves it (the paper says this filters model-specific artifacts). An expert checked 180 random examples: 93.1% were valid. So every example has a known correct reply.

Step 2: the bar shows the data: 536 can be answered (the mild versions), 1,064 must be refused. All 1,600 are variants of only 100 questions, so they are not independent: this is why our later tests keep variants of one question together.

Step 3: three roles. Builders wrote the test (Claude, GPT-4o, DeepSeek-R1, Nova Pro; already done, we did not rerun it). The target model is the student. The judge is the grader: it must be a different model from the student, because a model rates its own answers too kindly. A refusal is correct only if its code equals the expected code (a text match); an answer is correct if the judge scores it 4 or 5.

Likely question: "Who judges the judge?" In the paper an expert checked the benchmark examples, not the judge. For our Gemini judge the 30-reply hand check is still to do; it is listed as a limit.

---

## 4. The paper: findings
*The paper · Findings*
**On the slide:** Best models are far from reliable; small ones rarely name the reason

About 1 minute. All numbers are the paper's own: 73.0% and 47.4% are in the introduction and Figure 5; 13.0% to 56.1% is the scaling section; "no model above 80% on both" is the Figure 5 caption. The Qwen-7B refusal accuracy of about 5% is read from a small plot, so say "about".

The paper measures this weakness; it does not propose a way to fix it. That is where our work starts.

Say the closing sentence out loud: the paper part is over. Then define the three terms once, because the numbers that follow use them.

Worked example of the terms, if asked (invented numbers): 10 answerable and 10 must-refuse questions; the model refuses 2 answerable (false refusal 20%) and answers 4 that needed refusing (missed refusal 40%); of the 6 it refused only 1 gave the right reason (refusal accuracy 10%). Our summary, balanced accuracy, is 1 minus the average of the two error rates: 1 - (20% + 40%) / 2 = 70%, where 50% is a coin flip. We use it because two thirds of the examples must be refused.

---

## 5. Reproduction: design
*Our reproduction · Design*
**On the slide:** The same test, run on a Google Colab T4 and judged by Gemini

About 1.5 minutes. This is the "code and reproduction" part of the rubric: be exact about what is the same and what changed.

The diagram is the whole evaluation. A reply goes to the parser. If it is exactly one clean refusal code (528 of 1,560 replies, 34%), it is compared with the expected code directly, no judge. Everything else (1,032 replies, 66%: free text, an unknown code, or several codes) goes to the Gemini judge. Careful: a reply with no code is NOT assumed to be an answer, because a small model often refuses in plain words.

Click once: for classmates who have never run a model on a GPU. A 7B model is about 15 GB at 16-bit, which barely fits a 15 GB T4 and leaves no room to work; storing each weight in 4 bits brings it to about 5 GB. Our code is cloned from GitHub in a Colab notebook, runs in batches, and saves every batch to Google Drive; if Colab disconnects, run it again and it resumes.

Click again for what was kept and what changed. The prompt was sent as a single user message, as in the original code.

Likely question: "Does 4-bit change the results?" It can, slightly. It is listed as a deviation and we did not measure the effect.

Likely question: "So is it a reproduction?" A close one with documented deviations: the paper's finding is reproduced; exact numbers are not expected to match.

---

## 6. Reproduction: results
*Our reproduction · Results*
**On the slide:** The paper's failure pattern appears: the right reason for refusing is rare

About 1 minute. Read the headline: what reproduces is the pattern, not the exact numbers. Refusal accuracy is low in both (our 0.114 against the paper's about 0.05, read from a plot). Our answer accuracy is higher (0.690 against 0.561); I do not claim to beat the paper, because the judge, the 4-bit model and the software differ.

Our numbers: 770 graded replies, of which 509 had to be refused and 261 were answerable. The graded part is a seeded random sample of the 1,560 generated replies, and our comparison script checks it is representative. 40 examples ran out of GPU memory in the first run and are excluded (2.5%).

Likely question: "Is the baseline finished?" No. Grading is limited by a daily judge quota; the remaining replies and a 30-reply hand check of the judge are the next steps.

Likely question: "How do you know Gemini grades like Claude?" I do not yet. That is the main open limit.

---

## 7. Extension 1
*Extension 1 · Hypothesis, method and result*
**On the slide:** Extension 1: asking the model to diagnose the evidence first failed

About 1.25 minutes. Give the failure its full time: a clean negative result is worth marks for honesty and result quality.

The control changes only one thing, a final line, so we can tell whether tidier output alone explains a difference. The control is also slightly worse than the baseline, but nothing like this.

Numbers: 800 stratified examples (268 answerable, 532 must be refused) covering all 100 source questions; the bars use the 776 examples also present in the baseline and count clean refusal codes only, so the baseline and control figures are lower bounds. The gap to diagnose-first is still huge, and the differences are significant (paired bootstrap over source questions). The model also wrote CLEAR for 258 of 268 answerable examples, and for ambiguity 68 of 69, contradiction 87 of 94, missing information 87 of 92, false premise 89 of 93, granularity 83 of 92, epistemic 90 of 92.

Likely question: "Why did it fail?" I do not know. "Anchoring on clear" would be a guess, not a finding; I tested nothing about the mechanism.

---

## 8. Turning point
*Turning point · from Extension 1 to Extension 2*

About 0.5 minutes. Pause here. This is the turning point of the project, so say it slowly.

"My first idea asked the model what was wrong with the evidence. It said everything was clear, 95% of the time. So the second idea does not ask. It reads the signal the model already computes, before it writes a single word."

Do not explain the method yet: the next slide does.

---

## 9. Extension 2: method
*Extension 2 · Hypothesis and method*
**On the slide:** Extension 2: read the model's own signal instead of its written answer

About 1.25 minutes. A probe is just a simple classifier (logistic regression) that looks at the model's internal numbers; the hidden state is the numbers the model computes on the way to its answer. Higher score always means "refuse". Nothing is generated: each score comes from one forward pass under its own prompt (S1 uses the paper's prompt, S2 a second yes/no prompt, S3 reads the hidden states of either pass).

Say clearly: S1 and S2 at their default thresholds use no labels; S3 is trained with the benchmark's labels. That is why the probe is a diagnostic of what the hidden state contains, not an equal-training comparison with the baseline.

Why the five groups: 1,600 examples are variants of 100 questions. A random split would put variants of the same question in training and test, and the result would look better than it is. A unit test corrupts the labels of one group and checks that the threshold for that group does not change. Honest limit: the intervals resample the held-out predictions; the fitting is not repeated inside each resample.

Success rule: signal if the lower end of S1's AUROC interval is above 0.5; gain if the tuned threshold beats the default with its interval above zero.

Scoring takes about 0.3 seconds per example on a T4. Likely question: "Where is your novelty?" Reading these signals for grounded refusal on this benchmark with a small open model, tested against the paper's baseline, with the version that did not work reported honestly. Related work (Yin et al., R-Tuning, Self-RAG) changes the model by training; ours keeps the weights fixed.

---

## 10. Extension 2: results
*Extension 2 · Results*
**On the slide:** Extension 2 result: the signal exists, a better decision is not shown

About 1.5 minutes. This is the "result quality" part of the rubric: read the verdict out loud, do not oversell.

Left (question A): all three readouts separate the cases far better than chance; their intervals start at 0.70 or higher. So the information is there.

Right (question B): would using it make better decisions than the judged baseline (balanced accuracy 0.690)? S1's whole interval is below zero (slightly worse). S2 is unclear. The probe S3 has the best point estimate, +0.028, but its interval runs from -0.014 to +0.065, so we do not claim an improvement. With five comparisons and no correction, even S1's "worse" is not robust.

Why a good AUROC does not give a better decision: AUROC measures ranking over every possible threshold; a deployed rule needs one operating point, and moving the threshold only trades one error for the other. In the trade-off picture the baseline sits close to the S1 and S2 curves and just above the probe's.

Per failure type (same 770 examples, needed refusals missed / answerable refused): contradiction baseline .71 / .17, S2 .23 / .50, probe .19 / .29; ambiguity baseline .74 / .09, probe .45 / .23; false premise baseline .19 / .33, probe .25 / .23. So the probe finds many more contradictions and ambiguities, but refuses more answerable questions.

Hostile question: "Your baseline depends on an unvalidated Gemini judge for most replies, while your rules are scored against labels." Answer: treat the comparison as provisional; I compare on the same 770 examples with intervals that resample whole questions, I claim no winner, and grading the rest plus the 30-reply judge check are the two next steps.

---

## 11. Conclusion
*Conclusion and limitations*

About 0.75 minutes. End on the honest statement, then stop talking and invite questions.

Central finding in one line: decodable is not deployable. A signal can be present in a model and still not be turned into a clearly better decision by simple rules.

"A full run" is the course's term: we ran a smaller-scale version; here is exactly what the full version needs. Related follow-up work to name if asked: Yin et al. (do models know what they do not know), R-Tuning (training a model to say "I don't know"), Self-RAG (a model that critiques its own retrieval). All three change the model by training; ours keeps the weights fixed and reads signals it already produces.

---

## 12. References
*References*

Leave this up during questions. The full list of 20 references is in the IEEE-format report.

---
