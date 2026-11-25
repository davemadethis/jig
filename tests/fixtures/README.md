# Update fixtures

One made-up repo per generation of jig and the tools before it, for `tests/smoke.sh`.
Each `<generation>/repo/` is the tracked tree; `<generation>/git/` is copied into `.git/`
(hooks and markers that tool left there). Every repo has the same content: a docs page with
section 1, a source file, a merged job, a handoff, a spec, both ledgers' worth of rows.
`update --apply` must take each to the same jig paths and board keys.

- `claude-lane/`: `.claude/claude-lane/`, the coordination tool jig grew from.
- `ai-dev/`: `.aidev/`, with root ledgers, root `specs/`, `docs/REVIEW_LEDGER.md` and a
  root `HARDWARE.md`.
- `jig-0.2/`: the visible `jig/` folder every 0.2.x repo had.
- `dot-jig-v7/`: `.jig/` with the one-file board, version 7.

`roadmap-show/` is not a generation: a metarepo's `roadmap.json` with two products, and the
charts `jig roadmap show` draws of it, at the default width (one band per phase) and at
`--width 200`, compared byte for byte.
