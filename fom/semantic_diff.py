from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from .parser import parse
from .validator import validate_text


INFERENCE_PREDICATES = {
    "evidence-for",
    "evidence-against",
    "supports",
    "infers",
}

CERTAINTY_ORDER = {
    "low": 0,
    "possible": 1,
    "plausible": 2,
    "medium": 3,
    "high": 4,
    "certain": 5,
}

SALIENCE_ORDER = {
    "low": 0,
    "normal": 1,
    "high": 2,
}


@dataclass(frozen=True)
class RelationRecord:
    predicate: str
    args: Any


@dataclass(frozen=True)
class StatusRecord:
    value: str
    qualifiers: tuple[tuple[str, Any], ...]


@dataclass
class Snapshot:
    relations: dict[str, RelationRecord]
    statuses: dict[tuple[str, Any], StatusRecord]
    disclosures: dict[Any, tuple[tuple[str, Any], ...]]
    fixed_unknown: set[Any]


def _symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def _head(expr: Expr) -> str | None:
    if isinstance(expr, ListExpr) and expr.items:
        return _symbol(expr.items[0])
    return None


def normalize(expr: Expr) -> Any:
    if isinstance(expr, Atom):
        return (expr.kind, expr.value)

    if isinstance(expr, VectorExpr):
        return ("vector", tuple(normalize(x) for x in expr.items))

    if isinstance(expr, MapExpr):
        return (
            "map",
            tuple(
                sorted(
                    (str(k.value), normalize(v))
                    for k, v in expr.items
                )
            ),
        )

    return ("list", tuple(normalize(x) for x in expr.items))


def _map_dict(expr: MapExpr) -> dict[str, Expr]:
    return {str(k.value): v for k, v in expr.items}


def _qualifier_tuple(expr: MapExpr | None) -> tuple[tuple[str, Any], ...]:
    if expr is None:
        return ()
    return tuple(
        sorted((str(k.value), normalize(v)) for k, v in expr.items)
    )


def _scalar(norm_value: Any) -> Any:
    if (
        isinstance(norm_value, tuple)
        and len(norm_value) == 2
        and norm_value[0] in {"keyword", "string", "number", "boolean"}
    ):
        return norm_value[1]
    return norm_value


def _qualifier_value(
    qualifiers: tuple[tuple[str, Any], ...],
    key: str,
) -> Any:
    for name, value in qualifiers:
        if name == key:
            return _scalar(value)
    return None


def snapshot(text: str, path: str = "<memory>") -> Snapshot:
    validation = validate_text(text, path)
    if validation.errors:
        rendered = "\n".join(d.render() for d in validation.errors)
        raise ValueError(f"cannot diff invalid FoM:\n{rendered}")

    root = parse(text)

    relations: dict[str, RelationRecord] = {}
    statuses: dict[tuple[str, Any], StatusRecord] = {}
    disclosures: dict[Any, tuple[tuple[str, Any], ...]] = {}
    fixed_unknown: set[Any] = set()

    def walk(
        expr: Expr,
        current_scope: str | None = None,
    ) -> None:
        if isinstance(expr, (Atom,)):
            return

        if isinstance(expr, VectorExpr):
            for item in expr.items:
                walk(item, current_scope)
            return

        if isinstance(expr, MapExpr):
            for _, value in expr.items:
                walk(value, current_scope)
            return

        if not expr.items:
            return

        head = _head(expr)

        if head == "fom":
            start = 2
            if len(expr.items) > 2 and isinstance(expr.items[2], MapExpr):
                start = 3
            for child in expr.items[start:]:
                walk(child, current_scope)
            return

        if head == "rel" and len(expr.items) == 4:
            rel_id = _symbol(expr.items[1])
            predicate = _symbol(expr.items[2])
            if rel_id and predicate:
                relations[rel_id] = RelationRecord(
                    predicate,
                    normalize(expr.items[3]),
                )
            return

        if head == "scope" and len(expr.items) >= 2:
            scope_id = _symbol(expr.items[1])
            i = 2
            if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
                i += 1
            for child in expr.items[i:]:
                walk(child, scope_id)
            return

        if head in {"accept", "reject"}:
            args = list(expr.items[1:])
            scope_id = current_scope

            if scope_id is not None and len(args) in {1, 2}:
                content = args[0]
                q = args[1] if len(args) == 2 and isinstance(args[1], MapExpr) else None
            elif len(args) in {2, 3}:
                scope_id = _symbol(args[0])
                content = args[1]
                q = args[2] if len(args) == 3 and isinstance(args[2], MapExpr) else None
            else:
                return

            if scope_id is not None:
                statuses[(scope_id, normalize(content))] = StatusRecord(
                    head,
                    _qualifier_tuple(q),
                )
            return

        if head == "constraint":
            i = 2
            if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
                i += 1
            if i < len(expr.items):
                body = expr.items[i]
                body_head = _head(body)
                if isinstance(body, ListExpr) and body_head == "disclosure":
                    if len(body.items) >= 3 and isinstance(body.items[-1], MapExpr):
                        target = normalize(body.items[1])
                        disclosures[target] = _qualifier_tuple(body.items[-1])
                elif isinstance(body, ListExpr) and body_head == "fixed-unknown":
                    if len(body.items) >= 2:
                        fixed_unknown.add(normalize(body.items[1]))
            return

        for child in expr.items[1:]:
            walk(child, current_scope)

    walk(root)

    return Snapshot(
        relations=relations,
        statuses=statuses,
        disclosures=disclosures,
        fixed_unknown=fixed_unknown,
    )


