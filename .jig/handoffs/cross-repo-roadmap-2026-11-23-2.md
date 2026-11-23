# Handoff: cross-repo-roadmap

Commit: dd0cd99f6bd94894a1e7401d505bf61043776b9d
Date: 2026-11-23
Spec: .jig/specs/cross-repo-roadmap.md
Partial: yes
Review: tier 2, effort 2
Ran: claude-opus-5-5 at high
Review-change: tier 2, effort 2
Review-change ran: claude-opus-5-5 at high

## Built
Part C of cross-repo-roadmap: one roadmap in the metarepo.
- **Products:** a heading `## <Product> <phase>` belongs to the longest glossary term with an `Owner:` line, either a pararepo or `this repo` (`term_owners`, `product_of`). A heading ending ` No phase` is a list, with ids `<heading>/<id>`. `jig roadmap` reports an Owner: that `jig repos` doesn't know.
- **One reader:** `Family`, built once per command and keyed on `main_root()`:
  - Metarepo: its own text, its glossary owners, and the pararepos that keep no roadmap of their own.
  - Pararepo with no `.jig/roadmap.md`: meta's text and glossary, read live through `trunk_show(meta_checkout(…))`.
  - Anything else is a family of one.
  - Unreachable repos are named by `jig roadmap`, rig, reading-list and the fold-in.
- **States:** pulled from every reachable family repo's trunk specs and notes (`scope_takers`). Each product has its own current phase. A product whose owner is unreachable reads `unknown`. Reads are memoized per command.
- **Readers:** `jig roadmap`, rig (offering only what this repo builds, `fam.ours`), reading-list and fold-in, the gate's built check, the reference guard, and the hooks.
  - A pararepo's `Scope:` is checked against meta's trunk, with a warning when meta can't be reached.
  - Meta's drop guard names a pararepo's spec.
  - A product section's page is looked up on its owner's trunk.
  - A pararepo removing a touched page gets a warning.
- **Views:** only a metarepo writes ROADMAP.md. A pararepo's merge writes nothing to meta.
- **Moved page (Interpreted, the hubnode 2026-11-23):** an item in a meta-owned section follows its page into the pararepo's product section in the same commit. The staged route stays only for a pararepo with its own roadmap.

## Done-when evidence
At dd0cd99 (synced with main), in throwaway repos with `JIG_CONFIG`/`XDG_CONFIG_HOME` set:
- `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap family rig rig_batch sweep update page_contract boundary pin_bump moves pararepo metarepo consolidate update_roles sync_buffer`: rc=0, 727 PASS, 0 FAIL.
- `python3 .jig/jig.py queue -- .jig/scripts/check.sh`: rc=0.

Part C, all in smoke section `family`:
- (products) PASS "family: meta's roadmap with two products and its own phase commits, docs/p.md found on pa's trunk" and "…jig roadmap in meta shows each product's phase and its own as current". Also "…a product section's page is the owning repo's: one pa lacks is refused, though meta has it".
- (Issue 3's symptom gone) PASS "family: rig in pa doesn't offer Walyt alpha/pairing: it waits on Familiar App alpha/host".
- (progress, live) PASS "family: pb's spec taking Familiar App alpha/host commits, checked against meta's trunk", "…once pb merges it, with no meta release, rig in pa offers Walyt alpha/pairing", "…jig roadmap in meta shows host done, and pb's merge wrote nothing to meta".
- (the deadlock refused) PASS "family: the deadlock is refused: host waiting on Walyt alpha/pairing is a ring, named once".
- (live read) PASS "family: a scope added on meta's trunk, no release: a spec in pa taking it commits, one taking nope is refused, naming meta's roadmap", and "…jig roadmap in pa reads meta's roadmap from its trunk".
- (unreachable) PASS "family: with pb out of the repos file, meta's roadmap shows pb's open scopes unknown, naming pb", "…with meta out of the repos file, a spec commit in pa passes its Scope: check with a warning naming meta", "…rig and reading-list in pa say so".
- (drop guard) PASS "family: dropping Walyt alpha/pairing in meta while pa's spec takes it is refused, naming that spec".
- (unphased scope, live) PASS "family: pb's reading-list of a file docs/y.md covers lists Familiar App No phase/y, read from meta" and "…once pb merges the job taking it, meta's roadmap shows Familiar App No phase/y done, and pb wrote nothing to meta".
- (a moved page's items follow it) The Done-when line is rewritten per the Interpreted ruling, in the spec at 163b516. PASS "family: meta moving docs/w.md down to pa, its scope left in Demos, is refused, naming the scope, pa/docs/w.md and pa's section", and "…with the scope moved under ## Walyt alpha in that commit, the merge passes, the page checked on pa's trunk".
- Review fixes: PASS "…pc keeps its own roadmap…", "…a pa page naming a scope of meta's roadmap in code quotes is refused", "…pa removing a page … commits, with a warning", "…from a job's worktree in pa, jig roadmap counts pa's spec once".
- (no regression) the run above.

## Review
1. review-work of 163b516, blocking 3 (strike 1):
   - B1: takers pulled from pararepos with their own roadmap.
   - B2: the reference guard read the local roadmap.
   - B3: an unreachable meta was silent in rig, reading-list and fold-in.
   - Should-fixes, all taken: 4, a pa's removed page plus the owner in the message; 5, `built_untaken` reading the family; 6, memoized reads; 7, `family()` keyed on main_root.
   - 9: a RULES line.
   - All fixed at 913be2a, synced at dd0cd99.
   - 8 and 10: deferred (rows).
   - Carried to Part D: moving in through `roadmap_rules`' local branch, and the sweep writing a local roadmap.
2. review-change of dd0cd99, blocking 0. S2, O1, O2, O3 deferred (rows). The reviewer's S1 is the same as 10.

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
- [x] UNOWNED plugin/templates/jig/jig.py — no page needed because its documentation is `plugin/templates/jig/RULES.md`, updated here (Roadmap: the repo and product paragraph, Products, One reader, A touched page exists; Metarepo and pararepos: the live-read exception) with the spec skill's `Scope:` ids.

## Shared files changed
- `plugin/templates/jig/jig.py`: Family, products, the one reader, pulled states, readers, hooks and rig per repo. This is the product.
- `plugin/templates/jig/RULES.md`: Roadmap (repo and product, Products, One reader, A touched page exists) and Metarepo and pararepos (the live read).
- `plugin/skills/spec/SKILL.md`: `Scope:` ids with a product, with a generic example.
- `plugin/skills/rig/SKILL.md`: the sync's merge with main's step-1 paragraph, both kept.
- `tests/smoke.sh`: a new section `family` (24 cases), in UNITS.
- `.jig/specs/cross-repo-roadmap.md`: the Interpreted line and the moved-page Done-when.

## Test by hand
Make a metarepo whose glossary has `## App` with `` Owner: `pa`. ``, and register pa as a pararepo with no roadmap. With `## App alpha` in meta's roadmap:
- `jig roadmap` in pa prints meta's roadmap, read from its trunk.
- A spec in pa with `Scope: App alpha/<scope>` commits.
- Once that spec is complete, `jig roadmap` in meta shows the scope done, with no release.

## Left
- Part D: buffered edits through `jig propose` (R5 lets meta's `propose/` branch carry the roadmap), moving in by hand, unconfirmed cross-product waits flagged. It carries two items from Part C's review: the moving-in commit through `roadmap_rules`' local branch, and the sweep writing a local roadmap in a pararepo that plans from meta.
