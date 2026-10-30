# Maldives: law history in git

The law of the Maldives as a git history: one file per provision, one commit per amending law on the day its version took effect, and the amending law as each commit's author. `git blame` names the law behind every paragraph; picking a date gives the text in force that day, within the limits below. It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `mv/`.

**What is in it now**

| Folder | Act | Versions | History |
| --- | --- | ---: | --- |
| `constitution/` | The Constitution of the Republic of Maldives (Dhivehi) | 9 | From the Constitution as ratified on 7 August 2008, through the eight consolidated versions the Attorney General's Office publishes, to the latest (in force 1 December 2025) |
| `penal-code/` | Penal Code (Law No. 9/2014) (Dhivehi) | 7 | From 2015-04-13 to 2024-12-17 |
| `contract-act/` | Contract Act (Law No. 4/1991) (Dhivehi) | 1 | From 1991-05-28 to 1991-05-28 |
| `companies-act/` | Companies Act (Law No. 7/2023) (Dhivehi) | 2 | From 2024-01-01 to 2024-09-18 |

Language: the official language, Dhivehi (right to left). The source site carries no English text of these laws, so none is included.

The amending laws credited to the Constitution are Law No. 16/2015, 20/2015, 9/2018, 3/2019, 22/2019, 4/2020, 25/2024 and 21/2025; those credited to each statute are the laws named in its own amendment notes on the source.

**What it does not show**

- Only the Constitution and the statutes in the table. Other statutes and regulations are not included yet.
- The date of each version is the implementation date the source gives for that consolidation. The source does not give the enactment dates of the amending laws, so none is recorded.
- Provisions the source marks as removed are left out of the version that removes them. The three Schedules are headings only on the source and are not included. Amendment notes are not part of the text.
- Items the source prints without an article number are kept as extras of the article before them (for example `art-309-x01`).

**Source**

Maldives Laws, Attorney General's Office: <https://mvlaw.gov.mv/en/legislations/6> (Constitution, retrieved on 29 October 2026) and the pages of each statute in the table (retrieved on 30 October 2026).

Nothing here is legal advice; for anything that matters, read the original. How the files were made is in [REPRODUCE.md](REPRODUCE.md).

## Licence

See [LICENSE](LICENSE).
