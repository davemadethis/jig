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
copies to drift. A moved-in pararepo keeps no roadmap of its own. Each product's scopes with no
phase are one list in the metarepo's roadmap, and a spec may take one. A pararepo changes its
products' sections only through a BUFFER row and `jig propose`, merged at the next sync the owner
calls. A cross-product wait the waited-on product doesn't confirm is flagged for the owner,
never blocking. This is the first version, built in four parts (Change). What the report drafted
beyond it is under Out of scope as later work.

## Investigation

**1. Why**
- Q: Why did rig offer a blocked scope? A: `rig_next_step` takes the current phase's first open scope no spec takes. It reads no wait.
- Q: Why no wait to read? A: The roadmap has no dependency. A wait is prose in a scope's text, and `SCOPE_LINE` keeps it as text.
- Q: Why was the Lite–Familiar ring invisible, and why did copies drift? A: Each repo has its own roadmap, read one at a time, with no product level. A wait on another repo can't be checked. Root.

**2. Givens** (line numbers at trunk 485c13e)
- [seen] Reproduced at trunk 36787df, in a throwaway repo (`JIG_CONFIG`/`XDG_CONFIG_HOME` set): with `## alpha` scopes `pairing: … (after Familiar App alpha/host) (touches docs/x.md)`, `clip: the clip (after alpha/pairing)` and `free`, `jig rig` prints `next    alpha/pairing (phase alpha): pairing with the host (after Familiar App alpha/host) (touches docs/x.md)` under "Waiting on you". `jig roadmap` shows all three `open`. The `(after …)` is kept as text, and the ref to nothing commits.
- [seen] The ring, on two trunks (read with `git --no-optional-locks`). Maige-Lite `.jig/roadmap.md`, `## Familiar alpha`: every scope reads "after Maige-Familiar's alpha". Maige-Familiar `.jig/roadmap.md`, `## alpha`: "A compatibility scope is built when Maige-Lite is ready for it."
- [seen] Waits inside one repo are prose too. Maige-Lite's `radios` reads "(0.2, after `bring-up`)", and `power` reads "after `bring-up` and `radios`". So Issue 3 can happen in a repo with no metarepo.
- [seen] Guild-Rulebook (meta) and Adventure-Studio (para) are a second family. Adventure-Studio's `## loop` has the exit box "the pin points at Protocol v5.1.19", which is a wait on its metarepo written as prose.
- [seen] `rig_next_step` (jig.py:14299) returns the first Up next item not covered (by the pages a Touches names), else the current phase's first `open` scope not in `taken`. `roadmap_state` (jig.py:10427) makes one current phase per roadmap.
- [seen] `rig_state` already has a "Waiting on:" block for items with `waits_on` (`rig_text`). A ring among items is reported once as "a dependency cycle" that waits on the owner. That is the shape a scope's wait needs.
- [seen] A phase name may hold spaces, and a scope id is `<phase>/<scope>` (`SCOPE_LINE`, `parse_roadmap`). So `Walyt alpha/pairing` is already a valid id when the phase heading is `## Walyt alpha`, and ids need no new format.
- [seen] `TOUCHES` is anchored at the line's end. An `(after …)` written before it is kept as plain text today, and a roadmap written that way still commits.
- [seen] `roadmap_rules` (jig.py:10877) checks `Scope:` lines against this repo's own trunk roadmap. On trunk, it refuses a roadmap change that drops a scope a spec or note takes. Deleting the roadmap drops every scope, so moving a pararepo's phases out is already guarded: the move's commit must re-point every `Scope:` line.
- [seen] `meta_checkout` (jig.py:7796) finds the metarepo's checkout through `jig repos`, and `repo_path` (jig.py:7530) any registered repo's. All four Maige repos are registered on this machine, with paths (`jig repos`).
- [seen] `trunk_show(loc, path)` (jig.py:6102) is the one live read of another repo's text: `git show <its trunk>:<path>` in its checkout. bug-pararepo-sync-fixes (8605d2c) added the live read of the metarepo's roadmap in `meta_citations` (jig.py:8822), and move-to-pararepo (485c13e) lifted it into `trunk_show`. `meta_citations` reads a cite of `<meta>/.jig/roadmap.md` through it today.
- [seen] `spec_section(text, *names)` (jig.py:1288, from bug-nested-touches) is the one reader of a spec section at any level from `##` down; `touches_spans` and the Roles and Proposals reads use it. `scopes_in(path, text)` (jig.py:10257) reads a spec's or a note's `Scope:` line.
- [seen] maige-ecosystem's glossary has 26 `Owner:` lines in the form `` Owner: `maige-os`. `` or `Owner: this repo.`. That is an alias or a folded repo name, not always the `jig repos` name (`Maige-OS`).
- [seen] The roadmap is read at about 16 sites in jig.py (`show(ROADMAP)`, `at_rev(…, ROADMAP)`, `in_index(ROADMAP, …)`): view, state, rig, reading-list, fold-in, merge's Up next removal, sweep and the hooks.
- [seen] R5's check (jig.py:570) refuses `.jig/roadmap.md` on any branch but trunk, a metarepo's `propose/` branch included. A roadmap change is shown to the owner as a diff and applied on a yes (hubnode skill, "A roadmap change").
- [seen] `jig merge` removes the Up next items a job built (`built_up_next`, `remove_up_next`) and re-points each `(touches …)` naming a page the job moved (`retarget_touches`), in the merge commit (jig.py:2066).
- [seen] `boundary_rules`' dead-touch refusal (jig.py:10723, from move-to-pararepo): a trunk commit leaving an item or scope touching a page that has a move line is refused with "`<id>` touches <page>, moved to <pointer>: stage a roadmap change with `target: <repo>` carrying it, and drop it, or the page from its (touches …), here in this commit". That is move-to-pararepo's form of the owner's ruling "roadmap items relating to the items being moved should move too", made while each repo still had its own roadmap.
- [seen] Up next items must name pages and No phase items must name none (`parse_section`); a spec can't take either. `jig update --apply --sweep` writes pages' Undefined entries as Up next items.
- [assumed] The four Maige hubnodes run on one machine, so a pararepo's hubnode can reach the metarepo's checkout. This holds for this owner. A team on several machines would push and pull, which this version doesn't cover (Out of scope).

