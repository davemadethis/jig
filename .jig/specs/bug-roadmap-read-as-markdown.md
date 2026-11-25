# bug-roadmap-read-as-markdown: roadmap.json is the form the code reads, and the old parser runs only in the conversion

Source: layout-and-formats part 2, third blocking review (b789b3d) / 2026-11-25 / the job's reviewer, reported by the hubnode. Three blocking findings: "in a metarepo the conversion no longer places phases under their product", "a fenced `(after …)`/`(needed by …)`/`(labels …)` line in a note is counted as used, then filtered out by `roadmap_data`, and never named", and "an indented line before a list's first item joins an earlier list's last item, because `items` spans lists". Also a should-fix: products are judged with owners in different places, and `uncarried` never runs `roadmap_file_problems`. The two reviews before it (aa9e2b8, d1b5e54) blocked on findings of the same kind.

Bug-for: layout-and-formats

## Intent
The roadmap's records are what jig reads and writes. Every reader takes them from
`roadmap.json` directly, and every writer edits them and writes them with `roadmap_dumps`. The
old `roadmap.md` parser and a renderer of that form are left only in the one-time conversion
(and in `tests/roadmap.py`, which writes fixtures through it). Nothing reads JSON back through
Markdown, so a value can't be changed by a rewrite.

The conversion succeeds only when its output carries every old line. It renders the converted
records back in the old form and compares. Each line that doesn't come back under its heading,
and under the line it hung from, is named, and the conversion waits. It judges products with
the same owners the hook and `Family` use, and it runs the hook's own checks on the file it
would write.

## 1. Why
- Q: Why does `jig update --apply` in a metarepo leave `## Widget alpha` with no product? A: `convert_roadmap`'s `roadmap_data` finds `_HEADS["Widget alpha"]`, which `uncarried`'s owner-less `unkept` run had cached, and skips `product_of`.
- Q: Why is there a global heading cache? A: Every reader parses roadmap.json rendered to Markdown (`as_read` → `roadmap_md`), and a heading loses the product/name split. `_HEADS` puts it back.
- Q: Why do readers parse Markdown? A: Part 2 kept roadmap.md's parsers as the representation and put JSON only at the I/O edge. One `roadmap_data` serves exact round-trips and the lenient conversion. Root.

The other two blocking findings come from the same root. The conversion's check is bookkeeping
in parsers that also serve the round-trip (`used`), not a test of its output. So a line the
parser read but a later filter dropped (finding 2), or read into the wrong record (finding 3),
passes.

## 2. Givens (line numbers at b789b3d, `plugin/templates/jig/jig.py`)
- [seen] Finding 1, end to end. A throwaway metarepo with glossary term `Widget` (`Owner:
  this repo`) and an old roadmap `## Widget alpha` / `## Widget No phase`. After `jig update
  --apply`, `roadmap.json` holds `{"name": "Widget alpha"}` with no `product`, and the item
  `{"id": "q", "product": "Widget"}`. In one process, `roadmap_data(md, owners)` gives
  `product: Widget` before `uncarried(md)` runs and `name: Widget alpha` after it
  (`_HEADS == {'Widget alpha': ('', 'Widget alpha')}`). Probe: `bugrm/p.py` and `bugrm/e2e.sh`
  in this session's scratchpad.
- [seen] The mechanism. `roadmap_md` writes `_HEADS[head]` (11473). `roadmap_data` reads
  `_HEADS.get(p["name"])` before `product_of` (11538). `uncarried` calls `roadmap_data(md, {})`,
  and then `unkept`, which calls `roadmap_md` (11925-11926, 11674). `convert_roadmap` then calls
  `roadmap_data(md, owners)` (11935).
- [seen] Finding 2. In `## a`, a note `See:` with a fence holding `(after b)` converts to the
  note `"See:\n```\n```"`, and `uncarried` returns `[]`. `parse_roadmap` adds fenced lines to
  `pre` and `used` (11262-11276). `roadmap_data` keeps only `pre` lines where
  `phase_waits(l) is None and not phase_labels(l)` (11544), so the fenced wait is dropped.
