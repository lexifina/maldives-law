"""Parse the cached mvlaw.gov.mv consolidations of the Constitution into corpus.json (private)."""
import re, html, json, hashlib, pathlib
H = pathlib.Path(__file__).parent
C = H / '.cache'
# (consolidation id, amendment number, law key)
VERS = [(5, 0, None), (754, 1, 'law-16-2015'), (758, 2, 'law-20-2015'), (759, 3, 'law-9-2018'),
        (761, 4, 'law-3-2019'), (764, 5, 'law-22-2019'), (783, 6, 'law-4-2020'),
        (1260, 7, 'law-25-2024'), (1304, 8, 'law-21-2025')]
LAWNO = {'law-16-2015': '16/2015', 'law-20-2015': '20/2015', 'law-9-2018': '9/2018', 'law-3-2019': '3/2019',
         'law-22-2019': '22/2019', 'law-4-2020': '4/2020', 'law-25-2024': '25/2024', 'law-21-2025': '21/2025'}
MONTHS = {m: i + 1 for i, m in enumerate('January February March April May June July August September October November December'.split())}
NOTE_RE = 'तथ'  # placeholder, replaced below
LAW_WORD = 'ނާނޫނު ންބަންބަރު'  # unused


def load(i):
    raw = (C / f'cons-{i}.html').read_bytes()
    t = raw.decode('utf-8')
    m = re.search(r'data-page="([^"]+)"', t)
    return json.loads(html.unescape(m.group(1)))['props'], hashlib.sha256(raw).hexdigest()


def txt(s):
    s = s or ''
    s = re.sub(r'<br\s*/?>', ' ', s)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = html.unescape(s).replace(' ', ' ')
    return re.sub(r'\s+', ' ', s).strip()


def lines_of(sec, depth=0):
    """Lines of an item and its descendants (removed ones skipped)."""
    out = []
    if sec.get('amendment_type') == 'removed':
        return out
    num, title, body = txt(sec.get('number')), txt(sec.get('title')), txt(sec.get('content'))
    if depth == 0 and title and body:
        parts = [p for p in (num, title + ' --', body) if p]
    else:
        parts = [p for p in (num, title if depth == 0 else '', body) if p]
    if parts:
        out.append(' '.join(parts))
    for c in sec.get('children') or []:
        out += lines_of(c, depth + 1)
    return out


SCHED = re.compile(r'^ޖަދުވަލު (\d+)')


def build_units(props):
    units = {}
    prev_art = 0
    xk = 0
    for ch in props['sections']:
        if ch.get('amendment_type') == 'removed':
            continue
        kids = list(ch.get('children') or [])
        first = None
        for c in kids:
            m = re.match(r'(\d+)\.?$', txt(c.get('number')))
            if m and c.get('amendment_type') != 'removed':
                first = int(m.group(1))
                break
        title = txt(ch.get('title'))
        num = txt(ch.get('number'))
        sched = SCHED.match(num) or SCHED.match(title)
        head = ' '.join(p for p in (num, title) if p)
        if first is not None:
            units['chapter-%03d' % first] = {'label': 'Chapter before Art. %d' % first, 'kind': 'heading',
                                             'text': '# Chapter before Art. %d\n%s\n' % (first, head)}
        elif sched:
            continue  # schedule headings carry no text on the site
        elif not kids:
            continue
        for c in kids:
            if c.get('amendment_type') == 'removed':
                continue
            n = re.match(r'(\d+)\.?$', txt(c.get('number')))
            if n:
                prev_art = int(n.group(1))
                xk = 0
                k = 'art-%03d' % prev_art
                label = 'Art. %d' % prev_art
            else:
                xk += 1
                k = 'art-%03d-x%02d' % (prev_art, xk)
                label = 'Art. %d (unnumbered item %d)' % (prev_art, xk)
            ls = [l for l in lines_of(c) if l.strip('. ')]
            if not ls:
                continue
            assert k not in units, k
            units[k] = {'label': label, 'kind': 'art', 'text': '# %s\n' % label + '\n'.join(ls) + '\n'}
    return units


def fdate(s):
    d, m, y = s.split()
    return '%04d-%02d-%02d' % (int(y), MONTHS[m], int(d))


versions = []
prev = {}
laws = {'constitution-2008': {
    'label': 'Constitution of the Republic of Maldives (2008)',
    'title': 'Constitution of the Republic of Maldives, ratified 7 August 2008',
    'kind': 'law', 'enacted': '2008-08-07', 'published': '2008-08-07',
    'url': 'https://mvlaw.gov.mv/en/legislations/6/consolidations/5', 'temporary_until': None, 'restores': None,
    'note': None}}
for cid, n, law in VERS:
    props, sha = load(cid)
    units = build_units(props)
    frm = fdate(next(r['formatted_implemented_at'] for r in [props['legislation']['latest_consolidation']] + props['related_consolidations'] if r['id'] == cid))
    v = {'from': frm, 'source_url': 'https://mvlaw.gov.mv/en/legislations/6/consolidations/%d' % cid,
         'sha256': sha, 'units': units}
    if n > 0:
        cred = {k: [law] for k, u in units.items() if prev.get(k, {}).get('text') != u['text']}
        cred.update({k: [law] for k in prev if k not in units})
        v['credits'] = cred
        allnotes = []

        def walk(s):
            if s.get('amendment_note'):
                allnotes.append(txt(s['amendment_note']))
            for c in s.get('children') or []:
                walk(c)
        for s in props['sections']:
            walk(s)
        t = ''
        for a in allnotes:
            m = re.search(re.escape(LAWNO[law]) + r'\s*\(([^)]*)\)', a)
            if m:
                t = m.group(1)
                break
        laws[law] = {'label': 'Law No. ' + LAWNO[law], 'title': t or ('Law No. ' + LAWNO[law]), 'kind': 'law',
                     'enacted': None, 'published': None,
                     'url': 'https://mvlaw.gov.mv/en/legislations/6/consolidations/%d' % cid,
                     'temporary_until': None, 'restores': None, 'note': None}
        print(n, law, frm, 'changed', len(cred), 'notes', len(allnotes), 'title ok' if t else 'NO TITLE')
    versions.append(v)
    prev = units
head = json.loads((H / 'corpus_head.json').read_text('utf-8'))
head['laws'] = laws
head['acts'][0]['versions'] = versions
(H / 'corpus.json').write_text(json.dumps(head, ensure_ascii=False, indent=1) + '\n', 'utf-8')
print(len(versions), [len(v['units']) for v in versions])
