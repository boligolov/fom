# Quotation, use/mention, and metalinguistic negation

Status: research note

Quotation shows why SIGNAL must remain a first-class semantic object.

Metalinguistic negation shows that a negation-looking signal may target expression choice rather than world truth.

## 1. Direct quotation

```
Иван сказал: "Я устал".
```

There are at least three relevant objects:

1. Ivan;
2. the quoted signal token/type "Я устал";
3. the meaning expressed by that quoted signal in Ivan's speech context.

The indexical "я" refers to Ivan inside the quoted context.

A direct quote may require preservation of form as well as meaning.

## 2. Indirect report

```
Иван сказал, что он устал.
```

The reported content may be similar, but:

- exact wording is not asserted;
- indexicals are resolved/reframed;
- prosody/form may be lost.

Therefore direct and indirect report should not canonicalize to one signal structure merely because their headline content matches.

## 3. Nested signal context

A quoted signal needs its own production context:

```
speaker
time
place
language
indexical center
```

This can be represented as a SIGNAL node plus a scope/context node.

No QUOTE Core primitive is required.

## 4. Metalinguistic negation

Example:

```
"Он не умный — он гениальный."
```

In a common reading, the speaker does not reject:

```
intelligent(he)
```

Instead the speaker rejects the adequacy of the expression "умный" as too weak.

A naive semantic parse:

```
NOT intelligent(he)
AND genius(he)
```

would be wrong.

## 5. Target of negation

Metalinguistic negation may target:

- word choice;
- pronunciation;
- register;
- presupposition;
- scalar strength;
- framing;
- morphological form.

Therefore FoM must allow NEGATION / REJECTION to target a SIGNAL->MEANING mapping or realization choice, not only a world proposition.

## 6. Example structure

```
signal fragment: "умный"
candidate mapping:
    "умный" -> intelligent(person)

speaker:
    REJECT adequacy(mapping) in current context
    ACCEPT genius(person)
    may still ACCEPT intelligent(person)
```

This is naturally representable with SIGNAL + SEMIOTIC relation + evaluation/constraint.

## 7. Echo quotation

Signals such as:

```
Он у нас "эксперт".
```

may echo another person's word while expressing distance, skepticism, or irony.

The quoted word can therefore be:

- mentioned;
- reused;
- attributed;
- evaluated.

These channels should remain separately representable.

## 8. Translation / realization

If a quote's exact form is semantically relevant:

```
PRESERVE_FORM may be REQUIRED
```

If only quoted content matters:

```
PRESERVE_FUNCTION / REFERENT may be sufficient
```

A target-language realization must not silently translate a form-dependent pun and claim full equivalence if the quoted form relation is lost.

## 9. Current conclusion

No new Core primitive is required.

Quotation and metalinguistic negation require:

```
addressable SIGNAL fragments
SEMIOTIC mappings
nested production/context scopes
constraints over form/function
ability to reject/evaluate a mapping rather than its target proposition
```

This strengthens the principle:

```
NEGATION target must be explicit.
```
