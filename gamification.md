---
created: 31.05.2026
tags:
  - gamification
  - book
  - writing
  - game
  - dashboard
cssclasses:
  - dashboard-1920
---

# 🎮 Игровая система

```dataviewjs
// ═══════════════════════════════════════════════════
// 1. СБОР ДАННЫХ ИЗ ХРАНИЛИЩА
// ═══════════════════════════════════════════════════

const chs = dv.pages().where(p => 
  p.file.name.startsWith('Глава_') && 
  !p.file.name.includes('правки') && 
  !p.file.name.includes('бэкап')
).sort(p => p.file.name);

const chars = dv.pages('"5-Персонажи"').sort(p => p.file.name);
const lore = dv.pages('"6-Лор"');
const totalChs = chs.length;
let doneChs = 0;
let totalWords = 0;
let allDates = [];

for (let c of chs) {
  const ct = await dv.io.load(c.file.path);
  const wc = ct.split(/\s+/).filter(w => w.length > 0).length;
  totalWords += wc;
  if (ct.includes('**Конец')) doneChs++;
  const mt = dv.luxon.DateTime.fromMillis(c.file.mtime.ts);
  allDates.push(mt.toISODate());
}

// TODO задачи
const todoPages = dv.pages().where(p => p.file.name === 'TODO');
let doneTasks = 0, totalTasks = 0;
if (todoPages.length > 0) {
  const tc = await dv.io.load(todoPages[0].file.path);
  const tk = tc.match(/\[[ x]\]/g) || [];
  totalTasks = tk.length;
  doneTasks = tk.filter(t => t === '[x]').length;
}

// ═══════════════════════════════════════════════════
// 2. РАСЧЁТ СТРИКА (последовательные дни)
// ═══════════════════════════════════════════════════

const uniqueDates = [...new Set(allDates)].sort().reverse();
const today = dv.luxon.DateTime.now().toISODate();
const yesterday = dv.luxon.DateTime.now().minus({ days: 1 }).toISODate();
const mostRecent = uniqueDates.length > 0 ? uniqueDates[0] : null;

let streak = 0;
let wroteToday = false;
if (mostRecent === today || mostRecent === yesterday) {
  const startFrom = mostRecent;
  wroteToday = mostRecent === today;
  for (let i = 0; ; i++) {
    const d = dv.luxon.DateTime.fromISO(startFrom).minus({ days: i }).toISODate();
    if (uniqueDates.includes(d)) streak++;
    else break;
  }
}

// ═══════════════════════════════════════════════════
// 3. РАСЧЁТ XP И УРОВНЯ
// ═══════════════════════════════════════════════════

const xpWords = Math.floor(totalWords / 10);
const xpChapters = doneChs * 500;
const xpCharacters = chars.length * 100;
const xpLore = lore.length * 75;
const xpTasks = doneTasks * 25;
const xpStreak = streak * 50;
const totalXP = xpWords + xpChapters + xpCharacters + xpLore + xpTasks + xpStreak;

const level = Math.floor(Math.sqrt(totalXP / 100));
const nextLevelXP = (level + 1) * (level + 1) * 100;
const currentLevelXP = Math.max(level * level * 100, 0);
const xpInLevel = totalXP - currentLevelXP;
const xpNeeded = nextLevelXP - currentLevelXP;
const xpPercent = Math.min(Math.floor((xpInLevel / Math.max(xpNeeded, 1)) * 100), 100);

// Титулы
const titles = [
  { min: 0, title: '🌱 Новичок', desc: 'Первые шаги в мире письма', color: '#8bc34a' },
  { min: 3, title: '✍️ Ученик пера', desc: 'Уже кое-что умеешь', color: '#4caf50' },
  { min: 6, title: '📝 Рассказчик', desc: 'Слова начинают течь', color: '#2196f3' },
  { min: 10, title: '📖 Писатель', desc: 'Серьёзный автор', color: '#9c27b0' },
  { min: 15, title: '⚔️ Мастер слова', desc: 'Твои миры оживают', color: '#ff9800' },
  { min: 21, title: '🏆 Хранитель историй', desc: 'Нет преград твоему таланту', color: '#f44336' },
  { min: 30, title: '👑 Властелин страниц', desc: 'Ты — настоящий литератор', color: '#ffd700' },
  { min: 50, title: '🌟 Легенда пера', desc: 'О тебе слагают легенды', color: '#e040fb' },
];
let currentTitle = titles[0];
for (let t of titles) { if (level >= t.min) currentTitle = t; }

// ═══════════════════════════════════════════════════
// 4. ДОСТИЖЕНИЯ
// ═══════════════════════════════════════════════════

const achievements = [
  // Слова
  { id: 'w1k', name: 'Первые шаги', icon: '🌱', cond: totalWords >= 1000, desc: 'Написать 1000 слов', cat: 'Слова' },
  { id: 'w5k', name: 'Разогнался', icon: '🌿', cond: totalWords >= 5000, desc: 'Написать 5000 слов', cat: 'Слова' },
  { id: 'w10k', name: 'Писатель-любитель', icon: '🌳', cond: totalWords >= 10000, desc: 'Написать 10 000 слов', cat: 'Слова' },
  { id: 'w25k', name: 'На полпути', icon: '🏔️', cond: totalWords >= 25000, desc: 'Написать 25 000 слов', cat: 'Слова' },
  { id: 'w50k', name: 'NaNoWriMo', icon: '🎯', cond: totalWords >= 50000, desc: 'Написать 50 000 слов', cat: 'Слова' },
  // Главы
  { id: 'ch1', name: 'Первая глава', icon: '📖', cond: doneChs >= 1, desc: 'Завершить первую главу', cat: 'Главы' },
  { id: 'ch4', name: 'Половина книги', icon: '📚', cond: doneChs >= 4, desc: 'Завершить 4 главы', cat: 'Главы' },
  { id: 'ch7', name: 'Финишная прямая', icon: '🏁', cond: doneChs >= 7, desc: 'Завершить 7 глав', cat: 'Главы' },
  { id: 'ch10', name: 'Роман готов!', icon: '🎉', cond: doneChs >= 10, desc: 'Завершить 10 глав', cat: 'Главы' },
  // Персонажи
  { id: 'char3', name: 'Компания', icon: '👥', cond: chars.length >= 3, desc: 'Создать 3 персонажей', cat: 'Мир' },
  { id: 'char5', name: 'Целая команда', icon: '🤝', cond: chars.length >= 5, desc: 'Создать 5 персонажей', cat: 'Мир' },
  { id: 'char7', name: 'Все в сборе', icon: '👨‍👩‍👧‍👦', cond: chars.length >= 7, desc: 'Создать 7 персонажей', cat: 'Мир' },
  // Лор
  { id: 'lore1', name: 'Миростроитель', icon: '🌍', cond: lore.length >= 1, desc: 'Создать первую лор-заметку', cat: 'Мир' },
  { id: 'lore3', name: 'Глубокий мир', icon: '🌌', cond: lore.length >= 3, desc: 'Создать 3+ лор-заметки', cat: 'Мир' },
  { id: 'lore5', name: 'Архитектор вселенной', icon: '🪐', cond: lore.length >= 5, desc: 'Создать 5+ лор-заметок', cat: 'Мир' },
  // Стрики
  { id: 'str3', name: 'Задел', icon: '🔥', cond: streak >= 3, desc: 'Стрик 3 дня', cat: 'Стрики' },
  { id: 'str7', name: 'Неделя', icon: '🔥🔥', cond: streak >= 7, desc: 'Стрик 7 дней', cat: 'Стрики' },
  { id: 'str14', name: 'Две недели', icon: '🔥🔥🔥', cond: streak >= 14, desc: 'Стрик 14 дней', cat: 'Стрики' },
  { id: 'str30', name: 'Месяц', icon: '💪', cond: streak >= 30, desc: 'Стрик 30 дней!', cat: 'Стрики' },
  // Задачи
  { id: 'todo3', name: 'Планировщик', icon: '✅', cond: doneTasks >= 3, desc: 'Выполнить 3 задачи из TODO', cat: 'Задачи' },
  { id: 'todoall', name: 'Мастер планирования', icon: '🎯', cond: totalTasks > 0 && doneTasks === totalTasks, desc: 'Выполнить все задачи TODO', cat: 'Задачи' },
  // Специальные
  { id: 'bp', name: 'Вампирская сага', icon: '🧛', cond: lore.length >= 4, desc: 'Проработать весь лор вселенной', cat: 'Особые' },
  { id: 'drafting', name: 'Черновик', icon: '✏️', cond: totalChs > doneChs, desc: 'Работать над новой главой', cat: 'Особые' },
];

const earnedAch = achievements.filter(a => a.cond).length;
const totalAch = achievements.length;
const cats = [...new Set(achievements.map(a => a.cat))];

// ═══════════════════════════════════════════════════
// 5. РЕНДЕРИНГ
// ═══════════════════════════════════════════════════

let html = `<style>
  @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
  @keyframes glow { 0%, 100% { box-shadow: 0 0 8px rgba(255,215,0,0.2); } 50% { box-shadow: 0 0 20px rgba(255,215,0,0.5); } }
  @keyframes slideUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes confetti-pop { 0% { transform: scale(0); opacity: 0; } 50% { transform: scale(1.2); } 100% { transform: scale(1); opacity: 1; } }
  .game-section { margin-bottom: 28px; }
  .game-section h2 { font-size: 22px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid var(--interactive-accent); }
