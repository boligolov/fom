# Evidentiality, source reliability, and disagreement

Status: research note

FoM needs to distinguish:

- what proposition is under discussion;
- how the information was obtained;
- who the source is;
- how reliable that source is considered;
- how strongly an agent accepts the proposition.

These are separate semantic dimensions.

## 1. Direct report

```
"По словам Ивана, поезд ушёл."
```

The speaker strongly commits to:

```
Ivan said P
```

but may remain uncommitted about:

```
P = train left
```

Therefore source attribution must not collapse into assertion.

## 2. Direct perception

```
"Я видел, как поезд ушёл."
```

The signal represents a perceptual-evidence relation:

```
speaker visually perceived event E
```

and often licenses strong ACCEPT(E).

But these are still two structures:

```
perception evidence
epistemic update
```

A hallucination/error scenario can separate them.

## 3. Hearsay

```
"Говорят, поезд ушёл."
```

The source may be underspecified or collective.

FoM should preserve:

```
source = unspecified hearsay network
```

rather than inventing a concrete speaker.

## 4. Inferential evidence

```
"Поезд, видимо, ушёл."
```

The proposition may be supported by indirect evidence:

- empty platform;
- timetable;
- sound fading;
- absence of train.

The evidential route differs from hearsay even if certainty is similar.

## 5. Reliability belongs to a model

Source reliability is not an objective scalar attached forever to a person.

A source may be:

- reliable about train schedules;
- unreliable about medicine;
- honest but mistaken;
- deceptive in one context;
- unknown.

Therefore reliability should be:

```
scope-relative
domain-relative
context-relative
```

and preferably qualitative unless precise probability is actually licensed.

## 6. Reliability vs truth

```
reliable(source)
```

does not entail every claim by the source.

```
unreliable(source)
```

does not entail every claim is false.

Reliability affects inference strength.

## 7. Source conflict

Example:

```
Alice says P.
Bob says NOT P.
```

Represent:

```
scope Alice-report: ACCEPT P
scope Bob-report: ACCEPT NOT P
```

A synthesis scope can remain uncommitted with:

```
:indeterminacy-source :source-conflict
```

Confidence may later change when reliability/evidence is assessed.

## 8. Evidential source vs epistemic certainty

These axes must remain independent.

Examples:

```
direct perception + low certainty
hearsay + high confidence
inference + high confidence
official source + unresolved conflict
```

No one-to-one mapping is valid.

## 9. Nested source chains

```
Alice says that Bob told her that Carol saw P.
```

FoM can preserve the chain when it matters:

```
Carol perceived P
Bob reports Carol's report
Alice reports Bob's report
current speaker reports Alice
```

If the intermediate hops are irrelevant, abstraction may compress them only when source/provenance constraints permit.

## 10. Deception

A source may report P while believing NOT P.

That is a lie pattern, but the hearer's evidence relation remains:

```
source reported P
```

Reliability and sender-intention structure affect how much weight the report should receive.

## 11. Current conclusion

No new Core primitive is required.

Evidentiality is represented using:

```
SOURCE nodes
SEMIOTIC report relations
perception/evidence relations
INFERENTIAL support
SCOPE-relative source models
epistemic qualifiers
indeterminacy provenance
```

The central rule is:

> Evidence type, source reliability, and degree of belief are independent dimensions.
