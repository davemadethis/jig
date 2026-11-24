# layout-docmap: the docmap leaves config.json for its own file

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

Part 1 of 5 (layout-docmap, layout-roadmap-json, layout-later-ledger, layout-glossary-form,
layout-rules-templates-names). The parts are built in that order. Each is a job of its own,
and this part waits on none.

## Intent
The docmap and the other keys that describe the docs tree (`docmap`, `boards`, `deep_subsystems`,
`not_docs`) live in `.jig/docmap.json`, not `.jig/config.json`. Every reader reads them there.
Agents query them through a jig command instead of reading the file, and `jig update` moves the
keys in each repo. The owner, 2026-11-22: "docmap - is it really a configuration? I dont see it
as such. Why not make it it's own .json file? And agreed, query instead."

## Done when
- [ ] After `jig init`, a fresh repo has `.jig/docmap.json` holding `docmap: {}` and
      `not_docs: []`, and `.jig/config.json` holds none of the four keys (smoke).
- [ ] `jig update --apply`, in a repo whose `config.json` holds all four keys, moves each key into
      `docmap.json` with its value unchanged, removes it from `config.json` and bumps the stamp. A
      second run reports nothing to do (smoke).
- [ ] Every reader in the Touches list reads `docmap.json`. The smoke sections that exercise
      them (`sec_homes`, `sec_meta_docs`, `sec_glossary`, `sec_claims`, `sec_touches_terms`,
      `sec_update`, the reading-list and gate cases) pass, with fixtures writing `docmap.json`.
- [ ] A commit adding a key to `docmap.json` other than the four is refused, naming the four. A
      value of the wrong type is also refused: `docmap` must be an object mapping a page to a list
      of globs, `not_docs` and `deep_subsystems` lists of strings, and `boards` its present shape
      (smoke).
- [ ] `jig docmap <page>` prints the page's globs and whether it is a board or a deep subsystem.
      `jig docmap <path>` prints the pages that cover the path, without the reading list's
      pages-above (smoke).
- [ ] No skill, rule, template or docs page in this repo says to read one of the four keys from
      `config.json`. `grep -rn 'config.json' plugin docs README.md` shows none naming them.
- [ ] `.jig/decisions.md` `## Unreleased` has a Changed line, with a `**Breaking:**` line for a
      repo's own tools that read `config.json`'s docmap.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched.

## Out of scope
- Every other config key (`common`, `append_files`, `reserve`, `roles`, `queue`, `findings`,
  `derived_files`) stays in `config.json`. The owner moved the docmap only.
- This repo's own `.jig/` changes only when `/jig:update` is run, after release (AGENTS.md).

## Touches
- `plugin/templates/jig/jig.py`:
  - `BOARD_DEFAULTS` (L49-63), `BOARD_OPTIONAL` (L66-73), `Board.load` (L248-263), `STAMP` (L46), `cmd_init` (L879).
  - The 15 `.get("docmap")` sites: `doc_owners` L772, `cmd_reading_list` L3256/3268, `cmd_gate` L3435, `misfiled_seams` L4269, `page_levels` L4590, `unpaged_build` L5122, `named_pages` L5163, `cmd_survey` L5282/5297, `touches_problems` L7582, `decision_citers` L8837, `move_lines` L14756, and the rest.
  - `boards` (`carry_out` L4934, `board_pages` L5157).
  - `deep_subsystems` (L3281, L4591, L4774).
  - `not_docs` (`check_rules` L611-613, L4326, L4421, L4773).
  - `rewrite_board` (L14182-14282) and a new update step.
  - A new `docmap` subcommand in argparse.
- `plugin/templates/jig/RULES.md`: L193, L335, L561 ("Ownership comes from `docmap` in `config.json`").
- `plugin/skills/hardware/SKILL.md` (L78, L97), `plugin/skills/adopt/SKILL.md` (L44), `plugin/skills/work/SKILL.md` (L49), `plugin/skills/retro/SKILL.md` (L8), `plugin/skills/redocument/SKILL.md` (L118, L199), `plugin/skills/survey/SKILL.md` (L28), `plugin/skills/init/SKILL.md`, `plugin/skills/update/SKILL.md`
- `plugin/templates/AGENTS.md` (Firmware: "listed in `boards` in `.jig/config.json`")
- `tests/smoke.sh`
- `docs/records.md` (Docs move with code), `docs/commands.md`, `docs/hooks.md`, `docs/glossary.md § Board` (check it still holds)
- `.jig/decisions.md`

## Alternatives considered
- Keep the keys in `config.json` and add only the query command. Rejected because the owner ruled
  the docmap is not configuration and gets its own file. [seen]

## Decisions
- Interpreted: `boards`, `deep_subsystems` and `not_docs` move with `docmap`, since they describe the docs tree, not how jig runs (the stager's reading).
- Interpreted: `jig update` moves the keys in each repo (the stager's reading). The move is a step in the `STEPS` table, keyed on the keys being in `config.json`, not on the stamp.
- Interpreted: two jobs that change the docmap at once merge as they do today in `config.json`. jig writes `docmap.json` sorted, one key per line, so two separate additions merge as lines. Nothing new handles this, because the docmap already lives in a merged JSON file.
- Interpreted: the query command is `jig docmap <page or path>…`. `jig reading-list` stays the command for what to read before touching files. Agents still write the file by hand (a new page's row). The commit check refuses any key or shape jig doesn't know, per the owner, 2026-11-21: "hand-made fields should not be allowed".

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
