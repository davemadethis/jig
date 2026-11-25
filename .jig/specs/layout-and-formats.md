# layout-and-formats: docmap.json, roadmap.json, Later: retired, one glossary form, a rules folder

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

This spec merges the five specs written from the request: layout-docmap, layout-roadmap-json,
layout-later-ledger, layout-glossary-form and layout-rules-templates-names. All five carried the
Source line above, unchanged. It is one job. Line numbers are `plugin/templates/jig/jig.py` at
trunk 10f8a98 unless another file is named.

## Intent
Five changes to where jig keeps things and in what format, built as one job:
1. The docmap moves to its own file.
2. The roadmap becomes queryable JSON with a chart command.
3. The spec's `Later:` line retires: work not built stays on the roadmap.
4. The glossary takes one form, in which product headings carry `Repo:` and `Kind:`, and which jig checks and sorts.
5. The rulebook becomes a folder of rulesets. Every record gets a template, `.jig/` names are lowercase, and jig's text says "the owner" throughout.

In more detail:
1. `docmap`, `boards`, `deep_subsystems` and `not_docs` move from `.jig/config.json` to `.jig/docmap.json` and are queried through `jig docmap`.
2. `.jig/roadmap.json` replaces `.jig/roadmap.md`. It names the products it includes by their glossary terms. `jig roadmap show` prints a dependency-ordered chart in place of `ROADMAP.md`.
3. `Later:` is retired. A spec takes only what it builds, and work not built stays on the roadmap as unspecced work.
4. `docs/glossary.md` takes one form, `# Basic terms` then product H1, feature H2 and term H3. Product H1s carry `Repo:` and `Kind:`, and a term's controlling repo is its product's `Repo:`. The form is checked at commit and sorted at merge, and two commands query it.
5. The rulebook becomes `.jig/rules/rules-<ruleset>.md`, with metarepo and pararepo rules only in those repos. Every record gets a template in `.jig/templates/`. Names under `.jig/` are lowercase, and jig's text says "the owner" throughout.

## Done when

From part 1 (docmap.json):
- [ ] After `jig init`, a fresh repo has `.jig/docmap.json` holding `docmap: {}` and `not_docs: []`, and `.jig/config.json` holds none of the four keys (smoke).
- [ ] `jig update --apply`, in a repo whose `config.json` holds all four keys, moves each into `docmap.json` with its value unchanged, removes it from `config.json` and bumps the stamp. A second run reports nothing to do (smoke).
- [ ] Every reader in Touches reads `docmap.json`. The smoke sections that exercise them (`sec_homes`, `sec_meta_docs`, `sec_glossary`, `sec_claims`, `sec_touches_terms`, `sec_update`, the reading-list and gate tests) pass with fixtures writing `docmap.json`.
- [ ] A commit adding a key to `docmap.json` other than the four is refused, naming the four. A value of the wrong type is refused too: `docmap` maps a page to a list of globs, `not_docs` and `deep_subsystems` are lists of strings, and `boards` keeps its present shape (smoke).
- [ ] `jig docmap <page>` prints the page's globs and whether the page is a board or a deep subsystem. `jig docmap <path>` prints the pages covering the path, without the reading list's pages-above (smoke).
- [ ] No skill, rule, template or docs page says to read one of the four keys from `config.json`. `grep -rn 'config.json' plugin docs README.md` shows none naming them.

