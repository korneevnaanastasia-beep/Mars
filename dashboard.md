---
created: 2026-05-21
tags:
  - dashboard
  - book
  - writing
---

# Дашборд романа

**Жанр:** Тёмное городское фэнтези / Криминальная драма
**Сеттинг:** Современный Санкт-Петербург

```dataviewjs
const chapters = dv.pages()
  .where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
  .sort(p => p.file.name);

let done = 0;
let total = 0;
let inProgress = '';

for (let ch of chapters) {
  total++;
  const content = await dv.io.load(ch.file.path);
  if (content.includes('**Конец')) done++;
  else if (!inProgress) {
    const m = content.match(/^#{2,3}\s+(.+)$/m);
    inProgress = m ? m[1].trim() : ch.file.name;
  }
}

dv.span(`**Статус:** ${done}/${total} глав готово${inProgress ? `, в работе «${inProgress}»` : ''}`);
```

---

## Статистика проекта

```dataviewjs
const chapters = dv.pages()
  .where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'));

const dossiers = dv.pages('"Досье"');
const todoPages = dv.pages().where(p => p.file.name === 'TODO');
let todoTotal = 0, todoDone = 0;
if (todoPages.length > 0) {
  const todoContent = await dv.io.load(todoPages[0].file.path);
  const tasks = todoContent.match(/\[[ x]\]/g) || [];
  todoTotal = tasks.length;
  todoDone = tasks.filter(t => t === '[x]').length;
}

let total = chapters.length;
let totalWords = 0;
let completed = 0;
let allWords = [];
let totalEpisodes = 0;

for (let ch of chapters) {
  let content = await dv.io.load(ch.file.path);
  let words = content.split(/\s+/).filter(w => w.length > 0).length;
  totalWords += words;
  allWords.push(words);
  if (content.includes('**Конец')) completed++;

  const eps = content.match(/Эпизод \d+/g);
  if (eps) totalEpisodes += eps.length;
}

const doneWords = allWords.length > 1 ? allWords.slice(0, -1).reduce((a, b) => a + b, 0) : 0;
const avgWords = total ? Math.round(totalWords / total) : 0;
const minWords = allWords.length ? Math.min(...allWords) : 0;
const maxWords = allWords.length ? Math.max(...allWords) : 0;
const pages = Math.round(totalWords / 250);
const targetWords = 50000;

const barPct = Math.min(totalWords / targetWords * 100, 100);

dv.span(`
| Метрика | Значение |
|---------|----------|
| Написано глав | ${total} |
| Завершено | ${completed} |
| В работе | ${total - completed} |
| Всего слов | ${totalWords.toLocaleString()} |
| Слов в готовых главах | ${doneWords.toLocaleString()} |
| Среднее число слов на главу | ${avgWords.toLocaleString()} |
| Мин / Макс слов в главе | ${minWords} / ${maxWords} |
| Страниц (~250 сл.) | ${pages} |
| Эпизодов | ${totalEpisodes} |
| Персонажей | ${dossiers.length} |
| Задач: сделано / всего |  ${todoDone} / ${todoTotal}|
| Прогресс | ${barPct.toFixed(1)}% (${totalWords.toLocaleString()} / ${targetWords.toLocaleString()} сл.) |
`);
```

---

## Прогресс по главам

```dataviewjs
const chapters = dv.pages()
  .where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
  .sort(p => p.file.name);

for (let ch of chapters) {
  const content = await dv.io.load(ch.file.path);
  const words = content.split(/\s+/).filter(w => w.length > 0).length;
  const hasEnd = content.includes('**Конец');

  const titleMatch = content.match(/^#{2,3}\s+(.+)$/m);
  const title = titleMatch ? titleMatch[1].trim() : ch.file.name;

  const episodes = (content.match(/Эпизод \d+/g) || []).length;
  const pct = hasEnd ? 100 : Math.min(Math.floor(words / 2500 * 100), 95);

  const status = hasEnd ? 'Готова' : `/${episodes}`;

  const color = pct === 100 ? '#4caf50' : pct > 50 ? '#ff9800' : '#f44336';

  const row = dv.el('div');
  row.style.cssText = 'display: flex; align-items: center; gap: 12px; margin: 8px 0;';

  const num = document.createElement('div');
  num.textContent = ch.file.name.replace('Глава_', '');
  num.style.cssText = 'min-width: 60px; font-weight: bold;';
  row.appendChild(num);

  const titleDiv = document.createElement('div');
  titleDiv.textContent = title;
  titleDiv.style.cssText = 'min-width: 200px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;';
  row.appendChild(titleDiv);

  const barOuter = document.createElement('div');
  barOuter.style.cssText = 'flex: 1; height: 22px; background: #e0e0e0; border-radius: 11px; overflow: hidden; position: relative;';
  row.appendChild(barOuter);

  const barFill = document.createElement('div');
  barFill.style.cssText = `width: ${pct}%; height: 100%; background: ${color}; border-radius: 11px; transition: width 0.5s;`;
  barOuter.appendChild(barFill);

  const barLabel = document.createElement('div');
  barLabel.textContent = pct + '%';
  barLabel.style.cssText = 'position: absolute; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; color: #fff; text-shadow: 0 1px 2px rgba(0,0,0,0.5);';
  barOuter.appendChild(barLabel);

  const wc = document.createElement('div');
  wc.textContent = words + ' сл.';
  wc.style.cssText = 'min-width: 60px; text-align: right; color: #666;';
  row.appendChild(wc);
}
```

