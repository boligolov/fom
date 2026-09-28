# FoM Text Syntax

Status: work in progress

FoM Text is the human- and LLM-oriented surface syntax for Format of Meaning.

It is intentionally separate from the canonical graph representation.

The design goal is:

```
easy to read/write
+ explicit operator structure
+ graph references
+ lexical binding
+ deterministic parsing
+ deterministic desugaring
```

FoM Text is EDN/S-expression inspired, but it is not EDN and does not inherit EDN semantics unless explicitly stated here.

## 1. Processing pipeline

```
FoM Text
  -> parse
Surface AST
  -> resolve IDs and lexical bindings
Resolved AST
  -> expand standard macros
Core AST
  -> normalize predicates / roles / scopes
Canonical FoM Graph
```

A parser MUST NOT use world knowledge to change the graph during parsing.

Concept Ontology may be consulted only where this specification explicitly permits it, such as resolving positional argument roles during normalization.

## 2. Lexical elements

### 2.1 Whitespace

Whitespace separates tokens and is otherwise insignificant.

### 2.2 Comments

A semicolon starts a line comment.

```clojure
; comment
(node anna {:type :person})
```

### 2.3 Symbols

Symbols identify graph objects, predicates, forms, and document IDs.

Examples:

```
anna
platform
waiting-for
story-001
```

IDs are document-global unless a future module system explicitly changes this rule.

Forward references are allowed.

### 2.4 Variables

Variables begin with `?`.

```
?x
?student
?scope
```

Variables are lexical and MUST be introduced by a binding form before use.

Variables and graph IDs occupy different namespaces.

### 2.5 Keywords

Keywords begin with `:`.

```
:person
:belief
:required
:high
```

Keywords are literal values. They are never resolved as graph references.

### 2.6 Strings

Strings use double quotes.

```clojure
"он"
"do not open before evening"
```

Strings preserve surface form and are never treated as graph IDs.

### 2.7 Numbers and booleans

Implementations SHOULD support integers, decimal numbers, `true`, and `false`.

Numbers do not imply false semantic precision. A realization/extractor MUST NOT invent numeric values merely because the syntax supports them.

## 3. Collections

### 3.1 Vector

```clojure
[anna mark]
[?x ?y]
```

Vectors preserve order.

### 3.2 Map

```clojure
{:owner anna
 :mode :belief}
```

Maps contain keyword/value pairs.

Duplicate keys are invalid.

Map ordering is not semantically significant.

## 4. Grammar

The grammar below is descriptive EBNF. Semantic validation is defined separately.

```ebnf
document       = "(" "fom" symbol map? form* ")" ;

form           = node-form
               | relation-form
               | subgraph-form
               | scope-form
               | delta-form
               | constraint-form
               | pattern-form
               | status-form
               | operation-form
               | macro-form
               | expression ;

node-form      = "(" "node" symbol map? ")" ;

relation-form  = "(" "rel" symbol symbol relation-args ")" ;
relation-args  = vector | map ;

subgraph-form  = "(" "subgraph" symbol form* ")" ;

scope-form     = "(" "scope" symbol map? form* ")" ;

delta-form     = "(" "delta" symbol map? operation-form* ")" ;

constraint-form
               = "(" "constraint" symbol map? expression ")" ;

pattern-form   = "(" "pattern" symbol vector pattern-clause* ")" ;
pattern-clause = "(" "where" expression* ")"
               | "(" "require" expression* ")"
               | "(" "bind" binding-spec* ")" ;

binding-spec   = "(" variable expression ")" ;

status-form    = accept-form | reject-form ;
accept-form    = "(" "accept" scope-ref? expression map? ")" ;
reject-form    = "(" "reject" scope-ref? expression map? ")" ;

operation-form = add-form
               | remove-form
               | update-form
               | connect-form
               | disconnect-form
               | identify-form
               | activate-form
               | deactivate-form ;

add-form       = "(" "add" expression ")" ;
remove-form    = "(" "remove" reference ")" ;
update-form    = "(" "update" reference map ")" ;
connect-form   = "(" "connect" expression ")" ;
disconnect-form
               = "(" "disconnect" reference ")" ;
identify-form  = "(" "identify" reference reference ")" ;
activate-form  = "(" "activate" reference ")" ;
deactivate-form
               = "(" "deactivate" reference ")" ;

expression     = atom
               | vector
               | map
               | application ;

application    = "(" symbol application-args* ")" ;

application-args
               = expression ;

reference      = symbol | variable ;
scope-ref      = symbol | variable ;

atom           = symbol
               | variable
               | keyword
               | string
               | number
               | boolean ;
```

The grammar intentionally permits more applications than are semantically valid. Semantic validation determines whether a head symbol denotes an open predicate, a standard macro, or an invalid form.

