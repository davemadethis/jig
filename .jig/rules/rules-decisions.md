# Decision log rules

## Decision log

Every repo keeps one log, `.jig/decisions.md`, which `jig init` writes: what was decided and
why, and what changed, grouped by release. Its format is Keep a Changelog's, plus decision
entries; it opens with two lines saying so, that versions are MILESTONE.FEATURE.PATCH (`rules-release.md`, Versioning), and what breaking means here. Then two kinds of section, top to bottom:

- `## Unreleased`: accepted entries and change lines since the last release.
- `## vX.Y.Z - YYYY-MM-DD`: one per release, newest first, with a plain hyphen.

**A decision entry** is a heading with the id and title, never a status, then a status line,
then a `Touches:` line, then the body: what was decided, why, and what it is not. An entry is
about the product (`rules-docs.md`, Documentation, Product and project): a priority order, a delivery queue or
a phase is the roadmap's, never an entry, and an entry names no spec, handoff or scope.

```
### D-012 Store opens graph.sqlite read-only
Accepted (the owner, 2026-11-10). Supersedes D-007.
Touches: docs/store/store.md

When anything but the indexer opens graph.sqlite, it opens it read-only. …
```

**Touches** names the pages the decision rules on, comma-separated, as pointers
(`<repo>/<path>`, `<repo>:<path>`, or a path of this repo's own), each page in either form. A
page is a docs page: under `docs/`, or a file `docmap` names; in a metarepo, a page under
`docs/`. A pararepo names its metarepo's page for anything they share (a product, feature,
principle or concept: `<meta>/docs/<genre>/<page>.md`, read from the cache at the pin) and its
own pages for what is its alone; a metarepo names only its own pages; a repo with neither names
its own docs pages. A bare `docs/…` is always this repo's page: a metarepo named `docs` is
reached as `docs:<path>`. With no cache at the pin, a metarepo pointer is checked for its shape
only, a docs page. Pages are the shared vocabulary, so two repos laying one feature out in
different folders still meet on it. An entry already on trunk with no `Touches:` passes until it
changes, and so do the entries `jig update --merge-log` converts from a register; `jig update`
lists each one to backfill.

Not every decision rules on a page. One that rules on a term, such as how products are named,
names it in the glossary: `docs/glossary.md § <term>` (`<meta>/docs/glossary.md § <term>` from
a pararepo), the term a heading there at any of its three levels, matched whole. A genre's
term is its glossary heading. `§` names a glossary term only, never a heading of another page,
and a term holding a parenthesis can't be named. A term may hold a comma: what follows it up
to the next pointer is the term's. One that rules on no page and no term, such as a rule for
the whole repo, says so as the whole line: `Touches: none — <reason>`, with an em dash or
` - `. The review reads the reason.

**The rule sentence.** The body opens with what the decision rules, as *When <situation>,
<outcome>.*, or *Always, <outcome>.* Two entries that contradict each other govern one
situation with different outcomes, and this sentence is where a reader sees that side by side.
No hook judges it; the review reads it.

**Peers.** Two live entries are peers when their `Touches:` name one page, in either form, or
one names a page above the other's, or both name one glossary term. A pointer to the whole
glossary meets every term, and a term never meets the pages of its genre. An entry that
touches none has no peers. Peers come from this log; in a pararepo, from the
metarepo's log at the pin; in a metarepo, from each registered pararepo's log on its trunk
(`jig repos`). A log jig can't read (no cache, a cache at another pin than the pin, a pararepo
not found) is named. `jig decision <id> --peers` prints an
entry's peers with their rule sentences. The entry may be in any log read for peers, this one
first; `<repo>/<id>` picks the log when the id is in more than one. In a metarepo, `jig survey` names each of its pages
two pararepos' entries touch while none of its own does: that ruling is probably the
metarepo's.

The status is `Accepted (who, date).` The log holds decisions only. Only decision entries say
who decided. A rejected entry is removed; git and its spec's Alternatives keep it.

