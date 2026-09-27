# Canonical FoM

Status: work in progress

Canonical FoM is the strict graph representation produced after parsing, reference resolution, macro expansion, and normalization of FoM Text.

It is designed for tooling rather than manual authoring.

The surface syntax and canonical graph intentionally serve different purposes.

## 1. Goals

Canonical FoM should be:

- explicit;
- deterministic;
- graph-native;
- scope-aware;
- lossless with respect to required FoM semantics;
- independent of source-language syntax;
- easy to validate;
- suitable for semantic diff.

Canonical FoM does not need to be pleasant to write by hand.

## 2. Top-level model

A canonical document contains separate collections for semantic and structural records:

```
document
  metadata
  nodes
  relations
  scopes
  statuses
  deltas
  constraints
  subgraphs
  patterns
  provenance
```

A JSON-like shape is recommended for interchange, but JSON itself is not part of the semantic definition.

## 3. References

Every addressable canonical object has an ID.

References are explicit objects conceptually equivalent to:

```json
{"ref": "anna"}
```

Implementations may use compact string references internally if the schema guarantees that literals and references cannot be confused.

Surface keywords and strings never become graph references accidentally.

## 4. Nodes

Canonical node shape:

```json
{
  "id": "anna",
  "kind": "node",
  "types": ["person"],
  "qualifiers": {}
}
```

`types` are structural classifications, not arbitrary encyclopedic properties.

Open semantic claims should normally be represented as relations.

## 5. Relations

Canonical relation shape:

```json
{
  "id": "r17",
  "kind": "relation",
  "family": "open",
  "predicate": "transfer",
  "args": {
    "source": {"ref": "anna"},
    "theme": {"ref": "book"},
    "recipient": {"ref": "bob"}
  },
  "qualifiers": {}
}
```

`family` may currently be:

```
open
identity
temporal
causal
inferential
semiotic
structural
```

### Hyperedges

N-ary relations are first-class. They are not decomposed into chains of binary edges merely for storage convenience.

### Positional arguments

FoM Text may use positional arguments.

Canonical FoM SHOULD use named argument roles whenever a Concept Contract or standard definition provides them.

If a predicate lacks a known role schema, canonicalization may preserve neutral structural roles:

```
arg0
arg1
arg2
```

without pretending that their semantic roles are known.

## 6. Anonymous surface expressions

Canonical FoM contains no truly anonymous semantic object.

An anonymous surface expression is reified during normalization with an internal generated ID.

Example:

```clojure
(dangerous honey)
```

may become conceptually:

```json
{
  "id": "_anon-17",
  "kind": "relation",
  "family": "open",
  "predicate": "dangerous",
  "args": {"arg0": {"ref": "honey"}}
}
```

Generated IDs are document-local implementation identifiers.

Semantic diff MUST NOT rely on generated-ID equality across independently canonicalized documents.

## 7. Scopes

Canonical scope shape:

```json
{
  "id": "anna-belief",
  "kind": "scope",
  "owner": {"ref": "anna"},
  "center": null,
  "imports": [{"ref": "reality"}],
  "status_base": null,
  "inherit_mode": "none"
}
```

Reference accessibility and status inheritance are separate.

A scope may import graph material without inheriting its truth/status.

## 8. Status records

ACCEPT / REJECT are represented explicitly.

```json
{
  "id": "_status-12",
  "kind": "status",
  "scope": {"ref": "anna-belief"},
  "value": "accept",
  "content": {"ref": "_anon-17"},
  "qualifiers": {
    "certainty": "plausible"
  }
}
```

Canonical FoM preserves effective:

```
ACCEPT
REJECT
UNCOMMITTED
```

UNCOMMITTED is normally absence of a status record in a non-inheriting scope.

In an overlay/inheriting scope, explicit UNCOMMITTED is also permitted as a structural shadow/tombstone that masks an inherited ACCEPT or REJECT without changing the parent scope.

Therefore canonical status records may use `accept`, `reject`, or explicit `uncommitted` when inheritance semantics requires it.

## 9. Identity

Identity is represented as semantic content, not automatically as physical graph-node merging.

```json
{
  "id": "id-1",
  "kind": "relation",
  "family": "identity",
  "predicate": "same-as",
  "args": {
    "left": {"ref": "person-a"},
    "right": {"ref": "person-b"}
  }
}
```

Whether this identity is accepted depends on scope status.

Global graph unification is only an optional optimization when no semantically relevant scope distinguishes the referents.

