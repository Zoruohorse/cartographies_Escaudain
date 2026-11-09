import{loadRepository,esc,norm,actorClaim,evidenceHtml}from'./data-loader.js?v=20261109';
import { initEvolution } from './evolution.js?v=20261109';const d=await loadRepository();let cat='all',stance='all',q='';document.getElementById('title').textContent=d.meta.title;document.getElementById('subtitle').textContent=d.meta.subtitle;document.getElementById('notice').textContent=d.meta.data_notice;const stanceColor=s=>d.taxonomy.stances[s]?.color||'#64748b';function filters(){categories.innerHTML=Object.entries(d.taxonomy.categories).map(([k,v])=>`<button class="filter ${cat===k?'active':''}" data-cat="${k}"><span>${esc(v.label)}</span><b>${k==='all'?d.actors.filter(a=>a.display_in_cards!==false).length:d.actors.filter(a=>a.display_in_cards!==false&&a.categories.includes(k)).length}</b></button>`).join('');stances.innerHTML=Object.entries(d.taxonomy.stances).map(([k,v])=>`<button class="filter ${stance===k?'active':''}" data-stance="${k}"><span>${esc(v.label)}</span><b>${k==='all'?d.claims.length:d.claims.filter(c=>c.value===k).length}</b></button>`).join('')}function render(){const list=d.actors.filter(a=>a.display_in_cards!==false).filter(a=>{const c=actorClaim(d,a.id);const text=norm([a.name,a.description,c?.summary,...(c?.evidence_ids||[]).map(id=>d.evidenceById.get(id)?.text)].join(' '));return(cat==='all'||a.categories.includes(cat))&&(stance==='all'||c?.value===stance)&&(!q||text.includes(q))});count.textContent=`${list.length} acteurs affichés sur ${d.actors.filter(a=>a.display_in_cards!==false).length}`;grid.innerHTML=list.map(a=>{const c=actorClaim(d,a.id);return `<article class="card" data-id="${a.id}" style="--stance:${stanceColor(c?.value)}"><h3>${esc(a.name)}</h3><div class="role">${esc(a.description)}</div><p class="position">${esc(c?.summary||'Position non renseignée')}</p><div class="footer"><span class="badge">${esc(d.taxonomy.stances[c?.value]?.label||'Non qualifié')}</span><span>Certitude : ${esc(d.taxonomy.certainty_levels[c?.certainty]?.label||'Non qualifiée')}</span></div></article>`}).join('')}function open(id){const a=d.actorById.get(id),c=actorClaim(d,id);const rel=d.relations.filter(r=>r.source_id===id||r.target_id===id);detail.innerHTML=`<h2>${esc(a.name)}</h2><p class="role">${esc(a.description)}</p><h3>Position</h3><p>${esc(c?.summary||'Non renseignée')}</p><p><b>Certitude :</b> ${esc(d.taxonomy.certainty_levels[c?.certainty]?.label||'Non qualifiée')}</p><h3>Preuves et sources</h3>${evidenceHtml(d,c?.evidence_ids)}<h3>Relations documentables</h3>${rel.length?rel.map(r=>{const other=d.actorById.get(r.source_id===id?r.target_id:r.source_id);return `<div class="relation"><button data-open="${other?.id}">${esc(other?.name||'Acteur inconnu')}</button><div><b>${esc(d.taxonomy.relation_types[r.type]?.label||r.type)}</b></div><p>${esc(r.summary)}</p><small>Certitude : ${esc(d.taxonomy.certainty_levels[r.certainty]?.label||r.certainty)} · ${r.evidence_ids.length} preuve(s)</small></div>`}).join(''):'<p class="muted">Aucune relation.</p>'}`;if(!dialog.open)dialog.showModal()}document.addEventListener('click',e=>{const c=e.target.closest('[data-cat]'),s=e.target.closest('[data-stance]'),card=e.target.closest('.card'),op=e.target.closest('[data-open]');if(c){cat=c.dataset.cat;filters();render()}if(s){stance=s.dataset.stance;filters();render()}if(card)open(card.dataset.id);if(op)open(op.dataset.open)});search.addEventListener('input',e=>{q=norm(e.target.value);render()});reset.onclick=()=>{cat='all';stance='all';q='';search.value='';filters();render()};document.querySelector('.close').onclick=()=>dialog.close();filters();render();

