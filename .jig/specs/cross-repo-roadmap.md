# cross-repo-roadmap: one roadmap across a metarepo and its pararepos, with dependencies rig reads

Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): "A deadlock nobody could see", with copies of scopes drifting between repos, because waits on another repo are prose in one repo's roadmap (Issue 1).
Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): "`jig rig` offers a scope that waits on another repo as the next step" (Issue 3).

Kept separate from bug-empty-proposal: the owner, 2026-11-20: "Hold on the cross-repo roadmap until we discuss it."
Kept separate from bug-metarepo-roadmap-cites: the owner, 2026-11-20: "Hold on the cross-repo roadmap until we discuss it."

Kept separate from move-to-pararepo: the owner, 2026-11-21: "would you agree we should start both bugs and let them finish, then do 2, then 1?" and "agreed with move-to-para after job 3": built in sequence, move-to-pararepo first.
## Intent
A scope or phase names what it waits on in a form jig reads, so `jig rig` never offers blocked
work and a ring is refused when it is written. A metarepo and its pararepos then plan from one
roadmap in the metarepo, each product with its own phases, read live, so no scope exists in two
copies to drift. This is the first version: the smallest change that ends the deadlock and the
drift. A moved-in pararepo keeps no roadmap of its own. Each product's scopes with no phase are
one list in the metarepo's roadmap, and a spec may take one. The rest of the report's draft is
listed under Out of scope as later work.

## Investigation

### 1. Why
- Q: Why did rig offer a blocked scope? A: `rig_next_step` takes the current phase's first open scope no spec takes. It reads no wait.
- Q: Why no wait to read? A: The roadmap has no dependency. A wait is prose in a scope's text, and `SCOPE_LINE` keeps it as text.
- Q: Why was the Lite–Familiar ring invisible, and why did copies drift? A: Each repo has its own roadmap, read one at a time, with no product level. A wait on another repo can't be checked. Root.

### 2. Givens
- [seen] Reproduced at trunk 36787df, in a throwaway repo (`JIG_CONFIG`/`XDG_CONFIG_HOME` set): with `## alpha` scopes `pairing: … (after Familiar App alpha/host) (touches docs/x.md)`, `clip: the clip (after alpha/pairing)` and `free`, `jig rig` prints `next    alpha/pairing (phase alpha): pairing with the host (after Familiar App alpha/host) (touches docs/x.md)` under "Waiting on you". `jig roadmap` shows all three `open`. The `(after …)` is kept as text, and the ref to nothing commits.
- [seen] The ring, on two trunks (read with `git --no-optional-locks`). Maige-Lite `.jig/roadmap.md`, `## Familiar alpha`: every scope reads "after Maige-Familiar's alpha". Maige-Familiar `.jig/roadmap.md`, `## alpha`: "A compatibility scope is built when Maige-Lite is ready for it."
- [seen] Waits inside one repo are prose too. Maige-Lite's `radios` reads "(0.2, after `bring-up`)", and `power` reads "after `bring-up` and `radios`". So Issue 3 can happen in a repo with no metarepo.
- [seen] Guild-Rulebook (meta) and Adventure-Studio (para) are a second family. Adventure-Studio's `## loop` has the exit box "the pin points at Protocol v5.1.19", which is a wait on its metarepo written as prose.
- [seen] `rig_next_step` (jig.py:13998) returns the first Up next item not covered, else the current phase's first `open` scope not in `taken`. `roadmap_state` (jig.py:10136) makes one current phase per roadmap.
- [seen] `rig_state` already has a "Waiting on:" block for items with `waits_on` (`rig_text`). A ring among items is reported once as "a dependency cycle" that waits on the owner. That is the shape a scope's wait needs.
- [seen] A phase name may hold spaces, and a scope id is `<phase>/<scope>` (`SCOPE_LINE`, `parse_roadmap`). So `Walyt alpha/pairing` is already a valid id when the phase heading is `## Walyt alpha`, and ids need no new format.
- [seen] `TOUCHES` is anchored at the line's end. An `(after …)` written before it is kept as plain text today, and a roadmap written that way still commits.
- [seen] `roadmap_rules` (jig.py:10576) checks `Scope:` lines against this repo's own trunk roadmap. On trunk, it refuses a roadmap change that drops a scope a spec or note takes. Deleting the roadmap drops every scope, so moving a pararepo's phases out is already guarded: the move's commit must re-point every `Scope:` line.
- [seen] `meta_checkout` (jig.py:7588) finds the metarepo's checkout through `jig repos`. All four Maige repos are registered on this machine, with paths (`jig repos`).
- [seen] maige-ecosystem's glossary has 26 `Owner:` lines in the form `` Owner: `maige-os`. `` or `Owner: this repo.`. That is an alias or a folded repo name, not always the `jig repos` name (`Maige-OS`).
- [seen] The roadmap is read at about 20 sites in jig.py (`show(ROADMAP)`, `at_rev(…, ROADMAP)`, `in_index(ROADMAP, …)`): view, state, rig, reading-list, fold-in, merge's Up next removal, sweep and the hooks.
- [seen] A roadmap change is shown to the owner as a diff and applied on a yes (hubnode skill, "A roadmap change"). R5 (the rule) keeps `.jig/roadmap.md` on trunk.
- [assumed] The four Maige hubnodes run on one machine, so a pararepo's hubnode can reach the metarepo's checkout. This holds for this owner. A team on several machines would push and pull, which this version doesn't cover (Out of scope).