## 5. Document form

Every file contains exactly one top-level `fom` form.

```clojure
(fom example
  {:kind :test
   :language :none}

  ...)
```

The optional header map is document metadata.

Document metadata does not automatically become represented meaning.

## 6. NODE

```clojure
(node anna
  {:type :person})
```

A node declaration introduces one addressable semantic object.

Node properties may include standardized structural fields such as `:type`.

Open-world semantic claims SHOULD normally be relations rather than arbitrary node properties.

For example, prefer:

```clojure
(rel r1 located-at
  {:entity anna
   :place platform})
```

over hiding the relation inside a node map.

## 7. RELATION

An addressable relation is explicit:

```clojure
(rel r17 loves
  [anna bob])
```

or role-based:

```clojure
(rel r18 transfer
  {:source anna
   :theme book
   :recipient bob})
```

The relation ID is mandatory in `rel`.

If no addressable relation is needed, use an anonymous expression:

```clojure
(loves anna bob)
```

### 7.1 Positional arguments

```clojure
(loves anna bob)
```

Positional arguments are allowed only when the predicate's argument ordering is known from a Concept Contract, standard library definition, or local schema.

### 7.2 Named roles

```clojure
(transfer
  {:source anna
   :theme book
   :recipient bob})
```

An application using named roles MUST contain exactly one role map as its argument.

A single application MUST NOT mix positional and named arguments.

## 8. Anonymous semantic expressions

Any application whose head is not a reserved core form is interpreted as either:

1. an open semantic predicate;
2. a registered standard macro;
3. an error if neither interpretation is available.

Examples:

```clojure
(dangerous honey)

(not
  (dangerous honey))

(almost
  (late ivan))
```

Anonymous expressions are not directly addressable.

If another graph element must refer to the expression as an object, it SHOULD be reified as a relation or wrapped in an addressable subgraph.

## 9. SUBGRAPH

```clojure
(subgraph mistaken-interpretation
  (rel r1 waiting-for
    {:actor mark
     :target anna}))
```

A subgraph is an addressable selection/grouping of graph material.

Nesting a declaration inside a subgraph establishes membership, not truth status.

## 10. SCOPE

```clojure
(scope anna-belief
  {:owner anna
   :mode :belief}

  (accept
    (waiting-for mark anna)
    {:certainty :plausible}))
```

A scope creates a perspective/model context.

### 10.1 Current scope

Inside a `scope` form, `accept` and `reject` may omit the explicit scope argument.

```clojure
(scope s
  (accept (home ivan)))
```

is surface shorthand for:

```clojure
(accept s (home ivan))
```

### 10.2 No implicit truth

A semantic expression nested in a scope is NOT automatically accepted merely because it is textually nested there.

Truth/status must be established explicitly through `accept`, `reject`, or a defined macro expansion.

### 10.3 Scope visibility and inheritance

Reference visibility and semantic-status inheritance are separate mechanisms.

A nested scope may refer to outer graph IDs without inheriting the outer scope's ACCEPT/REJECT statuses.

The following properties are reserved for scope linkage:

```
:parent
:imports
:inherits-status-from
:inherit-mode
:center
```

`:imports` controls reference/model accessibility.

`:inherits-status-from` controls semantic-status inheritance.

Explicit status shadows use `(uncommit content)` inside a scope or
`(uncommit scope content)` outside it. `uncommitted` is an equivalent spelling.
Both accept an optional qualifier map and canonicalize to a status record
whose value is `uncommitted`. A shadow is different from an absent status:
it masks inherited ACCEPT/REJECT without rejecting the content.

No status inheritance occurs merely because `:parent` is present.

## 11. ACCEPT and REJECT

Examples:

```clojure
(accept reality
  (home ivan))

(reject anna-belief
  (home ivan)
  {:certainty :high})
```

ACCEPT and REJECT are scope-relative statuses.

Absence of ACCEPT is not REJECT.

An implementation MUST preserve this three-way distinction:

```
ACCEPT
REJECT
UNCOMMITTED / UNSPECIFIED
```

`unknown` may constrain the third state but is not equivalent to a simple missing edge.

## 12. DELTA

```clojure
(delta correction
  {:intended-by mark
   :target-scope anna-belief}

  (update belief-r17
    {:certainty {:from :high
                 :to :low}})

  (add
    (accept anna-belief
      (waiting-for mark sister))))
```

A delta contains graph operations.

The Core operation vocabulary is:

```
ADD
REMOVE
UPDATE
CONNECT
DISCONNECT
IDENTIFY
ACTIVATE
DEACTIVATE
```

### 12.1 UPDATE

UPDATE takes a reference and a field-diff map.

