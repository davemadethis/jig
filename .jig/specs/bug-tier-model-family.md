Source: orbyt-supply hubnode session / 2026-11-24 / Dave (owner) (staged as feedback-orbyt-supply-2026-11-24-tier-lookup-by-model-family.md): "tiers refer to the ranking of model at any model version. opus 5 and 5.5 are both tier 2. We dont need to have a 5-5 or a 5 key to know that, that's overcomplicating it." A hubnode on `claude-opus-5` found no exact `tiers.json` entry, passed tier 3, and capped every tier-2 role; the subnode mismatch check compares the model string the same way.

# bug-tier-model-family: a model's tier is read from its exact id, not its family

## Intent
A tier is a model family at any version. `tiers.json` keeps its shape: `model[tier]` is the id
a session is started or raised to. Reading it backwards (which tier is this session on?) and
comparing a subnode's `running` line with its brief both compare families: the id with its
version dropped. Only a family the map doesn't name at all is stale, and only a different
family is a mismatch.

## 1. Why
- Q: Why did the hubnode report tier 3 on `claude-opus-5`? A: `tiers.json` maps tier 2 to `claude-opus-5-5`; step 6 matched the id exactly and missed.
- Q: Why did a miss mean tier 3 and a cap? A: hubnode step 6: a model `tiers.json` doesn't name is stale, pass tier 3, raise no model above tier 3's until the owner answers.
- Q: Why exact? A: The map is written tier → id for launching; no skill says how to read it id → tier or compare two ids, so the plain string compare is all there is. Root.

## 2. Givens (this checkout, trunk fcd1b92)
- [seen] `plugin/tiers.json` `model`: `1` `claude-fable-5-2`, `2` `claude-opus-5-5`, `3`
  `claude-sonnet-5-5`, `5` `claude-haiku-5-5`. No `claude-opus-5`. Each value's name before
  its trailing number parts is distinct (`claude-fable`, `claude-opus`, `claude-sonnet`,
  `claude-haiku`).
- [seen] `plugin/skills/hubnode/SKILL.md:53-62` (step 6), unchanged since the reporter's
  version: "A model `tiers.json` doesn't name: say so, `tiers.json` is stale, pass tier 3, say
  the floor line rests on that guess, and start nothing above tier 3's model (no model raise)
  until the owner answers."
- [seen] `hubnode/SKILL.md:110-111`: "With a model `tiers.json` doesn't name, raise no model
  until the owner answers (step 6)." `:108-110`: the brief goes "once the session's line names
  the role's model".
- [seen] `hubnode/SKILL.md:94-99`: "only a model that differs is [a mismatch]. A mismatch stops
  a raised session", and the prompt line "if your own model differs from this line, reply with
  only your `running` line and stop".
- [seen] The same line opens each role's **Brief**: `spec/SKILL.md:19`, `bug/SKILL.md:22`,
  `review/SKILL.md:17`, `work/SKILL.md:16`, `check/SKILL.md:18`; `review/SKILL.md:33-35`
  repeats it for the review subagent ("At a mismatch in model, retry once").
  `subnode/SKILL.md:14-17`: "If the kickoff named a different model, say so and stop".
- [seen] Forward-only readers, unaffected: `review/SKILL.md:27`, `rigger/SKILL.md:88`,
  `stage/SKILL.md:69`, `hubnode/SKILL.md:80-82` (`model[tier]`, `effort[effort]`).
- [seen] `plugin/templates/jig/jig.py` holds no model id: its only `tiers` mentions are
  comments (`:94` "jig can't see a session's model", `:409` `--from TIER,EFFORT` "as numbers
  from the tool's tiers map"). `jig roles --from` takes numbers; the lookup is skill text.
- [seen] `RULES.md:726-730`: "Which model and level a number means is the tool's business, not
  `.jig/`'s: the plugin maps them in `plugin/tiers.json`." So RULES needs no change.
- [seen] `jig roles` here: spec 2,2; bug 2,1; work 2,3; review 2,2; check 3,4. So on the
  reporter's reading (tier 3) every role but check was capped.
- [seen] `tests/smoke.sh:8061` requires `stage/SKILL.md` to name no `opus|sonnet|haiku`: skill
  text defines tiers by number and `tiers.json`, not by family name. The fix keeps that.
- [seen] The reporter's session ran `claude-opus-5` (its system prompt) and the owner ruled it
  tier 2. Taken from the report; the rule as written misreads it either way.
- [assumed] The host can clamp a new session to a different point version of the starter's
  family. Not observed here; not converted. The fix doesn't depend on it: a check stricter than
  the owner's rule is the defect whether or not the host ever does this.

## 3. One layer up
- Sibling: the effort direction of the same map. Reading `high` → 2 works, because effort
  values are a closed set of names with no version. The structural difference is exactly that.
- Sibling: the mismatch check (Issue 2 of the report) is the same exact compare, in six brief
  lines, the hubnode's paragraph and the subnode's check-in. Same cause, same fix.
- Existing pattern: jig compares a normalized form rather than the raw string elsewhere (repo
  names with case ignored, headings with code marks dropped). Compare families, not ids.

## 4. Correction
Change the rule that reads the map, at every place that reads it backwards or compares ids. A
workaround (add `claude-opus-5` to `tiers.json`) would fix this one session and go stale at the
next release.

General? Any repo's hubnode runs on whatever the owner opened it on. The day a tool ships a
point version jig's `tiers.json` doesn't list, or an owner stays on the previous one, every repo
hits this: roles capped at tier 3 and correctly configured subnodes stopped, with no one working
against jig. Worth keeping.

## Change
1. `hubnode/SKILL.md`, **Assigning a step** (`:80`): one sentence defining a model's family: its
   id with the version dropped (the trailing number parts and any bracketed or date suffix), and
   that a tier is a family at any version: the tier whose `model` value has the session's family.
   An exact id match wins; a family two tiers share maps to the higher number (the lesser tier),
   and the floor line says it rests on that guess. No family is named in the text.
2. `hubnode/SKILL.md` step 6: map the model to a tier by family. The stale branch applies only to
   a family `tiers.json` doesn't name, and is otherwise unchanged (pass tier 3, flag the guess, no
   model raise).
