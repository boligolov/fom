# Counterfactual causation and causal uncertainty

Status: research note

Counterfactuals and causation interact closely, but FoM must not collapse them.

The central distinction is:

```
counterfactual dependence != causal relation
```

They may support one another, but they are not definitionally identical.

## 1. Counterfactual structure

Example:

```
"Если бы не дождь, матч бы состоялся."
```

A natural representation uses:

- a reality scope;
- a counterfactual scope derived from reality;
- an explicit override;
- a consequence inside the counterfactual scope.

Reality:

```
ACCEPT rain
REJECT match-held
```

Counterfactual:

```
REJECT rain
ACCEPT match-held
```

The relation between the scopes is not merely temporal. It is an alternative-world/model relation.

## 2. But-for dependence

The statement may license:

```
absence(rain) -> match-held
```

as a counterfactual dependence.

This can support an inference:

```
rain contributed causally to cancellation
```

but that causal conclusion should be represented separately.

## 3. Why dependence is not causation

Consider:

```
If Ivan had not been born, he would not have pressed the button.
```

The birth is counterfactually relevant to the button press in a broad sense, but a target FoM may not want to represent it as the immediate cause of the light turning on.

Causal granularity matters.

## 4. Overdetermination

Suppose two independent fires each would have been sufficient to destroy a house.

Actual world:

```
fire-A
fire-B
house-destroyed
```

Removing only fire-A may still leave:

```
house-destroyed
```

Yet fire-A may still count as a cause under some causal models.

Therefore simple but-for dependence is not a universal definition of causation.

FoM should not bake one philosophical theory of causation into the Core.

## 5. Counterfactual scope relation

A useful standard pattern:

```
COUNTERFACTUAL {
    base_scope
    alternative_scope
    overrides
    retained assumptions
    accessibility / similarity constraints
}
```

This can be implemented through SCOPE + CONSTRAINT without a new Core primitive.

The exact "closest worlds" theory is not part of the Core.

## 6. Causal uncertainty

Example:

```
"Возможно, пожар начался из-за короткого замыкания."
```

The modal operator scopes over the CAUSAL relation:

```
POSSIBLE(
    CAUSES(short-circuit, fire)
)
```

Reality need not ACCEPT that causal relation.

Thus CAUSAL relations themselves are scope-relative content.

## 7. Temporal order is insufficient

```
short-circuit BEFORE fire
```

does not imply:

```
short-circuit CAUSES fire
```

This remains an important validation rule.

## 8. Evidence for causation

A report may contain:

```
burn pattern
electrical damage
timing
```

which INFERENTIALLY supports a causal hypothesis.

Again:

```
evidence-for(cause)
!=
cause
```

## 9. Causal chains

FoM may represent multiple levels:

```
spark -> ignition -> fire -> structural damage
```

A realization may legitimately abstract this to:

```
short-circuit caused damage
```

only if the Concept Ontology / abstraction rules license that causal compression and no required intermediate step is lost.

## 10. Current conclusion

No new Core primitive is required.

Counterfactual causation uses:

```
SCOPE
CONSTRAINT
CAUSAL relations
INFERENTIAL relations
TEMPORAL relations
modal accessibility
```

The important invariant is:

> Keep actual causation, counterfactual dependence, temporal order, and evidence for causation as distinct relations.
