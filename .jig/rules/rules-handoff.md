# Fold-in and handoff rules

## Fold-in

Code and the page that documents it move together, or the page starts lying. `jig handoff`
works out every documentation page that covers a file the branch changed — a file can have
several, such as its system page and the page of the board it runs on — and writes a
checklist into the note. A moved file asks the page that covered its old path too. Each line
asks whether the page still describes the code: it is either ticked as updated — the stale
sentences edited, deleting text included — or says why none went stale. Each roadmap item
naming a covering page in its `touches`, a No phase item not done or a taken scope,
gets a line of its own, answered **built**, **untouched**, or **departed: <why>**, with
anything after the answer the answerer's to add. Built means the work's description is in the
page's body now. An answer changes no roadmap: an item's state, like a scope's, comes from the
specs that take it, so a built item stays, read done once its spec is complete, until the
owner's roadmap change removes it. So `jig gate` refuses built on a No phase item that no
spec of the job takes, as the gate's own merge of trunk leaves the spec, read once that merge
is made (a merge that needs a hand is refused first): the spec's `Scope: No phase/<id>` is what
makes it read done. `jig gate` refuses while a line is unanswered; untouched and
departed are answers.

Ownership comes from `docmap` in `.jig/docmap.json`:

```json
"docmap": {"docs/storage/storage.md": ["server/storage.py", "server/migrations/**"]}
```

`docmap` can name any file, config such as `sdkconfig` included; a page is asked about
whenever a file it names changes. A changed source file nothing covers is listed as
`UNOWNED` — add it to `docmap`, starting a new page from `.jig/templates/page.md`, or answer why
it needs no page.

A decision entry and the pages citing it are one home, so a branch that adds, edits or removes
an entry in `.jig/decisions.md` also asks each page whose text cites that id, even in passing,
with the ids on its line; an entry that supersedes another asks for the old id too. The pages
are a metarepo's entry pages, and `docmap`'s pages in any other repo. The id matches whole:
`D-7` is not `D-70`. The log itself is not asked.

An entry the branch adds or changes also gets one line per page it meets peers on, per peer log
(`rules-decisions.md`, Decision log), naming the entry, every peer there and the page:

```
- [ ] D-?id-lock vs <meta>/.jig/decisions.md § D-033, D-041 (<meta>/docs/features/gestures.md): ___
```

It is answered once for every id on it: **agrees**, **narrows: <how>** (one is an exception the
other allows), or **conflicts: <resolution>**. On a line of several ids, narrows and conflicts
name at least one of them (`narrows: D-041, <how>`). jig picks the pairs and never judges one;
the gate refuses a line unanswered, reshaped, answered with another word, or answered conflicts
or narrows with nothing after it. A checklist line `- [ ] <id> vs …` is a pair line: one that
drops or changes any part of jig's shape is refused, naming it. A line with no checkbox is the
job's own. A peer log jig couldn't read gets a line too, answered by reading it or saying why
not. The commit hook refuses a note whose pair line is reshaped or has none of the three
answers, naming the line, so a blank is found when the note is committed, not at the gate.
The gate finds the pairs again on its merge of trunk, and refuses one the note doesn't answer,
naming its cause: a pair jig listed at the handoff and the note left out, or one new on trunk
since the job's base, where a job merged since ruled on the same page. A pair with another
repo's log names no cause: jig reads that log as it stands now, not as it stood at the base.
The job adds each pair it names to the note's fold-in, ticked and answered, and commits the
note alone: no sync, no new review and no new handoff, since the note is bookkeeping the merge
doesn't count as a change. It syncs only when the gate's merge itself needed a hand.

## Handoff, gate, merge

1. **The work subnode hands off.** Runs the checks, has the diff adversarially reviewed (the
   session that dispatched the review records it once, `jig reviewed` with `--blocking`), then `jig handoff` writes a note naming that exact commit, in
   `.jig/handoffs/<name>-<date>.md` with a `/` in the job's or branch's name as `-`. Its
   `Spec:` is `--spec`, as a path from the repo root, else the job's spec on the board:
   working alone, pass `--spec`. A chunk that doesn't finish its spec hands off with
   `--partial`. Fill every heading, commit the note with the work, tell the hubnode the job
   and the commit. The note and the review's `.jig/ledgers/deferred.md` rows may be one
   commit after the reviewed one. deferred.md is judged by its net change from the reviewed
   commit to the branch, not commit by commit: a row edited and restored later deleted
   nothing, and only a line the net change deletes, one trunk didn't delete, counts as a
   change since the check. A job may hand off several times, but not while trunk's board has
   it gated: the hubnode marks it back (`jig mark <job> ready`) first, and the new note is
   gated again, so a gated state never outlives the note it was gated on.
   The review needn't be HEAD itself. A clean `jig sync` of a reviewed commit hands off with
   no new `jig reviewed`: the merge carries nothing a reviewer didn't see. A fix, or a sync
   resolved by hand, is refused, naming the files, until it has a review-change (`rules-workflow.md`, Workflow;
   working alone, a fix after a committed note gets a full review). So is a review whose
   record has blocking findings: Fix first.
