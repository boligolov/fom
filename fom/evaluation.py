"""A bounded executable contract profile; unsupported meaning never passes silently."""
from __future__ import annotations

from typing import Any

from .scope_resolution import resolve_status


def _reference(value: Any) -> str | None:
    if isinstance(value, dict) and set(value) == {"ref"} and isinstance(value["ref"], str):
        return value["ref"]
    return None


def evaluate_constraints(
    contract: dict[str, Any], candidate: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Evaluate source constraints against a state using explicit shared IDs.

    Checks status only, not content preservation, inference, or recoverability.
    Omitting candidate checks the contract document's own represented state.
    """
    state = contract if candidate is None else candidate
    source_scopes = {s["id"] for s in contract["scopes"]}
    candidate_scopes = {s["id"] for s in state["scopes"]}
    source_content = {r["id"]: r for key in ("relations", "subgraphs") for r in contract[key]}
    candidate_content = {r["id"]: r for key in ("relations", "subgraphs") for r in state[key]}
    results = []

    for constraint in contract["constraints"]:
        operator = constraint["operator"]
        strength = constraint["strength"]
        result: dict[str, Any] = {
            "constraint": constraint["id"], "operator": operator,
            "strength": strength,
        }

        def finish(outcome: str, reason: str) -> None:
            result.update(outcome=outcome, reason=reason)
            results.append(result)

        if strength not in ("required", "optional"):
            finish("ERROR", "unsupported constraint strength")
            continue
        if operator not in ("status-is", "unknown"):
            finish("UNSUPPORTED", "operator has no evaluator in this profile")
            continue
        parameters = constraint["parameters"]
        allowed = {"scope", "value"} if operator == "status-is" else {"scope"}
        if (set(parameters) != allowed or "arguments" in constraint
                or "metadata" in constraint):
            finish("UNSUPPORTED", "unsupported parameters or metadata; no fields are ignored")
            continue
        scope = _reference(parameters["scope"])
        target = _reference(constraint.get("target"))
        expected = parameters["value"] if operator == "status-is" else "uncommitted"
        if scope not in source_scopes or target not in source_content:
            finish("ERROR", "contract requires a scope and a relation/subgraph target reference")
            continue
        if expected not in ("accept", "reject", "uncommitted"):
            finish("ERROR", "expected status must be accept, reject, or uncommitted")
            continue
        if source_content[target].get("generated", False):
            finish("UNSUPPORTED", "anonymous target has no cross-document identity contract")
            continue
        result.update(scope=scope, target=target, expected=expected)
        if scope not in candidate_scopes or target not in candidate_content:
            finish("VIOLATED", "candidate is missing the required scope or content reference")
            continue
        if (candidate_content[target].get("generated", False)
                or candidate_content[target]["kind"] != source_content[target]["kind"]):
            finish("VIOLATED", "candidate target does not preserve the declared reference kind")
            continue
        try:
            resolved = resolve_status(state, scope, target)
        except ValueError as exc:
            finish("ERROR", str(exc))
            continue
        result["resolved"] = resolved
        if resolved["status"] == expected:
            finish("SATISFIED", "resolved status matches the requirement")
        else:
            finish("VIOLATED", "resolved status does not match the requirement")

    required = [r for r in results if r["strength"] == "required"]
    if any(r["outcome"] == "ERROR" for r in results):
        outcome = "ERROR"
    elif any(r["outcome"] == "VIOLATED" for r in required):
        outcome = "FAIL"
    elif any(r["outcome"] == "UNSUPPORTED" for r in required):
        outcome = "INDETERMINATE"
    elif not required:
        outcome = "NOT_APPLICABLE"
    else:
        outcome = "PASS"
    return {
        "outcome": outcome,
        "complete": all(r["outcome"] in ("SATISFIED", "VIOLATED") for r in results),
        "required_count": len(required),
        "results": results,
    }
