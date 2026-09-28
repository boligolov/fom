# Executable constraint evaluation

Status: first bounded profile, not a complete semantic validator.

The existing UNKNOWN contract requires a scope to remain uncommitted about
content. The scope resolver now makes that requirement executable. This adds
no semantic primitive: `status-is` is the explicit operator spelling for a
constraint over the existing scope-status model.

## Usage

```sh
python -m fom evaluate tests/fixtures/evaluation/source.fom
python -m fom evaluate tests/fixtures/evaluation/source.fom tests/fixtures/evaluation/corrupted.fom
```

With one file the command checks that document's represented state against
its own constraints. With two files it takes constraints exclusively from
the source and evaluates them against the candidate state. Deleting source
constraints from the candidate cannot bypass the contract. Candidate-added
constraints are not evaluated as part of the source contract.

Python API: `evaluate_constraints(contract_graph, candidate_graph=None)`.
Arguments are canonical graphs; neither is modified.

## Supported forms

```clojure
(constraint required-acceptance
  {:strength :required}
  (status-is proposition {:scope reader :value :accept}))

(constraint required-unknown
  (unknown proposition {:scope reader}))
```

The target must be an explicitly named relation or subgraph. Scope and target
IDs form an explicit shared interface between these two documents. The scope
parameter is mandatory even when a constraint is lexically nested in a scope.
No scope is inferred from nesting, audience, imports, or ownership.

`status-is` accepts `accept`, `reject`, or `uncommitted` as its expected value.
`unknown` is the state-level requirement `status-is ... :uncommitted`.
It is not yet a bare macro expansion and does not enforce unknownness across
future states, audiences, or realizations. It must not be substituted for
`fixed-unknown`.

Resolution uses the existing none/overlay profile. Explicit local shadows,
inherited statuses, and conflicts are preserved. An absent status satisfies
unknownness only when the target and scope both exist and no status is
inherited. A conflict never satisfies unknownness. Missing target or scope
in the candidate violates the requirement; it does not make it vacuously true.

Strength defaults to `required`. `optional` requirements are still evaluated
and reported, but their violations do not fail required satisfaction. Only
these two strengths are supported. Put strength in the declaration metadata,
not inside the operator's parameter map.

## Results and exit codes

Each result names its source constraint and reports `SATISFIED`, `VIOLATED`,
`UNSUPPORTED`, or `ERROR`. Evaluated requirements include resolved status and
originating status evidence. Unknown operators, extra parameters or metadata,
and anonymous targets are not silently ignored.

Overall results, in precedence order:

| Result | Meaning | CLI exit |
| --- | --- | --- |
| ERROR | A contract or required evaluation cannot be interpreted safely, including invalid inheritance | 2 |
| FAIL | At least one required requirement is demonstrably violated | 1 |
| INDETERMINATE | No known required violation, but a required requirement is unsupported | 2 |
| NOT_APPLICABLE | No required constraints, including an empty contract | 2 |
| PASS | Every required requirement was evaluated and satisfied | 0 |

Malformed optional requirements also produce ERROR. Unsupported optional
requirements are reported without blocking otherwise satisfied required
requirements. `complete` means all listed constraints were evaluated to a
determinate satisfaction/violation result, including optional constraints.
Thus a known required violation plus unsupported requirements is FAIL with
`complete: false`. PASS certifies the declared required profile only.

## Deliberate limits

This evaluator checks statuses of addressed content. Reusing a target ID
while changing its meaning is outside this profile: PASS is not a content
preservation or translation-equivalence judgment. Independently decomposed
graphs, renamed scopes/targets, and generated IDs require a separate alignment
contract. Anonymous targets return UNSUPPORTED, even in single-file mode, to
keep one consistent supported profile.

No generic inference, confidence comparison, temporal reasoning, disclosure,
recoverability, constraint propagation, or FIXED_UNKNOWN realization check is
implemented here. These operators remain visible as UNSUPPORTED rather than
being treated as satisfied. The static `check` command remains a structural
check; passing it does not imply that `evaluate` can execute every constraint.

The executable fixture tests a base that accepts two propositions and a child
that masks one. Removing the mask makes the inherited acceptance violate the
source UNKNOWN requirement while the other status requirement stays satisfied.
Additional tests cover the status matrix, conflicts, optional strength,
missing references, unsupported operators, cycles, immutability, and CLI exits.