From part 2 (roadmap.json):
- [ ] `jig init` writes `.jig/roadmap.json` (`products: []`, `phases: []`, `no_phase: []`), and no `ROADMAP.md` or `.jig/roadmap.md` (smoke).
- [ ] The records hold:
      - a phase: `product` (only where the roadmap includes more than one product), `name`, `note`, `exit` (a list of `{text, done}`), `after`, `needed_by`, `scopes`;
      - a scope: `id`, `text`, `labels`, `touches`, `after`, `needed_by`;
      - a `no_phase` item: what a scope holds, plus optional `product`, `stopped_at` and `parked` (`YYYY-MM-DD`);
      - `products`: the included products, each a product term of the glossary (the metarepo's in a family).

      Nothing else is written. State and blocked stay derived, and a phase's type is still read from its name.
- [ ] A commit changing the roadmap or the glossary is refused when the roadmap has an unknown field or a field of the wrong type, or names a product that isn't in its `products` or isn't a product heading with `Repo:` and `Kind:` in the glossary. Every check `roadmap_problems` runs today still runs: refs, rings, repeated waits, phase-type order, labels against the glossary, and the unconfirmed cross-product `after` (smoke).
- [ ] A product in the glossary that the roadmap doesn't include gets no phase, scope or item. Rig, update and staging never ask about it (smoke).
- [ ] On a converted fixture, `jig roadmap`, its filters (`--product`, `--phase`, `--type`, `--state`, `--owner`, `--label`), the `Scope:` id checks, the drop guard, rig and the gate give the same answers as on its `roadmap.md` before conversion. `sec_roadmap`, `sec_roadmap_edit`, `sec_phase_types`, `sec_labels`, `sec_family`, `sec_boundary`, `sec_move`, `sec_movein`, `sec_close`, `sec_sweep` and `sec_rig` pass on JSON fixtures.
- [ ] `jig roadmap --draft` writes the roadmap as a JSON draft. `--edit` checks it and writes it, with section ownership, `propose/` branches and BUFFER rows working as today (smoke).
- [ ] `jig roadmap show [filters]` prints a text chart with no dates. A scope's column is one past the furthest column of anything it waits on. Every entry is one width, and a phase box (and a product box where there is more than one product) is as wide as its children. Each box shows the scope's id and state. Within a column, scopes sharing a first label sit together. A chart wider than 100 columns (or `--width`) prints one band per phase (smoke, against an expected-output fixture).
- [ ] `--view` and `--write` are gone. No path writes `ROADMAP.md`: merge, `close_merged`, `rig_close`, `fold_roadmap` and seeding all stop. The R5 guard and every `ROADMAP_VIEW` reader drop it, so `grep -n ROADMAP_VIEW plugin/templates/jig/jig.py` finds nothing.
- [ ] `jig update --apply` converts `.jig/roadmap.md` to `roadmap.json`, carrying every phase, scope, item, suffix, note and exit check with its text unchanged. It places each phase under its product as the old `Owner:` terms did, and removes `roadmap.md`. It removes a `ROADMAP.md` that jig generated and leaves a repo's own. A second run changes nothing (smoke, with `sec_roadmap`'s fixtures).
- [ ] The AGENTS.md template's Commands list carries `roadmap: python3 .jig/jig.py roadmap show (the roadmap as a chart; run it when asked to show the roadmap)`, and `jig update` adds the line to a repo's AGENTS.md where it is missing.
- [ ] Rules, skills and docs describe the JSON roadmap and `show`, and none describes `roadmap.md` or `ROADMAP.md` as current. A grep of `plugin` and `docs` for either finds only update's conversion and its rule.

From part 3 (`Later:` retired):
- [ ] `Later:` is gone from jig.py:
      - `spec_laters` and `laters_in`;
      - the `Later:` half of `cited`, `scope_holders` and `roadmap_rules`, including the pararepo check against the metarepo;
      - the gate's `later` lines under "Closes with the spec at merge:", which keeps the spec's `## Out of scope` lines;
      - `close_specs` carrying `Later:` onto the note;
      - rig's Left for later and its `--json` `later` key;
      - move-in's re-pointing of `Later:`.

      `grep -n 'Later' plugin/templates/jig/jig.py` finds only the refusal below and update's step (smoke: `sec_roadmap`, `sec_close`, `sec_rig`, `sec_movein`, `sec_move`).
- [ ] A commit that adds or changes a spec carrying a `Later:` line is refused. The refusal says the work stays on the roadmap, unspecced, and to delete the line (smoke).
- [ ] `jig update --apply` deletes the `Later:` line from each spec on trunk and reports each one. Each id is already on the roadmap, so nothing is lost. Handoff notes are history and are left as they are (smoke).
- [ ] RULES, the spec template, and the spec, review, work and hubnode skills carry the two rules:
      1. A spec takes only what it builds. When a spec builds only part of a scope, a roadmap change on the owner's yes splits it: the built part becomes a new scope, which the spec takes whole and may restate in its own words; the parts not built stay in the original scope, under its id, with their text unchanged; and a wait on the original id keeps waiting until the rest is built. No new scope state: a scope stays untaken, taken or done.
      2. Out of scope never defers. Work worth building later goes onto the roadmap as a scope or `No phase` item on the owner's word, and review blocks a deferral written as prose.
- [ ] The spec template's `Later:` comment is gone, and its `## Out of scope` comment states rule 2. A grep of `plugin` and `docs` for `Later:` finds only the refusal's rule and update's step.

