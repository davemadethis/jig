# Handoff: moving-in-command

Commit: 4d1d79df3f626f10a376ad509c5d14a60ef6e7ec
Date: 2026-11-24
Spec: .jig/specs/moving-in-command.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part C of moving-in-command, with its bug spec bug-move-spec-lifecycle (7f10d7b): `jig move <what> --to <repo> [--as <path>] [--apply]`.
- One reader, `move_state`, gives a move's state from its spec's `- move:` record and the receiver's trunk; `jig move` and rig (`move_wait`) both call it.
- Step 1 writes `.jig/specs/move-<slug>.md` (its Touches the moved thing alone) and sends the text with its moved-from pointer: staged and forwarded down or sideways; up, a `propose/` branch whose commit the metarepo's hook judges, carrying the page's items into the metarepo's own phases. Down or sideways, step 1 is done once the spec records it; a drop is the owner's word (delete the spec, and step 1 sends again).
- Step 2 runs in the job opened from the move's spec in every repo, refused in a trunk checkout naming that job (M4 in a metarepo). It removes the thing with its move line. Sideways it proposes the metarepo's rewrites of its pointers to the moved thing (by `pointer_parts`/`same_thing`, an entry by its landed id, a section by the longest heading beginning the cited text, an id cited in the log or the ideas file), or writes `meta: none` when there is nothing to propose. `jig merge` closes the spec, keeping it in a pararepo while it names a metarepo branch, and moves the losing roadmap's items (`items_follow_moves`); a receiver keeping its own roadmap gets a staged file, forwarded after the merge.
- rig waits a move's spec on its receiver until step 2 is next; a spec listing buffer rows, or a move spec whose proposal was withdrawn, is a record and never waits.
- Synced with roadmap-labels: on a `propose/` branch a section the fork has is judged by the fork's glossary and a new one by the commit's own; a move's proposal may add to the receiver's sections only the items that follow the moved page (Interpreted, the hubnode, 2026-11-24).
- Synced with ideas-log: an id is found in the log or `.jig/ideas.md`; an open entry moves up into the metarepo's ideas file; step 2 takes an idea out of the ideas file; a cached pointer to a moved idea reads `(moved: …)`.

