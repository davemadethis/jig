# layout-rules-templates-names: a rules folder, a templates folder, lowercase names, "the user"

Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."

Part 5 of 5, built last. Parts 2 to 4 delete much of the rules text this part splits, and
its templates folder holds their records.

## Intent
Four changes:
- The rulebook becomes `.jig/rules/rules-<ruleset>.md`, one file per thing it governs. Each role reads only the rulesets it names. A metarepo's or pararepo's ruleset is installed only in such a repo. A file over 200 lines is reported.
- Each repo gets `.jig/templates/`, with a template for every record jig keeps. New JSON records are checked against theirs.
- Every file name under `.jig/` is lowercase.
- What jig ships says "the user", and a per-machine username is written wherever jig records who said or approved something.

The owner's words:
- 2026-11-22: "What do you think about creating a /rules folder with rules-<ruleset>.md as the naming convention where each <ruleset> is named for what it governs, and setting a cap for the line-count or file-size of each document?"
- 2026-11-23: "200 reported and not refused."
- 2026-11-21: "meta repo and pararepo rules should never be added to rules in regular repos, and meta rules only belong in a meta repo and para in a para."
- 2026-11-22: "We should have templates for basically everything, in a templates folder."
- 2026-11-22: "all repos should get all templates that apply to them (regular, para, meta)"
- 2026-11-21: "Lowercase for everything in jig"
- 2026-11-22: "We'll just have jig store a username so it stops inventing multiple references like owner and Dave, and mine will be davemadethis"
- 2026-11-22: "I'd make it per machine since repos could be managed by multiple users and that's a scenario where you'd want to have distinct names."

## Done when
Rules:
- [ ] `plugin/templates/jig/rules/` holds `rules-jobs.md`, `rules-docs.md`, `rules-handoff.md`, `rules-workflow.md`, `rules-roadmap.md`, `rules-decisions.md`, `rules-staging.md`, `rules-release.md`, `rules-inbox.md`, `rules-metarepo.md` and `rules-pararepo.md`. `plugin/templates/jig/RULES.md` is gone.
- [ ] Every rule RULES.md held is in exactly one file, apart from what the split drops. It drops the `## Commands` section (L1975-2036), which `jig -h` says, and text that only restates a hook's refusal. The handoff note lists each dropped passage and what says it instead.
- [ ] `jig init` and `jig update --apply` write `rules-metarepo.md` only in a metarepo, `rules-pararepo.md` only in a pararepo, and the other files in every repo. Update removes `.jig/RULES.md` and refreshes the folder as it refreshes `jig.py`. A file left from a kind the repo no longer is gets removed (smoke).
- [ ] `jig survey` reports each `.jig/rules/` file over 200 lines and refuses nothing. On a fresh repo it reports only `rules-decisions.md`, which this request leaves alone, and any other file still over the cap after its refine pass. The handoff note names each one (smoke).
- [ ] Each role's and node's skill names the rulesets it reads, in place of "Read `.jig/RULES.md` first": hubnode, subnode, rig, spec, bug, work, review and check. `jig open`'s kickoff (L1301) does the same.
- [ ] Every citation of `RULES.md` points at the file now holding the section: jig.py's messages (about 68), skills (about 61), templates, `docs/` and the AGENTS.md template. `grep -rn 'RULES.md' plugin docs` finds only update's step that removes it.

Templates:
- [ ] `plugin/templates/` holds one template for each of these, and `jig init` and `jig update --apply` write each that applies to the repo kind into `.jig/templates/`:
      - a page;
      - a spec;
      - a handoff note;
      - the process page;
      - a hardware page;
      - a skill;
      - each ledger (deferred, workarounds, later, and buffer in a pararepo);
      - a glossary entry;
      - a roadmap phase, a roadmap scope and a no-phase item;
      - a products-list entry.

      A prose record's template is a skeleton. A JSON record's template is an example record. `.jig/docs-page.md` moves to `.jig/templates/page.md` (smoke).
