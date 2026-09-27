# Format of Meaning

Format of Meaning (FoM) is an experimental language-independent intermediate representation for meaning.

The core idea is simple:

> Meaning is not just propositional content. A message can be viewed as an intended transformation of the receiver's and shared state.

FoM tries to represent that transformation explicitly enough that meaning can be analyzed, compared, transformed, or realized in different languages and modalities without reducing the task to literal translation.

## Why

Natural-language messages carry much more than facts:

- beliefs and uncertainty;
- presuppositions and implicatures;
- attention and salience;
- emotions and stance;
- social obligations and permissions;
- nested models of other agents;
- ambiguity and intentionally unresolved information;
- timing of disclosure;
- inference paths;
- metaphor, irony, jokes, silence, and other pragmatic effects.

FoM treats these as parts of the semantic/pragmatic state transition rather than as decoration around a sentence.

A useful working approximation is:

```
Meaning ≈ intended Δ State
```

FoM itself is **not Meaning**. It is an intermediate representation of that intended transformation.

## Current direction

FoM is currently being developed as a sparse, typed, scope-aware graph IR.

The current semantic core is intentionally small:

- **NODE** — an addressable semantic object
- **RELATION** — a typed relation between addressable objects
- **SCOPE** — a local model or perspective
- **DELTA** — an intended, attempted, observed, or actual graph-state transformation
- **CONSTRAINT** — a restriction on valid states, transformations, interpretations, disclosures, or realizations

Structural machinery such as subgraphs, patterns, variables, and bindings lives below the semantic core.

The project deliberately avoids a giant closed ontology. Domain meaning can use open predicates, while a small number of relation types such as identity, temporal, causal, inferential, and semiotic relations receive special treatment.

## Design principles

- Represent only distinctions relevant to the current meaning.
- Unknown information is still information.
- Ambiguity may be intentional and must not be silently resolved.
- More detail is not automatically more accurate.
- Semantic decomposition is demand-driven.
- Signal, intended meaning, interpretation, and actual effect are distinct.
- Recoverability and explicitness are distinct.
- Timing of disclosure can be part of meaning.
- Semantic equivalence is primarily constraint satisfaction, not a scalar similarity score.
- Realization may invent compatible details only when they do not change required meaning or inference space.

## Repository structure

- [Conceptual specification](docs/specification.md)
- [FoM Text syntax](docs/text-syntax.md)
- [Concept ontology boundary](docs/concept-ontology.md)
- [Testing and semantic diff](docs/testing.md)
- [Canonical FoM graph](docs/canonical-format.md)
- [Standard macros](docs/standard-macros.md)
- [Research roadmap](docs/research-roadmap.md)
- [Core relation operators](docs/research-core-operators.md)
- [Temporal model](docs/research-temporal-model.md)
- [Scope semantics](docs/research-scope-semantics.md)

## Status

This repository is a work in progress.

The current documents capture the working architecture and are expected to change as the model is stress-tested against quantification, reference, binding, modality, coded language, literary texts, historical anecdotes, and round-trip realization tests.
