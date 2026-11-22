Source: claude.ai chat (Squarish Projects), 2026-11-20, Dave with Claude (staged as feedback-jig-2026-11-20-docstring-escape-warning.md): jig.py prints a SyntaxWarning for an invalid escape in a docstring (`jig.py:2933: SyntaxWarning: invalid escape sequence '\['`)

## Whys
- Why the warning? `link_spans`' docstring is a plain `"""` string that quotes a regex with `\[`, `\]`, `\(`, `\)`, `\s`. Python 3.12+ warns at compile.
- Why on every command and hook call? jig.py always runs as a script, and Python never caches a script, so it compiles (and warns) each run.
- Why did no check catch it? check.sh's `py_compile` runs without `-W error`, and this machine's `python3` is 3.9.6, where the escape is a silent DeprecationWarning. Root.

## Givens
- `[seen]` Reproduced in a throwaway folder on trunk 53cf79e: `python3.12 -I jig.py --help` (3.12.15), 3.13.15 and 3.14.8 each print `jig.py:2947: SyntaxWarning`. 3.14's text adds "Such sequences will not work in the future". `/usr/bin/python3` (3.9.6) prints nothing.
- `[seen]` No `__pycache__` was written next to the script, so the warning repeats on every run.
- `[seen]` Line numbers move between copies: the plugin copy's docstring opens at 2946 (warning at 2947), the installed `.jig/jig.py` at 2933, cross-repo-roadmap's branch at 2931.
- `[seen]` Every invalid escape: compiling each tracked `.py` with `-W error` on 3.14 and on 3.9 fails only `plugin/templates/jig/jig.py` and `.jig/jig.py`, and `-W always` lists one warning in each, this docstring. `scripts/roles_svg.py` and the eight fixture `.py` files are clean.
- `[seen]` Python embedded in shell: 28 heredoc or single-quoted `python3 -c` blocks and 151 double-quoted ones (shell backslashes undone first) across every tracked `.sh`, `tests/smoke.sh` and `plugin/templates/jig/scripts/` included. None has an invalid escape.
- `[seen]` The fix holds: a copy with `r"""` compiles under `-W error` on 3.9 and 3.14, runs with no SyntaxWarning on 3.14, and `link_spans` returns the same spans as the regex its docstring quotes.
- `[seen]` The guard fires: `python3 -W error -m py_compile` exits 1 on the current file and 0 on the fixed copy, on both 3.9.6 and 3.14.8. On 3.9 the escape is raised as a DeprecationWarning, so `-W error::SyntaxWarning` alone would never fire on this machine's `python3`.
- `[seen]` `.jig/scripts/check.sh` is this repo's own check (plugin validate, roles_svg), not the template's TODO version. It runs on every stop and already does `python3 -m py_compile plugin/templates/jig/jig.py`.
- `[assumed]` A future Python turns invalid escapes into a SyntaxError, and then jig would not load. No version is set, so this is a risk, not a date. The fix doesn't depend on it.

## One layer up
- Sibling: `scripts/roles_svg.py` also runs as a script. It's clean today, and check.sh already runs it, so the guard line compiles it too, at the cost of one argument.
- Sibling: the installed `.jig/jig.py` has the same line. It's fixed by the next `/jig:update`, not by hand.
- Existing pattern: check.sh's `py_compile` line is already the place where "jig.py must compile" is enforced. Adding `-W error` makes compile warnings fail there too.

## Correction
This is a correction, not a workaround: it makes the docstring raw, and the check that let the docstring through now fails on compile warnings.

## Collision with cross-repo-roadmap
No collision, and no need to wait. `git diff 53cf79e...cross-repo-roadmap` touches jig.py in many hunks, but none comes within 100 lines of `link_spans`: the nearest hunks start at 2766 and 3273, and the branch still has the plain `"""` at its line 2931. The branch doesn't touch `.jig/scripts/check.sh`. A one-character change on trunk merges cleanly into the job at its next `jig sync`. The job's own jig.py edits will still face the new guard after it syncs.

## Alternatives considered
- Escape each backslash (`\\[`) instead of `r"""` — rejected because it makes the quoted regex unreadable and no longer the same as the `r"..."` it documents — [seen]
- Put the guard in a smoke section — rejected because smoke runs once per gate or batch, while check.sh runs on every stop, so the warning fails at the edit that adds it — [seen]
- A new check.sh loop that compiles every tracked `.py` — rejected because the fixtures are frozen old releases, all clean, and not jig's live code. It's more lines for no failure — [seen]
- Guard shell-embedded Python — rejected because none has an escape problem, and pulling those blocks out of the shell is a parser, not a one-line guard — [seen]
- `-W error::SyntaxWarning` instead of `-W error` — rejected because on 3.9–3.11, this machine's `python3` included, the escape is a DeprecationWarning, so the guard would never fire here — [seen]
- Fix `.jig/jig.py` by hand too — rejected because AGENTS.md says `.jig/` changes only by `/jig:update` — [seen]
- Add the guard to the template `check.sh` for adopting repos — rejected because adopting repos don't edit jig.py, and their check is theirs to fill — [seen]
- Wait for cross-repo-roadmap to merge — rejected because no hunk overlaps — [seen]

## Done when
- [ ] The guard fires. With the guard line changed and the docstring not yet fixed, `bash .jig/scripts/check.sh` exits 2 with `check: jig.py does not compile`, and the error names the escape. Show the output.
- [ ] After `r"""`, `bash .jig/scripts/check.sh` exits 0 under this machine's `python3` (3.9.6).
- [ ] The symptom is gone: `/opt/homebrew/bin/python3.14 -I plugin/templates/jig/jig.py --help 2>&1 | grep -c SyntaxWarning` prints `0` (it prints `1` on trunk 53cf79e). It also prints `0` with `python3.12`.
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh` passes. The change is a string prefix and a flag, so the full suite is the check role's, at the gate.

## Touches
- `plugin/templates/jig/jig.py`: `link_spans`' docstring opens `r"""`.
- `.jig/scripts/check.sh`: the `py_compile` line becomes `python3 -W error -m py_compile plugin/templates/jig/jig.py scripts/roles_svg.py`.

## Out of scope
- `.jig/jig.py` still warns until the next `/jig:update` installs a release that has the fix. That's expected: the installed copy changes only by update.
- Repos already running 0.15.0 or earlier keep the warning until they update. It's harmless until some Python version makes it an error.
- A guard for Python embedded in shell scripts: there are no cases, and see Alternatives.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
