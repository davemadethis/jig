# phase-types: phase types and roadmap filters

Source: Dave (owner), 2026-11-23, ruling on cross-repo-roadmap's deferral of its end state to "later specs": "end state was supposed to mean exactly that: everything including labels." The design is his of 2026-11-19 to 2026-11-21, in maige-ecosystem's hubnode session (staged there as `request-scope-ownership-from-maige-{os,familiar,lite}.md`, § Owner's answers).

Kept separate from roadmap-labels: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from ideas-log: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from moving-in-command: the owner, 2026-11-23: "start what you can in parallel"
Kept separate from bug-deferred-scope: the owner, 2026-11-23: "start what you can in parallel"

## Intent
Each phase has a type, Prototype, Pilot or Production. The type is read from the phase's name,
as the owner named the types, and is shown wherever phases are. `jig roadmap` can narrow its
listing and the view to a product, a phase, a type, a state or an owning repo, so "what's in
Walyt alpha" is one command.

## Investigation

**The owner's words** (Owner's answers in the three staged inputs, identical in each):
- Types, 2026-11-19, round 1: "Phases have 3 types: Prototype, Pilot, Production. Prototype
  phase names are alpha, beta, gamma, etc. Pilot phase names are "Pilot A", "Pilot B" etc.
  Production phase names are chosen by the user." Round 2: "production phase one is called
  "Walyt Launch"". Round 6: "each product has its own phases, like Walyt Alpha and USB-C
  Adapter Beta", and "the product is Walyt and the phase is Launch".
- Filters: the word "filter" isn't his. Round 2: "if I said "whats in walyt alpha" that would
  mean what scopes and specs apply to that product during the alpha phase", "show me
  <ProductName> <PhaseName> that would mean show me items that match that products label in
  this phase", and "I could've just said show me specs for features you own". Round 5 agreed
  "the rendered roadmap working from the central file".
- Departures: his two rulings of 2026-11-23 (Decisions) leave nothing to build.

**Givens** (trunk 06550ea)
- [seen] `parse_roadmap` (jig.py:10298) reads `## <heading>` as a phase, and `product_of` splits
  a product's term off a metarepo heading (`Walyt alpha` → `Walyt`, phase `alpha`). Nothing
  reads a type.
- [seen] `_roadmap_full` (jig.py:10946) gives each phase a `product`, `state` and `waits`, and
  each scope and No phase item a `product`, `state` and `waits`. `cmd_roadmap` (jig.py:11062)
  prints them all and takes only `--write` (jig.py:15595). `render_roadmap` writes the whole
  ROADMAP.md.
- [seen] A pararepo departing from a metarepo decision entry is changing a metarepo claim.
  Today's path already covers it, and the page text already says so:
  - RULES.md, Metarepo and pararepos (plugin/templates/jig/RULES.md:1464): "A reversed decision
    is a new entry that supersedes the old. A pararepo's own entry that touches a contract
    cites its BUFFER row or proposal; once the metarepo accepts it, a new entry here supersedes
    it".
  - `docs/metarepos.md` § Proposals and § The buffer (:51): "Every such difference is a row in
    `.jig/ledgers/BUFFER.md`".
  So no text is added.

**One layer up.** The type is a reading of the name, as the product is, so there is no new
syntax. The filters are one predicate over what `roadmap_full` already returns, shared by the
listing and the view.

## Change

**Part A: phase types** (every roadmap)
1. A phase's type comes from its name, after any product term. A Greek letter name (`alpha`
   … `omega`, case folded) is **Prototype**. `Pilot <one letter>` (case folded) is **Pilot**.
   Any other name is **Production**, its name the owner's. There is no marker and no config.
2. `jig roadmap` prints the type beside each phase's state. The view's phase line and each
   phase heading show it (`## Walyt alpha (Prototype, current)`).
3. Within one product, and within a roadmap's own phases, types run Prototype, then Pilot,
   then Production, in file order. When the roadmap changes on trunk, the hook refuses, by
   line, a phase whose type comes before the type of a phase above it in the same product.
   `jig roadmap` reports it. (Decided: the owner, 2026-11-23.)

**Part B: filters** (`jig roadmap` and the view)
4. `jig roadmap` takes `--product <term>`, `--phase <name>`, `--type <prototype|pilot|production>`,
   `--state <open|taken|done|blocked|unknown>` and `--owner <repo>`. Each flag is repeatable
   and case folded. Values of one flag are or'd, and different flags are and'ed.
   - `--phase alpha` matches every product's alpha. `--phase "Walyt alpha"` matches that one
     heading, and so does `--product Walyt --phase alpha`.
   - `--owner` matches the products whose `Owner:` names that repo. A metarepo's own phases and
     its `this repo` products are the metarepo's. In a stand-alone repo everything is this
     repo's.
