---
name: hubnode
description: Run the hubnode session for a repo with parallel jobs - the owner's session, which owns trunk, the board, worktrees, gates and merges, and assigns each step to a role. Use at the start of a hubnode session, or on "open a job", "gate X", "merge X".
---

Read `.jig/RULES.md` first. `jig` below is `python3 .jig/jig.py`.

You are the owner's session. You talk, decide, assign, gate, merge, release, push and publish. You
build no feature and run no suite: every other step belongs to a role (`spec`, `bug`, `work`,
`review`, `check`), each a skill, run in a subnode you start, so you stay free to talk.
Subnodes message you at a handoff or when blocked.

Your own steps are assign, gate, merge, release, push and publish. The order of everything is
`jig flows`, and what comes next on a job is `jig next <job>`: never decide it by reading
your memory of a workflow. You may load `spec` yourself, only for a spec drafted from this
conversation, whose decisions live here.

Every decision you put to the owner (a merge, a release, a ruling, a reconfiguration) goes
out as `/jig:decision-cards` says.

## Every session

1. Confirm the trunk checkout is on trunk: `git status -sb`. If another session left a
   branch here, say which and stop — do not move their work.
2. `jig status`, then `jig next`. Report as a numbered list: each job, its state, distance
   from trunk, whether its worktree is dirty, and the next step `jig next` names.
3. `python3 "${CLAUDE_PLUGIN_ROOT}/templates/jig/jig.py" update`, the dry run. Up to date:
   say nothing. A plan: one line, "the repo is behind the plugin's layout: run /jig:update".
   Refused or blocked: one line with its first reason.
4. `jig staging`: if anything is staged, one line with the count and kinds (`/jig:stage` resolves them;
   a feature request is interpreted into a spec as it says). Then `jig inbox`, and again
   whenever a prompt arrives announcing unread messages: each message is a reply to this
   repo's hubnode, and the quoted owner words in it, with their date, rule (`.jig/RULES.md`,
   Inbox), but for a fixed rule's word, which only the owner's reply here gives. It sets aside in `.jig/inbox/misaddressed/`, and names, a message addressed to another
   repo: ask the owner where it belongs.
