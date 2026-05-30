---
created: 21.05.2026
cssclasses:
  - dashboard-1920
tags:
  - dashboard
  - book
  - writing
---

# 📊 Дашборд романа

## Сводка
```dataviewjs
const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
const docs = dv.pages('"5-Персонажи"');
const tp = dv.pages().where(p => p.file.name === 'TODO');
let total = chs.length, done = 0, words = 0;
for (let c of chs) {
  const ct = await dv.io.load(c.file.path);
  words += ct.split(/\s+/).filter(w => w.length > 0).length;
  if (ct.includes('**Конец')) done++;
}
let tt = 0, td = 0;
if (tp.length > 0) {
  const tc = await dv.io.load(tp[0].file.path);
  const tk = tc.match(/\[[ x]\]/g) || [];
  tt = tk.length; td = tk.filter(t => t === '[x]').length;
}
const pct = Math.min(words / 50000 * 100, 100);
dv.container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">' +
  [{v:total,l:'Глав написано',c:'#4caf50',s:done+' завершено'},{v:words.toLocaleString(),l:'Всего слов',c:'#2196f3',s:pct.toFixed(1)+'% от цели 50 000'},{v:docs.length,l:'Персонажей',c:'#9c27b0',s:'в досье'},{v:td+'/'+tt,l:'Задач выполнено',c:'#ff9800',s:(tt>0?Math.round(td/tt*100):0)+'% готово'}]
  .map(c => '<div style="background:var(--background-secondary);border-radius:12px;padding:22px 20px;border-left:4px solid '+c.c+';position:relative">' +
    '<div style="position:absolute;top:12px;right:12px;width:10px;height:10px;border-radius:50%;background:'+c.c+';opacity:0.6"></div>' +
    '<div style="font-size:38px;font-weight:700;line-height:1.2">'+c.v+'</div>' +
    '<div style="font-size:15px;color:var(--text-muted);margin-top:4px">'+c.l+'</div>' +
    '<div style="font-size:13px;color:var(--text-muted);margin-top:6px">'+c.s+'</div></div>').join('') + '</div>';
```

## Прогресс и статистика
```dataviewjs
const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
const docs = dv.pages('"5-Персонажи"');
const chapterData = [];
let totalWords = 0, doneCount = 0, totalEps = 0;
for (let c of chs) {
  const ct = await dv.io.load(c.file.path);
  const w = ct.split(/\s+/).filter(x => x.length > 0).length;
  totalWords += w;
  const end = ct.includes('**Конец');
  if (end) doneCount++;
  const m = ct.match(/^#{2,3}\s+(.+)$/m);
  const t = m ? m[1].trim() : c.file.name;
  const pct = end ? 100 : Math.min(Math.floor(w / 2500 * 100), 95);
  const col = pct === 100 ? '#4caf50' : pct > 50 ? '#ff9800' : '#f44336';
  const eps = (ct.match(/Эпизод \d+/g) || []).length;
  totalEps += eps;
  chapterData.push({ short: c.file.name.replace('Глава_', ''), title: t, words: w, pct, col, end });
}
const total = chs.length, inProgress = total - doneCount;
const wordPct = Math.min(totalWords / 50000 * 100, 100);
const avgWords = total ? Math.round(totalWords / total) : 0;
const pages = Math.round(totalWords / 250);
let html = '<div style="display:flex;flex-wrap:wrap;gap:16px">';
html += '<div style="flex:2;min-width:350px;background:var(--background-secondary);border-radius:14px;padding:16px 20px">';
html += '<h3 style="margin:0 0 12px;font-size:1.1em;font-weight:600">Прогресс глав</h3>';
html += '<div style="display:flex;flex-direction:column;gap:6px">';
for (let ch of chapterData) {
  html += '<div style="display:flex;align-items:center;gap:6px">'+
    '<span style="min-width:22px;font-weight:700;font-size:13px;color:var(--text-muted)">'+ch.short+'</span>'+
    '<span style="flex:1;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">'+ch.title+'</span>'+
    '<span style="padding:1px 6px;border-radius:5px;font-size:11px;font-weight:700;background:'+ch.col+';color:#fff;min-width:32px;text-align:center">'+ch.pct+'%</span>'+
    '<div style="flex:0 0 100px;height:16px;background:rgba(255,255,255,0.06);border-radius:8px;overflow:hidden">'+
    '<div style="width:'+ch.pct+'%;height:100%;background:'+ch.col+';border-radius:8px;transition:width 0.4s"></div></div>'+
    '<span style="font-size:11px;font-weight:600;color:var(--text-muted);min-width:50px;text-align:right">'+ch.words+'</span></div>';
}
html += '</div></div>';
html += '<div style="flex:1;min-width:250px;background:var(--background-secondary);border-radius:14px;padding:16px 20px">';
html += '<h3 style="margin:0 0 12px;font-size:1.1em;font-weight:600">Статистика</h3>';
const statRows = [
  ['Завершено', doneCount, '#4caf50'], ['В работе', inProgress, '#ff9800'],
  ['Всего слов', totalWords.toLocaleString(), ''], ['Среднее', avgWords.toLocaleString(), ''],
  ['Страниц (~250)', pages, ''], ['Эпизодов', totalEps, ''],
  ['Персонажей', docs.length, ''], ['К цели 50K', wordPct.toFixed(1)+'%', wordPct>50?'#4caf50':'#ff9800'],
];
html += '<div style="display:grid;grid-template-columns:1fr 1fr;gap:2px 16px">';
for (let i = 0; i < statRows.length; i++) {
  const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.03)';
  html += '<div style="display:flex;justify-content:space-between;padding:6px 10px;border-radius:4px'+bg+'">'+
    '<span style="color:var(--text-muted);font-size:13px">'+statRows[i][0]+'</span>'+
    '<span style="font-weight:600;font-size:14px'+(statRows[i][2]?';color:'+statRows[i][2]:'')+'">'+statRows[i][1]+'</span></div>';
}
html += '</div></div></div>';
dv.container.innerHTML = html;
```

