# Handoff: phase-types

Commit: dcea63d8031b4c2afb44b8b72b2c7acba96e5174
Date: 2026-11-23
Spec: .jig/specs/phase-types.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
The whole of phase-types. Part A (handed off partial in phase-types-2026-11-23.md): a phase's type, Prototype, Pilot or Production, is read from its name; types run in that order within a product, refused by line on trunk, reported by `jig roadmap`, and listed by `jig update`'s dry run (the owner's "Option 1", whole roadmap). Part B: `jig roadmap` takes `--product`, `--phase`, `--type`, `--state` and `--owner` (repeatable, case folded, or'd within a flag and and'ed across), from one table, `ROADMAP_FILTERS`, and one predicate, `roadmap_filter`, which refuses a row it has no test for. Unknown product, phase, type or owner values are refused, naming the known ones; `--owner` takes any name jig knows this repo by and compares repos through their aliases; filters that match nothing say so. Problems and the exit code never change. `jig roadmap --view [filters]` prints that part as Markdown, saying it is a part; `--write` refuses a filter, so ROADMAP.md stays whole.

## Done-when evidence
All in smoke section phase_types (throwaway repos, JIG_CONFIG and XDG_CONFIG_HOME set per section):
- (types) `jig roadmap` prints `alpha  Prototype, current`, `Pilot A  Pilot, next`, `Launch  Production, next`; `--write` puts `## alpha (Prototype, current)` in ROADMAP.md: PASS
- (case) `Beta  Prototype, next`, `pilot b  Pilot, next`: PASS
- (order) a trunk commit adding gamma after Pilot A refused by line; `jig roadmap` reports it and exits 1; update's dry run lists it and exits 1: PASS
- (per product) `Familiar App beta` refused, never `Walyt alpha`; Walyt Launch then Familiar App alpha commits; meta's Demos then alpha refused: PASS
- (product and phase) `--product Walyt --phase alpha` prints Walyt alpha and its scopes only; `--phase alpha` both alphas: PASS
- (type, state) `--type pilot` only Familiar App Pilot A; `--state open` drops taken and done scopes and empty phases; `--state blocked` only open scopes with an unmet after: PASS
- (owner) `--owner pb` only Familiar App's phases and its No phase list; aliases resolve in meta and in pa: PASS
- (problems kept) a dead touch under Familiar App still prints with `--product Walyt`, exit 1: PASS
- (typo) `--product Walty` refused naming Familiar App, Walyt; unknown type, owner and phase refused too: PASS
- (view) `--view --product Walyt` prints Walyt's phases only, ROADMAP.md unchanged; `--write --product Walyt` refused with "--write takes no filter": PASS
- (stand-alone) `--type prototype` prints alpha only: PASS
- (no regression) at dcea63d: `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap family phase_types page_contract rig rig_batch sweep update moves boundary pararepo metarepo`: 669 PASS, 0 FAIL; `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0; `claude plugin validate ./plugin`: Validation passed
- (docs) `grep -n -E 'Prototype|--product' docs/records.md docs/commands.md docs/glossary.md` finds each

## Review
Part A: see phase-types-2026-11-23.md.
review-change of 1a2e9b2 (Part B): 0 blocking. Should-fixes 1 (untested filter row ignored), 2 (--owner names for this repo), 3 (spec's regression line) fixed in 9686ed6; optionals 1 (unknown phase, nothing-matches note), 3 (filtered view header), 4 (smoke gaps) fixed; optional 2 (--view skips the stale note) in DEFERRED.md.
review-change of 9686ed6: 0 blocking. S1 (Owner: aliases), O2 (pararepo view note), O3 (spec Touches) fixed in dcea63d.
review-change of dcea63d: 0 blocking. Its should-fix (pararepo unfiltered --view header predates this job) and optional (an owner of no product refused in meta, "nothing matches" in pa) in DEFERRED.md.

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
- [x] docs/commands.md — updated: roadmap's type column, filters, --view, --write takes no filter   (1 file)
- [x] docs/hooks.md — no change because it names no roadmap rule; RULES.md § Roadmap holds the type-order refusal   (1 file)
- [x] docs/jobs.md — no change because it mentions the roadmap only for R5, which is unchanged   (2 files)
- [x] docs/metarepos.md — no change because moving phases in is unchanged; types and filters are described in records.md and RULES.md   (2 files)
- [x] docs/records.md — updated: § Roadmap says how types are read and ordered, and how to show part of the roadmap   (2 files)
- [x] docs/workflows.md — no change because rig's next step is unchanged   (2 files)

## Shared files changed
- plugin/templates/jig/jig.py: phase_type, type_problems, ROADMAP_FILTERS, roadmap_filters, roadmap_filter, _roadmap_full (type), render_roadmap (type, filtered header), cmd_roadmap and its parser, roadmap_rules, cmd_update (the type warning). `--label` (roadmap-labels) is one row in ROADMAP_FILTERS plus its test in roadmap_filter.
- plugin/templates/jig/RULES.md: § Roadmap, Types and Filters bullets.
- tests/smoke.sh: new section phase_types (in UNITS after family); old-format phase-state assertions updated in roadmap, family and rig cases.
- docs/records.md, docs/commands.md, docs/glossary.md: types and filters.

## Test by hand
In a metarepo with products, run `python3 .jig/jig.py roadmap --product <Product> --phase alpha` and see only that phase; add `--view` to see it as Markdown that says it is a part.

## Left
Nothing. `--label` is roadmap-labels': whichever lands second adds its row and test.
