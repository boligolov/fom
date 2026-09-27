# Social acts and felicity conditions

Status: research note

Speech/social acts are a direct test of DELTA.

The same sentence can:

- merely describe a social act;
- attempt to perform one;
- successfully perform one;
- fail because required authority/context/procedure is missing.

The key distinction is:

```
intended / attempted social delta
!=
actual social delta
```

## 1. Promise

Signal:

```
"Я обещаю вернуть деньги завтра."
```

A successful promise normally creates a commitment/obligation relation involving the speaker and future action.

A useful pattern:

```
signal expresses proposition P
speaker intends promise-act
felicity constraints satisfied
therefore actual DELTA:
    add commitment(speaker, P, addressee/context)
```

The commitment is social-state content, not merely a belief about the speaker.

## 2. Failed promise-like utterance

A child actor in a play says:

```
"Я обещаю вернуть деньги."
```

Inside the fictional/performance context, the line may represent a promise by the character.

In real-world social scope, the actor may incur no corresponding obligation.

This requires scope separation.

## 3. Declaration

```
"Объявляю вас мужем и женой."
```

Said by an authorized officiant under a valid procedure may create a legal/social status.

Said by a random stranger normally does not.

Same propositional/signal content, different felicity conditions.

Therefore FoM must represent:

```
attempted declaration
authority/context/procedure constraints
actual social effect
```

## 4. Command

```
"Закрой дверь."
```

A command/request may aim to create:

- an obligation;
- a social pressure;
- an action goal;
- an expectation of compliance.

Which effect is licensed depends on relation/authority/context.

A boss's command and a stranger's demand may have different normative force even with identical surface wording.

## 5. Permission

```
"Можете идти."
```

Depending on context, this may:

- report ability;
- grant permission;
- dismiss someone;
- make a conversational move.

The social-act reading requires authority over the relevant permission domain.

## 6. Felicity conditions

Common condition types include:

```
authority
role
procedure
context
jurisdiction
uptake
speaker commitment
capacity/control
non-contradictory prior obligations
```

FoM should not hard-code one universal list.

Concept/social-act contracts specify relevant constraints.

## 7. Constraint-gated DELTA

A useful general schema is:

```
ATTEMPTED_DELTA d1

CONSTRAINTS C

if C satisfied:
    ACTUAL_DELTA d2 corresponds-to d1
else:
    d1 remains attempted/invalid/ineffective
```

This does not require a special "speech act engine" in the Core.

## 8. Uptake

Some acts require the addressee/institution to recognize or register the act.

Example:

- a private intention is not a promise;
- an unheard warning may fail to update the receiver;
- a declaration may require institutional recording.

Uptake can therefore be a felicity condition or a separate actual-effect DELTA.

## 9. Social state is scoped

Social facts can differ across systems:

```
legal scope
organizational scope
personal relationship scope
game/fiction scope
```

An act may be valid in one and invalid in another.

## 10. Current conclusion

No new Core primitive is required.

Social acts are naturally represented as:

```
SIGNAL
+
intended/attempted DELTA
+
CONSTRAINTS (felicity conditions)
+
actual DELTA
+
scope/jurisdiction
```

The important invariant is:

> FoM must never equate intended operation with successful social-state change.