## Персонажи
```dataviewjs
const docs = dv.pages('"5-Персонажи"').sort(p => p.file.name);
if (docs.length === 0) { dv.paragraph('Нет досье в 5-Персонажи/'); }
const roleColors = {
  'Главный герой': ['#9c27b0','rgba(156,39,176,0.15)'], 'Отец': ['#455a64','rgba(69,90,100,0.15)'],
  'Лучший друг': ['#e91e63','rgba(233,30,99,0.15)'], 'Технарь': ['#00bcd4','rgba(0,188,212,0.15)'],
  'Тактик': ['#ff5722','rgba(255,87,34,0.15)'], 'Аналитик': ['#607d8b','rgba(96,125,139,0.15)'],
  'Боец': ['#f44336','rgba(244,67,54,0.15)'],
};
const defColor = ['#795548','rgba(121,85,72,0.15)'];
function getColor(role) {
  if (!role) return defColor;
  for (const [k,v] of Object.entries(roleColors)) { if (role.toLowerCase().includes(k.toLowerCase().slice(0,4))) return v; }
  return defColor;
}
function ago(mt) {
  const h = dv.luxon.DateTime.now().diff(mt,'hours').hours;
  if (h<1) return 'только что'; if (h<24) return Math.round(h)+' ч. назад'; if (h<48) return 'вчера';
  return mt.toFormat('dd MMM');
}
let rows = '';
for (let i = 0; i < docs.length; i++) {
  const p = docs[i];
  const role = p.role || '—';
  const [rc, rb] = getColor(role);
  const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
  const bg = i % 2 === 0 ? '' : ';background:var(--background-primary)';
  rows += '<div style="display:contents">'+
    '<div style="padding:10px 16px;display:flex;align-items:center;gap:10px'+bg+'">'+
      '<span style="width:8px;height:8px;border-radius:50%;background:'+rc+';flex-shrink:0"></span>'+
      '<a class="internal-link" href="'+p.file.path+'" style="color:var(--interactive-accent);text-decoration:none;font-weight:500;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block">'+p.file.name+'</a></div>'+
    '<div style="padding:10px 16px;overflow:hidden'+bg+'">'+
      '<span class="badge" style="background:'+rb+';color:'+rc+'">'+role+'</span></div>'+
    '<div style="padding:10px 16px;color:var(--text-muted);font-size:13px'+bg+'">'+(p.age||'—')+'</div>'+
    '<div style="padding:10px 16px;text-align:right;color:var(--text-muted);font-size:13px'+bg+'">'+ago(mt)+'</div></div>';
}
dv.container.innerHTML = '<div style="display:grid;grid-template-columns:0.5fr 3.5fr 0.5fr 0.5fr;border-radius:12px;overflow:hidden;background:var(--background-secondary)">'+
  '<div class="hdr-cell" style="padding:10px 16px;background:rgba(255,255,255,0.04)"><span style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Персонаж</span></div>'+
  '<div class="hdr-cell" style="padding:10px 16px;background:rgba(255,255,255,0.04)"><span style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Роль</span></div>'+
  '<div class="hdr-cell" style="padding:10px 16px;background:rgba(255,255,255,0.04)"><span style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Возраст</span></div>'+
  '<div class="hdr-cell" style="padding:10px 16px;background:rgba(255,255,255,0.04);text-align:right"><span style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Изменён</span></div>'+
  rows+'</div>';
```

