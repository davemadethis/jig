# Handoff: jig-0.17.0-upgrade

Commit: 977808e48d4e5e2fd9c4191661e1264c414613fd
Date: 2026-11-26
Spec: .jig/specs/jig-0.17.0-upgrade.md
Source: jig hubnode session / 2026-11-26 / the owner (staged as jig-0.17.0-upgrade.md)
Review: tier 2, effort 3
Ran: claude-opus-5-5 at medium

## Built
`docs/glossary.md` rebuilt into the one form: `# Glossary`, `# Basic terms` (Trunk, Workaround),
then `# jig` (own terms Page contract and Spec; features Decision log, Job, Metarepo, Roadmap,
Staging, Workflow, the rest their terms). Every term's text is unchanged; new text is the two new
headings, `Repo: jig`, `Kind: software` and jig's two-sentence definition. `AGENTS.md`'s line on
Claude-specific text names the rules folder where it said `RULES.md` (owner: "Yes, repoint it").
No spec on trunk had a `Later:` line, and no `## Out of scope` read needed a roadmap item.

## Done-when evidence
Rollback: main at 357a0d37f4cf5afebfca42bbcae51711c19fa42e, pushed to origin on 2026-11-26
Update's trunk commits: b688967 (run 1; run 2 said up to date), 4768eb9 (docmap globs).

- Rollback line first: `git log -- <spec>` shows c807e39 (10:15) before b688967 (15:33);
  `git branch -r --contains 357a0d3` prints origin/main.
- Process check before open: cdcea41 (10:35) predates add5178 `open jig-0.17.0-upgrade` (15:34).
- Update "up to date": the hubnode's run 2 on trunk, not rerun here. `git hash-object .jig/jig.py`
  and `plugin/templates/jig/jig.py` both a0c85e8. In this worktree the repo plugin's dry run exits
  2 (a job's worktree is open); it lists `.jig/templates/skill.md` as differing only by
  frontmatter comments (the process check: the host strips them) and AGENTS.md:20,23-25, kept.
- Layout: `.jig/rules/` holds 9 rulesets, no `.jig/RULES.md`; `.jig/templates/` exists;
  `.jig/ledgers/` holds deferred.md.
- `.jig/docmap.json` exists; config.json has none of docmap, boards, deep_subsystems, not_docs.
- `jig roadmap show`: "The roadmap is empty." No `.jig/roadmap.md`, no `ROADMAP.md`.
- `grep '^Later:' .jig/specs/*.md`: nothing.
- Glossary: commit hook passed 529318a; no `Owner:` lines (count 0); `jig glossary Gate` prints
  `jig > Job > Gate`; the update dry run reports no form problem, only `.jig/` path lines; all 28
  linked `glossary.md#` anchors resolve; a script compare with the old file lost no line or heading.
- `grep -n roadmap: AGENTS.md`: line 17.
- Step 2's grep outside `.jig/`: no hit in AGENTS.md, README.md or docs/. Hits are in plugin/ and
  tests/ (left, process check) and `scripts/roles_svg.py:166`, matched by `rigger` inside
  `trigger`: not a stale name.
- `jig queue -- .jig/scripts/check.sh` at 977808e: exit 0. `jig survey`: exit 0, "On jig already:
  nothing to do."; it still lists the `.jig/` path lines in docs (owner's exception) and long
  rulesets. No smoke section run (docs only); full suite not run.
- This note carries the `Rollback:` line and the commits.

## Review
Two passes. (1) The glossary at 529318a: 0 blocking, 0 should-fix, 1 optional; taken: 0
should-fix, 0 optional; deferred: 1. (2) The AGENTS.md line at 977808e: 0 blocking, 0 should-fix,
1 optional that asked for no change; taken: 0 should-fix, 0 optional; deferred: 0.

## Fold-in
<!-- Every documentation page that covers code this changed: does it still describe the
     code? Replace each ___ and tick the box: the stale sentences are edited (deleting
     counts), or none went stale and this says why. Each roadmap item naming one of those
     pages (a No phase item not done, or a taken scope) has its own line: keep one answer,
     built, untouched or departed: <why>. An item stays in the roadmap, read done once a
     spec taking it is complete. The gate refuses an unanswered line. An UNOWNED file has no page
     covering it: add it to docmap in .jig/docmap.json, or say why it needs none. A pair line
     (`<id> vs <log> § <ids> (<page>): ___`) is answered after its colon, once for every id
     on it: agrees, narrows: <how>, or conflicts: <resolution>; on a line of several ids,
     narrows and conflicts name at least one of them. jig reads the rest of the line, so it
     stays as jig wrote it. -->
- [x] no code changed — nothing to fold in

## Shared files changed
- `docs/glossary.md`: the rebuild into the one form.
- `AGENTS.md`: the stale `RULES.md` mentions.

## Test by hand
Read `docs/glossary.md`; follow a glossary link from README.md on GitHub.

## Left
Gate and merge (the merge on the owner's word).
