# bug-deferred-scope: every stand-alone repo and metarepo keeps a roadmap, and work a spec leaves for later goes on it, on the owner's word

Source: Dave (owner), 2026-11-23, in jig's hubnode session, after cross-repo-roadmap merged (9ef4031) and he asked about labels: "Seriously? How can a major part of what we agreed on go to deferred without noticing." His ruling on it: "end state was supposed to mean exactly that: everything including labels."

Kept separate from roadmap-labels: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from ideas-log: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from moving-in-command: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from phase-types: the owner, 2026-11-23: "start what you can in parallel"

## Intent
Every stand-alone repo and metarepo keeps a roadmap, with an empty structure if nothing else.
`jig init` writes it, `jig update` adds it where it's missing, and a command that finds none
writes it then. jig writes none in a pararepo, which plans from its metarepo's. Work a spec leaves for later
is never prose that closes with the spec. The spec names it on a `Later:` line of roadmap ids,
and each id must already be on trunk's roadmap. Only a roadmap change on the owner's yes puts
one there, so each deferral is a line he approves. The gate shows what closes with the spec
before the merge question. After the merge, the note keeps the `Later:` line, and `jig rig`
lists each item a merged job left until a spec takes it or the owner drops it.

## 1. Why
- Q: Why did labels vanish? A: They were only in the spec's `## Out of scope`, and `jig merge` deletes the spec, carrying only `Scope:` and staged marks to the note.
- Q: Why only there? A: A spec may defer work in prose. jig's one home for work not started, `## No phase`, needs a roadmap and the owner's word, and jig's repo has no roadmap.
- Q: Why didn't the owner see it as a choice? A: It was folded into open question 1 ("Parts 1 and 2 only"). His later "end state" ruling was applied to one item, and the rest was never asked again. Root: a deferral needs no answer of its own, and a repo may have nowhere to put one.

