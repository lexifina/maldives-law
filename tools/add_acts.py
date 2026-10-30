"""Add statutes from the cached mvlaw.gov.mv consolidations to corpus.json (private; reads .cache only).

usage: python -X utf8 add_acts.py <legislation id> <slug> <short> <english title>   (repeat the group for several acts)
Keeps every act already in corpus.json; replaces an act with the same slug.
"""
import json, re, sys, hashlib
import mvlib
from mvlib import H, C, load, txt

MONTHS = {m: i + 1 for i, m in enumerate('January February March April May June July August September October November December'.split())}


def fdate(s):
    d, m, y = s.split()
    return '%04d-%02d-%02d' % (int(y), MONTHS[m], int(d))


def pad_units(units, width):
    out = {}
    for k, u in units.items():
        k2 = re.sub(r'(?<=-)(\d{3})(?=-|$)', lambda m: m.group(1).zfill(width), k)
        out[k2] = u
    return out


def note_laws(sec, base):
    """{unit-level node -> set of law numbers cited in its amendment notes}"""
    found = {}

    def walk(s):
        n = s.get('amendment_note')
        if n:
            for m in re.finditer(r'ޤާނޫނު ނަންބަރު (\d+/\d{4})', txt(n)):
                if m.group(1) != base:
                    found[m.group(1)] = found.get(m.group(1), None)
        for c in s.get('children') or []:
            walk(c)
    walk(sec)
    return set(found)


def unit_laws(props, base):
    """unit key -> laws cited in that unit's notes (keys as build_units makes them, unpadded)."""
    out, prev_art, xk = {}, 0, 0
    for ch in props['sections']:
        if ch.get('amendment_type') == 'removed':
            continue
        for c in ch.get('children') or []:
            if c.get('amendment_type') == 'removed':
                continue
            n = re.match(r'(\d+)\.?$', txt(c.get('number')))
            if n:
                prev_art = int(n.group(1)); xk = 0
                k = 'art-%03d' % prev_art
            else:
                xk += 1
                k = 'art-%03d-x%02d' % (prev_art, xk)
            out[k] = note_laws(c, base)
    return out


def law_titles(props, titles):
    def walk(s):
        if s.get('amendment_note'):
            for m in re.finditer(r'ޤާނޫނު ނަންބަރު (\d+/\d{4}) \[([^\[\]]*)\]', txt(s['amendment_note'])):
                titles.setdefault(m.group(1), m.group(2).strip())
        for c in s.get('children') or []:
            walk(c)
    for s in props['sections']:
        walk(s)


def build_act(lid, slug, short, title, corpus):
    leg, _ = load_leg(lid)
    base = leg['legislation_number']
    cons = {c['id']: c for c in leg['related_consolidations']}
    assert leg['consolidation_id'] in cons
    order = sorted(cons.values(), key=lambda c: (fdate(c['formatted_implemented_at']), c['number']))
    width = 4 if any(int(x) >= 1000 for x in re.findall(r'\d+', json.dumps([s.get('number') for s in leg['sections']]))) else 3
    versions, prev, prev_laws, titles = [], {}, {}, {}
    seen_laws = []
    for c in order:
        props, sha = load(c['id'])
        raw_units = mvlib.build_units(props)
        units = pad_units(raw_units, width)
        ul = unit_laws(props, base)
        law_titles(props, titles)
        v = {'from': fdate(c['formatted_implemented_at']), 'source_url': 'https://mvlaw.gov.mv/en/legislations/%d/consolidations/%d' % (lid, c['id']),
             'sha256': sha, 'units': units}
        if versions and versions[-1]['from'] == v['from']:
            v['same_day'] = True
        if prev:
            cred = {}
            for k, u in raw_units.items():
                k2 = pad_units({k: 0}, width).popitem()[0]
                if prev.get(k2, {}).get('text') != units[k2]['text']:
                    new = sorted(ul.get(k, set()) - prev_laws.get(k, set()))
                    if new:
                        cred[k2] = ['law-' + n.replace('/', '-') for n in new]
                        for n in new:
                            if n not in seen_laws:
                                seen_laws.append(n)
            for k in prev:
                if k not in units:
                    gone = []
                    cred[k] = gone
            cred = {k: v_ for k, v_ in cred.items() if v_}
            v['credits'] = cred
        versions.append(v)
        prev, prev_laws = units, ul
    first_is_original = order[0]['number'] == 0
    law_key = 'law-' + base.replace('/', '-')
    corpus['laws'][law_key] = {'label': 'Law No. ' + base, 'title': leg['legislation']['title'], 'kind': 'law', 'enacted': None,
                               'published': leg['published_at'] and fdate(leg['published_at']), 'url': 'https://mvlaw.gov.mv/en/legislations/%d' % lid,
                               'temporary_until': None, 'restores': None, 'note': None}
    for n in seen_laws:
        k = 'law-' + n.replace('/', '-')
        corpus['laws'].setdefault(k, {'label': 'Law No. ' + n, 'title': titles.get(n) or ('Law No. ' + n), 'kind': 'law', 'enacted': None, 'published': None,
                                      'url': 'https://mvlaw.gov.mv/en/legislations/%d' % lid, 'temporary_until': None, 'restores': None, 'note': None})
    act = {'slug': slug, 'short': short, 'title': title + ' (Dhivehi)', 'url': 'https://mvlaw.gov.mv/en/legislations/%d' % lid,
           'first_law': law_key if first_is_original else None, 'earlier_laws': [] if first_is_original else [law_key], 'versions': versions}
    corpus['acts'] = [a for a in corpus['acts'] if a['slug'] != slug] + [act]
    print(slug, [(v['from'], len(v['units']), len(v.get('credits', {}))) for v in versions], 'laws', seen_laws)


def load_leg(lid):
    import html
    t = (C / ('leg-%d.html' % lid)).read_bytes()
    return json.loads(html.unescape(re.search(r'data-page="([^"]+)"', t.decode('utf-8')).group(1)))['props'], hashlib.sha256(t).hexdigest()


corpus = json.loads((H / 'corpus.json').read_text('utf-8'))
a = sys.argv[1:]
for i in range(0, len(a), 4):
    build_act(int(a[i]), a[i + 1], a[i + 2], a[i + 3], corpus)
corpus['sources'] = [s for s in corpus['sources'] if 'Constitution' in s['notes']] + [{
    'name': "Maldives Laws (mvlaw.gov.mv), Attorney General's Office: statutes", 'url': 'https://mvlaw.gov.mv', 'retrieved': '2026-10-30',
    'licence': 'Official publication of the laws of the Maldives',
    'notes': "Every consolidated version of each statute, read from the site's own structured pages. The official language is Dhivehi; the site carries no English text of these statutes. robots.txt allows all; 4 s between requests."}]
decs = [d for d in corpus['decisions'] if not d.startswith('Statutes:')]
decs += ['Statutes: each statute is built from every consolidation the site lists, ordered by the consolidation implementation date the site gives. The first consolidation (the law as passed) is credited to the law itself; later changes are credited to the amending laws named in the unit\'s own amendment notes that were not named in the same unit in the previous version. A changed unit with no new note is left uncredited (the commit is labelled unexplained).',
         'Statutes: unit rules follow the Constitution (one file per article with its sub-items as lines, one file per chapter heading, removed items left out, amendment notes not part of the text). Part headings and Schedules carry no text on the site and are not included. Article keys are padded to the width of the act\'s highest article number.']
corpus['decisions'] = decs
(H / 'corpus.json').write_text(json.dumps(corpus, ensure_ascii=False, indent=1) + '\n', 'utf-8', newline='\n')
