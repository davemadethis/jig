# Bug: the complete check fails on GitHub's runner

Source: the owner (Dave Seeman), 2026-11-23, through the hubnode: "the complete check fails on GitHub's runner: 75 smoke FAILs on ubuntu-26.04" (`queue.overflow` to GitHub, run https://github.com/davemadethis/jig/actions/runs/45041832530 at trunk 53cf79e; the same commit's suite passed on the owner's Mac)

## Intent
The complete check gives the same answer on the runner as on the Mac. Smoke stops reading the
machine it runs on: git's identity and Python's bytecode files come from smoke itself, not from
`~/.gitconfig`, Apple's Python or the session's environment.

## Whys
1. Why 75 FAILs on the runner and none on the Mac? Three independent causes, by count: a SyntaxWarning
   on stderr (50), no git identity in clones smoke makes (23), a `__pycache__` copied into `.jig/` (1).
   One more (`checked --trace`) is unconverted; see Givens.
2. Why did the Mac hide all three? Each is filled in by this machine: Python 3.9 doesn't warn,
   `~/.gitconfig` and the account's full name give every clone an identity, and Apple's Python
   writes bytecode to `~/Library/Caches/com.apple.python`, never beside the source.
3. Why can smoke lean on the machine? It sets `user.name` in each repo it `git init`s, but nothing
   for the repos it `git clone`s, and nothing about bytecode. Root: smoke has no hermetic setup of its own.

## Givens
- `[seen]` The CI log: 75 `FAIL` lines; `Image: ubuntu-26.04`, `git version 2.56.1`; the warning's
  text "Such sequences will not work in the future" is Python 3.14's (bug-docstring-escape's givens).
  `claude plugin validate` passed there (check.sh got to smoke), with the npm postinstall script skipped.
- `[seen]` Reproduced 74 of the 75 here, by causes run apart (Python 3.14.8 through a `python3` shim on PATH,
  every run through `jig queue`):
  - py3.14 with the Mac's identity: 50 FAILs, all from `jig.py:2947: SyntaxWarning` on stderr. Cases
    that read `$(… 2>&1 | head -1)` or compare all output get the warning line, e.g. `update <old>:
    a second --apply is up to date`, every `next:` case, `form: … judged in seconds`.
  - py3.9 with no identity: 23 FAILs, all in `sec_pararepo` (propose, sync, pointers, roadmap-cite and
    R2 cases): every one follows a `jig propose` (or a release's buffer proposal) whose opening `git commit-tree`
    runs in a metarepo checkout smoke made with `git clone`. A clone doesn't copy the source's local
    `user.name`, so only a global identity reaches it.
  - The two sets are disjoint; py3.14 with no identity gives 73, exactly CI's set minus two.
  - `init: .jig/ holds … nothing else`: reproduced by running py3.14's `py_compile` on
    `plugin/templates/jig/jig.py` first, as check.sh does before smoke. It writes
    `plugin/templates/jig/__pycache__/`, and `cp -r "$P/jig" .jig` (46 places in smoke) copies it in.
- `[seen]` `python3 -m py_compile` writes `__pycache__` beside the source on Python 3.14 even with
  `PYTHONDONTWRITEBYTECODE=1`. `/usr/bin/python3` (3.9.6) has `sys.pycache_prefix` set to
  `~/Library/Caches/com.apple.python`, so it never writes into the tree. This session's environment
  also has `PYTHONDONTWRITEBYTECODE=1`; the runner's doesn't.
- `[seen]` Smoke's importlib loads of `$P/jig/jig.py` (smoke.sh:503, 2471, 7100) write into the same
  `plugin/templates/jig/__pycache__/` wherever bytecode writes are on, and sections run in parallel, so
  which sections copy it is a race.
- `[seen]` On this Mac `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1` alone does not remove the
  identity: git builds one from the account's full name and host (`Dave Seeman <daveseeman@MacBook-Pro-2.local>`).
  Adding `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.useConfigOnly GIT_CONFIG_VALUE_0=true` gives the
  runner's refusal. On the runner, the `runner` account has no full name: "empty ident name … not allowed".
- `[seen]` Runs with `GIT_CONFIG_GLOBAL=/dev/null` (no `init.defaultBranch`, no global settings at all)
  failed only identity cases, so no other smoke case depends on the owner's global git config. The
  default branch name doesn't matter: smoke's `git init`s say `-b main`, and its bare remotes only receive pushes.
- `[assumed]` `checked --trace: the printed first-parent bisect … names the second merge` fails for a
  fourth reason. It passed here on py3.14, with no identity, with bytecode writes on and with
  `__pycache__` copied in. What's left: Linux (dash as `sh`, GNU tools) or git 2.56.1 (this Mac has 2.53.0;
  no Linux or newer git here: Docker's daemon isn't running). The case discards the bisect's output,
  so the log can't say which. `[seen]` that it's apart from the other three: one full run here with
  all of them stacked (py3.14, no identity, bytecode writes on, `__pycache__` made first) fails 74
  cases, CI's 75 less this one.
