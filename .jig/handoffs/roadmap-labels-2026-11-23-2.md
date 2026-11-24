# Handoff: roadmap-labels

Commit: cc569049b936c92c72ac720e5dd3c0ca8677e572
Date: 2026-11-23
Spec: .jig/specs/roadmap-labels.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
The whole of roadmap-labels, three parts. This note supersedes roadmap-labels-2026-11-23.md, whose gate failed on CI over one test (Review).
Part A, labels: a scope or a `No phase` item may end `(labels <term>, …)`, peeled by `split_waits` in any order with its other parentheses. Each label is a glossary term (the metarepo's in a family, read live; a stand-alone repo's own), matched with case and spacing folded (`label_fold`). The hook refuses on trunk a label naming no term, an empty `(labels)`, a second `(labels …)`, a labels line on a phase, and a glossary commit dropping a term a label names, naming each scope. A label is no ref and changes no state. `split_labels` and `label_problems` are the one reader and the one check. `jig roadmap` and the view show labels, and `--label` is a row in phase-types' `ROADMAP_FILTERS`, headed by the term's owner, each line naming its owning repo.
Part B, `jig family`, from the metarepo or any pararepo: staged files with ages, unmerged or empty `propose/` branches with ages and the specs citing them, Open and Unreleased entries touching a term that labels work not done, and pairs of names. Stale is past 7 days. `jig rig` prints one `Family:` line, counted in neither number.
Part C, `jig roadmap --draft` / `--edit`. The draft sits outside the tree; in a pararepo with an open roadmap proposal it shows that proposal's lines (Interpreted, confirmed by the owner). The edit refuses by line a change under another repo's heading, a new heading in a pararepo naming no product it owns, and anything the hook refuses on the result. In the metarepo or a stand-alone repo it writes trunk's checkout. In a pararepo it writes the proposal branch first, by plumbing (no checkout moves), then a BUFFER row and a `roadmap-<date>.md` spec. A label the metarepo's glossary lacks is left off and staged there as `label-<term>.md`. The hook on a metarepo `propose/<repo>-…` branch runs the same section check: the repo is found by its `jig repos` name or its folder; a branch naming none is refused; the fork is the commit being made's, so trunk merged in is trunk's.

## Done-when evidence
At 2cca386, each in a throwaway repo with JIG_CONFIG and XDG_CONFIG_HOME set per section:
- Part A, form, refused, no dependency, term guard, read by label, no glossary: smoke `labels`, 18 PASS.
- Part A, one of the filters: `labels` cases `--label teleport --state open`, `--label teleport --phase alpha`, and `--view --label teleport` (stdout only, ROADMAP.md unchanged): PASS.
- Part A, one reader: `grep -c '^LABELS = re.compile'` prints 1 and no other pattern reads `(labels` (smoke `labels`); `roadmap_filter` asks `label_problems`: PASS.
- Part A, live and unreachable: smoke `family`, the 3 "family labels" cases ("Teleport: owned by pb" in pa), plus the existing unreachable-meta case: PASS.
- Part B, staged, proposals, entries, two names, rig, unreachable: smoke `family_report`, 14 PASS.
- Part C, pararepo edit, one proposal at a time, another repo's line, the hook's refusals first, label staged, metarepo edit, no clobber, stand-alone, plus the review's cases (label-only, after-only and exit-box edits; trunk bytes kept; hand commits and merges on a proposal branch; folder-named pararepo; branch naming no pararepo; no filters): smoke `roadmap_edit`, 36 PASS.
- No regression: `python3 .jig/jig.py queue -- bash tests/smoke.sh labels family_report roadmap_edit phase_types roadmap family rig pararepo metarepo sync_buffer staging boundary moves`: 601 PASS, 0 FAIL, rc=0 at 2cca386. At cc56904: `python3 .jig/jig.py queue -- bash tests/smoke.sh update labels`: 129 PASS, 0 FAIL, rc=0; `python3 .jig/jig.py queue -- bash tests/smoke.sh update_roles`: 38 PASS, 0 FAIL, rc=0, including "update roles: no repo name and no exception list in jig.py or the update skill"; `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0. `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0. `claude plugin validate ./plugin`: Validation passed.