---

```dataviewjs
const chapters = dv.pages()
  .where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
  .sort(p => p.file.name);

let allScenes = [];
const chapterData = [];

for (let ch of chapters) {
  const content = await dv.io.load(ch.file.path);
  const lines = content.split('\n');
  const headings = [];

  for (let line of lines) {
    const m = line.match(/^(#{2,3})\s+(.+)/);
    if (m) headings.push(m[2]);
  }

  if (headings.length === 0) continue;

  const title = headings[0];
  const scenes = headings.slice(1);

  allScenes.push(...scenes);
  chapterData.push({ name: ch.file.name, title, scenes });
}

dv.header(2, `Эпизоды по главам (${allScenes.length})`);

for (let ch of chapterData) {
  dv.header(3, `${ch.name}: ${ch.title}`);

  if (ch.scenes.length > 0) {
    for (const s of ch.scenes) {
      dv.paragraph(`- ${s}`);
    }
  } else {
    dv.paragraph('_(нет подзаголовков)_');
  }
}
```

---

## Персонажи

```dataviewjs
const dossiers = dv.pages('"Досье"').sort(p => p.file.name);

if (dossiers.length > 0) {
  dv.table(
    ['Персонаж', 'Роль', 'Возраст', 'Изменён'],
    dossiers.map(p => [
      p.file.link,
      p.role || '—',
      p.age || '—',
      dv.luxon.DateTime.fromMillis(p.file.mtime.ts).toRelative()
    ])
  );
} else {
  dv.paragraph('Файлы в папке Досье/ не найдены.');
}
```

---

## Последние изменения

```dataviewjs
const files = dv.pages()
  .sort(p => p.file.mtime, 'desc')
  .limit(10);

dv.table(
  ['Файл', 'Изменён', 'Размер'],
  files.map(p => {
    const mtime = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
    const diff = dv.luxon.DateTime.now().diff(mtime, 'hours').hours;
    const display = diff > 24 ? mtime.toFormat('dd.MM.yyyy HH:mm') : mtime.toRelative();
    return [
      p.file.link,
      display,
      (p.file.size / 1024).toFixed(1) + ' KB'
    ];
  })
);
```

---

## Задачи — [[TODO.md]]

```dataview
TASK
WHERE file.name = "TODO"
SORT completed ASC
```

---

## Связи персонажей (упоминания в главах)

```dataviewjs
const chapters = dv.pages()
  .where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
  .sort(p => p.file.name);

const dossiers = dv.pages('"Досье"').sort(p => p.file.name);

function getAliases(d) {
  const raw = d.name || d.file.name.replace(/\(.*\)/, '').trim();
  const aliases = raw.split(/[()]+/).map(s => s.trim()).filter(s => s.length > 0);
  return [...new Set(aliases)];
}

const totalCh = chapters.length;
const data = await Promise.all(dossiers.map(async (d) => {
  const aliases = getAliases(d);
  let chapterCount = 0;
  for (let ch of chapters) {
    const content = await dv.io.load(ch.file.path);
    if (aliases.some(a => content.includes(a))) chapterCount++;
  }
  return [d.file.link, `${chapterCount} / ${totalCh}`, chapterCount];
}));

const total = dossiers.length;
const mentioned = data.filter(r => r[2] > 0).length;

dv.paragraph(`Найдено по имени в тексте глав: упомянуто **${mentioned}/${total}** персонажей`);

dv.table(['Персонаж', 'Глав', ''], data
  .sort((a, b) => b[2] - a[2])
  .map(r => [r[0], r[1], r[2] === 0 ? '❌' : r[2] > 3 ? '⭐⭐' : '⭐']));
```

---

## Статистика хранилища

```dataviewjs
const all = dv.pages();
const chapters = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'));
const dossiers = dv.pages('"Досье"');
const reviews = dv.pages('"Рецензии"');
const images = dv.pages().where(p => p.file.path.match(/\.(jpg|jpeg|png|webp|gif)$/i));

const folders = new Set(all.map(p => p.file.folder).filter(f => f && f !== '/'));

dv.span(`
| Метрика | Значение |
|---------|----------|
| Всего заметок | ${all.length} |
| Из них глав | ${chapters.length} |
| Персонажей | ${dossiers.length} |
| Рецензий | ${reviews.length} |
| Изображений | ${images.length} |
| Папок | ${folders.size} |
`);
```

---

## Идеи — [[идеи.md]]

```dataviewjs
const ideasFile = dv.pages().where(p => p.file.name === 'идеи');
if (ideasFile.length > 0) {
  const content = await dv.io.load(ideasFile[0].file.path);
  const lines = content.split('\n').filter(l => l.trim());
  const todos = content.match(/[-*]\s\[.?\]/g) || [];
  const done = content.match(/[-*]\s\[x\]/gi) || [];
  const questions = content.match(/\?/g) || [];

  dv.span([
    `**${lines.length}** строк`,
    `**${todos.length}** задач (${done.length} сделано)`,
    `**${questions.length}** вопросов`,
  ].join(' · '));
}
```

---

## Быстрые ссылки

```dataviewjs
const all = dv.pages().sort(p => p.file.name);
const items = [];

for (let p of all) {
  const isChapter = p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап');
  const isProject = ['project', 'TODO', 'идеи', 'roadmap_v2', 'prompt_structure', 'обучения_Марселя'].includes(p.file.name);
  if (isChapter || isProject) {
    items.push(p.file.link);
  }
}

dv.list(items);
```
