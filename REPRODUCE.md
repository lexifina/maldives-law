# How this repository was made (Maldives)

This file is written by the build on 2026-10-30, the day the source data was retrieved.

## Sources

| Source | Address | Retrieved | Licence |
| --- | --- | --- | --- |
| Maldives Laws (mvlaw.gov.mv), Attorney General's Office | <https://mvlaw.gov.mv/en/legislations/6> | 2026-10-29 | Official publication of the laws of the Maldives |
| Maldives Laws (mvlaw.gov.mv), Attorney General's Office: statutes | <https://mvlaw.gov.mv> | 2026-10-30 | Official publication of the laws of the Maldives |

Every word of law in this repository comes from these sources. Lexifina reads them and records each act's dated versions, and the laws that made each change, in one corpus file. This repository is built from that file.

## What is in it

| Act | Title | Versions | Span |
| --- | --- | ---: | --- |
| `constitution` | Constitution of the Republic of Maldives (Dhivehi) | 9 | 2008-08-07 to 2025-12-01 |
| `penal-code` | Penal Code (Law No. 9/2014) (Dhivehi) | 7 | 2015-04-13 to 2024-12-17 |
| `contract-act` | Contract Act (Law No. 4/1991) (Dhivehi) | 1 | 1991-05-28 to 1991-05-28 |
| `companies-act` | Companies Act (Law No. 7/2023) (Dhivehi) | 2 | 2024-01-01 to 2024-09-18 |

The build made 26 commits:

| Commits | Kind |
| ---: | --- |
| 4 | first version of an act |
| 16 | one law on its in-force day |
| 6 | changes no amendment note explains, credited to the publisher |

Other counts:
- 0 commits on the branch `future`: laws not yet in force on 2026-10-30.
- 0 commits dated 1 January 1970: in force before 1970, with the real day in their `In-force` trailer.
- 19 laws in the record.
- 38 tags.

## Dates

Each commit is dated at noon (Indian/Maldives) on the day the change took effect. The other dates, enacted and published, are trailers.

When a law gives no date of its own, the default rule applies: No default rule is applied. Each version's in-force day is the date the Attorney General's Office gives for that consolidation of the Constitution on mvlaw.gov.mv (its implementation date). https://mvlaw.gov.mv/en/legislations/6

## How the history is built

`tools/build.py` turns the corpus into this history in one pass: one commit per law, on the day it took effect. The same corpus always gives the same commit hashes. `tools/check_repo.py` reads every version back from git and compares it with the corpus. `tools/on.py` shows the law as it stood on any date. The corpus format is described in `tools/SCHEMA.md`.

- Corpus: sha256 `3398c6d52de157ad2e8a4439ef11fab9aa8b3b21a7ea28cbff47626a61c9f3ee` (9266252 bytes).
- Builder blob hashes (`git hash-object`): `build.py` `a4faa25af85facb64b956b372f6b528aafdd7ec1`, `check.py` `3e59cb6f05eccb94a9ec14431a7f6781221e83ef`, `on.py` `644a6c0857fbcc72562032b58d57aa113fee0641`.
- Python 3.12.10; git version 2.46.0.windows.1.

## Checks

Not yet run for this build.

No second build of this corpus has been compared yet.

## Decisions made by hand

- The text is the Dhivehi text, the official language; mvlaw.gov.mv carries no English text of the Constitution.
- Nine versions: the 2008 text and the site's eight consolidations, each dated by the implementation date the site gives for it, and each credited to the amendment law that the site's own amendment notes name (Law No. 16/2015, 20/2015, 9/2018, 3/2019, 22/2019, 4/2020, 25/2024, 21/2025).
- The site does not give the enactment dates of the amending laws, so none is recorded for them.
- Provisions the site shows as removed by an amendment are left out of the version that removes them and of later versions; amendment notes themselves are not part of the text.
- One file per article, with its sub-items as lines; one file per chapter heading. The three Schedules are headings only on the site and are not included. Chapters are keyed by the first article that follows them.
- Items the site prints without an article number are kept as numbered extras of the article before them (for example art-309-x01).
- Statutes: each statute is built from every consolidation the site lists, ordered by the consolidation implementation date the site gives. The first consolidation (the law as passed) is credited to the law itself; later changes are credited to the amending laws named in the unit's own amendment notes that were not named in the same unit in the previous version. A changed unit with no new note is left uncredited (the commit is labelled unexplained).
- Statutes: unit rules follow the Constitution (one file per article with its sub-items as lines, one file per chapter heading, removed items left out, amendment notes not part of the text). Part headings and Schedules carry no text on the site and are not included. Article keys are padded to the width of the act's highest article number.

## What AI did and did not do

The scripts that read the sources and build this repository were written by Claude Code running Claude Opus 5.5 (`claude-opus-5-5`) under Lexifina's direction.

No model wrote, translated or corrected legal text. No model runs at build time. Every word of law in this repository comes from the official sources above.

The commit messages are written by `build.py` from the source data.

Model use at data-build time:
- Claude Code (Claude Sonnet 5.5) wrote the parser. No model wrote, edited or summarised legal text.