// Onglets supplémentaires, basés sur la synthèse du corpus Dunkerque.
const synthesis=d.synthesis;
const selectTab=key=>{
  document.querySelectorAll('[data-tab]').forEach(b=>{b.classList.toggle('active',b.dataset.tab===key);b.setAttribute('aria-selected',String(b.dataset.tab===key))});
  document.querySelectorAll('.tab-pane').forEach(p=>p.classList.toggle('active',p.id==='tab-'+key));
};
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>selectTab(b.dataset.tab)));

// Sources cliquables de la synthèse, preuves et chronologie.
const sourceEvidence=ids=>{
 const out=new Map();
 for(const id of ids||[]){
  const ev=d.evidenceById.get(id),s=ev?.source_id?d.sourceById.get(ev.source_id):null;
  if(s?.url&&s.url.startsWith('https://'))out.set(s.id,s);
 }
 return [...out.values()];
};
const refs=ids=>{
 const items=sourceEvidence(ids);
 return items.length?items.map(s=>'<a href="'+esc(s.url)+'" rel="noopener noreferrer" target="_blank">'+esc(s.publisher||s.title)+'</a>').join(' · '):'Source non qualifiée';
};
const proofDetails=ids=>{
 const list=ids||[];
 return list.length?'<details class="synth-proofs"><summary>Consulter les preuves documentaires ('+list.length+')</summary>'+list.map(id=>{
 const item=d.evidenceById.get(id);
 return item?'<div class="synth-proof">'+esc(item.text)+'<div class="synth-ref">'+refs([id])+'</div></div>':'';
 }).join('')+'</details>':'';
};
document.getElementById('opposition-intro').innerHTML=
 '<h2>État des oppositions documentées</h2><p>'+esc(synthesis.opposition_status?.description||'')+'</p><p class="muted">Les thèmes présentés ci-dessous sont des enjeux ou des questions : ils ne constituent pas, par eux-mêmes, des positions opposées.</p><p class="synth-ref">Références : '+refs(synthesis.opposition_status?.evidence_ids)+'</p>';

const griefGrid=document.getElementById('griefGrid');
griefGrid.innerHTML=synthesis.griefs.length?synthesis.griefs.map(g=>'<article class="griefCard"><h2>'+esc(g.title)+'</h2><p>'+esc(g.text)+'</p><p class="synth-qualification">'+esc(g.qualification||'')+'</p><div class="synth-ref"><b>Sources : </b>'+refs(g.evidence_ids)+'</div>'+proofDetails(g.evidence_ids)+'</article>').join(''):'<p class="muted">Aucun enjeu documenté.</p>';
// Le texte d'origine autorise seulement des balises <strong> pour les intitulés.
const safeRich=t=>esc(t).replace(/&lt;strong&gt;/g,'<strong>').replace(/&lt;\/strong&gt;/g,'</strong>');
document.getElementById('vigilance').innerHTML=synthesis.vigilance.map(t=>`<li>${safeRich(t)}</li>`).join('');
document.getElementById('sources').innerHTML=d.sources.filter(s=>s.url&&s.status==='qualified').map(s=>`<li><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">${esc(s.publisher||'Source')} — ${esc(s.title)}</a></li>`).join('');

// Chronologie : date de l'événement et date de publication restent distinctes.
const dateLabel=m=>m.period_precision==='year'?m.date.slice(0,4):m.period_precision==='month'?m.date.slice(0,7):m.date;
document.getElementById('timelineGrid').innerHTML=(d.content?.milestones||[]).map(m=>
 '<article class="griefCard chrono-card '+(m.status==='scheduled'||m.status==='forecast'?'chrono-future':'')+'"><span class="chrono-date">'+esc(dateLabel(m))+' · '+(m.status==='scheduled'?'À VENIR':m.status==='forecast'?'PRÉVISION':'DOCUMENTÉ')+'</span><h2>'+esc(m.title)+'</h2><p>'+esc(m.details)+'</p>'+(m.date_basis?'<p class="muted">'+esc(m.date_basis)+'</p>':'')+'<div class="synth-ref"><b>Sources : </b>'+refs(m.evidence_ids)+'</div></article>').join('');
document.getElementById('factGrid').innerHTML=(d.content?.fact_sheet||[]).map(f=>
 '<article class="griefCard"><h2>'+esc(f.label)+'</h2><p><strong>'+esc(f.value)+'</strong></p><p class="muted">'+esc(f.qualifier)+'</p><div class="synth-ref"><b>Sources : </b>'+refs(f.evidence_ids)+'</div></article>').join('');
initEvolution({repository:d,root:document.getElementById('evolution-root')});
