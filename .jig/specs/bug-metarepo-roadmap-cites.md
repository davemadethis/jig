# Bug: `jig sync` checks a metarepo roadmap cite against a pin cache that never holds the roadmap

Source: maige-ecosystem hubnode session for Maige-OS, 2026-11-19 (staged as feedback-maige-ecosystem-2026-11-19-cross-repo-roadmap.md): `jig sync` reports a cite of the metarepo's `.jig/roadmap.md` as a file the release "doesn't have" — "cites maige-ecosystem/.jig/roadmap.md, which maige-ecosystem v3.1.0 doesn't have", at `.jig/ledgers/DEFERRED.md:229`, `.jig/specs/buffer-b1-b4.md:15` and `:16`.

## Intent

A pararepo's cite of its metarepo's roadmap (`<meta>/.jig/roadmap.md`, `<meta>/ROADMAP.md`) is
checked against the roadmap on the metarepo's trunk, read live, so a heading that's there
resolves and one that isn't is "has no heading for". A buffer proposal spec's copies of BUFFER
rows are history and aren't checked; the BUFFER row itself still is.

## 1. Why

- Q: Why does sync say v3.1.0 doesn't have `.jig/roadmap.md`? A: `meta_citations` reads the pin
  cache, which has no such file, so `pointer_gap` gets no body and returns NO_FILE.
- Q: Why isn't it in the cache? A: `fill_cache` copies `entry_paths(pin)` and `CHANGELOG.md`, and
  `is_entry` drops every `.jig/` path but `.jig/decisions.md`. The roadmap isn't a contract.
- Q: Why read a roadmap cite at a pin at all? A: Nothing tells the roadmap apart. It's project
  data the metarepo changes on trunk and can't release alone, so a pin is the wrong place to read
  it. Root.

## 2. Givens

- [seen] Reproduced at this trunk (36787df, 0.15.0) in a throwaway `meta` (v0.1.0, `.jig/roadmap.md`
  with `## Up next`) and `para` pinned to it. `jig sync` on `para`'s trunk printed
  `.jig/specs/t.md:3 cites meta/.jig/roadmap.md, which meta v0.1.0 doesn't have` for a line citing
  both `§ Up next` (exists) and `§ Nowhere` (doesn't). The two collapse into one line because
  NO_FILE drops the section. It printed the same for a DEFERRED row citing `§ Up next`, and
  "doesn't have" for `meta/ROADMAP.md`.
- [seen] `para`'s cache held only `PIN`, `docs/glossary.md` and `.jig/decisions.md`. Maige-OS's
  `.jig/meta-cache/` (read only) holds `PIN` (v3.1.0), `.jig/decisions.md` and 39 files under
  `docs/`. No roadmap.
- [seen] A scratch patch in `para`'s copy of jig.py (4 lines, `meta_text` reading `ROADMAP` and
  `ROADMAP_VIEW` from `git show <Board.trunk_name(loc)>:<path>` in `loc`) made sync print nothing
  for `§ Up next` or the DEFERRED row, and print `cites meta/.jig/roadmap.md § Nowhere, which meta
  v0.1.0 has no heading for`. A `## Nowhere` committed on `meta`'s trunk with no release then
  resolved. The message still named the pin, which is wrong for a live read.
- [seen] Release side: `meta_citations`' `at` mode (used by `stage_pin_bumps`) reads the tag's whole
  tree, so it does read the roadmap at a tag. Called directly, before the patch, it gave nothing
  at v0.1.5 and `§ Nowhere … has no heading for` at v0.2.0 (heading removed between them). That
  is a pin-bump request for a cite a pin bump can't fix. With the patch, both tags read trunk,
  give the same line, and `stage_pin_bumps`' `key` skips it (`was`).
- [seen] Both of sync's callers (jig.py:7647 pararepo release, :8249 `sync_meta`) pass `loc`, the
  checkout `jig repos` registers. Sync fetches only tags (`git fetch -q --tags`), so "live" means
  that checkout's trunk branch as it stands. For maige-ecosystem that is its own working checkout
  (`/…/Maige-Eco`, `jig repos`).
- [seen] On maige-ecosystem's main (6dad871) and at v3.1.0, `.jig/roadmap.md` has `## Deliver to
  maige-os` (line 10) and `## Up next` (81). Maige-OS's three lines cite exactly those: L-318
  `§ Up next`; B3 `§ Deliver to maige-os`; B4 `§ Up next`. So the live read alone clears all
  three.
- [seen] Maige-OS's `.jig/ledgers/BUFFER.md` rows B3 and B4 are **Closed** (lines 15–16), so their
  proposal was released and sync closed them. `buffer-b1-b4.md` still carries B3 and B4 as `Open`
  copies, and `closed_row` exempts only `BUFFER.md` lines, so the copies are checked.