</style>`;

// ═══════════ ПРОФИЛЬ ═══════════

html += `<div class="game-section">
<h2>👤 Профиль писателя</h2>
<div style="display:grid;grid-template-columns: 280px 1fr;gap:16px">`;

// Левая колонка — уровень
html += `
<div style="background:var(--background-secondary);border-radius:16px;padding:24px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:8px;animation:slideUp 0.5s ease">
  <div style="position:relative;width:110px;height:110px">
    <div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(${currentTitle.color} 0deg ${xpPercent * 3.6}deg, rgba(255,255,255,0.06) ${xpPercent * 3.6}deg 360deg);${xpPercent >= 100 ? 'animation:glow 2s infinite' : ''}"></div>
    <div style="position:absolute;top:9px;left:9px;right:9px;bottom:9px;border-radius:50%;background:var(--background-secondary);display:flex;flex-direction:column;align-items:center;justify-content:center">
      <div style="font-size:40px;font-weight:800;color:${currentTitle.color};line-height:1">${level}</div>
      <div style="font-size:11px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">уровень</div>
    </div>
  </div>
  <div style="font-size:20px;font-weight:700;color:${currentTitle.color}">${currentTitle.title}</div>
  <div style="font-size:13px;color:var(--text-muted)">${currentTitle.desc}</div>
  <div style="font-size:28px;font-weight:700;color:var(--text-normal);margin-top:4px">${totalXP.toLocaleString()}</div>
  <div style="font-size:11px;color:var(--text-muted)">всего опыта</div>
