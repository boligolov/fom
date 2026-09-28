import unittest

from fom.model import Atom, ListExpr, Loc, MapExpr, VectorExpr
from fom.parser import parse
from fom.canonical import canonicalize_text


def fragment(text, expr):
    lines = text.splitlines(keepends=True)
    start = sum(map(len, lines[:expr.loc.line - 1])) + expr.loc.col - 1
    end = sum(map(len, lines[:expr.end.line - 1])) + expr.end.col - 1
    return text[start:end]


class SourceSpanTests(unittest.TestCase):
    def test_spans_preserve_raw_escapes_unicode_comments_and_crlf(self):
        text = '(fom demo\r\n\t; ignored ) ] }\r\n (node anna {:label "Я\\n\\\"🙂" :values [true 12 ?x]}))'
        root = parse(text)
        node = root.items[2]
        metadata = node.items[2]
        label = metadata.items[0][1]
        vector = metadata.items[1][1]
        self.assertEqual(fragment(text, root), text)
        self.assertEqual(fragment(text, label), '"Я\\n\\\"🙂"')
        self.assertEqual(label.value, 'Я\n"🙂')
        self.assertEqual(fragment(text, vector), '[true 12 ?x]')
        for value, expected in zip(vector.items, ('true', '12', '?x')):
            self.assertEqual(fragment(text, value), expected)
        self.assertEqual(node.loc, Loc(3, 2))
        self.assertEqual(fragment(text, metadata)[-1], '}')

    def test_multiline_string_ends_at_source_position(self):
        text = '(fom demo (node anna {:label "first\nsecond"}))'
        root = parse(text)
        label = root.items[2].items[2].items[0][1]
        self.assertEqual(label.end, Loc(2, 8))
        self.assertEqual(fragment(text, label), '"first\nsecond"')

    def test_provenance_span_covers_complete_nested_expression(self):
        text = '(fom demo (node anna) (scope s (accept (possible\n  (home anna)))))'
        result = canonicalize_text(text, include_provenance=True)
        origins = {p['target']['ref']: p['source'] for p in result['provenance']}
        for relation in result['relations']:
            loc = origins[relation['id']]
            expr = ListExpr((), Loc(loc['line'], loc['column']), Loc(loc['end_line'], loc['end_column']))
            expected = '(possible\n  (home anna))' if relation['predicate'] == 'possible' else '(home anna)'
            self.assertEqual(fragment(text, expr), expected)

    def test_programmatic_ast_constructors_remain_compatible(self):
        for expr in (Atom('symbol', 'a', Loc(1, 1)), ListExpr((), Loc(1, 1)),
                     VectorExpr((), Loc(1, 1)), MapExpr((), Loc(1, 1))):
            self.assertIsNone(expr.end)
