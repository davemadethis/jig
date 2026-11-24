# bug-id-pointers: a cached pointer that cites an entry or an idea by id never resolves

Source: moving-in-command review / 2026-11-24 / reviewer, confirmed by the job's work session in a throwaway family (DEFERRED.md row "pointer_gap never resolves an id pointer"): "`pointer_gap` never resolves a pointer that cites a decision-log entry or an idea by id", so `jig sync` lists every cached metarepo pointer to a live pararepo entry as stale, and the reviewer suspects P2 never fires for one.

## Intent
A metarepo pointer `L/.jig/decisions.md § D-001` or `L/.jig/ideas.md § D-002` names an entry
by its id. RULES already reads a move's target that way: the id is looked up in either file
(Decision log, Released sections). The pointer checks (`jig sync`, the pararepo's release,
`jig update`'s Metarepo pointers block and P2) read it the same way. An id that is live in
either file resolves. One that neither file has is reported, and P2 asks a change that removes
it.

## 1. Why
- Q: Why does sync report a live D-001? A: `dangling` asks `pointer_gap`, which matches a section only against headings, whole (a code span) or as a heading the text begins with (prose).
- Q: Why doesn't `### D-001 three` match `D-001`? A: The heading is longer than the id. A code span must equal a heading, and prose matches only when the heading begins the text, not the other way round.
- Q: Why was the id never handled? A: `pointer_gap` (f2ca8db, 11-03) predates the log (fbd990c, 11-10). The log taught `meta_citations` and the move code ids. It never taught `pointer_gap`. Root.

## 2. Givens (line numbers at trunk 8d1d603, `plugin/templates/jig/jig.py`)
- [seen] Reproduced in a throwaway family (`bug-id-pointers-repro.sh` in the group's notes
  folder, `JIG_CONFIG`/`XDG_CONFIG_HOME` set). L has D-001 accepted under `## Unreleased` and
  D-002 open in `.jig/ideas.md`. M (prefix E-) releases v0.1.0 with E-001: "Per
  `` `L/.jig/decisions.md § D-001` `` and `` `L/.jig/ideas.md § D-002` ``, and
  `` `L/.jig/decisions.md § D-009` ``". L is pinned at v0.1.0. `jig sync` in L prints all three,
  `… § D-001, which .jig/decisions.md has no heading for`, the same for `.jig/ideas.md § D-002`,
  and D-009. Only D-009 is really missing.
- [seen] `pointer_gap('.jig/decisions.md', 'D-001', True, '### D-001 three\n')` returns
  `(1, '… has no heading for')`. With the section `D-001 three` it returns `(0, '')`.
- [seen] P2 never fires for an id (`bug-id-pointers-p2.sh` beside the repro). On a branch in L,
  a commit that drops idea D-002 from `.jig/ideas.md` passes (rc 0). So does a commit that removes
  D-001 from the log. Both are cited by M's cached E-001. P2 (jig.py:8656-8660) compares
  `pointer_gap` now with `pointer_gap` at base, and both are NO_HEADING.
- [seen] The readers of `pointer_gap`:
  - `dangling` (9775-9787). It is behind `stale_pointers`, which is `jig sync` and the
    pararepo's release, and behind `pointer_cleanup` and `contract_removals`, which are
    `jig update`.
  - `removal` (9808-9821), through `pointer_cleanup`. It walks history for the commit where
    the pointer started to miss, so for an id it never finds one.
  - P2 (8656-8660).
  - `meta_citations` (9592). It reaches `pointer_gap` only for a non-id section: its own id
    branch (9583-9597) comes first.
  - `move_rules` (6713, 6734). It uses `pointer_gap` only for a non-id section and looks ids up
    with `entry_keys(entries_at(…))` (6731).
  - `moved_from_rules` (6814), for a moved-from line naming `.jig/ideas.md § <id>`. Out of scope.
- [seen] The other direction already works: `meta_citations` looks an id in `LOG` or `IDEAS` up
  in `with_ideas(log, ideas)` (9579-9581): "One id names an entry or an idea: one decided or
  folded keeps it, in the other file". `move_rules` does the same with
  `entry_keys(entries_at(t, loc))`, and `entry_keys` compares by `move_key` (D-2 is D-002).
  `moved_to` (6597) reads a log or ideas section as an id. That is why a moved id already
  reads `(moved: …)` in `dangling`.
- [seen] `entries_at(rev)` joins the log and the ideas file at REV. `""` is the index, as
  `body_at` reads it. `read_entries_text(root)` is the working tree's.
- [seen] The `sec_pointers` smoke section (tests/smoke.sh:3776) holds the pararepo-side pointer
  observables (sync lines, P2 refusals). No smoke asserts an id pointer's `dangling` text.

## 3. One layer up
- Sibling paths: `meta_citations` (the pararepo citing the metarepo) and `move_rules` (a move's
  target) both read an id in `.jig/decisions.md` or `.jig/ideas.md` as an entry, found in
  either file. `dangling`, `removal` and P2 are the pararepo reading the metarepo's pointers to
  it. They share `pointer_gap`, which knows only headings. That is the one structural
  difference.
- The pattern to reuse: `with_ideas`/`entries_at` for the text, and `entry_keys` + `move_key` for
  the lookup. Nothing new is recorded. There is no new reader, only `pointer_gap` taught what
  its siblings already know.

## 4. Correction
A correction, in `pointer_gap` and the text its three callers hand it. Every reader gets it at
once: sync, release, update's block and P2. Filtering the symptom in `dangling` would leave P2
and `removal` blind.

## Change
1. **`pointer_gap`**: for a path in (`LOG`, `IDEAS`), a section that is an entry id names that
   entry. In a code span the id is the whole span. In prose it is the leading id token. This is
   the shape `meta_citations` uses at 9583-9584. The pointer resolves when
   `move_key(id) in entry_keys(body)`. Otherwise the gap reads `<path> § <id>, which
   .jig/decisions.md and .jig/ideas.md have no entry for`. A section that isn't an id, like
   `D-001 three`, keeps the heading rule.
2. **The text it reads**: for a path in (`LOG`, `IDEAS`) whose file exists, `dangling`, `removal`
   and P2 hand `pointer_gap` both files joined, as `with_ideas` joins them. That is
   `entries_at(rev)` at a revision and the index's or working tree's pair in P2's
   `body_now`. A missing cited file stays NO_FILE. Put it once in `body_at`/`body_now`, whose
   other readers (7561, 7624) never ask for `LOG` or `IDEAS`, or in one small helper the three
   callers share. The builder's choice.
3. **Words**: RULES.md (Metarepo and pararepos), at the paragraph on how a pointer is checked
   (around line 1658). Add: a section that is an entry id in `.jig/decisions.md` or
   `.jig/ideas.md` names that entry, found in either file, as a move's target is. In the P2 row
   (around line 1783): "or the heading its `§` names" becomes "or the heading or entry its `§`
   names". Add one line under `### Fixed` in `.jig/decisions.md` `## Unreleased`.

## Done when
- [ ] Log form: in `sec_pointers`, M's released entry cites `` `pp/.jig/decisions.md § D-001` ``,
  with D-001 accepted in the pararepo's log. `jig sync` prints no line naming `§ D-001`.
- [ ] Ideas form: the same entry cites `` `pp/.jig/ideas.md § D-002` ``, with D-002 open in the
  pararepo's ideas file. `jig sync` prints no line naming `§ D-002`. After D-002 is decided
  (its block in the log, gone from the ideas file), sync still prints none: either file holds it.
- [ ] The fix fires: a cited `§ D-009` that neither file has prints `points to
  .jig/decisions.md § D-009, which .jig/decisions.md and .jig/ideas.md have no entry for`.
- [ ] P2: on a branch, a commit removing D-001 from the log is refused, and the refusal names
  `§ D-001`. A commit dropping idea D-002 from the ideas file is refused, naming `§ D-002`. With
  `meta: none — <reason>` in a spec it touches, the drop passes.
- [ ] Moved still reads moved: the `movein` smoke section's `(moved: …)` observables pass
  unchanged.
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh pointers movein moves sync_buffer` and
  `python3 .jig/jig.py queue -- .jig/scripts/check.sh` pass. The complete smoke is the gate's.

## Out of scope
- `moved_from_rules` (6814, `source()` at 6770): a moved-from line naming
  `<repo>/.jig/ideas.md § <id>` is keyed by `path § id`, where `moves_in` keys an id alone.
  Change 1 makes its `pending` check see an idea there, but `points_here` would still miss.
  Not reported and not reproduced. `jig move` writes the log form. If it matters, it is its
  own bug.
- `meta_citations`' own id branch (register rows, the successor via `holds_now`) stays as it is.
  It already works.
- A pointer into an old `DECISIONS.md` register by row id. The log replaced registers
  (`jig update --merge-log`).

## Touches
- `plugin/templates/jig/jig.py` (`pointer_gap`, `body_at`/`body_now` or one helper, `dangling`,
  `removal`, P2's pointer lines)
- `plugin/templates/jig/RULES.md` (Metarepo and pararepos; the P2 row)
- `tests/smoke.sh` (`sec_pointers`)
- `.jig/decisions.md` (one `### Fixed` line)

## Alternatives considered
- Skip id pointers in `dangling` (a workaround at the symptom). Rejected because P2 and `removal`
  would stay blind, and a removed entry M still cites would pass with no report. This reason is
  [seen]: P2 passed both removals in the repro.
- Route `dangling`/P2 through `meta_citations`' id branch (its row regex on `### <id>`).
  Rejected because that branch is written for the other direction. It reports "has no row" with
  a pin and a successor, and its regex compares ids as text, while `entry_keys` compares by
  number (D-2 is D-002), as `move_rules` does. This reason is [seen].
- Make an id resolve only in the cited file. Rejected because RULES reads a move's target id
  "in either file there", and a decided idea moves to the log under the same id. An ideas-file
  pointer would dangle the moment the idea is decided. This reason is [seen] (RULES.md:1362,
  meta_citations 9579-9581).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
