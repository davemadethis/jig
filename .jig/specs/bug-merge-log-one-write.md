# bug-merge-log-one-write: `--merge-log` builds every file's text in one plan and writes each file once

Source: the review of c40e6bf, ideas-log's third blocking review, 2026-11-23, relayed by jig's hubnode: "`--merge-log` silently loses a proposed record whenever `.jig/ideas.md` cites a record." Its should-fix: "the `untouched_entries` docstring (jig.py:7283) contains `## Open`, so Part C's grep finds a hit its expected list doesn't name."
Bug-for: ideas-log

## Intent
`jig update --apply --merge-log` writes each file once, from one plan that holds every file's
final text and every file it removes. The dry run prints that plan, and M2 judges it, so what
the owner is shown, what is checked and what is written are one text. A proposed record lands
in `.jig/ideas.md` with its citations rewritten. A kept register or changelog keeps only what
had no home, and a removed one stays removed. Part C's "none left" check becomes one that runs
in smoke and can fail, over the files a reader takes as rules.

## 1. Why
- Q: Why is `D-002` lost? A: `cmd_merge_log` writes `.jig/ideas.md` with the new idea blocks (jig.py:14864), then `rp["write"]` writes it again from the disk's text (14870). The last write wins.
- Q: Why two texts for one file? A: Round 4 let `record_plan`'s citation pass rewrite `.jig/ideas.md` (14356). The pass reads `plan["write"]` before the disk, but the idea blocks are built outside the plan.
- Q: Why outside it? A: No single plan: `merged_log` makes the log and kept files, `record_plan` the records, `cmd_merge_log` the ideas, each from disk. Root: a file two touch is written twice.

## 2. Givens (line numbers at c40e6bf)
- [seen] The brief's repro, at c40e6bf, in a throwaway repo (scratchpad `bugrepro/repro.sh`, with `JIG_CONFIG` and `XDG_CONFIG_HOME` set). Records `0001` accepted and `0002` proposed, `jig init`, "as record 0001 says." appended to `.jig/ideas.md` and committed, then `jig update --apply --merge-log`. `.jig/ideas.md` reads "as D-001 says." and has no `### D-002`. The log has only `### D-001`. The record files are staged deleted, and the output says "Written .jig/decisions.md and .jig/ideas.md".
- [seen] The same repro with 41d3735's jig.py keeps `### D-002 Use a log` in `.jig/ideas.md`, but leaves "as record 0001 says." unrewritten. Round 4 (1d97721) fixed that by dropping `IDEAS` from the pass's skip (14356).
- [seen] The dry run at c40e6bf prints a third text for `.jig/ideas.md`, with `D-002` present and the citation not rewritten. `ideas_problems` (14803) judges that text, not the one written.
- [seen] The same lost write hits the old files `merged_log` keeps or removes. On trunk 622184b the bug predates this job: `bugrepro/repro2.sh` and `repro3.sh`, the same output at 622184b and at c40e6bf.
  - A kept `DECISIONS.md` whose prose cites "record 0001", merged with a record folder in one run, gets its decision table back, so `D-001` is then in the log and in the register. A kept `CHANGELOG.md` citing a record gets its `## Unreleased` back.
  - A register whose only citation sits in a row is `git rm`'d and reported "removed", then written again and staged as modified.
  - This happens only when the old file cites a record and a record folder merges in the same run. Only then does the pass put it in `plan["write"]`.
- [seen] The round-4 smoke for this ("merge-log records: a citation of a record in .jig/ideas.md is rewritten to its id, as in a page") uses `mlrecs`, which has no open or proposed record. With no new idea blocks the first write changed nothing, so the test passed.
- [seen] Writers of the log and ideas file in one command, at c40e6bf:
  - each written once from one text: `jig init` (881–884), staging resolve (10118, 10121), `fold_ideas` (12411–12412);
  - `number_placeholders` (6504) builds one dict, path to text, and writes each path once;
  - `update --apply`'s `STEPS` run in turn, and each reads the disk when it runs (`swap_log_head` 12299, `fold_ideas` 12407), so a later step builds on the earlier one's write;
  - `cmd_merge_log` is the only one that writes a file twice.
- [seen] Readers have one shape: `with_ideas`, `read_entries_text` and `entries_at` (5957–5980) join the two files for every reader by id. Strike 1's "the join closes the log's last entry" was fixed in that join (0a42f7e), which is the right place.
- [seen] The sibling that does this right: `glossary_plan` (15248) puts README.md's remaining text and the new glossary into `plan["write"]` *before* its pointer pass. The pass reads `plan["write"].get(f)` before the disk (15296) and skips `plan["remove"]`. `cmd_glossary` (15344) then writes each path in `plan["write"]` once and `git rm`s `plan["remove"]`.
- [seen] `record_plan`'s pass has the same read-the-plan-first line (14360). Today only a record folder's index file is in the plan when the pass runs (14349).
- [seen] The three strikes, from the commit messages and the hubnode's brief.
  - Strike 1's findings were separate edge cases of the split, each fixed where it arose.
  - Strike 2's blocking finding was the spec's own grep (`'## Open$'`), which the hubnode had asked for.
  - Strike 3 is the only fix that broke its neighbour.
