# Aspect and event structure

Status: research note

Aspect is a stress test for the relationship between EVENT, STATE, TEMPORAL structure, and DELTA.

The main question is whether FoM needs primitive event classes such as PROCESS, ACCOMPLISHMENT, ACHIEVEMENT, or whether these can be represented compositionally.

Current conclusion:

> Event structure can remain compositional. No new Core primitive is required.

## 1. Process vs culmination

Compare:

```
Иван строил дом.
Иван построил дом.
```

The first licenses an ongoing/process view without entailing completion.

The second entails a culmination and normally a resulting state in which the house exists as completed.

A useful decomposition is:

```
building-process e1
participant: ivan
theme: house

culmination c1
terminates e1

result-state s1
completed(house)

c1 CAUSES / INITIATES s1
```

"Иван строил дом" can reference the process without committing to c1 or s1.

"Иван построил дом" requires the relevant culmination/result structure.

## 2. Imperfective paradox

A crucial test:

```
Иван строил дом, но не построил его.
```

This is coherent.

Therefore:

```
PROCESS(build-house)
does not entail
CULMINATION(build-house)
```

FoM must not encode a coarse BUILD predicate whose contract always entails completion if the source uses an imperfective/process reading.

## 3. Achievements

Compare:

```
Иван находил ключ.
Иван нашёл ключ.
```

A completed FIND normally entails a transition from not-found/not-known-location to found/identified.

The process leading to the transition may be absent or irrelevant.

Thus event granularity is demand-driven.

## 4. Progressive / ongoing view

A progressive-like reading can be represented as:

```
event e
evaluation time t
t DURING e
culmination status unresolved
```

The progressive viewpoint is a relation between an evaluation interval and an event/process, not necessarily a property stored inside the event node.

## 5. Perfective viewpoint

A perfective/completed reading may constrain the evaluation interval to include the event boundary or completed event as a whole.

This does not require PERFECTIVE as a Core primitive.

It can be represented through TEMPORAL relations and completion/result constraints.

## 6. Result state

Some predicates conventionally imply a result state.

Examples:

```
break
open
close
arrive
die
build-to-completion
```

Concept Contracts may specify such entailments.

Example:

```
OPEN_TRANSITION(agent, door)
    -> result: open(door)
```

But the transition and result should remain separately addressable when needed.

## 7. Inchoative / change of state

"Дверь открылась" can be represented as:

```
prior: closed(door) or not-open(door)
transition e
after: open(door)
```

The agent/cause may remain unknown.

FoM must not invent an agent merely because many openings are agent-caused.

## 8. START and STOP

"Иван начал курить."

Requires a transition into a process/habitual pattern.

"Иван перестал курить."

Normally presupposes or strongly requires a prior smoking state/pattern and asserts its termination.

Thus START/STOP are not just temporal adverbs. They operate on event/state patterns and can contribute presupposition.

## 9. Iterative vs habitual

Compare:

```
Иван три раза постучал.
Иван стучал по утрам.
```

The first is bounded iteration over event instances.

The second is habitual/generic recurrence across occasions.

They should not share one opaque "repeated" flag.

### Iterative

```
finite set of event instances
count = 3
```

### Habitual

```
recurrence pattern
contextual occasion domain
exceptions permitted
```

Habitual therefore interacts with genericity/default semantics.

## 10. Event identity

Two descriptions may refer to the same event under different conceptualizations.

Example:

```
Иван разбил вазу.
Ваза упала со стола.
```

The source may or may not license identity/causal linkage between the described events.

FoM should not merge them merely because a plausible story connects them.

## 11. Event mereology

Complex events may contain phases/subevents:

```
preparation
process
culmination
result
```

This can use ordinary relations:

```
part-of
phase-of
terminates
initiates
causes
before
during
```

No EVENT-STRUCTURE Core primitive is needed yet.

## 12. Current conclusion

Aspect/event structure can be modeled through:

```
typed EVENT/STATE nodes
TEMPORAL relations
CAUSAL relations
DELTA / result-state transitions
PATTERN for recurrence
CONSTRAINTS for completion / presupposition
Concept Contracts for predicate-specific entailments
```

Important design rule:

> Never infer culmination from a process description unless the concept/aspect contract explicitly licenses it.
