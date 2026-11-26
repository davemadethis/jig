# Documentation rules

## Documentation

One page per system, `docs/<system>.md`. A subsystem's page sits in its system's folder,
`docs/<system>/<subsystem>.md`. A page is a single file, flat in its parent's folder, until it
holds more than itself — subsystem pages, files it links, a `datasheets/` folder; then it moves
into a folder named for it, `docs/<system>/<system>.md`, with that company beside it, in the
change that adds the first of them. Both forms are one page, and that is about naming only: a
`docmap` key or `boards` entry written in either names it in either, so a branch grows the
folder with a `git mv` alone, and the key on trunk may be rewritten later or never. A key that
names a page in the wrong form doesn't make that form right: the page still moves. The tree names the product's systems, not its files, so a rule that touches several
files lives once.

In a folder that has a page, another `.md` is a flat page when `docmap` or `boards` names it, or it
has an Invariants section (or a retired `## Undefined`); anything else there is one of the folder page's files.

A **subsystem** is a system inside a system: it works independently of the rest of it. It has files
of its own, which the rest of its system doesn't edit, and the rest of the system reaches it
only through the interfaces between them. A car's cooling system is separate from its
suspension and its drivetrain, even where they touch. A section with no files of its own stays
a section, however long it gets.

The tree is two levels deep: systems and their subsystems. A subsystem inside a subsystem needs
the owner's word. It is proposed with a rationale: what it is independent of, and the files it
has of its own. On a yes, it is recorded on trunk in `docmap.json`'s `deep_subsystems`, a map
from its folder to that rationale: `{"docs/power/battery/cells": "own firmware module and test
rig; independent of pack thermal"}`. An entry with an empty rationale doesn't count, and each
deeper level needs an entry of its own. `jig survey` lists any other deeper page to fold into
its subsystem's page or to propose.