## 2. Givens (line numbers at trunk 06550ea)
- [seen] `git show 9ef4031^1:.jig/specs/cross-repo-roadmap.md`, `## Out of scope`: "Later versions, each its own spec once this lands", then labels, the ideas log, the cross-repo report, the edit and conversion commands, and phase types, filters and departures. The same list sits beside lines that defer nothing ("dropped by the owner's ruling", "landed in bug-pararepo-sync-fixes", "its job (R6)").
- [seen] In 7fad841, the spec's first version, open question 1 read: "**The first version is Parts 1 and 2 only.** Labels, `needed by`, one list per product, the ideas log, the report and the conversion command follow as later specs. Recommendation: yes." The rulings record "1.1 yes" (2026-11-20). On 2026-11-21: "I want to reach the end state I specced", recorded against moving in only. The rest of the list stayed, and the question stayed "Answered".
- [seen] Reproduced at trunk 06550ea in throwaway repos (`JIG_CONFIG`/`XDG_CONFIG_HOME` set; `scratchpad/bds/repro.sh`). A spec whose Out of scope says "Later versions, each its own spec once this lands: Labels" was built, reviewed, handed off, gated and merged. Afterwards, `jig status`, `jig next`, `jig rig` and `jig roadmap` print "labels" 0 times, with no roadmap and with one. The spec is gone from trunk. The note's header holds `Spec:` and `Scope:` only.
- [seen] `close_specs` (jig.py:10631) carries `Scope:` and each `Source: … (staged as …)` mark to the note's header, then `git rm`s the spec. jig.py has no reader of `## Out of scope`, and none of a note's `## Left` (jig.py:2708). cross-repo-roadmap's final note's Left doesn't name the deferred list.
- [seen] `.jig/ledgers/DEFERRED.md` holds review findings not taken at handoff. The work role writes its rows with no owner word, and retro keeps them apart from No phase items ("not both").
- [seen] A `## No phase` item is written "only on the owner's word" (RULES.md:281, 936). `.jig/roadmap.md` changes only on trunk (R5), shown to the owner as a diff and applied on a yes (hubnode skill, A roadmap change). RULES.md:756-758 already sends unspecced behavior a finding needs to the spec or to "a `## No phase` item".
- [seen] RULES.md:915: "Optional: a repo with no `.jig/roadmap.md` has no roadmap, and nothing here applies to it." jig.py:10054 says the same. `jig init` (jig.py:849) writes the board, `jobs.json`, staging, inbox and the decision-log seed, and no roadmap. The init skill keeps the other templates in the plugin "until first used".
- [seen] Empty roadmaps, tested in throwaway repos. `# Roadmap`, a comment, then `## No phase` with nothing under it commits. `jig roadmap` exits 0, and `jig roadmap --write` writes a `ROADMAP.md` holding only its header. A comment or a prose line *under* `## No phase` is refused: "not a No phase item".
- [seen] In one trunk commit, a new No phase item and a spec whose `Scope:` takes it pass the hook together. `roadmap_rules`' docstring (jig.py:11509) says so.
- [seen] With no roadmap on trunk, a spec's `Scope: No phase/x` commits unchecked: `roadmap_rules` returns at jig.py:11550. A trunk commit that `git rm`s `.jig/roadmap.md` passes too.
- [seen] Repro C: an open No phase item naming no pages appears in `jig roadmap` only. `rig_next_step` (jig.py:15079) skips items with no `touches`, as cross-repo-roadmap decided.
- [seen] `spec_scopes` (jig.py:10525) reads the first `^Scope:` line. `roadmap_rules` checks spec and note ids against trunk's roadmap, or the metarepo's read live. Its drop guard refuses a change dropping an id a spec or note still takes (jig.py:11558-11579).
- [seen] Readers: `Family` (jig.py:10736) gives a pararepo with no roadmap of its own the metarepo's. `roadmap_rules` refuses a roadmap in a pararepo whose products the metarepo's roadmap holds (moved in), and `moving_in` (jig.py:11481) judges the commit that removes one. The commands that read the roadmap are `roadmap`, `rig` (and `--close`), `reading-list`, `handoff` (fold-in lines), `gate` (`built_untaken`), `merge`, `survey`, `staging` and `update` (its review and `--sweep`). The hooks read it through `check_rules`.
- [seen] `jig update --apply --sweep` already creates `.jig/roadmap.md` when absent (jig.py:14669). It refuses when a root `ROADMAP.md` is the repo's own, which "with .jig/roadmap.md would be jig's generated view" (jig.py:14664). `jig merge` rewrites `ROADMAP.md` (jig.py:2095), and `plan_files` lists a hand-written `ROADMAP.md` for review only while `.jig/roadmap.md` is absent (jig.py:14485).
- [seen] jig commands already commit on trunk by themselves: `jig rig --close` ("close finished specs: …") and `jig merge`.
- [seen] Two specs waiting on trunk already defer in prose: `jig-folder.md` and `meta.md`, both 2026-10-29.
- [assumed] A swept repo can hold dozens of pages-less No phase items. This bears only on rig listing what a merged job left rather than all of them.

## 3. One layer up
- Homes for leftover work: the note's `## Left` (work role's prose, read by nothing),
  `DEFERRED.md` (review findings, triaged by retro) and `## No phase` (the owner's list, read by
  `jig roadmap`, rig and fold-in). Only No phase is the owner's, outlives every spec and is
  read by jig. The gaps: nothing routes a spec's deferral to it, and a repo may have no roadmap.
- The pattern already built: `Scope:` is a header line of roadmap ids. The hook checks it, the
  drop guard keeps it pointing at something, and `close_specs` carries it to the note. `Later:`
  is the same line for the opposite relation, with the same three checks reused. RULES.md says
  "a wait written as prose is no wait", and a deferral in prose is no deferral by the same rule.
- Seeding a missing file already has two patterns: init's decision-log seed, and update's
  `STEPS` rows (each one a plan line, a check and an action). The roadmap seed uses both.
- The hubnode's idea, tested: at the gate or merge, turn Out of scope's "later" lines into No
  phase items or drops on the owner's word. It fails as the whole fix. jig can't pick out a
  "later" line without searching words, which RULES.md (Product and project) declines for
  prose. And at the merge the job is built, so "build it in this job" is no longer an answer.
  It stays as the gate's last look.

## 4. Correction
A correction. A deferral becomes a form jig reads (`Later:`) that can only name the owner's
list, and that list exists in every repo. No workaround: the place the symptom shows, the
merge, comes too late for the decision.

