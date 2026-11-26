# Roadmap rules

## Roadmap

Every stand-alone repo and metarepo keeps one, `.jig/roadmap.json`, its structure there even
when it holds nothing: `{"products": [], "phases": [], "no_phase": []}`. Nobody reads it by
hand: `jig roadmap` prints its states and `jig roadmap show` draws it. `jig init` writes it, `jig update --apply` adds it where it's missing, and `jig roadmap`, rig,
reading-list, survey, staging, the gate and the merge write it when trunk has none: in the
trunk checkout on trunk with nothing staged they commit it alone, `roadmap: the empty structure
jig init writes` (`ROADMAP:` leading in a metarepo, M6); anywhere else they write nothing and say where it is written. A root
`ROADMAP.md` that is the repo's own holds it back until its content is moved into
`.jig/roadmap.json` (`jig update` lists it). On trunk the hook refuses a commit removing it, and
with none on trunk it refuses a spec's `Scope:` line, naming `jig roadmap`. jig
writes none in a pararepo, which plans from its metarepo's (Products, below): `jig init --para`
removes the empty structure a plain init wrote, and the sweep there writes none.
A repo is for one software product, and the hardware that runs it may be defined there, its
pages segmented within `docs/` as the hardware skill's board pages are; so a stand-alone repo
keeps one roadmap with no product level in it. A metarepo and its pararepos plan from one
roadmap, the metarepo's (Products, below), so no scope exists in two copies to drift.

