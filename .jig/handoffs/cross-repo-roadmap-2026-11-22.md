# Handoff: cross-repo-roadmap

Commit: 84518ef2468527d5d50e2706867dee4e9a9e1e7d
Date: 2026-11-22
Spec: .jig/specs/cross-repo-roadmap.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part A of cross-repo-roadmap: roadmap dependencies, with bug-crr-next-step folded in.
- A scope may end `(after <ref>, …)` before any `(touches …)`. A phase may carry an `(after …)` line anywhere outside its `Scopes:`, and it applies to each of its scopes. A ref is `<phase>/<scope>` or `<phase>`. The `(after …)` text leaves the scope's `what`.
- `ref_problems` refuses each of these by line, on trunk in the hook and in `jig roadmap`:
  - a ref to nothing the roadmap has;
  - a ref to itself, its own phase, or (through its phase) one of its own scopes;
  - an empty `(after)`;
  - a second phase `(after …)` line;
  - a ring, named once at the first line writing one of its waits. `rings()` is an iterative Tarjan.
- `roadmap_state` derives `after` and `waits` per scope and `waits` per phase. Blocked is a qualifier, not a state. A phase still waiting on another is never current. `jig roadmap` and ROADMAP.md show `after <ref>` beside an open blocked scope.
- rig: `roadmap_step` is one walk out from the front: every phase that isn't done, up to and including the current one, nearest first, each round in file order. It offers the first open, unblocked scope no rig item takes. A blocked or taken scope stands for what it waits on. A step past the front's own scopes reads `(phase X; <who> waits on it)`. Each open blocked scope of a front phase that no rig item takes is a `blocked` next-step item under Waiting on: (`next    <id>  waits on <ref>`). A waiting spec or staged file whose `Scope:` names a blocked scope waits on that scope's refs, never under Can start now. Waiting on: prints every next-step item as `next    <id>`.

