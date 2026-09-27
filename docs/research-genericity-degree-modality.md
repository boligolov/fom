# Genericity, degree, and modality

Status: research note

This note stress-tests three remaining semantic areas against the current FoM Core.

Conclusion so far:

> None requires a sixth semantic primitive, but each needs an explicit reusable interface above the Core.

The three interfaces are:

```
normality/default model
ordered scale
modal accessibility model
```

## 1. Genericity

Consider:

```
Birds fly.
Birds lay eggs.
Mosquitoes carry malaria.
```

Generic statements are not ordinary universal quantification.

They are also not reducible to statistical majority:

- penguins do not fly;
- not every bird lays eggs;
- only a minority of mosquitoes may carry malaria.

Therefore:

```
GENERIC != ALL
GENERIC != MOST
```

### 1.1 Architectural requirement

A generic statement needs a kind-level or normality-relative interpretation.

A useful abstract shape is:

```
kind K
property/pattern P
normality/context model N
generic relation G(K, P, N)
```

This may license defeasible inference from an instance of K to P without asserting universal truth.

### 1.2 Defeasible inference

A generic may support:

```
bird(tweety)
therefore normally:
    can-fly(tweety)
```

but an explicit exception:

```
penguin(tweety)
penguins normally do not fly
```

must not create logical explosion.

Thus any inferential use of generics needs defeasibility/priority information.

This can be represented through INFERENTIAL relations and CONSTRAINTS rather than a new Core primitive.

### 1.3 Why no normative GENERIC macro yet

Natural-language generics are heterogeneous.

Some describe:

- characteristic properties;
- biological functions;
- social norms;
- striking dangerous properties;
- habitual behavior;
- kind-level facts.

A single expansion would currently add false precision.

Therefore `generic` remains experimental in the standard macro library.

FoM may preserve "generic mode" without prematurely deciding which theory of generic truth conditions applies.

## 2. Degree semantics

Consider:

```
almost late
barely passed
very tall
too hot to drink
enough water to survive
```

These expressions depend on ordered domains and contextual thresholds.

### 2.1 Scale interface

A scale can be represented without a new primitive as a typed node plus relations/constraints describing:

```
domain
ordering
direction
measure mapping
contextual standard
target threshold
distance / closeness
```

Example abstractly:

```
scale lateness-scale
threshold late-boundary
actual degree d
```

FoM need not assign a number to `d`.

Qualitative relations may be enough:

```
below(d, threshold)
near(d, threshold)
```

### 2.2 ALMOST

```
ALMOST(P)
```

requires:

1. P is not attained;
2. the actual state lies contextually close to P's satisfaction boundary.

For "almost late":

```
NOT late
+
close to lateness threshold from the non-late side
```

ALMOST is not low-confidence P.

### 2.3 BARELY

```
BARELY(P)
```

is approximately the mirror configuration:

1. P is attained;
2. the state is close to the satisfaction boundary.

Thus:

```
almost passed -> did not pass, near threshold
barely passed -> passed, near threshold
```

### 2.4 VERY

VERY generally means degree substantially beyond a contextual standard on the relevant scale.

It does not require an exact multiplier.

### 2.5 TOO

"too hot to drink" contains more than degree.

It links:

```
degree(hotness) exceeds threshold
+
threshold is defined relative to goal/action drink
+
excess prevents or defeats that goal/action
```

Thus TOO has a teleological/causal component.

### 2.6 ENOUGH

"enough water to survive" means:

```
quantity reaches a contextual sufficiency threshold
+
threshold is relative to goal survive
```

This is not just "a lot of water".

### 2.7 No new ORDER primitive yet

Ordered scales do require comparison semantics, but this can currently live in:

- Concept Contracts for scale types;
- open comparison predicates;
- CONSTRAINT evaluation.

A separate Core ORDER relation family is not justified yet.

If many independent phenomena later require generic ordered-domain reasoning, this decision should be revisited.

## 3. Modality

The current working model remains:

```
modal content
+
base/model of alternatives
+
accessibility relation
+
quantificational force
```

### 3.1 Epistemic possibility

"Ivan may be at home."

Approximation:

```
there exists an epistemically accessible scope
that ACCEPTS home(ivan)
```

### 3.2 Epistemic necessity

"Ivan must be at home."

Approximation:

```
all relevant epistemically accessible scopes
ACCEPT home(ivan)
```

### 3.3 Deontic necessity

"Ivan must be at home."

Deontic reading:

```
all relevant scopes satisfying the applicable norms
ACCEPT home(ivan)
```

The surface modal force may be the same while the modal base differs.

### 3.4 Ability is not plain possibility

"Ivan can open the door" does not merely mean:

```
some possible world contains door-open
```

It normally attributes ability/control to Ivan.

A stronger structure is required:

```
there exists an accessible outcome scope
where door opens
+
the transition is achievable through actions/capacities controlled by Ivan
```

Thus dynamic ability combines modality with agency/control and often causal feasibility.

No new primitive is required because:

- accessible alternatives use SCOPE;
- existential force uses BINDING/CONSTRAINT;
- control is an open semantic relation;
- causal feasibility uses CAUSAL structure where relevant.

### 3.5 Opportunity

"Ivan can enter now" may describe opportunity rather than stable ability.

The distinction may be:

```
ability:
    agent-capacity based accessibility

opportunity:
    circumstance based accessibility
```

If context does not decide, FoM should preserve the modal-base ambiguity.

## 4. Modal frame

A useful normalized interface is:

```
MODAL_FRAME {
    anchor_scope
    content
    base
    accessibility
    force
    controller?       ; for ability / agency-sensitive cases
    qualifiers
}
```

This is a standard semantic pattern, not a new Core object type.

It can compile into SCOPE + RELATION + PATTERN/BINDING + CONSTRAINT.

## 5. Result

Current Core still survives:

```
NODE
RELATION
SCOPE
DELTA
CONSTRAINT
```

But reusable semantic interfaces now include:

```
PATTERN / BINDING
normality model
scale model
modal accessibility model
```

These interfaces should be explicit enough for semantic diff without being promoted prematurely to Core primitives.