- `[seen]` Every jig.py path that commits, with no identity:
  - `jig propose` / `--buffer`, and `jig release`'s buffer proposal in a pararepo (`open_proposal`):
    `die` with git's message ("Author identity unknown … tell me who you are"), exit 2, before the spec
    line, the buffer spec or the branch is written. Nothing half-done.
  - `jig release`'s own `commit-tree` and `tag -a`: `die` with git's message. Only reachable in a
    repo nobody has committed in, since jig's hooks run on the owner's own commits first.
  - `jig merge`: `git merge --no-ff --no-commit` itself refuses (exit 128, no MERGE_HEAD), so it dies
    with git's message before the "If the hook refused" text.
  - `jig sync` (`merge_trunk`): the merge refuses, then `git commit --no-edit` dies with git's message.
  - `jig sync` on a pararepo (`sync_meta`, `sync_answered`) and `jig rig --close`: git's message on
    stderr, then jig's line ("the commit was refused: … staged as jig wrote them" / "fix what the hook refused").
  - `jig init` commits nothing.

## One layer up
- Sibling: the product. Every jig commit path stops with git's own message, which names the fix. The
  only one an ordinary adopter reaches is `jig propose` (or a pararepo release with Open buffer rows)
  when the metarepo checkout has no identity of its own and the user's identity lives only in the
  pararepo's local config. There, jig writes nothing before git refuses, and git says exactly what
  to run. So the product stays as it is: git's message suffices, and a smoke case pins that behavior.
- Sibling: the adopter's workflow template, `plugin/templates/github/jig-check.yml`, runs the adopter's
  own check. jig.py commits nothing in a check run, so nothing there needs an identity from jig. A
  suite that commits in throwaway repos is the adopter's to make hermetic, as smoke is here.
- Existing pattern: smoke already isolates jig's own config (`JIG_CONFIG`, `XDG_CONFIG_HOME`, the
  isolation case). Git's config and Python's bytecode get the same treatment, in the same place.

## Correction
This is a correction: smoke builds its own environment instead of inheriting the machine's.
- The SyntaxWarning (50) is fixed by bug-docstring-escape (gated, batch, not yet merged at e8d549f):
  `r"""` on `link_spans`' docstring. This job waits for that merge and changes nothing of it.
- Identity (23): smoke writes a git config of its own in `$RUN` (`user.name`, `user.email`) and
  exports `GIT_CONFIG_GLOBAL` to it and `GIT_CONFIG_NOSYSTEM=1`, before any section starts. Every
  repo and clone a section makes gets the identity; the owner's `~/.gitconfig` is never read.
- Bytecode (1): smoke exports `PYTHONDONTWRITEBYTECODE=1` before any section starts, and check.sh's
  compile line stops writing: it compiles with `compile()` under `-W error` instead of `py_compile`,
  which writes `__pycache__` whatever the environment says.
- `checked --trace` (unconverted): the case prints the bisect commands and their output when it
  fails, so the next runner log names the cause. If it still fails once the rest is green, the work
  role reads that log, fixes it in this job if the cause is the test's or jig's printed bisect, and
  records what it was under Decisions.

## Alternatives considered
- `git config --global user.name …` as a step in `.github/workflows/jig-check.yml` — rejected because
  smoke on the Mac would still read the owner's `~/.gitconfig`, so the next clone without an identity
  passes here and fails there again — [seen]
