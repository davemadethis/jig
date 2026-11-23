# bug-crr-gate-merged-spec: the gate reads a built answer's spec from the merge it makes

Source: hubnode session for jig, 2026-11-23, the third blocking review of cross-repo-roadmap's part B (review-change of 928a645): "the gate's refusal of 'built' on a roadmap list item no spec of the job takes reads the job's spec scopes from a copy the merge doesn't leave". The reviews before it: review of e0c4bb5 (the scopes came from trunk's copy, so a branch re-point from p to q let built on p pass) and review of 734b2b5 (`merged_copies` took both copies when both sides changed the spec, so built on p passed again).

Bug-for: cross-repo-roadmap

## Intent
`jig gate` refuses built on a `## No phase` item that no spec of the job takes, as the merge
leaves the spec. Today it reads that spec from a copy it builds itself, before it makes the
merge, and each way of building the copy has been wrong in a case a review found. This spec
moves the check after the gate's own merge of trunk and reads the spec from that merge's
checkout, so the gate has one merge, not a merge and a model of it.

## Why
- Q: Why did the gate pass built on p at 928a645? A: merge-tree exited 1 for `.jig/decisions.md` alone, so `merged_spec` read the branch's copy, which took p. Trunk had re-pointed it to q.
- Q: Why read a copy at all, when the gate merges trunk itself? A: The built check runs with the fold-in checks, before `merge_trunk` makes the scratch merge. No merged spec exists yet, so each fix built one.
- Q: Why did each copy fail? A: Each was a second model of the merge: both copies, then merge-base sides, then merge-tree's exit code. Each differed from `merge_trunk` in one case. Root: the check runs before its merge.

## Givens
Line numbers at 928a645. Every repro ran in throwaway repos under the session's scratchpad, with `JIG_CONFIG`/`XDG_CONFIG_HOME` set on every jig command, using the plugin's `jig.py` at 928a645 and git 2.53.
- [seen] `cmd_gate` (jig.py:3247) runs the fold-in checks, the built check among them (jig.py:3281-3293), and returns 1 on any of them before `board_refusals`, the scratch checkout and `merge_trunk` (jig.py:3350).
- [seen] `merged_spec` (jig.py:3235) runs `git merge-tree --write-tree --no-messages <rev> <trunk>` and reads REV's copy on any nonzero exit.
- [seen] Repro S3, built on p: trunk re-points `g.md` from p to q and adds `D-001` at the top of `## Unreleased`; the job added `D-?gj` there. merge-tree exits 1, `--name-only` lists only `.jig/decisions.md`, and its tree's `g.md` reads `Scope: No phase/q`. The gate exits 0 and passes built on p.
- [seen] Repro S3, built on q (the same repo shape): the gate refuses `built, but no spec of this job takes No phase/q`. The merge takes q, so the refusal is false.
- [seen] Repro S4: a `git` on PATH whose `merge-tree --write-tree` exits 129, as git older than 2.38 does. Trunk re-points p to q, with no conflict. The gate exits 0 on built on p. The same case with real git refuses on p.
- [seen] In S3 and S4, after `merge_trunk`, the gate's scratch checkout holds `.jig/specs/g.md` with `Scope: No phase/q`. The right answer was on disk in the gate's own checkout.
- [seen] S1 (the branch re-points p to q) and S2 (S1, and trunk appends a line to `g.md`) refuse built on p at 928a645, as smoke 5255 and 5258 expect.
- [seen] `merge_trunk` (jig.py:2281) is `git merge` in the checkout, with append conflicts resolved by `resolve_appends`. It needs no `merge-tree` and so no git 2.38. When anything else conflicts it returns the files, and the gate refuses with "the job resolves that by `jig sync`" (jig.py:3356-3363).
- [seen] Timing in the repro: a fold-in refusal before the merge took 0.37s. A gate through the scratch checkout, the merge, the append resolution and `setup.sh` took 3.08s.
- [seen] RULES.md Fold-in already says the gate refuses "as the merge leaves the spec". `replay_sync` (jig.py:2314) and `changed_since` (jig.py:2367-2369) are `jig merge`'s and keep their git 2.38 floor (RULES.md:639, :643). No other gate check calls `merge-tree`.
- [seen] The spec file is not an append file by default, so the gate's merge of trunk into the commit and `jig merge`'s merge of the branch into trunk leave it with the same text (it was [assumed]; converted by reading): `append_globs` (jig.py:2193) is the board's `append_files` and the decision log. The default `append_files` is `AGENTS.md`, `.jig/ledgers/**` and `.jig/decisions.md` (jig.py:51), and the repro board's is the same, so a spec is not one. A repo that lists `.jig/specs/**` in `append_files` would resolve it the same way in both merges, by `resolve_appends`.

## One layer up
- `gate_pairs`, in the same function, runs after `merge_trunk` and reads the scratch checkout (`where`), because "the merge here is where the two first meet". It is a fold-in answer judged against the merge, and it has none of this bug.
- `jig merge`'s clean path (jig.py:2079) and `close_merged` (jig.py:2148) read `Snapshot(where="index")`: the index of the merge they are making. Neither models that merge.
- The pattern is already in the codebase: a check that needs the merged result runs after the merge and reads it there. The built check is the one that didn't.

## Correction
This is a correction. The check reads the one merge the gate makes, so no second picture of
that merge is left to disagree with it, and no git floor comes with it.

