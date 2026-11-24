# bug-merge-log-entry-files: `--merge-log` leaves `entry_files` naming the record files it removes

Source: jig hubnode session / 2026-11-24 / Dave, with Claude (staged as feedback-jig-2026-11-24-merge-log-entry-files.md): `--merge-log` removes a record folder's index but `meta.json` keeps naming it

## Intent
In a metarepo, when `jig update --apply --merge-log` removes a file that `.jig/meta.json`'s
`entry_files` names, `entry_files` stops naming it in the same change, with the log in its
place. This holds whether or not a register or `CHANGELOG.md` merges in the same run. RULES.md
already promises it: "in a metarepo, `entry_files` names the log in place of what was merged".

Opens after ideas-log merges. That job rewrote `cmd_merge_log` and `record_plan` into one plan
that writes each path once (the owner's word, 2026-11-24, in the report). This spec is written
against ideas-log's shape.

## 1. Why
- Q: Why does `entry_files` still name the removed index? A: `kept_entry` drops only `gone`, which holds the registers and `CHANGELOG.md` (`files_in`), not `rp["remove"]`.
- Q: Why only those? A: `kept_entry` predates record folders. When folders came in, their removals went to the board (`board_rewrite` gets `rp["remove"]`), but not to META.
- Q: Why is META not rewritten at all in a folder-only run? A: The write is guarded by `if files_in`. The guard was right when only files could be removed. Root: META's rewrite never learned about the plan's removals.

## 2. Givens
- [seen] Reproduced on trunk 5e40489, in throwaway repos (`JIG_CONFIG`/`XDG_CONFIG_HOME` set; the script is `bug-merge-log-entry-files-repro.sh` in the group's notes folder). The repo is a metarepo (`init --meta`). `docs/decisions/` holds records 0001 and 0002, both accepted, and a `README.md` holding only links to them. `entry_files` is set on trunk, then `--apply --merge-log` runs on branch `ml`.
  - **Case reg**: a root `DECISIONS.md` with one row, and `entry_files: ["docs/decisions/README.md", "DECISIONS.md"]`. The run prints `removed after: docs/decisions/0001-a.md, docs/decisions/0002-b.md, docs/decisions/README.md` and `.jig/meta.json entry_files: ['docs/decisions/README.md', 'DECISIONS.md'] → ['.jig/decisions.md', 'docs/decisions/README.md']`. `git status` shows `D docs/decisions/README.md` and `M .jig/meta.json`. The commit passes the hooks, and `jig rules` prints `ok`.
  - **Case folder**: no register, and `entry_files: ["docs/decisions/README.md", ".jig/decisions.md"]`. The run prints no `entry_files` line. `.jig/meta.json` is not staged, and still names `docs/decisions/README.md` after the commit. The commit passes, and `jig rules` prints `ok`.
- [seen] Reproduced on ideas-log's code at 8921001 (its `plugin/templates` from `git archive ideas-log`, same script). Both cases give the same result. In case reg, ideas-log's summary line reads `Written .jig/decisions.md, .jig/meta.json; … docs/decisions/README.md removed`. In case folder, META is not in the written list.
- [seen] trunk `cmd_merge_log` (jig.py:15511-15514, 15560-15565) and ideas-log `cmd_merge_log` (jig.py:15121-15124, 15164-15168): `kept_entry = [LOG, *[e for e in entry if e not in gone and e != LOG]]`. Both the print and the write sit under `entry is not None and files_in`. On ideas-log, `removals = list(dict.fromkeys(gone + rp["remove"]))` is already built (jig.py:15102), before `kept_entry`.
- [seen] `record_plan` puts the records into `plan["remove"]`, and an index whose `record_index_left` is empty goes there too. An index with anything left is kept and rewritten (`plan["keep"]`, `plan["write"]`). So a kept index exists after the run, and it is right for `entry_files` to keep naming it.
- [seen] The report's other givens hold as written: the reviewer's repro on ideas-log b832061 gives the same output as case reg above.
- [seen] Nothing catches the dangling name later. `jig rules` passes, and `jig update` and `jig survey` print nothing about it (run in case folder, after the commit). No check in jig.py says "an `entry_files` name matches no file".
- [seen] `entry_files` items are globs (`is_entry` → `matches`), but a literal path is the common form (`init --meta` writes two). `old_registers` compares items to paths literally (`f in entry`).
- [assumed] The cost of the dangling name is mostly latent. Today a name that matches nothing counts nothing. If a later change adds a file at that path, it silently becomes an entry file: M3 asks a log line for it, and pararepos cite it. The fix doesn't depend on this; it rests on RULES.md's promise.

## 3. One layer up
- **The board, in the same function.** `board_rewrite` is handed `{files_in} | rp["remove"] | indexes`, so `append_files` and `reserve` stop naming removed records and indexes. META is the one target of the run that was never handed `rp["remove"]`. The fix gives META the set the board already gets.
- **`glossary_plan`** (`--glossary`), the other command that removes an entry file. It rewrites `entry_files` whenever its removal changes it (`if entry != data.get("entry_files")`), and puts META into `plan["write"]`, so the one-plan writer writes it. That is the pattern to follow: decide from what the plan removes, then write META through the plan.
- **The trunk-side rerun** (`stale_board_names`, `in_use and not folders_in`) rewrites only the board. It never touches META, and in a metarepo it can't on trunk, since META changes only in a reviewed merge (M4). That is why the fix belongs in the branch run.
- **Registers and `CHANGELOG.md`** already work: they are in `gone`. Only the folder path has the bug.

## 4. Correction
A correction. `kept_entry` is computed from the run's full removals, and META is rewritten
whenever `entry_files` names one of them. The guard that let META skip a folder-only run is
the thing that produced the symptom, so the fix changes it, not the output.

## General?
Picture a metarepo that keeps its decisions as ADRs (adr-tools, MADR) with an index page. Its
pararepos cite that index, so the index is in `entry_files`, which is ordinary use of both
features as RULES.md describes them. Running `--merge-log` as RULES.md says leaves a config line
naming a file that no longer exists, and nothing ever says so. Any metarepo that names a record
or an index in `entry_files` hits it, and no one has to work against jig to get there. It is
general: keep it.

## Change
In `cmd_merge_log` (ideas-log's shape), nothing else:
1. `kept_entry = [LOG, *[e for e in entry if e not in removals and e != LOG]]`, built from
   `removals` (registers, `CHANGELOG.md`, the folder's records and any index the plan removes),
   not `gone`.
2. One condition, `entry_changes = entry is not None and (files_in or any(e in removals for e in entry))`,
   guards two things: the dry run's `entry_files: … → …` line and the `planned[META]` write
   (staged with the rest of `planned`). A run that merges files keeps rewriting META as today. A folder-only run
   rewrites it only when `entry_files` names something removed, so a run that removes nothing
   it names leaves META byte for byte (no reorder to put the log first).
3. An item is a removal only when it equals a removed path. A glob (`docs/decisions/*.md`) is
   never dropped: it names a place, and a new file there is meant to match.

## Done when
- [ ] Smoke (`merge_log`), the symptom: the report's fixture (case reg above) on a metarepo
  job's branch. After `--apply --merge-log` and the commit, `entry_files` is
  `[".jig/decisions.md"]`: it names neither `DECISIONS.md` nor `docs/decisions/README.md`. The
  output's `entry_files:` line shows that list, and `jig rules` passes. Today it ends
  `['.jig/decisions.md', 'docs/decisions/README.md']`.
- [ ] Smoke (`merge_log`), the fix firing where today nothing runs: case folder above (no
  register, log already named). The dry run prints `.jig/meta.json entry_files:
  ['docs/decisions/README.md', '.jig/decisions.md'] → ['.jig/decisions.md']`. `--apply` stages
  `.jig/meta.json` with that list, and the commit passes the hooks. Today no line prints and
  META isn't staged.
- [ ] Smoke (`merge_log`): an index with prose left after its record rows (kept, rewritten)
  stays in `entry_files`. A glob item (`docs/decisions/*.md`) stays as written.
- [ ] Smoke (`merge_log`): a folder-only run in a metarepo whose `entry_files` names nothing
  removed leaves `.jig/meta.json` unstaged and byte for byte.
- [ ] Every existing `merge_log` and `metarepo` smoke case passes unchanged:
  `python3 .jig/jig.py queue -- bash tests/smoke.sh merge_log metarepo`.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and the full smoke passes.

## Out of scope
- A metarepo that already committed a dangling name with the old code. The trunk rerun can't
  edit META (M4), and no repo is known to have one: this report comes from a review of
  ideas-log, not from a merge in the wild. Its owner removes the line in a job.
- A general check that every literal `entry_files` item matches a file. That is a new rule,
  not this fix, and no report asks for it.
- A glob that matched only removed files. It stays as written, per Change 3.
- `split-merge-log`, the waiting spec that renames `--merge-log` to `jig migrate-log`. It is a
  separate spec. Whichever of the two runs second carries the other's change.

## Touches
- `plugin/templates/jig/jig.py`: `cmd_merge_log` only (`kept_entry`, its print, the META write
  into `planned`), on ideas-log's shape. No other function.
- `tests/smoke.sh`: section `merge_log` only (`sec_merge_log`), new cases beside the metarepo
  job case (`MM`, `ml-meta`) and the records cases (`mlrecs`).
- Not touched: `RULES.md` (its Decision log bullet already promises it), skills, docs,
  `marketing/FEATURES.md` (a fix, no new feature).
- Process or product: product (jig's behaviour).

## Alternatives considered
- Drop removed items in `record_plan` and hand META to it as its own write. Rejected because
  META is cmd_merge_log's: `record_plan` knows nothing of `files_in`, and splitting one list's
  edit across two functions brings back the two-writer shape ideas-log removed. Reason is [seen]
  (ideas-log's one-plan comment, jig.py:15077).
- Rewrite META whenever `kept_entry != entry`. Rejected because `kept_entry` puts the log first,
  so a folder-only run whose list holds the log second would reorder META with nothing removed.
  That is a META diff in a metarepo job for no reason. Reason is [seen] (case folder's list,
  `['docs/decisions/README.md', '.jig/decisions.md']`, shows the order is the owner's).
- A trunk-side repair in the `stale_board_names` rerun, as for the board. Rejected because
  META changes on a metarepo's trunk only through a reviewed merge (M4), and the branch run
  already holds every removal. Reason is [seen] (`branch_needed` die, and the trunk rerun
  writes only CONFIG).
- Warn about the dangling name (a `jig update` or `jig rules` line) instead of preventing it.
  Rejected as a workaround: it reports the symptom after the commit, where the run that made
  it could have avoided it. Reason is [seen] (the run already computes `removals`).
- Drop globs that match a removed path. Rejected because a glob names a place, and RULES.md
  says a new page there needs no edit. Reason is [seen] (RULES.md Metarepo, `entry_files`).

## Decisions
- Written against ideas-log's shape: `removals` and `planned[META]` exist only there. On trunk
  the same two changes are the `kept_entry` line and the `if entry is not None and files_in`
  guards (jig.py:15512-15513, 15560, 15566).
- The second half of the report (META is rewritten only `if files_in`) is the same root, and
  Change 2 fixes it.

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
