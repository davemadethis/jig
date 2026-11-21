# Handoff: bug-nested-touches

Commit: fb848c3aa46d04f6e5276a8eef6a1e159b43f6a1
Date: 2026-11-21
Spec: .jig/specs/bug-nested-touches.md
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
- `spec_section(text, *names)` in jig.py is now the one reader of a spec section. It matches a heading at `##` or deeper, and the body ends at the next heading from `##` down to its own level. `touches_spans`, `proposal_branches` and `review_shortfall` call it, so a bug role's nested `### Touches`, `### Proposals` or `### Roles` is read.
- `plugin/skills/bug/SKILL.md` step 5 says to write the template's sections as `## ` headings, with steps 1–4 above them, never nested under a step.
- `plugin/templates/jig/RULES.md`: the two Touches lines say any heading level is read.

## Done-when evidence
- Fix fires: `jig queue -- bash tests/smoke.sh consolidate workflow` → `PASS  consolidate: a ### Touches nested under another heading overlaps a ## Touches` (it greps `n1 and n2 share: lib/a.py`), and `PASS  rig: a nested Touches ends at its level's next heading; …` (rig --json: n2 touches `['lib/a.py']`).
- A nested section ends where it should: the same rig case asserts n2 leaves out `app/src/x.ts`, which sits under `### Out of scope`, and n1 keeps `lib/n1.py`, which sits under a `### Notes` inside `## Touches`. It also keeps `lib/n0.py`, which comes after a fenced `# run it`.
- Proposals nested: `PASS  metarepo: open on a spec listing proposals (nested under ## Spec): the kickoff says to merge each into the job's branch, in the spec's order`. A top-level `## Proposals` is covered too: `PASS  proposals: a top-level ## Proposals is read in order, and ends at the next ## heading`.
- Roles nested: `PASS  gate: a ### Roles nested under another heading is read: a review below its line is warned about` (it greps `warning: review ran at tier 2, effort 2; the spec asks for tier 2, effort 1`).
- Symptom gone: in a throwaway repo (JIG_CONFIG/XDG_CONFIG_HOME set), with c075cc0's bug-empty-proposal.md and 7f264f4's bug-metarepo-roadmap-cites.md as waiting specs, the fixed `jig consolidate` printed `group 1: 2 specs, proposed as one job … bug-empty-proposal and bug-metarepo-roadmap-cites share: plugin/templates/jig/jig.py, plugin/templates/jig/RULES.md, tests/smoke.sh`. Trunk's installed `.jig/jig.py` printed `no waiting specs overlap: each can open as its own job`.
- `grep -n '_template' plugin/skills/bug/SKILL.md` → line 53, "The spec takes the template's sections (.jig/specs/_template.md, as /jig:spec finds it), each a".
- `jig queue -- .jig/scripts/check.sh` → rc=0. `jig queue -- bash tests/smoke.sh consolidate workflow` at fb848c3 → rc=0, 65 PASS, 0 FAIL. The full output is in the hubnode's notes folder as bug-nested-touches-smoke-2.out.

## Review
- review-work of d3c6c7a, blocking 0:
  - should-fix: a top-level section also ended at a `# ` line, so a fenced shell comment cut Touches short. Fixed in fb848c3: the end pattern is `^#{2,N} `, and a smoke case covers it.
  - optional: the only `## Proposals` case had been converted to the nested shape. Taken: a top-level case was added.
  - optional: first match wins across levels, so an earlier nested `### Touches` would shadow a later `## Touches`. Deferred: DEFERRED.md row.
- review-change of fb848c3, blocking 0:
  - optional: the `spec_section` docstring doesn't say the end stops at `##`. Deferred: DEFERRED.md row.
  - optional: a nested `### Touches` reads past a second `# ` heading. Deferred: DEFERRED.md row.

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because jig.py is the product's checker, and its rules are documented in plugin/templates/jig/RULES.md. This job updated that file's Touches lines.

## Shared files changed
- `plugin/templates/jig/jig.py`: the readers live there.
- `plugin/skills/bug/SKILL.md`: step 5 is where nested specs came from.
- `plugin/templates/jig/RULES.md`: it described Touches as `## Touches` only.
- `tests/smoke.sh`: the new cases are in sec_consolidate and sec_workflow.

## Test by hand
- None needed. All of it is exercised in smoke. To see it yourself: put a spec that nests `### Touches` under `## 5. Spec` next to one with `## Touches` naming the same path, and run `jig consolidate`.

## Left
- Nothing. This hands off the whole spec.
