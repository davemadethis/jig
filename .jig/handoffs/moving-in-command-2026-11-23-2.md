# Handoff: moving-in-command

Commit: 6e2fbdd68e279b1355f77a000738eb2d4d650b4b
Date: 2026-11-23
Spec: .jig/specs/moving-in-command.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part B of moving-in-command: a moved claim's record at both ends, in any direction.
- The moved-from line (`- D-016: moved from <repo>/.jig/decisions.md § E-085.`, a page or `<page> § <heading>`)
  under `## Unreleased` `### Added`, read by `moved_from_in`. A `D-?<slug>` there is numbered at the merge.
- `move_rules` runs in every family member: a metarepo's pararepos; for a pararepo, its metarepo and the
  metarepo's other pararepos, matched by checkout. A repo with no family is refused. A move line needs the
  receiver's moved-from line. A moved-from line needs the source still there or a move line pointing here,
  stays while that move line points here, and goes under `### Added`. An unreachable repo or metarepo warns.
- Readers: `jig decision` and `reading-list --claims` name "moved from". `dangling`, P2 and `pointer_cleanup`
  read `(moved: <pointer>)` for a page, section or entry moved away, keeping the removal's answers (a pointers
  proposal or a row). `meta_citations` skips both move records.
- Staging: an optional `moved-from:` header. `resolve` writes the moved-from line for the one entry, the page
  or the section, in the same change.
- First commit 824ca64: Part A's review-change follow-ups (the "every Open row" places, the live move-in
  proposal named by `propose --buffer`, RULES step 1 on a rerun).

## Done-when evidence
- Part B's items, in smoke `moves` (48 cases, all PASS at 6e2fbdd):
  - record lands: L's four moved-from lines, numbered, and `jig decision`/`--claims D-002` (the fixture's
    D-002 stands for the spec's D-001);
  - both ends: E-003 refused until L has its line, then passes; with L out of the repos file, a warning;
  - source checked: E-009;
  - up: D-005 → M's E-010, and `jig decision D-005`;
  - outside the family;
  - sideways: K lands `docs/l.md`, L moves it, and L's sync shows `(moved: K/docs/l.md)` and the moved D-005;
  - no family.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0. `claude plugin validate ./plugin` → ✔ Validation passed.
- `python3 .jig/jig.py queue -- bash tests/smoke.sh movein moves pararepo metarepo roadmap rig boundary staging
  decisions supersede removals pin_bump claims sync_buffer family phase_types buffer_answered glossary pointers`
  → rc=0, 810 PASS, 0 FAIL.

## Review
- review-work of e54d657: 1 blocking (B1: a moved pointer skipped the removal path and named `jig move`).
  Fixed in 6e2fbdd, with S2 (an entry found by id), S3 (unreachable metarepo), S4 (moved-from removal guarded),
  O5 (family by checkout) and O6 (M's moved-from line checked by its hook; a misplaced one refused).
- review-change of 6e2fbdd: clean. Its should-fix (S3's early `continue` ahead of the still-has check), its
  optional (smoke's reset after a failed commit) and its RULES line on re-pointing are taken in Part C's
  first commit. Its optional on `pointer_cleanup`'s row wording is in DEFERRED.md.
- The reviewer answered O5's question: no separate alias case, since a break would be a loud refusal.

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
- [x] docs/commands.md — no change because Part B adds no command; `jig move` is Part C's   (3 files)
- [x] docs/hooks.md — no change because it names each hook's job in general terms, and none changed job   (1 file)
- [x] docs/jobs.md — no change because the board, jobs and their files are untouched   (2 files)
- [x] docs/metarepos.md — updated: Moving claims says claims move in every direction, both ends recorded   (2 files)
- [x] docs/records.md — no change because its decision log and staging sections stay general; moves are metarepos.md's   (4 files)
- [x] docs/workflows.md — no change because no role, workflow or step changed   (3 files)

## Shared files changed
- `plugin/templates/jig/jig.py`:
  - `MOVED_FROM`, `moved_from_lines`/`moved_from_in`/`any_moved_from`, `is_here`, `thing_of`/`thing_key`/
    `same_thing`, `family_names`/`in_family`;
  - `move_rules`, `moved_from_rules`, `moved_to`, `moved_gap`/`dangling`/P2 broken pointers/`pointer_cleanup`;
  - `meta_citations` (skips move records), `cmd_decision`, `claims_of_id`, `read_staged` and `cmd_staging`
    resolve, the `frozen_problems` text;
  - 824ca64: `move_in_left`, the `--buffer` messages and help, the release comment.
- `plugin/templates/jig/RULES.md`: Decision log (Released sections), What the metarepo holds, Staging, the sync
  buffer.
- `plugin/templates/ledgers/BUFFER.md`, `plugin/skills/release/SKILL.md`: "every Open row" but a move-in row.
- `tests/smoke.sh`:
  - `moves` lands each thing with `moved-from:`, its two-entry file split, plus Part B's cases;
  - `family`'s pa lands docs/w.md with its moved-from line;
  - `movein`'s pw cases for 824ca64.
- `docs/metarepos.md`: Moving claims.

## Test by hand
In a metarepo and a pararepo: stage a decision entry to the pararepo with `moved-from: <meta>/.jig/decisions.md
§ <id>`, resolve it there and merge, then remove the entry in the metarepo with its move line. Then try the move
line before the pararepo's merge, and see it refused.

## Left
Part C (`jig move`), starting with 6e2fbdd's review follow-ups.
