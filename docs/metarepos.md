# Metarepos

Some products are several repos: an app, its firmware, the hardware it runs on. They have to agree
on names, decisions and contracts. A [metarepo](glossary.md#metarepo) holds those shared things,
as docs only. Each [pararepo](glossary.md#pararepo) cites it at a released tag. The metarepo
points, and nothing copies it.

## Setup

`python3 .jig/jig.py init --meta` makes a repo a metarepo. Its pages sit in genre folders under
`docs/`, declared at init: products, features, principles and concepts, or your own.
`python3 .jig/jig.py init --para <metarepo>` makes a repo a pararepo of it, pinned to a release.
Its `--contract` globs name the files whose changes the metarepo has to hear about.

Three rules do the work:

1. A pararepo writes to the metarepo only by branch, through `python3 .jig/jig.py propose`.
2. The metarepo holds no code, and no copy of a pararepo's content.
3. Only `python3 .jig/jig.py release` tags, so a pin never names a release that failed its checks.

## Citations

A pararepo cites the metarepo as `<metarepo>/<path> § <heading>`, or a decision as
`<metarepo>/.jig/decisions.md § D-012`. Each claim has one home and is stated only there.
Everywhere else is a pointer to it. A question the pararepos have to wait on is an idea in the
metarepo's `.jig/ideas.md`, cited the same way before it's answered, and it keeps its id when
it's decided.

A claim lives in the metarepo when another repo has to agree with it or build against it.
Otherwise it lives with its one owner, and the metarepo points there.

## Sync

`python3 .jig/jig.py sync`, on a pararepo's [trunk](glossary.md#trunk), checks every citation against the pinned
release. It names a page the metarepo moved, a heading it renamed, or a decision it dropped. A
change to a decision asks every page that cites it whether it still holds.

When the metarepo releases, it stages a pin-bump request in each pararepo whose citations the
release broke, with the list of rewrites.

## Proposals

A pararepo changes the metarepo by proposal, written up first as a [spec](glossary.md#spec). `python3 .jig/jig.py propose <spec> <slug>` opens a
`propose/<repo>-<slug>` branch on the metarepo with the change on it. The metarepo's owner
merges it and releases. A [job](glossary.md#job) whose spec waits on a proposal doesn't pass its [gate](glossary.md#gate) until the
pinned release holds it.

`python3 .jig/jig.py propose --withdraw <branch>` takes back a proposal the metarepo will never release.

## The buffer

A pararepo may work ahead of its metarepo while behavior settles. It can change what a metarepo
claim describes, as often as testing needs. Every such difference is a row in
`.jig/ledgers/buffer.md`: the claim at the pin, what the repo does now, who decided, and Open or
Closed.

Before its build, the pararepo's release puts every Open row into one metarepo proposal, except the
row `jig move-in` keeps for itself. When
the metarepo releases it, the pararepo's next sync moves the pin and closes those rows in one
commit.

## Moving claims

A claim found to have only one owner moves to it: down to a pararepo, up to the metarepo, or
sideways to another pararepo. The receiving repo lands the text first, with a line in its log
saying where it came from. Down or sideways it arrives through [staging](glossary.md#staging) and
a job there; up it's a proposal. Then the sending repo removes its copy, with a line saying where
it went. The hook refuses that line until the receiver has its own. Old citations keep resolving
through it. `python3 .jig/jig.py move <what> --to <repo>` does both steps, one per `--apply`.
The removal runs in a job opened from the move's spec, in any repo, and that job's merge closes
the spec. A moved page's roadmap items go with it, unless a spec took them or left them for
later. If the receiver drops what was sent, its owner says so, and deleting the move's spec lets
step 1 send it again.

A pararepo with a [roadmap](glossary.md#roadmap) of its own can move it into the metarepo's, once, on the owner's yes.
`python3 .jig/jig.py move-in --product <Name>` does it in two steps, one per `--apply`. First it proposes the
pararepo's [phases](glossary.md#phase) under the product's name, with the product's glossary heading (`Repo:` and `Kind:`) when the
metarepo has none yet, on one `propose/` branch. The metarepo's hubnode decides the name and the
phases together when it merges that branch. Then the pararepo's roadmap leaves, with every `Scope:`
line pointed at the metarepo's ids. After that, the metarepo holds the one roadmap for every
product it lists.

## Editing the roadmap

`python3 .jig/jig.py roadmap --draft` writes the roadmap a repo plans from to a draft outside its
tree, and `roadmap --edit` checks it and writes it. A pararepo may change only its own products'
sections. Its edit lands as a `buffer.md` row and a commit on its open roadmap proposal in the
metarepo, so nothing moves on the metarepo's trunk until its owner merges it at the next sync. A
label the metarepo's glossary lacks is left off and staged there as a new term.

## The family report

`python3 .jig/jig.py family`, run in the metarepo or any of its pararepos, prints the same
report from either: every file waiting in each repo's staging folder, with its age; every
`propose/` branch the metarepo hasn't merged, with its age, whether anything is written on it,
and the specs citing it; each pending decision entry touching a term that labels work not done;
and names that may be one thing under two. A file or a proposal older than a week is marked
stale. It writes nothing. `rig` prints one line pointing at it when there's something to see.

## Design sessions

A [designer](glossary.md#designer) is a design session for one product repo, kept outside it. It
keeps the owner's running record of the product and drafts what the repo will get. It reaches
the repo only by staging files and writing to its [inbox](glossary.md#inbox). A metarepo has no designer of its own:
its pararepos' designers stage to it.
