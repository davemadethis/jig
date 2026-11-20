# bug-pararepo-sync-fixes: an empty proposal branch shows, and a metarepo roadmap cite is read live

Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): "Two of Maige-Lite's proposal branches in maige-ecosystem have no commit of their own … `git branch --no-merged main`, which the metarepo hubnode's proposal listing uses (hubnode skill, step 5), hides both." B3's proposal "sat unseen for two days."
Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-19 / Dave, on his word: "have eco combine those, sort out the final solutions, and file the jig feedback" (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): `jig sync` reports a cite of the metarepo's `.jig/roadmap.md` as a file the release "doesn't have" — "cites maige-ecosystem/.jig/roadmap.md, which maige-ecosystem v3.1.0 doesn't have", at `.jig/ledgers/DEFERRED.md:229`, `.jig/specs/buffer-b1-b4.md:15` and `:16`.

Kept separate from cross-repo-roadmap: the owner, 2026-11-20: "Hold on the cross-repo roadmap until we discuss it."

## Intent

Two pararepo-sync fixes in one job. A metarepo proposal branch has a commit of its own from the
moment `jig propose` (or `jig release`) opens it, so the metarepo's `--no-merged` listing shows
it, and `jig sync` names a proposal with nothing written on it as empty, with the date it was
proposed. A pararepo's cite of its metarepo's roadmap (`<meta>/.jig/roadmap.md`, `<meta>/ROADMAP.md`)
is checked against the roadmap on the metarepo's trunk, read live, not the pin cache; a buffer
proposal spec's copies of BUFFER rows are history and aren't checked.

The investigations (Why, Givens, One layer up, Correction, General?) are in the two inputs as
they stood at 5418108: `.jig/specs/bug-empty-proposal.md` and
`.jig/specs/bug-metarepo-roadmap-cites.md`.

## Change

From bug-empty-proposal:
1. `open_proposal`: make the branch at an opening commit on top of the metarepo's trunk (`git commit-tree <trunk>^{tree} -p <trunk> -m <subject>`, then `git branch <branch> <commit>`). Callers and messages unchanged.
2. A helper `proposal_empty(loc, branch, trunk)`: the branch exists and its tip is the opening commit (subject starts `propose: ` and ends `nothing written yet`) or sits on trunk's first-parent line (branches made before this fix). `proposal_in` returns False for an empty branch, replacing its inline `on_trunk` test.
3. `sync_meta`: for a cited, unreleased proposal that `proposal_empty` says is empty, print `proposal <branch> (<spec>): empty: nothing written on it in <meta> since <date>; write the change there (git -C <loc> worktree add <dir> <branch>), or <withdraw_line>`, in place of `not released`. `<date>` is the date of the pararepo commit that added the spec (`git log --diff-filter=A -1 --format=%cs -- <spec>`), or `uncommitted`. The "carries no Open row" clause still applies.
4. Hubnode skill step 5, pararepo half: a proposal sync names as empty goes to the owner too: write it (a job in the metarepo, or by hand there) or withdraw it on a yes. Metarepo half: one clause: an Open row whose pararepo spec cites a branch the `--no-merged` listing doesn't show is named with that branch, "nothing unmerged here: empty, or merged and awaiting a release". That catches the two branches made before the fix.
5. RULES.md, The sync buffer: one sentence: `jig propose` opens its branch with a commit of its own, so the metarepo's list of unmerged branches shows it from the start; sync names a proposal with nothing written past that as empty, with the date it was proposed.
6. `tests/smoke.sh`, pararepo section: the Done when lines below.

