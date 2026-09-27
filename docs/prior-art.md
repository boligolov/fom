# Prior art and FoM positioning

Status: working comparison, not a novelty claim

FoM overlaps substantially with established work in formal semantics, pragmatics, discourse representation, and meaning representation.

This document exists to prevent accidental reinvention.

The rule for the project is:

> If an established formalism already solves a subproblem adequately, FoM should reuse, adapt, map to, or interoperate with it rather than rename it.

Any statement below that a FoM idea is "distinctive" is a research hypothesis to be tested against the literature, not a claim of originality.

## 1. Comparison matrix

| FoM area | Closest prior work | What prior work already provides | FoM direction |
| --- | --- | --- | --- |
| Predicate/argument semantic graph | AMR | Graph-based sentence meaning representation / sembanking | Do not reinvent basic predicate-argument representation without a reason; investigate AMR/UMR interoperability |
| Cross-lingual document meaning | UMR | Sentence graph plus document graph; aspectuality; coreference; temporal and modal relations; multilingual annotation | Treat UMR as the strongest immediate neighboring representation and compare field-by-field |
| Meaning as state/context change | Dynamic semantics; Heim-style file change; update semantics | Meaning as context-change potential / information-state update | FoM's delta/state view is not novel by itself; define exactly which state dimensions and validation constraints go beyond existing update semantics |
| Discourse referents and accessibility | DRT | Incremental discourse representation, anaphora, tense, accessibility | Prefer established accessibility insights instead of inventing a binding theory from scratch |
| Discourse coherence relations | SDRT | Narration, Result, Explanation, Contrast, Elaboration, discourse structure and accessibility constraints | Compare FoM inference/trajectory relations with SDRT before defining a new discourse-relation layer |
| Shared conversational state | Stalnaker/common-ground tradition | Shared/presumed information and speech-act changes to common ground | FoM's shared-state model should explicitly map to common-ground concepts |
| Speech/social acts | Austin; Searle and successors | Illocutionary acts, felicity conditions, authority/procedure, successful vs failed acts | FoM can express these as attempted/actual deltas, but the act taxonomy and felicity theory should reuse prior work |
| Said vs implicated | Grice and later pragmatics | Speaker meaning, conversational implicature, inference from context/shared assumptions, cancellability | FoM's explicit inference paths should be compared to Gricean and post-Gricean accounts rather than treated as newly discovered |
| Questions / issue resolution | Hamblin/Karttunen traditions; partition semantics; inquisitive semantics | Alternatives/issues and resolution conditions | FoM question-state deltas should map to issue semantics rather than inventing a standalone question theory |
| Temporal interval relations | Allen interval algebra | Qualitative interval relations and composition-based temporal reasoning | Adopt Allen-style relations where applicable instead of a home-grown interval taxonomy |
| Vagueness / precisifications | Supervaluationism, especially Fine/Kamp traditions | Admissible precisifications, borderline cases, supertruth/superfalsity | FoM precisification scopes are an implementation/adaptation candidate, not a novel vagueness theory |
| Quantification/scope/modality in graph meaning representations | UMR precursor work on AMR scope | Scope graphs for quantification, negation and modality | Compare FoM PATTERN/SCOPE machinery directly with UMR rather than treating graph scope as unique |
| Coreference/temporal/modal document annotation | UMR | Explicit document-level :coref, :temporal, :modal dependencies | FoM should justify every parallel mechanism that is not simply reusable UMR structure |

## 2. AMR

Abstract Meaning Representation (AMR) was introduced as a graph-based semantic representation for sembanking.

FoM overlaps with AMR wherever it represents ordinary semantic content as nodes, predicates, roles, and relations.

### Working decision

FoM should not spend research effort proving that graph-shaped predicate/argument structure is useful.

Instead:

- identify the subset of FoM CONTENT that could be imported from or exported to AMR;
- document losses in both directions;
- prefer compatibility over gratuitous reinvention.

Reference:

- Banarescu et al. (2013), *Abstract Meaning Representation for Sembanking*: https://aclanthology.org/W13-2322/

## 3. UMR

Uniform Meaning Representation is the most important immediate neighbor for FoM.

The published UMR infrastructure includes:

