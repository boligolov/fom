# Historical reports, source chains, and legend

Status: research note

Historical narrative is a useful FoM stress test because the representation must distinguish:

- an event;
- a later report of the event;
- a report of somebody remembering the event;
- evidence for the event;
- later embellishment;
- narrator confidence.

## 1. Newton's apple as a test case

William Stukeley's later memoir records a conversation with Newton on 15 April 1726. Stukeley says that while they sat in a garden under apple trees, Newton described an earlier occasion on which the fall of an apple prompted thoughts about gravitation.

John Conduitt also left a draft account describing Newton, during the plague period, musing in a garden about the power that made an apple fall and whether the same power extended as far as the Moon.

These documents strongly support:

```
Stukeley reported that Newton told him apple-story P
Conduitt reported apple-story Q
```

They do not automatically entail:

```
every detail of P/Q happened exactly as narrated decades earlier
```

## 2. Source proposition vs world proposition

FoM should represent:

```
SOURCE S reports P
```

independently from:

```
REALITY accepts P
```

A source report may create an INFERENTIAL relation:

```
report(S, P)
    evidence_for
P
```

with qualifiers such as:

- source type;
- temporal distance;
- directness;
- attribution;
- editorial transmission;
- confidence/reliability where modeled.

## 3. Multi-hop testimony

Stukeley's structure is approximately:

```
historical event E
  -> Newton remembers/describes E
  -> Stukeley hears Newton
  -> Stukeley records the conversation
  -> later editor/digital edition transmits text
  -> modern reader
```

FoM should preserve relevant hops when they matter.

It need not model every publication layer if those layers have no semantic relevance to the task.

## 4. What can be high-confidence

The historical evidence may support different claims at different strengths.

For example:

```
Stukeley wrote an apple account
    high confidence

Stukeley attributed the account to Newton
    high confidence

Newton actually told Stukeley substantially this story
    strong evidence

an apple actually fell during Newton's earlier reflection
    supported by testimony, but not directly observed by Stukeley

the apple struck Newton on the head
    not supported by these source passages

the apple instantly produced the complete theory of universal gravitation
    stronger than the source wording and should not be silently inferred
```

FoM must allow these claims to have different epistemic status.

## 5. Legend and embellishment

A later popular version may add:

```
apple hits Newton on head
instant eureka
complete theory appears at once
```

Those additions can be modeled as a separate LEGEND / RETELLING scope.

They should not be copied into the historical-reality scope without evidence.

This enables semantic diff between:

```
source report
historical reconstruction
popular legend
```

## 6. Attribution matters

Compare:

```
Newton discovered gravity when an apple fell.
```

with:

```
Stukeley reports that Newton later said an apple's fall prompted his thinking about gravitation.
```

Even if the first sentence is intended as a shorthand retelling, its epistemic and attribution structure is stronger.

FoM semantic diff should detect:

```
source attribution LOST
certainty STRENGTHENED
event causality possibly STRENGTHENED
trajectory compressed
```

## 7. Source disagreement

If two sources disagree, FoM should not force one reality graph.

Instead:

```
scope source-A:
    ACCEPT P

scope source-B:
    ACCEPT NOT P

historian-model:
    uncertainty / weighted evidence / unresolved conflict
```

The historian's synthesis is a separate scope.

## 8. Narrator stance

A modern narrator may say:

```
"According to Stukeley..."
"Newton later recalled..."
"Legend has it..."
"It is often said..."
```

These signals encode different commitments.

The realization must preserve those distinctions when they are required.

## 9. Result

Historical evidence requires no new Core primitive.

The needed structure is already available through:

```
SOURCE as NODE
report/assert relations
SCOPE
INFERENTIAL evidence relations
epistemic qualifiers
trajectory/provenance
CONSTRAINTS against unjustified strengthening
```

The central rule is:

> A report of P is not P, and evidence for P is not ACCEPT(P) unless the target scope explicitly performs that epistemic update.