2. **The hubnode gates.** `jig gate <job>` refuses on R8 and on a missing note. Then it sets
   up a **detached scratch checkout of the commit the note names**, with trunk merged in the
   way `jig sync` merges it, and prints the complete check to run there
   (`jig queue --full -- ./.jig/scripts/check.sh --full`), the check role's tier and effort, and the `jig checked`
   that records it. It never runs the check: whoever runs it runs the same command. Never the
   job's live worktree, which the subnode may still be building in.
   The scratch checkout lives until the job is marked gated or merged: `jig mark <job> gated`
   and `jig merge <job>` remove it, untracked files and all, and refuse while it holds a
   tracked edit, which belongs on the job's branch. `jig update` removes one left behind.
   The checkout must hold the commit the job's newest note names (HEAD, or HEAD's first
   parent when trunk was merged in). One built from an older note is stale: `jig next` says
   gate, and `jig checked` there and `jig mark <job> gated` refuse it, naming `jig gate <job>`,
   which builds it again.
   `jig mark <job> gated` refuses until `jig checked` has recorded the checkout's commit;
   `jig mark <job> gated --batch` leaves the check to the batch (`rules-workflow.md`, Workflow).
   After the check lines the gate prints `Closes with the spec at merge:`, every `## Out of
   scope` line of the job's spec: the owner's last look at what the merge deletes with the
   spec. A spec with none prints no such block.
   The hooks set that checkout up with `.jig/scripts/setup.sh`, when it is added and again
   after its merge of trunk, so the checks run in an environment built from the job's own
   manifests.
   That means a merge runs the merged-in `setup.sh`: review a change to it like any other
   code, because the next merge executes it. The same goes for `derive.sh`, whose output the
   merge commits.
3. **The hubnode merges** with `jig merge <job>`, on the owner's word. It refuses a job not
   marked gated. It deletes the job's entry and numbers its
   `D-?<slug>` ids (`rules-decisions.md`, Decision log) in the merge commit itself, then syncs the clean jobs. A job synced since its note still merges: only
   the job's own commits count as changes since the check, and what a sync's resolution
   carries beyond what `jig sync` would make of it (this replay needs git 2.38 or later).
   Either refuses until it is handed off again. A job that wasn't synced and conflicts with
   trunk only in `append_files` files where both sides only added is resolved in the merge as
   `jig sync` would resolve it (a replay of that sync, so trunk's lines, then the job's; git
   2.38 or later), and the job's branch is left as it was. Any other conflict in an append
   file, or one beside a conflict elsewhere, is refused with "`jig sync` the job, then merge":
   the sync resolves the appends as the gate did and stops on anything else. A job whose only
   conflicts were appends needs no new handoff after it. The merge prints each open job
   holding a later number of a counter the merged job used: that job syncs before its next
   handoff. What the merge touched in shared files goes in that commit's message (`-m`).
   `--subject <ids>` is the ids the subject leads with, e.g. `D-001, D-002`, for a repo whose
   subjects lead with ids: the subject becomes `<ids>: merge <job>`. `: merge <job>` is added
   unless the text already ends with it, so pass the ids and don't write the merge yourself.
   Before its commit the merge runs `.jig/scripts/setup.sh`, then `.jig/scripts/derive.sh`,
   and commits what the board's `derived_files` globs match in the merge commit, and nothing
   else it wrote: a tracked file left changed outside them is named and not committed. A failing
   derive stops the merge before its commit, as a conflict does: fix it, `jig merge --number`,
   `git commit`.
   After its commit, the merge removes the job's worktree when `git status` there is clean, then
   its branch (`git branch -d`); a worktree holding an uncommitted or untracked file is named,
   and nothing is removed. A merge finished by hand after conflicts removes nothing.
   A merge also leaves nothing of the job in flight: in the merge commit it removes the job's
   spec, once the notes this job filed complete it and no other open job names it, and each
   `Bug-for: <job>` spec, and writes each removed spec's `Scope:` line on its
   completing note (a `Bug-for:` spec's on its job's newest note, merged into any line already
   there), in the note's header after its `Spec:` line, which the roadmap then
   reads, and beside it each
   `Source: … (staged as …)` line the spec carried, which `resolve` then reads (`rules-staging.md`, Staging). In a
   pararepo a spec naming a metarepo proposal or pointers branch stays: `jig sync` follows the
   branch through it. A conflicted merge closes at `jig merge --number`, its last step before
   the commit. A merge writes nothing in `.jig/staging/`. `jig rig --close` closes the rest
   (`rules-workflow.md`, Workflow).
   `jig open` refuses a name whose earlier job's `Bug-for:` spec is still on trunk, which would
   be read as the new job's own (closed by its merge), naming `jig rig --close`. The job's sessions end at its merge: the merge
   prints `close the sessions that worked on <job>`, and the hubnode closes them.
   A hand `git merge` on trunk runs `setup.sh` but not `derive.sh`: run it and commit what it
   wrote, or the derived files stay stale until the next `jig merge`. In a metarepo, don't run
   `derive.sh` on trunk after a hand merge: M4 refuses the commit, and what it writes blocks the
   next `jig merge`, which writes them.