- sentence-level predicate-argument graphs;
- named entities and word senses;
- event aspectuality;
- person and number;
- document-level coreference;
- document-level temporal relations;
- document-level modal relations;
- multilingual/cross-linguistic annotation.

Earlier UMR work explicitly extended AMR with scope mechanisms for quantification, negation and modality.

### Working decision

Before expanding FoM CONTENT/TEMPORAL/MODAL/COREFERENCE machinery, compare it directly against UMR.

A plausible architecture to investigate is:

```
UMR or UMR-like semantic/content layer
              +
FoM transformation / constraint layer
```

where the FoM-specific layer concentrates on:

- intended / attempted / actual receiver/shared-state deltas;
- recoverability vs explicitness;
- disclosure trajectory;
- FIXED_UNKNOWN and realization invariants;
- semiotic-function constraints;
- multidimensional semantic diff;
- licensed invention;
- audience-relative recoverability.

This architecture is only a hypothesis. It must be tested for whether the layering is actually clean.

References:

- Pustejovsky, Lai & Xue (2019), *Modeling Quantification and Scope in Abstract Meaning Representations*: https://aclanthology.org/W19-3303/
- Bonn et al. (2024), *Building a Broad Infrastructure for Uniform Meaning Representations*: https://aclanthology.org/2024.lrec-main.229/
- Chun & Xue (2024), *Uniform Meaning Representation Parsing as a Pipelined Approach*: https://aclanthology.org/2024.textgraphs-1.3/
- UMR document-level annotation schema: https://umr4nlp.github.io/web/UMRSchemaPages/Document-Level-Graph.html

## 4. Dynamic semantics

Dynamic semantics explicitly treats linguistic meaning as an update to an information state/context.

The slogan "meaning is context change potential" is already standard in this tradition.

This is very close to the original FoM intuition:

```
Meaning ≈ intended Δ State
```

### Working decision

The delta/state framing alone cannot be treated as FoM's contribution.

The research question becomes narrower:

> Does FoM define a useful richer state/update contract for translation, realization and comparison that is not already captured by existing dynamic frameworks?

Potentially relevant FoM additions include changes to:

- epistemic state;
- attention/salience;
- affect;
- social commitments/permissions;
- shared state;
- expected inference routes;
- disclosure/recoverability.

Each of these must be compared against existing work before being claimed as additional scope.

References:

- Stanford Encyclopedia of Philosophy, *Dynamic Semantics*: https://plato.stanford.edu/entries/dynamic-semantics/
- Stanford Encyclopedia of Philosophy, *Theories of Meaning*, dynamic-semantics section: https://plato.stanford.edu/entries/meaning/

## 5. DRT and discourse accessibility

Discourse Representation Theory was developed by Hans Kamp in the early 1980s, with closely related independent work by Irene Heim.

DRT already addresses:

- discourse-level representation;
- discourse referents;
- anaphora;
- tense;
- accessibility;
- propositional-attitude contexts in later developments.

### Working decision

FoM's PATTERN/BINDING/accessibility work should be checked against DRT/dynamic semantics before any custom binding semantics is stabilized.

The current FoM distinction between:

```
mention
reference
identity
coreference
bound/dependent reference
```

may still be a useful engineering interface, but it is not evidence of theoretical novelty.

Reference:

- Stanford Encyclopedia of Philosophy, *Discourse Representation Theory*: https://plato.stanford.edu/entries/discourse-representation-theory/

## 6. SDRT and discourse relations

Segmented Discourse Representation Theory extends DRT with discourse/coherence relations such as:

- Narration;
- Result;
- Contrast;
- Explanation;
- Elaboration;
- Correction.

These relations can interact with temporal interpretation and anaphoric accessibility.

### Working decision

Before FoM standardizes relations such as narrative explanation, reinterpretation, contrast, or discourse coherence, compare them against SDRT.

FoM may need different machinery for intended receiver-state trajectories, but it should not duplicate a discourse-relation inventory merely under different names.

Reference:

- DRT article section discussing SDRT: https://plato.stanford.edu/entries/discourse-representation-theory/

## 7. Common ground

The common-ground tradition, especially associated with Stalnaker, treats discourse as occurring against shared/presumed information and studies how speech acts alter that common state.

