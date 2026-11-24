# roadmap-labels: labels on scopes, the family report, and the roadmap edit command

Source: Dave (owner), 2026-11-23, in jig's hubnode session, on cross-repo-roadmap having deferred part of his agreed design to "later specs" without his yes: "end state was supposed to mean exactly that: everything including labels."
Source: maige-ecosystem hubnode session, 2026-11-19, the owner's design for one roadmap across repos (Maige-Eco `.jig/staging/request-scope-ownership-from-maige-{os,familiar,lite}.md`, `## Owner's answers`), the parts spec cross-repo-roadmap listed under Out of scope as later work: labels (R1–R3), the cross-repo report, and the edit command that refuses a line under another repo's product and stages label changes.

Kept separate from ideas-log: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from moving-in-command: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from phase-types: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from bug-deferred-scope: the owner, 2026-11-23: "start what you can in parallel" (the bug fix for deferred scope; its spec's name is the hubnode's to fill in here)

## Intent
A scope or a `No phase` item names the features it touches as labels, each a term of the
glossary that holds the family's names, so work can be read by feature and a misspelt label is
refused. One report shows what the family has let sit: stale staged files and `propose/`
branches with their ages, pending rulings that touch labelled work, and two names for one
thing. One command edits a family's roadmap: it refuses a line under another repo's product,
buffers a pararepo's edit onto its proposal branch, and stages a new label for the metarepo.

## Investigation

**The owner's design** (`request-scope-ownership-from-maige-*.md`, `## Owner's answers`; Rn is
round n):
- R1, 1.3: "introduce a 'label' you can apply to scopes, basically tagging scopes to group them
  together", so a repo knows "what it waits on vs. what is it's own".
- R2: "if scopes are labeled by feature, and features are owned by repos, then would we really
  need grouping labels"; "a naming scheme for features and their labels … live in the meta";
  "labels could map back to products and therefore ownership"; specs "probably dont need
  labels", and sort by the scope they take.
- R3: "Labels - agreed on all."
- R4 (ideas log): "ideas should be their own log, labeled the same way scopes are".
- R6: "roadmaps have phases, scopes within phases, and labels on scopes."
- R7: "a scope names the pages and the labels it touches"; "labels do not need dependencies,
  only scopes and phases".
- The pararepos' inputs ask the sync to report "a name used for two things or two names for
  one", "staged items over a week old", "a proposal or staged request nobody acts on … with its
  age", and "released entries that touch its scopes". cross-repo-roadmap settled: "A label
  carries no dependency, and no ref names a label (R7)", and "Labels, names and new products
  (the glossary term and its `Owner:` line) are the metarepo's hubnode's."
- bug-empty-proposal (c075cc0) deferred "a metarepo-side report that ages every `propose/`
  branch" and flags empty ones from the metarepo, to this report.

**The product today** (trunk 06550ea):
- [seen] `split_waits` (jig.py:10144) peels `(after …)`, `(needed by …)` and `(touches …)` off a
  scope's or item's tail in any order, and `repeated_waits` names one written twice. A
  `(labels …)` today stays in the scope's text, so a label is prose and checks nothing.
- [seen] `term_owners` (jig.py:10712) and `product_of` read the glossary's `## <term>` headings
  and `Owner:` lines, case folded; `glossary_terms` (jig.py:4869) reads headings and table first
  cells through `term_text`. `Family` (jig.py:10736) already reads the metarepo's glossary live
  in a pararepo (`trunk_show(meta_loc, GLOSSARY)`) and its own on the metarepo's trunk.
- [seen] `cmd_roadmap` prints states, refs, dead touches, unknown owners and unconfirmed waits;
  `roadmap_rules` is the hook's check; `rig_state`/`rig_text` hold Waiting on and Waiting on you.