From part 4 (the glossary):
- [ ] H1, H2 and H3 headings are glossary terms: a product, a feature and a term are each one. That holds for labels, `docs/glossary.md § <term>` pointers, Touches terms, `--claims`, duplicate checks and release term diffs. Table rows are no longer terms (smoke: `sec_glossary`, `sec_labels`, `sec_touches_terms`, `sec_claims`, `sec_headings`).
- [ ] A product H1 carries a `Repo:` line (the repo that builds it, or `none`) and a `Kind:` line (`software` or `hardware`). A term may carry only `Binds:`, and only in a metarepo's glossary. A feature H2 and `Basic terms` carry no field line.
- [ ] A commit changing `docs/glossary.md` is refused when it adds any of these problems. A glossary in the form has none (smoke, one test each):
      - the first H1 isn't `Basic terms`;
      - `Basic terms` holds an H2;
      - a heading is H4 or deeper;
      - the file has a table;
      - two headings fold to one term;
      - a product H1 lacks `Repo:` or `Kind:`;
      - a field line isn't one its heading may carry (an `Owner:` line's refusal names `Repo:`);
      - a `Binds:` value isn't a product or feature heading in the glossary;
      - two products name one repo with `Kind: software`;
      - a product the roadmap includes or names is dropped.

      The last replaces `owner_dropped`.
