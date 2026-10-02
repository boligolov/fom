# TODO

Working list of unfinished FoM research and implementation tasks.

## Highest priority

- [x] Freeze broad semantic expansion while tooling and empirical validation catch up.
- [x] Make the current FoM corpus parse and structurally validate in CI.
- [x] Add first executable torture-test discipline rule against phenomenon-name predicates.
- [x] Add prior-art comparison matrix: FoM vs AMR/UMR, DRT/dynamic semantics, common ground, speech acts, Allen, supervaluation, questions/discourse frameworks.
- [x] Design annotation-agreement experiment.
- [ ] Run annotation-agreement pilot with independent annotators (requires genuinely independent annotators/models).
- [x] Freeze an evidence-backed v2 author proposal for all ten source texts and generate blind-at-delivery Pass A packets; independent responses and adjudication remain pending.
- [x] Collect two same-model fresh-context Pass A responses, validate source evidence, and record a qualitative review (required wordplay remains disputed; external/different-model pilot remains pending).
- [x] Version neutral source-status/preservation clarification and author errata without rewriting earlier responses (annotation_v21).
- [x] Collect and review one fresh-context GPT-5.6-terra response under v2.1; model/instruction effects are confounded and P02/P05/P06 obligations remain open.
- [x] Collect a fresh same-instruction v2.1 response and align preservation objects across dispatch configurations; exact model independence and semantic adjudication remain open (Run 03).
- [ ] Build and independently review a realization contrast set for P02/P05/P06/P10 to test cue preservation versus separate inference obligations; do not force an invalid cue-preserving contrast.
- [x] Define first narrow end-to-end use case: translation/retelling preservation validation.

- [x] Define enough canonical schema for first-pass parser/canonicalizer implementation.
- [ ] Tighten canonical schema for macros, provenance, extension contracts and generated-ID stability.
- [x] Prevent generated relation/status IDs from colliding with explicit declarations, including later and nested declarations.
- [ ] Specify deterministic macro expansions for the standard library.
- [x] Define canonicalization / normal-form rules.
- [ ] Decide how stable IDs, generated IDs, and cross-document references work.
- [ ] Specify module/import semantics for larger FoM documents.
- [x] Build a minimal parser for FoM Text.
- [x] Build first-pass validator for syntax, references, bindings, scopes, and structural constraints.
- [x] Build first executable semantic-diff subset (content, certainty, salience, inference, disclosure, fixed-unknown).
- [x] Remove relation/subgraph ID dependence and add conservative unique-node structural alignment.
- [ ] Extend semantic diff to ambiguous graph matching and broadly independently decomposed graphs.
- [x] Add first contract-driven refinement/abstraction matching.

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
- [x] Run seven-pair carrier/overlay feasibility pilot and audit all ten source cases; independent annotation cost/agreement and actual UMR validation remain open (experiments/layered_architecture).
- [ ] Define a representation-agnostic semantic-carrier interface if the layered experiment succeeds.

## Representation questions

- [ ] Decide whether ordered scales require a special relation family or remain standard semantic patterns.
- [ ] Decide how generic/default knowledge is represented without turning FoM into a knowledge base.
- [ ] Decide the exact representation of open questions and alternative sets.
- [x] Define first-pass provenance records and source maps with complete source spans.
- [x] Implement optional record-level source spans, including anonymous applications and statuses.
- [ ] Define macro provenance and pretty-printing back to FoM Text.
- [ ] Define extension namespaces and compatibility rules.
- [ ] Define graph partitioning / partial loading.
- [ ] Define canonical serialization format (JSON-like first; binary later if useful).

- [x] Add post-freeze original mini-corpus for the translation/retelling experiment.
- [x] Validate the mini-corpus schema in CI.

## Validation / testing

- [ ] Add round-trip tests: FoM -> realization -> independent extraction -> semantic diff.
- [ ] Complete the Winnie-the-Pooh round trip with an independent realization.
- [x] Add the historical anecdote combat test.
- [x] Add deliberate multi-meaning tests.
- [x] Add audience-dependent decoding tests.
- [x] Add source-report vs event-reality tests.
- [ ] Add long-form trajectory tests with spoilers and delayed disclosure.
- [x] Add executable controlled corruption fixtures for eight dimensions.
- [x] Tie seven post-freeze benchmark cases to executable gold FoM source/corrupted pairs.
- [x] Add first executable refinement/abstraction equivalence tests using Concept Contracts.
- [x] Add executable scope-inheritance conflict, shadow, cycle, and isolation tests.
- [ ] Add temporal-consistency tests.
- [ ] Add de se / de re mistaken-identity tests.

## Realization

- [x] Define first-pass PRESERVE_REFERENT / FUNCTION / EFFECT / FORM semantics.
- [x] Define first-pass realization freedom and licensed invention rules.
- [x] Define first-pass background world-knowledge licensing.
- [x] Define first-pass audience-sensitive recoverability checks.
- [x] Define first-pass realization validation model.

## Engineering

- [x] Implement FoM Text parser.
- [x] Implement first-pass canonicalizer (structural normalization; macro expansion and full schema remain incomplete).
- [x] Implement first-pass structural/schema validator.
- [ ] Implement macro expander.
- [x] Implement the first macro expansion (SELF), shared by check/canonical/diff, with scope validation and substitution provenance.
- [ ] Implement graph visualizer.
- [x] Implement first executable semantic-diff subset.
- [ ] Implement semantic constraint evaluator beyond static structural validation.
- [x] Implement first status-constraint evaluation profile (status-is/unknown) against source or candidate state, with explicit unsupported outcomes; generic preservation evaluation remains open.
- [x] Implement first derived scope-status resolver for none/overlay inheritance and explicit uncommitted shadows (not a generic constraint evaluator).
- [ ] Implement simple realizer/extractor experiments.
- [x] Add CI tests; full current FoM corpus passes structural validation.

## Later

- [ ] Explore binary/canonical wire encoding.
- [ ] Explore content-addressed fragments.
- [ ] Explore ontology distribution/versioning.
- [ ] Explore long-form book representation and reader-specific realization.
- [ ] Revisit latent/generative-only structure as a separate layer without mixing it into recoverable FoM meaning.
