# Handoff: cross-repo-roadmap

Commit: 678c5d46006c8c154b47bbd428409e46514a27ac
Date: 2026-11-23
Spec: .jig/specs/cross-repo-roadmap.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part B of cross-repo-roadmap: one list for work with no phase, with bug-crr-gate-merged-spec folded in.
- **The list:** `## No phase` is the one list, for parked and not-yet-started work. Each item reads `` - `<id>`: <what> `` and may end with `(after …)` and `(touches …)`. Its id is `No phase/<id>`, which `Scope:` lines take and `(after …)` refs name.
- **States:** `roadmap_full` derives each item's state (open, taken, done) and its waits, exactly as for scopes (`list_phase`). The list is never current. `jig roadmap` lists the items, and ROADMAP.md shows them as an Open/Taken/Done board.
- **rig:**
  - The first open, unblocked, uncovered, untaken item that names pages is the step, ahead of the scope walk. An item naming no pages is offered only as what unblocks a scope that waits on it.
  - A covered or blocked item is listed under Waiting on and never walked to.
  - A spec on a blocked item waits on its refs.
- **Readers:** reading-list and fold-in read the items that aren't done. `dead_touches` and the sweep (`with_list`) use the list too.
- **What goes:** merge's Up next removal (`built_up_next`, `remove_up_next`) and the solo-trunk gate refusal. A built item stays, read done from its spec. Dropping a done item is no drop.
- **The fold:** `## Up next` is folded by `jig update --apply` (`fold_up_next`, fence-aware, ROADMAP.md rewritten). The fold runs only once trunk's committed checker is `ONE_LIST` (STAMP 11) or newer, so the first update installs the checker and the second folds. After it, the hook refuses `## Up next` by line.
- **The gate:** it refuses built on a list item that no spec of the job takes, as its own merge of trunk leaves the spec. `built_untaken` runs after `merge_trunk` in the scratch checkout. An item gone from the merged roadmap is told to `jig sync`.

## Done-when evidence
At 678c5d4, in throwaway repos with `JIG_CONFIG`/`XDG_CONFIG_HOME` set:
- `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig rig_batch sweep update page_contract boundary pin_bump moves pararepo metarepo consolidate update_roles`: rc=0, 663 PASS, 0 FAIL.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0.

Part B (cross-repo-roadmap):
- (one list) PASS "no phase: jig update --apply folds an old ## Up next into ## No phase, ids and text kept", and "no phase: the fold commits on trunk, and a later commit adding ## Up next is refused by line". The real migration from an older checker: PASS "migration:" ×5. The older plugin's update refuses STAMP 11.
- (taken) PASS "no phase: a spec takes a No phase item by its id: it commits, and the item reads taken", "…once the spec is complete, the item reads done, and stays in the roadmap", "…a spec taking an item the list lacks is refused, naming the roadmap".
- (rig) PASS "one list: rig offers No phase/p ahead of the current phase's open scope, and never q", "…with p taken by an open job…", "…the merge completing p's spec leaves p in the roadmap, shown done there and in ROADMAP.md", "…once p is done, rig offers nothing from the list". Also the waits cases: a spec on a blocked item, a scope waiting on a page-less item, a covered item never walked to.
- (readers) PASS "one list: jig reading-list of a file docs/x.md covers lists No phase/p". It reads a code file, a reading the reviewer accepted. Also PASS "sweep: --apply --sweep creates .jig/roadmap.md with both under ## No phase".
- (no regression) the run above.

bug-crr-gate-merged-spec:
- (re-point only) PASS "gate merge: the branch re-points p to q: built on p is refused, nothing on q, and no checkout is left".
- (re-point and a trunk edit) PASS "one list: with trunk editing the spec elsewhere too, the merge still takes only q: built on p is refused".
- (fix fires, and no false refusal) PASS "gate merge: trunk re-points p to q and both sides append to the log: built on p is refused…" and "…the same shape, built on q, passes".
- (git floor) PASS "gate merge: with a git whose merge-tree has no --write-tree, built on p is refused as with real git, and no git floor is named" and "…no merged_spec is left".
- (gone from trunk) a departure from the line's wording: the spec says "Smoke 5261 passes". 5261's shape has the branch re-point p to q while trunk re-points p to p2, which conflicts on g.md's `Scope:` line. Under the new order the gate refuses it first as a merge that needs a hand, and 5261 now asserts that ("one list: trunk re-pointing the Scope: line the branch re-pointed too is a merge that needs a hand, refused first"). The gone-from-trunk refusal is shown by the new clean case gm6, which PASSes: "gate merge: an item trunk renamed since the handoff is refused as gone from trunk, with jig sync as the way on". The spec isn't amended, which would move HEAD off the reviewed commit.
- (order) PASS "gate merge: an unanswered line is refused first, before any checkout", and "…once it is answered, the next gate refuses the wrong built answer, after the merge".
- (symptom) The bug spec's repro scripts, copied with their paths moved: S1, S2, S3c, the S4 shim and scen3-p are refused on p, and scen3-q passes.
- (no regression) the run above.

