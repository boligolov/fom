"""Experimental content carrier adapter, deliberately not a UMR importer."""
import re

from fom.validator import validate_text


def symbol(value):
    if not isinstance(value, str) or not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', value):
        raise ValueError(f'unsupported symbol: {value!r}')
    return value


def keys(value, expected):
    if not isinstance(value, dict) or set(value) != set(expected):
        raise ValueError(f'expected fields: {expected}')


def expression(value):
    if set(value) == {'ref'}:
        return symbol(value['ref'])
    if set(value) == {'value'}:
        return ':' + symbol(value['value'])
    keys(value, ('application', 'args'))
    return '(' + symbol(value['application']) + ''.join(' ' + expression(a) for a in value['args']) + ')'


def relation(record):
    keys(record, ('id', 'predicate', 'roles'))
    roles = '{' + ' '.join(':' + symbol(k) + ' ' + expression(v) for k, v in record['roles'].items()) + '}'
    pred = symbol(record['predicate'])
    if record['id'] is not None:
        return f'(rel {symbol(record["id"])} {pred} {roles})'
    return f'({pred} {roles})' if record['roles'] else f'({pred})'


def nodes(entities):
    return [f'(node {symbol(name)} {{:type :{symbol(kind)}}})' for name, kind in entities.items()]


def content_forms(content):
    keys(content, ('entities', 'propositions', 'relations', 'commitments'))
    forms = nodes(content['entities'])
    for name, clauses in content['propositions'].items():
        forms.append(f'(subgraph {symbol(name)} ' + ' '.join(relation(c) for c in clauses) + ')')
    forms.extend(relation(r) for r in content['relations'])
    for commitment in content['commitments']:
        keys(commitment, ('scope', 'mode', 'target', 'certainty'))
        forms.append(f'(scope {symbol(commitment["scope"])} {{:mode :{symbol(commitment["mode"])}}} '
                     f'(accept {expression(commitment["target"])} {{:certainty :{symbol(commitment["certainty"])}}}))')
    return forms


def control_forms(control):
    keys(control, ('entities', 'relations', 'attention', 'constraints'))
    forms = nodes(control['entities'])
    forms.extend(relation(r) for r in control['relations'])
    for attention in control['attention']:
        keys(attention, ('scope', 'target', 'salience'))
        forms.append(f'(scope {symbol(attention["scope"])} {{:mode :attention}} '
                     f'(accept {expression(attention["target"])} {{:salience :{symbol(attention["salience"])}}}))')
    for constraint in control['constraints']:
        kind = constraint['kind']
        if kind == 'fixed-unknown':
            keys(constraint, ('id', 'kind', 'target'))
            body = f'(fixed-unknown {expression(constraint["target"])})'
        elif kind == 'disclosure':
            keys(constraint, ('id', 'kind', 'target', 'before', 'after'))
            body = f'(disclosure {expression(constraint["target"])} '
            body += f'{{:prohibited-before {symbol(constraint["before"])} :required-after {symbol(constraint["after"])}}})'
        elif kind == 'coactivation':
            keys(constraint, ('id', 'kind', 'targets'))
            targets = ' '.join(symbol(t) for t in constraint['targets'])
            body = f'(preserve {{:coactivated [{targets}]}} {{:strength :required}})'
        else:
            raise ValueError(f'unsupported overlay constraint: {kind}')
        forms.append(f'(constraint {symbol(constraint["id"])} {body})')
    return forms


def checked(forms):
    text = '(fom layered-pilot\n  ' + '\n  '.join(forms) + ')\n'
    result = validate_text(text)
    if result.errors:
        raise ValueError('\n'.join(d.render() for d in result.errors))
    return text


def lower(document, carrier_only=False):
    keys(document, ('carrier', 'overlay'))
    forms = content_forms(document['carrier'])
    carrier_text = checked(forms)  # Carrier must not depend on overlay objects.
    overlay_forms = control_forms(document['overlay'])
    complete = checked(forms + overlay_forms)  # Checks dangling refs and double ownership.
    return carrier_text if carrier_only else complete
