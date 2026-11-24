# Handoff: moving-in-command

Commit: 04f0ea62a60c67c9f8d133e3c32eeb56cfa55ec3
Date: 2026-11-23
Spec: .jig/specs/moving-in-command.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part A of moving-in-command, with bug-move-in-record (its bug spec after the third blocking review):
- `jig move-in --product <Name> [--definition] [--apply]` in a pararepo's trunk checkout, one step per `--apply`.
  Step 1 proposes the product's phases (headings and refs mapped) and, when the metarepo has none, its glossary
  term, as one `propose/<repo>-move-in` commit made in a temporary worktree of the metarepo, which the metarepo's
  hook judges. It writes one BUFFER row and a spec listing it alone. Step 2, once the metarepo merged it, stages
  `git rm` of the roadmap and its view and re-points every `Scope:` line.
- Step 2 reads the product from step 1's record, found by scanning specs. `--product` is the owner's word for
  a rename at the merge. A re-proposal after a withdrawal takes `move-in-2`, and the withdrawn spec stays.
  The move-in row is `jig move-in`'s alone: no release or `propose --buffer` carries it.
- In a metarepo, the hook reads a commit's product headings by the commit's own glossary, and refuses a
  commit or merge that leaves a product's headings without the `Owner:` either side gave.

## Done-when evidence
- Part A's items (plan, one proposal, one merge, term edges, map edges, removal, moved in), and every item of
  bug-move-in-record's Done when: smoke `movein`, 43 cases, all PASS at 04f0ea6.
- `grep -c 'def moved_in_as\|withdrawn-{n}' plugin/templates/jig/jig.py` → 0.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0.
- `claude plugin validate ./plugin` → ✔ Validation passed.
- `python3 .jig/jig.py queue -- bash tests/smoke.sh movein moves pararepo metarepo roadmap rig boundary staging
  decisions supersede removals pin_bump claims sync_buffer family phase_types buffer_answered` → rc=0, 742 PASS,
  0 FAIL.

## Review
- review-work of 81b4852: 1 blocking (step 2 missed a proposal `jig merge` had deleted), fixed in 16d6184,
  with S1-S4 and O1, O3 and O4. O2's three items are in DEFERRED.md.
- review-change of 16d6184: 2 blocking (owner check against trunk's tip; the `kept` filter), fixed in c47c2d5,
  with S1, S2, O1-O4.
- review-change of c47c2d5: 1 blocking (product guessing), so the bug role wrote bug-move-in-record. It was
  built in 9ac1ee9.
- review-change of 9ac1ee9: 1 blocking (a withdrawn move-in row swept into a buffer proposal), fixed in 476bc9c,
  then synced with trunk (phase-types) in ac61d68. a9fc7c8 renamed family D's hand-made row.
- review-change of a9fc7c8: clean. Its two should-fixes and the optional were taken in 04f0ea6.
- review-change of 04f0ea6: clean. Its two should-fixes (the remaining "every Open row" places; "proposes it
  again" while a live record carries the row) and its optional (RULES Moving in step 1 on a rerun) are taken in
  Part B's first commit, so Part B's review-work covers them.
- Not caught: SIGTERM, SIGHUP, and a second Ctrl-C during the undo's `finally` (DEFERRED.md).

## Fold-in
<!-- Every documentation page that covers code this changed: does it still describe the
     code? Replace each ___ and tick the box: the stale sentences are edited (deleting
     counts), or none went stale and this says why. Each roadmap item naming one of those
     pages (an Up next item, or a taken scope) has its own line: keep one answer, built,
     untouched or departed: <why>. An Up next item answered built leaves the roadmap when
     the job merges. The gate refuses an unanswered line. An UNOWNED file has no page
     covering it: add it to docmap in the board, or say why it needs none. A pair line
     (`<id> vs <log> § <ids> (<page>): ___`) is answered after its colon, once for every id
     on it: agrees, narrows: <how>, or conflicts: <resolution>; on a line of several ids,
     narrows and conflicts name at least one of them. jig reads the rest of the line, so it
     stays as jig wrote it. -->
- [x] docs/commands.md — updated: `jig move-in` added under Across repos   (2 files)
- [x] docs/hooks.md — no change because it names each hook's job in general terms, and the metarepo checks it lists still hold   (1 file)
- [x] docs/jobs.md — no change because the board, jobs and their files are untouched   (2 files)
- [x] docs/metarepos.md — updated: Moving claims describes `jig move-in`, and the release's proposal leaves the move-in row out   (2 files)
- [x] docs/records.md — no change because the roadmap's shape and the decision log's are unchanged; moving in is metarepos.md's   (2 files)
- [x] docs/workflows.md — no change because no role, workflow or step changed   (3 files)

## Shared files changed
- `plugin/templates/jig/jig.py`: the new `moving` section (`cmd_move_in`, `move_in_propose`, `move_in_records`,
  the map helpers, `proposal_commit`, `owner_dropped`, `log_with_line`). It also changes `buffer_proposal`
  (`only=`), `unproposed` (move-in rows out), the glossary read and owner check in `check_rules`, the
  `withdraw_proposal` and `propose --buffer` messages, and the parser.
- `plugin/templates/jig/RULES.md`: Roadmap (Edits, Moving in), the sync buffer, Commands.
- `tests/smoke.sh`: the new `movein` section and its UNITS entry; family D's hand-made move-in row reads "moved
  in by hand", since "moving in" now marks `jig move-in`'s own row.
- `docs/commands.md`, `docs/metarepos.md`, `plugin/skills/hubnode/SKILL.md`: the command and the merge route.
- For later: bug-deferred-scope adds `Later:` lines. Whichever of the two jobs merges second makes `jig move-in`
  step 2 re-point `Later:` lines as it does `Scope:` lines.

## Test by hand
In a pararepo with its own roadmap, run `jig move-in --product <Name> --definition "<sentence>"` and read the
plan. With `--apply`, look at the metarepo's `propose/<repo>-move-in` (`git log -p main..`), merge it there in a
job opened on that branch, then run step 2 here and look at the staged `Scope:` lines.

## Left
Part B (the moved-from record at both ends, moves in any direction), starting with 04f0ea6's review follow-ups.
Then Part C (`jig move`).
