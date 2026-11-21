# Handoff: move-to-pararepo

Commit: 07495e1ccf1629a2f24c821094043c782cb6356d
Date: 2026-11-21
Spec: .jig/specs/move-to-pararepo.md
Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-20 / Dave, on his word: "file a short jig feedback for moving entries and pages; leave them here meanwhile" (staged as feedback-maige-ecosystem-2026-11-20-move-entries-and-pages.md): "jig can't move a decision entry or a page from a metarepo down to the pararepo that owns it. A released entry can't leave the log at all, and a page that leaves reads as removed."
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
A metarepo can move a decision entry (released or Open), a page or a page's section down to the pararepo that owns it. It does this with one line under `## Unreleased` `### Removed`: `- E-085: moved to <repo>/.jig/decisions.md § D-016.`, `- docs/x.md: moved to <repo>/docs/x.md.` or `- docs/x.md § H: moved to <repo>/docs/x.md § H.`
- **The hook checks a move line the change adds** (`move_rules`). The line must be under ## Unreleased; a move-shaped line elsewhere is refused. Each id, page or section takes one line, and a line not yet released may be corrected in place. The repo must be in `pararepos`. A moved id must be an entry the change removes, and not one a live entry supersedes. The page or section must be gone from this repo. The target must be on the pararepo's trunk, read through `trunk_show` (an id matched by number, a heading by `pointer_gap`), and a missing target is refused, naming the file read. An unreachable repo warns and passes. An entry superseding a moved id is refused.
- **The strike line has one reason.** `struck_ids` frees a released entry only for `project scope, not a product decision.` or a move line, and the refusal names both forms.
- **One reader.** `moves_in`, with `Moves` keyed by `move_key` (E-2 is E-002), feeds `hold_chain` and `holds_now` (the chain ends at the pointer), `jig decision`, `reading-list --claims`, `--peers`, `meta_citations` ("…, which M vX moved: now <home>"), `stage_pin_bumps` ("(moved: <home>, this repo)", "n moved"), `changes_report` and the dead-touch refusal in `boundary_rules` (it names the pointer and `target: <repo>`).
- **`trunk_show(loc, path)`** is lifted from `meta_citations`' nested `live`; `meta_citations` and `move_rules` call it.
- **The pin bump's bare-id grep** skips jig's own `.jig/` files, as `meta_citations` and `used_in` do.
- **RULES.md** is updated in five places: Released sections, What the metarepo holds, A pin-bump request, Versioning Z, Roadmap (A touched page exists).