**3. One layer up**
- The sibling: rig already orders staged files by `after:` and specs by `Build after`, and it reports a ring once (RULES.md, Workflow). Scopes are the one rig input with no wait. This spec gives them the same treatment, with the same "Waiting on:" line and the same cycle handling.
- The pattern for reading other repos live is built: `trunk_show` through `meta_checkout` or `repo_path`. Every cross-repo read here is a call to it, never a second copy.
- Phase names that hold spaces already give `<Product> <phase>` ids for free.

**4. Correction**
A correction. Dependencies become syntax that jig parses (Part A). The roadmap moves to one home (Parts C and D), so a cross-repo wait is a check within one file and no copy exists to drift. There's no workaround to keep: the interim workaround of writing waits as plain text is exactly what hid the ring.

**General?**
- **A metarepo with pararepos**: yes. Any family whose plans wait on each other meets the ring and the drift, because jig reads one roadmap per repo with waits as prose. Guild-Rulebook/Adventure-Studio already writes such a wait as prose.
- **A stand-alone repo**: Parts A and B apply to any repo (Maige-Lite writes in-repo waits as prose, and Issue 3 fires on them). Parts C and D don't: a stand-alone repo keeps its own roadmap.

## Change — first version

Four parts, in build order. Each is mergeable alone and hands off `--partial` except the last,
which completes the spec; each has its own group under Done when. A needs nothing; B needs
nothing; C builds on A and B; D builds on C. The rulings' "Part 1" is Part A, their "Part 2"
is Parts B to D, and their "item 13" (one list per product) is Part B with item 8's
`## <Product> No phase`.

