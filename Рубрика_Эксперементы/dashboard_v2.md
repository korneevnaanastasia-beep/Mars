---
cssclasses:
  - dashboard-1920
created: 21.05.2026
tags:
  - dashboard
  - book
  - writing
---

```dashboard
title: 📊 Проект Марсель
rows:
  - height: auto
    columns:
      - width: 12
        widget:
          type: heading
          text: 📊 Проект Марсель
          level: 1

  - height: auto
    columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'));
            const docs = dv.pages('"5-Персонажи"');
            const tp = dv.pages().where(p => p.file.name === 'TODO');
            let done = 0, words = 0, tt = 0, td = 0;
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              words += ct.split(/\s+/).filter(w => w.length > 0).length;
              if (ct.includes('**Конец')) done++;
            }
            if (tp.length > 0) {
              const tc = await dv.io.load(tp[0].file.path);
              const tk = tc.match(/\[[ x]\]/g) || [];
              tt = tk.length; td = tk.filter(t => t === '[x]').length;
            }
            const wordPct = Math.min(words / 50000 * 100, 100).toFixed(1);
            dv.container.innerHTML = '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px">' +
              '<div class="stat-card"><div class="stat-value" style="color:#4caf50">' + chs.length + '</div><div class="stat-label">Глав написано</div><div class="stat-sub">' + done + ' завершено · ' + (chs.length - done) + ' в работе</div></div>' +
              '<div class="stat-card"><div class="stat-value" style="color:#2196f3">' + words.toLocaleString() + '</div><div class="stat-label">Всего слов</div><div class="stat-sub">' + wordPct + '% от цели 50 000</div></div>' +
              '<div class="stat-card"><div class="stat-value" style="color:#9c27b0">' + docs.length + '</div><div class="stat-label">Персонажей</div><div class="stat-sub">в досье</div></div>' +
              '<div class="stat-card"><div class="stat-value" style="color:#ff9800">' + td + '/' + tt + '</div><div class="stat-label">Задач выполнено</div><div class="stat-sub">' + (tt > 0 ? Math.round(td/tt*100) : 0) + '% готово</div></div>' +
              '</div>';
            ```

  - height: auto
    columns:
      - width: 8
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            let bars = '<h3 style="margin:0 0 10px">Прогресс глав</h3>';
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              const w = ct.split(/\s+/).filter(x => x.length > 0).length;
              const end = ct.includes('**Конец');
              const m = ct.match(/^#{2,3}\s+(.+)$/m);
              const t = m ? m[1].trim() : c.file.name.replace('Глава_', 'Глава ');
              const pct = end ? 100 : Math.min(Math.floor(w / 2500 * 100), 95);
              const col = pct === 100 ? '#4caf50' : pct > 50 ? '#ff9800' : '#f44336';
              bars += '<div style="display:flex;align-items:center;gap:10px;padding:5px 0">' +
                '<span style="min-width:50px;font-weight:600;font-size:13px;color:var(--text-muted)">' + c.file.name.replace('Глава_', 'Гл.') + '</span>' +
                '<span style="flex:1;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">' + t + '</span>' +
                '<div style="position:relative;width:140px;height:22px;background:rgba(255,255,255,0.06);border-radius:11px;overflow:hidden;flex-shrink:0">' +
                '<div style="width:' + pct + '%;height:100%;background:' + col + ';border-radius:11px;transition:width 0.4s"></div>' +
                '<span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:600;color:#fff;text-shadow:0 1px 2px rgba(0,0,0,0.4)">' + pct + '% · ' + w + ' сл.</span></div></div>';
            }
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:14px;padding:16px 20px;height:100%">' + bars + '</div>';
            ```

      - width: 4
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'));
            let tw = 0, done = 0, eps = 0, aw = [];
            for (let c of chs) {
              const ct = await dv.io.load(c.file.path);
              const w = ct.split(/\s+/).filter(x => x.length > 0).length;
              tw += w; aw.push(w);
              if (ct.includes('**Конец')) done++;
              const e = ct.match(/Эпизод \d+/g); if (e) eps += e.length;
            }
            const avg = chs.length ? Math.round(tw / chs.length) : 0;
            const mn = aw.length ? Math.min(...aw) : 0;
            const mx = aw.length ? Math.max(...aw) : 0;
            const pgs = Math.round(tw / 250);
            const rows = [
              ['Завершено', done, '#4caf50'],
              ['В работе', chs.length - done, '#ff9800'],
              ['Среднее слов', avg.toLocaleString(), ''],
              ['Мин / Макс', mn + ' / ' + mx, ''],
              ['Страниц (~250)', pgs, ''],
              ['Эпизодов', eps, ''],
            ];
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:14px;padding:16px 20px;height:100%">' +
              '<h3 style="margin:0 0 10px">Статистика</h3>' +
              rows.map((r, i) => '<div style="display:flex;justify-content:space-between;padding:5px 8px;border-radius:4px;background:' + (i % 2 === 0 ? 'transparent' : 'rgba(255,255,255,0.03)') + '">' +
                '<span style="font-size:13px;color:var(--text-muted)">' + r[0] + '</span>' +
                '<span style="font-weight:600;font-size:14px' + (r[2] ? ';color:' + r[2] : '') + '">' + r[1] + '</span></div>').join('') + '</div>';
            ```

  - height: auto
    columns:
      - width: 12
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const docs = dv.pages('"5-Персонажи"').sort(p => p.file.name);
            if (docs.length === 0) { dv.paragraph('Файлы в папке 5-Персонажи/ не найдены.'); }

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

            function timeAgo(mt) {
              const now = dv.luxon.DateTime.now();
              const diffHours = now.diff(mt, 'hours').hours;
              if (diffHours < 1) return 'только что';
              if (diffHours < 24) return Math.round(diffHours) + ' ч. назад';
              if (diffHours < 48) return 'вчера';
              return mt.toFormat('dd MMM');
            }

            let rows = '';
            for (let i = 0; i < docs.length; i++) {
              const p = docs[i];
              const role = p.role || '—';
              const [rColor, rBg] = getRoleColor(role);
              const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
              const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.02)';
              rows += '<div style="display:contents">' +
                '<div style="padding:8px 14px;display:flex;align-items:center;gap:8px' + bg + '">' +
                  '<span style="width:8px;height:8px;border-radius:50%;background:' + rColor + ';flex-shrink:0"></span>' +
                  '<a class="internal-link" href="' + p.file.path + '" style="color:var(--interactive-accent);text-decoration:none;font-weight:500;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;display:block">' + p.file.name + '</a></div>' +
                '<div style="padding:8px 14px' + bg + '">' +
                  '<span class="badge" style="background:' + rBg + ';color:' + rColor + '">' + role + '</span></div>' +
                '<div style="padding:8px 14px;color:var(--text-muted);font-size:13px' + bg + '">' + (p.age || '—') + '</div>' +
                '<div style="padding:8px 14px;text-align:right;color:var(--text-muted);font-size:13px' + bg + '">' + timeAgo(mt) + '</div></div>';
            }

            dv.container.innerHTML = '<h3 style="margin:0 0 10px">Персонажи</h3>' +
              '<div style="display:grid;grid-template-columns:1.8fr 2.5fr 0.7fr 0.9fr;border-radius:12px;overflow:hidden;background:var(--background-secondary)">' +
                '<div style="display:contents">' +
                  '<div style="padding:8px 14px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Персонаж</div>' +
                  '<div style="padding:8px 14px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Роль</div>' +
                  '<div style="padding:8px 14px;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Возраст</div>' +
                  '<div style="padding:8px 14px;text-align:right;font-size:11px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px">Изменён</div></div>' +
                rows +
              '</div>';
            ```

  - height: auto
    columns:
      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const chs = dv.pages().where(p => p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап')).sort(p => p.file.name);
            const chapterData = [];
            let headingIssues = [], formatChapters = [];
            for (let ch of chs) {
              const ct = await dv.io.load(ch.file.path);
              const lines = ct.split('\n');
              const hdgs = [];
              let epFormatAllGood = true;
              for (let j = 0; j < lines.length; j++) {
                const line = lines[j];
                const m = line.match(/^(#{2,3})\s+(.+)/);
                if (m) hdgs.push(m[2]);
              }
              if (hdgs.length === 0) continue;
              // Check heading structure
              const first = lines[0];
              if (!/^#{2,3}\s/.test(first)) headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': нет ## у названия');
              else {
                const lvl = first.match(/^(#{2,3})/)[1];
                if (lvl !== '##') headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': ' + lvl + ' вместо ##');
              }
              const eps = lines.filter(l => /^#{2,3}\s/.test(l)).slice(1);
              const ul = [...new Set(eps.map(l => l.match(/^(#{2,3})/)[1]))];
              if (ul.length > 1) headingIssues.push(ch.file.name.replace('Глава_', 'Глава ') + ': эпизоды на ' + ul.join('/'));
              // Check episode name format
              const epsOnly = hdgs.slice(1);
              for (let e of epsOnly) {
                if (!/^Эпизод \d+\s\/\s/.test(e.trim())) {
                  epFormatAllGood = false;
                  break;
                }
              }
              if (!epFormatAllGood) formatChapters.push(ch.file.name.replace('Глава_', ''));
              chapterData.push({ name: ch.file.name, title: hdgs[0], scenes: hdgs.slice(1) });
            }
            let html = '<h3 style="margin:0 0 10px">Эпизоды по главам</h3>' +
              '<div style="font-size:13px;color:var(--text-muted);margin-bottom:10px">Всего эпизодов: <strong style="color:var(--text-normal)">' + chapterData.reduce((s,ch) => s + ch.scenes.length, 0) + '</strong></div>';

            if (headingIssues.length > 0) {
              html += headingIssues.map(h => '<div class="warning-block" style="background:rgba(244,67,54,0.1);color:#f44336;margin:2px 0">⚠️ ' + h + '</div>').join('');
            }
            if (formatChapters.length > 0) {
              html += '<div class="warning-block" style="background:rgba(255,152,0,0.1);color:#ff9800;margin:4px 0">⚠️ Главы: ' + formatChapters.join(',') + ' — названия эпизодов не соответствуют формату «Эпизод N / Название»</div>';
            }

            for (let ch of chapterData) {
              html += '<div style="font-weight:600;font-size:14px;color:var(--interactive-accent);margin:8px 0 4px;padding-left:10px;border-left:3px solid var(--interactive-accent)">' + ch.name.replace('Глава_', 'Глава ') + ': ' + ch.title + '</div>';
              for (let s of ch.scenes) {
                html += '<div style="padding:2px 0 2px 20px;font-size:13px;color:var(--text-normal)">— ' + s + '</div>';
              }
            }
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:14px;padding:16px 20px;height:100%">' + html + '</div>';
            ```

      - width: 6
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const todoPages = dv.pages().where(p => p.file.name === 'TODO');
            if (todoPages.length === 0) { dv.paragraph('Файл TODO.md не найден.'); }
            const content = await dv.io.load(todoPages[0].file.path);
            const lines = content.split('\n');
            let currentGroup = '';
            let tasks = [];
            for (const line of lines) {
              if (!line.trim()) continue;
              const groupMatch = line.match(/^-\s+(.+?)(?::)?$/);
              const taskMatch = line.match(/^[\t ]*-?\s*\[([ x])\]\s+(.+)/);
              const topTaskMatch = line.match(/^-\s+\[([ x])\]\s+(.+)/);
              if (groupMatch && !line.includes('[ ]') && !line.includes('[x]')) {
                currentGroup = groupMatch[1].trim();
                continue;
              }
              if (topTaskMatch) {
                tasks.push({ group: currentGroup || 'Основное', done: topTaskMatch[1] === 'x', text: topTaskMatch[2] });
                continue;
              }
              if (taskMatch) {
                tasks.push({ group: currentGroup || 'Основное', done: taskMatch[1] === 'x', text: taskMatch[2] });
              }
            }
            const total = tasks.length;
            const completed = tasks.filter(t => t.done).length;
            const active = tasks.filter(t => !t.done);
            const groups = [...new Set(tasks.map(t => t.group))];
            const grouped = {};
            for (const t of active) {
              if (!grouped[t.group]) grouped[t.group] = [];
              grouped[t.group].push(t.text);
            }
            const color = total > 0 ? (completed === total ? '#4caf50' : '#ff9800') : '#f44336';

            let html = '<h3 style="margin:0 0 10px">Задачи</h3><div style="display:flex;gap:14px;align-items:start">';
            html += '<div style="flex:0 0 120px;text-align:center;background:var(--background-primary);border-radius:12px;padding:14px">' +
              '<div style="position:relative;width:90px;height:90px;margin:0 auto 8px">' +
                '<div style="position:absolute;inset:0;border-radius:50%;background:conic-gradient(' + color + ' 0deg ' + (completed/total*360) + 'deg, rgba(255,255,255,0.06) ' + (completed/total*360) + 'deg 360deg)"></div>' +
                '<div style="position:absolute;top:8px;left:8px;right:8px;bottom:8px;border-radius:50%;background:var(--background-primary)"></div>' +
                '<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center">' +
                  '<div style="font-size:22px;font-weight:700;line-height:1.1">' + completed + '/' + total + '</div>' +
                  '<div style="font-size:9px;color:var(--text-muted);text-transform:uppercase">готово</div></div></div>';
            if (active.length > 0) html += '<div style="font-size:11px;color:' + color + ';font-weight:600">' + active.length + ' активных</div>';
            else html += '<div style="font-size:11px;color:#4caf50;font-weight:600">✅ Все готово</div>';
            html += '</div>';

            html += '<div style="flex:1">';
            if (active.length > 0) {
              for (const [group, items] of Object.entries(grouped)) {
                html += '<div style="font-size:10px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:0.5px;margin:4px 0 2px">' + group + '</div>';
                for (const item of items) {
                  html += '<div style="display:flex;align-items:center;gap:6px;padding:3px 0;font-size:12px;border-bottom:1px solid rgba(255,255,255,0.04)">' +
                    '<span style="width:8px;height:8px;border:2px solid ' + color + ';border-radius:50%;flex-shrink:0"></span>' +
                    '<span style="color:var(--text-normal);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + item + '</span></div>';
                }
              }
            } else {
              html += '<div style="font-size:13px;color:#4caf50;font-weight:600">✅ Все задачи выполнены</div>';
            }
            html += '</div></div>';
            dv.container.innerHTML = '<div style="background:var(--background-secondary);border-radius:14px;padding:16px 20px;height:100%">' + html + '</div>';
            ```

  - height: auto
    columns:
      - width: 8
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
              if (diffHours < 2) return { text: '1 ч. назад', color: '#8bc34a' };
              if (diffHours < 24) return { text: Math.round(diffHours) + ' ч. назад', color: '#ff9800' };
              if (diffHours < 48) return { text: 'вчера', color: '#ff5722' };
              return { text: mt.toFormat('dd.MM.yy'), color: '#9e9e9e' };
            }

            let list = '';
            for (let i = 0; i < files.length; i++) {
              const p = files[i];
              const mt = dv.luxon.DateTime.fromMillis(p.file.mtime.ts);
              const ta = timeAgo(mt);
              const icon = getFolderIcon(p.file.path);
              const folder = p.file.folder || '/';
              const bg = i % 2 === 0 ? '' : ';background:rgba(255,255,255,0.02)';
              list += '<div style="display:flex;align-items:center;gap:10px;padding:6px 8px' + bg + ';border-radius:4px">' +
                '<span style="font-size:16px;flex-shrink:0;width:20px;text-align:center">' + icon + '</span>' +
                '<div style="flex:1;min-width:0">' +
                  '<a class="internal-link" href="' + p.file.path + '" style="color:var(--interactive-accent);text-decoration:none;font-size:13px;font-weight:500;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">' + p.file.name + '</a>' +
                  '<div style="font-size:11px;color:var(--text-muted)">' + folder + '</div></div>' +
                '<span style="font-size:12px;font-weight:600;color:' + ta.color + ';flex-shrink:0">' + ta.text + '</span></div>';
            }
            dv.container.innerHTML = '<h3 style="margin:0 0 10px">Последние изменения</h3>' +
              '<div style="background:var(--background-secondary);border-radius:14px;padding:12px 16px">' + list + '</div>';
            ```

      - width: 4
        widget:
          type: markdown
          content: |
            ```dataviewjs
            const all = dv.pages().sort(p => p.file.name);
            let chs = '', prs = '';
            for (let p of all) {
              if (p.file.name.startsWith('Глава_') && !p.file.name.includes('правки') && !p.file.name.includes('бэкап'))
                chs += '<a class="internal-link" style="display:inline-block;background:rgba(255,255,255,0.04);border-radius:8px;padding:4px 10px;font-size:12px;color:var(--interactive-accent);text-decoration:none;transition:all 0.15s" href="' + p.file.path + '">' + p.file.name.replace('Глава_', 'Глава ') + '</a>';
              if (['project', 'TODO', 'roadmap', 'ПЛАН_РАБОТЫ', 'анализ', 'вектор_сюжета'].includes(p.file.name))
                prs += '<a class="internal-link" style="display:inline-block;background:rgba(255,255,255,0.04);border-radius:8px;padding:4px 10px;font-size:12px;color:var(--interactive-accent);text-decoration:none;transition:all 0.15s" href="' + p.file.path + '">' + p.file.name + '</a>';
            }
            dv.container.innerHTML = '<h3 style="margin:0 0 10px">Быстрые ссылки</h3>' +
              '<div style="background:var(--background-secondary);border-radius:14px;padding:14px 16px;height:100%">' +
              (chs ? '<div style="font-size:10px;font-weight:600;color:var(--text-muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">Главы</div><div style="display:flex;flex-wrap:wrap;gap:4px;margin-bottom:12px">' + chs + '</div>' : '') +
              (prs ? '<div style="font-size:10px;font-weight:600;color:var(--text-muted);margin-bottom:6px;text-transform:uppercase;letter-spacing:0.5px">Проекты</div><div style="display:flex;flex-wrap:wrap;gap:4px">' + prs + '</div>' : '') +
              '</div>';
            ```
```
