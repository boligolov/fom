# FoM annotation guide

Status: pilot guide

This guide is intentionally shorter and stricter than the conceptual specification.

Its purpose is reproducible annotation, not maximal expressiveness.

## 1. First rule: annotate commitments, not possibilities

Annotate a semantic distinction only when the source/context requires it for interpretation or preservation.

Do not add a relation merely because it is plausible.

Bad:

```
source: "Anna entered the room."

annotation:
    tired(anna)
    came-from-work(anna)
    ...
```

unless those facts are licensed by the supplied context.

## 2. Minimum Sufficient Resolution

Use the coarsest predicate that preserves every required distinction.

Keep:

```
loves(anna, bob)
```

atomic unless the source requires internal components such as attachment, desire, care, commitment, etc. to be separately addressed.

Do not decompose for the sake of appearing precise.

## 3. Unknown stays unknown

Never resolve an ambiguity or missing fact by plausibility alone.

Use explicit uncertainty/ambiguity when the unresolved state matters.

If the source requires the uncertainty to survive realization, use FIXED_UNKNOWN or another appropriate preservation constraint.

## 4. Signal and referent are different

A word, phrase, gesture, quote, or other signal is not identical to what it denotes.

Create/address a SIGNAL object only when signal form or signal-to-meaning mapping matters.

Ordinary semantic content does not need a signal node for every word.

## 5. Attribution is not truth

```
Alice says P
```

does not imply:

```
reality ACCEPTS P
```

Represent source/report scope separately when attribution matters.

## 6. Evidence is not causation

Do not encode:

```
E CAUSES P
```

when the source only licenses:

```
E is evidence for P
```

Similarly, temporal precedence does not imply causation.

## 7. Belief scope does not inherit reality automatically

Belief, fiction, hypothetical, counterfactual, and source scopes may reuse the same referents without inheriting reality's ACCEPT/REJECT statuses.

Use explicit status inheritance only where the modeled scope is truly an overlay.

## 8. Distinguish absence from explicit uncommitted status

In a normal non-inheriting scope, absent status usually means unspecified.

In an overlay scope, explicit UNCOMMITTED/shadow is needed when inherited content must be masked without being rejected.

## 9. Do not smuggle the phenomenon into an opaque predicate

If annotating a joke, do not write:

```
(funny ...)
(joke ...)
```

as the explanation.

If annotating irony, do not use an opaque `ironic` predicate as the structure that proves irony.

Phenomenon labels may appear in comments, test names, or derived annotations, but the required meaning must survive their deletion.

## 10. Separate readings correctly

### Ordinary ambiguity

Use when one reading is intended but unresolved:

```
A OR B
```

### Deliberate multi-meaning

Use when both readings and their relation are intended:

```
A AND B
coactivation required
```

Do not encode deliberate multi-meaning as unresolved ambiguity.

## 11. Inference paths

Annotate an inference path only when its preservation matters.

If P is merely a reasonable consequence that has no communicative role, do not annotate it as required.

If the source relies on evidence E causing the receiver to infer P, represent:

```
E
INFERENTIAL relation
P
```

rather than making P explicit.

## 12. Presupposition

If content is treated as already established before the message, represent it in the appropriate prior state / presuppositional structure.

Do not simply add it to current asserted content.

## 13. Affect, stance, and salience

Annotate these only when supported by the signal/context and relevant to preservation.

Avoid mind-reading the author.

Examples that may justify annotation:

- explicit evaluation;
- conventional expressive;
- strongly structured narrative affect;
- contrastive focus essential to the utterance.

## 14. Intended vs generative-only structure

Do not annotate hidden authorial intentions as recoverable meaning merely because they produce a good explanation of the text.

If a latent intention is useful for generation but not recoverable by the target audience, keep it outside REQUIRED recoverable meaning.

## 15. Social acts

Distinguish:

```
attempted act
felicity conditions
actual social-state effect
```

Do not assume an utterance successfully creates an obligation, permission, declaration, etc. without the required context/authority.

## 16. Disclosure

Add trajectory/disclosure constraints only where timing changes meaning/effect.

Do not add checkpoints mechanically to every sentence.

When used, specify concrete addressable checkpoints rather than informal labels.

## 17. World knowledge

Use supplied or explicitly licensed background knowledge to interpret the source.

Do not turn typical world knowledge into semantic entailment.

Typical is not required.

## 18. Free realization detail

Absence from the annotation does not mean FREE.

Only mark detail FREE/CONSTRAINED when realization is allowed to choose it.

Unknown, irrelevant, hidden, and free are different.

## 19. Annotation order

Recommended workflow:

1. write a one-paragraph natural-language account of what must be preserved;
2. list unresolved/ambiguous information;
3. identify attribution/scopes;
4. identify required inference/disclosure/social effects;
5. choose Minimum Sufficient Resolution;
6. encode FoM;
7. run `fom check`;
8. inspect every added relation and ask: "What source evidence requires this?"

## 20. Stopping rule

Stop decomposing when every required distinction is addressable and further decomposition would not change:

- reference;
- scope/status;
- inference;
- disclosure;
- realization constraints;
- semantic diff.

A smaller valid graph is preferred to an elaborate speculative one.
