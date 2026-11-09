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


# Contrôles des deux nouveaux onglets, de la chronologie et de la classification.
from datetime import date
import re
from urllib.parse import urlsplit
timeline=load('data/timeline.json');content=load('data/content.json')
TS={x['id'] for x in timeline}
assert len(TS)==len(timeline),'Timeline : IDs doublons'
assert len({x['actor_id'] for x in timeline})==len(timeline),'Acteur compté deux fois'
assert t['timeline']['event_type']=='first_documented_appearance'
st={x['id'] for x in t['timeline']['stances']}
cats={x['id'] for x in t['timeline']['categories']}
stanceByActor={x['subject_id']:x['value'] for x in c}
direct=0;context=0
for x in timeline:
 assert x['actor_id'] in A,x['id']
 assert x['category'] in cats and x['stance'] in st,x['id']
 assert x['stance']==stanceByActor.get(x['actor_id'],'unknown'),x['id']
 assert x.get('source_ids') and x.get('evidence_ids'),x['id']
 assert all(k in E for k in x['evidence_ids']),x['id']
 for sid in x['source_ids']:
  assert sid in SM and urlsplit(SM[sid].get('url') or '').scheme=='https',x['id']
 if x['scope']=='direct':direct+=x['status']=='confirmed'
 elif x['scope']=='context':context+=x['status']=='confirmed'
 else:raise AssertionError('Périmètre incohérent '+x['id'])
 if x['status']=='confirmed':
  assert x['date_precision']=='day' and re.fullmatch(r'\d{4}-\d{2}-\d{2}',x['date']),x['id']
  assert date.fromisoformat(x['date'])<=date(2026,11,9),x['id']
 else:
  assert x['status']=='undated' and x['date'] is None and x['date_precision']=='unknown',x['id']

def verify_documentary(items):
 for x in items:
  assert x['evidence_ids'],x.get('id',x.get('title'))
  for eid in x['evidence_ids']:
   assert eid in E,x.get('id',x.get('title'))
   proof=next(z for z in e if z['id']==eid)
   assert proof['source_id'] in SM and SM[proof['source_id']].get('url'),eid

verify_documentary(syn['griefs'])
verify_documentary(content['milestones'])
verify_documentary(content['fact_sheet'])
assert syn['opposition_status']['documented_opponent_count']==0
assert not any(x['stance']=='opposed' and x['status']=='confirmed' for x in timeline)
for x in content['milestones']:
 if x['period_precision']=='day':date.fromisoformat(x['date'])
 else:assert x['period_precision']=='year' and re.fullmatch(r'\d{4}',x['date'])
 assert x['status'] in ('documented','scheduled','forecast')

page=(root/'apps/cards/index.html').read_text(encoding='utf-8')
for tab in ('carto','griefs','watch','timeline','evolution'):
 assert f'data-tab="{tab}"' in page and f'id="tab-{tab}"' in page,tab
assert len(re.findall(r'data-tab="[^"]+"',page))==5
for path in ('assets/js/evolution.js','assets/css/evolution.css'):
 assert (root/path).is_file(),path
module=(root/'assets/js/evolution.js').read_text(encoding='utf-8')
assert 'data-mode="stance"' in module and 'data-mode="new"' in module and 'data-mode="cumulative"' in module
loader=(root/'assets/js/data-loader.js').read_text(encoding='utf-8')
for key in ('timeline:"data/timeline.json"','content:"data/content.json"','synthesis:"data/synthesis.json"'):
 assert key in loader,key
print(f'EXTENSION OK — {len(timeline)} entrées, {direct} datées et directes, {context} datées et contextuelles, {len(syn["griefs"])} thèmes, {len(content["milestones"])} jalons, 5 onglets.')
