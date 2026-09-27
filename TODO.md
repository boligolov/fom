# TODO

Working list of unfinished FoM research and implementation tasks.

## Highest priority

- [x] Freeze broad semantic expansion while tooling and empirical validation catch up.
- [x] Make the current FoM corpus parse and structurally validate in CI.
- [x] Add first executable torture-test discipline rule against phenomenon-name predicates.
- [x] Add prior-art comparison matrix: FoM vs AMR/UMR, DRT/dynamic semantics, common ground, speech acts, Allen, supervaluation, questions/discourse frameworks.
- [x] Design annotation-agreement experiment.
- [ ] Run annotation-agreement pilot with independent annotators (requires genuinely independent annotators/models).
- [x] Define first narrow end-to-end use case: translation/retelling preservation validation.

- [ ] Define the canonical FoM schema precisely enough to implement a parser/canonicalizer.
- [ ] Specify deterministic macro expansions for the standard library.
- [x] Define canonicalization / normal-form rules.
- [ ] Decide how stable IDs, generated IDs, and cross-document references work.
- [ ] Specify module/import semantics for larger FoM documents.
- [x] Build a minimal parser for FoM Text.
- [x] Build first-pass validator for syntax, references, bindings, scopes, and structural constraints.
- [x] Build first executable semantic-diff subset (content, certainty, salience, inference, disclosure, fixed-unknown).
- [ ] Extend semantic diff beyond ID-stable corruption fixtures.

## Semantics still under research

- [ ] Formalize genericity / normality semantics.
- [ ] Formalize degree/scale semantics beyond ALMOST.
- [ ] Formalize modality bases and accessibility relations.
- [ ] Distinguish ability from opportunity rigorously.
- [ ] Finish temporal semantics: tense, deixis, duration, recurrence, habituality.
- [x] Finish first-pass scope overlay conflict rules.
- [x] Define default constraint inheritance policy across scopes.
- [x] Define first-pass world-knowledge licensing during realization.
- [x] Define a sparse audience model.
- [x] Formalize deliberate multi-meaning / co-activation of readings.
- [ ] Test lexical polysemy, homonymy, puns, double entendre, and frame collision.
- [x] Test conventional implicatures / scalar / contrastive / expressive side meaning (first pass).
- [x] Test quotation, mention/use distinction, and metalinguistic negation.
- [x] Test questions, alternatives, and partial resolution (first pass).
- [x] Test comparatives and superlatives.
- [x] Test plurals, groups, mass nouns, and part-whole structure (first pass).
- [x] Test aspect and event structure.
- [x] Test vague predicates and sorites-like boundaries.
- [x] Test counterfactual causation and causal uncertainty.
- [x] Test evidentiality and source reliability.
- [x] Test conflicting sources and disagreement.
- [x] Test social authority / felicity conditions in declarations, promises, commands, permissions, and prohibitions.

- [x] Formalize first-pass uncertainty/indeterminacy provenance vocabulary.
- [ ] Formalize event phase / culmination / result patterns in the standard library.

- [ ] Run layered-architecture experiment: standalone FoM vs UMR/content carrier + FoM overlay on the post-freeze corpus.
- [ ] Define a representation-agnostic semantic-carrier interface if the layered experiment succeeds.

## Representation questions

- [ ] Decide whether ordered scales require a special relation family or remain standard semantic patterns.
- [ ] Decide how generic/default knowledge is represented without turning FoM into a knowledge base.
- [ ] Decide the exact representation of open questions and alternative sets.
- [ ] Define provenance records and source maps.
- [ ] Define macro provenance and pretty-printing back to FoM Text.
- [ ] Define extension namespaces and compatibility rules.
- [ ] Define graph partitioning / partial loading.
- [ ] Define canonical serialization format (JSON-like first; binary later if useful).

- [x] Add post-freeze original mini-corpus for the translation/retelling experiment.
- [x] Validate the mini-corpus schema in CI.

## Validation / testing

- [ ] Add round-trip tests: FoM -> realization -> extraction -> semantic diff.
- [ ] Complete the Winnie-the-Pooh round trip with an independent realization.
- [x] Add the historical anecdote combat test.
- [x] Add deliberate multi-meaning tests.
- [x] Add audience-dependent decoding tests.
- [x] Add source-report vs event-reality tests.
- [ ] Add long-form trajectory tests with spoilers and delayed disclosure.
- [x] Add executable source/candidate/expected-diff corruption fixtures for first six dimensions.
- [ ] Add refinement/abstraction equivalence tests.
- [ ] Add scope-inheritance conflict tests.
- [ ] Add temporal-consistency tests.
- [ ] Add de se / de re mistaken-identity tests.

## Realization

- [x] Define first-pass PRESERVE_REFERENT / FUNCTION / EFFECT / FORM semantics.
- [x] Define first-pass realization freedom and licensed invention rules.
- [x] Define first-pass background world-knowledge licensing.
- [x] Define first-pass audience-sensitive recoverability checks.
- [x] Define first-pass realization validation model.

## Engineering

- [ ] Implement FoM Text parser.
- [ ] Implement canonicalizer.
- [ ] Implement schema validator.
- [ ] Implement macro expander.
- [ ] Implement graph visualizer.
- [ ] Implement semantic diff.
- [ ] Implement constraint validator.
- [ ] Implement simple realizer/extractor experiments.
- [x] Add CI tests; full current FoM corpus passes structural validation.

## Later

- [ ] Explore binary/canonical wire encoding.
- [ ] Explore content-addressed fragments.
- [ ] Explore ontology distribution/versioning.
- [ ] Explore long-form book representation and reader-specific realization.
- [ ] Revisit latent/generative-only structure as a separate layer without mixing it into recoverable FoM meaning.