- [seen] Finding 3. Under `## No phase`, `` - `q`: x ``, then `## Widget No phase` with
  `  lead in` before `` - `w`: y ``, converts q's text to `"x\n  lead in"`, and `uncarried` returns
  `[]`. The same happens with `## Up next` / `  up lead` after the No phase items. In
  `parse_section`, the nested-line branch tests `items`, which spans every list (11158-11161).
- [seen] Should-fix. In a stand-alone repo whose glossary has `Widget`, the old `## Widget
  alpha` converts to `products: ["Widget"]`. The stand-alone hook's `roadmap_file_problems(raw,
  {})` then refuses it ("product Widget is no product of docs/glossary.md"), while `uncarried`
  returns `[]`. `convert_roadmap` takes `term_owners` of the glossary in any repo (11934).
  `Family` (12409-12422) and the trunk hook (14101) take owners only in a metarepo (or a
  pararepo's metarepo).
- [seen] The round-trip shows in JSON itself. A scope whose `text` is `build it (after lunch)`
  is refused by `roadmap_file_problems` ("ends in what reads as `after`") through `tail_field`
  (11627, 11646). The refusal exists only because the internal form would read that text back as a
  wait.
- [seen] Every read goes through the internal form. `as_read` renders ROADMAP with
  `roadmap_md_of` (629-632). It is behind `at_rev`, `in_index`, `trunk_show` and
  `Snapshot.show`. `Family.text` is that text. `parse_roadmap` has 19 call sites and
  `parse_no_phase` 18.
- [seen] Every write goes through it. `cmd_merge` (2303-2310), `roadmap_draft` (13050-13054),
  `roadmap_edit` (13312-13357), `cmd_sweep` (17423) and `proposal_commit` (18364-18369) edit
  Markdown text, then call `roadmap_json_of`, which re-parses it with `roadmap_data`. The
  text editors are `retarget_touches`, `items_follow_moves`, `follow_items`,
  `move_items_here`, `only_items_for`, `with_list`, `drop_labels`, `splice_sections`,
  `roadmap_sections`, `section_refusals`, `roadmap_changes`, `proposal_section_refusals` and
  `unknown_labels`, about 290 lines together.
- [seen] Seven of the nine blocking findings across the three reviews sit in this layer.
  - Round-trip: aa9e2b8's "a note or text lost lines on any rewrite, and a text ending
    '(after x)' was read as a wait", d1b5e54's "No phase refused unless grouped by product"
    and b789b3d's `_HEADS`.
  - Conversion sharing the round-trip's parsers: aa9e2b8's drops, d1b5e54's drops and nested
    touches, and b789b3d's fenced waits and pre-item lines.
  - The other two (exit field checks, the chart fixture) are outside the layer.
- [seen] The internal form's patches: `HOLD`/`hold`/`unhold` (11427-11447), `_HEADS`,
  `unkept` (11669-11713), `tail_field`, the `kept`/`pre`/`more`/`used` branches in the parsers,
  `JSON_SAID`/`unline`. Each was added by one of the three fix passes (`git show d1b5e54
  b789b3d`).
- [seen] Smoke writes its roadmap fixtures in the old form and converts them with
  `tests/roadmap.py json` (`rj`, 139 uses). It edits them through `open` (`rmd`, 59 uses),
  which renders JSON to Markdown for `sed`. Two smoke lines assert the `tail_field` refusal
  (tests/smoke.sh:5885, 6146). The second makes the conversion wait on an old item with a
  nested `  - detail (touches docs/a.md)` line.
- [seen] Part 1 of this job reads its JSON directly. `docmap.json` is loaded with `json.loads`
  and merged by `with_docmap` (368, 769), with no text form between.
- [assumed] The record-level writers are shorter than the text-level ones they replace. A
  section becomes the records under one heading key, and a line edit becomes a field edit.
  This is an estimate, not measured: about 300 lines rewritten, about 140 deleted and about 60
  new, close to d1b5e54 and b789b3d together (263 + 160 lines of jig.py). If it can't be
  confirmed before the build, it is the owner's risk (below), not a fact.

## 3. One layer up
- Sibling paths:
  - `docmap.json` in part 1 is read as data and never round-trips, and it has no class like
    this one.
  - The decision log has one reader per format, joined for the same consumers: `with_ideas`
    and `entries_at` (6260-6278). The roadmap gets the same, reused as-is: a JSON reader that
    returns `parse_roadmap`'s and `parse_no_phase`'s shapes for every consumer, and the old
    parser kept for the old format only.
  - `record_plan` (16476) builds one plan of writes from a parsed form and writes each file
    once. The conversion step stays one plan (convert, check, write, or name and wait). Its
    write is `roadmap_dumps` alone.
- Structural difference: the roadmap is the only JSON file whose readers parse a rendering of
  it. That is the whole class.

## 4. Correction
A correction. The data is read as data, so the round-trip class can't recur. The conversion is
judged by its output, so a parser slip is named instead of passing. Patching the three
findings in place (passing products to `roadmap_data`, filtering only unfenced waits, a
per-list `items`) would leave the layer. Each of the last two passes added a patch to it, and
each patch opened the next finding.

## Change
Part A: the records are the representation.
1. A JSON reader, `roadmap_phases(raw)` and `roadmap_list_items(raw)` (names free), returns
   what `parse_roadmap` and `parse_no_phase` return today, built from the records:
   - the phase's heading key is `<product> <name>` (or `<name>`), and a scope's id is `<key>/<id>`;
   - `text`, `after`, `needed_by`, `labels` and `touches` are taken as stored;
   - `line` is 0, and problems name the phase, scope or item, as `unline` already words them.

   Every consumer that reads a roadmap from `ROADMAP` calls it.
2. `as_read` no longer renders. `at_rev`, `in_index`, `trunk_show`, `Snapshot.show` and
   `Family.text` carry the file's JSON.
3. The writers edit records, and every roadmap write is `roadmap_dumps`. These are:
   - `retarget_touches` and `items_follow_moves` (merge);
   - `follow_items`, `move_items_here`, `only_items_for` and `proposal_commit` (move-in);
   - `with_list` (sweep);
   - `drop_labels`, `unknown_labels`, `splice_sections`, `roadmap_sections`,
     `section_refusals`, `roadmap_changes` and `proposal_section_refusals` (draft, edit and the
     proposal hook).

   A section is the records under one heading key: `<product> <name>` for a phase, and
   `<product> No phase` (or `No phase`) for a list's items. So `may_change`, `heading_owner`,
   `heading_product` and `product_of` keep working on the key. `--draft` writes the trunk's
   records. `--edit` compares the draft's records with the base's, by section, as today.
4. Deleted: `HOLD`, `hold`, `unhold`, `_HEADS`, `roadmap_md_of`, `roadmap_json_of`, `unkept`,
   `tail_field` and its refusal, and the parsers' `HOLD`/`kept` branches. A JSON text is prose
   wherever it ends: `build it (after lunch)` is a text, not a wait.

Part B: the conversion is the one place the old parser runs.
1. One owners source. `convert_roadmap` and `uncarried` take products from
   `family(root, trunk).owners`, as-is: the glossary's in a metarepo, none elsewhere. That is
   what the hook (14101) and every reader use, so the conversion places a phase as the old
   roadmap.md was read. This is the should-fix's first half.
2. Every function in the conversion takes its input as arguments and reads and writes no
   module state.
3. The parsers carry what has a home:
   - a phase's note is every line above `Exit when:`/`Scopes:`, fences whole, so a fenced
     `(after …)`, `(needed by …)` or `(labels …)` line stays note text (finding 2). Only an
     unfenced wait line is the phase's wait, as old jig read it.
   - a nested line joins only an item of its own list (finding 3). A line before a list's
     first item, or before an `## Up next` section's first item, has no home and is named.
