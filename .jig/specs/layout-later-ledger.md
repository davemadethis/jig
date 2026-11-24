# layout-later-ledger: a later ledger in place of the spec's Later: line

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

Part 3 of 5. It is built after layout-roadmap-json, whose roadmap ids its rows name, and before
layout-glossary-form and layout-rules-templates-names.

## Intent
Work a spec or its job leaves for later becomes a row in one ledger, `.jig/ledgers/later.md`,
beside the deferred ledger. It is no longer a `Later:` line on the spec, so a spec is never updated
once its job starts. The gate, the rig and the roadmap's drop guard read the ledger. A command adds
a row to it or to the deferred ledger, and retro walks it. The deferred ledger keeps working as it
does today.

The owner's words, 2026-11-24:
- "I was okay with having two ledgers, one for deferred and one for later. I'm just arguing for a later leger rather than a later entry on specs. That's as many homes as there are specs, vs having one home in a dedicated ledger."
- "I should've been more precise: the roadmap does not carry later. Later gets a ledger."
- On Claude's description of the ledger: "Agreed."

## Done when
- [ ] `plugin/templates/ledgers/later.md` has a header row of six columns: `| Date | Job | Spec | Left | Roadmap id | Reason |`.
- [ ] `jig ledger later <id> --left "<what>" --reason "<why>" --spec <spec> [--job <job>]` appends a row. It creates the ledger from the template when the ledger is missing, and writes `—` for an absent job. It refuses an id that trunk's roadmap lacks, checked as `Scope:` ids are, against the metarepo's live trunk in a pararepo (smoke).
- [ ] `jig ledger deferred --job <job> --finding "<f>" --rank <r> --disposition <d> --reason "<why> [seen|assumed]"` appends a deferred row in that ledger's columns (smoke).
- [ ] A commit adding a later row whose roadmap id trunk's roadmap lacks is refused (smoke).
- [ ] A roadmap change that drops an id a later row names is refused. The refusal names the row and says to close it first. A spec's `Later:` no longer counts for the drop guard (`scope_holders`) (smoke).
- [ ] A spec that carries a `Later:` line is refused at commit. The refusal names `jig ledger later` (smoke).
- [ ] `jig gate` prints, under "Closes with the spec at merge:", the later rows naming the job or its spec, then the spec's `## Out of scope` lines as today (smoke).
- [ ] `jig rig` lists each later row whose id no spec takes yet and that isn't done, under Left for later and in `--json` `later`. A row whose id a spec has taken is no longer listed (smoke).
- [ ] The merge no longer carries `Later:` onto the handoff note (`close_specs`). Move-in re-points later rows' ids where it re-pointed `Later:` lines (smoke: `sec_close`, `sec_movein`, `sec_move`).
- [ ] The spec template has no `Later:` comment. `/jig:spec` step 3 says that work the spec leaves for later is a later row written with the spec. `/jig:work` says that at handoff, what the job's spec named and the job didn't build is a later row. `/jig:review` (L50) makes it a blocking finding when such work appears in Out of scope with no later row.
- [ ] `/jig:retro` walks the later ledger after the deferred ledger and before `## No phase`. It removes rows whose roadmap id is done. For a row nothing has taken in a long time, it asks the user whether to place its id in a phase or drop both row and id.
- [ ] Rules, skills, templates and docs name the later ledger and no `Later:` line. A grep of `plugin` and `docs` for `Later:` finds only the refusal text and its rule.
- [ ] `.jig/decisions.md` `## Unreleased` has Added and Changed lines, with a `**Breaking:**` line for a spec carrying `Later:`.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched.

## Out of scope
- The deferred ledger's purpose, rows and rules. It still holds review findings not taken at
  handoff, and the owner left it as it is (2026-11-24). Only the command that adds its rows is new.
- Lowercasing the other ledgers' file names: layout-rules-templates-names. This part names the new
  ledger in lowercase from the start.
- Converting existing `Later:` lines. The owner, 2026-11-24: "since "later:" isn't rolled out into
  a single repo yet". No repo's specs or notes carry one (this repo's don't), so nothing converts.

## Touches
- `plugin/templates/jig/jig.py`:
  - `spec_laters` and `laters_in` L11313-11320, `cited` L11324.
  - `close_specs` L11454-11500 (the `Later:` carry, L11472-11475 and L11497-11500).
  - `closes_with` L3577 (from `cmd_gate` L3395).
  - `left_for_later` L17365 and rig state L17353.
  - `scope_holders` L13228-13237 and the warning at L13386.
  - `roadmap_rules` L13382-13428.
  - The constants beside `DEFERRED` (L39).
  - `deferred_deleted` L2476, which also covers later rows.
  - `move_in_takers` L17720, `cmd_move_in` L17922-17937, `roadmap_takers` L18086.
  - The roadmap seed comment.
  - A new `ledger` subcommand in argparse.
- `plugin/templates/ledgers/later.md` (new)
- `plugin/templates/specs/_template.md` (L6, L19)
- `plugin/templates/jig/RULES.md`: L643, L680, L875, L878, L953, L1078-1084, L1184, L1192, L1201, L1708, L1995
- `plugin/templates/AGENTS.md` (the deferred line, plus a later line)
- `plugin/skills/spec/SKILL.md` (L38-39), `plugin/skills/bug/SKILL.md` (L64), `plugin/skills/rig/SKILL.md` (L79), `plugin/skills/review/SKILL.md` (L50), `plugin/skills/hubnode/SKILL.md` (L235, L237, L337), `plugin/skills/work/SKILL.md` (handoff, L82-84), `plugin/skills/retro/SKILL.md` (L14-28)
- `tests/smoke.sh`
- `docs/records.md` (L88-91), `docs/commands.md`, `docs/jobs.md`
- `.jig/decisions.md`

## Alternatives considered
- Keep `Later:` on the spec. Rejected by the owner: a spec is an artifact of how its job started,
  and one ledger is one home instead of as many as there are specs. [seen]
- Put later on the roadmap. Rejected by the owner: "the roadmap does not carry later". [seen]

## Decisions
- Interpreted: the request is built as five jobs, one per part, in the order layout-docmap, layout-roadmap-json, layout-later-ledger, layout-glossary-form, layout-rules-templates-names. Each part changes a different system, so each review stays small, and the order is real (parts 2 to 4 build on part 2's products list and ids, and part 5 splits and templates what 2 to 4 rewrite). The alternative is one job carrying all five specs, which the owner leaned to on 2026-11-23 ("Recommend building 2,3,4 with 1 then") before he said "your call". He hasn't answered this yet (the owner was away when it was written). Keeping them apart needs `Kept separate` lines on his word.
- Interpreted: jig still refuses a roadmap change that drops an id a row names, as it does for a spec's `Later:` today (the stager's reading).
- Interpreted: every later row names a roadmap id already on trunk's roadmap. Claude put that to the owner with the description, and the owner answered "Agreed".
- Interpreted: the command is `jig ledger <later|deferred>`, one subcommand for the "command adds a row to either ledger" the owner agreed to. The workarounds ledger keeps its R7 path.
- Interpreted: a row is written in two places. The spec role writes it with the spec, with job `—`, and the hubnode commits it with the spec on trunk. The work role writes it at handoff, naming its job. A row is never edited. Retro removes a closed row, and git keeps it.
- Interpreted: retro's stop goes after the deferred ledger and before `## No phase` ("Add it wherever it makes sense in context"). Its rows point at roadmap ids, the next stop's subject.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
