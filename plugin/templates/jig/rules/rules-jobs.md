# Jobs: parallel work on one repository

Several sessions change this repo at once. This is how they stay out of each other's way.

**A job** is one piece of work in flight: a *topic branch*, its *git worktree*, and a *CODEOWNERS-style* claim on files.

A handoff is a *pull request*; the gate is a *merge queue* with *branch protection*. The **hubnode** is what others call the *team lead*,
*orchestrator*, or *manager*; a **subnode** is a *teammate* or *worker*. If you already run any of those, you already run most
of a job — `jig survey` names what you have and what it maps to.

The rulebook is the files in `.jig/rules/`, one ruleset each; this is `rules-jobs.md`. Each role's skill names the rulesets it reads.

## Nodes

- **The hubnode** is one session, the owner's. It owns the trunk branch, the board, the
  worktrees, and the merges. It opens jobs, gates handoffs, merges. It builds no feature.
- **A subnode** is every other session. One job and one role each (`rules-workflow.md`, Workflow): its branch,
  its worktree, its files. It never works in the trunk checkout, never commits on trunk, never
  pushes trunk, never merges. A role with no job of its own (a check for a batch or a
  release, a spec from files, a consolidate, a bug for a feedback group) works in a detached
  worktree of trunk's tip and commits nothing: the hubnode commits what it wrote.

**Working alone?** Open no jobs and you are the hubnode of a one-job repo. R1–R5 and R8 go
quiet — a feature branch in your one checkout is nobody else's problem — while R7, the review
record, the handoff note, and the gate all still apply. `jig handoff` names the branch
instead of a job; `jig gate` with no argument gates the current branch. The discipline is
identical; only the coordination disappears.

## The board

Two files on trunk, written only by the hubnode. `.jig/config.json` holds what rarely
changes: `name`, `trunk`, `common`, `append_files`, `reserve`, `release`,
`reference_files`, `roles` (optional; see Workflow), `findings` (optional; see
Documentation), `derived_files` (optional; globs naming every file `.jig/scripts/derive.sh`
writes, which `jig merge` commits) and the layout's `version`.
`.jig/jobs.json` holds the open jobs, nothing else. Per job:

| Key | Meaning |
|---|---|
| `spec` | its spec: a path under `.jig/specs/`, or one line |
| `state` | claimed → building → ready → gated (or parked) |
| `after` | jobs this one is gated behind |
| `owns` | existing files only this job may change while it is open |
| `shares` | existing files it may change alongside others |
| `reserved` | scarce numbers handed out centrally (migration steps, schema versions) |

A job's branch is its name, and its worktree is `.git/jig/worktrees/<branch>`. A job
adopted on another branch, or checked out somewhere else, stores `branch` or `worktree` —
only the one that differs. The day it opened is the commit that added its entry. Merging a
job deletes its entry in the merge commit, so git log of `jobs.json` is the board's history.

`common` and `append_files` are repo-wide. A file new to the repo belongs to whoever makes it.

The docs tree's map is not configuration, so it has its own file, `.jig/docmap.json`, written
like the board on trunk only (R5). It holds `docmap` (each page's globs), `not_docs`, and the
optional `deep_subsystems` and `boards` (see Documentation), and no other key: the hook refuses
a key jig doesn't know or a value of another shape. `jig docmap <page>` prints a page's globs
and whether it is a board or an approved deep subsystem; `jig docmap <path>` prints the pages
covering a file. `not_docs` lists globs where markdown ships as code (skills, templates,
fixtures); `survey` does not look for a home for those files.

**Owns is narrow on purpose.** Before opening a job, `jig open` diffs every open job's
branch against trunk and refuses an `owns` entry another live branch already touched. Those
go in `shares` from the start, or both jobs get blocked on every commit afterward.
It also warns, naming each path, when a backticked path in the spec's Touches section (a
`## Touches`, or a `### Touches` nested under another heading) is in
neither `owns`, `shares` nor `common`; `jig share <job> <path>…` adds paths to an open job's
shares, refusing one another open job owns.

