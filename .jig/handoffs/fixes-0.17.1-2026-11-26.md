# Handoff: fixes-0.17.1

Commit: 2742cfd836cc18dc085eebb2d35d9b865a1199bd
Date: 2026-11-26
Spec: .jig/specs/fixes-0.17.1.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
All three groups of the spec; the job is complete.

**The glossary's title.** The one form opens with `# Glossary`, holding no term and no field
line, above `# Basic terms`; every other heading keeps its level. The check, `jig init`'s seed,
`jig glossary add`, the merge's re-sort and the `--glossary` move follow. `jig update --apply`
adds the title to a 0.17.0-form glossary once trunk's checker takes it (`STAMP` 13 -> 14):
0.17.0's hook refuses a commit adding it, so the first run says it waits and the next adds it.
While trunk's checker is older, the move writes the glossary without the title and says so. The
form check is two problems: a first `#` heading that isn't `Glossary`, and a first `#` heading
after it that isn't `Basic terms`; headings under the title are refused only once `Basic terms`
exists, so older glossaries stay editable. A glossary lacking only the title is never refused for
it, so the log has no Breaking line.

**A spec named with dots.** `spec_name` drops only the folder and a trailing `.md`, and every
spec-name match uses it, so a bare dotted name works in `Kept separate` and `Build after`.

**A metarepo's `Owner:` rewrite.** Trunk's update lists the rewrite and the title as a job's and
writes neither; `jig update --apply` in that job's worktree makes both and nothing else. Elsewhere
the rewrite runs on trunk as before. The owner's ruling: "I think it'd be best to do it through
the job anyway".

## Done-when evidence
Runs, each through `python3 .jig/jig.py queue --`. The full suite was not run: it is the gate's.
- A: `bash tests/smoke.sh` on 42 touched sections (rules update board_split docmap metarepo
  staging staging_batches entry_globs report_fixes pointers removals homes meta_docs glossary
  family family_report roadmap_edit labels roadmap phase_types ideas ideas_fold ideas_meta
  ideas_labels touches_terms merge_log headings consolidate rig rig_batch close moves claims movein
  move glossary_form structure update_per_file update_roles init_old_board designer inbox), on the
  abfcfd3 tree before its last two test line numbers and one log sentence: 1595 PASS, 2 FAIL (two
  `claims` cases expecting old fixture line numbers). Fixed; `claims`: 15 PASS, 0 FAIL.
- B, at c060330: `glossary glossary_form`: 77 PASS, 0 FAIL. `homes meta_docs update`: 214 PASS,
  0 FAIL.
- C, at the 2742cfd tree: `glossary_form glossary metarepo update docmap homes meta_docs
  ideas_meta ideas_fold`: 428 PASS, 2 FAIL (the new job cases committed with subjects a metarepo
  refuses). Fixed; `glossary_form`: 42 PASS, 0 FAIL.
- `.jig/scripts/check.sh` at 2742cfd: exit 0.

The glossary's title:
- Form and check: C, "glossary form: # Glossary then # Basic terms has neither heading problem, a
  glossary lacking only the title has that one, one in neither order both" and the refusal cases.
- Seed, add and re-sort: A (`rules`, the init seed case) and C (`glossary_form`: add writes
  nothing into the title, the sort keeps it first, `jig merge` re-sorts below it).
- `update --apply` adds it, changing no other line, and names it: C, the six "glossary title"
  cases. A throwaway repo on real 0.17.0, run at abfcfd3: 0.17.0's hook
  refused the title added by hand ("the first # heading is Glossary, not `# Basic terms`"); run 1
  said the heading waits and committed; run 2 added it and committed, the diff `+# Glossary` and a
  blank line; run 3 "up to date".
- A titled glossary in the form commits clean: C (prose under the title commits; jig's own
  `docs/glossary.md` has no title problem). jig's own file still lacks `# Basic terms` (its one
  problem, pre-existing); a copy with its `##` terms moved to `###` under it has none. The hook
  on this repo's next commit to it is not yet seen: it waits for the upgrade to 0.17.1.
