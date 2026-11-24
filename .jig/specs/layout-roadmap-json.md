# layout-roadmap-json: the roadmap as JSON, a products list, and a chart in place of ROADMAP.md

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

Part 2 of 5. It is built after layout-docmap and before layout-later-ledger, layout-glossary-form
and layout-rules-templates-names. layout-glossary-form reads the products list this part adds.

## Intent
The roadmap moves from `.jig/roadmap.md` to `.jig/roadmap.json`, records that are queried, not
read. A products list names each product, the repo that builds it, and whether it is that repo's
software product or hardware the software runs on. The roadmap names which of those products it
includes. `jig roadmap show` prints the roadmap as a chart ordered by its waits, and jig no longer
writes `ROADMAP.md`. `jig update` converts each existing roadmap.

The owner's words:
- 2026-11-22: "I would also make roadmap a .json because I dont need to read it."
- 2026-11-22: "I think structured data is right here because scopes live in or out of stages and phases and relate to products and features and have labels."
- 2026-11-24: "Each repo is one software product, which may run on one or more hardware products. That should be the updated rule."
- 2026-11-22: "Perhaps each roadmap names the products included, that way excluded products done get asked about."
- 2026-11-21: "we dont need the generated view of roadmap, I'd cut it."
- 2026-11-23: "not a true gantt, just dependency-based ordering and each entry's width can be standard where parent widths are set to fit the standard children. There should be a command to render this in-chat, maybe jig roadmap show so it'll trigger if I say something like "show me the roadmap""

## Done when
- [ ] `jig init` writes `.jig/roadmap.json` (`products: []`, `phases: []`, `no_phase: []`) and
      `.jig/products.json`. It writes no `ROADMAP.md`, and no `.jig/roadmap.md` (smoke).
- [ ] The records hold:
      - a phase: `product` (only where the roadmap includes more than one product), `name`, `note`, `exit` (a list of `{text, done}`), `after`, `needed_by` and `scopes`;
      - a scope: `id`, `text`, `labels`, `touches`, `after` and `needed_by`;
      - a `no_phase` item: what a scope holds, plus an optional `product`, `stopped_at` and `parked` (`YYYY-MM-DD`);
      - a products entry: `name`, `repo` (or `null` for a product no repo builds yet) and `kind` (`software` or `hardware`).

      Nothing else is written. State and blocked stay derived, and a phase's type is still read from its name.
- [ ] A commit refuses a roadmap or products file with an unknown field or a field of the wrong type. It also refuses:
      - a phase, scope or item naming a product the roadmap doesn't include;
      - a product the roadmap includes that the products list doesn't have;
      - a repo with more than one `software` product.

      Every check `roadmap_problems` runs today still runs: refs, rings, repeated waits, phase-type order, labels against the glossary, the unconfirmed cross-product `after` (smoke).
- [ ] A product on the products list that the roadmap doesn't include gets no phase, scope or item. Rig, update and staging never ask about it (smoke).
- [ ] `jig roadmap`, its filters (`--product`, `--phase`, `--type`, `--state`, `--owner`, `--label`), `Scope:` id checks, the drop guard, rig and the gate give the same answers on a converted fixture as on its `roadmap.md` before conversion. The existing `sec_roadmap`, `sec_roadmap_edit`, `sec_phase_types`, `sec_labels`, `sec_family`, `sec_boundary`, `sec_move`, `sec_movein`, `sec_close`, `sec_sweep` and `sec_rig` pass on JSON fixtures.
- [ ] `jig roadmap --draft` writes the roadmap as a JSON draft. `--edit` checks and writes it, with section ownership, `propose/` branches and BUFFER rows working as they do today (smoke).
- [ ] `jig roadmap show [filters]` prints a text chart. It carries no dates. A scope's column is one past the furthest column of anything it waits on, and every entry is the same width. A phase box, and a product box where there is more than one product, is as wide as its children. Each box shows the scope's id and state. Within a column, scopes sharing a first label sit together. A chart wider than 100 columns (or `--width`) prints one band per phase (smoke, against an expected-output fixture).
- [ ] `--view` and `--write` are gone. No path writes `ROADMAP.md`: merge, `close_merged`, `rig_close`, `fold_roadmap` and seeding. The R5 guard and every `ROADMAP_VIEW` reader drop it (`grep -n ROADMAP_VIEW plugin/templates/jig/jig.py` finds nothing).
- [ ] `jig update --apply` converts `.jig/roadmap.md` to `roadmap.json`, carrying every phase, scope, item, suffix, note and exit check with its text unchanged. It removes `roadmap.md` and writes `products.json`. It removes a `ROADMAP.md` that jig generated and leaves a repo's own. A second run changes nothing (smoke, with the fixtures `sec_roadmap` uses).
- [ ] The AGENTS.md template's Commands list carries `roadmap: python3 .jig/jig.py roadmap show (the roadmap as a chart; run it when asked to show the roadmap)`. `jig update` adds the line to a repo's AGENTS.md where it is missing.
- [ ] Rules, skills and docs describe the JSON roadmap, the products list and `show`, and none describes `roadmap.md` or `ROADMAP.md` as current. A grep of `plugin` and `docs` for `roadmap.md` and `ROADMAP.md` finds only update's conversion and its rule text.
- [ ] `.jig/decisions.md` `## Unreleased` has Added and Changed lines, with a `**Breaking:**` line for repos that edit `roadmap.md` or read `ROADMAP.md`.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched.

