# Handoff: layout-and-formats

Commit: 5862d506579d21d70771a0e5c87a8843a2c790e9
Date: 2026-11-25
Spec: .jig/specs/layout-and-formats.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part 2 of 5, with the bug spec `bug-roadmap-read-as-markdown` (Bug-for: layout-and-formats) built
into it. The roadmap is `.jig/roadmap.json`: `products`, `phases` and `no_phase` records. jig
reads and writes the records themselves, through `roadmap_phases`/`roadmap_list_items` (the old
parsers' shapes, built from the records) and record-level writers. Each roadmap file is parsed once
per command (`roadmap_records`). `jig roadmap show [filters] [--width N]` draws a dateless chart,
and `jig roadmap --json [filters] [--id <id>…]` prints only the records asked for. ROADMAP.md,
`--view` and `--write` are gone. `jig update --apply` converts an old roadmap.md once trunk's checker
reads JSON. The conversion is judged by its output: the records are drawn in the old form again,
and each line that doesn't come back is named, as is anything the hook would refuse. The
conversion waits on those. The old parser runs only in the conversion. `roadmap_home` is the one
answer to where a pararepo plans from (its roadmap.json, its unconverted roadmap.md, or its
metarepo's), and every site that decides it asks it. The hook guards the old roadmap.md, as the
owner approved on 2026-11-25. The AGENTS.md template carries the `roadmap:` command, and update adds it.

## Done-when evidence
Part 2's items and the bug spec's. Parts 3 to 5 are still to do.
- Full smoke at 5862d50, `python3 .jig/jig.py queue -- bash tests/smoke.sh`: rc 0, 2407 PASS,
  0 FAIL. check (`.jig/scripts/check.sh`): rc 0.
- init writes roadmap.json and no ROADMAP.md: `smoke roadmap` and `init`.
- Records, the hook's shape refusals (fields, types, an exit check's fields, a key written twice,
  a phase with neither exit nor scopes, products the glossary or `products` lacks): `smoke roadmap`
  "the hook refuses …" cases.
- A product the roadmap doesn't include gets nothing: `smoke roadmap_edit`, the "Teleport" case.
- Readers on converted fixtures: `smoke roadmap roadmap_edit phase_types labels family boundary
  move movein close sweep rig` all pass in the full run. Every fixture is converted by jig's own
  conversion (tests/roadmap.py).
- --draft/--edit with section ownership, propose/ branches and BUFFER rows: `smoke roadmap_edit`.
- show against an expected-output fixture: `tests/fixtures/roadmap-show/` (a metarepo with two
  products) matches byte for byte at the default width (banded) and at `--width 200`.
- --view/--write gone, and no ROADMAP_VIEW: `grep -n ROADMAP_VIEW plugin/templates/jig/jig.py` finds
  nothing.
- Conversion: `smoke roadmap` "no phase: jig update --apply converts …" and the hand-written shapes.
  The conversion-side sweep (`tests/roadmap.py sweep`): every line inserted anywhere in a rich old
  roadmap is either named or held as a whole line. With the output compare disabled, 90 mutants
  fail it.
- The bug spec: metarepo placement, fenced note waits, pre-item lines, stand-alone products, the
  check firing on output (`tests/roadmap.py lossy`), data-side values surviving draft/edit byte for
  byte, `--json`/`--id`, one load (`tests/roadmap.py loads`: 1 for roadmap, rig, --id and the
  hook). The whole-word grep for the internal form's names finds nothing. All are `smoke roadmap`
  "bug: …" cases.
- roadmap_home and the old file's guard: the `smoke move` PP cases (item plan, sweep, jig roadmap,
  move-in, removals, mid-conversion), and in `smoke roadmap` splace the branch removal and the
  conversion dropping a taken phase.
- The AGENTS.md roadmap: line: `smoke update_roles` F and `smoke update`.
- Rules, skills and docs describe the JSON roadmap: `grep -rn 'roadmap.md\|ROADMAP.md' plugin docs`
  finds only update's conversion, its rule, and the old-form names the conversion reads.

## Review
- review-work of aa9e2b8: 4 blocking (strike 1). (1) Conversion dropped text silently. (2) Notes
  and texts lost lines or gained data on any rewrite. (3) Exit checks weren't field-checked. (4) No
  chart fixture. Should-fix: duplicate JSON keys, the neither-exit-nor-scopes refusal, product
  refusal smoke, two docs lines. Optional: move-in's old buffer rows, the update skill's line,
  messages in JSON words. All taken in d1b5e54.
- review-change of aa9e2b8..d1b5e54: 2 blocking (strike 2). B1: No phase refused unless grouped
  by product. B2: conversion lines not accounted for. Should-fix: exit `[]`, the update skill on
  waiting lines, a second product in the chart fixture. Optional: refuse all four Markdown-style
  tails, other line breaks, an item with empty text. All taken in b789b3d.
