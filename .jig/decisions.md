# Decisions and changes

This log follows Keep a Changelog (https://keepachangelog.com/en/1.1.0/) plus decision entries, and versions are MILESTONE.FEATURE.PATCH, set by how much the product changed (`.jig/RULES.md`, Versioning).
A breaking change is one that a reader taking the release must act on: a `**Breaking:**` line says what to change, and it doesn't set the version's level.

## Open

## Unreleased

### Changed
- The glossary's one form opens with a `# Glossary` title, holding no term and no field line, above `# Basic terms`, every other heading at its level as before. The hook refuses a commit adding a first `#` heading that isn't `Glossary`, a `#` heading after the title that isn't `Basic terms`, or a heading or field line under the title; `jig init` and `jig update --glossary` write the title (the move leaves it to a later update while trunk's checker is older than it), and `jig glossary add` and the merge's re-sort keep it first. `jig update --apply` adds it to a glossary whose first heading is `# Basic terms`, on a second run once the update installing this checker is committed (a metarepo's is a job's). A glossary without it stays editable until then: the hook refuses only problems a commit adds.

### Fixed
- A spec named with dots matches itself by its bare name: a `Kept separate from` or `Build after` line naming `app-1.2-fixes` now means that spec, in `jig open`, `jig consolidate` and rig, as its path and file name already did.

## v0.17.0 - 2026-11-26

### Added
- `jig docmap <page or path>…` queries the docs tree's map: a page's globs and whether it is a board or an approved deep subsystem, or the pages covering a file.
- `jig roadmap --json [filters] [--id <id>…]` prints only the roadmap records asked for, each with its key and derived state: an agent asks jig rather than reading the file.
- `jig roadmap show [filters] [--width N]` prints the roadmap as a text chart with no dates: a box per phase as wide as its scopes, each scope in the column one past what it waits on, a box per product where there is more than one, each product's No phase items last, and one band per phase past 100 columns. The agent instructions template's Commands carry a `roadmap:` line for it, and `jig update --apply` adds that line where it is missing.
- A `jig update --apply` step deleting a `Later:` line from each spec on trunk, naming the spec and the ids it named.
- `jig glossary "<term>"` prints a term's heading path, definition, fields and controlling repo, and `jig glossary add` writes a term (`--under <product>[/<feature>]`, `--binds`) or a product (`--repo`, `--kind`) in its sorted place. `jig decision --page <page>` prints each decision whose `Touches:` names the page or a term on it.
- `.jig/templates/` holds every record's template, written by `jig init` and refreshed by `jig update --apply` from jig's own copy: a page, a spec, a handoff note, the process page, a hardware page, a skill, the deferred and workarounds ledgers (and the buffer in a pararepo), a glossary term and product, and the roadmap's phase, scope and no-phase item as JSON examples, built from the one example record the commit check compares with.
- `jig survey` reports each ruleset in `.jig/rules/` over 200 lines, refusing none.

