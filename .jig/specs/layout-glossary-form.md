# layout-glossary-form: one glossary form, controls from the products list, binds on the term

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

Part 4 of 5. It is built after layout-roadmap-json, whose `.jig/products.json` it reads, and before
layout-rules-templates-names.

## Intent
`docs/glossary.md` takes one form:
- `# Basic terms` comes first.
- Then one H1 per product, in alphabetical order.
- Each product holds its own H3 terms, then its H2 features in alphabetical order, each feature with its H3 terms.

It is checked at commit and re-sorted at merge. A term's controlling repo is read from its
product and the products list, not from a hand-written `Owner:` line. `Binds:` is the one field line
a term may carry. Two query commands print one term, and the decision entries touching one page.

The owner's words:
- 2026-11-22: "I want glossary to be organized by product and feature with H1 tags for products and H2 tags for features and H3 tags for everything within a feature or non-feature items outside of a feature."
- 2026-11-23: "Product-less terms go in their own H1 which should be first in the glossary. Call it "Basic terms"."
- 2026-11-23: "Controls is implicit, yes."
- 2026-11-23: "Agreed jig should refuse fields not in the template, and entries should be checked."

## Done when
- [ ] Terms are read at H1, H2 and H3: a product, a feature and a term are each a glossary term. That holds for labels, `docs/glossary.md § <term>` pointers, Touches terms, `--claims`, duplicate checks and release term diffs. Table rows are no longer terms (smoke: `sec_glossary`, `sec_labels`, `sec_touches_terms`, `sec_claims`, `sec_headings`).
- [ ] A commit that changes `docs/glossary.md` is refused when any of these holds (smoke, one case each):
      - its first H1 isn't `Basic terms`;
      - `Basic terms` holds an H2;
      - an H1 other than `Basic terms` isn't a product on the products list (the metarepo's in a family);
      - a heading is H4 or deeper;
      - the file has a table;
      - two headings fold to one term;
      - a term's body has a field line other than `Binds:`. An `Owner:` line's refusal names `.jig/products.json`;
      - a `Binds:` line appears outside a metarepo's glossary;
      - a `Binds:` value isn't a product or feature heading in the glossary.
- [ ] `jig merge` re-sorts `docs/glossary.md` in the merge commit. `Basic terms` comes first, then products in alphabetical order. Within a parent, its own H3s come first in alphabetical order, then its H2s in alphabetical order. Whole entries move, no words change, and no entry moves to another parent. A glossary already in order is left byte-identical (smoke).
- [ ] `jig glossary add "<term>" --under "<product>[/<feature>]" --text "<definition>" [--binds <a>,…]` writes the entry in its sorted place and refuses a duplicate. `jig glossary "<term>"` prints the term's heading path, its definition, its `Binds:` and its controlling repo (smoke).
- [ ] `jig decision --page <page>` prints each decision entry whose `Touches:` names the page, or a term on it (smoke).
- [ ] The controlling repo of a term is the repo of the product it sits under, from the products list. A term under `Basic terms` is controlled by the repo holding the glossary. No `Owner:` line is read, and `this repo` is no longer a value. `grep -n 'OWNER_LINE\|THIS_REPO' plugin/templates/jig/jig.py` finds nothing. Every former reader gives the same answer on a fixture moved from `Owner:` lines to a products list: the product of a roadmap heading, the `--label` head, `--owner`, the Family class, move-in, `owner_dropped`, the family report, `type_problems` and update's type check. `sec_family`, `sec_family_report`, `sec_phase_types` and `sec_movein` pass.
- [ ] `owner_dropped` becomes: a commit dropping a product from the products list is refused while the glossary still has its H1 (smoke).
- [ ] `jig move-in` adds the moved product to the products list instead of writing `Owner:` (`sec_movein`).
- [ ] `jig init` seeds the glossary as `# Basic terms` with no title heading. `jig update` reports a glossary not in the form, and each `Owner:` line, saying where its value now lives. It rewrites neither (smoke).
- [ ] RULES says, for whoever writes a term and for review: a heading that is a name (a product, a feature, a library, a package) keeps its own spelling. Any other heading starts with one capital and is otherwise lowercase, as "Basic terms" is. `§` is written only in a pointer, `docs/glossary.md § <term>`, and names a heading at any of the three levels.
- [ ] Rules, skills, templates and docs describe the one form, `Binds:` and the products list as the source of control, and none describes `Owner:` or a table glossary as current.
- [ ] `.jig/decisions.md` `## Unreleased` has Added and Changed lines, with a `**Breaking:**` line for repos whose glossary uses `Owner:`, tables or another form.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched.

## Out of scope
- Rebuilding any repo's glossary in the new form, Maige-Ecosystem's, Daisy's and this repo's
  included. The request lists these as those repos' own work once this lands, and asks for no
  migration of any repo's pages.
