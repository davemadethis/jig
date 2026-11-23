# ideas-log: open questions leave the decision log for an ideas log of their own

Source: Dave (owner), 2026-11-23, in jig's hubnode session, on cross-repo-roadmap shipping part of the design he agreed and deferring the rest without his yes: "end state was supposed to mean exactly that: everything including labels." This is R4 and R5 of that design.
Source: Dave (owner), 2026-11-19, fourth round of the scope-ownership design in maige-ecosystem's hubnode session (R4): "I think ideas should be their own log, labeled the same way scopes are. It's basically a list of things I need to research before they can be decided, scoped, built, and documented." Fifth round (R5), on the hubnode's reply "the decision log's Open entries move into the ideas log, so the log keeps only decisions": "Agreed on all of it."
Source: move-to-pararepo's Out of scope, deferred there: "Where Open questions should live (the report's ideas log)."

Kept separate from roadmap-labels: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from moving-in-command: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from phase-types: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from bug-deferred-scope: the owner, 2026-11-23: "start what you can in parallel"

## Intent
Every repo with a decision log keeps a second file, `.jig/ideas.md`. It holds the questions and
ideas still to be researched before they can be decided, scoped, built and documented. Each
idea carries the labels a scope carries. The decision log then holds only decisions: `## Open`
goes, and its entries move to the ideas log with their ids. Everything that cites or reads them
keeps working: citations, `jig decision`, peers, numbering, staging, the pin bump, and the
metarepo's move line. A spec that reads a page sees the ideas still open on it.

## Investigation

**Givens** (line numbers at trunk 06550ea)
- [seen] The owner's rounds, read in Maige-Eco's `.jig/staging/request-scope-ownership-from-maige-*.md`.
  - Round 3: open questions "are in decisions not roadmap right?"
  - Round 4: ideas get their own log, "labeled the same way scopes are". "If it's an idea its not in scope yet and it needs research."
  - Round 5 agrees that Open entries move there, "so the log keeps only decisions".
  - Rounds 12 and 13 already route held questions to it: "Hold Walytpass questions and Teleport questions including E-023 for the idea log when it gets here". He also dropped one: "drop it, no ideas log entry".
- [seen] cross-repo-roadmap's Out of scope deferred "Ideas log and open questions leaving the decision log (R4, R5)" to "later versions". move-to-pararepo deferred "Where Open questions should live".
- [seen] Open and Proposed entries live under `## Open` in `.jig/decisions.md` (`LOG`, jig.py:5833; `LOG_SEED`, :5848). M2 (`log_problems`, :5958) allows Open and Proposed statuses only there. `removed_entries` (:6024) lets them leave freely. R3 (:711–723) lets any job change lines in place only under `## Open`.
- [seen] These readers of the log's entries would each miss an idea if ideas moved to another file and nothing else changed:
  - `log_entries` (:5891), `cmd_decision` (:6471), `claims_of_id` (:3025) and `hold_chain`/`holds_now` (:6435)
  - `live_entries`/`touching`/`peer_logs` (:6669–6745). Peers include Open entries today.
  - `proposed_added` (:3246), the gate's "Proposed: it merges unruled" warning
  - merge's numbering and the trunk refusal of `D-?` (:6340), and `append_globs` (:2204)
  - `stage_pin_bumps` (:8619), `changes_report` (:8815) and `meta_citations` (:8860)
  - the move-line check (:6150–6235), which looks up a target id in the pararepo's `LOG` only
  - `cmd_merge_log` (:14285): open rows and ADR open/proposed/draft go under `## Open`
  - `jig init` (:876, `LOG_SEED`) and `project_sections` (:5544, "an open question → an ## Open entry")
