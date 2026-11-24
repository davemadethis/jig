# bug-board-name-follows-registry: a repo's board name doesn't follow the name it is registered under

Source: zencad hubnode session / 2026-11-24 / Dave (owner) (staged as feedback-zencad-2026-11-24-board-name-follows-registry.md): The board kept `"name": "zenshape"` in the repo's `.jig/config.json` until it was edited by hand. Also noticed: `jig repos` has `add` and `rename` but no way to remove an entry, so removing one meant editing repos.json by hand.

## 1. Why
- Q: Why did the board keep the old name? A: `cmd_repos` (`add`, `rename`) writes only repos.json. Nothing in it touches the checkout's `.jig/config.json`.
- Q: Why was it built that way? A: On Oct 29 a listed name was a per-machine label. The repos skill says "A rename is an alias in this list only", and the repo's own committed name kept finding it.
- Q: Why does that fail now? A: No rule links the two names, and no command changes a repo's own name. Lookups match both, which hides the mismatch until someone reads the board. Root.
- Q (remove): Why edit repos.json by hand? A: The only actions are `add`, `rename`, `alias` and `which`. `add` refuses while the stale entry answers to the checkout's own name, so the stale entry has to go first. Root.

## 2. Givens (line numbers at trunk fcd1b92, `plugin/templates/jig/jig.py`)
- [seen] Reproduced in a throwaway repo, with `JIG_CONFIG`/`XDG_CONFIG_HOME` set outside it. I ran
  `jig init` in `oldname`, committed, and ran `jig repos add repo` (entry `oldname`). Then I renamed
  the folder to `newname`. `jig repos add repo --name newname` is refused: "… newname calls itself
  oldname, which already names oldname, …/oldname: change `name` in one checkout's
  .jig/config.json, or list only one of them". `jig repos remove newname` is rejected by argparse.
  After an emptied repos.json (the report's hand edit), `jig repos add repo --name newname`
  registers it, but `.jig/config.json` still says `"name": "oldname"`, with `git status` clean.
  `jig repos which oldname` and `which newname` both print the checkout.
- [seen] `cmd_repos` (8227-8302) writes repos.json through `save_repos` and nothing else. The
  parser's actions are `add, rename, alias, which` (18809).
- [seen] `repo_matches` (8193) finds an entry by its listed name, its aliases, or `repo_identity`
  (8175), which is the checkout's config.json `name`, a legacy board's name, and meta.json's
  `name`. So both names find the repo, and nothing reports that they differ.
- [seen] The board's `name` is what other code treats as the repo's identity.
  `this_repo_names` (10236) reads the trunk checkout's config. A staging forward uses `me` (10736)
  and compares it, exactly, with a metarepo's `pararepos` (10741). The roadmap's `me` (12220) uses
  it when there's no meta.json. Init writes it from the folder name (895).
- [seen] The board is edited on trunk only (R5, RULES.md:94). jig commands that rewrite it outside
  a merge write config.json in the trunk checkout and `git add` it, leaving the commit to the owner:
  `jig update --merge-log` (16287-16291: "Staged, nothing committed: commit it on {trunk}") and
  `jig update --apply` (15249-15253). Hooks and gates read trunk's committed copy
  (`Board.load`, 248).
- [seen] The current promise. RULES.md:1615-1622 says a typed repo name is a listed name, an alias, or
  the checkout's own name. The repos skill says "A rename is an alias in this list only. The repo's
  own name still finds it, so a pararepo citing a metarepo you renamed keeps working." Smoke
  `sec_repos` (tests/smoke.sh:2076) asserts that the old name still finds a renamed entry.
- [seen] The owner's word in the report: "the board always catches up to jig config". Removing an
  entry leaves the board name alone. Registering under a name sets the board's `name`, "in a
  commit on trunk or as a change for the owner to commit".
- [seen] Family names are committed in other files. A pararepo's `para.json` `meta` cites the
  metarepo by meta.json's `name` (exact compare, 10746). The metarepo's `pararepos` lists each
  pararepo by name, found through `repo_path` (`name_in_family`, 17638).
- [assumed] The report's `jig_version` 78b2f6443204 is older than fcd1b92. The code above is
  unchanged in that area. Converted: the reproduction ran on fcd1b92's `jig.py` and shows the same
  behavior.

## General?
Yes. Any repo that is renamed (on its host and its folder) and registered again goes through
these same steps. The stale entry blocks the re-add, so it has to be removed, and there is no
command for that. The board then keeps the old name, and jig's own output (staging forwards, the
roadmap's owner) keeps using it. Nobody has to work against jig to get there, and every kind of
repo (regular, meta, para) has a board `name`. What jig promises about names after this fix:
- A repo's listed name in `jig repos` is its name. Registering or renaming an entry sets the
  board's `name` to match.
- An alias is a shorthand. It never touches the board.
- Removing an entry changes nothing in the checkout.
- The name the board gave up becomes an alias of the entry, so text that still cites it (a
  staged target, an inbox `to`, a metarepo's `pararepos`, an `Owner:` line) keeps finding the repo
  on this machine. That is the property the rename promise protected.

## 3. One layer up
- Sibling paths: `alias` also changes what an entry answers to. It has the right behavior already
  (a shorthand, board untouched) and keeps it. `add` in its first form (`add <name> <path>`) gives
  an entry its listed name the same way `add repo --name` does, so it gets the same rule.
- What's structurally different: repos.json is per machine and the board is committed. Every
  other board write respects that by writing the trunk checkout and staging it. `cmd_repos` never
  writes there.
- Patterns to reuse: the merge-log write-and-stage on trunk (16287-16291), `repo_names`/`aliases`
  for keeping the old name, and `repos_alias`'s lookup (a listed name or alias) for `remove`.

## 4. Correction
A correction. `cmd_repos` gets one rule linking the listed name to the board, and the missing
`remove`. A warning that the names differ would leave the hand edit in place, which is the
symptom the owner rejects.

## Intent
The board's `name` follows the name a repo is registered under. When `jig repos add` (either
form) or `jig repos rename` leaves an entry with a listed name different from its checkout's board
`name`, jig writes the new name into that checkout's `.jig/config.json` and stages it, provided the
checkout is on its trunk. The old board name joins the entry's aliases. Aliases and removal never
touch the board. `jig repos remove <name>` deletes an entry by its listed name or an alias.

## Change
1. **Board catch-up** (one helper, called after `save_repos` in `add` and `rename`). The checkout
   is the entry's path. It has to hold `.jig/config.json`, be a git repo, and be on its trunk
   branch (`Board.trunk_name`). If the board's `name` differs from the listed name, jig sets
   `name` and leaves every other key as it is. It writes the file and runs `git add` on it in that
   checkout, then prints `<path>/.jig/config.json: name <old> → <new>. Staged, nothing committed:
   commit it on <trunk>.` A checkout that isn't on its trunk is still registered. jig writes
   nothing there and prints one line saying the board still says `<old>`, and that re-running the
   same `jig repos add`/`rename` on `<trunk>` brings it in line (re-adding is idempotent). A
   checkout with no board, or that isn't a git repo, gets no write and no line.
2. **The old name stays findable.** When the board's name changes, the entry gains the old name as
   an alias. An alias equal to the entry's own listed name is dropped, so renaming back and forth
   doesn't list a name twice.
3. **`jig repos remove <name>`** takes a listed name or alias (case ignored, the same lookup as
   `repos_alias`) and deletes that entry. It prints `removed <name> (<path>)` and nothing in the
   checkout changes. An unknown name is refused with `unknown_repo`'s text.
4. **Refusals name the command.** `refuse_own_names` (8318) and `unknown_repo`'s "remove one entry
   from {repos_file()}" (8160) name `jig repos remove <entry>` in place of a hand edit.
5. **Text.** RULES.md's typed-name paragraph (1615-1622) states the four promises above (General?).
   The command list line (1987) gains `remove <name>`. `plugin/skills/repos/SKILL.md` replaces
   "A rename is an alias in this list only…" with the board rule, and adds `remove`. The
   `jig repos` help text (18809-18812) gains `remove`.

## Done when
- [ ] The fix fires, in `sec_repos`. In a git repo on `main` whose committed board says `rp`,
  `jig repos add repo --name tools` leaves `.jig/config.json`'s `name` as `tools`, and
  `git diff --cached --name-only` lists `.jig/config.json`. HEAD is unchanged, and the output says
  `Staged, nothing committed`. `jig repos` lists `tools` with alias `rp`, and
  `jig repos which rp` prints the checkout.
- [ ] `jig repos rename tools2` there sets the board's `name` to `tools2` the same way, and the
  entry's aliases are `rp` and `tools`. `jig repos rename tools` back lists `tools` with aliases
  `rp` and `tools2`, never `tools` itself.
- [ ] `jig repos alias tools t` leaves `.jig/config.json` byte for byte as it was.
- [ ] The report's sequence no longer needs a hand edit. Entry `old` is registered for a committed
  board named `old`, then the folder is moved. `jig repos add repo --name new` is refused, naming
  `jig repos remove old`. `jig repos remove old` deletes the entry and changes nothing in the
  checkout. Then `jig repos add repo --name new` leaves the board's `name` as `new`, staged.
- [ ] Off trunk: with the checkout on branch `x`, `jig repos add repo --name other` registers
  `other`, leaves `.jig/config.json` unchanged, and prints the line naming the board's current
  name and `main`.
- [ ] `jig repos remove nosuch` exits 2 with `unknown_repo`'s text. `remove` by an alias deletes
  the entry the alias names.
- [ ] The existing `sec_repos` observables pass, including "repos rename: the repo's own name
  still finds it".
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh repos` and
  `python3 .jig/jig.py queue -- .jig/scripts/check.sh` pass. The complete smoke is the gate's.

## Out of scope
- Family names in committed files stay as they are. In a metarepo, meta.json's `name` is the
  family's name, which every pararepo's `para.json` `meta` cites exactly (10746). Only
  config.json's `name` follows the registry. A renamed pararepo's old name stays in its
  metarepo's `pararepos` until the metarepo's hubnode changes it. The staging forward's existing
  refusal ("doesn't list <name> as a pararepo: add it there first", 10741) already names the
  fix, and the alias from Change 2 keeps the old name resolving meanwhile. Rewriting another
  repo's files from `jig repos` would edit a repo the command wasn't run in.
- Entries that already differ from their board (registered before this fix) catch up the next
  time they're added or renamed. The list doesn't flag them, because a name chosen as a label
  under the old rule isn't wrong until its owner re-registers.
- Committing the board change. jig stages it and the owner commits on trunk, as merge-log does.
- Two machines registering one repo under different names would each restage the board. R0, one
  user: not reported.

## Touches
- `plugin/templates/jig/jig.py` (`cmd_repos`, a board catch-up helper, `repos remove`,
  `refuse_own_names`, `unknown_repo`, the `repos` parser)
- `plugin/templates/jig/RULES.md` (the typed-name paragraph in Staging/Inbox; the command list)
- `plugin/skills/repos/SKILL.md`
- `tests/smoke.sh` (`sec_repos`)
- `.jig/decisions.md` (Unreleased: a `### Fixed` line for the board name, an `### Added` line for
  `repos remove`)
