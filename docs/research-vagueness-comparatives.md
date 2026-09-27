# Vagueness, comparatives, and superlatives

Status: research note

Vagueness exposes a distinction that FoM must preserve:

> semantic indeterminacy is not the same as epistemic uncertainty.

## 1. "Иван высокий"

Suppose Ivan's exact height is known.

The statement may still be borderline because "tall" depends on a contextual comparison class and a vague standard.

Thus the uncertainty is not:

```
we do not know Ivan's height
```

but:

```
the contextual boundary for tall is not sharp / uniquely fixed
```

## 2. Precisification model

A useful standard pattern is a set of admissible precisification scopes.

Each precisification supplies a sharper contextual threshold.

Example:

```
scope p1:
    tall-threshold = 180
    ACCEPT tall(ivan)

scope p2:
    tall-threshold = 185
    REJECT tall(ivan)
```

If both are admissible:

```
tall(ivan)
```

is semantically borderline in the parent context.

This is not ordinary ignorance.

## 3. Status of borderline content

FoM does not need a new Core status value if BORDERLINE is represented as a derived constraint over admissible scopes:

```
some admissible precisifications ACCEPT P
some admissible precisifications REJECT P
```

The parent scope may remain UNCOMMITTED while the reason for non-commitment is explicitly semantic-vagueness rather than missing evidence.

This suggests a qualifier/source for uncertainty:

```
:indeterminacy-source :vagueness
```

## 4. Comparatives

```
Иван выше Петра.
```

This can be determinate even if neither:

```
Иван высокий
Пётр высокий
```

is determinate.

Comparative structure:

```
degree(height, ivan) > degree(height, petr)
```

The exact numeric heights are unnecessary if ordering is all the source provides.

## 5. "Намного выше"

Adds a contextual constraint on difference magnitude:

```
difference(height(ivan), height(petr))
is contextually large
```

No exact centimeters should be invented.

## 6. Superlatives

```
Иван самый высокий в группе.
```

Requires:

```
comparison class C
ivan in C
for every relevant member x in C:
    height(ivan) >= height(x)
```

Strict uniqueness may or may not be entailed.

Natural language can allow ties depending on context.

Therefore a superlative contract must state whether:

- unique maximum is required;
- ties are permitted;
- comparison class is fixed or context-inferred.

## 7. Contextual comparison class

"Иван высокий" may mean:

- tall for a child;
- tall for a basketball player;
- tall among the people in this room.

The comparison class is semantically relevant.

If omitted by the signal, FoM may preserve it as a context dependency rather than invent one.

## 8. Sorites

Vagueness permits chains where adjacent differences are too small to motivate a sharp boundary, yet endpoints differ clearly.

FoM should not force one hidden exact cutoff merely to make validation easier.

A precisification set or interval of acceptable thresholds preserves this correctly.

## 9. Scale interface

Degree semantics uses a standard scale model:

```
subject
dimension
ordered domain
degree/value or qualitative position
contextual comparison class
threshold/standard
```

This remains above the Core.

No special ORDER primitive is justified yet.

## 10. Current conclusion

No new Core primitive is required.

Vagueness can be represented using:

```
SCOPE over admissible precisifications
scale relations
CONSTRAINTS
explicit source of indeterminacy
```

Comparatives and superlatives use PATTERN/BINDING plus ordered-scale relations.

Important new design distinction:

```
UNKNOWN because evidence missing
!=
UNCOMMITTED because predicate is semantically borderline
```
