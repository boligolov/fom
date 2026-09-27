# Core relational operators

Status: research note

This note tests whether the current five special relation families are genuinely distinct:

```
IDENTITY
TEMPORAL
CAUSAL
INFERENTIAL
SEMIOTIC
```

The conclusion so far is that all five remain useful, but IDENTITY needs a refinement: semantic identity is not the same operation as unconditional graph-node merging.

## 1. IDENTITY

Identity answers whether two semantic references denote the same object within a relevant scope/model.

Example:

```
Clark Kent = Superman
```

This is meaningful content, so identity cannot be only an implementation detail.

However, identity may be scope-relative.

A mistaken belief may contain:

```
scope Alice-belief:
    REJECT IDENTITY(person-A, person-B)

reality:
    ACCEPT IDENTITY(person-A, person-B)
```

Therefore a canonical implementation MUST NOT always merge the two nodes globally.

### Current rule

IDENTITY has equivalence semantics within the scope in which it is accepted.

Physical graph unification is an optional optimization only when:

- identity is valid in every relevant scope;
- no message-relevant distinction depends on keeping references separate;
- no later delta needs to represent discovery/re-identification.

This replaces the earlier informal idea that IDENTITY always has graph-merging semantics.

## 2. TEMPORAL

Temporal relations model ordering and extent in a time model.

They cannot be reduced to ordinary open predicates if the engine is expected to reason about:

- inversion;
- transitivity;
- interval overlap;
- temporal consistency;
- anchoring.

TEMPORAL remains a special relation family.

## 3. CAUSAL

Causal structure is about the represented world/model.

```
A caused B
```

cannot be reduced to:

```
A happened before B
```

and cannot be reduced to:

```
A is evidence for B
```

A and B can be temporally ordered without causation, and evidence can support a causal claim without itself causing the event.

CAUSAL therefore remains distinct.

## 4. INFERENTIAL

Inferential structure belongs to a reasoning model.

```
E -> therefore P
```

does not assert that E caused P in the represented world.

Examples:

- smoke is evidence for fire;
- an empty chair is evidence that someone left;
- wording can support an implicature.

INFERENTIAL cannot be collapsed into CAUSAL.

## 5. SEMIOTIC

Semiotic relations connect signals/representations with what they mean, refer to, evoke, or reveal.

Examples:

```
word REFERS_TO entity
sentence EXPRESSES proposition
gesture SUGGESTS intention
symptom INDICATES condition
```

Some semiotic relations can also license inference, but representation is not identical to inference.

A proper name may refer to an entity without functioning as evidence that the entity exists.

A fictional signal may express a proposition inside fiction without asserting it in reality.

SEMIOTIC therefore remains distinct.

## 6. Result

No relation family currently reduces cleanly to another.

The more precise architecture is:

```
open semantic predicates
+
special relation/operator families:
    IDENTITY
    TEMPORAL
    CAUSAL
    INFERENTIAL
    SEMIOTIC
+
structural IR relations
```

The word "operator" should not imply that each family has only one predicate. TEMPORAL and SEMIOTIC are families with specialized semantics.
