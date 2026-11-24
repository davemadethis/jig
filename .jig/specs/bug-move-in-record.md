# Bug: `jig move-in` step 2 re-derives what step 1 decided, and M's owner check sees one side of a merge

Source: the jig hubnode, 2026-11-23, starting the bug role on job `moving-in-command` after its third blocking review of Part A. The reviewer's words, as the hubnode relayed them: "`moved_in_as()` scores headings that map identically, so it picks the wrong product and overrides a correct `--product`." Repro: pararepo `pf` owns Foxy and Gadget, its roadmap is `## alpha`, `## Gadget gamma`, `## Gadget delta`, and step 1 ran with `--product Foxy`. Step 2 returns Gadget. The three blocking reviews: 81b4852, where step 2's `exists and proposal_in` missed a proposal `jig merge` had merged. 16d6184, where `owner_dropped` read trunk's tip instead of the commit being judged, and the `kept` filter emptied the candidate products. c47c2d5, the symptom above. c47c2d5's review also left two should-fixes: the `move-in-withdrawn-<n>.md` convention, and a merge that turns pararepo headings into M's own phases when M dropped the `Owner:` first. It left one optional: an empty branch prints "gone".

Bug-for: moving-in-command

## Intent
Step 2 of `jig move-in` reads what step 1 decided from step 1's own record: the product from
its buffer row, and the proposal from its spec's `meta:` line. It finds that record the way
`jig sync` finds a proposal. It asks the metarepo only what the metarepo decides: whether it
merged the proposal, and under which name, when the owner says it renamed it. A re-proposal
after a withdrawal takes a new name, as `jig propose --buffer` does, and the withdrawn spec stays
as it is. The metarepo's hook judges a merge against both of its sides, so the merge that
brings a product's phases can't turn them into the metarepo's own.

## 1. Why
- Why did c47c2d5's review block? `moved_in_as` scores every mapped heading. `Gadget gamma` and
  `Gadget delta`, which map to themselves, outvote `Foxy alpha` and override `--product Foxy`. [seen]
- Why does step 2 score M's roadmap at all? Since 16d6184 it derives the product from M's
  current state, to follow a rename at the merge. It never reads the `§ Foxy` that step 1 wrote. [seen]
- Why derive instead of read? The command finds its steps by a fixed name and reads M for the
  rest. `jig propose` and `jig sync` read their own records instead. No spec asked for the rename. [seen]

Root: step 2 re-derives what step 1 already recorded (the product, the live proposal) from the
metarepo's state, so each derivation has its own edge. The hypothesis holds for the product and
the proposal. The owner findings have another root, M's hook judging one parent (Givens).

Each finding, and what was re-derived instead of read:

| Review | Finding | Re-derived | Already held by |
|---|---|---|---|
| 81b4852, blocking | `exists and proposal_in` missed a `jig merge` | whether M took it | `proposal_in` itself, called as `jig sync` calls it. Fixed in 16d6184 |
| 16d6184, blocking | `owner_dropped` read trunk's tip | the owner the commit started from | HEAD. Fixed in c47c2d5. The merge case remains (below) |
| 16d6184, blocking | `kept` emptied the candidates | the product | step 1's row, `§ <Product>` |
| c47c2d5, blocking | `moved_in_as` picks Gadget | the product | step 1's row, `§ <Product>` |
| c47c2d5, should-fix | `move-in-withdrawn-<n>.md` | which proposal is live | the spec's `meta:` line, found by scanning specs |
| c47c2d5, should-fix | a merge turns headings into M's own | the owner the merged side gives | `merging_commits()`, as `numbers_given` reads the merged side |
| c47c2d5, optional | an empty branch says "gone" | the branch's state | `proposal_empty`, already computed there |

## 2. Givens
- [seen] Step 1 records the product and the proposal. The run in `pf` committed `BUFFER.md`
  row `| B1 | M/.jig/roadmap.md § Foxy: none yet | its phases and list, moving in | … | Open |`.
  It also committed `.jig/specs/move-in.md`, which lists `- B1` under `## Buffer rows`, copies
  the row into its own table and ends with `- meta: M proposal propose/pf-move-in`.
