"""Derived scope views. Canonical records are never mutated or materialized."""
from __future__ import annotations

from typing import Any


def resolve_status(graph: dict[str, Any], scope_id: str, content_id: str) -> dict[str, Any]:
    """Resolve one exact content reference under the none/overlay profile.

    This is not semantic graph matching or constraint satisfaction. Evidence
    retains explicit records, including uncommitted shadows and conflicts.
    """
    scopes = {scope["id"]: scope for scope in graph["scopes"]}
    ids = {record["id"] for name in (
        "nodes", "relations", "subgraphs", "patterns", "constraints", "deltas", "scopes", "statuses",
    ) for record in graph[name]}
    if content_id not in ids:
        raise ValueError(f"unknown content reference: {content_id}")

    parents: dict[str, list[str]] = {}
    visiting: set[str] = set()

    def validate_scope(name: str) -> None:
        if name in visiting:
            raise ValueError(f"cyclic status inheritance at scope: {name}")
        if name in parents:
            return
        if name not in scopes:
            raise ValueError(f"unknown scope: {name}")
        scope = scopes[name]
        mode = scope["inherit_mode"]
        if mode not in ("none", "overlay"):
            raise ValueError(f"unsupported inheritance mode in {name}: {mode}")
        visiting.add(name)
        bases = []
        if mode == "overlay" and scope["status_base"] is not None:
            raw = scope["status_base"]
            for ref in raw if isinstance(raw, list) else [raw]:
                if not isinstance(ref, dict) or set(ref) != {"ref"}:
                    raise ValueError(f"invalid status base in scope: {name}")
                bases.append(ref["ref"])
                validate_scope(ref["ref"])
        visiting.remove(name)
        parents[name] = bases

    validate_scope(scope_id)
    cache: dict[str, list[dict[str, Any]]] = {}

    def evidence(name: str) -> list[dict[str, Any]]:
        if name in cache:
            return cache[name]
        local = [s for s in graph["statuses"]
                 if s["scope"] == {"ref": name} and s["content"] == {"ref": content_id}]
        if local:
            records = local
        else:
            records = [record for parent in parents[name] for record in evidence(parent)]
        # A shared ancestor in a diamond contributes the same record once.
        by_id = {record["id"]: record for record in records}
        cache[name] = [by_id[key] for key in sorted(by_id)]
        return cache[name]

    records = evidence(scope_id)
    values = sorted({record["value"] for record in records})
    result = values[0] if len(values) == 1 else "conflict" if values else "uncommitted"
    return {
        "scope": scope_id,
        "content": content_id,
        "status": result,
        "alternatives": values,
        "evidence": [
            {"record": record["id"], "scope": record["scope"]["ref"],
             "value": record["value"], "qualifiers": dict(record["qualifiers"])}
            for record in records
        ],
    }
