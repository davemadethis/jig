# Pararepo rules

These are a pararepo's rules. What its metarepo is and holds is in the metarepo's `.jig/rules/rules-metarepo.md`.

## Pararepo

A **pararepo** (code, firmware, hardware) cites its metarepo at a released tag. One of the metarepo's three rules binds it:

1. A pararepo writes the metarepo only by branch, via `jig propose`. That `propose/` branch is
   on no job by design, so R2 lets it commit while the metarepo has jobs open; R1 still keeps
   the trunk checkout off it.

One thing is read live instead of at the pin: the roadmap (`rules-roadmap.md`, Roadmap, Products and One reader).
It is the plan, not a claim, so no release carries it, and a pararepo planning from it reads
the metarepo's trunk.

A pointer is checked from the pararepo's side, in what it caches: `jig sync` and its release report
each one whose file or heading (`§`) the pararepo doesn't have, and P2 asks a commit that leaves one
dangling for what a contract change needs. A pointer is `<repo>/<path>` or `<repo>:<path>`, best
written in backticks (`` `app/docs/ui.md § Build (release)` ``): there the section is the span's
text, matched whole; in prose it is any heading the text after `§` begins with. A section that
starts with a number, `2` or `2.1`, names the heading whose leading number is exactly that: `§ 2` is
`## 2. Motes`, not `### 2.1` or `## 20`, and words after the number aren't compared. Headings are
compared as read, code and emphasis marks dropped. The name folds case (`App/…` is `app/…`); the
path and heading don't. A superseded or rejected decision row isn't checked.

### Moving a claim

A claim found to have one owner moves to it, released or not, in any direction: down from the
metarepo to a pararepo, up from a pararepo to its metarepo, or sideways between two pararepos
of one metarepo. The receiving repo lands the text first, with its moved-from line: down or
sideways through staging (`target: <repo>`, `moved-from: <pointer>`) and a job there, up by a
`propose/` branch in the metarepo. Its entry keeps who and date and drops a `Supersedes` of the
sending log's ids, since that chain stays there. The sending repo then removes the entry, page
or section with its move line (`rules-decisions.md`, Decision log, Released sections), in one commit, which the hook
refuses until the receiver's trunk has the moved-from line. Frozen citations of the old id keep
resolving through the line, so nothing released is rewritten. A metarepo pointer to a page or
section a pararepo moved away reads `(moved: <pointer>)` in `jig sync`, the release and P2,
never as missing. The answer is a removal's: the metarepo's rewrite as a pointers proposal
(`jig propose --pointers`), or a `buffer.md` row. A pararepo bumping its pin past such a release
reads the pointer's new home in the pin-bump request.

`jig move <what> --to <repo> [--as <path>]` does both ends, one step per `--apply`; without it,
it prints each step's state and what the next would write, read from the repos each run. `<what>`
is an entry id, a page, or `<page> § <heading>`; `--as` is the page's path there (the same path by
default). Step 1 writes `.jig/specs/move-<slug>.md` here, the job that removes the claim, its
Touches the moved thing alone (the move line is a log append any job may make), and
sends the text with its `moved-from:` pointer by the route for its direction: a file staged with
`target: <repo>` and forwarded down or sideways (an entry as `### <their prefix>?<slug>`, who and
date kept, a `Supersedes` of this log's ids dropped); up, a `propose/<repo>-move-<slug>` branch in
the metarepo whose one commit, the entry or page with its moved-from line, the metarepo's hook
judges, recorded as `meta: <meta> proposal <branch>` with the metarepo's own citations of it
listed. Step 2 waits for the receiver's trunk to hold the moved-from line, its id numbered; it
then removes the entry, page or section here and writes the move line, staged in the job opened
from the move's spec, in any repo: in a trunk checkout it is refused, naming that job (in a
metarepo, M4). `jig merge` closes the spec as it closes any job's, keeping it in a pararepo while
it names a metarepo branch. The spec's `- move:` and `meta:` lines are the move's record, found
by scanning specs: a withdrawn up proposal is proposed again under the next free name, and down
or sideways, step 1 is done once its spec records the move. What the receiver does with the file
is its owner's: the plan says whether it is still in the receiver's staging, and a drop is the
owner's word, given by deleting the move's spec, after which step 1 sends it again. Sideways from a
pararepo, step 2 also writes, from the metarepo's trunk once the receiver holds the thing, the
metarepo's rewrites of its pointers to the moved thing (an entry's by its landed id, a section's
and a page's by the landed path; every other pointer into that page or log stays) and its roadmap
items, on `propose/<repo>-move-<slug>-pointers`, recorded as `meta: <meta> pointers <branch>`,
which P2 accepts; with nothing to propose, the spec answers P2 with `meta: none — <meta> names
nothing of <pointer>; it moved to <pointer>`.