4. The check is the output, not the parsers' bookkeeping. The `used` sets go. `uncarried`
   renders the converted records in the old form, using `roadmap_md` with its `HOLD` writing
   removed and made conversion-only. It names each non-blank old line that doesn't come back
   with the same key. A line's key is its `## ` heading (with `## Up next` taken as
   `## No phase`) and, for an indented line, the unindented line it follows under that
   heading. Lines compare after exactly these normalizations:
   - trailing space dropped;
   - `[X]` read as `[x]`;
   - `Exit when:`/`Scopes:` in any case;
   - a list line's trailing `(after …)`/`(needed by …)`/`(labels …)`/`(touches …)` in
     `split_waits`' order.

   The first `# ` line and jig's `SEED_COMMENT` are exempt. Any other difference is named.
   The fold-loss count and the parsers' problems stay as they are.
5. `uncarried` also runs the hook's checks on the file the conversion would write:
   `roadmap_file_problems(raw, owners)` and `roadmap_problems`, with the owners of B1, reused
   as-is. A conversion never writes a file the next commit refuses. This is the should-fix's
   second half.
6. `tests/roadmap.py`: `json` converts through the conversion, and fails on anything
   `uncarried` names. `open` renders with the conversion's renderer. `md` and `edit` go, or
   edit records. `rj` and `rmd` keep their names in smoke.

