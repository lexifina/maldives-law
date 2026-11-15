# Maldives: law history in git


The law of the Maldives as a git history: one file per article for the Constitution and four main statutes and one file per act for the other statutes, one commit per version (or per amending law, where several laws made one version) on the day it took effect, and the law that made each change as the commit's author. `git blame` names the law behind every line; `git log` lists every change to an article; picking a date gives the text in force that day.

Part of [lexifina/global-law](https://github.com/lexifina/global-law), one git history for every country's law: this is the Maldives' national law, which global-law reads at `maldives/national/acts/`.

**What is in it now:** the Constitution and 174 statutes from the Attorney General's Office, with 205 versions in force from 1978 to 2026. The Constitution (9 versions, from 2008), the Penal Code (7), the Contract Act, the Companies Act (2) and the Family Act (3) are kept article by article with their amendments; the other 170 statutes are one file each, 3 of them with earlier versions. [`REPRODUCE.md`](REPRODUCE.md) lists every act with its versions, and [`data/versions.json`](data/versions.json) gives each version's source page.

The Constitution and those four statutes are in named folders, one file per article (`constitution/art-109.md` is Article 109 of the Constitution, who may be elected President); the other statutes are in `law-<id>/text.md`, by the act's number on mvlaw.gov.mv (`law-109/text.md` is the ވަޒީފާއާބެހޭ ޤާނޫނު, the Employment Act, Law No. 2/2008). Each folder's `README.md` lists its provisions.

The text is in Dhivehi, in Thaana script, as mvlaw.gov.mv publishes it. An English translation is not part of this record.

## Questions as git commands

| Question | Command |
| --- | --- |
| Every change to Article 109 of the Constitution | `git log -p --word-diff -- constitution/art-109.md` |
| Which law wrote each line of Article 109? | `git blame constitution/art-109.md` |
| Every version of the Constitution, with the day each took effect | `git log --format="%h %(trailers:key=In-force,valueonly,separator=) %an" -- constitution ":!constitution/README.md"` |
| Article 109 as in force on 1 January 2016 | `python tools/on.py 2016-01-01 constitution art-109` |

**Outside git**, we also host this record publicly, for free:

- **[Ask Claude about Maldivian law](https://global-law.lexifina.com/v1/try_claude?country=maldives)**: opens Claude with a first question ready.
- **[Ask ChatGPT](https://global-law.lexifina.com/v1/try_chatgpt?country=maldives)**: the same question in ChatGPT.
- **[Call the API in your browser](https://global-law.lexifina.com/v1/search_law?query=%DE%87%DE%A6%DE%80%DE%A6%DE%83%DE%A9+%DE%97%DE%AA%DE%87%DE%B0%DE%93%DE%A9&jurisdictions=maldives)**: a search of Maldivian law for "އަހަރީ ޗުއްޓީ" (annual leave), returned as JSON. See the [documentation here](https://lexifina.com/api/global-law).

Both assistants read the record through the free Global law connector (MCP, `https://global-law.lexifina.com/mcp`); the first time, the chat gives you the link that adds it. Ask in Dhivehi or in English.

**Host it yourself easily.** All it takes is git and Python, and the tools run on your machine:

```sh
git clone --depth 1 https://github.com/lexifina/global-law && cd global-law
python3 tools/countries.py add maldives/national/acts
python3 tools/law.py show 2026-01-01 maldives/national/acts/constitution/art-109.md
```

Opened in Claude Code, Cursor, VS Code or Codex, the clone also starts a local MCP server with the same tools ([MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md)).

## Dates

Each commit is dated at noon, Indian/Maldives, on the day the version took effect, and carries it in its `In-force:` trailer:

- for every version, the implementation date mvlaw.gov.mv gives for that consolidation; the Constitution's first version is the day it was ratified, 7 August 2008;
- for the 170 statutes kept one file each, the history starts at the oldest consolidation the site publishes as text, so the first date can be years after the law was passed (the Employment Act starts on 2026-03-08);
- the site gives no enactment dates for the amending laws, so none is recorded.

The first text of each article-by-article act is credited to its own law, and each later change to the law the site's amendment notes name for the changed article (23 commits in all). The oldest available version of each of the other 170 statutes, and 20 changes no note explains, are credited to the publisher, the Attorney General's Office of the Maldives.

## How it is checked

- `tools/check_repo.py` reads every version back from git on the day it took effect and on the day before, compares it file by file with the corpus it was built from, and checks that every commit's trailers parse; `REPRODUCE.md` records no run of it for this build yet.
- A second build from the same corpus into an empty folder gave identical hashes for all 213 history commits and 227 tags; the corpus hash is in [`data/corpus.sha256`](data/corpus.sha256) and the details in [`REPRODUCE.md`](REPRODUCE.md).
- History is append-only: new versions are added after the published head, no commit is rewritten, and `main` has no merge commits and no commit dated in the future.

## What it does not show

- **Earlier versions of most statutes.** Of the 170 statutes kept one file each, 167 have only the one consolidation the site publishes as text; their earlier versions, and for many the law as first passed, are not here.
- **Regulations, case law, treaties and bills.** Only the Constitution and statutes are here, and statutes with unverified embedded documents or media, or incomplete consolidations on the site, are left out in full.
- **Schedules and headings without text.** The Constitution's three Schedules and the Part headings of the four article-by-article statutes carry no text on the site and are not included.
- **Amendment notes and removed provisions.** The site's amendment notes are not part of the text, and provisions it marks as removed are left out from the version that removes them.

## Sources

| Source | Kind | Past versions | Notes |
| --- | --- | --- | --- |
| [Maldives Laws](https://mvlaw.gov.mv) (Attorney General's Office) | Official legislation website | the consolidations it publishes as text, each with its implementation date | Dhivehi text; its amendment notes name the amending laws |

## Licence

See [`LICENSE`](LICENSE). The laws of the Maldives are published on mvlaw.gov.mv for public use, and this repository makes no claim over them; Lexifina converted the site's pages to Markdown, removing the HTML and normalising whitespace, and the wording is otherwise the site's.

No AI model wrote, translated or corrected legal text, and no model runs when the history is built; the scripts were written by AI models (Claude and GPT-6, see [`REPRODUCE.md`](REPRODUCE.md)).

## More

From [lexifina/global-law](https://github.com/lexifina/global-law):

- [FEATURES.md](https://github.com/lexifina/global-law/blob/main/FEATURES.md): every feature, and what every corpus must support (`git blame`, `law.py`, the MCP tools)
- [FAQ.md](https://github.com/lexifina/global-law/blob/main/FAQ.md): questions and answers · [CONTRIBUTING.md](https://github.com/lexifina/global-law/blob/main/CONTRIBUTING.md): proposing changes · [MCP.md](https://github.com/lexifina/global-law/blob/main/MCP.md): the MCP server · [REPRODUCE.md](https://github.com/lexifina/global-law/blob/main/REPRODUCE.md): how it was built · [CHANGELOG.md](https://github.com/lexifina/global-law/blob/main/CHANGELOG.md)
- [FRESHNESS.md](https://github.com/lexifina/global-law/blob/main/FRESHNESS.md): how current each corpus is · [Monitoring](https://github.com/lexifina/global-law/tree/main/monitoring): whether updates are running · [WATCHING.md](https://github.com/lexifina/global-law/blob/main/WATCHING.md): how each official source is watched for changes
- [performance/](https://github.com/lexifina/global-law/tree/main/performance): how fast the tools are, measured
- [visualisations/](https://github.com/lexifina/global-law/tree/main/visualisations): charts and bridges across the world's law
- [Vulnerabilities](https://github.com/lexifina/global-law/tree/main/vulnerabilities): mistakes in legislation as published