- [seen] A pararepo's spec that names a metarepo proposal is never closed: `finished_specs` keeps it,
  "it names a metarepo proposal or pointers branch `jig sync` follows" (jig.py:10047; RULES.md:843–845).
  A released buffer proposal's copied rows keep citing the pin they were proposed at, and those
  are the very claims the release was asked to change. Every released proposal leaves cites that
  will dangle.
- [seen] A copy is a copy: `proposed_copy` (jig.py:7167) reads the rows a spec lists under
  `## Buffer rows` "as they read when proposed". The live claim is the BUFFER.md row, which
  `meta_citations` checks while it is Open.
- [seen] DEFERRED rows are a work list, not a frozen note. `/jig:retro` re-ranks them when their
  scope closes, "take, or reject with a reason" (plugin/skills/retro/SKILL.md:19–20), and
  `used_in` counts ledgers as this repo's use on purpose (jig.py `used_in`).
- [seen] `is_entry` and `closed_row` are unchanged between Maige-OS's copy (87a18a359f74) and
  0.15.0 (the report's line map, re-checked against this source).
- [assumed, Maige-OS's] The notices fired at v3.0.0 too. Not converted; nothing here depends on it.

## 3. One layer up

- **Sibling read:** `meta_citations`' `at` mode reads the roadmap at a tag, and sees it, but at the
  wrong time: a tag's roadmap lags trunk. Both modes get one rule: the roadmap is read on trunk.
- **Sibling exemption:** `closed_row` leaves Closed BUFFER rows out as history. A buffer
  proposal's copies are the same rows frozen at proposal time, so they get the same treatment. The
  Open BUFFER row stays checked, so nothing live is lost.
- **Not a sibling:** handoffs are left out because they are frozen notes. DEFERRED rows look like
  that (written with a handoff) but they are triaged and taken later. They stay checked.
- **Existing pattern for "read the other repo live":** Issue 1's `Scope:` lines in the same report
  read the metarepo's roadmap on its trunk through `jig repos` (R6). Same read.

## 4. Correction

A correction. Today the roadmap is checked where it can't be (the pin cache) and checked at a tag
where it lags (the release). After the fix it's read from the one place it's current. A buffer
proposal's copies stop being treated as live claims.

## General?

Any pararepo that cites its metarepo's roadmap (a spec, a page, a DEFERRED row) gets a false
"doesn't have" on every sync today, and a real missing heading is hidden behind it. Any pararepo
that uses the sync buffer gets, after each released proposal, a cite notice for every claim the
release fixed, forever, because the proposal's spec is never closed. Both come from using jig as
RULES.md describes, with no unusual policy. General.

The report's change 3, DEFERRED half, is **not** taken: a DEFERRED row is live work (retro takes
some), so a cite there that dangles is worth fixing, and the live read already clears Maige-OS's
L-318. The buffer half **is** taken, as above, and widened to every listed copy (not only Closed
ones): the BUFFER row is the claim and is checked, so checking the copy too only repeats it.

## Change

1. **The roadmap is read live.** In `meta_citations`, both modes: a cite of `ROADMAP`
   (`.jig/roadmap.md`) or `ROADMAP_VIEW` (`ROADMAP.md`) reads `git show <trunk>:<path>` in the
   metarepo checkout (`loc`; `<trunk>` is `Board.trunk_name(loc)`). That is not the cache and not
   the tag. Its message names `<meta> <trunk>`, not the pin ("which maige-ecosystem main has no
   heading for"), so a reader knows a pin bump won't change it. It still checks the heading, so a
   missing one is reported. The release gets this for free: both tags read the same trunk, so a
   roadmap cite never selects a pin-bump request.
2. **A buffer proposal's copies are history.** In a file under `.jig/specs/`, a table row whose
   first cell is an id the spec lists under `## Buffer rows` is left out, as a Closed BUFFER row
   is. One predicate beside `closed_row`, which can reuse `listed_rows`.
3. **The cache is unchanged.** The roadmap stays out of `fill_cache`, `pointers()` and P2: it is
   project data, not a contract, and P2's answers (a BUFFER row, a proposal) don't fit it.
4. RULES.md, **Citing the metarepo** (RULES.md:1482–1487): a cite of the metarepo's roadmap is read
   on its trunk, not at the pin; a buffer proposal's copied rows are left out with handoffs and
   Closed BUFFER rows.

## Done when

All in `tests/smoke.sh`, with `JIG_CONFIG`/`XDG_CONFIG_HOME` set as the sections already do.

- [ ] (fix fires) `pararepo`: a `para` spec line citing `` `meta/.jig/roadmap.md § Up next` `` (the
  heading exists) prints no cite line from `jig sync`. One citing `§ Nowhere` prints
  `cites docs/.jig/roadmap.md § Nowhere, which docs main has no heading for` (the section's
  metarepo is `docs`), not "doesn't have".
- [ ] (live) A `## Nowhere` committed on the metarepo's trunk, with no release: the same cite then
  prints nothing.
- [ ] (no regression) A cite of a metarepo page that is truly absent at the pin still prints
  "doesn't have" with the pin (the existing case at smoke.sh:1637 still passes).
- [ ] (release) `pin_bump`: a roadmap heading a pararepo spec cites, removed between two metarepo
  releases, stages no pin-bump request for that cite.
- [ ] (copies) `sync_buffer`: a buffer proposal spec whose `## Buffer rows` lists B1, with B1's
  copied row citing a metarepo page the pin lacks, prints nothing for the spec's line. The same cite
  on BUFFER.md's Open B1 row still prints "doesn't have".
- [ ] (DEFERRED stays checked) A DEFERRED.md row citing a metarepo page the pin lacks still
  prints "doesn't have".
- [ ] (symptom gone) On Maige-OS's trunk after `/jig:update` to the fixed jig, `python3 .jig/jig.py
  sync` prints none of the lines for `DEFERRED.md:229`, `buffer-b1-b4.md:15`, `:16`. That is the
  owner's check in Maige-OS; jig's sessions don't run it there (read-only).
- [ ] `check` and the `pararepo`, `pin_bump` and `sync_buffer` smoke sections pass.

## Out of scope

- A process for moving an item between a page, a spec and a scope. None of the three lines was a
  move (Maige-OS's finding, re-checked above). A separate request if the owner wants one.
- Issue 1 (one roadmap across repos). How this fits it: Issue 1 reads the metarepo's roadmap on
  its trunk through `jig repos`, the same read as Change 1, so whichever lands second reuses the
  other's helper. Once pararepos have no roadmap of their own, every roadmap cite is a
  `<meta>/.jig/roadmap.md` one and this check covers its headings. Issue 1's scope ids are
  checked by Issue 1's own rules, not here.
- NO_FILE dropping the section from its message, so two cites of one missing file on one line
  collapse into one. Cosmetic, and with the roadmap read live it no longer hides anything here.
- Fetching the metarepo's trunk before the read. Sync fetches tags only; the registered checkout's
  trunk is what the owner works on (for a metarepo, its own checkout).

## Touches

- `plugin/templates/jig/jig.py`: `meta_citations` (both `meta_text`s, the NO_FILE/NO_HEADING
  message for a roadmap cite, the per-line skip), a predicate beside `closed_row`
- `plugin/templates/jig/RULES.md`: Metarepo and pararepos, **Citing the metarepo**
- `tests/smoke.sh`: `pararepo`, `pin_bump`, `sync_buffer`

## Alternatives considered

- Cache the roadmap at the pin (`fill_cache`) and check it there (Maige-OS's recommendation 3 as
  written) — rejected because R6 settled a live read ("reading it live is smart regardless, read
  it live, settled"), the pin's roadmap lags trunk (a roadmap change alone can't be released), and
  `pointers()` reads every cached `*.md`, so P2 would ask BUFFER rows for project data — [seen]
- Skip roadmap cites entirely (Maige-OS's recommendation 1) — rejected because a cite to a heading
  that's gone should be reported, and Issue 1 makes such cites deliberate — [seen]
- Add `.jig/roadmap.md` to `entry_files` — rejected because `is_entry` drops every `.jig/` path but
  the decision log, and that would make the roadmap a contract — [seen]
- Leave DEFERRED rows out as history (the report's change 3, first half) — rejected because retro
  re-ranks and takes deferred rows, so their cites are live work, and the live read already clears
  the one Maige-OS saw — [seen]
- Leave out only a copy whose BUFFER row is Closed (the report's change 3 as written) — rejected
  because it needs a lookup into BUFFER.md for no gain: an Open copy only repeats the Open
  BUFFER row's notice, and a row edited after proposing is still its old form in the copy — [seen]
- Exempt all of `.jig/specs/` — rejected because a live spec's cite should be checked — [seen]
  (this repro's `t.md` is such a spec)
- Leave the release reading the roadmap at its tags — rejected because it would ask a pararepo to
  bump its pin over a cite the bump can't change — [seen] (direct call above)

## Decisions

- The roadmap cite's message names the metarepo's trunk, not the pin, because the reader's next
  move differs: fix the cite or ask the metarepo, never bump.
- `ROADMAP.md` (the generated view) is read live too: it's derived from the roadmap on the same
  trunk, and it isn't cached either.

## Roles

spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