- A heading-case check in the hook. jig can't tell a name from an ordinary word, so the rule is for
  writers and review (the stager's reading).
- The decision log's format. Only a query over it is added. The owner left the log as it is (2026-11-24).

## Touches
- `plugin/templates/jig/jig.py`:
  - Parsing: `GLOSSARY` and `GLOSSARY_SEED` L4943-4950, `term_text` L4978, `bold_terms` L4990, `table_terms` L4999, `glossary_terms` L5016, `glossary_term_in` L5024, `glossary_unheaded` L5031, `page_sections` L2797.
  - Terms and pointers: `claims_of_term` L3188, `touched_term` L7542, `pointer_gap` L9747, `term_blocks`, `glossary_at` and `glossary_changes` L8901-8926.
  - Checks: `heading_lines` and `heading_rules` L13049-13066, `label_fold` and `label_problems` L10868-10874, `doc_homes` L4163.
  - Metarepo: `entry_files` and M3/M6 L5662-5830.
  - `Owner:` and its readers:
    - `OWNER_LINE`, `THIS_REPO`, `term_owners`, `product_of` and `type_problems` L11551-11598;
    - `Family` L11615-11740 (`owner_loc`, `owner_gone`, `ours`, `pages_of`, `page_home`, `section_of`, `products_in`, `unknown_owners`);
    - `roadmap_filter`/`owner_of` L12107-12127, `cmd_roadmap` L12222-12246, `label_heads` and `work_owner` L12297-12305, `stage_label` L12594, `family_report.repo_of` L12780, `cmd_family` L12796-12813;
    - `moving_in` L13187-13209, `proposal_section_refusals` L13294, `roadmap_rules` L13369-13374;
    - `cmd_update` type check L15051, `owner_dropped` L17568 (hook at L603-609), `cmd_move_in` L17764-17995, `receiver_plan` L18144.
  - Merge: `cmd_merge` L2044 (the re-sort).
  - Commands: `cmd_decision` L7074, `entry_touches` L7199, argparse `decision` and a new `glossary`.
- `plugin/templates/jig/RULES.md`:
  - glossary L440-458 (under `### Homes`) and duplicate addresses L298-305;
  - labels L976-993, `--owner` L1005-1012, products and `Owner:` L1035-1044;
  - Touches terms L1257-1262, idea labels L1296-1303;
  - metarepo entry files L1763-1781, family report L1881-1890, `--claims` L1919-1923.
- `plugin/skills/init/SKILL.md` (L60), `plugin/skills/spec/SKILL.md` (L46-47, L62), `plugin/skills/update/SKILL.md` (L125, L183-190), `plugin/skills/hubnode/SKILL.md` (L305, L314), `plugin/skills/retro/SKILL.md` (L30), `plugin/skills/stage/SKILL.md` (staging a new label)
- `tests/smoke.sh`
- `docs/records.md` (Pages: "one heading per term"), `docs/metarepos.md`, `docs/commands.md`, `docs/hooks.md`, `docs/glossary.md § Label` (the definition, not the file's form)
- `.jig/decisions.md`

## Alternatives considered
- Glossary as JSON. Rejected by the owner: "I'd like to be able to read that one" (2026-11-22). [seen]
- Controls and binds on the docmap as well as the term. Proposed first, then the owner settled on one place, the term (2026-11-22). [seen]
- Keep `Owner:`, renamed `Controls:`. Rejected: "Controls is implicit". [seen]
- Keep reading table rows as terms during the move. Rejected: the owner wants one form, and the table form's readers are most of the code this part replaces. [assumed]

## Decisions
- Interpreted: the request is built as five jobs, one per part, in the order layout-docmap, layout-roadmap-json, layout-later-ledger, layout-glossary-form, layout-rules-templates-names. Each part changes a different system, so each review stays small, and the order is real (parts 2 to 4 build on part 2's products list and ids, and part 5 splits and templates what 2 to 4 rewrite). The alternative is one job carrying all five specs, which the owner leaned to on 2026-11-23 ("Recommend building 2,3,4 with 1 then") before he said "your call". He hasn't answered this yet (the owner was away when it was written). Keeping them apart needs `Kept separate` lines on his word.
- Interpreted: the terms under "Basic terms" are H3, as non-feature items outside a feature. A product's own terms are H3 directly under its H1, before its first H2 (the stager's reading).
- Interpreted: a product's or a feature's own definition is the paragraph directly under its heading (the stager's reading).
- Interpreted: in a stand-alone repo the H1s are its software product and any hardware it runs on, and the H2s are its features (the stager's reading). In a pararepo, the H1s are products on the metarepo's list.
- Interpreted: a heading that is a name keeps its own spelling, and any other heading is sentence case. This is a rule for writers and review, not a hook check (the stager's reading). Whether a term like `mote` counts as a name was never asked, so it is left to the writer.
- Interpreted: `§` is written only in a pointer and names a heading at any of the three levels (the stager's reading).
- Interpreted: controls is never written. A term's controlling repo is its product's repo, read from the products list (the stager's reading). A `Basic terms` term is controlled by the repo whose glossary holds it.
- Interpreted: binds is one line under a term, written only where the term applies beyond its own product, and only in a metarepo's glossary (the stager's reading).
- Interpreted: the commit check refuses structure, fields, binds and duplicates. Order is not refused, because the merge re-sorts it ("Agreed on chart and upkeep").
- Interpreted: the re-sort is there for entries edited by hand. It moves an entry only within its parent, since a move across parents changes what controls it (the stager's reading).
- Interpreted: the glossary has no title heading, since its first H1 is `Basic terms`.
- Interpreted: the check runs only on a commit that changes the glossary. A repo whose glossary isn't yet in the form keeps working until its own rebuild, which is the commit that puts it in the form. A `## <term>` glossary still resolves, since H2 headings are read. A table glossary does not: its labels and pointers fail at `jig update` until its rebuild. That is the cost of dropping the table form now.
- Interpreted: the queries are `jig glossary "<term>"` and `jig decision --page <page>`, the "query commands" among the owner's four Do's (the stager's reading). `jig glossary add` is the command that "writes it in its place" ("Agreed on chart and upkeep").

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