### Changed
- The docs tree's map has its own file, `.jig/docmap.json`: `docmap`, `boards`, `deep_subsystems` and `not_docs` move there from `.jig/config.json`, which keeps only configuration. It is trunk-only like the board (R5), and the hook refuses a key jig doesn't know or a value of another shape. `jig init` writes it, and `jig update --apply` moves the four keys with their values unchanged.
- **Breaking:** a repo's own tool or script that reads `docmap`, `boards`, `deep_subsystems` or `not_docs` from `.jig/config.json` reads `.jig/docmap.json` instead, or runs `jig docmap`.
- The roadmap is a JSON file, `roadmap.json` in jig's folder: `products` (the glossary's product terms it includes), `phases` (each `product` where it has one, `name`, `note`, `exit` checks, `after`, `needed_by`, `scopes`) and `no_phase` items (a scope's fields plus `product`, `stopped_at`, `parked`). States and blocked stay derived, and a phase's type is still read from its name. The hook refuses a field or a type the records don't have, and a product `products` doesn't include or the glossary doesn't hold, and runs every check it ran on the Markdown roadmap. `jig roadmap --draft` writes a JSON draft, and `--edit` checks and writes it. `jig init` writes the empty roadmap, and `jig update --apply` converts the Markdown roadmap, every phase, scope, item, suffix, note and exit check with its text unchanged, once trunk's checker reads JSON; it is judged by its output, drawn in the old form again, and every line that doesn't come back where it was (prose above the first heading or among the boxes, a fence outside a note, a line the old checks refuse), or that the hook would refuse, is listed, and the conversion waits until it is moved, fixed or deleted. A text in the JSON is prose wherever it ends.
- **Breaking:** the Markdown roadmap is gone: edit the roadmap with `jig roadmap --draft` and `--edit`, and read it with `jig roadmap` or `jig roadmap show`. A tool reading `ROADMAP.md` reads `jig roadmap show` instead.
- A spec takes only what it builds. Work it doesn't build stays on the roadmap, unspecced; a spec building only part of a scope waits on a roadmap change, on the owner's yes, that splits it, the built part a new scope the spec takes and the rest under the original id, its text unchanged. `## Out of scope` never defers: work worth building later goes onto the roadmap as a scope or No phase item, and review blocks a deferral written as prose.
- **Breaking:** the hook refuses a spec carrying a `Later:` line in its header. `jig update --apply` deletes the line from each spec on trunk and names it; each id it named is already on the roadmap. Handoff notes keep theirs, as history nothing reads.
- The glossary takes one form: `# Basic terms`, then a product per `#` heading with `Repo:` (the repo that builds it, or `none`) and `Kind:` (`software` or `hardware`), a feature per `##`, a term per `###`, a term in a metarepo's glossary perhaps carrying `Binds:`. A term's controlling repo is its product's `Repo:`. The hook refuses a commit adding a form problem, `jig merge` re-sorts the glossary in the merge commit, `jig init` seeds it with `Basic terms` and the repo's software product, and `jig move-in` writes the moved product's `Repo:` and `Kind:`.
- **Breaking:** a glossary's table rows are no longer terms: a label, a `§` pointer or a Touches term naming one is refused until it is a heading. `Owner:` lines aren't read: `jig update --apply` rewrites each as `Repo:` and `Kind: software` (two products naming one repo get `Repo:` and no `Kind:`, for the owner to mark), and reports a glossary out of the form for the owner to rebuild.
- The rigger, the chat session that designs a product outside its repo, is the designer: `/jig:designer` and `jig designer <repo>`, and `rules-inbox.md` § Designers. `/jig:rig` and `jig rig` are unchanged.
- **Breaking:** `/jig:rigger` and `jig rigger` are gone: run `/jig:designer` and `jig designer <repo>`. The per-machine repos list's `rigger` key is read as `designer`, and the next save writes it as `designer`: a tool reading the key reads `designer`.
- The ledgers are `.jig/ledgers/deferred.md`, `workarounds.md` and `buffer.md`; `/jig:spec` copies `.jig/templates/spec.md`, and the page template is `.jig/templates/page.md`.
- **Breaking:** the ledgers' capital names and `.jig/docs-page.md` are gone. `jig update --apply` renames each ledger with `git mv`, rewrites the deferred ledger's header cell `Lane / handoff` as `Job / handoff` (no row changes) and the agent instructions' lines citing a ledger's old name, and moves the page template. A tool citing the old names reads the new ones. A spec template of the repo's own stays where it is, named by update when it differs from jig's.
- The rulebook is a folder of rulesets, `.jig/rules/rules-<ruleset>.md`: jobs, docs, handoff, workflow, roadmap, decisions, staging, release, inbox, and `rules-metarepo.md` or `rules-pararepo.md` only in a metarepo or a pararepo. Each skill and `jig open`'s kickoff name the rulesets they read.
- **Breaking:** `.jig/RULES.md` is gone: `jig update --apply` removes it and writes `.jig/rules/`, removing a ruleset of a kind the repo no longer is. A citation of `.jig/RULES.md (<section>)` cites the ruleset holding the section now. The rulebook's command list is gone: `jig -h` and each command's `-h` say it.

### Removed
- `docmap`, `boards`, `deep_subsystems` and `not_docs` as `.jig/config.json` keys: the hook refuses a config commit adding one.
- `ROADMAP.md`, the generated view, with `jig roadmap --view` and `--write`: no command writes it, and `jig update --apply` removes one jig generated. A repo's own `ROADMAP.md` is left alone.
- `Later:` on specs: the gate's later lines under "Closes with the spec at merge:" (it keeps the spec's `## Out of scope` lines), the merge carrying the line to the note, and rig's Left for later with its `--json` `later` key.
- `Owner:` on glossary terms, and `this repo` as its value: a product's `Repo:` names its repo.
- `.jig/RULES.md`, and its command list: `.jig/rules/` holds the rules, and `jig -h` lists the commands.
- `jig rigger` and `/jig:rigger`: `jig designer` and `/jig:designer`.
- `.jig/docs-page.md`: the page template is `.jig/templates/page.md`.
- The ledgers' capital names `DEFERRED.md`, `WORKAROUNDS.md` and `BUFFER.md`: `deferred.md`, `workarounds.md`, `buffer.md`.

