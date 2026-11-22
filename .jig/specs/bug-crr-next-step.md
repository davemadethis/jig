# bug-crr-next-step: rig's next step from one walk over the roadmap's waits

Source: hubnode session for jig, 2026-11-22, the third blocking review of cross-repo-roadmap's part A (review-change of 13bda97): "A taken, blocked scope in the current phase never seeds `unblocking_step`, so the work that would unblock it is never offered." The two before it: review-work of 626a69a (a current phase whose open scopes all wait on a scope in another phase offered nothing) and review-change of f495209 (the unblocking chain stopped at a taken scope; a waiting spec on a blocked scope was listed under Can start now).

Bug-for: cross-repo-roadmap

## Intent
Rig's next step comes from one rule over the roadmap's waits, so each case the three reviews
found falls out of the rule and none needs a case of its own. The rule, in one line: walk out
from the unfinished phases up to the current one, nearest first, and offer the first scope
that can start; a blocked or taken scope stands for what it waits on. It holds the owner's R1
ruling ("Work gets done as soon as its not blocked. Blocked items are brought to the user's
attention."), keeps item 4's order (the current phase's own free scope first) and changes
nothing outside part A's step and its Waiting on list for scopes.

## Why
- Q: Why does t6 offer nothing? A: `unblocking_step` starts only from the current phase's open blocked scopes. `alpha/a` is taken (its spec is on trunk), so nothing starts the walk.
- Q: Why did each fix leave a new hole? A: Each fix added one case: a fallback when all are blocked, then the walk through taken scopes, then the specs' waits. None said which work the walk starts from.
- Q: Why was that never said? A: The step is two passes with two rules: a pre-pass over the current phase's open scopes, then a fallback walk seeded from what the pre-pass kept. Root.

## Givens
Line numbers at 13bda97. Probes in a throwaway repo with `JIG_CONFIG`/`XDG_CONFIG_HOME` set
(`bug-crr-next-step-probe.sh` in the hubnode's side-session notes folder, run with `rig --json`).
- [seen] t6 (`## alpha` with `` - `a`: x (after beta/b) ``, `## beta` with `` - `b`: y ``, a waiting spec `Scope: alpha/a`): rig's only item is `spec sa ready waits ['beta/b']`. No next step, while `beta/b` is open, unblocked and untaken.
- [seen] A fourth case of the same hole, through a phase wait. `## alpha` with `(after gamma)` and scope `a`, then `## beta` with `b`, then `## gamma` with `g`. Rig offers `beta/b`, and `alpha/a` shows up nowhere in rig. With a waiting spec taking `beta/b`, rig offers nothing, while `gamma/g` is open, unblocked and untaken, and alpha waits on it.
- [seen] `roadmap_state` (jig.py:10602) makes the first not-done phase whose own waits are done current. So a phase's `(after gamma)` makes the next phase in file order current, not gamma. RULES.md's "as a phase's own wait makes the phase it names current" (RULES.md:991) and the job's (all blocked) Done-when say otherwise.
- [seen] `rig_next_step` (jig.py:14441). The pre-pass (14471–14481) keeps each open scope of a current phase that no rig item takes: blocked ones go to `blocked`, and the first free one is the step. Only if there is no step does `unblocking_step(phases, blocked, …)` (14487) run, seeded from `blocked`. A taken scope passes neither.
- [seen] `unblocking_step`'s walk is already the right walk. It goes breadth first over refs, a phase ref reaching its waits and its scopes, a done scope passed. It returns the first open scope that has no waits and that no rig item takes, and otherwise follows a scope's waits, a taken scope's included.
- [seen] There are two takens. A scope's roadmap state `taken` comes from a spec in trunk's tree, which covers waiting specs and open jobs. Rig's `taken` argument holds the scopes of rig's items, which covers waiting specs and staged files (jig.py:14421). A scope can start only when it is `open` and not in rig's `taken`.
- [seen] The spec side already follows one rule. `rig_state`'s `blocked_by` (jig.py:14549) makes any spec or staged file taking a scope that isn't done and has waits wait on those refs. All three holes are in the step.
- [seen] smoke `roadmap` (tests/smoke.sh:5160–5234) pins today's cases with `rnext`, which prints every next-step item, blocked ones included. Every one of those cases follows from the rule below, unchanged, except three. Those are the cases where `## beta` with `(after alpha)` is written above `## alpha` (5182, 5205, 5208). Each gains a `beta/<scope>:blocked` item, because beta is then in the front.
- [assumed] An open job whose scope turned blocked, because an `(after …)` was added after it opened, is rare. Rig lists no line for it, today or under this rule (Out of scope).

## One layer up
- The sibling: `rig_state` orders items by `Build after` with one computation over the graph (`reach_of`, then a fixpoint), and the spec side of part A (`blocked_by`) is one rule too. The step is the one rig output built as a pre-pass plus a fallback.
- No new pattern is needed. `unblocking_step`'s walk is correct. Only its start is wrong: the pre-pass decides what seeds it. Starting the walk from the front and deleting the pre-pass makes the step one walk.

## Correction
A correction. The step is one walk with one start, so the holes go at their source and no fourth
seed is added. A workaround here would be a fourth case of the same kind (seeding taken blocked
scopes too), and the phase-wait probe shows it would still leave one hole.

## Change
1. **The front.** It is each phase that isn't done, in file order, up to and including the
   current one (`roadmap_state`'s current, unchanged). A phase before the current one that
   isn't done is there because it waits on a phase ref.
2. **One walk.** The step comes from a walk out from the front, nearest first and in file order
   within a round.
   - A phase reaches its waits, then its scopes that aren't done.
   - A done scope is passed.
   - A scope that is `open`, unblocked and not in rig's `taken` is the step, and the walk stops.
   - Any other scope, blocked or taken, reaches its waits.
   - Each ref is visited once.

   The first round is the front's own scopes, so a current phase's own first free scope still
   comes first (item 4). A blocked or taken scope stands for what it waits on, so the work that
   unblocks it is offered (R1). A walk that ends with no step leaves every path at done work or
   work under way, and rig offers no step from the roadmap.
3. **The why.** A step reached past the front's own scopes reads
   `(phase <its phase>; <who> waits on it)`, as today. `<who>` is the front scope whose wait the
   path started from, or the front phase for its own wait.
4. **Waiting on.** Each open, blocked scope of a front phase that no rig item takes is listed
   as `next    <id>  waits on <refs>`, as today, now including a blocked phase before the
   current one. A taken blocked scope is shown by its spec's or staged file's own line
   (`blocked_by`, unchanged).
5. **One function.** `unblocking_step` and `rig_next_step`'s pre-pass become one function
   returning the step and the blocked list. `rig_next_step` keeps its Up next loop in front of
   it, unchanged (part B replaces that loop).
6. **Words.** RULES.md, Roadmap, "The next step" states the rule above, and loses "as a phase's
   own wait makes the phase it names current". The job spec's Change item 4 and its
   (all blocked) Done-when say the same rule.

## Done when
Every command runs in a throwaway repo with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.
"rnext" is smoke's `rnext` (the next-step items' `id:state`, in rig's order), and "waits" means a
line under rig's "Waiting on:".
- [ ] (repro 3, fix fires) t6: `## alpha` with `` - `a`: x (after beta/b) ``, `## beta` with `` - `b`: y ``, a waiting spec `Scope: alpha/a`. Rig offers `beta/b` under Waiting on you, reading `(phase beta; alpha/a waits on it)`. The spec waits on `beta/b`.
- [ ] (repro 1) `alpha/a (after beta/b)`, `beta/b` open: rnext is `alpha/a:blocked beta/b:open`. A phase's `(after …)` after a list or among its Exit when boxes is still read: rig offers `alpha/a`, and `beta/b` is listed waiting on `alpha` (smoke 5205 and 5208, which gain that line).
- [ ] (repro 2) `alpha/a (after beta/b)`, `beta/b (after gamma/g)`, `gamma/g`, with a waiting spec taking `beta/b`: rig offers `gamma/g`, and the spec waits on `gamma/g`. A waiting spec with `Scope: alpha/pairing` while pairing waits on `alpha/host` waits on `alpha/host` and is not under "Can start now".
- [ ] (a phase waiting on a later phase) `## alpha` with `(after gamma)` and scope `a`, `## beta` with `b`, `## gamma` with `g`. Rig offers `beta/b`, and waits lists `next    alpha/a  waits on gamma`. With a waiting spec taking `beta/b`, rig offers `gamma/g`, reading `(phase gamma; alpha waits on it)`.
- [ ] (own first) `## alpha` with `p (after beta/b)` then `f`, and `## beta` with `b`: rig offers `alpha/f`, not `beta/b`, and lists `alpha/p` waiting on `beta/b`.
- [ ] (all blocked) `alpha/a` and `alpha/b`, each `(after alpha/c)`, then `alpha/c (after beta)`, and `beta/z`: rig offers `beta/z (phase beta; alpha/c waits on it)`, as smoke 5190 does today. With `beta/z` taken, rig offers no step and lists all three.
- [ ] (all under way) Every path ends at taken or done work (smoke 5233): no step, and the blocked scope is listed.
- [ ] (phase order) `## beta` with `(after alpha)` above `## alpha`: rig offers `alpha/a1`, and waits lists `next    beta/b1  waits on alpha` (rnext `alpha/a1:open beta/b1:blocked` in rig's order). The smoke case at 5182 is updated to that. Once alpha is done, `beta/b1` is offered.
- [ ] (one function) `plugin/templates/jig/jig.py` has no `unblocking_step`. Its scope step and its scope Waiting on lines come from one function.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap rig rig_batch` passes, with the cases above added to `roadmap`. `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes.

## Out of scope
- An open job whose scope turned blocked after it opened gets no rig line. Its picture is its own `jig next`, and rig reads scopes only for waiting work. The owner may want this one listed too, as a later spec. The reason is [assumed].
- A front phase with no scopes and no exit boxes is never done, so the phases after it never become current. That is today's rule for an empty phase, untouched here.
- Up next items and the one list (part B) come ahead of the walk, as today.

## Touches
- `plugin/templates/jig/jig.py`: `rig_next_step` and `unblocking_step` (one walk from the front)
- `plugin/templates/jig/RULES.md`: Roadmap, "The next step"
- `.jig/specs/cross-repo-roadmap.md`: Change item 4 and the (all blocked) Done-when
- `tests/smoke.sh`: roadmap
- Process or product: product (jig's behaviour).

## Alternatives considered
- Seed `unblocking_step` from the current phase's taken blocked scopes too. Rejected because it is a fourth case added the same way. With a phase wait naming a later phase (`alpha (after gamma)`, `beta/b` taken) it would still offer nothing. This reason is [seen].
- Depth first in file order, so the first scope's blockers come before the phase's next free scope. Rejected because it reverses item 4's order: "own first" would offer `beta/b` ahead of `alpha/f`. Both orders satisfy R1, and breadth first keeps the job spec and smoke as written. This reason is [seen].
- Make the current phase the one a phase wait names. Rejected because it changes `jig roadmap`'s phase line and the view, and a phase may wait on several phases. The front gives rig the same reach without changing them. This reason is [assumed].
- Offer the first open, unblocked, untaken scope anywhere in the roadmap. Rejected because it offers later work no one waits on ahead of the phase line, against "the current phase's first open scope" (RULES.md). This reason is [seen].
- List every blocked scope the walk passes, not only the front's. Rejected because it adds lines without adding information: the step's why already names who waits. This reason is [assumed].

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