## Эпизоды по главам
```dataviewjs
const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
let cardsHtml = '', totalEpisodes = 0;
for (let ch of chs) {
  const ct = await dv.io.load(ch.file.path);
  const lines = ct.split('\n');
  const hdgs = [];
  for (let line of lines) { const m = line.match(/^(#{2,3})\s+(.+)/); if (m) hdgs.push(m[2]); }
  if (hdgs.length === 0) continue;
  const title = hdgs[0];
  const scenes = hdgs.slice(1);
  totalEpisodes += scenes.length;
  cardsHtml += '<div style="background:var(--background-secondary);border-radius:10px;padding:12px 16px">'+
    '<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">'+
      '<span style="font-weight:600;font-size:14px;color:var(--interactive-accent)">'+ch.file.name.replace('Глава_','Глава ')+': '+title+'</span>'+
      '<span style="font-size:11px;padding:2px 8px;border-radius:6px;background:rgba(255,255,255,0.06);color:var(--text-muted);font-weight:600;white-space:nowrap">'+scenes.length+' эп.</span></div>';
  for (let s of scenes) {
    cardsHtml += '<div style="padding:2px 0 2px 8px;font-size:13px;color:var(--text-normal);border-left:2px solid rgba(255,255,255,0.08);margin:2px 0 2px 4px">'+s+'</div>';
  }
  cardsHtml += '</div>';
}
let html = '<div style="font-size:13px;color:var(--text-muted);margin-bottom:10px">Всего эпизодов: <strong style="color:var(--text-normal)">'+totalEpisodes+'</strong></div>';
html += '<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(350px,1fr));gap:10px">'+cardsHtml+'</div>';
dv.container.innerHTML = html;
```