## Done-when evidence
Every case is in `tests/smoke.sh` roadmap, run in throwaway repos with `JIG_CONFIG`/`XDG_CONFIG_HOME` set. `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig rig_batch consolidate`: rc=0, 154 PASS, 0 FAIL, at 84518ef. `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0.

Part A (cross-repo-roadmap):
- (fix fires) PASS "after: rig offers alpha/host and lists alpha/pairing under Waiting on:, not as the next step", "after: the blocked scope is a next-step item in state blocked", "after: jig roadmap shows pairing open with after alpha/host, the (after …) out of its text".
- (unblocked) PASS "after: once the spec taking alpha/host is complete, rig offers alpha/pairing".
- (phase) PASS "after: a phase waiting on another isn't current, and none of its scopes is offered" and "after: once alpha is done, beta's first scope is offered".
- (all blocked) PASS "after: every open scope of the current phase blocked: none offered, each listed, and the scope they wait on through a chain is offered" (`beta/z (phase beta; alpha/c waits on it)`), "after: with the waited-on scope taken, rig offers no step and lists each blocked scope".
- (a spec on a blocked scope) PASS "after: a waiting spec taking a blocked scope waits on its refs, never ready to start", "…blocked by its phase's (after …) waits on the phase", "after: once the scope it waits on is done, the spec can start now".
- (chain through taken) PASS "after: the chain runs through a taken scope: rig offers gamma/g, and the spec taking beta/b waits on it", plus the longer chain and the all-taken case.
- (ring) PASS "after: a ring is refused on trunk, named once with both members" (`line 3: a ring: alpha/a, alpha/b`), "…through a phase's (after …) … at the first line writing one of its waits", "a ring of inherited waits alone is reported at the phase's (after …) line", "jig roadmap reports a ring the trunk already holds".
- (a wait on nothing) PASS "after: a wait on nothing the roadmap has is refused by line", "a scope naming itself is refused by line, and so is one naming its own phase", "(after) with nothing inside is refused by line".
- (no regression) roadmap and rig pass in the run above. Also "after: a chain of 1500 waits commits".

bug-crr-next-step:
- (repro 3, fix fires) PASS "after: a taken blocked scope stands for what it waits on: rig offers beta/b, and the spec waits on it" (`next    beta/b (phase beta; alpha/a waits on it): y`; `spec    .jig/specs/sa.md  waits on beta/b`).
- (repro 1) PASS "after: a scope waiting on a later phase's open scope gets that scope offered" (`alpha/a:blocked beta/b:open`), and the e5 and boxes cases, now `alpha/a:open beta/b:blocked`.
- (repro 2) PASS the chain-through-taken case and the spec-on-a-blocked-scope cases above.
- (a phase waiting on a later phase) PASS "…rig offers the current phase's beta/b and lists alpha/a waiting on gamma", "with beta/b taken, rig offers gamma/g, which alpha waits on" (`(phase gamma; alpha waits on it)`).
- (own first) PASS "after: the current phase's own free scope comes first: rig offers alpha/f, not beta/b, and lists alpha/p".
- (all blocked) and (all under way) PASS, as above.
- (phase order) PASS "after: a phase waiting on another isn't current…": `alpha/a1:open beta/b1:blocked`, `next    beta/b1  waits on alpha`; then beta/b1 once alpha is done.
- (one function) PASS "after: the scope step comes from one function: no unblocking_step is left". Also "after: within a round the walk goes in file order".
- (no regression) the run above. The bug spec's probe script, copied with its paths rewritten, gives each case's expected step.

## Review
1. review-work of 626a69a, blocking 1 (strike 1):
   - blocking: a phase `(after …)` after a list or among the boxes was dropped (e5). Fixed: read wherever it sits outside `Scopes:`.
   - should-fix: a ring reported at line 0. Fixed.
   - should-fix: a blocked phase never offered the scope it waits on (e3). Fixed, then replaced by the walk (5).
   - optional: recursive `rings()`. Fixed, now iterative.
   - optional: `(after)` empty. Fixed. `(After …)` in capitals deferred (row).
2. review-change of f495209, blocking 2 (strike 2):
   - B1: the chain stopped at a taken scope. Fixed.
   - B2: a waiting spec on a blocked scope showed under Can start now. Fixed (`blocked_by`).
   - optional: RULES wording. Taken.
3. review-change of 13bda97, blocking (strike 3): a taken blocked scope in the current phase never seeded the walk (t6). The bug role wrote bug-crr-next-step (d6caeb1).
4. bug-crr-next-step built at 84518ef: one walk from the front, which also fixes its fourth hole (a phase waiting on a later phase).
5. review-change of 84518ef, blocking 0. Optional O1 (a front phase's own scope reads `beta waits on it`), O2 (a broken docstring wrap), and the t8 overlap group with a waiting member under Can start now: all deferred (rows).

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because its documentation is `plugin/templates/jig/RULES.md`, updated here (Roadmap: the Dependencies bullet, States with blocked, The next step's one walk from the front) and `plugin/skills/rig/SKILL.md` (blocked items under Waiting on).

## Shared files changed
- `plugin/templates/jig/jig.py`: the parser, state, ref checks, roadmap view and command, and rig's step and waits. This is the product.
- `plugin/templates/jig/RULES.md`: Roadmap (Dependencies, States, The next step).
- `plugin/skills/rig/SKILL.md`: blocked items under Waiting on.
- `tests/smoke.sh`: the `after:` cases in the roadmap section.
- `.jig/specs/cross-repo-roadmap.md`: item 4 and the Part A Done when, amended from the reviews and the bug spec.

## Test by hand
In a throwaway repo, write `## alpha` with `` - `pairing`: x (after alpha/host) `` and `` - `host`: y ``, then commit. `jig rig` offers alpha/host and lists alpha/pairing under Waiting on:. `jig roadmap` shows `after alpha/host`. Adding `(after alpha/pairing)` to host is refused as a ring.

## Left
- Part B: one list for work with no phase (`## No phase` absorbs Up next; ids `No phase/<id>`; rig, reading-list and fold-in read it; merge's Up next removal goes; update folds the old section).
- Part C: one roadmap in the metarepo (products by glossary `Owner:`, a live read through `trunk_show`, pulled states, pages in a product section, rig per repo, RULES).
- Part D: buffered edits through `jig propose`, moving in by hand, unconfirmed cross-product waits flagged.
- The FEATURES rows are the hubnode's.
