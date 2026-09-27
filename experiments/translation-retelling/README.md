# Translation / retelling preservation experiment

Status: first narrow evaluation target

## Goal

Test one practical claim:

> A FoM-based multidimensional contract can detect important translation/retelling failures that content-similarity or proposition-only comparison misses.

This experiment deliberately does not test "all of FoM".

## 1. Target failure classes

The first benchmark focuses on six classes already supported by executable FoM diff or close to it:

1. **content corruption** — proposition/event changed;
2. **certainty corruption** — assertion strength changed;
3. **salience corruption** — required focus weakened;
4. **inference-path corruption** — inferred content made explicit or evidence relation changed;
5. **disclosure corruption** — correct information revealed at the wrong point;
6. **fixed-unknown corruption** — candidate resolves something required to remain unknown.

The next two classes are especially important but require additional diff support:

7. **source/attribution loss**;
8. **deliberate multi-meaning collapse**.

## 2. Corpus design

Start with 12–20 short original items.

Do not use copyrighted passages.

Each item should have:

- source text;
- target audience/context;
- source FoM;
- one valid translation or retelling;
- 2–4 controlled corruptions;
- expected semantic-diff dimensions;
- human acceptability/preservation judgment.

At least half of the final evaluation items should be written independently after the FoM rules are frozen.

## 3. Example item families

### Fixed unknown

Source intentionally leaves a cause or identity unresolved.

Corruption adds a plausible explanation.

Expected:

```
CONTENT may remain compatible
FIXED_UNKNOWN = violated/lost
RESOLUTION = strengthened without license
```

### Delayed disclosure

A short two/three-stage narrative with a reveal.

Corruption moves the reveal into an earlier sentence.

Expected:

```
CONTENT = preserved
TIMING/DISCLOSURE = early/broken
```

### Inference route

Source shows evidence from which a character's emotion/conclusion is inferred.

Corruption states the emotion/conclusion directly and removes the evidence function.

Expected:

```
CONTENT target may be preserved
EXPLICITNESS = strengthened
INFERENCE_PATH = lost/broken
```

### Source attribution

Source says:

```
According to Alice, P.
```

Corruption says:

```
P.
```

Expected:

```
CONTENT = similar
SOURCE/ATTRIBUTION = lost
EPISTEMIC COMMITMENT = strengthened
```

### Multi-meaning

Source contains a deliberate double reading.

Corruption paraphrases only one reading.

Expected:

```
one reading preserved
other reading lost
coactivation/function lost
```

## 4. Experiment phases

### Phase A — FoM-to-FoM controlled corruption

Input is gold source FoM plus manually constructed corrupted candidate FoM.

Purpose:

- validate diff mechanics;
- establish executable expected outcomes;
- avoid confounding extraction quality.

This phase is already underway in `tests/fixtures/corruption/`.

### Phase B — Text realization with gold candidate FoM

Produce target-language/retelling texts from source FoM.

Annotate candidate texts manually with gold FoM.

Purpose:

- test whether the representation distinguishes good and bad realizations.

### Phase C — Automatic/model extraction

Have an independent model extract candidate FoM from the produced text without seeing source FoM.

Purpose:

- measure how much performance is lost due to extraction;
- separate representation failure from parser/extractor failure.

## 5. Baselines

The benchmark should compare against at least:

- exact/string similarity where relevant;
- embedding/semantic similarity;
- a strong LLM judge given source and candidate text but not FoM;
- proposition/content-only FoM comparison.

The important comparison is not "FoM beats every baseline".

It is:

> Which corruption classes require trajectory, uncertainty, attribution, or inference information that content-only methods systematically miss?

## 6. Metrics

For each corruption dimension:

```
precision
recall
F1
```

for detecting the injected corruption.

Also report:

- false positives on valid paraphrases;
- false positives caused by different but licensed resolution;
- human agreement on expected labels;
- extraction-induced errors separately from diff errors.

Do not collapse the benchmark to one similarity score.

## 7. Success criteria

A useful first result would be:

- near-perfect detection of synthetic controlled corruptions in Phase A;
- low false-positive rate on hand-verified valid paraphrases;
- evidence that at least one FoM-specific dimension catches failures missed by content-only comparison;
- clear accounting of cases where the representation or annotations disagree.

## 8. Failure criteria

The experiment should count against FoM if:

- valid paraphrases frequently fail because graph structure differs;
- humans cannot agree on the expected corruption dimension;
- source FoM must be excessively detailed to make the test work;
- the same result can be obtained more simply by an existing representation such as UMR plus a small evaluator;
- extraction noise dominates the semantic signal.

## 9. Architectural comparison

A particularly important variant is:

```
UMR/content graph
+
small FoM constraint layer
```

versus:

```
full standalone FoM
```

If the layered version performs equally well, the project should prefer the smaller architecture.

## 10. Immediate engineering work

1. extend executable diff to source attribution;
2. add explicit coactivation/multi-meaning constraint diff;
3. classify early/late disclosure using checkpoint order;
4. add candidate FoM fixtures for all benchmark dimensions;
5. create the first 12 original source items;
6. freeze an annotation guide before external annotation.
