---
name: rig
description: Show the repo's picture - what can start now, what waits on what, what waits on the owner, the roadmap's next step - then put one batch of decisions to the owner, and act on the answers. Run only when invoked by name as /jig:rig, /jig:rig fresh or /jig:rig auto, in the hubnode's session.
---

Read `.jig/RULES.md` first (Workflow: `jig rig`). `jig` below is `python3 .jig/jig.py`. You
are the hubnode, in the trunk checkout: rig's actions (a spec written, a job opened) are
yours, done the way `/jig:hubnode` does them.

`jig rig` computes the state, its order and its groups. You add only the judgments it can't
make, store them, and draw what it printed. Never reorder, regroup or reword its picture.

## 1. Judge what isn't judged

`/jig:rig fresh` starts with `jig rig --fresh`, which forgets every stored judgment. Then
`jig rig --json`. Each item has a `kind` (`spec`, `staged`, `feedback`, `next-step`), a
`state`, what it `waits_on`, its `group`, and `judged`: the judgment stored for it, or null
when there is none or its item or the board changed since. A `taken` staged file is carried by
a spec already: it gets no judgment and no question. Nor does a `built` or `noted` one: what
carried it decides it, and `--store-put` refuses all three.

First, in the jig repo, each `feedback` item whose `state` is `new`: start `/jig:fix` on it (one
fix for every new report, grouped as that skill says), without waiting for it, and store
`{"call": "fixing", "about": "<its group>", "context": "<the session that took it>"}` with
`jig rig --store-put <path>`. A `fixing` report is never started twice. Its drops and specs show
as `/jig:fix` shows them; its specs come back as waiting specs on a later run. A report `/jig:fix`
ended with still staged is stored `concluded` (that skill says when): it waits on the owner.

For each item whose `judged` is null: each staged file, and the next-step item whose `state`
is `open` (a next-step item whose `state` is `taken` is already under way, and one whose
`state` is `blocked` is a roadmap scope waiting on the refs its `after` names: each is
listed under Waiting on, and gets no judgment and no question):

- **A staged file:** read it whole. Call it `ready` when a spec can be written from it as it
  is, with no answer from the owner; `open` when it can't. An open file gets only the questions
  its owner's words leave open, checked as `/jig:decision-cards` (Is it open?) says: the quoted
  words settle what they say, over any note in the file that asks it again, and a fact about
  the repo is read, not asked. Each question has two to four options, one recommended, from
  what the file and the repo say, and a `because`: the context line its block draws, quoting
  the owner's sentence that leaves it open, or "the owner's words say nothing on this". A
  file whose every question its owner's words answer is `ready`. A ready file gets its
  recommendation: the spec it becomes, in one line. A judgment handed to a subagent gets this
  paragraph and Is it open? in its brief.
- **The next step** (the open one): a No phase item naming pages, or a roadmap scope. Its
  question: take it now (a spec for it, whose `Scope:` line takes it, `No phase/<id>` for an
  item, so it reads done once built), or leave it where it is, with one recommended and why.

Store each: `jig rig --store-put <path>` with a JSON object on stdin,
`{"call": "ready"|"open", "about": "…", "context": "…", "questions": [{"ask": "…", "options": ["…"], "recommended": 0, "because": "…"}], "recommend": "…"}`.
An item whose `judged` isn't null is replayed as stored: never judge it again in this run.
Then `jig rig --json` once more: ready staged files now sit in its groups.

## 2. The picture

Draw it from that last output, in this order, the same every run. Where the host can draw an
inline visual, it may; the sections and their contents stay these.

1. The count line: how many things wait on the owner's answers (every question: the open
   staged files, each `noted` file and `concluded` feedback report, the open next step, each
   group with an overlap, each dependency cycle, a ring once, and each unconfirmed
   cross-product wait), and how many can start now.
2. **Can start now:** each `group`, its items in the order given, each with what it comes
   after, and each overlapping pair the group's `overlaps` names.
