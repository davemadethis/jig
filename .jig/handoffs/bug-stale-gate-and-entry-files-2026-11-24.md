# Handoff: bug-stale-gate-and-entry-files

Commit: 9a47849181363dd16ea12a746fba1efc9b23e9fc
Date: 2026-11-24
Spec: .jig/specs/bug-stale-gate-and-entry-files.md
Source: jig hubnode session / 2026-11-24 / Dave, with Claude ("open a bug spec for it after these jobs merge") (staged as feedback-jig-2026-11-24-next-stale-gate.md): `jig next` names the check in a stale gate checkout after a new handoff
Source: jig hubnode session / 2026-11-24 / Dave, with Claude ("Stage it") (staged as feedback-jig-2026-11-24-merge-log-entry-files.md): `--merge-log` removes a record folder's index but `meta.json` keeps naming it
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Both halves of the spec, whole.
- Stale gate: `gate_holds` says whether the gate checkout holds the commit the job's newest
  note names (HEAD, or the first parent of the merge `jig gate` made). `jig next` says gate for
  a stale checkout, before the check log. `jig checked` in a stale gate checkout and `jig mark
  <job> gated` refuse it, naming `jig gate <job>`. `jig handoff` refuses while the job is gated
  on trunk's committed board or in the trunk checkout's jobs.json (an uncommitted mark), and
  refuses in one line when that jobs.json doesn't parse.
- `this_repo_names` reads the name from the trunk checkout's config alone, so a broken
  jobs.json there no longer crashes a solo handoff (on trunk it did).
- `--merge-log`: `kept_entry` drops every path the run removes (registers, a changelog, records,
  an emptied index), and META is rewritten when files merge or `entry_files` names a removal.
  A glob or a kept index stays; a folder-only run naming nothing removed leaves META byte for byte.
- Words: RULES.md Workflow steps 1 and 2 and the `jig checked` paragraph, the hubnode skill's
  Gating step 5, two `### Fixed` lines in decisions.md.

## Done-when evidence
Commands:
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh` → rc=0 each round, last at 9a47849 (it runs `claude plugin validate ./plugin`).
- `python3 .jig/jig.py queue -- bash tests/smoke.sh next merge_log metarepo` at 81820e6 → 207 PASS, 0 FAIL;
  `next merge_log` at dedd53a → 112 PASS, 0 FAIL; `next` at 9a47849 → 54 PASS, 0 FAIL.
- `grep -rnE 'Maige|maige|Daisy|daisy|"E-' plugin` → nothing.
Per item, the smoke line that proves it:
- next, the report's case → PASS  next: a gate checkout built from an older note is the gate again, naming both commits
- checked in the stale checkout → PASS  checked: in a stale gate checkout, refused, naming the note's commit and jig gate; nothing recorded
- check recorded before the new handoff → PASS  next: a check recorded before the new handoff doesn't make it mark gated: gate;
  PASS  mark gated: a stale checkout is refused, naming jig gate; the checkout and the board stay
- the fix end to end → PASS  gate: run again, the checkout holds the new note's commit, and next says check;
  PASS  mark gated and merge: the rebuilt checkout's check gates the job, and it merges
- Repro B → PASS  handoff: refused while trunk's board has the job gated, naming jig mark ready;
  PASS  handoff: marked back, the handoff goes through, and next says gate
- review A, B and the should-fixes → PASS  handoff: refused while the trunk checkout has the job marked gated, before the hubnode commits it;
  PASS  next and checked: a commit added on top in the gate checkout is stale, not the note's;
  PASS  handoff: a trunk checkout jobs.json that doesn't parse refuses the handoff in one line, no traceback, no note
- existing sec_next cases → all PASS in each run above.
- merge-log case reg → PASS  merge-log entry_files: a register and a removed index both leave entry_files, the log alone left; the commit and rules pass
- case folder → PASS  merge-log entry_files: a folder-only run drops the removed index, prints it in the dry run, stages META, and the commit passes
- kept index and glob → PASS  merge-log entry_files: a kept index and a glob stay as written; a removed record goes
- names nothing removed → PASS  merge-log entry_files: a folder-only run whose entry_files names nothing removed leaves META unstaged, byte for byte
- existing merge_log and metarepo cases → all PASS at 81820e6 (207/0); merge_log again at dedd53a.
- The full smoke is the check role's, at the gate.

## Review
- review-work of 81820e6: 0 blocking. Taken: A (a note filed between `jig mark gated` and the
  hubnode's commit of jobs.json), fixed by `jig handoff` also reading the trunk checkout's
  jobs.json; the asked re-check before `board.save()` couldn't close that window, and the
  hubnode agreed. B (`gate_holds` took HEAD^1 of a non-merge): HEAD^1 only when HEAD^2 exists.
  C: the spec's ancestor alternative reasoned from `cmd_gate`/`merge_trunk`, tagged [seen].
  Each has a smoke case (dedd53a).
- review-change of dedd53a: 0 blocking. Should-fix taken: a broken trunk-checkout jobs.json
  crashed the handoff. `cmd_handoff` reads only `main_root() / JOBS` (47eeef9); the smoke case
  exposed the same crash in `this_repo_names`, fixed there on the hubnode's word (f06972a).
- review-change of f06972a: 0 blocking. Should-fix taken: falling back to trunk's committed
  board on a broken jobs.json reopened A, so the handoff refuses in one line (9a47849).
  Optional taken: Touches names `this_repo_names`. Optional deferred: its folder-name fallback.
- review-change of 9a47849: 0 blocking. Two optionals deferred: the `this_repo_names`
  comment's reason, and the refusal's "doesn't parse" wording.
- Each deferred optional has a row in .jig/ledgers/DEFERRED.md.

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
- [x] docs/commands.md — no change because its one-line entries for gate, mark, checked and next still hold; it names no refusal   (2 files)
- [x] docs/hooks.md — no change because no hook changed, and it describes none of these commands   (1 file)
- [x] docs/jobs.md — no change because every sentence in its Handoff and Gate sections still holds; the new refusals are detail RULES.md and the hubnode skill carry   (2 files)
- [x] docs/metarepos.md — no change because it names neither `--merge-log` nor how a run changes `entry_files`   (2 files)
- [x] docs/records.md — no change because it describes no merge-log rewrite of `entry_files`   (2 files)
- [x] docs/workflows.md — no change because ROLES and FLOWS are unchanged: no step, role or flow added   (3 files)

## Shared files changed
- plugin/templates/jig/jig.py: `gate_holds` and `gate_job` (new), `chain_step`, `cmd_checked`, `cmd_mark`'s gated branch, `cmd_handoff`, `this_repo_names`, `cmd_merge_log` (`kept_entry`, `entry_changes`). Nothing else: moving-in-command shares the file.
- plugin/templates/jig/RULES.md: Workflow steps 1 and 2, the `jig checked` paragraph.
- plugin/skills/hubnode/SKILL.md: Gating step 5.
- tests/smoke.sh: new cases inside `sec_next` (jobs ks, kt) and `sec_merge_log` (`mlentry`), at each section's end.
- .jig/decisions.md: two lines under a new `### Fixed` in `## Unreleased`.

## Test by hand
Gate a job, then have it hand off again before marking it gated: `jig next <job>` says gate,
naming both commits, and `jig checked` in the old checkout refuses. Mark a job gated, then try
`jig handoff` in its worktree: it names `jig mark <job> ready`.

## Left
Nothing of the spec. Three optionals are deferred in .jig/ledgers/DEFERRED.md.
