from __future__ import annotations

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


def symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def head(expr: Expr) -> str | None:
    if isinstance(expr, ListExpr) and expr.items:
        return symbol(expr.items[0])
    return None


@dataclass
class SemanticResolver:
    root: Expr

    def __post_init__(self) -> None:
        self.relations: dict[str, ListExpr] = {}
        self.subgraphs: dict[str, ListExpr] = {}
        self._collect(self.root)

    def _collect(self, expr: Expr) -> None:
        if isinstance(expr, Atom):
            return

        if isinstance(expr, VectorExpr):
            for item in expr.items:
                self._collect(item)
            return

        if isinstance(expr, MapExpr):
            for _, value in expr.items:
                self._collect(value)
            return

        if not expr.items:
            return

        h = head(expr)

        if h == "rel" and len(expr.items) == 4:
            rel_id = symbol(expr.items[1])
            if rel_id:
                self.relations[rel_id] = expr

        elif h == "subgraph" and len(expr.items) >= 2:
            subgraph_id = symbol(expr.items[1])
            if subgraph_id:
                self.subgraphs[subgraph_id] = expr

        for child in expr.items[1:]:
            self._collect(child)

    def normalize(
        self,
        expr: Expr,
        stack: tuple[tuple[str, str], ...] = (),
    ) -> Any:
        if isinstance(expr, Atom):
            if expr.kind == "symbol":
                name = str(expr.value)

                if name in self.relations:
                    key = ("rel", name)
                    if key in stack:
                        return ("cycle-ref", "relation", name)
                    return self.relation_signature(
                        name,
                        stack + (key,),
                    )

                if name in self.subgraphs:
                    key = ("subgraph", name)
                    if key in stack:
                        return ("cycle-ref", "subgraph", name)
                    return self.subgraph_signature(
                        name,
                        stack + (key,),
                    )

            return (expr.kind, expr.value)

        if isinstance(expr, VectorExpr):
            return (
                "vector",
                tuple(self.normalize(x, stack) for x in expr.items),
            )

        if isinstance(expr, MapExpr):
            return (
                "map",
                tuple(
                    sorted(
                        (
                            str(key.value),
                            self.normalize(value, stack),
                        )
                        for key, value in expr.items
                    )
                ),
            )

        if not expr.items:
            return ("list", ())

        h = head(expr)

        if h == "rel" and len(expr.items) == 4:
            rel_id = symbol(expr.items[1])
            if rel_id:
                return self.relation_signature(
                    rel_id,
                    stack + (("rel", rel_id),),
                )

        if h == "subgraph" and len(expr.items) >= 2:
            subgraph_id = symbol(expr.items[1])
            if subgraph_id:
                return self.subgraph_signature(
                    subgraph_id,
                    stack + (("subgraph", subgraph_id),),
                )

        return (
            "list",
            tuple(self.normalize(x, stack) for x in expr.items),
        )

    def relation_signature(
        self,
        rel_id: str,
        stack: tuple[tuple[str, str], ...] = (),
    ) -> Any:
        expr = self.relations[rel_id]
        predicate = symbol(expr.items[2])
        return (
            "relation",
            predicate,
            self.normalize(expr.items[3], stack),
        )

    def subgraph_signature(
        self,
        subgraph_id: str,
        stack: tuple[tuple[str, str], ...] = (),
    ) -> Any:
        expr = self.subgraphs[subgraph_id]
        members = [
            self.normalize(child, stack)
            for child in expr.items[2:]
        ]
        return (
            "subgraph",
            tuple(sorted(members, key=repr)),
        )
