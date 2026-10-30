"""Shared helpers for reading mvlaw.gov.mv consolidation pages (copied from parse.py)."""
import re, html, json, hashlib, pathlib
H = pathlib.Path(__file__).parent
C = H / ".cache"


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
        if first is not None and head:
            units['chapter-%03d' % first] = {'label': 'Chapter before Art. %d' % first, 'kind': 'heading',
                                             'text': '# Chapter before Art. %d\n%s\n' % (first, head)}
        elif first is not None:
            pass
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


