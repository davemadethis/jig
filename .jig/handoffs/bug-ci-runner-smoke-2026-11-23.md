# Handoff: bug-ci-runner-smoke

Commit: 0629c2766769fa1993f8d42e800798ba0721306d
Date: 2026-11-23
Spec: .jig/specs/bug-ci-runner-smoke.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
The complete check gives the same answer on GitHub's runner as on the Mac. Smoke stops reading the
machine. Before any section starts it writes its own gitconfig in `$RUN`, exports `GIT_CONFIG_GLOBAL`
to it, and sets `GIT_CONFIG_NOSYSTEM=1` and `PYTHONDONTWRITEBYTECODE=1`. check.sh compiles with
`compile()` under `-W error` instead of `py_compile`, and exports `PYTHONDONTWRITEBYTECODE=1` for
`roles_svg.py`'s import of jig.py. A new pararepo case pins `jig propose` with no identity: git's own
message, nothing written. The `checked --trace` bisect case prints what ran when it fails, and it reads
git 2.56's quoted verdict ("the first 'bad' commit"), the fourth cause. No jig.py change.

## Done-when evidence
- bug-docstring-escape merged: on trunk at bf69b81, already in this branch's base b1ff946; check.sh keeps its `-W error`.
- Identity: `jig queue -- env GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.useConfigOnly GIT_CONFIG_VALUE_0=true bash tests/smoke.sh pararepo` → rc=0, 94 PASS, 0 FAIL (at eddd94b).
- No bytecode: `jig queue -- env -u PYTHONDONTWRITEBYTECODE PATH=<py3.14 shim>:$PATH bash .jig/scripts/check.sh` → rc=0, then `find plugin -name __pycache__` printed nothing (at eddd94b; compile() alone still left one, through roles_svg.py, hence the export).
- Runner's conditions stacked: `jig queue -- env -u PYTHONDONTWRITEBYTECODE PATH=<py3.14 shim>:$PATH GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.useConfigOnly GIT_CONFIG_VALUE_0=true bash .jig/scripts/check.sh --full` → rc=0, 1876 PASS, 0 FAIL (at eddd94b).
- No-identity propose case: "PASS  propose: with no git identity in the metarepo checkout, git's own message stops it before the spec or a branch is written" (exit non-zero, "Author identity unknown", spec unchanged, no new propose/ branch).
- checked --trace prints on failure: run 45214696987 of eddd94b printed "bisect commands:" / "bisect output:", which named the cause (1 FAIL, down from 25). After the fix, `jig queue -- bash tests/smoke.sh check_levels` → rc=0, 49 PASS (at b741c47).
- Symptom gone: https://github.com/davemadethis/jig/actions/runs/45217530959 of b741c47, conclusion success, 0 FAIL. `jig checked --ci <that url> --tier 3 --effort 4 --seconds 905` printed "checked b741c4778ba8: tier 3, effort 4, 905s, on CI: https://github.com/davemadethis/jig/actions/runs/45217530959".

## Review
- review-work of eddd94b: 0 blocking, 0 should-fix, 4 optional, each deferred with a row in `.jig/ledgers/DEFERRED.md`:
  `--unit` run by hand isn't isolated; outer `GIT_AUTHOR_*`/`GIT_COMMITTER_*` beat smoke's gitconfig;
  `GIT_CONFIG_NOSYSTEM` drops a system `safe.directory`; check.sh's `read_text()` vs bytes.
- review-change of b741c47: 0 blocking. Two optional notes, not acted on, and the spec isn't amended: the spec's
  Whys still tags the `--trace` cause `[assumed]`, which the new Decisions bullet settles (git 2.56's quoted
  'bad', seen in run 45214696987); and the Touches line for `tests/smoke.sh` doesn't mention the verdict parse.

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
- [x] no code changed — nothing to fold in: only `tests/smoke.sh` and `.jig/scripts/check.sh` changed, which no page covers

## Shared files changed
- `tests/smoke.sh` (shares): the hermetic setup, the no-identity case, the bisect case's output and verdict parse.
- `.jig/scripts/check.sh` (shares): the compile line and the bytecode export.
- `.jig/specs/bug-ci-runner-smoke.md` (common): a Decisions bullet naming the `--trace` cause.
- `.jig/ledgers/DEFERRED.md` (append): four rows for review-work's optional findings.

## Test by hand
Nothing to click. The next `jig queue --full` that overflows to GitHub should come back green.

## Left
Nothing. Every Done-when item is met. The installed `.jig/jig.py` is unchanged. This job changed `.jig/scripts/check.sh`, which is this repo's own file.
