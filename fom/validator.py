from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .lexer import LexError
from .macros import MacroError, parse_expanded
from .status import STATUS_FORMS
from .model import Atom, Expr, ListExpr, Loc, MapExpr, VectorExpr
from .parser import ParseError


DECL_FORMS = {
    "node",
    "rel",
    "subgraph",
    "scope",
    "delta",
    "constraint",
    "pattern",
}


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    path: str
    loc: Loc
    code: str
    message: str

    def render(self) -> str:
        return (
            f"{self.path}:{self.loc.line}:{self.loc.col}: "
            f"{self.severity}: {self.code}: {self.message}"
        )


@dataclass
class ValidationResult:
    diagnostics: list[Diagnostic]

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "warning"]


class Validator:
    def __init__(self, path: str):
        self.path = path
        self.diags: list[Diagnostic] = []
        self.ids: dict[str, Loc] = {}
        self.decl_kinds: dict[str, str] = {}
        self.used_ids: set[str] = set()
        self.doc_id: str | None = None

    def error(self, node: Expr, code: str, message: str) -> None:
        self.diags.append(
            Diagnostic("error", self.path, node.loc, code, message)
        )

    def warn(self, loc: Loc, code: str, message: str) -> None:
        self.diags.append(
            Diagnostic("warning", self.path, loc, code, message)
        )

    def validate(self, root: Expr) -> ValidationResult:
        if not isinstance(root, ListExpr) or not root.items:
            self.error(root, "F001", "document must be a non-empty (fom ...) list")
            return ValidationResult(self.diags)

        head = root.items[0]
        if not self._sym_is(head, "fom"):
            self.error(head, "F002", "top-level form must be (fom ...)")
            return ValidationResult(self.diags)

        if len(root.items) < 2 or not self._is_symbol(root.items[1]):
            self.error(
                root,
                "F003",
                "fom document requires a symbolic document id",
            )
            return ValidationResult(self.diags)

        self.doc_id = self._symbol(root.items[1])

        forms = list(root.items[2:])
        if forms and isinstance(forms[0], MapExpr):
            self._validate_map(forms.pop(0), set())

        for form in forms:
            self._collect_decls(form)

        for form in forms:
            self._validate_form(
                form,
                current_scope=None,
                bound=set(),
            )

        for name, loc in sorted(self.ids.items()):
            if (
                self.decl_kinds.get(name) == "node"
                and name not in self.used_ids
            ):
                self.warn(
                    loc,
                    "W001",
                    f"declared node '{name}' is never referenced",
                )

        return ValidationResult(self.diags)

    def _collect_decls(self, expr: Expr) -> None:
        if not isinstance(expr, ListExpr) or not expr.items:
            return

        head_expr = expr.items[0]

        if (
            self._is_symbol(head_expr)
            and self._symbol(head_expr) in DECL_FORMS
        ):
            if len(expr.items) < 2 or not self._is_symbol(expr.items[1]):
                self.error(
                    expr,
                    "F010",
                    f"{self._symbol(head_expr)} requires a symbolic id",
                )
            else:
                name = self._symbol(expr.items[1])
                if name in self.ids:
                    self.error(
                        expr.items[1],
                        "F011",
                        (
                            f"duplicate id '{name}' "
                            f"(first declared at "
                            f"{self.ids[name].line}:{self.ids[name].col})"
                        ),
                    )
                else:
                    self.ids[name] = expr.items[1].loc
                    self.decl_kinds[name] = self._symbol(head_expr)

        for child in expr.items[1:]:
            if isinstance(child, ListExpr):
                self._collect_decls(child)
            elif isinstance(child, VectorExpr):
                for item in child.items:
                    self._collect_decls(item)
            elif isinstance(child, MapExpr):
                for _, value in child.items:
                    self._collect_decls(value)

    def _validate_form(
        self,
        expr: Expr,
        current_scope: str | None,
        bound: set[str],
    ) -> None:
        if not isinstance(expr, ListExpr) or not expr.items:
            self.error(
                expr,
                "F020",
                "top-level/nested form must be a non-empty list",
            )
            return

        head_expr = expr.items[0]

        if not self._is_symbol(head_expr):
            self.error(head_expr, "F021", "form head must be a symbol")
            return

        head = self._symbol(head_expr)

        if head == "node":
            self._validate_node(expr, bound)
        elif head == "rel":
            self._validate_rel(expr, bound)
        elif head == "subgraph":
            for child in expr.items[2:]:
                self._validate_form(child, current_scope, bound)
        elif head == "scope":
            self._validate_scope(expr, bound)
        elif head == "delta":
            self._validate_delta(expr, current_scope, bound)
        elif head == "constraint":
            self._validate_constraint(expr, current_scope, bound)
        elif head == "pattern":
            self._validate_pattern(expr, current_scope, bound)
        else:
            self._validate_expr(expr, current_scope, bound)

    def _validate_node(self, expr: ListExpr, bound: set[str]) -> None:
        if len(expr.items) not in {2, 3}:
            self.error(
                expr,
                "F100",
                "node syntax is (node <id> [<map>])",
            )
            return

        if len(expr.items) == 3:
            if not isinstance(expr.items[2], MapExpr):
                self.error(
                    expr.items[2],
                    "F101",
                    "node metadata must be a map",
                )
            else:
                self._validate_map(expr.items[2], bound)

    def _validate_rel(self, expr: ListExpr, bound: set[str]) -> None:
        if len(expr.items) != 4:
            self.error(
                expr,
                "F110",
                "relation syntax is "
                "(rel <id> <predicate> <vector|map>)",
            )
            return

        if not self._is_symbol(expr.items[2]):
            self.error(
                expr.items[2],
                "F111",
                "relation predicate must be a symbol",
            )

        args = expr.items[3]

        if not isinstance(args, (MapExpr, VectorExpr)):
            self.error(
                args,
                "F112",
                "relation arguments must be a map or vector",
            )
            return

        self._validate_expr(args, None, bound)

    def _validate_scope(
        self,
        expr: ListExpr,
        outer_bound: set[str],
    ) -> None:
        if len(expr.items) < 2:
            return

        scope_id = (
            self._symbol(expr.items[1])
            if self._is_symbol(expr.items[1])
            else None
        )

        i = 2

        if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
            self._validate_map(expr.items[i], outer_bound)
            i += 1

        for child in expr.items[i:]:
            self._validate_form(
                child,
                scope_id,
                set(outer_bound),
            )

    def _validate_delta(
        self,
        expr: ListExpr,
        current_scope: str | None,
        bound: set[str],
    ) -> None:
        i = 2

        if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
            self._validate_map(expr.items[i], bound)
            i += 1

        for child in expr.items[i:]:
            self._validate_expr(child, current_scope, bound)

    def _validate_constraint(
        self,
        expr: ListExpr,
        current_scope: str | None,
        bound: set[str],
    ) -> None:
        i = 2

        if i < len(expr.items) and isinstance(expr.items[i], MapExpr):
            self._validate_map(expr.items[i], bound)
            i += 1

        if len(expr.items) - i != 1:
            self.error(
                expr,
                "F130",
                "constraint requires exactly one constraint expression",
            )
            for child in expr.items[i:]:
                self._validate_expr(child, current_scope, bound)
            return

        self._validate_expr(expr.items[i], current_scope, bound)

    def _validate_pattern(
        self,
        expr: ListExpr,
        current_scope: str | None,
        outer_bound: set[str],
    ) -> None:
        if len(expr.items) < 3 or not isinstance(
            expr.items[2],
            VectorExpr,
        ):
            self.error(
                expr,
                "F140",
                "pattern syntax is "
                "(pattern <id> [<variables>...] <clauses>...)",
            )
            return

        local = set(outer_bound)

        for item in expr.items[2].items:
            if not isinstance(item, Atom) or item.kind != "variable":
                self.error(
                    item,
                    "F141",
                    "pattern variable list may contain only ?variables",
                )
            else:
                if item.value in local:
                    self.error(
                        item,
                        "F142",
                        (
                            "duplicate/shadowed pattern variable "
                            f"'{item.value}'"
                        ),
                    )
                local.add(item.value)

        for clause in expr.items[3:]:
            if (
                not isinstance(clause, ListExpr)
                or not clause.items
                or not self._is_symbol(clause.items[0])
                or self._symbol(clause.items[0])
                not in {"where", "require", "bind"}
            ):
                self.error(
                    clause,
                    "F143",
                    "pattern children must be "
                    "(where ...), (require ...), or (bind ...)",
                )
                continue

            if self._sym_is(clause.items[0], "bind"):
                for spec in clause.items[1:]:
                    if (
                        not isinstance(spec, ListExpr)
                        or len(spec.items) != 2
                        or not isinstance(spec.items[0], Atom)
                        or spec.items[0].kind != "variable"
                    ):
                        self.error(
                            spec,
                            "F144",
                            "bind entry must be (?var <expression>)",
                        )
                        continue

                    if spec.items[0].value not in local:
                        self.error(
                            spec.items[0],
                            "F145",
                            (
                                f"bind target '{spec.items[0].value}' "
                                "must be declared in pattern variable list"
                            ),
                        )

                    self._validate_expr(
                        spec.items[1],
                        current_scope,
                        local,
                    )
            else:
                for body in clause.items[1:]:
                    self._validate_expr(
                        body,
                        current_scope,
                        local,
                    )

    def _validate_expr(
        self,
        expr: Expr,
        current_scope: str | None,
        bound: set[str],
    ) -> None:
        if isinstance(expr, Atom):
            if expr.kind == "variable":
                if expr.value not in bound:
                    self.error(
                        expr,
                        "F200",
                        f"unbound variable '{expr.value}'",
                    )
            elif expr.kind == "symbol":
                self._use_ref(expr)
            return

        if isinstance(expr, VectorExpr):
            for item in expr.items:
                self._validate_expr(
                    item,
                    current_scope,
                    bound,
                )
            return

        if isinstance(expr, MapExpr):
            self._validate_map(
                expr,
                bound,
                current_scope,
            )
            return

        if not expr.items:
            self.error(expr, "F201", "empty application is invalid")
            return

        head_expr = expr.items[0]

        if not self._is_symbol(head_expr):
            self.error(
                head_expr,
                "F202",
                "application head must be a symbol",
            )
            return

        head = self._symbol(head_expr)

        if head in DECL_FORMS:
            self._validate_form(
                expr,
                current_scope,
                bound,
            )
            return

        if head in STATUS_FORMS:
            self._validate_status(
                expr,
                current_scope,
                bound,
            )
            return

        if (
            head in {"for-each", "exists"}
            and len(expr.items) >= 2
            and isinstance(expr.items[1], VectorExpr)
        ):
            local = set(bound)

            for var in expr.items[1].items:
                if not isinstance(var, Atom) or var.kind != "variable":
                    self.error(
                        var,
                        "F203",
                        f"{head} binder list may contain only variables",
                    )
                else:
                    local.add(var.value)

            for item in expr.items[2:]:
                self._validate_expr(
                    item,
                    current_scope,
                    local,
                )
            return

        if (
            head == "the"
            and len(expr.items) >= 2
            and isinstance(expr.items[1], Atom)
            and expr.items[1].kind == "variable"
        ):
            local = set(bound)
            local.add(expr.items[1].value)

            for item in expr.items[2:]:
                self._validate_expr(
                    item,
                    current_scope,
                    local,
                )
            return

        if head in {"where", "require"}:
            for item in expr.items[1:]:
                self._validate_expr(
                    item,
                    current_scope,
                    bound,
                )
            return

        if head in {"add", "connect"}:
            if len(expr.items) != 2:
                self.error(
                    expr,
                    "F210",
                    f"{head} requires exactly one expression",
                )

            for item in expr.items[1:]:
                self._validate_expr(
                    item,
                    current_scope,
                    bound,
                )
            return

        if head in {
            "remove",
            "disconnect",
            "activate",
            "deactivate",
            "uncommit",
        }:
            if len(expr.items) != 2:
                self.error(
                    expr,
                    "F211",
                    f"{head} requires exactly one target",
                )

            for item in expr.items[1:]:
                self._validate_expr(
                    item,
                    current_scope,
                    bound,
                )
            return

        if head == "identify":
            if len(expr.items) != 3:
                self.error(
                    expr,
                    "F212",
                    "identify requires two references",
                )

            for item in expr.items[1:]:
                self._validate_expr(
                    item,
                    current_scope,
                    bound,
                )
            return

        if head == "update":
            if len(expr.items) != 3:
                self.error(
                    expr,
                    "F213",
                    "update syntax is "
                    "(update <target> <map>)",
                )

            if len(expr.items) > 1:
                self._validate_expr(
                    expr.items[1],
                    current_scope,
                    bound,
                )

            if len(expr.items) > 2:
                if not isinstance(expr.items[2], MapExpr):
                    self.error(
                        expr.items[2],
                        "F214",
                        "update changes must be a map",
                    )
                else:
                    self._validate_map(
                        expr.items[2],
                        bound,
                        current_scope,
                    )
            return

        for item in expr.items[1:]:
            self._validate_expr(
                item,
                current_scope,
                bound,
            )

    def _validate_status(
        self,
        expr: ListExpr,
        current_scope: str | None,
        bound: set[str],
    ) -> None:
        args = list(expr.items[1:])

        if not args:
            self.error(
                expr,
                "F220",
                f"{self._symbol(expr.items[0])} requires content",
            )
            return

        if current_scope is not None:
            if (
                len(args) in {1, 2}
                and (
                    len(args) == 1
                    or isinstance(args[1], MapExpr)
                )
            ):
                self.used_ids.add(current_scope)
                self._validate_expr(
                    args[0],
                    current_scope,
                    bound,
                )

                if len(args) == 2:
                    self._validate_map(
                        args[1],
                        bound,
                        current_scope,
                    )
                return

        if len(args) not in {2, 3}:
            self.error(
                expr,
                "F221",
                (
                    f"{self._symbol(expr.items[0])} syntax is "
                    f"({self._symbol(expr.items[0])} "
                    "[scope] content [map])"
                ),
            )

            for arg in args:
                self._validate_expr(
                    arg,
                    current_scope,
                    bound,
                )
            return

        self._validate_expr(
            args[0],
            current_scope,
            bound,
        )
        self._validate_expr(
            args[1],
            current_scope,
            bound,
        )

        if len(args) == 3:
            if not isinstance(args[2], MapExpr):
                self.error(
                    args[2],
                    "F222",
                    "status qualifiers must be a map",
                )
            else:
                self._validate_map(
                    args[2],
                    bound,
                    current_scope,
                )

    def _validate_map(
        self,
        expr: MapExpr,
        bound: set[str],
        current_scope: str | None = None,
    ) -> None:
        for _, value in expr.items:
            self._validate_expr(
                value,
                current_scope,
                bound,
            )

    def _use_ref(self, atom: Atom) -> None:
        name = atom.value

        if name in self.ids:
            self.used_ids.add(name)
        else:
            self.error(
                atom,
                "F300",
                f"unresolved symbol/reference '{name}'",
            )

    @staticmethod
    def _is_symbol(expr: Expr) -> bool:
        return isinstance(expr, Atom) and expr.kind == "symbol"

    @staticmethod
    def _symbol(expr: Expr) -> str:
        assert isinstance(expr, Atom) and expr.kind == "symbol"
        return str(expr.value)

    @classmethod
    def _sym_is(cls, expr: Expr, value: str) -> bool:
        return cls._is_symbol(expr) and cls._symbol(expr) == value


def validate_text(
    text: str,
    path: str = "<memory>",
) -> ValidationResult:
    try:
        root = parse_expanded(text)
    except (LexError, ParseError, MacroError) as exc:
        return ValidationResult(
            [
                Diagnostic(
                    "error",
                    path,
                    exc.loc,
                    "M001" if isinstance(exc, MacroError) else "P001",
                    exc.message,
                )
            ]
        )

    return Validator(path).validate(root)


def validate_path(path: Path) -> ValidationResult:
    return validate_text(
        path.read_text(encoding="utf-8"),
        str(path),
    )
