# hubnode-guardrails: a job can't run away from the owner, burn the suite or lose work

Source: Dave (owner), 2026-11-25, in jig's hubnode session, after layout-and-formats part 2 took eleven review rounds and seven strikes in a day without him: "Seven failures without talking to me is unacceptable, jig has a 3 strike rule". Then: "Instead of canning your work and making memories so you dont make the mistake again, what would be more useful is making sure this can't happen again in any hubnode … figure out why jig allowed you to go off the rails and waste so much time and effort." The hubnode's analysis named six causes. The owner took five ("1. yes 2. yes 3. yes 4. drop 5. yes 6. yes") and amended two of them, as quoted under Decisions.

## Intent
A job's blocking rounds return to the owner instead of looping, a build never runs the complete
suite, a review gets only its standard inputs, a fix round takes few optionals, and no agent can
rewind trunk or a job's branch, or wipe uncommitted work, without the owner's approval.

## Why (from the analysis)
1. Once a part's bug spec is committed, `jig reviewed` lifts the strike limit for that part with
   no end. Strikes 4 to 7 went straight back to the work session. Nothing returned to the owner.
2. "The full suite is the check role's, once per gate or batch" is text only. The hubnode's briefs
   asked for full runs before every review, and the work session complied.
3. `/jig:review` says to give the reviewer the diff, the spec and AGENTS.md, and nothing else. The
   hubnode wrote its own briefs, adding "look hard at…" and "try to get past it…". Those steered
   reviewers into edge hunts and their own suite runs.
4. A fix round may take any number of optionals at the hubnode's pick. Nearly every round took
   several, which added commits and reviews.
5. A review subagent's failed `cd` ran `git reset --hard HEAD~2` in the owner's trunk checkout. No
   hook covers a branch moved backwards, and nothing covers uncommitted work.

## Done when
1. **Under a bug spec, a review's findings go to the owner.**
   - [ ] Before a part's bug spec, a review's blocking and should-fix findings go to the work
     session as fixes, with no owner step, as today.
   - [ ] `jig reviewed` records a review with findings under a part's bug spec and prints that the next
     step is the owner's, with three options: fix, rescope, or another bug investigation. It no
     longer prints "the work session fixes them" (smoke).
   - [ ] `jig next <job>` names the owner, not the work role, until the owner's answer is on the
     job's branch (smoke).
   - [ ] The owner's answer is a line in the bug spec, `Strike <N>: <the owner's words>`,
     committed on the job's branch. Until it is there, the next `jig reviewed` of that part is
     refused, naming the line to add (smoke).
   - [ ] Strikes 1 to 3 before a bug spec work as today (smoke: `sec_next`'s strike cases pass
     unchanged).
2. **A build never runs the complete suite.**
   - [ ] `jig queue --full` is refused outside a gate checkout (`gate-<job>`) or a detached check
     worktree (`check-<name>`), naming the check role (smoke).
   - [ ] In this repo, `tests/smoke.sh` run with no section names is refused unless `check.sh
     --full` started it, which sets a variable naming the complete check. `smoke.sh <section>…`
     works as today (smoke).
   - [ ] The work, review and hubnode skills say a check or smoke section already run once for the
     change in hand is run again only on the owner's OK, asked through the hubnode with what would
     rerun and why. A failure is reported, not rerun.
   - [ ] The hubnode skill says a brief never asks a work session or reviewer for the complete
     suite. The work skill says to run `check` and the sections the change touches, and to refuse
     a request for more.
3. **A review gets its standard brief, from jig.**
   - [ ] `jig brief review <job>` prints the brief:
     - which review it is (review-work or review-change, from `jig next`);
     - the range, `git diff <base>..<head>`, from the review record and the last handoff;
     - the spec and its `Bug-for:` specs;
     - `AGENTS.md`;
     - the job's worktree, read-only;
     - the safety lines: git only as `git -C <own path>`, and no stash, reset, checkout or merge
       outside a throwaway repo;
     - the throwaway-repo variables;
     - the report's format.
     It prints nothing else (smoke).
   - [ ] The hubnode and review skills say the hubnode sends that brief as printed, adding only the
     `running <model> at <effort>` line from the tiers map. A review's job is to judge the diff
     against the spec with the builder's evidence. It runs the suite only when a finding needs a
     section to show it.
4. **A fix round takes no more optionals than should-fixes.**
   - [ ] The review and hubnode skills say that in the one should-fix round after a review, the
     hubnode takes no more optionals than should-fixes, and none when it takes no should-fix.
     Every finding not taken gets a `DEFERRED.md` row at handoff.
   - [ ] Each round in a handoff note's `## Review` carries a line `taken: <N> should-fix, <M>
     optional; deferred: <K>`. The commit hook refuses a note in which any round has M greater
     than N, naming the round (smoke).
5. **No branch moves backwards, and no work is wiped, without the owner.**
   - [ ] `jig init` and `jig update --apply` install a `reference-transaction` hook. It refuses any
     update of the trunk branch or a job's branch that isn't a fast-forward: a reset, a rewind, an
     amend or a forced update. It names the branch and says it is the owner's call. Two moves pass:
     `jig merge`'s deletion of a merged job's branch, and the gate's detached checkouts (smoke,
     with reset, amend, `branch -f`, and a fast-forward that passes).
   - [ ] The init and update skills show the owner the Claude Code permission rules that make
     these ask first: `git reset --hard`, `git checkout -- `, `git restore`, `git clean`, `git
     branch -D`, `git push --force` and `git stash` without `-m`. The owner adds them to the
     settings, since Claude Code's settings are the owner's to edit; jig writes none of them.
   - [ ] RULES (Hooks) names the hook and why, with no Claude-specific text.
6. **Every part.**
   - [ ] RULES (Workflow: strikes, Gate, Hooks), the hubnode, review, work, init and update skills,
     and `docs/workflows.md`, `docs/hooks.md` and `docs/commands.md` describe 1 to 5. Nothing
     describes the old unlimited rounds under a bug spec.
   - [ ] `.jig/decisions.md` Unreleased has Added and Changed lines for 1 to 5, with a Breaking line
     for the refused `--full` and the ref hook.
   - [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` and the touched smoke sections pass.
     The complete suite runs at the gate only.

