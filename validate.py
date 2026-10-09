import json
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text(encoding='utf-8'))
a=load('data/actors.json');c=load('data/claims.json');e=load('data/evidence.json');r=load('data/relations.json');s=load('data/sources.json');syn=load('data/synthesis.json');t=load('config/taxonomy.json');m=load('data/meta.json')
assert m['id']=='project_escaudain'
A={x['id'] for x in a};E={x['id'] for x in e};S={x['id'] for x in s}
assert len(A)==len(a),'IDs acteurs dupliqués'
assert len({x['id'] for x in r})==len(r),'IDs liens dupliqués'
assert len({x['id'] for x in c})==len(c),'IDs positions dupliqués'
assert len({x['id'] for x in e})==len(e),'IDs preuves dupliqués'
assert len({x['id'] for x in s})==len(s),'IDs sources dupliqués'
assert m['id'] in A
assert len(a)==55 and len(c)==32 and len(e)==32 and len(r)==90 and len(s)==15
assert sum(x.get('display_in_cards',True) for x in a)==32
assert len(syn['griefs'])==7 and len(syn['vigilance'])==6 and len(syn['sources'])==15
for x in a:assert all(y in t['categories'] for y in x['categories'])
for x in c:assert x['subject_id'] in A and set(x.get('evidence_ids',[]))<=E and x['value'] in t['stances'] and x['certainty'] in t['certainty_levels']
for x in e:assert x.get('source_id') is None or x['source_id'] in S
for x in r:assert x['source_id'] in A and x['target_id'] in A and x['type'] in t['relation_types'] and set(x.get('evidence_ids',[]))<=E
print(f"VALIDATION OK: {len(a)} nœuds, {len(r)} relations, {len(c)} fiches, {len(e)} preuves, {len(s)} références, 3 onglets")
