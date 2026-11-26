# Handoff: layout-and-formats

Commit: 2c348f9514952989ee5f6d1adaf64d6ebdd2cb85
Date: 2026-11-26
Spec: .jig/specs/layout-and-formats.md
Source: Claude chat session reviewing the .jig folders of seven repos / 2026-11-21 to 2026-11-24 / the owner, with Claude (staged as request-layout-and-formats.md): "One request in five parts, wanted before 0.16's roadmap and glossary features are rolled out to any other repo. It changes where jig keeps things and in what format."
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Parts 4 and 5 of 5; the job is complete. Parts 1 to 3 were handed off in the 2026-11-24,
2026-11-25 and 2026-11-25-2 notes.

**Part 4.** The glossary takes one form: `# Basic terms`, then each product as an H1 with `Repo:`
and `Kind:`, each feature as an H2 and each term as an H3. The headings are the terms; table rows
no longer are. A term's controlling repo is its product's `Repo:`; `Owner:` and `this repo` are
gone, and the glossary's own repo reads "" in `term_owners`. The hook refuses a commit that adds
a form problem (`glossary_rules`, which replaces `owner_dropped`), and treats an absent glossary
as having none. `jig merge` re-sorts a glossary in the form. Also new: `jig glossary "<term>"`,
`jig glossary add` and `jig decision --page`. init seeds `Basic terms` and the repo's software
product. update rewrites `Owner:` as `Repo:`/`Kind:` and reports a glossary out of the form under
Repo files to review. move-in writes `Repo:`/`Kind:`.

**Part 5.** The rulebook is eleven rulesets in `.jig/rules/`, split word for word. Each family
ruleset is written only in its kind of repo, and every citation follows. `.jig/templates/` holds
every record's template. The ledgers are lowercase, and update renames them with `git mv` and
rewrites the header cell. jig's text says "the owner". The rigger is the designer (`/jig:designer`,
`jig designer`); the repos list's old `rigger` key is read and rewritten. update now cites the
rulesets in the log header and in staging's and inbox's `.gitignore`.

## Done-when evidence
Parts 4 and 5's items.
- **The complete suite runs at the gate, as the owner set.** While building, the runs were check
  plus the touched sections, each run once except where the owner approved a rerun.
- **check** (`python3 .jig/jig.py queue -- .jig/scripts/check.sh`): rc 0 on every run.
- **Part 4**, at bb4a086:
  - `queue -- bash tests/smoke.sh claims docmap family family_report glossary glossary_form headings
    homes ideas_labels labels meta_docs metarepo move movein phase_types pointers removals
    report_fixes roadmap roadmap_edit rules staging update`: rc 0, 1041 PASS, 0 FAIL;
  - part 4's fixes (609b7ce): `glossary_form rules`, rc 0, 78 PASS. The other 9 sections stand on
    the prior run, on the owner's word.
- **Part 5:**
  - designer: `designer inbox repos`, rc 0, 68 PASS;
  - templates and ledgers (818f28a): 19 sections, rc 0, 714 PASS; `ledger_rows`, 8 PASS;
  - rules split (f2c5e43): 25 sections, 905 PASS, 15 FAIL. Three causes, all fixed. Then
    `decisions metarepo pointers`: 164 PASS, 5 FAIL. One more cause (the ledger step and M4), fixed.
    Then `decisions`: rc 0, 55 PASS;
  - strike-2 fixes (5adb287): `rules update homes decisions ledger_rows`, rc 1, 315 PASS, 2 FAIL.
    Both failures were the two pararepo ruleset cases, whose metarepo fixture had no release. The
    fixture now runs `jig release`. **Not rerun after that fix, on the owner's word ("Skip, commit
    as is")**: the gate's complete check runs them.
- **Glossary form:** `smoke glossary_form`, one case each:
  - the refusals;
  - a new glossary held to the whole form;
  - an older one staying editable;
  - update's rewrite, including two products naming one repo;
  - update's report of the real rewrite;
  - glossary add and query;
  - the sort, byte for byte, and no sort out of the form;
  - the merge re-sort;
  - decision --page.

  The dropped-product refusal is in `smoke movein`. `grep -n 'OWNER_LINE\|THIS_REPO' jig.py` finds
  nothing.
- **The rulesets:** `find plugin/templates/jig -name '*[A-Z]*'` finds nothing. `grep -rn 'RULES.md'
  plugin docs` finds only old-layout names jig recognises (LAYOUT, RETIRED_LINES, SEED_COMMENT, the
  old log header) and a repo's own root RULES.md.
- **"The owner":** `grep -rniz 'the[[:space:]]*user' plugin` finds nothing.
- **The designer:** `grep -rnw 'rigger|riggers|Rigger|Riggers' plugin docs tests` finds only the
  old-key read and its smoke case.
- **The Later grep exception (part 3):** `SEED_COMMENT` (jig.py ~11926) keeps the old seed's
  `Later:` text. The conversion drops that comment only when it matches byte for byte.