## Done-when evidence
All items: `python3 .jig/jig.py queue -- bash tests/smoke.sh moves decisions supersede removals pin_bump pararepo staging claims boundary roadmap` at 07495e1 → rc=0, 467 PASS, 0 FAIL (smoke output: move-to-pararepo-smoke-4.out in the hubnode's notes folder). The `moves` cases, item by item:
- The strike has one reason: "PASS moves: a strike line giving another reason doesn't let released E-002 go, and the refusal names both lines"; "PASS moves: the strike line still lets it go".
- The text lands first: "PASS moves: the three staged files forward to L"; "PASS moves: L numbers the landed entries, accepted D-002 keeping E-002's who and date, and Open D-001". `jig merge --number` numbers in file order, so Open E-004 is D-001 and E-002 is D-002.
- The move line is checked: "PASS … naming § D-009 / nope.md / § Nope / X is refused, naming what it read"; "PASS … with L out of the repos file, the move passes with a warning naming L"; "PASS … removing E-002 and E-004, the page and the section, with move lines naming L's trunk, commits". Plus the review cases: "… under ## Open is refused", "two move lines for one id in one change are refused", "… an id a live entry supersedes is refused", "… an id this change doesn't remove from the log is refused", "a second move line for an id the log already moves is refused", "a merged, unreleased move line corrected in place commits …", "a later entry superseding a moved id is refused", "a move-shaped line naming a pararepo under ### Changed is refused".
- Roadmap items follow the page: "PASS moves: the merge is refused while the roadmap touches the moved page, naming both, the pointer and target: L"; "PASS … a staged roadmap change to L forwards there"; "PASS … with charge dropped and the page out of alpha/battery's touches in the merge commit, the merge passes"; "PASS … a job moving only walyt.md § Mods merges with the roadmap untouched".
- History reads the move: "PASS moves: jig decision E-002 names the release it stood in and the move"; "… E-001 walks to E-002, then the move"; "… E-004 names § D-001"; "… reading-list --claims E-002 names the move in its note".
- Frozen citations still pass: "PASS moves: the frozen E-003, citing E-002 and E-004, is unchanged and the log passes".
- The symptom is gone: "PASS moves: the release stages L's pin bump, every id and page moved, nothing removed or missing". It checks `L: staged … (5 moved)`, each id `(moved: …, this repo)`, the pages ending `now docs/battery.md, this repo`, and no `(removed)`, "doesn't have" or "has no heading for". "PASS moves: L's jig sync lists E-002 and E-004 as moved". The page lines read "…, which M v0.1.1 moved: now …" rather than the spec's "doesn't have …: now …"; that rewording is what keeps "no doesn't have" true.
- One live read: "PASS moves: one live read of another repo's trunk: trunk_show, defined once, called by meta_citations and move_rules"; `git grep -n 'def live\b' plugin/templates/jig/jig.py` → no match.
- No regression: the run above; `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0; `claude plugin validate ./plugin` → "✔ Validation passed" (at fe41996; no plugin manifest or skill changed since).

## Review
- **review-work of fe41996** (tier 2, effort 2): 1 blocking, recorded. Fixed in 548e614 and c7fcf6b.
  - Blocking: a move line under `## Open` was read but not checked. `moves_in` now reads Unreleased and releases only, and a misplaced line is refused.
  - Should-fix: a second move line for one key. Refused, in the log or in one change.
  - Should-fix: a move of a superseded id, or of one not removed. Refused.
  - Optional, taken: `E-2` keys. Normalised by `move_key`.
  - Optional, deferred: backticked headings; `changes_report`'s `endswith`.
  - c7fcf6b also fixes a pin_bump regression that 548e614 introduced: a fixture id in a docstring.
- **review-change of c7fcf6b** (tier 2, effort 2): 0 blocking, recorded. Its should-fixes were all taken in 07495e1:
  - an in-place correction of an unreleased move line;
  - an entry superseding a moved id refused;
  - the pin bump's grep skipping `.jig/`, with the `E-085` comment made generic.
  - Optional (a), taken: a move-shaped line outside `### Removed` refused.
  - Optional (c), taken: target ids matched by number.
  - Optional (b) and (d), deferred.
- **review-change of 07495e1** (tier 2, effort 2): 0 blocking, recorded. The remaining optionals are deferred.

Every untaken finding has a row in `.jig/ledgers/DEFERRED.md`, in this commit.

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
- [x] UNOWNED plugin/templates/jig/jig.py — add to docmap (a new page starts from .jig/docs-page.md), or no page needed because the repository's own tooling needs none: its rules are `plugin/templates/jig/RULES.md`, changed here in the five places the spec names (the repository's own tooling, its build, CI, release and dev scripts, needs none)

## Shared files changed
- `plugin/templates/jig/jig.py`: the new helpers `STRIKE_WHY`, `MOVE_LINE`, `move_key`, `Moves`, `log_move_lines`, `move_held`, `moves_in`, `pointer_parts`, `shown_pointer`, `moved_to`, `trunk_show` and `move_rules`. Changed: `struck_ids`, `frozen_problems`' message, `check_rules` (one call), `hold_chain`, `holds_now`, `cmd_decision`, `claims_of_id`, the `--peers` die, `meta_citations` (its new `ours` parameter, `live` lifted to `trunk_show`), `stage_pin_bumps` (`broken`'s `here`, the hopped ids, the counts, and the `.jig/` filter on its bare-id grep), `changes_report` and `boundary_rules`' dead-touch message. All in the spec's Touches.
- `plugin/templates/jig/RULES.md`: the five places the spec names.
- `tests/smoke.sh`: the new `moves` section (`sec_moves`, after `sec_pin_bump`, 31 cases), and `moves` added to UNITS. No existing case was edited.

## Test by hand
Nothing to click. The owner's check is the Maige repos: with maige-ecosystem's hubnode, move one entry (say E-085) down to Maige-Lite once its D-entry has landed there. Then confirm that `jig decision E-085` names the pointer and that the next release's pin bump reads `(moved: …)`.

## Left
Nothing on this spec. The deferred findings are in DEFERRED.md. `cross-repo-roadmap` follows and can reuse `trunk_show`.
