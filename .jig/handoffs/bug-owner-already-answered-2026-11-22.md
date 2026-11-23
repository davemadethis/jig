# Handoff: bug-owner-already-answered

Commit: 1f408da236920f815c49e75e4a6e114e53783b96
Date: 2026-11-22
Spec: .jig/specs/bug-owner-already-answered.md
Source: Daisy hubnode session / 2026-11-20 / the owner (Dave Seeman) (staged as feedback-Daisy-2026-11-20-questions-already-answered.md): "your recommendation is exactly what I already specced. It's what I specifically asked for. Why ask it?" … "I'm asked things that dont need asked."
Review: tier 2, effort 3
Ran: claude-opus-5-5 at medium
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Before a question goes to the owner, the session that writes it checks the owner's own words, and asks only what they leave open.
- `/jig:decision-cards` gets a new section, "Is it open?". A block is only a decision the owner's words leave open. The search covers a staged file's quotes and `## Owner's answers`, a spec's `Source:` quotes (not its Intent), accepted decision entries, and his rulings in the conversation. The question stays open when a fixed rule needs his word, the state moved after the quote, his words disagree, or they settle only part. Each block's context line quotes what leaves it open.
- `/jig:rig` step 1 judges open files by that test and stores `"because"` on each question. §4 says what a start on an open file with unanswered questions does: answered parts go under Decisions, quoted and dated; the rest are built as recommended, each with an `Interpreted:` line.
- `/jig:stage`, `/jig:spec`, and RULES.md Staging and Inbox now rank the owner's quoted words above the stager's text. `/jig:spec` step 1 and `/jig:hubnode` Rulings check the owner's words before asking.
- The owner ruled, 2026-11-22: "No, only my reply here." A fixed rule's word (merge, push, publish, release, a `roles` or config yes) comes only from his reply in the hubnode's conversation; no recorded text gives it. That carve-out is in decision-cards, RULES Staging and Inbox, the hubnode inbox, startup and Release lines, `/jig:release`, `/jig:spec`'s staging line, and `jig inbox`'s closing line.

## Done-when evidence
- DW1: `grep -n "Is it open" plugin/skills/decision-cards/SKILL.md` printed `10:## Is it open?`. `grep -n "decision-cards.*Is it open" plugin/skills/{rig,spec,hubnode}/SKILL.md` found a line in each (rig:35, rig:123, spec:29, hubnode:143 at 1d6547f).
- DW2: rig's JSON shape names `"because"`. In a scratch repo with one staged file, `--store-put` of the spec's JSON printed `stored the judgment of .jig/staging/x.md`, rc=0. The review replayed it through `--json` and `--store-get` intact.
- DW3: RULES.md Staging, `/jig:stage` and `/jig:spec` each except the owner's quoted words from "nothing decided", in the Inbox section's terms.
- DW4: rig §4's "Start on an open file with unanswered questions" bullet.
- DW5 (amended in review): fresh tier-2 workers (claude-opus-5-5) were given the new text. On both inputs they returned no question about the list: 2 of 2 runs. The original before-and-after contrast is **unmet**: under the old text the list question came back in 0 of 2 runs, so no cheap fixture tells the fix from a no-op. What remains guards against regression and does not show the fix works. The outputs are in the shared notes folder, bug-owner-already-answered-symptom-test.md.
- DW6: `python3 .jig/jig.py queue -- .jig/scripts/check.sh` returned rc=0 at 1f408da. `python3 .jig/jig.py queue -- bash tests/smoke.sh inbox staging rig` gave 147 PASS, 0 FAIL. At 31b5eb9, `staging_batches staging rig rig_batch inbox pointers` gave 215 PASS, 0 FAIL.

## Review
Six rounds. Blocking reviews counted 2 of 3.
1. review-work of 1d6547f, 1 blocking (strike 1). Blocking: a staged quote could give a fixed rule's word (merge). Fixed with the "a fixed rule needs the owner's word" case. Should-fixes taken: stale quotes, contradicting quotes, partly clear words, accepted decision entries only. Optional taken: the Intent isn't the owner's words; where answers are recorded. DW5 amended to its positive half. → 78cb20d
2. review-change of 78cb20d, 0 blocking. Should-fixes taken: the quote rule narrowed so the inbox and `queue.overflow` rules stand; rig §4 records answers under Decisions, not the Intent. Optional taken: the spec's What changes and DW5's regression note. → 75ee8a1
3. review-change of 75ee8a1, 0 blocking. Taken: one closed positive sentence, word for word in decision-cards and RULES Staging, replacing the list of places; the spec's What changes aligned. → 8dda569
4. review-change of 8dda569, 0 blocking. It found the sentence contradicted `/jig:hubnode` Release, and that any session can write an inbox quote. The owner ruled, 2026-11-22: "No, only my reply here." Built: only his reply in the hubnode's conversation gives a fixed rule's word; Inbox and the hubnode inbox and Release lines agree; the ruling is recorded under the spec's Decisions. → 31b5eb9
5. review-change of 31b5eb9, 1 blocking (strike 2). Blocking: `jig inbox`'s closing line called quoted owner words the ruling with no exception. Fixed in that one string. Also taken: `/jig:release` line 11, `/jig:hubnode` startup step 4, `/jig:spec`'s staging limit, and the spec's Touches. Deferred to DEFERRED.md, optional [seen]: rigger and send don't warn that a fixed-rule word sent by inbox gets asked again. → 1f408da
6. review-change of 1f408da, at the review role's settings because `jig.py` changed: 0 blocking.

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because jig's docs are `plugin/templates/jig/RULES.md`, updated here: Staging and Inbox carry the same fixed-rule carve-out as the one string changed in `jig inbox`'s closing line.

## Shared files changed
- `plugin/skills/decision-cards/SKILL.md`: the new "Is it open?" section, the one home for the check.
- `plugin/skills/rig/SKILL.md`: step 1's judging and the JSON shape's `"because"`; §4's start-on-open bullet. It conflicts with cross-repo-roadmap in one hunk in step 1, next to that job's next-step bullet. Resolving it is mechanical: keep both bullets.
- `plugin/skills/stage/SKILL.md`: the top line's exception for the owner's quotes and its limits; Resolving's rule for notes.
- `plugin/skills/spec/SKILL.md`: step 1's ask-after-check; the staging line's exception and limit.
- `plugin/skills/hubnode/SKILL.md`: startup step 4, Rulings, the inbox ruling and Release each carry the check or the carve-out.
- `plugin/templates/jig/RULES.md`: Staging (rank, question rule, carve-out) and Inbox (one clause).
- `plugin/skills/release/SKILL.md`: the owner's-word line, added in review.
- `plugin/templates/jig/jig.py`: one printed string in `cmd_inbox`, added in review. No logic changes.

## Test by hand
Stage a feature request whose quote reads `The owner, <date>: "/x lists the nodes connected to it"`, plus a stager note "Decide whether /x lists only connected nodes". Run `/jig:rig`. The file should judge `ready`, with no block about the list. Then put an inbox message quoting "merge it" and run `jig inbox`. The closing line should name the fixed-rule exception, and the hubnode should still ask for the merge word.

## Left
Nothing on this job. Whichever of this job and cross-repo-roadmap merges second resolves the rig step-1 hunk in its sync. DW5's before-and-after contrast stays unmet, for the reason above.
