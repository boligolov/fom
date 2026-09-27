from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr


DECLARATION_HEADS = {
    "node",
    "rel",
    "subgraph",
    "scope",
    "delta",
    "constraint",
    "pattern",
}


def _symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def _head(expr: Expr) -> str | None:
    if isinstance(expr, ListExpr) and expr.items:
        return _symbol(expr.items[0])
    return None


@dataclass(frozen=True)
class NodeInfo:
    node_id: str
    metadata: MapExpr | None


@dataclass(frozen=True)
class RelationInfo:
    predicate: str
    args: Expr


def _collect_nodes(root: Expr) -> dict[str, NodeInfo]:
    out: dict[str, NodeInfo] = {}

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

        h = _head(expr)
        if h == "node" and len(expr.items) >= 2:
            node_id = _symbol(expr.items[1])
            if node_id:
                metadata = (
                    expr.items[2]
                    if len(expr.items) >= 3
                    and isinstance(expr.items[2], MapExpr)
                    else None
                )
                out[node_id] = NodeInfo(node_id, metadata)

        for child in expr.items[1:]:
            walk(child)

    walk(root)
    return out


def _collect_relations(root: Expr) -> list[RelationInfo]:
    out: list[RelationInfo] = []

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

        h = _head(expr)
        if h == "rel" and len(expr.items) == 4:
            predicate = _symbol(expr.items[2])
            if predicate:
                out.append(RelationInfo(predicate, expr.items[3]))

        for child in expr.items[1:]:
            walk(child)

    walk(root)
    return out


def _node_occurrences(
    expr: Expr,
    node_ids: set[str],
) -> set[str]:
    found: set[str] = set()

    def walk(item: Expr) -> None:
        if isinstance(item, Atom):
            if item.kind == "symbol" and str(item.value) in node_ids:
                found.add(str(item.value))
            return
        if isinstance(item, VectorExpr):
            for child in item.items:
                walk(child)
            return
        if isinstance(item, MapExpr):
            for _, child in item.items:
                walk(child)
            return
        for child in item.items:
            walk(child)

    walk(expr)
    return found


def _normalize_context(
    expr: Expr,
    node_ids: set[str],
    focal: str | None,
    colors: dict[str, Any],
) -> Any:
    if isinstance(expr, Atom):
        if expr.kind == "symbol":
            name = str(expr.value)
            if name in node_ids:
                if name == focal:
                    return ("self",)
                return (
                    "node",
                    colors.get(name, ("unresolved-node",)),
                )
            return ("graph-ref",)
        return (expr.kind, expr.value)

    if isinstance(expr, VectorExpr):
        return (
            "vector",
            tuple(
                _normalize_context(
                    item,
                    node_ids,
                    focal,
                    colors,
                )
                for item in expr.items
            ),
        )

    if isinstance(expr, MapExpr):
        return (
            "map",
            tuple(
                sorted(
                    (
                        str(key.value),
                        _normalize_context(
                            value,
                            node_ids,
                            focal,
                            colors,
                        ),
                    )
                    for key, value in expr.items
                )
            ),
        )

    if not expr.items:
        return ("list", ())

    h = _head(expr)
    return (
        "application",
        h,
        tuple(
            _normalize_context(
                item,
                node_ids,
                focal,
                colors,
            )
            for item in expr.items[1:]
        ),
    )


def _base_colors(
    nodes: dict[str, NodeInfo],
    seeded_aliases: dict[str, str],
) -> dict[str, Any]:
    node_ids = set(nodes)
    colors: dict[str, Any] = {}

    for node_id, info in nodes.items():
        if node_id in seeded_aliases:
            colors[node_id] = ("seed", seeded_aliases[node_id])
            continue

        metadata = (
            _normalize_context(
                info.metadata,
                node_ids,
                None,
                {},
            )
            if info.metadata is not None
            else ("map", ())
        )
        colors[node_id] = ("node-meta", metadata)

    return colors


def _fingerprints(
    nodes: dict[str, NodeInfo],
    relations: list[RelationInfo],
    seeded_aliases: dict[str, str],
) -> dict[str, Any]:
    node_ids = set(nodes)
    colors = _base_colors(nodes, seeded_aliases)

    # Two conservative refinement rounds are enough for the first matcher.
    for _ in range(2):
        incidence: dict[str, list[Any]] = defaultdict(list)

        for relation in relations:
            participants = _node_occurrences(
                relation.args,
                node_ids,
            )
            for node_id in participants:
                incidence[node_id].append(
                    (
                        relation.predicate,
                        _normalize_context(
                            relation.args,
                            node_ids,
                            node_id,
                            colors,
                        ),
                    )
                )

        refined: dict[str, Any] = {}
        for node_id in nodes:
            if node_id in seeded_aliases:
                refined[node_id] = (
                    "seed",
                    seeded_aliases[node_id],
                )
                continue

            refined[node_id] = (
                colors[node_id],
                tuple(
                    sorted(
                        incidence.get(node_id, []),
                        key=repr,
                    )
                ),
            )

        colors = refined

    return colors


def align_node_aliases(
    source_root: Expr,
    candidate_root: Expr,
) -> tuple[dict[str, str], dict[str, str]]:
    source_nodes = _collect_nodes(source_root)
    candidate_nodes = _collect_nodes(candidate_root)

    source_aliases: dict[str, str] = {}
    candidate_aliases: dict[str, str] = {}

    # Same explicit ID is a continuity hint, not a semantic proof, but it is
    # useful for mutation fixtures and authored revisions.
    for node_id in sorted(set(source_nodes) & set(candidate_nodes)):
        alias = f"@id:{node_id}"
        source_aliases[node_id] = alias
        candidate_aliases[node_id] = alias

    source_relations = _collect_relations(source_root)
    candidate_relations = _collect_relations(candidate_root)

    match_index = 0

    while True:
        source_fp = _fingerprints(
            source_nodes,
            source_relations,
            source_aliases,
        )
        candidate_fp = _fingerprints(
            candidate_nodes,
            candidate_relations,
            candidate_aliases,
        )

        source_groups: dict[Any, list[str]] = defaultdict(list)
        candidate_groups: dict[Any, list[str]] = defaultdict(list)

        for node_id, fingerprint in source_fp.items():
            if node_id not in source_aliases:
                source_groups[fingerprint].append(node_id)

        for node_id, fingerprint in candidate_fp.items():
            if node_id not in candidate_aliases:
                candidate_groups[fingerprint].append(node_id)

        matches: list[tuple[Any, str, str]] = []

        for fingerprint in set(source_groups) & set(candidate_groups):
            left = source_groups[fingerprint]
            right = candidate_groups[fingerprint]

            if len(left) == 1 and len(right) == 1:
                matches.append(
                    (fingerprint, left[0], right[0])
                )

        if not matches:
            break

        for fingerprint, source_id, candidate_id in sorted(
            matches,
            key=lambda item: repr(item[0]),
        ):
            match_index += 1
            alias = f"@match:{match_index:04d}"
            source_aliases[source_id] = alias
            candidate_aliases[candidate_id] = alias

    return source_aliases, candidate_aliases