## Done when
- [ ] Metarepo placement: in `sec_roadmap`, a metarepo's glossary has `Widget` controlled by
  this repo, and its old roadmap has `## Widget alpha` (a scope `s`) and `## Widget No phase`
  (an item `q`). `jig update` names nothing. `jig update --apply` writes the phase as
  `{"product": "Widget", "name": "alpha", …}` and q with `"product": "Widget"`. The commit
  passes the hook, and `jig roadmap --product Widget` lists `Widget alpha/s` and
  `Widget No phase/q`, as it did before the conversion.
- [ ] Fenced note waits: an old `## a` whose note holds a fence with `(after b)`,
  `(needed by c)` and `(labels ui)` lines converts with the fence and all three lines in a's
  `note`, byte for byte. a has no `after`, and `jig roadmap` shows its scopes not blocked, as
  the old file read.
- [ ] Pre-item lines: under `## No phase`, `` - `q`: x ``. Under `## Widget No phase`,
  `  lead in` comes before `` - `w`: y ``. `jig update` names `under ## Widget No phase: lead in`,
  `--apply` leaves `roadmap.md` in place, and no record's text holds `lead in`. The same is
  true for `## Up next` with `  up lead` before its first item, after `## No phase` items.
  With the line deleted, the conversion runs, and q's text is `x`.
- [ ] Stand-alone products: a stand-alone repo whose glossary has `Widget` converts
  `## Widget alpha` to a phase named `Widget alpha` with no `product`, and `products: []`. The
  commit passes the hook, and `jig roadmap` names `Widget alpha/s`, as before.
- [ ] The fix fires on the output. A conversion whose records lose a line (in the test, the
  conversion's renderer fed a record with one note line removed) is named by `uncarried`
  with that line's text.
- [ ] The class is closed, conversion side. In `sec_roadmap`, a sweep through
  `tests/roadmap.py` takes `sec_roadmap`'s richest old fixture (two products, notes, boxes,
  scopes, both lists, an `## Up next`). At every line position it inserts each of these:
  - prose and indented prose;
  - `- bullet` and `  - nested`;
  - a three-line fence holding `(after x)`;
  - `(after x)` and `(labels ui)` alone;
  - `# H1` and `<!-- c -->`;
  - `- [ ] box` and `` - `z`: scope ``.

  For every mutant, either `uncarried` names the inserted text, or the converted JSON holds it
  in a record under the heading it was inserted under. For an indented line, that is the
  record of the line it hung under, or the phase's note. The test's own few-line section
  split decides that, not jig's parser. Every mutant that converts passes
  `roadmap_file_problems` with the same owners. The unmutated fixture converts with nothing
  named.
