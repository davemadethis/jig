# Records

jig keeps a handful of records in a repo, each with one home. Everything it makes lives in a
hidden `.jig/` folder, so nobody mistakes it for your project. A session reads them to learn
what's true, what was decided, and what comes next. They are the pages, the
[decision log](glossary.md#decision-log), the [roadmap](glossary.md#roadmap), [staging](glossary.md#staging), and
releases.

## The always-loaded file

Agents read one instructions file at the root on every task, and a long one gets ignored
wholesale. jig keeps it under 40 lines: what the project is, its commands, and the rules every
task needs. Everything else loads only when a task calls for it. The rulebook,
`.jig/RULES.md`, holds every rule the hooks enforce.

## Pages

The product is described under `docs/`, one page per system. A page says what's true of its
system on [trunk](glossary.md#trunk) today, in plain present tense. It isn't a rulebook, a plan or a changelog.

Every page keeps the [page contract](glossary.md#page-contract):

1. A lead paragraph, with no heading, saying what the system is and why it exists.
2. Sections named for what the code has (Schema, Renderer, Sync), never Overview or Notes.
3. An optional Talks to section: what crosses the system's boundary.
4. An optional Invariants section: only the facts that must hold, each saying why and what test holds it.

A page stays a single file until it has something else to hold, like a datasheet or a
subsystem's page. Only then does it get a folder. Your own words live in `docs/glossary.md`,
one heading per term, so any page can point at one. It takes one form: `# Basic terms` first, then
each product as a `#` heading with a `Repo:` line (the repo that builds it, or `none`) and a
`Kind:` line (`software` or `hardware`), each feature as a `##` under its product, and each term
as a `###`. A term belongs to the repo its product's `Repo:` names. The hook refuses a change
that breaks the form, `jig merge` keeps it sorted, and `jig glossary` reads and adds terms.

Docs point only at docs. The root files may point into `docs/`, but a page never points back
out. A page also never names a plan, a [phase](glossary.md#phase) or a [handoff](glossary.md#handoff). The hook refuses those lines.

## Docs move with code

`.jig/docmap.json`'s `docmap` maps each page to the source files it covers. A handoff has to answer for
every page its change touched: still true, or updated. `python3 .jig/jig.py reading-list <files>`
prints which pages to read before touching those files, including the system page above each.

## Decision log

Every repo keeps one decision log, `.jig/decisions.md`. It holds
decision entries, each saying who decided, when, and what it replaced. It also holds plain change
lines in Keep a Changelog's groups, under one heading per release.

You change your mind by writing a new entry that supersedes the old one. The old one comes out
in the same commit. So the log shows what holds now, and git keeps the rest. Each entry names
the pages it touches. When two entries touch one page, the handoff has to say whether they agree.

`python3 .jig/jig.py update` can fold an old changelog and decisions file into the log, when
you say yes.

What you still need to research before you can decide it lives beside the log, in the
[ideas log](glossary.md#ideas-log), `.jig/ideas.md`. An idea keeps its decision id, so deciding
it moves it into the log under that id. Ideas carry labels the way scopes do, and
`python3 .jig/jig.py ideas` lists them. A log from an older jig kept its open questions in a
section of its own, and `python3 .jig/jig.py update` moves them over, word for word.

## Roadmap

Every stand-alone repo and metarepo keeps a roadmap, with its empty structure if nothing else.
`jig init` writes it, `jig update` adds it where it's missing, and a command that finds none on
trunk writes it then. A pararepo keeps none: it plans from its metarepo's. The roadmap lists
phases in order, and each phase lists its
[scopes](glossary.md#scope). A [spec](glossary.md#spec) says which scopes it takes. A scope is done when every spec
taking it has landed, so nobody ticks a box to show progress.

Each phase has a type, read from its name: a Greek letter (`alpha`, `beta`) is Prototype,
`Pilot A` is Pilot, and any other name, such as `Launch`, is Production. Within a product the
types run Prototype, then Pilot, then Production, and the hook refuses a roadmap on trunk that
puts them out of order.

The roadmap is a JSON file in jig's folder, records nobody reads by hand: `jig roadmap --draft` writes
it as a draft to edit, and `--edit` checks it and writes it. `python3 .jig/jig.py roadmap show`
draws it as a chart, each scope in the column one past what it waits on.
`python3 .jig/jig.py roadmap` can show part of the roadmap: `--product Widget --phase alpha` is
what's in Widget alpha, and `--type`, `--state` and `--owner` narrow it the same way, with or
without `show`.

Work you've named but haven't placed in a phase yet is an item in the roadmap's `no_phase` list.
`python3 .jig/jig.py roadmap` prints the roadmap's states.

A scope or a No phase item can name the features it touches as [labels](glossary.md#label),
its `labels` list (`["teleport", "wallet-compatibility"]`), each a term of the glossary (the metarepo's, in a
family). A misspelt label is refused, and a label orders nothing. `roadmap --label <term>` lists
the work carrying one, across every product.

A spec takes only what it builds. Work it doesn't build stays on the roadmap, unspecced, until a
later spec takes it. When a spec builds only part of a scope, the owner's roadmap change splits
the scope first: the built part becomes a new scope the spec takes, and the rest stays under the
original id, its text unchanged. `## Out of scope` never defers: it closes with the spec, so work
worth building later goes onto the roadmap as a scope or No phase item. The gate shows what
closes with the spec.

Pages and decisions describe the product. The roadmap holds the project: what comes next, and
in what order.

## Staging

A spec, a doc, a user story, a feature request or a roadmap change written in some other chat
goes into the repo's staging folder. It waits there until a session in
the repo lands it or drops it. A feature request comes back as a spec that lists everything it
had to fill in, so you can correct the reading before anything's built.

`python3 .jig/jig.py staging` lists what's waiting. A release is refused while anything is still
staged.

## Releases

Every repo ships its own way, through one command. `python3 .jig/jig.py release` runs the repo's
own `.jig/scripts/release.sh`. That could build a plugin file for one repo, or a `.dmg` and an
`.exe` for another. jig checks that the files it promised came out, then tags `vX.Y.Z`. After
the tag, `.jig/scripts/publish.sh` sends it out.

The first time, `/jig:release` asks what the repo builds and writes the script with you.