</div>`;

// Правая колонка — XP бар и статистика
html += `
<div style="background:var(--background-secondary);border-radius:16px;padding:24px;display:flex;flex-direction:column;gap:12px;animation:slideUp 0.5s ease 0.1s both">
  <div>
    <div style="display:flex;justify-content:space-between;font-size:12px;color:var(--text-muted);margin-bottom:4px">
      <span>Ур. ${level}</span>
      <span>${xpInLevel.toLocaleString()} / ${xpNeeded.toLocaleString()} ✦</span>
      <span>Ур. ${level + 1}</span>
    </div>
    <div style="height:12px;background:rgba(255,255,255,0.08);border-radius:6px;overflow:hidden">
      <div style="height:100%;width:${xpPercent}%;background:linear-gradient(90deg,${currentTitle.color},${level >= 20 ? '#ffd700' : '#4caf50'});border-radius:6px;transition:width 1.5s ease"></div>
    </div>
  </div>
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:4px">
    ${[
      { v: totalWords.toLocaleString(), l: 'Всего слов', c: '#4caf50' },
      { v: doneChs + '/' + totalChs, l: 'Глав завершено', c: '#2196f3' },
      { v: '🔥 ' + streak, l: 'Стрик (дней)', c: '#ff6b35' },
      { v: earnedAch + '/' + totalAch, l: 'Достижений', c: '#ffd700' },
    ].map(s => `<div style="text-align:center;padding:10px 4px;background:rgba(255,255,255,0.04);border-radius:10px">
      <div style="font-size:20px;font-weight:700;color:${s.c}">${s.v}</div>
      <div style="font-size:11px;color:var(--text-muted);margin-top:2px">${s.l}</div>
    </div>`).join('')}
  </div>
</div>`;

html += `</div></div>`;

// ═══════════ ИСТОЧНИКИ XP ═══════════

html += `<div class="game-section">
<h2>⚡ Источники опыта</h2>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px">`;

const xpSources = [
  { name: 'Слова', xp: xpWords, color: '#4caf50', icon: '✍️', formula: '10 слов = 1 XP' },
  { name: 'Главы', xp: xpChapters, color: '#2196f3', icon: '📖', formula: '1 глава = 500 XP' },
  { name: 'Мир', xp: xpCharacters + xpLore, color: '#9c27b0', icon: '🌍', formula: 'лор/персонажи' },
  { name: 'Задачи', xp: xpTasks, color: '#ff9800', icon: '✅', formula: '1 задача = 25 XP' },
  { name: 'Стрик', xp: xpStreak, color: '#ff6b35', icon: '🔥', formula: '1 день = 50 XP' },
];

