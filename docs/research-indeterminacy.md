# Uncertainty and indeterminacy provenance

Status: research note

FoM uses ACCEPT / REJECT / uncommitted status, but the reason for non-commitment matters.

A single generic UNKNOWN flag is insufficient for semantic diff.

## 1. Distinct sources of non-commitment

### 1.1 Epistemic ignorance

The proposition has a determinate truth value in the modeled world, but the agent lacks enough evidence.

Example:

```
I do not know whether Ivan is home.
```

Suggested provenance:

```
:indeterminacy-source :missing-evidence
```

### 1.2 Unresolved reference

The signal contains a reference whose intended referent is not resolved.

Example:

```
Ivan told Petr that he was wrong.
```

Suggested provenance:

```
:indeterminacy-source :reference-ambiguity
```

### 1.3 Interpretation ambiguity

Several readings are licensed and one may be intended, but the available context does not determine which.

```
:indeterminacy-source :interpretation-ambiguity
```

This differs from deliberate multi-meaning, where multiple readings are intended simultaneously.

### 1.4 Vagueness

The world facts may be known, but a vague predicate has multiple admissible precisifications.

```
:indeterminacy-source :vagueness
```

### 1.5 Source conflict

Different sources/scopes support incompatible claims.

```
:indeterminacy-source :source-conflict
```

This is not the same as "no evidence".

### 1.6 Modal openness

Several future/possible alternatives remain live.

```
:indeterminacy-source :modal-openness
```

This is not necessarily ignorance. The modeled system itself may be non-settled.

### 1.7 Intentional concealment

The sender deliberately keeps content unresolved for the receiver.

```
:indeterminacy-source :withheld
```

This often combines with disclosure constraints.

### 1.8 Fixed unknown

The representation requires that an issue remain unresolved through a defined trajectory/domain.

```
:indeterminacy-source :fixed-unknown
```

FIXED_UNKNOWN is a constraint, not merely a provenance label.

### 1.9 Underspecification

The source meaning does not make a distinction because the distinction is irrelevant.

```
:indeterminacy-source :underspecified
```

This should not be "resolved" unless a realization is licensed to choose a FREE detail.

## 2. Multi-meaning is not indeterminacy

Deliberate multi-meaning is different:

```
A required
B required
coactivation required
```

There is no missing choice between A and B.

Therefore it should not be tagged as ambiguity merely because two readings exist.

## 3. Probability

Probability or confidence is not itself a source of indeterminacy.

These are separate axes:

```
source of uncertainty
confidence/degree
evidence/source
```

For example:

```
P plausible because evidence is incomplete
P disputed because sources conflict
P borderline because predicate is vague
```

may all have similar numeric confidence but radically different semantics.

FoM should avoid collapsing them.

## 4. Representation

No new Core primitive is required.

The provenance may be represented through:

- qualifiers on status/constraint records;
- relations to evidence/source/alternative scopes;
- explicit ambiguity/precisification structures;
- trajectory constraints.

A standard vocabulary is useful for diff/validation.

## 5. Semantic diff

Diff should compare not only whether a proposition remains unresolved, but why.

Examples:

```
source:
    unresolved due vagueness

realization:
    unresolved due missing factual information

=> CONTENT maybe similar
=> INDETERMINACY PROVENANCE changed
```

or:

```
source:
    deliberate ambiguity

realization:
    chooses one reading

=> ambiguity LOST
```

## 6. Current candidate vocabulary

```
:missing-evidence
:reference-ambiguity
:interpretation-ambiguity
:vagueness
:source-conflict
:modal-openness
:withheld
:fixed-unknown
:underspecified
```

This list is extensible and is not a closed ontology of all uncertainty.

## 7. Conclusion

FoM should treat uncertainty as multidimensional:

```
status
+ certainty
+ evidence
+ source
+ indeterminacy provenance
+ constraints on future resolution
```

This avoids using one UNKNOWN bucket for fundamentally different semantic situations.