5. Product, phase, type and owner choose phases. `--state` chooses scopes within them, and a
   phase left with no scope isn't printed. A No phase item matches product, owner and state.
   `--phase "No phase"` chooses the lists, and `--type` leaves them out.
6. A filter hides rows, never a problem: the roadmap's problems print in full, and the exit
   code is unchanged. A `--product`, `--owner` or `--type` value naming nothing jig knows is
   refused, naming the known values, so a typo never reads as an empty roadmap.
7. `jig roadmap --view [filters]` prints the view's Markdown for what the filters choose, to
   the terminal. `--write` takes no filter and refuses one: ROADMAP.md is always the whole
   roadmap. (Decided: the owner, 2026-11-23.)
8. RULES.md, Roadmap, says this: types, their order, and the filters.

## Done when

Every command runs in a throwaway repo with `JIG_CONFIG=<dir>/repos.json XDG_CONFIG_HOME=<dir>/config`.
Nothing writes `~/.config/jig/`.

Part A, in a stand-alone repo:
- [ ] (types) A roadmap with `## alpha`, `## Pilot A` and `## Launch`, each with a scope: `jig roadmap` prints `Prototype`, `Pilot` and `Production` beside them, and `jig roadmap --write` puts `(Prototype, current)` in `## alpha`'s heading in ROADMAP.md.
- [ ] (case) `## Beta` reads Prototype, and `## pilot b` reads Pilot.
- [ ] (order) A trunk commit adding `## gamma` after `## Pilot A` is refused, naming `gamma` by line. `jig roadmap` on such a roadmap reports it and exits 1.