- **Refine pass, deferred to its own spec on the owner's choice ("Defer to its own spec",
  2026-11-25):** three rulesets are still over 200 lines: rules-docs.md 405, rules-roadmap.md 297
  and rules-workflow.md 249. rules-decisions.md is 272, which the spec expects. Survey reports all
  four. The Done when reads as met by that deferral.
- **What the split dropped:** only RULES.md's `## Commands` section, which `jig -h` covers.
- **The gate.** The complete check ran once at c8c772e: 2,432 PASS and 1 FAIL. The failure was
  the staging_batches case "rules-staging.md § Staging: the target sentence and the Accepted
  warning". Its `sed -n '/^## Staging/,$p'` sat inside a double-quoted `sh -c`, so `$p` expanded
  under `set -u` (p: unbound variable). It came in with f2c5e43. 2c348f9 escapes it as `\$p`, and
  changes nothing else. A run of staging_batches alone confirms the fix, on the owner's word
  ("re-check this 1 case and then force recording the gate as passed").

## Review
Parts 4 and 5 share one review count, since part 4 wasn't handed off on its own.
- review-change of f88681f..bb4a086 (part 4): 3 blocking (strike 1).
  - B1: a new glossary escaped the first-H1 rule.
  - B2: update's report invented a shared repo.
  - B3: genre and Touches wording.
  - Should-fix S1 (the report as a no-op step) and S2 (sort only in the form); optional O2 and O3.
  - All fixed in 609b7ce. taken: 2 should-fix, 2 optional; deferred: 3 (part 4's O1, O4, O5).
- review-change of bb4a086..f2c5e43 (parts 4's fixes and 5): 3 blocking (strike 2).
  - B1: "the user" split across lines.
  - B2: no smoke for the family rulesets or the survey report.
  - B3: no Removed lines.
  - Should-fix S1 (old RULES.md citations in the log header and the .gitignores); optional O2.
  - Fixed in 7646005 (spec) and 5adb287. taken: 1 should-fix, 1 optional; deferred: 2 (O1
    DOC_HOMES, O3 survey's README message).
- review-change of f2c5e43..5adb287: 0 blocking. taken: 0 should-fix, 0 optional; deferred: 2 (two
  seeded lines citing .jig/RULES.md; the survey case's unchecked rc).
- review-change of 5adb287..2c348f9 (the gate fix): 0 blocking. taken: 0 should-fix, 0 optional; deferred: 0.

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
- [x] docs/commands.md — updated: jig glossary, decision --page, init's glossary, the designer
- [x] docs/hooks.md — no change because it describes the plugin's hooks.json, which this job didn't change
- [x] docs/jobs.md — updated: the merge keeps the spec's Scope: line, and the workarounds ledger's name
- [x] docs/metarepos.md — updated: move-in's product heading with Repo: and Kind:, the buffer ledger's name, the designer
- [x] docs/records.md — updated: the glossary's one form, the rulesets' citations
- [x] docs/workflows.md — no change because it names no file, form or rulebook path this job changed
- [x] UNOWNED tests/roadmap.py — no page needed because it is smoke's own tooling (the repository's own tooling, its build, CI, release and dev scripts, needs none)

## Shared files changed
- `plugin/templates/jig/jig.py`, `plugin/templates/jig/rules/` (new; RULES.md removed),
  `plugin/templates/jig/templates/` (new), `plugin/templates/AGENTS.md`, `plugin/templates/jig/scripts/derive.sh`,
  `plugin/templates/jig/staging/.gitignore`: the glossary form, rulesets, templates, ledger names, the owner.
- `plugin/skills/*/SKILL.md` (most, for rulesets, the owner and template paths); `plugin/skills/rigger/` → `designer/`.
- `tests/smoke.sh`, `docs/*.md`, `README.md`, `.jig/decisions.md` (Unreleased), `.jig/ledgers/DEFERRED.md`
  (rows), `.jig/specs/layout-and-formats.md` (part 5's designer list and Breaking line, the owner check).
- `tests/smoke.sh` (2c348f9): the staging_batches case's sed.

## Test by hand
In a repo set up by an older jig, run `jig update --apply` and commit. Check:
- `.jig/rules/` replaces `.jig/RULES.md`;
- the ledgers are lowercase, with `Job / handoff` in deferred.md's header;
- `.jig/templates/` is filled;
- each glossary `Owner:` line now reads `Repo:` and `Kind:`.

Then `jig glossary add <term> --text ...`, `jig glossary <term>`, and `jig survey`, which names the
rulesets over 200 lines.

## Left
Nothing on this job. Its spec's refine pass for rules-docs, roadmap and workflow is deferred to
its own spec, which the hubnode writes on trunk (the owner, 2026-11-25). Two things are for the
hubnode:
- marketing/FEATURES.md's rows for the rulesets, templates, glossary commands and the designer
  rename;
- the spec for the refine pass.
