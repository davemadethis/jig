# Handoff: layout-and-formats

Commit: 192699c633d2c241dfd262030f121db203549d0d
Date: 2026-11-25
Spec: .jig/specs/layout-and-formats.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part 3 of 5: `Later:` is retired. A spec takes only what it builds. Work it doesn't build stays on
the roadmap, unspecced. A scope built only in part is split first by a roadmap change on the owner's
yes: the built part becomes a new scope the spec takes, and the rest stays under the original id,
its text unchanged, so a wait on that id holds until the rest is built. Out of scope never defers.
The hook refuses a spec with a `Later:` line in its header (`later_line`). `jig update --apply`
deletes that line from each spec on trunk and names each one; handoff notes keep theirs, as
history. These are gone: the gate's later lines (it shows only the Out of scope lines), the merge
carrying `Later:` onto the note, rig's Left for later and its `--json` `later` key, the `Later:`
half of `cited`, `scope_holders`, the pararepo warning, `move_in_takers` and `roadmap_takers`, and
move-in's re-pointing of `Later:`. RULES, the spec template, and the spec, review, work and hubnode
skills carry both rules, and the bug and rig skills were updated. When a split lands on trunk for
an open job, the hubnode tells the work session, which syncs and re-points its spec's `Scope:`
line to the new scope.

## Done-when evidence
Part 3's items. Parts 4 and 5 are still to do.
- check at 192699c, `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc 0.
- `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap close` at 192699c: rc 0, 238 PASS,
  0 FAIL. At c60062e, `roadmap roadmap_edit family close rig movein move update`: rc 0, 580 PASS,
  0 FAIL.
- `Later:` gone from jig.py: `grep -n Later plugin/templates/jig/jig.py` finds the refusal
  (~725-728), `LATER_LINE`/`later_line` (~12199-12210), and update's step (~14819-14860). The one
  exception is `SEED_COMMENT` (~11926). It quotes the old seed's comment, which named `Later:`,
  and the conversion drops that comment only when it matches byte for byte, so it must stay.
- The refusal: `smoke roadmap` covers "a spec with a Later: line is refused, saying the work stays
  on the roadmap, unspecced, and to delete the line", a changed spec still carrying one, and no
  roadmap on trunk. `smoke family` covers it in a pararepo. A fenced example in a spec's body
  commits.
- update's step: `smoke roadmap` "jig update --apply deletes a Later: line from each spec on trunk,
  naming each, leaves a body's example and a note's", and its commit passes.
- Gate, merge and rig: `smoke close` (the gate shows only the Out of scope lines, under the file
  for a Bug-for spec; the merge writes no `Later:`; rig has no Left for later and no `later` key).
- Move-in: `smoke family` D (a note's `Later:` is left as history and the move-in passes),
  `smoke movein`, `smoke move`.
- The two rules in RULES (§ Roadmap), the spec template, and the spec, review, work and hubnode
  skills. `grep -rn 'Later:' plugin docs` (jig.py aside) finds only RULES's line on the refusal and
  update's step.
- decisions.md Unreleased: an Added line for update's step, and Changed, Breaking and Removed
  lines.

## Review
- review-change of 38745c0..72ad4c2: 1 blocking (strike 1 for part 3): the spec template's Scope:
  comment didn't carry rule 1. Should-fix:
  - a split never re-pointed the open job's spec;
  - the SEED_COMMENT grep exception (named above);
  - review blocked only Out of scope prose.

  Optional:
  - `Later:` matched anywhere in the spec;
  - a stale comment;
  - no Added line.

  All taken in c60062e. One more optional (a Bug-for spec only on an unmerged branch) was deferred
  with a row.
- review-change of 72ad4c2..c60062e: 0 blocking. Should-fix: the template's other half of rule 1.
  Optional: "in its header" wording. Both taken in 192699c. Two optionals deferred with rows
  (`later_line` reads the header only; it recomputes `note_head`).
- review-change of c60062e..192699c: 0 blocking. One should-fix: the template's "takes the new
  scope … whole, in its own words if it likes". It goes in part 4's first commit (Left).

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
- [x] docs/commands.md — updated in part 2; part 3 changed no command's syntax, and rig's Left for later was never in it
- [x] docs/hooks.md — no change because it describes the plugin's hooks.json, not the spec checks
- [x] docs/jobs.md — updated: the merge keeps only the spec's `Scope:` line on the note
- [x] docs/metarepos.md — no change because it never named `Later:`; move-in re-points `Scope:` lines as it says
- [x] docs/records.md — updated: a spec takes only what it builds, the split, and out of scope never defers
- [x] docs/workflows.md — updated: rig no longer lists work left for later
- [x] UNOWNED tests/roadmap.py — no page needed because it is smoke's own tooling (the repository's own tooling, its build, CI, release and dev scripts, needs none)

## Shared files changed
- `plugin/templates/jig/jig.py`, `plugin/templates/jig/RULES.md`, `plugin/templates/specs/_template.md`:
  the refusal, update's step, and the `Later:` readers removed.
- `plugin/skills/{spec,review,work,hubnode,bug,rig}/SKILL.md`: the two rules; rig's Left for later
  removed.
- `tests/smoke.sh`, `docs/jobs.md`, `docs/records.md`, `docs/workflows.md`, `.jig/decisions.md`
  (Unreleased), `.jig/ledgers/DEFERRED.md` (three rows).

## Test by hand
In a repo whose spec carries `Later: <id>` in its header (committed by an older jig): run `jig update`.
It names the spec and the ids, and `--apply` deletes the line and nothing else. Then commit a spec
with a `Later:` line: the hook refuses it, saying to delete the line.

## Left
Parts 4 and 5: one glossary form with `Repo:`/`Kind:`, then the rules and templates folders,
lowercase names, "the owner" and the designer. Part 4's first commit also takes the should-fix
from the review-change of c60062e..192699c: the spec template's Scope: comment says the spec takes
the new scope "whole, in its own words if it likes". Part 5's first commit corrects the designer
list and adds the `rigger` key's scan and write to its Breaking list (from part 2's note).
