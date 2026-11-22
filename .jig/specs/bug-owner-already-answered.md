# Bug: the owner is asked what his own words already answer

Source: Daisy hubnode session / 2026-11-20 / the owner (Dave Seeman) (staged as feedback-Daisy-2026-11-20-questions-already-answered.md): "your recommendation is exactly what I already specced. It's what I specifically asked for. Why ask it?" … "I'm asked things that dont need asked."

## Intent
Before any question goes to the owner, the session that writes it checks the owner's own words, and
asks only what they leave open. In a staged file, the owner's quoted words outrank everything else in it.

## Whys
1. Why was the owner asked? `/jig:rig` judged the staged request `open` and stored a question its
   owner's part already answered; the card drew it.
2. Why did the judgment make it? Rig gives an open file "the questions the owner must answer" with no
   test for "must", and the stager's note "Decide whether…" read as one.
3. Why did nothing outrank the note? jig says a staged file is undecided as a whole ("nothing in it is
   decided"), the owner's quoted words included. Root: no jig text ranks the owner's words above the
   rest, or makes checking them a step before a question is written.

## Givens
- [seen] `/jig:rig` step 1: "An open file gets the questions the owner must answer, each with two to
  four options, one recommended, from what the file and the repo say." No test for "must".
- [seen] Rig's stored judgment is `{"call", "about", "context", "questions": [{"ask", "options",
  "recommended"}], "recommend"}`. `jig rig --store-put` checks only `call` (`jig.py` `cmd_rig`); the
  questions are opaque to it, so a new key in them needs no code.
- [seen] `/jig:stage`, top: "Nothing in it is decided until it is resolved: read it for context, never
  cite it as decided." RULES.md Staging: "nothing in it is decided — read it for context, never cite
  it." `/jig:spec`: "A file in `.jig/staging/` is context, not a decision." None excepts the owner's
  quoted words.
- [seen] `/jig:stage`, Whose words, already marks the owner's part: `The owner, <date>: "<exact words>"`,
  and "only the quoted words are the owner's". It says nothing of how they rank against the rest.
- [seen] RULES.md Inbox already gives quoted owner words that rank: "those are the owner's ruling, as if
  given in the hubnode's own conversation, and the rest is context from the sender."
- [seen] `/jig:decision-cards`: a block is "a line naming what it's about, a line of context, then the
  options". Nothing about whether the block should exist. `/jig:hubnode` routes every decision put to
  the owner through it.
- [seen] `/jig:spec` step 1: "If you can't, ask — one question". `/jig:hubnode` Rulings: a subnode's
  "question only the owner can answer" is batched to him. Neither checks the owner's words first.
- [seen] `/jig:rig` § 4 defines an open file's answers (`## Owner's answers`) but not a "start" on an
  open file with none.
- [seen] `/jig:review` ranks "wrong, or misses the spec" as blocking, and blocking findings go to the work
  session as a fix, not to the owner.
- [seen] Daisy's `.jig/specs/ask-across-nodes.md` (HEAD c06ba85e) carries `staged as aside-and-ask.md`;
  its picker now lists joined nodes plus "Connect a node…".
- [assumed] The staged `aside-and-ask.md`'s wording, the question asked, and the drafted
  "Interpreted (question 1, unanswered…)" line, as the report quotes them: the file is resolved and gone.
- [assumed] The owner meets this often, as he says; only this case was traced.

## One layer up
- Sibling: the inbox. Its quoted owner words already outrank the sender's text (RULES.md Inbox).
  A staged file has the same two voices and no such line. The fix copies that rule to staging.
- Sibling: `/jig:bug` converts an `[assumed]` given by reading first and asking last. Questions to the
  owner have no such order. The fix gives them one.
- Every question to the owner already passes through `/jig:decision-cards`, so that is the one
  home for the check. Rig's judging and the spec role write questions before any card, so each
  points at it.