```clojure
(update r17
  {:certainty {:from :possible
               :to :high}
   :salience {:from :normal
              :to :high}})
```

A field may omit `:from` when the source value is intentionally unconstrained.

### 12.2 IDENTIFY

```clojure
(identify ref-slot-1 petr)
```

IDENTIFY records a delta that resolves two graph referents as identical in the relevant semantic context.

It MUST NOT be implemented as unconditional global node merging; identity may be scope-relative.

## 13. CONSTRAINT

```clojure
(constraint sister-fate
  {:strength :required}

  (fixed-unknown
    (fate sister)))
```

A constraint is addressable and contains exactly one constraint expression.

Constraint semantics come from the standard library or an explicitly imported extension.

## 14. PATTERN and binding

Variables are introduced explicitly.

```clojure
(pattern student-read [?x]
  (where
    (student ?x))

  (require
    (read ?x book)))
```

Dependent binding:

```clojure
(pattern loves-own-mother [?x ?y]
  (where
    (person ?x))

  (bind
    (?y (the ?m
          (mother-of ?m ?x))))

  (require
    (loves ?x ?y)))
```

A pattern defines a lexical binding environment.

A variable remains visible only within the pattern clauses and nested scopes/forms whose accessibility rules permit it.

Binding accessibility is semantic structure and MUST survive normalization.

## 15. SELF / CENTER

A scope may define a distinguished center:

```clojure
(scope oleg-belief
  {:owner oleg
   :center oleg}

  (accept
    (winner (self))))
```

`(self)` is a standard macro that resolves to the current scope's distinguished center.

This preserves the difference between de se and merely de re reference.

## 16. Standard macros

Macros are surface-language conveniences, not new Core primitives.

Candidate standard macros include:

```
unknown
fixed-unknown
ambiguity
presuppose
inference
expectation
mapping
disclosure
preserve
reinterpret
almost
again
possible
necessary
generic
for-each
exists
self
```

Every standard macro MUST define:

1. accepted syntax;
2. semantic preconditions;
3. deterministic expansion to Core AST or Canonical FoM;
4. validation rules;
5. whether expansion requires a Concept Contract.

A macro MUST NOT rely on unspecified "common sense" to decide its canonical meaning.

## 17. Negation and operator attachment

Operator topology is semantic.

These forms are distinct:

```clojure
(again
  (not P))

(not
  (again P))
```

and:

```clojure
(not
  (for-each ...))

(for-each ...
  (require
    (not P)))
```

The AST MUST preserve nesting exactly until a semantics-preserving normalization rule explicitly transforms it.

## 18. Unknown and ambiguity

Unknown information is never encoded as `nil`.

Examples:

```clojure
(unknown
  (fate sister))

(fixed-unknown
  (fate sister))

(ambiguity
  {:candidates [ivan petr]
   :target ref-slot-1})
```

`nil` is therefore not currently part of FoM Text's semantic value language.

## 19. IDs and reference resolution

Graph IDs:

- are document-global;
- may be forward-referenced;
- must be unique;
- are not variables.

Variables:

- begin with `?`;
- are lexical;
- shadow neither graph IDs nor keywords because they occupy a separate namespace.

Unresolved graph IDs are validation errors.

Unresolved semantic references should be represented explicitly as nodes/reference slots, not as unresolved syntax identifiers.

## 20. Canonicalization rules

Canonicalization SHOULD perform at least the following steps:

1. expand lexical scope shorthands;
2. resolve all graph IDs;
3. resolve all lexical variables;
4. expand registered macros;
5. convert positional predicate applications to explicit argument roles where a contract provides those roles;
6. make scope/status relations explicit;
7. make binding accessibility explicit;
8. preserve addressable subgraphs;
9. preserve source-location metadata separately from semantic content;
10. reject ambiguous surface syntax rather than guessing.

Canonicalization MUST NOT:

- resolve semantic ambiguity without a semantic rule;
- invent omitted world knowledge;
- globalize scope-relative identity;
- strengthen certainty;
- resolve FIXED_UNKNOWN content.

## 21. Extensions

FoM Text is expected to evolve.

Extensions SHOULD use namespaced predicate or macro names when collision is possible.

An extension MUST NOT silently redefine Core forms.

## 22. Formatting conventions

Recommended style:

- two-space indentation;
- one major form per line/block;
- role maps vertically aligned for non-trivial relations;
- explicit IDs only where addressability is needed;
- comments explain modeling decisions, not restate syntax.

## 23. Surface vs canonical form

FoM Text is designed for authors, models, tests, and review.

Canonical FoM is designed for deterministic tooling.

```
FoM Text
  -> Canonical FoM Graph
  -> validation
  -> semantic diff
  -> realization
  -> extraction
```

The surface language may remain pleasant and concise precisely because canonicalization is strict.
