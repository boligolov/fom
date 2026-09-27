# FoM standard macros

Status: work in progress

FoM Text macros are ergonomic surface constructs that expand deterministically into Core structures.

A macro is not a semantic primitive.

A normative macro must define:

1. syntax;
2. preconditions;
3. expansion;
4. validation;
5. interaction with scope and constraints.

This document separates macros whose semantics are currently clear from those still under research.

## 1. SELF

Surface:

```clojure
(self)
```

Precondition: a current scope with `:center`.

Expansion: reference to the current scope's center.

Failure: using `self` without a center is invalid.

## 2. UNKNOWN

Surface:

```clojure
(unknown P)
```

Meaning: the relevant scope is constrained to remain uncommitted about P at that state.

Expansion:

```
CONSTRAINT status(P, current-scope) = UNCOMMITTED
```

UNKNOWN is stronger than simple absence of ACCEPT/REJECT because the uncommitted state is itself meaningful.

## 3. FIXED-UNKNOWN

Surface:

```clojure
(fixed-unknown P)
```

Meaning:

- P is unresolved in the relevant source state;
- valid interpretation/realization must not resolve P within the constraint's domain.

Expansion: a CONSTRAINT over status/recoverability rather than a new status value.

FIXED-UNKNOWN does not mean that P is unknowable in reality.

## 4. AMBIGUITY

Surface:

```clojure
(ambiguity
  {:target ref-slot
   :candidates [ivan petr]})
```

Expansion: a CONSTRAINT preserving the candidate interpretation set and preventing unauthorized resolution.

A later DELTA may legitimately resolve the ambiguity.

## 5. PRESUPPOSE

Surface:

```clojure
(presuppose P)
```

Expansion:

- create/reference the relevant pre-message state scope/checkpoint;
- require ACCEPT(P) or an explicitly weaker licensed status in that pre-state;
- mark P as not introduced solely by the headline assertion.

Presupposition therefore modifies the modeled prior state, not just current propositional content.

The exact pre-state must be explicit in canonical form.

## 6. AGAIN

Surface:

```clojure
(again P)
```

Expansion conceptually requires:

1. a current instance/state satisfying P;
2. a distinct prior instance/state satisfying P;
3. TEMPORAL(prior, current) = BEFORE;
4. the prior instance is presupposed rather than newly asserted unless context overrides this contract.

AGAIN operates on the complete P subgraph.

Therefore:

```
AGAIN(NOT P) != NOT(AGAIN P)
```

## 7. ALMOST

Surface:

```clojure
(almost P)
```

Normative core:

1. P is not fully attained in the relevant scope;
2. the actual state is contextually close to the satisfaction boundary of P on a relevant scale.

Expansion requires a scale interface.

If the relevant scale cannot be identified from a Concept Contract or explicit argument, canonicalization must preserve an unresolved scale slot rather than inventing one.

ALMOST must never be implemented as "P with low certainty".

## 8. POSSIBLE

Surface:

```clojure
(possible P)
```

Required parameters after normalization:

- modal base;
- accessibility relation;
- evaluation scope.

Expansion:

```
EXISTS accessible scope s:
    ACCEPT(s, P)
```

If the modal base is ambiguous and meaning depends on it, FoM must preserve that ambiguity.

## 9. NECESSARY

Surface:

```clojure
(necessary P)
```

Expansion:

```
FOR EACH relevant accessible scope s:
    ACCEPT(s, P)
```

The domain of relevant scopes is part of the meaning.

## 10. INFERENCE

Surface candidate:

```clojure
(inference
  {:evidence E
   :conclusion P
   :strength :plausible})
```

Expansion: one or more INFERENTIAL-family relations plus qualifiers.

Inference never implies world causation unless a separate CAUSAL relation is present.

## 11. MAPPING

Surface candidate:

```clojure
(mapping
  {:source S
   :target T
   :target-explicitness :inferable})
```

Expansion: addressable correspondence relations between source and target structures, plus any explicitness/recoverability constraints.

MAPPING is used for metaphor, allegory, symbolism, iconicity, and related structure-preserving correspondences.

## 12. DISCLOSURE

Surface:

```clojure
(disclosure P
  {:before cp7 :prohibited
   :after cp7 :required})
```

Expansion: trajectory-position constraints over recoverability/availability of P.

DISCLOSURE constrains when information may become recoverable, not merely when a literal sentence may occur.

## 13. PRESERVE

Surface:

```clojure
(preserve X
  {:aspect :inference-path
   :strength :required})
```

Expansion: validation CONSTRAINT over realization/diff.

PRESERVE does not itself add semantic content.

## 14. REINTERPRET

Surface candidate:

```clojure
(reinterpret
  {:from interpretation-a
   :to interpretation-b})
```

Expansion: DELTA over interpretation/status/salience.

There is no primitive REINTERPRET operation.

At minimum, expansion must specify which statuses or preference qualifiers change.

A bare `reinterpret X` without a defined state change should be rejected.

## 15. FOR-EACH

Surface candidate:

```clojure
(for-each [?x]
  (where (student ?x))
  (require (read ?x book)))
```

Expansion: PATTERN + VARIABLE + BINDING + universal CONSTRAINT over the binding domain.

FOR-EACH does not itself assert that the binding domain is non-empty.

## 16. EXISTS

Surface candidate:

```clojure
(exists [?x]
  (where (student ?x))
  (require (read ?x book)))
```

Expansion: PATTERN + existential CONSTRAINT requiring at least one satisfying binding.

## 17. Experimental macros

The following should remain non-normative until their semantics are better specified:

```
generic
habitual
very
barely
too
enough
```

They may be used in research examples but a conforming canonicalizer is not yet required to expand them.

## 18. Macro provenance

Canonicalization should retain provenance indicating which canonical structures originated from a macro.

This is useful for:

- debugging;
- round-trip pretty-printing;
- semantic diff explanation.

Macro provenance is not itself meaning unless explicitly constrained.
