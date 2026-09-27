# Format of Meaning — Conceptual Specification

Status: work in progress

## 1. Definition

Format of Meaning (FoM) is a language-independent intermediate representation of an intended transformation of receiver/shared state.

A useful approximation is:

```
Meaning ≈ intended Δ State
```

More precisely, meaning may involve an intended transformation of multidimensional receiver/shared state along a trajectory, under constraints on content, uncertainty, inference, attention, affect, social state, disclosure, and realization.

FoM is the graph-based IR used to represent that transformation.

## 2. Fundamental distinctions

FoM should keep separate:

1. intended meaning;
2. observable signal/message;
3. interpreted meaning;
4. actual effect;
5. unintentionally revealed information.

Similarly:

- what the sender says;
- what the sender means;
- what the sender reveals;
- what the receiver infers;
- what the receiver becomes after processing the signal.

An intended transformation need not equal the actual transformation.

```
intended_delta != actual_delta
```

This distinction is required for failed persuasion, invalid declarations, deception, irony, failed promises, misunderstanding, and similar cases.

## 3. Representation model

FoM is a sparse typed semantic/pragmatic graph.

The graph:

- may contain cycles;
- may contain nested perspectives;
- may contain incompatible claims in different scopes;
- may contain overlapping addressable subgraphs;
- need not be a DAG;
- need not form a tree.

The same entity, event, concept, or proposition-like fragment should normally be referenced across scopes rather than copied.

FoM does not attempt to model the entire world or mind. It stores only distinctions relevant to the current meaning.

## 4. Semantic core

The current semantic core contains five mechanisms:

```
NODE
RELATION
SCOPE
DELTA
CONSTRAINT
```

`SUBGRAPH` is structural graph addressing rather than a semantic primitive.

### NODE

A NODE is an addressable semantic object.

Examples:

- person;
- object;
- place;
- event;
- concept;
- signal;
- question;
- model;
- abstract process.

FoM does not require ENTITY, EVENT, CONCEPT, SIGNAL, or STATE to be separate primitive classes. They can be represented as typed nodes.

### RELATION

A RELATION is an addressable typed connection between semantic objects.

Relations may be binary or n-ary and may themselves carry:

- identity;
- source;
- confidence;
- time;
- salience;
- scope;
- evidence;
- qualifiers.

FoM does not define one universal closed vocabulary of all semantic relations.

### SCOPE

A SCOPE is a local model or perspective relative to which graph content receives status.

Scopes allow incompatible graph states to coexist without contradiction.

Examples:

- reality;
- beliefs;
- attributed beliefs;
- dreams;
- fiction;
- memories;
- plans;
- expectations;
- counterfactuals;
- normative models;
- reader states at checkpoints.

Minimal scope-relative status currently includes:

```
ACCEPT
REJECT
```

Absence of ACCEPT is not equivalent to REJECT.

### DELTA

A DELTA is an addressable transformation of graph state.

A delta may:

- add or remove content;
- update qualifiers;
- connect or disconnect objects;
- identify referents;
- activate or deactivate scopes;
- change certainty;
- change salience;
- change affect;
- create or remove social commitments;
- open or close questions.

Useful roles include:

```
intended_delta
attempted_delta
actual_delta
observed_delta
```

### CONSTRAINT

A CONSTRAINT restricts the space of acceptable graph states, transformations, interpretations, disclosures, inference paths, or realizations.

Examples:

- fixed unknown;
- preserve ambiguity;
- prohibit disclosure before checkpoint;
- require disclosure after checkpoint;
- preserve inference route;
- preserve affect;
- constrain realization freedom.

## 5. Structural kernel

Below the semantic core, FoM currently needs structural machinery:

```
SUBGRAPH
PATTERN
VARIABLE
BINDING
BINDING ACCESSIBILITY
```

### SUBGRAPH

An addressable selection of nodes and relations.

A proposition is not required as a primitive:

```
PROPOSITION := truth-evaluable SUBGRAPH used in a propositional role
```

### PATTERN / VARIABLE / BINDING

These support quantification, distribution, dependent reference, and other parameterized structures.

Examples include:

- "every student...";
- distributive readings;
- "everyone loves their mother";
- donkey anaphora;
- modal quantification over accessible scopes.

Binding accessibility determines where a bound variable remains referable.