This directly overlaps with FoM's SHARED/CONVERSATIONAL state.

### Working decision

FoM should explicitly distinguish:

- individual agent state;
- sender's model of receiver state;
- receiver state;
- common/shared ground;
- social/institutional state.

The shared-information part should map to common-ground theory rather than be presented as a new construct.

Reference:

- Stanford Encyclopedia of Philosophy, *Common Ground in Pragmatics*: https://plato.stanford.edu/entries/common-ground-pragmatics/

## 8. Speech acts and felicity conditions

Austin's speech-act theory explicitly treats some utterances as actions whose success depends on conditions such as accepted procedure, proper participants, authority, time and circumstances.

This maps closely to the FoM distinction:

```
intended social operation
attempted DELTA
felicity conditions
actual DELTA
```

### Working decision

The FoM representation may be a useful computational encoding of the distinction, but the distinction itself is prior art.

FoM should reuse established speech-act vocabulary when possible and focus on how such acts interact with semantic diff, realization, audience, and state trajectories.

Reference:

- Stanford Encyclopedia of Philosophy, *Speech Acts*: https://plato.stanford.edu/entries/speech-acts/

## 9. Grice and implicature

Grice distinguishes what is said from what a speaker communicates beyond what is literally said, and models conversational implicature through inference involving context, shared assumptions, and rational/cooperative principles.

This overlaps strongly with FoM's:

```
literal content
+
context dependencies
+
inference path
+
intended conclusion
```

### Working decision

FoM's useful engineering hypothesis is not "implicature has an inference path"; that is established territory.

A more specific hypothesis is:

> preserving or changing a required inference route can be an independent dimension of semantic diff, even when the final inferred proposition is preserved.

That claim should be tested experimentally.

References:

- Stanford Encyclopedia of Philosophy, *Paul Grice*: https://plato.stanford.edu/entries/grice/
- Stanford Encyclopedia of Philosophy, *Implicature*: https://plato.stanford.edu/entries/implicature/

## 10. Questions and inquisitive semantics

Modern theories of questions treat questions in terms of alternatives/issues and conditions under which an issue is resolved. Inquisitive semantics develops this explicitly.

This substantially overlaps with FoM's open-question state and alternative-set representation.

### Working decision

FoM should not invent independent truth conditions for questions.

Instead, it should investigate how issue semantics connects to:

- DELTA over conversational state;
- trajectory;
- partial resolution;
- disclosure;
- salience.

Reference:

- Stanford Encyclopedia of Philosophy, *Questions*: https://plato.stanford.edu/entries/questions/

## 11. Allen interval algebra

James F. Allen's 1983 interval-based temporal logic introduced a qualitative system for reasoning about temporal intervals. The familiar algebra distinguishes thirteen basic interval relations, with converse pairs and equality.

Our provisional FoM set:

```
BEFORE
MEETS
OVERLAPS
STARTS
DURING
FINISHES
EQUAL
```

plus inverses is effectively an Allen-style normalization.

### Working decision

Use Allen interval algebra as the default prior art for qualitative interval relations.

FoM should only add machinery where required for:

- scope-relative temporal beliefs;
- uncertain/partial temporal knowledge;
- distinction between world time and reader/discourse trajectory;
- semantic-diff constraints.

References:

- Allen (1983), *Maintaining Knowledge about Temporal Intervals*, Communications of the ACM 26(11), 832–843, DOI 10.1145/182.358434.
- Expository relation table: https://ics.uci.edu/~alspaugh/cls/shr/allen.html

## 12. Supervaluationism and vagueness

Supervaluationist approaches represent vague language through admissible precisifications; a borderline statement can receive different classical values under different admissible sharpenings.

This is directly analogous to the FoM experiment using precisification scopes.

### Working decision

Do not present precisification scopes as a new theory of vagueness.

Instead, treat them as a possible graph encoding of supervaluation-style structure where that theory is appropriate.

FoM should remain neutral where a source does not require commitment to a particular philosophical theory of vagueness.

References:

- Stanford Encyclopedia of Philosophy, *Vagueness*: https://plato.stanford.edu/entries/vagueness/
- Fine (1975) is among the seminal references discussed in the SEP material.

## 13. Annotation reliability is part of the problem

