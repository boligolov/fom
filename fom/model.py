from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Loc:
    line: int
    col: int


@dataclass(frozen=True)
class Atom:
    kind: str
    value: Any
    loc: Loc
    end: Loc | None = None


@dataclass(frozen=True)
class ListExpr:
    items: tuple["Expr", ...]
    loc: Loc
    end: Loc | None = None


@dataclass(frozen=True)
class VectorExpr:
    items: tuple["Expr", ...]
    loc: Loc
    end: Loc | None = None


@dataclass(frozen=True)
class MapExpr:
    items: tuple[tuple[Atom, "Expr"], ...]
    loc: Loc
    end: Loc | None = None


Expr = Atom | ListExpr | VectorExpr | MapExpr
