from __future__ import annotations

import tomllib
from dataclasses import dataclass
from importlib.resources import files
from typing import Any

from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from .parser import parse


@dataclass(frozen=True)
class RelationView:
    rel_id: str
    predicate: str
    args: dict[str, Any]


@dataclass(frozen=True)
class RefinementMatch:
    source_relation_id: str
    source_predicate: str
    candidate_relation_ids: tuple[str, ...]
    contract_name: str


def _symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def _head(expr: Expr) -> str | None:
    if isinstance(expr, ListExpr) and expr.items:
        return _symbol(expr.items[0])
    return None


def _value(expr: Expr) -> Any:
    if isinstance(expr, Atom):
        return (expr.kind, expr.value)
    if isinstance(expr, VectorExpr):
        return ("vector", tuple(_value(item) for item in expr.items))
    if isinstance(expr, MapExpr):
        return (
            "map",
            tuple(
                sorted(
                    (str(key.value), _value(value))
                    for key, value in expr.items
                )
            ),
        )
    return (
        "list",
        tuple(_value(item) for item in expr.items),
    )


def _map(expr: MapExpr) -> dict[str, Expr]:
    return {str(key.value): value for key, value in expr.items}


def collect_relations(text: str) -> dict[str, RelationView]:
    root = parse(text)
    out: dict[str, RelationView] = {}

    def walk(expr: Expr) -> None:
        if isinstance(expr, Atom):
            return
        if isinstance(expr, VectorExpr):
            for item in expr.items:
                walk(item)
            return
        if isinstance(expr, MapExpr):
            for _, value in expr.items:
                walk(value)
            return
        if not expr.items:
            return

        if _head(expr) == "rel" and len(expr.items) == 4:
            rel_id = _symbol(expr.items[1])
            predicate = _symbol(expr.items[2])
            args_expr = expr.items[3]

            if (
                rel_id
                and predicate
                and isinstance(args_expr, MapExpr)
            ):
                out[rel_id] = RelationView(
                    rel_id=rel_id,
                    predicate=predicate,
                    args={
                        role: _value(value)
                        for role, value in _map(args_expr).items()
                    },
                )

        for child in expr.items[1:]:
            walk(child)

    walk(root)
    return out


def load_contracts() -> list[dict[str, Any]]:
    path = files("fom").joinpath("data/concept_contracts.toml")
    return tomllib.loads(
        path.read_text(encoding="utf-8")
    )["concepts"]


def _required_candidate_args(
    source: RelationView,
    pattern_args: dict[str, str],
) -> dict[str, Any] | None:
    out: dict[str, Any] = {}

    for candidate_role, source_binding in pattern_args.items():
        if not source_binding.startswith("$"):
            return None

        source_role = source_binding[1:]
        if source_role not in source.args:
            return None

        out[candidate_role] = source.args[source_role]

    return out


def _find_relation(
    candidates: dict[str, RelationView],
    used: set[str],
    predicate: str,
    required_args: dict[str, Any],
) -> str | None:
    matches: list[str] = []

    for rel_id, relation in candidates.items():
        if rel_id in used or relation.predicate != predicate:
            continue

        if all(
            relation.args.get(role) == value
            for role, value in required_args.items()
        ):
            matches.append(rel_id)

    if len(matches) == 1:
        return matches[0]

    return None


def find_refinement_matches(
    source_text: str,
    candidate_text: str,
) -> list[RefinementMatch]:
    source_relations = collect_relations(source_text)
    candidate_relations = collect_relations(candidate_text)
    contracts = load_contracts()

    matches: list[RefinementMatch] = []

    for source in source_relations.values():
        matching_contracts = [
            contract
            for contract in contracts
            if contract["predicate"] == source.predicate
        ]

        for contract in matching_contracts:
            used: set[str] = set()
            complete = True

            for refinement in contract.get("refinement", []):
                required_args = _required_candidate_args(
                    source,
                    refinement.get("args", {}),
                )
                if required_args is None:
                    complete = False
                    break

                rel_id = _find_relation(
                    candidate_relations,
                    used,
                    refinement["predicate"],
                    required_args,
                )

                if rel_id is None:
                    complete = False
                    break

                used.add(rel_id)

            if complete:
                matches.append(
                    RefinementMatch(
                        source_relation_id=source.rel_id,
                        source_predicate=source.predicate,
                        candidate_relation_ids=tuple(sorted(used)),
                        contract_name=contract["predicate"],
                    )
                )
                break

    return matches
