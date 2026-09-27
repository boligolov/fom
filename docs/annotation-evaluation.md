# Annotation agreement and evaluation

Status: experiment design

FoM cannot assume that two competent annotators will produce identical graphs.

Existing meaning-representation projects already show substantial structural disagreement, and FoM attempts to annotate additional pragmatic and trajectory-sensitive dimensions.

Therefore exact graph equality is not an acceptable definition of annotation agreement.

## 1. Motivation from prior work

AMR commonly evaluates graph agreement with Smatch, which aligns graph variables and measures triple overlap. Reported human annotation agreement is high enough to be useful but far from graph identity; published AMR work reports ranges around 0.7–0.9 depending on corpus, language, annotator experience, and setup.

UMR annotation can also be difficult. A 2024 study of Chinese aspect annotation with four trained annotators reported Fleiss' kappa of about 0.53 for the UMR aspect lattice.

These results matter for FoM because FoM currently allows:

- multiple semantic resolutions;
- optional decomposition;
- alternative but equivalent graph structures;
- explicit uncertainty;
- inference paths;
- audience assumptions;
- disclosure trajectories;
- affective and social-state annotations.

Agreement must therefore be evaluated at multiple levels.

References:

- Cai & Knight (2013), *Smatch: an Evaluation Metric for Semantic Feature Structures*: https://aclanthology.org/P13-2131/
- Wein (2025), *Ambiguity and Disagreement in Abstract Meaning Representation*: https://aclanthology.org/2025.comedi-1.14/
- *Annotate Chinese Aspect with UMR — A Case Study* (2024): https://aclanthology.org/2024.lrec-main.104/

## 2. First experiment

Use a small corpus of 20–30 items.

The first corpus should deliberately mix:

- plain factual statements;
- reference ambiguity;
- presupposition;
- implicature;
- source attribution;
- unknown/fixed-unknown information;
- deliberate multi-meaning;
- disclosure/trajectory;
- social acts;
- one or two short narrative fragments.

Do not select only examples that were used to design FoM.

At least half of the items should be externally sourced or independently written after the annotation guidelines are frozen.

## 3. Annotators

Initial target:

- two human annotators;
- two independent model annotators.

All annotators receive:

- the same FoM specification;
- the same annotation guide;
- the same Concept Contracts / allowed standard library;
- the same source text and audience/context description.

They do not see each other's annotations.

Model annotators should run in separate conversations/contexts and should not receive the reference FoM.

## 4. Two-pass annotation

### Pass A — semantic commitments

Annotators first record only semantic commitments:

- required content;
- explicit unknowns/ambiguities;
- scopes/attribution;
- intended state changes;
- required inference dependencies;
- disclosure constraints;
- preservation constraints.

No detailed graph decomposition is required yet.

### Pass B — FoM graph

Annotators encode the commitments in FoM Text at Minimum Sufficient Resolution.

This separation lets us distinguish disagreement about meaning from disagreement about graph engineering.

## 5. Agreement dimensions

Agreement should be reported separately for at least:

### 5.1 Required content

Do annotators agree on the propositions/events/relations that must be preserved?

### 5.2 Reference

Do they agree on resolved referents, unresolved slots, and binding dependencies?

### 5.3 Scope and attribution

Do they agree which agent/source/model accepts, rejects, reports, or remains uncommitted about content?

### 5.4 Epistemic / indeterminacy status

Do they agree on:

- certainty;
- unknown vs rejected;
- ambiguity;
- vagueness;
- source conflict;
- fixed-unknown constraints?

### 5.5 Inference route

Do they agree that some conclusion is:

- explicit;
- inferable;
- dependent on specific evidence/context;
- not required?

### 5.6 Disclosure / trajectory

Do they agree on when information may or must become recoverable?

### 5.7 Social state

Do they agree on attempted vs actual commitments, permissions, obligations, declarations, etc.?

### 5.8 Affect / stance / salience

Do they agree on required evaluative or affective structure?

### 5.9 Resolution / decomposition

Do they agree on whether a predicate may remain atomic?

This dimension is diagnostic rather than automatically an error.

## 6. Agreement metrics

No single score should replace the vector.

A first report should contain:

```
required-content agreement
reference agreement
scope/status agreement
uncertainty agreement
inference-path agreement
trajectory agreement
social-state agreement
affect/stance agreement
resolution agreement
```

### Binary / categorical fields

Use ordinary agreement measures where appropriate:

- raw agreement;
- Cohen's kappa for two annotators;
- Fleiss' kappa for more annotators where categories fit.

### Graph structure

Use a graph-overlap metric only as a secondary structural diagnostic.

A Smatch-like result can answer:

> Did the annotations produce similar graphs?

It cannot by itself answer:

> Did they preserve the same required meaning?

### Constraint agreement

For each annotation pair:

1. normalize both graphs;
2. identify REQUIRED constraints;
3. test whether annotation A satisfies B's required constraints;
4. test whether B satisfies A's required constraints.

Report both directions because refinement may be asymmetric.

Conceptually:

```
A -> satisfies constraints of B?
B -> satisfies constraints of A?
```

This is the most FoM-specific candidate metric.

## 7. Disagreement taxonomy

Every disagreement in the pilot should be manually classified.

Candidate classes:

```
source ambiguity
guideline ambiguity
ontology/concept disagreement
different but equivalent decomposition
different Minimum Sufficient Resolution
missed inference
invented inference
scope/attribution disagreement
reference disagreement
trajectory disagreement
affect/stance disagreement
annotation error
```

The taxonomy is expected to change after the pilot.

## 8. Adjudication

Adjudication should not automatically choose one existing graph.

Possible outcomes:

- A is preferred;
- B is preferred;
- both are valid;
- merge/refinement;
- source is genuinely ambiguous;
- annotation guide is underspecified;
- FoM lacks a required mechanism.

"Both are valid" is an important result, not a failure.

## 9. What would falsify the current approach

The pilot should be considered a serious warning if:

- annotators agree on source meaning but required-constraint agreement remains low because graph freedom is too large;
- required inference/trajectory annotations are not reproducible;
- Minimum Sufficient Resolution cannot be applied consistently;
- adjudication repeatedly requires arbitrary conventions unrelated to semantic preservation;
- model and human annotations systematically encode different kinds of objects;
- semantic diff mostly measures annotation style.

Any of these should trigger simplification before expanding the representation.

## 10. Annotation guide requirement

Before running the pilot, produce a short guide that says not only what can be represented, but what **must not** be annotated.

Examples:

- do not add merely plausible world knowledge;
- do not decompose an open predicate unless a required distinction penetrates it;
- do not resolve ambiguity without evidence;
- do not annotate intended affect unless supported;
- do not introduce hidden author intentions as recoverable meaning;
- mark generative-only structure separately if used at all.

Negative annotation rules are essential for agreement.

## 11. Initial success criterion

The first pilot is not expected to produce publication-grade agreement.

A useful first target is:

- high agreement on required factual/reference content;
- identifiable and explainable disagreement on pragmatic dimensions;
- most graph-structure disagreements classified as equivalent refinement rather than contradictory meaning;
- a small enough adjudication burden that a second guideline revision is feasible.

The objective is to learn where FoM is annotatable, not to maximize a headline score.
