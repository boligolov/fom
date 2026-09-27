# FoM Text Syntax

Status: exploratory

FoM Text is intended to be a human- and LLM-friendly surface language for FoM.

It is **not** the canonical storage format.

The current direction is an EDN / S-expression-like DSL where:

- parentheses express semantic composition;
- maps hold metadata and named roles;
- vectors hold ordered collections or bindings;
- symbols identify semantic objects;
- keywords represent enumerated metadata;
- strings preserve literal surface form.

## 1. Why not YAML

YAML is readable for simple records but becomes awkward for deeply nested operator structure, binding, scope, and graph references.

For example:

```clojure
(not
  (almost
    (late ivan)))
```

directly exposes operator topology.

An equivalent object-heavy representation obscures that structure.

FoM Text should therefore optimize for semantic composition rather than configuration syntax.

## 2. Basic forms

Current core surface forms:

```clojure
(node id {...})

(rel [id] predicate {...})

(subgraph id
  ...)

(scope id {...}
  ...)

(delta id {...}
  ...)

(constraint id
  ...)
```

The exact grammar is not frozen.

## 3. Anonymous expressions

Short semantic relations may be written directly:

```clojure
(loves anna bob)
(dangerous honey)
(open pooh jar)
```

These are anonymous semantic expressions.

A relation receives an explicit ID only when it must be addressed separately:

```clojure
(rel r17 loves
  {:experiencer anna
   :target bob})
```

## 4. Positional vs named arguments

Simple predicates may use positional arguments:

```clojure
(loves anna bob)
```

Frame-like predicates should use named roles:

```clojure
(transfer
  {:source anna
   :theme book
   :recipient bob})
```

The Concept Ontology determines the semantic role schema.

## 5. Metadata

Maps carry metadata:

```clojure
(node anna
  {:type :person})

(scope anna-belief
  {:owner anna
   :mode :belief}
  ...)
```

Metadata should not be used to hide operator structure.

For example, prefer:

```clojure
(not
  (almost
    (late ivan)))
```

over flat flags such as:

```
negation=true
almost=true
```

because attachment order is semantically meaningful.

## 6. Scope status

Convenience forms may include:

```clojure
(accept anna-belief
  (waiting-for mark anna)
  {:certainty :plausible})

(reject reality
  (waiting-for mark anna))
```

These should compile to canonical scope-status relations.

## 7. Standard macros

FoM Text may provide standard macros such as:

```
unknown
fixed-unknown
ambiguity
inference
expectation
mapping
disclosure
preserve
reinterpret
almost
again
quantification
modality
```

These are not additional semantic primitives.

Every macro should have a defined expansion into Core forms.

## 8. Example

```clojure
(fom example

  (node anna {:type :person})
  (node mark {:type :person})

  (scope anna-belief
    {:owner anna}

    (accept
      (waiting-for mark anna)
      {:certainty :plausible}))

  (delta correction
    {:intended-by mark}

    (update
      (waiting-for mark anna)
      {:status :accepted}
      {:status :rejected}))

  (constraint reveal-later
    (disclosure
      (reason-for correction)
      {:before cp7 :prohibited
       :after cp7 :required})))
```

## 9. Binding

The surface language must support explicit parameterized patterns.

Example:

```clojure
(pattern student-read [x]
  :where
  (student x)

  :require
  (read x book))
```

A future syntax should cover:

- variable declarations;
- binding environments;
- binding accessibility;
- quantification over bindings;
- bindings crossing licensed scope boundaries.

## 10. Surface language vs canonical form

The intended architecture is:

```
FoM Text
   ↓ parse / macro expansion
Canonical FoM Graph
   ↓
validation / realization / diff / storage
```

FoM Text should be ergonomic.

Canonical FoM should be strict and explicit.

The two formats should not be forced to serve the same purpose.
