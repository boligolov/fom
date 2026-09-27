# TODO

Working list of unfinished FoM research and implementation tasks.

## Highest priority

- [ ] Define the canonical FoM schema precisely enough to implement a parser/canonicalizer.
- [ ] Specify deterministic macro expansions for the standard library.
- [x] Define canonicalization / normal-form rules.
- [ ] Decide how stable IDs, generated IDs, and cross-document references work.
- [ ] Specify module/import semantics for larger FoM documents.
- [ ] Build a minimal parser for FoM Text.
- [ ] Build a validator for references, bindings, scopes, and constraints.
- [ ] Build a semantic-diff prototype.

## Semantics still under research

- [ ] Formalize genericity / normality semantics.
- [ ] Formalize degree/scale semantics beyond ALMOST.
- [ ] Formalize modality bases and accessibility relations.
- [ ] Distinguish ability from opportunity rigorously.
- [ ] Finish temporal semantics: tense, deixis, duration, recurrence, habituality.
- [ ] Finish scope overlay conflict rules.
- [ ] Define constraint inheritance across scopes.
- [ ] Define world-knowledge licensing during realization.
- [x] Define a sparse audience model.
- [x] Formalize deliberate multi-meaning / co-activation of readings.
- [ ] Test lexical polysemy, homonymy, puns, double entendre, and frame collision.
- [ ] Test conventional implicatures and expressive meaning.
- [ ] Test quotation, mention/use distinction, and metalinguistic negation.
- [ ] Test questions, answers, alternatives, and open-question state more deeply.
- [x] Test comparatives and superlatives.
- [ ] Test plurals, groups, mass nouns, and part-whole structure more deeply.
- [x] Test aspect and event structure.
- [x] Test vague predicates and sorites-like boundaries.
- [ ] Test counterfactual causation and causal uncertainty.
- [ ] Test evidentiality and source reliability.
- [ ] Test conflicting sources and disagreement.
- [x] Test social authority / felicity conditions in declarations, promises, commands, permissions, and prohibitions.

- [ ] Formalize a general uncertainty/indeterminacy provenance vocabulary (evidence gaps, vagueness, ambiguity, source conflict, etc.).
- [ ] Formalize event phase / culmination / result patterns in the standard library.

## Representation questions

- [ ] Decide whether ordered scales require a special relation family or remain standard semantic patterns.
- [ ] Decide how generic/default knowledge is represented without turning FoM into a knowledge base.
- [ ] Decide the exact representation of open questions and alternative sets.
- [ ] Define provenance records and source maps.
- [ ] Define macro provenance and pretty-printing back to FoM Text.
- [ ] Define extension namespaces and compatibility rules.
- [ ] Define graph partitioning / partial loading.
- [ ] Define canonical serialization format (JSON-like first; binary later if useful).

## Validation / testing

- [ ] Add round-trip tests: FoM -> realization -> extraction -> semantic diff.
- [ ] Complete the Winnie-the-Pooh round trip with an independent realization.
- [x] Add the historical anecdote combat test.
- [x] Add deliberate multi-meaning tests.
- [x] Add audience-dependent decoding tests.
- [x] Add source-report vs event-reality tests.
- [ ] Add long-form trajectory tests with spoilers and delayed disclosure.
- [ ] Add semantic corruption fixtures with expected validator outcomes.
- [ ] Add refinement/abstraction equivalence tests.
- [ ] Add scope-inheritance conflict tests.
- [ ] Add temporal-consistency tests.
- [ ] Add de se / de re mistaken-identity tests.

## Realization

- [ ] Define PRESERVE_REFERENT / FUNCTION / EFFECT / FORM semantics more precisely.
- [ ] Define realization freedom and licensed invention operationally.
- [ ] Define when background world knowledge may be used.
- [ ] Define audience-sensitive recoverability checks.
- [ ] Define realization validation against disclosure windows and inference constraints.

## Engineering

- [ ] Implement FoM Text parser.
- [ ] Implement canonicalizer.
- [ ] Implement schema validator.
- [ ] Implement macro expander.
- [ ] Implement graph visualizer.
- [ ] Implement semantic diff.
- [ ] Implement constraint validator.
- [ ] Implement simple realizer/extractor experiments.
- [ ] Add CI tests once executable tooling exists.

## Later

- [ ] Explore binary/canonical wire encoding.
- [ ] Explore content-addressed fragments.
- [ ] Explore ontology distribution/versioning.
- [ ] Explore long-form book representation and reader-specific realization.
- [ ] Revisit latent/generative-only structure as a separate layer without mixing it into recoverable FoM meaning.