A moved page's roadmap items follow it. An item a spec or note takes stays, the page dropped from its `touches`; any other goes to the receiver's plan, in its phase of the same name, else its
No phase list: the receiver's product section of the metarepo's roadmap, the metarepo's own
phases when it moves up, or, for a receiver keeping a roadmap of its own, a `kind: roadmap` file
staged in the sender's main checkout, unforwarded until the job merges, when `jig staging
resolve` forwards it. The metarepo's roadmap changes only by its own merge or a `propose/` branch:
a page moving up takes its items in step 1's proposal, and sideways in step 2's pointers proposal,
whatever roadmap the sending pararepo keeps; no roadmap file is staged to it. The losing roadmap
changes by its own route: in a pararepo planning from the metarepo, in the step's proposal;
otherwise `jig merge` moves the items in the job's merge commit, read from the move lines the
merge adds, as it re-points a renamed page.

### Its own and the metarepo's decisions

A superseded entry, and a released section's change lines, are history: their paths aren't pointers,
and this repo's own released lines aren't checked as citations. `jig sync` and the release say when
the pinned release has been yanked, with its line.
A citation of an id reads it in either file at the pin, so an idea folded or decided keeps every
citation; `jig sync` reads one decided `<id> (accepted)`.
A pararepo's own entry that touches a contract cites its BUFFER row or proposal; once the metarepo
accepts it, a new entry here supersedes it and points to the metarepo's id without restating it.

### Gates

A pararepo's gates are on only when `.jig/para.json` is on trunk; `jig init --para <metarepo>` writes it and the pararepo's header in `AGENTS.md`, whose lines are jig's (P1).

| Gate | Refuses |
|---|---|
| P1 | an `AGENTS.md` header that differs from what `.jig/para.json` generates |
| P2 | a contract-path change (an edit, a delete, or a rename from one) with none of: a row added or changed in `.jig/ledgers/buffer.md` in the same commit, or a spec saying `meta: buffered <row id>`, `meta: <name> proposal <branch>`, `meta: <name> pointers <branch>` or `meta: none — <reason>` (a spec the change touches, or the job's own: the board's `spec`, read as trunk has it, a one-line spec being its own text; in a merge, the one job whose branch tip is what is merged in, or whose own first-parent line holds it, and none for an octopus); the same for a change that deletes or renames a file a cached metarepo pointer names, or the heading its `§` names; a lost file counts even when its heading was already missing. Also, in `buffer.md`: a state other than `Open`, `Closed` or `Closed (answered in <release>: <reason>)`, a repeated id, an `Open` row deleted, or one closed with its other cells changed, in a commit that changes a contract path, or by anything but `jig sync`: a `Closed` row needs the pin to hold a proposal that carried it as it stands (checked against the metarepo's checkout), an answered one a release at or below the pin |
| P4 | a contract-path change while a file targeting the metarepo is staged |
| P3 | the metarepo's cache (`.jig/meta-cache/`) or its checkout committed into the pararepo |

A pararepo pins a release, never `main`, and bumps it in a commit of its own, `meta: <name> v0.3.0 →
v0.4.0`, with the report `jig sync` prints on its trunk as the body: each decision id and glossary
term that changed, and each entry file the new release moved (`<old> (now <new>)`) or removed
(`<old> (removed)`), with every file here that uses it, specs and ledgers included. A two-part pin
(`v0.3`), from before releases had three parts, keeps working: it sorts below `v0.3.0`.
`defer_until` in `para.json` is a date, `YYYY-MM-DD`: before it, the pararepo's `jig sync` reports
nothing upstream and no metarepo release asks it to move.

A metarepo release that breaks what this repo cites stages a pin-bump request here (the metarepo's `rules-metarepo.md`, A pin-bump request). A noted request (its job merged without moving the pin) is never dropped: the hubnode specs a job
that moves the pin.

`jig gate` refuses a job whose spec cites a proposal that isn't in the pinned release, and one whose
`pointers` branch isn't on the metarepo it names (one merged into its trunk counts, released or
not), or names another metarepo; a metarepo it can't reach refuses too.

**Pointers ahead of the metarepo.** `meta: <name> pointers <branch>` (`jig propose --pointers`)
means the metarepo's pointers into this change are being rewritten on that metarepo branch, and
no metarepo claim changes. A job answered that way merges without waiting for the release:
cached pointers dangle against the pending branch until the pin moves, and `jig sync` and the
release report them meanwhile. A claim change is a `buffer.md` row; a dependency on a metarepo
change is `proposal <branch>`, which the gate waits for. P2 can't tell a pointer move from a claim
change, so review holds a `pointers` spec to this sentence.

**The sync buffer.** A pararepo may work ahead of its metarepo: change what a metarepo claim
describes, as often as testing needs, and commit and push each change. Every such difference
is a row in `.jig/ledgers/buffer.md` (the first row creates it from jig's ledger template): the
claim at the pin, what this repo does now, who decided, and a state, `Open` or `Closed`. A change
of mind edits the row. `jig release` in the pararepo, before its build, puts every `Open` row
no proposal carries yet, as it stands, but a move-in row (`jig move-in`'s alone), into one metarepo proposal (`jig propose --buffer`, also
run by hand): one branch, and a spec here that lists and copies the rows under `## Buffer rows`.
A row edited after it was proposed goes again in the next one. When the metarepo releases a
proposal, `jig sync` on the pararepo's trunk makes the pin commit itself: it moves the pin to
that release and marks `Closed` the rows the proposal carried that are unchanged since, in one
commit `meta: <name> v0.3.0 → v0.4.0` (or, when the pin already holds the release, `meta:
<name> v0.4.0: close B1`). Rows added or edited after the proposal stay `Open` for the next one.
A claim the metarepo answered by some other change, its proposal never released, closes on the
owner's word: `jig sync --answered B1,B2 --in <release> --reason <text>`, on trunk, with the pin
at or above that release, writes `Closed (answered in <release>: <reason>)` in each row and
commits it alone, refusing while a merge, cherry-pick, revert or rebase is in progress there. jig checks the release, not the claim: the reason is the owner's, as
`meta: none — <reason>` is. A proposal the metarepo will never release is withdrawn:
`jig propose --withdraw <branch> --reason <text>` rewrites its spec's line to
`meta: <name> withdrawn <branch> — <reason>`. Sync and gate stop waiting on it, it answers no
change, and the rows it carried that are still `Open` go again in the next proposal, a move-in
row by `jig move-in`. Its branch
in the metarepo is the metarepo's to delete. A proposal a release already holds can't be withdrawn: the
pin moves instead, and sync closes its rows. One withdrawn and released anyway, sync names, with
the `--answered` that closes its rows. Sync names a buffer proposal that carries no `Open`
row as one to withdraw. `jig propose` opens its branch with a commit of its own, so the
metarepo's list of unmerged branches shows it from the start; sync names a proposal with nothing
written past that as empty, with the date it was proposed.
`jig sync` also names each file here that a decision at the pin cites and `contract_paths`
doesn't cover. A path under a folder counts bare or after this repo's name; a root file every
repo has (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `README.md`, `CHANGELOG.md`) counts only after
this repo's name, since named bare it is about every repo. A decision may cite this repo by name in any case (`App/docs/ui.md`); the path
after it is exact. The line asks: the hubnode puts it to the owner with what the decision says,
and adds the path only if the decision describes something this repo can change there.

**A staged label.** A pararepo's roadmap edit naming a label the metarepo's glossary lacks
stages `label-<term>.md` in the metarepo's `.jig/staging/` (`rules-roadmap.md`, Roadmap, Edits): a `kind: doc`
update to `docs/glossary.md`, the metarepo hubnode's, since a new term is. The label is added
by the pararepo's next edit once the term lands. A repo puts an existing term on its own
scopes freely.

**Citing the metarepo.** A pararepo cites the metarepo the way the metarepo points to it:
`<meta>/<path>` (or `<meta>:<path>`), with `§ <section>` for a heading, matched as above. On
every run, `jig sync` and the release name each citation in this repo's tracked files, specs and
ledgers included, whose file or heading the pin doesn't have, and each bare path that names an
entry file at the pin and no file here, as `write it as <meta>/<path>`. A cite of the metarepo's
roadmap (`<meta>/.jig/roadmap.json`) is read on the metarepo's trunk, not at
the pin: it is project data no release holds, so a pin bump never changes it. Handoffs, `Closed`
BUFFER rows and a buffer proposal's copies of the rows it lists are left out: they cite the pin
they were written at. Reported; nothing refuses.
