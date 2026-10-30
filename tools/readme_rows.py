"""Rewrite the table in repo/README.md from corpus.json (private)."""
import json, re, pathlib
H = pathlib.Path(__file__).parent
c = json.load(open(H / 'corpus.json', encoding='utf-8'))
rows = []
for a in c['acts']:
    if a['slug'] == 'constitution':
        continue
    v = a['versions']
    rows.append('| `%s/` | %s (Dhivehi) | %d | From %s to %s |' % (a['slug'], a['title'].replace(' (Dhivehi)', ''), len(v), v[0]['from'], v[-1]['from']))
s = (H / 'repo' / 'README.md').read_text('utf-8')
s = re.sub(r'(\| `constitution/` \|[^\n]*\n)(\| `[a-z-]+/` \|[^\n]*\n)*', lambda m: m.group(1) + ''.join(r + '\n' for r in rows), s, count=1)
s = s.replace('**What is in it now (a first build)**', '**What is in it now**')
s = s.replace('- Only the Constitution. Other statutes and regulations are not included yet.', '- Only the Constitution and the statutes in the table. Other statutes and regulations are not included yet.')
s = s.replace('Maldives Laws, Attorney General\'s Office: <https://mvlaw.gov.mv/en/legislations/6>, retrieved on 29 October 2026.', 'Maldives Laws, Attorney General\'s Office: <https://mvlaw.gov.mv/en/legislations/6> (Constitution, retrieved on 29 October 2026) and the pages of each statute in the table (retrieved on 30 October 2026).')
(H / 'repo' / 'README.md').write_text(s, 'utf-8', newline='\n')
