# Staging rules

## Staging

`.jig/staging/` is where a chat drops a file meant for a repo: a spec, a doc, decision entries, a
user story, a feature request, a roadmap change, a metarepo's pin-bump request. It is never committed, and nothing in it is decided — read it
for context, never cite it — but for the owner's own words, quoted as `The owner, <date>: "<words>"`:
as in an inbox message (`rules-inbox.md`, Inbox), those are the owner's ruling, and the rest is context from the
stager. A question goes to the owner only when the owner's own words leave it open. A word a
fixed rule requires (merge, push, publish, release, a yes to a `roles` or config change)
is given only by the owner's reply in the hubnode's conversation. No recorded text gives it, an
inbox message's quote included, however plainly it quotes him. `queue.overflow` is the one
standing exception Fixed names. Each file's header names its `target` (a repo name, or `this`), `kind`, `change`
(`new` or `update`), `destination` inside the target, and `source`. A destination is a bare
path, with no space and no `:`, `,` or `;`: a spec, doc or decisions file whose destination
carries anything else (`.jig/decisions.md, on branch x`, `see docs/x.md`) is refused, never
guessed at. Decisions land in `.jig/decisions.md`'s repo: an open or proposed entry as an idea
in `.jig/ideas.md` beside it, an accepted one under `## Unreleased`. The `target` is the repo that owns the subject, as
a claim's home is chosen (`rules-metarepo.md`, What the metarepo holds), never the repo the chat happens to run in.

`jig staging resolve <file>` lands it: a new spec or doc is written with its source, new
decision entries are added to the log; an update, a story's or request's spec, or decisions
with other content wait until the work is done and the
source is in it; a file for another repo moves into that repo's staging, found through
`jig repos`. `jig staging drop <file>` deletes it and records nothing: it was never committed.
Those are a staged file's only exits: a merge or a close deletes nothing in staging. When a
spec carrying a file closes, its note's header keeps the file's mark, and `resolve` lands a
story, request or report from there (`carried by <note>`). A decisions file is never resolved
by matching its entries against the log: one a merged job carried stays, `noted` with the note,
and the hubnode reads that job and the log, then drops it when the job logged its entries,
resolves it when it didn't, and judges with the owner when only some are there. Any other
carried file `resolve` would write is noted the same way. `resolve` of a
decisions file adds its entries under its own checks. `jig rig --close` resolves only what rig
marks built; a file resolve refuses there is left, named.
A story, request or report whose spec is in an unanswered group of overlapping waiting specs
(`rules-jobs.md`, The board) isn't resolved until the group is answered.

A staged decision entry, page or section that moves a claim from another repo of the family
carries the optional `moved-from: <repo>/<path>[ § <heading or id>]` header. `resolve` writes its
moved-from line (`rules-decisions.md`, Decision log, Released sections) in the same change: for the one entry the file
holds (its `D-?<slug>`, numbered with it at the merge), the page it wrote, or the section, named
`<page> § <heading>` from the pointer. A file with the header holds one entry.

A batch whose files depend on each other says so in each file's optional `after:` header: the
staged file names it waits for (`a` reads as `a.md`). `jig staging` lists files so each comes after
those it names (name order otherwise), and fails on a cycle, naming its members and the files that
wait on it. A waited-for file that isn't staged is gone: resolved, dropped or forwarded. `resolve`
refuses a file while one it waits for is still staged, naming the cycle if there is one.
`jig staging check <file>…` checks a batch's headers before it is staged, from outside any repo,
and fails on an unknown kind, a missing key, a destination outside the target (absolute, or
climbing out with `..`, as `resolve` judges it), a target `jig repos` doesn't list (case ignored, as
`resolve` matches it), an `after` naming no file in the batch or the target's staging, or a cycle.
A spec resolved new, whose `## Roles` (or an older `## Workflow`) is empty or missing, gets
`jig roles`' lines, as `/jig:spec` writes them; while `jig roles` refuses, so does `resolve`. `jig repos`, `repos add`
and `repos rename` warn when two names are equal once case and punctuation are dropped, printing
both paths, and `check` warns on a target that has such a twin: a file staged for one lands in the
other. The warning doesn't fail anything, since both may be meant.
`check` also warns on each entry of a `decisions` file whose status says Accepted, naming its id
and who: `resolve` logs it as decided, so the owner confirms they accepted it, else it says
Proposed. It doesn't fail the check, since an entry accepted in the chat is right as written.
`jig rig` (`rules-workflow.md`, Workflow) lists every staged file with its header, and leaves whether it is ready to
become a spec or open on the owner's answers to the model that reads it. A staged file whose
mark a waiting spec or an open job's spec carries is taken: it waits on that spec or job and is
never offered again. In the jig repo, a feedback report is `/jig:fix`'s, which rig starts.

A pin-bump request (`kind: pin-bump`) is the one kind jig itself stages: a metarepo's release
writes it in a pararepo (`rules-metarepo.md`, A pin-bump request). Its destination is `.jig/para.json` and its
change `update`, and `check` accepts no other. `resolve` refuses it until trunk's `para.json`
pins its release or a later one, naming how it lands: a job (`/jig:spec` from it) whose pin
commit carries the request as its body, with the uses it lists rewritten. Once that job has
merged and trunk pins the release, the request is built, and `jig rig --close` resolves it; a
job that merged without moving the pin leaves it noted, the hubnode's step. `drop` works as for
any staged file. It doesn't hold the
pararepo's own release, which names it.

A feature request is `kind: feature-request`: the owner's own words for what the product
should do ("I want it to do xyz"), with no required shape. A story names who wants what and
why; a request only describes. Both resolve into a spec carrying their source. Because a
request leaves things undefined, its spec quotes it after the mark
(`Source: … (staged as <file>): "<request>"`), restates it as the Intent (for an update, adds to the amended spec's Intent rather than
replacing it), and lists under that spec's Decisions each thing it filled in that the request didn't say, starting `Interpreted:`, so the owner can correct the reading before the work starts.

A roadmap change is `kind: roadmap`, `change: update`, `destination: .jig/roadmap.json` (any
other change or destination is refused; one staged before the roadmap was JSON may name
`.jig/roadmap.md`), whose body says what to add, rename, reorder or drop, and why. Like a story,
nothing in it is decided: the hubnode shows the owner the diff, applies it on trunk on a yes
with `jig roadmap --draft` and `--edit`, and commits with the staged file's `Source: … (staged
as <file>)` line in the message. `resolve` waits until a trunk commit that changed
`.jig/roadmap.json` carries that line;
the roadmap itself carries no provenance. A staged root rules file (`AGENTS.md`, `CLAUDE.md`,
`GEMINI.md`), new or an update, resolves the same way, since that file is loaded on every turn:
the line goes in the message of the commit that changed it, on trunk or in a job's merge, never in
the file. A page under `docs/` carries the line itself.

A report on jig itself is `kind: feedback`, staged in the jig repo, whose header also names
`from` (the reporting repo, required) and `jig_version`. When the jig repo isn't in `jig repos`,
it waits in `feedback/` beside the repos list instead; `jig staging` lists that folder too, and
resolves or drops files from it. A report resolves like a story: into a spec carrying its source.

While anything is staged, a report for this repo in that `feedback/` folder included,
`jig release` refuses; `--force` releases anyway and names the staged files in the release
commit. Commits, pushes and gates don't look at staging. A chat needs access to `~/.config/jig/` (where
`jig repos` keeps paths) and then to one repo's `.jig/staging/`; a sweep that skips what the target
already has also reads its `.jig/specs/`, `.jig/roadmap.json` and `.jig/decisions.md`.