## Done-when evidence
- Part C and bug-move-spec-lifecycle's items, in smoke `move` (all PASS at 7818f73): down both ends with rig waiting then Can start now and a finished move quiet; a page down with items; up D-002 in L's job with the spec kept; up withdrawn, re-proposed, numbered, and step 2's job opening unrefused; sideways in L's job with pointers, the spec kept, and `jig sync` following the branch; Q up and sideways with its own roadmap; down to Q's own roadmap; lu/ls/lq item routes; a landing in progress (S3); dropped on the owner's word; records aren't work (a buffer spec, and move-in.md in `movein`); up a contract page in N/V: trunk refusal naming `jig open move-docs-v-md --spec …`, the gate refusing on the pin, then passing once N's release is pinned, merge printing `kept`, sync printing `released by`; sideways with nothing to propose writing `meta: none` and the merge closing the spec; N5 by thing (entries, sections, Power/Powertrain, ideas); an idea up both steps; a cached pointer to a moved idea read as moved; the roadmap-labels guard cases (an item not touching the page, a changed receiver line, no matching move line, another repo's move line: each refused; the matching item passes).
- `grep -c 'is done once this commits' plugin/templates/jig/jig.py` → 0.
- At 08bf5f5: `python3 .jig/jig.py queue -- bash tests/smoke.sh move moves movein close sync_buffer pararepo rig roadmap labels metarepo boundary staging decisions supersede removals pin_bump claims family family_report roadmap_edit` → PASS 913, FAIL 0.
- At 907a1dd: the same list less family_report, plus `ideas ideas_fold ideas_meta ideas_labels` → PASS 961, FAIL 0.
- At 4d1d79d: `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0; `claude plugin validate ./plugin` → ✔ Validation passed; `python3 .jig/jig.py queue -- bash tests/smoke.sh update_roles` → PASS 38, FAIL 0. The gate's complete check at 7818f73 passed every other case.
- At 7818f73: `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0; `claude plugin validate ./plugin` → ✔ Validation passed; `python3 .jig/jig.py queue -- bash tests/smoke.sh move moves movein pararepo sync_buffer` → PASS 283, FAIL 0, isolation passing.

## Review
- review-work of Part C at e6d557f: B1 sideways items to the wrong plan, B2 an up move forwarding a roadmap file instead of `propose/`, B3 `Later:` ids not taken, B4 a finished move's spec offered as work. Fixed in 4e57127.
- review-change of 4e57127: blocking. Pointers proposed at step 1 could merge before the receiver had the page; deleting a spec naming a pointers branch broke `jig sync`. Fixed in c40ea6c (pointers back at step 2; P2's deleted-spec read reverted on the hubnode's word).
- review-change of c40ea6c: blocking B1 (P2 refused step 2 of an up contract page; sideways with no branch), B2 (the staying spec offered by rig, nothing closing it), S3 (a landing in progress read as dropped), O4 (a warning about an item step 2's own proposal moved). Third blocking review: the bug role wrote bug-move-spec-lifecycle (7f10d7b), the owner confirmed it; built in 67e8c87. O4 is that spec's Out of scope.
- review-change of 08bf5f5 (67e8c87, the roadmap-labels sync 5aece4e, 08bf5f5): blocking B1 (a withdrawn move spec offered as work and blocking the re-proposal's job), B2 (`§ Power` rewriting `§ Powertrain`); should-fix S1 (the move exception lent by another repo's move line), S2 (the rename Interpreted line and bug-move-in-record's wording). All fixed in b239c52; the reviewer judged the one-commit rename a consequence of the two agreed rules.
- review-change of 08bf5f5..907a1dd (the ideas-log sync 42ddb5d, a41708b, 907a1dd): 0 blocking. Should-fix: N5 for ideas, RULES on idea moves, RULES on withdrawn move specs — taken in 582a8f3. Optionals (idea removal's blank lines; `## Open` up into an unfolded log; a hand-written ideas-form moved-from source) in DEFERRED.md.
- review-change of 907a1dd..582a8f3: 0 blocking. S1 (`moved_to` for ideas) and O1 (comments) taken in 7818f73. O2 confirmed in a throwaway family: left to its own bug spec (Left).
- review-change of 582a8f3..7818f73: 0 blocking. One optional (the comment above `moved_to`'s id branch) in DEFERRED.md.
- The gate at 7818f73 failed one case, `update roles: no repo name and no exception list in jig.py or the update skill`: `phase_part`'s docstring used an adopting repo's name as its example. 4d1d79d makes it `Prod alpha` / `Prod No phase`; `grep -rnE` of that case's name list over plugin/ finds nothing. review-change of 7818f73..4d1d79d: 0 blocking.

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
- [x] docs/commands.md — updated: `jig move` moves an entry, page or section to another repo of its family, one step per `--apply`   (3 files)
- [x] docs/hooks.md — no change because it names each hook's job in general terms, and none changed job   (1 file)
- [x] docs/jobs.md — no change because a move's job opens, gates and merges as any job does; its spec closing or staying is RULES' detail   (2 files)
- [x] docs/metarepos.md — updated: Moving claims says the removal runs in a job opened from the move's spec in any repo, its merge closing the spec, and a drop is the receiver's owner's word   (2 files)
- [x] docs/records.md — no change because its decision log, ideas and staging sections stay general; moves are metarepos.md's   (4 files)
- [x] docs/workflows.md — no change because the rig's picture and every role and step are as described; what a move's spec waits on is RULES' detail   (3 files)

## Shared files changed
- `plugin/templates/jig/jig.py`: `jig move` and its reader, rig's waits, `waiting_specs`, the propose/ section rule's owners and move exception, staging resolve and the move-line checks with ideas, `moved_to`.
- `plugin/templates/jig/RULES.md`: The board (waiting), Workflow (rig), the roadmap edit command (propose/ owners, the move exception), Decision log (ideas moving, the moved-from target), What the metarepo holds (Moving claims).
- `tests/smoke.sh`: `sec_move` reworked into jobs, with U, N/V and the guard cases; `sec_movein` (records aren't work; the one-commit rename); `sec_moves` and `ideas_meta` fixtures for the moved-from line; UNITS.
- `docs/metarepos.md`, `plugin/skills/hubnode/SKILL.md`: step 2 in a job in any repo; a drop is the owner's word.

## Test by hand
In a metarepo M with pararepos L and K (`jig repos` knowing all three):
- In L, `jig move docs/x.md --to K --apply`, commit the spec, and run `jig rig`: the spec waits on K. Resolve and merge the staged file in K; rig in L then offers it.
- In L's trunk checkout `--apply` is refused, naming `jig open move-docs-x-md --spec …`. Open that job, run `--apply` in its worktree, commit, hand off and merge: M gets `propose/L-move-docs-x-md-pointers` if it cites `L/docs/x.md`, else the spec carries `meta: none` and the merge closes it.

## Left
- Nothing on this job.
- For its own bug spec (the hubnode opens it after the merges): `pointer_gap` never resolves an id pointer, so `dangling` lists a metarepo's cached pointers to a pararepo's live entries and ideas as stale (`… which .jig/decisions.md has no heading for`), and P2's id comparison never fires. Seen in a throwaway family at 7818f73; it predates this job. Its row is in DEFERRED.md (should-fix).