- `marketing/FEATURES.md` (the `jig repos` and `/jig:repos` rows: `rename` no longer just gives
  an alias, and `remove` is added. The file is gitignored, so it's edited in the main checkout.)

## Alternatives considered
- A `jig repos` warning when an entry's listed name differs from its board's (a workaround at
  the symptom). Rejected because the owner still hand-edits the board, and the owner's words are
  "the board always catches up to jig config". This reason is [seen] (the report).
- Commit the board change on trunk from `jig repos`. Rejected because every board rewrite outside
  a merge writes and stages, leaving the commit to the owner on trunk, and the owner's words allow
  "a change for the owner to commit". This reason is [seen] (16287-16291, 15249-15253, the report).
- Change the board's name without keeping the old one as an alias. Rejected because committed
  text in other repos and staged files cites a repo by its old name, and the rename promise (smoke
  2076) is that the old name keeps finding it. This reason is [seen].
- Also rewrite meta.json's `name` in a metarepo. Rejected because every pararepo's `para.json`
  cites it exactly (10746), so one repo's rename would break its whole family. This reason is
  [seen].
- Write the board in any checkout, on any branch. Rejected because R5 edits the board on trunk
  only, and hooks read trunk's copy, so a write on a job branch would be refused or lost. This
  reason is [seen] (RULES.md:94, `Board.load` 248).

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