## 10. Subgraphs

Canonical subgraph shape:

```json
{
  "id": "gloves-reunited",
  "kind": "subgraph",
  "members": [
    {"ref": "r31"},
    {"ref": "r32"}
  ]
}
```

Subgraph membership does not imply ACCEPT.

## 11. Patterns and bindings

Canonical pattern shape:

```json
{
  "id": "student-read",
  "kind": "pattern",
  "variables": ["?x"],
  "where": [{"ref": "_anon-41"}],
  "bindings": [],
  "require": [{"ref": "_anon-42"}],
  "accessibility": {}
}
```

Variables are structural placeholders, not graph nodes.

Canonicalization alpha-renames variables when needed to prevent accidental capture.

Binding accessibility must remain explicit.

## 12. Deltas

Canonical delta shape:

```json
{
  "id": "correction",
  "kind": "delta",
  "role": "intended",
  "agent": {"ref": "mark"},
  "target_scope": {"ref": "anna-belief"},
  "operations": [
    {
      "op": "update",
      "target": {"ref": "status-17"},
      "changes": {
        "certainty": {
          "from": "high",
          "to": "low"
        }
      }
    }
  ]
}
```

Core operations:

```
add
remove
update
connect
disconnect
identify
activate
deactivate
```

`identify` creates or changes semantic identity status. It does not require destructive physical node merging.

## 13. Constraints

Canonical constraint shape:

```json
{
  "id": "sister-fate",
  "kind": "constraint",
  "operator": "fixed-unknown",
  "target": {"ref": "_anon-91"},
  "strength": "required",
  "parameters": {}
}
```

Constraint operators may come from the standard library or declared extensions.

A canonical validator must know the semantics of every constraint operator used in a document.

Unknown constraint operators are validation errors unless an extension schema is explicitly available.

## 14. Temporal relations

World-time relations, discourse order, and reader-trajectory order must not be collapsed into one generic `before` relation.

Canonical temporal relations carry an explicit domain or typed predicate.

Example:

```json
{
  "id": "t1",
  "kind": "relation",
  "family": "temporal",
  "predicate": "before",
  "args": {
    "left": {"ref": "event-a"},
    "right": {"ref": "event-b"}
  },
  "qualifiers": {
    "domain": "world-time"
  }
}
```

## 15. Provenance

Source provenance is not semantic content but should be preservable.

Possible provenance includes:

- source file and span;
- macro expansion origin;
- generated/internal ID origin;
- extractor source signal;
- realization source graph object.

Provenance must not affect semantic equivalence unless a constraint explicitly refers to it.

## 16. Canonical ordering

Serialization order is not semantic.

For stable files, implementations SHOULD sort:

1. explicit user IDs lexicographically;
2. generated IDs by deterministic canonicalization order;
3. map keys lexicographically.

This is a serialization convention, not graph meaning.

## 17. Normalization invariants

After canonicalization:

- every graph reference resolves;
- every variable is bound;
- no surface-only scope shorthand remains;
- every anonymous semantic expression is reified;
- every registered macro is expanded;
- positional roles are normalized where known;
- scope statuses are explicit;
- status inheritance is explicit;
- binding accessibility is explicit;
- unknown semantic ambiguity remains unresolved unless a semantic rule resolved it.

## 18. What canonicalization must not do

Canonicalization must not:

- add world knowledge;
- resolve an ambiguous pronoun from plausibility alone;
- turn uncommitted status into REJECT;
- convert typical knowledge into entailment;
- collapse de se into de re;
- globally merge scope-relative identities;
- strengthen certainty;
- resolve FIXED_UNKNOWN;
- disclose information earlier than allowed.

## 19. Diff implications

Canonical IDs generated independently are not semantic identifiers across documents.

Semantic diff therefore matches graph structure using:

- explicit IDs where provenance establishes continuity;
- predicate/role structure;
- scope;
- constraints;
- Concept Contract equivalence/refinement;
- binding structure.

Canonical FoM is a normalized graph, not a content-addressed hash tree.


## 20. Overlay status resolution

For scopes with status inheritance, effective status resolution is:

```
explicit local status/shadow
    overrides
selected inherited status
    otherwise
UNCOMMITTED
```

An explicit local `uncommitted` record masks inherited status.

If multiple inherited bases provide incompatible statuses and no precedence rule is declared, canonicalization must preserve the conflict rather than choose one.

Constraint inheritance is independent from status inheritance and defaults to none.