- [ ] `jig merge` re-sorts `docs/glossary.md` in the merge commit. `Basic terms` comes first, then products alphabetically. Within a parent, its own H3s come first in alphabetical order, then its H2s in alphabetical order. Whole entries move, no words change, and no entry moves to another parent. A glossary already in order stays byte-identical (smoke).
- [ ] `jig glossary add "<term>" --under "<product>[/<feature>]" --text "<definition>" [--binds <a>,…]` writes a term in its sorted place. `jig glossary add "<product>" --repo <repo|none> --kind <software|hardware> --text "<definition>"` writes a product H1. Both refuse a duplicate. `jig glossary "<term>"` prints the term's heading path, its definition, its `Binds:` (or, for a product, `Repo:` and `Kind:`) and its controlling repo (smoke).
- [ ] `jig decision --page <page>` prints each decision entry whose `Touches:` names the page or a term on it (smoke).
- [ ] A term's controlling repo is its product H1's `Repo:`. A term under `Basic terms`, or under a product with `Repo: none`, is controlled by the repo whose glossary holds it. No `Owner:` line is read, and `this repo` is no longer a value: `grep -n 'OWNER_LINE\|THIS_REPO' plugin/templates/jig/jig.py` finds nothing.
- [ ] Every former `Owner:` reader gives the same answer on a fixture moved from `Owner:` lines to `Repo:`/`Kind:` lines: the `--label` head, `--owner`, the Family class, move-in, the family report, `type_problems` and update's type check. `sec_family`, `sec_family_report`, `sec_phase_types` and `sec_movein` pass.
- [ ] `jig move-in` writes `Repo: <repo>` on the moved product's heading instead of `Owner:` (`sec_movein`).
- [ ] `jig init` seeds the glossary with no title heading. It holds `# Basic terms` and, in a stand-alone repo, an H1 for its software product named for the board's `name`, with `Repo: <name>` and `Kind: software` (smoke).
- [ ] `jig update --apply` rewrites each `Owner: <repo>` line (`this repo` as the repo's name) to `Repo: <repo>` plus `Kind: software` on the same heading. Where two products name one repo, it writes `Repo:` on both, leaves `Kind:` off both, and reports that the owner marks one `software` and the other `hardware`. It reports a glossary not in the form, and re-forms nothing (smoke).
- [ ] RULES says `§` is written only in a pointer, `docs/glossary.md § <term>`, and names a heading at any of the three levels.
- [ ] Rules, skills, templates and docs describe the one form, `Repo:`/`Kind:` on products and `Binds:` on terms. None describes `Owner:` or a table glossary as current.

From part 5 (rules, templates, names, wording):
- [ ] `plugin/templates/jig/rules/` holds `rules-jobs.md`, `rules-docs.md`, `rules-handoff.md`, `rules-workflow.md`, `rules-roadmap.md`, `rules-decisions.md`, `rules-staging.md`, `rules-release.md`, `rules-inbox.md`, `rules-metarepo.md` and `rules-pararepo.md`. `plugin/templates/jig/RULES.md` is gone.
- [ ] Every rule RULES.md held is in exactly one file, apart from what the split drops: the `## Commands` section (L1975-2036, said by `jig -h`) and text that only restates a hook's refusal. The handoff note lists each dropped passage and what says it instead.
- [ ] `jig init` and `jig update --apply` write `rules-metarepo.md` only in a metarepo, `rules-pararepo.md` only in a pararepo, and the rest in every repo. Update removes `.jig/RULES.md`, refreshes the folder as it refreshes `jig.py`, and removes a file left from a kind the repo no longer is (smoke).
- [ ] `jig survey` reports each `.jig/rules/` file over 200 lines and refuses none. On a fresh repo it reports only `rules-decisions.md`, plus any file still over after its refine pass, each named in the handoff note (smoke).
- [ ] The skills of hubnode, subnode, rig, spec, bug, work, review and check each name the rulesets they read, in place of "Read `.jig/RULES.md` first". So does `jig open`'s kickoff (L1301).
- [ ] Every citation of `RULES.md` points at the file now holding the section: jig.py's messages (about 68), skills (about 61), templates, `docs/` and the AGENTS.md template. `grep -rn 'RULES.md' plugin docs` finds only update's removal step.
- [ ] `plugin/templates/` holds a template for each of the following, and `jig init` and `jig update --apply` write each that applies to the repo's kind into `.jig/templates/`:
      - a page, a spec, a handoff note, the process page, a hardware page, a skill;
      - each ledger (deferred, workarounds, and buffer in a pararepo);
      - a glossary term, a glossary product (with `Repo:` and `Kind:`);
      - a roadmap phase, a roadmap scope, a no-phase item.

      A prose record's template is a skeleton, and a JSON record's is an example record. `.jig/docs-page.md` moves to `.jig/templates/page.md` (smoke).
- [ ] The fields of each JSON record (phase, scope, no-phase item) come from one example record in `jig.py`. Update writes it as the template, and the commit check compares new records with it. A field it lacks, or a field of another type, is refused (smoke).
- [ ] `/jig:spec` copies `.jig/templates/spec.md`. Update reports a repo's own `.jig/specs/_template.md` that differs from jig's, and leaves it in place.
- [ ] The ledgers are `.jig/ledgers/deferred.md`, `workarounds.md` and `buffer.md`, and the templates are renamed to match. `jig update --apply` renames each with `git mv`, and re-points the lines jig wrote that cite them, in AGENTS.md and jig's own files. It rewrites the deferred ledger's header cell `Lane / handoff` to `Job / handoff` and changes no row (smoke).
- [ ] `find plugin/templates/jig plugin/templates/ledgers -name '*[A-Z]*'` finds nothing, and no path jig writes under `.jig/` has a capital.
- [ ] Skills, rules, templates and jig.py's messages and comments say "the owner" where they said "the user". There are 44, 2, 0 and 5 today. `grep -rni 'the user' plugin` finds nothing. RULES' `Accepted (Dave, 2026-11-10)` example (L1238) and the docstring at L6116 say `the owner`.

Every part:
- [ ] `.jig/decisions.md` `## Unreleased` has Added, Changed and Removed lines for each part. `**Breaking:**` lines cover:
      - a repo's own tools reading `config.json`'s docmap;
      - edits to `roadmap.md`, or reads of `ROADMAP.md`;
      - a spec carrying `Later:`;
      - a glossary using `Owner:`, tables or another form;
      - citations of `.jig/RULES.md` or the old ledger names.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched. Given the renames, that is most of them.

## Out of scope
- Every other config key (`common`, `append_files`, `reserve`, `roles`, `queue`, `findings`, `derived_files`) stays in `config.json`. The owner moved only the docmap and the keys describing the docs tree.
- A stage level. The owner asked whether one is needed, and Claude answered no: product-scoped phases, waits and labels cover it.
- The decision log, the ideas log and the deferred ledger. The owner left them as they are (2026-11-24). The decision log gains a query only, and `rules-decisions.md` isn't cut under the cap.
- Rebuilding any repo's glossary in the new form, including Maige-Ecosystem's, Daisy's and this repo's. Also taking Towyr off a roadmap, moving the Maige repos onto one roadmap, and Maige-OS's pre-jig deferred ledger layout. The request lists each as that repo's own work once this lands, and asks for no migration of any repo's pages. Update converts only the lines jig wrote or reads: `Owner:`, `Later:` and the ledger header cell.
- Rewording any repo's own pages, code or records. The owner, 2026-11-22: "put the new convention in jig but leave rename out entirely. I'll run it as a job afterwards in the repos that need it." This includes this repo's root AGENTS.md and its own `.jig/`, which change only through `/jig:update` after release (AGENTS.md).
- The author field in `plugin/.claude-plugin/plugin.json`. It is plugin metadata, not jig's text.
- A `questions` record. It came from the direction the request sets aside.

## Touches
- `plugin/templates/jig/jig.py`:
  - **Part 1:**
    - `BOARD_DEFAULTS` L49-63, `BOARD_OPTIONAL` L66-73, `Board.load` L248-263, `STAMP` L46, `cmd_init` L879.
    - The 15 `.get("docmap")` sites: `doc_owners` L772, `cmd_reading_list` L3256/3268, `cmd_gate` L3435, `misfiled_seams` L4269, `page_levels` L4590, `unpaged_build` L5122, `named_pages` L5163, `cmd_survey` L5282/5297, `touches_problems` L7582, `decision_citers` L8837, `move_lines` L14756, and the rest.
    - `boards` (`carry_out` L4934, `board_pages` L5157), `deep_subsystems` (L3281, L4591, L4774), `not_docs` (`check_rules` L611-613, L4326, L4421, L4773).
    - `rewrite_board` L14182-14282 and a new update step, plus a `docmap` subcommand.
  - **Part 2:**
    - Parsing: the roadmap constants L10765-10820; `split_waits` L10891, `phase_waits` L10916, `phase_labels` L10923, `repeated_waits` L10931, `refs_of` L10951; `parse_no_phase` and `parse_section` L10955-10968, `parse_roadmap` L11060.
    - Checks: `roadmap_label_problems` L11168, `ref_problems` L11185, `unconfirmed` L11232, `rings` L11261, `cited` L11324.
    - Products and states: `product_of`, `phase_type` and `type_problems` L11571-11598, `scope_takers` L11787, `_roadmap_full` L11835.
    - Rendering and seeding: `render_roadmap` L11910, `ROADMAP_SEED` L11961, `roadmap_withheld` L11974, `empty_roadmap` and `ensure_roadmap` L11987-12045.
    - The command: `ROADMAP_FILTERS` and `roadmap_filter` L12089-12127, `cmd_roadmap` L12182, `roadmap_problems` L12281.
    - Draft and edit: `draft_path` L12316, `may_change` L12342, `roadmap_draft` L12357, `section_refusals` L12415, `plumb_commit` L12494, `record_roadmap_row` L12561, `roadmap_edit` L12599.
    - Hooks: R5 in `check_rules` L592-601, `roadmap_rules` L13335-13428 (`dropped_scopes` L13220, `scope_holders` L13228, `others_holding` L13243).
    - Update: `up_next_heading`, `fold_up_next` and `fold_roadmap` L13817-13874, `STEPS` L13954-14022.
    - Merge and close: `cmd_merge` L2156-2176, `close_merged` L2240, `rig_close` L17484.
    - `ROADMAP_VIEW` readers: `DOC_HOMES` L3614, `at_home` L4050, `meta_rules` L5814, `meta_problems` L5862, `meta_citations` L9572, `boundary_rules` L12979, `PLAN_FILES` and `plan_files` L16446-16484, `cmd_sweep` L16675-16692.
    - Move-in and sweep: `undefined_sweep` L16536, `cmd_move_in` L17893-17937, `roadmap_takers` L18086.
    - argparse L18750-18759.
  - **Part 3:** `spec_laters` and `laters_in` L11313-11320, `cited` L11324, `close_specs` L11454-11500, `closes_with` L3577 (`cmd_gate` L3395), `left_for_later` L17365 and rig state L17353, `scope_holders` L13228-13237, the warning at L13386, `roadmap_rules` L13382-13428, `move_in_takers` L17720, `cmd_move_in` L17922-17937, `roadmap_takers` L18086, the roadmap seed comment, and a new update step.
  - **Part 4:**
    - Parsing: `GLOSSARY` and `GLOSSARY_SEED` L4943-4950, `term_text` L4978, `bold_terms` L4990, `table_terms` L4999, `glossary_terms` L5016, `glossary_term_in` L5024, `glossary_unheaded` L5031, `page_sections` L2797.
    - Terms and pointers: `claims_of_term` L3188, `touched_term` L7542, `pointer_gap` L9747, `term_blocks`, `glossary_at` and `glossary_changes` L8901-8926.
    - Headings and labels: `heading_lines` and `heading_rules` L13049-13066, `label_fold` and `label_problems` L10868-10874, `doc_homes` L4163.
    - Metarepo: `entry_files` and M3/M6 L5662-5830.
    - `Owner:` and its readers:
      - `OWNER_LINE`, `THIS_REPO`, `term_owners`, `product_of` and `type_problems` L11551-11598;
      - `Family` L11615-11740;
      - `roadmap_filter`/`owner_of` L12107-12127, `cmd_roadmap` L12222-12246, `label_heads` and `work_owner` L12297-12305, `stage_label` L12594, `family_report.repo_of` L12780, `cmd_family` L12796-12813;
      - `moving_in` L13187-13209, `proposal_section_refusals` L13294, `roadmap_rules` L13369-13374;
      - `cmd_update`'s type check L15051, `owner_dropped` L17568 (hook at L603-609), `cmd_move_in` L17764-17995, `receiver_plan` L18144.
    - The re-sort in `cmd_merge` L2044.
    - `cmd_decision` L7074, `entry_touches` L7199, argparse `decision` and a new `glossary`.
  - **Part 5:**
    - RULES.md as a path: `cmd_reading_list` L3275, `RETIRED_RULES` L4119, `doc_homes` L4139, L5048, survey's presence check L5275, `LAYOUT` L13446, `TOOL_FILES` L13461, the `.gitignore` text L13504/13522, `RETIRED_LINES` and the AGENTS.md checks L14456-14471 and L14688-14702, update's `sources` L15081, L16199.
    - RULES.md cited in messages (about 68), and the kickoff L1301.
    - Ledger names: `WORKAROUNDS` L36, `DEFERRED` L39, `BUFFER` L7999, `BUFFER_HEAD` L12520, `BUFFER_SEED` L17564.
    - Survey's size check: `cmd_survey` L5260-5370.
    - Every "the user" string and comment, and the docstring at L6116.
- `plugin/templates/jig/RULES.md` → `plugin/templates/jig/rules/rules-*.md`. Its passages on:
  - the docmap: L193, L335, L561;
  - the glossary: L298-305, L440-458;
  - `Later:`: L643, L680, L875, L878, L953, L1078-1084, L1184, L1192, L1201, L1708, L1995;
  - `## Roadmap` L943-1221: labels L976-993, `--owner` L1005-1012, products and `Owner:` L1035-1044;
  - Touches terms L1257-1262, idea labels L1296-1303, metarepo entry files L1763-1781, family report L1881-1890, `--claims` L1919-1923;
  - the Decision log example L1238.
- `plugin/templates/jig/docs-page.md` → `.jig/templates/page.md`'s source, beside new templates for the handoff note, glossary term, glossary product, phase, scope and no-phase item. The work role picks their folder in `plugin/templates/`.
- `plugin/templates/ledgers/DEFERRED.md`, `WORKAROUNDS.md`, `BUFFER.md` → lowercase
- `plugin/templates/specs/_template.md` (L6, L19), `plugin/templates/process.md`, `plugin/templates/hardware.md`, `plugin/templates/skills/_template/SKILL.md`, `plugin/templates/AGENTS.md`
- `plugin/skills/*/SKILL.md`: every skill, for the rulesets it reads and for "the owner". In particular:
  - hardware L78, L97; adopt L44; work L49, L82-84; retro L8, L14-30; redocument L118, L199; survey L28;
  - init L44, L46, L60; update L125, L143, L183-190, L230, L233, L260;
  - hubnode L235, L237, L305, L314, L337, L343; spec L38-39, L46-47, L62;
  - bug L64; rig L79; review L50; stage.
- `tests/smoke.sh`, and a chart fixture under `tests/fixtures/`
- `README.md` (L32-34, L96-97)
- `docs/records.md`, `docs/metarepos.md`, `docs/commands.md`, `docs/hooks.md`, `docs/jobs.md`, `docs/workflows.md`
- `docs/glossary.md`: § Board, § Roadmap, § Phase, § Scope, § Label (`reading-list --claims` lists each copy, and each is updated or made a pointer)
- `.jig/decisions.md`
- Process homes (RULES.md, Homes): the two spec rules and the rulesets are the rulebook's. Which ruleset a role reads is the role's skill.

## Alternatives considered
- Keep the docmap keys in `config.json` and add only the query command. Rejected because the owner ruled the docmap is not configuration. [seen]
- Keep `roadmap.md` and add query commands. Rejected: the owner wanted JSON ("I dont need to read it"). [seen]
- A products list in `.jig/products.json`, or inside `roadmap.json`. Rejected by the owner, 2026-11-24: "I question if we really need products.json, thats not much information and I feel like it could live somewhere else, maybe glossary or equivalent". [seen]
- Commands that add, change and drop a phase or scope, in place of `--draft`/`--edit`. Rejected by the owner: "keep --draft and --edit, editing JSON". [seen]
- A later ledger, `.jig/ledgers/later.md`, the request's part 3 as staged. Rejected by the owner, 2026-11-24: "if a scope moves content to a spec, that should be content that gets built. If it's not getting built, it should stay in that scope and then its already slated for "later" without having to give it any special place to live. It's just still not specced." [seen]
- Keep `Later:` on the spec. Rejected by the owner: a spec is an artifact of how its job started. [seen]
- A `Scope: <id> (part)` marker, leaving a partly built scope open with "part built by <spec>" beside it. Rejected (the owner, 2026-11-25: "Splitting it is"): it adds a "taken but open" state that every reader would have to agree on, where a split keeps the three states. [seen]
- Glossary as JSON. Rejected by the owner: "I'd like to be able to read that one" (2026-11-22). [seen]
- Controls and binds on the docmap as well as the term. Proposed first, then the owner settled on one place, the term (2026-11-22). [seen]
- Keep `Owner:`, renamed `Controls:`. Rejected: "Controls is implicit". [seen]
- Keep reading table rows as terms until each repo rebuilds. Rejected by the owner: "stop reading table rows as terms at once". [seen]
- A rules-file cap that refuses. Rejected by the owner: "200 reported and not refused". The owner, 2026-11-22: "The quality of a doc in that regard is the ideal measure, not it's size". [seen]
- Keep one RULES.md and mark the metarepo and pararepo sections conditional. Rejected: the owner wants those rules absent from regular repos. [seen]
- Read the JSON field list from each repo's `.jig/templates/`. Rejected by the owner: "once in jig.py, the template a copy". [seen]
- "The user" in jig's text, with a per-machine username in records. Rejected by the owner, 2026-11-24: "keep "the owner" and use it everywhere. Drop the username part of the spec and the github username. Just use "the owner" since its already largely in use." [seen]

## Decisions
- The owner, 2026-11-24, confirming the parts:
  - "1. yes we deemed some of those items as being not really about configuration"
  - "2. yes roadmap.json replaces the md"
  - "4. yes standardized glossary"
  - "5. yes rules get broken up so they're not all read as often"
- The owner, 2026-11-24: "one job for all five".
- The owner, 2026-11-24, on the products list: "glossary: Repo and Kind lines under each product's H1". Each product H1 carries `Repo:` (the repo that builds it, or `none`) and `Kind:` (`software` or `hardware`). These are product-level fields, and `Binds:` stays the only field line on a term. `roadmap.json`'s `products` names the included products by their glossary terms. Control comes from the product H1's `Repo:`.
- The owner, 2026-11-24, on the roadmap trigger: "a Commands line in AGENTS.md".
- The owner, 2026-11-24, on editing the roadmap: "keep --draft and --edit, editing JSON".
- The owner, 2026-11-24, replacing the later ledger, said "yes to all" to two rules:
  1. A spec takes only what it builds. When only part of a scope gets built, the scope is first split in a roadmap change on the owner's yes, and the spec takes only its part.
  2. Out of scope never defers. Work worth building later goes onto the roadmap as a scope or `No phase` item on the owner's word, and review blocks a deferral written as prose.
- The owner, 2026-11-25, amending rule 1: "I disagree with that rule in-so-far as a scope is probably a less specific definition than a spec, a scope's text should be treated more like a staged document when turned into a spec. The parts that come out dont have to stay unchanged, the parts that dont get built yet stay in the scope unchanged. That way homeless lines don't get pushed into odd places, too." This replaces "split the scope first in a roadmap change": the spec takes the parts it builds, in its own words if it likes, and the parts not built stay in the scope's text, unchanged, with the scope open for them.
- The owner, 2026-11-25, choosing how part of a scope is taken: "Splitting the scope in a roadmap change is a fine approach. Which one is easier and more reliable?", then "Splitting it is". A roadmap change on the owner's yes splits the scope: the built part becomes a new scope the spec takes whole, in its own words if it likes, and the parts not built stay in the original scope, its id and their text unchanged, so a wait on that id holds until the rest is built.
- The owner, 2026-11-24, on table glossaries: "stop reading table rows as terms at once".
- The owner, 2026-11-24, on `Basic terms`: control goes to "the repo whose glossary holds it".
- The owner, 2026-11-24, on the JSON fields: "once in jig.py, the template a copy".
- The owner, 2026-11-24, on wording: "keep "the owner" and use it everywhere. Drop the username part of the spec and the github username. Just use "the owner" since its already largely in use." jig.py's comments follow too.
- Interpreted: `boards`, `deep_subsystems` and `not_docs` move with `docmap`, since they describe the docs tree (the stager's reading). The owner's confirmation of part 1 covers "those items".
- Interpreted: update moves the docmap keys in a `STEPS` step keyed on the keys being in `config.json`, not on the stamp.
- Interpreted: two jobs changing the docmap at once merge as today in `config.json`. jig writes `docmap.json` sorted, one key per line.
- Interpreted: the docmap query is `jig docmap <page or path>…`. `jig reading-list` stays the command for what to read first. Agents still write the file by hand, and the commit check refuses any key or shape jig doesn't know, per the owner, 2026-11-21: "hand-made fields should not be allowed".
- Interpreted: a `no_phase` item holds what a scope holds, plus `stopped_at` and `parked`. Conversion fills them from RULES's form, "`<what>; stops at <where>; parked <YYYY-MM-DD>`". Otherwise it keeps the whole text in `text`.
- Interpreted: `--view` and `--write` go, since `show` replaces the one and nothing is left for the other to write.
- Interpreted: in `show`, a scope's column comes from its waits, and within a column, scopes sharing a first label sit together. A product's `no_phase` items print as a last band.
- Interpreted: the roadmap still changes only on trunk or on a metarepo's `propose/` branch (R5), so two jobs never change it at once. The products' `Repo:` and `Kind:` lines live in the glossary, which merges as text like any page. This answers the owner's question, "cant a branch check out a file and another branch wait until the file is available again?"
- Interpreted: a repo's own `ROADMAP.md` still holds the seed back, as now. Its content is a roadmap for the owner to move in.
- Interpreted: `Later:` lines already on trunk go in `jig update --apply`, which deletes each from its spec and reports it. Every id a `Later:` line names is already on the roadmap, so the work stays there, unspecced, as the owner's rule wants. This repo's specs and notes carry none. Landed handoff notes keep theirs as history, and nothing reads them. A job's branch gets trunk's spec at its next sync.
- Interpreted: rule 1 (a spec takes only what it builds) is a rule for the spec role and for review, not a hook check. Nothing in a commit shows whether a job built all of a scope.
- Interpreted: the terms under `Basic terms` are H3. A product's own terms are H3 directly under its H1, before its first H2. A product's or a feature's own definition is the paragraph directly under its heading (the stager's reading).
- Interpreted: in a stand-alone repo, the H1s are its software product and any hardware it runs on, and the H2s are its features. In a pararepo, a product H1 is one from the metarepo's glossary. `jig init` seeds a stand-alone repo's software product H1, named for the board's `name`, so control and `--owner` work from the start.
- Interpreted: `Binds:` is one line under a term, written only where the term applies beyond its own product, and only in a metarepo's glossary (the stager's reading).
- Interpreted: `§` is written only in a pointer and names a heading at any of the three levels (the stager's reading).
- Interpreted: a product with `Repo: none` is controlled, like `Basic terms`, by the repo whose glossary holds it, until a repo builds it.
- Interpreted: the glossary check refuses a commit that adds a form problem, the way `heading_rules` refuses a commit that raises a heading's copy count, not one that leaves an older glossary out of form. `jig update`'s `Owner:` → `Repo:`/`Kind:` rewrite removes problems, so a repo can commit it before rebuilding its glossary. A new term in an out-of-form glossary is refused until the rebuild. The alternative was to refuse any commit that leaves the glossary out of form, which would block update's own rewrite.
- Interpreted: until a glossary is in the form, a heading at any level carrying `Repo:` is read as a product, so an older metarepo glossary keeps its products after update's rewrite. In the form, only H1s may carry `Repo:`.
- Interpreted: the commit check refuses structure, fields, binds and duplicates. Order is not refused, because the merge re-sorts it ("Agreed on chart and upkeep"). The re-sort moves an entry only within its parent, since a move across parents changes what controls it.
- Interpreted: the glossary has no title heading, since its first H1 is `Basic terms`.
- Interpreted: the queries are `jig glossary "<term>"` and `jig decision --page <page>`, the "query commands" among the owner's four Do's. `jig glossary add` is the command that "writes it in its place" ("Agreed on chart and upkeep").
- Interpreted: a rules file over the cap gets a refine pass, and is split only if it governs two things (the stager's reading).
- Interpreted: the rulesets are jobs, docs, handoff, workflow, roadmap, decisions, staging, release and inbox, plus metarepo or pararepo where the repo is one (the stager's reading). A rule both kinds need goes in each, worded for that side. Today's sections map as follows:

  | Today's section | Ruleset |
  |---|---|
  | Nodes, The board, The rules, Keeping merges mechanical, Reserved numbers, Hooks are opt-in | jobs |
  | Documentation | docs |
  | Fold-in, Sync, Handoff gate merge | handoff |
  | Workflow | workflow |
  | Roadmap | roadmap |
  | Decision log | decisions |
  | Staging | staging |
  | Inbox, Riggers | inbox |
  | Versioning, Release | release |
  | Metarepo and pararepos | metarepo and pararepo, split by which repo each rule binds |
- Interpreted: the split drops the command list and any text that only restates a hook's refusal (the stager's reading).
- Interpreted: `rules-decisions` starts over the cap and is reported, not cut (the stager's reading).
- Interpreted: templates are jig's files, refreshed by update like `jig.py` (the stager's reading). A prose record's template is a skeleton, and a JSON record's is an example record.
- Interpreted: `jig update` renames the ledgers and re-points what cites them (the stager's reading). That means the lines jig wrote, not a repo's own pages. It also rewrites the one header cell, `Lane / handoff` → `Job / handoff`, and no row.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