`jig survey` works out each page's level from evidence, never its path: the files it owns
(its docmap globs' files that no page but those above it covers), the repo's structure maps
and manifests, and with `--levels` its imports. A page below a system whose docmap globs cover no file
is a section of the page above it; one whose every file another page covers is that page's
subsystem, or a seam; each folds on the owner's yes. A fold joins sections of one name into one
— the folded page's Invariants entries under the receiving page's Invariants, its Talks to
under its Talks to — since a page holds each heading once. It also lists the repo's own files that
still hold the old page shape — a check of the Now / Rules / Checks headings, a counter over
numbered page headings, an always-loaded line that makes page rules bind or cites a page by
number — and the files that declare the docs structure beside the docmap. Those convert with
the pages; jig never edits them, except a counter that matches no line with no
`/jig:redocument` run under way: it numbers nothing, and `jig update --apply` removes it from
the board, which is jig's.

A page describes what is built: what is true of its system on trunk today, in present-tense
prose. It is not a rulebook; this file holds the rules about documentation, and no page
restates them.

**Product and project.** A page and a decision entry are about the product: what it is and how
it behaves today. Priorities, phases, ordering, delivery queues, build status and "not built
yet, phase n" are the project, and live in `.jig/roadmap.json` only (`rules-roadmap.md`, Roadmap). A spec is where
the two meet: it takes project items and turns them into product, as code, pages and decisions.
A page may say what the product doesn't do today ("Changing the PIN isn't supported"); it never
says when, or in what order, that will change. References run one way: a spec, a handoff or
the roadmap cites pages and decisions freely, and a page or a decision entry never names
`.jig/specs/`, `.jig/handoffs/`, `.jig/roadmap.json`, or a phase or scope, built or not. The
hook refuses an added line in a page under `docs/`, in `.jig/decisions.md` or in a metarepo's
entry file that names `.jig/specs/`, `.jig/handoffs/` or `.jig/roadmap.json`, or a
scope id the roadmap has in code quotes (`` `alpha/screen` ``), and names the line; a moved
page's old lines, or a line moved within a file, aren't new. What can be product text too, it can't judge: `ROADMAP.md`, a
bare scope id ("the v1/api endpoint"), a phase name, prose like "phase 3" or "spec step 6", a
`## Status` heading. Nothing searches for those, at commit or after: words like these are often
the product's own (a status call, a three-phase motor, a launch configuration), so whoever
writes the line judges it, and the spec, fold-in and review ask. The hook also refuses a
`roadmap.md` or `roadmap.json` under `docs/` or matching a metarepo's `entry_files`: the roadmap
is `.jig/roadmap.json`.

**Product and process.** A page describes the product, never how the repository is worked: the
order a builder reads in, the commands that build, test and check it, its code style, its review
and handoff, jig and its files under `.jig/`, and the steps of its build, CI and release. Each
has its own home, by the test under Homes: `AGENTS.md` for rules every task needs and the
commands, `jig reading-list` for what to read, `.jig/scripts/` for steps a script runs, a skill
for a procedure an agent runs, CI's own files for CI, and `.jig/process.md` for the rest, code
style included. What the product does with the same things is the product's: a page describes
an app that runs a user's tests, a CI service, an app that reads a user's instruction files, or
a tool whose product is jig. A board page's Toolchain and Flash / rollback belong to the board.
Whoever writes the line judges it, and the spec and review ask. `jig survey` and `jig update`
list a page line that names a path under `.jig/` other than `.jig/decisions.md`, outside fenced
code and HTML comments; the hook refuses nothing for it, since a product that reads jig's files
names them too. It searches no words ("jig", "CI", a test runner's name): each may be the
product's.

**Docs point only at docs.** The root documents (`README.md`, `AGENTS.md`, `CLAUDE.md`,
`GEMINI.md`, `CHANGELOG.md`) are for outsiders and for agents: they may point into `docs/`, and
a page or a decision entry never names one. The hook refuses an added line in a page under
`docs/` or in `.jig/decisions.md` that names a root document as a path, with or without `§`
(`README.md § mote`, `../AGENTS.md`), and names the line; a file `not_docs` matches is exempt.
A Markdown link resolves from the page's folder, so a page's link to its own folder's
`README.md` is no root document; any other path is from the repo's root, as jig's pointers are.
Another repo's file (`<repo>/README.md`) and a code path are not root documents. Prose
that names one without a path ("listed in the root README") the hook can't judge; `jig survey`
lists those lines too.

Every page, in this order (`.jig/templates/page.md`, which `jig update` keeps
current, is the skeleton):

1. **A lead paragraph**, with no heading of its own: what the system is and why it exists.
2. **Body sections**, named for what its code has — its nouns (Schema,
   Renderer, Sync) — never for a lifecycle or a genre (Overview, Notes, Misc, Changes). A
   subsystem gets a page of its own, beside its system's, once it has something to say that
   whoever works on it needs and its system's page doesn't; the parent's section then shrinks
   to a paragraph and a link. Until then it is a section, its files in its system page's globs.
3. **`## Talks to`**, optional: what crosses the system's boundary, meaning what it calls, what
   calls it and what passes between them, each linked to its seam page or contract where one
   exists. Calls inside the system stay in the body.
4. **`## Invariants`**, optional: only the facts that are load-bearing. Each entry states,
   inline, why it must hold and what holds it — a named test, or what is seen on screen (on a
   board, on the board):
   `- Rows are at least 44px — the touch-target minimum; held by test_touch_targets.` An
   entry without a why and a holder is description, and goes in the body or nowhere. Review is
   no holder: no step reads a page's Invariants, so what only review would hold goes in the body.

A page has no `## Undefined` section, and no section that holds the project: build status
(done, pending, not built yet), or when and in what order work will happen. What the section
says decides, not its heading: a `## Status` or `## Current state` describing the product's own
thing (a status call, a state machine's states) is product. Work with no phase yet, parked
mid-build (naming the pages it will touch) or not started, is a No phase item (`no_phase`) in
`.jig/roadmap.json` (`rules-roadmap.md`, Roadmap), written only on the owner's word. An open
product question is an idea in `.jig/ideas.md`, which the page may cite. Review
findings not taken go in `.jig/ledgers/deferred.md`. `jig survey` lists a `## Undefined`
heading, jig's own retired one, with where its content goes; it searches no other heading,
since a heading's word alone says nothing. A page that still carries a project section works as
before until it is moved.

Trunk's code is reality. A page that disagrees with the code is a stale page, and gets fixed.
An invariant the code breaks is a finding the handoff surfaces for a person to rule on, never
an instruction to bend the code. Cite a page by its heading (`docs/ui/ui.md § Invariants`),
not by a number. A moved rule leaves no forwarding address behind — that is history, and
git keeps it.

A heading is its page's address, as a section number was, so a page holds each heading once,
at any level: two `### Errors` under different sections are renamed apart (`### Sync errors`).
The hook refuses a change that leaves a page under `docs/` with more copies of one heading than
it had, compared as `§` compares them: code and emphasis marks dropped, case kept. A
heading quoted in fenced code is an example, not an address, and isn't counted. A page that
already holds a duplicate isn't refused for it, wherever the change moved it from. A
`CHANGELOG.md` or `DECISIONS.md` there, a datasheet and a file `not_docs` matches are exempt.

In `docmap`, a subsystem's page names its own files and its system's page names the rest:
fold-in asks every page that covers a changed file, so a system page whose globs reach into
its subsystems is asked about every change made in them.

A **seam** page covers what crosses between two systems: in `docmap`, a page whose globs name
files from both sides. It lives, as a datasheet two pages share does, in the nearest folder both
systems sit under: `docs/<seam>.md` for two systems, flat, with no page above it. `jig reading-list <files>` prints which pages to read before touching
those files, and after each the pages above it in the docs tree, marked as its parent, since a
system's shared facts live on its own page. Fold-in still asks only the pages that cover a
changed file.

A page's folder holds the files the page links — a schematic, a snapshot of a definition, an
image — beside the page and its subsystems' pages. `jig survey` lists a file there that no
page links (a link from a note in the folder counts); a page named for its folder with nothing
else in it, flat at its parent's (`docs/a/b/b.md`: flat at `docs/a/b.md`); and a flat page
with a folder of its own name beside it, to move into. The hook refuses a change that puts a
page in the wrong one of its two forms — it adds or moves a page there, or adds a page's first
other file or removes its last without the move — and names the move, in survey's words. A page
already in the wrong form is survey's, and a change that leaves it there isn't refused. A flat
page's own file left loose in its parent's folder is that folder page's to survey, so review
catches it.

A board, a screen, a battery are parts of the product, so each is a system or subsystem like
any other: `docs/<board>.md`, or `docs/<system>/<board>.md` where the board is part of a larger
system, in a folder of its own once it holds files (a spec sheet makes a `datasheets/`), beside the code's pages, never under a genre folder. Every board has a
page the repo builds, made from jig's board template (`/jig:hardware`) out of a hardware
definition and checked against the code; a dev board gets one too, written from its vendor's
spec sheet. It is a board page because `docmap.json`'s `boards` lists it, never because of where
it sits. A `docmap` entry ties each page to the code that targets its board, so every handoff
that changes that code asks whether the page still matches. `jig gate` refuses:

- a branch that adds or changes a board-build file (`sdkconfig*`, `platformio.ini`,
  `idf_component.yml`, `west.yml`, `*.ino`, `*.overlay`) that no registered board page's
  `docmap` globs cover: write the board's page, list it in `boards`, map the file to it;
- a branch that deletes or moves a page `boards` lists;
- "no page needed" in the fold-in for a file a registered board page's `docmap` globs cover.

A repo with no board-build files has none of these. `jig survey` lists each board-build file
no registered board page covers, and a `boards` entry naming no page: the page may still be on
a job's branch, so the gate leaves that one to survey. Survey reads board pages against the page
contract like any page, and the gate doesn't refuse one off it.

A part whose behavior the code touches is a subsystem with its own page. A vendor's documents —
datasheets, a dev board's spec sheet, app notes, reference manuals — sit in a `datasheets/`
folder in the folder of the page that leans on them: a part documented only by its datasheet is
a file in its page's `datasheets/`, and a board's own spec sheet is in `docs/<board>/datasheets/`.
A file the repo wrote, its own schematic or a definition the owner wrote, sits in the page's
folder itself. A datasheet two pages use lives in the `datasheets/` of the nearest folder both
pages sit under: two subsystems of one system share the system's `datasheets/`, two systems
share `docs/datasheets/`. Both pages link it; it moves there when the second page starts using
it, and is never copied: `jig survey` names a page linking into the `datasheets/` of a page that
is neither its own nor above it, and the shared folder the file belongs in. `datasheets/` is a reserved name at any depth: it holds reference
files, is never a subsystem and never a page's home, and a note inside it is a reference file,
not a page. `jig survey` names a page called `datasheets` (rename its folder), and a
`datasheets/` folder that is neither in a page's folder nor at `docs/datasheets/`.

Each link to a datasheet carries its source URL, the date it was retrieved and the first 12 hex
digits of its sha256 (a board page's Components table, or the page's text), so a check names
the exact document it was made against; a board page's table also says whether each part is
verified on the board yet. Whether the binaries are committed is the repo's call,
`reference_files` in the config: `commit`, or `ignore`: `.gitignore` ignores the PDFs under any
`datasheets/` folder (`docs/**/datasheets/**/*.[pP][dD][fF]`), and the page keeps each one's
URL and hash to fetch it again. Notes stay committed, and so does every file the repo wrote.
`jig survey` reports a link from a page into a `datasheets/` folder that doesn't exist.

### Homes

`jig survey` checks each Markdown file the repo tracks against this list, outside tool folders
(`.jig/`, `.claude/`, `.github/`, …) and `not_docs`:

- `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` and `README.md` at the root, a `CHANGELOG.md` there
  until `jig update` merges it into `.jig/decisions.md` (`rules-decisions.md`, Decision log);
- under `docs/`, a page, flat or named for its folder: `docs/<system>.md` or
  `docs/<system>/<system>.md`, `docs/<system>/<subsystem>.md` or
  `docs/<system>/<subsystem>/<subsystem>.md`, and a deeper one only where `deep_subsystems`
  approves the folder it stands for (`docs/a/b/c` for `docs/a/b/c.md` and `docs/a/b/c/c.md`
  alike) and each level above it past the subsystem;
- any other file in a page's folder or below it, outside the folders of its subsystems;
- nothing under `docs/hardware/`, the layout before boards were systems: survey and update
  say where each of its files goes, and `/jig:redocument` moves them;
- anything under a `datasheets/` folder, inside a page's folder or at `docs/datasheets/`;
- in a metarepo, its decision registers, and its pages under a genre folder (`rules-metarepo.md`, A
  metarepo's docs tree), not the code repo's tree;
- a decision register (a `DECISIONS.md` with rows) or a folder of decision records, and every
  file in that folder, until `jig update --merge-log` merges it into `.jig/decisions.md`.

Any other file has no home, and survey says which kind: an `AGENTS.md`, `CLAUDE.md` or
`GEMINI.md` off root is a second rulebook; three or more sentences of this file word for word
is a copy, which freezes while this file moves on; a page, flat or in its folder, below a
subsystem, with no `deep_subsystems` entry, is deep: fold it into its subsystem's page, joining
sections of one name, or
propose its folder to the owner with its rationale; a page outside the tree — one with an
Invariants section or a retired Undefined one, the old Now, Rules and Checks headings, or any file `docmap`
names, whatever its format — goes flat beside
the nearest page that has a folder, as a subsystem at most (into that page, where it would be
deeper), or to `docs/<name>.md`, even when it quotes this file;
anything else is a stray. A package's own rules file stays only on the owner's word. A
file names a document by its path, or by its bare name only when no other tracked file has
that name.

Each kind of document has one home: rules in `AGENTS.md`, and the rules about documentation
here; what the code is now and its invariants in `docs/`; a task in flight in
`.jig/specs/`, removed once its job merges, its scopes kept on its handoff note; decisions that outlive their spec, and what a release changed, in
`.jig/decisions.md`; the phases, scopes and parked work ahead in `.jig/roadmap.json`; patches in the code in `.jig/ledgers/workarounds.md`; review findings not taken
in `.jig/ledgers/deferred.md`; a procedure an agent runs in a skill, and the rest of how the
repo is worked in `.jig/process.md`, never in `docs/`; what outsiders need in `README.md`;
history in git.

`.jig/process.md` holds how the repository is worked wherever no other home takes it, one `##`
section per topic, a new topic its own section. It is read on demand, never always-loaded, with
no line cap, and `AGENTS.md` points to it, naming when to read which section. It is created on
first use from jig's template, as the ledgers are. Where new process goes, one test decides, and
whoever places it (the owner, a hubnode, a spec, a retro) applies this table rather than
restating it:

| The process is… | Home |
|---|---|
| a rule every task needs | `AGENTS.md` |
| a rule for one situation (releasing, a migration, touching the build) | a section of `.jig/process.md`, its trigger named in `AGENTS.md`'s pointer line |
| knowledge behind how the repo is worked: code style, why the build is shaped so, packaging, a release's judgment calls, debugging recipes, CI quirks | a section of `.jig/process.md` |
| a procedure an agent runs when a task calls for it: steps, often a script, invoked by name | a skill; its knowledge stays in `.jig/process.md`, and the skill points to the section |
| something a machine can do or check | a script or a check (`.jig/scripts/`, `check.sh`, a hook), which a skill may call |
| a role's tier or effort | `roles` in `.jig/config.json`, with its reason |
| jig's own rules | `.jig/rules/` holds them; the lines every task needs arrive as jig's own lines in `AGENTS.md` (the template's, or a generated block) |
| the product | `docs/` |

A line cut from `AGENTS.md` to keep it under its cap goes by the same test: a rule every task
needs stays; the rest of how the repo is worked, code style included, to a section of
`.jig/process.md`; a release step to `.jig/scripts/release.sh`; a fact about the product to its
system's page; history to git. How the repo is worked never goes to a page.

A repo's terms are its glossary, `docs/glossary.md`, in one form:
- `# Glossary` first, the title: it holds no term and carries no field line;
- then `# Basic terms`, holding the terms every product uses, each an `###` heading;
- then a product per `#` heading: the software a repo builds, or the hardware it runs on. Its
  own definition is the paragraph under it, and it carries a `Repo:` line (the repo that builds
  it, or `none`) and a `Kind:` line (`software` or `hardware`). A repo builds one software
  product, so two products naming one repo can't both be `Kind: software`;
- under a product, its own terms as `###` headings before its first feature, then a feature per
  `##` heading, each with its own terms as `###` headings.

A product, a feature and a term are each a term, and each heading says what it means and what it
is not. A term may carry one field line, `Binds: <product or feature>, …`, naming where it applies
beyond its own product, and only in a metarepo's glossary. The title, a feature and `Basic terms`
carry none. A term's controlling repo is its product's `Repo:`; a term under `Basic terms`, or
under a product with `Repo: none`, is controlled by the repo whose glossary holds it. In a
stand-alone repo the products are its software and the hardware it runs on, and the features its
own; in a pararepo a product is one from the metarepo's glossary. `jig init` writes the title,
`Basic terms` and, in a stand-alone repo, its software product named for the board. `§` is written
only in a pointer, `docs/glossary.md § <term>`, and names a term's heading at any of the three
levels; the title and a table row are no term.

A commit changing the glossary is refused for each of these it adds: a first `#` heading that
isn't `Glossary`, a second that isn't `Basic terms` (one lacking only the title is told that
alone), a heading or a field line under the title, an `##` under `Basic terms`, a heading deeper
than `###`, a table, two headings that fold to one term (as a label folds), a product missing
`Repo:` or `Kind:`, a field line its heading may not carry (an `Owner:` line's refusal names
`Repo:`, the line it became), a `Binds:` naming no product or feature heading, two products naming
one repo with `Kind: software`, and a product the roadmap includes or names dropped. One already
there doesn't refuse the commit, so an older glossary stays editable until its rebuild; until it
is in the form, any heading carrying `Repo:` reads as a product. Order isn't refused: `jig merge`
re-sorts the glossary in the merge commit, the title and `Basic terms` first, then the products in
alphabetical order, and within each its own terms first, then its features, each set in
alphabetical order. Whole entries move, within their parent, and no word changes; one already in
order stays byte for byte. `jig glossary "<term>"` prints a term's heading path, its definition,
its `Binds:` (a product's `Repo:` and `Kind:`) and its controlling repo, and `jig glossary add`
writes one in its sorted place, refusing a duplicate. `jig update --apply` adds `# Glossary` above
`# Basic terms` in a glossary whose first heading that is, changing no other line, once trunk's
committed checker takes the title: the run installing it says the heading waits, and the next adds
it. In a metarepo it is listed as a job's (M4). `jig update --apply` also rewrites each
`Owner: <repo>` line (`this repo` as the repo's own name) as `Repo: <repo>` and `Kind: software`;
where two products name one repo, it writes `Repo:` on both, `Kind:` on neither, and says the
owner marks one `software` and the other `hardware`. It reports a glossary out of the form, and
re-forms nothing: its rebuild is the owner's. The glossary is no system's page: it is not in
`docmap`, covers no files, and the page contract doesn't apply to it. No other glossary is a home:
survey and update list a `## Glossary` section of the root `README.md`, or a root `GLOSSARY.md`,
with `docs/glossary.md` as where it goes, and survey names each term in the glossary written as a
bold word opening a paragraph (`**term** — …`) rather than a heading.
`jig update --apply --glossary`, on the owner's yes, moves it under `# Basic terms`, below the
title: a README's `### <term>` stays `### <term>`, a GLOSSARY.md's `## <term>` becomes
`### <term>`, a bold-paragraph term gets an `###` heading, and a table moves as the table, listed
with what else the one form refuses, for the session to rebuild before committing; the old section
or file removed, and in the same change every pointer to the old home rewritten
(`README.md § <term>` to `docs/glossary.md § <term>`, a pointer to the section itself and
`GLOSSARY.md` to `docs/glossary.md`). The dry run lists each line it rewrites; each pointer it
can't (a section naming no term, prose naming the README), and each line the hook would refuse in
the move's commit (a term's text naming a root document), which it leaves for the session to edit
before committing; and each pointer in history, left as written: fenced code, a handoff, a
released section of the decision log or of a root `CHANGELOG.md`. A README `## Glossary` section
holding no term, only a link to `docs/glossary.md`, is no glossary.

`jig survey` also reads each page at home under `docs/`, board pages included, against the
contract above, and names a page in the old Now, Rules and Checks shape (convert it: fold
what it says into description, delete what no longer holds, keep as Invariants only what
passes the test), an Invariants entry with no why (` — `) or no holder (`held by`), or whose
holder names review (listed: survey reads the word, never the other holders), and a
page whose first line of text after its title is a heading rather than a lead paragraph. It
lists, apart, a page line naming a `.jig/` path other than the decision log (Product and
process), and the project in the product: an `## Undefined` heading on a page or a metarepo's
entry file, and what the hook refuses on an added line (a `.jig/specs/`, `.jig/handoffs/` or
`.jig/roadmap.json` path, a scope id in code quotes) in old text on a page or in the decision
log, each with where it goes. It searches no words that may be the product's. `jig update --apply` brings this file; it
changes a page only by `--sweep`, below, on the owner's yes, and reshaping a repo's pages is a job of its own there.

`jig update` sweeps a repo onto the boundary, each move on the owner's yes. Under Repo files to
review it lists each page's `## Undefined` entry as the No phase item it would become, the
project paths and quoted scope ids above, and the repo's plan and register files with where
each one's content goes: `TODO.md`, `BACKLOG.md`, `STATUS.md`, `PLAN.md` and a hand-written
`ROADMAP.md` to `.jig/roadmap.json`; `FEATURES.md` to its systems' pages and decision entries;
`RULES.md`, `CONVENTIONS.md` and `CONTRIBUTING.md` sorted line by line by the test under Homes.
It lists, too, each page line naming a `.jig/` path (Product and process). It judges none of
them. `jig update --apply --sweep` writes the items under No phase in `.jig/roadmap.json`, creating it when
absent, on trunk (R5), and removes each emptied Undefined section where the pages may change:
on trunk, or in a metarepo a job's worktree (M4), where it removes only the sections whose
entries trunk's roadmap holds. In a pararepo with no roadmap of its own whose metarepo holds
none of its products, or can't be reached, it writes nothing and refuses, saying to propose the
product to the metarepo first (a glossary product with a `Repo:` line naming the repo), then
`jig move-in`; the dry run says the same.

### The findings record

Each file finding `jig survey` prints, and `jig update` lists under Repo files to review, has
an id, `<kind>:<path>`, the kind as survey's `--json` gives it (`shape`, `page`, `deep`,
`contract`, and a page's level when it isn't a subsystem: `section`, `shared`, `unmapped`):
`shape:docs/a/b/b.md`. Two approved moves onto one path go one at a time: `--apply` makes the
first and keeps the other recorded, and says so. A stray, a metarepo page in no genre, an old board file
and a page whose only problem is the old contract have no id: `/jig:redocument`'s remap answers
them. The owner's answer to each is recorded on trunk in
`config.json`'s `findings`, one entry per id, no globs, trunk-only like the rest of the board
(R5):

- `"approved"`: do it;
- `"deferred: <where>"`: later, and where it will be answered (`deferred: redocument`);
- `"exception: <the owner's reason>"`: the repo differs from this file on purpose. An exception
  or a deferral with nothing after its colon doesn't count, and survey lists each entry that
  doesn't. A deep page's exception is its folder in `deep_subsystems`, with its rationale, never
  a `deep:` entry here: one finding has one exception record.

jig acts on the recorded entry, never on an answer in chat, so the answers are one commit on
trunk before anything acts on them. Survey and update print each finding's outcome beside it —
not answered, approved and not done, the deferral, the exception — and survey's `--json` gives
`id` and `outcome`. Survey's last line counts the findings not answered, those approved and
not done, the exceptions that answer no finding, and the remap rows that contradict it (below),
each with who acts on it, so it never says there is nothing to do while one stands. A carried-out
move never renames an entry onto an id already recorded: it leaves that entry at its old id and
says so.

An answer stays where the owner put it: it answers the finding with its id, at its path, and
nothing reads it anywhere else. An entry moves only with jig's own move, below, and jig never
drops an exception: it is the owner's reason, which no tree can rebuild. When a page moves by
other means (a job, a remap), its exception is recorded again at the new path, or dropped, on
trunk. Survey lists each exception that answers no finding, except while `.jig/redocument.md`
is on trunk.

`jig update --apply` carries out each approved move, whether or not the layout is current: a
`shape` finding, or a `page` outside the tree that isn't a fold. It makes the `git mv`, renames
the `docmap` key and `boards` entry naming the old path, drops the entry, and moves the page's
other entries (an exception on its `contract` finding) to its new path. It drops an approval or
a deferral whose finding no longer fires: that question is settled. What it can't do — a reference in another file, a
`contract_paths` glob, a `buffer.md` row per cached pointer, an edit — it prints for the
session to make in the same commit, and an approved finding it can't carry out stays recorded.
The usual refusals apply (open jobs, tracked changes), and it commits nothing. In a metarepo a
page moves only in a job (M4): `--apply` lists the approved moves as the job's and makes none,
and each approval drops on trunk's next `--apply` once its move has merged.

`/jig:redocument`'s remap, `.jig/redocument.md`, is read by its table's `Old path(s)` and `New
path` columns, `same` keeping each old path. The hook refuses a commit that adds or changes it
while a row keeps a page at a path survey moves it from (a `shape` or `page` finding), judged on
the tree the remap leaves — a page alone in its folder today that another row gives company is
in the right form — unless
`findings` records the owner's exception for that page; the refusal names the page, survey's
destination and the entry to record. Survey names such rows in a remap already on trunk.
