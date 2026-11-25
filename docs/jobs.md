# Jobs

A [job](glossary.md#job) is how several sessions change one repo at the same time without
stepping on each other. Each job gets its own branch, its own worktree and its own files, its
[owns and shares](glossary.md#owns-and-shares), listed on the [board](glossary.md#board). Git
hooks refuse any commit that strays outside them. Finished work goes through a
[handoff](glossary.md#handoff) and a [gate](glossary.md#gate) before it merges. It's a small
version of what teams already do with topic branches, CODEOWNERS and a merge queue, checked at
every commit.

## The board

The board is two files on [trunk](glossary.md#trunk). `.jig/config.json`
holds the settings that rarely change. `.jig/jobs.json` holds the open jobs, and nothing else.
Only the [hubnode](glossary.md#hubnode) edits either one, on trunk, and `.jig/docmap.json`,
the map of which docs page covers which files, the same way.

Each job on the board has:

| Key | What it holds |
|---|---|
| `spec` | the job's [spec](glossary.md#spec), a path or one line |
| `state` | claimed, building, ready, gated, or parked |
| `after` | jobs that have to merge before this one |
| `owns` | files only this job may change while it's open |
| `shares` | files it may change alongside other jobs |
| `reserved` | scarce numbers it holds, like migration steps |

Merging a job deletes its entry in the merge commit. So `git log .jig/jobs.json` is the board's
whole history.

## Owns and shares

Owns and shares are the job's two file lists. Keep owns narrow.
Before a job opens, `python3 .jig/jig.py open` checks every open branch. It refuses to give this
job a file that another branch has already touched. Those files go in shares from the start.

A file that's new to the repo belongs to whoever makes it. A few paths are common to every job,
listed in `common` in the config. Any job may add to the [decision log](glossary.md#decision-log).

`python3 .jig/jig.py share <job> <path>` adds a path to an open job's shares later. It refuses
one that another open job owns.

## Worktrees

Every job is built in its own worktree, at `.git/jig/worktrees/<branch>`. The trunk checkout
stays on trunk. A [subnode](glossary.md#subnode) works only in its job's worktree and never
touches trunk. When a new worktree is made, a hook runs `.jig/scripts/setup.sh` there, so
every job starts with its dependencies installed.

## Rules from trunk

The git hooks check eight rules before every commit:

- **R1.** The trunk checkout stays on trunk.
- **R2.** A job is built in its own worktree. While jobs are open, a branch that's on no job is refused.
- **R3.** A job changes only its owns, its shares, the common paths, or new files.
- **R4.** Another open job's owned file is refused, even if this job lists it too.
- **R5.** The board and the [roadmap](glossary.md#roadmap) change on trunk only.
- **R6.** A scarce number belongs to the one job that reserved it.
- **R7.** A new [workaround](glossary.md#workaround)'s `WORKAROUND:` comment needs its ledger row in the same commit.
- **R8.** A job is gated only after the jobs in its `after` have merged.

The hooks run trunk's copy of `jig.py`, not the branch's. A branch can't weaken the rules it's
judged by, and an old checkout still gets today's rules. `python3 .jig/jig.py rules` runs the
same check by hand.

## Reserved numbers

Some numbers are scarce across the whole repo: migration steps, schema versions, anything a
runner stores and compares. Two branches that both take migration 17 corrupt the first
database that runs both. So numbers come from the board. `python3 .jig/jig.py open --reserve`
hands one out when a job opens, and `python3 .jig/jig.py reserve` hands out another. The hook
refuses a number the branch doesn't hold.

## Handoff

A handoff is a mergeable chunk, not the whole job. The work session
runs its checks. Then a fresh session reviews the diff, seeing only the diff, the spec and the
rules. It never sees the conversation that wrote the code. Whoever dispatched the review
records it with `python3 .jig/jig.py reviewed`, along with how many blocking findings it left.

`python3 .jig/jig.py handoff` then writes a note naming that exact commit. It refuses while the
newest review still has blocking findings. The work session fills in every heading of the note,
including which docs pages its change touched, and commits it with the work. A fix after a blocking review gets a review of only
what changed. A job's third blocking review stops the loop and starts the bug
[workflow](glossary.md#workflow) instead.

## Gate

The hubnode runs `python3 .jig/jig.py gate <job>`. A gate refuses a job
whose `after` jobs haven't merged, or one with no handoff note. Then it sets up a scratch
checkout of the noted commit, with trunk merged in. It prints the complete check to run
there, but it never runs it. A check session, in the check [role](glossary.md#role), runs it
there and records the pass with `python3 .jig/jig.py checked`.

Then the hubnode runs `python3 .jig/jig.py mark <job> gated`, which removes the scratch
checkout, and commits `.jig/jobs.json` on trunk. The mark refuses until the check is recorded.

## Merge

`python3 .jig/jig.py merge <job>` happens only on the owner's word, and only for a gated job.
In one commit it merges the branch and deletes the job's entry. It also numbers any new
decisions and removes the finished spec, keeping its `Scope:` and `Later:` lines on the handoff note. It then prints "Sync the clean jobs", and the hubnode
runs `python3 .jig/jig.py sync` in each clean job's worktree. After the commit it removes the job's worktree and branch, if the worktree is clean.

Two or more gated jobs can merge as a [batch](glossary.md#batch), with one complete check on
trunk afterward. A batch that fails is traced to the merge that broke it.

## Sync

`python3 .jig/jig.py sync` brings trunk into a job. In the append files (`append_files` in the
config, plus the decision log), lines both sides only added resolve themselves. A clean sync
needs no new review. Anything else stops with
the files named. A sync resolved by hand gets a review of what changed before the next handoff.

## Bugs

A bug is investigated before anyone writes a fix. The bug role asks why, up to three times. It
tags every fact it relies on as `[seen]` or `[assumed]`, and looks one layer up for a sibling
path that doesn't have the problem. Then it says plainly whether the fix corrects the cause or
patches the symptom. It ends with a spec for what it found.

The bug role runs when a workflow calls it, or when the owner types `/jig:bug`. A session
never starts one on its own hunch that something is broken.

## Workarounds

A patch is allowed. Each one is a workaround: a `WORKAROUND:`
comment in the code, and a row in `.jig/ledgers/WORKAROUNDS.md`. The hook refuses the commit if
the row is missing, so nothing gets patched quietly.
