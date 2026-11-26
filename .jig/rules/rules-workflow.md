# Workflow rules

## Sync

`jig sync` merges trunk in. A conflict in an `append_files` file where **both sides only
added at the same spot** is resolved automatically: trunk's lines, then the job's. Anything
else stops with the files named, and a person resolves it.

## Workflow

Every session is a node: the hubnode or a subnode (`rules-jobs.md`, Nodes). A subnode takes one of five roles,
each with its own model tier and effort. Workflows are data in `jig.py`: `jig flows` prints
them, `jig next [<job>]` names a job's next step, the node or role that does it, and whether
it continues a session or starts one, and each recording command refuses a step taken out of
order.

**Nodes.**

| Node | Settings | What it does | Roles it may load |
|---|---|---|---|
| hubnode | the owner's session; tier 2, effort 1 or better, ranked as below | talks, decides, assigns, gates, merges, releases, pushes, publishes | spec (only for specs drafted from the conversation) |
| subnode | the role's | takes one role on one job, works only in its worktree, reports back, never touches trunk | any of the five |

**Roles.**

| Role | Tier, effort | Steps it owns | An override must keep |
|---|---|---|---|
| spec | 2, 2 | spec, consolidate | — |
| bug | 2, 1 | bug, then the spec for what it found | tier no worse than spec's; effort no lower |
| work | 2, 3 | work, handoff, fixes, hand-resolved syncs | tier no better than spec's; effort lower |
| review | 2, 2 | review-work (the job's whole diff), review-change (only what changed since the last review); always a fresh session | tier no worse than work's; any effort |
| check | 3, 4 | check (the complete suite, before a release too), trace a failed batch, survey | nothing: fixed commands |

The hubnode's own steps, which are no role's: assign, gate, merge, release, push, publish. jig itself
(no model) refuses a step out of order, and removes a merged job's clean worktree and branch.
One push is the check role's: with `queue.overflow` set (The queue), it pushes and deletes
`jig-check/*` branches for an overflowed complete check, and no other branch.

Tier 1 is the best model the tool has; a higher number is a lesser model. Effort 0 is the
tool's highest; each number up is one level lower. The defaults leave effort 0 free, so a
repo can raise any role. Which model and level a number means is the tool's business, not
`.jig/`'s: the plugin maps them in `plugin/tiers.json`.

**Workflows.** `→` continues a session that already exists (the same one, the hubnode, the
job's work session); `⇢` starts a new one.

| Workflow | Steps | Trigger | Controls |
|---|---|---|---|
| Job | spec ⇢ work ⇢ review-work → handoff → gate ⇢ check → merge | `jig open` | merge only on the owner's word |
| Fix | work ⇢ review-change → handoff | a review with blocking findings | three strikes: a job's third blocking review starts Bug |
| Sync | work ⇢ review-change → handoff | a sync with a hand-resolved conflict | a clean sync needs nothing |
| Bug | bug → spec ⇢ Job | a job's third blocking review, a feedback group, or the owner's `/jig:bug` | never on a session's own reading that something is broken |
| Feedback | consolidate ⇢ bug + spec → consolidate ⇢ Job | staged feedback, in the jig repo (`/jig:rig` starts it; `/jig:fix` by hand too) | one bug + spec per group; overlaps answered before any job opens |
| Batch | gate → merge ⇢ check → trace | two or more gated jobs | one check on trunk; a failure is traced to its merge, then Fix on that job |
| Release | check → release → push → publish | the owner's word | refused while a batch check is owed; push and publish only on the owner's word |
| Survey | survey ⇢ spec ⇢ Jobs | `/jig:survey`, `/jig:adopt`, `/jig:update` | |
| Redocument | spec ⇢ Jobs ⇢ Batch ⇢ Job | `/jig:redocument` | the spec is the remap; the last job is the cleanup |

**Fixed, whatever the config says:** the owner's word before merge, push and publish; a fresh
session for every review; a complete check before a release. The one exception is the owner's
word given once: `queue.overflow`, with the owner's words as its reason, stands for every push of
a `jig-check/*` branch, and for nothing wider. The commit hook refuses it without a reason, and
refuses any other key that weakens a fixed rule. Everything else the hubnode may
propose to reconfigure, with a reason, and apply only on the owner's yes; on a no it continues
with the defaults.

**Session rules.**
1. A session never changes model or effort once it holds context: a model change discards its
   cache, and the next turn re-reads everything at full price.
2. One session per role per job. The work session keeps the build through every fix and sync.
3. A new session starts only when the role changes and the new role needs a fresh context
   (review), different settings, or nothing but files (check).

**Contracts.** Each is a refusal naming the missing step.
- `jig merge <job>` refuses a job not marked gated.
- `jig reviewed --blocking N` records the blocking findings a review left; `jig handoff`
  refuses while the newest review of HEAD has any.
- Strikes are counted per part of a job (a handoff note, `--partial` too, ends a part): each
  review that records blocking findings, full or `--change`, the first review-work included,
  is one, and a clean review between them resets nothing. The third strike starts Bug: the
  next `jig reviewed` is refused, full or `--change`, until a spec for the job carrying
  `Bug-for: <job>` on a line of its own, outside fenced code, is committed in that part. A bug
  spec lifts the limit for the part it was written in only: a later part that reaches three
  strikes needs its own, at a new path, as an earlier part's, edited or moved, counts for nothing.

A review with no blocking findings ends the fixing: the job hands off, as `jig next` says.
Should-fix and optional findings get one round per part; what is left after it gets DEFERRED
rows. A finding that needs behavior the spec never names is a spec change before it is built
(an `Interpreted:` line the hubnode accepts, or the owner's answer), or a No phase item.

**Ranking settings.** A setting ranks by tier first, then effort: a better tier at any effort
ranks above a worse tier at any effort, and within one tier the higher effort ranks above.
Starting a session is compared one setting at a time, since the tool clamps a new session's
model and its effort apart: `jig roles --from TIER,EFFORT` takes the starting session's own
settings and says, under each role, whether to start it with its settings or start it and then
raise its model, its effort, or both, and whether those settings rank below the hubnode floor.
The tier-first ranking is for the hubnode floor only: starting a session and `jig gate`'s
review-line warning (below) compare tier and effort apart.

**Settings in effect.** `jig roles` prints each role's tier and effort. A repo overrides them
in `config.json`, each entry with its reason:
`"roles": {"review": {"tier": 1, "effort": 0, "reason": "..."}}`. An override that breaks the
last column, has no reason, or weakens a fixed rule is refused by `jig roles` and by the
commit hook. There is no per-task override: an instruction about settings for one run stays in
that run's sessions, and `roles` changes only on the owner's word that a setting is standing.
The key's older name, `workflow`, is not read: `jig update --apply` removes it, and jig's
standard replaces what it held; the hook refuses a config holding it. `jig workflow`, the older
command, prints the settings under the old step names (`execute` for work), then the flows.

A spec's `## Roles` section is `jig roles`' output when it was written. The review records the
review role's configured settings (`jig reviewed --tier N --effort N --ran "..."`), the
handoff note carries them, and `jig gate` warns when they are a worse tier or a lower effort
than the spec asks. So the warning catches a review recorded without them, or a config
changed after the spec was written; it can't see a review that actually ran weaker than it
was set to. A spec written before roles has `## Workflow` (with `execute:` and `recheck:`
lines), read alike.

The first review of a job is review-work. After it, a round costs what it changed: a fix, or
a sync resolved by hand, takes a **review-change**, a fresh review of the delta against the
previous findings, at the review role's settings: `git diff <last recorded review>..HEAD` for
a fix, and for a sync resolved by hand `git show --remerge-diff <merge>` and what follows it,
never trunk's work. `jig reviewed --change --tier N --effort N` records it, refused unless a
full review of the job is on HEAD's first-parent chain. The note carries a `Review-change:`
line beside `Review:` (an older note's `Recheck:` reads alike), and `jig gate` warns when
either is below the spec's review line. A review-change widens to a review-work when the diff
changes anything the findings didn't name. What needs no new review at all: a clean `jig sync`
of a reviewed commit, and deferred.md rows whose net change deletes no line (`rules-handoff.md`, Handoff, gate,
merge). Working alone, a review-change leans only on a full review made since the last
handoff note: history can't tell a new task from a fix after a note, so either gets a full
review.

A `Proposed` entry the job adds or changes is a ruling the owner still owes. The job tells the
hubnode when it writes one, the hubnode sends it up while the job builds, and `jig gate` warns,
naming each, but never refuses: the owner may say to gate a job as proposed.

`jig rig` is the repo's picture, the hubnode's entry point: what can start now, what waits on
what, what waits on the owner, and the open jobs with `jig next`'s step for each. It lists four
kinds of item: a **ready spec** (a waiting spec, as The board defines it), a **staged file**,
which a model reading it calls **ready** (it can become a spec as it is) or **open** (it needs
the owner's answers first), and the roadmap's **next step** (`rules-roadmap.md`, Roadmap). Ready items whose Touches
overlap, with no `Kept separate` line, are one job to answer (merged, or kept apart); an item
that depends on another (a staged file's `after:` header, a spec's `Build after <name>` line)
is in the same group and opens after it, with nothing to answer; one that depends on an open
job, named or by its spec's name, or on an item not ready, waits on it, and a dependency
cycle waits on the owner. A move's spec (a `- move:` line) waits on its receiver until step 2
is next, read by `jig move`'s own reader (`rules-pararepo.md`, Moving a claim). An item that could start but overlaps any waiting spec, one that
waits included, is to answer first, since `jig open` refuses it. The order is
fixed (kind, dependency, path), so the same state prints the same bytes. Its count of what
waits on the owner's answers counts every question: each open or unjudged staged file, each
`noted` file and `concluded` feedback report, the open next step, each group with an overlap (once, however many pairs it holds: one job for its
items, or keep some apart) and each dependency cycle, a ring once; `--json` prints it as
data, each group with, per member, the Touches it shares with the rest and whether all of them
are append files (`append_only`): a member that meets its group only in the log is the one most
likely kept apart. In a family, after Waiting on you, rig prints one line when the family
report (`rules-metarepo.md`, The family report) holds a stale staged file, a stale or empty proposal, an entry
or a pair: `Family: <n> stale staged, <m> stale or empty proposals, <k> entries touch labelled
work, <j> pairs of names: jig family`. It counts in neither number: a report, not a question. A staged decisions file's Touches are its entries' `Touches:` lines, less a
pointer into another repo, plus `.jig/decisions.md`, so it meets the spec written from it by
the same rule. A staged file a spec in the tree or an open job's spec carries, by its exact
mark, is **taken**: it waits on that spec or job, in no group, and counts nowhere. A spec in
flight carries: a waiting spec, an open job's spec, or one whose only notes are partial. One a
finished spec still in the tree or a landed, non-partial note's header carries (a whole
`Source:` line), which `resolve` would land writing nothing, is **built**: rig lists it under Finished, and `jig rig --close` resolves it.
A carried file `resolve` would write is never built (a decisions file always: the owner,
2026-11-18; any other kind that `resolve` would write too): it is **noted**, with
what carried it, takes no judgment (`--store-put` refuses it, as it does a taken or built item),
opens nothing, and counts as the hubnode's step (`rules-staging.md`, Staging). Only what the tree holds now counts: nothing is read from
history. In the jig repo a
staged feedback report not taken is a **feedback** item, in no group and counted only as
`feedback`: the hubnode starts `/jig:fix` on it and stores the call `fixing` (keyed on the
report alone, so opening a job doesn't start a second fix), which `--store-put` takes for a
feedback item only. A report `/jig:fix` ends with still staged (nothing reproduced, a note of
what's missing) is stored `concluded`, with what it found as `about`: it leaves Running and
waits on the owner, to drop or keep. A model's open/ready call, its questions and its recommendation are kept per item in
`.git/jig/rig.json` (never committed) with a key of the item's content and the board, and
replayed while both are unchanged: `jig rig --store-put <path>` stores one (a JSON object on
stdin), `--store-get <path>` prints one that still holds, and `--fresh` forgets them all. It
never edits the roadmap, only writes its empty structure where trunk has none (`rules-roadmap.md`, Roadmap), and
touches staging only through `--close`'s resolves. It is called
by name only: `jig next` is unchanged.
It also lists the **finished** specs, which count in neither number: each complete spec (a
landed handoff note that isn't partial names it) that no open job names, and each `Bug-for:`
spec whose job has left the board, with the note that completed it. A spec a cached metarepo
pointer names is kept, saying so, as is a pararepo's spec naming a metarepo proposal or
pointers branch. `jig rig --close`, on trunk in the trunk checkout with a
clean tree and no merge, cherry-pick, revert or rebase in progress, removes them in one commit, `close finished specs: <names>`, each one's `Scope:`
on its note as a merge writes it; then, closing anything or not,
it runs `jig staging resolve` on each built staged file, printing resolve's line. Anywhere else
it refuses and writes nothing.

### Two levels of check

`.jig/scripts/check.sh` has two levels. With no argument it runs the quick part: what runs
on every stop and while working (lint, type-check, unit tests). With `--full` it runs the
quick part, then the complete one (the full suite, slow and end-to-end tests). While working,
the work role runs `check.sh` and the parts its change touched, never `--full`. Review
reruns no check the builder's report shows for the same commit. Only the check role runs
`--full`.

`jig checked --tier N --effort N --seconds S` records a complete run that passed: HEAD, the
check role's numbers, the seconds and the date, in `.git/jig/checked.log` (never committed;
shared by every worktree). It warns when the numbers differ from the check role's. In a
job's gate checkout that no longer holds the commit the job's newest note names, it records
nothing and names `jig gate <job>`. `jig
status` prints the last one's seconds and date: what a complete check costs here.

`jig checked --ci <run url> --tier N --effort N --seconds S` records a complete check that ran
on GitHub Actions (The queue). jig reads the run with `gh run view` and refuses unless it is
this repo's `origin`'s, is the `jig check` workflow on `jig-check/<HEAD's short sha>`, ran HEAD,
completed and succeeded, or when `gh` is missing or can't read it; the record carries the
run's URL as a sixth field. `jig status` and the gate's mark read it as they read a local one.

### The queue

Every test or check run a role starts goes through `jig queue -- <command…>`: it waits for one
of the machine's slots, runs the command holding it, and returns the command's exit code. jig
holds the slot; it never chooses what runs. The slots are OS file locks in `.git/jig/queue/`,
shared by every worktree, so a run that dies frees its slot with nothing to clean up. jig holds
them, not the command, so a process the command leaves behind never keeps a slot. A run
that finds none free prints `waiting for a slot: N running, M waiting` and waits. `jig queue`
with no command prints the slots, who holds them, who waits, and whether a complete check runs.

`queue` in `.jig/config.json` sets it: `width` is the cores one run uses (default 1, `"all"`
for every core), and the slots are the core count over the width, at least 1; `slots` sets
the number outright. `max_load`, a load average per core, stops handing out slots while the
machine's 1-minute load is above it; unset, only the queue counts. The Stop hook's quick check
doesn't queue: it has a time limit, and waiting would spend it.

The complete check runs as `jig queue --full -- check.sh --full`: it also takes the single
full lock, so two complete checks never run at once. With `queue.overflow: {"to": "github",
"reason": "<the owner's words>"}` set on trunk, a complete check that finds every slot held, or
another complete check running, doesn't wait: it exits 3 and prints the route. A wait for
the load alone is still a wait. The check role
pushes HEAD as `jig-check/<sha>`, where `.github/workflows/jig-check.yml` (copied from jig's
template in the same commit as the key) runs setup and the complete check; records the run
with `jig checked --ci` once it passes; and deletes the branch. Without the key it waits.

A single job keeps its own gate check: `jig queue --full -- ./.jig/scripts/check.sh --full`
once in the gate's checkout, `jig
checked` there, then `jig mark <job> gated`, which refuses without that record.

A batch of jobs gated together owes one complete check instead: each is marked `jig mark <job>
gated --batch`, they merge in sequence with `jig sync` between them, and `jig merge` writes
`Check: batch` into each one's merge commit. Then, before a push or a release, `check.sh
--full` runs once on trunk, and `jig checked` there. `jig release` refuses while a merge on
trunk since its last recorded check carries `Check: batch`. When that check fails, `jig
checked --trace [command]` on trunk lists the merges since the last checked commit and prints
the `git bisect --first-parent` run that finds the one that broke it, running only the failing
command at each step.
