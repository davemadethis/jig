# move-to-pararepo: a metarepo hands an entry or a page down to the pararepo that owns it

Source: maige-ecosystem hubnode session, bug role (claude-opus-5-5) / 2026-11-20 / Dave, on his word: "file a short jig feedback for moving entries and pages; leave them here meanwhile" (staged as feedback-maige-ecosystem-2026-11-20-move-entries-and-pages.md): "jig can't move a decision entry or a page from a metarepo down to the pararepo that owns it. A released entry can't leave the log at all, and a page that leaves reads as removed."

## Intent
A metarepo can move a decision entry (released or open), a page or a page's section to the
pararepo that owns it. One line in the log records the move. That line is the forwarding
address: frozen citations of the old id still resolve, `jig decision` names the new home, and
the release tells each pararepo "moved, now here", not "removed". This is the first version:
one line form, one helper that reads it, and the readers that today say "removed". The text
itself moves the way it can today, by staging.

## Investigation

**1. Why**

- Q: Why can't E-085 move to Maige-Lite? A: A released entry leaves only when an accepted entry in the same log supersedes it, or when it is struck as project scope. A move is neither.
- Q: Why can't a Maige-Lite entry supersede it? A: `status_parts` parses `Supersedes` with the log's own prefix only. Git's rename detection sees one repo's history.
- Q: Why does nothing else record it? A: Cross-repo paths go up (`jig propose`, BUFFER rows). Going down, jig has staging for the text, and no record of where a claim went. Root.


**2. Givens**

- [seen] The report's five steps, reproduced at trunk 6340aea in a throwaway metarepo `M` (`E-`) and pararepo `L` (`D-`, pinning v0.1.0). Every jig command ran with `JIG_CONFIG` and `XDG_CONFIG_HOME` under my scratch folder (script: `move-to-pararepo-repro.sh` in the hubnode's shared notes folder):
  1. A new `M` entry `Accepted (owner, 2026-11-20). Supersedes L/D-001.` is refused: "M2 … E-003 needs a status line under its heading".
  2. Removing E-001 from release v0.1.0 with the line `- E-001: moved to L as D-001.` under `## Unreleased` `### Removed` commits (rc 0). `struck_ids` (jig.py:5995) reads the id and ignores the text, though RULES.md:1082–1084 gives the strike one reason, project scope.
  3. `M`'s release v0.1.1 printed `L: staged .jig/staging/pin-bump-M.md (2 rewrites, 1 removed id)`. The request lists `battery.md` as a file "which M v0.1.1 doesn't have", `walyt.md § Mods` as a heading it "has no heading for", and `E-001 (removed): cited in docs/dock.md:3`. Nothing names a new home.
  4. `jig decision E-001` in `M` prints the entry and "E-001 was removed from .jig/decisions.md; it stood last at 79decaa, in v0.1.0." It names nothing that holds now.
  5. A new page in `M` saying "Per E-001." commits. `jig reading-list --claims E-001` lists it as a `copy`, under the note "no entry E-001 in .jig/decisions.md or in its history", which is wrong for a removed entry.
