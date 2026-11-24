# Handoff: phase-types

Commit: a23c7511eda3bd5cf8a7b9f08d3331b34f70ea7f
Date: 2026-11-23
Spec: .jig/specs/phase-types.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part A of phase-types: phase types. `phase_type` reads Prototype (a Greek letter), Pilot (`Pilot <letter>`) or Production (any other name) from a phase's name after its product term, case folded. `type_problems` refuses, by line, a phase whose type comes before one above it in the same product (the repo's own phases are one product): in the trunk hook (roadmap_rules, trunk and proposal paths), in `jig roadmap` (exit 1), and as a warning in `jig update`'s dry run, to fix in the same update (the owner's "Option 1": the whole roadmap). `jig roadmap` prints `alpha  Prototype, current`; the view's phase line and headings carry the type (`## alpha (Prototype, current)`). Part B (filters) follows.

## Done-when evidence
- (types) smoke phase_types: `jig roadmap` prints `alpha  Prototype, current`, `Pilot A  Pilot, next`, `Launch  Production, next`; `--write` puts `## alpha (Prototype, current)` in ROADMAP.md: PASS
- (case) smoke phase_types: `Beta  Prototype, next` and `pilot b  Pilot, next`: PASS
- (order) smoke phase_types: commit adding `## gamma` after Pilot A/Launch refused with `line N: phase gamma (Prototype) comes after Launch (Production)`; `jig roadmap` reports it and exits 1: PASS
- (per product) smoke phase_types in meta: `Familiar App beta` refused, `Walyt alpha` never named; `Walyt Launch` then `Familiar App alpha` commits; meta's own `Demos` then `alpha` refused: PASS
- (update, owner's ruling) smoke phase_types: update's dry run lists gamma by line and type under Warnings: and exits 1: PASS
- (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap family phase_types rig rig_batch sweep update moves boundary pararepo metarepo` at 15a0ebc: 620 PASS, 0 FAIL; `… smoke.sh phase_types roadmap family update` at a23c751: all PASS but my own case's grep, fixed and rerun: 9/9 phase types PASS; `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0; `claude plugin validate ./plugin`: Validation passed
- (docs) `grep -n -E 'Prototype' docs/records.md docs/commands.md docs/glossary.md` finds each; `--product` comes with Part B

## Review
review-work of 15a0ebc: 0 blocking. Should-fix 1 (existing out-of-order roadmaps refused on update) went to the owner: "Option 1", whole roadmap, applied as update's dry-run warning (a23c751). Should-fix 2 (per-product test couldn't tell per-product from global order): two cases added (c973540). Optional 2 (vacuous `No phase  current` check): fixed (c973540). Optional 1 and 3: DEFERRED.md.
review-change of a23c751: 0 blocking. Its four optional findings: DEFERRED.md; its 3 is taken in Part B's evidence command.

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
- [x] docs/commands.md — updated: roadmap prints each phase's type   (1 file)
- [x] docs/hooks.md — no change because it names no roadmap rule; RULES.md § Roadmap holds the type-order refusal   (1 file)
- [x] docs/jobs.md — no change because it mentions the roadmap only for R5, which is unchanged   (2 files)
- [x] docs/metarepos.md — no change because moving phases in is unchanged; types are per product, described in records.md and RULES.md   (2 files)
- [x] docs/records.md — updated: § Roadmap says how types are read and ordered   (2 files)
- [x] docs/workflows.md — no change because rig's next step is unchanged   (2 files)

## Shared files changed
- plugin/templates/jig/jig.py: phase_type, type_problems, _roadmap_full (type), render_roadmap, cmd_roadmap, roadmap_rules, cmd_update (the warning).
- plugin/templates/jig/RULES.md: § Roadmap, a Types bullet.
- tests/smoke.sh: a new section phase_types (own function, in UNITS after family); old-format assertions on phase states updated in roadmap, family and rig cases; rphase reads the state's new column.
- docs/records.md, docs/commands.md, docs/glossary.md: types.

## Test by hand
In a repo with a roadmap, run `python3 .jig/jig.py roadmap` and see each phase's type; `--write` and open ROADMAP.md to see `(Prototype, current)` in the headings.

## Left
Part B: `jig roadmap` filters (--product, --phase, --type, --state, --owner) and `--view`, then its docs (`--product` in records, commands, glossary).