## 6. Relation architecture

FoM separates three layers.

### Open semantic predicates

Domain/world meaning may use an open vocabulary:

```
parent_of
located_at
owns
loves
holds
transfer
betray
expensive
contains
```

These are not universal Core primitives.

### Core relational operators

A small set currently appears to have special computational or representational semantics:

```
IDENTITY
TEMPORAL
CAUSAL
INFERENTIAL
SEMIOTIC
```

Causality and inference remain distinct:

- causality belongs to a model of the world;
- inference belongs to a model of reasoning.

Semiotic relations are also independent: representation/expression is neither causation nor evidence.

Identity has graph-merging consequences.

### Structural relations

Some relations belong to the IR rather than to represented meaning:

```
TYPE
ARGUMENT_ROLE
SUBGRAPH_MEMBERSHIP
```

## 7. Signals and meaning

Signals are ordinary typed nodes whose semantic role is established through SEMIOTIC relations.

Examples:

```
signal expresses P
signal suggests Q
signal unintentionally_reveals R
```

Signal and meaning are not identical.

Preserving a physical signal or event does not guarantee preserving its semiotic function.

Meaningful silence can be modeled as:

```
expected signal/action
+ observed absence
+ inference
```

No SILENCE primitive is required.

## 8. Unknown information and ambiguity

Unknown information is meaningful and must not be silently guessed or discarded.

Useful forms include:

```
UNKNOWN
FIXED_UNKNOWN
MUST_REMAIN_UNKNOWN
```

A FIXED_UNKNOWN constraint means realization must not create enough evidence to resolve the unknown.

Ambiguity may also be an invariant.

If multiple interpretations remain licensed by the source and context, FoM may preserve them rather than choosing one.

## 9. Explicitness and recoverability

Explicitness and recoverability are independent.

Possible explicitness statuses:

```
EXPLICIT
INFERABLE
LATENT
```

Possible recoverability statuses:

```
REQUIRED
OPTIONAL
NONE
```

For example, a relation may be inferable but still required to be recoverable.

Generative-only structure may shape realization without itself becoming recoverable meaning.

Recoverability is trajectory-dependent:

```
fragment × audience × context × trajectory_position
```

Thus a fragment may be prohibited before one checkpoint and required after another.

A spoiler can be modeled as a semantically valid patch applied at the wrong trajectory position.

## 10. Reader / receiver trajectory

Long-form works may define an intended trajectory of receiver state.

A checkpoint may specify:

- knowledge;
- ignorance;
- suspicion;
- confidence;
- salience;
- open questions;
- preferred interpretations;
- affect.

Timing of disclosure may therefore be part of meaning.

## 11. Minimum Sufficient Resolution

FoM uses the coarsest representation that preserves every required observable semantic distinction while avoiding unnecessary precision.

A semantic fragment may remain atomic iff replacing its internal structure with its semantic interface preserves all required distinctions and constraints.

Decomposition is required when internal structure becomes independently meaningful, for example through:

- independent reference;
- independent scope/status;
- independent timing;
- independent delta;
- required inference;
- constraints acting on internal components;
- realization requirements;
- hidden precision.

Decomposition should not occur merely because it is possible.

More detail can be semantic corruption if it:

- introduces unsupported detail;
- resolves required uncertainty;
- adds unintended presupposition;
- adds unintended causality;
- changes inference possibilities.

## 12. Refinement and abstraction

A coarse semantic predicate may have a more detailed graph representation.

Two FoMs can remain semantically equivalent at different resolutions when the Concept Ontology licenses the refinement and all required constraints are preserved.

A detailed structure may be abstracted only when the abstraction does not erase required distinctions.

## 13. Standard patterns

The following are currently treated as standard patterns rather than semantic primitives:

- inference;
- expectation;
- attention;
- affect;
- mapping;
- quantification;
- distribution;
- genericity;
- approximation;
- modality;
- reference slots.

## 14. Derived pragmatic phenomena

The following are currently treated as derived patterns:

- lie;
- bluff;
- irony;
- sarcasm;
- metaphor;
- promise;
- threat;
- warning;
- request;
- command;
- secret;
- joke;
- plot twist;
- counterfactual;
- implicature;
- meaningful silence;
- coded / Aesopian language.

Deleting the derived label should not destroy the underlying meaning.

## 15. Reference and binding

