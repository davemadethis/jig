# bug-nested-touches: a spec whose Touches sits under another heading overlaps nothing

Source: the hubnode, 2026-11-20, on the owner's word ("the jig:bug for the issue you found"): a bug role wrote `.jig/specs/bug-empty-proposal.md` with its sections one level down, under `## 5. Spec` (`### Change`, `### Done when`, `### Touches`, …). `jig rig --json` listed it with `"touches": []`, and `jig consolidate` and rig both missed its overlap with two other specs on `jig.py`, `RULES.md` and `tests/smoke.sh`. Raising the headings to `## ` (69a7330) made rig group them.

Kept separate from cross-repo-roadmap: the owner, 2026-11-20: "Hold on the cross-repo roadmap until we discuss it."

## Intent
A spec's Touches, Proposals and Roles are read wherever the spec puts them: as a `## ` section, or nested one level or more under another heading. An overlap is never missed because of a heading level. The bug skill tells the role to write the template's sections at `## `, so new specs stop nesting.

## Why
- Q: Why did consolidate and rig miss bug-empty-proposal's overlap? A: `touches_spans` (jig.py:1287) matches only `^## Touches`; the spec had `### Touches`, so it read no paths.
- Q: Why was Touches at `###`? A: /jig:bug's steps are `## 1. Why` … `## 5. Write the spec`, and it says to write the run to the spec. Agents copy that, nesting the spec under `## 5. Spec`.
- Q: Why did nothing say so? A: Each section reader is its own strict `^## ` regex, and an unmatched one returns nothing. No check looks at heading levels, so the miss is silent. Root.

## Givens
- [seen] Reproduced in a throwaway repo (scratch, `JIG_CONFIG`/`XDG_CONFIG_HOME` set): spec `a` with `## Touches` `lib/a.py`; spec `b` with `## 5. Spec` / `### Touches` `lib/a.py`. Committed with no complaint. `jig consolidate`: "no waiting specs overlap". `jig rig --json`: `('b', [])`.
- [seen] Same repo, `b`'s `### ` raised to `## `: `jig consolidate` prints "group 1: 2 specs … a and b share: lib/a.py".
- [seen] The shape is systematic. Before 37dca17 closed them, 12 of 55 `bug-*` specs (and 4 of 66 others) had `### Touches`. On trunk today, bug-feedback-menu, bug-hook-modes, bug-r6-take and bug-r7-literal nest it under `## 5. Spec`. None of those four is waiting: `jig rig --json` on trunk lists only bug-empty-proposal, bug-metarepo-roadmap-cites and cross-repo-roadmap.
- [seen] Each nested spec's top-level headings are the bug skill's own steps (`## 1. Why`, `## 2. Givens`, `## 3. One layer up`, `## 4. …`, `## 5. Spec`). `plugin/skills/bug/SKILL.md` step 5 never names the spec template or its heading level. It does say "Fill `## Roles`", and bug-empty-proposal still wrote `### Roles`.
- [seen] `/jig:spec` step 2 copies `_template.md`, whose sections are all `## `; the bug skill never points to it.
- [seen] The feedback report behind bug-empty-proposal isn't on trunk (resolved out of `.jig/staging/`). The 12 earlier nested bug specs came from other reports, so the shape comes from the skill, not one report.
- [seen] Spec-section readers in `plugin/templates/jig/jig.py`, each a separate `^## ` regex: `touches_spans` (1290: consolidate, rig, `jig open`'s uncovered-Touches warning, open jobs' Touches), `proposal_branches` (1446: `jig open` takes in a consolidated spec's proposals), `review_shortfall` (3197: the gate's "review ran below the spec's Roles" warning; a nested `### Roles` gives `sec = None` and no warning), `fill_roles` (9329: staging resolve).
- [seen] Readers that already ignore heading level, because they read a line: `bug_for` (`Bug-for:`), `kept_separate` (`Kept separate from`), `built_after` (`Build after`), `spec_scopes` (`Scope:`). Done when, Out of scope, Intent and Alternatives considered have no jig.py reader; only roles read them, and an agent reads a nested section fine.
- [seen] Nothing at commit checks a spec's section headings. The commit hook's only spec check is `roadmap_rules`' `Scope:` line.
- [assumed] No adopting repo depends on a `## Touches` section ending only at the next `## `, so ending it at a heading of its level or higher changes nothing for a top-level section. A `### Sub` inside `## Touches` stays inside it.

## One layer up
- Sibling paths: all four section readers above share the bug. `touches_spans` is where it costs: an overlap missed means two jobs edit the same files and collide at merge. `review_shortfall` loses a gate warning. `proposal_branches` would open a job without its proposals. All fail silently.
- What's different about the line readers: they match a line anywhere, so they never depended on heading level. Section readers can't do that, since a section is the lines under a heading.
- An existing pattern: `bug_for` (jig.py:1327) is "the one reader of the line", so every caller agrees. The fix gives sections the same: one `spec_section(text, name)` that the readers call.

