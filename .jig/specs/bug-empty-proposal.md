# bug-empty-proposal: a proposal branch with no commit of its own is invisible to the metarepo

Source: maige-ecosystem hubnode session, 2026-11-19 (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): "Two of Maige-Lite's proposal branches in maige-ecosystem have no commit of their own … `git branch --no-merged main`, which the metarepo hubnode's proposal listing uses (hubnode skill, step 5), hides both." B3's proposal "sat unseen for two days."

## 1. Why
- Q: Why didn't the metarepo see B3's proposal? A: Its listing is `git branch --no-merged <trunk>`; a branch with no commit of its own counts as merged, so it never shows.
- Q: Why has the branch no commit? A: `open_proposal` makes it at the metarepo's trunk tip; the change is written later, by hand, and `jig release` proposes on its own, with nobody told to write.
- Q: Why does nothing say so later? A: `proposal_in` knows the shape (tip on trunk's first-parent line) only to answer "not released"; `jig sync` prints just that. Root.

## 2. Givens
- [seen] Reproduced in throwaway `mr`/`pr` (scratch, `JIG_CONFIG`/`XDG_CONFIG_HOME` set): after `jig propose --buffer b1`, `git -C mr branch --no-merged main --list 'propose/pr-*'` prints nothing; `git branch -v` shows `propose/pr-b1` at `release v0.1.0`, trunk's tip.
- [seen] Same repro: `pr`'s `jig sync` prints `proposal propose/pr-b1 (.jig/specs/b1.md): not released`, nothing more; a second `jig propose --buffer b2` goes through without a word about b1.
- [seen] maige-ecosystem (read-only): of 14 `propose/` branches, `propose/Maige-Lite-buffer-b3` (4135dcb) and `propose/Maige-Lite-buffer-v0.0.1` (5cb91e3) have tips on main's first-parent line; `git branch --no-merged main --list 'propose/*'` lists none of the 14.
- [seen] Maige-Lite main: `.jig/specs/buffer-b3.md:13` is `- meta: maige-ecosystem proposal propose/Maige-Lite-buffer-b3`, committed c4de9ee 2026-11-17; BUFFER row B3 is `Open`.
- [seen] `jig release` in a pararepo runs `buffer_proposal` before its build (jig.py:7022–7025): a branch named `buffer-<tag>` is made on every release with an unproposed Open row, and the release ends there. `buffer-v0.0.1` is that path; `buffer-b3` is a hand-run `jig propose --buffer`.
- [seen] `proposal_in` (jig.py:8073–8082) treats a tip on trunk's first-parent line as not released, its comment naming this exact state.
- [seen] Hubnode skill step 5 (plugin/skills/hubnode/SKILL.md:43–49): the metarepo half lists `--no-merged` branches beside each pararepo's Open rows; the pararepo half reports sync's lines, and only "carries no Open row" goes to the owner.
- [seen] Prototype in throwaway `mr`: `git branch propose/pr-b3 $(git commit-tree 'main^{tree}' -p main -m '…')` leaves main and the checkout untouched, and `--no-merged` then lists the branch with its date and subject.
- [assumed] A metarepo hubnode won't merge a branch whose only commit says nothing is written yet. Risk if it does: covered by `proposal_in` reading that tip as not released (Change 2).

## 3. One layer up
- Sibling: `jig propose <spec> <slug>` (and `--pointers`) goes through the same `open_proposal`, so it has the same blind spot. The fix sits in `open_proposal` to cover all three callers, release included.
- `proposal_in` already detects the empty shape; `jig sync` already names one proposal state that needs the owner ("carries no Open row: withdraw"). This adds a second state in the same line, to the same person.
- Issue 1's metarepo report (another group) ages `propose/` branches and flags empty ones from the metarepo. This fix doesn't wait for it: the existing listing shows new proposals once they have a commit.

## 4. Correction
Correct the cause, not the listing: a proposal is never made empty. `open_proposal` gives the branch one opening commit of its own (the trunk's tree, no change, subject `propose: <repo>-<slug> opened by <repo>, nothing written yet`), made by `git commit-tree` + `git branch`, so nothing is checked out. From then on, `--no-merged` lists it with its date, in the metarepo's existing step 5 listing. For branches already empty (the two in maige-ecosystem), and for a branch still holding only its opening commit, the pararepo's `jig sync` names it as empty, with the date it was proposed and what to do. The skill's step 5 sends that line to the owner, as it does "carries no Open row" today.

## 5. Spec

## Change
1. `open_proposal`: make the branch at an opening commit on top of the metarepo's trunk (`git commit-tree <trunk>^{tree} -p <trunk> -m <subject>`, then `git branch <branch> <commit>`). Callers and messages unchanged.
2. A helper `proposal_empty(loc, branch, trunk)`: the branch exists and its tip is the opening commit (subject starts `propose: ` and ends `nothing written yet`) or sits on trunk's first-parent line (branches made before this fix). `proposal_in` returns False for an empty branch, replacing its inline `on_trunk` test.
3. `sync_meta`: for a cited, unreleased proposal that `proposal_empty` says is empty, print `proposal <branch> (<spec>): empty: nothing written on it in <meta> since <date>; write the change there (git -C <loc> worktree add <dir> <branch>), or <withdraw_line>`, in place of `not released`. `<date>` is the date of the pararepo commit that added the spec (`git log --diff-filter=A -1 --format=%cs -- <spec>`), or `uncommitted`. The "carries no Open row" clause still applies.
4. Hubnode skill step 5, pararepo half: a proposal sync names as empty goes to the owner too: write it (a job in the metarepo, or by hand there) or withdraw it on a yes. Metarepo half: one clause: an Open row whose pararepo spec cites a branch the `--no-merged` listing doesn't show is named with that branch, "nothing unmerged here: empty, or merged and awaiting a release". That catches the two branches made before the fix.
5. RULES.md, The sync buffer: one sentence: `jig propose` opens its branch with a commit of its own, so the metarepo's list of unmerged branches shows it from the start; sync names a proposal with nothing written past that as empty, with the date it was proposed.
6. `tests/smoke.sh`, pararepo section: the Done when lines below.

## Done when
In smoke's pararepo section (throwaway `mr`/`pr`, `JIG_CONFIG` set):
- [ ] (fix fires) After `jig propose --buffer` with nothing written on the branch, `git -C mr branch --no-merged main --list 'propose/pr-*'` lists it, and its tip's subject says nothing is written yet. `mr`'s main and its checked-out branch are unchanged.
- [ ] (fix fires) `pr`'s `jig sync` prints `proposal propose/pr-… (.jig/specs/….md): empty: nothing written on it in docs since <date>`, naming the worktree command and the withdraw line, and not `not released`.
- [ ] A branch made the old way (`git -C mr branch propose/pr-old main`, cited by a spec in `pr`) also reads as empty in sync.
- [ ] With a commit written on top of the opening commit, sync says `not released` as today; merged and released, sync says `released by …` and closes its rows as today; an empty branch merged into `mr` and released does not close its rows.
- [ ] `jig release` in `pr` with an Open row makes its `buffer-<tag>` branch with the opening commit (the existing release check still passes, and the branch is listed by `--no-merged`).
- [ ] (symptom gone) A fixture with the report's shape: `mr` has `propose/pr-buffer-b3` at main's tip, `pr` cites it with row B3 Open. `pr`'s `jig sync` names it as empty with the spec's date; a new `jig propose --buffer` there makes a branch `--no-merged` lists. In Maige-Lite itself, the owner's next `jig sync` on its trunk names `propose/Maige-Lite-buffer-b3` as empty (not run here: that repo is read-only to this role).
- [ ] `check` and the pararepo smoke section pass.

## Touches
- `plugin/templates/jig/jig.py` (`open_proposal`, `proposal_in`, new `proposal_empty`, `sync_meta`)
- `plugin/skills/hubnode/SKILL.md` (step 5)
- `plugin/templates/jig/RULES.md` (Metarepo and pararepos, The sync buffer)
- `tests/smoke.sh` (pararepo)

## Out of scope
- maige-ecosystem's `docs/features/identity/unlock.md` contradiction (B3's content): maige-ecosystem's to fix once B3 is written.
- Deleting the two existing empty branches in maige-ecosystem: the metarepo's owner's, as RULES.md says for any proposal branch.
- A metarepo-side report that ages every `propose/` branch: Issue 1's report (another group).

## Alternatives considered
- `jig propose` refuses to make a branch with no commit of its own (the report's) — rejected because propose can't write the change: it is free text written after, so every new branch starts empty; the opening commit is the version of this that can be done — [seen] (`open_proposal`, `cmd_propose` print "Write the change there" after making it).
- The next `jig propose` refuses while an earlier one is empty (the report's, Proposed) — rejected because `jig release` proposes on its own, so a pararepo release would stop on unwritten metarepo work, and it would not have fired for B3, which no later propose followed — [seen] (jig.py:7022–7025; Maige-Lite's last buffer spec is buffer-b3).
- The metarepo's listing reads the pararepos' buffer specs instead of `--no-merged` (the report's) — taken only as the step 5 clause for old branches; as the main fix rejected because new proposals then show without it, and telling empty from merged-unreleased from the specs needs first-parent reasoning in skill text — [seen] (prototype: `--no-merged` lists a branch with an opening commit).
- List `propose/` branches with `--merged` too — rejected because every merged proposal would show: 12 of maige-ecosystem's 14 are real and merged — [seen].
- Only change sync's line, no opening commit — rejected because the metarepo stays blind to new empty proposals, which is the report's symptom — [seen] (repro: `--no-merged` empty).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4

## General?
Yes. Any pararepo whose `jig release` proposes Open rows and whose session moves on, or that runs `jig propose` and stops before writing, leaves an invisible branch. The release path makes it the default, not an edge: 2 of maige-ecosystem's 14 proposal branches, both buffer proposals, one from a release.

## Decisions
- Correction at the source (an opening commit), plus sync naming empties; no refusal in `jig propose`. Proposed (bug role, 2026-11-20).
