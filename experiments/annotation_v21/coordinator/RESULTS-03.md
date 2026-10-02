# Run 03: shared cues, incompletely aligned inference obligations

Both responses use the same frozen 2.1 packet (canonical hash
`ee3fcf8392131c48cbeaa0d43ead8507bc5ae3f25c3f791852cd330083d685ff`).
The new agent reports reading only packet/template. Its 37 commitments contain
35 required, one optional and one unresolved decision. Terra supplied 26
required commitments. Both cover ten items, all evidence quotes validate, and
no timings were measured. Counts describe responses, not accuracy or agreement.

This comparison removes the changed-instruction confound from Run 02 versus
v2.0. It compares requested Terra routing with inherited parent configuration;
exact backend identities and model-family independence remain unverified.
One sample per configuration cannot establish model-level behavior.

The [manual alignment](alignment-03.json) cites every commitment, allowing
one-to-many matches and unpaired objects. Its automated audit verifies references
and coverage, not the coordinator's nonblind semantic judgments. Reproduce with
`python -m experiments.annotation_v21.compare_responses`.

## Findings

- Ordinary factual and attribution content is provisionally compatible across
  the ten cases. Extra fresh rows frequently state nonaddition boundaries that
  Terra places in unresolved prose. Raw row counts would misrepresent this.
- P02: Terra C03 requires availability of recent occupancy; fresh C04 leaves a
  particular visitor explanation beyond the cues unresolved. This is a real
  boundary to investigate, but not cleanly identical propositions receiving
  different labels. Both preserve continued warmth and reject asserted visitors.
- P05: both require an inferred feature, but Terra C03 names ineffective closure
  whereas fresh C04 names the speech/action contrast. Formal invalidity remains
  unknown, and corridor attachment remains unadjudicated.
- P06: both C03 rows require availability of idiomatic/literal interplay.
  This is provisional convergence on a shared object under 2.1, not proof that
  the guide caused agreement or that the old response was wrong. Terra's
  comparable-effect allowance and fresh's no-new-joke policy leave realization
  latitude unsettled. The two reading cues are a stronger common basis than
  an asserted author intention or a generic requirement to be funny.
- P10: Terra C04 concerns delayed awareness; fresh C04 concerns possible
  causation/reconsideration. Equal inferred/required labels conceal different
  objects. Both preserve order and avoid asserting actual belief revision.
- P03 independently retains a generic stop. P04's optional Cyrillic is a
  separate policy object, compatible with required negative meaning and count.
  P07's supplied signing complement versus unspecified agreement object needs
  care before gold encoding. P01/P08/P09 retain attribution and uncertainty.

## Decision

Do not expand semantics or replace gold based on this collection. Preserve the
raw responses and historical reports. Shared content can seed provisional
constraints; P02/P05/P10 inference obligations and P06 realization latitude
remain open. There is no kappa, percentage agreement or adjudicated score.

The next bounded experiment is a realization contrast set for P02/P05/P06/P10,
reviewed without these annotations. For each source, prepare a faithful literal
baseline and explicit controls that remove a cue or assert a speculative
conclusion. Separately attempt a candidate retaining the factual cues while
changing inference availability. Reject that candidate design if it requires
extra facts or merely changes wording without demonstrable semantic effect;
do not invent a separation to fit the architecture. Reviewers should extract
what each candidate asserts and makes available before seeing intended labels.

This tests whether a separate inference obligation has observable work to do
beyond factual cues and order. It is a more concrete next step than repeatedly
collecting free-text annotation until the required flags happen to match.
