from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .model import Atom, Expr, ListExpr, MapExpr, VectorExpr
from .parser import parse
from .validator import validate_text


DECLARATION_HEADS = {
    "node",
    "rel",
    "subgraph",
    "scope",
    "delta",
    "constraint",
    "pattern",
}

TEMPORAL_PREDICATES = {
    "before",
    "after",
    "meets",
    "overlaps",
    "starts",
    "during",
    "finishes",
    "equal",
}

CAUSAL_PREDICATES = {
    "causes",
    "prevents",
    "enables",
}

INFERENTIAL_PREDICATES = {
    "evidence-for",
    "evidence-against",
    "supports",
    "infers",
}

SEMIOTIC_PREDICATES = {
    "expresses",
    "refers-to",
    "semiotic-maps-to",
    "conventionally-activates",
    "conventionally-expresses",
}

IDENTITY_PREDICATES = {
    "identity",
    "same-as",
}

STRUCTURAL_PREDICATES = {
    "member-of",
    "part-of",
    "subset-of",
}


def _symbol(expr: Expr) -> str | None:
    if isinstance(expr, Atom) and expr.kind == "symbol":
        return str(expr.value)
    return None


def _head(expr: Expr) -> str | None:
    if isinstance(expr, ListExpr) and expr.items:
        return _symbol(expr.items[0])
    return None


def _map(expr: MapExpr) -> dict[str, Expr]:
    return {str(key.value): value for key, value in expr.items}


def _family(predicate: str) -> str:
    if predicate in IDENTITY_PREDICATES:
        return "identity"
    if predicate in TEMPORAL_PREDICATES:
        return "temporal"
    if predicate in CAUSAL_PREDICATES:
        return "causal"
    if predicate in INFERENTIAL_PREDICATES:
        return "inferential"
    if predicate in SEMIOTIC_PREDICATES:
        return "semiotic"
    if predicate in STRUCTURAL_PREDICATES:
        return "structural"
    return "open"