## Задачи
```dataviewjs
const tp = dv.pages().where(p => p.file.name === 'TODO');
const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
if (tp.length === 0) { dv.paragraph('Файл TODO.md не найден.'); }
const content = await dv.io.load(tp[0].file.path);
const lines = content.split('\n');
let currentGroup = '', tasks = [];
for (const line of lines) {
  if (!line.trim()) continue;
  const groupMatch = line.match(/^-\s+(.+?)(?::)?$/);
  const taskMatch = line.match(/^[\t ]*-?\s*\[([ x])\]\s+(.+)/);
  const topTaskMatch = line.match(/^-\s+\[([ x])\]\s+(.+)/);
  if (groupMatch && !line.includes('[ ]') && !line.includes('[x]')) { currentGroup = groupMatch[1].trim(); continue; }
  if (topTaskMatch) { tasks.push({ group: currentGroup||'Основное', done: topTaskMatch[1]==='x', text: topTaskMatch[2] }); continue; }
  if (taskMatch) { tasks.push({ group: currentGroup||'Основное', done: taskMatch[1]==='x', text: taskMatch[2] }); }
}
const total = tasks.length, completed = tasks.filter(t=>t.done).length, active = tasks.filter(t=>!t.done);
const grouped = {};
for (const t of active) { if (!grouped[t.group]) grouped[t.group]=[]; grouped[t.group].push(t.text); }
const donutColor = total>0?(completed===total?'#4caf50':'#ff9800'):'#f44336';
let chData = [];
for (let c of chs) {
  const ct = await dv.io.load(c.file.path);
  const w = ct.split(/\s+/).filter(x => x.length > 0).length;
  const end = ct.includes('**Конец');
  const pct = end ? 100 : Math.min(Math.floor(w / 2500 * 100), 95);
  chData.push({ name: c.file.name.replace('Глава_', 'Гл. '), words: w, pct, end });
}
const chTotal = chData.length;
const chDone = chData.filter(ch => ch.end).length;
const chActive = chData.filter(ch => !ch.end && ch.pct > 0).length;
const chIdle = chData.filter(ch => !ch.end && ch.pct === 0).length;
let html = '<div style="display:flex;flex-wrap:wrap;gap:12px">';
html += '<div style="flex:1;min-width:180px;background:var(--background-secondary);border-radius:14px;padding:14px;text-align:center">';
html += '<div style="position:relative;width:80px;height:80px;margin:0 auto 10px">';
html += '<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient('+donutColor+' 0deg '+(completed/total*360)+'deg, rgba(255,255,255,0.06) '+(completed/total*360)+'deg 360deg)"></div>';
html += '<div style="position:absolute;top:8px;left:8px;right:8px;bottom:8px;border-radius:50%;background:var(--background-secondary)"></div>';
html += '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">';
html += '<div style="font-size:18px;font-weight:700;line-height:1.1">'+completed+'/'+total+'</div>';
html += '<div style="font-size:8px;color:var(--text-muted);text-transform:uppercase">готово</div></div></div>';
if (active.length>0) {
  for (const [group, items] of Object.entries(grouped)) {
    html += '<div style="font-size:9px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.3px;margin:6px 0 2px;text-align:left">'+group+'</div>';
    for (const item of items) {
      html += '<div style="display:flex;align-items:center;gap:4px;padding:2px 0;font-size:11px;text-align:left">'+
        '<span style="width:10px;height:10px;border:2px solid '+donutColor+';border-radius:50%;flex-shrink:0"></span>'+
        '<span style="color:var(--text-normal);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+item+'</span></div>';
    }
  }
} else { html += '<div style="font-size:11px;color:#4caf50;font-weight:600">✅ Все выполнены</div>'; }
html += '</div>';
html += '<div style="flex:1.5;min-width:200px;background:var(--background-secondary);border-radius:14px;padding:12px 14px">';
html += '<div style="font-size:10px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.3px;margin-bottom:6px">Все задачи</div>';
for (const t of tasks) {
  html += '<div style="display:flex;align-items:center;gap:6px;padding:4px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px">'+
    '<span>'+(t.done?'✅':'⬜')+'</span>'+
    '<span style="flex:1;'+(t.done?'text-decoration:line-through;color:var(--text-muted)':'color:var(--text-normal)')+'">'+t.text+'</span>'+
    '<span style="font-size:9px;color:var(--text-muted);padding:1px 6px;border-radius:4px;background:rgba(255,255,255,0.05);white-space:nowrap">'+t.group+'</span></div>';
}
html += '</div>';
html += '<div style="flex:1;min-width:180px;background:var(--background-secondary);border-radius:14px;padding:12px 14px">';
html += '<div style="font-size:10px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.3px;margin-bottom:8px">Статус глав</div>';
html += '<div style="font-size:13px;color:var(--text-muted);margin-bottom:6px">Всего глав: <strong style="color:var(--text-normal)">'+chTotal+'</strong></div>';
if (chTotal > 0) {
  html += '<div style="font-size:12px;color:#4caf50">✅ Завершено: '+chDone+' ('+Math.round(chDone/chTotal*100)+'%)</div>';
  html += '<div style="font-size:12px;color:#ff9800">🔄 В работе: '+chActive+' ('+Math.round(chActive/chTotal*100)+'%)</div>';
  html += '<div style="font-size:12px;color:#9e9e9e">⬜ Не начато: '+chIdle+' ('+Math.round(chIdle/chTotal*100)+'%)</div>';
}
html += '<div style="margin-top:8px;border-top:1px solid rgba(255,255,255,0.06);padding-top:8px">';
for (let ch of chData) {
  const icon = ch.end ? '✅' : (ch.pct > 0 ? '🔄' : '⬜');
  const col = ch.end ? '#4caf50' : (ch.pct > 0 ? '#ff9800' : '#9e9e9e');
  html += '<div style="display:flex;align-items:center;gap:4px;padding:3px 0;font-size:11px;border-bottom:1px solid rgba(255,255,255,0.03)">'+
    '<span>'+icon+'</span>'+
    '<span style="flex:1">'+ch.name+'</span>'+
    '<span style="font-size:10px;color:'+col+';font-weight:600">'+ch.pct+'%</span>'+
    '<span style="font-size:10px;color:var(--text-muted)">'+ch.words+' сл.</span></div>';
}
html += '</div></div></div>';
dv.container.innerHTML = html;
```

