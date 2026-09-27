# Mention vs use

Status: research note

FoM must distinguish talking about an entity from talking about the signal used to refer to that entity.

## 1. Example

```
"Москва состоит из шести букв."
```

This sentence is naturally understood as talking about the word/name "Москва", not the city.

The city does not consist of letters.

The signal token and its referent are different semantic objects.

## 2. Use

Ordinary use:

```
"Москва большая."
```

Signal fragment:

```
"Москва"
```

SEMIOTICALLY refers to:

```
city Moscow
```

The predicate applies to the city.

## 3. Mention

Mention:

```
"Слово «Москва» состоит из шести букв."
```

The semantic target is the linguistic expression itself.

The predicate applies to the SIGNAL object or an abstract lexical/type object representing the name.

## 4. Mixed cases

Natural language often omits explicit quotation markers:

```
"Москва состоит из шести букв."
```

Interpretation uses a metalinguistic frame to redirect the argument from referent to signal/name.

Thus reference resolution needs access to type constraints:

```
has-six-letters(city) -> type conflict
has-six-letters(name-signal) -> coherent
```

But FoM extraction must not "repair" every type conflict automatically. The metalinguistic reading must be licensed by the signal/context.

## 5. Quotation

Quotation can make the signal object explicit.

FoM should eventually distinguish:

- token;
- type / lexical form;
- quoted occurrence;
- referent;
- meaning/concept.

No new semantic Core primitive appears necessary: SIGNAL is a typed NODE, and SEMIOTIC relations connect signal and referent.

## 6. Conclusion

Mention/use reinforces:

```
signal != referent != concept
```

and shows that SIGNAL nodes are not merely realization metadata. Sometimes the signal itself is the semantic object under discussion.