@dataclass
class Canonicalizer:
    root: Expr

    def __post_init__(self) -> None:
        self.ids: set[str] = set()
        self.nodes: list[dict[str, Any]] = []
        self.relations: list[dict[str, Any]] = []
        self.scopes: list[dict[str, Any]] = []
        self.statuses: list[dict[str, Any]] = []
        self.deltas: list[dict[str, Any]] = []
        self.constraints: list[dict[str, Any]] = []
        self.subgraphs: list[dict[str, Any]] = []
        self.patterns: list[dict[str, Any]] = []
        self._anon_counter = 0
        self._status_counter = 0
        self._collect_ids(self.root)

    def _collect_ids(self, expr: Expr) -> None:
        if isinstance(expr, Atom):
            return

        if isinstance(expr, VectorExpr):
            for item in expr.items:
                self._collect_ids(item)
            return

        if isinstance(expr, MapExpr):
            for _, value in expr.items:
                self._collect_ids(value)
            return

        if not expr.items:
            return

        head = _head(expr)

        if head in DECLARATION_HEADS and len(expr.items) >= 2:
            name = _symbol(expr.items[1])
            if name:
                self.ids.add(name)

        for child in expr.items[1:]:
            self._collect_ids(child)

    def _next_anon(self) -> str:
        self._anon_counter += 1
        return f"_anon-{self._anon_counter:04d}"

    def _next_status(self) -> str:
        self._status_counter += 1
        return f"_status-{self._status_counter:04d}"

    def _value(
        self,
        expr: Expr,
        env: dict[str, str] | None = None,
        *,
        reify_applications: bool = True,
    ) -> Any:
        env = env or {}

        if isinstance(expr, Atom):
            if expr.kind == "symbol":
                return {"ref": str(expr.value)}
            if expr.kind == "variable":
                return {"var": env.get(str(expr.value), str(expr.value))}
            if expr.kind == "keyword":
                return str(expr.value)
            return expr.value

        if isinstance(expr, VectorExpr):
            return [
                self._value(
                    item,
                    env,
                    reify_applications=reify_applications,
                )
                for item in expr.items
            ]

        if isinstance(expr, MapExpr):
            return {
                str(key.value): self._value(
                    value,
                    env,
                    reify_applications=reify_applications,
                )
                for key, value in sorted(
                    expr.items,
                    key=lambda item: str(item[0].value),
                )
            }

        if not expr.items:
            return {"application": []}

        head = _head(expr)
        if head is None:
            return {
                "application": [
                    self._value(
                        item,
                        env,
                        reify_applications=reify_applications,
                    )
                    for item in expr.items
                ]
            }

        if reify_applications and head not in DECLARATION_HEADS:
            rel_id = self._next_anon()

            if (
                len(expr.items) == 2
                and isinstance(expr.items[1], MapExpr)
            ):
                args = self._value(
                    expr.items[1],
                    env,
                    reify_applications=True,
                )
            else:
                args = {
                    f"arg{i}": self._value(
                        item,
                        env,
                        reify_applications=True,
                    )
                    for i, item in enumerate(expr.items[1:])
                }

            self.relations.append(
                {
                    "id": rel_id,
                    "kind": "relation",
                    "family": _family(head),
                    "predicate": head,
                    "args": args,
                    "qualifiers": {},
                    "generated": True,
                }
            )
            return {"ref": rel_id}

        return {
            "operator": head,
            "args": [
                self._value(
                    item,
                    env,
                    reify_applications=reify_applications,
                )
                for item in expr.items[1:]
            ],
        }

    def _metadata(
        self,
        expr: MapExpr | None,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        if expr is None:
            return {}
        return self._value(
            expr,
            env,
            reify_applications=True,
        )

    def _relation_record(
        self,
        expr: ListExpr,
        env: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        rel_id = _symbol(expr.items[1])
        predicate = _symbol(expr.items[2])
        assert rel_id is not None
        assert predicate is not None

        args_expr = expr.items[3]
        if isinstance(args_expr, MapExpr):
            args = self._value(args_expr, env)
        elif isinstance(args_expr, VectorExpr):
            args = {
                f"arg{i}": self._value(item, env)
                for i, item in enumerate(args_expr.items)
            }
        else:
            args = {}

        return {
            "id": rel_id,
            "kind": "relation",
            "family": _family(predicate),
            "predicate": predicate,
            "args": args,
            "qualifiers": {},
            "generated": False,
        }

    def _process_status(
        self,
        expr: ListExpr,
        current_scope: str | None,
        env: dict[str, str] | None,
    ) -> str | None:
        status = _head(expr)
        assert status in {"accept", "reject"}

        args = list(expr.items[1:])
        scope_id = current_scope
        qualifiers: MapExpr | None = None

        if current_scope is not None and len(args) in {1, 2}:
            content = args[0]
            if len(args) == 2 and isinstance(args[1], MapExpr):
                qualifiers = args[1]
        elif len(args) in {2, 3}:
            scope_id = _symbol(args[0])
            content = args[1]
            if len(args) == 3 and isinstance(args[2], MapExpr):
                qualifiers = args[2]
        else:
            return None

        status_id = self._next_status()
        self.statuses.append(
            {
                "id": status_id,
                "kind": "status",
                "scope": {"ref": scope_id} if scope_id else None,
                "value": status,
                "content": self._value(content, env),
                "qualifiers": self._metadata(qualifiers, env),
            }
        )
        return status_id

    def _process_constraint(
        self,
        expr: ListExpr,
        env: dict[str, str] | None,
    ) -> str:
        constraint_id = _symbol(expr.items[1])
        assert constraint_id is not None

        i = 2
        metadata: MapExpr | None = None
        if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
            metadata = expr.items[i]
            i += 1

        body = expr.items[i]
        operator = _head(body)

        record: dict[str, Any] = {
            "id": constraint_id,
            "kind": "constraint",
            "operator": operator,
            "strength": "required",
            "parameters": {},
        }

        meta = self._metadata(metadata, env)
        if "strength" in meta:
            record["strength"] = meta.pop("strength")
        if meta:
            record["metadata"] = meta

        if isinstance(body, ListExpr) and operator is not None:
            body_items = list(body.items[1:])

            if body_items and isinstance(body_items[-1], MapExpr):
                record["parameters"] = self._metadata(
                    body_items.pop(),
                    env,
                )

            if len(body_items) == 1:
                record["target"] = self._value(
                    body_items[0],
                    env,
                )
            elif body_items:
                record["arguments"] = [
                    self._value(item, env)
                    for item in body_items
                ]
        else:
            record["expression"] = self._value(
                body,
                env,
                reify_applications=False,
            )

        self.constraints.append(record)
        return constraint_id

    def _process_pattern(
        self,
        expr: ListExpr,
    ) -> str:
        pattern_id = _symbol(expr.items[1])
        assert pattern_id is not None
        variable_expr = expr.items[2]
        assert isinstance(variable_expr, VectorExpr)

        env: dict[str, str] = {}
        variables: list[str] = []

        for i, item in enumerate(variable_expr.items):
            assert isinstance(item, Atom)
            original = str(item.value)
            canonical = f"?v{i}"
            env[original] = canonical
            variables.append(canonical)

        where: list[Any] = []
        require: list[Any] = []
        bindings: list[dict[str, Any]] = []

        for clause in expr.items[3:]:
            if not isinstance(clause, ListExpr) or not clause.items:
                continue

            clause_head = _head(clause)

            if clause_head == "where":
                where.extend(
                    self._value(item, env)
                    for item in clause.items[1:]
                )

            elif clause_head == "require":
                require.extend(
                    self._value(item, env)
                    for item in clause.items[1:]
                )

            elif clause_head == "bind":
                for spec in clause.items[1:]:
                    if not isinstance(spec, ListExpr):
                        continue
                    variable = spec.items[0]
                    assert isinstance(variable, Atom)
                    bindings.append(
                        {
                            "variable": env.get(
                                str(variable.value),
                                str(variable.value),
                            ),
                            "value": self._value(
                                spec.items[1],
                                env,
                            ),
                        }
                    )

        self.patterns.append(
            {
                "id": pattern_id,
                "kind": "pattern",
                "variables": variables,
                "where": where,
                "bindings": bindings,
                "require": require,
                "accessibility": {},
            }
        )
        return pattern_id

    def _process_delta(
        self,
        expr: ListExpr,
        env: dict[str, str] | None,
    ) -> str:
        delta_id = _symbol(expr.items[1])
        assert delta_id is not None

        i = 2
        metadata: MapExpr | None = None
        if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
            metadata = expr.items[i]
            i += 1

        operations: list[dict[str, Any]] = []

        for op_expr in expr.items[i:]:
            if not isinstance(op_expr, ListExpr) or not op_expr.items:
                continue

            op = _head(op_expr)
            operations.append(
                {
                    "op": op,
                    "args": [
                        self._value(item, env)
                        for item in op_expr.items[1:]
                    ],
                }
            )

        self.deltas.append(
            {
                "id": delta_id,
                "kind": "delta",
                "metadata": self._metadata(metadata, env),
                "operations": operations,
            }
        )
        return delta_id

    def _process_form(
        self,
        expr: Expr,
        current_scope: str | None = None,
        env: dict[str, str] | None = None,
    ) -> str | None:
        if not isinstance(expr, ListExpr) or not expr.items:
            return None

        head = _head(expr)

        if head == "node":
            node_id = _symbol(expr.items[1])
            assert node_id is not None

            metadata = (
                expr.items[2]
                if len(expr.items) == 3
                and isinstance(expr.items[2], MapExpr)
                else None
            )
            data = self._metadata(metadata, env)

            node_type = data.pop("type", None)
            types = (
                node_type
                if isinstance(node_type, list)
                else ([node_type] if node_type is not None else [])
            )

            self.nodes.append(
                {
                    "id": node_id,
                    "kind": "node",
                    "types": types,
                    "qualifiers": data,
                }
            )
            return node_id

        if head == "rel":
            record = self._relation_record(expr, env)
            self.relations.append(record)
            return str(record["id"])

        if head == "subgraph":
            subgraph_id = _symbol(expr.items[1])
            assert subgraph_id is not None

            members: list[dict[str, str]] = []

            for child in expr.items[2:]:
                child_id = self._process_form(
                    child,
                    current_scope,
                    env,
                )
                if child_id:
                    members.append({"ref": child_id})
                elif isinstance(child, ListExpr):
                    members.append(
                        self._value(child, env)
                    )

            self.subgraphs.append(
                {
                    "id": subgraph_id,
                    "kind": "subgraph",
                    "members": members,
                }
            )
            return subgraph_id

        if head == "scope":
            scope_id = _symbol(expr.items[1])
            assert scope_id is not None

            i = 2
            metadata: MapExpr | None = None
            if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
                metadata = expr.items[i]
                i += 1

            data = self._metadata(metadata, env)

            self.scopes.append(
                {
                    "id": scope_id,
                    "kind": "scope",
                    "owner": data.pop("owner", None),
                    "center": data.pop("center", None),
                    "imports": data.pop("imports", []),
                    "status_base": data.pop(
                        "inherits-status-from",
                        None,
                    ),
                    "inherit_mode": data.pop(
                        "inherit-mode",
                        "none",
                    ),
                    "qualifiers": data,
                }
            )

            for child in expr.items[i:]:
                self._process_form(
                    child,
                    scope_id,
                    env,
                )

            return scope_id

        if head in {"accept", "reject"}:
            return self._process_status(
                expr,
                current_scope,
                env,
            )

        if head == "constraint":
            return self._process_constraint(expr, env)

        if head == "pattern":
            return self._process_pattern(expr)

        if head == "delta":
            return self._process_delta(expr, env)

        return None

    def build(self) -> dict[str, Any]:
        assert isinstance(self.root, ListExpr)
        document_id = _symbol(self.root.items[1])
        assert document_id is not None

        i = 2
        metadata: MapExpr | None = None
        if i < len(self.root.items) and isinstance(
            self.root.items[i],
            MapExpr,
        ):
            metadata = self.root.items[i]
            i += 1

        for form in self.root.items[i:]:
            self._process_form(form)

        def sorted_records(
            records: list[dict[str, Any]],
        ) -> list[dict[str, Any]]:
            return sorted(
                records,
                key=lambda record: str(record["id"]),
            )

        return {
            "document": document_id,
            "metadata": self._metadata(metadata),
            "nodes": sorted_records(self.nodes),
            "relations": sorted_records(self.relations),
            "scopes": sorted_records(self.scopes),
            "statuses": sorted_records(self.statuses),
            "deltas": sorted_records(self.deltas),
            "constraints": sorted_records(self.constraints),
            "subgraphs": sorted_records(self.subgraphs),
            "patterns": sorted_records(self.patterns),
            "provenance": [],
        }


def canonicalize_text(
    text: str,
    path: str = "<memory>",
) -> dict[str, Any]:
    validation = validate_text(text, path)
    if validation.errors:
        rendered = "\n".join(
            diagnostic.render()
            for diagnostic in validation.errors
        )
        raise ValueError(
            f"cannot canonicalize invalid FoM:\n{rendered}"
        )

    return Canonicalizer(parse(text)).build()
