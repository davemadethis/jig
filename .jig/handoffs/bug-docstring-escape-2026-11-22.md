# Handoff: bug-docstring-escape

Commit: 26f9ef952fc7240d98f8c8d8941269a608513108
Date: 2026-11-22
Spec: .jig/specs/bug-docstring-escape.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high

## Built
<!-- what this delivers, in a few lines -->
`link_spans`' docstring in `plugin/templates/jig/jig.py` opens `r"""`, so Python 3.12+ no longer prints a SyntaxWarning for `\[` on every jig command and hook call. `.jig/scripts/check.sh` now compiles jig.py and `scripts/roles_svg.py` with `-W error`, so a compile warning fails the check on every stop.

## Done-when evidence
<!-- one line per spec item: the command run and what it printed -->
- Guard fires: check.sh line changed, old docstring, `python3 .jig/jig.py queue -- bash .jig/scripts/check.sh` -> `File "plugin/templates/jig/jig.py", line 2946` / `SyntaxError: invalid escape sequence \[` / `check: jig.py does not compile`, exit=2 (python3 3.9.6).
- After `r"""`: same command -> exit=0 (3.9.6).
- Symptom gone: `/opt/homebrew/bin/python3.14 -I plugin/templates/jig/jig.py --help 2>&1 | grep -c SyntaxWarning` -> `0`; with `python3.12` -> `0`.
- Full smoke: not run here; the spec leaves it to the check role at the gate. No smoke section reads this repo's check.sh compile line (its check.sh hits are throwaway repos' copies).

## Review
<!-- findings from the adversarial review, and what you did about each -->
review-work of cd5ab77 (tier 2, effort 2, recorded by the hubnode): blocking 0. The reviewer reproduced the guard firing and passing on 3.9.6, 3.12, 3.13 and 3.14, confirmed the raw docstring is identical in the AST, found `-W error` raises nothing else on any of them, and that `scripts/roles_svg.py` is tracked wherever check.sh runs. One optional finding, deferred in `.jig/ledgers/DEFERRED.md`: the fail message still says "jig.py does not compile" when `roles_svg.py` is the file that failed.

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because the change is a docstring prefix: no behavior a page describes moved (its documentation, `plugin/templates/jig/RULES.md`, is untouched and still true).

## Shared files changed
<!-- each shared/common file, and why this job had to touch it -->
- `plugin/templates/jig/jig.py`: the one docstring is the bug.
- `.jig/scripts/check.sh`: its compile line is where the guard belongs (spec, One layer up).

## Test by hand
<!-- what a person should click or watch -->
On Python 3.12 or later, run any jig command from the plugin copy (`python3.12 plugin/templates/jig/jig.py --help`): no SyntaxWarning line. The installed `.jig/jig.py` still warns until the next `/jig:update`.

## Left
<!-- what remains on this job -->
Nothing on this job.