## v0.16.0 - 2026-11-24

### Added
- A spec names the work it leaves for later on a `Later:` line of roadmap ids, beside `Scope:`, each already on trunk's roadmap: the hook checks them as it checks `Scope:` ids, the drop guard included. `jig gate` prints `Closes with the spec at merge:` with the spec's `Later:` ids and `## Out of scope` lines, the merge keeps the `Later:` line on the note, and `jig rig` lists each id still open under Left for later (`later` in `--json`). Work left for later in an `## Out of scope` line, with no `Later:` id, is a blocking review finding.

### Changed
- Every stand-alone repo and metarepo keeps a roadmap, its empty structure if nothing else: `jig init` writes the roadmap and its view, `ROADMAP.md`, `jig update --apply` adds them where missing, and `jig roadmap`, rig, reading-list, survey, staging, the gate and the merge commit them on trunk in the trunk checkout when trunk has none (elsewhere they say where it is written). On trunk the hook refuses a commit removing it, and with none on trunk refuses a spec's `Scope:` or `Later:` line. A repo whose root `ROADMAP.md` is its own gets none until that content moves into the roadmap. A pararepo keeps none: `jig init --para` removes the empty structure a plain init wrote, and `jig update --apply --sweep` there refuses, naming the metarepo's glossary `Owner:` term and `jig move-in`, unless the pararepo keeps a roadmap of its own.

### Fixed
- A gate's check counts only for the commit the job's newest handoff note names: a gate checkout built from an older note is stale, so `jig next` says gate, `jig checked` there and `jig mark <job> gated` refuse it naming `jig gate <job>`, and `jig handoff` refuses while trunk's board has the job gated until the hubnode marks it ready.
- In a metarepo, `jig update --apply --merge-log` drops from `.jig/meta.json`'s `entry_files` any path it removes, a record folder's index included, with the log in its place, whether or not a register or a changelog merges in the same run. A glob item stays as written.

## v0.15.0 - 2026-11-19

### Added
- `jig queue -- <command>` runs a test or check holding one of the machine's slots (OS file locks in `.git/jig/queue/`, freed when a run dies), and waits when none is free; `jig queue` lists who holds and who waits. `queue.width` (the cores one run uses, or `"all"`), `queue.slots` and `queue.max_load` in `.jig/config.json` set it. The work, review and check roles run their tests and checks through it. A repo whose suite uses every core sets `queue.width: "all"`.
- `jig queue --full` is the complete check's: it also takes a single full lock, so two complete checks never run at once.
- `queue.overflow: {"to": "github", "reason": "<the owner's words>"}` is the owner's standing yes for the check role to push and delete `jig-check/*` branches, the one exception to "the owner's word before a push". With it, a complete check that finds the machine full exits 3 and prints the route to GitHub Actions; copy `plugin/templates/github/jig-check.yml` to `.github/workflows/` in the same commit. `jig checked --ci <run url>` records such a run only after `gh` shows it passed on HEAD.

### Fixed
- In a metarepo, a commit on a `propose/` branch passes R2 while jobs are open, as it does when none are: a proposal is on no job by design. A `propose/` branch in any other repo is refused as before, and R1 still keeps the trunk checkout off it.
- `jig roles --from TIER,EFFORT` takes the starting session's own settings and says under each role whether to start it with its settings or start it and then raise its model, its effort or both, compared one at a time as the tool clamps them; it also says when those settings rank below the hubnode floor. Settings rank by tier first, then effort. The hubnode runs it at the start of a session and follows it when starting a role.
- `tiers.json` names the tier-1 model in use today.
- A metarepo gets a generated block of its rules in its always-loaded agent instructions, as a pararepo gets its header: `jig init --meta` writes it, and `jig update` lists it when it is missing or older. A metarepo set up before this writes it in a job, with `jig init --meta` in the job's worktree, and removes the lines it wrote by hand for those rules, which update lists as the repo's procedure.

### Changed
- Pages describe the product only: how the repository is worked has its homes, by one test in `.jig/RULES.md` (Homes), and the rest of it goes to `.jig/process.md`, created on first use with a pointer line in the always-loaded rules file naming when to read which section (a repo already on jig adds that line itself; only jig's template has it). `jig survey` and `jig update` now list a page line naming a `.jig/` path other than the decision log, and an invariant whose holder names review: move each line to its home, and for what review covers give the invariant a named test or what is seen on screen, or move it to the body.

## v0.14.0 - 2026-11-16
