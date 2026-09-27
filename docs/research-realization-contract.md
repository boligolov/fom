# Realization contract and licensed invention

Status: research note

FoM defines a space of valid realizations rather than one target sentence.

A realization is valid when its extracted meaning satisfies the source constraints for the target audience/context.

The preservation dimensions need operational definitions.

## 1. PRESERVE_REFERENT

Preserve the semantic object(s) referred to.

Example:

```
source refers to person-A
target wording may change
target must still resolve to person-A
```

This does not require preserving the same lexical form.

A pronoun, name, description, gesture, or icon may all preserve referent if the reference conditions remain valid.

## 2. PRESERVE_FUNCTION

Preserve what a signal fragment does in the communication.

Examples:

- functions as a warning;
- carries the second reading of a pun;
- creates contrast;
- acts as evidence rather than direct assertion;
- hides a coded meaning from outsiders;
- marks a quote as an echo of another speaker;
- delays disclosure.

FUNCTION is about the semiotic/pragmatic role, not the literal surface.

A different target-language construction may preserve function.

## 3. PRESERVE_EFFECT

Preserve the intended receiver/shared-state transformation under the target audience model.

Examples:

- increase confidence in P;
- create suspense;
- make two readings co-active;
- produce cautious hope;
- make a threat socially salient;
- leave a question unresolved.

This is an intended/expected effect, not a guarantee about an actual human receiver.

Therefore:

```
PRESERVE_EFFECT
!=
observed actual effect must be identical
```

## 4. PRESERVE_FORM

Preserve signal-level structure when that structure itself matters.

Examples:

- exact quotation;
- rhyme;
- acrostic;
- alliteration;
- pun locus;
- acronym;
- iconic word order;
- repeated wording;
- deliberate grammatical error.

FORM may be preserved:

- exactly;
- structurally;
- functionally analogous.

The required mode must be constrained explicitly.

## 5. Dimensions may conflict

A literal translation may preserve FORM while losing FUNCTION.

A free adaptation may preserve EFFECT while changing FORM.

FoM therefore must not collapse these dimensions into one "faithfulness" score.

## 6. Realization freedom

Useful levels:

```
FIXED
CONSTRAINED
FREE
```

These apply to semantic choices or realization slots, not necessarily whole documents.

### FIXED

Choice must not vary in a valid realization.

### CONSTRAINED

Variation is allowed within explicit semantic limits.

### FREE

The realization may choose compatible detail, subject to global constraints.

## 7. Unspecified is not automatically free

A crucial rule:

> Absence from FoM does not by itself license invention.

A detail may be absent because:

- it is irrelevant;
- it is unknown;
- it is intentionally hidden;
- it is outside current representational resolution;
- it is free.

Therefore licensed invention needs either:

- an explicit FREE/CONSTRAINED slot;
- a standard realization-default rule;
- a target-language requirement whose resolution is proven semantically inert;
- another explicit license.

## 8. Target-language obligatory distinctions

Languages may force distinctions not present in source FoM.

Examples may include:

- grammatical gender;
- number;
- evidential marking;
- politeness/honorific level;
- definiteness;
- tense/aspect;
- social relation encoded in address forms.

A realizer must not silently turn a required grammatical choice into a new semantic claim.

## 9. Resolution strategy

When the target language forces an unrepresented distinction, try in this order:

1. find a natural construction that avoids resolving it;
2. preserve ambiguity/unknown through paraphrase;
3. use a grammatically required form whose distinction is demonstrably non-semantic in context;
4. choose a value only if the FoM marks the dimension FREE/CONSTRAINED;
5. otherwise report that full realization under the requested constraints is impossible.

This is especially important for FIXED_UNKNOWN.

## 10. Example: unknown gender

Suppose FoM contains:

```
person X
gender(X) = FIXED_UNKNOWN
X arrived yesterday
```

A target language might require gender agreement in the most direct past-tense construction.

An invalid realization chooses a gender and thereby makes it recoverable.

A valid realizer should prefer a construction that avoids the distinction if available.

Thus grammatical convenience never overrides FIXED_UNKNOWN.

## 11. Realization-only defaults

Some details may be needed to make a signal well-formed but should not become required meaning.

Examples:

- article choice where it carries no relevant discourse distinction;
- punctuation;
- harmless word-order choice;
- conventional connective required by the target language.

These can be classified as:

```
REALIZATION_DEFAULT
```

A realization default is licensed only while semantic diff shows no required dimension changed.

## 12. Invention audit

After realization, extraction/diff should classify added material:

```
REQUIRED
LICENSED
UNLICENSED
```

A detail is LICENSED only if:

- compatible with source;
- permitted by freedom/default rules;
- does not resolve protected unknowns;
- does not alter required reference;
- does not alter required inference space;
- does not violate disclosure;
- does not introduce a new salient frame/evaluation;
- does not change required social or affective state.

## 13. Background world knowledge

World knowledge may help select a natural realization.

It must not be promoted silently to source meaning.

Example:

FoM:

```
bird on branch
```

World knowledge may help choose a natural verb such as "perched" only if that verb does not add an unsupported posture/state distinction relevant to the target task.

If "perched" becomes meaningful evidence later, the invention is no longer semantically inert.

## 14. Function-preserving invention

Sometimes invention is required to preserve meaning.

A pun may not transfer literally.

The realizer may invent a different lexical construction if:

- the required readings remain;
- their coactivation remains;
- the same intended effect/trajectory remains;
- no fixed content changes.

Thus licensed invention can be more faithful than literal preservation.

## 15. Current validation model

Conceptually:

```
candidate signal
    -> extract FoM'
    -> semantic diff(source, FoM')
    -> evaluate source constraints
    -> PASS / WARN / FAIL
```

No single similarity score decides validity.

## 16. Conclusion

The realization contract is:

```
preserve required semantic invariants
+
respect uncertainty/disclosure
+
preserve required semiotic function/effect
+
allow only licensed invention
```

The key principle is:

> Do not force the source FoM to answer distinctions that only the target language asks.