### 3. One layer up
- The sibling: rig already orders staged files by `after:` and specs by `Build after`, and it reports a ring once (RULES.md, Workflow). Scopes are the one rig input with no wait. This spec gives them the same treatment, with the same "Waiting on:" line and the same cycle handling.
- The pattern for reading other repos live: `meta_checkout` and `peer_logs` already read another repo's trunk through `jig repos`. Issue 2's spec (bug-metarepo-roadmap-cites) needs the same live read of the metarepo's roadmap. Build one helper, and whichever spec lands second reuses it.
- Phase names that hold spaces already give `<Product> <phase>` ids for free.

### 4. Correction
A correction. Dependencies become syntax that jig parses (Part 1). The roadmap moves to one home (Part 2), so a cross-repo wait is a check within one file and no copy exists to drift. There's no workaround to keep: the interim workaround of writing waits as plain text is exactly what hid the ring.

### General?
- **A metarepo with pararepos**: yes. Any family whose plans wait on each other meets the ring and the drift, because jig reads one roadmap per repo with waits as prose. Guild-Rulebook/Adventure-Studio already writes such a wait as prose.
- **A stand-alone repo**: Part 1 applies to any repo whose scopes wait on each other (Maige-Lite writes in-repo waits as prose, and Issue 3 fires on them). Part 2 doesn't apply: a stand-alone repo keeps its own roadmap, and only gains `(after …)`.

## Change — first version

Two mergeable parts, in order. Part 1 stands alone; Part 2 builds on it.

### Part 1: dependencies, and a blocked scope (any roadmap; fixes Issue 3)
1. A scope may name what it waits on, `(after <ref>, …)`, written after its text and before any
   `(touches …)`. A phase may name what it waits on with a line `(after <ref>, …)` of its own
   in its note, which applies to each of its scopes. A ref is `<phase>/<scope>` or `<phase>`
   in the roadmap being read. A label carries no dependency, and no ref names a label (R7).
2. The hook, on trunk when the roadmap changes, refuses three things, by line. It refuses a ref to a phase or scope that doesn't exist. It refuses a ref to itself. It refuses a ring, named once with all its members. `jig roadmap` reports the same.
3. A scope is **blocked** while any ref, its own or its phase's, is not done (a scope ref
   not `done`, or a phase ref not `done`). Blocked is derived, like the states. A scope still
   reads `open`, `taken` or `done`, and `jig roadmap` adds `after <ref>` beside an open
   blocked scope. The `(after …)` text leaves the scope's `what`, as `(touches …)` does.