**Ideas.** What is still to be researched before it can be decided, scoped, built and
documented is an idea, in `.jig/ideas.md` beside the log, which `jig init` writes. It opens
with `# Ideas` and a line saying what it holds; then its entries, one after another, with no
sections. An idea is an entry in the decision entry's form, with an id from the log's counter
(a branch writes `D-?<slug>`, `jig merge` numbers it in either file, one id names one thing
across both), and the status `Open (date).` or `Proposed (date).`, optionally ending
`Supersedes <id>.`. `Proposed` means an answer is put forward. An idea changes in place, and
leaves in one of three ways: decided, its block moves with its id to the log's `## Unreleased`
as `Accepted (who, date).`; dropped, removed with no line, as a rejected entry is; or, in a
repo of a family, moved down, up or sideways with a move line, as an entry moves (Released
sections). A question that binds others is
written as an idea when it is asked, so it can be cited before it is answered. An idea is
labelled by a line of its own after its status line, `(labels <term>, …)`, each
label a term of the glossary a scope's labels name here, checked by the same rule and refused by
line. Against the repo's own glossary every label line is judged, so a glossary change that
drops a term an idea names is refused. Against the metarepo's (a family planning from its
roadmap), only the label lines a commit adds or changes are judged, since the metarepo changes
its glossary in commits of its own; with the metarepo out of reach they pass with a warning, as
a roadmap's `Scope:` lines do. A log not folded yet keeps its ideas under `## Open`, and their
label lines are judged the same way. `jig decision`, `jig reading-list` and peers read both
files; `jig reading-list <paths>` shows each page's ideas. `jig ideas [--label <term>]` is the
research list: each idea with its status, labels and touched pages, a not-yet-folded log's
`## Open` entries included, in a metarepo each registered pararepo's too, read on its trunk and
named by repo. A log from before the ideas file kept them under `## Open`: `jig update --apply` folds
that section into `.jig/ideas.md`, ids and blocks byte for byte (in a metarepo, `jig update
--apply --fold-ideas` in a job), and then the hook refuses an `## Open` heading or an open or
proposed entry the log adds.

**Change lines** follow the entries, in Keep a Changelog's groups and order: `### Added`,
`### Changed`, `### Deprecated`, `### Removed`, `### Fixed`, `### Security`, an empty group
left out. A line is one change, with an area prefix where it has one (`GLOSSARY: Add "vault"`).
A change that is a decision is recorded once, as its entry; the one duplicate allowed is a
`**Breaking:** … (D-007).` pointer in its group.

**What belongs**: a choice that outlives its spec, and any change a reader of the release can
act on. A spec's own Decisions stay with the task, and history stays in git.

**Writing it.** Anyone writing the log writes for anyone deciding whether to take this release:

- Lead with what changes for that reader, in their words, not the code's. One change per line,
  in the imperative or the past tense, the same throughout a section.
- Say what a reader must do when they must do it: a breaking change says what to change, in a
  `**Breaking:**` line; it doesn't set the release's level (`rules-release.md`, Versioning).
- No commit hashes, file lists or internal names a reader can't act on; link a page by its
  heading instead.
- Deprecate before removing: a removal names the release that deprecated it.
- A yanked release keeps its section, with ` [YANKED]` on its heading and one line under it
  saying why and what to pin instead.

**Ids.** A branch writes `D-?<slug>` (`D-?store-ro`), so no job waits for a number, and pages
can cite it before the merge. `jig merge` numbers each entry the merge brings into the log,
after the highest the log has, in every file the merge changes, with the repo's prefix (a
metarepo's `decision_prefix`, `D-` elsewhere), and lists each number in the merge commit's
message. Only an id with an entry is numbered: the same text with no entry behind it is left
alone. A merge that stops on conflicts numbers them with `jig merge --number`, once they are
resolved and added, before its commit. On trunk an id is a number: M2 refuses a `D-?<slug>`
entry there, and `jig release` refuses to release one.

