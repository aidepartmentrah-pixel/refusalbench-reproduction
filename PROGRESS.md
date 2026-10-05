# Progress Log

Updated live as each task finishes. `[x]` done, `[ ]` to do, **>>** is the task in progress.
Owners: **[C]** Claude, **[Y]** you, **[B]** both together.

## Master Progress Matrix

|Slice|Primary capability|Main dependency|Environment|Core automated proof|Real/manual proof|Status|
|---|---|---|---|---|---|---|
|S0|Project setup + dataset foundation|None|Windows + Python 3.10|Dry-run prints the exact prompt, 20-example seeded sample|Loaded the real 1,600-row RefusalBench-NQ, schema checked against the original repo|**DONE** (Stage 1)|
|S1|Paper reading + reference targets|S0|Windows|—|GPT-4o numbers read from Fig. 24 (GPT's were wrong), Qwen-7B answer accuracy 56.1% from text, refusal about 0.05 from Fig. 9|**DONE**|
|S2|Judge ready (Gemini, free)|S0|Windows + Gemini API|4 hand-made judge cases, parser with visible fallbacks, retries for 503/429|Real calls through our own client class: `gemini-3.5-flash-lite` 4/4 sensible, about 375 tokens in per call|**DONE** (judge pinned: `gemini-3.5-flash-lite`)|
|S3|Qwen runner (generation, resume)|S0|Windows (fake model) + Colab T4|Fake-model run: forced crash at reply 25, re-run resumed with 60 unique IDs, no gaps, no duplicates|10-example run of the real Qwen on Colab|**BUILT + TESTED locally** — the real Qwen has not run yet (needs Colab)|
|S4|Parser, judge pipeline, metrics, report|S2, S3|Windows|`tests/selftest.py`: parser, judge parser, metrics vs hand-computed values, all pass; fake end-to-end run produced report, CSVs, hand-check sheet|Judge on real Qwen replies, 30-response hand check|**BUILT + TESTED locally** — waiting for real Qwen replies|
|S5|One-click Colab notebook (Run all)|S3, S4|Windows + Colab T4|`scripts/run_all.py --fake` runs 10, 100, rest, judge, metrics, report in one command|Click Run all on Colab|**BUILT + PUSHED** — your first real click on Colab (repo is private: add the `GITHUB_TOKEN` secret or make it public)|
|S6|Baseline generation (10, 100, 1,600)|S5|Colab T4|Automatic checks between stages (error rate, empty replies)|1,600 unique IDs on Drive|NOT STARTED|
|S7|Baseline judging, metrics, comparison, report|S6|Colab or Windows|Counts reconcile, no unjudged gaps|`reproduction_report.md` vs paper (Qwen-7B)|NOT STARTED|
|S8|Review gate|S7|You + Claude|—|We read the results and failure patterns together|NOT STARTED|
|S9|Novelty design (category-first)|S8|You + Claude|—|Proposed in Obsidian note 9, pitch to your professor (E1–E4)|NOT STARTED — proposed, conditional on baseline failure analysis|
|S10|Novelty runs: baseline vs format-only vs category-first on the stratified 800|S9|Windows (code) + Colab T4 (runs)|`tests/selftest_conditions.py` passes; fake end-to-end of all three conditions on the real 800 subset; paired bootstrap runs|Real 800-example runs, paired bootstrap over source questions|**CODE BUILT + TESTED locally** — not pushed yet (so a Colab re-run of the baseline cannot pick it up); real runs wait for the gate, approval and prompt freeze|
|S10b|Novelty 1 verdict (Classify-then-Decide)|S10|Windows|Paired cluster bootstrap on 776 common examples, parse-only scoring|Raw replies read by eye: Qwen writes `EVIDENCE_STATE: CLEAR` on 95%|**DONE: NEGATIVE RESULT.** Code archived in `Benchmark-Novelty-1-Classify-then-Decide/`|
|S12|Novelty 2: confidence-threshold refusal gate|S10b|Windows (code) + Colab T4 (one run, about 20-40 min *estimate*)|Fake end-to-end run, metric and bootstrap tests, tokenizer check|Real 1,600 forward passes (dev pool to tune, 800 to test), judge-free|**RUN DONE: signal but no significant gain from the threshold; probe S3 best** (see Phase H)|
|S11|Course deliverables|S7, S10, S12|Windows|Both `baseline/` and `extension/` run|Report, slides (cover + 6 + references), 12-minute defense|NOT STARTED|

---

## Current plan (decided)

- **Target model:** Qwen 1.5 7B Chat on free Colab T4 (4-bit or 8-bit, a documented deviation)
- **Judge:** a free Gemini model (replaces the paper's Claude Sonnet 4, a documented deviation)
- **Scoring:** parse first, judge only unclear replies and answerable examples
- **Baseline:** all 1,600 RefusalBench-NQ examples. **Novelty:** a stratified random 800 of the same examples, compared paired
- **Budget:** $0 target, $20 hard limit
- **Paper targets (Qwen-7B, NQ):** answer accuracy 56.1%, refusal accuracy about 0.05 (read from a small plot, approximate). GPT-4o reference (Fig. 24): answer 0.332, refusal 0.518, CRS 0.425, false refusal 0.628, missed refusal 0.043
- **Gate:** we stop after the baseline report and review it together before any novelty work

---

## Phase A: Judge ready (Gemini, free)

- [x] A0 [C] Key is in `.env` (never printed). `google-genai` installed. Model list works with the key
- [x] A0b [C] Wrote `src/judge.py` (paper's judge prompt verbatim + parser with visible fallbacks) and `scripts/test_judge.py`
- [x] A0c [C] **Finding:** `gemini-2.5-flash` returns 404 "no longer available to new users". Google suggests `gemini-3.8-flash`. The listing shows `gemini-2.5-pro` and several 3.x models, but visibility does not mean usable
- [x] A1 [C] Probed which models accept calls (`scripts/probe_gemini.py`). **Work:** `gemini-3.8-flash`, `gemini-3.7-flash`, `gemini-3.5-flash`, `gemini-3.5-flash-lite`, `gemini-flash-latest`. **Closed to new keys (404):** `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`
- [x] A2 [C] Ran the 4 hand-made judge cases. `gemini-3.5-flash-lite`: 4 of 4 sensible (correct answer scored 5; bare `REFUSE_AMBIGUOUS_QUERY` recognised; wrong answer "1492" vs "1611" scored 3; free-text refusal with no code classified `REFUSE_OTHER`). `gemini-3.8-flash`: first case correct (score 5), second call hit a **503 "high demand"**, so retries are required
- [x] A3 [C] Measured per call: about 375 input tokens, 45 to 115 output tokens (my estimate was 450 and 60). `3.8-flash` also spends about 170 thinking tokens and took 8.4 s, `3.5-flash-lite` has no thinking and took about 1 s. No rate limit or daily cap was hit in about 12 calls, but that proves little. Free tier means no cost either way
- [x] A4 [B] Judge pinned: `gemini-3.5-flash-lite` (you left the choice to me; fastest, 4 of 4 sensible, no 503s seen). Fallback `gemini-3.8-flash` if the hand check shows problems
- [x] A5 [C] Gemini judge client (`GeminiJudge`) with a finite retry limit for 503/429 with backoff, a request-rate limiter, and a clean stop when quota runs out. Tested live through our own class

## Phase B: Qwen runner (code, tested locally)

- [x] B1 [C] `configs/qwen15_7b_baseline.yaml`: model, precision (4bit/8bit/fp16), temperature 1.0, top_p 1.0, max new tokens 256, seed, batch size, judge settings, stages
- [x] B2 [C] Qwen client (`HFClient`, transformers + chat template, `bitsandbytes` 4-bit/8-bit switch) in `src/model_client.py`
- [x] B3 [C] Batched generation; a CUDA out-of-memory error halves the batch automatically
- [x] B4 [C] Append-only `target_outputs.jsonl` (ID, question, context, reference, expected, config, prompt hash, raw reply, status, timestamp) plus `errors.jsonl`; run folder is fixed per run name and a settings lock refuses to mix settings
- [x] B5 [C] Resume: skips finished IDs, flushes after every batch. Proven with a forced crash
- [x] B6 [C] `scripts/run_all.py` (the one-click entry point, replaces separate run scripts), `--fake` and `--dev-subset` for tests only
- [x] B7 [C] Local test with a fake model: crash then resume gives 60 unique IDs, no gaps, no duplicates
- [x] B8 [C] `requirements-colab.txt` (lower bounds only, exact versions get recorded in each run's report)
- [x] B9 [C] `Benchmark-Baseline-Reproduction/colab_baseline.ipynb` (moved from `notebooks/`): Drive, clone, install, secrets, GPU check, run everything, show report, download zip
- [x] B10 [C] Committed and pushed to `origin/main` (commit `d2164cd`, no secrets, `.env` and `.venv` ignored). **The repo is PRIVATE**, so Colab needs either the repo made public or a `GITHUB_TOKEN` secret (read-only token for this repo). I did not change the visibility without your say-so

## Phase C: Parser, judge pipeline, metrics (code, tested locally)

- [x] C1 [C] `src/parser.py`: exactly one distinct valid `REFUSE_*` code means refusal, anything else goes to the judge
- [x] C2 [C] Judge pipeline (`run_judging`) writing `judged_outputs.jsonl`, append-only, resumable, stops cleanly on quota, refuses to mix judge models in one folder
- [x] C3 [C] Refusal metrics with the paper's definitions (`src/metrics.py`)
- [x] C4 [C] Answer accuracy (score 4 or 5) and calibrated refusal score
- [x] C5 [C] Breakdowns by uncertainty type and by intensity, confusion matrix
- [x] C6 [C] `tests/selftest.py` (all pass), metrics checked against a hand-computed case
- [x] C7 [C] Paper comparison in the generated report (Qwen-7B: answer accuracy 0.561 exact, refusal accuracy about 0.05 approximate, other metrics marked not extracted)

## Phase D: Baseline delivered (all 1,600) — automated by the notebook

Everything below runs by itself when you click Run all, except D5 and D12.

- [ ] D1 [auto] Stage 10 on Colab T4, automatic check (at least 80% ok replies, at most 30% empty), prints 3 sample replies
- [ ] D2 [auto] Reports clean `REFUSE_*` rate, seconds per example, estimated time left
- [ ] D3 [auto] Stage 100, same checks
- [ ] D4 [auto] Judge runs after generation; the report states how many calls the judge needed
- [ ] D5 [B] **Hand-check about 30 judged responses:** open `handcheck_sheet.csv`, write y or n in `human_ok`, then run `python scripts/score_handcheck.py <file>` to get the agreement rate (this validates the substitute judge)
- [ ] D6 [auto] All 1,600 generated (resumes across disconnects; keep the tab open and the laptop awake)
- [ ] D7 [auto] Verifies 1,600 unique IDs, no gaps, no duplicates
- [ ] D8 [auto] Judge on unclear replies (parse first)
- [ ] D9 [auto] Metrics, breakdowns, confusion matrix written to the run folder
- [ ] D10 [auto] Paper comparison and deviation list in the report
- [ ] D11 [auto] `reproduction_report.md` generated
- [ ] D12 [B] **GATE: review the baseline results together. No novelty work until this is done**

**Baseline data check (from `Benchmark-Baseline-Reproduction/qwen15_7b_baseline.zip`, first Colab run):** generation is **1,560 of 1,600 done**, valid and duplicate-free (config matches: Qwen1.5-7B-Chat, 4-bit, temperature 1.0, top_p 1.0, max 256 tokens, prompt hash `c0008c7504b3`). **40 examples failed with CUDA out-of-memory** in batches of 8 and were never retried; the run stopped at the missing-IDs check before judging. They are ordinary examples (longest 1,852 characters, the dataset maximum is 2,012 and one of those succeeded), so the one-by-one retry in the pushed fix should recover them. No judging, metrics or report yet. Reply format: 568 clean `REFUSE_*` (36%), 991 free text with no code (64%), 1 multi-code, 0 empty, so the judge will handle about 1,000 replies, more than the earlier 804 estimate. **Action: re-run Cell 1 on the first account** (pulls the fix, retries the 40, judges, computes metrics, writes the report). Do not redo the run.

**Judge quota finding (2026-10-04 night):** the free Gemini tier allows **500 requests per day per project per model** (`gemini-3.5-flash-lite`, error 429 `GenerateRequestsPerDayPerProjectPerModel-FreeTier`, reset about 5 hours after the error, so around 03:00 local). The local baseline judging used 495 calls and stopped cleanly at **730 of 1,560 rows**. **Those 730 are not a random sample** (the old order was by example ID: all 400 `claude`, 274 `deepseek`, only 31 `gpt`, 25 `nova`), so the metrics in that report (answer 0.717, refusal 0.099) **must not be read or compared with the paper**. The report now carries an INCOMPLETE banner. Judge calls still needed for the baseline: **517** (a bit more than one day's quota). Estimated total still needed: baseline 517 + format-only about 600 + category-first about 300. Quota is per project, so a key from another project has its own 500 per day. Code fixes (not yet pushed when written): judging now runs in a seeded random order, a daily-quota error stops immediately, and the report shows the INCOMPLETE banner. Options to finish faster: wait for the daily resets (about 2 to 3 days), use a second key from a different project (the Colab account may already have one), or enable billing on the project (cost for about 2,000 calls would be a few cents, your decision). Mixing different judge models inside one condition is blocked by the code on purpose.

## Phase E: Novelty pass: category-first selective refusal (Obsidian note 9)

Three conditions on the same stratified 800, same Qwen, same settings, same judge: **baseline**, **format-only control**, **category-first**.
The code is built (E5 to E11, E12b, E15). Still open: E12 prompt pilots on the dev pool, which need the GPU after the baseline finishes. Nothing real runs before the review gate and your professor's approval.

- [ ] E1 [B] Failure analysis from the baseline (gate D12). The novelty is conditional: reconsider if Qwen almost never emits valid labels, almost always refuses, or the run has a bug
- [ ] E2 [B] Confirm category-first as the novelty (proposed in note 9)
- [ ] E3 [B] Related-work check, so the claim stays narrow ("does evaluating the evidence state first help a small model, beyond format fixing")
- [ ] E4 [Y] One-paragraph pitch to your professor, wait for approval
- [x] E5 [C] Add `source_id` to the schema adapter (needed for the bootstrap). The baseline run can be joined later by example ID, no rerun **Done:** `source_id` is now in the adapter; baseline rows are unchanged and join by ID later.
- [x] E6 [C] `scripts/make_novelty_sample.py`: stratified 800 (answerable vs refusal x uncertainty type x intensity), seed 0, **keeps all ~100 source questions**, saved to `data/novelty_sample_ids.json`. The other 800 become the dev pool for prompt pilots **Done:** `data/novelty_sample_ids.json`: 800 ids (268 answerable, 532 refusal, LOW 268 / MEDIUM 265 / HIGH 267), **all 100 source questions covered** (2 to 15 each), plus 800 dev-pool ids.
- [x] E7 [C] `src/conditions.py`: the three prompts. Baseline stays verbatim. Format-only adds one instruction (end with a `FINAL:` line). Category-first asks for `EVIDENCE_STATE:` then `FINAL:`. **Same definitions text in all conditions**, so only the structure differs. Mapping: AMBIGUOUS, CONTRADICTORY, MISSING_INFORMATION, FALSE_PREMISE, GRANULARITY_MISMATCH map to the matching `REFUSE_*` code, EPISTEMIC_MISMATCH maps to `REFUSE_NONFACTUAL_QUERY` **Done:** `src/conditions.py`; the baseline prompt is verbatim and the definitions text is asserted identical in all three prompts.
- [x] E8 [C] Reply extraction per condition. Category-first: state decides the outcome (not CLEAR means the mapped refusal, CLEAR means the text after `FINAL:` is the answer). Logs how often `FINAL` contradicts the state **Done:** Extraction in `src/conditions.py`; flags `no_final_line`, `final_conflicts_with_state`, `clear_but_refused`, `no_valid_state`.
- [x] E9 [C] Config fields `condition` and `subset_file`, added to the settings lock, one run folder per condition. `run_all.py` accepts a subset and skips the 1,600 size assertion for it **Done:** `configs/qwen15_7b_format_only.yaml`, `configs/qwen15_7b_category_first.yaml`, `--subset-file`; the baseline lock stays byte-identical.
- [x] E10 [C] Judging uses the extracted reply (code scored by parser, answer text to the judge), unchanged otherwise **Done:** Judging scores the extracted reply and records `effective_reply`, `evidence_state`, `flags` for non-baseline runs.
- [x] E11 [C] Tests: `FINAL` and `EVIDENCE_STATE` parsing, malformed output, state-vs-final conflicts, fake end-to-end for both conditions **Done:** `tests/selftest_conditions.py` passes (it caught a markdown-bold parsing bug in `FINAL:`, fixed). Fake runs of all three conditions on the real 800 subset worked, crash-safe.
- [ ] E12 [C] Pilot on the **dev pool (the other 800)**, 30 examples per prompt, at most 3 prompt revisions, each recorded. Then **freeze the prompts** before touching the 800
- [x] E12b [C] `Benchmark-Novelty-1-Classify-then-Decide/colab_novelty1.ipynb` (moved) built: setup, format-only run, category-first run, comparison (all resumable). Do not run before the gate, approval and prompt freeze. **Update:** you chose to start the novelty sweep early on a second T4 (other Google account). Code pushed in `dcc878d` (also adds the out-of-memory fallback and catch-up passes). The prompts were not piloted on the real Qwen, so the first 10 sample replies of each condition must be checked by eye; results are provisional until the gate, the professor's approval and a prompt review.
- [ ] E13 [Y] Run the format-only condition on the 800 on Colab (about 1.5 h on the T4, resumable)
- [ ] E14 [Y] Run the category-first condition on the 800 (about 1.5 to 2 h)
- [x] E15 [C] `scripts/compare_conditions.py` + `src/compare.py`: baseline vs format-only vs category-first on identical examples, paired cluster bootstrap over the ~100 source questions, 95% intervals. **Done:** tested on fake runs (numbers meaningless, intervals realistically wide).
- [ ] E16 [C] `novelty_report.md`: main comparison is **category-first vs format-only control**, plus limitations
- [ ] E17 [B] Review the novelty results together
- [ ] E18 [optional, C] Probability-based answer/refuse threshold curve (note 9, section 16), only if time remains

## Phase N1: Novelty 1 archived (Classify-then-Decide, category-first): NEGATIVE RESULT

Result and numbers: `Benchmark-Novelty-1-Classify-then-Decide/RESULT.md`. Qwen answered `EVIDENCE_STATE: CLEAR` on 95% of examples, so it almost never refused (correct category 0.0% vs 3.3% format-only vs 6.8% baseline; all paired-bootstrap intervals exclude zero).
Rule from now on: **every experiment lives in its own folder** (`Benchmark-Novelty-N-<name>/` with `README.md`, `code/`, `configs/`, notebook, `RESULT.md`). Shared infrastructure (`src/`, `data/`, baseline) stays at the top.

- [x] N1.1 [C] Run the comparison on the three conditions and write `RESULT.md` (done, in the folder)
- [x] N1.2 [C] Move the Novelty 1 code into the folder (`code/conditions.py`, `code/compare.py`, `code/compare_conditions.py`, `code/selftest_conditions.py`, `configs/`, notebook) and keep the baseline pipeline working through a small plug-in hook (`experiment_dir` in the config) **Done:** `src/conditions.py` is now baseline-only plus the loader; Novelty 1 lives in its folder.
- [x] N1.3 [C] Re-run all self-tests and a fake baseline + fake novelty-1 run to prove nothing broke **Done:** all pass; fake baseline, format-only and category-first runs work from the new paths.
- [x] N1.4 [C] Baseline folder tidied the same way: `Benchmark-Reproduction-Data/` renamed `Benchmark-Baseline-Reproduction/`, now holds `colab_baseline.ipynb`, `configs/qwen15_7b_baseline.yaml`, `README.md` (how to run on Colab) and the two result zips. `scripts/run_all.py` default config path updated.

## Phase H: Novelty 2: confidence-threshold refusal gate (folder `Benchmark-Novelty-2-Confidence-Threshold/`)

Idea (note 9, idea 5, with 2 and 6 as ablations): do not read what Qwen *writes*. Read how likely Qwen is to start a refusal code, and decide answer vs refuse with a threshold tuned on other source questions (5-fold cross-fitting over all 1,600 examples, also reported on the 800 novelty subset). Judge-free, so the Gemini quota does not matter. Targets refusal **detection** (answer vs refuse), not category.

- [x] H0 [C] Design written down in the folder `README.md`: hypotheses, three scorers (S1 refuse-code probability = the novelty, S2 yes/no sufficiency probability, S3 hidden-state linear probe), protocol, metrics, what would count as failure
- [x] H1 [C] `code/scorer.py`: one forward pass per example (no generation), probability of the refusal first-tokens, last-token hidden states, left-padding fix, out-of-memory halving, fake scorer for tests **Done:** tested on a tiny random Qwen2 with the real Qwen tokenizer (left padding invariant, cached scoring equals the cache-free reference to 1e-6, out-of-memory halving).
- [x] H2 [C] `code/analysis.py`: AUROC and AUPRC, false-refusal vs missed-refusal curve, thresholds and probe cross-fitted over source questions, linear probe, paired cluster bootstrap over source questions, plots, auto-written `RESULT_AUTO.md`
- [x] H3 [C] `code/run_novelty2.py`: resumable (shards on Drive), dev pool + novelty 800, then analysis; `configs/novelty2.yaml`
- [x] H4 [C] Tests: metric values checked by hand, a fold's threshold never depends on its own labels, tokenizer first-token check, fake end-to-end run
- [x] H5 [C] `colab_novelty2.ipynb`: ONE code cell (also pasted in the folder `README.md`)
- [x] H6 [B] **Committed, pushed and run on a Colab T4 (2026-10-05).** Note: the cross-fitting over source questions replaces the plain dev-pool split, because all 100 source questions appear in both pools (a split would leak)
- [x] H7 [B] `RESULT.md` written. **Verdict: SIGNAL BUT NO GAIN FROM THE THRESHOLD** (S1 AUROC 0.726 [0.699, 0.752]; tuned vs default balanced accuracy +0.015 [-0.008, +0.036]). Best variant is the supervised hidden-state probe S3 (balanced accuracy 0.721 [0.691, 0.749]). Cannot claim to beat the baseline until the baseline is fully judged.
- [ ] H8a [Y] **Finish judging the baseline on Colab** (`Benchmark-Baseline-Reproduction/colab_baseline.ipynb`, `GEMINI_API_KEY` secret). It retries the 40 failed examples and judges the rest; free quota is 500 calls per day, so 1 to 2 days (or a second key). Then download and unzip `qwen15_7b_baseline/` into `Benchmark-Baseline-Reproduction/`
- [x] H8b [C] `code/compare_to_baseline.py` + `code/selftest_compare.py`: the fair comparison, baseline (judged replies) vs S1/S2/S3 on the same examples, paired cluster bootstrap, fixed BETTER / NO CLEAR DIFFERENCE / WORSE rule, labels-used column, representativeness warning, figure. Tested on synthetic cases with known answers and run on real data with the judged format-only control as a stand-in (pipeline check, not a result)
- [ ] H8c [Y] Run `compare_to_baseline.py` once the baseline is judged (command in the Novelty 2 README, step 2)
- [x] H9a [C] `PITCH.md` drafted (one paragraph, what we ask to approve, related work to verify, honest status)
- [ ] H9b [Y] Check the citations in `PITCH.md`, adjust, send it to the professor and wait for approval
- [ ] H10 [B] Decide what to claim from `COMPARISON.md`, update `RESULT.md`

## Phase F: Course deliverables

- [ ] F1 [C] Repo layout with `baseline/` and `extension/` that both run
- [ ] F2 [C] README: setup, Colab steps, commands, outputs, deviations
- [ ] F3 [B] Research-style report: problem, original paper, baseline reproduction, limitation, extension, method, experiment, results, limitations, related work
- [ ] F4 [B] Slides: cover, six content slides (problem, original solution, original and reproduced results, limitation and idea, our implementation, our results), references
- [ ] F5 [Y] Prepare the 12-minute defense and questions
- [ ] F6 [C] Update the Obsidian notes with final results

---

## Log of what is already done

### Stage 1: Inspect, set up, dry-run (no API calls)
- [x] Cloned the original repo outside the project and read its README, config template, `run_models.py` and `run_models_all.py`
- [x] Schema mismatch confirmed: only `run_models.py` uses the old fields (`query`, `retrieved_docs`, `ground_truth_label`, `answer`). `run_models_all.py` already uses the released fields but reads `unique_id` where the dataset has `id`
- [x] The prompt is identical in both scripts: one user message, no system prompt, no temperature, top_p or max_tokens set (provider defaults). The original retries up to 100 times, ours will be capped
- [x] Created `.venv` (Python 3.10.0), pinned `datasets`, `openai`, `python-dotenv`. Created `.gitignore`, `.env.example`
- [x] Dataset checked: 1,600 rows, 536 `ANSWER_CORRECTLY` (all LOW intensity), 1,064 refusal rows (MEDIUM and HIGH)
- [x] Wrote `src/schema_adapter.py`, `src/dataset_loader.py`, `src/prompt_builder.py`, `src/model_client.py` (interface only), `run_smoke_test.py` (dry-run only, `--limit` capped at 50)
- [x] Dry-run works: seeded 20-example sample saved to `data/smoke_sample_ids.json` (7 answerable, 13 refusal, all six uncertainty types, LOW 7 / MEDIUM 6 / HIGH 7)

### Reading the paper (read-only)
- [x] Gemini 2.5 Pro has **no published result** in the paper (only a lever-example generator role and an appendix listing), so it is not a baseline
- [x] Judge in the paper: Claude-4-Sonnet, score 4 or 5 is correct, refusal correct only on an exact category match. Judge prompt in Appendix I.1.4 matches the repo
- [x] Settings in the paper: temperature 1.0 and top_p 1.0 for proprietary and open models (Gemini 2.5 Pro at 0.1)
- [x] GPT's proposed GPT-4o numbers were **wrong**. Verified from Figure 24: answer 0.332, refusal 0.518, CRS 0.425, false refusal 0.628, missed refusal 0.043, correct refusal 0.957
- [x] Qwen-7B on NQ: answer accuracy 56.1% (text), refusal accuracy below 17% for every Qwen size and about 0.05 at 7B (small plot). Qwen-7B almost never gets the refusal category right in the paper either, so a very low refusal accuracy in our run is expected

### Decisions and notes
- [x] Obsidian note 6 read: target moved to Qwen 1.5 7B Chat on Colab
- [x] Decision: baseline on all 1,600, novelty on a stratified 800 (note 7 saved)
- [x] Colab screenshot: free tier gives a T4 only, so Qwen 7B needs 4-bit or 8-bit
- [x] Decision: zero-cost plan with a free Gemini judge and parse-first scoring (note 8 saved, includes the Colab "can I walk away" answer: keep the tab open, resume handles disconnects)
- [x] GPT's parse-first idea reviewed: sound, but "no REFUSE code means ANSWER" is wrong for a small model, so unclear replies must go to the judge