4. `jig rig`'s next step skips a blocked open scope. Each blocked open scope in a current
   phase is listed under "Waiting on:" as `next    <id>  waits on <ref>, …`, which brings blocked
   items to the owner's attention (R1). If every open scope in a phase is blocked, that phase
   offers no next step.

### Part 2: one roadmap in the metarepo (ends the drift)
5. **Products.** In a metarepo's `.jig/roadmap.md`, a heading `## <Product> <phase>` belongs to
   a product when its leading words, case folded, are a term in the metarepo's glossary. That
   term must have an `Owner:` line naming a pararepo (its first backticked name, matched
   against `jig repos` names and aliases, case folded) or `this repo`. If several terms match,
   the longest wins. Every other heading is one of the metarepo's own phases, as today. Each
   product's phases are ordered among themselves in file order and have their own current
   phase, and so do the metarepo's own phases. Nothing orders one product after another except
   an `after`. A product heading whose `Owner:` names no repo jig knows is reported by
   `jig roadmap`.
6. **One reader.** A pararepo with no phases of its own reads the metarepo's roadmap live, from
   its checkout's trunk through `jig repos` (`meta_checkout`), never at the pin. A roadmap
   change can't be released, and R6 settles it: "read it live". Every roadmap read site
   goes through this reader: state, view, rig, reading-list, fold-in and the hooks. If the
   checkout can't be reached, the reader says so by name, and the hook passes the `Scope:`
   check with a warning instead of refusing what it can't read.
7. **States are pulled.** A scope's specs and notes are read from the metarepo's trunk and from
   each pararepo's trunk that `jig repos` reaches (`meta.json`'s `pararepos`). A pararepo it
   can't reach is named, and its products' scopes read `unknown`. The same read serves the
   metarepo's hook: it refuses dropping a scope that a reachable pararepo's spec or note takes,
   naming the file.
8. **Pages in a product section.** A `(touches …)` page under a product heading is a page of the
   product's owning repo, and is checked on that repo's trunk when it can be reached. In the
   owning pararepo, reading-list and fold-in match those scopes against its own pages.
9. **Rig per repo.** In a pararepo, the next step comes from the current phases of the products
   it owns. In the metarepo, it comes from its own phases and the products it owns as
   `this repo`. Blocked scopes are skipped and listed as in Part 1, across products.
10. **Moving in, by hand.** This version has no conversion command. Once per pararepo, on the owner's yes:
    1. The metarepo gains `## <Product> <phase>` sections holding the pararepo's phases.
    2. The pararepo's next commit removes its phases and re-points every `Scope:` line. The existing drop guard enforces this.
    3. The move carries the pararepo's `## Up next` and `## No phase` items into its product's list in the metarepo, and the move's commit removes the pararepo's `.jig/roadmap.md` and `ROADMAP.md`. After the move, the pararepo's hook refuses a `.jig/roadmap.md` while the metarepo's roadmap holds a product it owns.
11. **Edits.** No hubnode edits another repo's content (the owner, 2026-11-21). A pararepo's changes to its products' sections are buffered and reach the metarepo by the regular sync process, when the owner decides; the mechanism is still being settled. A pararepo's merge writes nothing to the metarepo's roadmap. The metarepo's hook checks shape, refs, rings and touched pages. Labels, names and new products are the metarepo's hubnode's. RULES.md says this.
12. **RULES.md, Roadmap.** "The product is the repo" is said precisely, per R6: a repo is for one software product, and the hardware that runs it may be defined there, with its pages segmented within `docs/` as the hardware skill's board pages are. A metarepo's roadmap gains the product level of item 5. The pin rule gains the live-read exception for the roadmap only.


