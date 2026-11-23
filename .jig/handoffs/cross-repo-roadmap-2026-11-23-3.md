# Handoff: cross-repo-roadmap

Commit: e227b4dcb7950e9c331a01b4ee6d502203be36e6
Date: 2026-11-23
Spec: .jig/specs/cross-repo-roadmap.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
The whole of cross-repo-roadmap, in four parts. A, B and C have their own partial notes; this note completes the spec with Part D.
- A (note cross-repo-roadmap-2026-11-22.md, with bug-crr-next-step): `(after …)` on scopes and phases; refs, self-waits and rings refused; blocked scopes; rig's one walk from the front.
- B (note cross-repo-roadmap-2026-11-23.md, with bug-crr-gate-merged-spec): `## No phase` as the one list, ids `No phase/<id>`, states derived. Up next is folded by update (two runs past an older checker, STAMP 11) and then refused. The gate refuses built on an item no spec takes, read in its merged checkout.
- C (note cross-repo-roadmap-2026-11-23-2.md): one roadmap in the metarepo. Products by glossary `Owner:`, one live reader (`Family`), states pulled across the family, a current phase per product, rig per repo, the hooks against meta's trunk, and a moved page's items following it.
- D (this note): buffered edits and moving in.
  - Buffered edits: R5 lets a metarepo's `propose/` branch that `jig propose` opened carry `.jig/roadmap.md`, its roadmap checked there.
  - Moving in: `moving_in` checks every `Scope:` against meta's ids, and needs meta to hold a product of this repo. A moved-in pararepo refuses a roadmap of its own, and its sweep proposes instead, removing a section once meta holds its item.
  - `(needed by …)` on scopes, list items and phases, and unconfirmed cross-product waits listed by `jig roadmap` and rig in meta. Nothing is refused for them.
  - `split_waits` reads `(after …)`, `(needed by …)` and `(touches …)` in any order, and refuses a repeat.
  - Merge re-points `(touches …)` wherever it sits, in sections this repo owns.

## Done-when evidence
Final run on the synced tree e227b4d, in throwaway repos with `JIG_CONFIG`/`XDG_CONFIG_HOME` set:
- `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap family rig rig_batch sweep update page_contract boundary pin_bump moves pararepo metarepo consolidate update_roles sync_buffer`: rc=0, 756 PASS, 0 FAIL.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0.
- `python3 .jig/jig.py queue -- claude plugin validate ./plugin`: "✔ Validation passed".

Parts A, B and C: every Done-when line is evidenced in their notes, by smoke case name. The pointers are above under Built. All those cases still pass in the run above (sections roadmap, rig, sweep, update, family).

Part D, all in smoke section `family`:
- (buffered edit) PASS "family D: jig propose --buffer from pa makes propose/pa-z in meta, and meta's trunk is unchanged", "…meta's propose/ branch carries the roadmap change, and its commit passes meta's hook", "…before the merge, a spec in pa taking Walyt alpha/z is refused", "…after meta merges the proposal, the spec commits, and pa wrote nothing to meta's trunk itself", "…a .jig/roadmap.md change on any other meta branch is still refused (R5)". Also "…a hand-made propose/ branch in meta carries no roadmap change".
- (moving in) PASS "family D: pd's commit removing its roadmap and view, re-pointing to a scope meta lacks, is refused", "…re-pointed to Delta alpha/x, the moving-in commit passes", "…moved in, a spec in pd taking Delta No phase/v commits, and pd's reading-list shows u, read from meta", "…a new .jig/roadmap.md in pd is refused: its plan is meta's". Also the sweep cases (refused, then held by meta and the section removed), and "…removing that roadmap is refused while meta holds none of its products".
- (flagged, not blocking) PASS "family D: Walyt alpha/pairing's wait on Familiar App alpha/host, unconfirmed, is listed by jig roadmap and rig in meta", and "…once pb's proposal confirms it, merged, it isn't listed".
- (stand-alone unchanged) The Part A and B cases pass in repos with no metarepo (sections roadmap and rig), plus the four annotation orders, each repeat refused, and the combined phase line. The full run above. `claude plugin validate ./plugin` passes.

