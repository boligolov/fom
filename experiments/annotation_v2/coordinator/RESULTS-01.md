# Run 01 results: fresh-context reproducibility, not diverse-model agreement

Two isolated-context model agents returned complete Pass A responses, preserved
verbatim in `responses/annotator-a.json` and `responses/annotator-b.json`.
Both report reading only the designated packet/template. Each annotated all
10 sources; A lists 35 commitments and B lists 31. All evidence quotes match
their source text. All per-item timing values are null: annotation speed and
cost have not been measured. The delivery report records normalized file hashes.

Both agents used the parent's model configuration without a model override.
Exact model versions were not verified. They did not see each other's answers,
but this does not supply different-model or human independence. Repository
access was constrained by instruction, not technical file isolation. The
coordinator knew the author proposal; the review below is not blind or an
independent third annotation.

## Substantive findings

The [review ledger](review-ledger.json) covers all ten items and cites local
commitment IDs in both raw responses. On the inspected ordinary facts and
attribution boundaries the accounts are compatible; extra commitment rows
often reflect decomposition rather than disagreement. This is a qualitative
review, not an exhaustive alignment or a percentage agreement claim.

The material required-status disagreement is P06, the language/tongue example:

- A C04: inferred wordplay, `required: false`.
- B C03: inferred wordplay, `required: true`.

Both recognize the lexical interaction. A also recommends retaining it where
possible in policy assumptions. Thus this may be a guideline/required-field
boundary problem, not disagreement that the wordplay exists. A nonasserted
reading can still be required to remain recoverable in a translation. The
current response format lets these questions be conflated. Do not resolve the
dispute by declaring this author's coactivation proposal correct. Keep P06
blocked for consensus graph encoding until the preservation requirement is
clarified in a versioned task and evaluated again.

Both annotators also independently flag that P03 says only `на остановке`:
bus versus tram is unspecified. Our v2 author proposal says bus stop, as does
the old English candidate labeled valid. This is an additional author/baseline
defect, not a difference between A and B. No original source, gold fixture,
proposal, packet, or previous result has been edited to hide it.

Other useful confirmations and boundaries:

- P02: both keep recent visitor/occupancy defeasible and optional while
  preserving the observations. An inference route is not an asserted event.
- P05: both distinguish speech from formal closure and decline to certify
  institutional authority/invalidity. Corridor attachment remains a small
  unresolved reference issue; avoid unnecessary narrowing.
- P07: both preserve focused identity and distinguish agreement from signing.
- P08: both preserve competing attributions without asserting dishonesty or
  formal logical exclusivity. One separate optional row versus prose in
  alternatives is not disagreement.
- P10: both preserve envelope/box distinction and do not assert belief revision;
  B lists a possible causal link that A does not separately enumerate.

## Disposition

Record the bus-stop correction in a future version; generic stop is sufficient
without supplied narrowing context. Clarify required as an obligation on the
realization, separate from whether the source literally asserts a fact. The
clarification must not tell a blind annotator which case should receive which
answer. Preserve the distinction between recognizing a possible inference and
requiring a particular reading to remain available.

This collection supplies a real diagnostic pilot and a concrete guideline
issue. It does **not** close the independent human/different-model study,
annotation-time comparison, architecture choice, or automatic cross-constraint
agreement metric. The existing narrow evaluator cannot adjudicate these free
text commitments. No kappa, F1, or aggregate agreement score is manufactured.

Next: version the neutral required-field clarification and the author errata,
then collect an external/different-model review of the disputed boundary
before treating any graph pair as adjudicated gold. The other dispositions
are provisional compatible commitments, not independently certified gold.