## Correction
A correction. The reader is changed to read the shape writers actually produce, and the skill is changed to stop producing it.
- `spec_section(text, *names)` in jig.py: the body under the first heading at level 2 or deeper (`##`, `###`, …) whose text is one of the names. The body runs to the next heading at that level or higher, or the end. `touches_spans`, `proposal_branches` and `review_shortfall` call it, replacing their own regexes.
- `plugin/skills/bug/SKILL.md` step 5: the spec takes the template's sections (`_template.md`, as `/jig:spec` finds it), each a `## ` heading. Steps 1–4 go above them as `## Why`, `## Givens`, `## One layer up`, `## Correction`, never with a spec nested under a step.
- `RULES.md` lines 58 and 65 say Touches is read at any heading level.

## Done when
- [ ] Fix fires (`sec_consolidate`): spec `b` with `## 5. Spec` and a nested `### Touches` naming `lib/a.py`, next to spec `a` with `## Touches` `lib/a.py`. `jig consolidate` prints `a and b share: lib/a.py`, and `jig rig --json` lists `b` with `lib/a.py` in its touches.
- [ ] A nested section ends where it should (`sec_consolidate`): a path under `### Out of scope` after `### Touches` is not in `b`'s touches. A `### Notes` heading inside a top-level `## Touches` still counts the paths below it.
- [ ] Proposals nested (`sec_consolidate`): the existing consolidated-spec case, with `### Proposals` under `## Spec`, still has `jig open` take in both proposals in order.
- [ ] Roles nested (`sec_workflow`): a spec whose `review:` line is under `### Roles` gets the gate's `warning: review ran at tier …; the spec asks for …`, as the `## Roles` case does.
- [ ] Symptom gone: in a throwaway repo with the fixed `jig.py`, c075cc0's `bug-empty-proposal.md` (nested) and 7f264f4's `bug-metarepo-roadmap-cites.md` as waiting specs. `jig consolidate` lists them as one group sharing `plugin/templates/jig/jig.py, plugin/templates/jig/RULES.md, tests/smoke.sh`. Output shown in the handoff.
- [ ] `plugin/skills/bug/SKILL.md` step 5 names the template and `## ` headings for the spec's sections (`grep -n '_template' plugin/skills/bug/SKILL.md` prints the line).
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes, and `python3 .jig/jig.py queue -- bash tests/smoke.sh consolidate workflow` passes. Output shown.

## Out of scope
- `fill_roles` (staging resolve) keeps reading only `## Roles`. A staged spec with a nested `### Roles` would get a second `## Roles` appended. Staged specs come from `/jig:stage`, which writes the template's shape, and nobody has seen this happen.
- A spec with no Touches section at all still overlaps nothing. That's a missing section, not a misread one, and the template carries `## Touches`. A warning for it is a separate call.
- A section under another name ("Files touched") isn't read. The names stay the template's.
- Headings inside fenced code are matched as they are today: the old readers didn't skip fences either.
- The four closed specs on trunk that nest Touches (bug-feedback-menu, bug-hook-modes, bug-r6-take, bug-r7-literal) are left as they are. None is waiting, and the fix makes them readable anyway.
- Handoff notes' `## Fold-in` readers: jig writes those notes itself, at `## `.

## Touches
- `plugin/templates/jig/jig.py` — `spec_section`; `touches_spans`, `proposal_branches`, `review_shortfall` call it
- `plugin/skills/bug/SKILL.md` — step 5: the template's sections at `## `
- `plugin/templates/jig/RULES.md` — the Touches lines (58, 65) say any heading level
- `tests/smoke.sh` — `sec_consolidate`, `sec_workflow` cases above

## Alternatives considered
- Skill text only (step 5 says `## ` headings) — rejected because the skill already says "Fill `## Roles`" and bug-empty-proposal wrote `### Roles` anyway. Agent compliance can't be the only guard against a silent miss. This reason is [seen].
- Commit-hook refusal of a spec whose Touches isn't at `## ` — rejected because it adds a new refusal, and a message, for a shape jig can just read. It stops the bug role's commit over a heading level and still leaves the four readers strict. This reason is [assumed]: it's a cost judgment, nothing built.
- A `jig consolidate`/rig warning for a waiting spec whose Touches reads empty — rejected because a warning still leaves the group unformed until someone acts. Consolidate's output is what rig and `jig open`'s refusal use, so the miss would reach `jig open` anyway. This reason is [seen] from the repro: open is refused only for a group consolidate forms.
- Loosening each regex in place (`^#{2,} Touches` four times) — rejected because four copies each need the same end-of-section rule, and they drift. jig already keeps one reader for a shared shape (`bug_for`, "the one reader of the line"). This reason is [seen].
- Rewriting the nested specs on trunk instead — rejected because it fixes today's files, not the next bug role's. This reason is [seen]: 12 nested bug specs in history.

## Decisions
- A nested section ends at the next heading of its own level or higher, so `### Touches` stops at the next `### `. A top-level `## Touches` keeps everything under it to the next `## `, sub-headings included, as today.
- Level 2 and deeper only, never `# `: a spec's `# ` line is its title.
- The first matching heading wins, as the old `re.search` did.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
