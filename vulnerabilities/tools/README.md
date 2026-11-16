# Tools

The scripts behind this Maldives-only run of global-law's vulnerability detectors. They run inside a copy of
[global-law/vulnerabilities/scripts](https://github.com/lexifina/global-law/tree/main/vulnerabilities/scripts) (Python 3.11+,
`pip install duckdb pyarrow`), with a bare clone of this repository at `sources/corpus/maldives-law.git`, a blobless bare
clone of global-law at `sources/global-law.git`, and a `pins.json` that names only maldives-law and its commit (language
`dv`). `build_vulns.py`, `flags_chart.py`, `late_ext_select.py` and `late_ext_rebut.py` sit two folders above the scripts,
next to `config.json`.

| Script | What it does |
| --- | --- |
| `run.sh` | Indexes the history and texts, maps moved paths (`map_moved.py`), adds this repository's history rows, and runs the detectors (`bash run.sh <shards>`) |
| `map_moved.py` | Rewrites old paths in the history table to each act's folder today through `data/paths.json`; this repository has no such file, so it changes nothing here |
| `add_root.py` | Builds the history rows from this repository's own commits (global-law replays it only up to an earlier commit), so the history detectors read every change |
| `run_triage.sh` | The model review: the 40 strongest flags per category, the 40 strongest lapsed time limits in law texts, and the empty periods (here 11 lapsed time limits, reviewed in both passes, and no empty periods) |
| `late_ext_select.py` | Chooses the empty periods for global-law's review of that category (there were none here) |
| `late_ext_rebut.py` | Adds the second, arguing-against pass to the empty-period review, as `triage.py` does for the other categories |
| `build_vulns.py` | Builds `data/flags.csv`, `data/reviewed.csv` and `data/by_category.csv` from the findings and the model review |
| `flags_chart.py` | Draws the chart at the top of the READMEs, in Dhivehi and English, light and dark; the Dhivehi chart is drawn right to left |
| `config.json` | The repository, the Dhivehi category names, the files that are not law, and the chart's labels |
| `patch_detectors.py` | Fixes blind spots found in runs on several country repositories in the copy of global-law's scripts (`python -X utf8 patch_detectors.py <scripts dir>`) |
| `patch_detectors_vi.py`, `patch_es.py`, `patch_ca.py`, `patch_en.py`, `patch_de.py`, `patch_en_et.py`, `patch_co.py`, `patch_sv.py`, `patch_pt.py`, `patch_ru.py`, `patch_r18.py`, `patch_xk.py`, `patch_mo.py`, `patch_lu.py`, `patch_li.py`, `patch_mx.py`, `patch_mn.py`, `patch_mt.py` | The same for the blind spots other runs found in other languages and repositories; this run's copy carries them all. None of them reads Dhivehi |
| `patch_dv.py` | The fixes for Dhivehi, below (`python -X utf8 patch_dv.py <scripts dir>`; each change carries a `patch_dv` marker, and one already in place is skipped) |
| `apply_patches.py` | Applies every patch above once, in order, recording each in `.kit_patches.json` in the scripts folder (`python -X utf8 apply_patches.py <scripts dir>`); `patch_dv.py` is last in its list |
| `redo.py` | Runs `apply_patches.py`, then again only the scans and detectors the fixes change, the model review of lapsed time limits, references to deleted provisions and empty periods, and the build (`python -X utf8 redo.py <run folder> [--keep-reviews] [--full]`; `--full` runs every step again through `run.sh`; `EMBED_FONTS` names the script that embeds the chart's fonts); not needed here, as every fix was in place before the run whose results are published |

The model review needs `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL` and `LLM_AUTH` set for an OpenAI-compatible Responses API.
It was run as `bash run_triage.sh '^(data/|tools/|README|REPRODUCE|LICENSE|jurisdiction)'`; every law is under
`constitution/`, `penal-code/`, `contract-act/`, `companies-act/`, `family-act/` or `law-<id>/`, so the review of lapsed time
limits in law texts drew the same 11 flags as the review of all of them, and `build_vulns.py` keeps the later review of each.

Changes made for this repository:

- `pins.json` names the corpus language as `dv` (global-law's list of corpora gave none): every text is in Dhivehi, in
  Thaana script.
- `add_root.py` is unchanged: the 23 commits credited to the law that made a change carry `Kind: law`, and the 190 that
  hold a statute's oldest version available or a change no amendment note explains carry `Kind: publisher`, which the kit
  already counts as law. The commits with no `In-force` trailer (the READMEs, tables, tools and `REPRODUCE.md`) are left out.
- `patch_dv.py`, time limits (`ingest/textscan.py`): no Dhivehi date was read. Dhivehi writes "until" after the date, in
  Thaana ("31 ޑިސެންބަރު 2021 ގެ ނިޔަލަށް", until 31 December 2021; "ނިޔަލަށެވެ" at the end of a sentence), and the months
  are spelt several ways (ޑިސެމްބަރު, ޑިސެންބަރު, ޑިސެމްބަރ; އޭޕްރިލް, އެޕްރީލް ...). A day, a Dhivehi month and a
  four-digit year followed by "until" are now read in a corpus whose language is `dv`. Lapsed time limits went from 0 to
  11. In the law texts at this commit, all 11 such phrases are read; the 3 that give only a year ("2030 ވަނަ އަހަރުގެ
  ނިޔަލަށް", until the year 2030) are left out, as "until 2030" is in other languages, and none of them has passed.
- `patch_dv.py`, amounts (`ingest/textscan.py`): amounts in rufiyaa and US dollars, written with the amount in words in
  brackets and a case ending on the currency ("10,000 (ދިހަހާސް) ރުފިޔާއާ", "500 (ފަސްސަތޭކަ) އެމެރިކާ ޑޮލަރު"), were not
  read; they are now, for the search for stale amounts. It found none: amounts can only go stale between versions, and
  most statutes have one.
- Not fixed: the reference scan (`ingest/refscan.py`) does not read Dhivehi references ("މި ޤާނޫނުގެ 25 ވަނަ މާއްދާ"), and
  references to inserted articles are written with the inserted number first ("1-51 ވަނަ މާއްދާ" for Article 51-1). Read by
  hand, none of the 569 references of the five article-by-article acts to their own articles points to an article this
  repository no longer holds, so a fix would change no count here.
- `flags_chart.py` draws the Dhivehi chart mirrored, right to left (`direction="rtl"` on each text), and measures Thaana
  vowel signs as taking no width. The Thaana labels use the reader's system font, as this repository's own Dhivehi charts
  in `data/dv/` do: the embedded fonts (Manrope, JetBrains Mono) have no Thaana glyphs.
- `config.json` counts as not law `data/`, `tools/`, the root files and every `README.md` (each folder's list of its files).
- There are no amounts in a dead currency: the amounts are in rufiyaa and US dollars.
