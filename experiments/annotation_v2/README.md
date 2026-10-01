# Semantic commitments v2 and independent annotation packet

Status: a [same-model fresh-context Pass A pilot](coordinator/RESULTS-01.md)
has been collected and reviewed. The independent human/different-model study
has **not** been run. Raw responses, delivery hashes and a qualitative review
ledger are retained; no annotation-time or numerical agreement claims are made.

This version responds to the layered-architecture coverage audit without
rewriting the original corpus, old gold pairs, or recorded pilot results.
It covers all ten original texts. `commitments.toml` is a frozen single-author
proposal for adjudication, **not consensus gold** and not executable FoM.
Freeze means a reviewable version exists; it does not mean its interpretations
are beyond challenge. Future revisions must retain this proposal's history.

## What changed in the proposed commitments

- Umbrella: unresolved leaver, not inferred owner; wetness and non-discovery retained.
- Bridge: report attribution, night, and absence of other confirmation retained.
- Chair: cups/table, persistent warmth, and silence retained. A visitor is
  defeasible, not an asserted fact or a pre-decided REQUIRED inference.
- Letter: empty envelope, Lena's attributed conclusion, and evening discovery
  retained separately from reader disclosure policy.
- Tongue: utterance, interpreter, action, and two linked readings retained;
  no claim that all readers must experience amusement.
- Train: uncertainty and already both retained without invented probabilities.
- Peter: contract and others' agreement retained; contrastive focus is not
  reduced to high salience or agreement to completed signing.
- Declaration: speech event and continued discussion retained; institutional
  authority is not invented to force the intended failure label.
- Key: competing attributed claims and narrator uncertainty retained; a
  universal exclusivity axiom is not silently added.
- Note: specific quoted word and exactly one-word form retained. The explicit
  translation policy permits translated quotation; no archival grapheme claim.

Each proposed requirement has a stable case-local key, a dimension, a claim,
literal source evidence, and `basis = text | policy`. Evidence for a policy
explains what it protects; it does not turn that policy into a source assertion.
Every case also lists prohibited inferences, open questions, and legacy issues.
Open questions are deliberately not pre-scored as violations.

## Distribution boundary

Give an annotator **only**:

1. `blind/packet.json`
2. `blind/response-template.json`

The packet contains neutral IDs P01–P10 in a fixed shuffled order, unchanged
sources, languages, shared context, translation policy, and generic Pass A
instructions. It excludes the semantic case names, designer commitments,
valid/corrupted candidates, expected dimensions, and audit notes.

Do not send the repository, this README, the proposal, or the coordinator
manifest to blind annotators. These files are public together in the repository:
this is **blindness at delivery**, not access control or secrecy. Use genuinely
fresh contexts/annotators with no previous exposure, and record any exposure.
The shared translation task policy is supplied intentionally, not hidden.

No dispatch, external messages, model calls, annotation times, or agreement
measurements are fabricated by the preparation script. Empty response fields
are not annotations. The author of the proposal is not an independent annotator.

## Collection and adjudication protocol

Collect at least two independent Pass A responses before showing either
annotator the proposal or the other's response. Each should provide a short
meaning account, evidence-backed commitments, attribution, explicit/inferred
status, unresolved alternatives, policy assumptions, and actual elapsed time.
Unknown timing stays null. Preserve raw responses and participant/model details.

An adjudicator then compares commitments by meaning and evidence, not by exact
wording, item count, graph equality, or agreement with this author's proposal.
Record for each issue: both supported, one unsupported, genuine ambiguity,
guideline gap, or missing source content. Allow both annotations to be valid.
Report factual/reference, attribution, uncertainty, inference, trajectory,
social-state, focus/function/form disagreements separately. Do not invent an
automatic cross-constraint agreement score: the current evaluator is too narrow.

Only after Pass A adjudication should Pass B encode the agreed requirements
in standalone FoM and carrier+overlay. Counterbalance which representation
is encoded first across annotators and record actual elapsed time for each.
Keep encoder identity/exposure and order in the record. Prefer a separate
qualified UMR annotation check before calling the carrier UMR-compatible.

Unresolved annotation disputes remain visible and unscored. Valid candidates
and controlled corruptions must be judged after source commitments are fixed;
the old `valid` and `corrupted` names are designer hypotheses, not final labels.
Do not retroactively replace the old seven-pair feasibility results with v2.

## Reproduction

```sh
python -m experiments.annotation_v2.prepare
python -m unittest discover -s python_tests -p test_annotation_v2.py
```

The coordinator manifest records the source mapping and hashes of the corpus,
proposal, and packet. Hashes use LF-normalized UTF-8. Tests check full coverage,
literal evidence, deterministic reproduction, empty responses, and allowlisted
packet fields. They do not establish semantic correctness or human agreement.
