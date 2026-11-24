# bug-stale-gate-and-entry-files: a stale gate checkout gets checked and gated; `--merge-log` leaves `entry_files` naming files it removes

Source: jig hubnode session / 2026-11-24 / Dave, with Claude ("open a bug spec for it after these jobs merge") (staged as feedback-jig-2026-11-24-next-stale-gate.md): `jig next` names the check in a stale gate checkout after a new handoff
Source: jig hubnode session / 2026-11-24 / Dave, with Claude ("Stage it") (staged as feedback-jig-2026-11-24-merge-log-entry-files.md): `--merge-log` removes a record folder's index but `meta.json` keeps naming it

Opens after ideas-log merges (its `cmd_merge_log`/`record_plan` rewrite is the base of bug-merge-log-entry-files' fix).

## Intent
Two bugs in `plugin/templates/jig/jig.py`, built as one job. A gate's check counts only for
the commit the job's newest handoff note names: a gate checkout built from an older note is
stale, so `jig next` sends it back to `jig gate`, `jig checked` and `jig mark <job> gated`
refuse it, and `jig handoff` refuses while trunk's board has the job gated. And in a metarepo,
when `jig update --apply --merge-log` removes a file that `.jig/meta.json`'s `entry_files`
names, `entry_files` stops naming it in the same change, with the log in its place, whether or
not a register or `CHANGELOG.md` merges in the same run.

## Bug evidence
Each input's bug-role sections, kept as written.

### From bug-next-stale-gate

#### Intent
The gate checks the commit the job's newest handoff note names, and nothing downstream trusts
a check of any other commit. A gate checkout built from an older note is stale: `jig next`
sends it back to `jig gate`, and `jig checked` and `jig mark <job> gated` refuse it. A job
already marked gated can't file a new handoff until the hubnode marks it back, so a gated
state never outlives the note it was gated on.

#### 1. Why
- Q: Why did `jig next` name the check in a checkout holding 067402b after the ae675c7 handoff? A: `chain_step` sees the checkout exists and its HEAD has no record in `checked.log`, so it says check.
- Q: Why doesn't it see the checkout is stale? A: Nothing compares the checkout's commit to the newest note's `Commit:`. `jig gate` rebuilds it, but only when someone runs the gate again.
- Q: Why does no other command catch it? A: `jig checked` records any HEAD, and `jig mark gated` asks only for a record of the checkout's HEAD. `jig merge` then assumes "the gate checked the commit the latest note names". Root: that assumption has no check behind it.

#### 2. Givens (line numbers at trunk 5e40489)
- [seen] The report's `jig_version` is 8990c123c8c1. This trunk (5e40489) has the same code path. Reproduced here, below.
- [seen] `chain_step` (jig.py:2630-2638): with a newest note not changed since, it reads `gate_scratch(name)`. Missing checkout → "gate". Checkout HEAD with no `checked.log` record → "check … the complete check in <scratch>". Otherwise → "gate; checked: `jig mark <job> gated`". It never reads the note's `Commit:` against the checkout.
- [seen] `cmd_gate` (jig.py:3344, 3370-3378) checks out the note's `Commit:` detached, then `merge_trunk` merges trunk in. So the checkout's HEAD is the note's commit (trunk already in) or a merge whose first parent is it. Before building, it removes any old checkout: "A gate whose checks failed is gated again after a new handoff, with no mark between."
- [seen] `cmd_checked` (jig.py:1687-1735) appends HEAD to `checked.log` wherever it runs. It doesn't know it's in a gate checkout.
- [seen] `cmd_mark … gated` (jig.py:1562-1579) refuses only when the checkout is missing, dirty, or its HEAD has no `checked.log` record.
- [seen] `cmd_merge` (jig.py:2018-2026), under the comment "The gate checked the commit the latest note names; anything built since is unchecked", compares only the newest note's `Commit:` with the branch. `next_step`'s gated branch (jig.py:2600-2614) does the same.
- [seen] RULES.md:622-632 (Workflow, step 2) promises "a detached scratch checkout of the commit the note names", and that "A job may hand off several times" (RULES.md:616).
- [seen] Repro A, `bug-next-stale-gate-repro-a.sh` in the hubnode's side-session notes folder (throwaway repo, `JIG_CONFIG`/`XDG_CONFIG_HOME` set). Steps: open k, commit, review, handoff 1 at 44266d5, `jig gate k`. Checkout HEAD 9cf9639, first parent 44266d5. No check recorded. Then a fix, `reviewed --change`, handoff 2 naming f06a80d. `jig next k` printed `k: check — check, new session (Job; the complete check in .git/jig/worktrees/gate-k)`, the report's symptom. `jig checked` there recorded 9cf9639 (rc 0). `jig next` said `checked: jig mark k gated`, and `jig mark k gated` accepted. `jig next` said merge and `jig merge k` merged. Main holds the fix ("x y"), and `checked.log` holds only 9cf9639.
- [seen] Repro B, `bug-next-stale-gate-repro-b.sh` beside it: gate, check and mark gated were done properly at handoff 1. Then a fix with the board still gated, and `jig next` correctly said "gated at …, changed since: mark it back; review-change, handoff, gate again". After `reviewed --change` and handoff 2, with no mark back, `jig next k` said `merge`, and `jig merge k` merged the unchecked fix. A gated state carries no record of the note it was gated on.
- [seen] `cmd_handoff` (jig.py:2837) loads the board from trunk (`Board.load`, jig.py:235-243), so it can read the job's trunk state.
- [seen] The smoke's `sec_next` (tests/smoke.sh:2268-2318) covers gate → check → mark → merge for one handoff only.

#### 3. One layer up
- Siblings: `jig checked`, `jig mark gated`, `jig merge` and `next_step`'s gated branch all read
  "the gate's check". None compares it to the newest note, so all have the gap (Repros A and B).
  `jig gate` is the one path that gets it right: it always builds from the newest note's
  `Commit:` and throws away an old checkout. The fix reuses that. A stale checkout's step is
  `jig gate <job>`, which the hubnode already runs again after a failed check.
- The existing pattern: `changed_since(<newest note's Commit:>, branch)` ties `next` and `merge`
  to the newest note. What's missing is the same tie from the gate checkout to that note. One
  helper answers "does the gate checkout hold the newest note's commit?". Yes if its HEAD is that
  commit, or HEAD's first parent is and HEAD is the merge `jig gate` made. `chain_step`,
  `cmd_checked` and `cmd_mark` all call it. No new record and no new ledger.
- Repro B, the gated case: `jig next`'s gated branch already says "mark it back; review-change,
  handoff, gate again", in that order. Making `jig handoff` refuse while trunk's board says the
  job is gated enforces that order with nothing new recorded. Marking back makes the job's
  newest note be gated again.

#### 4. Correction
A correction. The commands that act on a gate's check now confirm which commit it covers, and
a gated state can't outlast its note. There's no workaround: the symptom shows in `jig next`,
but `jig checked`, `jig mark gated` and the merge let it through too.

General?: the problem is general. In any repo (regular, metarepo or pararepo), a gate's complete
check fails, the job fixes it, and the job hands off again. RULES.md describes this ("A job may
hand off several times"), and `cmd_gate`'s own comment expects it. An ordinary hubnode follows
`jig next` and gets the stale checkout. Nobody has to work against jig to trigger it.

#### Change
1. **`gate_holds(board, name)`**, one helper. It finds the job's newest note's `Commit:` (as
   `next_step` reads it) and the gate checkout's HEAD. It answers whether the checkout holds
   that commit: HEAD equals it, or HEAD's first parent does. Callers print the checkout's commit
   and the note's.
2. **`jig next`** (`chain_step`): when the checkout exists but doesn't hold the newest note's
   commit, return `gate — hubnode, continue the hubnode (Job; <scratch> holds <old 12>, not
   <new 12> that <note> names: `jig gate <job>`)`. Do this before checking `checked.log`, so a
   check recorded for the stale checkout doesn't make the step "mark gated".
3. **`jig checked`** run in a job's gate checkout (its top level is `main_root() /
   gate_scratch(name)` for a job on trunk's board) refuses when the checkout doesn't hold the
   newest note's commit. It records nothing, and names both commits and `jig gate <job>`. `--ci`
   runs through the same test. `--trace` and checks outside a gate checkout are unchanged.
4. **`jig mark <job> gated`** refuses the same way before it reads `checked.log`, and leaves the
   checkout in place. `--batch` is unchanged: it removes the checkout and the batch's check
   runs on trunk.
5. **`jig handoff`** refuses while trunk's board has the job `gated`. It says: "<job> is gated on
   <trunk>: the hubnode marks it back (`jig mark <job> ready`) before a new handoff, which is
   gated again." A solo handoff (no job) is unchanged.
6. **Words**: RULES.md Workflow step 2 (the gate checkout holds the newest note's commit; a
   stale one is gated again, and `jig checked` and `jig mark gated` refuse it) and step 1 (no
   handoff while gated). Also the `jig checked` paragraph (RULES.md:881) and the hubnode skill's
   Gating step 5. One line under `### Fixed` in `.jig/decisions.md` `## Unreleased`.

### From bug-merge-log-entry-files

#### Intent
In a metarepo, when `jig update --apply --merge-log` removes a file that `.jig/meta.json`'s
`entry_files` names, `entry_files` stops naming it in the same change, with the log in its
place. This holds whether or not a register or `CHANGELOG.md` merges in the same run. RULES.md
already promises it: "in a metarepo, `entry_files` names the log in place of what was merged".

Opens after ideas-log merges. That job rewrote `cmd_merge_log` and `record_plan` into one plan
that writes each path once (the owner's word, 2026-11-24, in the report). This spec is written
against ideas-log's shape.

#### 1. Why
- Q: Why does `entry_files` still name the removed index? A: `kept_entry` drops only `gone`, which holds the registers and `CHANGELOG.md` (`files_in`), not `rp["remove"]`.
- Q: Why only those? A: `kept_entry` predates record folders. When folders came in, their removals went to the board (`board_rewrite` gets `rp["remove"]`), but not to META.
- Q: Why is META not rewritten at all in a folder-only run? A: The write is guarded by `if files_in`. The guard was right when only files could be removed. Root: META's rewrite never learned about the plan's removals.

#### 2. Givens
- [seen] Reproduced on trunk 5e40489, in throwaway repos (`JIG_CONFIG`/`XDG_CONFIG_HOME` set; the script is `bug-merge-log-entry-files-repro.sh` in the group's notes folder). The repo is a metarepo (`init --meta`). `docs/decisions/` holds records 0001 and 0002, both accepted, and a `README.md` holding only links to them. `entry_files` is set on trunk, then `--apply --merge-log` runs on branch `ml`.
  - **Case reg**: a root `DECISIONS.md` with one row, and `entry_files: ["docs/decisions/README.md", "DECISIONS.md"]`. The run prints `removed after: docs/decisions/0001-a.md, docs/decisions/0002-b.md, docs/decisions/README.md` and `.jig/meta.json entry_files: ['docs/decisions/README.md', 'DECISIONS.md'] → ['.jig/decisions.md', 'docs/decisions/README.md']`. `git status` shows `D docs/decisions/README.md` and `M .jig/meta.json`. The commit passes the hooks, and `jig rules` prints `ok`.
  - **Case folder**: no register, and `entry_files: ["docs/decisions/README.md", ".jig/decisions.md"]`. The run prints no `entry_files` line. `.jig/meta.json` is not staged, and still names `docs/decisions/README.md` after the commit. The commit passes, and `jig rules` prints `ok`.
- [seen] Reproduced on ideas-log's code at 8921001 (its `plugin/templates` from `git archive ideas-log`, same script). Both cases give the same result. In case reg, ideas-log's summary line reads `Written .jig/decisions.md, .jig/meta.json; … docs/decisions/README.md removed`. In case folder, META is not in the written list.
- [seen] trunk `cmd_merge_log` (jig.py:15511-15514, 15560-15565) and ideas-log `cmd_merge_log` (jig.py:15121-15124, 15164-15168): `kept_entry = [LOG, *[e for e in entry if e not in gone and e != LOG]]`. Both the print and the write sit under `entry is not None and files_in`. On ideas-log, `removals = list(dict.fromkeys(gone + rp["remove"]))` is already built (jig.py:15102), before `kept_entry`.
- [seen] `record_plan` puts the records into `plan["remove"]`, and an index whose `record_index_left` is empty goes there too. An index with anything left is kept and rewritten (`plan["keep"]`, `plan["write"]`). So a kept index exists after the run, and it is right for `entry_files` to keep naming it.
- [seen] The report's other givens hold as written: the reviewer's repro on ideas-log b832061 gives the same output as case reg above.
- [seen] Nothing catches the dangling name later. `jig rules` passes, and `jig update` and `jig survey` print nothing about it (run in case folder, after the commit). No check in jig.py says "an `entry_files` name matches no file".
- [seen] `entry_files` items are globs (`is_entry` → `matches`), but a literal path is the common form (`init --meta` writes two). `old_registers` compares items to paths literally (`f in entry`).
- [assumed] The cost of the dangling name is mostly latent. Today a name that matches nothing counts nothing. If a later change adds a file at that path, it silently becomes an entry file: M3 asks a log line for it, and pararepos cite it. The fix doesn't depend on this; it rests on RULES.md's promise.

#### 3. One layer up
- **The board, in the same function.** `board_rewrite` is handed `{files_in} | rp["remove"] | indexes`, so `append_files` and `reserve` stop naming removed records and indexes. META is the one target of the run that was never handed `rp["remove"]`. The fix gives META the set the board already gets.
- **`glossary_plan`** (`--glossary`), the other command that removes an entry file. It rewrites `entry_files` whenever its removal changes it (`if entry != data.get("entry_files")`), and puts META into `plan["write"]`, so the one-plan writer writes it. That is the pattern to follow: decide from what the plan removes, then write META through the plan.
- **The trunk-side rerun** (`stale_board_names`, `in_use and not folders_in`) rewrites only the board. It never touches META, and in a metarepo it can't on trunk, since META changes only in a reviewed merge (M4). That is why the fix belongs in the branch run.
- **Registers and `CHANGELOG.md`** already work: they are in `gone`. Only the folder path has the bug.

#### 4. Correction
A correction. `kept_entry` is computed from the run's full removals, and META is rewritten
whenever `entry_files` names one of them. The guard that let META skip a folder-only run is
the thing that produced the symptom, so the fix changes it, not the output.

#### General?
Picture a metarepo that keeps its decisions as ADRs (adr-tools, MADR) with an index page. Its
pararepos cite that index, so the index is in `entry_files`, which is ordinary use of both
features as RULES.md describes them. Running `--merge-log` as RULES.md says leaves a config line
naming a file that no longer exists, and nothing ever says so. Any metarepo that names a record
or an index in `entry_files` hits it, and no one has to work against jig to get there. It is
general: keep it.

#### Change
In `cmd_merge_log` (ideas-log's shape), nothing else:
1. `kept_entry = [LOG, *[e for e in entry if e not in removals and e != LOG]]`, built from
   `removals` (registers, `CHANGELOG.md`, the folder's records and any index the plan removes),
   not `gone`.
2. One condition, `entry_changes = entry is not None and (files_in or any(e in removals for e in entry))`,
   guards two things: the dry run's `entry_files: … → …` line and the `planned[META]` write
   (staged with the rest of `planned`). A run that merges files keeps rewriting META as today. A folder-only run
   rewrites it only when `entry_files` names something removed, so a run that removes nothing
   it names leaves META byte for byte (no reorder to put the log first).
3. An item is a removal only when it equals a removed path. A glob (`docs/decisions/*.md`) is
   never dropped: it names a place, and a new file there is meant to match.

## Done when

From bug-next-stale-gate:
- [ ] Smoke (`sec_next`), the report's case: gate, no check recorded, then a fix,
  review-change and a new handoff. `jig next k` prints `k: gate — hubnode, continue the hubnode`,
  naming the checkout's commit, the note's commit and `` `jig gate k` ``. It doesn't print
  `check` (the symptom gone).
- [ ] Smoke: in that stale checkout, `jig checked --tier 3 --effort 4 --seconds 1` exits
  non-zero, names the newest note's commit and `jig gate k`, and `checked.log` gains no line.
- [ ] Smoke: a check recorded in the checkout before the new handoff doesn't make `jig next`
  say mark gated. It says gate, and `jig mark k gated` exits non-zero naming `jig gate k`, with
  the checkout still there and the board unchanged.
- [ ] Smoke (the fix fires end to end): after the refusals, `jig gate k` rebuilds the checkout.
  Its HEAD's first parent (or HEAD) is the new note's commit, `jig next` says check, `jig
  checked` records, `jig mark k gated` accepts, and `jig merge k` merges.
- [ ] Smoke, Repro B: with k marked gated, a fix and review-change, `jig handoff` in k's
  worktree exits non-zero naming `jig mark k ready`. After the hubnode marks k ready and
  commits, the handoff goes through and `jig next k` says gate.
- [ ] The existing `sec_next` cases still pass: one handoff, gate, check, mark, merge.
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh` (complete, the check role's) and
  `claude plugin validate ./plugin` pass. `grep -rnE 'Maige|maige|Daisy|daisy|"E-' plugin`
  finds nothing.

From bug-merge-log-entry-files:
- [ ] Smoke (`merge_log`), the symptom: the report's fixture (case reg above) on a metarepo
  job's branch. After `--apply --merge-log` and the commit, `entry_files` is
  `[".jig/decisions.md"]`: it names neither `DECISIONS.md` nor `docs/decisions/README.md`. The
  output's `entry_files:` line shows that list, and `jig rules` passes. Today it ends
  `['.jig/decisions.md', 'docs/decisions/README.md']`.
- [ ] Smoke (`merge_log`), the fix firing where today nothing runs: case folder above (no
  register, log already named). The dry run prints `.jig/meta.json entry_files:
  ['docs/decisions/README.md', '.jig/decisions.md'] → ['.jig/decisions.md']`. `--apply` stages
  `.jig/meta.json` with that list, and the commit passes the hooks. Today no line prints and
  META isn't staged.
- [ ] Smoke (`merge_log`): an index with prose left after its record rows (kept, rewritten)
  stays in `entry_files`. A glob item (`docs/decisions/*.md`) stays as written.
- [ ] Smoke (`merge_log`): a folder-only run in a metarepo whose `entry_files` names nothing
  removed leaves `.jig/meta.json` unstaged and byte for byte.
- [ ] Every existing `merge_log` and `metarepo` smoke case passes unchanged:
  `python3 .jig/jig.py queue -- bash tests/smoke.sh merge_log metarepo`.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and the full smoke passes.

## Out of scope

From bug-next-stale-gate:
- Recording on the board which commit a job was gated at. Repro B is closed by refusing the
  handoff, which uses the order `jig next` already prints. A record would be a new ledger for
  the same guarantee.
- Changing `jig merge`'s test. Once a checkout can't be gated stale and a gated job can't hand
  off again, its newest-note test is the right one.

From bug-merge-log-entry-files:
- A metarepo that already committed a dangling name with the old code. The trunk rerun can't
  edit META (M4), and no repo is known to have one: this report comes from a review of
  ideas-log, not from a merge in the wild. Its owner removes the line in a job.
- A general check that every literal `entry_files` item matches a file. That is a new rule,
  not this fix, and no report asks for it.
- A glob that matched only removed files. It stays as written, per Change 3.
- `split-merge-log`, the waiting spec that renames `--merge-log` to `jig migrate-log`. It is a
  separate spec. Whichever of the two runs second carries the other's change.

## Touches
- `plugin/templates/jig/jig.py`: a new `gate_holds`, plus `chain_step`, `cmd_checked`, the
  gated branch of `cmd_mark`, and `cmd_handoff` (bug-next-stale-gate); `cmd_merge_log` only
  (`kept_entry`, its print, the META write into `planned`), on ideas-log's shape
  (bug-merge-log-entry-files). Nothing in `cmd_merge`, `cmd_gate`, `next_step`'s gated branch
  or `record_plan`.
- `plugin/templates/jig/RULES.md` (Workflow steps 1 and 2, the `jig checked` paragraph). Its
  Decision log bullet on `entry_files` is not touched: it already promises the merge-log fix.
- `plugin/skills/hubnode/SKILL.md` (Gating a handoff, step 5)
- `tests/smoke.sh`: `sec_next`, and section `merge_log` (`sec_merge_log`), new cases beside the
  metarepo job case (`MM`, `ml-meta`) and the records cases (`mlrecs`).
- `.jig/decisions.md` (`## Unreleased`, `### Fixed`)
- Not touched: other skills, docs, `marketing/FEATURES.md` (two fixes, no new feature).
- Process or product: product (jig's behaviour).

## Alternatives considered

From bug-next-stale-gate:
- Check only in `jig next`, as the report's first item asks. Rejected because `jig checked` and
  `jig mark gated` would still record and gate the stale commit for anyone not reading `next`
  (Repro A) — reason is [seen].
- Have `jig next` or `jig checked` rebuild the stale checkout themselves. Rejected because `jig
  gate` is the hubnode's step and carries refusals (fold-in, pairs, R8, board pages) that a
  silent rebuild would skip. `next` and `checked` only read and record — reason is [seen]
  (cmd_gate, jig.py:3288-3440).
- Compare by "the note's commit is an ancestor of the checkout's HEAD" instead of HEAD or
  first parent. It works too, since trunk never holds a job's commits before its merge. Rejected
  because HEAD or a merge's first parent names exactly what `jig gate` builds: `cmd_gate` checks
  out the note's commit detached, and `merge_trunk` runs `git merge --no-edit <trunk>`, which
  leaves HEAD at the commit when it already holds trunk, or makes a merge whose first parent is
  the commit (a fast-forward would need trunk to hold the job's commit, which it doesn't before
  the merge). An ancestor test would also accept commits added on top in the checkout — reason
  is [seen] (`cmd_gate`, `merge_trunk`).
- For Repro B, store the gated commit on the job's board entry and have `next` and `merge`
  compare against it. Rejected as a new record for a guarantee the handoff refusal gives with
  none (a need jig already handles uses that path) — reason is [seen] (`next_step`'s gated branch
  already names the order).
- Leave Repro B out as a separate bug. Rejected because it's the same root (the gate's check
  isn't tied to the newest note) in the same files, and it lets an unchecked commit merge —
  reason is [seen] (Repro B).

From bug-merge-log-entry-files:
- Drop removed items in `record_plan` and hand META to it as its own write. Rejected because
  META is cmd_merge_log's: `record_plan` knows nothing of `files_in`, and splitting one list's
  edit across two functions brings back the two-writer shape ideas-log removed. Reason is [seen]
  (ideas-log's one-plan comment, jig.py:15077).
- Rewrite META whenever `kept_entry != entry`. Rejected because `kept_entry` puts the log first,
  so a folder-only run whose list holds the log second would reorder META with nothing removed.
  That is a META diff in a metarepo job for no reason. Reason is [seen] (case folder's list,
  `['docs/decisions/README.md', '.jig/decisions.md']`, shows the order is the owner's).
- A trunk-side repair in the `stale_board_names` rerun, as for the board. Rejected because
  META changes on a metarepo's trunk only through a reviewed merge (M4), and the branch run
  already holds every removal. Reason is [seen] (`branch_needed` die, and the trunk rerun
  writes only CONFIG).
- Warn about the dangling name (a `jig update` or `jig rules` line) instead of preventing it.
  Rejected as a workaround: it reports the symptom after the commit, where the run that made
  it could have avoided it. Reason is [seen] (the run already computes `removals`).
- Drop globs that match a removed path. Rejected because a glob names a place, and RULES.md
  says a new page there needs no edit. Reason is [seen] (RULES.md Metarepo, `entry_files`).

## Decisions

From the consolidation:
- Opens after ideas-log merges (its `cmd_merge_log`/`record_plan` rewrite is the merge-log fix's base). The owner's word, 2026-11-24: "consolidate those bug jobs if possible". The stale-gate fix waits with it.
- bug-next-stale-gate's Change 5 (`jig handoff` refuses while trunk's board says the job is gated) is in: a second hole of the same root.

From bug-next-stale-gate:
- `gate — hubnode` is the step for a stale checkout, not check, because `jig gate` is what
  rebuilds it (the report's first Done-when item).
- Repro B is in scope: same root, no file added to Touches. Cutting it means dropping Change 5 and its Done-when item.

From bug-merge-log-entry-files:
- Written against ideas-log's shape: `removals` and `planned[META]` exist only there. On trunk
  the same two changes are the `kept_entry` line and the `if entry is not None and files_in`
  guards (jig.py:15512-15513, 15560, 15566).
- The second half of the report (META is rewritten only `if files_in`) is the same root, and
  Change 2 fixes it.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
