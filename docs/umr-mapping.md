# FoM ↔ UMR mapping

Status: architectural hypothesis under test

The first [carrier/overlay pilot](../experiments/layered_architecture/README.md)
preserves all seven existing gold target findings with 35 carrier-owned and
10 overlay-owned source records, versus 45 standalone records. This is
shared-engine feasibility, not UMR conformance or reduced total complexity.
The all-ten-case audit identifies incomplete gold coverage; architecture
selection remains open pending independent annotation cost/agreement.

UMR is currently the most important neighboring representation for FoM.

This document asks a concrete question:

> Can FoM stop owning most ordinary semantic content and instead operate as a transformation / constraint layer over UMR or another compatible semantic graph?

If yes, FoM should become smaller.

## 1. Why this comparison changes the architecture

UMR already represents, among other things:

### Sentence level

- predicate-argument structure;
- word senses;
- named entities;
- person and number;
- negation/modality-related structure;
- event aspectuality;
- discourse relations.

### Document level

- coreference;
- temporal dependencies;
- modal dependencies.

Its document-level modal representation explicitly associates a cognizer with a modal strength and an event.

Its temporal layer provides document-relative and event-relative temporal dependencies.

Its aspect system already distinguishes categories including state, process, habitual, activity, endeavor, and performance.

FoM should not duplicate these merely to remain self-contained.

References:

- UMR project: https://umr4nlp.github.io/web/
- UMR schema: https://umr4nlp.github.io/web/UMRSchemaPages/index.html
- UMR document-level graph: https://umr4nlp.github.io/web/UMRSchemaPages/Document-Level-Graph.html
- UMR 2024 dataset paper: https://aclanthology.org/2024.lrec-main.229/
- UMR quantification/scope precursor: https://aclanthology.org/W19-3303/

## 2. Provisional layer split

Instead of:

```
FoM
  owns ordinary semantic graph
  owns modality
  owns temporal relations
  owns coreference
  owns pragmatic/transformation structure
```

test:

```
SEMANTIC CARRIER
    UMR / compatible graph
    predicate-argument content
    entities/events
    coreference
    linguistic aspect
    ordinary temporal/modal structure
    discourse relations where adequate

              ↓ referenced by

FoM TRANSFORMATION / CONSTRAINT LAYER
    agent/shared state transitions
    intended / attempted / actual deltas
    recoverability
    disclosure trajectory
    fixed unknown / ambiguity invariants
    required inference dependencies
    signal↔meaning function constraints
    audience dependencies
    affect / attention when preservation-relevant
    social-state transformations
    realization freedom
    semantic diff requirements
```

The semantic carrier need not be UMR forever. FoM should ideally depend on a small interface rather than one serialization.

## 3. NODE / RELATION

### FoM today

FoM owns generic nodes and open semantic predicates.

### UMR overlap

UMR already provides graph nodes and semantic relations for ordinary text content.

### Proposed direction

FoM should distinguish:

```
external semantic object reference
FoM-owned control/state object
```

Example:

```
UMR event u:e17 = leave-01

FoM:
    ACCEPT(receiver-before, ref(u:e17)) = low
    ACCEPT(receiver-after, ref(u:e17)) = high
```

FoM does not need to restate the full leave predicate graph.

## 4. Identity and coreference

UMR document-level coreference includes:

```
:same-entity
:same-event
:subset-of
```

FoM currently has IDENTITY plus open part/member relations.

### Proposed division

Use semantic-carrier coreference for ordinary referential identity across text.

FoM retains scope-relative identity only where **a model can disagree with reality about identity**.

Example:

```
UMR/reality:
    same-entity Clark-Kent Superman

FoM belief scope:
    REJECT identity(ref Clark-Kent, ref Superman)
```

Thus FoM's special need is not ordinary coreference. It is **perspective-relative identity state**.

## 5. Temporal structure

UMR document temporal relations currently include relations such as:

- before;
- after;
- contained;
- overlap;
- depends-on relative to document/past/present/future reference anchors.

FoM independently drifted toward Allen interval algebra.

### Proposed division

For linguistic source annotation:

- use UMR temporal dependency where adequate;
- do not force a richer Allen relation unless the source meaning needs it.

For reasoning/validation:

- an optional temporal reasoner may map carrier relations into a richer Allen-style calculus.

FoM itself primarily owns a different time axis:

```
reader / receiver trajectory time
```

World time and disclosure time remain distinct.

This looks like a genuine architectural separation:

```
UMR temporal graph -> when events happen
FoM trajectory      -> when information becomes available / salient
```

## 6. Modality / epistemic state

UMR document modality assigns modal strength to events relative to cognizers.

This overlaps substantially with FoM:

```
SCOPE
ACCEPT / REJECT
certainty
source/cognizer
```

### Potential mapping

A UMR relation conceptually like:

```
(cognizer :partial-affirmative event)
```

can populate a FoM state view:

```
scope cognizer-model:
    ACCEPT event
    certainty = partial
```

### Where FoM may still differ

FoM needs to represent transitions between such states:

```
before signal:
    cognizer partial / uncommitted

after signal:
    cognizer strongly accepts
```

and can constrain the **intended transition** independently of the event's static modal annotation.