## Out of scope
- A stage level. The owner asked whether one is needed. Claude answered no: product-scoped phases,
  waits and labels cover it. Nothing here adds one.
- Which repo controls a glossary term, and the `Owner:` line: layout-glossary-form, which reads
  this part's products list. Until it lands, `--owner` and the Family code read `Owner:` as today.
- The decision log, the ideas log and the deferred ledger: the owner left them as they are (2026-11-24).
- Taking Towyr off a roadmap, and moving the Maige repos onto one roadmap: that is those repos'
  work once this lands.
- This repo's own `.jig/` changes only when `/jig:update` is run, after release (AGENTS.md).

## Touches
- `plugin/templates/jig/jig.py`:
  - Roadmap parsing:
    - the constants `ROADMAP`, `ROADMAP_VIEW`, `SCOPE_LINE`, `NO_PHASE`, `UP_NEXT`, `TOUCHES` and `RESERVED` (L10765-10820);
    - `split_waits` L10891, `phase_waits` L10916, `phase_labels` L10923, `repeated_waits` L10931, `refs_of` L10951;
    - `parse_no_phase` and `parse_section` L10955-10968, `parse_roadmap` L11060;
    - `roadmap_label_problems` L11168, `ref_problems` L11185, `unconfirmed` L11232, `rings` L11261, `cited` L11324;
    - `product_of` L11571, `phase_type` and `type_problems` L11582-11598.
  - States: `scope_takers` L11787, `_roadmap_full` L11835.
  - The chart and the seed: `render_roadmap` L11910, `ROADMAP_SEED` L11961, `roadmap_withheld` L11974, `empty_roadmap` and `ensure_roadmap` L11987-12045.
  - The command: `ROADMAP_FILTERS` and `roadmap_filter` L12089-12127, `cmd_roadmap` L12182.
  - Draft and edit: `roadmap_problems` L12281, `draft_path` L12316, `may_change` L12342, `roadmap_draft` L12357, `section_refusals` L12415, `plumb_commit` L12494, `record_roadmap_row` L12561, `roadmap_edit` L12599.
  - Hooks: `check_rules` R5 L592-601, `roadmap_rules` L13335-13428 (`dropped_scopes` L13220, `scope_holders` L13228, `others_holding` L13243).
  - Update and fold: `up_next_heading`, `fold_up_next` and `fold_roadmap` L13817-13874, `STEPS` L13954-14022, a conversion step.
  - Merge and close: `cmd_merge` L2156-2176 (`retarget_touches`, `items_follow_moves`, the view), `close_merged` L2240, `rig_close` L17484.
  - Other `ROADMAP_VIEW` readers: `DOC_HOMES` L3614, `at_home` L4050, `meta_rules` L5814, `meta_problems` L5862, `meta_citations` L9572, `boundary_rules` L12979, `PLAN_FILES` and `plan_files` L16446-16484, `cmd_sweep` L16675-16692.
  - Move-in: `undefined_sweep` L16536, `cmd_move_in` L17893-17937, `roadmap_takers` L18086.
  - argparse L18750-18759.
