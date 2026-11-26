# Handoff: layout-and-formats

Commit: 898725ebff6761a8ef7508b644bd7ddca99df6c4
Date: 2026-11-24
Spec: .jig/specs/layout-and-formats.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part 1 of 5: the docmap moves to `.jig/docmap.json`. `docmap`, `boards`, `deep_subsystems` and
`not_docs` leave `.jig/config.json` for their own file, which is trunk-only (R5) and written
sorted. Board.load lays it over the config, so every reader finds the four keys where it did. A
config.json still holding them keeps working until `jig update --apply` moves them. The hook
refuses an unknown key or a value of the wrong shape in docmap.json, and a config.json commit
that carries one of the four. `jig docmap <page|path>` is new. `jig init` writes the file, and
writes none while config.json still holds the keys. Update moves the keys, refuses when both
files hold one key with different values, and bumps STAMP to 13. RULES, skills, docs, the
AGENTS template (with a RETIRED_LINES entry for the old firmware line) and decisions.md follow.

## Done-when evidence
Part 1's items. The rest of the spec is parts 2 to 5.
- init writes docmap.json `{docmap: {}, not_docs: []}` and config.json holds none of the four:
  `smoke docmap` "init writes .jig/docmap.json with an empty docmap and not_docs…" PASS.
- update --apply moves the four keys unchanged and bumps the stamp, and a second run has nothing
  to do: `smoke docmap` "update --apply moves all four keys…" and "a second update reports
  nothing to do" PASS. update's generations: `smoke update` PASS, stamped 13.
- every reader reads docmap.json, and the named sections pass with fixtures writing it (the
  `board` helper writes the four keys to docmap.json): `smoke update board_split
  init_old_board hardware homes meta_docs structure` rc 0; `smoke family findings holders ideas
  movein removals roadmap rules sweep touches next close rig claims glossary page_contract
  pararepo` 784 PASS and 2 FAIL, both fixture expectations fixed in 55232fc; rerun of `roadmap
  findings` rc 0, 187 PASS.
- an unknown key is refused naming the four, and a wrong type is refused for each key:
  `smoke docmap` cases for an unknown key, docmap, boards, not_docs and deep_subsystems all
  PASS. The spec's Done when calls deep_subsystems "a list of strings". The code checks, and
  the refusal names, the folder → rationale map every reader has always read
  (`{"docs/<system>/<subsystem>/<folder>": rationale}`). That is the key's present shape, so
  the spec's words are the slip.
- `jig docmap <page>` prints globs and board or deep subsystem, and `<path>` prints the covering
  pages with no pages-above: `smoke docmap` page, path, uncovered path, board with no entry, deep
  page in either form, and a figure in a deep folder all PASS.
- no skill, rule, template or docs page reads the four from config.json: `grep -rn 'config.json'
  plugin docs README.md` shows only jig.py docstrings and the R5 line naming config.json beside
  docmap.json.
- check: `python3 .jig/jig.py queue -- .jig/scripts/check.sh` rc 0 at 55232fc, 4445ec1 and
  898725e. The last `smoke docmap` run: rc 0, 19 docmap PASS.

## Review
- review-work of 55232fc: 0 blocking. Should-fix 1, update could lose a docmap value (init wrote
  a default docmap.json over a not-yet-updated config): fixed in 4445ec1. Init writes none while
  config.json holds the keys, and update refuses a key both files hold with different values.
  Should-fix 2, two messages told you to list a board in config.json: fixed in 4445ec1, both
  name docmap.json. Should-fix 3, `jig docmap` didn't name a board page that had no docmap
  entry: fixed in 4445ec1. Optional 4, shape-refusal cases for not_docs and deep_subsystems:
  taken in 4445ec1. Optional 5, stale lines in adopt and fold-in: fixed in 4445ec1. RULES §
  Commands gets a DEFERRED row: part 5 removes that block.
- review-change of 55232fc..4445ec1: 1 blocking (strike 1). `jig docmap <path>` called a
  non-page file in a deep folder a page. Fixed in 898725e: the board and deep tests run only
  on a page, and smoke has the case. Optional, update merging equal values: a smoke case was
  added. Optional, `docmap_conflicts` doesn't check for an object: deferred, with a row.
- review-change of 4445ec1..898725e: 0 blocking. Optional, the `is_page` test's second half
  never changes the result, and its comment says "Only a page" while a reference `.md` passes
  too: deferred, with a row.

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
- [x] docs/commands.md — updated: `jig docmap` added
- [x] docs/hooks.md — no change because it describes the plugin's hooks.json, not the board's files or R5
- [x] docs/jobs.md — updated: the board section names docmap.json, edited like the board on trunk
- [x] docs/metarepos.md — no change because it names no docmap key or config.json
- [x] docs/records.md — updated: the docmap is `.jig/docmap.json`'s
- [x] docs/workflows.md — no change because it names only `roles` in config.json, which stays

## Shared files changed
- `plugin/templates/jig/jig.py`, `plugin/templates/jig/RULES.md`, `plugin/templates/AGENTS.md`: the docmap file and its checks.
- `plugin/skills/{adopt,hardware,redocument,retro,survey,work}/SKILL.md`: they named the keys in config.json.
- `tests/smoke.sh`: the `board` helper writes the four keys to docmap.json, a new `docmap` section, and fixture expectations (stamp 13).
- `docs/commands.md`, `docs/glossary.md`, `docs/jobs.md`, `docs/records.md`: the docmap's new home.
- `.jig/decisions.md` (Unreleased), `.jig/ledgers/DEFERRED.md` (three rows).

## Test by hand
In a repo set up with an older jig, `jig update` lists "move docmap, boards, deep_subsystems and
not_docs … to .jig/docmap.json". `--apply` writes the file. `jig docmap docs/<page>.md` and
`jig docmap src/<file>` answer from it.

## Left
Parts 2 to 5 of the spec: roadmap.json and `jig roadmap show`, retiring `Later:`, one glossary
form, and the rules and templates folders with lowercase names and "the owner". Part 2 is built
and uncommitted in the worktree, its smoke fixtures being converted.