Reference must be distinguished from identity.

A linguistic mention is a SIGNAL fragment that SEMIOTICALLY refers to a semantic referent or unresolved reference slot.

Two mentions corefer when their semantic referents are identified.

Bound anaphora is different from ordinary coreference.

Example:

"everyone loves their mother"

requires dependent reference through binding.

Cross-scope binding is allowed where accessibility rules permit it.

Attitude reports may also require distinguishing de se from de re reference. SCOPE may therefore mark a distinguished CENTER / SELF role without adding a new semantic primitive.

## 16. Scope-sensitive operators

Operators such as negation, AGAIN, ALMOST, quantification, and modality must have explicit attachment to semantic fragments.

These are not interchangeable:

```
AGAIN(NOT P)
NOT(AGAIN P)

NOT(ALL P)
ALL(NOT P)
```

Compositional scope is therefore part of meaning.

## 17. Modality

Modality can be represented through SCOPE + CONSTRAINT + BINDING over accessible alternative scopes.

Approximation:

```
POSSIBLE(P)  := some relevant accessible scope ACCEPTS P
NECESSARY(P) := all relevant accessible scopes ACCEPT P
```

The modal base or source must be explicit when relevant:

- epistemic;
- deontic;
- ability;
- plan;
- other contextual bases.

## 18. Genericity and plurality

Generic statements are not universal quantification.

For example:

"Birds fly"

must allow exceptions.

Genericity is currently treated as a standard exception-tolerant pattern rather than a Core primitive.

Collective and distributive readings are structurally distinct:

- collective: a plural/group node participates once;
- distributive: a pattern applies independently to members.

## 19. Realization

FoM defines a space of acceptable realizations rather than one unique signal.

A realization function may be conceptualized as:

```
realize(
    FoM,
    target_language,
    target_culture,
    target_audience,
    context,
    constraints
)
```

Realization may preserve:

```
PRESERVE_REFERENT
PRESERVE_FUNCTION
PRESERVE_EFFECT
PRESERVE_FORM
```

with strengths such as REQUIRED, PREFERRED, or OPTIONAL.

## 20. Realization freedom

Possible freedom levels:

```
FIXED
CONSTRAINED
FREE
```

A realization may invent compatible detail.

Such invention is LICENSED only if it:

- is compatible with FoM;
- serves realization;
- does not alter required meaning;
- does not resolve FIXED_UNKNOWN information;
- does not change required inference space;
- does not violate disclosure/timing constraints.

Logical compatibility alone is insufficient.

## 21. Semantic diff

Semantic comparison is multidimensional.

At minimum, diff may compare:

- CONTENT;
- REFERENCE;
- EPISTEMIC STATUS / CERTAINTY;
- PRESUPPOSITION;
- EXPLICITNESS;
- INFERENCE PATH;
- TIMING / DISCLOSURE;
- FOCUS / SALIENCE;
- AFFECT;
- SOCIAL STATE;
- FIXED_UNKNOWN;
- REALIZATION INVENTION;
- RESOLUTION.

Possible local statuses include:

```
PRESERVED
WEAKENED
STRENGTHENED
LOST
INVENTED
CONTRADICTED
EARLY
LATE
BROKEN
LICENSED
UNLICENSED
EQUIVALENT_UNDER_REFINEMENT
```

Diff is descriptive.

Validation evaluates the diff against source constraints.

## 22. Semantic equivalence

Semantic equivalence is modeled primarily as constraint satisfaction rather than scalar similarity.

A realization may be considered equivalent when:

- all REQUIRED constraints hold;
- FIXED invariants are preserved;
- FIXED_UNKNOWN remains unresolved;
- required inference paths remain available;
- required disclosure windows are respected;
- required receiver-state transformations remain achievable.

OPTIONAL, FREE, and LICENSED differences need not break equivalence.

## 23. Working definition

Format of Meaning is a sparse, typed, scope-aware graph IR representing an intended transformation of receiver/shared state along a trajectory.

It consists of addressable semantic objects and relations, perspective-relative scopes, graph-state deltas, and constraints over content, uncertainty, inference, timing, focus, affect, social state, recoverability, and realization.

Its semantic resolution is demand-driven: concepts remain atomic until their internal distinctions become relevant, and refinement is allowed only where required meaning and uncertainty are preserved.
