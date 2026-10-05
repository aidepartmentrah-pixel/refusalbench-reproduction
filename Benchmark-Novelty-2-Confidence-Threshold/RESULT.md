# Novelty 2: confidence-threshold refusal gate: RESULT

**Status: NOT RUN YET.** The code is built and tested locally (unit tests, a tiny-model test, a full fake end-to-end run on the real 1,600 examples). The real run on a Colab T4 is the next step: see `README.md`.

After the run, this file will hold:
- the verdict from `RESULT_AUTO.md` (SUPPORTED / SIGNAL BUT NO GAIN / NOT SUPPORTED), copied with its numbers,
- the table of S1, S2, S3 with 95% intervals,
- the false-vs-missed refusal trade-off figure,
- what it means for the defense, and the limitations.
