# Handoff: bug-deferred-scope

Commit: ae675c7c46153969cf7d526fdf4a998da45bf133
Date: 2026-11-23
Spec: .jig/specs/bug-deferred-scope.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
<!-- what this delivers, in a few lines -->
Every stand-alone repo and metarepo keeps a roadmap, and work a spec leaves for later is a `Later:` line of roadmap ids, never prose that closes with the spec.
- `ROADMAP_SEED` and `ensure_roadmap`: `jig init` writes `.jig/roadmap.md` and `ROADMAP.md` (`init --para` removes an empty one a plain init wrote); a `STEPS` row adds them on `jig update --apply`; roadmap, rig, reading-list, survey, staging, gate and merge commit the seed alone in the trunk checkout on trunk (`seed_held` names what holds it back otherwise: a worktree, another branch, a merge/pick/revert/rebase in progress, a seed left staged, staged changes); handoff only says where it is written. A root `ROADMAP.md` of the repo's own withholds it.
- Hook: on trunk in a stand-alone repo or metarepo, removing the roadmap is refused; with none on trunk, a spec's `Scope:`/`Later:` is refused. A pararepo removing an empty roadmap passes `moving_in`.
- `Later:` (`spec_laters`, `laters_in`, `cited`): checked wherever `Scope:` is, the drop guard included for specs; a note's `Later:` is history, except that moving in checks it while the removed roadmap still has the id.
- `jig gate` prints `Closes with the spec at merge:` (the job's spec and its `Bug-for:` specs: `Later:` ids with their text, Out of scope lines). `close_specs` carries `Scope:`/`Later:` onto the note (a Bug-for spec's onto its job's note, via `job_note`) and prints `left for later by <spec>: <ids>`. `jig rig` lists `Left for later:` (`later` in `--json`), never counted as a question or offered as the next step.
- `jig update --apply --sweep` in a pararepo with no roadmap of its own refuses, naming the glossary `Owner:` term and `jig move-in`, dry run too.
- `in_progress` guards every trunk commit jig makes by itself: the seed, `rig --close`, `sync --answered`, `sync_meta`'s settle.
- RULES.md, the spec template, the spec/review/bug/hubnode/rig/retro/init/update skills, docs/records, glossary, jobs, commands and workflows, and a decisions.md Unreleased entry.

## Done-when evidence
<!-- one line per spec item: the command run and what it printed -->
Commands, all through `python3 .jig/jig.py queue --`: the full smoke at 3c7905c (2003 PASS, 19 FAIL, each an expected change or a bug in a new case, all fixed); then on the synced tree 871dfd3 `bash tests/smoke.sh rules update roadmap family boundary sweep close rig metarepo pararepo buffer_answered phase_types` → 750 PASS, 0 FAIL; at ca46385 `bash tests/smoke.sh family buffer_answered sync_buffer close roadmap pararepo rig` → 438 PASS, 0 FAIL; `.jig/scripts/check.sh` → exit 0.
- [x] init: "roadmap: a fresh init's seed and view commit; jig roadmap exits 0, with no problem, stale or missing line" PASS; "init --meta writes the seed and its view too" PASS.
- [x] family: "pa and pb, a plain init then init --para, keep no roadmap, and jig rig and jig update there write none" PASS; pe (meta holds none) and pe with meta away PASS; pa with meta holding its product PASS; "a pararepo keeping a roadmap of its own: update --apply leaves it as it was" PASS.
- [x] sweep: "family D: in a pararepo meta names no product of, the sweep refuses, naming the Owner: term and jig move-in, writing nothing", its dry run, and meta out of reach PASS; "and the sweep writes its items there, as before" PASS.
- [x] init with own ROADMAP.md: "init in a repo whose root ROADMAP.md is its own writes neither file, says to move it in, and leaves ROADMAP.md byte for byte" PASS.
- [x] update: "the dry run lists the roadmap step", "--apply writes and stages both", "after the commit, update lists nothing for it" PASS.
- [x] roadmap removed by hand: "in the trunk checkout on trunk, jig rig commits the empty structure as its own commit, says so, then prints its picture" PASS; "jig reading-list in a job's worktree writes nothing, says where the roadmap is written, and exits 0 as before" PASS.
- [x] "on trunk in a stand-alone repo, a commit removing .jig/roadmap.md is refused" PASS; family moving-in cases PASS.
- [x] "with no roadmap on trunk, a spec's Scope: line is refused, naming jig roadmap" and the Later: case PASS.
- [x] "on trunk, a spec with Later: No phase/nope is refused with the Scope:-shaped message naming nope" and "with the item added … it passes, and jig roadmap shows it open" PASS.
- [x] "a roadmap change dropping an item a spec's Later: names is refused, naming the spec" and "it passes once the same commit re-points the Later: line" PASS.
- [x] "family: in pa, Later: is checked on meta's trunk as Scope: is" PASS.
- [x] "close: jig gate on a spec with Later: and an Out of scope line prints Closes with the spec at merge:…" and "…with neither prints no such block" PASS.
- [x] "close: the merge prints what the spec left for later, the note's header keeps its Later: line, and the item stays open" PASS.
- [x] The symptom: "close: the symptom: rig lists what the merged job left under Left for later, with its job, and --json under later" and "once a new spec takes No phase/labels, Left for later no longer lists it" PASS.
- [x] "close: an open, pages-less No phase item no note's Later: names stays out of rig, as before" PASS.
- [x] Smoke repos assuming no roadmap were updated (init/update file lists; NR, boundary-meta, sweep and update cases plant a hand-removed roadmap); none deleted.
- [x] `grep -rn -i 'roadmap is optional\|optional: a repo with no\|keeps no roadmap\|if the repo keeps one\|if the repo has a roadmap' plugin/ docs/` → no matches; `grep -n 'Later:'` finds it in RULES.md, the template, the spec, review, bug and hubnode skills, docs/records and docs/jobs.
- [x] check.sh passes; the full smoke is the check role's at the gate.

## Review
<!-- findings from the adversarial review, and what you did about each -->
- review-work of 9df549f: 0 blocking. Should-fixes taken: the seed no longer commits into a merge in progress (`seed_held`, pathspec commit); the drop guard reads specs' `Later:` only; the gate covers Bug-for specs; the hand ROADMAP.md survives a merge (smoke); release accepts the metarepo drop (smoke); refusal lines name their cause; RULES `rig --close` carries `Later:`. O8 (two [assumed] rejections) left: no cheap check, and the fix depends on neither.
- review-change of 4ded1ad: 1 blocking (B1, a Bug-for spec's `Later:` lost at merge): fixed by carrying it to the job's note (`job_note`), smoke added. S1 (wrong advice after a refused seed commit), S2 (moving in re-points notes' `Later:`), O1 (`in_progress` in `rig --close` and `sync --answered`): all taken, with smoke.
- review-change of 871dfd3 (after the sync with phase-types): 0 blocking. Taken: moving in counts a note's `Later:` id only while the removed roadmap has it; `sync_meta`'s settle refuses mid-merge; a `sync --answered` mid-merge smoke case; `job_note` reads the first line; an uncarried `Later:` is said, not claimed; the spec's Touches.
- review-change of ca46385: 0 blocking; three optional findings deferred (DEFERRED.md). The spec's Touches fix and two stale fold-in pages went in 067402b.
- review-change of 067402b (docs only): 0 blocking; three optional findings deferred (DEFERRED.md).
- review-change of ae675c7: 0 blocking. The gate's one CI failure (run 45318274482, `next: jig.py reads the Bug-for: line only in bug_for and bug_specs_at`) is fixed: the gate comment quotes `Bug-for:`; `smoke.sh next close rig` 119 PASS, check exit 0.

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
- [x] docs/commands.md — updated: init's line names the roadmap's empty structure, and `jig roadmap` says it commits a missing one in the trunk checkout   (9 files)
- [x] docs/hooks.md — no change because it names hooks and what they run, not the rules they check   (1 file)
- [x] docs/jobs.md — updated: Merge keeps the spec's `Scope:` and `Later:` lines on the note   (4 files)
- [x] docs/metarepos.md — no change because it says only that a pararepo with a roadmap of its own can move it in, which still holds   (2 files)
- [x] docs/records.md — updated: Roadmap says every stand-alone repo and metarepo keeps one, and adds `Later:`   (4 files)
- [x] docs/workflows.md — updated: the rig paragraph names the work merged jobs left for later   (7 files)

## Shared files changed
<!-- each shared/common file, and why this job had to touch it -->
- `plugin/templates/jig/jig.py`: the build itself (enforcement lives there).
- `plugin/templates/jig/RULES.md`: Roadmap, Handoff gate merge, Workflow, Commands, Documentation (sweep), the metarepo sync paragraph.
- `plugin/templates/specs/_template.md`, the eight skills: Change 15 and 16.
- `docs/glossary.md`, `docs/jobs.md`, `docs/records.md` (Change 17); `docs/commands.md`, `docs/workflows.md` (fold-in, common).
- `tests/smoke.sh`: new cases in rules/update/roadmap/family/boundary/sweep/close/buffer_answered, and the cases that assumed no roadmap after init.
- `.jig/decisions.md` (Unreleased Added/Changed), `.jig/ledgers/DEFERRED.md` (rows), `.jig/specs/bug-deferred-scope.md` (Touches), all common.
- `tests/fixtures/**`: untouched; no update case's expected plan needed the new step.

## Test by hand
<!-- what a person should click or watch -->
In a throwaway repo (`JIG_CONFIG`/`XDG_CONFIG_HOME` set): `jig init`, commit; add `` - `labels`: x `` under `## No phase`; a spec with `Later: No phase/labels` and an Out of scope line; open, hand off, `jig gate` (watch "Closes with the spec at merge:"), merge (watch "left for later by …"), then `jig rig` lists `No phase/labels` under Left for later.

## Left
<!-- what remains on this job -->
Nothing. Change 8's refusal names `jig move-in`, which moving-in-command builds: whichever of the two jobs merges second makes them agree. The FEATURES rows are the hubnode's.