**Part A: dependencies, and a blocked scope** (any roadmap; fixes Issue 3)
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
   offers no next step; rig offers instead the first open, unblocked, untaken scope they wait
   on, directly or through a chain, a taken scope's waits followed too (the hubnode, from the
   reviews of 626a69a and f495209). A waiting spec or staged file whose `Scope:` names a blocked
   scope waits on that scope's refs, listed under "Waiting on:" as `spec <path>  waits on <ref>`
   like a `Build after`, never under "Can start now".

**Part B: one list for work with no phase** (any roadmap; item 13 of the end state, built first
so products in Part C get it for free)
5. **One list.** `## Up next` and `## No phase` stop being two places, per R2: "one place for
   them not two". The one list is `## No phase`. Its items read `` - `<id>`: <what it is> ``,
   optionally ending `(after …)` and `(touches …)`; a parked item's "stops at …; parked …" is
   kept as its text. Its id is `No phase/<id>`, which a `Scope:` line can name, and its state is
   derived like a scope's: open, taken or done. It sits in no phase line and is never current.
6. **Readers.** rig's next step offers the list's first open item that names pages and whose
   pages no open job's, waiting spec's or staged file's Touches covers, ahead of the current
   phase's scope, as it offers Up next today; an item naming no pages is never offered, as No
   phase today. reading-list and fold-in match items by their pages, as they read Up
   next items today. The view shows the list with its states. A spec's Touches and `Scope:`
   lines are read through `touches_spans`/`spec_section` and `scopes_in`, never a new parse.
7. **What goes.** merge's Up next removal goes: a built item reads `done` by its derived state
   and stays until the owner's roadmap change removes it. `jig update --apply --sweep` writes
   the list. `jig update --apply` folds an existing `## Up next` into `## No phase`, keeping each
   item's id and text, as a roadmap change on trunk on the owner's yes; after it, the hook
   refuses a `## Up next` heading by line.

**Part C: one roadmap in the metarepo** (ends the drift)
8. **Products.** In a metarepo's `.jig/roadmap.md`, a heading `## <Product> <phase>` belongs to
   a product when its leading words, case folded, are a term in the metarepo's glossary. That
   term must have an `Owner:` line naming a pararepo (its first backticked name, matched
   against `jig repos` names and aliases, case folded) or `this repo`. If several terms match,
   the longest wins. Every other heading is one of the metarepo's own phases, as today. Each
   product's phases are ordered among themselves in file order and have their own current
   phase, and so do the metarepo's own phases. Nothing orders one product after another except
   an `after`. `## <Product> No phase` is that product's one list (Part B); its ids are
   `<Product> No phase/<id>`. A product heading whose `Owner:` names no repo jig knows is
   reported by `jig roadmap`.
9. **One reader.** A pararepo with no phases of its own reads the metarepo's roadmap live, from
   its checkout's trunk: `trunk_show(meta_checkout(…), ROADMAP)`, the read `meta_citations`
   already makes, never at the pin. A roadmap change can't be released, and R6 settles it:
   "read it live". Every roadmap read site goes through one function over it: state, view, rig,
   reading-list, fold-in and the hooks. If the checkout can't be reached, the reader says so by
   name, and the hook passes the `Scope:` check with a warning instead of refusing what it
   can't read.
10. **States are pulled.** A scope's specs and notes are read from the metarepo's trunk and from
    each pararepo's trunk that `jig repos` reaches (`meta.json`'s `pararepos`, through
    `repo_path` and `trunk_show`), their `Scope:` lines by `scopes_in`. A pararepo it can't
    reach is named, and its products' scopes read `unknown`. The same read serves the
    metarepo's hook: it refuses dropping a scope that a reachable pararepo's spec or note takes,
    naming the file.
11. **Pages in a product section.** A `(touches …)` page under a product heading is a page of the
    product's owning repo, and `dead_touches` checks it on that repo's trunk when it can be
    reached. In the owning pararepo, reading-list and fold-in match those scopes against its own
    pages. Where this meets move-to-pararepo's ruling: a page the metarepo moves down to a
    pararepo that reads the one roadmap no longer needs a staged roadmap change. Its items
    follow it in the same commit, into that pararepo's product section, with `(touches …)` at
    the page's new path, and the dead-touch refusal for a moved page says so. The staged
    `target: <repo>` route stays only for a pararepo that still keeps its own roadmap.
