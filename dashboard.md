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

```dashboard
title: Дашборд романа
rows:
  - columns:
      - width: 12
        widget:
          type: heading
          text: Сводка
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            const docs = dv.pages('"5-Персонажи"');
            let total = chs.length, done = 0, words = 0;
            let headingIssues = [];
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              words += ct.split(/\s+/).filter(w => w.length > 0).length;
              if (ct.includes('**Конец')) done++;
              // Check heading format consistency
              const lines = ct.split('\n');
              const first = lines[0];
              if (!/^#{2,3}\s/.test(first)) {
                headingIssues.push(c.file.name.replace('Глава_', 'Глава ') + ': нет ## у названия');
              } else {
                const lvl = first.match(/^(#{2,3})/)[1];
                if (lvl !== '##') headingIssues.push(c.file.name.replace('Глава_', 'Глава ') + ': ' + lvl + ' вместо ##');
              }
              const eps = lines.filter(l => /^#{2,3}\s/.test(l)).slice(1);
              const ul = [...new Set(eps.map(l => l.match(/^(#{2,3})/)[1]))];
              if (ul.length > 1) headingIssues.push(c.file.name.replace('Глава_', 'Глава ') + ': эпизоды на ' + ul.join('/'));
            }
            const hasWarning = headingIssues.length > 0;
            const pct = Math.min(words / 50000 * 100, 100);
            dv.container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">' +
              [
                { v: total, l: 'Глав написано', c: '#4caf50', s: done + ' завершено' },
                { v: done, l: 'Глав завершено', c: '#2196f3', s: total - done + ' в работе' },
                { v: words.toLocaleString(), l: 'Всего слов', c: '#ff9800', s: pct.toFixed(1) + '% от цели 50 000' },
                { v: docs.length, l: 'Персонажей', c: '#9c27b0', s: 'в досье' },
              ].map(c => '<div style="background:var(--background-secondary);border-radius:12px;padding:22px 20px;border-left:4px solid ' + c.c + ';position:relative">' +
                '<div style="font-size:38px;font-weight:700;line-height:1.2">' + c.v + '</div>' +
                '<div style="font-size:15px;color:var(--text-muted);margin-top:4px">' + c.l + '</div>' +
                '<div style="font-size:13px;color:var(--text-muted);margin-top:6px">' + c.s + '</div>' +
                '<div style="position:absolute;top:12px;right:12px;width:10px;height:10px;border-radius:50%;background:' + c.c + ';opacity:0.6"></div>' +
                '</div>').join('') + '</div>';
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Прогресс глав
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            let done = 0;
            for (let c of chs) { const ct = await dv.io.load(c.file.path); if (ct.includes('**Конец')) done++; }
            const total = chs.length, inProgress = total - done;
            const dp = total > 0 ? done / total : 0, ip = total > 0 ? inProgress / total : 0;
            let bars = '';
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              const w = ct.split(/\s+/).filter(x => x.length > 0).length;
              const end = ct.includes('**Конец');
              const m = ct.match(/^#{2,3}\s+(.+)$/m);
              const t = m ? m[1].trim() : c.file.name;
              const pct = end ? 100 : Math.min(Math.floor(w / 2500 * 100), 95);
              const col = pct === 100 ? '#4caf50' : pct > 50 ? '#ff9800' : '#f44336';
              bars += '<div style="display:flex;align-items:center;gap:8px">' +
                '<span style="min-width:28px;font-weight:700;font-size:14px;color:var(--text-muted)">' + c.file.name.replace('Глава_', '') + '</span>' +
                '<span style="flex:1;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0">' + t + '</span>' +
                '<span style="padding:2px 8px;border-radius:6px;font-size:13px;font-weight:700;background:' + col + ';color:#fff;min-width:40px;text-align:center">' + pct + '%</span>' +
                '<span style="font-size:13px;color:var(--text-muted);min-width:60px;text-align:right">' + w + ' сл.</span></div>';
            }
            const dg = dp * 360, og = (dp + ip) * 360;
            dv.container.innerHTML = '<style>@keyframes chartPop{from{transform:scale(0.6);opacity:0}}@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}}</style>' +
              '<div style="display:flex;gap:20px;align-items:stretch">' +
              '<div style="flex:0.1 0 220px;display:flex;flex-direction:column;align-items:center;gap:14px;background:var(--background-secondary);border-radius:14px;padding:20px;animation:chartPop 0.5s ease-out">' +
                '<div style="position:relative;width:130px;height:130px;flex-shrink:0">' +
                  '<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(#4caf50 0deg ' + dg + 'deg, #ff9800 ' + dg + 'deg ' + og + 'deg, rgba(255,255,255,0.06) ' + og + 'deg 360deg);box-shadow:0 4px 24px rgba(0,0,0,0.2)"></div>' +
                  '<div style="position:absolute;top:14px;left:14px;right:14px;bottom:14px;border-radius:50%;background:var(--background-secondary)"></div>' +
                  '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">' +
                    '<div style="font-size:32px;font-weight:700;line-height:1.1">' + done + '/' + total + '</div>' +
                    '<div style="font-size:10px;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">готово</div></div></div>' +
                '<div style="display:flex;gap:8px;width:100%">' +
                  '<div style="flex:1;display:flex;align-items:center;gap:6px;padding:6px 10px;border-radius:8px;background:rgba(76,175,80,0.12)">' +
                    '<span style="width:8px;height:8px;border-radius:50%;background:#4caf50;flex-shrink:0"></span>' +
                    '<span style="font-size:11px;color:var(--text-muted)">Готово</span>' +
                    '<span style="font-weight:700;font-size:13px;margin-left:auto">' + done + '</span></div>' +
                  '<div style="flex:1;display:flex;align-items:center;gap:6px;padding:6px 10px;border-radius:8px;background:rgba(255,152,0,0.12)">' +
                    '<span style="width:8px;height:8px;border-radius:50%;background:#ff9800;flex-shrink:0"></span>' +
                    '<span style="font-size:11px;color:var(--text-muted)">В работе</span>' +
                    '<span style="font-weight:700;font-size:13px;margin-left:auto">' + inProgress + '</span></div></div></div>' +
              '<div style="flex:1;display:flex;flex-direction:column;gap:8px;animation:fadeUp 0.5s ease-out 0.15s both">' + bars + '</div></div>';
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Статистика проекта
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'));
            const docs = dv.pages('"5-Персонажи"');
            const tp = dv.pages().where(p => p.file.name === 'TODO');
            let tt = 0, td = 0;
            if (tp.length > 0) {
              const tc = await dv.io.load(tp[0].file.path);
              const tk = tc.match(/\[[ x]\]/g) || [];
              tt = tk.length; td = tk.filter(t => t === '[x]').length;
            }
            let total = chs.length, tw = 0, done = 0, aw = [], eps = 0;
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              const w = ct.split(/\s+/).filter(x => x.length > 0).length;
              tw += w; aw.push(w);
              if (ct.includes('**Конец')) done++;
              const e = ct.match(/Эпизод \d+/g); if (e) eps += e.length;
            }
            const dw = aw.length > 1 ? aw.slice(0, -1).reduce((a, b) => a + b, 0) : 0;
            const avg = total ? Math.round(tw / total) : 0;
            const mn = aw.length ? Math.min(...aw) : 0;
            const mx = aw.length ? Math.max(...aw) : 0;
            const pgs = Math.round(tw / 250);
            const bp = Math.min(tw / 50000 * 100, 100);
            const rows = [
              ['Написано глав', total, ''], ['Завершено', done, '#4caf50'], ['В работе глав', total - done, '#ff9800'],
              ['Всего слов', tw.toLocaleString(), ''], ['Слов в готовых', dw.toLocaleString(), ''],
              ['Среднее слов', avg.toLocaleString(), ''], ['Мин / Макс слов', mn + ' / ' + mx, ''],
              ['Страниц (~250 сл.)', pgs, ''], ['Эпизодов', eps, ''], ['Персонажей', docs.length, ''],
              ['Задач сделано', td + ' / ' + tt, ''], ['Прогресс к цели 50K', bp.toFixed(1) + '%', bp > 50 ? '#4caf50' : '#ff9800'],
            ];
            dv.container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(2,1fr);gap:2px 32px">' +
              rows.map((r, i) => '<div style="display:flex;justify-content:space-between;padding:7px 12px;border-radius:4px;background:' + (i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.03)') + '">' +
                '<span style="color:var(--text-muted);font-size:14px">' + r[0] + '</span>' +
                '<span style="font-weight:600;font-size:15px' + (r[2] ? ';color:' + r[2] : '') + '">' + r[1] + '</span></div>').join('') + '</div>';
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Эпизоды по главам
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            let allScenes = []; let headingIssues = []; let formatChapters = [];
            const chapterData = [];
            for (let ch of chs) {
              const ct = await dv.io.load(ch.file.path);
              const lines = ct.split('\n');
              const hdgs = [];
              for (let line of lines) {
                const m = line.match(/^(#{2,3})\s+(.+)/);
                if (m) hdgs.push(m[2]);
              }
              if (hdgs.length === 0) continue;
              chapterData.push({ name: ch.file.name, title: hdgs[0], scenes: hdgs.slice(1) });
              allScenes.push(...hdgs.slice(1));
              // Heading format check
              const first = lines[0];
              if (!/^#{2,3}\s/.test(first)) {
                headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': нет ## у названия');
              } else {
                const lvl = first.match(/^(#{2,3})/)[1];
                if (lvl !== '##') headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': ' + lvl + ' вместо ##');
              }
              const eps = lines.filter(l => /^#{2,3}\s/.test(l)).slice(1);
              const ul = [...new Set(eps.map(l => l.match(/^(#{2,3})/)[1]))];
              if (ul.length > 1) headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': эпизоды на ' + ul.join('/'));
              // Check episode name format: "Эпизод N / Name"
              const eNames = hdgs.slice(1);
              const badEps = eNames.filter(h => !/^Эпизод \d+ \/ /.test(h));
              if (badEps.length > 0) formatChapters.push(ch.file.name.replace('Глава_', ''));
            }
            let html = '<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px">' +
              '<div style="font-size:14px;color:var(--text-muted);margin-bottom:12px">Всего эпизодов: <strong style="color:var(--text-normal)">' + allScenes.length + '</strong></div>' +
              (headingIssues.length > 0 ? '<div style="font-size:12px;color:#f44336;margin-bottom:6px;padding:8px 12px;background:rgba(244,67,54,0.08);border-radius:8px">⚠️ ' + headingIssues.join(', ') + '</div>' : '') +
              (formatChapters.length > 0 ? '<div style="font-size:12px;color:#ff9800;padding:8px 12px;background:rgba(255,152,0,0.08);border-radius:8px">⚠️ Главы: ' + formatChapters.join(', ') + ' — названия эпизодов не соответствуют формату «Эпизод N / Название»</div>' : '');
            for (let ch of chapterData) {
              html += '<div style="font-weight:600;font-size:15px;color:var(--interactive-accent);margin:12px 0 6px;padding-left:12px;border-left:3px solid var(--interactive-accent)">' + ch.name.replace('Глава_', 'Глава ') + ': ' + ch.title + '</div>';
              if (ch.scenes.length > 0) {
                for (let s of ch.scenes) {
                  html += '<div style="padding:3px 0 3px 24px;font-size:14px;color:var(--text-normal)">— ' + s + '</div>';
                }
              } else {
                html += '<div style="padding:3px 0 3px 24px;font-size:12px;color:var(--text-muted);font-style:italic">— нет подзаголовков</div>';
              }
            }
            html += '</div>';
            dv.container.innerHTML = html;
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Персонажи
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const docs = dv.pages('"5-Персонажи"').sort(p => p.file.name);

            if (docs.length === 0) { dv.paragraph('Файлы в папке 5-Персонажи/ не найдены.'); }

            // role colors
            const roleColors = {
              'Главный герой': ['#9c27b0', 'rgba(156,39,176,0.15)'],
              'Отец': ['#455a64', 'rgba(69,90,100,0.15)'],
              'Лучший друг': ['#e91e63', 'rgba(233,30,99,0.15)'],
              'Технарь': ['#00bcd4', 'rgba(0,188,212,0.15)'],
              'Тактик': ['#ff5722', 'rgba(255,87,34,0.15)'],
              'Аналитик': ['#607d8b', 'rgba(96,125,139,0.15)'],
              'Боец': ['#f44336', 'rgba(244,67,54,0.15)'],
            };
            const defaultColor = ['#795548', 'rgba(121,85,72,0.15)'];

            function getRoleColor(role) {
              if (!role) return defaultColor;
              for (const [key, val] of Object.entries(roleColors)) {
                if (role.toLowerCase().includes(key.toLowerCase().slice(0, 4))) return val;
              }
              return defaultColor;
            }

            const hdrC = '<div style="padding:10px 16px;font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">';
            const hdrR = '<div style="padding:10px 16px;font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;text-align:right">';

            let rows = '';
            for (let i = 0; i < docs.length; i++) {
              const p = docs[i];
              const role = p.role || '—';
              const [rColor, rBg] = getRoleColor(role);
              const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
              const now = dv.luxon.DateTime.now();
              const diffHours = now.diff(mt, 'hours').hours;
              let timeStr;
              if (diffHours < 1) timeStr = 'только что';
              else if (diffHours < 24) timeStr = Math.round(diffHours) + ' ч. назад';
              else if (diffHours < 48) timeStr = 'вчера';
              else timeStr = mt.toFormat('dd MMM');
              const bg = i % 2 === 0 ? '' : ';background:var(--background-primary)';
              rows += '<div style="display:contents">' +
                '<div style="padding:10px 16px;display:flex;align-items:center;gap:10px' + bg + '">' +
                  '<span style="width:6px;height:6px;border-radius:50%;background:' + rColor + ';flex-shrink:0"></span>' +
                  '<a class="internal-link" href="' + p.file.path + '" style="color:var(--interactive-accent);text-decoration:none;font-weight:500;font-size:15px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block">' + p.file.name + '</a></div>' +
                '<div style="padding:10px 16px;overflow:hidden' + bg + '">' +
                  '<span style="display:inline-block;font-size:12px;font-weight:600;padding:2px 10px;border-radius:10px;background:' + rBg + ';color:' + rColor + ';white-space:nowrap">' + role + '</span></div>' +
                '<div style="padding:10px 16px;color:var(--text-muted);font-size:14px' + bg + '">' + (p.age || '—') + '</div>' +
                '<div style="padding:10px 16px;text-align:right;color:var(--text-muted);font-size:14px' + bg + '">' + timeStr + '</div></div>';
            }

            dv.container.innerHTML = '<style>' +
              '.char-table { display:grid; grid-template-columns:0.5fr 3.75fr 0.4fr 0.35fr; border-radius:12px; overflow:hidden; background:var(--background-secondary); }' +
              '.char-table > div { border-top:1px solid rgba(255,255,255,0.04); }' +
              '.char-table .header-row > div { border-top:none; }' +
              '</style>' +
              '<div class="char-table">' +
                '<div class="header-row" style="display:contents">' +
                  hdrC + 'Персонаж</div>' +
                  hdrC + 'Роль</div>' +
                  hdrC + 'Возраст</div>' +
                  hdrR + 'Изменён</div></div>' +
                rows +
              '</div>';
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Задачи
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const todoPages = dv.pages().where(p => p.file.name === 'TODO');
            if (todoPages.length === 0) { dv.paragraph('Файл TODO.md не найден.'); }

            const content = await dv.io.load(todoPages[0].file.path);
            const lines = content.split('\n');

            // Parse tasks: capture main tasks and subtasks
            let currentGroup = '';
            let tasks = [];

            for (const line of lines) {
              const groupMatch = line.match(/^-\s+(.+?)(?::)?$/);
              const taskMatch = line.match(/^[\t ]*-?\s*\[([ x])\]\s+(.+)/);
              const topTaskMatch = line.match(/^-\s+\[([ x])\]\s+(.+)/);

              if (!line.trim()) continue;

              // Check if this is a group header (no checkbox)
              if (groupMatch && !line.includes('[ ]') && !line.includes('[x]')) {
                currentGroup = groupMatch[1].trim();
                continue;
              }

              // Top-level task
              if (topTaskMatch) {
                tasks.push({
                  group: 'Основное',
                  done: topTaskMatch[1] === 'x',
                  text: topTaskMatch[2]
                });
                continue;
              }

              // Subtask (tab-indented)
              if (taskMatch) {
                tasks.push({
                  group: currentGroup || 'Основное',
                  done: taskMatch[1] === 'x',
                  text: taskMatch[2]
                });
              }
            }

            const total = tasks.length;
            const completed = tasks.filter(t => t.done).length;
            const active = tasks.filter(t => !t.done);
            const groups = [...new Set(tasks.map(t => t.group))];

            // Group active tasks
            const grouped = {};
            for (const t of active) {
              if (!grouped[t.group]) grouped[t.group] = [];
              grouped[t.group].push(t.text);
            }

            const color = total > 0 ? (completed === total ? '#4caf50' : '#ff9800') : '#f44336';

            let html = '<div style="display:flex;gap:16px;align-items:start">';
            // Summary card
            html += '<div style="flex:0 0 280px;background:var(--background-secondary);border-radius:14px;padding:20px;text-align:center">' +
              '<div style="position:relative;width:100px;height:100px;margin:0 auto 12px">' +
                '<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(' + color + ' 0deg ' + (completed/total*360) + 'deg, rgba(255,255,255,0.06) ' + (completed/total*360) + 'deg 360deg)"></div>' +
                '<div style="position:absolute;top:10px;left:10px;right:10px;bottom:10px;border-radius:50%;background:var(--background-secondary)"></div>' +
                '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">' +
                  '<div style="font-size:24px;font-weight:700;line-height:1.1">' + completed + '/' + total + '</div>' +
                  '<div style="font-size:10px;color:var(--text-muted);text-transform:uppercase">готово</div></div></div>';

            if (active.length > 0) {
              html += '<div style="text-align:left">';
              for (const [group, items] of Object.entries(grouped)) {
                html += '<div style="font-size:10px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin:8px 0 4px">' + group + '</div>';
                for (const item of items) {
                  html += '<div style="display:flex;align-items:center;gap:6px;padding:4px 0;font-size:12px">' +
                    '<span style="width:14px;height:14px;border:2px solid ' + color + ';border-radius:50%;flex-shrink:0"></span>' +
                    '<span style="color:var(--text-normal)">' + item + '</span></div>';
                }
              }
              html += '</div>';
            } else {
              html += '<div style="font-size:13px;color:#4caf50;font-weight:600">✅ Все задачи выполнены</div>';
            }
            html += '</div>';

            // All tasks list
            html += '<div style="flex:1;background:var(--background-secondary);border-radius:14px;padding:16px 20px">' +
              '<div style="font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:8px">Все задачи</div>';
            for (const t of tasks) {
              const icon = t.done ? '✅' : '⬜';
              html += '<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:13px">' +
                '<span>' + icon + '</span>' +
                '<span style="' + (t.done ? 'text-decoration:line-through;color:var(--text-muted)' : 'color:var(--text-normal)') + '">' + t.text + '</span>' +
                '<span style="margin-left:auto;font-size:10px;color:var(--text-muted);padding:1px 8px;border-radius:4px;background:rgba(255,255,255,0.05)">' + t.group + '</span></div>';
            }
            html += '</div></div>';

            dv.container.innerHTML = html;
            ```
  - columns:
      - width: 6
        widget:
          type: heading
          text: Идеи
          level: 3
      - width: 6
        widget:
          type: heading
          text: Связи персонажей
          level: 3
  - columns:
      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const f = dv.pages().where(p => p.file.name === 'идеи');
            if (f.length > 0) {
              const c = await dv.io.load(f[0].file.path);
              const lines = c.split('\n').filter(l => l.trim()).length;
              const q = (c.match(/\?/g) || []).length;
              dv.container.innerHTML = '<div style="display:flex;gap:12px">' +
                [{ v: lines, l: 'Строк', c: '#2196f3' }, { v: q, l: 'Вопросов', c: '#ff9800' }]
                  .map(x => '<div style="flex:1;background:var(--background-secondary);border-radius:10px;padding:14px;text-align:center">' +
                  '<div style="font-size:28px;font-weight:700;color:' + x.c + '">' + x.v + '</div>' +
                    '<div style="font-size:13px;color:var(--text-muted);margin-top:4px">' + x.l + '</div></div>').join('') + '</div>';
            }
            ```
      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            const docs = dv.pages('"5-Персонажи"').sort(p => p.file.name);
            function aliases(d) { const r = d.name || d.file.name.replace(/\(.*\)/, '').trim(); return [...new Set(r.split(/[()]+/).map(s => s.trim()).filter(s => s))]; }
            const tc = chs.length;
            const data = await Promise.all(docs.map(async (d) => {
              const a = aliases(d); let cnt = 0;
              for (let c of chs) { const ct = await dv.io.load(c.file.path); if (a.some(x => ct.includes(x))) cnt++; }
              return { p: d.file.path, n: d.file.name, cnt, tc };
            }));
            const t = docs.length, m = data.filter(r => r.cnt > 0).length;
            data.sort((a, b) => b.cnt - a.cnt);
            const hdrC = '<div style="padding:10px 16px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;background:rgba(255,255,255,0.04)">';
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:12px;overflow:hidden">' +
              '<div style="padding:14px 16px 6px;font-size:14px;color:var(--text-muted)">Упомянуто <strong style="color:var(--text-normal)">' + m + '/' + t + '</strong> персонажей</div>' +
              '<div style="display:grid;grid-template-columns:2fr 1fr 1fr">' +
                hdrC + 'Персонаж</div>' + hdrC + 'Глав</div>' + hdrC + 'Активность</div></div>' +
              data.map((r, i) => {
                const em = r.cnt === 0 ? '✕' : r.cnt > 3 ? '★★' : '★';
                const bp = r.tc > 0 ? Math.round(r.cnt / r.tc * 100) : 0;
                const bc = bp === 0 ? '#f44336' : bp > 50 ? '#4caf50' : '#ff9800';
                const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.02)';
                return '<div style="display:grid;grid-template-columns:2fr 1fr 1fr;border-top:1px solid rgba(255,255,255,0.04)' + bg + '">' +
                  '<div style="padding:10px 16px"><a class="internal-link" href="' + r.p + '" style="color:var(--interactive-accent);text-decoration:none;font-weight:500;font-size:14px">' + r.n + '</a></div>' +
                  '<div style="padding:10px 16px;text-align:center;color:var(--text-normal);font-size:14px">' + r.cnt + ' / ' + r.tc + '</div>' +
                  '<div style="padding:10px 16px;text-align:center"><span style="font-size:14px;color:var(--text-muted)">' + em + '</span> <span style="font-size:13px;color:' + bc + ';font-weight:600">' + bp + '%</span></div></div>';
              }).join('') + '</div></div>';
            ```
  - columns:
      - width: 12
        widget:
          type: heading
          text: Последние изменения
          level: 3
  - columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const files = dv.pages().sort(p => p.file.mtime, 'desc').limit(12);

            function getFolderIcon(path) {
              if (path.includes('4-Готово')) return '📖';
              if (path.includes('5-Персонажи')) return '👤';
              if (path.includes('6-Лор')) return '🌌';
              if (path.includes('3-Рецензии')) return '📝';
              if (path.includes('1-План')) return '📋';
              if (path.includes('0-Сырьё')) return '💡';
              if (path.includes('7-Промпты') || path.includes('8-Промпты')) return '🤖';
              if (path.includes('8-Материалы') || path.includes('9-Материалы')) return '🖼️';
              if (path.startsWith('dashboard')) return '📊';
              return '📄';
            }

            function timeAgo(mt) {
              const now = dv.luxon.DateTime.now();
              const diffHours = now.diff(mt, 'hours').hours;
              if (diffHours < 1) return { text: 'только что', color: '#4caf50' };
              if (diffHours < 2) return { text: '1 час назад', color: '#8bc34a' };
              if (diffHours < 24) return { text: Math.round(diffHours) + ' ч. назад', color: '#ff9800' };
              if (diffHours < 48) return { text: 'вчера', color: '#ff5722' };
              if (diffHours < 168) return { text: Math.round(diffHours / 24) + ' дн. назад', color: '#f44336' };
              return { text: mt.toFormat('dd.MM.yy'), color: '#9e9e9e' };
            }

            let html = '<div style="background:var(--background-secondary);border-radius:12px;overflow:hidden">';
            for (let i = 0; i < files.length; i++) {
              const p = files[i];
              const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
              const ta = timeAgo(mt);
              const icon = getFolderIcon(p.file.path);
              const folder = p.file.folder || '/';
              const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.03)';
              const border = i === 0 ? '' : ';border-top:1px solid rgba(255,255,255,0.05)';
              html += '<div style="display:flex;align-items:center;gap:10px;padding:10px 16px' + bg + border + '">' +
                '<span style="font-size:16px;flex-shrink:0;width:20px;text-align:center">' + icon + '</span>' +
                '<div style="flex:1;min-width:0;line-height:1.4">' +
                  '<a class="internal-link" href="' + p.file.path + '" style="color:var(--interactive-accent);text-decoration:none;font-size:14px;font-weight:500;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + p.file.name + '</a>' +
                  '<span style="font-size:11px;color:var(--text-muted)">' + folder + '</span>' +
                '</div>' +
                '<span style="font-size:13px;font-weight:600;color:' + ta.color + ';flex-shrink:0;text-align:right;white-space:nowrap">' + ta.text + '</span></div>';
            }
            html += '</div>';
            dv.container.innerHTML = html;
            ```
  - columns:
      - width: 6
        widget:
          type: heading
          text: Статистика хранилища
          level: 3
      - width: 6
        widget:
          type: heading
          text: Быстрые ссылки
          level: 3
  - columns:
      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const all = dv.pages();
            const stats = [
              ['Всего заметок', all.length],
              ['Из них глав', all.where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).length],
              ['Персонажей', dv.pages('"5-Персонажи"').length],
              ['Рецензий', dv.pages('"3-Рецензии"').length],
              ['Изображений', app.vault.getFiles().filter(f => /\.(jpg|jpeg|png|webp|gif)$/i.test(f.path)).length],
              ['Папок', new Set(all.map(p => p.file.folder).filter(f => f && f !== '/')).size],
            ];
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px">' +
              '<div style="display:flex;flex-direction:column;gap:2px">' +
              stats.map((s, i) => '<div style="display:flex;justify-content:space-between;padding:7px 12px;border-radius:4px;background:' + (i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.03)') + '">' +
                '<span style="color:var(--text-muted);font-size:14px">' + s[0] + '</span>' +
                '<span style="font-weight:600;font-size:15px">' + s[1] + '</span></div>').join('') + '</div></div>';
            ```
      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const all = dv.pages().sort(p => p.file.name);
            let chs = '', prs = '';
            for (let p of all) {
              if (p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
                chs += '<a class="internal-link" style="display:inline-block;background:var(--background-primary);border-radius:6px;padding:4px 10px;font-size:13px;color:var(--interactive-accent);text-decoration:none" href="' + p.file.path + '">' + p.file.name + '</a>';
              if (['project', 'TODO', 'идеи', 'roadmap', 'prompt_structure', 'обучения_Марселя', 'ПЛАН_РАБОТЫ'].includes(p.file.name))
                prs += '<a class="internal-link" style="display:inline-block;background:var(--background-primary);border-radius:6px;padding:4px 10px;font-size:13px;color:var(--interactive-accent);text-decoration:none" href="' + p.file.path + '">' + p.file.name + '</a>';
            }
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:12px;padding:16px 20px">' +
              (chs ? '<div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px">Главы</div><div style="display:flex;flex-wrap:wrap;gap:6px;margin-bottom:16px">' + chs + '</div>' : '') +
              (prs ? '<div style="font-size:11px;font-weight:600;color:var(--text-muted);margin-bottom:8px;text-transform:uppercase;letter-spacing:0.5px">Проекты</div><div style="display:flex;flex-wrap:wrap;gap:6px">' + prs + '</div>' : '') +
              '</div>';
            ```
```