- [seen] Part C's grep (`git grep -nw '## Open' plugin/`) finds 22 lines at c40e6bf.
  - 6 are in prose files: RULES.md 88, 1159, 1161 and 1557; the update skill 165 and 167. Each names the fold, a log not folded yet, or the hook's refusal.
  - 16 are in jig.py: comments, docstrings, help text and the fold's own messages.
  - Round 4 added the `untouched_entries` docstring (7283) in the same commit that rewrote the grep's expected list, and the list missed it.
- [seen] Smoke already greps the plugin's prose for required words: smoke.sh:5562 and 7369 read `$P/jig/RULES.md` and `$P/../skills/*/SKILL.md`.
- [seen] Smoke already runs `cmd_merge_log` in-process with a function patched (smoke.sh:8017–8024, `parse_register`).
- [assumed] No other command writes one file twice in a way that loses text. I read the writers of the log and the ideas file, and `cmd_glossary`, not every command. The guard below covers `--merge-log` only.

## 3. One layer up
- Siblings: `cmd_glossary` and `number_placeholders` build one dict of final texts and write
  each path once. `update --apply` runs its steps in turn, each re-reading the disk.
  `cmd_merge_log` does neither. It builds texts for one file in three producers, all from the
  same disk text, then writes them in turn, so the last producer's text wins.
- What's structurally different: `record_plan` copied `glossary_plan`'s pass, which reads the
  plan first, but not its seeding. `glossary_plan` puts every text it has made into the plan
  before the pass. `cmd_merge_log` keeps the log (`text`), the kept old files (`keep`), the
  removed ones (`gone`) and the ideas text (`ideas_text`) outside the plan.
- Why each round breaks something next to it: splitting the log into two files gave every
  writer a second output. The readers got one join, and the bugs found in it were fixed in
  the join. `--merge-log`'s writer got an extra write instead. Round 4 made the ideas file the
  third file that two producers write, on a shape already broken on trunk for kept and
  removed files.
- The existing pattern is `glossary_plan`'s: seed the plan, run the pass over it, then write
  once. It is reused as-is: no new mechanism, ledger or check in the hook.

## 4. Workaround or correction
Correction. A workaround would build `ideas_text` from `rp["write"].pop(IDEAS)` and append the
blocks there. It fixes the reported symptom but leaves the kept and removed files, which the
same root breaks on trunk, and leaves the dry run printing a text that isn't written.

## Change
1. **One plan.** Before `record_plan`'s citation pass, `cmd_merge_log` builds a plan of every
   file's final text and every file it removes:
   - the log's text: `merged_log`'s, or the disk's or the seed's;
   - each kept old file's remaining text (`keep`);
   - each removed old file (`gone`), as a removal.

   `record_plan` takes that plan in, as `glossary_plan` builds its own. Its pass then reads a
   file's planned text before the disk (14360 already does this) and skips a planned removal
   as it skips a removed record. The log is read from the plan, and its lines are never
   rewritten, as now. A merged entry citing a record is listed as a citation left as written.
2. **Ideas last.** The new idea blocks (`m["ideas"]` and `rp["ideas"]`) are appended after the
   pass, to the plan's `.jig/ideas.md`. That text is the pass's rewrite of the file, else the
   disk's, else `IDEAS_SEED`. Appending after the pass keeps a new block's
   `Record N before this log.` line out of the citation rewrite.
3. **One write.** The apply branch writes each path in the plan once and `git rm`s each planned
   removal. `.jig/meta.json` and the board, when the run changes them, go in the plan too. No
   other `write_text` remains in the apply branch. "Written …" names what the plan wrote.
4. **Shown and checked as written.** `log_problems` and `ideas_problems` judge the plan's log
   and ideas texts. The dry run prints the plan's `.jig/ideas.md`, and its log when the log is
   not in use, as now.
5. **Part C's check runs in smoke.** In `.jig/specs/ideas-log.md`, Part C's "(none left)" line
   is replaced by one smoke assertion in `ideas_fold`. Among `$P/../skills`, `$P/jig/RULES.md`
   and the repo's `docs/`, the files holding `## Open` as a word are exactly RULES.md and
   `skills/update/SKILL.md`. Review still reads each of their hits, which should name the fold,
   a log not folded yet, or the hook's refusal of it. jig.py is left out of the check: its
   leftover names are comments and the fold's own code, and its behaviour is checked by Parts
   A and B's observables (the seed, the writers, the hook's refusal, survey). The assertion
   passes at c40e6bf, since 0a42f7e brought RULES.md and the skills to the ideas file.