3. **Waiting on:** each item and what it waits for: a job, a spec or a staged file. A taken
   staged file waits on the spec or job that carries it. A blocked scope waits on the scopes
   or phases its `after` names: work, not an answer. In a pararepo the roadmap is the
   metarepo's: only the products this repo owns give it steps, and a line naming a repo rig
   couldn't reach says so.
4. **Waiting on you:** the open staged files, each `noted` file with the note that carried it
   (the hubnode's step), each `concluded` feedback report with what
   `/jig:fix` found, the next step whose `state` is `open`, each
   group with an overlap (one line: one job for its items, or keep some apart), each
   dependency cycle (`cycles`), and in a metarepo each cross-product wait no section confirms
   (`unconfirmed`): the owner rules on it, and it blocks nothing. In a family, then the
   `Family:` line when rig printed one (`family`): stale staged files, stale or empty
   proposals, entries touching labelled work and pairs of names, for `jig family`. It is a
   report, not a question, so it counts in neither number.
5. **Running:** each open job with its step, who takes it, and whether it continues a session
   or starts one, as `jig rig` printed it from `jig next`; then each `fixing` feedback report
   with its group and its session.

Then close what merges left, which needs no answer: `jig rig --close` removes every spec in
`finished` in one commit on trunk, each one's scopes and staged marks kept on its note, then
resolves each `built` staged file (resolve writes nothing for those); archive the sessions you started for jobs no longer on the board, with the
host's tool where it has one, unless one is still working (that one stays, and you say why).
Draw both as the sixth part:

6. **Finished:** each spec `jig rig --close` closed or kept, each staged file it resolved,
   and each session archived or still working. A `noted` file (a carried file `resolve` would
   write, a decisions file most often) is never resolved here: it shows under Waiting on you as
   "noted: <note> carried it; the hubnode's step", and § 4 takes that step.

## 3. The decisions

Load `/jig:decision-cards` and put every decision in one batch, drawn as it says. The blocks,
in this order:

1. Each open staged file's questions, from its stored judgment.
2. The next step whose `state` is `open`.
3. Each group with no overlap that holds ready staged files: write their specs, in `after`
   order? A lone ready staged file in no such group: write its spec? The stored
   recommendation is the recommended option.
4. Each spec whose `opens` is `now`: start it as a job? A staged file is never opened as a
   job: block 3 writes its spec, and the next run offers that spec.
5. Each group with an overlap, one block whatever its members' `opens`, its pairs perhaps
   reaching a waiting spec outside the group: "one job for <its items>" (recommended), a
   "keep <item> apart" option for each member the judgments or the group's `append_only`
   flag set apart, then "each its own job". The one reply may give any split. Its ready
   staged files get no block 3 and its pairs no block of their own. An item whose `opens` is
   `after` gets no other block: it builds after another item in its group, and once that
   opens as a job, it waits on that job.
6. Each dependency cycle named under Waiting on: which item goes first?
7. Each unconfirmed cross-product wait (`unconfirmed`, a metarepo's): keep it, the waited-on
   product's repo confirming it with `needed_by` naming the waiter on the scope or phase it names
   (recommended when the work really is needed), or drop it, the waiter's repo removing its
   `after` entry. It blocks nothing meanwhile: the wait itself still blocks as any does.
8. No block for a `noted` file: it is the hubnode's step (`/jig:hubnode`, Merging), done here
   in § 4 as that step says, and drawn under Waiting on you until it is.
9. Each `concluded` feedback report: drop it (`jig staging drop`), or keep it staged for more
   of what its `about` says is missing. A changed report is new again, and rig starts
   `/jig:fix` on it.

Every block has "not now". It is an answer: the item stays as it is and comes back next run.
Nothing is ever dropped for it.

## 4. Act on the answers

- **A noted file** (no question, your own step, as `/jig:hubnode`'s Merging gives it): read the
  job that note names and the log. A decisions file whose entries that job logged: `jig staging
  drop <file>`, saying so; none logged: `jig staging resolve <file>`; some: put it to the owner.
  A noted pin-bump request (its job merged without moving the pin) is never dropped: keep it,
  and spec a job that moves the pin. Any other noted file: resolve or drop it by hand, saying why.

- **An open file's answers:** append them to the staged file under `## Owner's answers`, dated,
  in the owner's words. The file changed, so the next run judges it again.
- **Start on an open file with unanswered questions** (the owner says to write its spec
  anyway): re-check each question as `/jig:decision-cards` (Is it open?) says. What the owner's
  words answer goes under the spec's Decisions, in those words, quoted and dated. Each one still open is built as its recommended option,
  with an `Interpreted:` line under the spec's Decisions naming it unanswered. Show the spec
  before `resolve`, as `/jig:stage` says.
- **Write a spec:** resolve the staged file as `/jig:stage` says (a request or story is
  interpreted into a spec, with the spec role where the hubnode's rules say), carrying
  `Source: <source> (staged as <file>)` for each staged file, a decisions file included. Its
  `after:` header becomes a `` Build after `<spec>` `` line in that spec, naming the spec each
  file it waited for became, so the order survives the staging file.
- **One job for a group:** the spec role's consolidate, with the group's staged files and
  specs as its inputs, each staged file's mark a `Source:` line. The next run lists those
  files as taken by the merged spec.
- **Keep an item apart:** a `Kept separate from <the group's spec>: <reason>` line, in the
  owner's words: in that item's spec, or under `## Owner's answers` in its staged file.
- **A cycle's answer:** the item chosen to go first stops building after each ring member it
  names, so it has nothing left to wait for in the ring. In
  a spec, remove those names from its own `Build after` line. In a staged file, remove them
  from its own `after:` header, as `/jig:stage` breaks a cycle: `jig rig` and `jig staging`
  read only the header, so nothing else breaks it.
- **An unconfirmed wait's ruling:** show it; rig changes no roadmap. Keep: the waited-on
  product's repo adds the waiter to its `needed_by`; drop: the waiter's repo removes it from its `after`.
  The repo whose section changes proposes it, as any change to a product's section goes: a
  `BUFFER.md` row and `jig propose --buffer` there, the change on the `propose/` branch it
  makes, merged in the metarepo at the next sync the owner calls. For the metarepo's own
  sections, or a product it owns as `this repo`, the hubnode makes it as its skill's "A roadmap
  change" says: the diff shown, applied on the owner's yes.
- **Start a job:** open it and start its subnode as `/jig:hubnode` says (Assigning a step).
- **The next step taken:** a spec for it, with the spec role. The roadmap itself is the
  owner's to edit: never change it here.

Then `jig rig --json` again. Opening a job changes the board, and a changed board voids every
stored judgment, so judge each item whose `judged` is null as in step 1 before drawing. Then
show the new picture, so the owner sees items move from open to ready to running.

## `/jig:rig auto`

The same run, its feedback step and Finished included, without asking for what needs no
answer. It takes no `noted` file's step: whether a job logged only some entries is the owner's
to hear, so those stay listed for an interactive run. Then: write a spec from every ready staged file in no group with an overlap, then run `jig rig --json` again (judging what comes back null, as in step 1) and open and
start every spec whose `opens` is `now` in that output. A group with an overlap needs the
owner's answer, and an item that comes `after` another waits for that job, so neither starts. Answer
no open question, break no cycle and take no roadmap step: those are proposed, as blocks, for
the owner. End with the picture and a short list of what you did.

## Never

Run on a phrase: only `/jig:rig` by name starts it. Change `jig next`, the roadmap or a staged
file's own text above `## Owner's answers`, but for one thing: the owner's answer to a cycle
removes ring members from the chosen file's own `after:` header.
