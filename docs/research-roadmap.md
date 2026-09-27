# Research roadmap

Status: active

This document tracks architectural questions that are not yet fully closed.

## Substantially resolved

### FoM ↔ Concept Ontology boundary

Current direction: Concept Ontology stores semantic contracts, not encyclopedic definitions.

See `concept-ontology.md`.

### Quantification / plurality

Current direction: structural PATTERN / VARIABLE / BINDING machinery plus constraints; collective readings use group nodes, distributive readings use bound patterns.

### Reference / binding

Current direction: distinguish mention, reference, identity, coreference, and bound/dependent reference. Binding accessibility is explicit.

### Core relation-family separation

Current direction: IDENTITY, TEMPORAL, CAUSAL, INFERENTIAL, and SEMIOTIC remain distinct specialized families.

See `research-core-operators.md`.

### Scope inheritance

Current direction: separate reference visibility from status inheritance; no implicit truth inheritance.

See `research-scope-semantics.md`.

## Active

### 1. Canonical FoM representation

Need to specify the strict graph form produced by FoM Text normalization.

Questions:

- node/relation record schema;
- hyperedge representation;
- scope-status storage;
- subgraph membership;
- binding environments;
- source maps;
- macro provenance;
- canonical IDs;
- stable serialization.

### 2. Macro standard library

Need normative expansions for:

- unknown / fixed-unknown;
- ambiguity;
- presuppose;
- almost;
- again;
- possible / necessary;
- generic;
- mapping;
- inference;
- disclosure;
- preserve;
- reinterpret.

A macro should not become a hidden second semantics.

### 3. Genericity

We know GENERIC != ALL and GENERIC != statistical majority.

Still open:

- default/normality semantics;
- exception structure;
- kind-level predication;
- audience/world-knowledge dependency.

### 4. Degree semantics

ALMOST has a useful general form:

```
target state not reached
+
contextually close on relevant scale
```

Still open:

- scale representation;
- multi-dimensional scales;
- "very", "barely", "too", "enough";
- contextual thresholds.

### 5. Modality

SCOPE + accessibility appears sufficient.

Still open:

- representation of modal bases;
- accessibility relation contracts;
- mixed deontic/epistemic readings;
- ability vs opportunity.

### 6. Temporal algebra implementation

A qualitative interval algebra is proposed.

Still open:

- interaction with uncertain scopes;
- recurring/habitual events;
- tense/deixis;
- duration and granularity;
- world-time vs narrative-time APIs.

### 7. Scope overlay semantics

Current design is explicit.

Still open:

- exact conflict-resolution rules;
- selective inheritance syntax;
- constraint inheritance;
- efficient resolved-view computation.

### 8. World knowledge in realization

Need a contract for when a realizer may use knowledge not stored in FoM.

Likely distinction:

```
required semantic content
licensed background knowledge
realization-only defaults
forbidden resolution of unknowns
```

### 9. Audience model

Recoverability depends on audience.

Need explicit representation of:

- language competence;
- shared cultural knowledge;
- in-group code;
- prior discourse;
- assumed world knowledge;
- expertise.

The model should remain sparse rather than becoming a full simulation of a person.

### 10. Canonicalization / normal forms

Need to decide which semantically equivalent surface forms normalize identically.

Candidates:

- inverse relation orientation;
- identity normalization;
- commutative argument ordering where licensed;
- scope overlay expansion;
- macro expansion level;
- alpha-renaming of variables.

### 11. Complexity and scalability

Need to test:

- long documents;
- many nested scopes;
- large trajectories;
- graph diff performance;
- partial loading;
- modular/imported FoM fragments.

### 12. Historical anecdote combat test

Still pending.

This should test:

- event vs source report;
- uncertain historicity;
- attribution;
- later retelling;
- legendary embellishment;
- narrator stance;
- source disagreement.

### 13. Round-trip realization

Continue:

```
FoM -> independent realization -> extraction -> semantic diff
```

with no access to the original FoM during extraction.