- [seen] Step 2 reads `move-in.md` only to see whether it names the fixed branch (`listed`,
  jig.py:15725). The product comes from `moved_in_as` (jig.py:15605-15629, called at 15740),
  which reads M's roadmap and glossary.
- [seen] The repro, in throwaway repos built like the smoke `movein` fixture. M's trunk holds
  `## Foxy alpha`, `## Gadget gamma` and `## Gadget delta` after the merge. Step 2 prints "jig:
  note: M names the product Gadget now, not Foxy" and `## alpha → ## Gadget alpha`. It does so
  with `--product Foxy` and with no flag. Its `--apply` leaves `sa.md` at `Scope: alpha/a` and
  names it for re-pointing by hand.
- [seen] The spec asks no rename-following of step 2. moving-in-command step 2 (lines 84-91)
  names the ids the metarepo lacks, "the owner changed it before merging", for the hubnode to
  re-point. Rename-following came in with 16d6184's RULES.md line ("under the product's name as
  the metarepo's glossary now gives it"), whose spec diff changes only a fixture line. c47c2d5
  then added `moved_in_as`. The hubnode rule from bug-strike-count holds that behaviour a spec
  never names "is a spec change before it is built".
- [seen] How jig's siblings carry state between steps:
  - `jig propose` writes `meta: <M> proposal <branch>` in a spec.
  - `sync_meta`, `withdraw_proposal` and `unreleased_proposals` find a proposal by scanning
    specs for that line (`PROPOSAL`, jig.py:7387). No reader uses a fixed name.
  - A buffer proposal's spec lists its rows and keeps their copy. `proposed_copy` counts a
    withdrawn spec as carrying nothing, and `buffer_proposal` refuses a spec name that exists.
  - `cmd_propose --buffer` names a new proposal by the user's slug or `buffer-<date>`.
  - When M decides other than proposed, the pararepo learns it on the owner's word:
    `jig sync --answered` closes rows "on the owner's word" (jig.py:8549).
  - Part C's `jig move` (spec step 9) records `meta: <meta> proposal <branch>` in
    `.jig/specs/move-<slug>.md` for its step 2 to read.
- [seen] The withdrawn repro (`pw`): step 1, `jig propose --withdraw propose/pw-move-in`, M
  deletes the branch, then step 1 again. That leaves `move-in-withdrawn-1.md` (`meta: M withdrawn
  propose/pw-move-in`) and `move-in.md` (`meta: M proposal propose/pw-move-in`). After M merges
  and releases v0.2.0, `jig sync` prints "proposal propose/pw-move-in
  (.jig/specs/move-in-withdrawn-1.md): withdrawn, but released by v0.2.0: … `jig sync --answered
  B1 --in v0.2.0`". That is false: the live proposal carried B1. With the old branch still in M,
  step 1 again is refused ("already exists in M, with a change on it").
- [seen] `free_name(folder, f)` (jig.py:11738) gives `move-in.md`, then `move-in-2.md`. It is
  jig's existing rule for a reused name that never overwrites.
- [seen] `owner_dropped` runs only when the commit's paths include the glossary
  (`check_rules`, jig.py:584). It compares with `HEAD` alone (jig.py:15523). On a trunk merge
  `base()` is HEAD, so a proposal that carries no glossary change never runs it.
- [seen] The owner repro (`pd`): Delta is pd's on M's trunk at step 1, so the proposal carries no
  glossary change. M then drops Delta's `Owner:` on a reviewed branch merged to main, which
  passes because no Delta heading is on trunk yet. `jig open mj --branch propose/pd-move-in` and
  `jig merge mj` both pass, and so does a plain `git merge`. M's glossary then gives Delta no
  owner, and `product_of("Delta alpha", …)` is `''`, M's own phase. pd's step 2 then refuses with
  "its hubnode decides the term at the proposal's merge", after that merge.
- [seen] `merging_commits()` (jig.py:5586) names what a merge in progress brings in, in both the
  pre-merge-commit hook and a conflicted merge's commit. `numbers_given` (jig.py:6402) reads the
  merged side's file through it, and M5 reads it too.