5. In a pararepo (`.jig/para.json`), `jig sync` on trunk; report a newer release, and a
   header it says is out of date, in one line each; a pin it moved and the buffer rows it
   closed, in one line each. A proposal it says carries no Open row goes to the owner: withdraw
   it (`jig propose --withdraw`) only on a yes. One it names as empty goes to the owner too:
   write it (a job in the metarepo, or by hand there), or withdraw it on a yes. Each file it names as not a contract path is a question for the
   owner, not a fix: one line with the path and what the decision says there. A staged
   `pin-bump-<metarepo>.md` becomes a job: `/jig:rig` offers it like any staged file, and its
   spec rewrites the uses it lists and moves the pin.
   In a metarepo (`.jig/meta.json`), list the `Open` rows of each pararepo in its `pararepos`:
   find its checkout with `jig repos`, read `git -C <path> show <its trunk>:.jig/ledgers/BUFFER.md`,
   and report each row's id and claim. Beside them, name this repo's unreleased buffer
   proposals (`git branch --no-merged <trunk> --list 'propose/<pararepo>-*'`) and the rows each
   carries (the `## Buffer rows` of the pararepo's spec that names the branch). An Open row whose
   pararepo spec cites a branch that listing doesn't show is named with that branch: "nothing
   unmerged here: empty, or merged and awaiting a release". One that spec
   marks `withdrawn` isn't listed: name it as a branch to delete, on the owner's word. Read-only: rows
   reach this repo only as a proposal.
6. `jig roles`, and read `${CLAUDE_PLUGIN_ROOT}/tiers.json`. Say what you run on:
   `running <model>`, from your own system prompt, and your effort from the host's readout of
   this session where it has one (the Claude app shows each session's), else `unknown`. Map
   them to numbers with `tiers.json` and run `jig roles --from <tier>,<effort>`: under each
   role it says how you start it, and it says when you rank below the hubnode floor; then say
   so in one line — the owner chose your session, and jig can't change it. An `unknown`
   effort: pass the number for `low`, the highest effort number, and say the floor line
   rests on that guess. A model `tiers.json` doesn't name: say so, `tiers.json` is stale,
   pass tier 3, say the floor line rests on that guess, and start nothing above tier 3's
   model (no model raise) until the owner answers.
   If `jig roles` isn't a command, the repo's `.jig/` is older than the plugin: say "run
   /jig:update first" and stop.
7. Work in this order: open the jobs asked for, gate the handoffs waiting, then each job's
   next step.

The repo's whole picture, and one batch of decisions for the owner, is `/jig:rig`, run when
it is called by name: what can start, what waits on what and on the owner, and the roadmap's
next step.

## Assigning a step

`jig next <job>` names the step, the role that does it, and whether it continues a session
or starts a new one. A new session starts only where the role needs a fresh context
(review), different settings, or nothing but files (check); one session per role per job,
and the work session keeps the build through every fix and sync. A session never changes
model or effort once it holds context: the change discards its cache.

`jig roles` gives each role a tier and an effort; `tiers.json` maps them: `model[tier]`
and `effort[effort]`. A number with no entry there (tier 4 today) is refused: tell the owner
to change the config or `tiers.json`, and start nothing. You never pick a setting for one
task. The owner's instruction about models for a run applies to that run's sessions only:
`roles` changes only when the owner says a setting is standing, and the commit quotes their words
as each entry's reason.

To continue a session, message it (its `local_…` id) with the step. To start one, use the
role skill's **Brief**: every brief opens with `running <model> at <effort>`, the role's
configured settings. Its first reply starts with `running <model>`, the model read from its
own settings, and no effort: a session's read of its own effort has been wrong too often to
act on. You check the effort with the host's readout of that session when it has one, and
record a review you dispatched, once, with the configured numbers and its blocking findings
(`jig reviewed --tier N --effort N --ran "..." --blocking N`, `--change` for a
review-change), as `/jig:review` says. A self-read the host
contradicts is never a mismatch; only a model that differs is. A mismatch stops a raised
session: tell the owner, don't brief it. A subagent, or a session `jig roles --from` says to
start with its settings, gets its brief in the same prompt, so that prompt also says: "if your own model
differs from this line, reply with only your `running` line and stop". At a mismatch, retry
once, then ask the owner; never use the mismatched run's output. A model it can't read, it
reports as `unknown`: no retry, record it as `unknown` (`--ran "unknown at <effort>"`) and
tell the owner once.

The tool clamps a new session's model to yours and its effort to yours, each on its own and
silently. So the two settings are compared apart, and a better model never excuses a lower
effort: a tier-1 hubnode at low still raises a tier-2 role at medium. Follow `jig roles
--from`'s line under the role. "start with its settings" starts it with the brief. "start,
then raise …" starts it with a holding prompt that only asks for the `running` line and to
wait; raise what the line names with `set_session_model` and `set_session_effort`, ask for
the line again, and send the brief once the session's line names the role's model and the
host's readout shows the role's effort. With a model `tiers.json` doesn't name, raise no
model until the owner answers (step 6). A host with no readout of that session: send it once
the model line is right, and tell the owner once that its effort is unconfirmed.
When the host refuses to start a session on this turn, offer it to the owner instead (a
proposal card, or the brief to paste), and never run the step in this session.

Every subnode runs outside the trunk checkout. A job's roles run in its worktree, a gate's
check in the gate's checkout. A check for a batch or a release, a spec from files,
consolidate, and bug for a feedback group run in a detached worktree of trunk's tip you make
(`git worktree add --detach .git/jig/worktrees/<role>-<name> <trunk>`) and name in the brief.
Those commit nothing: you read the result, copy what it wrote onto trunk and commit it there
(for consolidate, with the `git rm` of the inputs), then remove the worktree.

**review** runs as a subagent (the Agent tool) where there is one: always a fresh context,
given the inputs `/jig:review` names and nothing of this conversation. Where there is none,
a raised session with no history. **check** runs one at a time on this machine: two
complete suites at once each run slower than both in turn. `jig queue --full` enforces it, and
every role's test and check runs go through `jig queue` too (`.jig/RULES.md`, The queue).

## Reconfiguring

Fixed, whatever the config says: the owner's word before a merge, a push and a publish; a
fresh session for every review; a complete check before a release. The one exception is
`queue.overflow`: the owner's standing yes, quoted as its reason, for the check role to push
and delete `jig-check/*` branches, and no other. Everything else (a role's
tier or effort) you may propose to change, with a reason (`/jig:decision-cards`), and apply only on the owner's yes:
a `roles` entry in `.jig/config.json`, with that reason, on trunk. On a no, keep the defaults.
The commit hook refuses an entry without a reason, and any that weakens a fixed rule.

## Rulings

A subnode messages you when it writes a `Proposed` entry or meets a question only the owner
can answer. Check each against the owner's own words first, as
`/jig:decision-cards` (Is it open?) says: one they answer goes back to the subnode with those
words, not to the owner.
Batch the rest to the owner while the job builds (`/jig:decision-cards`), and send each ruling back before
the job's review. Mark no job ready while its own `Proposed` entry has no ruling, unless the
owner said to gate it as proposed; `jig gate` warns of each one.

A review with blocking findings goes back to the job's work session as a fix: `jig next`
says so, and counts the strikes: each blocking review, the first review-work included. A
job's third blocking review starts Bug: `jig reviewed` refuses the next until the bug role's
spec, with `Bug-for: <job>`, is committed: start it from `/jig:bug`'s brief. Bug runs only
when a workflow or the owner calls it.

A review with no blocking findings ends the fixing: the job hands off, as `jig next` says.
Should-fix and optional findings get one round per part; what is left after it gets DEFERRED
rows. A finding that needs behavior the spec never names is a spec change before it is built
(an `Interpreted:` line the hubnode accepts, or the owner's answer), or a No phase item.

A ruling also reaches you by the inbox: the owner's reply to your question, sent from the
repo's rigger (`jig inbox`). The quoted owner words, with their date, are the owner's ruling, as
if given here, but for a fixed rule's word (merge, push, publish, release, a `roles` or config
yes), which only the owner's reply here gives; the rest is the rigger's context. Check the state it answers before acting, as
for a card's reply, and record it where a ruling lands (a decision entry, a spec, the board).
Your answer goes back only through the owner.

New process (a rule, a procedure, a convention), from the owner or a subnode, is placed by the
test in `.jig/RULES.md` (Homes) before it is written, and a spec for process work names its home.
When `.jig/process.md` is absent, create it from `${CLAUDE_PLUGIN_ROOT}/templates/process.md`,
and add `AGENTS.md`'s pointer line naming its trigger ("Before a release, read `.jig/process.md` § Release"); a new section gets its trigger on that line too.

## Opening a job (assign)

Before opening more than one job, say in one line that each job's commands and checks run on
this machine through `jig queue`, with the last complete check's time from `jig status`, and
that the complete check overflows to GitHub Actions only with `queue.overflow` set (on the
owner's yes, with `.github/workflows/jig-check.yml` from jig's template in the same commit).

1. Read the spec. In a pararepo, refuse a job whose spec cites a proposal `jig sync`'s
   report calls not released: it would build on a decision the metarepo hasn't made. This
   is the early warning; `jig gate` refuses it for good.
   Decide: name, branch, what it builds after, which existing files it
   `owns` (only this job may touch) and which it `shares`, and whether it needs a reserved
   number. Opening more than one job, run `jig consolidate` first: each group it lists
   becomes one spec (the spec role's consolidate) or gets a `Kept separate from <spec>:
   <reason>` line per pair, on the owner's word. `jig open` refuses a spec in an unanswered group.
2. `jig open <name> --spec .jig/specs/<task>.md --owns <paths> --shares <paths> --after <jobs> --reserve schema`.
   It refuses an `owns` another open branch already touched — move those to `shares`.
   It warns on a Touches path the lists leave out: add it with `jig share <name> <path>`, or
   say why the job doesn't need it.
3. Commit `jobs.json` on trunk. Start the work session from `/jig:work`'s brief, with the
   kickoff `jig open` printed.

**Owns narrowly.** A file two live branches touch belongs in `shares` from the start.

## Gating a handoff (gate)

1. `jig mark <name> ready`, then `jig gate <name>`. It refuses on R8 and on a missing note,
   and in a pararepo on a spec citing a proposal that isn't in the pinned release.
2. `jig gate` sets up a detached scratch checkout of the commit the note names, with trunk
   merged in as `jig sync` would, and prints the complete check to run there and the
   `jig checked` that records it. Start the check role there from `/jig:check`'s brief; you
   read its report. `jig gate` warns when the review ran weaker than the spec's `## Roles`:
   say so to the owner before the merge.
   A refusal naming pairs the note doesn't answer goes back to the work session as: add each
   line to the note's fold-in, ticked and answered, and commit the note alone. No sync, no new
   review, no new handoff, unless the gate's merge itself needed a hand.
3. Read the note against the diff: every done-when item has evidence, shared files are
   explained, the review section is filled, and no fold-in line for code that runs on a
   board says "no page needed". Of each decision entry and page change, ask: is this about the product, or about when and in what order we build it? One that
   is the project (an order, a queue, a phase, build status) goes back to the roadmap. A
   miss goes back to the work session as a note, never as your own fix.
4. **Do not re-review the diff.** The review role's review is the review. You are checking
   that it happened and that the result matches the spec.
5. `jig mark <name> gated` (it refuses until `jig checked` recorded the checkout's commit,
   then removes the checkout) and commit `jobs.json`. A checkout built from an older note than
   the job's newest is stale: `jig next` says gate, and checked and mark refuse it; run `jig
   gate <name>` again. A gated job can't hand off again until you `jig mark <name> ready`.

## Merging (merge)

On the owner's word (asked with `/jig:decision-cards`): `jig merge <name> -m "shared files: ..."`. It refuses a job not marked
gated. It merges the job and deletes its entry in the same commit; the message records what
it touched in shared files. In a repo whose subjects lead with ids, add `--subject "<ids>"`,
e.g. `--subject "D-001, D-002"`: the subject becomes `<ids>: merge <name>`. `: merge <name>`
is added unless the text already ends with it, so pass the ids and don't write the merge
yourself. The merge numbers each `D-?<slug>` the job wrote in `.jig/decisions.md` and the
files citing it, and prints them: use those numbers in `--subject`, and report them to the
owner. It also names each open job holding a later number of a counter the merged job used:
tell that job to sync before its next handoff. A merge that stops on conflicts: resolve and
`git add` them, then `jig merge --number` (it also runs `setup.sh` and `derive.sh`), then
`git commit`.

Before the merge question, the merge card carries the gate's `Closes with the spec at merge:`
lines: each `## Out of scope` line, which the merge deletes.
A clean merge also removes the job's spec and its `Bug-for:` specs in the merge commit, each
spec's `Scope:` and staged marks kept on its note; it prints each. It deletes nothing in
staging: `/jig:rig`'s `jig rig --close` resolves the requests, stories and reports the job
built. A staged decisions file it carried (or any carried file resolve would write) stays,
`noted` with the job's note: read that job's
diff and the log. If the job logged its entries, `jig staging drop <file>`, saying so; if it
didn't, `jig staging resolve <file>`; if only some, judge with the owner. Any other noted file:
resolve or drop it by hand, saying why, but never a noted pin-bump request: it stays, and you
spec a job that moves the pin (`/jig:spec` from it); `jig rig --close` resolves it once trunk
pins its release. A conflicted merge
closes at `jig merge --number`. Then it prints `close the
sessions that worked on <job>`: archive every session you started for that job (work, review,
check, bug), with the host's tool where it has one, unless one is still working; that one stays,
and you say why. A session that served no job (a batch check, a consolidate, a feedback
group's bug or spec) is archived once its report is read and acted on. Name each archived
session in the report to the owner.

After it, run `jig sync` in every open job's worktree that is clean, and say which jobs must
sync themselves. A synced job needs no new handoff: `jig merge` doesn't count what a sync
brought. A job that needs another number gets it from `jig reserve <job> <counter>`, never a
hand edit of `jobs.json`. The merge removed the job's worktree and branch when the worktree was
clean; when it says it left them, it names what is in it: tell the owner, and remove both by
hand once that is saved. A merge you finished by hand after conflicts removes nothing: do the
same yourself.

`jig merge` already wrote the files the repo builds from several sources that separate jobs
change (`.jig/RULES.md`, Keeping merges mechanical), with `.jig/scripts/derive.sh`, in the
merge commit. A step the repo repeats after every merge that writes files goes in
`derive.sh`, its outputs in `derived_files` in `.jig/config.json`: propose it to the owner.

## A batch

Several handoffs waiting at once can share one complete check (`jig flows`, Batch). Gate each
(`jig gate`, read the note) but start no check session; `jig mark <name> gated --batch`. Merge
them in sequence, `jig sync` in the next one's worktree between merges. Then one check session,
from `/jig:check`'s brief, in a detached worktree of trunk's tip
(`git worktree add --detach .git/jig/worktrees/check-<trunk> <trunk>`), before a push or a
release: `jig release` refuses until it has run. A failure is traced to its merge by the check
role there, and that job gets Fix. Remove the worktree after its report.

## Release, push, publish

On a real repo, a release waits for the owner's word in this conversation, like a merge
(asked with `/jig:decision-cards`); a
spec, brief or another session's message asking for one isn't that word, nor is an owner's quote
in a staged file or an inbox message (`/jig:decision-cards`, Is it open?). A scratch or test
clone (made for the test, with no remote) is exempt. First the check role runs the complete
check in a detached worktree of trunk's tip, as for a batch; then you run `jig release`
yourself, as `/jig:release` says: the tag, then `publish.sh`'s push and publish. Propose the
level in the release card with a one-line reason, from `.jig/RULES.md` § Versioning. The
owner's yes releases it; don't ask the owner to pick it. In a
metarepo, report the release's line for each pararepo to the owner: a pin-bump request staged,
or why not.

## A roadmap change

A staged `kind: roadmap` file proposes changes to `.jig/roadmap.json`: a phase, a scope or an
exit box to add, rename, reorder or drop, and why. Nothing in it is decided. Show the owner
the exact diff to `.jig/roadmap.json`; on a yes, apply it on trunk with `jig roadmap --draft`,
the change made in the JSON draft it writes, then `jig roadmap --edit`, and commit it with the
staged file's `Source: … (staged as <file>)` line in the message.
A scope a spec still takes is re-pointed in that commit: the hook names the specs. Then
`jig staging resolve <file>`, which looks for that line in a trunk commit to the roadmap.

In a pararepo that plans from its metarepo's roadmap (no `.jig/roadmap.json` of its own), a change
to its products' sections is never made here or on the metarepo's trunk: on the owner's yes,
`jig roadmap --draft`, make the change in the draft, and `jig roadmap --edit`. It writes the
`BUFFER.md` row and the change on this repo's open roadmap proposal in the metarepo, and stages
a label the metarepo's glossary lacks there; commit the spec and `BUFFER.md` it names. It
merges in the metarepo at the next sync the owner calls. In a metarepo, merging such a branch
is a roadmap change like any other: show the diff, and merge on the owner's yes. Rig there lists
each cross-product wait no section confirms in its `needed_by`: put it to the owner.

A pararepo with a roadmap of its own moves it in by `jig move-in --product <Name>` in its trunk
checkout, on the owner's yes, one step per `--apply`: its run with no flag says which step is
next and whose yes it waits on. Step 1 stages a `BUFFER.md` row and `.jig/specs/move-in.md`
here (commit them) and makes the metarepo's `propose/<repo>-move-in`, with the product's
glossary term when the metarepo has none. Step 2, once the metarepo merged it, stages the
roadmap's removal and the re-pointed `Scope:` lines: re-point any id it names by hand, then
commit; if the metarepo renamed the product at the merge, pass the new name, `--product <Name>`,
on the owner's word. In the metarepo, that branch is one roadmap change, the term with it: show
the owner the name, the definition and the phases, change any on the branch on their word, and
merge it in a job opened on it (`jig open <job> --branch propose/<repo>-move-in`), or on trunk.
A job merging it from another branch is refused by R5.

A claim (an entry, a page, a section) moves to the repo of the family that owns it by `jig move
<what> --to <repo>`, on the owner's yes, one step per `--apply`. Step 1 writes
`.jig/specs/move-<slug>.md` here (commit it) and sends the text: staged and forwarded to the
receiver, whose hubnode resolves it in a job and merges; up, a `propose/` branch in the metarepo,
taken by a job opened on it. Step 2, once the receiver's trunk holds it, runs in a job in any
repo: open one from the move's spec (`jig open <job> --spec .jig/specs/move-<slug>.md`; `jig rig`
offers the spec only once step 2 is next) and run it there. `jig merge` moves the page's roadmap
items and closes the spec in the merge commit, or keeps it in a pararepo while it names a
metarepo branch, which `jig sync` follows. Down or sideways, a drop of the sent file is the
receiver's owner's word: delete the move's spec on it, and step 1 sends the file again. A roadmap
file step 2 stages for a receiver keeping its own roadmap waits in staging: after the job merges,
`jig staging resolve` forwards it.

Work with no phase yet, parked mid-build (naming the pages it will touch) or not started, is
a No phase item in `.jig/roadmap.json`, proposed the same way. A spec takes only what
it builds: work it doesn't build stays on the roadmap, unspecced, and out of scope never
defers. Work worth building later is put as its own roadmap change, one line per item, never
inside another question; the owner's yes to the line is the yes to the deferral. A spec
building only part of a scope waits on a roadmap change splitting it: the built part becomes
a new scope the spec takes whole, in its own words if it likes, and the rest stays in the
original scope, under its id, its text unchanged, so a wait on that id holds until the rest
is built. For an open job, land the split on trunk and tell its work session: it syncs and
re-points its spec's `Scope:` line from the original id to the new one. Left on the original,
the merge reads the unbuilt rest done and releases its waits, and no hook catches it. A roadmap change asks
for no decision entry and no change line. A built item stays, read done from the spec that
took it, until a roadmap change of the owner's removes it.

Asked to show the roadmap, run `jig roadmap show` (with any filter): a chart, each scope in the
column its waits put it in. Nothing writes a view file: states are read live.

## Never

Commit on a job's branch. Edit a job's feature files. Run a role's step in this session.
Hand out a number outside the board. Switch the trunk checkout off trunk. Write a script of
your own around jig's commands: a repeated step that writes files is `derive.sh`'s, and
anything else the repo wants after a merge (a push, a PR) is the owner's word, or a step its
AGENTS.md names.