- `plugin/templates/jig/RULES.md`: `## Roadmap` (L943-1221) and the Metarepo and pararepos lines on editing the roadmap
- `plugin/templates/AGENTS.md`
- `plugin/skills/init/SKILL.md` (L44, L46), `plugin/skills/update/SKILL.md` (L143, L230, L233, L260), `plugin/skills/hubnode/SKILL.md` (L343), `plugin/skills/stage/SKILL.md` (a roadmap change lands through `--draft`/`--edit`), `plugin/skills/spec/SKILL.md` (step 3), `plugin/skills/rig/SKILL.md`, `plugin/skills/retro/SKILL.md` (`## No phase` stop)
- `tests/smoke.sh`, and a chart fixture under `tests/fixtures/`
- `README.md` (L32-34, L96-97), `docs/records.md` (`## Roadmap`), `docs/metarepos.md` (Editing the roadmap, L71-87), `docs/commands.md` (L56, L91-108), `docs/jobs.md` (L58)
- `docs/glossary.md § Roadmap`, `§ Phase`, `§ Scope`, `§ Label` (`reading-list --claims` lists each copy; each is updated or made a pointer)
- `.jig/decisions.md`

## Alternatives considered
- Keep `roadmap.md` and add query commands. Rejected: the owner ruled for JSON ("I dont need to read it"). [seen]
- Commands that add, change and drop a phase or scope, in place of `--draft`/`--edit`. Rejected for now. `--draft`/`--edit` already carry section ownership, `propose/` branches and BUFFER rows, and a JSON draft keeps all of that. The field check stops hand-made fields at `--edit` and at commit. [assumed]
- Put the products list inside `roadmap.json`. Rejected: which repo builds a product describes the family, not the plan. layout-glossary-form reads it for every term, and a product left off the roadmap still has its repo. [assumed]

## Decisions
- Interpreted: the request is built as five jobs, one per part, in the order layout-docmap, layout-roadmap-json, layout-later-ledger, layout-glossary-form, layout-rules-templates-names. Each part changes a different system, so each review stays small, and the order is real (parts 2 to 4 build on part 2's products list and ids, and part 5 splits and templates what 2 to 4 rewrite). The alternative is one job carrying all five specs, which the owner leaned to on 2026-11-23 ("Recommend building 2,3,4 with 1 then") before he said "your call". He hasn't answered this yet (the owner was away when it was written). Keeping them apart needs `Kept separate` lines on his word.
- Interpreted: a phase holds its name, its product (where the roadmap has more than one), its note, its exit checks and its waits. A scope holds its id, its text, its labels, the pages it touches and its waits. State and blocked stay derived. A phase's type stays read from its name (the stager's reading).
- Interpreted: a `no_phase` item holds what a scope holds, plus `stopped_at` and `parked` as fields (the stager's reading). Conversion fills them from RULES's form, "`<what>; stops at <where>; parked <YYYY-MM-DD>`". An item not written in that form keeps its whole text in `text`.
- Interpreted: no stage level (the stager's reading of the 2026-11-23 exchange).
- Interpreted: the products list is `.jig/products.json`, in each stand-alone repo and metarepo. A pararepo reads its metarepo's. The roadmap's `products` names the included ones. A stand-alone repo lists its software product (its repo is the board's `name`) and any hardware it runs on.
- Interpreted: `jig update` converts each `roadmap.md` (the stager's reading). In a metarepo it fills `products.json` from the glossary's `Owner:` terms. Where two products name one repo, it writes both as `software` and reports the clash for the user to mark the hardware one. The commit check then refuses until they do.
- Interpreted: `--draft` and `--edit` stay, reading and writing JSON (jig's choice).
- Interpreted: `--view` goes, since `show` replaces it. So does `--write`, since nothing is left for it to write.
- Interpreted: "show me the roadmap" triggers through a line in the always-loaded AGENTS.md, which any agent reads, not through a Claude skill description.
- Interpreted: in `show`, a scope's column comes from its waits, and within a column, scopes sharing a first label sit together. A product's `no_phase` items print as a last band.
- Interpreted: two jobs never change these files at once. As on trunk today, the roadmap and now the products list change only on trunk or on a metarepo's `propose/` branch (R5). That answers the owner's question about a branch holding a file while another waits ("cant a branch check out a file and another branch wait until the file is available again?").
- Interpreted: a repo's own `ROADMAP.md` still holds the seed back, as now. Its content is a roadmap for the user to move in.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
