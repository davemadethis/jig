# Handoff: bug-pararepo-sync-fixes

Commit: 23d2ab6f5a194fe7718c65923e7754a5f0fed7f3
Date: 2026-11-21
Spec: .jig/specs/bug-pararepo-sync-fixes.md
Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): "Two of Maige-Lite's proposal branches in maige-ecosystem have no commit of their own … `git branch --no-merged main`, which the metarepo hubnode's proposal listing uses (hubnode skill, step 5), hides both." B3's proposal "sat unseen for two days."
Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): `jig sync` reports a cite of the metarepo's `.jig/roadmap.md` as a file the release "doesn't have" — "cites maige-ecosystem/.jig/roadmap.md, which maige-ecosystem v3.1.0 doesn't have", at `.jig/ledgers/DEFERRED.md:229`, `.jig/specs/buffer-b1-b4.md:15` and `:16`.
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
<!-- what this delivers, in a few lines -->
Two pararepo-sync fixes:
- An empty proposal branch now shows. `jig propose` (and `jig release`'s buffer proposal) opens the metarepo branch with an opening commit of its own, so the metarepo's `git branch --no-merged` lists it. `jig sync` names a proposal with nothing written past that (or an old branch on trunk's line) as `empty`, giving the opening commit's date (the spec's date for an old branch), the worktree command and the withdraw line, said once. An empty merge, whether the branch is kept or deleted, releases nothing.
- A metarepo roadmap cite is read live. A cite of `<meta>/.jig/roadmap.md` or `<meta>/ROADMAP.md` is read on the metarepo's trunk in its registered checkout, not at the pin, and its message names `<meta> <trunk>`, so a release never asks a pin bump for it. A buffer proposal spec's copies of the rows it lists are history, left unchecked; the Open BUFFER row and DEFERRED rows are still checked.
- Hubnode skill step 5 (both halves) and RULES.md (The sync buffer, Citing the metarepo) say so.

## Done-when evidence
<!-- one line per spec item: the command run and what it printed -->
All runs: `python3 .jig/jig.py queue -- bash tests/smoke.sh pararepo pin_bump sync_buffer buffer_answered` at 23d2ab6: rc=0, 175 PASS, 0 FAIL. `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0. With trunk's jig.py swapped in, all 13 new or changed cases FAIL (the bc43f94 mutation run), and with the fallback guard removed, the deleted-b8 case FAILs (the 23d2ab6 mutation run).

From bug-empty-proposal:
- [x] (fix fires) PASS `propose: the branch opens with a commit of its own, so the metarepo's --no-merged lists it, the release's buffer branch too`. It checks the tip subject `propose: … nothing written yet`. `propose: a branch on the metarepo, …, the metarepo's main untouched` still passes.
- [x] (fix fires) PASS `sync: a proposal with nothing written on it is named empty, with the date, the worktree command and the withdraw, not 'not released'`.
- [x] Old-way branch: PASS `sync: an old-style empty branch whose spec isn't committed yet reads empty since uncommitted` and `… at the metarepo's trunk tip, its row Open, reads empty with the spec's date`.
- [x] PASS `sync: with a commit written on top of the opening commit, the proposal reads not released`. Released: the existing sbland cases pass (`answered P2: sync's own close …`, `withdraw: a withdrawn proposal released anyway …`). Empty merged and released: PASS `buffer: an empty proposal merged into the metarepo and released closes none of its rows`, and `buffer: the same empty proposal, its branch deleted after the merge, still reads not released and closes nothing`.
- [x] `jig release` with an Open row: PASS on the `propose/pr-buffer-v0.1.1` half of the first case above, and `para release: with two Open rows it also makes the one proposal branch` still passes.
- [x] (symptom gone) Fixture `propose/pr-buffer-b3` at mrclone's main, row B3 Open: the two old-style PASS lines above, plus PASS `propose --buffer: there, a new proposal makes a branch the metarepo's --no-merged lists`. Maige-Lite itself is the owner's check, not run here (read-only).

From bug-metarepo-roadmap-cites:
- [x] (fix fires) PASS `para sync: a roadmap cite whose heading the metarepo's trunk has, unreleased, is not named` and `para sync: a roadmap cite of a missing heading names the metarepo's trunk, not the pin` ("which mm main has no heading for", not "doesn't have"). The section's metarepo is `mm`, not `docs`: the MM/PP pair is the one with citation fixtures. PASS also `para sync: a cite of the metarepo's ROADMAP.md view is read on its trunk too`.
- [x] (live) PASS `para sync: the heading committed on the metarepo's trunk, with no release, clears it`.
- [x] (no regression) PASS `para sync: a spec citing <meta>/<path> the pin no longer has is named` (the "doesn't have" case).
- [x] (release) pin_bump: C's spec cites `M/.jig/roadmap.md § Later`, and the v0.1.1 release drops it. PASS `pin bump: a metarepo release with … names each pararepo` with `C: skipped, it cites nothing v0.1.1 broke`. On trunk's code, that case FAILs.
- [x] (copies) PASS `buffer cites: a buffer proposal spec's copy of a row it lists is history; the Open BUFFER row and a DEFERRED row with the same cite are named`. It is in `buffer_answered`, beside its fixture, not `sync_buffer`.
- [x] (DEFERRED stays checked) The same case: `DEFERRED.md:5 cites bam/docs/nopage.md, which bam v… doesn't have`.
- [x] (symptom gone) Maige-OS is the owner's check, not run here (read-only).
- [x] check and the pararepo, pin_bump and sync_buffer sections (plus buffer_answered) pass: see the first paragraph.

## Review
<!-- findings from the adversarial review, and what you did about each -->
- review-work of bc43f94 (tier 2, effort 2): 0 blocking.
  - should-fix 1, an empty proposal merged `--no-ff` then deleted read as released: fixed in 23d2ab6 (`proposal_in`'s fallback skips a merge whose `^2` is the opening commit, plus a smoke case).
  - optional 1, the opening commit's date: taken.
  - optional 2, withdraw said twice: taken.
  - optional 3, a ROADMAP.md live test: taken.
  - optional 4, Touches not naming `buffer_answered`: answered here in Shared files.
  - The three disclosed moves were judged sound.
- review-change of 23d2ab6 (tier 2, effort 2): 0 blocking, all four earlier findings confirmed fixed. Four optionals: three deferred in DEFERRED.md (an amended opening commit, the date test, a merged-and-deleted hint), and the fourth (Touches) answered in Shared files.

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because its documentation is `plugin/templates/jig/RULES.md`, updated here (The sync buffer; Citing the metarepo), with the hubnode skill's step 5.

## Shared files changed
<!-- each shared/common file, and why this job had to touch it -->
- `plugin/templates/jig/jig.py`: `open_proposal`, `proposal_empty`, `opening_commit`, `proposal_in`, `sync_meta`, `meta_citations`, `buffer_copy`. The spec's Change.
- `plugin/templates/jig/RULES.md`: one sentence in The sync buffer; Citing the metarepo.
- `plugin/skills/hubnode/SKILL.md`: step 5, both halves.
- `tests/smoke.sh`: the `pararepo`, `pin_bump` and `buffer_answered` sections. `buffer_answered` isn't in the spec's Touches; its ba-meta/ba-para fixture holds the moot proposal and the buffer rows these cases need. The moot expectation now reads `empty: …; it carries no Open row`.

## Test by hand
<!-- what a person should click or watch -->
In a pararepo: `jig propose --buffer`, then `git -C <meta> branch --no-merged main --list 'propose/*'` lists it, and `jig sync` names it `empty: nothing written on it in <meta> since <date>`. Cite `<meta>/.jig/roadmap.md § <a heading on its trunk>`: sync prints nothing for it.

## Left
<!-- what remains on this job -->
Nothing on this job. Maige-Lite's and Maige-OS's symptom checks are the owner's, after `/jig:update`.
