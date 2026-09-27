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


@dataclass(frozen=True)
class ListExpr:
    items: tuple["Expr", ...]
    loc: Loc


@dataclass(frozen=True)
class VectorExpr:
    items: tuple["Expr", ...]
    loc: Loc


@dataclass(frozen=True)
class MapExpr:
    items: tuple[tuple[Atom, "Expr"], ...]
    loc: Loc


Expr = Atom | ListExpr | VectorExpr | MapExpr
