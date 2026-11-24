# bug-next-stale-gate: a gate's check counts only for the commit the job's newest handoff note names

Source: jig hubnode session / 2026-11-24 / Dave, with Claude (staged as feedback-jig-2026-11-24-next-stale-gate.md): `jig next` names the check in a stale gate checkout after a new handoff

## Intent
The gate checks the commit the job's newest handoff note names, and nothing downstream trusts
a check of any other commit. A gate checkout built from an older note is stale: `jig next`
sends it back to `jig gate`, and `jig checked` and `jig mark <job> gated` refuse it. A job
already marked gated can't file a new handoff until the hubnode marks it back, so a gated
state never outlives the note it was gated on.

## 1. Why
- Q: Why did `jig next` name the check in a checkout holding 067402b after the ae675c7 handoff? A: `chain_step` sees the checkout exists and its HEAD has no record in `checked.log`, so it says check.
- Q: Why doesn't it see the checkout is stale? A: Nothing compares the checkout's commit to the newest note's `Commit:`. `jig gate` rebuilds it, but only when someone runs the gate again.
- Q: Why does no other command catch it? A: `jig checked` records any HEAD, and `jig mark gated` asks only for a record of the checkout's HEAD. `jig merge` then assumes "the gate checked the commit the latest note names". Root: that assumption has no check behind it.

## 2. Givens (line numbers at trunk 5e40489)
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

## 3. One layer up
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

## 4. Correction
A correction. The commands that act on a gate's check now confirm which commit it covers, and
a gated state can't outlast its note. There's no workaround: the symptom shows in `jig next`,
but `jig checked`, `jig mark gated` and the merge let it through too.

General?: the problem is general. In any repo (regular, metarepo or pararepo), a gate's complete
check fails, the job fixes it, and the job hands off again. RULES.md describes this ("A job may
hand off several times"), and `cmd_gate`'s own comment expects it. An ordinary hubnode follows
`jig next` and gets the stale checkout. Nobody has to work against jig to trigger it.

## Change
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

## Done when
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

## Out of scope
- Recording on the board which commit a job was gated at. Repro B is closed by refusing the
  handoff, which uses the order `jig next` already prints. A record would be a new ledger for
  the same guarantee.
- Changing `jig merge`'s test. Once a checkout can't be gated stale and a gated job can't hand
  off again, its newest-note test is the right one.

## Touches
- `plugin/templates/jig/jig.py`: a new `gate_holds`, plus `chain_step`, `cmd_checked`, the
  gated branch of `cmd_mark`, and `cmd_handoff`. Nothing in `cmd_merge`, `cmd_gate` or
  `next_step`'s gated branch.
- `plugin/templates/jig/RULES.md` (Workflow steps 1 and 2, the `jig checked` paragraph)
- `plugin/skills/hubnode/SKILL.md` (Gating a handoff, step 5)
- `tests/smoke.sh` (`sec_next`)
- `.jig/decisions.md` (`## Unreleased`, `### Fixed`)

## Alternatives considered
- Check only in `jig next`, as the report's first item asks. Rejected because `jig checked` and
  `jig mark gated` would still record and gate the stale commit for anyone not reading `next`
  (Repro A) — reason is [seen].
- Have `jig next` or `jig checked` rebuild the stale checkout themselves. Rejected because `jig
  gate` is the hubnode's step and carries refusals (fold-in, pairs, R8, board pages) that a
  silent rebuild would skip. `next` and `checked` only read and record — reason is [seen]
  (cmd_gate, jig.py:3288-3440).
- Compare by "the note's commit is an ancestor of the checkout's HEAD" instead of HEAD or
  first parent. It works too, since trunk never holds a job's commits before its merge. Rejected
  because first parent names exactly what `jig gate` builds — reason is [assumed] (judgment, not a
  failure case).
- For Repro B, store the gated commit on the job's board entry and have `next` and `merge`
  compare against it. Rejected as a new record for a guarantee the handoff refusal gives with
  none (a need jig already handles uses that path) — reason is [seen] (`next_step`'s gated branch
  already names the order).
- Leave Repro B out as a separate bug. Rejected because it's the same root (the gate's check
  isn't tied to the newest note) in the same files, and it lets an unchecked commit merge —
  reason is [seen] (Repro B).

## Decisions
- `gate — hubnode` is the step for a stale checkout, not check, because `jig gate` is what
  rebuilds it (the report's first Done-when item).
- Repro B is in scope: same root, no file added to Touches. Cutting it means dropping Change 5 and its Done-when item.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