3. `hubnode/SKILL.md:94-99` and `:108-111`: a mismatch is a different family; the brief goes once
   the session's line names the role's model's family; "a model `tiers.json` doesn't name" becomes
   "a family". The quoted prompt line reads: "if your own model is another family than this
   line's (the id with its version dropped), reply with only your `running` line and stop".
4. The same prompt line in the **Brief** of `spec`, `bug`, `review`, `work` and `check`, and
   `review/SKILL.md:33-35` (its quote and "a mismatch in model" → in family).
5. `subnode/SKILL.md:16`: "If the kickoff named a different model" → a different family. The
   `running` line still reports the exact id (it is what `--ran` records).
6. `.jig/decisions.md`: one `### Fixed` line under `## Unreleased`.

`tiers.json`, `jig.py` and `RULES.md` are unchanged.

## Done when
- `grep -c claude- plugin/tiers.json` is 4, as before: no per-version keys.
- `grep -rn 'own model differs from this line\|a model .tiers.json. doesn.t name\|only a model that differs\|named a different model' plugin/skills/`
  prints nothing; `grep -rl 'another family than this line' plugin/skills/` lists hubnode, spec,
  bug, review, work and check (`family` alone won't do: hubnode already uses it for a metarepo's
  family), and `subnode/SKILL.md`'s Check in says a different family stops it.
- `grep -rniE 'opus|sonnet|haiku|fable' plugin/skills/` prints nothing, as today: the family
  rule is written without naming one.
- The fix fires: a hubnode session on a model id `tiers.json` doesn't list but whose family it
  does (one on `claude-opus-5` today) reports `tier 2` in step 6, runs
  `jig roles --from 2,<effort>`, and does not call `tiers.json` stale, pass tier 3 or flag the
  floor line as a guess.
- The symptom is gone: in that session `jig roles --from 2,2` prints "start with its settings"
  under spec, work and review and "start, then raise effort" under bug, and the hubnode raises
  no role to tier 3's model. A subnode briefed `running claude-opus-5-5` that replies
  `running claude-opus-5` (or the reverse) is briefed, not stopped; one that replies with
  another family (tier 3's model for a tier-2 role) is still stopped and reported to the owner.
- The old branch still fires where it should: a session whose family no `tiers.json` value has
  says `tiers.json` is stale, passes tier 3, flags the guess and raises no model.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes.

## Out of scope
- `tiers.json`'s shape (a `{family, launch}` value per tier). The forward readers work and the
  owner said the key stays.
- The `unknown` effort branch of step 6: effort names carry no version; it is sound.
- `HUBNODE_FLOOR` and the ranking in `jig.py`: they ranked correctly once given the right
  numbers.
- A smoke test of skill wording: this is skill text only (the lighter review tier); the greps in
  Done when are its evidence.

## Touches
- `plugin/skills/hubnode/SKILL.md` (step 6; Assigning a step)
- `plugin/skills/subnode/SKILL.md` (Check in)
- `plugin/skills/spec/SKILL.md`, `bug/SKILL.md`, `review/SKILL.md`, `work/SKILL.md`,
  `check/SKILL.md` (Brief; review's Dispatch)
- `.jig/decisions.md` (one `### Fixed` line)

## Alternatives considered
- Add `claude-opus-5` beside `claude-opus-5-5` in `tiers.json` (the workaround) — rejected
  because it needs an entry per version and goes stale at the next release, and the owner ruled
  the tier belongs to the family — this reason is [seen] (the owner's words in the report).
- Restructure each `model` value into a family and a launch id — rejected because the four
  forward readers already work and the owner said the key can stay; a schema change touches them
  for no gain — this reason is [seen] (`review:27`, `rigger:88`, `stage:69`, `hubnode:80`).
- Do the lookup in `jig.py` (`jig roles --from <model>`) — rejected because `jig.py` names no
  model by design ("jig can't see a session's model") and RULES puts the mapping in the plugin —
  this reason is [seen] (`jig.py:94`, `RULES.md:730`).
- Fix step 6 only and leave the mismatch check exact — rejected because the brief line would
  then stop the very subnode step 6 now starts without a raise, on a point version — this reason
  is [seen] (`hubnode:94-99` and the six brief lines).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
