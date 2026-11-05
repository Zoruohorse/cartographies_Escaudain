import json
from pathlib import Path
root=Path(__file__).resolve().parent
load=lambda p:json.loads((root/p).read_text(encoding='utf8'))
a=load('data/actors.json');c=load('data/claims.json');e=load('data/evidence.json');r=load('data/relations.json');s=load('data/sources.json');syn=load('data/synthesis.json');t=load('config/taxonomy.json');m=load('data/meta.json')
def unique(v):
 ids=[x['id'] for x in v];assert len(ids)==len(set(ids)), 'identifiants dupliques';return set(ids)
A=unique(a);C=unique(c);E=unique(e);R=unique(r);S=unique(s);SM={x['id']:x for x in s}
assert m['id']=='project_escaudain' and m['id'] in A
for x in a: assert all(cat in t['categories'] for cat in x['categories']),x['id']
for x in c:
 assert x['subject_id'] in A and x['project_id'] in A and x['value'] in t['stances'] and x['certainty'] in t['certainty_levels'],x['id']
 assert x.get('evidence_ids') and all(z in E for z in x['evidence_ids']),x['id']
for x in e:
 assert x['source_id'] in S and SM[x['source_id']]['status']=='qualified' and SM[x['source_id']]['url'].startswith(('http://','https://')),x['id']
for x in r:
 assert x['source_id'] in A and x['target_id'] in A and x['type'] in t['relation_types'] and x['certainty'] in t['certainty_levels'],x['id']
 assert x.get('evidence_ids') and all(z in E for z in x['evidence_ids']),x['id']
print(f"VALIDATION OK : {len(a)} acteurs, {len(c)} positions, {len(r)} relations, {len(e)} preuves, {sum(bool(x.get('url')) for x in s)} sources qualifiees, {sum(not x.get('url') for x in s)} archivales non qualifiees")