12. **Rig per repo.** In a pararepo, the next step comes from the current phases and the one list
    of the products it owns. In the metarepo, it comes from its own phases and list and the
    products it owns as `this repo`. Blocked scopes are skipped and listed as in Part A, across
    products.
13. **RULES.md, Roadmap.** "The product is the repo" is said precisely, per R6: a repo is for one
    software product, and the hardware that runs it may be defined there, with its pages
    segmented within `docs/` as the hardware skill's board pages are. A metarepo's roadmap gains
    the product level of item 8. The pin rule gains the live-read exception for the roadmap only.

**Part D: moving in, buffered edits, unconfirmed waits**
14. **Edits.** No hubnode edits another repo's content (the owner, 2026-11-21). A pararepo's
    changes to its products' sections are buffered and reach the metarepo by the regular sync
    process, when the owner decides: a BUFFER row and `jig propose`, so the change is written on
    a `propose/<repo>-<slug>` branch in the metarepo, never on its trunk, and merged there at the
    next sync the owner calls. R5's check lets a metarepo's `propose/` branch carry a
    `.jig/roadmap.md` change: its merge is a trunk commit on the metarepo owner's yes, where
    the hook checks shape, refs, rings and touched pages. No other branch may. A pararepo's
    merge writes nothing to the metarepo's roadmap. Labels, names and new products (the glossary
    term and its `Owner:` line) are the metarepo's hubnode's. RULES.md says this.
15. **Moving in, by hand.** This version has no conversion command. Once per pararepo, on the
    owner's yes:
    1. The metarepo's glossary names the product with its `Owner:` line (item 14).
    2. The pararepo proposes its phases as `## <Product> <phase>` sections, and its
       `## No phase` items (its Up next folded in by Part B) as `## <Product> No phase`, by
       item 14; the metarepo merges it.
    3. The pararepo's next commit removes its `.jig/roadmap.md` and `ROADMAP.md` and re-points
       every `Scope:` line to the metarepo's ids. The existing drop guard enforces this.
    4. After the move, the pararepo's hook refuses a `.jig/roadmap.md` while the metarepo's
       roadmap holds a product it owns.
16. **Unconfirmed dependencies are flagged, never blocking.** A cross-product `after` that the
    waited-on product's section doesn't confirm (with `(needed by <ref>)` on the waited-on
    scope or phase) is listed by `jig roadmap` in the metarepo and under rig's Waiting on you,
    for the owner to rule on. It blocks no commit and no step; the blocked state of item 3
    still holds.

## Done when

Every command in a throwaway repo, run with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.

Part A, in a stand-alone repo:
- [ ] (fix fires) `## alpha` with `pairing: … (after alpha/host) (touches docs/x.md)` then `host`: `jig rig` offers `alpha/host`, and lists `next    alpha/pairing  waits on alpha/host` under "Waiting on:", not as the next step. `jig roadmap` shows pairing `open` with `after alpha/host`.
- [ ] (unblocked) Once a spec taking `alpha/host` is complete on trunk, `jig rig` offers `alpha/pairing`.
- [ ] (phase) `## beta` whose note has `(after alpha)` and whose scopes are open, with `alpha` not done: no beta scope is offered or counted as current work. Once alpha is done, beta's first scope is offered.
- [ ] (all blocked) A current phase whose every open scope is blocked: rig offers no next step from that phase and lists each blocked scope. When a scope they wait on, directly or through a chain, is open, unblocked and untaken, rig offers it (R1: "Work gets done as soon as its not blocked"), as a phase's own `(after …)` makes the phase it names current.
- [ ] (a spec on a blocked scope) A waiting spec with `Scope: alpha/pairing` while `alpha/pairing` waits on `alpha/host`: rig lists it under "Waiting on:" as `spec .jig/specs/<it>.md  waits on alpha/host`, not under "Can start now"; once `alpha/host` is done, it can start now.
- [ ] (chain through taken) `alpha/a (after beta/b)`, `beta/b (after gamma/g)`, `gamma/g` open, a waiting spec taking `beta/b`: rig offers `gamma/g`.
- [ ] (ring) `a (after alpha/b)` and `b (after alpha/a)`: the trunk commit is refused, naming the ring once with `alpha/a` and `alpha/b`.
- [ ] (a wait on nothing) `(after alpha/nope)` is refused by line, and so is a scope naming itself.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig` passes.

Part B, in a stand-alone repo:
- [ ] (one list) A roadmap with `## Up next` item `p (touches docs/x.md)` and `## No phase` item `q`: `jig update --apply` folds both into `## No phase`, ids and text kept, and after it a trunk commit adding `## Up next` is refused by line.
- [ ] (taken) A spec with `Scope: No phase/q` commits; `jig roadmap` shows `q` taken, then done once the spec is complete. `Scope: No phase/nope` is refused.
- [ ] (rig) `jig rig` offers `No phase/p` ahead of the current phase's first open scope, never offers `q`, and offers nothing from the list once `p` is done; the merge completing `p`'s spec leaves `p` in the roadmap, shown done.
- [ ] (readers) `jig reading-list docs/x.md` lists `No phase/p`. `jig update --apply --sweep` writes a page's Undefined entry under `## No phase`.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig sweep update` passes.