for (let s of xpSources) {
  const pct = totalXP > 0 ? Math.round(s.xp / totalXP * 100) : 0;
  html += `<div style="background:var(--background-secondary);border-radius:12px;padding:14px;text-align:center">
    <div style="font-size:28px">${s.icon}</div>
    <div style="font-size:14px;font-weight:600;margin:6px 0 2px">${s.name}</div>
    <div style="font-size:20px;font-weight:700;color:${s.color}">+${s.xp.toLocaleString()}</div>
    <div style="font-size:11px;color:var(--text-muted)">${pct}%</div>
    <div style="height:4px;background:rgba(255,255,255,0.06);border-radius:2px;margin-top:6px;overflow:hidden">
      <div style="height:100%;width:${pct}%;background:${s.color};border-radius:2px;transition:width 1s"></div>
    </div>
    <div style="font-size:10px;color:var(--text-muted);margin-top:6px">${s.formula}</div>
  </div>`;
}
html += `</div></div>`;

// ═══════════ ДОСТИЖЕНИЯ ═══════════

html += `<div class="game-section">
<h2>🏆 Достижения</h2>
<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px;margin-bottom:16px">
  <div style="display:flex;justify-content:space-between;font-size:13px;color:var(--text-muted);margin-bottom:6px">
    <span>Прогресс: <strong style="color:var(--text-normal)">${earnedAch}/${totalAch}</strong></span>
    <span>${Math.round(earnedAch/totalAch*100)}%</span>
  </div>
  <div style="height:8px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden">
    <div style="height:100%;width:${earnedAch/totalAch*100}%;background:linear-gradient(90deg,#4caf50,#8bc34a,#ffd700);border-radius:4px;transition:width 1s"></div>
  </div>
</div>`;

// По категориям
for (let cat of cats) {
  const catAch = achievements.filter(a => a.cat === cat);
  const catDone = catAch.filter(a => a.cond).length;
  html += `<div style="margin-bottom:12px">
    <div style="font-size:14px;font-weight:600;color:var(--text-muted);margin-bottom:8px;display:flex;gap:8px;align-items:center">
      <span>${cat}</span>
      <span style="font-size:12px;font-weight:400">(${catDone}/${catAch.length})</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:8px">
      ${catAch.map(a => `
        <div style="background:${a.cond ? 'rgba(76,175,80,0.08)' : 'var(--background-primary)'};border-radius:10px;padding:12px;text-align:center;border-left:3px solid ${a.cond ? '#4caf50' : '#555'};opacity:${a.cond ? 1 : 0.5}">
          <div style="font-size:28px">${a.icon}</div>
          <div style="font-size:13px;font-weight:600;margin:4px 0 2px;color:${a.cond ? 'var(--text-normal)' : 'var(--text-muted)'}">${a.name}</div>
          <div style="font-size:10px;color:var(--text-muted)">${a.desc}</div>
          <div style="font-size:10px;margin-top:4px;font-weight:600;color:${a.cond ? '#4caf50' : '#555'}">${a.cond ? '✅ Получено' : '🔒 Закрыто'}</div>
        </div>
      `).join('')}
    </div>
  </div>`;
}
html += `</div>`;

// ═══════════ КАРТА ПРИКЛЮЧЕНИЯ ═══════════

html += `<div class="game-section">
<h2>🗺️ Карта приключения</h2>
<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px">`;