- [seen] RULES.md names `## Open` as an open question's home at :87 (R3), :283 (Product and project), :1064, :1120–1123 and :1162–1170 (Decision log), :1213 and :1254 (`--merge-log`), :1297 (Staging), :1463 and :1492 (Metarepo and pararepos), :1513 (M2) and :1544. Skills say it in `stage`, `update`, `redocument` and `retro`. The kickoff text (jig.py:1267) says it too.
- [seen] Released entries are frozen and cite Open ids (move-to-pararepo's Givens: E-039, E-057 and E-094 cite moving ids). A pararepo cites a metarepo's Open id bare (Maige-Lite cites E-017 and E-044). So an idea must keep the id it has.
- [seen] A phase's `(after …)` is a line of its own in its note (RULES.md, Roadmap), because a block has no single line to end. That is the precedent for a block-level `(labels …)`.
- [seen] cross-repo-roadmap names a scope's labels as `(labels …)`, "checked against the metarepo glossary's folded terms". roadmap-labels, written in parallel today, builds that.
- [assumed] A checker too old to know `.jig/ideas.md` passes a commit that adds the file and empties `## Open`, because R3 and M2 let Open entries leave freely. So the fold takes one run, not the two the `## Up next` fold needed. To check during the build.

**One layer up**
- The `## Up next` fold (cross-repo-roadmap Part B) is the sibling: two homes become one, `jig update --apply` folds the old one with ids and text kept, and then the hook refuses the old heading. This spec does the same in the other direction, splitting one file into two homes. It reuses that shape: the update fold, then a refusal by line.
- The move line already gives a frozen id a forwarding address across repos. An idea keeps its id in the same repo, so it needs no address. It needs only the readers to look in two files.

## Change

Three parts, in build order. A and B hand off `--partial`, and C completes the spec. A and B
start now. C starts once roadmap-labels' Part A is on trunk (Decisions).

**Part A: the ideas log** (any repo)
1. **The file.** `.jig/ideas.md` opens with `# Ideas` and one line saying what it holds:
   questions and ideas to research before they can be decided, scoped, built and documented.
   Then come entries, one per idea, in the decision entry's form: `### <id> <title>`, a status
   line, a `Touches:` line, and the body (the question, what is known, how it might be answered).
   The status is `Open (YYYY-MM-DD).` or `Proposed (YYYY-MM-DD).`, the latter optionally ending
   `Supersedes <id>.`. The file has no sections and no releases, and an idea changes in place.
2. **Ids.** An idea's id is a decision id, from the same counter as the log. A branch writes
   `D-?<slug>`, `jig merge` numbers it in either file, and trunk refuses an unnumbered one in
   either file. Numbering starts above every id either file has ever named. One id names one
   thing across both files.
3. **Leaving.** An idea leaves in one of three ways:
   - **Decided:** the commit removes its block from `.jig/ideas.md` and adds it under the log's
     `## Unreleased`, with the same id and `Accepted (who, date).`.
   - **Dropped:** removed with no line, as a rejected entry is today. Git keeps it.
   - **Moved down (a metarepo):** removed with a move line under the log's `### Removed`, its
     target `<repo>/.jig/ideas.md § <id>`, or `<repo>/.jig/decisions.md § <id>` when it lands
     decided. This answers move-to-pararepo's "Where Open questions should live". A question
     lives in the ideas log of the repo that owns it.
4. **Checked** (M2, by the hook, whenever a commit touches either file):
   - each idea has a heading with no status, a status line, an accepted-free status (an
     `Accepted` idea is refused: "decided: move it to `.jig/decisions.md` `## Unreleased`"), and
     a `Touches:` line as an entry's is checked;
   - one block per id across both files;
   - on trunk, numbered ids only.
   R3 lets any job add an idea or change one in place. `.jig/ideas.md` is an append file
   (`append_globs`), like the log.
5. **Readers.** Every reader of an entry by id reads both files: `jig decision <id>` (printing
   "an idea in `.jig/ideas.md`"), `jig reading-list --claims`, `hold_chain`/`holds_now`, peers
   (`touching`, `peer_logs`, `jig decision --peers`, which show an idea marked as one), and the
   gate's Proposed warning (`proposed_added`). `jig reading-list <paths>` prints, after each
   page, the ideas whose `Touches:` names it, as it prints the roadmap's items not done. That
   way a spec sees what is still open research before it takes the page on.
6. **`jig init`** writes `.jig/ideas.md` beside the log. The log's seed loses `## Open`.

**Part B: Open entries move in** (any repo, then metarepo readers)
7. **The fold.** `jig update` lists a log that still has `## Open`. On the owner's yes,
   `jig update --apply` moves every entry under it into `.jig/ideas.md`, keeping ids and blocks
   byte for byte, and removes the heading. This runs on trunk, or in a metarepo in a job, as
   `--merge-log` does there, since the log is an entry file. After the fold, the hook refuses
   two things in the log, by line: an `## Open` heading, and an `Open` or `Proposed` status
   ("an idea goes in `.jig/ideas.md`"). A log that never had ideas folds to an empty
   `.jig/ideas.md`.
8. **Writers that used `## Open`.**
   - `jig staging resolve` lands an open or proposed staged entry in `.jig/ideas.md`, and an
     accepted one under `## Unreleased`, as now.
   - `--merge-log` writes open and proposed rows, and ADR open, proposed and draft records, into
     `.jig/ideas.md`.
   - `jig update --sweep` and `project_sections` name an open question's home as "an idea in
     `.jig/ideas.md`".
   - The kickoff says "a Proposed idea in `.jig/ideas.md`".
9. **A metarepo's ideas.** In a metarepo, `.jig/ideas.md` is an entry file always, as the log
   is, recorded by itself: M3 asks no change line for it. A pararepo cites a metarepo idea the
   way it cites an entry, read at the pin. `meta_citations`, `stage_pin_bumps`' `gone` set and
   `changes_report` count an id in either file as present. So an Open entry folded into ideas
   reads as neither removed nor moved, and an idea decided in place reads `(accepted)` as an
   entry does. The move-line check looks a target id up in the pararepo's `.jig/ideas.md` as
   well as its log.

**Part C: labels, and the list** (after roadmap-labels' Part A is on trunk)
10. **Labels.** An idea may carry a line of its own, `(labels <label>, …)`, anywhere in its
    block after the status line. An idea is labelled "the same way scopes are" (R4), so it uses
    roadmap-labels' two functions and has no label reader or check of its own:
    `split_labels(what)` peels the labels off the line, and
    `label_problems(labels, glossary_text, where)` refuses, by line, a label naming no term.
    `glossary_text` is the glossary a scope's labels are checked against for this repo: the
    metarepo's in a family, read as roadmap-labels reads it, and the repo's own otherwise.
11. **`jig ideas`** prints each idea: id, title, status, labels and touched pages.
    `--label <label>` keeps those carrying it, matched after `label_problems`' fold, with the
    same flag shape as `jig roadmap --label`. In a metarepo it also lists each pararepo's
    ideas, read on its trunk through `peer_logs`' read, named by repo, and a pararepo it can't
    reach is named. This is the research list R4 asks for, grouped by label across the family,
    so "Teleport questions" can be found in one place.
12. **RULES.md and the skills.** Every place in Givens that names `## Open` names the ideas log:
    - RULES.md, Decision log: a new "Ideas" paragraph after the status paragraph, and the
      sections list down to `## Unreleased` and releases;
    - R3, M2, Staging, `--merge-log`, Product and project, Metarepo and pararepos
      (questions that bind the pararepos are ideas, cited before they are answered; "an open
      question is an idea in its repo's ideas log"), and Commands (`jig ideas`);
    - the `stage`, `update`, `redocument` and `retro` skills;
    - `docs/records.md` and `docs/glossary.md` gain the ideas log, `docs/commands.md` gains
      `jig ideas`, and `docs/metarepos.md` gets its question line.

## Done when

Every command in a throwaway repo, run with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.

Part A, in a stand-alone repo:
- [ ] (init) `jig init` writes `.jig/ideas.md`, and `.jig/decisions.md` has no `## Open`.
- [ ] (an idea, numbered) A job adds `### D-?adapter-hid Does the adapter emulate a HID?` with `Open (2026-11-23).` and `Touches: docs/x.md` to `.jig/ideas.md`. Its commit passes. `jig merge` numbers it `D-001` in `.jig/ideas.md`, and the next entry the log gets is `D-002`. A `D-?x` idea committed on trunk is refused.
- [ ] (checked) `.jig/ideas.md` with an `Accepted (Dave, 2026-11-23).` idea is refused, naming the log's `## Unreleased`. So is an idea with no status line, and an idea whose id the log also has.
- [ ] (decided keeps its id) A commit moving `D-001` to the log's `## Unreleased` as `Accepted (Dave, 2026-11-23).` passes. `jig decision D-001` prints it from the log. Before that commit, it printed it as an idea in `.jig/ideas.md`.
- [ ] (dropped) A commit removing an idea with no other change passes.
- [ ] (readers) `jig reading-list docs/x.md` lists `D-001` under `docs/x.md` while it is an idea. `jig reading-list --claims D-001` names its home in `.jig/ideas.md`. `jig decision <accepted id touching docs/x.md> --peers` lists the idea, marked as one.
- [ ] (gate) A job adding a `Proposed` idea gets the gate's "Proposed: it merges unruled" warning, naming `.jig/ideas.md`.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh decisions supersede removals claims touches init_old_board` passes.

Part B:
- [ ] (fold) A repo whose log has `## Open` with `D-003` Open and `D-004` Proposed: `jig update` lists it. `jig update --apply` writes both blocks byte for byte into `.jig/ideas.md` and removes `## Open`, and its trunk commit passes. Afterwards, a commit adding `## Open`, or an `Open (…)` entry under `## Unreleased`, is refused by line, naming `.jig/ideas.md`.
- [ ] (writers) A staged `kind: decisions` file with an Open entry resolves into `.jig/ideas.md`. `--apply --merge-log` on a register with an open row, and on an ADR folder with a `proposed` record, writes each into `.jig/ideas.md`. `jig survey` on a page with `## Undefined` names `.jig/ideas.md` for an open question.
- [ ] (metarepo, citations) Metarepo `M` (`E-`) with pararepo `L`. `M` releases v0.1.0 with `E-001` under `## Open`, and `L` cites `E-001`. `M` folds it into ideas and releases v0.1.1. `L`'s pin-bump request lists no `E-001 (removed)`, and `L`'s `jig sync` lists no removal. `M` then accepts `E-001` in place and releases v0.1.2, and `L`'s request reads it as accepted, with no removal.
- [ ] (metarepo, moved down) In `M`, idea `E-002` removed with `- E-002: moved to L/.jig/ideas.md § D-001.` passes when `L`'s trunk has idea `D-001`, and is refused, naming `L/.jig/ideas.md`, when it doesn't.
- [ ] (M3) A metarepo job that only adds an idea needs no change line.
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh update staging merge_log sweep pin_bump moves pararepo metarepo entry_globs` passes.

Part C:
- [ ] (labels) An idea with `(labels teleport)`, where `teleport` passes roadmap-labels' check for a scope, commits. One with a label that check refuses is refused by line, with the same message a scope gets.
- [ ] (one label reader) `grep -c '^LABELS = re.compile' plugin/templates/jig/jig.py` prints 1, and the ideas code reads and checks labels only through `split_labels` and `label_problems`.
- [ ] (list) `jig ideas` lists every idea with its labels. `jig ideas --label teleport` lists only those carrying it. In `M`, `jig ideas` also lists `L`'s ideas, named `L`. With `L` dropped from the repos file, it names `L` as not read.
- [ ] (none left) `git grep -n '## Open' plugin/` finds only the fold and its refusal in `jig.py` and RULES.md's sentence on the fold. `git grep -n '## Open' docs/` finds nothing.
- [ ] (complete) `python3 .jig/jig.py queue -- bash tests/smoke.sh` passes, and so does `claude plugin validate ./plugin`.

## Out of scope
- Writing maige-ecosystem's held questions (Walytpass, Teleport, E-023) into its ideas log, and folding its `## Open`: that repo's job, on its owner's word, once a jig with this is installed.
- Folding this repo's own `## Open`: `/jig:update` does it, as for any adopter.
- A spec taking an idea. An idea isn't in scope yet (R4), so a `Scope:` line names roadmap ids only, as today.

## Touches
- `plugin/templates/jig/jig.py`:
  - Part A: a new `IDEAS` path and seed; `log_problems` (M2 over both files, one id across them), the R3 log exemption, `append_globs`, merge numbering and the trunk `D-?` refusal; `cmd_decision`, `claims_of_id`, `hold_chain`/`holds_now`, `live_entries`/`touching`/`peer_logs`, `proposed_added`; `cmd_reading_list` (ideas per page); `cmd_init`; `LOG_SEED`.
  - Part B: `cmd_update` (the fold and its listing), the `## Open` refusal, staging resolve for `kind: decisions`, `cmd_merge_log`, `project_sections`, the kickoff text, `is_entry` and M3, `meta_citations`, `stage_pin_bumps`, `changes_report`, the move-line target check.
  - Part C: the idea `(labels …)` line, read by `split_labels` and checked by `label_problems`; a new `cmd_ideas`.
  - Reused, not copied: `log_entries`, `status_parts`, `entry_touches`, `peer_logs`, `trunk_show`, `MOVE_LINE`, and roadmap-labels' `split_labels` and `label_problems`.
- `plugin/templates/jig/RULES.md`: The rules (R3), Documentation (Product and project), Decision log (sections, Ideas, Released sections' move line, Checked, `--merge-log`, decision records), Staging, Metarepo and pararepos (a question that binds pararepos, an open question's home, M2's row), Commands (`jig ideas`).
- `plugin/skills/stage/SKILL.md`, `plugin/skills/update/SKILL.md`, `plugin/skills/redocument/SKILL.md`, `plugin/skills/retro/SKILL.md`
- `docs/records.md`, `docs/glossary.md`, `docs/commands.md`, `docs/metarepos.md`
- `tests/smoke.sh`: decisions, supersede, removals, claims, touches, init_old_board, update, staging, merge_log, sweep, pin_bump, moves, pararepo, metarepo, entry_globs, and a new `ideas` section for the checks above
- Process or product: product (jig's behaviour), written in RULES.md and the skills as their homes.

## Alternatives considered
- **Keeping `## Open` and adding labels to it.** Rejected because the owner rejected it: "It's very confusing to me that ideas can basically live in both places... I think ideas should be their own log" (R4), and agreed the log "keeps only decisions" (R5). Reason is [seen].
- **Ideas as roadmap items (`## No phase`).** Rejected because the owner said "If it's an idea its not in scope yet and it needs research" (R4), and No phase items are scoped work a spec may take. Reason is [seen].
- **A new id form for ideas (`I-001`).** Rejected because released entries and pararepos already cite Open ids (E-017, E-044), and frozen text can't be rewritten. A new form would need a move line for every Open entry in every repo. Reason is [seen].
- **One ideas log in the metarepo, as with the roadmap.** Rejected by the owner, 2026-11-23: "one ideas log per repo". Each repo's Open entries carry its own prefix, and `jig ideas` in the metarepo gives the one view. Reason is [seen].
- **`Labels:` as a field line.** Rejected for `(labels …)` on a line of its own. That is the scope's form, so one parser serves both, and a phase's `(after …)` line is the precedent. Reason is [seen].
- **A two-run fold like `## Up next`'s.** Not planned. An old checker already lets Open entries leave (Givens, [assumed]). If the build finds otherwise, it takes the Up next fold's two-run shape.

## Decisions
- An idea keeps its decision id, and deciding it moves its block with that id. Frozen citations resolve with no new address, and accepting an idea stays the edit it is today, with the block moved to the other file.
- An idea's status stays `Open` or `Proposed`. Proposed means an answer is put forward, and the gate's warning and the kickoff's message to the hubnode still key on it.
- `.jig/ideas.md` is treated like the log for jobs (R3 and append), and in a metarepo as an entry file recorded by itself, since pararepos cite its ids.
- One ideas log per repo. The owner, 2026-11-23: "one ideas log per repo".
- Parts A–C with `--partial`, so the file and its readers land before the fold moves anything into it. The hubnode, 2026-11-23: Parts A and B start now. Part C waits for roadmap-labels' Part A on trunk, and calls its `split_labels` and `label_problems` with no label check of its own.
- Interpreted (the hubnode, 2026-11-23): in a metarepo the fold runs as `jig update --apply --fold-ideas` in a job's worktree, refused on its trunk, as `--merge-log` runs there, since `jig update --apply` refuses while any job is open. On any other repo's trunk `jig update --apply` folds as a step. Rejected: asking the job to move the blocks by hand, which can't promise byte for byte.
- Interpreted (the hubnode, 2026-11-23): the refusal after the fold is by added line: an `## Open` heading the log didn't have, and an Open or Proposed entry the change adds. A log not folded yet keeps its `## Open`, so a metarepo's trunk with the new checker isn't stuck before its fold job merges. Rejected: refusing every `## Open` outright.
- Interpreted (the hubnode, 2026-11-23): an idea accepted in place breaks no citation, so the release stages no pin-bump request for it; the pararepo's `jig sync` reads it `<id> (accepted)`. Rejected: staging a request only to say an idea was accepted.
- The `marketing/FEATURES.md` row:

  | Ideas log | `.jig/ideas.md`: open questions and ideas to research before they can be decided, scoped, built and documented. Each is in a decision entry's form with its decision id, Open or Proposed, `(labels …)` as a scope's, and leaves by being decided (same id, into the log's `## Unreleased`), dropped, or moved down. The log's `## Open` folds into it by `jig update --apply`. `jig reading-list` shows a page's ideas, and `jig ideas [--label]` lists them, family-wide in a metarepo. | Dave, 2026-11-19, rounds 4–5 of the scope-ownership design ("ideas should be their own log, labeled the same way scopes are"; "Agreed on all of it"); built on his 2026-11-23 ruling "end state was supposed to mean exactly that" (`.jig/specs/ideas-log.md`) | Open questions in the decision log made it hold things not decided, and ideas parked in phases or Open entries got lost. A research list of its own keeps the log to decisions and lets a spec see what still needs research. | Scope: a spec can't take an idea. A second id space: ideas keep decision ids. |

## Open questions for the owner
1. Answered: one ideas log per repo (Decisions).
2. Answered by the hubnode: build order (Decisions).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