## Review
review-work of 18b0f0a: B1 (an edit changing no scope id or text was thrown away) fixed in bde08ab: changes are judged by section text. S2 (splice respaced others' sections), S3 (a hand commit on a proposal branch passed under another repo's product), O5 (row and spec written before the branch) and O6 (spec regression line) fixed. O4 (label-term guard fires only at the trunk merge) is in DEFERRED.md.
review-change of 64c1c35: 0 blocking. After the sync with phase-types: `--label` wired into ROADMAP_FILTERS; F1 (folder-named pararepo unmatched), F2 (merging trunk refused) and F3 (RULES sentence) fixed in 3ab9fb7 and 5f617b2.
review-change of 5f617b2: B1 (a merge resolution keeping a stale copy of another repo's section passed) fixed in 2cca386: the fork is the commit being made's. S1 (`--label` copying label_problems) and O1 (filters ignored by --draft and --edit) fixed.
review-change of 2cca386: 0 blocking. Its two notes (squash-merge hint; `since_trunk`'s mid-merge form) are in DEFERRED.md.
The gate's complete check on CI failed once: label examples named an adopting repo (`walyt-compatibility`) in jig.py and RULES.md, which update_roles refuses. Fixed in cc56904 (`wallet-compatibility`, also in docs/records.md).
review-change of cc56904: 0 blocking. Its should-fix (docs/workflows.md's family line left out an empty proposal and a pending decision touching labelled work, both of which `family_counts` counts) is fixed in this handoff commit.

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
- [x] docs/commands.md — updated: `roadmap --label` among the filters, `--draft`/`--edit`, and `jig family`   (4 files)
- [x] docs/hooks.md — no change because it names no roadmap rule; RULES.md § Roadmap holds the label and proposal-branch refusals   (1 file)
- [x] docs/jobs.md — no change because it mentions the roadmap only for R5, which is unchanged   (2 files)
- [x] docs/metarepos.md — updated: § Editing the roadmap and § The family report   (2 files)
- [x] docs/records.md — updated: § Roadmap says how scopes carry labels and how to read by one   (2 files)
- [x] docs/workflows.md — updated: § The rig says when the family line points at `jig family`, every trigger `family_counts` counts   (5 files)

## Shared files changed
- plugin/templates/jig/jig.py: the label reader (`LABELS`, `split_labels`, `label_fold`, `label_problems`) and `split_waits` returning four values; parse_roadmap/parse_section, Family (its glossary), roadmap_full, scope_cell, cmd_roadmap, ROADMAP_FILTERS and roadmap_filter (`--label`), roadmap_rules (labels on trunk, the term guard, the proposal-branch section check); roadmap_problems, dropped_scopes, scope_holders and others_holding, factored so `--edit` calls what the hook calls; the edit command (roadmap_draft, roadmap_edit, roadmap_changes, section_refusals, splice_sections, plumb_commit, record_roadmap_row, stage_label); the family report (family_report, cmd_family, rig's `Family:` line); the parser.
- plugin/templates/jig/RULES.md: § Roadmap (Labels, Filters, Edits: the edit command and the proposal-branch check), § Metarepo and pararepos (the family report, a staged label), § Workflow (rig's Family: line), Commands.
- plugin/skills/hubnode/SKILL.md (a roadmap change by --draft/--edit), plugin/skills/rig/SKILL.md (the Family: line), plugin/skills/spec/SKILL.md (an item's labels).
- docs/records.md, docs/metarepos.md, docs/commands.md, docs/glossary.md (a Label term), docs/workflows.md (the rig's family line).
- tests/smoke.sh: new sections labels, family_report, roadmap_edit (in UNITS); family labels cases at the end of family; phase_types' untested-row case now uses a made-up `colour` filter, since `label` is real.

## Test by hand
In a pararepo of a family: `python3 .jig/jig.py roadmap --draft`, add a scope with `(labels <a glossary term>)` under one of its own product's phases in the draft it names, then `python3 .jig/jig.py roadmap --edit`. The metarepo gains a `propose/<repo>-roadmap-<date>` branch with the scope, its trunk untouched, and this repo a BUFFER row and a spec to commit. Then `python3 .jig/jig.py roadmap --label <term>` and `python3 .jig/jig.py family` in the metarepo.

## Left
Nothing on this job. Three optional notes are in DEFERRED.md: the label-term guard firing only at the trunk merge, the squash-merge refusal's missing hint, and `since_trunk`'s older mid-merge form.
