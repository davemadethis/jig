# fixes-0.17.1: the fixes 0.17.1 ships

Source: Dave (owner), 2026-11-26, in jig's hubnode session, answering the process check of jig's own 0.17.0 upgrade, on `docs/glossary.md` being out of the one form because its first heading is `# Glossary`: "Note the glossary's first h1 *should* be \"Glossary\" and this is a gap in 0.17.0, we should fix it and push 0.17.1. Take the rebuild now with this exception, and write a spec of fixes for 0.17.1 (this will be its only entry for now)"

Source: Dave (owner), 2026-11-26, in jig's hubnode session, after `jig open fixes-0.17.1` ignored a `Kept separate from jig-0.17.0-upgrade:` line, on the hubnode's explanation that `Path(name).stem` cuts a bare dotted name at its last dot: "why does it drop it, should we fix that too?", then "yep add it"

Kept separate from .jig/specs/jig-0.17.0-upgrade.md: 0.17.1 ships first, and the upgrade then runs on it (owner, 2026-11-26: "make that one fix, release 0.17.1, then I'll run jig update here").

## Intent
Each fix 0.17.1 ships is a labelled group below: the glossary's title, and a spec named with
dots matching itself wherever a spec names another.

## Done when
From the glossary's title:
- [ ] The one form opens with a `# Glossary` heading, holding no term and no fields, then
  `# Basic terms`, then each product. `glossary_problems` reports a glossary whose first `#`
  heading isn't `Glossary` or whose second isn't `Basic terms`, and reports neither for one in
  that order (smoke).
- [ ] `jig init` seeds the glossary with `# Glossary` first; `jig glossary add` and the merge's
  re-sort keep `# Glossary` first and sort nothing above it or into it (smoke).
- [ ] `jig update --apply` adds a `# Glossary` heading at the top of a glossary in the 0.17.0 form
  (first heading `# Basic terms`), changing no other line, and names it (smoke).
- [ ] A glossary whose first heading is already `# Glossary` and is otherwise in the form commits
  with no glossary problem, jig's own `docs/glossary.md` among them (smoke, and the hook on this
  repo's next commit to it).
- [ ] `rules-docs.md` (Documentation, the glossary's form), the update skill's glossary
  paragraph, `docs/records.md` and `docs/commands.md` describe the form with `# Glossary` first.
- [ ] `.jig/decisions.md` Unreleased has a Changed line for the title, and a Breaking line only
  if a 0.17.0-form glossary would be refused before `jig update --apply` adds the heading.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` and the smoke sections that cover the
  glossary pass.

From a spec named with dots:
- [ ] One helper turns a spec's path, file name or bare name into one key, dropping only its
  folder and a trailing `.md`: `jig-0.17.0-upgrade`, `jig-0.17.0-upgrade.md` and
  `.jig/specs/jig-0.17.0-upgrade.md` give one key. `kept_separate`, `built_after` and rig's
  overlap check use it, and no other spec-name match uses `Path(...).stem` (grep).
- [ ] In a throwaway repo, two specs named with dots whose Touches overlap: a `Kept separate from
  <bare dotted name>: <reason>` line lets `jig open` go ahead, and `jig consolidate` and rig list
  no group (smoke).
- [ ] A spec whose `Build after` names a bare dotted spec waits on that spec, and is free once it
  merges (smoke).
- [ ] `.jig/decisions.md` Unreleased has a Fixed line.
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` and the smoke sections that cover
  consolidate, `Build after` and rig pass.

## Out of scope
- Any other change to the glossary's form.
- Renaming the specs or branches jig builds from a spec's name (`spec.stem` for a file jig
  wrote itself, always ending in `.md`).

## Touches
- `plugin/templates/jig/jig.py` (`glossary_problems`, `glossary_seed`, the glossary insertion
  and re-sort, the update step; `kept_separate`, `built_after`, rig's overlap check)
- `plugin/templates/jig/rules/rules-docs.md`, `plugin/skills/update/SKILL.md`
- `plugin/templates/jig/templates/glossary-term.md`, `glossary-product.md` (if they show the file's top)
- `docs/records.md`, `docs/commands.md`
- `tests/smoke.sh`
- `.jig/decisions.md`

## Alternatives considered
- Leave `# Basic terms` first and record jig's own glossary as an exception: rejected by the
  owner: "the glossary's first h1 *should* be \"Glossary\" and this is a gap in 0.17.0".
  [seen: the owner's words above]
- `# Glossary` as a title with the rest one level down (`## Basic terms`, `##` products):
  rejected, since it would change every product, feature and term's level in every repo. [assumed]
- Write spec names by path in Kept and Build after lines, as a rule: rejected, because the rules
  promise a path, a file name and a bare name are one spec, and the bare form is what people
  write [seen: `kept_separate`'s docstring, and the existing Kept lines on trunk].

## Decisions
- Interpreted: "the glossary's first h1 should be Glossary" means a `# Glossary` title heading
  above `# Basic terms`, with every other heading at its 0.17.0 level.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