- [seen] `open_proposal` (jig.py:9428) makes `propose/<repo>-<slug>` from the metarepo's trunk
  with plumbing (`commit-tree`, `branch`), never a checkout; `buffer_proposal` writes the spec
  that lists the rows; `proposal_empty`/`opening_commit` say a branch has nothing written.
  Today the change itself is written on that branch by hand in a metarepo worktree (smoke
  `family`, Part D's `fland`).
- [seen] `coordination_report` lists `git branch --no-merged` for adopt; nothing lists the
  metarepo's `propose/` branches with an age, and nothing reads staging across repos.
- [seen] Staging is never committed (RULES.md, Staging), so a staged file's age is its file's
  modification time; nothing else dates it.
- [seen] R5 lets only trunk and a metarepo's `propose/` branch made by `jig propose`
  (`proposed_branch`) carry `.jig/roadmap.md`.

**One layer up.** Labels are one more trailing parenthesis, read by the reader that reads the
other three; their check is the glossary-term lookup the `§` pointers already make. The edit
command is the check `roadmap_rules` runs at commit, run before writing, plus the propose path
that already exists. The report reads what `Family`, `proposal_empty` and the staging list
already read, for every member at once.

## Change

Three parts, in build order, each mergeable alone; A and B hand off `--partial`, C completes the
spec. B needs A (entries touching labelled scopes). C needs A (labels it stages).

**Part A: labels** (R1–R3, R6, R7)
1. **Form.** A scope or a `No phase` item may end with `(labels <term>, …)`, peeled by
   `split_waits` with `(after …)`, `(needed by …)` and `(touches …)`, in any order; a second
   `(labels …)` on one line is refused as the others are. A label is written as any case and
   spacing of a glossary term: it matches when both, case folded with each run of spaces,
   `-` and `_` read as one `-`, are equal (`walyt-compatibility` names `## Walyt
   compatibility`). Labels sit on scopes and items only (R6): a `(labels …)` line of its own in
   a phase is refused by line, so no label is ever lost as note prose.
2. **The glossary.** In a family, the metarepo's `docs/glossary.md`, read where the roadmap is
   read (on its trunk in the metarepo, live from its trunk in a pararepo); in a stand-alone
   repo, its own `docs/glossary.md`. On trunk when the roadmap changes, the hook refuses by line
   a label naming no term of it (naming the glossary), and a `(labels)` naming nothing. On the
   metarepo's or a stand-alone repo's trunk, a commit that removes or renames a term a label
   names is refused, naming the scope: re-point it in the same commit. A pararepo that can't
   reach the metarepo passes its check with the warning the `Scope:` check gives.
3. **No dependency.** A label is never a ref, changes no state, blocks nothing, and moves no
   step (R7). A ref naming a label is refused as a ref to nothing, as today.
4. **Read by label.** `jig roadmap` prints each scope's and item's labels after its state;
   the view (`ROADMAP.md`) shows them in the scope's cell. `jig roadmap --label <term>` prints
   only the scopes and items carrying that label, across every product, each with its state,
   specs and owning repo, headed by the term's own `Owner:` when it has one: "show me what
   touches this feature", and, for a term a repo owns, which of another repo's work leans on it
   (R2). `--label` is one of `jig roadmap`'s filters, which spec phase-types adds (`--product`,
   `--phase`, `--type`, `--state`, `--owner`, and `--view` for a filtered view on stdout): the
   same flag shape, combining with the others as they combine with each other, and honoured by
   `--view`. Whichever of the two specs lands second wires `--label` into that set; until
   phase-types lands, `--label` stands alone with that shape.
5. **One reader.** The label reader and its check are two functions, called by every reader of
   labels and never copied: `split_labels(what) -> (text, labels | None)` peels the
   `(labels …)` off a line's tail (inside `split_waits`, so the order of the parentheses never
   matters), and `label_problems(labels, glossary_text, where) -> list[str]` returns, by line,
   each label naming no term, after the fold of item 1. The ideas log (spec ideas-log, R4)
   calls both for its entries rather than parsing labels its own way.