- review-change of d1b5e54..b789b3d: 3 blocking (strike 3). Products lost through the heading
  cache, fenced note waits filtered out, nested lines joining another list's item. Should-fix:
  owners judged in different places. The bug role ran: `.jig/specs/bug-roadmap-read-as-markdown.md`
  (d986dad, ab4011b). The owner chose the full fix on 2026-11-25 (records as the representation,
  plus a query and one load), amended in ce1670f. Built in 7ddc804.
- review-change of b789b3d..7ddc804: 1 blocking (strike 4). A pararepo converting its own
  roadmap took M's products. Should-fix: a weak sweep oracle, and `products` refusing a move's new
  receiver product. Optional: the spec's grep -w, the stage skill line, the data-side check. All in
  f360654.
- review-change of 7ddc804..f360654: 1 blocking (strike 5). Family read an unconverted pararepo as
  planning from M. Optional: the products refusal's wording. 27cb98e.
- review-change of f360654..27cb98e: 2 blocking (strike 6). The plans-from question was decided
  in several places, so I wrote one predicate (`roadmap_home`) and routed six sites through it. The
  sweep wrote beside an unconverted roadmap.md. Should-fix: jig roadmap and move-in in an
  unconverted pararepo. c7221bd.
- review-change of 27cb98e..c7221bd: 1 blocking (strike 7). Removing the old roadmap.md was
  unguarded. The owner approved the rule on 2026-11-25 ("Works for me"). Should-fix: the sweep dry
  run. Optional: roadmap_withheld reads trunk. 780964c.
- review-change of c7221bd..780964c: 0 blocking. Should-fix S1 (a conversion's dropped scopes), S2
  (R5 for roadmap.md), S3 (empty means nothing named). Optional O4, O5. All taken in 5862d50.
- review-change of 780964c..5862d50 (with the spec-only 7ed87f2): 0 blocking. Optional: once M holds
  this repo's products, removing an old roadmap.md holding only prose passes, and the prose is lost.
  Deferred, with a row. Two findings for part 5, about the designer list and the `rigger` key's
  scan and write, go to part 5's first commit.

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
- [x] docs/commands.md — updated: `jig roadmap show`, `--json`/`--id`, `--draft`/`--edit` editing JSON
- [x] docs/hooks.md — no change because it describes the plugin's hooks.json, not the roadmap's checks
- [x] docs/jobs.md — no change because its R5 line names the roadmap, not its file or form
- [x] docs/metarepos.md — no change because move-in and --draft/--edit read as they work now; it names no file form
- [x] docs/records.md — updated: the roadmap is a JSON file in jig's folder, drafted and checked by --draft/--edit
- [x] docs/workflows.md — no change because it names the roadmap's next step only
- [x] UNOWNED tests/roadmap.py — no page needed because it is smoke's own tooling (the repository's own tooling, its build, CI, release and dev scripts, needs none)

## Shared files changed
- `plugin/templates/jig/jig.py`, `plugin/templates/jig/RULES.md`, `plugin/templates/jig/docs-page.md`,
  `plugin/templates/AGENTS.md`: the JSON roadmap, its readers, writers, hook, query, chart and
  conversion.
- `plugin/skills/{init,update,hubnode,spec,review,redocument,retro,stage,survey,rig}/SKILL.md`: they
  described roadmap.md, ROADMAP.md or reading the file.
- `tests/smoke.sh`, `tests/roadmap.py` (new), `tests/fixtures/roadmap-show/` (new),
  `tests/fixtures/README.md`: fixtures through the conversion, the chart fixture, the bug cases.
- `README.md`, `docs/commands.md`, `docs/glossary.md`, `docs/records.md`, `.jig/decisions.md`
  (Unreleased), `.jig/specs/bug-roadmap-read-as-markdown.md`, `.jig/specs/layout-and-formats.md`
  (the owner's 2026-11-25 answers, part 3's split, part 5's designer).

## Test by hand
In a repo set up with an older jig that has a `.jig/roadmap.md`: run `jig update --apply`, commit,
then run it again. The second run converts it, or names each line it can't carry and waits. Then
`jig roadmap show` draws the chart, and `jig roadmap --id <phase>/<scope>` prints one record.

## Left
Parts 3 to 5: retiring `Later:` (rule 1 as the owner amended it: a partly built scope is split by
a roadmap change), one glossary form, and the rules and templates folders with lowercase names,
"the owner" and the designer. Part 5's first commit also corrects the designer list (only hubnode,
relay, stage and rigger name it) and adds the `rigger` key's scan and write to its Breaking list.