## Последние изменения и ссылки
```dataviewjs
const files = dv.pages().sort(p => p.file.mtime, 'desc').limit(12);
const all = dv.pages().sort(p => p.file.name);
function icon(path) {
  if (path.includes('4-Готово')) return '📖'; if (path.includes('5-Персонажи')) return '👤';
  if (path.includes('6-Лор')) return '🌌'; if (path.includes('3-Рецензии')) return '📝';
  if (path.includes('1-План')) return '📋'; if (path.includes('0-Сырьё')) return '💡';
  if (path.includes('7-Промпты')) return '🤖'; if (path.includes('8-Материалы')||path.includes('9-Материалы')) return '🖼️';
  if (path.includes('dashboard')) return '📊'; return '📄';
}
function ago(mt) {
  const h = dv.luxon.DateTime.now().diff(mt,'hours').hours;
  if (h<1) return {t:'только что',c:'#4caf50'}; if (h<2) return {t:'1 ч. назад',c:'#8bc34a'};
  if (h<24) return {t:Math.round(h)+' ч. назад',c:'#ff9800'}; if (h<48) return {t:'вчера',c:'#ff5722'};
  return {t:mt.toFormat('dd.MM.yy'),c:'#9e9e9e'};
}
let html = '<div style="display:flex;flex-wrap:wrap;gap:16px">';
html += '<div style="flex:2;min-width:350px;background:var(--background-secondary);border-radius:14px;overflow:hidden;padding:4px 0">';
for (let i = 0; i < files.length; i++) {
  const p = files[i];
  const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
  const ta = ago(mt);
  const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.03)';
  html += '<div style="display:flex;align-items:center;gap:10px;padding:8px 16px'+bg+'">'+
    '<span style="font-size:16px;flex-shrink:0;width:20px;text-align:center">'+icon(p.file.path)+'</span>'+
    '<div style="flex:1;min-width:0;line-height:1.4">'+
      '<a class="internal-link" href="'+p.file.path+'" style="color:var(--interactive-accent);text-decoration:none;font-size:14px;font-weight:500;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">'+p.file.name+'</a>'+
      '<span style="font-size:11px;color:var(--text-muted)">'+(p.file.folder||'/')+'</span></div>'+
    '<span style="font-size:13px;font-weight:600;color:'+ta.c+';flex-shrink:0;white-space:nowrap">'+ta.t+'</span></div>';
}
html += '</div>';
let prs = '';
for (let p of all) {
  if (['project','TODO','roadmap','идеи','идеи_2','ПЛАН_РАБОТЫ','обучения_Марселя','семейное_древо','команда_мафия','механика_магии'].includes(p.file.name))
    prs += '<a class="internal-link link-btn" style="display:inline-block;background:rgba(255,255,255,0.04);border-radius:8px;padding:4px 10px;font-size:12px;color:var(--interactive-accent);text-decoration:none" href="'+p.file.path+'">'+p.file.name+'</a>';
}
html += '<div style="flex:1;min-width:200px;background:var(--background-secondary);border-radius:14px;padding:14px 16px">'+
  (prs?'<div style="font-size:10px;font-weight:600;color:var(--text-muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">Проекты</div><div style="display:flex;flex-wrap:wrap;gap:4px">'+prs+'</div>':'')+
  '</div></div>';
dv.container.innerHTML = html;
```

