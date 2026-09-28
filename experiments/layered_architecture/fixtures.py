"""Hand-authored carrier/overlay pairs; gold labels are intentionally absent.

Constructors only abbreviate this data. Nothing is extracted from FoM gold.
"""
from copy import deepcopy


def ref(name):
    return {"ref": name}


def predicate(name, roles=None, identifier=None):
    return {"predicate": name, "roles": roles or {}, "id": identifier}


def carrier(entities=None, propositions=None, relations=None, commitments=None):
    return {"entities": entities or {}, "propositions": propositions or {},
            "relations": relations or [], "commitments": commitments or []}


def overlay(entities=None, relations=None, attention=None, constraints=None):
    return {"entities": entities or {}, "relations": relations or [],
            "attention": attention or [], "constraints": constraints or []}


def pair(name, content, controls, change):
    source = {"carrier": content, "overlay": controls}
    candidate = deepcopy(source)
    change(candidate)
    return {"id": name, "source": source, "candidate": candidate}


def unknown_change(doc):
    doc['carrier']['entities']['anna'] = 'person'
    doc['carrier']['relations'].append(predicate('owner-of', {'object': ref('umbrella'), 'owner': ref('anna')}, 'invented-owner'))
    doc['overlay']['constraints'] = []


def attribution_change(doc):
    doc['carrier']['relations'] = []
    doc['carrier']['commitments'][0]['target'] = ref('closure')


def inference_change(doc):
    doc['overlay']['relations'] = []
    doc['carrier']['commitments'] = [{"scope": "narrator", "mode": "narrator", "target": ref('recent-visitor'), "certainty": "high"}]


def disclosure_change(doc):
    doc['overlay']['constraints'][0].update(before='initial-reading', after='initial-reading')


def coactivation_change(doc):
    doc['overlay']['constraints'] = []


def certainty_change(doc):
    doc['carrier']['commitments'][0]['certainty'] = 'high'


def attention_change(doc):
    doc['overlay']['attention'][0]['salience'] = 'low'


CASES = [
    pair('unknown-owner',
         carrier({'umbrella': 'object', 'bus-stop': 'place'}, relations=[
             predicate('located-at', {'object': ref('umbrella'), 'place': ref('bus-stop')}, 'umbrella-location')]),
         overlay(constraints=[{'id': 'unknown-owner', 'kind': 'fixed-unknown',
                               'target': {'application': 'owner-of', 'args': [ref('umbrella')]}}]), unknown_change),
    pair('source-attribution',
         carrier({'marina': 'person', 'bridge': 'object'},
                 {'closure': [predicate('closed', {'object': ref('bridge'), 'time': {'value': 'overnight'}}, 'bridge-closed')]},
                 [predicate('reported', {'source': ref('marina'), 'content': ref('closure')}, 'marina-report')],
                 [{'scope': 'narrator', 'mode': 'narrator', 'certainty': 'high',
                   'target': {'application': 'reported', 'args': [ref('marina'), ref('closure')]}}]),
         overlay(), attribution_change),
    pair('inference-route',
         carrier({'sergei': 'person', 'warm-chair': 'object', 'cup-a': 'object', 'cup-b': 'object'},
                 {'evidence-state': [predicate('warm', {'object': ref('warm-chair')}, 'chair-warm'),
                                     predicate('present', {'object': ref('cup-a')}, 'cup-a-present'),
                                     predicate('present', {'object': ref('cup-b')}, 'cup-b-present')],
                  'recent-visitor': [predicate('recently-occupied', {'chair': ref('warm-chair'), 'other-than': ref('sergei')})]}),
         overlay(relations=[predicate('evidence-for', {'evidence': ref('evidence-state'), 'conclusion': ref('recent-visitor')}, 'visitor-inference')]), inference_change),
    pair('delayed-reveal', carrier(propositions={'hidden-letter': [predicate('letter-attached-inside-box')]}),
         overlay({'initial-reading': 'checkpoint', 'evening-reveal': 'checkpoint'},
                 [predicate('before', {'left': ref('initial-reading'), 'right': ref('evening-reveal')}, 'checkpoint-order')],
                 constraints=[{'id': 'reveal-window', 'kind': 'disclosure', 'target': ref('hidden-letter'),
                               'before': 'evening-reveal', 'after': 'evening-reveal'}]), disclosure_change),
    pair('common-tongue',
         carrier(propositions={'communication-reading': [predicate('shared-language-achieved')],
                               'anatomical-reading': [predicate('prosthetic-tongue-found')]}),
         overlay(constraints=[{'id': 'dual-reading', 'kind': 'coactivation',
                               'targets': ['communication-reading', 'anatomical-reading']}]), coactivation_change),
    pair('uncertain-train',
         carrier({'train': 'vehicle'}, {'departure': [predicate('departed', {'vehicle': ref('train')}, 'train-left')]},
                 commitments=[{'scope': 'speaker', 'mode': 'epistemic', 'target': ref('departure'), 'certainty': 'possible'}]),
         overlay(), certainty_change),
    pair('contrastive-focus',
         carrier({'petr': 'person'}, {'refusal': [predicate('refused-to-sign', {'actor': ref('petr')}, 'peter-refused')]}),
         overlay(attention=[{'scope': 'discourse-state', 'target': ref('refusal'), 'salience': 'high'}]), attention_change),
]
