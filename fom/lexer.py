from __future__ import annotations

from dataclasses import dataclass

from .model import Loc


@dataclass(frozen=True)
class Token:
    kind: str
    text: str
    loc: Loc
    end: Loc | None = None


class LexError(ValueError):
    def __init__(self, message: str, loc: Loc):
        super().__init__(f"{loc.line}:{loc.col}: {message}")
        self.message = message
        self.loc = loc


DELIMS = set("()[]{}")


def lex(text: str) -> list[Token]:
    out: list[Token] = []
    i = 0
    line = 1
    col = 1
    n = len(text)

    def advance(ch: str) -> None:
        nonlocal line, col
        if ch == "\n":
            line += 1
            col = 1
        else:
            col += 1

    while i < n:
        ch = text[i]

        if ch.isspace():
            advance(ch)
            i += 1
            continue

        if ch == ";":
            while i < n and text[i] != "\n":
                advance(text[i])
                i += 1
            continue

        loc = Loc(line, col)

        if ch in DELIMS:
            advance(ch)
            out.append(Token(ch, ch, loc, Loc(line, col)))
            i += 1
            continue

        if ch == '"':
            i += 1
            advance('"')
            buf: list[str] = []
            while i < n:
                ch = text[i]
                if ch == '"':
                    advance(ch)
                    i += 1
                    out.append(Token("STRING", "".join(buf), loc, Loc(line, col)))
                    break
                if ch == "\\":
                    advance(ch)
                    i += 1
                    if i >= n:
                        raise LexError("unterminated escape", loc)
                    esc = text[i]
                    mapping = {
                        "n": "\n",
                        "t": "\t",
                        "r": "\r",
                        '"': '"',
                        "\\": "\\",
                    }
                    buf.append(mapping.get(esc, esc))
                    advance(esc)
                    i += 1
                    continue

                buf.append(ch)
                advance(ch)
                i += 1
            else:
                raise LexError("unterminated string", loc)
            continue

        start = i
        while (
            i < n
            and not text[i].isspace()
            and text[i] not in DELIMS
            and text[i] != ";"
        ):
            advance(text[i])
            i += 1

        out.append(Token("ATOM", text[start:i], loc, Loc(line, col)))

    return out