- [seen] `L`'s `jig sync` after that release prints `E-001: used in docs/dock.md` under "Changed, in this repo's terms", with no new home.
- [seen] The text can already be carried down. In `M`, a staged `kind: decisions` file with `target: L` and `### D-?battery one` / `Accepted (owner, 2026-11-01).` printed "forwarded move-e001.md to L's .jig/staging/". In `L`, `jig staging resolve` printed "1 entry added to .jig/decisions.md", with the status line (who and date) unchanged. A `D-?` id is refused on trunk (RULES.md, Ids), so it lands in a job and `jig merge` numbers it. Nothing records where it came from.
- [seen] maige-ecosystem trunk (5d9d084, read with `git --no-optional-locks`): E-029 (v0.3), E-058, E-073 (v3.0.0) and E-085 (v3.1.0) are accepted and released. E-058 says `Supersedes E-045.`, E-073 `Supersedes E-036.` and E-085 `Supersedes E-035.` So a pararepo citing E-035 hops to E-085 today (`hold_chain`, jig.py:6209), and after a move that chain would end at an id the log doesn't have.
- [seen] Released entries that stay cite moving ids: E-039, E-057 and E-094 (the report's table; E-039, E-057 and E-094 are on maige-ecosystem trunk). Released text is frozen (RULES.md:1073–1081), so those citations can't be rewritten. A moved id has to keep resolving from the log alone.
- [seen] maige-ecosystem's existing strike lines are exactly `- E-001: project scope, not a product decision.` and `- E-041: project scope, not a product decision.` Checking the strike's reason would refuse neither.
- [seen] Maige-Lite (4aae823) cites E-017, E-029, E-044 and E-058 bare, in its log, specs and its board page. Its prefix is `D-`, so a bare `E-` id is a citation of the metarepo (RULES.md:1418–1424).
- [seen] Open entries leave the log freely (`removed_entries`, jig.py:5978), but `stage_pin_bumps`' `gone` set (jig.py:8392) holds every id the old tag had and the new one lacks, Open ones included. So E-017, E-043 and E-044, moved by deletion alone, would read `(removed)` too: the same symptom.
- [seen] A released section's change lines are frozen (`frozen_problems`, jig.py:6024). A move line written under `## Unreleased` `### Removed` becomes part of its release's section and stays in the log for good. A map from the log's text alone needs no git history.
- [seen] A pointer is `<repo>/<path> § <section>` (RULES.md:1323–1339). `POINTER` (jig.py:8697) parses it, and `pointer_gap` (jig.py:8786) checks a path and heading against a file's text.
- [seen] `peer_logs` (jig.py:6457) and `meta_checkout` (jig.py:7588) read another repo's trunk through `repo_path` (jig.py:7322). The held `cross-repo-roadmap` spec reads the metarepo's roadmap the same way.
- [assumed] The metarepo's hubnode can reach the receiving pararepo's checkout through `jig repos`. That holds on this machine (all four Maige repos are registered with paths). Where it can't, the move line passes with a warning (Change 2), so nothing depends on it.


**3. One layer up**

- **The sibling inside one repo.** A page rename reads `(now <new>)` in the pin bump through `git diff -M` (jig.py:8362). A glossary term reads "moved". A superseded id hops to its successor. Each forwarding address lives in one repo's history or log. A move across repos has no history to read, so it writes its address down, in the log.
- **The existing pattern.** The strike line is already a `### Removed` line that lets an entry leave a release. The move line is its sibling: same group, same id-first shape, with a pointer for the reason.
- **The other direction.** Claims go up through `jig propose` and BUFFER rows and are recorded on the metarepo's side. This is the same idea pointing down: the metarepo, which loses the claim, writes where it went.


**4. Correction**

A correction. The move gets a record that jig reads, written by the repo that loses the claim. A
workaround on the readers, such as treating every removed id as "maybe moved", can't name a new
home. Writing the move as a strike passes the hook today and states a false reason, so Change 2
closes that.

## General?
- **Any metarepo.** Yes. Any claim that turns out to have one owner is meant to live with that
  owner (RULES.md, What the metarepo holds). Once it is released, or cited by released text,
  jig has no way to get it there without every pararepo reading it as removed.
- **A stand-alone repo or a pararepo.** No. Inside one repo a move already leaves an address,
  as One layer up says. Moving a claim up or sideways is out of scope.

## Change — first version

1. **The move line.** In the metarepo's log, under `## Unreleased` `### Removed`, one line per
   moved thing. The target is a pointer, in the form a pararepo cites with:
   - an entry: `- E-085: moved to Maige-Lite/.jig/decisions.md § D-016.`
   - a page: `- docs/products/walyt/battery.md: moved to Maige-Lite/docs/battery.md.`
   - a section: `- docs/products/walyt/walyt.md § Mods: moved to Maige-Lite/docs/walyt.md § Mods.`

   The repo named must be one of `meta.json`'s `pararepos`. A move line for a released entry
   lets it leave its release, as a strike line does. An Open entry or a page needs no
   permission to leave, and the line is its address.
2. **The hook checks it.** On a commit that adds a move line, the hook:
   - refuses a repo that isn't in `pararepos`;
   - reads that repo's trunk through `jig repos` and refuses a target id, page or heading
     that isn't there, naming the file it read;
   - warns, naming the repo, when the repo can't be reached;
   - refuses a moved entry or page the metarepo still has, as it refuses a strike of an entry
     still in the log.

   It also checks the strike's reason. An added `### Removed` line that lets a released entry
   leave must be `- <id>: project scope, not a product decision.` or a move line. Any other
   text is refused, and the refusal names both forms.
3. **One reader.** A helper reads every move line in a log's text, in any section, into a map
   from the old id, path or path § heading to its pointer. These use it:
   - `hold_chain` and `holds_now`: a chain that reaches a moved id ends at its pointer, so
     E-035 → E-085 → `Maige-Lite/.jig/decisions.md § D-016`.
   - `jig decision E-085`: after "was removed", it prints "moved to <pointer>".
   - `jig reading-list --claims E-085`: its note names the move in place of "no entry … in its
     history".
   - `stage_pin_bumps`: a gone id with a move prints `E-085 (moved: <pointer>): cited in …`,
     never `(removed)`. A citation of a moved page or heading ends `: now <pointer>`, as a
     rename's does. In the receiving pararepo itself, the pointer is its own path
     (`now docs/battery.md, this repo`). The release's count line says `n moved`.
   - `meta_citations` and `jig sync`'s "Changed" list: a moved id or page reads
     `(moved: <pointer>)` with its uses.
4. **RULES.md**, four places:
   - Released sections: the move line beside the strike line, and the strike's one reason.
   - What the metarepo holds: moving a claim down to its one owner. The pararepo lands the
     text first, through staging. Its entry keeps who and date and drops a `Supersedes` of
     the metarepo's ids, since that chain stays in the metarepo's log. The metarepo then
     removes it, with the move line, in one commit.
   - A pin-bump request: a moved id or path is listed with its new home.
   - Versioning: a move with no change in meaning is Z, as a file move is.

The order is fixed by the check: the receiving entry or page has to be on the pararepo's trunk
before the metarepo's commit can name it.

## Done when
Fixture: a throwaway metarepo `M` (`decision_prefix` `E-`, `pararepos` `["L"]`) and pararepo `L`
(`D-`), both in `jig repos`, every jig command run with `JIG_CONFIG` and `XDG_CONFIG_HOME` beside
the repos. `M` releases v0.1.0 with E-002 (accepted, `Supersedes E-001.`, E-001 removed in that commit),
E-003 (accepted, citing E-002 in its body), `docs/products/walyt/battery.md`, and
`docs/products/walyt/walyt.md` with a `## Mods` section. `L` pins v0.1.0, and its `docs/dock.md`
cites `M/.jig/decisions.md § E-002`, a bare `E-001`, `M/docs/products/walyt/battery.md` and
`M/docs/products/walyt/walyt.md § Mods`.

- [ ] **The strike has one reason.** `M`'s commit removing E-002 with `- E-002: moved to L as D-001.` is refused, and the refusal names the strike line and the move line. `- E-002: project scope, not a product decision.` still passes. (Today the first passes: the first Given, step 2.)
- [ ] **The text lands first.** A `kind: decisions` file staged in `M` with `target: L` forwards to `L`, lands in a job there and merges as `D-001`, with E-002's who and date unchanged. The same with a `kind: doc` file lands `docs/battery.md` and a `docs/walyt.md` with `## Mods`.
- [ ] **The move line is checked.** In `M`, removing E-002 from v0.1.0, deleting `battery.md` and removing `## Mods`, with move lines naming `L/.jig/decisions.md § D-001`, `L/docs/battery.md` and `L/docs/walyt.md § Mods`, commits. Each of these is refused, naming `L`'s file: a move line naming `§ D-009`, which `L` lacks; one naming `L/docs/nope.md`; one naming `§ Nope`; one naming a repo not in `pararepos`. With `L` dropped from the repos file, the good commit passes with a warning naming `L`.
- [ ] **History reads the move.** `jig decision E-002` in `M` prints the entry, "stood last … in v0.1.0", and `moved to L/.jig/decisions.md § D-001`. `jig decision E-001` walks E-001 → E-002 → the move. `jig reading-list --claims E-002` names the move in its note.
- [ ] **Frozen citations still pass.** E-003, which cites E-002, is unchanged, and `M`'s log check passes.
- [ ] **The symptom is gone.** `M`'s release stages `L`'s pin-bump request, in which E-002 and E-001 are each `(moved: …)` with `L`'s own path, and `battery.md` and `walyt.md § Mods` each end `: now docs/battery.md, this repo` and the like. It has no `(removed)`, no "doesn't have" and no "has no heading for". The release prints `L: staged … (… moved)`. Today it prints `(2 rewrites, 1 removed id)`. `L`'s `jig sync` lists E-002 with `(moved: …)`.
- [ ] **No regression.** `python3 .jig/jig.py queue -- bash tests/smoke.sh moves decisions supersede removals pin_bump pararepo staging claims` passes (`moves` is the new section holding the checks above), and so does `claude plugin validate ./plugin`.

## Out of scope
- **Which entries and pages move, and when.** Dave's call, made in maige-ecosystem. Meanwhile they stay there, by his word.
- **A record on the receiving side.** The landed entry may say "Moved from maige-ecosystem E-085." in its body. jig doesn't parse it, and `jig decision D-016` doesn't name an origin: the metarepo's line is the one record, and the check at Change 2 already ties the two ends.
- **Listing live citations in the move commit.** `jig reading-list --claims <id>` lists every line naming the id already, and a metarepo spec that changes a claim starts from it (RULES.md, Every copy). With Change 3 its note names the move.
- **Where Open questions should live** (the report's ideas log). That is the held `cross-repo-roadmap` work. An Open entry that moves now takes the move line like any other (Open question 1).
- **Moving a claim up, or between two pararepos.** Up already goes through `jig propose` and BUFFER rows. Sideways can be asked for when a case comes up.
- **One command that does both ends.** This version is two commits, a job in the pararepo and a commit in the metarepo, checked by the hook.
- **A stub page left at the old path.** The move line is the address. A stub would be a page with no claim of its own.

## Touches
- `plugin/templates/jig/jig.py`:
  - `struck_ids`, `removed_entries` and `frozen_problems`: the move line lets a released entry leave; the strike's reason is checked;
  - a new move-line helper, and the hook check of its target, through `repo_path` as `peer_logs` reads a peer;
  - `hold_chain`, `holds_now`, `cmd_decision` and `claims_of_id`: the hop to a move;
  - `stage_pin_bumps`, `meta_citations` and `changes_report`: a moved id or path with its new home.
- `plugin/templates/jig/RULES.md`: Decision log (Released sections); Metarepo and pararepos (What the metarepo holds, A pin-bump request); Versioning (Z).
- `tests/smoke.sh`: a new `moves` section; `decisions`, `supersede`, `removals`, `pin_bump`, `pararepo`, `staging` and `claims` rerun.

## Alternatives considered
- **A cross-repo `Supersedes Maige-Lite/D-016.`** — rejected because a move isn't a reversal: a supersede asks for a `**Breaking:**` line and reads as a change of decision (RULES.md:1073–1078), and `status_parts` would have to read every repo's prefix — reason is [seen].
- **A `### Moved` group** — rejected because the groups are Keep a Changelog's (RULES.md:1043), and `### Removed` is already the group whose id-first line lets an entry leave a release (jig.py:5995) — reason is [seen].
- **A move line of its own form, `- E-085: moved to Maige-Lite D-016.`** (the report's) — rejected because the pointer form is what a pararepo cites with, `POINTER` and `pointer_gap` already parse and check it, and one form then covers ids, pages and sections — reason is [seen].
- **A record at both ends, with the receiving entry's origin parsed and checked** (the report's Change 1 and 4) — rejected for this version because the metarepo's line, checked against the pararepo's trunk, already ties the two ends, and the body can say where the text came from in words — reason is [assumed]: nothing yet needs jig to read the origin.
- **Listing every live citation in the move commit** (the report's Change 5) — rejected because `jig reading-list --claims` already lists them and the Every copy rule already sends a claim change there — reason is [seen].
- **Rewriting every citation in the move commit** — rejected because the released entries citing moved ids (E-039, E-057, E-094) are frozen — reason is [seen].
- **Reading the move from git history, as a supersede is** — rejected because a move crosses repos, so one repo's history can't show it, and a frozen change line in the log persists anyway — reason is [seen].

## Decisions
- The metarepo writes the move, not the pararepo: it is the repo losing the claim, the one whose readers see "removed", and the one whose release builds the pin bump.
- Open entries and pages take the same line. They need no permission to leave, but without it the pin bump reads them as removed (Givens).
- Shares a mechanism with the held `cross-repo-roadmap` spec: both read another repo's trunk live through `jig repos` (`repo_path`, as `peer_logs` and `meta_checkout` do). Neither waits on the other. Whichever lands second reuses the first's read helper if one exists by then. This spec doesn't change that one.

## Open questions for the owner
1. **The Open entries E-017, E-043 and E-044.** Move them with the same move line now, or wait for the held roadmap work's ideas log? Recommend: the move line now. It costs nothing extra, and without it their frozen citations in E-039 and E-057 read "removed" in Maige-Lite's pin bump.
2. **An unreachable or missing target.** When the pararepo can be reached and lacks the target, the commit is refused. When it can't be reached, the commit warns. Is that the line you want, or warn in both cases? Recommend: refuse when reachable. Once released, the move line is frozen, so a wrong address could never be corrected.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
