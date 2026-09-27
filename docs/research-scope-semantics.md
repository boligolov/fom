# Scope semantics and inheritance

Status: research note

SCOPE is used for beliefs, hypotheticals, fiction, plans, expectations, normative models, reader states, and other perspective-relative graph states.

The key finding in this note is:

> reference visibility and semantic-status inheritance must be separate.

## 1. The problem

Suppose reality contains:

```
ACCEPT married(ivan, anna)
```

and Ivan's belief scope contains a mistaken model.

The belief scope must be able to refer to the same Ivan and Anna nodes, but it must not automatically inherit reality's ACCEPT statuses.

Therefore lexical/graph accessibility is not truth inheritance.

## 2. Scope links

The surface syntax reserves:

```
:parent
:imports
:inherits-status-from
:inherit-mode
:center
```

### parent

Structural nesting / provenance.

It does not imply status inheritance.

### imports

Makes external IDs/subgraphs available for reference/model reuse.

### inherits-status-from

Explicitly identifies another scope whose statuses form a base layer.

### inherit-mode

Candidate modes:

```
:none
:overlay
:selective
```

`:none` — no status inheritance.

`:overlay` — inherit base statuses except explicit local overrides.

`:selective` — inherit only explicitly named classes/subgraphs.

## 3. Default rule

The safe default is:

```
reference visibility: available through graph/import rules
status inheritance: none
```

This prevents accidental leakage of reality into belief, fiction, hypothetical, or attributed scopes.

## 4. Overlay scopes

Overlay inheritance is useful for:

- counterfactual worlds;
- nearby hypothetical alternatives;
- successive reader-state checkpoints;
- plans derived from a current model.

Example:

```clojure
(scope counterfactual-1
  {:imports [reality]
   :inherits-status-from reality
   :inherit-mode :overlay}

  (reject
    (open door))

  (accept
    (closed door)))
```

The scope means "reality, except for explicit overrides" only because overlay inheritance is explicitly requested.

## 5. Belief scopes

A belief scope usually imports referents but does not inherit reality's truth statuses.

```clojure
(scope alice-belief
  {:owner alice
   :imports [reality]
   :inherit-mode :none}

  (accept
    (flat earth)))
```

## 6. Nested theory of mind

For:

```
Mark believes that Anna believes P
```

the Anna-belief scope may be represented inside Mark's model without copying world entities.

The nested scope imports the relevant referents and is attributed/modelled by Mark.

Its content is not automatically asserted in Mark's own belief scope unless separately represented.

## 7. CENTER / SELF

A scope may designate a center:

```
:center oleg
```

The standard `(self)` macro resolves to this center.

This allows de se representation without requiring a new semantic primitive.

## 8. Status conflicts

A child overlay may override inherited status.

A canonical implementation should distinguish:

```
inherited ACCEPT(P)
local REJECT(P)
```

from destructive mutation of the parent scope.

The resolved view of the child may reject P while provenance still records that the base accepted it.

## 9. Constraints and inheritance

Constraints should not automatically inherit with semantic statuses unless their type explicitly declares inheritance behavior.

For example, a realization-level disclosure constraint may govern a whole trajectory independently of one belief scope.

## 10. Current conclusion

SCOPE should be modeled as an overlay-capable perspective with separate channels for:

- reference accessibility;
- status inheritance;
- binding accessibility;
- ownership/attribution;
- center/self.

This avoids both graph copying and accidental truth leakage.


## 11. Masking inherited status

Overlay semantics exposes an important case.

Base scope:

```
ACCEPT P
```

Child scope may need:

```
neither ACCEPT P nor REJECT P
```

This is different from simply omitting a local status, because omission would continue to inherit ACCEPT(P).

Therefore canonical overlay representation needs an explicit way to shadow an inherited status.

Conceptually:

```
MASK inherited status for P
```

or:

```
local effective status = UNCOMMITTED
```

without modifying the parent.

This is structural overlay machinery, not a new semantic truth value.

### Recommended canonical behavior

Status records may use:

```
accept
reject
uncommitted
```

where explicit `uncommitted` is allowed when it acts as an overlay tombstone/shadow.

Outside inheritance contexts, uncommitted normally remains represented by absence unless the uncommitted state is itself constrained/meaningful.

## 12. Conflict resolution order

For an overlay scope, effective status should be resolved in this order:

1. explicit local status/shadow;
2. explicitly selected inherited base status;
3. otherwise UNCOMMITTED.

A local ACCEPT or REJECT overrides the inherited status.

A local explicit UNCOMMITTED masks the inherited status.

No child operation mutates the parent.

## 13. Multiple inherited bases

Multiple status bases create possible conflicts.

FoM should not silently choose one.

If:

```
base-A ACCEPT P
base-B REJECT P
```

and neither has declared priority, the child should preserve a source-conflict state rather than pick a winner.

Priority/precedence, if intended, must be explicit.

## 14. Constraint inheritance

Constraints must not automatically follow status inheritance.

Different constraint classes have different propagation semantics.

Safe default:

```
constraint inheritance = none
```

A constraint may explicitly declare:

```
:applies-to [scope-a scope-b]
:propagation :descendants
:propagation :trajectory
```

or another defined policy.

This avoids accidentally importing:

- epistemic restrictions;
- disclosure rules;
- local social rules;
- realization constraints;

into unrelated child scopes.

## 15. Updated conclusion

SCOPE overlay semantics requires a distinction between:

```
no local status record
explicit local UNCOMMITTED shadow
local ACCEPT
local REJECT
```

This remains compatible with the five-part Core but must be represented in the canonical graph.
