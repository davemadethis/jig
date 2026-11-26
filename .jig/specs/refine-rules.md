# refine-rules: tighten the rules files still over 200 lines, changing no rule

Source: Dave (owner), 2026-11-25, in jig's hubnode session, on layout-and-formats part 5's rules split: the spec asked each rules file refined toward 200 lines, and the split moved the text as it stood, leaving three over. Asked whether to refine now or defer, the owner chose "Defer to its own spec".

## Intent
Each `plugin/templates/jig/rules/rules-<set>.md` that layout-and-formats left over 200 lines is
tightened toward 200, and no rule in it changes meaning. A file that must stay over says why in
one line at its top.

## Done when
- [ ] `rules-docs.md` (405 lines at the split), `rules-roadmap.md` (297) and
  `rules-workflow.md` (249) are each 200 lines or under, or carry a one-line reason for staying
  over (`wc -l`).
- [ ] No rule is added, dropped or changed in meaning. The handoff note lists, per file, each
  rule sentence before and after, and the review checks the list against the diff.
- [ ] Every citation of a moved or renamed section still resolves: the citations in jig.py's
  messages, the skills, the templates and `docs/`. `grep` finds no pointer to a heading that's
  gone.
- [ ] `jig survey` on a fresh repo reports no rules file over 200 lines without its reason.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` and the smoke sections that grep rules
  text (`rules`, `pointers`, `decisions`, `metarepo`, `pararepo`) pass.

## Out of scope
- Changing what any rule says. That's a spec of its own, on the owner's word.
- `rules-decisions.md`: layout-and-formats reports it at 272 lines as a file allowed over.

## Touches
- `plugin/templates/jig/rules/rules-docs.md`, `rules-roadmap.md`, `rules-workflow.md`
- citations of their sections: `plugin/templates/jig/jig.py` (messages), `plugin/skills/*/SKILL.md`,
  `plugin/templates/`, `docs/`
- `tests/smoke.sh` (greps of rules text)

## Alternatives considered
- Refine inside layout-and-formats. Rejected by the owner: a prose rewrite gets its own review,
  where no rule changing meaning is the whole check. [seen: the owner's choice, 2026-11-25]

## Decisions
- Waits until layout-and-formats merges, since that job writes these files.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