13. **One list per product.**
    - Each product, and the metarepo's own work, has one list of scopes with no phase. `## Up next` and `## No phase` stop being two places for them.
    - A scope in the list has an id a `Scope:` line can name, and it names what it touches. Its state is derived like any scope's (item 7).
    - rig's next step, reading-list and fold-in read the list through the one reader (item 6), as they read the product's phases.
    - A pararepo's merge writes nothing to the metarepo's roadmap, per the owner's 2026-11-21 ruling on edits.
    - The list's syntax, and what replaces merge's Up next removal, are jig's to choose.
    - A stand-alone repo's Up next and No phase become one list the same way, per R2: "one place for them not two".

## Done when

Part 1, in a throwaway stand-alone repo, every jig command run with
`JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`:
- [ ] (fix fires) `## alpha` with `pairing: … (after alpha/host) (touches docs/x.md)` then `host`: `jig rig` offers `alpha/host`, and lists `next    alpha/pairing  waits on alpha/host` under "Waiting on:", not as the next step. `jig roadmap` shows pairing `open` with `after alpha/host`.
- [ ] (unblocked) Once a spec taking `alpha/host` is complete on trunk, `jig rig` offers `alpha/pairing`.
- [ ] (phase) `## beta` whose note has `(after alpha)` and whose scopes are open, with `alpha` not done: no beta scope is offered or counted as current work. Once alpha is done, beta's first scope is offered.
- [ ] (all blocked) A current phase whose every open scope is blocked: rig offers no roadmap next step and lists each blocked scope.
- [ ] (ring) `a (after alpha/b)` and `b (after alpha/a)`: the trunk commit is refused, naming the ring once with `alpha/a` and `alpha/b`.
- [ ] (a wait on nothing) `(after alpha/nope)` is refused by line, and so is a scope naming itself.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig` passes.

Part 2, in a throwaway metarepo `meta` with pararepos `pa` and `pb`. Both are registered and both are in `meta.json`'s `pararepos`, with the same variables set. `meta`'s glossary has `## Walyt` with `` Owner: `pa` `` and `## Familiar App` with `` Owner: `pb` ``. `pa` has `docs/p.md`. Neither pararepo has phases of its own:
- [ ] (products) `meta`'s roadmap `## Walyt alpha` with `pairing (after Familiar App alpha/host) (touches docs/p.md)`, `## Familiar App alpha` with `host`, and `## Demos` with one scope commits on `meta`'s trunk, with `docs/p.md` found on `pa`'s trunk. `jig roadmap` in `meta` shows all three phases as current, and no phase line orders one product after another.
- [ ] (Issue 3's symptom gone) `jig rig` in `pa` doesn't offer `Walyt alpha/pairing`. It lists it as waiting on `Familiar App alpha/host`.
- [ ] (progress, live) `pb` merges a job whose spec has `Scope: Familiar App alpha/host`. The hook checks that line against `meta`'s trunk. With no `meta` release and nothing done in `meta`, `jig rig` in `pa` then offers `Walyt alpha/pairing`, and `jig roadmap` in `meta` shows `host` done.
- [ ] (the deadlock refused) Adding `(after Walyt alpha/pairing)` to `host` in `meta` is refused, naming the ring once with both members.
- [ ] (live read) A scope added under `## Walyt alpha` on `meta`'s trunk, with no release: a spec in `pa` with `Scope: Walyt alpha/<it>` commits, and `Scope: Walyt alpha/nope` is refused, naming `meta`'s roadmap.
- [ ] (unreachable) With `pb` removed from the repos file, `jig roadmap` in `meta` shows `Familiar App alpha/host` as `unknown`, naming `pb`.
- [ ] (drop guard) A `meta` commit dropping `Walyt alpha/pairing` while a spec in `pa` takes it is refused, naming that spec.
- [ ] (moving in) A `pa` that had `## alpha` with `x` and a spec with `Scope: alpha/x`. After `meta` gains `x` under `## Walyt alpha`, `pa`'s commit removing its phase and re-pointing the spec to `Walyt alpha/x` passes. Re-pointing to a scope `meta` lacks is refused. After that, `pa` has no `.jig/roadmap.md`. What `pa` had under Up next and No phase sits in `Walyt`'s one list in `meta`. A spec in `pa` taking one of them commits, and `pa`'s reading-list shows them, read from `meta`. A new `.jig/roadmap.md` in `pa` is refused.
- [ ] (unphased scope, live) `pb` merges a job whose spec takes a scope from `Familiar App`'s list. `jig roadmap` in `meta` shows that scope done, and `pb`'s merge wrote nothing to `meta`.
- [ ] (stand-alone one list) In a stand-alone repo, the Up next and No phase items are one list, a spec may take one, and `jig rig` offers from it.
- [ ] (stand-alone unchanged) The Part 1 cases pass in a repo with no metarepo. `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig pararepo` passes. `claude plugin validate ./plugin` passes.

## Out of scope
Later versions, each its own spec once this lands, in the order they build on each other:
- **Labels** (R1–R3): `(labels …)` on a scope, checked against the metarepo glossary's folded terms.
- **Dependency confirmation** (R6: "the owner of the scope it waits on confirms it in its own section"): `(needed by …)`, with an unconfirmed dependency reported. Until then, the owner approves every roadmap diff (open question 4).
- **Ideas log and open questions leaving the decision log** (R4, R5).
- **The cross-repo report**: stale staged files and `propose/` branches, entries touching labelled scopes, and two names for one thing.
- **A jig edit command** that refuses a line under another repo's product and stages label changes. A **conversion command** for moving in.
- **Phase types** (Prototype/Pilot/Production), **filters**, and **departures** shown across pararepos.
- Issue 2 (bug-metarepo-roadmap-cites) and Issue 4 (empty proposals): other groups. Issue 2 shares item 6's live reader.
- A family whose repos sit on different machines: the reader names an unreachable repo, and nothing more.
- maige-ecosystem's own roadmap rewrite and its glossary's `Owner:` lines: its job (R6).

## Touches
- `plugin/templates/jig/jig.py`: `SCOPE_LINE`/`split_touches` (an `after` split), `parse_roadmap` (phase `after`, products), `roadmap_state` (blocked, current per product, pulled states, unknown), `roadmap_view`, `cmd_roadmap`, `roadmap_rules` (refs, rings, `Scope:` against the metarepo, drop guard across repos, no phases in a moved-in pararepo), `rig_next_step`/`rig_state`/`rig_text`, the roadmap read sites (one reader), `dead_touches` (owning repo's pages), merge's Up next removal, update's `--sweep` (which writes `## Up next`), reading-list, fold-in and `rig_next_step`'s Up next read
- `plugin/templates/jig/RULES.md`: Roadmap (dependencies, products, one reader, "the product is the repo"), Metarepo and pararepos (live read of the roadmap, edits in the metarepo), Workflow (rig's blocked scopes), Roadmap (Up next and No phase become one list)
- `plugin/skills/hubnode/SKILL.md` (A roadmap change: editing a product's section in the metarepo), `plugin/skills/rig/SKILL.md` (blocked scopes), `plugin/skills/spec/SKILL.md` (`Scope:` ids with a product)
- `tests/smoke.sh`: roadmap, rig, pararepo

## Alternatives considered
- The report's whole first version (products, edit command, labels, `needed by`, one list, ideas log, report, conversion, about 17 checks) as v1. Rejected because each piece is separable, and the owner's standing rule is "Solve the problem, be pragmatic, keep it simple". The deadlock and the drift need only dependencies and one roadmap. Reason is [seen] (the report's own Done when list).
- Cross-repo refs between separate roadmaps (`(after Maige-Familiar:alpha)`), with no move. Rejected because ruling 8 (R5) puts the scopes in one file, so that syntax would be thrown away, and copies would keep drifting. Reason is [seen].
- Parsing prose waits ("after …", "waits on"). Rejected because prose waits are what hid the ring for a week. Reason is [seen].
- Blocked as a fourth state beside open/taken/done. Rejected because states come from specs and blocked comes from refs. Keeping it a qualifier leaves the view's columns and every state reader alone. Reason is [assumed].
- The product map in `meta.json`. Rejected because R6 names the glossary as "the right place" for ownership, and maige-ecosystem already keeps `Owner:` lines. Reason is [seen].
- Keeping Up next and No phase in the pararepo for v1: rejected. The owner, 2026-11-21: "I want to reach the end state I specced" (R4, R2, R7).
- Pushing progress from a pararepo's merge into the metarepo. Rejected because it would mean a second repo's commit in every merge, while states are derived everywhere else in jig. Reason is [assumed].

## Decisions
- `(after …)` comes before `(touches …)` so `TOUCHES` stays anchored at the line's end, and so roadmaps already written in this order (the report's interim advice) parse unchanged.
- A phase's `after` is a line of its own in the note, since a note is prose and has no single line to end.
- Blocked scopes go under rig's "Waiting on:", not "Waiting on you". A blocked scope waits on work, not on an answer. A ring is still the owner's question, as rig's cycles are now.
- An unreachable repo warns, never refuses: a hook that refuses what it can't read would block every commit while a disk is unmounted.

## Open questions for the owner
1. **The first version is Parts 1 and 2 only.** Labels, `needed by`, one list per product, the ideas log, the report and the conversion command follow as later specs. Recommendation: yes. Part 1 alone already fixes Issue 3 in every repo, and Part 2 ends the drift.
2. Answered: the first version reaches the end state (Owner's rulings).
3. **Edits by hand in the metarepo's clean trunk checkout, on your yes, with no jig check of whose section a line is in.** Recommendation: yes for v1. You already see every roadmap diff, and the command that refuses another repo's section is later work.
4. **R6's confirmation of a cross-product dependency is RULES.md text in v1** ("the waited-on scope's owner agrees before the `after` is committed"), with the `(needed by …)` check later. Recommendation: yes. The ring check and rig's blocked list are what end the deadlock, and confirmation only records agreement.

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4

## Owner's rulings, 2026-11-20 and 2026-11-21

Still being settled; the spec's body is revised to these once they are.
- First version (open question 1): "1.1 yes": Parts 1 and 2 first, the rest as later specs.
- Up next and No phase (open question 2): the owner, 2026-11-20: "roadmap items relating to the items being moved should move too." A pararepo's Up next and No phase move up with its phases, and a scope whose `(touches …)` names a page moved down follows it.
- Section edits (open question 3), the owner, 2026-11-21: "I dont like the idea of hubnodes editing each other's content, I think they should buffer the changes and use the regular sync process periodically (as the user decides)." No hubnode edits the metarepo's roadmap from a pararepo: a pararepo's changes to its product sections are buffered and reach the metarepo by the regular sync process, when the owner decides.
- Dependency confirmation (open question 4), the owner, 2026-11-21: "Remove the requirement that they agree and flag when they dont so the user can rule on it." A cross-product `after` the waited-on section doesn't confirm never blocks: it is flagged for the owner to rule on.
- Order, the owner, 2026-11-21: bug-pararepo-sync-fixes and bug-nested-touches first, then move-to-pararepo, then this spec.
- The end state, Source: Dave (owner), 2026-11-21, in maige-ecosystem's hubnode session, on reading that a moved-in pararepo keeps `## Up next` and `## No phase` until a later spec: "I want to reach the end state I specced". One list per product joins Part 2 (item 13), and a moved-in pararepo keeps no `.jig/roadmap.md`.
