# jig-0.17.0-upgrade: bring this repo to jig 0.17.0, with a rollback point recorded first

Source: jig hubnode session / 2026-11-26 / the owner (staged as jig-0.17.0-upgrade.md)

Source: the owner, 2026-11-26, in jig's hubnode session: "everything in this latest release, since the one before it, needs to be applied to every repo, including but not limited to updating roadmaps … Require that each hubnode checks jig and its own repo to make sure the process is what it would recommend also. Each hubnode should also commit and push before running the spec, and remember that point so that it can rollback if needed, and that rollback point will be recorded into its spec before the job opens and must be recorded in the handoff when it finishes."

Rollback: main at 357a0d37f4cf5afebfca42bbcae51711c19fa42e, pushed to origin on 2026-11-26

## Intent
This repo (a stand-alone repo: no `.jig/meta.json`, no `.jig/para.json`) runs jig 0.17.0's
layout and formats, every 0.17.0 change applied, from a pushed rollback point recorded here
before anything runs and again in the handoff.

## Steps
The hubnode runs these in order. `jig` is `python3 .jig/jig.py`, and the plugin's copy is
`python3 "${CLAUDE_PLUGIN_ROOT}/templates/jig/jig.py"`.

1. **Rollback point.** On trunk, in the trunk checkout: `git status -sb` shows trunk, nothing
   in the tree is uncommitted (commit it, or ask the owner about it), and no job is open
   (`jig status`; `jig update` refuses while one is: merge it or close it, on the owner's
   word). Push trunk, on the owner's word in this conversation (a spec can't give it). Then
   write the `Rollback:` line above, as `Rollback: <trunk> at <full sha>, pushed to <remote>
   on <date>`, commit this spec with only that change, and push again on the same word. Save
   the line to the session's memory too. Nothing below runs before this commit is pushed.
2. **Process check.** Before the job opens, read jig and this repo, and fill
   `## Process check` below:
   - the plugin is 0.17.0 (`version` in `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json`);
     if not, the owner updates the plugin first;
   - jig's 0.17.0 release notes (`gh release view v0.17.0 --repo davemadethis/jig`), the
     plugin's `/jig:update` skill and `rules-roadmap.md` in
     `${CLAUDE_PLUGIN_ROOT}/templates/jig/rules/`;
   - the plugin's update dry run (`python3 "${CLAUDE_PLUGIN_ROOT}/templates/jig/jig.py" update`)
     and what it lists for this repo;
   - this repo's own files that name what 0.17.0 moved or renamed: `grep -rn` across tracked
     files outside `.jig/` for `RULES.md`, `ROADMAP.md`, `roadmap.md`, `DEFERRED.md`,
     `WORKAROUNDS.md`, `BUFFER.md`, `docs-page.md`, `specs/_template.md`, `rigger`, `Later:`,
     `Owner:`, and `docmap`/`boards`/`deep_subsystems`/`not_docs` read from `config.json`.
   For each step here, say whether you'd recommend it as written for this repo. A step you'd
   change, add or drop goes to the owner with your reason; nothing runs until they answer, and
   their answer is quoted in `## Process check`.
3. **Update, on trunk.** Run `/jig:update` as its skill says, from the plugin's copy, as many
   times as it asks: the first run installs the new checker (commit it on trunk), the next
   converts `.jig/roadmap.md` to `.jig/roadmap.json` once the new checker can judge it. Each
   line the conversion can't carry is the owner's: move it into its phase's note, fix it, or
   delete it. Show every plan, removal and finding to the owner and apply on their yes. Commit
   each run on trunk, and note each commit's sha for the handoff.
4. **Open the job** for the follow-ups the update leaves to the repo: `jig open
   jig-0.17.0-upgrade --spec .jig/specs/jig-0.17.0-upgrade.md --shares <the files step 2's
   grep and the update's Repo files to review named>`. The work role, in its worktree:
   - repoints each stale name in the repo's own files (skills, scripts, docs, `AGENTS.md`), each
     on the owner's yes, as `/jig:update`'s After `--apply` says;
   - brings a glossary update reported out of form into the one form, with the owner;
   - for each spec on trunk whose deleted `Later:` line named ids, checks those ids are on the
     roadmap; for each spec's `## Out of scope` that defers work, proposes a roadmap item;
   - runs `check` and the repo's tests the change touched.
   Then review, `jig reviewed`, and `jig handoff`. The note's Evidence starts with the
   `Rollback:` line, copied from this spec, and lists step 3's trunk commits.
5. **Gate and merge** as every job does, the merge on the owner's word.

## Process check
<filled in by step 2: per step, agree or the change proposed, and the owner's answer in their words>

## Done when
- [ ] The `Rollback:` line is filled in, committed and pushed before step 3's first commit
  (`git log --format=%H -- .jig/specs/jig-0.17.0-upgrade.md` is older than the update's
  commits, and `git branch -r --contains <the rollback sha>` names the remote's trunk).
- [ ] `## Process check` has a line for each step and the owner's answer to any change, before
  `jig open` (the commit adding them predates the board's `open` commit).
- [ ] The plugin's update dry run says "up to date", and `git hash-object .jig/jig.py` matches
  the plugin's copy.
- [ ] `.jig/rules/` holds the rulesets and `.jig/RULES.md` is gone; `.jig/templates/` exists;
  the ledgers are `deferred.md`, `workarounds.md`, `buffer.md` where the repo has them.
- [ ] `.jig/docmap.json` exists, and `.jig/config.json` has no `docmap`, `boards`,
  `deep_subsystems` or `not_docs` key.
- [ ] `.jig/roadmap.json` exists, `.jig/roadmap.md` and a jig-generated `ROADMAP.md` are gone,
  and `jig roadmap show` prints the roadmap. Every phase, scope and No phase item the
  Markdown roadmap held is in it, or the owner's answer for it is in the handoff.
- [ ] No spec on trunk has a `Later:` line, and each id one named is on the roadmap.
- [ ] The glossary is in the one form: the commit hook passes it, it has no `Owner:` lines, and
  `jig glossary "<any term>"` prints the term.
- [ ] `AGENTS.md`'s Commands has the `roadmap:` line.
- [ ] Step 2's grep finds no old name in the repo's own files, or each hit is in the handoff
  with the owner's answer.
- [ ] `.jig/scripts/check.sh` passes, and `jig survey` reports nothing the update was meant to
  fix.
- [ ] The handoff note's Evidence carries the `Rollback:` line and step 3's commits.

## Rollback
Only on the owner's word: reset trunk to the `Rollback:` sha and force-push it, then run
`python3 .jig/jig.py install-hooks` (the old copy reinstalls its own hooks). Remove any
worktree or branch the job left. Nothing else in this spec rolls back on its own.

## Out of scope
- Changing what any rule says, or the repo's own settings (`roles`, `queue`).
- Other repos: each runs its own copy of its kind's spec.

## Touches
- `.jig/` (on trunk, by `/jig:update`), `AGENTS.md`
- the repo's own files step 2's grep names (filled in at `jig open`)

## Alternatives considered
- Running the update inside the job: rejected, because `jig update` refuses while any job is
  open, since it moves files the worktrees rely on [seen: jig.py `cmd_update`].
- Recording the rollback point only in the handoff: rejected, because a run that fails before
  the handoff would leave no record of where to go back to [seen: the owner's words above].

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
