# Architectural pilot: interpretation and coverage audit

## Decision

**Ownership separation is feasible on the seven existing gold pairs. Prefer
neither architecture yet.** This prototype gives a smaller FoM-owned layer,
not a smaller total representation or demonstrated annotation saving.

The standalone and layered paths both detect 7/7 frozen target labels; their
full dimension/status signatures also agree. All 21 source-self controls are
empty. Of 45 source canonical records, 35 move to the carrier and 10 remain
in the overlay. Total canonical records stay 45. The carrier-only path retains
2/7 target labels: attribution and certainty. That is expected when ordinary
reports and epistemic commitments belong to the carrier.

The independent serialized representations occupy 2,571 UTF-8 bytes for the
existing FoM sources versus 3,356 bytes for compact layered JSON. JSON field
names and different formatting make this a format-specific observation, not
an intrinsic complexity metric. Still, no storage reduction was observed.

This is an engineering feasibility result. The layered fixtures were manually
authored with the old gold visible; the adapter lowers to FoM and uses the
same diff engine. Parity is therefore not independent validation of meaning,
an extraction benchmark, or evidence of better detection than standalone FoM.
The new status evaluator is not used to pretend that it can execute all these
preservation constraints: this pilot compares the existing semantic diff.

## Audit of all ten corpus items

| Case | Carrier / overlay boundary | Source coverage and unresolved issue |
| --- | --- | --- |
| unknown-owner | Carrier: umbrella, location, potential owner relation. Overlay: fixed unknown. | Existing gold tracks ownership, but the text leaves the identity of the person who **left** the umbrella unknown. These are not equivalent. Wetness and the explicit history of failed discovery are omitted. Parity preserves this annotation defect. |
| source-attribution | Carrier: report, speaker, closure, narrator commitment. No overlay needed for the current target. | Existing gold omits the explicit absence of other confirmation. It encodes the report twice, as a named relation and a positional application inside ACCEPT; both representations retain that baseline choice. Do not credit FoM uniquely for ordinary attribution. |
| inference-route | Carrier: evidence and proposed visitor content; overlay: evidence-for link. | Existing gold omits Sergei's silence and table location. More seriously, corrupted gold retains the warm-chair evidence that the corrupted text removes. It tests a deleted inference edge and added assertion, not a complete annotation of that text. The evidence/conclusion link could also belong to a discourse-capable carrier; its present ownership is provisional. |
| delayed-reveal | Carrier: location of letter; overlay: receiver checkpoints and disclosure window. | Existing gold omits the empty envelope, Lena's mistaken conclusion, and several event-time facts. Reader order must remain distinct from the carrier's event time. This is a promising boundary, not full narrative coverage. |
| common-tongue | Carrier: two reading graphs; overlay: required coactivation. | The two gold readings are coarse zero-argument predicates. They do not establish whether an independently produced translation supports the pun. A preserved coactivation marker alone is insufficient evidence of preserved reader effect. |
| uncertain-train | Carrier: departure and epistemic commitment. No overlay needed. | Existing gold omits the contribution of 'already'. Ordinary certainty is already within the intended carrier scope; moving it to an overlay would manufacture an advantage. |
| contrastive-focus | Carrier: Peter's refusal; overlay: attention state. | Existing gold omits the contract and everyone else's agreement. It substitutes high/low salience for contrastive focus; these are not generally equivalent. This pilot checks that proxy only. |
| failed-declaration | Candidate split: carrier for utterance/participants/continued discussion; overlay for attempted vs actual social transition. | No executable gold pair exists. Felicity/authority and the social-state outcome need an explicit contract and independent annotation. Not scored as success or failure. |
| conflicting-sources | Candidate split: carrier for attributed claims and cognizers; overlay for the requirement not to resolve the disagreement. | No executable gold pair exists. Do not duplicate ordinary attribution in FoM. The precise exclusivity and resolution commitments must be established before scoring. Not scored. |
| exact-note | Carrier for note, quoted signal and refusal interpretation; overlay for required form preservation. | No executable gold pair exists. The supplied 'valid' English translates 'нет' to 'no': original graphemes vs translated quotation vs one-word form must be distinguished before a form-preservation benchmark is coherent. Not scored. |

The seven gold pairs are controlled feature fixtures, not complete semantic
annotations of their source texts. They cannot establish whole-text
expressiveness. The three missing cases are not silently filled in using the
same author and counted as independent confirmation.

## What prior art changes

UMR's document schema explicitly includes cognizers/modal commitments and
attributed speech. Those observations motivate keeping certainty and reporting
in the carrier. Its temporal dependencies concern event/time relations; this
prototype keeps receiver disclosure checkpoints separate. This is a proposed
division of responsibility, not a claim that UMR cannot represent more.

References checked for this pilot:
- [UMR document-level schema](https://umr4nlp.github.io/web/UMRSchemaPages/Document-Level-Graph.html)
- [Bonn et al. 2024](https://aclanthology.org/2024.lrec-main.229/)

Our carrier uses the baseline's open predicate names and roles, not validated
UMR senses, roles, or modal labels. It has no official UMR parsing/conformance
test. No conclusion about actual UMR annotation cost is justified.

## Next decision gate

1. Freeze full text-level commitments, including the omissions and proxy
   mismatches above, before extending gold or claiming more coverage.
2. Resolve the owner/leaver and quoted-form contracts; preserve the original
   corpus and version any revised annotation targets.
3. Have genuinely independent annotators produce both representations from
   blinded source/context packets. Measure time and cross-constraint agreement.
4. Add real valid-paraphrase controls and the three missing corruption pairs.
5. Validate a real UMR adapter on that subset before deciding its ownership
   boundary. Adopt layering only if the total burden/agreement gate succeeds.

Do not rewrite the main FoM spec or freeze a production carrier interface from
this pilot. The experiment identifies an implementable boundary and the
specific evidence still missing to choose it.
