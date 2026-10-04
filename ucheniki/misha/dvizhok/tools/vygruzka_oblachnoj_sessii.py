#!/usr/bin/env python3
"""Выгрузка транскрипта облачной сессии (jsonl) в markdown: реплики владельца дословно (включая вложения-файлы и
сообщения посреди хода), ответы Claude (текст + SendUserMessage), вызовы инструментов — одной строкой.
Запуск: python3 vygruzka.py <session.jsonl> <out.md>"""
import json, re, sys, datetime
SR = re.compile(r'<system-reminder>.*?</system-reminder>', re.S)
def t(ts):
    d = datetime.datetime.fromisoformat(ts.replace('Z', '+00:00')) + datetime.timedelta(hours=3)
    return d.strftime('%d.%m %H:%M')
def clean(x): return SR.sub('', x).strip()
out = []; n_owner = 0
for line in open(sys.argv[1]):
    o = json.loads(line); ty = o.get('type'); ts = o.get('timestamp', '')
    if ty == 'user':
        if o.get('isMeta'): continue
        c = o['message']['content']
        if isinstance(c, str): c = [{'type': 'text', 'text': c}]
        texts = []; imgs = 0
        for b in c:
            if b.get('type') == 'text':
                tx = b['text']
                if tx.startswith('Base directory for this skill') or tx.startswith('Called the Read tool'): continue
                tx = clean(tx)
                if tx: texts.append(tx)
            elif b.get('type') == 'image': imgs += 1
        if texts or imgs:
            n_owner += 1
            out.append(f'\n---\n## 🟦 Владелец · {t(ts)}\n')
            out += texts
            if imgs: out.append(f'*[изображений: {imgs}]*')
    elif ty == 'attachment':
        a = o.get('attachment', {})
        if a.get('type') == 'file':
            f = a['content'].get('file', {})
            out.append(f'\n**Вложение-файл** `{f.get("filePath","").split("/")[-1]}` (дословно):\n\n> ' + f.get('content', '').replace('\n', '\n> '))
        elif a.get('type') == 'queued_command':
            pr = a.get('prompt', [])
            if isinstance(pr, str): pr = [{'type': 'text', 'text': pr}]
            tx = ' '.join(clean(p['text']) for p in pr if isinstance(p, dict) and p.get('type') == 'text').strip()
            nimg = sum(1 for p in pr if isinstance(p, dict) and p.get('type') == 'image')
            if nimg and not tx: tx = f'*[изображений: {nimg}]*'
            if tx.startswith('<agent-message'):
                out.append(f'\n### 🟪 Отчёт субагента · {t(ts)}\n\n' + re.sub(r'</?agent-message[^>]*>', '', tx).strip())
            elif tx:
                n_owner += 1; out.append(f'\n---\n## 🟦 Владелец (посреди хода) · {t(ts)}\n\n{tx}')
        elif a.get('type') == 'inlined_image_paths':
            out.append(f'*изображения сохранены: {a.get("paths") or a}*')
    elif ty == 'assistant':
        for b in o['message'].get('content', []):
            if b.get('type') == 'text' and b['text'].strip():
                out.append(f'\n### 🟧 Claude · {t(ts)}\n\n' + b['text'].strip())
            elif b.get('type') == 'tool_use':
                nm = b['name']; inp = b.get('input', {})
                if nm == 'SendUserMessage':
                    out.append(f'\n### 🟧 Claude (сообщение) · {t(ts)}\n\n' + inp.get('message', ''))
                else:
                    brief = inp.get('description') or inp.get('file_path') or inp.get('skill') or inp.get('query') or inp.get('url') or (inp.get('command', '')[:120] if isinstance(inp.get('command'), str) else '')
                    out.append(f'`⚙ {nm}: {str(brief)[:140]}`')
hdr = f'# ВЫГРУЗКА сессии {sys.argv[1].split("/")[-1][:8]} (27–29.09.2026)\n\n> Собрана скриптом `vygruzka.py`. Реплики владельца — дословно; вызовы инструментов — одной строкой. Реплик владельца: {n_owner}.\n'
open(sys.argv[2], 'w').write(hdr + '\n'.join(out) + '\n')
print('владелец:', n_owner, 'строк:', len(out))