- [ ] The class is closed, data side. A JSON roadmap sets each `text`, `note` and exit `text`
  in turn to each of:
  - `x (after y)`, `x (touches docs/a.md)`, `x (labels ui)`;
  - `a\nb`, `  lead`;
  - `x; stops at y; parked 2026-01-01`;
  - `## h`, `Exit when:`, `` - `z`: w ``, `\u0002`.

  It also has No phase items interleaved by product. Each one commits through the hook,
  survives `jig roadmap --draft` then `--edit` with no change byte-identical, and is listed by
  `jig roadmap` as text, with no waits, labels or touches read from it.
- [ ] `grep -nwE 'HOLD|_HEADS|unkept|roadmap_md_of|roadmap_json_of|tail_field' plugin/templates/jig/jig.py`
  finds nothing. `parse_roadmap(`, `parse_section(` and `parse_no_phase(` are called only from
  the conversion's functions and `tests/roadmap.py`.
- [ ] tests/smoke.sh:5885 and 6146 assert the opposite. A text ending `(after …)` (or the
  others) commits as text. An old item with a nested `  - detail (touches docs/a.md)` line
  converts with that line in its `text` and no `touches`.
- [ ] One query: `jig roadmap --json [filters] [--id <id>…]` prints only the records asked for,
  as JSON: one scope or item by its id (`Widget alpha/s`, `Widget No phase/q`), a phase by its
  key, or what the existing filters (`--product`, `--phase`, `--type`, `--state`, `--owner`,
  `--label`) choose. Each record carries its key and its derived state, and nothing it wasn't
  asked for is printed. An id the roadmap lacks is refused, naming it. The skills that read
  the roadmap ask jig this way, and none says to read `roadmap.json` (smoke: by id, by each
  filter, an unknown id).
