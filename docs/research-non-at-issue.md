# Non-at-issue meaning: scalar particles, contrast, and expressives

Status: research note

Messages often carry meaning that is not part of the main asserted proposition but is still conventionally communicated.

Examples include:

- scalar particles such as "even";
- contrastive conjunctions such as "but";
- parenthetical epithets and expressives.

FoM already has enough machinery to represent these without forcing everything into one proposition.

## 1. "Даже Иван пришёл"

Headline content:

```
Ivan came
```

Additional scalar structure:

```
Ivan was relatively unlikely / low-ranked among relevant alternatives expected to come
```

and often:

```
others with higher expectation may also have come
```

The exact alternative set is context-dependent.

### Important

The scalar contribution should not be represented as mere speaker surprise.

A speaker can say "even Ivan came" calmly while still invoking the low-expectation ranking.

Thus:

```
scalar ordering != affect
```

## 2. "Иван бедный, но честный"

Headline conjunction:

```
poor(ivan)
honest(ivan)
```

BUT contributes contrast against an expectation or stereotype such as:

```
poor -> less expected honest
```

The speaker need not endorse the stereotype as a universal truth.

FoM should represent:

- both asserted propositions;
- an activated expectation/contrast relation;
- whether the expectation is attributed to speaker, culture, interlocutor, or generic common ground.

## 3. "Иван, этот идиот, пришёл"

Headline assertion:

```
came(ivan)
```

Expressive contribution:

```
speaker negative evaluation of Ivan
```

The insult is not merely evidence from which the receiver might infer dislike. It is conventionally expressed by the signal.

Thus one SIGNAL can have separate SEMIOTIC mappings:

```
asserted content
expressive/evaluative content
```

with different discourse behavior.

## 4. Projection

Some non-at-issue meanings survive embedding differently from asserted content.

Compare:

```
"Если Иван, этот идиот, придёт, мы уйдём."
```

The condition scopes over Ivan's coming, but the negative evaluation may project outside the conditional.

Therefore FoM cannot assume all semantic material inside the same sentence shares the same logical scope.

This is another reason to model meaning as a graph rather than one proposition tree.

## 5. Conventional vs inferred

FoM should distinguish:

```
CONVENTIONALLY_EXPRESSED
INFERRED
PRESUPPOSED
ASSERTED
```

These need not become primitive status values.

They can be represented through different SEMIOTIC relations, source/provenance, and constraints.

## 6. Conclusion

Non-at-issue meaning reinforces the distinction between:

```
headline truth-conditional content
speaker stance/evaluation
activated expectations
conventional side meanings
```

No new Core primitive is required, but semantic diff must compare these channels separately.
