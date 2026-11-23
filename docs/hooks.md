# Hooks

jig keeps its prose short and puts what must not be skipped into hooks. A rule an agent reads
in a prompt is a polite request. A rule a git hook checks is a refused commit. There are two
sets of hooks: git hooks the checker installs in your repo, and plugin hooks Claude Code runs.

## Git hooks

`python3 .jig/jig.py install-hooks` writes six git hooks. Each one runs [trunk](glossary.md#trunk)'s copy of `jig.py`,
so a branch can't weaken the rules it's judged by.

- **pre-commit** and **pre-merge-commit** run the rules on what's staged. A commit outside the
  [job](glossary.md#job)'s files, a scarce number the branch doesn't hold, or a [workaround](glossary.md#workaround) with
  no ledger row is refused, with the reason.
- **commit-msg** checks a [metarepo](glossary.md#metarepo)'s commit subjects.
- **pre-push** checks what a metarepo pushes to trunk.
- **post-checkout** runs `.jig/scripts/setup.sh` in a new worktree. It warns when the trunk
  checkout has moved off trunk.
- **post-merge** runs the setup script again after a merge.

A repo that already had hooks keeps them: jig chains each one as a `.local` hook beside its own.

## Plugin hooks

The plugin's whole hook config is `plugin/hooks/hooks.json`, and it's short enough to read in a
minute. It has four hooks:

- **After an edit**, it runs the repo's own `.jig/scripts/format.sh`.
- **When the agent stops**, it runs the repo's own `.jig/scripts/check.sh`, the quick level.
  A failure there keeps the agent from finishing.
- **With each prompt**, in the trunk checkout, it prints a count of unread messages in the
  repo's [inbox](glossary.md#inbox). It reads nothing else and moves nothing.
- **At session start**, it prints one line naming the session's [node](glossary.md#node):
  [hubnode](glossary.md#hubnode) or [subnode](glossary.md#subnode), and which job. A session
  that lost its instructions to compaction is told again. It runs in any repo with a `.jig/`
  folder, and it only reads and prints.

## Opting in

Claude Code warns about every plugin with hooks, because hooks run shell commands as you.
The other three hooks run only in a repo that opted in. The session-start hook runs nothing of
the repo's: it reads and prints one line.
`python3 .jig/jig.py install-hooks` writes the opt-in marker, `.git/jig/enabled`. Git never clones `.git/`, so a repo you fetched can't turn itself
on and get its scripts run.