- [ ] One load: a command reads the roadmap file of each source (a rev, the index, the work
  tree, a metarepo's trunk) once, and every reader in it shares the records. `tests/roadmap.py
  loads <jig args>` runs jig in-process, counting the parses of each source: `jig roadmap`,
  `jig rig`, `jig roadmap --json --id …` and a trunk commit's hook each parse trunk's roadmap
  once (smoke).
- [ ] Part 2's Done when sections pass on JSON fixtures, and so does `check`:
  `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap roadmap_edit phase_types labels family boundary move movein close sweep rig`
  and `python3 .jig/jig.py queue -- .jig/scripts/check.sh`. The complete smoke is the gate's.

## Decisions
- The owner, 2026-11-25, on which fix: "build the full fix and make sure it can query so it
  doesn't have to read the whole json every time". Part A, the records as the
  representation, with a query that prints only the records asked for and one load of the
  file per command.
- The owner, 2026-11-25, on "text unchanged": "I disagree with that rule in-so-far as a scope
  is probably a less specific definition than a spec, a scope's text should be treated more
  like a staged document when turned into a spec. The parts that come out dont have to stay
  unchanged, the parts that dont get built yet stay in the scope unchanged. That way homeless
  lines don't get pushed into odd places, too." For the conversion this is the reading above:
  no line is pushed into a neighbouring field; each old line comes over where it belongs, or
  is named and waits for the owner. (The scope-to-spec half is layout-and-formats' part 3.)
- Interpreted: the query is `--json` on `jig roadmap`, with `--id` added beside the existing
  filters, so one reader serves the listing, the chart and the query.
- Interpreted: "loaded once" is per source within one command (trunk, the index, the work
  tree, a metarepo's trunk are different files), cached by source, and never a cache across
  commands.

## Out of scope
- `jig roadmap show`'s chart and its fixture: it already draws from records (`render_show`),
  and nothing here changes what it reads.
- Part 4's glossary form. The conversion takes `Family.owners` as-is, so when part 4 changes
  what `Family` reads as a product, the conversion follows with no change here.
- The optional finding (other readers of the internal form use `splitlines()`): fixed by
  Part A, since no reader of the internal form remains.

## Touches
- `plugin/templates/jig/jig.py`:
  - the roadmap block 10925-11945 (parsers, records, `roadmap_md`, `roadmap_data`,
    `roadmap_shape`, `roadmap_file_problems`, `uncarried` and `convert_roadmap`);
  - `as_read` 629;
  - the readers named in Givens, and `Family` 12395;
  - the writers listed in Change A3;
  - `cmd_merge` 2296-2312, `roadmap_draft` and `roadmap_edit` 13040-13375, `roadmap_rules`
    14028-14134, `cmd_sweep` 17361, `proposal_commit` 18344, and update's STEPS 14676-14690.
- `tests/roadmap.py`.
- `tests/smoke.sh`: `sec_roadmap` (the conversion and sweep observables), and the sections
  whose fixtures use `rmd` with `sed`, kept working through `open`.
- `plugin/templates/jig/RULES.md`, Roadmap: one sentence. A text in `roadmap.json` is prose
  wherever it ends, and the conversion waits on each line it can't carry.

## Alternatives considered
- Keep the internal form and close the three findings in it: pass products into
  `roadmap_data` instead of `_HEADS`, Part B's output check, and Family's owners. Rejected
  because the round-trip class stays open: `HOLD`, `unkept`, and `tail_field` refusing prose
  in JSON. Three of the nine blocking findings were round-trip ones, and every new reader or
  writer of the internal form re-enters the class (the optional `splitlines()` finding). This
  reason is [seen]. It is the smaller change, and is the owner's alternative below.
- The invariant alone, with no Part A: conversion succeeds only if rendering its JSON
  reproduces every old line. Rejected as the whole fix because a line compare can't see
  placement: `## Widget alpha` renders the same with or without `product: Widget`, so
  finding 1 passes it. This reason is [seen] (the e2e output renders to the same heading).
  B2 (no module state) and B1 (one owners source) close placement, and the compare closes
  loss.
- Line accounting in the parsers (b789b3d's `used`), made exact. Rejected because it checks
  what the parser touched, not what the output holds. Findings 2 and 3 are lines counted as
  used and then dropped or misplaced. This reason is [seen].
- Revert to `roadmap.md` with query commands. Rejected by the owner ("I dont need to read
  it"). This reason is [seen] (layout-and-formats, Alternatives).
- Drop the conversion's "text unchanged" and convert fields only, with a report of dropped
  prose. Rejected because the owner's Done when asks for text unchanged. Naming a line and
  waiting already keeps it unchanged, so the decision stands as written. This reason is [seen].

## For the owner
- The spec's decisions and this churn:
  - "JSON in place of Markdown" and "--draft/--edit editing JSON" did not cause it. The build
    did, by keeping Markdown as what the code reads. The parent spec left that open: its
    Touches lists part 2 under the Markdown parsers and never says what the code reads. This
    spec says it.
  - "With its text unchanged" contributed. Read as "every old line goes into some field", it
    pushed lines with no home (a list's lead-in, prose above the first heading, extra H1s)
    into notes and neighbouring items. Finding 3 is one of them. This spec reads it as
    "unchanged, or named and waiting for the owner", which the update step already words.
- One call: Part A, the records as the representation, which is this spec, or the
  alternative of keeping the internal form with Part B only. Part A is larger, roughly the
  size of the last two fix passes together (an [assumed] estimate). It closes both halves of
  the class. The alternative is smaller and closes the conversion half. The round-trip half
  stays, and so does the refusal of a JSON text ending `(after …)`.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