- [seen] A `## Proposals` job can't take a move-in proposal. An ordinary job branch in M,
  synced, merging `propose/pd-move-in` is refused: "R5 the roadmap is the owner's: .jig/roadmap.md
  is edited on main only, or on a propose/ branch". This holds with the owner kept and with it
  dropped. The routes R5 allows are a job opened on the proposal's own branch, as smoke does, and
  a merge on trunk. moving-in-command step 1 says "merges it in a job (`## Proposals`)".
- [seen] Optional finding: `if listed and not proposed` prints "is gone from M unmerged"
  (jig.py:15767-15769) when the branch exists with only its opening commit.
- [assumed] A metarepo's hubnode seldom renames a product at its merge, so the owner naming it
  at step 2 (`--product`) costs one word on a step that already waits on their yes. Not
  converted: that needs use. Held as a risk to the UX, not to correctness. Step 2 refuses and
  names the candidates rather than guess.
- [assumed] At most one move-in record's branch is on M's trunk. Two would mean two move-in
  proposals merged. Step 2 refuses, naming both, rather than pick.

## 3. One layer up
- **Siblings.** `jig sync`, `withdraw_proposal` and `unreleased_proposals` read the pararepo's
  own decisions from its specs (`meta:` lines, listed rows). They ask the metarepo only what it
  decides: `proposal_in` for "is it in this tag". None has this problem.
  Part C's step 2 reads its own spec and the receiver's moved-from line, which is the
  receiver's decision.
- **What's different.** Step 2 needs one value both sides may decide: pd proposes the
  product's name, and M's hubnode may change it at the merge. The command settled that by
  inferring M's choice. jig's existing answer to "the metarepo decided otherwise" is the
  owner's word, as with `jig sync --answered`, and naming what doesn't match, as moving-in-command
  step 2 already does for ids.
- **Existing patterns this reuses.** The buffer-proposal spec (row copy plus `meta:` line) as
  step 1's record, read as-is. `PROPOSAL`/`WITHDRAWN` scanning to find it. `free_name` for a
  re-proposal's slug. `proposal_in` and `proposal_empty` for M's side. `merging_commits()` for the
  merged side of a merge. Nothing new is recorded and no new file is written.

## 4. Workaround or correction
Corrections, all three:
- Step 2 reads the product and the proposal from step 1's record, and `moved_in_as` goes.
- Step 1's re-proposal takes a fresh name, and the withdrawn spec is left alone.
- M's owner check judges every parent of the commit.

The reviewer's direction (score only re-headed headings, honour `want` above 0) would patch
`moved_in_as`. That is a workaround for a derivation that needn't exist.

## 5. Spec

