# Temporal model

Status: research note

FoM needs temporal structure, but it should not require exact timestamps when the source gives only qualitative order.

## 1. Time objects

Time points, intervals, events, and trajectory checkpoints may be represented as nodes.

Events may carry temporal extent through relations rather than by embedding timestamps directly into event objects.

Example:

```clojure
(rel t1 occurs-during
  {:event meeting
   :time interval-17})
```

## 2. World time vs trajectory order

FoM must distinguish:

1. represented-world temporal order;
2. discourse/reader trajectory order;
3. processing order in a signal.

These can disagree.

A flashback may be late in discourse but early in world time.

A spoiler may reveal a future-world event too early in reader trajectory.

Therefore `before` is never safe as an untyped universal relation.

Temporal relations should specify their order domain or use distinct concept contracts.

## 3. Qualitative interval algebra

For represented-world intervals, the following normalized relation set appears sufficient for an initial algebra:

```
BEFORE
MEETS
OVERLAPS
STARTS
DURING
FINISHES
EQUAL
```

Inverse relations are obtained by swapping arguments:

```
AFTER         = inverse(BEFORE)
MET_BY        = inverse(MEETS)
OVERLAPPED_BY = inverse(OVERLAPS)
STARTED_BY    = inverse(STARTS)
CONTAINS      = inverse(DURING)
FINISHED_BY   = inverse(FINISHES)
```

This gives the expressive coverage of the usual 13 qualitative interval relations while avoiding duplicate primitive names.

FoM does not need to expose all of these in every message.

## 4. Partial information

A source may license only:

```
A BEFORE B
```

without giving duration, distance, or exact dates.

That information must remain partial.

The temporal reasoner may infer valid consequences such as transitivity where licensed, but must not invent exact durations.

## 5. Points and intervals

A point may be treated as a degenerate interval only if doing so does not change required semantics.

Otherwise point-like anchors may remain distinct typed nodes.

## 6. Repetition and AGAIN

AGAIN is not itself a temporal primitive.

```
AGAIN(P)
```

expands to a current instance of P plus a presupposed prior instance related through TEMPORAL ordering.

The content of P remains addressable because:

```
AGAIN(NOT P)
```

differs from:

```
NOT(AGAIN(P))
```

## 7. Temporal uncertainty

Temporal relations may themselves carry uncertainty or be scope-relative.

Example:

```
Alice believes event-A happened before event-B
```

does not require reality to accept that ordering.

## 8. Current conclusion

TEMPORAL should remain a special relation family with qualitative algebra and consistency rules.

Exact calendrical arithmetic belongs to values/tools around the graph, not to the semantic Core.
