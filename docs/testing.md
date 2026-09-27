# Testing and Semantic Diff

Status: exploratory

FoM is being developed through adversarial semantic tests rather than by extending the ontology whenever a difficult phenomenon appears.

## 1. Core torture-test principle

A phenomenon should not become a primitive if it can be reconstructed compositionally from more general structure.

Examples already tested compositionally include:

- lie;
- irony;
- metaphor;
- promise;
- threat;
- secret;
- counterfactual;
- joke;
- implicature;
- meaningful silence;
- nested theory of mind.

Derived labels may exist as annotations, but deleting them must not destroy the required underlying meaning.

## 2. Round-trip testing

A basic end-to-end test is:

```
FoM₀
  ↓ realization
Signal
  ↓ extraction
FoM'
  ↓
semantic diff
```

The extractor should not use FoM₀ to fill gaps.

The goal is not graph identity but preservation of required semantic constraints.

## 3. Multidimensional diff

A scalar similarity score is not sufficient.

Useful independent dimensions include:

```
CONTENT
REFERENCE
EPISTEMIC STATUS / CERTAINTY
PRESUPPOSITION
EXPLICITNESS
INFERENCE PATH
TIMING / DISCLOSURE
FOCUS / SALIENCE
AFFECT
SOCIAL STATE
FIXED_UNKNOWN
REALIZATION INVENTION
RESOLUTION
```

Possible local outcomes include:

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

## 4. Diff vs validation

Diff is descriptive.

Validation evaluates a diff against source constraints.

Example:

```
DIFF:
    explicitness = STRENGTHENED

VALIDATION:
    PASS
```

may be acceptable in documentation but fail in a joke or mystery.

## 5. Corruption tests

Useful corruption classes include:

### Content corruption

Change the proposition itself.

### Certainty corruption

Keep content but change assertion strength.

### Explicitness corruption

Turn required inference into direct assertion or vice versa.

### Timing corruption

Reveal correct information at the wrong trajectory position.

### Focus corruption

Preserve facts but reduce required salience.

### Affect corruption

Preserve event structure but change required stance or emotional effect.

### Inference-path corruption

Preserve an observable signal while changing the reason it supports the conclusion.

### Fixed-unknown corruption

Add compatible detail that resolves information required to remain unknown.

### Presupposition corruption

Change the assumed pre-message state while preserving headline content.

## 6. Constraint-based equivalence

Semantic equivalence should primarily be tested by constraint satisfaction:

- all REQUIRED constraints hold;
- FIXED invariants are preserved;
- FIXED_UNKNOWN remains unresolved;
- required inference paths remain available;
- required disclosure windows are respected;
- required receiver-state transformations remain achievable.

OPTIONAL, FREE, and LICENSED differences need not break equivalence.

## 7. Current stress-test areas

The current architecture has been tested against:

- quantification;
- plurality;
- collective vs distributive readings;
- generic statements;
- modality;
- negation scope;
- AGAIN;
- ALMOST;
- pronouns;
- dependent anaphora;
- donkey binding;
- definite re-identification;
- cross-scope binding;
- de se vs de re reference.

These tests have not required a sixth semantic Core primitive so far.

They did strengthen the need for structural PATTERN / VARIABLE / BINDING machinery.

## 8. Coded / Aesopian language

A future dedicated test should cover in-group coded language where:

- the surface lexical concept points one way;
- the intended target meaning is conventionally reassigned by group context;
- a metaphorical source domain may still be active;
- the literal interpretation is explicitly rejected;
- recoverability depends strongly on audience/shared code.

This is useful for testing signal→meaning mappings beyond ordinary dictionary semantics.


## Executable tooling

The repository now has two executable validation layers.

### Structural validation

```bash
python -m fom check examples tests
```

This validates FoM Text syntax, IDs/references, basic lexical binding, and structural forms.

A green structural check means the files obey the current surface contract. It does **not** establish semantic correctness.

### First semantic-diff subset

```bash
python -m fom diff SOURCE.fom CANDIDATE.fom
```

The current implementation intentionally supports only a narrow subset:

- addressable relation content;
- scope-relative ACCEPT/REJECT and certainty;
- salience qualifiers;
- inference relations such as `evidence-for`;
- disclosure constraints;
- FIXED_UNKNOWN preservation.

The first executable corruption fixtures live under:

```
tests/fixtures/corruption/
```

and are checked by `python_tests/test_semantic_diff.py`.

This diff currently assumes stable IDs for deliberately mutated fixtures. It is **not yet** a general semantic graph matcher and must not be described as such.

## Torture-test discipline

`tests/discipline.toml` and `python_tests/test_torture_discipline.py` provide an initial falsifiability guard.

For selected tests, predicate names may not contain the name of the phenomenon under test.

For example, a humor test may not pass by encoding its result as an opaque predicate named `funny` or `joke`.

This rule is deliberately incomplete. The longer-term requirement is that every torture test specify which lower-level vocabulary/mechanisms it is allowed to use and what competency condition must be satisfied.


## Cross-document structural matching

Semantic diff must not treat local implementation IDs as meaning.

The current matcher therefore:

1. resolves relation and subgraph references to structural signatures;
2. cancels semantically identical relations even when their IDs differ;
3. aligns nodes with the same explicit ID as a continuity hint for authored revisions;
4. conservatively aligns differently named nodes only when a structural fingerprint is unique on both sides;
5. leaves ambiguous/symmetric node groups unmatched rather than guessing.

The node fingerprint currently uses node metadata plus explicit-relation incidence, with two refinement rounds.

This is deliberately weaker than general graph isomorphism/Smatch-style alignment. It is a safe intermediate step.

Current limitation:

```
different valid decompositions
ambiguous repeated entities
ontology refinements
scope-ID differences
```

can still create structural diff noise.


## Refinement / abstraction matching

Semantic diff now has a first executable resolution-equivalence mechanism.

A Concept Contract can declare how a coarse predicate may be refined into lower-level relations.

The current test contract is:

```
transfer-control
    -> controls-before(source, theme)
    -> controls-after(recipient, theme)
```

When the contract is satisfied:

```
coarse source -> refined candidate
    RESOLUTION = EQUIVALENT_UNDER_REFINEMENT

refined source -> coarse candidate
    RESOLUTION = EQUIVALENT_UNDER_ABSTRACTION
```

The matched coarse/refined relations are removed from ordinary CONTENT loss/invention reporting.

Negative tests require:

- every contract-required relation to be present;
- source/candidate role bindings to match.

This is not yet a general theorem prover. It is a contract-driven equivalence mechanism intended to make Minimum Sufficient Resolution testable.
