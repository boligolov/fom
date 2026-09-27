from __future__ import annotations

from .lexer import Token, lex
from .model import Atom, Expr, ListExpr, Loc, MapExpr, VectorExpr


class ParseError(ValueError):
    def __init__(self, message: str, loc: Loc):
        super().__init__(f"{loc.line}:{loc.col}: {message}")
        self.message = message
        self.loc = loc


def _atom(tok: Token) -> Atom:
    if tok.kind == "STRING":
        return Atom("string", tok.text, tok.loc)

    s = tok.text

    if s.startswith(":"):
        return Atom("keyword", s[1:], tok.loc)

    if s.startswith("?"):
        return Atom("variable", s, tok.loc)

    if s == "true":
        return Atom("boolean", True, tok.loc)

    if s == "false":
        return Atom("boolean", False, tok.loc)

    try:
        if any(c in s for c in ".eE"):
            return Atom("number", float(s), tok.loc)
        return Atom("number", int(s), tok.loc)
    except ValueError:
        return Atom("symbol", s, tok.loc)


def parse(text: str) -> Expr:
    tokens = lex(text)
    pos = 0

    def read() -> Expr:
        nonlocal pos

        if pos >= len(tokens):
            loc = tokens[-1].loc if tokens else Loc(1, 1)
            raise ParseError("unexpected end of input", loc)

        tok = tokens[pos]
        pos += 1

        if tok.kind in {"ATOM", "STRING"}:
            return _atom(tok)

        if tok.kind == "(":
            items: list[Expr] = []
            while True:
                if pos >= len(tokens):
                    raise ParseError("unclosed '(' container", tok.loc)
                if tokens[pos].kind == ")":
                    pos += 1
                    return ListExpr(tuple(items), tok.loc)
                items.append(read())

        if tok.kind == "[":
            items: list[Expr] = []
            while True:
                if pos >= len(tokens):
                    raise ParseError("unclosed '[' container", tok.loc)
                if tokens[pos].kind == "]":
                    pos += 1
                    return VectorExpr(tuple(items), tok.loc)
                items.append(read())

        if tok.kind == "{":
            raw: list[Expr] = []
            while True:
                if pos >= len(tokens):
                    raise ParseError("unclosed '{' container", tok.loc)
                if tokens[pos].kind == "}":
                    pos += 1
                    break
                raw.append(read())

            if len(raw) % 2:
                raise ParseError("map requires key/value pairs", tok.loc)

            pairs: list[tuple[Atom, Expr]] = []
            seen: set[str] = set()

            for i in range(0, len(raw), 2):
                key = raw[i]
                if not isinstance(key, Atom) or key.kind != "keyword":
                    raise ParseError(
                        "map keys must be keywords",
                        getattr(key, "loc", tok.loc),
                    )
                if key.value in seen:
                    raise ParseError(f"duplicate map key :{key.value}", key.loc)
                seen.add(key.value)
                pairs.append((key, raw[i + 1]))

            return MapExpr(tuple(pairs), tok.loc)

        if tok.kind in {")", "]", "}"}:
            raise ParseError(
                f"unexpected closing delimiter {tok.kind!r}",
                tok.loc,
            )

        raise ParseError(f"unexpected token {tok.kind!r}", tok.loc)

    root = read()

    if pos != len(tokens):
        raise ParseError("multiple top-level expressions", tokens[pos].loc)

    return root
