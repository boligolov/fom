# Groups, reciprocals, mass nouns, and part-whole structure

Status: research note

Plurality is not one phenomenon.

FoM should distinguish:

- plural collections;
- group entities;
- distributive predication;
- collective predication;
- reciprocal relations;
- mass/substance reference;
- portions and quantities;
- part-whole relations.

No new Core primitive is currently required.

## 1. Group entity vs member set

A team, committee, crowd, or couple may be represented as an addressable group node.

```
group G
members(G) = {a, b, c}
```

Predicates may target:

- G as one participant;
- each member;
- subsets/pairs of members.

These readings are not interchangeable.

## 2. Collective predicate

```
Студенты подняли пианино.
```

may describe one lifting event with the group as collective agent.

It does not entail that every student independently lifted the piano.

## 3. Distributive predicate

```
Студенты получили по письму.
```

requires a member-wise pattern.

PATTERN/BINDING handles this without turning plurality into a Core mechanism.

## 4. Reciprocal predicate

```
Иван и Пётр встретились.
```

cannot be represented as:

```
meet(ivan, ivan)
meet(petr, petr)
```

A reciprocal reading constrains distinct members of a plural/group participant to stand in a relation.

For two participants:

```
meet(ivan, petr)
```

For larger groups, natural-language reciprocity may be weaker than every-pair coverage.

Example:

```
The students know each other.
```

may contextually tolerate network connectivity rather than all-to-all acquaintance.

Therefore reciprocity should be a standard pattern with a coverage constraint, not a hard-coded complete graph.

## 5. Distributive/collective ambiguity

```
Три студента написали статью.
```

may mean:

- one article written collectively;
- one article per student;
- several articles in another distribution.

If context does not resolve this, FoM must preserve the reading set.

## 6. Mass nouns

```
Вода покрыла пол.
```

The relevant semantic object is not necessarily the abstract substance-kind WATER and not a countable object.

Useful distinctions:

```
substance kind: water
contextual portion: water-portion-17
quantity/measure: optional
```

The event normally involves a portion/amount of water.

Exact quantity need not be known.

## 7. Portions

A portion node may be linked to a substance kind:

```
portion-of(water-portion-17, water)
```

This allows:

```
water is drinkable
this water is dirty
two liters of water
some water spilled
```

to refer at different semantic resolutions.

## 8. Part-whole

Useful open relations include:

```
part-of
member-of
portion-of
component-of
region-of
```

They should not be collapsed into one generic PART relation if their inferential contracts differ.

For example:

```
member-of(person, team)
```

does not license the same reasoning as:

```
wheel part-of car
```

or:

```
water-portion portion-of water-substance
```

## 9. Quantities

Measure phrases can attach to portions:

```
quantity(water-portion, 2 liters)
```

FoM should preserve exact measurement only when the source provides it.

## 10. Current conclusion

Plural/mass semantics can be represented through:

```
NODE types (group, portion, substance-kind)
open mereological/member relations
PATTERN/BINDING
CONSTRAINTS on distribution/reciprocity
ambiguity when reading is unresolved
```

No GROUP or MASS Core primitive is justified yet.