Existing meaning-representation projects show that trained annotators can disagree substantially even on narrower semantic dimensions.

A 2024 case study of Chinese aspect annotation with UMR reports, for example, Fleiss' kappa of approximately 0.53 for the UMR aspect lattice despite trained linguist annotators.

### Working decision

FoM cannot define success as "two annotators drew the same graph."

We need to measure agreement separately on:

- required content;
- reference;
- scope/status;
- uncertainty/indeterminacy provenance;
- inference route;
- disclosure/trajectory;
- affect/social state;
- resolution level / decomposition.

Reference:

- *Annotate Chinese Aspect with UMR — A Case Study* (LREC-COLING 2024): https://aclanthology.org/2024.lrec-main.104/

## 14. Candidate FoM contribution: hypotheses, not claims

After this comparison, the following remain plausible areas where FoM may add a useful engineering/research layer.

They are not yet established as novel.

### 14.1 Recoverability separate from explicitness

FoM distinguishes whether content is explicit, inferable, or latent from whether it is required to be recoverable for a target audience at a trajectory position.

Research question:

> Does this distinction improve evaluation of translation/retelling beyond existing semantic graphs?

### 14.2 Disclosure trajectory as semantic invariant

FoM can mark content:

```
PROHIBITED before checkpoint
REQUIRED after checkpoint
```

Research question:

> Can this detect meaning failures such as spoilers or premature explanation that proposition-level equivalence misses?

### 14.3 FIXED_UNKNOWN

FoM can require an unknown/ambiguity to remain unresolved.

Research question:

> Can this catch hallucinated specificity and overtranslation reliably?

### 14.4 Multidimensional semantic diff

Rather than one similarity score, FoM compares dimensions such as:

```
content
reference
certainty
presupposition
explicitness
inference path
timing/disclosure
focus/salience
affect
social state
resolution
licensed invention
```

Research question:

> Are these dimensions independently annotatable and predictive of human judgments?

### 14.5 Constraint-satisfaction equivalence

FoM treats required semantic equivalence as satisfaction of required invariants rather than graph identity.

Research question:

> Can independently produced representations disagree structurally but still yield stable agreement on required constraints?

### 14.6 Licensed invention

Realization may add compatible details when explicitly licensed, but must not alter required meaning, inference space or protected unknowns.

Research question:

> Is this a useful operational contract for controlled LLM realization?

### 14.7 Referential / functional / effect / form preservation

FoM distinguishes:

```
PRESERVE_REFERENT
PRESERVE_FUNCTION
PRESERVE_EFFECT
PRESERVE_FORM
```

Research question:

> Does this provide a useful framework for translation of jokes, coded language, stylistic signals and form-dependent meaning?

### 14.8 Intended / attempted / actual deltas across state dimensions

Dynamic semantics supplies the broad update perspective; speech-act theory supplies many social-act distinctions.

FoM's candidate contribution is a unified graph/diff interface that applies the intended/attempted/actual distinction across epistemic, attentional, affective, social and shared state.

This needs literature comparison and empirical justification.

### 14.9 Deliberate co-activation of readings

FoM distinguishes unresolved ambiguity from communication where several readings are intentionally required simultaneously and their relationship is part of the effect.

This should be compared more deeply with the literature on puns, double entendre, ambiguity, polysemy and lexical pragmatics before any novelty claim.

## 15. Immediate architectural consequence

The project should test whether FoM can be factored as:

```
established semantic representation
    (UMR / DRT-like content where appropriate)

+

FoM transformation/constraint layer
    receiver/shared-state delta
    recoverability
    trajectory/disclosure
    semantic-preservation constraints
    multidimensional diff
    realization freedom
```

If this factoring works, FoM becomes smaller and easier to validate.

If it does not, the failed mappings will identify exactly which semantic structures FoM needs to own itself.

## 16. Research rule going forward

For every proposed new FoM mechanism:

1. identify the closest prior formalism;
2. show whether it can represent the case;
3. reuse it if adequate;
4. add FoM machinery only for a demonstrated missing requirement;
5. add an executable test for that requirement.

"No new Core primitive was needed" is no longer considered evidence by itself. The test must be executable or tied to a falsifiable empirical evaluation.