def _ordered_change(
    old: Any,
    new: Any,
    ordering: dict[Any, int],
) -> str:
    if old == new:
        return "PRESERVED"
    if old in ordering and new in ordering:
        if ordering[new] < ordering[old]:
            return "WEAKENED"
        return "STRENGTHENED"
    return "CHANGED"


def diff_texts(
    source_text: str,
    candidate_text: str,
    source_path: str = "<source>",
    candidate_path: str = "<candidate>",
) -> dict[str, list[dict[str, Any]]]:
    source = snapshot(source_text, source_path)
    candidate = snapshot(candidate_text, candidate_path)

    result: dict[str, list[dict[str, Any]]] = {
        "content": [],
        "epistemic_status": [],
        "salience": [],
        "inference_path": [],
        "disclosure": [],
        "fixed_unknown": [],
    }

    all_rel_ids = sorted(set(source.relations) | set(candidate.relations))
    for rel_id in all_rel_ids:
        left = source.relations.get(rel_id)
        right = candidate.relations.get(rel_id)
        dimension = (
            "inference_path"
            if (
                (left and left.predicate in INFERENCE_PREDICATES)
                or (right and right.predicate in INFERENCE_PREDICATES)
            )
            else "content"
        )

        if left is None:
            result[dimension].append(
                {"id": rel_id, "status": "INVENTED"}
            )
        elif right is None:
            result[dimension].append(
                {"id": rel_id, "status": "LOST"}
            )
        elif left != right:
            result[dimension].append(
                {
                    "id": rel_id,
                    "status": (
                        "BROKEN"
                        if dimension == "inference_path"
                        else "CONTRADICTED"
                    ),
                }
            )

    common_status_keys = set(source.statuses) & set(candidate.statuses)
    for key in sorted(common_status_keys, key=repr):
        left = source.statuses[key]
        right = candidate.statuses[key]

        if left.value != right.value:
            result["epistemic_status"].append(
                {
                    "target": repr(key),
                    "status": "CONTRADICTED",
                }
            )
            continue

        old_certainty = _qualifier_value(left.qualifiers, "certainty")
        new_certainty = _qualifier_value(right.qualifiers, "certainty")
        if old_certainty != new_certainty:
            result["epistemic_status"].append(
                {
                    "target": repr(key),
                    "status": _ordered_change(
                        old_certainty,
                        new_certainty,
                        CERTAINTY_ORDER,
                    ),
                    "from": old_certainty,
                    "to": new_certainty,
                }
            )

        old_salience = _qualifier_value(left.qualifiers, "salience")
        new_salience = _qualifier_value(right.qualifiers, "salience")
        if old_salience != new_salience:
            result["salience"].append(
                {
                    "target": repr(key),
                    "status": _ordered_change(
                        old_salience,
                        new_salience,
                        SALIENCE_ORDER,
                    ),
                    "from": old_salience,
                    "to": new_salience,
                }
            )

    for key in sorted(set(source.statuses) - set(candidate.statuses), key=repr):
        result["epistemic_status"].append(
            {"target": repr(key), "status": "LOST"}
        )

    for key in sorted(set(candidate.statuses) - set(source.statuses), key=repr):
        result["epistemic_status"].append(
            {"target": repr(key), "status": "INVENTED"}
        )

    all_disclosure = set(source.disclosures) | set(candidate.disclosures)
    for target in sorted(all_disclosure, key=repr):
        left = source.disclosures.get(target)
        right = candidate.disclosures.get(target)
        if left is None:
            result["disclosure"].append(
                {"target": repr(target), "status": "INVENTED"}
            )
        elif right is None:
            result["disclosure"].append(
                {"target": repr(target), "status": "LOST"}
            )
        elif left != right:
            result["disclosure"].append(
                {"target": repr(target), "status": "CHANGED"}
            )

    for target in sorted(
        source.fixed_unknown - candidate.fixed_unknown,
        key=repr,
    ):
        result["fixed_unknown"].append(
            {"target": repr(target), "status": "LOST"}
        )

    for target in sorted(
        candidate.fixed_unknown - source.fixed_unknown,
        key=repr,
    ):
        result["fixed_unknown"].append(
            {"target": repr(target), "status": "INVENTED"}
        )

    return result


def nonempty_diff(
    diff: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    return {k: v for k, v in diff.items() if v}