**Part B: the family report**
6. **`jig family`**, in a metarepo or any of its pararepos, the same report from either, read
   through the metarepo's checkout and each pararepo `meta.json` lists that `jig repos`
   reaches; one it can't reach is named and skipped. It writes nothing and exits 0. Four
   sections, each printing `nothing` when empty:
   - **Staged**: every file in each reachable member's `.jig/staging/`, with its repo, `target`,
     `kind` and age in days, `stale` past 7 days.
   - **Proposals**: every `propose/` branch in the metarepo not merged into its trunk, with its
     age (its opening commit's date; for an older branch, its first commit past trunk), `empty`
     when nothing is written on it (`proposal_empty`), `stale` past 7 days, and the pararepo
     specs citing it (`meta: <meta> proposal <branch>`) or `cited by no spec`. This is
     bug-empty-proposal's deferred metarepo report.
   - **Entries touching labelled work**: each entry in the metarepo's `.jig/decisions.md` under
     `## Open` or `## Unreleased` whose `Touches:` names `docs/glossary.md § <term>` for a term
     that labels a scope or item not done, with those scopes and their owning repos: a pending
     ruling each repo should read before its next pin.
   - **Two names**: two glossary terms equal once folded (item 1's fold); and two scope or item
     ids under different products (the metarepo's own sections count as one) that are equal
     once folded, or where one is the other with whole hyphen-words added at its start or end
     (`teleport`, `teleport-clipboard`). Listed for the owner; never refused.
7. **Rig points at it.** In a family, `jig rig` prints one line after Waiting on you when any
   section holds a stale file, a stale or empty proposal, an entry or a pair:
   `Family: <n> stale staged, <m> stale or empty proposals, <k> entries touch labelled work,
   <j> pairs of names: jig family`. It counts in neither of rig's numbers: it is a report, not
   a question.

**Part C: the edit command**
8. **`jig roadmap --draft`** writes the roadmap this repo plans from (the metarepo's trunk,
   live, in a pararepo; trunk's own otherwise) to `<git common dir>/jig/roadmap-draft.md`,
   outside the tree so no second copy is ever committed, and prints its path and the headings
   this repo may change: in a pararepo, its products' phases and lists; in the metarepo, its
   own phases and list and the products it owns as `this repo`; in a stand-alone repo, all. It
   refuses while a draft that differs from its base is there, naming it.
9. **`jig roadmap --edit [<file>]`** (the draft by default) reads the base again, live, and
   checks the file against it. It refuses, writing nothing, by line: an added, removed or
   changed line under a heading whose product another repo owns; in a pararepo, a new heading
   that is no product it owns (a new product is the metarepo hubnode's: its glossary term and
   `Owner:` line come first); and anything the hook would refuse on the result (shape, refs,
   rings, dead touches checked on the owning repo's trunk, a dropped scope a reachable spec or
   note takes, labels as Part A).
10. **Labels it stages.** In a pararepo, a label the metarepo's glossary lacks is not refused:
    it is left off the line written, and staged in the metarepo's `.jig/staging/` as
    `label-<term>.md` (`target: <meta>`, `kind: doc`, `change: update`, `destination:
    docs/glossary.md`, `source:` this repo's hubnode and date), naming the term, the scopes it
    labels and the repo; `--edit` prints that the label is added once the term lands. In the
    metarepo or a stand-alone repo, a label the glossary lacks is refused: the glossary is that
    hubnode's, so the term goes in first, in the same commit.
11. **Where it lands.** In the metarepo or a stand-alone repo: it writes `.jig/roadmap.md` in
    the trunk checkout (refused elsewhere, R5, and while that file differs from trunk's
    committed one, so nothing uncommitted is overwritten) and says to commit it on the owner's
    yes. In a pararepo, buffered (the owner, 2026-11-21, Q3): it adds an Open `BUFFER.md` row
    (`<meta>/.jig/roadmap.md § <heading>, …`; the scopes and items added, changed or removed,
    by id; `hubnode, <date>`), and writes the change on this repo's open roadmap proposal: an
    unmerged `propose/<repo>-roadmap-<date>` branch its spec `roadmap-<date>.md` cites, or a new
    one opened as `jig propose` opens one, its spec listing only roadmap rows, so `jig propose
    --buffer` and `jig release` never sweep it. The commit on that branch is made with plumbing
    in the metarepo's checkout (a temporary index, `commit-tree`, `update-ref` from the old
    tip): no checkout moves, and the metarepo's trunk is untouched until its owner merges the
    branch at the next sync. It replaces only this repo's sections, whole, in the branch's
    roadmap. It prints the branch and the row, and says to commit the spec and `BUFFER.md` here.
    Either way the draft is deleted.
12. **RULES.md** says all three: Roadmap (Labels; the edit command under Edits), Metarepo and
    pararepos (the family report; the staged label), Commands (`jig family`, `jig roadmap
    --label`, `--draft`, `--edit`).

## Done when

Every command in a throwaway repo, run with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.
Nothing writes `~/.config/jig/`.

Part A, in a stand-alone repo with `docs/glossary.md` holding `## Teleport` and `## Walyt compatibility`:
- [ ] (form) `## alpha` scopes `pairing: … (labels teleport, walyt-compatibility) (after alpha/host)` and `host: … (touches docs/x.md) (labels Teleport)` commit on trunk. `jig roadmap` prints `labels teleport, walyt-compatibility` beside pairing, and `after alpha/host` still; the view shows both labels in pairing's cell.
- [ ] (refused) `(labels telport)` is refused by line, naming `docs/glossary.md`; so are `(labels)`, a second `(labels …)` on one line, and a `(labels teleport)` line of its own in a phase.
- [ ] (no dependency) `(after teleport)` is refused as a ref to nothing; pairing's and host's states and `jig rig`'s next step are what they are with the labels removed.
- [ ] (term guard) A trunk commit removing `## Teleport` from the glossary is refused, naming `alpha/pairing` and `alpha/host`; with both labels re-pointed or dropped in that commit, it passes.
- [ ] (read by label) `jig roadmap --label Teleport` prints `alpha/pairing` and `alpha/host` with their states and nothing else; a `No phase` item `q (labels teleport)` is listed too.
- [ ] (one of the filters) Whichever of this spec and phase-types lands second makes this pass: `jig roadmap --label teleport --state open` prints only the open ones of those, `--label teleport --phase alpha` only alpha's, and `jig roadmap --view --label teleport` prints a view of only the labelled work to stdout, writing no file. Until phase-types lands, `--label` alone passes the case above.
- [ ] (one reader) `split_labels` and `label_problems` are the only places jig.py reads `(labels …)` or checks a label against the glossary (`grep -c '^LABELS = re.compile' plugin/templates/jig/jig.py` prints 1, and no other pattern in it matches `(labels`); ideas-log's entries call the same two.
- [ ] (no glossary) In a repo with no `docs/glossary.md`, any label is refused, naming the missing glossary.

Part A, in a family (`meta` with pararepos `pa` and `pb`, the fixture `sec_family` builds; `meta`'s glossary adds `## Teleport` with `` Owner: `pb` ``):
- [ ] (live) `meta`'s `Walyt alpha/pairing … (labels teleport)` commits on `meta`'s trunk; in `pa`, `jig roadmap --label teleport` lists it, headed `Teleport: owned by pb`.
- [ ] (unreachable) With `meta` removed from the repos file, a spec commit in `pa` passes with the warning naming `meta`.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh labels roadmap family rig` passes.

Part B, in the family fixture:
- [ ] (staged) A file in `pa`'s `.jig/staging/` with its mtime set 10 days back, and one fresh in `meta`'s: `jig family` in `meta` lists both with repo, target, kind and age, only the first `stale`. The same command in `pb` prints the same lines.
- [ ] (proposals) `pa` runs `jig propose --buffer z`, then the opening commit's date is set 9 days back (`GIT_COMMITTER_DATE` on a fresh opening): `jig family` lists `propose/pa-z` as `empty`, `stale`, cited by `pa`'s spec. A branch made by hand (`git branch propose/pb-old main`) is listed as empty and `cited by no spec`. Once `meta` merges a written `propose/pa-z`, it isn't listed.
- [ ] (entries) `meta`'s log has an `## Open` entry `Touches: docs/glossary.md § Teleport`: `jig family` lists it with `Walyt alpha/pairing` and `pa`. Once pairing is done, it isn't listed.
- [ ] (two names) `## Walyt alpha` scope `teleport` and `## Familiar App alpha` scope `teleport-clipboard`: listed as a pair. `teleport` and `pairing` aren't. Two glossary terms `Walyt pass` and `walyt-pass` are listed as a pair.
- [ ] (rig) `jig rig` in `meta` prints the `Family:` line with those counts, and its two numbers are what they are without it; with nothing stale or flagged, no `Family:` line.
- [ ] (unreachable) With `pb` removed from the repos file, `jig family` names `pb` and reports the rest.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh family_report family rig pararepo sync_buffer` passes.

Part C, in the family fixture:
- [ ] (pararepo edit) In `pa`, `jig roadmap --draft` prints the draft's path and `Walyt alpha`, `Walyt No phase`. Adding scope `z3 (labels teleport)` under `## Walyt alpha` there and running `jig roadmap --edit`: `meta` gains `propose/pa-roadmap-<date>` whose tip's roadmap has `z3` and differs from `meta`'s trunk only in `pa`'s sections; `meta`'s trunk and every checkout's HEAD are unchanged; `pa` has a new Open `BUFFER.md` row and `.jig/specs/roadmap-<date>.md` citing the branch, uncommitted; the draft is gone. `meta` reviews and merges the branch, and the merge passes `meta`'s hook; a spec in `pa` taking `Walyt alpha/z3` then commits.
- [ ] (one proposal at a time) A second `--edit` before `meta` merges adds a commit to the same branch and a row to the same spec. `jig propose --buffer` in `pa` afterwards doesn't take the roadmap rows.
- [ ] (another repo's line) A draft in `pa` changing a line under `## Familiar App alpha`, or under `meta`'s own `## Demos`, is refused by line, naming the heading and its owner, and nothing is written in either repo. So is a new heading `## Gadget alpha` naming no product `pa` owns.
- [ ] (hook's refusals first) A draft in `pa` with a ring, a ref to nothing, or a page `pa`'s trunk lacks is refused as the hook words it, and nothing is written.
- [ ] (label staged) A draft in `pa` adding `(labels walyt-mesh)`, a term `meta`'s glossary lacks: the branch's line has no `(labels …)`, `meta`'s `.jig/staging/label-walyt-mesh.md` exists with `target: meta`, `kind: doc`, `destination: docs/glossary.md` and names `Walyt alpha/<scope>` and `pa`; `jig staging check` passes on it.
- [ ] (metarepo edit) In `meta`'s trunk checkout, `--edit` of a draft changing `## Demos` writes `.jig/roadmap.md` there uncommitted, and the commit passes; a draft changing `## Walyt alpha` is refused, naming `pa`; a draft with a label the glossary lacks is refused, naming the glossary; `--edit` in a job worktree is refused (R5).
- [ ] (no clobber) With `.jig/roadmap.md` changed and uncommitted in `meta`'s trunk checkout, `--edit` there is refused, naming it.
- [ ] (stand-alone) In a repo with no metarepo, `--draft` then `--edit` writes trunk's checkout after the same checks.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap_edit family_report roadmap family rig pararepo metarepo sync_buffer staging boundary moves` passes, and so does `claude plugin validate ./plugin`.

## Out of scope
- Labels on specs: a spec reads by the labels of the scopes it takes (R2).
- Labels on phases (R6: "labels on scopes").
- A dependency on a label (R7).
- Interactive or per-field editing (`add scope`, `set after`): the edit is a draft file, so one
  command covers every change.
- Phase types, filters by phase type, and departures (spec phase-types); the ideas log (spec
  ideas-log); the conversion command for moving in (spec moving-in-command).
- A family on several machines: the report and the edit name a repo they can't reach, and
  nothing more, as cross-repo-roadmap's reader does.

## Touches
- `plugin/templates/jig/jig.py`:
  - Part A: `split_waits`/`repeated_waits`/`phase_waits` (a `labels` kind), `parse_roadmap`/`parse_section` (labels on scopes and items; a phase's labels line refused), new `split_labels`/`label_problems` (fold, glossary lookup; the one label reader and check, which ideas-log calls), `roadmap_rules` (labels on trunk; the term guard on a glossary change), `roadmap_full`/`roadmap_view`/`render_roadmap`/`cmd_roadmap` (labels shown; `--label`, one of phase-types' filters: `--product`, `--phase`, `--type`, `--state`, `--owner`, `--view`), `Family` (the glossary text it already reads).
  - Part B: new `cmd_family` and its readers over `repo_path`, `trunk_show`, `staged_files`, `proposal_empty`/`opening_commit`, `PROPOSAL`, the decision log's sections; `rig_state`/`rig_text` (the `Family:` line); the parser.
  - Part C: `cmd_roadmap` (`--draft`, `--edit`), the edit's section diff and ownership check over `product_of`/`Family.ours`, the checks `roadmap_rules` runs (called, not copied), `open_proposal`/`buffer_proposal` (a spec of roadmap rows only; `unproposed` leaving them out), a plumbing commit on the branch, the staged label file in `cmd_staging`'s header shape.
- `plugin/templates/jig/RULES.md`: Roadmap (Labels; Edits: the edit command), Metarepo and pararepos (the family report; a staged label), Workflow (rig's `Family:` line), Commands.
- `plugin/skills/hubnode/SKILL.md` (A roadmap change: in a family, `jig roadmap --draft`/`--edit`), `plugin/skills/rig/SKILL.md` (the `Family:` line), `plugin/skills/spec/SKILL.md` (step 5: an item's labels are the features it touches).
- `docs/records.md` (Roadmap: labels), `docs/metarepos.md` (the edit command, the family report), `docs/commands.md` (`jig family`, `roadmap --label`, `--draft`, `--edit`), `docs/glossary.md` (a `label` term).
- `tests/smoke.sh`: roadmap, family, rig, pararepo, sync_buffer; a new section `family_report` for Part B and `roadmap_edit` for Part C.
- Process or product: product (jig's behaviour), written in RULES.md, the skills and the docs pages as their homes.

## Alternatives considered
- Labels as a separate list in the metarepo (`## Labels` naming scopes per feature). Rejected: R7 has the scope name its labels, as it names its pages, and the glossary already is the naming scheme's home (R2: "naming schemes live in the meta"). Reason is [seen].
- Labels free-form, with no glossary check. Rejected: one label spelt two ways is the drift the owner's design exists to end, and a refused misspelling is cheap. Reason is [seen] (the inputs' "two names for one").
- Labels matched exactly as the glossary heading writes them. Rejected: scope ids are lowercase and hyphenated (R1, 1.2) while glossary headings are written as prose, so an exact match would make every label read like a heading. Reason is [assumed].
- Staging every label assignment for the metarepo hubnode. Rejected by the owner, 2026-11-23: "stage only a new label term; a repo tags its own scopes freely". Reason is [seen].
- The report inside `jig sync`. Rejected: sync runs on a pararepo's trunk at a pin bump; the owner asked for these at any time, from the metarepo too, and the report reads every member, not one pin. Reason is [seen].
- The report counted under rig's Waiting on you. Rejected: a stale file or a pair of names is a thing to look at, not a question; counting each would bury the real questions. Reason is [assumed].
- The edit writing a pending section into a tracked file in the pararepo until the next `jig propose --buffer`. Rejected: that is a second copy of the scopes, the drift cross-repo-roadmap removed; the unmerged branch is the buffer, as the owner's Q3 ruling ("a BUFFER row and `jig propose`, merged at the next sync the owner calls") reads. Reason is [seen].
- The edit command writing the branch in a metarepo worktree. Rejected: plumbing writes the commit without moving any checkout, as `open_proposal` already does. Reason is [seen].

## Decisions
- `(labels …)` is a fourth trailing parenthesis, peeled in any order with the other three, so no order hides a label as text, as `split_waits` already does for waits.
- The fold is case plus each run of spaces, `-` and `_` read as one `-`, the fold that makes a hyphenated scope-style label name a prose glossary heading.
- A stand-alone repo checks labels against its own glossary, so a repo that later joins a family keeps the same form.
- Stale is past 7 days, fixed, from the inputs' "staged items over a week old"; the age is printed whatever it is, so a nearer judgment needs no setting.
- A staged file's age is its file's modification time: staging is never committed, so nothing else dates it.
- One open roadmap proposal per pararepo: each edit adds to it until the metarepo merges it, so the owner merges a pararepo's roadmap edits in one step at the sync he calls.
- The edit replaces a pararepo's sections whole on the branch: no other repo writes them, so the branch never carries another repo's lines.
- The "two names" check is a heuristic for the owner to read, never a refusal; a pair judged distinct costs a line in a report, not an answer.
- Only a new label term is staged; a pararepo puts an existing label on its own scope in its edit. The owner, 2026-11-23: "stage only a new label term; a repo tags its own scopes freely".
- Interpreted (the hubnode), confirmed by the owner, 2026-11-23: "keep: start from the open proposal": in a pararepo with an open roadmap proposal, `--draft` and `--edit` start from the metarepo's trunk with this repo's sections as that branch has them, so a second edit keeps what the first wrote there. Rejected: trunk as the base, as item 8 reads, since the edit replaces this repo's sections whole on the branch and would drop the pending buffered lines, breaking the owner's buffer-and-sync ruling (Q3).
- `marketing/FEATURES.md` rows, for the hubnode to add before the work starts:
  - | Roadmap labels (`(labels …)`, `jig roadmap --label`) | A scope or a `No phase` item names the features it touches, `(labels <term>, …)`, each a term of the family's glossary (the metarepo's; a stand-alone repo's own), matched with case and spacing folded. The hook refuses a label naming no term and a glossary change dropping a term a label names. `jig roadmap` and the view show labels; `--label <term>` lists the work carrying one across products, with the term's owner. | Owner's design for maige-ecosystem, R1–R3, R6, R7 (2026-11-19); the owner, 2026-11-23: "everything including labels"; `.jig/specs/roadmap-labels.md` | A repo needs to tell its own work from work leaning on another repo's feature; ownership already lives on glossary terms, so a label read against them answers it, and a misspelt label is refused instead of drifting. | A dependency (R7: labels need none), a state, or an order. GitHub-style free tags. Labels on specs or phases. |
  - | Family report (`jig family`) | From a metarepo or any of its pararepos: every staged file across the family with its age; every unmerged `propose/` branch in the metarepo with its age, empty or not, and the specs citing it; pending decision entries touching labelled work; two names for one thing. `jig rig` points at it with one line. | maige-ecosystem inputs, 2026-11-19 (stale staged files and proposals, two names for one); bug-empty-proposal's deferred metarepo report; `.jig/specs/roadmap-labels.md` | A proposal and two staged requests sat for weeks unseen, and one piece of work went by three names across repos; nothing read the family as a whole. | A refusal or a question: it reports. A scheduler. A cross-machine reader. |
  - | Roadmap edit command (`jig roadmap --draft` / `--edit`) | Edits the roadmap a repo plans from through a draft file: refuses a line under another repo's product and anything the hook would refuse; in a pararepo buffers the edit as a `BUFFER.md` row and a commit on its open `propose/` branch in the metarepo, without moving a checkout; stages a label the glossary lacks for the metarepo's hubnode. | Owner's rulings on cross-repo-roadmap, 2026-11-21 ("hubnodes … should buffer the changes and use the regular sync process"); the owner, 2026-11-23: "everything including labels"; `.jig/specs/roadmap-labels.md` | A pararepo's roadmap edit took a BUFFER row, a proposal and a hand edit on a metarepo branch, with nothing stopping a line under another product. | An editor or per-field CLI. A way to write the metarepo's trunk from a pararepo. |

## Open questions for the owner
1. Answered by the owner, 2026-11-23: "stage only a new label term; a repo tags its own scopes freely" (Decisions).
2. Answered by the hubnode, 2026-11-23: `--label` stays here as one of phase-types' filters, the same flag shape; whichever spec lands second wires it in (Change, item 4).

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