## Change
**A. Every stand-alone repo and metarepo keeps a roadmap** (the owner's rulings, Decisions).
1. **The seed**: `# Roadmap`, a comment giving the form (phases, `Exit when:`, `Scopes:`, No phase
   items, trunk only, the owner's word), then `## No phase` with nothing under it. Plus
   `ROADMAP.md`, its view, as `jig roadmap --write` renders it.
2. **`ensure_roadmap`**, one function, used by everything below. It does nothing when trunk has
   a roadmap, or when the repo is a pararepo (`.jig/para.json`), moved in or not. It writes
   nothing while a root `ROADMAP.md` is the repo's own, and says to move it into
   `.jig/roadmap.md` first, as `--sweep` says today. Otherwise it writes the seed and the view.
3. **`jig init`** writes them beside its other files. It runs after the meta or para files, so
   it sees a pararepo's `.jig/para.json`, and leaves them uncommitted like the rest of init.
4. **`jig update`**: a `STEPS` row, "add `.jig/roadmap.md`, the roadmap's empty structure, and
   `ROADMAP.md`, its view". The dry run lists it, and `--apply` writes and stages both.
5. **On read**: `roadmap`, `rig`, `reading-list`, `survey`, `staging`, `gate` and `merge` call
   `ensure_roadmap` first. In the main checkout on trunk, with both paths absent from the work
   tree and nothing staged, it writes both files and commits them as their own commit, `roadmap:
   the empty structure jig init writes`, before the command's own work. It prints that it did.
   Anywhere else (a job's or a detached worktree, another branch, staged changes) it writes
   nothing and prints one line: "`<trunk>` has no `.jig/roadmap.md`: `jig roadmap` in the
   `<trunk>` checkout writes it". The command then reads an empty roadmap, as it reads a missing
   one today. `handoff` runs in a job's worktree, so it only prints the line. Hooks never write.
6. **The hook**, on trunk in a stand-alone repo or metarepo, refuses a commit that removes
   `.jig/roadmap.md`. A pararepo's removal is moving in, which `moving_in` judges as today. In a
   stand-alone repo or metarepo with no roadmap on trunk, it refuses a spec's `Scope:` or
   `Later:` line, naming `jig roadmap` in the trunk checkout.
7. **No "no roadmap" path is left** in a stand-alone repo or metarepo. The messages "no
   roadmap: `<trunk>` has no `.jig/roadmap.md`" and "this repo keeps no roadmap" go, since
   `ensure_roadmap` has run before them or printed its line. The same goes for the comment at
   jig.py:10054 and every docstring that calls the roadmap optional.
8. **`jig update --apply --sweep` in a pararepo writes no `.jig/roadmap.md`**, the owner's
   "paras don't have a roadmap". Today, in a pararepo with no roadmap of its own whose metarepo
   holds none of its products or can't be reached, it writes one (jig.py:14660). There it now
   refuses, writing nothing (no roadmap, no page), and says to propose the product to the
   metarepo first: a glossary term with an `Owner:` line naming this repo, then `jig move-in`.
   The dry run says the same in place of its `--apply` line. A pararepo that already keeps a
   roadmap of its own is left alone: the sweep writes its items there as today. Only the
   sweep's write path changes: moving-in-command is building nearby.

**B. `Later:`**
9. A spec header line beside `Scope:`: `Later: No phase/labels, No phase/ideas-log`. It names the
   roadmap ids (a No phase item or a scope) this spec leaves for later work. Its reader sits
   beside `spec_scopes`/`scopes_in`, for specs and note headers. It never takes an id: the
   id's state is unchanged, so open stays open.
10. The hook checks `Later:` ids wherever it checks `Scope:` ids, with the same refusal. That
   covers a stand-alone repo, a metarepo, a pararepo reading the metarepo's roadmap, and the
   drop guard.
11. **`jig gate`** prints `Closes with the spec at merge:` after its check lines. Under it go the
    spec's `Later:` ids, each with its roadmap text, and every `## Out of scope` line, read with
    `spec_section`. A spec with neither prints no such block.
12. **`close_specs`** (merge, `merge --number`, `rig --close`) carries the `Later:` line to the
    note's header beside `Scope:` and prints `left for later by <spec>: <ids>`.
13. **`jig rig`** gets a `Left for later:` block: each id a landed note's `Later:` names that
    trunk's roadmap still has, open and taken by no spec, as `  <id>  left by <job>: <text>`.
    In `--json` it's under `later`. It isn't counted as waiting on the owner and is never offered
    as the next step. In a family, states come from `roadmap_list(snap, fam)`.

**C. Text**
14. RULES.md:
    - Roadmap: the "Optional" sentence becomes "every stand-alone repo and metarepo keeps one",
      naming init, update and the commands that write it. jig writes none in a pararepo. Add `Later:`.
    - Handoff, gate, merge: the gate's list and the note's `Later:` line.
    - Workflow: rig's block.
    - Commands: `jig roadmap` writes a missing roadmap in the trunk checkout.
15. The spec template:
    - Its `Scope:` comment no longer says "With a .jig/roadmap.md".
    - A `Later:` comment goes beside it.
    - The Out of scope comment: a line there is work nothing will do, or work another named spec,
      job or repo does. Work left for later is a `Later:` id, never a line here.
16. Skills:
    - spec: step 3 drops "If the repo has a roadmap" and "a repo with no roadmap", and adds
      `Later:` and the roadmap change it needs.
    - review: question 1 makes blocking an Out of scope line that leaves work for later, in any
      wording, with no `Later:` id.
    - bug: a symptom left for later is a `Later:` id. One not fixed at all is an Out of scope line
      with its reason.
    - hubnode: a `Later:` item is proposed as a roadmap change, one line per item, never inside
      another question. The merge card carries the gate's `Closes with the spec` lines.
    - rig: the `Left for later` block.
    - retro: drops "if the repo keeps one".
    - init: the roadmap is one of init's files.
    - update: the new step.
17. Docs: `docs/records.md` § Roadmap ("The roadmap is optional" goes, and `Later:` is added),
    `docs/glossary.md` § Roadmap ("It's optional" goes), and `docs/jobs.md` § Merge (one sentence).

## Done when
- [ ] Smoke (init): a fresh `jig init` writes `.jig/roadmap.md` as the seed and `ROADMAP.md`. Committing them passes the hook, and `jig roadmap` exits 0 with no problem lines and no "stale" or "missing" line. `init --meta` writes them too.
- [ ] Smoke (family): in a pararepo, `jig init --para`, `jig update` and `jig rig` write no roadmap. That holds whether the metarepo's roadmap holds its product, holds none, or can't be reached, and `jig roadmap` reads the metarepo's. A pararepo that already keeps a roadmap of its own still has it, unchanged, after `jig update --apply`.
- [ ] Smoke (sweep): in a pararepo with no roadmap of its own and a page holding `## Undefined`, `jig update --apply --sweep` exits non-zero and names the glossary `Owner:` term and `jig move-in`. That holds when the metarepo holds none of its products and when it can't be reached. Afterwards `git status --porcelain` is empty and no `.jig/roadmap.md` exists. In a pararepo that keeps a roadmap of its own, the same sweep writes its items there as today.
- [ ] Smoke (init): in a repo whose root `ROADMAP.md` is its own, init writes neither file, says to move it into `.jig/roadmap.md`, and leaves `ROADMAP.md` byte for byte.
- [ ] Smoke (update): in a repo with no roadmap, `jig update` lists the roadmap step. `--apply` writes and stages both files, and after the commit `jig update` lists nothing for it.
- [ ] Smoke (roadmap): on a trunk whose roadmap was removed by hand before this change, `jig rig` in the main checkout on trunk commits `roadmap: the empty structure jig init writes` with both files, prints that it did, then prints its picture. `jig reading-list` in a job's worktree writes nothing, prints the one line and exits as today.
- [ ] Smoke (roadmap): on trunk in a stand-alone repo, a commit removing `.jig/roadmap.md` is refused. The family section's moving-in cases still pass.
- [ ] Smoke (roadmap): with no roadmap on trunk, a spec's `Scope:` or `Later:` line is refused, naming `jig roadmap`.
- [ ] Smoke (roadmap): on trunk, a spec with `Later: No phase/nope` is refused with the `Scope:`-shaped message naming `nope`. With the item added to `## No phase` in the same commit, it passes, and `jig roadmap` shows `No phase/nope` `open`.
- [ ] Smoke (roadmap): a roadmap change dropping an item a spec's `Later:` names is refused, naming the spec. It passes once the same commit re-points the line.
- [ ] Smoke (family): in a pararepo reading its metarepo's roadmap, `Later: App No phase/x` is checked against the metarepo's trunk as `Scope:` is.
- [ ] Smoke (close): `jig gate` on a job whose spec has `Later: No phase/labels` and an Out of scope line prints `Closes with the spec at merge:`, then both, the id with its roadmap text. A spec with neither prints no such block.
- [ ] Smoke (close): after `jig merge`, the output has `left for later by .jig/specs/<spec>.md: No phase/labels`. The note's header carries the `Later:` line, and `jig roadmap` still shows the item `open`.
- [ ] The symptom, smoke (rig): the repro's case. A spec with `Later: No phase/labels` is built, gated and merged. `jig rig` then lists `No phase/labels` under `Left for later:` with its job, and `jig rig --json` has it under `later`. Today rig prints "labels" 0 times. Once a new spec takes `No phase/labels`, the block no longer lists it.
- [ ] Smoke (rig): an open, pages-less No phase item that no note's `Later:` names stays out of rig's output, as today.
- [ ] Smoke cases whose repos assumed no roadmap after init are updated to the seed. None is deleted to make the suite pass.
- [ ] `grep -n 'Later:'` shows each text Change 14–17 lists. `grep -rn -i 'roadmap is optional\|optional: a repo with no\|keeps no roadmap\|if the repo keeps one\|if the repo has a roadmap'` over `plugin/` and `docs/` finds nothing.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and the full smoke passes.

## Out of scope
- Rebuilding cross-repo-roadmap's deferred list. The owner put it in the specs being written in parallel (the Kept separate lines). Their coverage is the hubnode's to check.
- Finding prose deferrals by their words. jig reads only the form, as with `(after …)`. Review question 1 and the gate's list are the backstop.
- `DEFERRED.md`. Its rows are review findings, the work role's at handoff, and retro triages them. None moves to the roadmap here.
- The note's `## Left`. It is a part's remaining work, tracked by `Partial:`. A final note whose Left names spec'd work is already a gate miss (done-when evidence).
- Listing every pages-less No phase item in rig. Rig keeps to what a merged job left, for the reason under Alternatives.
- Seeding a repo whose hand-written root `ROADMAP.md` is still there. Writing `.jig/roadmap.md` would make that file jig's generated view, and the next `jig merge` would overwrite it, which `--sweep` already guards against (jig.py:14664, 2095). Converting its content isn't jig's to do. So nothing is seeded until the owner moves that file in, and update keeps listing it under Repo files to review.
- The two specs on trunk that already defer in prose (`jig-folder.md`, `meta.md`). They predate the rule. The hubnode decides with the owner whether they close or get `Later:` ids.
- jig's own `.jig/roadmap.md`. `.jig/` changes only by `/jig:update`, so jig's repo gets it at the `/jig:update` after the release that ships this.

## Touches
- `plugin/templates/jig/jig.py`:
  - A: a roadmap seed constant; `ensure_roadmap` (reusing `load_para` and `roadmap_view`); `cmd_init` (after `cmd_meta_init`/`cmd_para_init`); a `STEPS` row (jig.py:12033); the callers `cmd_roadmap`, `cmd_rig`, `cmd_reading_list`, `cmd_survey`, `cmd_staging`, `cmd_gate`, `cmd_merge`, `cmd_handoff`; `roadmap_rules` (no roadmap: refuse `Scope:`/`Later:`; on trunk outside a pararepo: refuse removing the roadmap); the "no roadmap" messages and the comment at jig.py:10054; `cmd_sweep`'s pararepo write path (jig.py:14660) and its dry-run line, nothing else in it.
  - B: a `Later:` reader beside `spec_scopes`/`scopes_in`; `roadmap_rules` (meta-read branch, trunk check, drop guard) and `moving_in`'s check of specs and notes (jig.py:11501); `cmd_gate` (the block, through `spec_section`); `close_specs`; `rig_state`/`rig_text` (`Left for later`, `later` in `--json`), reusing `roadmap_list` and `note_head`.
- `plugin/templates/jig/RULES.md`: Roadmap, Handoff gate merge, Workflow, Commands.
- `plugin/templates/specs/_template.md`
- `plugin/skills/spec/SKILL.md`, `review`, `bug`, `hubnode`, `rig`, `retro`, `init`, `update` (each `SKILL.md`)
- `docs/records.md` (§ Roadmap), `docs/glossary.md` (§ Roadmap), `docs/jobs.md` (§ Merge)
- `tests/smoke.sh`: sections roadmap, close, rig, family, update, sweep, and every section whose repos now get the seed from init. `tests/fixtures/*` only if an update case's expected plan has to list the new step.
- `marketing/FEATURES.md` (gitignored, in the main checkout): a row each for "every repo keeps a roadmap" and `Later:`. These are the hubnode's, before the feature.
- Process or product: product (jig's behaviour), written in RULES.md and the skills as their homes.

## Alternatives considered
- The hubnode's idea as the whole fix: at the gate or merge, Out of scope's "later" lines become No phase items or drops on the owner's word. Rejected because jig can't pick out a "later" line without searching words (the list mixed later, dropped and elsewhere lines), and because by then the job is built and "build it here" is gone. Kept as the gate's print. Reason is [seen] (the list; RULES.md Product and project; the gate and merge order).
- Carrying the spec's `## Out of scope` into the note at close. Rejected because it makes a record with no reader: no jig command reads a note's sections past the header and fold-in. Reason is [seen] (grep).
- `DEFERRED.md` as the home. Rejected because it holds review findings written by the work role without the owner's word, and retro keeps findings and No phase apart. Reason is [seen] (its header; retro skill).
- A separate list for repos with no roadmap (`.jig/later.md`). Rejected by the owner's ruling (every stand-alone repo and metarepo keeps a roadmap; a pararepo plans from its metarepo's), and because a second list is the drift cross-repo-roadmap removed when it folded Up next. Reason is [seen].
- A `## Later` section in the spec. Rejected because it closes with the spec like Out of scope does. A header line of ids is what `close_specs` already carries. Reason is [seen] (`close_specs`).
- Rig listing every open pages-less No phase item. Rejected because cross-repo-roadmap decided rig doesn't offer them, and a sweep can write many. Listing what a merged job left keeps rig to agreed work. Reason is [seen] for the decision and [assumed] for the count. The fix doesn't depend on the count.
- Skill text only, the hubnode asking each deferral as its own card. Rejected as the whole fix: this deferral was asked, inside a bundled question, and answered "1.1 yes". Enforcement lives in jig.py. Reason is [seen] (7fad841; AGENTS.md Code).
- Writing the seed on read and staging it without a commit. Rejected because a staged roadmap leaves trunk's checkout dirty, and `rig --close` and `merge` refuse a dirty tree. Reason is [seen] (smoke "close: --close on a dirty tree is refused").
- Writing the seed from a hook. Rejected because a hook judges the commit in progress, and a file it wrote would land in that commit or none. Reason is [assumed]. Nothing depends on it, since no hook writes today.
- A roadmap-less read treated as an empty roadmap, with nothing ever written. Rejected by the owner's ruling: "roadmap should be created at that time". Reason is [seen].

## Decisions
- The owner's ruling, 2026-11-23, answering this spec's open question 1: "After running update there should be no repo without a roadmap and it's structure should be there even if it's empty. If a command is somehow run and there is no roadmap, roadmap should be created at that time just like it would've from update. Update should leave a repo with what a new init [would have] created (regarding roadmap)". Change A builds it.
- The owner's ruling, 2026-11-23, on pararepos: "Fair, paras don't have a roadmap, so this applies to regular repos and metas". Change A covers stand-alone repos and metarepos only. `ensure_roadmap` writes nothing in a repo with `.jig/para.json`, moved in or not, so a metarepo it can't reach needs no warning. A pararepo that already keeps a roadmap of its own keeps it until moving in, as today: jig neither removes it nor creates one.
- The seed written on read is committed in the trunk checkout only, as its own commit. R5 keeps the roadmap on trunk, `rig --close` and `merge` already commit there by themselves, and the ruling is the owner's yes for the empty structure.
- The sweep's refusal names `jig move-in`, which moving-in-command builds; trunk at 06550ea has no such command. The one of the two jobs that merges second makes the message and the command agree.
- The seed's comment sits above `## No phase`, because under it the hook refuses any line that isn't an item. Reason [seen].
- `Later:` may name a scope as well as a No phase item. A scope not yet built is a home that outlives the spec too.
- `Later:` never changes an id's state. A deferred item stays open, so rig can list it.
- Rig's `Left for later` block isn't counted as waiting on the owner. It is work he already placed, shown so it can't drop out of sight.

## Open questions for the owner
1. Answered (Decisions): every stand-alone repo and metarepo keeps a roadmap, written by init, update or the first command that finds none. A pararepo gets none.

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