## Change
1. **After the merge.** In `cmd_gate`, the built check leaves the fold-in loop. It runs once
   `merge_trunk` has merged cleanly or resolved appends (`None` or `[]`), before `gate_pairs`.
   It reads each spec of the job (`job_specs` and the note's `Spec:`, as now) from the scratch
   checkout, `where / <path>`, as empty when the file is gone. It reads the roadmap's ids from
   `where / ROADMAP`. The note's own `Scope:` lines count as now.
2. **Same refusal.** It prints what it prints today: "the fold-in in <note> is unanswered:",
   then each line with its `<- built, but …` reason, the "add `Scope: …`" advice, or the
   "gone from <trunk>'s roadmap: `jig sync`" advice. It removes the checkout as the pair
   refusal does, or says how to remove it, and exits 1.
3. **What goes.** `merged_spec` goes, so `cmd_gate` calls no `git merge-tree`, and the gate
   keeps no git floor.
4. **What stays.** The other fold-in refusals (unanswered lines, `item_answer`,
   `pair_problem`, board pages) stay before the scratch checkout. They need no merge.
5. **Refusal order.** Write it down. A merge that needs a hand is refused first, because the
   sync it asks for brings trunk's spec into the job. A wrong built answer is refused after
   the fold-in's other refusals, `board_refusals` and `unreleased_proposals`, and before the
   pairs.
6. **RULES.md, Fold-in.** "as the merge leaves the spec" becomes "as the gate's own merge of
   trunk leaves the spec, read once that merge is made; a merge that needs a hand is refused
   first".

## Done when
Every command runs in a throwaway repo with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.
The base is smoke's `gq` shape: `## No phase` items `p` and `q` on `docs/x.md`, spec `g.md` with
`Scope: No phase/p`, and job G open on it, its note answering one item built and the other untouched.
- [ ] (re-point only) The branch re-points `g.md` from p to q, and built on p: the gate exits 1 with `no spec of this job takes No phase/p`, and no line for q. No `gate-G` checkout is left. This is smoke 5255, with the checkout check added.
- [ ] (re-point and a trunk edit to the spec) Add a trunk commit that appends a line to `g.md`: built on p is still refused, as smoke 5258 expects.
- [ ] (fix fires: a re-point and an append-only conflict) Trunk re-points `g.md` from p to q and adds an entry at the top of `## Unreleased`; the job added one there too. Built on p: the gate exits 1 with `no spec of this job takes No phase/p`. At 928a645 it exits 0.
- [ ] (no false refusal) The same shape, built on q: the gate prints no `no spec of this job takes` line and exits 0. At 928a645 it refuses on q.
- [ ] (git floor) The trunk re-point with no conflict, run with a `git` first on PATH whose `merge-tree --write-tree` exits 129: built on p is refused, as with real git, and nothing mentions git 2.38. At 928a645 it exits 0. `plugin/templates/jig/jig.py` has no `merged_spec`, and `cmd_gate` calls no `merge-tree`.
- [ ] (gone from trunk) Smoke 5261 passes: an item trunk renamed since the handoff is refused as gone from trunk's roadmap, with `jig sync` as the way on.
- [ ] (order) A note with an unanswered line and a wrong built answer: the first gate refuses on the unanswered line and leaves no scratch checkout. Once that line is answered, the next gate refuses on built.
- [ ] (symptom) The scenarios above show the gate no longer reads the spec from a copy the merge doesn't leave: S3 and the git-floor case are the ones 928a645 got wrong.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap` passes, with these cases added to `roadmap`. `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes.

## Out of scope
- `jig merge` doesn't judge the fold-in again if trunk moves between the gate and the merge. Every gate check works that way today. The reason is [seen]: `cmd_merge` (jig.py:1962) refuses a job that isn't gated, and one that `changed_since` finds changed since its note, never a trunk that moved.
- A combined refusal that names the unanswered lines and the wrong built answer in one run. The order costs a second gate in that case, which is rare and cheap next to a fourth model of the merge. The reason is [assumed].
- `jig merge`'s replay floor (git 2.38) stays as RULES.md states it.

## Touches
- `plugin/templates/jig/jig.py`: `cmd_gate` (the built check after `merge_trunk`, reading the scratch checkout), `merged_spec` (gone)
- `plugin/templates/jig/RULES.md`: Fold-in (the gate's own merge; the refusal order)
- `tests/smoke.sh`: roadmap
- Process or product: product (jig's behaviour).

## Alternatives considered
- The review's fix: read merge-tree's tree on exit 0 or 1 with `--name-only`, fall back only when the spec itself is conflicted, and die below git 2.38. Rejected because it is a fourth model of a merge the gate makes anyway, and each of the three strikes was a gap between such a model and `merge_trunk`. It also gives every gate with a built answer a git 2.38 floor its own merge doesn't have (S4, `merge_trunk`). And it still needs a fallback copy for a conflicted spec, where the gate refuses at the merge anyway. This reason is [seen].
- Run every fold-in check after `merge_trunk`. Rejected because the other fold-in refusals need no merge. Each of them would pay for the scratch checkout and the merge, 3.08s against 0.37s in the repro, and would wait behind a merge that needs a hand. This reason is [seen].
- Read the branch's copy and trunk's copy, and take both (e0c4bb5). Rejected: a branch re-point from p to q let built on p pass (strike 1). This reason is [seen].
- Decide by merge base which side changed the spec (`merged_copies`, 734b2b5). Rejected: when both sides changed it, it took both copies, and built on p passed (strike 2). This reason is [seen].
- Refuse the built answer in `jig merge`, which reads the merge's index. Rejected because the merge runs on the owner's word after the check has run. A refusal there sends checked, gated work back. The gate is where the job's answers are judged. This reason is [assumed].

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