## Review
1. review-work of 721c5e4, blocking 1 (strike 1):
   - B1: the migration commit was refused by the old checker. Fixed at 5fe0293: the fold waits a run.
   - S1: a spec on a blocked list item showed under Can start now. Fixed.
   - S2: built on an untaken item. Fixed with the gate refusal.
   - O1: fence-aware detection. Taken.
   - O2: ROADMAP.md rewritten by the fold. Taken.
   - O3: the walk reaches list items. Taken.
   - O4: the rig skill line. Taken.
2. review-change of 5fe0293, blocking 0. Should-fixes, all fixed at e0c4bb5:
   - N1: a covered item was walked to.
   - N2: STAMP 11, and the fold keyed on trunk's STAMP.
   - N3: the gate missed a spec's trunk scopes.
   - Optional: the RULES line and the "no checker" message. Taken.
3. review-change of e0c4bb5, blocking 0. S1: the gate read a spec's old Scope (the branch re-point). Fixed at 734b2b5.
4. review-change of 734b2b5, blocking 1 (strike 2):
   - B1: the union when both sides changed. Fixed at 928a645 with `git merge-tree`.
   - S1: the advice for a renamed item. Fixed with the gone-from-trunk refusal.
   - S2: wording. Done.
   - O1, O2: deferred (rows).
5. review-change of 928a645, blocking (strike 3). The bug role wrote bug-crr-gate-merged-spec at 7ee09bc: the built check ran before the merge it needed, and each fix had modelled that merge its own way.
6. bug-crr-gate-merged-spec built at 678c5d4. Its review-change came back with blocking 0:
   - should-fix 1: the 5261 departure, recorded above.
   - optional 2: the "gone" message blames trunk. Deferred (row).
   - optional 3: gm3 doesn't assert no checkout is left. Deferred (row).
   - The trunk_stamp old-path note from round 3 is deferred (row).

## Fold-in
<!-- Every documentation page that covers code this changed: does it still describe the
     code? Replace each ___ and tick the box: the stale sentences are edited (deleting
     counts), or none went stale and this says why. Each roadmap item naming one of those
     pages (an Up next item, or a taken scope) has its own line: keep one answer, built,
     untouched or departed: <why>. An Up next item answered built leaves the roadmap when
     the job merges. The gate refuses an unanswered line. An UNOWNED file has no page
     covering it: add it to docmap in the board, or say why it needs none. A pair line
     (`<id> vs <log> § <ids> (<page>): ___`) is answered after its colon, once for every id
     on it: agrees, narrows: <how>, or conflicts: <resolution>; on a line of several ids,
     narrows and conflicts name at least one of them. jig reads the rest of the line, so it
     stays as jig wrote it. -->
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because its documentation is `plugin/templates/jig/RULES.md`, updated here (Product and project, the sweep, Fold-in with the gate's built refusal, Roadmap's No phase bullet, the view, the hook, The next step, Commands, Decision log's finding line) with the spec, hubnode, rig, update, redocument, review and retro skills.

## Shared files changed
- `plugin/templates/jig/jig.py`: the list's parser, states, readers, rig, the update steps, STAMP, and the gate. This is the product.
- `plugin/templates/jig/RULES.md`: where work with no phase goes (Product and project, the sweep, Fold-in, Roadmap, the view, the hook, The next step, Commands, Decision log).
- `plugin/skills/{spec,hubnode,rig,update,redocument,review,retro}/SKILL.md`: `## Up next` becomes `## No phase`, and update's second run.
- `tests/smoke.sh`: Up next fixtures converted, plus the new "no phase:", "one list:", "migration:" and "gate merge:" cases.

## Test by hand
In a throwaway repo, write `## No phase` with `` - `p`: offline (touches docs/x.md) ``. `jig rig` offers `No phase/p`. Add a spec with `Scope: No phase/p`, complete it, and `jig roadmap` shows p done. In a repo with an old `## Up next`, `jig update --apply` folds it (twice if the checker is older), and a new `## Up next` is then refused.

## Left
- Part C: one roadmap in the metarepo: products by glossary `Owner:`, a live read through `trunk_show`, pulled states, pages in a product section, rig per repo, RULES.
- Part D: buffered edits through `jig propose`, moving in by hand, unconfirmed cross-product waits flagged.
- README.md:44 still says `## Up next`, for the release's README pass.