- [ ] The fields of each JSON record (phase, scope, no-phase item, products entry) come from one example record in `jig.py`. Update writes it as the template, and the commit check compares new records with it. A field it doesn't have is refused, as is a field of another type (smoke).
- [ ] `/jig:spec` copies `.jig/templates/spec.md`. A repo's own `.jig/specs/_template.md` that differs from jig's is reported by update and left in place.

Names:
- [ ] The ledgers are `.jig/ledgers/deferred.md`, `workarounds.md` and `buffer.md`, and the templates are renamed to match. `jig update --apply` renames each with `git mv`. It re-points the lines jig wrote that cite them, in AGENTS.md and in jig's own files. In the deferred ledger it rewrites the header cell `Lane / handoff` to `Job / handoff` and changes no row (smoke).
- [ ] `find plugin/templates/jig plugin/templates/ledgers -name '*[A-Z]*'` finds nothing. No path jig writes under `.jig/` has a capital.

"The user":
- [ ] Skills, rules, templates and jig.py's messages and comments say "the user" where they said "the owner": 247, 87, 3 and 119 today. `owns`, `owner_*` identifiers and job ownership stay. Remaining counts are `grep -rni 'the owner' plugin` → 0. The rules' `Accepted (Dave, …)` example (L1238) and the docstring at jig.py L6116 use a generic name.
- [ ] `jig user [<name>]` prints or sets the username in `user.json`, beside the repos list (`repos_file()`'s folder). When it is unset, jig takes the GitHub login from `gh api user --jq .login`, or else from `git config github.user`, or leaves it unset and says how to set it (smoke, with `JIG_CONFIG`/`XDG_CONFIG_HOME` set).
- [ ] The SessionStart hook prints `jig: the user is <name>`, or how to set one. `jig status` prints the same (smoke for `status`).
- [ ] Where jig or a skill writes down who said or approved something, it writes the username:
      - a staged file's quotes;
      - a `Kept separate` line;
      - a decision entry's `Accepted (<who>, <date>)`;
      - a BUFFER row's decider;
      - `queue.overflow`'s reason.

Every part:
- [ ] `.jig/decisions.md` `## Unreleased` has Changed lines, with `**Breaking:**` lines for repos citing `.jig/RULES.md` or the old ledger names in their own files.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and so do the smoke sections touched, which is most of them, given the renames.

## Out of scope
- Renaming "the owner" or "Dave" in any repo's own pages, code or records. The owner, 2026-11-22:
  "put the new convention in jig but leave rename out entirely. I'll run it as a job afterwards in
  the repos that need it." That includes this repo's root AGENTS.md and its own `.jig/`.
- Cutting `rules-decisions.md` under the cap. The decision log is left as it is (2026-11-24).
- An `@` before the username. The owner dropped it, since GitHub treats `@name` as a mention.
- A `questions` record. It came from the direction set aside under "Not in this request".
- Maige-OS's pre-jig deferred ledger layout. That is its own work: update rewrites only the
  header cell.

## Touches
- `plugin/templates/jig/RULES.md` → `plugin/templates/jig/rules/rules-*.md`
- `plugin/templates/jig/docs-page.md` → `plugin/templates/templates/page.md`, beside new templates for the handoff note, glossary entry, phase, scope, no-phase item and products entry. The folder name is the work role's to settle.
- `plugin/templates/ledgers/DEFERRED.md`, `WORKAROUNDS.md`, `BUFFER.md` → lowercase
- `plugin/templates/specs/_template.md`, `plugin/templates/process.md`, `plugin/templates/hardware.md`, `plugin/templates/skills/_template/SKILL.md`, `plugin/templates/AGENTS.md`
- `plugin/templates/jig/jig.py`:
  - RULES.md as a path: `cmd_reading_list` L3275, `RETIRED_RULES` L4119, `doc_homes` L4139, L5048, the survey presence check L5275, `LAYOUT` L13446, `TOOL_FILES` L13461, the `.gitignore` text L13504/13522, `RETIRED_LINES` and the AGENTS.md checks L14456-14471 and L14688-14702, update's `sources` L15081, L16199.
  - RULES.md cited in messages: about 68 sites.
  - The kickoff, L1301.
  - Ledger names: `WORKAROUNDS` L36, `DEFERRED` L39, `BUFFER` L7999, `BUFFER_HEAD` L12520, `BUFFER_SEED` L17564.
  - Survey's size check: `cmd_survey` L5260-5370.
  - `repos_file` L8098 and a `user` subcommand.
  - Every "the owner" string.
- `plugin/scripts/session-start.sh`
- Every `plugin/skills/*/SKILL.md`: the rulesets each reads, and "the user"
- `tests/smoke.sh`
- `README.md`, `docs/records.md`, `docs/commands.md`, `docs/hooks.md`, `docs/jobs.md`, `docs/workflows.md`, `docs/metarepos.md`
- `.jig/decisions.md`
- Process homes (RULES.md, Homes): the rules files are the rulebook's own home. Which ruleset a role reads is the role's skill.

## Alternatives considered
- A hard cap that refuses. Rejected by the owner: "200 reported and not refused". The owner, 2026-11-22: "The quality of a doc in that regard is the ideal measure, not it's size". [seen]
- Keep one RULES.md and mark the metarepo and pararepo sections conditional. Rejected: the owner wants those rules absent from regular repos. [seen]
- Read the JSON field list from the repo's `.jig/templates/`. Rejected: a repo could then widen its own fields, which is the hand-made field the owner ruled out. One example in `jig.py` is the source, and the template is its copy. [assumed]

## Decisions
- Interpreted: the request is built as five jobs, one per part, in the order layout-docmap, layout-roadmap-json, layout-later-ledger, layout-glossary-form, layout-rules-templates-names. Each part changes a different system, so each review stays small, and the order is real (parts 2 to 4 build on part 2's products list and ids, and part 5 splits and templates what 2 to 4 rewrite). The alternative is one job carrying all five specs, which the owner leaned to on 2026-11-23 ("Recommend building 2,3,4 with 1 then") before he said "your call". He hasn't answered this yet (the owner was away when it was written). Keeping them apart needs `Kept separate` lines on his word.
- Interpreted: a file over the cap gets a refine pass. It is split only if it governs two things (the stager's reading, from the owner's line on quality over size).
- Interpreted: the rulesets are jobs, docs, handoff, workflow, roadmap, decisions, staging, release and inbox, plus metarepo or pararepo where the repo is one. Each role's skill names the rulesets it reads (the stager's reading).

  Today's sections map as follows:

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
  | Metarepo and pararepos | metarepo, pararepo, split by which repo each rule binds |

  A rule both kinds need goes in each, worded for that side.
- Interpreted: the split also drops what the tool already says, the command list and text that only restates a hook's refusal (the stager's reading).
- Interpreted: `rules-decisions` starts over the cap and is reported, not cut (the stager's reading).
- Interpreted: one folder per repo, `.jig/templates/`, with the list above. A prose record's template is a skeleton, and a JSON record's is an example record that new ones are checked against (the stager's reading). Templates are jig's files, refreshed by update like `jig.py`.
- Interpreted: `jig update` renames the ledgers and re-points what cites them (the stager's reading). "What cites them" means the lines jig wrote, not a repo's own pages ("no migration of any repo's pages").
- Interpreted: renaming a ledger also rewrites the one header cell, `Lane / handoff` → `Job / handoff`, and no row (the stager's reading).
- Interpreted: "the user" goes in the rules, skills, templates and the tool's messages. The stored username goes wherever jig writes down who said or approved something (the stager's reading). jig.py's comments change too, so one grep shows one term.
- Interpreted: the username defaults to the installer's GitHub username, is stored beside the repos list, and is printed at session start so no agent guesses it (the stager's reading). It is found through `gh`, then `git config github.user`, since jig is stdlib and has no network call of its own.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
