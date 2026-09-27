# Canonicalization and normal forms

Status: research note

Canonicalization must make FoM deterministic enough for tooling without silently changing meaning.

The central rule is:

> Normalize representation, not semantics.

A canonicalizer may remove syntactic accidents. It must not freely replace one semantically related graph with another merely because classical logic or world knowledge considers them equivalent.

## 1. Three kinds of equivalence

FoM needs to distinguish:

### 1.1 Surface equivalence

Two FoM Text forms differ only in syntax.

Example:

```clojure
(scope s
  (accept P))
```

vs:

```clojure
(accept s P)
```

These SHOULD canonicalize identically.

### 1.2 Structural semantic equivalence

Two forms are equivalent by an explicitly defined Core/Concept rule.

Example:

```
AFTER(B, A)
```

vs:

```
BEFORE(A, B)
```

if TEMPORAL defines AFTER as the exact inverse of BEFORE.

These MAY canonicalize identically.

### 1.3 Contextual / inferential equivalence

Two forms can license the same conclusion but differ in:

- focus;
- presupposition;
- explicitness;
- inference path;
- source;
- trajectory;
- affect.

Example:

```
not(all P)
```

and a logically equivalent existential formulation.

These SHOULD NOT automatically canonicalize to one structure.

They may compare as equivalent along selected semantic dimensions during semantic diff.

## 2. Alpha-renaming

Bound variable names are non-semantic.

```
?x
?student
?foo
```

may normalize to canonical lexical names such as:

```
?v0
?v1
?v2
```

within each binding environment.

Alpha-renaming MUST preserve binding accessibility and avoid capture.

## 3. Map and set ordering

Map key order is non-semantic and SHOULD be canonicalized.

Unordered semantic collections may be sorted only when the schema declares them unordered.

Vectors remain ordered by default.

Never sort:

- discourse sequences;
- temporal sequences;
- ordered alternatives;
- signal fragments;
- ranked candidates;

unless their contract says order is irrelevant.

## 4. Symmetric relations

A relation may normalize argument order only if its Concept Contract or Core family declares it symmetric.

Example:

```
IDENTITY(A, B)
```

can use a deterministic argument orientation for serialization, while retaining scope-relative identity semantics.

But:

```
loves(A, B)
```

must never be reordered unless LOVES were explicitly declared symmetric, which it normally is not.

## 5. Inverse relation normalization

Special families may define exact inverses.

Example:

```
AFTER(B, A)
-> BEFORE(A, B)
```

This is safe only when the inverse relation is definitionally exact.

The same principle may apply to:

```
contains / during
started-by / starts
```

It must not be generalized to merely related predicates.

## 6. Negation

Canonicalization MUST preserve explicit operator topology.

Do not automatically apply:

- double-negation elimination;
- De Morgan transformations;
- quantifier-negation transformations;
- contraposition.

Even when truth-conditionally equivalent under classical logic, these transformations can alter:

- presupposition;
- focus;
- discourse structure;
- recoverability;
- conventional form;
- inference route.

A later logic engine may reason over these structures without replacing the source graph.

## 7. Scope overlays

Canonical storage SHOULD preserve:

```
base scope
local overrides
inheritance mode
```

rather than materializing every inherited ACCEPT/REJECT edge into the child scope.

A resolved scope view is derived.

Why:

- provenance is preserved;
- updates remain local;
- parent changes can be propagated;
- inherited vs local status remains distinguishable.

Therefore:

```
canonical representation != fully materialized resolved view
```

## 8. Identity

Canonicalization MUST NOT globally merge references merely because one scope accepts IDENTITY.

A deterministic serialization may orient the identity relation, but scope-relative referents remain addressable.

## 9. Macros

Normative macros SHOULD expand before canonical semantic storage.

Example:

```
(again P)
```

expands to its canonical presupposition/current-instance/temporal structure.

Macro provenance SHOULD remain attached.

Pretty-printers may reconstruct a macro only when the canonical structure unambiguously matches the macro contract.

## 10. Concept refinement

Canonicalization MUST NOT automatically refine open predicates into ontology graphs.

For example:

```
persuade(A,B,P)
```

should not always expand to a detailed causal/belief-change graph.

Why:

- source resolution may intentionally be coarse;
- refinement can introduce irrelevant addressable structure;
- Minimum Sufficient Resolution would be violated.

Refinement equivalence belongs to semantic diff / ontology reasoning, not basic canonicalization.

## 11. Units and values

Values MAY normalize to canonical units when:

- conversion is exact or declared sufficiently precise;
- the original precision is preserved;
- the unit choice itself is not semantically meaningful.

Example:

```
100 cm
1 m
```

may share a normalized quantity value.

But source precision and wording may remain in provenance/qualifiers.

## 12. Generated IDs

Generated IDs are serialization aids, not semantic identity.

Requirements:

- deterministic within one canonicalization run;
- stable under non-semantic map ordering changes if practical;
- never used as the sole basis for cross-document semantic matching.

A simple initial strategy is deterministic traversal IDs:

```
_anon-0001
_anon-0002
...
```

A future implementation may add structural fingerprints, but fingerprints must not become graph identity automatically.

## 13. Duplicate anonymous structure

Two structurally identical anonymous expressions MUST NOT automatically collapse into one object.

Example:

```
John said P.
Mary said P.
```

The proposition-like content may be structurally identical, but occurrences/provenance may matter.

Deduplication is allowed only when identity of the semantic object itself is licensed.

## 14. Canonical serialization

Stable serialization SHOULD:

1. sort top-level record collections by canonical serialization ID;
2. sort map keys;
3. normalize exact inverse relations where defined;
4. alpha-normalize variables;
5. preserve meaningful list/vector order;
6. preserve scope overlays rather than materializing them;
7. include macro/source provenance in a non-semantic metadata section.

## 15. Semantic diff after canonicalization

Canonicalization reduces irrelevant structural noise.

Semantic diff still must handle:

- different graph decompositions;
- Concept Ontology refinements;
- licensed invention;
- different but valid inference routes;
- audience-dependent realizations.

Thus:

```
canonical equality => strong evidence of equivalence

canonical inequality != semantic inequality
```

## 16. Current conclusion

FoM should avoid one giant "normal form of meaning".

Instead it should have:

```
surface normalization
+
Core structural normalization
+
optional family-specific exact normalization
+
semantic diff for deeper equivalence
```

This prevents the canonicalizer from destroying the very distinctions FoM is designed to preserve.
