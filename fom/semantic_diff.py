from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .alignment import align_node_aliases
from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from .parser import parse
from .refinement import find_refinement_matches
from .signature import SemanticResolver
from .validator import validate_text


INFERENCE_PREDICATES = {
    "evidence-for",
    "evidence-against",
    "supports",
    "infers",
}

ATTRIBUTION_PREDICATES = {
    "reported",
    "reports",
    "says",
    "said",
    "said-signal",
    "attributed-to",
    "source-of",
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
    coactivations: set[Any]
    order_edges: set[tuple[str, str]]


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


def _qualifier_tuple(
    expr: MapExpr | None,
    normalizer=normalize,
) -> tuple[tuple[str, Any], ...]:
    if expr is None:
        return ()
    return tuple(
        sorted(
            (str(k.value), normalizer(v))
            for k, v in expr.items
        )
    )


def _qualifier_dict(
    qualifiers: tuple[tuple[str, Any], ...],
) -> dict[str, Any]:
    return dict(qualifiers)


def _scalar(norm_value: Any) -> Any:
    if (
        isinstance(norm_value, tuple)
        and len(norm_value) == 2
        and norm_value[0] in {
            "keyword",
            "string",
            "number",
            "boolean",
        }
    ):
        return norm_value[1]
    return norm_value


def _symbol_from_normalized(value: Any) -> str | None:
    if (
        isinstance(value, tuple)
        and len(value) == 2
        and value[0] == "symbol"
    ):
        return str(value[1])
    return None


def _qualifier_value(
    qualifiers: tuple[tuple[str, Any], ...],
    key: str,
) -> Any:
    for name, value in qualifiers:
        if name == key:
            return _scalar(value)
    return None


def snapshot(
    text: str,
    path: str = "<memory>",
    aliases: dict[str, str] | None = None,
) -> Snapshot:
    validation = validate_text(text, path)
    if validation.errors:
        rendered = "\n".join(d.render() for d in validation.errors)
        raise ValueError(f"cannot diff invalid FoM:\n{rendered}")

    root = parse(text)
    resolver = SemanticResolver(root, aliases)
    norm = resolver.normalize

    relations: dict[str, RelationRecord] = {}
    statuses: dict[tuple[str, Any], StatusRecord] = {}
    disclosures: dict[Any, tuple[tuple[str, Any], ...]] = {}
    fixed_unknown: set[Any] = set()
    coactivations: set[Any] = set()
    order_edges: set[tuple[str, str]] = set()

    def walk(
        expr: Expr,
        current_scope: str | None = None,
    ) -> None:
        if isinstance(expr, Atom):
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
            args_expr = expr.items[3]
            if rel_id and predicate:
                relations[rel_id] = RelationRecord(
                    predicate,
                    norm(args_expr),
                )

                if predicate == "before" and isinstance(args_expr, MapExpr):
                    args = _map_dict(args_expr)
                    left = _symbol(args.get("left")) if args.get("left") else None
                    right = _symbol(args.get("right")) if args.get("right") else None
                    if aliases:
                        if left:
                            left = aliases.get(left, left)
                        if right:
                            right = aliases.get(right, right)
                    if left and right:
                        order_edges.add((left, right))
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
                q = (
                    args[1]
                    if len(args) == 2
                    and isinstance(args[1], MapExpr)
                    else None
                )
            elif len(args) in {2, 3}:
                scope_id = _symbol(args[0])
                content = args[1]
                q = (
                    args[2]
                    if len(args) == 3
                    and isinstance(args[2], MapExpr)
                    else None
                )
            else:
                return

            if scope_id is not None:
                statuses[(scope_id, norm(content))] = StatusRecord(
                    head,
                    _qualifier_tuple(q, norm),
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
                    if (
                        len(body.items) >= 3
                        and isinstance(body.items[-1], MapExpr)
                    ):
                        target = norm(body.items[1])
                        disclosures[target] = _qualifier_tuple(
                            body.items[-1],
                            norm,
                        )

                elif (
                    isinstance(body, ListExpr)
                    and body_head == "fixed-unknown"
                ):
                    if len(body.items) >= 2:
                        fixed_unknown.add(norm(body.items[1]))

                elif (
                    isinstance(body, ListExpr)
                    and body_head == "preserve"
                    and len(body.items) >= 2
                    and isinstance(body.items[1], MapExpr)
                ):
                    preserve_map = _map_dict(body.items[1])
                    if "coactivated" in preserve_map:
                        coactivations.add(
                            norm(preserve_map["coactivated"])
                        )
                    elif (
                        "readings" in preserve_map
                        and "coactivation" in preserve_map
                    ):
                        flag = preserve_map["coactivation"]
                        if (
                            isinstance(flag, Atom)
                            and flag.kind == "boolean"
                            and flag.value is True
                        ):
                            coactivations.add(
                                norm(preserve_map["readings"])
                            )
            return

        for child in expr.items[1:]:
            walk(child, current_scope)

    walk(root)

    return Snapshot(
        relations=relations,
        statuses=statuses,
        disclosures=disclosures,
        fixed_unknown=fixed_unknown,
        coactivations=coactivations,
        order_edges=order_edges,
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


def _is_before(
    edges: set[tuple[str, str]],
    left: str,
    right: str,
) -> bool:
    if left == right:
        return False

    frontier = [left]
    seen = {left}

    while frontier:
        current = frontier.pop()
        for a, b in edges:
            if a != current or b in seen:
                continue
            if b == right:
                return True
            seen.add(b)
            frontier.append(b)

    return False


def _relation_dimension(
    left: RelationRecord | None,
    right: RelationRecord | None,
) -> str:
    predicates = {
        record.predicate
        for record in (left, right)
        if record is not None
    }

    if predicates & INFERENCE_PREDICATES:
        return "inference_path"

    if predicates & ATTRIBUTION_PREDICATES:
        return "source_attribution"

    return "content"


def _disclosure_change_status(
    source: Snapshot,
    left: tuple[tuple[str, Any], ...],
    right: tuple[tuple[str, Any], ...],
) -> str:
    left_map = _qualifier_dict(left)
    right_map = _qualifier_dict(right)

    old_after = _symbol_from_normalized(
        left_map.get("required-after")
    )
    new_after = _symbol_from_normalized(
        right_map.get("required-after")
    )

    if old_after and new_after and old_after != new_after:
        if _is_before(source.order_edges, new_after, old_after):
            return "EARLY"
        if _is_before(source.order_edges, old_after, new_after):
            return "LATE"

    return "CHANGED"


def diff_texts(
    source_text: str,
    candidate_text: str,
    source_path: str = "<source>",
    candidate_path: str = "<candidate>",
) -> dict[str, list[dict[str, Any]]]:
    source_root = parse(source_text)
    candidate_root = parse(candidate_text)

    source_aliases, candidate_aliases = align_node_aliases(
        source_root,
        candidate_root,
    )

    source = snapshot(
        source_text,
        source_path,
        source_aliases,
    )
    candidate = snapshot(
        candidate_text,
        candidate_path,
        candidate_aliases,
    )

    result: dict[str, list[dict[str, Any]]] = {
        "content": [],
        "epistemic_status": [],
        "salience": [],
        "inference_path": [],
        "source_attribution": [],
        "disclosure": [],
        "fixed_unknown": [],
        "coactivation": [],
        "resolution": [],
    }

    source_left = set(source.relations)
    candidate_left = set(candidate.relations)

    refinement_matches = find_refinement_matches(
        source_text,
        candidate_text,
    )

    for match in refinement_matches:
        if match.source_relation_id not in source_left:
            continue
        if not set(match.candidate_relation_ids).issubset(
            candidate_left
        ):
            continue

        source_left.discard(match.source_relation_id)
        for rel_id in match.candidate_relation_ids:
            candidate_left.discard(rel_id)

        result["resolution"].append(
            {
                "id": match.source_relation_id,
                "status": "EQUIVALENT_UNDER_REFINEMENT",
                "contract": match.contract_name,
                "candidate_relations": list(
                    match.candidate_relation_ids
                ),
            }
        )

    candidate_by_record: dict[RelationRecord, list[str]] = {}
    for rel_id, record in candidate.relations.items():
        candidate_by_record.setdefault(record, []).append(rel_id)

    # First cancel semantically identical relations, regardless of their IDs.
    # This makes generated/internal relation names non-semantic.
    for source_id, source_record in source.relations.items():
        matches = candidate_by_record.get(source_record)
        if not matches:
            continue

        candidate_id = (
            source_id
            if source_id in matches
            else matches[0]
        )
        matches.remove(candidate_id)
        if not matches:
            candidate_by_record.pop(source_record, None)

        source_left.discard(source_id)
        candidate_left.discard(candidate_id)

    # If the same ID remains on both sides, treat it as a deliberately
    # mutated semantic locus. This preserves useful corruption diagnostics.
    for rel_id in sorted(source_left & candidate_left):
        left = source.relations[rel_id]
        right = candidate.relations[rel_id]
        dimension = _relation_dimension(left, right)

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

        source_left.discard(rel_id)
        candidate_left.discard(rel_id)

    for rel_id in sorted(source_left):
        left = source.relations[rel_id]
        dimension = _relation_dimension(left, None)
        result[dimension].append(
            {"id": rel_id, "status": "LOST"}
        )

    for rel_id in sorted(candidate_left):
        right = candidate.relations[rel_id]
        dimension = _relation_dimension(None, right)
        result[dimension].append(
            {"id": rel_id, "status": "INVENTED"}
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

    for key in sorted(
        set(source.statuses) - set(candidate.statuses),
        key=repr,
    ):
        result["epistemic_status"].append(
            {"target": repr(key), "status": "LOST"}
        )

    for key in sorted(
        set(candidate.statuses) - set(source.statuses),
        key=repr,
    ):
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
                {
                    "target": repr(target),
                    "status": _disclosure_change_status(
                        source,
                        left,
                        right,
                    ),
                }
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

    for target in sorted(
        source.coactivations - candidate.coactivations,
        key=repr,
    ):
        result["coactivation"].append(
            {"target": repr(target), "status": "LOST"}
        )

    for target in sorted(
        candidate.coactivations - source.coactivations,
        key=repr,
    ):
        result["coactivation"].append(
            {"target": repr(target), "status": "INVENTED"}
        )

    return result


def nonempty_diff(
    diff: dict[str, list[dict[str, Any]]],
) -> dict[str, list[dict[str, Any]]]:
    return {k: v for k, v in diff.items() if v}
