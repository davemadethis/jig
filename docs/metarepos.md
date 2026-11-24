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
Everywhere else is a pointer to it.

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
`.jig/ledgers/BUFFER.md`: the claim at the pin, what the repo does now, who decided, and Open or
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
through it.

A pararepo with a [roadmap](glossary.md#roadmap) of its own can move it into the metarepo's, once, on the owner's yes.
`python3 .jig/jig.py move-in --product <Name>` does it in two steps, one per `--apply`. First it proposes the
pararepo's [phases](glossary.md#phase) under the product's name, with the product's glossary term when the
metarepo has none yet, on one `propose/` branch. The metarepo's hubnode decides the name and the
phases together when it merges that branch. Then the pararepo's roadmap leaves, with every `Scope:`
line pointed at the metarepo's ids. After that, the metarepo holds the one roadmap for every
product it lists.

## Design sessions

A [rigger](glossary.md#rigger) is a design session for one product repo, kept outside it. It
keeps the owner's running record of the product and drafts what the repo will get. It reaches
the repo only by staging files and writing to its [inbox](glossary.md#inbox). A metarepo has no rigger of its own:
its pararepos' riggers stage to it.