## Связи персонажей
```dataviewjs
const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
const docs = dv.pages('"5-Персонажи"').sort(p => p.file.name);
function aliases(d) { const r = d.name||d.file.name.replace(/\(.*\)/,'').trim(); return [...new Set(r.split(/[()]+/).map(s=>s.trim()).filter(s=>s))]; }
const tc = chs.length;
const data = await Promise.all(docs.map(async (d) => {
  const a = aliases(d); let cnt = 0;
  for (let c of chs) { const ct = await dv.io.load(c.file.path); if (a.some(x=>ct.includes(x))) cnt++; }
  return { p: d.file.path, n: d.file.name, cnt, tc };
}));
const t = docs.length, m = data.filter(r=>r.cnt>0).length;
data.sort((a,b)=>b.cnt-a.cnt);
let html = '<div style="background:var(--background-secondary);border-radius:12px;overflow:hidden">'+
  '<div style="padding:14px 16px 6px;font-size:14px;color:var(--text-muted)">Упомянуто <strong style="color:var(--text-normal)">'+m+'/'+t+'</strong> персонажей</div>'+
  '<div style="display:grid;grid-template-columns:2fr 1fr 1fr">'+
  '<div class="hdr-cell" style="padding:10px 16px;background:rgba(255,255,255,0.04);font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Персонаж</div>'+
  '<div class="hdr-cell" style="padding:10px 16px;text-align:center;background:rgba(255,255,255,0.04);font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Глав</div>'+
  '<div class="hdr-cell" style="padding:10px 16px;text-align:center;background:rgba(255,255,255,0.04);font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Активность</div></div>';
for (let i = 0; i < data.length; i++) {
  const r = data[i];
  const em = r.cnt===0?'✕':r.cnt>3?'★★':'★';
  const bp = r.tc>0?Math.round(r.cnt/r.tc*100):0;
  const bc = bp===0?'#f44336':bp>50?'#4caf50':'#ff9800';
  const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.02)';
  html += '<div style="display:grid;grid-template-columns:2fr 1fr 1fr;border-top:1px solid rgba(255,255,255,0.04)'+bg+'">'+
    '<div style="padding:10px 16px"><a class="internal-link" href="'+r.p+'" style="color:var(--interactive-accent);text-decoration:none;font-weight:500;font-size:14px">'+r.n+'</a></div>'+
    '<div style="padding:10px 16px;text-align:center;color:var(--text-normal);font-size:14px">'+r.cnt+' / '+r.tc+'</div>'+
    '<div style="padding:10px 16px;text-align:center"><span style="font-size:14px;color:var(--text-muted)">'+em+'</span> <span style="font-size:13px;color:'+bc+';font-weight:600">'+bp+'%</span></div></div>';
}
html += '</div>';
dv.container.innerHTML = html;
```

## Статистика хранилища и идеи
```dataviewjs
const all = dv.pages();
const ideasFile = dv.pages().where(p => p.file.name === 'идеи');
let ideasStr = '—', ideasQ = '—';
if (ideasFile.length > 0) {
  const c = await dv.io.load(ideasFile[0].file.path);
  ideasStr = c.split('\n').filter(l=>l.trim()).length;
  ideasQ = (c.match(/\?/g)||[]).length;
}
const stats = [
  ['Всего заметок', all.length],
  ['Из них глав', all.where(p=>p.file.name.startsWith('Глава_')&&!p.file.name.includes('правки')&&!p.file.name.includes('бэкап')).length],
  ['Персонажей', dv.pages('"5-Персонажи"').length],
  ['Рецензий', dv.pages('"3-Рецензии"').length],
  ['Изображений', app.vault.getFiles().filter(f=>/\.(jpg|jpeg|png|webp|gif)$/i.test(f.path)).length],
  ['Папок', new Set(all.map(p=>p.file.folder).filter(f=>f&&f!=='/')).size],
];
let html = '<div style="display:flex;flex-wrap:wrap;gap:16px">';
html += '<div style="flex:1;min-width:250px;background:var(--background-secondary);border-radius:14px;padding:16px 20px">'+
  '<h3 style="margin:0 0 12px;font-size:1em;font-weight:600;color:var(--text-muted)">📁 Статистика хранилища</h3>';
html += '<div style="display:flex;flex-direction:column;gap:2px">';
for (let i = 0; i < stats.length; i++) {
  const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.03)';
  html += '<div style="display:flex;justify-content:space-between;padding:7px 12px;border-radius:4px'+bg+'">'+
    '<span style="color:var(--text-muted);font-size:14px">'+stats[i][0]+'</span>'+
    '<span style="font-weight:600;font-size:15px">'+stats[i][1]+'</span></div>';
}
html += '</div></div>';
html += '<div style="flex:1;min-width:250px;background:var(--background-secondary);border-radius:14px;padding:16px 20px">'+
  '<h3 style="margin:0 0 12px;font-size:1em;font-weight:600;color:var(--text-muted)">💡 Идеи</h3>'+
  '<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">'+
  '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;background:var(--background-primary);border-radius:12px">'+
    '<div style="font-size:32px;font-weight:700;color:#2196f3">'+ideasStr+'</div>'+
    '<div style="font-size:12px;color:var(--text-muted);margin-top:4px">Строк</div></div>'+
  '<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:20px;background:var(--background-primary);border-radius:12px">'+
    '<div style="font-size:32px;font-weight:700;color:#ff9800">'+ideasQ+'</div>'+
    '<div style="font-size:12px;color:var(--text-muted);margin-top:4px">Вопросов</div></div></div></div>';
html += '</div>';
dv.container.innerHTML = html;
```