Therefore:

```
UMR modality ~= state snapshot
FoM DELTA     ~= transition / intended change between snapshots
```

This is a hypothesis to test, not a proven clean decomposition.

## 7. Aspect and event structure

UMR already has an aspect lattice with categories such as:

```
state
process
habitual
activity
endeavor
performance
```

The distinction between endeavor and performance directly overlaps FoM tests such as:

```
Иван строил дом, но не построил его.
```

### Proposed direction

Use UMR aspect annotation for ordinary linguistic aspect where possible.

Only decompose:

```
process -> culmination -> result state
```

inside FoM when those phases are independently required for:

- inference;
- reference;
- social/state delta;
- realization constraint;
- semantic diff.

This is exactly FoM's Minimum Sufficient Resolution rule applied to UMR interoperability.

## 8. Source attribution and reported speech

UMR's modal document graph handles quoted/attributed speech by distinguishing:

- author commitment to the speech event;
- the speech actor as cognizer of the reported content.

This overlaps strongly with FoM's historical-source work.

### Proposed direction

Ordinary:

```
Alice said P
```

should preferably come from the carrier graph.

FoM should add structure only when required for:

- source-reliability comparison;
- receiver-state update;
- protected attribution in translation;
- report-vs-reality semantic diff;
- multi-hop source trajectory.

## 9. Quantification, negation and scope

UMR originated partly as an extension to AMR to add scope for:

- quantification;
- negation;
- modality.

FoM should therefore stop treating its own PATTERN/SCOPE experiments as evidence that it needs an independent theory of linguistic quantifier scope.

### Proposed direction

Try importing carrier scope structures.

FoM PATTERN/BINDING remains necessary only for FoM-native constraints that quantify over:

- audiences;
- trajectory checkpoints;
- accessible state alternatives;
- realization slots;
- semantic-diff obligations;

or when the semantic carrier cannot represent a required source distinction.

## 10. Discourse relations

UMR and SDRT already provide discourse-relation machinery.

FoM currently contains open relations such as:

```
contrasts-with
explains
reinterpretation dependencies
```

### Proposed direction

Before standardizing any discourse relation in FoM:

1. check UMR;
2. check SDRT;
3. reuse/mapping if adequate.

FoM should own only relations that are specifically about transformation/preservation rather than discourse coherence itself.

## 11. What appears not to be ordinary UMR territory

The following FoM concerns remain candidates for a separate layer.

### 11.1 Intended state delta

Not merely what the speaker/cognizer believes, but:

```
what change the sender intends the signal to cause
```

including failed changes.

### 11.2 Attempted vs actual state operation

Especially social acts:

```
attempted declaration
actual declaration effect
```

### 11.3 Recoverability

Whether content must be recoverable for a specified audience/context.

### 11.4 Disclosure trajectory

When content is prohibited/required to become recoverable.

### 11.5 FIXED_UNKNOWN

A realization invariant requiring an issue to remain unresolved.

### 11.6 Signal-function preservation

A source signal may need to preserve:

- inference role;
- ambiguity/coactivation;
- coded access;
- evidence function;
- exact or analogous form.

### 11.7 Realization freedom / licensed invention

What a generator may add while remaining semantically valid.

### 11.8 Multidimensional semantic diff

Comparison of transformations/constraints rather than only carrier-graph overlap.

These areas still need comparison against other prior work.

## 12. Proposed carrier interface

FoM should not hard-code UMR syntax into its Core.

A minimal carrier interface might expose:

```
SemanticObjectRef
    stable local reference to entity/event/state/subgraph

PredicateView(ref)
    optional predicate/role structure

CoreferenceView(ref)
    same-entity / same-event / subset relations

TemporalView(ref)
    source temporal dependencies

ModalView(ref, cognizer)
    source modal commitment

AspectView(ref)
    linguistic aspect information

DiscourseView(ref)
    discourse/coherence relations where available
```

FoM structures refer to `SemanticObjectRef`.

This keeps open the possibility of:

- UMR;
- AMR + extensions;
- DRS;
- manually authored semantic graphs;
- future model-produced semantic carriers.

## 13. Interoperability experiment

Take the post-freeze translation/retelling mini-corpus.

For each case create two gold representations:

### A. Standalone FoM

Current style.

### B. Layered

```
UMR-like carrier
+
FoM transformation/constraint overlay
```

Compare:

- annotation time;
- graph size;
- agreement;
- ability to express required benchmark constraints;
- semantic-diff performance.

### Decision rule

If layered representation preserves all required benchmark distinctions with less annotation and no worse agreement:

> prefer layered architecture.

If a required distinction cannot be expressed without duplicating/rewriting the carrier graph:

> document that exact failure before expanding FoM.

## 14. Immediate consequence for current Core

The five Core mechanisms may still be useful internally, but their interpretation changes.

Instead of saying:

```
NODE / RELATION are a universal semantic content representation
```

we should test:

```
NODE / RELATION are FoM graph mechanics
and may reference semantic content owned by another representation.
```

This would make FoM closer to a **semantic transformation contract / overlay IR** than an all-purpose replacement for existing meaning representations.

That may be a stronger and more defensible project.
