# Semantic stress tests

These files are adversarial examples for the FoM architecture.

The goal is not conventional unit testing yet. Each file isolates a semantic phenomenon that should be representable without adding a new Core primitive.

Current tests:

- `quantification.fom` — universal patterns, collective readings, approximation, generics.
- `binding.fom` — bound anaphora, unresolved reference, donkey binding, re-identification, de se/de re.
- `aesopian-language.fom` — in-group coded meaning, metaphorical remapping, literal rejection, audience-dependent recoverability.
- `semantic-corruption.fom` — expected semantic-diff signatures for content, certainty, explicitness, timing, focus, affect, inference, fixed unknowns, and presupposition corruption.