- `git -C <clone> config user.name …` after each of smoke's six `git clone`s — rejected because the
  seventh clone repeats the bug; one setting before the sections covers every repo — [seen]
- `GIT_AUTHOR_NAME` / `GIT_COMMITTER_NAME` env vars in smoke — rejected because they override every
  repo's local identity, which a case reading `%an` could depend on; a global config file sits below
  local config, as the owner's does — [assumed]
- jig.py refuses up front with its own message when no identity is set — rejected because git's
  message already names the fix and every jig path stops before writing anything that matters (Givens);
  an up-front check would be a second, weaker copy of git's own — [seen]
- `cp -r` without `__pycache__` in smoke's 46 copies — rejected because it patches 46 readers instead
  of the two writers — [seen]
- `PYTHONDONTWRITEBYTECODE=1` in check.sh in place of `compile()` — rejected because `py_compile`
  writes `__pycache__` with it set, on 3.14 — [seen]
- Pin the runner to `ubuntu-24.04` or an older Python — rejected because the Mac's Homebrew 3.14 gives
  the same failures; the image only showed them — [seen]

## Done when
- [ ] bug-docstring-escape is merged on trunk, and this job has synced it.
- [ ] Identity no longer comes from the machine: `python3 .jig/jig.py queue -- env GIT_CONFIG_COUNT=1
  GIT_CONFIG_KEY_0=user.useConfigOnly GIT_CONFIG_VALUE_0=true bash tests/smoke.sh pararepo`
  passes (on trunk e8d549f the same command fails the 23 propose-led cases, all in that section). Show the output.
- [ ] No bytecode beside the source: after `env -u PYTHONDONTWRITEBYTECODE PATH=<a python3.14 shim>:$PATH
  bash .jig/scripts/check.sh`, `find plugin -name __pycache__` prints nothing (on e8d549f it prints
  `plugin/templates/jig/__pycache__`). Show the output.
- [ ] The runner's conditions, stacked, here: `python3 .jig/jig.py queue -- env -u PYTHONDONTWRITEBYTECODE
  PATH=<a python3.14 shim>:$PATH GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_COUNT=1
  GIT_CONFIG_KEY_0=user.useConfigOnly GIT_CONFIG_VALUE_0=true bash .jig/scripts/check.sh --full` passes. Show the output.
- [ ] The product's chosen behavior with no identity: a new pararepo smoke case runs `jig propose` once
  with `GIT_CONFIG_GLOBAL=/dev/null` and `user.useConfigOnly=true`, against a metarepo clone with no
  local identity. It exits non-zero, its output holds git's "Author identity unknown", the spec is
  unchanged, and the clone has no `propose/` branch.
- [ ] `checked --trace`'s bisect case prints the bisect commands and their output when it fails.
- [ ] The symptom is gone: `jig queue --full` overflows to GitHub, a fresh `jig-check/*` run is green,
  and `jig checked --ci <that run's url>` records it. Show the run's URL and the record.

## Out of scope
- `jig rig --close`'s "fix what the hook refused" and `sync_meta`'s "the commit was refused" lines
  under git's identity message. Git's line above them names the cause; rewording them is polish.
- The installed `.jig/` keeps its old check.sh and jig.py until the next `/jig:update`. The overflow
  run uses this repo's `.jig/scripts/check.sh`, which is this repo's own file, so it changes in this job.
- The npm postinstall warning in the workflow's `claude CLI` step: validate passed with it skipped.
- `~/.config/jig/repos.json` changed during one local rerun here (08:37, 2026-11-23), from another
  session's live jig work; smoke's isolation case reported it as designed.

## Touches
- `tests/smoke.sh`: before the sections start, a git config file in `$RUN` exported as `GIT_CONFIG_GLOBAL`,
  `GIT_CONFIG_NOSYSTEM=1`, `PYTHONDONTWRITEBYTECODE=1`; the propose-with-no-identity case in `sec_pararepo`;
  the `checked --trace` bisect case prints what it got on failure.
- `.jig/scripts/check.sh`: the compile line compiles without writing bytecode. Waits for
  bug-docstring-escape, which changes the same line (`-W error`); keep its flag.

## Decisions
- The product keeps git's own identity message; no jig.py change (see One layer up).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