- **The source**, `.jig/roadmap.json`, three lists. `phases`, in order (no dates: order is the
  list's): each `{"product", "name", "note", "exit", "after", "needed_by", "scopes"}`, where
  `exit` is the checklist the owner checks, `[{"text", "done"}]`, and `product` is written only
  in a roadmap holding more than one product. `scopes`: each `{"id", "text", "labels",
  "touches", "after", "needed_by"}`, the id with no space or `/`; a scope's ref is
  `<phase>/<id>`, the phase named `<product> <name>` where it has a product. `no_phase`: items,
  each what a scope holds plus `product`, `stopped_at` and `parked` (`YYYY-MM-DD`). `products`:
  the glossary's product terms the roadmap includes. A phase carries `exit`, `scopes` or both,
  either of them maybe empty. A field left empty is left out; nothing
  else is written, since states and blocked are derived and a phase's type is read from its
  name. The fields and their types come from one example record of each kind in `jig.py`; `jig
  update` writes those as the repo's templates. The hook refuses a field or a type they don't
  have (each exit check's too), a key written twice in one object, a phase with neither `exit`
  nor `scopes`, a product `products` doesn't include or the glossary doesn't hold, a duplicate
  phase or scope id, and every problem below, and `jig roadmap` reports them. jig reads and
  writes the records themselves: a text or a note is prose wherever it ends, kept as written,
  lists and line breaks included (`build it (after lunch)` is a text, not a wait). No phase's
  items are in no order. "Every scope is done" is
  implied, never written as a box. A scope's `touches` are the pages it will change.
- **Dependencies**: a scope's `after` names what it waits on; a phase's `after` applies to each
  of its scopes. A ref is `<phase>/<scope>`, `<phase>` or `No phase/<id>` in the same roadmap.
  A wait written as prose is no wait: jig reads only `after`. On trunk, when the roadmap
  changes, the hook refuses a ref naming nothing the roadmap has, a ref to itself (a scope
  naming its own phase too), and a ring, named once with all its members; `jig roadmap` reports
  the same.
- **Labels**: a scope's or a No phase item's `labels` are the features it touches. Labels sit on
  scopes and items, never on a phase: a phase has no `labels` field. Each label is a term of
  the glossary: in a family the metarepo's `docs/glossary.md`, read where the
  roadmap is (on its trunk, live from there in a pararepo); in a stand-alone repo its own. It
  matches in any case and spacing: both, case folded with each run of spaces, `-` and `_` read
  as one `-`, are equal, so `wallet-compatibility` names `## Wallet compatibility`. On trunk, when
  the roadmap changes, the hook refuses a label naming no term; with no glossary, any label is
  refused, naming it. On the metarepo's or a
  stand-alone repo's trunk, a commit removing or renaming a term a label names is refused,
  naming each scope: re-point the label in the same commit. A label is never a ref: it orders
  nothing, changes no state and blocks nothing, so a ref naming one is a ref to nothing.
  `jig roadmap` prints each scope's labels after its state, and `jig roadmap --label <term>`, one of its filters (below), keeps only the scopes and items
  carrying it, across every product, headed by the repo controlling the term (its product's `Repo:`): what touches a feature,
  and which other repo's work leans on one this repo owns. A new term is the
  metarepo hubnode's; a repo labels its own scopes freely.
- **Types**: each phase is a *Prototype*, a *Pilot* or a *Production* phase, read from its name
  after any product term, case folded: a Greek letter (`alpha`, `beta`, `gamma`, …) is
  Prototype, `Pilot <letter>` is Pilot, and any other name (`Launch`) is Production. There is
  no marker and no config. Within one product, and among the repo's own phases, types run
  Prototype, then Pilot, then Production, in file order: on trunk, when the roadmap changes,
  the hook refuses a phase whose type comes before the type of a phase above it in the same
  product, and `jig roadmap` reports it; `jig update`'s dry run lists each one, to fix in the
  same update. `jig roadmap` prints each phase's type beside its state, and `show` in each
  phase's box (`alpha (Prototype, current)`).
- **Filters**: `jig roadmap` takes `--product`, `--phase`, `--type`, `--state`, `--owner` and `--label`,
  each repeatable and case folded; values of one flag are or'd, different flags and'ed.
  Product, phase, type and owner choose phases: `--phase alpha` is every product's alpha,
  `--phase "Widget alpha"` that one heading. `--owner` is the repo a product's `Repo:` names; a
  metarepo's own phases and the products it controls (`Repo:` naming it, or `none`) are the metarepo's, and in a stand-alone
  repo everything is the repo's; any name jig knows this repo by (`this`, its name, an alias in
  `jig repos`) means this repo, so in a pararepo it is the products whose `Repo:` names it.
  `--state` (`open`, `taken`, `done`, `blocked`, `unknown`) and `--label` (a glossary term, as
  labels match) choose scopes within them, and a phase left with no scope isn't printed. A No phase item
  matches product, owner, state and label; `--phase "No phase"` chooses the lists, and `--type`
  leaves them out. A filter hides rows, never a problem: the problems print in full and the
  exit code is unchanged. A product, phase, owner or type naming nothing jig knows is refused,
  naming the known values, and filters that match nothing say so. `jig roadmap show [filters]`
  draws what they choose (The chart, below). `jig roadmap --json [filters]` prints the records
  they choose, each with its key and derived state, and `--id <id>` only the phases, scopes or
  items named: an agent asks jig for the records it needs rather than reading the file.
- **No phase**, `no_phase`, the one list for work with no phase, in no order, on the owner's
  word: work parked mid-build and work not started, one place for both. An item holds what a
  scope holds; a parked one says where it stopped, `stopped_at`, and when, `parked`. Its id is
  `No phase/<id>` (`<Product> No phase/<id>` for an item with a `product`), which a `Scope:` line takes as it takes a scope, and its state is derived the
  same way: open, taken or done. It is never current, so work with no stage never reads as a
  stage. The hook refuses a duplicate id. `jig reading-list` prints, after each page, the items not done and the scopes
  not done that name it, and fold-in asks about them (`rules-handoff.md`, Fold-in). A built item stays, shown done,
  until the owner's roadmap change removes it: dropping a done item a note still takes is no
  drop.
- **The old form.** `jig update --apply` converts a `.jig/roadmap.md` to `roadmap.json` on trunk
  on the owner's yes: every phase, scope, item, suffix, note and exit check with its text
  unchanged, a note whole (its lists and the prose after them), lines nested under an item as
  its text, each phase under the product its heading's leading words named, a product of the metarepo's glossary, an old
  `## Up next` folded into No phase, and a parked item's text split into `text`, `stopped_at`
  and `parked` where it has that form. It is judged by its output: the converted records drawn
  in the old form again, each old line that doesn't come back under its heading and the line it
  hung from is listed (prose above the first heading but the title and jig's own seed comment,
  prose or a fence among the boxes, after `Scopes:` or in No phase, an indented line before a
  list's first item), with each problem the old file's own checks name and each the hook would
  refuse in the file it would write, and the conversion waits until the owner moves, fixes or
  deletes it. Nothing is dropped unnamed. Products are placed as every reader places them: by
  the glossary in a metarepo, nowhere else. It removes `roadmap.md`, and a `ROADMAP.md` jig
  generated (a repo's own is left). It runs in two runs: the hook runs trunk's committed
  checker, and an older one refuses a commit removing `roadmap.md`, so the first run installs
  the checker and names the conversion as waiting on it, and the run after that commit
  converts.
- **Products**, in a metarepo's roadmap: a phase or an item with a `product` belongs to that
  product, a product of the metarepo's glossary (a `#` heading with its `Repo:` and `Kind:`
  lines), which `products` includes; its `Repo:` names the pararepo that builds it, as `jig
  repos` knows it, or the metarepo itself, or `none`, and the metarepo controls the last two. Every
  other phase is one of the metarepo's own. A product in the glossary that `products` doesn't
  include gets no phase, scope or item, and nothing asks about it. Each
  product's phases are ordered among themselves in file order and have their own current
  phase, and so do the metarepo's own; nothing orders one product after another but an
  `after`, and a ref may name another product's phase or scope. A product's items are its list,
  their ids `<Product> No phase/<id>`. A `touches` page of a product's
  phase or item is a page of the product's owning repo, checked on that repo's trunk when it can be
  reached. `jig roadmap` reports a product whose `Repo:` names no repo jig knows.
- **One reader.** A pararepo with no roadmap of its own reads the metarepo's live, from its
  checkout's trunk, never at the pin: a roadmap change is never released (`rules-pararepo.md`,
  Pararepo). Every reader goes through it: `jig roadmap`, rig, reading-list, fold-in and the
  hooks. A scope's states are pulled from the specs and notes on the metarepo's trunk and on
  each pararepo's that `jig repos` reaches; one it can't reach is named, and its products'
  scopes read *unknown*. The hook checks a pararepo's `Scope:` lines against the metarepo's
  trunk, and passes them with a warning naming it when it can't be reached; on the metarepo's
  trunk it refuses dropping a scope a reachable pararepo's spec or note takes, naming the file;
  one dropped while that pararepo can't be reached passes with a warning, and that pararepo's
  next commit to the spec taking it is refused. A pararepo that keeps a roadmap of its own is
  its own family of one: its specs take its own scopes, never the metarepo's. A pararepo whose
  trunk removes a page its product section touches commits, warning that the metarepo's item
  needs re-pointing.
  A pararepo's merge writes nothing to the metarepo. In a pararepo the next step comes from the current phases and lists of the
  products it owns; in the metarepo, from its own and the products it owns as `this repo`.
- **A phase's note** is its `note`, prose. `jig roadmap` prints it under the phase.
- **A touched page exists**, in either form. `jig roadmap` reports one that doesn't; on trunk
  the hook refuses a commit that leaves an item or a scope touching no page, so a page renamed
  or deleted there is re-pointed in the same commit; and `jig merge` re-points each page the job
  moved. A page a metarepo moves down to a pararepo takes its items with it, and the refusal
  names the move's pointer. To a pararepo that plans from the one roadmap, they follow it in the
  same commit, into that pararepo's product, with `touches` at the page's path there. To one that keeps a roadmap of its own, the item goes by a roadmap change staged with
  `target: <pararepo>`, applied there on its owner's yes, while this commit drops it, or the page
  from its `touches`. A section moved down leaves its page, so it moves no item.
- **Specs take scopes** with a `Scope:` line under `Source:`, e.g. `Scope: alpha/screen,
  alpha/battery`. Many-to-many: a spec may take several scopes, a scope may be taken by several
  specs, and a spec with no `Scope:` line takes none. A spec removed once its job merged keeps
  its scopes on its completing note's `Scope:` line, which counts as the spec's: the hook
  refuses a trunk commit dropping a scope a note still takes, naming the note, until its line is
  re-pointed in that commit.
- **A spec takes only what it builds.** Work it doesn't build stays on the roadmap, unspecced,
  where a later spec takes it. When a spec builds only part of a scope, a roadmap change on the
  owner's yes splits the scope first: the built part becomes a new scope, which the spec takes
  whole and may restate in its own words; the parts not built stay in the original scope, under
  its id, with their text unchanged; and a wait on the original id keeps waiting until the rest
  is built. No new scope state: a scope stays open, taken or done. Nothing in a commit shows
  whether a job built all of a scope, so this is the spec role's rule and review's, not the
  hook's.
- **Out of scope never defers.** An `## Out of scope` line is work nothing will do, or work
  another named spec, job or repo does; it closes with the spec. Work worth building later goes
  onto the roadmap as a scope or No phase item on the owner's word, and review blocks a deferral
  written as prose. The hook refuses a spec carrying a `Later:` line in its header, the retired form of a
  deferral, and `jig update --apply` deletes one from each spec on trunk, naming it: each id it
  named is already on the roadmap. A handoff note's is history, left as it is.
- **A spec is complete** when a handoff note naming it (`Spec:`) is on trunk and the commit it
  names is in trunk's history, merged or handed off solo on trunk. `jig handoff --partial` is a
  chunk that doesn't finish its spec: its note records `Partial: yes` and completes nothing.
- **States are derived**, never edited. A scope is *open* (no spec takes it), *taken* (a spec
  that takes it isn't complete) or *done* (taken, and every spec that takes it is complete). A
  phase is *done* when every scope in it is done and every `exit` check is done; one with
  no scopes and no checks is *empty*, and never done. The first phase not done whose own
  `after` refs are all done is *current*, the rest *next*. A scope is **blocked** while any
  ref, its own or its phase's, isn't done: derived like the states, a qualifier on them, never
  a fourth. `jig roadmap` adds `after <ref>` beside an open blocked scope, and `show` says
  `blocked`.
- **The chart**, `jig roadmap show [filters] [--width N]`, printed and never written: a box per
  phase, each scope a box of one width with its id and state, in the column one past the
  furthest column of anything it waits on (a phase standing for all its scopes). A phase's box
  is as wide as its scopes, and where the chart holds more than one product, a box per product
  is as wide as its phases. Within a column, scopes sharing a first label sit together. Each
  product's No phase items come last. Wider than 100 columns (or `--width`), each phase is a
  band of its own, its first column at the left. No dates: order is the waits'. The AGENTS.md
  template's Commands carry `roadmap:`, the line any agent asked to show the roadmap runs.
- **R5** covers the roadmap: it changes on trunk only. Phases and scopes are the owner's plan,
  not work, so they change on trunk only. A roadmap change asks for no decision entry and no
  change line: git keeps its history. One other branch may carry `.jig/roadmap.json`: a metarepo's
  `propose/` branch, a pararepo's buffered edit (Edits, below), whose merge is a trunk commit
  on the metarepo owner's yes, where the hook checks it as any trunk change.
- **Edits.** No hubnode edits another repo's content. A pararepo's changes to its products'
  sections are buffered and reach the metarepo by the regular sync process, when the owner
  decides: a `buffer.md` row and `jig propose`, the change written on its
  `propose/<repo>-<slug>` branch in the metarepo, never on its trunk, and merged there at the
  next sync the owner calls. A pararepo's merge writes nothing to the metarepo's roadmap.
  Labels, names and new products (the glossary product and its `Repo:` and `Kind:` lines) are the metarepo's
  hubnode's: a product a pararepo proposes with its phases (`jig move-in`) is decided with them,
  name and definition and all, at that proposal's merge, where its hubnode may change any of
  them first.
  **The edit command.** `jig roadmap --draft` writes the roadmap this repo plans from (the
  metarepo's trunk, live, in a pararepo, with its sections as its open roadmap proposal has
  them; trunk's own otherwise) to `<git common dir>/jig/roadmap-draft.json`, outside the tree, and
  prints its path and the headings this repo may change: a pararepo its products' phases and
  lists; the metarepo its own and the products it owns as `this repo`; a stand-alone repo all.
  It refuses while a draft that differs from that is there. `jig roadmap --edit [<file>]` reads
  the roadmap again and refuses, writing nothing: a phase or an item added, removed or changed
  under a product another repo owns; in a pararepo, a new phase naming no product it owns; and
  anything the hook would refuse on the result (fields, types, refs, rings, touched pages on
  the owning repo's trunk, a dropped scope a reachable spec or note takes, labels). In a
  pararepo a label the metarepo's glossary lacks is left off the line and staged in the
  metarepo as `label-<term>.md` (`target: <meta>`, `kind: doc`, `destination:
  docs/glossary.md`), naming the scopes it labels and the repo; in the metarepo or a
  stand-alone repo it is refused, the term going in first. In the metarepo or a stand-alone
  repo the edit writes `.jig/roadmap.json` in the trunk checkout (refused elsewhere, R5, and while
  that file differs from trunk's), to commit on the owner's yes. In a pararepo it adds an Open
  `buffer.md` row (`<meta>/.jig/roadmap.json § <phase>, …`; the scopes and items added, changed
  or removed; `hubnode, <date>`) and commits the change on this repo's open roadmap proposal,
  an unmerged `propose/<repo>-roadmap-<date>` branch its spec `roadmap-<date>.md` cites, or a
  new one: by plumbing in the metarepo's checkout, so no checkout moves, replacing only this
  repo's sections, whole. The spec lists roadmap rows only, so `jig propose --buffer` and
  `jig release` never sweep them; commit it and `buffer.md` here. Either way the draft is
  deleted. On a metarepo's `propose/<repo>-…` branch the hook refuses, as `--edit` does, a
  change to a section another repo owns, the proposing repo found by its `jig repos` name or
  its folder's, and a roadmap change on a branch naming no pararepo; a section that is
  trunk's as it stands, merged in, is trunk's change, never the branch's. A section the fork has is
  whose the fork's glossary says; a new one is whose the commit's own glossary says, so a product
  it proposes is its own, and a rename moves a product's headings in the commit that renames
  its term. A move's proposal
  (`jig move`, read from the moved-from or pointers line it adds to the log) may add to the
  receiver's sections the items that follow the moved page, each touching it, and nothing else
  there.
- **Moving in**, once per pararepo, on the owner's yes, by `jig move-in --product <Name>` in the
  pararepo's trunk checkout. It runs one step per `--apply`; without it, it prints each step's
  state (done, next, or whose yes it waits on) and what the next would write.
  1. *Product and phases proposed.* Each phase becomes `<Product> <phase>`, its `product` set,
     unless its name's leading words are already a term the metarepo's glossary says this repo
     owns, and each No phase item takes the product too; each ref in `after` and `needed_by` is
     mapped the same way, and every other field is kept as written. With no `<Product>` term on
     the metarepo's trunk, the same proposal carries it: `# <Product>` in its sorted place, with
     `Repo: <repo>`, `Kind: software` and the sentence `--definition` gives, and its line under `## Unreleased`
     `### Added`, so one yes decides the product and its phases. A term another repo owns, a
     mapped phase the metarepo's roadmap already has is refused before anything is written. `--apply` adds one `buffer.md` row, opens `propose/<repo>-move-in`
     carrying that row alone, listed in `.jig/specs/move-in.md` (the next free name, `move-in-2`
     and its branch, once a withdrawn proposal holds it), and commits the sections there in a
     temporary worktree of the metarepo, whose hook judges the commit. That spec is step 1's
     record, found by scanning specs as `jig sync` finds a proposal. A rerun of step 1, under
     another `--product` too, takes the one Open move-in row there is and edits its claim, never
     adding a second. That spec: it lists that row alone, its
     copy of the row names the product, and its `meta:` line the branch. The row is `jig
     move-in`'s: a release or `jig propose --buffer` never carries it. The metarepo's hubnode merges the branch in a job
     opened on it (`jig open <job> --branch propose/<repo>-move-in`), or on its trunk on the
     owner's yes; a job merging it from another branch is refused (R5). On the metarepo's trunk
     the hook reads a heading's product by the commit's own glossary, as by its own roadmap, so
     the term and the phases it owns land in one merge; it refuses a commit or a merge that
     leaves a product's phases without the glossary product either side had. A refused
     or failed step undoes what it wrote on both sides; a run interrupted part way may leave an
     empty `propose/` branch or its row, and a rerun recovers from either and starts the step
     again. A withdrawn proposal's spec stays as it is.
  2. *Its roadmap leaves*, once the metarepo's trunk has the proposal. `--apply` stages
     `git rm` of `.jig/roadmap.json` and each `Scope:` line in tracked
     specs and handoff notes re-pointed by the map, under the product its row names, or the name
     `--product` gives when the metarepo's hubnode renamed it at the merge (the owner's word:
     nothing is guessed from the metarepo). It is refused, naming what it read, while the
     metarepo's glossary doesn't give the product to this repo, or its roadmap holds none of the
     mapped phases. An id the metarepo's trunk lacks (its owner changed it before merging) is
     named with what takes it, and left for the hubnode to re-point by hand.
     The hubnode commits it on trunk on the owner's yes, and the hook checks every `Scope:`
     line it keeps against the metarepo's trunk.

  After it, the pararepo's hook refuses a `.jig/roadmap.json` while the metarepo's roadmap holds
  a product it owns, and `jig update --sweep` writes none there: its `## Undefined` entries are
  proposed as that product's No phase items.
- **Unconfirmed waits.** A scope or phase may say what waits on it, `needed_by`, as it says
  what it waits on. A cross-product `after` the waited-on scope or phase doesn't
  confirm so is listed by `jig roadmap` in the metarepo and under rig's Waiting on you, for the
  owner to rule on. It blocks no commit and no step: the wait itself still blocks as any does.
- **The hook refuses** a spec whose `Scope:` names a scope or `No phase/<id>` trunk's roadmap doesn't have (on
  trunk, the commit's own roadmap), and on trunk a roadmap change that drops or renames a scope
  a spec still takes, naming the spec: re-point it in the same commit.
- **The next step** is one step ahead, as if staging and the waiting specs were cleared: the
  first open, unblocked item of No phase that names pages, none of which an open job's,
  waiting spec's or staged file's Touches names (by the page itself: a glob or a folder
  doesn't count), and that no waiting spec or staged file takes; an item naming no pages is
  never offered. Else a scope from one walk out from the **front**, each phase not done up to
  and including the current one, nearest first and in file order within a round. A phase
  reaches its waits, then its scopes not done; the first scope that is open, unblocked and
  taken by no waiting spec or staged file's `Scope:` line is the step; a blocked or taken
  scope reaches what it waits on, so the work that unblocks it is offered as soon as it isn't
  blocked. So the current phase's own first free scope comes first, and one reached past the
  front's own scopes says who waits on it. A walk that ends at work done or under way offers
  no step. Under rig's Waiting on (work, not an answer) are each item passed over because its
  pages are named, waiting on what names them, each blocked item naming pages, and each open
  blocked scope of a front phase that nothing takes, waiting on its refs. A waiting spec or
  staged file whose `Scope:` names a blocked scope waits on that scope's refs, as a `Build
  after` waits, and never starts. `jig rig` (`rules-workflow.md`, Workflow) proposes the step to the owner and never
  writes the roadmap.
