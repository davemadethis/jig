# Metarepo rules

These are a metarepo's rules. Its pararepos keep theirs in `.jig/rules/rules-pararepo.md`.

## Metarepo

A set of repos can share one **metarepo**: docs only — definitions, decisions, conventions, the
contracts the pararepos share (What the metarepo holds). Each **pararepo** (code, firmware,
hardware) cites it at a released tag. The metarepo points; nothing copies it. Three rules do the work:

1. A pararepo writes the metarepo only by branch, via `jig propose` (the pararepo's `rules-pararepo.md`, rule 1).
2. The metarepo holds no code and no copied pararepo content (What the metarepo holds).
3. Only `jig release` tags, so a pin never names something that failed validation.

**What the metarepo holds.** A claim lives in the metarepo when another repo must agree with it or
build against it: a contract, unless a decision makes a pararepo page its authority; then the
metarepo holds the decision and points to the page. Otherwise a claim lives with its one owner, and
the metarepo points to it (`<repo>/<path> § <section>`) instead of restating it. Each claim has one
home and is stated only there; everywhere else is a pointer. Inside the metarepo, a decision row and
the pages that cite it as their source are one home.
A pointer's form, and how a pararepo checks it, are in `rules-pararepo.md` (Citing the metarepo).

A claim found to have one owner moves to it, down to a pararepo as well as up or sideways: `jig move` does both ends, one step per `--apply`, as `rules-pararepo.md` (Moving a claim) says.

The metarepo's decisions are its `.jig/decisions.md` (`rules-decisions.md`, Decision log), cited as
`<meta>/.jig/decisions.md § D-012`.

A question that binds the pararepos is an idea in the metarepo's `.jig/ideas.md` when it is asked,
cited as `<meta>/.jig/ideas.md § E-012` or by its id before it is answered; it moves to `Proposed`,
then is accepted (its block moved, id kept, to the log's `## Unreleased`) or removed. The ideas file
is an entry file always, as the log is, and recorded by itself: M3 asks no change line for it.
A reversed decision is a new entry that supersedes the old.

Each side's gates are on only when its file is on trunk: `.jig/meta.json` or `.jig/para.json`.
`jig init --meta` and `jig init --para <metarepo>` write them; every other command reads them and
does what that kind of repo needs. Each also writes AGENTS.md's generated block, between
`<!-- jig:meta — ` and `<!-- jig:meta end -->`, so the rules every task meets are always loaded
in jig's words: `jig init --para` the pararepo's header, `jig init --meta` the metarepo's block
(M1, M4, M6, M3, and that only `jig release` tags). A block's lines are jig's, never read as
the repo's procedure. `jig update` lists a metarepo's block when it is missing or older than
this jig's; once `meta.json` is on trunk it is rewritten in a job, by `jig init --meta` in the
job's worktree (M4).

**A metarepo's docs tree.** A metarepo's pages are under `docs/`, each in a genre folder:
`docs/<genre>/<name>.md`, or `docs/<genre>/<name>/<name>.md` once it holds more than itself,
with its subsystems below it. A genre is a folder directly under `docs/`, a category of the
ecosystem the metarepo defines (products, features, principles, concepts), so the opposite of a
code repo holds: genre folders are required here, where a code repo's tree names one product's
parts. A genre has no page of its own and adds no depth; its term is an `### <genre>` heading under
`# Basic terms` in `docs/glossary.md`, the one file directly in `docs/`. `meta.json`'s optional `genres` lists them (`jig init --meta --genres
a,b,c`, or `--genres product-ecosystem` for those four); without it, any folder under `docs/`
is one. `jig survey` names a page directly in `docs/`, one in a folder `genres` doesn't declare,
and every other Markdown file outside `docs/` that isn't a root document or a decision register
(a file named `DECISIONS.md`, or holding decision rows), with `docs/<its top folder>/<name>.md`
as where it goes; `/jig:redocument` moves them. `entry_files` never makes a page's home.
There, a claim's source is a decision row or the pararepo file a pointer names; an Invariant's
holder is an accepted decision id; an open question is an idea in its repo's ideas log. A dated state
section is checked against the pararepo's trunk and folded into the body or dropped.

`entry_files` in `meta.json` lists what pararepos cite: what a release counts, what M3 asks a
log line for, and what a pararepo caches. Its entries are globs, matched the way `owns`
is: a folder of pages goes in as `docs/**/*.md`, and a new page there needs no edit. Nothing
under `.jig/` counts, whatever the globs say, except `.jig/decisions.md`, which always does.
`jig init --meta` names `.jig/decisions.md` and `docs/glossary.md`, which holds the terms
(`rules-docs.md`, Documentation), and writes the glossary. The README is for outsiders and no entry file, so its
prose changes without a log line. A metarepo that hasn't moved its glossary still names
`README.md`, and pararepos cite only its `## Glossary` section: M3 counts a `README.md` change
only there, until the move takes `README.md` out of `entry_files`. A release's term report reads the glossary's terms, its headings
at the three levels, and names each term added, removed or reworded; across the release that
moves a README glossary to `docs/glossary.md`, it reads the older side's README, and names each
term as moved. The move, in a metarepo, runs in a job's worktree (M4), and rewrites
`entry_files` in the same change; a pararepo's `<meta>/README.md § <term>` is named at its pin
bump with the term's new home, `<meta>/docs/glossary.md § <term>`.

| Gate | Refuses |
|---|---|
| M1 | a source file outside `.jig/` in the metarepo |
| M2 | in every repo, a `.jig/decisions.md` entry with a status in its heading, no status line (`Accepted (who, YYYY-MM-DD).`, `Open (YYYY-MM-DD).`, `Proposed (YYYY-MM-DD).`), a supersedes link to no entry in the log or in trunk's history of it, an id used twice, an `## Open` heading or an open or proposed entry the log adds (an idea goes in `.jig/ideas.md`), a `.jig/ideas.md` entry with a status in its heading, no `Open` or `Proposed` status line, a decided status, an id the log also has, or a section, or an entry or idea added or changed with no `Touches:` line, or one naming what is no docs page there, a `§` that is no term of that glossary, or a `none` line not written `none — <reason>`, or beside pages (`rules-decisions.md`, Decision log) |
| M3 | an entry file changed without a line or entry in `.jig/decisions.md` (of a `README.md` still listed, only its `## Glossary` section), judged on the branch since it left trunk: a line an earlier commit on the branch added covers this one, and a commit that drops the branch's only line is refused |
| M4 | a commit on trunk that isn't a merge (jig's own files under `.jig/` excepted, but not `.jig/decisions.md`: a decision is reviewed work); a detached HEAD at trunk, or behind it, is trunk |
| M5 | a merge into trunk of a commit `jig reviewed` never recorded. A commit counts as reviewed when a recorded one is its first-parent ancestor and nothing of the job's changed since: handoff notes and the rows they add to `.jig/ledgers/deferred.md` (committed after the review by design) and syncs of trunk that `jig sync` would make don't count. A job's sync of trunk and the gate's scratch merge aren't merges into trunk; a merge on a detached HEAD at trunk, or behind it, is |
| M6 | a subject that doesn't start with the ids it touches (`D-022: …`, `GLOSSARY: …`; on a branch, `D-?store-ro: …`) |

A fast-forward runs no hook, so a metarepo's release and its pre-push re-check every
first-parent commit since the last release, and refuse any tag `jig release` didn't make: one
whose `.jig/decisions.md` has no heading for it, unless it was made before the log and the
`CHANGELOG.md` that tag holds has the heading the release wrote then.
Pre-push judges the commit pushed to the remote's trunk, which may not be the local trunk's;
a chained `pre-push.local` hook gets the same pushed refs.
In a metarepo the release needs no `release.sh` steps; its level is chosen as Versioning (`rules-release.md`) says.

**A pin-bump request.** After its tag, a metarepo's `jig release` stages a request in each pararepo
`meta.json`'s `pararepos` lists, found through `jig repos`, whose trunk `para.json` cites it, when
the release broke something that pararepo cites: a citation that resolved at the previous tag and
dangles at the new one, or a decision id the release removed or superseded, cited as
`<metarepo>/<path> § <id>`, or as a bare whole word where the pararepo's own decisions use another
prefix (with the same prefix, only the qualified citation counts: a bare id is the pararepo's own).
A rewording, an idea accepted or a glossary term reworded doesn't select it: its own `jig sync`
reports those. The request is `.jig/staging/pin-bump-<metarepo>.md`, `kind: pin-bump`, `destination:
.jig/para.json`, with `from`, `pin` and `release` in its header and, from the pin to the new tag,
the `**Breaking:**` lines, the citations to rewrite with each new home jig can name, and the removed
or superseded ids with the files that cite them. What the metarepo moved down is listed as moved,
with its new home: `D-040 (moved: .jig/decisions.md § D-016, this repo)` in the repo that received
it, and a page or heading cited ends `: now <home>`, never reading as removed or missing; the
release's line counts them as `n moved`. A later release rewrites it in place, covering the whole
gap from the pin, while it is open (its release above the pin) and something in that gap breaks what
the pararepo cites; when nothing does, the release leaves it as it stands and prints a skip line.
Once the pin holds it, it is answered, and a later release rewrites it only when that release breaks
something. A file of that name that isn't this metarepo's request is left alone and named.
The release prints a line per pararepo: staged, with counts, or skipped and why (not in `jig repos`,
on an older jig layout, not citing it, a future `defer_until`, already pinning the release, or
citing nothing it broke). A request that can't be written doesn't undo the tag. jig commits nothing
in a pararepo: the pin is its buffer.

**The family report.** `jig family`, in a metarepo or any of its pararepos, prints the same
report from either, read through the metarepo's checkout and each pararepo `jig repos`
reaches; one it can't reach is named and skipped. It writes nothing and exits 0. Four
sections, each `nothing` when empty: **Staged**, every file in each member's `.jig/staging/`
with its repo, `target`, `kind` and age in days (its file's modification time: staging is never
committed), `stale` past 7 days; **Proposals**, every `propose/` branch in the metarepo not
merged into its trunk, or with nothing written on it, with its age (its opening commit's date;
for an older branch, its first commit past trunk), `empty`, `stale` past 7 days, and the
pararepo specs citing it (`meta: <meta> proposal <branch>`) or `cited by no spec`; **Entries
touching labelled work**, each idea in the metarepo's `.jig/ideas.md` and each entry in its log under `## Unreleased`
whose `Touches:` names `docs/glossary.md § <term>` for a term labelling a scope or item not done
(`rules-roadmap.md`, Roadmap, Labels), with those scopes and their owning repos: a pending ruling each should read
before its next pin; **Two names**, two glossary terms equal once folded as labels are, and two
scope or item ids under different products (the metarepo's own sections count as one) equal
once folded, or one the other with whole hyphen-words added at its start or end. Listed for the
owner, never refused. `jig rig` points at it (`rules-workflow.md`, Workflow).

Two rules for the metarepo's own pages:

- **Newer wins.** A later decision, or a pararepo page a decision makes the authority, overrides
  older page text it contradicts, whether or not that text is marked Accepted. The update changes
  the claim where it lives (What the metarepo holds); when the home is a pararepo, it already
  says it, and the metarepo points. Any restatement elsewhere becomes a pointer to the home. Only
  when the claim lives in the metarepo does the update give the new text, on the decision and the
  pages that cite it as their source; it keeps an old "Accepted (who, date)" only on what it
  still covers. A decision changes only when the stale claim is one: the newer entry supersedes
  it, and the old entry is removed (`rules-decisions.md`, Decision log, Released sections). A pararepo citing the
  removed id hears of it at its next pin bump, with the successor named. A page update needs no new sign-off: the decision behind it is
  already the owner's.
- **Every copy.** A metarepo spec that changes a claim lists every place that states it, found
  by meaning, not only by its words, and its done-when covers each one: the claim's home is
  updated (a decision and the pages citing it as their source; when the home is a pararepo, it
  already says it, and the metarepo points), and every other place becomes a pointer to it.
  The list starts from `jig reading-list --claims <id or term>…`: every tracked line naming
  the decision id (a superseded id hops to its successor) or the glossary term, its peer
  entries by `Touches:`, each marked `home`, `pointer` (a `§` reference or a link to the home)
  or `copy`. It finds names only; a copy in other words is the spec writer's to find.