**Released sections.** The log shows what holds now; git keeps what held before. A reversed
decision is a new accepted entry whose status line ends `Supersedes D-007.`, and the commit
adding it removes D-007's whole block (its heading through the line before the next heading), wherever it
sits, a released section included. A release keeps its change lines: they are what that version
told its readers, and a reversal still goes in the new release's group as a `**Breaking:**`
line. Any other change to a released section is refused, except adding ` [YANKED]` and its
line, and adding or changing an entry's `Touches:` line, which says what the entry is about,
not what it decided (M2 checks its pages); and so is removing an entry no accepted entry supersedes: an open or proposed entry may
name what it would supersede, and retires nothing until it is accepted. The one other removal is
a struck entry, project scope rather than a decision (`rules-docs.md`, Documentation: Product and project): the
commit removing it adds, under `## Unreleased` `### Removed`, a line naming its id
(`- D-040: project scope, not a product decision.`). In a repo of a family (`rules-metarepo.md`,
`rules-pararepo.md`) the other is a move: a claim handed to the repo of the family that owns it, down to a
pararepo, up to the metarepo, or sideways to another pararepo (`rules-metarepo.md`, What the metarepo holds), whose
line is its forwarding address, a pointer to its new home: `- D-040: moved to
app/.jig/decisions.md § D-016.`, and for a page or a section `- docs/ui.md: moved to
app/docs/ui.md.` or `- docs/ui.md § Build: moved to app/docs/ui.md § Build.`. An idea moves
the same way, in any direction: its target is `<repo>/.jig/decisions.md § <id>` or
`<repo>/.jig/ideas.md § <id>`, the hook looking the id up in either file there (`jig move`
writes the log form); its moved-from line is in the receiver's log, as an entry's is; and it
leaves this ideas file in the commit writing its move line (`jig move` step 2). An idea or a page needs no
line to leave, but takes it all the same, so readers see it moved, not removed.
These are the only two reasons a `### Removed` line lets a released entry go; any other text
lets nothing go, and the refusal names both lines. The hook checks a move line the commit adds:
the line is under `## Unreleased` (a move line anywhere else is refused, and nothing reads
one there); it is the only move line for its id, page or section, in the log or the commit (a line not
yet released may be corrected in place);
the repo is of this one's family (a metarepo's `pararepos`; for a pararepo, its metarepo and the
`pararepos` its metarepo's trunk lists), and a repo with no family is refused, saying so; a moved
id is an entry this commit removes, not
one an accepted entry supersedes (its successor is what moves); this repo no longer has the
page or section; and the target is on that repo's trunk, read through `jig repos` (an id as an entry
heading in its log or its ideas file, matched by number, a heading as `§` resolves), whose log there has the
**moved-from line** naming this repo's thing ("land it there first, with its moved-from line").
The moved-from line is the move's record at the receiving end, under `## Unreleased` `### Added`:
`- D-016: moved from meta/.jig/decisions.md § D-040.`, `- docs/ui.md: moved from
meta/docs/ui.md.` or `- docs/ui.md § Build: moved from meta/docs/ui.md § Build.`, one form for ids,
pages and sections, as the move line is. A `D-?<slug>` written there is numbered with its entry
at the merge, an idea's as an entry's, its moved-from line in the log all the same. The hook checks a moved-from line the commit adds: it is under `## Unreleased`
`### Added` (anywhere else it is refused, as a misplaced move line is); its repo is of the family;
and on that repo's trunk the thing is still there (the move pending), or that repo's move line
for it points here; neither, it is refused, naming the file it read. A commit removing or
rewriting a moved-from line is refused while that repo's trunk has a move line pointing here: it
is that move's record. Family members are matched by checkout, as `jig repos` finds them, so an
alias is no stranger; a pararepo whose metarepo can't be reached reads no family, and its lines
pass with a warning naming the metarepo. An entry that supersedes a
moved id is refused: its home is the other repo now. It refuses a target that repo lacks, naming
the file it read, and passes with a warning when the repo can't be reached. Released, the line is
frozen like any change line, so the map from old id or path to new home needs no history: a
supersedes chain that reaches a moved id ends at its pointer, and `jig decision`, `jig
reading-list --claims`, `jig sync` and the pin-bump request name it. At the receiving end, `jig
decision <id>` prints `moved from <pointer>`, and `jig reading-list --claims` names it. Before the log, a register row struck so
says `struck` in its Status cell, and `--merge-log` leaves it out, its number still taken. `jig decision <id>` prints an
entry and its supersedes chain, newest last; for a removed id it reads the entry from git, with
the commit and release it stood in, and names what holds now. `jig update` lists a superseded
entry an older log still holds, to remove.

**Checked** in every repo, by the hook, whenever a commit touches the log: each entry's status
line and date, an accepted entry's who, supersedes links that resolve (to an entry in the log,
or in trunk's history of it; a shallow clone, which can't say, passes them), one entry per id,
that a release or `## Unreleased` holds accepted entries only, and that an entry added or
changed has a `Touches:` line whose every page and glossary term is there, or `none — <reason>` (M2); and the released sections.
On a branch, the log is judged from where the branch left trunk, as M3 is, so a later commit
may correct an earlier one as their squash would: a section is frozen once trunk has it.
`jig release` renames `## Unreleased` to the version's heading and adds an empty one above it.
A repo that never releases just grows Unreleased.

**Before the log.** A repo whose trunk has no `.jig/decisions.md` yet, a metarepo `jig update`
hasn't moved to it, keeps the rules it had: its register's rows are M2's, M3 asks for a line in
its `CHANGELOG.md`, which any job may add to, and the release writes the version's heading
there (`## vX.Y.Z — YYYY-MM-DD`). Staged decisions land in the register as rows. The log's rules
start with the commit that adds it.

`jig update` lists a root `CHANGELOG.md` and the register as files to review and changes neither
on its own. `jig update --merge-log` shows the log they would make; on the owner's yes,
`--apply --merge-log` writes it and removes both:

- each release section keeps its lines as written, its heading in the log's form, and an
  `## [Unreleased]` is the log's one `## Unreleased`;