From bug-metarepo-roadmap-cites:
1. **The roadmap is read live.** In `meta_citations`, both modes: a cite of `ROADMAP`
   (`.jig/roadmap.md`) or `ROADMAP_VIEW` (`ROADMAP.md`) reads `git show <trunk>:<path>` in the
   metarepo checkout (`loc`; `<trunk>` is `Board.trunk_name(loc)`). That is not the cache and not
   the tag. Its message names `<meta> <trunk>`, not the pin ("which maige-ecosystem main has no
   heading for"), so a reader knows a pin bump won't change it. It still checks the heading, so a
   missing one is reported. The release gets this for free: both tags read the same trunk, so a
   roadmap cite never selects a pin-bump request.
2. **A buffer proposal's copies are history.** In a file under `.jig/specs/`, a table row whose
   first cell is an id the spec lists under `## Buffer rows` is left out, as a Closed BUFFER row
   is. One predicate beside `closed_row`, which can reuse `listed_rows`.
3. **The cache is unchanged.** The roadmap stays out of `fill_cache`, `pointers()` and P2: it is
   project data, not a contract, and P2's answers (a BUFFER row, a proposal) don't fit it.
4. RULES.md, **Citing the metarepo** (RULES.md:1482–1487): a cite of the metarepo's roadmap is read
   on its trunk, not at the pin; a buffer proposal's copied rows are left out with handoffs and
   Closed BUFFER rows.

## Done when

From bug-empty-proposal (in smoke's pararepo section, throwaway `mr`/`pr`, `JIG_CONFIG` set):
- [ ] (fix fires) After `jig propose --buffer` with nothing written on the branch, `git -C mr branch --no-merged main --list 'propose/pr-*'` lists it, and its tip's subject says nothing is written yet. `mr`'s main and its checked-out branch are unchanged.
- [ ] (fix fires) `pr`'s `jig sync` prints `proposal propose/pr-… (.jig/specs/….md): empty: nothing written on it in docs since <date>`, naming the worktree command and the withdraw line, and not `not released`.
- [ ] A branch made the old way (`git -C mr branch propose/pr-old main`, cited by a spec in `pr`) also reads as empty in sync.
- [ ] With a commit written on top of the opening commit, sync says `not released` as today; merged and released, sync says `released by …` and closes its rows as today; an empty branch merged into `mr` and released does not close its rows.
- [ ] `jig release` in `pr` with an Open row makes its `buffer-<tag>` branch with the opening commit (the existing release check still passes, and the branch is listed by `--no-merged`).
- [ ] (symptom gone) A fixture with the report's shape: `mr` has `propose/pr-buffer-b3` at main's tip, `pr` cites it with row B3 Open. `pr`'s `jig sync` names it as empty with the spec's date; a new `jig propose --buffer` there makes a branch `--no-merged` lists. In Maige-Lite itself, the owner's next `jig sync` on its trunk names `propose/Maige-Lite-buffer-b3` as empty (not run here: that repo is read-only to this role).
- Its last item, "`check` and the pararepo smoke section pass", is dropped: the last item below states it.

From bug-metarepo-roadmap-cites (all in `tests/smoke.sh`, with `JIG_CONFIG`/`XDG_CONFIG_HOME` set as the sections already do):
- [ ] (fix fires) `pararepo`: a `para` spec line citing `` `meta/.jig/roadmap.md § Up next` `` (the
  heading exists) prints no cite line from `jig sync`. One citing `§ Nowhere` prints
  `cites docs/.jig/roadmap.md § Nowhere, which docs main has no heading for` (the section's
  metarepo is `docs`), not "doesn't have".
- [ ] (live) A `## Nowhere` committed on the metarepo's trunk, with no release: the same cite then
  prints nothing.
- [ ] (no regression) A cite of a metarepo page that is truly absent at the pin still prints
  "doesn't have" with the pin (the existing case at smoke.sh:1637 still passes).
- [ ] (release) `pin_bump`: a roadmap heading a pararepo spec cites, removed between two metarepo
  releases, stages no pin-bump request for that cite.
- [ ] (copies) `sync_buffer`: a buffer proposal spec whose `## Buffer rows` lists B1, with B1's
  copied row citing a metarepo page the pin lacks, prints nothing for the spec's line. The same cite
  on BUFFER.md's Open B1 row still prints "doesn't have".
- [ ] (DEFERRED stays checked) A DEFERRED.md row citing a metarepo page the pin lacks still
  prints "doesn't have".
- [ ] (symptom gone) On Maige-OS's trunk after `/jig:update` to the fixed jig, `python3 .jig/jig.py
  sync` prints none of the lines for `DEFERRED.md:229`, `buffer-b1-b4.md:15`, `:16`. That is the
  owner's check in Maige-OS; jig's sessions don't run it there (read-only).
- [ ] `check` and the `pararepo`, `pin_bump` and `sync_buffer` smoke sections pass.

## Out of scope

From bug-empty-proposal:
- maige-ecosystem's `docs/features/identity/unlock.md` contradiction (B3's content): maige-ecosystem's to fix once B3 is written.
- Deleting the two existing empty branches in maige-ecosystem: the metarepo's owner's, as RULES.md says for any proposal branch.
- A metarepo-side report that ages every `propose/` branch: Issue 1's report (another group).

From bug-metarepo-roadmap-cites:
- A process for moving an item between a page, a spec and a scope. None of the three lines was a
  move (Maige-OS's finding, re-checked above). A separate request if the owner wants one.
- Issue 1 (one roadmap across repos). How this fits it: Issue 1 reads the metarepo's roadmap on
  its trunk through `jig repos`, the same read as Change 1, so whichever lands second reuses the
  other's helper. Once pararepos have no roadmap of their own, every roadmap cite is a
  `<meta>/.jig/roadmap.md` one and this check covers its headings. Issue 1's scope ids are
  checked by Issue 1's own rules, not here.
- NO_FILE dropping the section from its message, so two cites of one missing file on one line
  collapse into one. Cosmetic, and with the roadmap read live it no longer hides anything here.
- Fetching the metarepo's trunk before the read. Sync fetches tags only; the registered checkout's
  trunk is what the owner works on (for a metarepo, its own checkout).

## Touches
- `plugin/templates/jig/jig.py` (`open_proposal`, `proposal_in`, new `proposal_empty`, `sync_meta`; `meta_citations` (both `meta_text`s, the NO_FILE/NO_HEADING message for a roadmap cite, the per-line skip), a predicate beside `closed_row`)
- `plugin/skills/hubnode/SKILL.md` (step 5)
- `plugin/templates/jig/RULES.md` (Metarepo and pararepos: The sync buffer, **Citing the metarepo**)
- `tests/smoke.sh` (`pararepo`, `pin_bump`, `sync_buffer`)

## Alternatives considered

From bug-empty-proposal:
- `jig propose` refuses to make a branch with no commit of its own (the report's) — rejected because propose can't write the change: it is free text written after, so every new branch starts empty; the opening commit is the version of this that can be done — [seen] (`open_proposal`, `cmd_propose` print "Write the change there" after making it).
- The next `jig propose` refuses while an earlier one is empty (the report's, Proposed) — rejected because `jig release` proposes on its own, so a pararepo release would stop on unwritten metarepo work, and it would not have fired for B3, which no later propose followed — [seen] (jig.py:7022–7025; Maige-Lite's last buffer spec is buffer-b3).
- The metarepo's listing reads the pararepos' buffer specs instead of `--no-merged` (the report's) — taken only as the step 5 clause for old branches; as the main fix rejected because new proposals then show without it, and telling empty from merged-unreleased from the specs needs first-parent reasoning in skill text — [seen] (prototype: `--no-merged` lists a branch with an opening commit).
- List `propose/` branches with `--merged` too — rejected because every merged proposal would show: 12 of maige-ecosystem's 14 are real and merged — [seen].
- Only change sync's line, no opening commit — rejected because the metarepo stays blind to new empty proposals, which is the report's symptom — [seen] (repro: `--no-merged` empty).

From bug-metarepo-roadmap-cites:
- Cache the roadmap at the pin (`fill_cache`) and check it there (Maige-OS's recommendation 3 as
  written) — rejected because R6 settled a live read ("reading it live is smart regardless, read
  it live, settled"), the pin's roadmap lags trunk (a roadmap change alone can't be released), and
  `pointers()` reads every cached `*.md`, so P2 would ask BUFFER rows for project data — [seen]
- Skip roadmap cites entirely (Maige-OS's recommendation 1) — rejected because a cite to a heading
  that's gone should be reported, and Issue 1 makes such cites deliberate — [seen]
- Add `.jig/roadmap.md` to `entry_files` — rejected because `is_entry` drops every `.jig/` path but
  the decision log, and that would make the roadmap a contract — [seen]
- Leave DEFERRED rows out as history (the report's change 3, first half) — rejected because retro
  re-ranks and takes deferred rows, so their cites are live work, and the live read already clears
  the one Maige-OS saw — [seen]
- Leave out only a copy whose BUFFER row is Closed (the report's change 3 as written) — rejected
  because it needs a lookup into BUFFER.md for no gain: an Open copy only repeats the Open
  BUFFER row's notice, and a row edited after proposing is still its old form in the copy — [seen]
- Exempt all of `.jig/specs/` — rejected because a live spec's cite should be checked — [seen]
  (this repro's `t.md` is such a spec)
- Leave the release reading the roadmap at its tags — rejected because it would ask a pararepo to
  bump its pin over a cite the bump can't change — [seen] (direct call above)

## Decisions

From bug-empty-proposal:
- Correction at the source (an opening commit), plus sync naming empties; no refusal in `jig propose`. Proposed (bug role, 2026-11-20).

From bug-metarepo-roadmap-cites:
- The roadmap cite's message names the metarepo's trunk, not the pin, because the reader's next
  move differs: fix the cite or ask the metarepo, never bump.
- `ROADMAP.md` (the generated view) is read live too: it's derived from the roadmap on the same
  trunk, and it isn't cached either.

Consolidation:
- One job, not two: both change `jig.py`, `RULES.md` and `tests/smoke.sh` (the `pararepo` section in both), and both are pararepo-sync fixes. The owner, 2026-11-20: "Start everything else: … the other two bug specs".

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