Part A, in a metarepo `meta` with products Walyt (`pa`) and Familiar App (`pb`):
- [ ] (per product) A roadmap with `## Walyt alpha`, `## Familiar App Pilot A`, `## Walyt Launch` and `## Familiar App beta` is refused for `Familiar App beta` alone (it comes after its own product's Pilot), and never for `Walyt alpha`.

Part B, in that metarepo:
- [ ] (product and phase) `jig roadmap --product Walyt --phase alpha` prints `Walyt alpha` and its scopes only. `jig roadmap --phase alpha` prints both products' alphas.
- [ ] (type, state) `jig roadmap --type pilot` prints only `Familiar App Pilot A`. `--state open` drops every taken and done scope, and every phase left empty. `--state blocked` prints only open scopes with an unmet `after`.
- [ ] (owner) `jig roadmap --owner pb` prints only Familiar App's phases and `## Familiar App No phase`.
- [ ] (problems kept) With a dead `(touches …)` under `Familiar App`, `jig roadmap --product Walyt` still prints that problem and exits 1.
- [ ] (typo) `jig roadmap --product Walty` is refused, naming Walyt and Familiar App.
- [ ] (view) `jig roadmap --view --product Walyt` prints Markdown with Walyt's phases only, and ROADMAP.md is unchanged. `jig roadmap --write --product Walyt` is refused.
- [ ] (stand-alone) In the Part A repo, `jig roadmap --type prototype` prints `alpha` only.

All parts:
- [ ] (no regression) `python3 .jig/jig.py queue -- bash tests/smoke.sh roadmap family rig rig_batch sweep update moves boundary pararepo metarepo` passes, and so do `python3 .jig/jig.py queue -- .jig/scripts/check.sh` and `claude plugin validate ./plugin`.
- [ ] (docs) `docs/records.md` § Roadmap, `docs/commands.md` (roadmap's flags) and `docs/glossary.md` § Phase describe types and filters. `grep -n -E 'Prototype|--product' docs/records.md docs/commands.md docs/glossary.md` finds each.

## Out of scope
- `--label`: labels are roadmap-labels' spec. It adds the flag through this spec's filter (Decisions).
- Departures from a roadmap item. The owner, 2026-11-23: "not worth tracking, forget that part". The fold-in's `departed: <why>` stays as it is.
- Departures from a metarepo decision entry: they follow today's path for a change to a metarepo claim, unchanged (Decisions).
- Renaming any adopting repo's phases to the scheme: each repo makes that roadmap change itself.

## Touches
- `plugin/templates/jig/jig.py`:
  - Part A: `parse_roadmap` and a `phase_type`, the type-order check in the roadmap rules and `cmd_roadmap`'s problems, `_roadmap_full` (type), `render_roadmap` (type in headings).
  - Part B: `cmd_roadmap` and its parser (`--product`, `--phase`, `--type`, `--state`, `--owner`, `--view`), and one filter over `roadmap_full`'s result.
  - Reused, not copied: `product_of`, `Family`.
- `plugin/templates/jig/RULES.md`: Roadmap.
- `docs/records.md`, `docs/commands.md`, `docs/glossary.md`.
- `tests/smoke.sh`: roadmap, family.
- `marketing/FEATURES.md`: lives in the main checkout and isn't tracked. The row is under Decisions.
- Process or product: product (jig's behaviour), homed in RULES.md.
- No contract path: jig is not a pararepo.

## Alternatives considered
- A type marker on the phase (`Type: pilot`). Rejected: the owner defined the types by their names ("Prototype phase names are alpha, beta, gamma"), so a marker could disagree with the name. Reason is [seen].
- Filtered ROADMAP.md files per product. Rejected by the owner's answer 2, and a second tracked copy would drift. Reason is [seen].
- Departures shown across a family, or gated until reconciled. Rejected by the owner's two rulings of 2026-11-23 (Decisions). Reason is [seen].

## Decisions
- The owner, 2026-11-23, on departures: "Departing from a decision entry must be reconciled with the meta before merging and I'd prefer to use existing processes and ledgers than create a new one. Departing from a roadmap is not worth tracking, forget that part."
- The owner, 2026-11-23, overriding the first ruling's timing: "Forget what I said about before or after merge. How it would currently work now for a change to a decision entry is exactly how this should work too, no new requirements or processes."
  - So departures build nothing. A pararepo departing from a metarepo decision entry changes a metarepo claim, and goes as one goes today: the spec's `meta:` line, a BUFFER row or `jig propose`, then the metarepo's superseding entry and `jig sync`. RULES.md (Metarepo and pararepos) and `docs/metarepos.md` already say so (Givens), so no text is added.
- Decided by the owner, 2026-11-23, on this spec's questions (relayed by the hubnode):
  - Type order (item 3): "enforce Prototype, then Pilot, then Production within a product".
  - The view's filters (item 7): "filters print to the terminal; ROADMAP.md stays whole".
- Decided by the owner, 2026-11-23, on the review's should-fix 1 (an existing roadmap already out of type order, such as one with `Beta` after `Demos`, has every trunk roadmap commit refused once it updates, `jig update`'s own fold included), relayed by the hubnode: "Option 1". The order check covers the whole roadmap, not only the phases a commit adds or moves.
  - Applied by `jig update`: its dry run lists every phase out of type order, by line and type, as a warning to fix in the same update before `--apply` folds anything, and exits 1 as update does for any warning.
- Part order: A, then B, the first `--partial`, in one job. Both touch `cmd_roadmap` and the view.
- A name that isn't Greek or `Pilot <letter>` is Production, never an error: the owner said Production names "are chosen by the user".
- `--label` is roadmap-labels': whichever of the two specs lands second adds `--label` to this filter set (Kept separate).
- FEATURES row, for `marketing/FEATURES.md`:

  ```
  | Phase types and roadmap filters | A phase's type (Prototype, Pilot, Production) is read from its name: Greek letters, "Pilot <letter>", anything else; types run in that order within a product, refused out of order on trunk. `jig roadmap` and `jig roadmap --view` filter by product, phase, type, state and owning repo, to the terminal; ROADMAP.md stays whole. | owner, Nov 19 (maige-ecosystem's scope-ownership rounds); ruling Nov 23 ("end state was supposed to mean exactly that"); `.jig/specs/phase-types.md` | A family plans many products in one roadmap: "what's in Walyt alpha" has to be one command, and the stage a phase is in has to show without a convention to remember. | A type marker or config. A filtered copy of ROADMAP.md. Tracking departures: a departure from a metarepo decision is a claim change, on the existing path. |
  ```

## Open questions for the owner
1. Answered: "enforce Prototype, then Pilot, then Production within a product" (Decisions).
2. Answered: "filters print to the terminal; ROADMAP.md stays whole" (Decisions).

## Roles
- spec: tier 2, effort 2
- bug: tier 2, effort 1
- work: tier 2, effort 3
- review: tier 2, effort 2
- check: tier 3, effort 4