### Change
1. **The move-in record.** It is a spec in `.jig/specs/` with three parts. Its `## Buffer rows`
   lists a row its own table reads as `<meta>/.jig/roadmap.md § <Product>: none yet` with `its
   phases and list, moving in`. A `meta: <meta> proposal <branch>` or `meta: <meta> withdrawn
   <branch> — …` line names its branch. Step 2 reads the product from the spec's own copy of the
   row, never from `BUFFER.md`, whose row `jig sync` may close. `cmd_move_in` finds the record
   by scanning specs as `withdraw_proposal` does, and the fixed-name lookup goes. Its state:
   - A record whose branch `proposal_in` finds on M's trunk, withdrawn or not: step 1 is done,
     and step 2 reads that record's product. If two records match, it is refused, naming both.
   - Else a live record (`proposal`) whose branch carries more than its opening: step 1 is
     done, waiting on M's owner.
   - Else a live record whose branch is empty: step 1 is next, and the plan says the branch is
     "empty in M: a run stopped before its commit" (the optional finding). If its branch is
     gone unmerged, the plan says "gone from M unmerged". Either way, step 1 proposes again
     under that record's name, its spec replaced and its empty branch dropped, as today.
   - Else, with no record or only withdrawn ones: step 1 is next, under the name `free_name`
     gives (`move-in`, then `move-in-2`), with branch `propose/<repo>-<slug>`. A withdrawn spec
     is never moved, renamed or rewritten. Its branch, if M kept it, is M's to delete and
     blocks nothing. The `move-in-withdrawn-<n>.md` code goes.
   - A spec counts as a record only when its `## Buffer rows` lists that row alone, as step 1
     writes it: a spec carrying more rows is some other proposal's.
   - The move-in row is `jig move-in`'s alone. `unproposed` leaves out every row whose "This
     repo now" cell reads `its phases and list, moving in`, except for step 1's own call, so
     neither `jig release` nor `jig propose --buffer` carries it. A row left Open by a withdrawal
     waits for `jig move-in` (review-change of 9ac1ee9, blocking: a withdrawn row swept into
     `buffer-<tag>.md` became step 2's record). `jig propose --withdraw` says so of a move-in row
     ("goes again by `jig move-in`"), apart from the rows that go in the next proposal, and `jig
     propose --buffer`'s "nothing to propose" says a move-in row is left to `jig move-in`.
   - Step 1 keeps one move-in row. Rerun, it takes the Open move-in row there is; under another
     `--product` it edits that row's claim in place, as a change of mind edits any row, never
     adding a second that nothing could carry (review-change of a9fc7c8).
2. **The product at step 2** is the record's. `--product <Name>` at step 2 is the owner's word
   that M's hubnode renamed it at the merge. When it differs from the record, the plan prints
   both names. The map is `move_in_map(own, product, mine)`, with `mine` as today. Before step 2
   is next, it is refused, naming what it read, when:
   - M's trunk glossary doesn't give the product to this repo. It names the term and what the
     glossary says of it (no `Owner:`, or another repo's), so M's hubnode can restore the owner.
   - M's trunk holds none of the headings the map gives. It names those headings and the terms
     M's glossary gives this repo: "if M's hubnode renamed the product, `--product <Name>`".

   Otherwise ids M lacks are named with their takers, as the spec already says. `moved_in_as`
   is deleted, so no step scores anything.
3. **M's owner check** (`owner_dropped`) runs on any metarepo commit whose paths include the
   roadmap or the glossary. It judges the commit against HEAD and against each commit
   `merging_commits()` names. A term that one of them gives an owner, which the commit's own
   glossary doesn't, is refused while the commit's roadmap heads a section with it. The
   refusal names the side that gave the owner (HEAD, or the merged branch) and the headings.
4. **Text.**
   - RULES.md, Roadmap, Moving in, step 1: the branch is `propose/<repo>-move-in`, or the
     next free name once a withdrawn proposal holds it. "it refuses a glossary change that takes
     a product's `Owner:` away" becomes "it refuses a commit or a merge that leaves a product's
     headings without the `Owner:` either side gave". "A withdrawn `move-in.md` is kept beside
     the new one" becomes "a withdrawn proposal's spec stays as it is". Step 2: "under the
     product its row names, or the name `--product` gives when the metarepo's hubnode renamed
     it", plus the two refusals above. The rename-inference wording goes.
   - moving-in-command.md, Part A step 1: "Its hubnode merges it in a job (`## Proposals`)"
     becomes "in a job opened on that branch (`jig open <job> --branch propose/<repo>-move-in`),
     or merged on trunk on its owner's yes". Step 2 gains the product-source sentence above.
   - The hubnode skill's move-in line: "merge in a job" names the `--branch` form, and says a
     job merging it from another branch is refused by R5.

### Done when
Smoke, `movein` section, in its throwaway repos (`JIG_CONFIG`, `XDG_CONFIG_HOME` set):
- [ ] (the reported symptom) `pf`'s fixture roadmap becomes:
  - `## alpha` with `a`, which spec `sa` takes;
  - `## Gadget gamma` with `g (after alpha/a)`;
  - `## Gadget delta` with `d`.

  M's glossary gives Foxy and Gadget to `pf`. Step 1, `--product Foxy --apply`, proposes `## Foxy
  alpha`, `## Gadget gamma` and `## Gadget delta`, and M merges it. Step 2, with no `--product`
  and with `--product Foxy`, prints `as Foxy` and `## alpha → ## Foxy alpha`, and the output
  holds no `Gadget alpha`. `--apply` stages `Scope: Foxy alpha/a` in `sa.md`, and the commit
  passes. pf's existing cases keep their checks with `beta` read as `alpha`:
  - `## Up next` is refused;
  - `## Foxy alpha` already on M's trunk is refused;
  - with Foxy already owned, the proposal makes no glossary change, keeps `## Gadget gamma`
    unchanged and maps its ref to `(after Foxy alpha/a)`.
- [ ] (no inference) In `pr`, M keeps Rex and re-heads `## Rex alpha` to `## Rover alpha` at the
  merge. Step 2 with no `--product` is refused, naming `## Rex alpha` as missing on M's trunk,
  the terms `Rex` and `Rover`, and `--product`, and nothing is staged. With `--product Rover`
  it prints that the record says Rex, stages `Scope: Rover alpha/r`, and the commit passes.
- [ ] (step 2 checks the owner) M's trunk holds `## Widget beta` while Widget's `Owner:` is gone,
  planted with hooks off to stand in for a merge that skipped the hook. `pg`'s step 2 is
  refused, naming Widget and `Owner:`, and nothing is staged.
- [ ] (owner, at the merge) Widget is `pg`'s on M's trunk at step 1, so the proposal carries no
  glossary change. M drops Widget's `Owner:` through a reviewed branch merged to main, which
  passes. Merging `propose/pg-move-in` into M's main is then refused, naming `## Widget` and
  `## Widget beta`, and M's main tip is unchanged. With the owner restored the merge passes, and
  pg's step 2 runs as today's case does. The existing owner cases still pass:
  - the drop on a branch is refused;
  - the unrelated glossary edit on a branch cut before Rex and Rover passes;
  - Rover renamed Rocket over two commits passes.
- [ ] (withdrawn) In a new pararepo `pw`:
  - step 1 is committed, then `jig propose --withdraw propose/pw-move-in --reason r` is committed;
  - with M still holding the old branch, step 1 `--apply` makes `propose/pw-move-in-2` and
    `.jig/specs/move-in-2.md`;
  - `git diff HEAD -- .jig/specs/move-in.md` is empty, it still reads `meta: M withdrawn
    propose/pw-move-in`, and no `move-in-withdrawn-*` file exists;
  - M merges `propose/pw-move-in-2` and releases, then `pw`'s `jig sync` prints
    `propose/pw-move-in-2 (.jig/specs/move-in-2.md): released by` and no `withdrawn, but
    released` line;
  - `jig move-in` in `pw` then says step 2 is next, as Wex.
- [ ] (empty is not gone) With a move-in branch reset to its opening commit, the plan says it is
  empty in M and step 1 is next. With the branch deleted unmerged, the plan says gone.
- [ ] (the move-in row stays move-in's) In `pw`, step 1 rerun with `--product Wox` on an empty
  record proposes Wox under `move-in.md`, its row listed alone, and `BUFFER.md` holds one move-in
  row, B1, which now reads Wox. Then, before and after the withdrawal, `jig propose --buffer`
  says nothing to propose: no `buffer-*` spec and no new branch in M2. Before the withdrawal it
  names the live proposal carrying the row, never that `jig move-in` proposes it again. After it
  says a move-in row is left to `jig move-in`, and the withdrawal itself said B1 goes again by
  `jig move-in`, not in the next proposal. The re-proposal as Wex reuses its row, B1, alone in
  `move-in-2.md`.
- [ ] (strike 1 stays fixed) "with the branch deleted by that merge, step 2 is next" still passes.
- [ ] `grep -c 'def moved_in_as\|withdrawn-{n}' plugin/templates/jig/jig.py` prints 0.
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh movein moves pararepo metarepo roadmap
  rig boundary staging decisions supersede removals pin_bump claims sync_buffer` passes.
  `claude plugin validate ./plugin` and `.jig/scripts/check.sh` pass.

### Out of scope
- A `## Proposals` job that takes a roadmap proposal. R5, cross-repo-roadmap's rule for every
  roadmap proposal, refuses the roadmap change on an ordinary job branch [seen]. This spec points
  move-in at the routes R5 allows and doesn't widen R5. The owner, 2026-11-23: "No, propose route
  suffices": a roadmap proposal is taken by a job opened on its `propose/` branch, and nothing
  is tracked.
- Following a rename without the owner's word. Step 2 names the mismatch and the candidates,
  and `--product` carries the owner's answer (Decisions).

### Touches
- `plugin/templates/jig/jig.py`:
  - `cmd_move_in`: the record lookup, the product from the record, `--product` at step 2,
    the two refusals, and empty told apart from gone;
  - `move_in_propose`: the slug from `free_name`, no `kept_as`;
  - `unproposed` and `buffer_proposal`: the move-in row left out of every proposal but step 1's;
  - `withdraw_proposal` and `cmd_propose --buffer`: what each says of a move-in row;
  - `moved_in_as`: deleted;
  - `owner_dropped` and its call in `check_rules`: every parent, roadmap or glossary paths;
  - the `MOVE_IN` comment.
- `plugin/templates/jig/RULES.md`: Roadmap, Moving in (steps 1 and 2); Metarepo and pararepos,
  the sync buffer ("every `Open` row" but a move-in row, and a withdrawn one's); Commands
  (`jig propose --buffer`).
- `docs/metarepos.md`: the release's buffer proposal, a move-in row left out.
- `plugin/templates/ledgers/BUFFER.md` and `plugin/skills/release/SKILL.md`: "every Open row"
  but a move-in row.
- `plugin/skills/hubnode/SKILL.md`: the move-in line.
- `.jig/specs/moving-in-command.md`: Part A steps 1 and 2, the sentences in Change 4.
- `tests/smoke.sh`: `sec_movein`, with the cases above and pf's and pr's fixtures as changed;
  `sec_family` D's hand-made move-in row reads "moved in by hand", since "moving in" marks
  `jig move-in`'s own row.

### Alternatives considered
- **Score only headings a map re-heads, and honour `--product` whenever it scores above 0**
  (c47c2d5's reviewer). Rejected because step 1 already wrote the product in its row. Each
  derivation tried so far failed a review on an edge: 16d6184's `kept` filter, then c47c2d5's
  score. This reason is [seen].
- **A new record of step 1's choices** (a state file, or a map section in `move-in.md`).
  Rejected because the row's `§ <Product>` and the `meta:` line hold what step 2 needs, and
  `move_in_map` rebuilds the map from the product. moving-in-command's Decisions say "no state
  file", and the owner's rule is to reuse a record as-is. This reason is [seen].
- **Read a renamed product from the merge's roadmap diff** (the headings the merge added).
  Rejected because M's hubnode may add or re-head other phases on the branch, so the added
  headings still need matching to the map. That is inference again. This reason is [assumed];
  the fix doesn't rest on it: rename-following was never asked for, and `--product` carries it.
- **Keep the fixed name and move a withdrawn spec aside** (c47c2d5). Rejected because the moved
  record and the new one name one branch, and `jig sync` then advises `--answered` for a row the
  live proposal carried. This reason is [seen], in the repro.
- **Keep the fixed name and require M to delete the old branch and the owner to delete the
  withdrawn spec.** Rejected because the withdrawn spec is the record of what went
  (`proposed_copy`, and `withdraw` says "Commit that spec"), and jig keeps it where it is. This
  reason is [seen].
- **Check the owner only at pd's step 2.** Rejected as the whole fix, because M's roadmap would
  still hold pd's phases as M's own after the merge. It is kept as a second check for a merge
  that skipped the hook. This reason is [seen]: the merge passed and M read `Delta alpha` as its
  own.
- **Widen R5 so a `## Proposals` job may merge a roadmap proposal.** Rejected here because R5
  covers every roadmap proposal, which is cross-repo-roadmap's rule, not this job's (Out of
  scope). This reason is [seen]: RULES.md, Roadmap, R5.

### Decisions
- Step 2 reads the product from step 1's row, in the move-in spec's own copy. A rename the
  metarepo's hubnode made at the merge reaches step 2 by the owner's word, `--product`, as `jig
  sync --answered` carries a metarepo decision the pararepo can't read. No step scores or guesses.
- The record is found as `jig sync` finds a proposal, by scanning specs. A re-proposal after a
  withdrawal takes the next free name, as `jig propose --buffer` takes a new slug, and a
  withdrawn spec is never moved.
- M's owner check judges a commit against every parent, read by `merging_commits()`, whenever
  the commit changes the roadmap or the glossary.
- This spec is the spec change for the behaviour Part A's fix rounds added without one:
  - the owner check is kept and widened;
  - rename-following is replaced by `--product` at step 2;
  - the withdrawn record moved aside is removed.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