- Texts: rules-docs.md, the update skill's glossary paragraph, docs/records.md, docs/commands.md.
- `.jig/decisions.md` Unreleased: a Changed line; no Breaking line, since the hook refuses only
  problems a commit adds.
- check and the glossary sections: above.

A spec named with dots:
- One helper: `spec_name`; `grep 'Path(..).stem'` finds no spec, `Kept`, `after` or job match
  (what is left is page paths, skill names and files jig wrote itself).
- Kept separate, and Build after through the merge: A, the seven "dotted" cases PASS
  (`consolidate`).
- `.jig/decisions.md` Unreleased: a Fixed line.
- check, `consolidate`, `rig`, `rig_batch`, `close`: A, no failure among them. No later commit
  changed spec-name code.

A metarepo's `Owner:` rewrite:
- Reproduced before building: a throwaway metarepo on real 0.17.0 whose glossary carries
  `Owner:`; this branch's `update --apply` on trunk (before the fix) rewrote the line, and the
  commit was refused, exit 1: "M3 docs/glossary.md changed: add a line or an entry..." and "M4
  main takes only merges of reviewed branches: commit on a branch". So the fix was built. The same
  flow after it, from real 0.17.0: trunk's update commit passed; in the job's worktree `update
  --apply` rewrote the line and added the title, and that commit passed.
- Smoke: C, the four "glossary job" cases PASS; outside a metarepo, "glossary form: update rewrites
  the Owner: line as Repo: and Kind: software, naming it, and its commit passes" unchanged.
- The update skill's glossary paragraph says both changes are a job's in a metarepo.
- `.jig/decisions.md` Unreleased: a Fixed line.

## Review
- review-work at abfcfd3, 0 blocking. Taken: 1 should-fix (the `--glossary` move waits for the
  checker that takes the title, c060330) and 1 optional (smoke for the metarepo's job-only title
  step, c060330). The second should-fix, the spec's `[assumed]` tag, was fixed on trunk. Deferred: 0.
- review-change at 2742cfd, 0 blocking. Taken: 1 should-fix (the spec's missing Alternatives line
  for the third group, fixed on trunk), 0 optional. Deferred: 3, rows in
  `.jig/ledgers/DEFERRED.md`.

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
- [x] docs/commands.md — updated: the `init` and `glossary` lines show the `# Glossary` title; the `update` line's general statement still holds   (2 files)
- [x] docs/hooks.md — no change because no hook was added or changed, and the page states no glossary rule   (1 file)
- [x] docs/jobs.md — no change because it states nothing about how spec names match or about update's glossary steps   (1 file)
- [x] docs/metarepos.md — no change because its move-in and proposal text on product headings still holds, and it says nothing about update   (1 file)
- [x] docs/records.md — updated: the glossary's form opens with the `# Glossary` title   (1 file)
- [x] docs/workflows.md — no change because it states nothing about how spec names match; consolidate behaves as described   (1 file)

## Shared files changed
- `plugin/templates/jig/jig.py`: the three groups.
- `plugin/templates/jig/rules/rules-docs.md`: the glossary's form, the update steps and the move.
- `plugin/skills/update/SKILL.md`: the glossary paragraphs.
- `docs/records.md`, `docs/commands.md`: the form with the title first.
- `tests/smoke.sh`: the new cases; older fixtures that write a whole glossary open with the title;
  the config stamp is 14.
- `.jig/decisions.md`: one Changed and two Fixed lines under Unreleased.
- `.jig/ledgers/DEFERRED.md`: three rows.
- The glossary templates under `plugin/templates/jig/templates/` are untouched: neither shows the
  file's top.

## Test by hand
- On this repo, after the upgrade to 0.17.1: rebuild `docs/glossary.md` into the form and commit
  it; the hook should name no glossary problem.

## Left
Nothing on this job. `docs/glossary.md`'s rebuild is jig-0.17.0-upgrade's.
