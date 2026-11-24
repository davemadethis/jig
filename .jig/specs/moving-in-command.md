# moving-in-command: `jig move-in` converts a pararepo's roadmap, and `jig move` moves a claim in any direction, both ends

Source: Dave (owner), 2026-11-23, in the jig hubnode session, on finding that cross-repo-roadmap and move-to-pararepo deferred parts of his agreed end state without his yes: "end state was supposed to mean exactly that: everything including labels." Build all of it. This spec covers the conversion command (cross-repo-roadmap, Out of scope: "A **conversion command** for moving in") and move-to-pararepo's deferred claim moves (its Out of scope: "Moving a claim up, or between two pararepos", "One command that does both ends", "A record on the receiving side").

Kept separate from roadmap-labels: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from ideas-log: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from phase-types: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from bug-deferred-scope: the owner, 2026-11-23: "start what you can in parallel"

## Intent
A pararepo moves its roadmap into its metarepo with one command, `jig move-in`, instead of four
steps by hand. Any claim (a decision entry, a page or a section) moves from one repo of a family
to another with one command, `jig move`: down from the metarepo, up to it, or sideways between
pararepos. The receiving side records where the claim came from, and the hook checks that both
ends name each other. Each step that crosses repos stays a proposal the owner approves: a file
staged in the other repo, or a `propose/` branch in the metarepo. No command writes another
repo's trunk (cross-repo-roadmap, Owner's rulings: "buffer the changes and use the regular sync
process"). Both commands run one step at a time. Without `--apply` a command prints every step
with its state (done, next, or waiting on whose yes) and what the next step would write. With
`--apply` it does the next step only, so the owner's yes sits between steps.

## Givens (trunk 06550ea)
- [seen] Moving in by hand is four steps (RULES.md, Roadmap, Moving in). smoke `pararepo` family D
  does them: a glossary term planted in meta; a BUFFER row and `jig propose --buffer move-in`; the
  sections written on `propose/pd-move-in` and merged; `git rm .jig/roadmap.md ROADMAP.md` with
  each `Scope:` line re-pointed by `sed`. `moving_in` (jig.py:11481) checks the last commit, and
  `roadmap_rules` refuses a new roadmap afterward.
- [seen] `open_proposal` (jig.py:9428) makes a `propose/` branch in the metarepo without a
  checkout. `buffer_proposal` (jig.py:9471) puts every Open row of the buffer into one proposal.
  `forward` (jig.py:10011) moves a staged file into another repo's staging, "the one place jig
  writes in another repo".
- [seen] The move line (`MOVE_LINE`, jig.py:6056) is checked by `move_rules` (jig.py:6146). That
  check is called only with the metarepo's `meta.json` (jig.py:558), and it refuses any repo
  not in `pararepos`. So today a claim moves down only (RULES.md:1456).
- [seen] `moves_in` reads a log's move lines into one map. `hold_chain`, `cmd_decision`,
  `meta_citations`, `changes_report` and `boundary_rules` read that map (jig.py:6452, 6503,
  8818, 8913, 11293). Nothing records the move on the receiving side.
- [seen] `number_placeholders` (jig.py:6353) numbers a `D-?<slug>` in every file the merge
  changes, so a change line naming the placeholder is numbered with its entry.
- [seen] `dangling` (jig.py:9131) lists the metarepo's cached pointers that miss this
  pararepo's HEAD. sync, the pararepo's release and P2 read it.
- [seen] `HEADER_KEYS` (jig.py:9484) are the staged header's required keys. Optional keys such
  as `after:` exist beside them.
- [assumed] Every repo of a family is reachable on one machine through `jig repos`, as
  cross-repo-roadmap assumed. A repo that can't be reached is named, and the step that needs it
  waits.

## Change

Three parts, in build order. Each part merges alone and hands off `--partial`, except the last.

**Part A: `jig move-in --product <Name> [--apply]`**, run in a pararepo's trunk checkout. It
refuses in any other repo, in one with no `.jig/roadmap.md` on trunk, and when the metarepo can't
be reached, naming the repo.