## Out of scope
- Weighing a review finding by how often the reviewed code runs. Dropped by the owner: "I dont
  trust the model to know how often something will run … I dont want you making those judgements
  in other repos." Items 1 and 3 bring a runaway to the owner anyway.
- Protecting uncommitted work from tools other than an agent's shell, such as an editor. The
  permission rules cover the agent, and the ref hook covers branches from any tool.

## Touches
- `plugin/templates/jig/jig.py`: `cmd_reviewed` and the strike logic (`blocking_reviews`,
  `bug_spec_for`, around `STRIKES`), `chain_step`/`cmd_next`, `cmd_queue`, a new `cmd_brief`, the
  note checks (`foldin_lines`/the note hook), `install_hooks` and a new `reference-transaction`
  hook, and `cmd_merge`'s branch deletion
- `plugin/templates/jig/RULES.md` (Workflow, Gate, Hooks)
- `plugin/templates/handoff` note template (the Review round line)
- `plugin/skills/hubnode/SKILL.md`, `review/SKILL.md`, `work/SKILL.md`, `init/SKILL.md`,
  `update/SKILL.md`
- `.jig/scripts/check.sh`, `tests/smoke.sh`
- `docs/workflows.md`, `docs/hooks.md`, `docs/commands.md`
- `.jig/decisions.md`

## Alternatives considered
- A second bug investigation at every third strike past the first. Rejected: the owner wants the
  decision, which may be rescoping rather than investigating. [seen: the owner's words above]
- Enforcing the optional cap in `jig reviewed` rather than in the note. Rejected: which findings
  are taken is known only when the fix lands, and the note is where the round is recorded.
  [assumed]
- Approval through an environment variable or a jig command the hook reads. Rejected: an agent can
  set either itself. Only the host's permission prompt is an approval only the owner can give.
  [assumed]

## Decisions
- The owner, 2026-11-25, on strikes (item 1): "Now we're talking - that is solving the problem."
- The owner, 2026-11-25, setting the whole rule (items 1 and 4): "I dont need to review blocking, blocking get fixed as do should-fix, and you can take from zero up to as many optionals as there are should-fix. After a 3rd strike the bug starts. After that, review findings with me." So before a part's bug spec, every blocking and should-fix finding goes to the work session as a fix, with no owner step; after the bug spec, every review's findings, blocking or not, go to the owner before any fix.
- The owner, 2026-11-25, on reruns (item 2): "dont run any checks or smokes twice without stopping to review if its necessary with me".
- Interpreted: the Stop hook's automatic `check.sh` after each turn isn't an agent's run and stays as it is; the rule covers runs an agent or the hubnode starts.
- The owner, on the optional cap (item 5): "overcorrecting. one round of should-fix with the
  hubnode stays. what we need to cut back on are subsequent rounds without intervention … and the
  hubnodes freedom to take tons of optionals … my idea is no more optionals than there are
  should-fix."
- The owner, on resets (item 6): "yea, reset should require my approval. You could erase more than
  an afternoon, that shouldn't be possible."
- The owner, on frequency-weighted review (dropped): "I wouldn't take this one … All the others
  combined woud've brought it to my attention anyway."
- The owner, 2026-11-25: "Build these as one spec, then save it for later." This spec waits. It
  touches the files layout-and-formats is rewriting (part 5 splits RULES.md and sweeps every
  skill), so it opens after that job merges.
- Interpreted: the owner's answer under item 1 is a line in the bug spec, reusing the spec's
  record rather than adding a ledger.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