for (let i = 0; i < chs.length; i++) {
  const c = chs[i];
  const ct = await dv.io.load(c.file.path);
  const wc = ct.split(/\s+/).filter(w => w.length > 0).length;
  const isDone = ct.includes('**Конец');
  const m = ct.match(/^#{2,3}\s+(.+)$/m);
  const title = m ? m[1].trim() : c.file.name.replace('Глава_', 'Глава ');
  const pct = isDone ? 100 : Math.min(Math.floor(wc / 2500 * 100), 95);
  const nodeColor = isDone ? '#4caf50' : pct > 50 ? '#ff9800' : '#f44336';
  const nodeIcon = isDone ? '⭐' : (pct > 0 ? '📍' : '🔒');
  
  html += `<div style="display:flex;align-items:center;gap:10px;padding:8px 12px;border-radius:8px;transition:background 0.2s" 
    onmouseover="this.style.background='rgba(255,255,255,0.05)'" 
    onmouseout="this.style.background='transparent'">
    <span style="font-size:18px">${nodeIcon}</span>
    <span style="min-width:28px;font-weight:700;font-size:14px;color:${nodeColor}">${c.file.name.replace('Глава_', '')}</span>
    <span style="flex:1;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${title}</span>
    <div style="width:120px;height:8px;background:rgba(255,255,255,0.06);border-radius:4px;overflow:hidden">
      <div style="height:100%;width:${pct}%;background:${nodeColor};border-radius:4px;transition:width 0.5s"></div>
    </div>
    <span style="min-width:60px;text-align:right;font-size:13px;color:var(--text-muted)">${wc.toLocaleString()} сл.</span>
    <span style="min-width:40px;text-align:right;font-size:13px;font-weight:600;color:${nodeColor}">${isDone ? '✓' : pct + '%'}</span>
  </div>`;
}

html += `</div></div>`;

// ═══════════ ЕЖЕДНЕВНАЯ МОТИВАЦИЯ ═══════════

html += `<div class="game-section">
<h2>⚡ Ежедневная мотивация</h2>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">`;

const quests = [
  { 
    name: wroteToday ? '✅ Писала сегодня!' : '✍️ Написать сегодня', 
    icon: '✍️', 
    done: wroteToday,
    desc: wroteToday ? 'Молодец! Стрик продолжается' : 'Открой Obsidian и напиши хоть 100 слов',
    bg: wroteToday ? 'rgba(76,175,80,0.1)' : 'rgba(255,152,0,0.1)',
    color: wroteToday ? '#4caf50' : '#ff9800'
  },
  { 
    name: totalChs - doneChs > 0 ? '📖 Продолжить главу ' + (doneChs + 1) : '🎉 Все главы готовы!', 
    icon: '📖',
    done: totalChs === doneChs,
    desc: totalChs - doneChs > 0 ? 'Осталось завершить ' + (totalChs - doneChs) + ' глав' : 'Поздравляю!',
    bg: totalChs === doneChs ? 'rgba(76,175,80,0.1)' : 'rgba(33,150,243,0.1)',
    color: totalChs === doneChs ? '#4caf50' : '#2196f3'
  },
  { 
    name: '👥 Всего персонажей: ' + chars.length, 
    icon: '👤',
    done: chars.length >= 7,
    desc: chars.length < 7 ? 'Создай ещё ' + (7 - chars.length) + ' персонажей' : 'Команда полностью собрана!',
    bg: chars.length >= 7 ? 'rgba(76,175,80,0.1)' : 'rgba(156,39,176,0.1)',
    color: chars.length >= 7 ? '#4caf50' : '#9c27b0'
  },
];

for (let q of quests) {
  html += `<div style="background:${q.bg};border-radius:12px;padding:16px;display:flex;align-items:center;gap:12px">
    <span style="font-size:32px">${q.icon}</span>
    <div style="flex:1">
      <div style="font-size:15px;font-weight:600;color:${q.color}">${q.name}</div>
      <div style="font-size:12px;color:var(--text-muted);margin-top:2px">${q.desc}</div>
    </div>
    <div style="font-size:20px">${q.done ? '✅' : '⏳'}</div>
  </div>`;
}

html += `</div></div>`;

// ═══════════ ВРЕМЯ СЛЕДУЮЩЕГО УРОВНЯ ═══════════

const xpToNext = xpNeeded - xpInLevel;
const wordsToNext = Math.ceil(xpToNext * 10); // because 10 words = 1 XP
html += `<div class="game-section">
<h2>🎯 До следующего уровня</h2>
<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px;display:flex;gap:24px;flex-wrap:wrap">
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:24px">✍️</span>
    <div>
      <div style="font-size:14px;color:var(--text-muted)">Написать ещё</div>
      <div style="font-size:22px;font-weight:700">${wordsToNext.toLocaleString()} слов</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:24px">📖</span>
    <div>
      <div style="font-size:14px;color:var(--text-muted)">Или завершить</div>
      <div style="font-size:22px;font-weight:700">${Math.ceil(xpToNext / 500)} глав</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:12px">
    <span style="font-size:24px">🔥</span>
    <div>
      <div style="font-size:14px;color:var(--text-muted)">Или поддерживать стрик</div>
      <div style="font-size:22px;font-weight:700">${Math.ceil(xpToNext / 50)} дней</div>
    </div>
  </div>
</div></div>`;

dv.container.innerHTML = html;
```
