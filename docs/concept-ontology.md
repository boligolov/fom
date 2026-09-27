# Concept Ontology Boundary

Status: exploratory

FoM deliberately avoids embedding a universal encyclopedia of concepts inside every message graph.

The Concept Ontology exists to provide reusable semantic interfaces for open predicates.

## 1. Boundary

### Message-specific FoM contains

What is specific to the current message:

- participants;
- scopes;
- uncertainty;
- deltas;
- timing;
- focus;
- inference routes;
- constraints;
- disclosure windows;
- realization requirements.

### Concept Ontology contains

What is invariant across valid instances of a concept and is necessary for sound semantic interpretation, abstraction, or refinement.

### World Knowledge contains

What is merely:

- usual;
- typical;
- probable;
- culturally common;
- empirically frequent.

Typical knowledge must not be promoted to semantic entailment.

### Lexicon contains

How words, phrases, gestures, and other signals in particular languages or communities may realize concepts or graph patterns.

Lexicalization may be many-to-many.

## 2. Concept contract

A current candidate interface is:

```
CONCEPT {
    ID

    ARGUMENT_SCHEMA

    ASSERTED_ENTAILMENTS

    PRESUPPOSITIONAL_REQUIREMENTS

    CONVENTIONAL_EFFECTS

    ABSTRACTION_CONDITIONS

    REFINEMENT_OPTIONS
}
```

Every section is sparse and optional where not required.

## 3. Minimum contract rule

A Concept Contract should contain only information required for sound abstraction/refinement and conventional interpretation.

It should not contain everything known about the concept.

A useful deletion test:

> If removing a rule would make an invalid semantic abstraction, refinement, or realization appear valid, the rule belongs in the contract.

Otherwise it is probably world knowledge.

## 4. Example: transfer

A concept such as TRANSFER_CONTROL may require:

- source-holder role;
- theme role;
- recipient role;
- source controls theme before;
- recipient controls theme after.

It should not automatically entail transfer of ownership.

## 5. Example: persuade

A successful persuasion concept may require:

- agent;
- target;
- proposition;
- target eventually accepts proposition;
- agent activity contributes causally to that change.

This distinguishes successful persuasion from attempted persuasion.

## 6. Example: betray

BETRAY may require:

- actor;
- affected party / commitment;
- some prior loyalty, trust, affiliation, or normative expectation;
- an action incompatible with that expectation;
- conventional negative framing within an evaluation scope.

The exact violated norm may remain unknown.

Over-decomposition can create false precision.

## 7. Example: love

LOVE should have a very weak contract.

It must not automatically entail:

- trust;
- sexual attraction;
- relationship commitment;
- jealousy;
- desire for contact;
- protectiveness.

Those may be associated, typical, or contextually inferred, but are not universal semantic guarantees.

## 8. Contextual atomicity

There are no assumed universal semantic atoms.

A fragment may be treated as atomic iff replacing its internal structure with its semantic interface preserves all required observable distinctions and constraints of the current FoM.

Atomicity is therefore contextual.

## 9. Refinement

A concept may license one or more graph refinements.

A refined graph and an opaque concept instance may coexist.

Resolution-independent semantic equivalence is allowed when the refinement preserves the concept contract and all message-specific constraints.