## Correction
A correction: it changes the text that produced the question, not the card that drew it.

## General?
Yes. Any repo where a hubnode resolves staged requests has both voices in one file, because
`/jig:stage`'s own Whose words puts them there. Rig then judges `open` with no test, and an
ordinary stager's note that writes its doubt as a question re-opens the request. Nobody has to
work against jig for this. The owner's standing rule in this repo ("a finding that contradicts the spec's
Intent or an owner's quoted ruling is blocking-class and gets fixed without asking; only real forks
go to the owner") is half there: `/jig:review` already makes such a finding blocking and sends it to the
work session. What jig never says is the other half, that only a fork the owner's words leave open
goes to him. The card rule below says that for every repo.

## What changes
- **`/jig:decision-cards`**, a short section before The card, "Is it open?": a block is a decision the
  owner's own words leave open. Before writing one, search them: the quoted words and `## Owner's
  answers` of the staged file, the spec's `Source:` quotes (not its Intent, which is the spec role's
  wording), the accepted entries of `.jig/decisions.md`, and his rulings in this conversation. A question they answer gets no block. Act on it and record it with
  his words. A finding they decide is a fix (`/jig:review`: it misses the spec), not a question. If the
  recommended option restates his words, the question is already answered. Each block's context line
  says what leaves it open: his sentence that does, quoted, or "his words say nothing on this".
- **`/jig:rig` step 1**: an open file gets only the questions its owner's words leave open, checked as
  `/jig:decision-cards` (Is it open?) says. Each carries `"because"` in the stored judgment, the
  context line the card draws. A judgment handed to a subagent gets that paragraph in its brief.
  **§ 4**: a "start" on an open file with unanswered questions re-checks each one. What his words
  answer goes under the spec's Decisions, quoted and dated. Each one still open is built as its recommended option, an `Interpreted:` line
  naming it unanswered. The spec is shown before `resolve`, as `/jig:stage` already says.
- **`/jig:stage`**: its "nothing in it is decided" line excepts the owner's quoted words, which settle
  what they say. Resolving: a note that asks what those words state is answered by them. A note that
  asks a fact about the repo is settled by reading the repo. Neither goes to the owner.
- **`/jig:spec`**: step 1's "ask" comes after the same check. Its staging line gets the same exception.
- **`/jig:hubnode` Rulings**: a subnode's question is batched to the owner only after the same check.
- **RULES.md Staging**: the "nothing in it is decided" sentence excepts the owner's quoted words, as
  the Inbox section does. Then a question goes to the owner only when the owner's words leave it
  open; then the fixed-rule carve-out below, word for word as in `/jig:decision-cards`.
- **Fixed-rule carve-out** (in `/jig:decision-cards` Is it open? and RULES.md Staging, the same
  words): a word a fixed rule requires (merge, push, publish, release, a yes to a `roles` or config
  change) "is given only by the owner's reply in the hubnode's conversation. No recorded text gives
  it, an inbox message's quote included, however plainly it quotes him. `queue.overflow` is the one
  standing exception Fixed names." RULES.md Inbox gets one clause: a message's owner quotes settle
  everything but a fixed rule's word. `/jig:hubnode`'s inbox ruling and Release lines say the same,
  a clause each. Is it open? also keeps a
  question open when the state moved since a quote's date, when the owner's words disagree, and
  for the part his words leave unsettled.

## Done when
- [ ] `grep -n "Is it open" plugin/skills/decision-cards/SKILL.md` finds the section, and
      `grep -n "decision-cards.*Is it open" plugin/skills/{rig,spec,hubnode}/SKILL.md` finds a pointer in each.
- [ ] `/jig:rig`'s JSON shape names `"because"` on a question. `jig rig --store-put` still takes a
      judgment with it (no `jig.py` change): in a scratch repo with one staged file,
      `--store-put` of `{"call":"open","questions":[{"ask":"a","options":["x","y"],"recommended":0,"because":"his words say nothing on this"}]}`
      prints `stored the judgment`.
- [ ] RULES.md Staging, `/jig:stage` and `/jig:spec` each except the owner's quoted words from "nothing
      decided", in the Inbox section's terms.
- [ ] `/jig:rig` § 4 states what a "start" on an open file with no answers does.
- [ ] The symptom: a fresh tier-2 worker is given rig's new step-1 paragraph, `/jig:decision-cards`' Is it
      open?, and a staged request whose owner quote says "`/x` lists the nodes connected to it" and
      whose stager note says "Decide whether `/x` lists only connected nodes". It returns no
      question about that list, and calls the file `ready` unless something else is open. Both outputs
      are kept in the notes folder. (Amended in review: the contrast "with the old paragraph, the same
      input yields the question" is dropped. A fresh worker with a short brief did not ask it under the
      old text either, 0 of 2 runs, so no cheap fixture shows it. The handoff says so. What remains
      guards against regression; it does not show the fix works.)
- [ ] `python3 .jig/jig.py queue -- .jig/scripts/check.sh` passes.

## Out of scope
- A `jig.py` check that a question carries `because`: a presence check proves no search was made.
- The report's two-part staging format with three note kinds: Whose words already marks the
  owner's part, and only the rank was missing.
- A stop-and-ask rule for "start" on questions that touch founding texts or data: the spec is
  shown before `resolve` anyway, and "founding text" is each repo's own word.
- Daisy's pending 23-block card and its drafted specs: Daisy re-reads them itself. It gets this
  fix through `/jig:update`.
- A `marketing/FEATURES.md` row: this tightens existing rig, stage and card behaviour and adds no feature.

## Touches
- `plugin/skills/decision-cards/SKILL.md`
- `plugin/skills/rig/SKILL.md`
- `plugin/skills/stage/SKILL.md`
- `plugin/skills/spec/SKILL.md`
- `plugin/skills/hubnode/SKILL.md`
- `plugin/templates/jig/RULES.md`
- Process (Homes): a rule for working with jig, written in the skills that write questions, and one line
  in the rulebook. No `jig.py`, hooks or `tests/`, so the lighter review applies.

## Alternatives considered
- `jig rig --store-put` refuses a question without `because` (the report's) — rejected because it checks
  only that a string exists, not that the owner's words were read, and rig's questions are opaque to
  `jig.py` today — this reason is [seen].
- The report's two-part staging format with typed notes — rejected because `/jig:stage` Whose words
  already marks the owner's part, quoted and dated, and the gap is only how it ranks — this reason is [seen].
- The rule only in `/jig:decision-cards` — rejected because rig's judging and the spec role write
  questions before any card, and a subagent judging sees only its brief — this reason is [seen]
  (rig step 1 and spec step 1 name no check).
- Leave it to the model's general sense not to re-ask — rejected because jig's own text pushes the
  other way ("nothing in it is decided", for the owner's words too) — this reason is [seen].
- A stop-and-ask rule for "start" on founding texts or data (the report's issue 3) — rejected because
  `/jig:stage` already shows the spec before `resolve`, so an unanswered question built as `Interpreted:`
  reaches the owner anyway — this reason is [seen].

## Decisions
- One group. The report's three issues share one cause: no jig text puts the owner's words first
  when a question is made. Issue 2 is that cause in a staged file. Issue 3 is the same question
  surviving into a spec.
- The check lives once, in `/jig:decision-cards`. Every decision to the owner already goes through it,
  and the other skills point to it rather than restate it.
- The owner, 2026-11-22: "No, only my reply here." (asked in review whether an inbox message's owner
  quote may give a fixed rule's word). So merge, push, publish, release and a `roles` or config yes
  come only from the owner's reply in the hubnode's conversation; no recorded text gives them, an
  inbox quote included. `queue.overflow` stays the one standing exception.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