Parts C and D, in a metarepo `meta` with pararepos `pa` and `pb`. Both are registered and both are in `meta.json`'s `pararepos`. `meta`'s glossary has `## Walyt` with `` Owner: `pa` `` and `## Familiar App` with `` Owner: `pb` ``. `pa` has `docs/p.md`. Neither pararepo has phases of its own.

Part C:
- [ ] (products) `meta`'s roadmap `## Walyt alpha` with `pairing (after Familiar App alpha/host) (touches docs/p.md)`, `## Familiar App alpha` with `host`, and `## Demos` with one scope commits on `meta`'s trunk, with `docs/p.md` found on `pa`'s trunk. `jig roadmap` in `meta` shows all three phases as current, and no phase line orders one product after another.
- [ ] (Issue 3's symptom gone) `jig rig` in `pa` doesn't offer `Walyt alpha/pairing`. It lists it as waiting on `Familiar App alpha/host`.
- [ ] (progress, live) `pb` merges a job whose spec has `Scope: Familiar App alpha/host`. The hook checks that line against `meta`'s trunk. With no `meta` release and nothing done in `meta`, `jig rig` in `pa` then offers `Walyt alpha/pairing`, and `jig roadmap` in `meta` shows `host` done.
- [ ] (the deadlock refused) Adding `(after Walyt alpha/pairing)` to `host` in `meta` is refused, naming the ring once with both members.
- [ ] (live read) A scope added under `## Walyt alpha` on `meta`'s trunk, with no release: a spec in `pa` with `Scope: Walyt alpha/<it>` commits, and `Scope: Walyt alpha/nope` is refused, naming `meta`'s roadmap.
- [ ] (unreachable) With `pb` removed from the repos file, `jig roadmap` in `meta` shows `Familiar App alpha/host` as `unknown`, naming `pb`. With `meta` removed, a spec commit in `pa` passes its `Scope:` check with a warning naming `meta`.
- [ ] (drop guard) A `meta` commit dropping `Walyt alpha/pairing` while a spec in `pa` takes it is refused, naming that spec.
- [ ] (unphased scope, live) `meta` has `## Familiar App No phase` with item `y (touches docs/y.md)`, `docs/y.md` on `pb`'s trunk. `pb` merges a job whose spec takes `Familiar App No phase/y`. `jig roadmap` in `meta` shows it done, and `pb`'s merge wrote nothing to `meta`. `jig reading-list docs/y.md` in `pb` lists it.
- [ ] (a moved page's items follow it) `meta` has `docs/w.md`, touched by `Walyt alpha/w`. A `meta` commit moving `docs/w.md` down to `pa` (its move line naming `pa/docs/w.md`) with the scope still touching `docs/w.md` is refused, the refusal naming `Walyt alpha/w` and the page's new path in `pa`, and no staged roadmap change. With the scope's `(touches …)` re-pointed in that commit, it passes, the page checked on `pa`'s trunk.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig pararepo metarepo moves boundary` passes.

Part D:
- [ ] (buffered edit) From `pa`, a change to `## Walyt alpha` adding scope `z` goes through a BUFFER row and `jig propose`: it is on a `propose/pa-…` branch in `meta`, the commit on that branch passes `meta`'s hook, and `meta`'s trunk is unchanged until that branch merges. Before the merge a spec in `pa` with `Scope: Walyt alpha/z` is refused; after it, it commits. Nothing in `pa` writes `meta`'s trunk. A `.jig/roadmap.md` change on any other `meta` branch is still refused (R5).
- [ ] (moving in) A `pa` that had `## alpha` with `x`, `## No phase` items `u (touches docs/p.md)` and `v`, and a spec with `Scope: alpha/x`. After `pa`'s proposal of `x` under `## Walyt alpha` and of `u` and `v` under `## Walyt No phase` merges in `meta`, `pa`'s commit removing its `.jig/roadmap.md` and `ROADMAP.md` and re-pointing the spec to `Walyt alpha/x` passes. Re-pointing to a scope `meta` lacks is refused. A spec in `pa` taking `Walyt No phase/v` commits, and `pa`'s reading-list of `docs/p.md` shows `u`, read from `meta`. A new `.jig/roadmap.md` in `pa` is refused.
- [ ] (flagged, not blocking) `Walyt alpha/pairing (after Familiar App alpha/host)` with no `(needed by Walyt alpha/pairing)` under `## Familiar App alpha` commits, and `jig roadmap` in `meta` and `jig rig` there list it as unconfirmed under Waiting on you. Once `pb`'s section confirms it (through `pb`'s proposal, merged), it isn't listed.
- [ ] (stand-alone unchanged) The Part A and B cases pass in a repo with no metarepo. `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig sweep update pararepo metarepo moves boundary sync_buffer` passes. `claude plugin validate ./plugin` passes.

## Out of scope
Later versions, each its own spec once this lands, in the order they build on each other:
- **Labels** (R1–R3): `(labels …)` on a scope, checked against the metarepo glossary's folded terms.
- **Requiring dependency confirmation**: dropped by the owner's ruling ("Remove the requirement that they agree"). The flag is in this version (item 16).
- **Ideas log and open questions leaving the decision log** (R4, R5).
- **The cross-repo report**: stale staged files and `propose/` branches, entries touching labelled scopes, and two names for one thing.
- **A jig edit command** that refuses a line under another repo's product and stages label changes. A **conversion command** for moving in.
- **Phase types** (Prototype/Pilot/Production), **filters**, and **departures** shown across pararepos.
- Issue 2 (bug-metarepo-roadmap-cites) and Issue 4 (empty proposals): landed in bug-pararepo-sync-fixes (8605d2c). Issue 2's live read is `trunk_show`, which item 9 reuses.
- A family whose repos sit on different machines: the reader names an unreachable repo, and nothing more.
- maige-ecosystem's own roadmap rewrite and its glossary's `Owner:` lines: its job (R6).

## Touches
- `plugin/templates/jig/jig.py`:
  - Part A: `SCOPE_LINE`/`split_touches` (an `after` split), `parse_roadmap` (phase `after`), `roadmap_state` (blocked), `roadmap_view`, `cmd_roadmap`, `roadmap_rules` (refs, rings), `rig_next_step`/`rig_state`/`rig_text`.
  - Part B: `parse_up_next`/`parse_no_phase`/`parse_section` (one list), `roadmap_scopes`/`scope_ids` (list ids), `roadmap_state` and `roadmap_view` (list states), `rig_next_step` (the list's first open item naming pages), reading-list and fold-in (list items), `jig merge`'s Up next removal (`built_up_next`, `remove_up_next`: gone), update's `--sweep` and the `## Up next` fold.
  - Part C: `parse_roadmap` (products), `roadmap_state` (current per product, pulled states, unknown), one roadmap reader over `trunk_show` with `meta_checkout`/`repo_path` at the roadmap read sites, `roadmap_rules` (`Scope:` against the metarepo, drop guard across repos), `dead_touches` and `boundary_rules` (owning repo's pages; a moved page's items follow it), `rig_next_step` per repo. Reused, not copied: `trunk_show`, `meta_citations`' roadmap read, `spec_section`/`touches_spans`, `scopes_in`.
  - Part D: R5's check in the rules (a metarepo's propose branch may carry the roadmap), `roadmap_rules` (no roadmap in a moved-in pararepo), `needed by` and the unconfirmed flag in `cmd_roadmap` and `rig_state`.
- `plugin/templates/jig/RULES.md`: Roadmap (dependencies; one list for work with no phase; products; one reader; "the product is the repo"; A touched page exists, for a page moved to a pararepo that reads the one roadmap; R5 and the propose branch), Metarepo and pararepos (live read of the roadmap; edits through the buffer), Workflow (rig's blocked scopes and unconfirmed waits), Commands (`--sweep` writes `## No phase`).
- `plugin/skills/hubnode/SKILL.md` (A roadmap change: a pararepo's edit is a BUFFER row and `jig propose`), `plugin/skills/rig/SKILL.md` (blocked scopes, unconfirmed waits), `plugin/skills/spec/SKILL.md` (`Scope:` ids with a product and the one list; Up next and No phase items in step 5)
- `tests/smoke.sh`: roadmap, rig, sweep, update, pararepo, metarepo, moves, boundary, sync_buffer
- `marketing/FEATURES.md`: a row each for roadmap dependencies, the one list, and the one roadmap across a family
- Process or product: product (jig's behaviour), written in RULES.md and the skills as their homes.

## Alternatives considered
- The report's whole draft (products, edit command, labels, `needed by`, one list, ideas log, report, conversion, about 17 checks) as v1. Rejected for the edit command, labels, the ideas log, the report and conversion, because each is separable, and the owner's standing rule is "Solve the problem, be pragmatic, keep it simple". One list per product and the `needed by` flag joined v1 on the owner's rulings ("I want to reach the end state I specced"; "flag when they dont"). Reason is [seen] (the report's own Done when list).
- Cross-repo refs between separate roadmaps (`(after Maige-Familiar:alpha)`), with no move. Rejected because ruling 8 (R5) puts the scopes in one file, so that syntax would be thrown away, and copies would keep drifting. Reason is [seen].
- Parsing prose waits ("after …", "waits on"). Rejected because prose waits are what hid the ring for a week. Reason is [seen].
- Blocked as a fourth state beside open/taken/done. Rejected because states come from specs and blocked comes from refs. Keeping it a qualifier leaves the view's columns and every state reader alone. Reason is [assumed].
- The product map in `meta.json`. Rejected because R6 names the glossary as "the right place" for ownership, and maige-ecosystem already keeps `Owner:` lines. Reason is [seen].
- Keeping Up next and No phase in the pararepo for v1: rejected. The owner, 2026-11-21: "I want to reach the end state I specced" (R4, R2, R7).
- A pararepo's hubnode editing the metarepo's roadmap on its trunk. Rejected by the owner, 2026-11-21: "I dont like the idea of hubnodes editing each other's content". Reason is [seen].
- Pushing progress from a pararepo's merge into the metarepo. Rejected because it would mean a second repo's commit in every merge, while states are derived everywhere else in jig. Reason is [assumed].
- A staged `kind: roadmap` file with `target: <meta>` for a pararepo's edit, which needs no R5 change. Rejected because the owner settled the BUFFER row and `jig propose` (Q3). Reason is [seen].
- Keeping `## Up next` as the one list's name. Rejected because its items are parked mid-build and No phase's are not started; "No phase" names both, and only the pages decide whether rig offers one. Reason is [assumed].

## Decisions
- `(after …)` comes before `(touches …)` so `TOUCHES` stays anchored at the line's end, and so roadmaps already written in this order (the report's interim advice) parse unchanged.
- A phase's `after` is a line of its own in the note, since a note is prose and has no single line to end.
- Blocked scopes go under rig's "Waiting on:", not "Waiting on you". A blocked scope waits on work, not on an answer. A ring and an unconfirmed cross-product wait are the owner's question, as rig's cycles are now.
- An unreachable repo warns, never refuses: a hook that refuses what it can't read would block every commit while a disk is unmounted.
- The one list is `## No phase` (`## <Product> No phase` for a product), its ids `<heading>/<id>`, so a list item is named like a scope and needs no new id form. Pages are optional; an item naming pages is offered by rig as Up next items are now, one naming none never is.
- A built list item stays in the roadmap, shown done, rather than being removed by merge: in a pararepo the merge can't write the metarepo's roadmap, and one rule for every repo is simpler than two.
- Built in four `--partial` parts (A dependencies, B one list, C one roadmap, D moving in and edits), so each review sees one idea and A and B help every repo before the metarepo work lands.

- Decided from the rulings, the hubnode, 2026-11-21 (the spec read's four questions):
  - R5 lets a metarepo's `propose/` branch carry a roadmap change: the owner's Q3 ruling ("Q3 agree, settled": a BUFFER row and `jig propose`) can't work without it, and the branch's merge is still a trunk commit on the owner's word.
  - The one list's form (`## No phase`, `## <Product> No phase`, ids `<heading>/<id>`) in every repo: the owner's correction left "the list's syntax" to jig, and R2 asks for "one place for them not two" in a stand-alone repo too.
  - A page moved down takes its items into the product's section in the same commit, once the pararepo reads the one roadmap: the owner's "roadmap items relating to the items being moved should move too", now that one roadmap makes it possible; the staged route stays for a pararepo with its own roadmap.
  - Built as parts A to D with `--partial`: build order is the hubnode's and the spec role's.

## Open questions for the owner
1. Answered: "1.1 yes", Parts 1 and 2 first, with one list per product joining by the end-state ruling (Owner's rulings). Built as parts A to D.
2. Answered: the first version reaches the end state (Owner's rulings).
3. Answered: a BUFFER row and `jig propose` (Owner's rulings).
4. Answered: `jig roadmap` in the metarepo and rig's Waiting on you (Owner's rulings).

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4

## Owner's rulings, 2026-11-20 and 2026-11-21

Settled 2026-11-21; the body above is revised to these.
- First version (open question 1): "1.1 yes": Parts 1 and 2 first, the rest as later specs.
- Up next and No phase (open question 2): the owner, 2026-11-20: "roadmap items relating to the items being moved should move too." A pararepo's Up next and No phase move up with its phases, and a scope whose `(touches …)` names a page moved down follows it.
- Section edits (open question 3), the owner, 2026-11-21: "I dont like the idea of hubnodes editing each other's content, I think they should buffer the changes and use the regular sync process periodically (as the user decides)." No hubnode edits the metarepo's roadmap from a pararepo: a pararepo's changes to its product sections are buffered and reach the metarepo by the regular sync process, when the owner decides.
- Dependency confirmation (open question 4), the owner, 2026-11-21: "Remove the requirement that they agree and flag when they dont so the user can rule on it." A cross-product `after` the waited-on section doesn't confirm never blocks: it is flagged for the owner to rule on.
- Order, the owner, 2026-11-21: bug-pararepo-sync-fixes and bug-nested-touches first, then move-to-pararepo, then this spec.
- The end state, Source: Dave (owner), 2026-11-21, in maige-ecosystem's hubnode session, on reading that a moved-in pararepo keeps `## Up next` and `## No phase` until a later spec: "I want to reach the end state I specced". One list per product joins Part 2 (item 13), and a moved-in pararepo keeps no `.jig/roadmap.md`.
- Buffered edits (open question 3), the owner, 2026-11-21: "Q3 agree, settled": a BUFFER row and `jig propose`, merged at the next sync the owner calls.
- Unconfirmed dependencies (open question 4), the owner, 2026-11-21: "Q4 agree, settled": flagged in `jig roadmap` in the metarepo and rig's Waiting on you, never blocking.