**Overlapping specs are answered before they open.** A spec is *waiting* when no open job names
it, no handoff note's `Spec:` line names it, and the newest release tag doesn't hold it (any spec,
with no tag yet), unless it carries `Bug-for: <job>` on a line of its own, outside fenced code: a bug spec
is built in the job it names and reaches trunk only when that job merges, so it never waits. Nor
does a spec listing buffer rows (`jig propose --buffer`, `jig move-in`), or a move's spec whose
proposal was withdrawn (a `- move:` line and a `meta: … withdrawn` line): each is a proposal's
record, and no job takes it. Two waiting specs overlap when their Touches sections meet, at any heading level: one path, a glob
covering the other's path, or the same `<page> § <term>` (a whole page meets any term on it).
`jig consolidate` lists each group of overlapping waiting specs with the paths they share, as
one proposed job. A group is answered one of two ways: one spec carries every input's `Source:`
lines and the inputs are deleted (the spec role's consolidate writes it), or either spec of a pair says
`Kept separate from <spec>: <reason>`, one line per pair. Until then `jig open` refuses a spec
in the group, and so does `jig staging resolve` for a file whose mark a spec in it carries.
A consolidated spec that takes in metarepo proposals lists their branches under `## Proposals`,
one backticked `propose/<repo>-<slug>` per bullet, in merge order; `jig open`'s kickoff then says
to `jig sync` and merge each into the job's branch in that order.

## The rules

Checked before every commit by a git hook, and by `jig rules`. A delete changes its path, and
a rename changes both of its paths: R3–R5, P1, P2 and P4 count each.

- **R1** The trunk checkout stays on trunk. Work in `.git/jig/worktrees/<branch>`.
- **R2** A job is built in its own worktree. Off trunk, a branch on no job is refused while
  jobs are open, except a `propose/` branch in a metarepo (`rules-metarepo.md`, Metarepo, rule 1).
- **R3** A job changes only its `owns`, its `shares`, `common`, or files new to the repo, and
  adds to `.jig/decisions.md` (`rules-decisions.md`, Decision log), whatever its lists say. There it changes in place
  only a line it added itself, and removes an entry only in adding the accepted one that
  supersedes it; but a log not folded yet keeps its open entries under `## Open`, where they
  change in place or leave (dropped, or moved to `.jig/ideas.md` by the fold), heading and all. It may add to `.jig/ideas.md` (`rules-decisions.md`, Decision log, Ideas) and change it in place.
- **R4** Another open job's `owns` is refused even if this job also lists it.
- **R5** The board is the hubnode's: `config.json`, `docmap.json` and `jobs.json` are edited on trunk only.
  So is the roadmap, the owner's: `.jig/roadmap.json` (`rules-roadmap.md`, Roadmap).
- **R6** A scarce number belongs to the one job that reserved it. A change that makes a
  number matching a counter's `pattern` exist where trunk had none, and the branch doesn't
  hold it, is refused; merging a job takes the numbers it holds, and so does the gate's
  scratch checkout of it (a detached HEAD off trunk); a detached trunk holds nothing. Numbers compare as numbers: `D-002` is 2. A number trunk already has
  is taken by nobody, however many times the change adds it: editing or moving a heading, or
  adding a rule under an existing section, takes nothing. A counter marked `"unique"` also
  refuses a change that adds a second match of one number. Two branches that each take
  migration step 17 corrupt the first database that runs both.
- **R7** A change adding a `WORKAROUND:` comment to code must stage `.jig/ledgers/workarounds.md` too;
  its first row creates the file. jig's own `jig.py` quotes the marker and is not checked.
  Prose may quote the marker.
- **R8** A job is gated only after the jobs in its `after` have merged.

**The hooks run trunk's copy of `jig.py`** (`git show <trunk>:.jig/jig.py`). A branch
cannot weaken the rules it is judged by, and a stale checkout is still judged by today's rules.
While a merge of trunk is being finished, a change is judged against trunk, so what trunk
brought in is not the job's.

**A bug in `.jig/jig.py`, a ruleset in `.jig/rules/` or a skill is the tool's, not this repo's.** Say what
in jig broke and tell the owner, then stop; the owner decides whether to run `/jig:feedback`.
Don't patch them; don't ledger it.

## Keeping merges mechanical

Conventions so two jobs rarely meet in one hunk:

- Append, never edit, shared prose. A change to someone else's section is a note in yours.
- Two jobs sharing a page each add their own section under their own name. A name both chose
  is refused at the merge that would join them (`rules-docs.md`, Documentation), so no number is reserved for
  it; two names for one thing are for fold-in and review to catch.
- A file of one's own: new routes in your own handler registered by one line; new state in
  your own module; new tests in your own file; a new fixture as a new file.
- Scarce numbers come from the board (`--reserve`, `jig reserve`), never from looking at what seems free.
  Two branches that both take migration 17 corrupt the first database that runs both.
- A file generated from several sources that separate jobs change (an index of a folder, a
  reference built from every module) is written on trunk by `.jig/scripts/derive.sh` at each
  merge and listed in `derived_files`, never on a branch: each job's copy differs, and two
  branches' copies merge into a wrong file, or conflict. Not such a file: one built from a
  single source, regenerated in the job that changes that source (`check.sh` may compare it);
  one the merge can't rebuild (made by hand, on special hardware, or too slow for every merge);
  and a lockfile, which a branch's own build needs, so its job commits it.

## Reserved numbers

Some things are scarce across the whole repo: migration step numbers, schema versions,
anything a runner stores and compares. Each counter in `config.json` says how
to find its numbers:

```json
"reserve": {
  "step": {"pattern": "^-- step (\\d+)", "files": ["db/migrations/*.sql"]},
  "schema": {"pattern": "SCHEMA_VERSION\\s*=\\s*(\\d+)", "files": ["**/storage.py"], "unique": true}
}
```

A number is taken where trunk had no match for it, in any of the counter's files, and the
change adds one. So editing the file that opens `-- step 17`, where trunk has it, takes
nothing, and a new file opening `-- step 18` takes 18. `"unique": true` is for numbers that
must also appear once: a second `SCHEMA_VERSION = 17` where trunk has one is refused as "17
already exists". It is off unless set, because some numbers rightly appear more than once. It
applies working alone too, with no job open: there is nobody to take a number from, but a
second 17 still breaks. A pattern that captures only the whole part of a dotted number counts
`17.2` as 17, so a dotted number under a whole number trunk already has takes nothing.

`--reserve <counter>` hands the job max(the highest on trunk, the highest an open job
holds) + 1, so two jobs open at once never get the same number. `jig reserve <job> <counter>`
hands an open job another by the same rule; it then holds a list. Nothing stores a "next":
the files say what is taken, and a counter without `pattern` and `files` is refused.

A job holding step N lists the job holding N−1 in `after`, so they merge in order: a
database already past a number never runs a step of that number that merges later.

## Hooks are opt-in per checkout

`jig install-hooks` writes `.git/jig/enabled`. Anything outside this repo that hooks into
your editor or agent runs this repo's `.jig/scripts/` only when that marker exists; `.git/` is never
cloned, so a fetched repo cannot enable itself.