- an open or proposed row becomes an idea in `.jig/ideas.md`, keeping who proposed it;
- an accepted row becomes an entry in the oldest release whose lines name its id, ranges
  (`D-029–D-044`) included, or under `## Unreleased` when none does, a row superseded by
  another becoming the one the newer entry supersedes, dated when it was accepted;
- a rejected row is left out, since git keeps it; the log's preamble names its id, so the
  number stays taken;
- a note that names one id joins that entry's body;
- in a metarepo, `entry_files` names the log in place of what was merged; in the board,
  `append_files` and a `reserve` counter over the old files count the log instead, every id
  it names included.

Nothing the owner wrote is dropped. What has no place in the log (a preamble, a note naming
several ids, a section of its own) stays in its old file, which keeps only that, and the run
lists each piece to move by hand. It also lists every file that still names the old ones, to
repoint. A row's words are kept: a decision that opens with a status word goes under a plain
`Decision` heading, and a row with no who says `not recorded`. A who is any text before the
last date, as a row's note was, so every row the old M2 took converts; one it refused is refused
here too, before anything is written. In a metarepo the merge is a change to its files, so it is
a job: run on trunk, `--apply --merge-log` refuses and names `jig open`; in the job's worktree it
writes everything but the board, the job merges like any other, and `--apply --merge-log` on
trunk then rewrites the board (R5). Elsewhere it runs on trunk, board included. The log's rules
judge the change that merges the old files away, one that adds the log and no longer holds
CHANGELOG.md's sections or a register's rows; one that adds a log beside them is still judged by
the old rules, as is everything until trunk has the log. A repo with neither file gets an empty log from `jig update --apply`,
and `jig init` writes none beside them, leaving them for the merge. Numbering, by `jig merge`,
a counter or the merge, starts above every id the log has ever named, so a rejected one's is
never given again. A pararepo's bump across the merge reports the register's move on one line, and only the
decisions whose title or status changed.

A **folder of decision records** is the ADR layout (adr-tools, MADR): a folder that directly
holds two or more files named `<n>-<slug>.md` (`adr-` before the number allowed, `template` in
the name never a record), each with a status jig reads (below), one of them decided (accepted,
superseded, rejected or deprecated): a front-matter `status:`, a `Status:` line or list item, or
the first line under `## Status`. A migration's `applied` or a book's chapters in `draft` make no
such folder. Its other Markdown files, an index or a template,
belong to the folder but are no records. `jig init` writes no log beside it, `jig update` lists
it, and `--merge-log` turns each record, in number order, into an entry with the next id above
every one the log has named, never its own number:

- `accepted`, `in force` and `approved` become `Accepted (<who>, <date>).`, the who from a
  `decision-makers` or `Deciders` field or `not recorded`; `proposed` and `draft` become
  `Proposed (<date>).` and `open` `Open (<date>).`, as ideas in `.jig/ideas.md`; `superseded by N` (or
  `superceded`) is accepted, and N's entry supersedes it; `rejected` and `deprecated` are left
  out and listed. Any other status, two records with one number, a superseder that is no record
  or is left out, and a numbered file with no status are refused before anything is written;
- the title loses its number; a relation naming a record by number (`amended by 0033`, `Amends
  0001 and 0002`, `supersedes`, `replaces`) names its new id, and one it can't map is listed;
  fields jig doesn't map stay as `Key: value` lines, each heading
  becomes a bold label paragraph, relative links are rebased to the log's folder, and a last line
  names the record (`Record 0001 before this log.`), so a citation left in history can be
  followed. A date missing takes the day git added the file, and the run lists it;
- accepted entries go after `## Unreleased`'s last entry, before its change lines, the ideas
  at the end of `.jig/ideas.md`. Into a log in use too: its entries and lines stay byte for byte, and the
  run says which ids it appends. A `CHANGELOG.md` or a register still goes only into an empty
  log, since their ids are the log's own form, and the run names each it leaves;
- in the same change, every tracked Markdown file's citation of a record (a path or link to its file,
  `record N`, `ADR N`, `ADR-N`) becomes the entry's id. Handoffs, fenced code, released sections
  and the log's own entries stay as written, and so does any other file, since a string in code
is behaviour: its matches are listed, to change by hand. The run lists each line it rewrites, each
  citation it can't (a record left out), each file still naming the folder, and each line of the
  new entries the hook would refuse (a spec path, a root document), to edit before committing;
- the records go, and so do the index's rows linking to them; the index goes when nothing else
  is left in it. What remains is kept and listed. On trunk, `append_files` or a `reserve`
  counter naming the index, kept or not, or a record counts the log instead; merged on a
  branch, `--apply --merge-log` on trunk after it rewrites the board.

The commit of that output passes as written: a converted entry whose record the same change
removes needs no `Touches:` yet, as a register's rows don't: a record in a record folder where
the change began, each claimed by one entry. One added later does.
