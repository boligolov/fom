# Audience model and world-knowledge licensing

Status: research note

Recoverability is not a property of a signal alone.

A more accurate model is:

```
recoverability(fragment, audience, context, trajectory_position)
```

FoM therefore needs an explicit but sparse way to represent the assumptions under which a meaning is expected to be recoverable.

## 1. Do not model a whole person

An audience model should not become a full simulation of the receiver.

It should contain only assumptions relevant to the current message.

Examples:

- language competence;
- knowledge of a local code;
- awareness of a prior event;
- knowledge of a cultural reference;
- domain expertise;
- knowledge that the speaker is a cannibal;
- access to previous discourse.

This follows the same sparsity principle as FoM itself.

## 2. Distinguish four things

### Actual receiver state

What a concrete receiver actually knows/believes.

### Sender model of receiver

What the sender believes the receiver knows.

### Target audience profile

The competence/context assumptions under which a realization is intended to work.

### Shared/common state

Information treated as mutually available in the interaction.

These may disagree.

A joke can fail because the target-audience assumptions were wrong.

## 3. Audience profile as a standard pattern

No new Core primitive is needed.

An audience profile can be represented as an addressable subgraph/node plus constraints.

Conceptually:

```
AUDIENCE PROFILE {
    language competencies
    shared assumptions
    available codebooks
    prior discourse
    expertise
    cultural/context dependencies
}
```

The profile does not assert these facts in reality. It defines assumptions for interpretation/realization validation.

## 4. Knowledge dependencies

A recoverable meaning may explicitly depend on background assumptions.

Example: the cannibal joke.

To recover the second reading, an interpreter may need access to:

```
speaker is a cannibal
cannibals may eat humans
Russian construction "на обед будет X" can place X in a food/menu role
Russian construction "на обед будут гости" conventionally supports a hospitality frame
```

These assumptions should be representable as dependencies of an inference route.

This is stronger than merely attaching an audience label.

## 5. Required vs licensed dependencies

Useful distinction:

```
REQUIRED_CONTEXT
LICENSED_BACKGROUND
REALIZATION_DEFAULT
FORBIDDEN_RESOLUTION
```

### REQUIRED_CONTEXT

Without this assumption, required meaning/effect is not expected to be recoverable.

### LICENSED_BACKGROUND

The realizer/interpreter may use it, but the meaning does not depend on it.

### REALIZATION_DEFAULT

May fill in harmless detail needed for a natural signal.

It must remain semantically non-required.

### FORBIDDEN_RESOLUTION

Knowledge that may be true in the world but must not be used to resolve a fixed unknown or disclosure-protected fact.

## 6. World knowledge during realization

A realizer may consult background knowledge if its use is licensed.

It must not convert background knowledge into required recoverable message content unless FoM licenses that transformation.

Example:

If FoM says:

```
bird on branch
```

a realizer may say "a small bird" only if size is FREE/LICENSED and the choice does not change relevant inference.

It may not choose "a raven" if raven symbolism would create a new required or strongly salient interpretation.

## 7. Knowledge is not ontology entailment

Concept Ontology and world knowledge remain distinct.

For a concept:

```
cannibal(person)
```

a semantic contract may entail a human-eating practice/disposition strongly enough to support interpretation.

But cultural stereotypes, typical behaviors, and narrative associations remain world knowledge.

The boundary must be tested concept by concept.

## 8. Audience-relative recoverability

The same signal can have different recoverability obligations for different audiences.

Example: Aesopian code.

```
ingroup:
    coded target = REQUIRED

outsider:
    coded target = OPTIONAL or NONE
```

Example: technical documentation.

```
expert:
    compressed inference route acceptable

novice:
    same target may require explicit intermediate structure
```

Thus a realization may be valid for one audience and invalid for another without changing the intended semantic target.

## 9. Multi-meaning and audience

For deliberate multi-meaning, the audience profile may constrain not only recovery of A and B, but their relationship.

For the cannibal joke:

```
reading A = hospitality
reading B = guests-as-food

required:
    recover A
    recover B
    recognize same signal supports both
    recognize role collision
```

If an audience can recover only B, the statement may remain informative but the joke is lost.

## 10. Signal structure dependency

Some meanings depend on a particular ambiguity or affordance of the signal form.

In:

```
"Сегодня у нас на обед будут гости"
```

the same surface region participates in two constructions:

```
hospitality frame:
    guests = visitors attending lunch

menu frame:
    guests = what will be for lunch
```

Therefore preservation of the two proposition graphs is not enough.

FoM may need a required SEMIOTIC constraint that both readings map to the same signal locus or to functionally equivalent loci in the target realization.

This is a PRESERVE_FUNCTION requirement, not necessarily PRESERVE_FORM.

A translation may use entirely different words if the target signal recreates the co-activation.

## 11. Realization validation

Given:

```
FoM
target audience profile
candidate signal
```

validation should ask:

1. Are all REQUIRED meanings recoverable?
2. Are protected unknowns still unresolved?
3. Are required inference routes available under the audience assumptions?
4. Are required multi-meaning relations recoverable?
5. Did licensed background knowledge introduce unintended salient content?
6. Did the realization depend on assumptions not granted by the audience profile?

## 12. Current conclusion

No AUDIENCE Core primitive is required.

Audience modeling can remain a sparse standard layer built from:

```
NODE / SUBGRAPH
SCOPE
SEMIOTIC and INFERENTIAL relations
CONSTRAINTS
context-dependency links
```

The key architectural addition is explicit **knowledge dependency**:

> FoM should be able to state not only what must be recoverable, but under which shared assumptions/inference resources it is expected to be recoverable.