## Done when
Every command in a throwaway repo, run with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`. Each check below is a smoke assertion in the section named.

- [ ] (the symptom, `merge_log`) This is the brief's repro. Records `0001-use-markdown.md` (accepted) and `0002-use-a-log.md` (proposed), then `jig init`. Append "as record 0001 says." to `.jig/ideas.md` and commit. Then run `jig update --apply --merge-log`. Afterwards `.jig/ideas.md` holds `### D-002 Use a log`, `Proposed (2026-01-02).` and `Record 0002 before this log.`, and the appended line reads "as D-001 says.". The staged change commits.
- [ ] (shown as written, `merge_log`) In the same fixture, before `--apply`, the dry run's `--- .jig/ideas.md, as it would be written ---` text is byte for byte the file `--apply` then writes.
- [ ] (kept and removed files, `merge_log`) Merge a register, a `CHANGELOG.md` and a record folder in one run, where the register's prose and the changelog's preamble each cite "record 0001". The kept `DECISIONS.md` has no row of the decision table, and the kept `CHANGELOG.md` has no `## Unreleased`. Each has its citation rewritten to the record's new id. In a second fixture, a register whose only citation is in a row is absent afterwards, and `git status` shows it `D`.
- [ ] (one write per file, `merge_log`) `cmd_merge_log` runs in-process on the kept-and-removed fixture plus an idea citing a record, as smoke.sh:8017 runs it, with `Path.write_text` and `Path.write_bytes` wrapped to record each resolved path. The assertion fails if any path is written twice, or written after the run removes it. Run against c40e6bf's jig.py, it fails, and the work role shows that output once as evidence that the guard fires.
- [ ] (a register's idea, `merge_log`) Accepted records `0001` and `0002`, and a `DECISIONS.md` with `D-001` accepted and `D-002` proposed citing "record 0001". Then `jig init`, commit, and `jig update --apply --merge-log`. The run isn't refused: the records take `D-003` and `D-004` above the register's idea. `.jig/ideas.md` reads `### D-002 b, per D-003`, that rewrite is listed, and the change commits. Nothing in `record_plan` or `cmd_merge_log` reads a file the plan already holds: the record counter and the citation pass read the planned ideas text.
- [ ] (a register that is a record folder's README, `merge_log`) `.jig/meta.json` names `docs/decisions/README.md`, a one-row register, as its entry file, with records `0001` and `0002` beside it. `jig update --apply --merge-log` on a branch removes the README (`D` in `git status`), and the log has `### D-001` once.
- [ ] (Part C's check, `ideas_fold`) The assertion in Change 5 passes. `.jig/specs/ideas-log.md`'s Part C "(none left)" line names that assertion, with no list of jig.py lines.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh merge_log ideas ideas_fold ideas_meta` passes, and so does `python3 .jig/jig.py queue -- .jig/scripts/check.sh`.

## Out of scope
- The `untouched_entries` docstring (jig.py:7283) keeps its `## Open`. It names the fold
  correctly ("an idea folded from an old log's ## Open"), and once Change 5 takes jig.py out of
  the check, the docstring is no finding.
- Rewriting a citation of a record inside an entry the register brings to the log. Log lines
  are never rewritten by the pass, which predates this job. Change 1 only makes the run list
  such a citation as left.
- A write-once guard over every command. `update --apply`'s steps may write one file twice on
  purpose, each step re-reading the disk (`swap_log_head`, then `fold_ideas`), so a global guard
  would refuse a correct run. The guard covers `--merge-log`, the command that builds its texts
  before it writes.

## Touches
- `plugin/templates/jig/jig.py`: `cmd_merge_log` (one plan, one write, the checks and the dry run read the plan), `record_plan` (takes the plan in; its pass reads it first and skips planned removals). Reused, not copied: `glossary_plan`'s seed-then-pass shape.
- `tests/smoke.sh`: `merge_log` (the symptom, shown as written, kept and removed files, one write per file), `ideas_fold` (Part C's check).
- `.jig/specs/ideas-log.md`: Part C's "(none left)" line.
- Process or product: product (jig's behaviour).

## Alternatives considered
- **Put `IDEAS` back in the pass's skip, as at 41d3735.** Rejected because it brings back round 4's finding: an idea citing a merged record keeps "record 0001", which no file names after the run. The reason is [seen] (the repro at 41d3735).
- **Patch `.jig/ideas.md` alone: start `ideas_text` from `rp["write"].pop(IDEAS)`.** Rejected because the kept and removed old files break the same way, on trunk too, and the dry run would still print a text that isn't written. The reason is [seen] (repro2 and repro3 at 622184b and c40e6bf, and the dry run at c40e6bf).
- **Write in turn, as `update --apply`'s steps do: write the ideas text, then run the pass over the disk.** Rejected because a dry run can't write, so it would still show and check a text that differs from what `--apply` writes. The reason is [seen] (the dry run's third text).
- **Keep Part C's full grep and add `untouched_entries` to its list.** Rejected because every round that edits a comment would have to edit the list too. Two of three strikes came from that list (strike 2's regex, strike 3's docstring), and a reviewer runs it by hand rather than smoke. The reason is [seen] (41d3735, 1d97721, and the brief).
- **A guard in jig.py that refuses a second write at run time.** Rejected because a plan held as a dict already can't hold two texts for one path. A smoke test that can fail is enough at R0. The reason is [seen]: AGENTS.md's `Risk: R0 — one user, nothing shipped. Optimize for simplicity and clarity, not assurance.`, and the apply branch writing every path from one dict, `planned`.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