1. **The product and its phases are proposed, in one proposal** (the owner, 2026-11-23: "carry
   the term in the same proposal (one yes)"). A `<Name>` term the metarepo's trunk glossary
   gives to another repo is refused, with its owner named. A `## Up next` here is refused,
   naming `jig update --apply`. With no `<Name>` term on the metarepo's trunk, the proposal
   carries it: `## <Name>`, the sentence `--definition "<text>"` gives (refused without it,
   naming the flag), and `` Owner: `<repo>`. ``, with a log line under `## Unreleased`
   `### Added` for it (M3), so the branch's subject leads with `GLOSSARY:` (M6). A term already
   giving `<Name>` to this repo is left alone. The metarepo's hubnode decides the name, the
   definition and the phases together at the one merge, and may change any of them on the
   branch before it (RULES.md, Edits). The mapping: each `## <phase>` becomes
   `## <Name> <phase>`, unless its leading words are already a term the glossary says this repo
   owns, in which case it stays as it is. `## No phase` becomes `## <Name> No phase`. Each ref
   in `(after …)` and `(needed by …)` is rewritten by the same map. Every other line is kept
   verbatim: notes, `Exit when:` boxes, scope text, `(touches …)`, and anything else a scope
   carries. A mapped heading the metarepo's roadmap already has is refused before anything is
   written, with each one named. `--apply` does three things:
   - adds one BUFFER row (`meta/.jig/roadmap.md § <Name>: none yet | its phases and list, moving
     in | owner, <date> | Open`);
   - opens `propose/<repo>-move-in` as a buffer proposal carrying that row only, listed in
     `.jig/specs/move-in.md`;
   - appends the mapped sections to the metarepo's roadmap on that branch, with the glossary
     term and its log line when the proposal carries them, in one commit made in a temporary
     worktree of the metarepo that it then removes. The metarepo's hook checks that commit,
     reading the branch's own glossary for the product headings.

   The branch waits on the metarepo's owner. Its hubnode merges it in a job (`## Proposals`).
   On trunk, the hook reads the commit's own glossary for a heading's product, as it reads the
   commit's own roadmap, so a term and the phases it owns land in one merge.
2. **Its roadmap leaves.** This step needs every mapped scope and list id on the metarepo's
   trunk. One the metarepo lacks (the owner changed it before merging) is named, with each spec
   and note that takes it. `--apply` runs `git rm` on `.jig/roadmap.md` and `ROADMAP.md`,
   rewrites each `Scope:` line in tracked specs and handoff notes by the map, and stages it all.
   The hubnode commits it on trunk on the owner's yes, and `moving_in` checks that commit as it
   does today. An id left unmapped stays for the hubnode to re-point by hand, and the hook
   refuses the commit until it is.

After step 2, `jig move-in` prints that the repo has moved in.

**Part B: a moved claim's record at both ends, in any direction**
4. **The moved-from line.** The receiving repo's log records where the claim came from. It is
   a line under `## Unreleased` `### Added`: `- D-016: moved from <repo>/.jig/decisions.md §
   E-085.`, `- docs/battery.md: moved from <repo>/docs/products/walyt/battery.md.` or
   `- docs/walyt.md § Mods: moved from <repo>/docs/products/walyt/walyt.md § Mods.`. It mirrors
   the move line: one form for ids, pages and sections, and frozen once released. A
   `D-?<slug>` written there is numbered with its entry at merge. One reader, `moved_from_in`,
   reads it the way `moves_in` reads move lines.
5. **Moves in any direction.** The repo losing the claim writes the move line, as it does now.
   That repo may be:
   - a metarepo, moving to one of its `pararepos` (down);
   - a pararepo, moving to its metarepo (up);
   - a pararepo, moving to another pararepo listed in its metarepo's trunk `meta.json` (sideways).

   A move line in a repo with no family is refused. `move_rules` runs in every family member,
   with the existing checks over the family's repos.
6. **The hook ties both ends.** It refuses an added move line whose target repo's trunk has no
   moved-from line naming this repo's thing ("land it there first, with its moved-from line"). It
   checks an added moved-from line too:
   - the repo must be one of the family;
   - on that repo's trunk the source must still be there (the move is pending), or that repo's
     move line for it must point here;
   - if neither holds, it is refused, naming the file it read;
   - if the repo can't be reached, it passes with a warning.
7. **Readers.**
   - `jig decision <id>` prints `moved from <pointer>`, and `jig reading-list --claims <id>`
     names it in its note.
   - In a pararepo that lost a claim, `hold_chain`, `jig decision` and `reading-list --claims`
     read its move lines as they do in a metarepo.
   - `dangling` reads this repo's move lines. A metarepo pointer to a page or section that moved
     away reads `(moved: <pointer>)` in sync, the release and P2, never as missing.
8. **Staging.** A staged file may carry an optional `moved-from: <pointer>` header.
   `jig staging resolve` writes the moved-from line for what it landed, in the same job: the
   `D-?<slug>` entry, the page, or the section.

**Part C: `jig move <what> --to <repo> [--as <path>] [--apply]`**. Here `<what>` is an entry id,
a page, or `<page> § <heading>`. `--as` is the page's path in the receiver, and defaults to the
same path.

9. **Step 1, land it there.** `--apply` writes `.jig/specs/move-<slug>.md` here: the spec of the
   job that removes the claim. It also sends the text, by whichever route crosses repos in that
   direction:
   - **Down or sideways:** a file staged with `target: <repo>` and
     `moved-from: <me>/<path>[ § …]`, then forwarded. An entry goes as `kind: decisions`: its
     block as `### <their prefix>?<slug>`, who and date kept, and a `Supersedes` of this log's
     ids dropped, because that chain stays here. A page or section goes as `kind: doc`, with
     `destination: <as>`.
   - **Up:** `propose/<me>-move-<slug>` in the metarepo. The entry as `<prefix>?<slug>`, or the
     page, plus its moved-from line, is committed in a temporary worktree of the metarepo, so the
     metarepo's hook checks it (the moved-from line is its M3 line). The spec records
     `meta: <meta> proposal <branch>`. It also lists the metarepo's own citations of the moved
     thing, for its hubnode to point at the landed text in the job that takes the proposal.

   The step then waits on the receiver's owner.
10. **Step 2, remove it here.** This step needs the receiver's trunk to hold a moved-from line
    naming this thing, with its id numbered. `--apply` removes the entry block, the page or the
    section, and writes the move line naming the receiver's id or path. It stages the change in
    the checkout it runs in. In a metarepo's trunk checkout it is refused, because M4 puts the
    change in a job.
    - **Sideways from a pararepo:** the metarepo's cached pointers to the moved thing are
      rewritten from `<me>/<path>[ § s]` to `<to>/<as>[ § s]`. The rewrite is made on a
      `propose/<me>-move-<slug>-pointers` branch, written by the command, and recorded as
      `meta: <meta> pointers <branch>`, which P2 accepts.
11. **Roadmap items follow the page** (the owner, 2026-11-20: "roadmap items relating to the
    items being moved should move too"). A moved page's items that no spec or note takes go to
    the receiver's plan:
    - its product section's phase of the same name, else its `No phase` list;
    - up, the metarepo's own phase of that name, else its `## No phase`;
    - a receiver that keeps its own roadmap gets a `kind: roadmap` file staged with
      `target: <repo>`.

    An item a spec or note takes stays where it is, and the page is dropped from its
    `(touches …)`. The change is written by the route the losing roadmap's edits take:
    - in the metarepo's job commit, when the metarepo loses the page;
    - in the step's proposal, when a pararepo that plans from the metarepo loses it;
    - as a `kind: roadmap` file staged here, when a pararepo with a roadmap of its own loses it.
      Its hubnode applies it on trunk on the owner's yes (R5).
12. **RULES.md and docs.** The changes:
    - Roadmap: Moving in, by `jig move-in`. Edits: names and new products stay the metarepo
      hubnode's, who decides a product a pararepo proposes with its phases at that proposal's
      merge.
    - Decision log: Released sections. The move line comes from any family member; add the
      moved-from line.
    - Metarepo and pararepos: What the metarepo holds. "A claim moves down only" becomes
      moves in every direction by `jig move`; add a pin-bump note.
    - Staging: the `moved-from:` header.
    - Commands: both commands.
    - `docs/metarepos.md` (Moving claims) and `docs/commands.md` describe both commands.
    - The hubnode skill names them, under A roadmap change and the moves.

## Done when

Every command runs in throwaway repos with `JIG_CONFIG=<dir>/repos.json
XDG_CONFIG_HOME=<dir>/config`. The fixture:
- metarepo `M` (`E-`), whose `pararepos` lists `L` (`D-`) and `K` (`C-`);
- all three are registered;
- `M`'s glossary has `## Walyt` with `` Owner: `L` `` and `## Kite` with `` Owner: `K` ``;
- a pararepo `pd` keeps its own roadmap: `## alpha` with `x` and `y (after alpha/x)`, and
  `## No phase` with `u (touches docs/p.md)` and `v`. A spec takes `alpha/x`, and a handoff note
  takes `No phase/v`;
- `M` lists `pd` in its `pararepos`.

Part A (`jig move-in`):
- [ ] (plan, nothing written) In `pd`, `jig move-in --product Delta --definition "The delta
  app."` lists two steps: "product and phases proposed" as next, carrying the term `Delta`, and
  "roadmap leaves" waiting. `git status` is clean in `pd` and `M`, and `M` has no new branch.
- [ ] (one proposal) With no `Delta` term in `M`, `--apply` makes `propose/pd-move-in` in `M`:
  - its one commit past the opening passed `M`'s hook, its subject leading with `GLOSSARY:`;
  - it adds `## Delta` with "The delta app." and `` Owner: `pd`. `` to `M`'s glossary, with a log
    line under `## Unreleased` `### Added`;
  - it holds `## Delta alpha` with `y (after Delta alpha/x)`, and `## Delta No phase` with `u`
    and `v`, each line otherwise as `pd` had it;
  - `M`'s trunk is unchanged, and nothing is staged in `M`;
  - `pd`'s `BUFFER.md` has the row, and `.jig/specs/move-in.md` lists it alone, with an Open
    row `B0` added before it left out.
- [ ] (one merge) `M`'s job taking the proposal merges, and in that one merge commit `jig
  roadmap` in `M` reads `Delta alpha` as `pd`'s product, not as one of `M`'s own phases.
- [ ] (term edges) Without `--definition` while `M` has no `Delta` term, `--apply` is refused,
  naming the flag. `--product Walyt` is refused, naming its owner `L`. With `Delta` already
  owned by `pd` on `M`'s trunk, the proposal carries no glossary change and needs no
  `--definition`.
- [ ] (map edges) A heading `## Gadget beta` in `pd`, with `M`'s glossary owning `Gadget` to
  `pd`, is proposed unchanged. With `## Delta alpha` already on `M`'s trunk, `--apply` is
  refused and names it, and no branch is made. With `## Up next` in `pd`, it is refused, naming
  `jig update --apply`.
- [ ] (removal) Before `M` merges the proposal, step 2 is waiting. After the merge, `--apply`
  stages the removal of `.jig/roadmap.md` and `ROADMAP.md`. It also stages `Scope: Delta
  alpha/x` and `Scope: Delta No phase/v`, and the commit passes. If `M`'s owner renamed `y` to
  `y2` before merging, the command names `alpha/y` and the spec taking it, and the commit is
  refused until that spec is re-pointed.
- [ ] (moved in) Then `jig move-in` prints that `pd` has moved in. `jig rig` in `pd` offers
  `Delta alpha/…`, read from `M`.

Part B (records):
- [ ] (record lands) A staged `kind: decisions` file in `L` with `moved-from: M/.jig/decisions.md
  § E-002` resolves and merges. After the merge, `L`'s log has `D-001` and `- D-001: moved from
  M/.jig/decisions.md § E-002.` under `## Unreleased` `### Added`, both numbered by the merge.
  `jig decision D-001` in `L` prints `moved from M/.jig/decisions.md § E-002`. `jig reading-list
  --claims D-001` names it.
- [ ] (both ends) `M`'s move line `- E-002: moved to L/.jig/decisions.md § D-001.` is refused
  while `L`'s trunk has no moved-from line for it, and passes once it does. If `L` is dropped
  from the repos file, it passes with a warning naming `L`.
- [ ] (source checked) In `L`, a moved-from line naming `M/.jig/decisions.md § E-009` is
  refused, naming `M`'s file, when `M` neither has E-009 nor moves it to `L`.
- [ ] (up) In `L`, removing `D-005` with `- D-005: moved to M/.jig/decisions.md § E-010.` passes
  when `M`'s trunk has E-010 with its moved-from line. `jig decision D-005` in `L` names the
  move. A move line in `L` naming a repo outside the family is refused.
- [ ] (sideways) In `L`, moving `docs/l.md` to `K/docs/l.md` passes once `K` has it with its
  moved-from line. Then `L`'s `jig sync` lists `M`'s cached pointer `L/docs/l.md` as `(moved:
  K/docs/l.md)`, not as missing.
- [ ] (no family) A move line in a stand-alone repo is refused, and the refusal says why.

Part C (`jig move`):
- [ ] (down, both ends) In `M`:
  - `jig move E-002 --to L` lists both steps;
  - `--apply` writes `.jig/specs/move-e-002.md` and stages, in `L`, a decisions file with
    `moved-from: M/.jig/decisions.md § E-002`, who and date kept, and no `Supersedes E-001`;
  - `L` resolves it and merges;
  - `--apply` in `M`'s job worktree removes E-002 and writes `- E-002: moved to
    L/.jig/decisions.md § D-001.`, and the job merges;
  - run in `M`'s trunk checkout, step 2 is refused, naming M4.
- [ ] (a page down, with its items) `jig move docs/products/walyt/battery.md --to L --as
  docs/battery.md`: step 2's commit moves the untaken item `charge` into `## Walyt alpha` with
  `(touches docs/battery.md)`. A scope a spec takes stays, with the page dropped from its
  `(touches …)`. The merge passes.
- [ ] (up) In `L`, `jig move D-003 --to M` makes `propose/L-move-d-003` in `M`, whose commit,
  the entry as `E-?…` with its moved-from line, passed `M`'s hook. The spec says `meta: M
  proposal propose/L-move-d-003`. After `M`'s job takes the proposal and numbers it, `--apply`
  in `L` removes D-003 with its move line, and the commit passes.
- [ ] (sideways) In `L`, `jig move docs/l.md --to K` stages it in `K`. After `K` lands it,
  `--apply` in `L`:
  - removes the page and writes its move line;
  - makes `propose/L-move-docs-l-md-pointers` in `M`, rewriting `M`'s `L/docs/l.md` to
    `K/docs/l.md`;
  - records `meta: M pointers <branch>`.

  P2 passes on `L`'s commit.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh moves movein pararepo
  metarepo roadmap rig boundary staging decisions supersede removals pin_bump claims sync_buffer`
  passes. `movein` is the new section holding Part A. `claude plugin validate ./plugin` passes.

## Out of scope
- A family whose repos sit on different machines: as in cross-repo-roadmap, an unreachable repo
  is named and the step waits.
- Moving a claim inside one repo. A rename already leaves its address (move-to-pararepo, One
  layer up).
- Moving a claim between two families. A move line names a repo of this family only.
- Labels and phase types carried by the conversion. Part A copies every line but headings and
  refs verbatim, so `(labels …)` and a phase type ride along in whatever form roadmap-labels and
  phase-types give them, and the metarepo's hook checks them when the proposal merges. Their
  checks are those specs'.

## Touches
- `plugin/templates/jig/jig.py`:
  - Part A: a new `cmd_move_in` and its parser; `buffer_proposal` (one given row); `open_proposal`
    and `forward` reused; a commit on a `propose/` branch through a temporary worktree of the
    metarepo, a helper shared with Part C; `moving_in` reused for the check; `Family` and
    `term_owners`' reads on trunk (the commit's own glossary, as the commit's own roadmap).
  - Part B: `MOVE_LINE` beside a new moved-from form and `moved_from_in`; `move_rules`
    (any family member, both ends tied) and its call site (jig.py:558); `log_rules` and
    `frozen_problems` (a moved-from line is a change line); `hold_chain`, `cmd_decision`,
    `claims_of_id`; `dangling`; `HEADER_KEYS` and `jig staging resolve` (`moved-from:`).
  - Part C: a new `cmd_move` and its parser; `boundary_rules` and `dead_touches` reused
    for the items that follow; `cmd_propose` (`--pointers`) reused.
- `plugin/templates/jig/RULES.md`: Roadmap (Edits, Moving in), Decision log (Released sections),
  Metarepo and pararepos (What the metarepo holds, A pin-bump request), Staging (header keys),
  Commands.
- `plugin/skills/hubnode/SKILL.md`: moving in and moves, by command.
- `docs/metarepos.md` (Moving claims), `docs/commands.md`.
- `tests/smoke.sh`: a new `movein` section; `moves`, `pararepo`, `staging`, `claims`,
  `boundary` and `sync_buffer` gain cases.
- `marketing/FEATURES.md`: the rows under Decisions.
- Process or product: product (jig's behaviour), written in RULES.md, the skill and the docs
  pages as their homes.

## Alternatives considered
- **The glossary term as a staged request the metarepo's hubnode lands before the phases are
  proposed**: rejected by the owner, 2026-11-23: "carry the term in the same proposal (one yes)".
  Two yeses in sequence bought nothing, because the metarepo's hubnode decides the name at the
  merge either way. Reason is [seen].
- **A record on the receiving side written in the entry's status line** (`Accepted (owner,
  date). Moved from …`): rejected because it covers entries only, and a page or section would
  need a second form. The `### Added` line mirrors the `### Removed` move line, one form for
  all three. Reason is [seen].
- **Writing the receiver's text straight onto its trunk** ("both ends" in one run): rejected by
  the owner's ruling, "I dont like the idea of hubnodes editing each other's content". Reason is
  [seen].
- **Moving a taken roadmap item with its page**: rejected because the spec or note taking it
  would need its `Scope:` line re-pointed in another repo, which is that repo's content, and its
  work was that product's. Reason is [assumed].
- **One `jig move` that also converts roadmaps**: rejected because a roadmap isn't a claim. It
  has no move line, and it moves once per pararepo. Reason is [seen].

## Decisions
- Both commands are dry by default and do one step per `--apply`, as `jig update --apply` does.
  The owner's yes sits between steps, and a rerun picks up where the last one stopped, read
  from the repos themselves, with no state file.
- A step that crosses repos uses the route that already exists for its direction: staging
  (`forward`) down and sideways, `jig propose` up and for roadmap edits. Nothing new writes in
  another repo.
- The command writes its proposal branch's commit in a temporary worktree of the metarepo, so
  the metarepo's own hook judges it there, not only when it merges.
- The product's glossary term goes in the same proposal as its phases. The owner, 2026-11-23:
  "carry the term in the same proposal (one yes)". The metarepo's hubnode decides the name at
  that merge, so names and new products stay its own (RULES.md, Edits, updated to say so).
- The move line's check requires the receiver's moved-from line. The owner, 2026-11-23: "hook
  refuses the move line until the receiver has its moved-from line". Today's check reads the
  target's existence only, so a hand-made move now needs the line at both ends.
- Writes in this repo are staged, never committed: the hubnode commits on the owner's yes, as
  with `jig propose` and `jig update --apply`.
- Built as parts A to C with `--partial`. A needs nothing new. B is the record, and C's step 2
  reads it.
- FEATURES rows, for `marketing/FEATURES.md`:
  - | `jig move-in`: a pararepo's roadmap moves into its metarepo by command (spec `moving-in-command`) | One step per `--apply`: the product's glossary term and its phases and No phase list are proposed together on one `propose/` branch, headings and refs mapped to `<Product> …`, for one yes; once merged, its roadmap and view leave with every `Scope:` line re-pointed. | Owner, 2026-11-23: "end state was supposed to mean exactly that: everything including labels" (cross-repo-roadmap had deferred it) | Moving in by hand was four steps across two repos, each easy to get half right, with every `Scope:` line edited by hand. | Not a write to the metarepo's trunk: each cross-repo step is a proposal its owner approves. Not a merge of two plans: a heading both have is refused. |
  - | `jig move`: a claim moves down, up or sideways, both ends by one command, recorded at both (spec `moving-in-command`) | The losing repo stages or proposes the text with a `moved-from` record, then removes it with its move line once the receiver has it; the hook refuses a move line the receiver's moved-from line doesn't answer; roadmap items untaken follow a moved page; a sideways move proposes the metarepo's pointer rewrites. | Owner, 2026-11-23, same ruling (move-to-pararepo had deferred up, sideways, one command and the receiving record) | A claim with one owner could only move down, by hand in two repos, and the receiving side couldn't say where it came from. | Not a forwarding stub on a page (row "No forwarding addresses"): both records are changelog lines. Not a move between families. |

## Open questions for the owner
1. **The product's glossary term in `jig move-in`.** Answered, the owner, 2026-11-23: "carry
   the term in the same proposal (one yes)" (Decisions).
2. **Both ends tied.** Answered, the owner, 2026-11-23: "hook refuses the move line until the
   receiver has its moved-from line" (Decisions).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
