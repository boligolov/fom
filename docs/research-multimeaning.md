# Deliberate multi-meaning and co-activated readings

Status: research note

Natural-language signals can intentionally support more than one meaning at the same time.

This is distinct from ordinary unresolved ambiguity.

## 1. Four different phenomena

### 1.1 Unresolved ambiguity

The interpreter cannot determine which reading was intended.

```
candidate meanings = {A, B}
intended meaning = one of {A, B}, unresolved
```

Example:

"Иван сказал Петру, что он ошибается."

The pronoun may refer to Ivan or Petr.

FoM should preserve the candidate set without selecting one.

### 1.2 Underspecification

The sender does not commit to a semantic distinction.

Several refinements may be compatible, but the communicative effect does not require the receiver to actively hold several competing readings.

### 1.3 Coded / Aesopian replacement

A surface reading L remains available, but an in-group convention maps the signal to intended target T.

Typical pattern:

```
outsider -> L
insider  -> T
```

The literal reading may function as cover, camouflage, euphemism, or decoy.

The target meaning may replace the literal reading for the intended audience.

### 1.4 Deliberate co-activation

The sender intends multiple readings to be available and relevant simultaneously.

```
intended meanings = {A, B}
co-activation = required
```

Examples include:

- puns;
- double meanings;
- some double entendre;
- frame collisions;
- jokes whose effect requires reinterpretation without deleting the first reading.

This is not equivalent to:

```
intended meaning = unknown(A or B)
```

## 2. Example: cannibal lunch

Signal:

```
"Сегодня у нас на обед будут гости"
```

said by a cannibal to his wife.

The signal supports at least two readings.

### Reading A — hospitality

```
guests visit household
guests participate in lunch
guests are co-eaters / social participants
```

### Reading B — cannibal meal

```
guests are the food consumed at lunch
cannibal household eats guests
```

The humor depends on the lexical/syntactic material supporting both frames.

The second reading does not simply replace the first. The first is needed as the normal frame against which the second produces the effect.

## 3. Frame-role conflict

The same referent occupies different roles in the two readings.

Hospitality frame:

```
guest -> visitor / participant
```

Cannibal-meal frame:

```
guest -> food / patient of eating
```

This is useful evidence that multi-meaning should not be represented merely as two propositions in a bag.

The relation among readings matters.

## 4. Co-activation constraint

A tentative representation is:

```
READING_SET rs1 = {reading-A, reading-B}

CONSTRAINT:
    both readings recoverable

CONSTRAINT:
    reading-A remains available after reading-B is recognized

CONSTRAINT:
    contrast/frame-collision between A and B is recoverable

CONSTRAINT:
    no early paraphrase may collapse the signal into only one reading
```

Thus semantic preservation requires not just preserving A and B individually, but preserving their simultaneous relationship.

## 5. Reading relations

Useful relations among readings may include:

```
COACTIVATED_WITH
CONTRASTS_WITH
REINTERPRETS
DEPENDS_ON
DOMINATES_AFTER
MASKS
LICENSES
```

These need not become new Core relation families.

They can remain open/meta-semantic relations plus CONSTRAINTS.

## 6. Trajectory

Many puns are trajectory-sensitive:

```
checkpoint 1:
    reading A is dominant

checkpoint 2:
    trigger appears

checkpoint 3:
    reading B becomes salient

checkpoint 4:
    A remains active and contrasts with B
```

The effect is lost if B is disclosed from the beginning.

Therefore deliberate multi-meaning interacts with disclosure and salience.

## 7. Same signal, multiple mappings

A single signal may have multiple SEMIOTIC relations:

```
signal -> reading A
signal -> reading B
```

with qualifiers such as:

```
recoverability
salience
audience
trajectory position
intendedness
```

This is preferable to creating a special MULTIMEANING primitive.

## 8. Intendedness

FoM needs to distinguish:

```
reading merely possible
reading accidentally evoked
reading intentionally licensed
reading intentionally required
```

A useful qualifier is therefore not just "candidate", but something like:

```
:intendedness :possible
:intendedness :licensed
:intendedness :required
```

This may belong to SEMIOTIC mapping or to a preservation constraint.

## 9. Polysemy vs homonymy

For FoM, the historical linguistic distinction between polysemy and homonymy is often less important than the semantic graph result.

What matters operationally is:

- how many reading graphs are activated;
- whether they share lexical material;
- whether they share conceptual structure;
- whether both are intended;
- whether one masks another;
- whether the relation among them is part of the effect.

## 10. Current conclusion

No new Core primitive is required.

Deliberate multi-meaning can be represented as:

```
one SIGNAL
+
multiple SEMIOTIC mappings
+
multiple reading SUBGRAPHs
+
salience/trajectory structure
+
CONSTRAINTS requiring co-recoverability and contrast
```

The important architectural distinction is:

```
AMBIGUITY:
    preserve unresolved choice

MULTI-MEANING:
    preserve multiple intended readings and their relationship
```