## Review
Parts A to C: their notes list their rounds (A: five rounds, one bug spec; B: six rounds, one bug spec; C: two rounds).
Part D:
1. review-work of a8e6678, blocking 1 (strike 1):
   - B1: `(needed by …)` after `(touches …)` dropped the wait. Fixed at 85deb85.
   - S1: the moved-in sweep never finished. Fixed.
   - S2: the sweep refused in every pararepo. Fixed to the hook's condition.
   - S3: rig put unconfirmed waits to no one. Fixed.
   - O1: a `propose/` branch by name alone. Fixed.
   - O2: `moving_in` with no product in meta. Fixed.
   - O3, O4, O5: deferred (rows).
2. review-change of 85deb85, blocking 1 (strike 2):
   - B1: a repeated annotation hid a wait. Fixed at 0b0ad60.
   - S1: retarget with a wait after `(touches …)`. Fixed.
   - S2: rig changing meta's roadmap. Fixed: rig shows the ruling, the hubnode makes it.
   - O1: `opening_commit` reused. Taken.
   - O2: R2 by name. Deferred (row).
   - O3: sweep `same`. Deferred (row).
3. review-change of 0b0ad60, blocking 0. Should-fixes that contradicted the spec, fixed at 3f5a518 and synced at e227b4d:
   - S1: merge retargeting other repos' touches.
   - S2: phase `(needed by …)` repeats and the combined line.
   - O2: a doubled `(touches …)` with no wait.
   - O4: smoke for a list item.
   - O1 and O3: deferred (rows).
4. review-change of e227b4d, blocking 0 and should-fix 0. Its optional findings are deferred (rows).

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because this repo has no docs/ pages; its documentation is `plugin/templates/jig/RULES.md`, updated by this job across Roadmap (Dependencies, States and blocked, No phase, Products, One reader, Edits, Moving in, Unconfirmed waits, A touched page exists, The next step, R5's propose/ exception), Fold-in, Product and project, the sweep, Commands, and Metarepo and pararepos (the live read). The skills that send work there are updated too: spec, hubnode, rig, update, redocument, review and retro.

## Shared files changed
- `plugin/templates/jig/jig.py`: the product, across all four parts.
- `plugin/templates/jig/RULES.md`: the sections named in Fold-in.
- `plugin/skills/{spec,hubnode,rig,update,redocument,review,retro}/SKILL.md`: where work with no phase goes, product ids, a pararepo's buffered edit, moving in, and unconfirmed waits.
- `tests/smoke.sh`: the `after:`, `no phase:`, `one list:`, `migration:` and `gate merge:` cases in roadmap; the new section `family` (in UNITS); and fixtures converted from Up next.
- `.jig/specs/cross-repo-roadmap.md`: amended through the reviews and the Interpreted ruling. Two bug specs are under it, `bug-crr-next-step.md` and `bug-crr-gate-merged-spec.md`.

## Test by hand
Take a metarepo with pararepos pa and pb, its glossary naming `## App` with `` Owner: `pa`. `` and `## Companion` with `` Owner: `pb`. ``.
- `## App alpha` has `pairing (after Companion alpha/host)`: `jig rig` in pa lists pairing as waiting, and `jig roadmap` in meta flags the wait as unconfirmed.
- pb proposes `(needed by App alpha/pairing)` on host through a BUFFER row and `jig propose --buffer`, and meta merges it: the flag goes.
- pb completes a spec taking `Companion alpha/host`: rig in pa offers pairing, with no release.

## Left
- README.md:44 still says `## Up next`. It's left for the readme-and-docs job.
- The deferred rows from all four parts are in `.jig/ledgers/DEFERRED.md`.
- `marketing/FEATURES.md`'s rows are the hubnode's.
