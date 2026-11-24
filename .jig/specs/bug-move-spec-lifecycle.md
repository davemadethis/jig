# Bug: `jig move` step 2 on a pararepo's trunk gives the move's spec no lifecycle, and step 1 infers a drop

Source: the jig hubnode, 2026-11-24, starting the bug role on job `moving-in-command` after Part C's third blocking review (c40ea6c). The reviewer's words, as the hubnode relayed them: "P2 now refuses step 2 of an up move of a contract-path page", and "the spec that stays is listed by rig as 'Can start now', and nothing ever closes it". The three blocking reviews:
- e6d557f: B1 sideways items went to the wrong plan; B2 up from a pararepo with its own roadmap forwarded a roadmap file to M instead of going through `propose/`; B3 spec `Later:` ids weren't counted as taken; B4 a finished move's spec stayed and rig offered it as new work.
- 4e57127, after the work session moved the sideways pointers proposal to step 1 so step 2 could close the spec on a pararepo's trunk: M could merge pointers before the receiver had the page; deleting a spec that names a pointers branch broke `jig sync`'s tracking and `trunk_answers`.
- c40ea6c: B1 and B2 above. It also left one should-fix, S3: a landing in progress in the receiver's job worktree, uncommitted, reads as "dropped", so `--apply` sends the file again. And one optional, O4: step 2's commit warns about an item step 2 just proposed moving.

Bug-for: moving-in-command

## Intent
A move's spec has the lifecycle every jig spec has, in every repo. Step 1 writes it on trunk,
step 2 runs in the job opened from it, and `jig merge` closes it, or keeps it in a pararepo while
it names a metarepo branch. P2 reads the move's answer where it reads any job's: the job's own
spec on trunk, or a spec the job's branch changed. `jig rig` offers a move's spec only once step
2 is next. Down or sideways, step 1 is done once its spec records the move, and jig never infers
that the receiver dropped the file. A sideways move proposes rewriting the metarepo's pointers to
the moved thing only.

## 1. Why
- Why did c40ea6c's review block? On L's trunk, step 2 of an up move deletes the spec holding
  `meta: M proposal …`. P2 reads answers from the index, so the page's removal has none. [seen]
- Why does step 2 delete it? On a pararepo's trunk no job's merge closes it. So 4e57127 closed it
  in step 2's own change, after e6d557f B4 found it offered as new work. [seen]
- Why is there no job? Step 2 was let run on a pararepo's trunk, though step 1 writes "the spec
  of the job that removes the claim". M4 refused it, but only in a metarepo. [seen]

Root: step 2 on a pararepo's trunk is a spec's change with no job. jig closes a spec, answers P2
for it and hides it from rig only through a job and its note. So each round patched one face of
a spec that had none: deleting it lost P2's answer and `jig sync`'s link, and keeping it left rig
offering it with nothing to close it.

| Review | Finding | What the trunk route did |
|---|---|---|
| e6d557f B4 | a finished move's spec stayed, and rig offered it | no note names it, so rig reads it as waiting work |
| 4e57127 | M could merge pointers before the receiver held the page | pointers moved to step 1 so the spec could close at step 2 |
| 4e57127 | deleting a spec naming a pointers branch broke `jig sync` and `trunk_answers` | closing in the change deletes the record sync follows |
| c40ea6c B1 | P2 refuses an up move of a contract page, and sideways with no branch | the change deletes its own answer; sideways with no branch never had one |
| c40ea6c B2 | the spec that stays is "Can start now", and nothing closes it | no note names it, and `finished_specs` closes only specs a note completes |

e6d557f B1 to B3 were code errors (the wrong plan, the wrong route, `Later:` ids), fixed in
4e57127, outside this root.

S3 has Part A's root (bug-move-in-record): state rebuilt from another repo instead of read from
step 1's record. Down or sideways, step 1's state is read from the receiver's staging folder and
branch heads, and "dropped" is inferred from finding nothing. A file `jig staging resolve` has
taken into a job worktree, uncommitted, is in neither. [seen]

O4 has no root here: a warning that is true of M's trunk until M merges the proposal (Out of
scope).

## 2. Givens
The repros are in
`/private/tmp/claude-501/-Users-daveseeman-Documents-GitHub-jig/d0fb14f3-b0e1-4eb6-bed0-c764cdad21c0/scratchpad/`,
run at c40ea6c: `fix.sh` is the reviewer's fixture (M with `E-`, L and K planning from M, L's
`contract_paths` `docs/**`, L's `docs/l.md`), and `p1.sh` to `p7.sh` each run on it.

- [seen] B1, up: the reviewer's `rvc/s9.sh up2` reproduces. Step 2 on L's trunk prints "closed
  .jig/specs/move-docs-l-md.md", the index holds the spec as deleted, and the commit is refused:
  "P2 docs/l.md is a contract path: …".
- [seen] B1, sideways with no branch (`p3.sh`, M citing nothing and holding no item): step 2
  prints "M has no pointer to L/docs/l.md and no roadmap item for it: no proposal" and "closed
  …", and P2 refuses the commit the same way. Step 1's spec for a sideways move has no `meta:`
  line (jig.py:17061-17065; only up appends one), so keeping that spec wouldn't answer P2 either.
- [seen] P2's sources (jig.py:8307-8337): a spec in this change, read in the index; on a job
  branch, the specs `trunk...HEAD` changed; at a merge, the specs the merging side changed, read
  there; the job's own spec as trunk holds it. Each is tied to the change. None reads a spec the
  commit deletes on trunk; the hubnode's revert of 4e57127's read at the base kept it so.
- [seen] The job route answers B1 with nothing changed (`p5.sh`). M merges the up proposal. `jig
  open lup --spec .jig/specs/move-docs-l-md.md` runs in L, step 2 `--apply` runs in its worktree,
  and the commit passes P2, read from the job's own spec on trunk. `jig gate lup` then refuses:
  "cites proposal propose/L-move-docs-l-md, which is not in M v0.1.0, the pin, nor in any
  release: it merges once it's released and pinned" (`unreleased_proposals`).
- [seen] With the gate stood in for, as smoke's `gated` does, `jig merge lup` prints "kept
  .jig/specs/move-docs-l-md.md: it names a metarepo proposal or pointers branch `jig sync`
  follows", and `jig rig` offers nothing. `jig rig --close` keeps it too. `finished_specs`
  (jig.py:10936) keeps a pararepo spec naming a branch with no test of a release, so it stays for
  good, as RULES.md (Merge) says every such spec does. No smoke case covers that keep.
- [seen] `jig merge` moves a moved page's roadmap items in its merge commit in any repo with a
  roadmap on trunk (`items_follow_moves`, jig.py:2109). A pararepo keeping its own roadmap loses
  them there, which the hubnode's Interpreted line already allows ("or `jig merge` does it in a
  job").
- [seen] B2 (`p6.sh`): after sideways step 2 on L's trunk, the spec stays, naming
  `propose/L-move-docs-l-md-pointers`. `jig rig` lists it under "Can start now", and `jig rig
  --close` prints "nothing to close". Step 2 printed that the spec stays "until M releases it",
  which nothing does.
- [seen] A waiting move (`p1.sh`): right after sideways step 1 is committed, before K lands the
  file, `jig rig` in L lists `.jig/specs/move-docs-l-md.md` under "Can start now". `waiting_specs`
  (jig.py:1383) counts every spec that no job, note or release tag names. `rig_state`'s waits come
  only from `Build after`, a staged file's `after:`, a carrier, roadmap refs and cycles
  (jig.py:15938-15955). Nothing in rig reads another repo.
- [seen] Siblings (`p2.sh`): a `jig propose --buffer` spec committed on L's trunk is listed
  under "Can start now" too. `move-in.md` (Part A step 1) has the same shape: rows under `##
  Buffer rows` and a `meta:` line, no job, no note. Both wait until the repo's next release tag
  holds them, and neither ever closes. `jig release`'s own buffer spec is committed with the
  release, so its tag holds it (jig.py:7532).
- [seen] S3 (`p4.sh`): K's job worktree resolves the staged file and commits nothing. L's plan
  prints "K has neither the file … nor its moved-from line: dropped there, so step 1 sends it
  again". `--apply` forwards it, and K's staging holds a second copy while the first lands in
  K's worktree.
- [seen] No repo records a drop. `jig staging drop` writes nothing ("A staged file was never
  committed, so a record of dropping it would point at nothing", jig.py:10077), and `forward`
  records nothing in the sender. Only the receiver's owner knows.
- [seen] N5, found in this investigation (`p7.sh`): M cites `L/.jig/decisions.md § D-001` and
  `§ D-002`. L moves D-002 to K, which numbers it D-003. Step 2's pointers proposal rewrites M's
  text to `K/.jig/decisions.md § D-001` and `§ D-002`. `move_pointers` (jig.py:17222) replaces
  the path `<me>/<path>` wherever it appears, so every pointer into the log or page moves, and an
  entry keeps its old id. A section move rewrites every pointer to its page the same way.
- [seen] O4 (`p6.sh`): step 2's commit warns "M's .jig/roadmap.md: `Walyt alpha/lx` touches
  docs/l.md, which this commit leaves with no page: propose re-pointing it", after the step's own
  proposal moved `lx`. It warns and doesn't refuse, and M's trunk holds that line until it merges
  the proposal.
- [seen] Where the trunk route came from: Part C item 9 (c7581e1) calls the move's spec "the
  spec of the job that removes the claim", and item 10 refused step 2 only in a metarepo's trunk
  checkout (M4). 063a355 let it run on a pararepo's trunk and closed nothing. The close in step
  2's change came in 4e57127, with the Interpreted line on a pararepo editing its own roadmap "in
  step 2's change on its trunk".
- [seen] jig runs other page commands on a plain repo's trunk (`jig update --sweep`, `jig
  redocument --apply`; RULES.md:476-480, 526-528), but none of them writes a spec.
- [assumed] An up move's job waiting at the gate until the pin holds its proposal costs the
  pararepo a pin bump it would take anyway. Not converted: that needs use. It is jig's rule for
  every pararepo job citing a proposal (RULES.md: "a dependency on a metarepo change is `proposal
  <branch>`, which the gate waits for"). Held as a cost in time, not a risk to correctness.
- [assumed] A receiver may resolve a forwarded file somewhere `git worktree list` from its main
  checkout doesn't show, such as a session's own clone. Not converted. The fix doesn't rest on it,
  because it stops reading the receiver for step 1's state at all.

## 3. One layer up
- **Siblings.** A pararepo spec naming a metarepo branch has two shapes today:
  - A job's spec (`jig propose <spec> <slug>`, or `--pointers`). P2 reads it as the job's own
    spec or the branch's change. The gate waits for a `proposal`, and needs a `pointers` branch
    only to be real. rig drops it once its note lands, and `jig merge` keeps it while it names
    the branch. No problem (`p5.sh`).
  - A record with no job (`jig propose --buffer` by hand, `jig move-in`'s `move-in.md`). rig offers
    it as work until a release tag holds it: B2's symptom (`p2.sh`).

  A metarepo's move already has the first shape: smoke's `move (down)` runs step 2 in M's job,
  and the merge closes the spec. A pararepo's move should have it too.
- **What's different.** Only the pararepo's trunk route. It writes a spec that no job carries, so
  the spec reaches neither P2's job read nor `jig merge`'s close. Every round since 063a355 moved
  work around that and never removed it.
- **Existing paths this reuses as they are.**
  - The job path: `jig open --spec`, P2's job and branch reads, `unreleased_proposals` at the
    gate, `finished_specs`'s keep in a pararepo, `items_follow_moves` in `jig merge`, and the
    metarepo job's rule for a receiver's roadmap file: staged, unforwarded until the merge, then
    forwarded by `jig staging resolve`.
  - P2's `meta: none — <reason>` answer, for a sideways move with nothing to propose.
  - `move_records`' scan of specs as step 1's record, as Part A's fix reads its own. The receiver
    is asked only what it decides: its moved-from line on trunk.
  - `pointer_parts` and `same_thing`, which `moved_from_in` and `dangling` use to match a moved
    thing, for N5.
  - `listed_rows`, for telling a proposal's record from a spec of work.
- **Where no path exists.** rig can't say a spec waits on another repo. The one addition is rig
  reading a move's state with `jig move`'s own reader. Nothing new is recorded.

## 4. Workaround or correction
Corrections, all three:
- Step 2 runs in a job in every repo, so the move's spec has the lifecycle every spec has. The
  pararepo trunk route goes, and with it the close in step 2's own change.
- Step 1 reads its state from its own record. A drop is the owner's word.
- Pointers are rewritten by the moved thing, not by its path.

The two fixes on the table, P2 reading a deleted spec and a close for specs with no note, would
each add a second route for one kind of spec. They are rejected below.

## 5. Spec

### Change
1. **Step 2 runs in a job, in every repo.** `--apply` refuses step 2 in any trunk checkout,
   naming the job: `jig open move-<slug> --spec <spec>`, then `jig move … --apply` in its
   worktree. In a metarepo the reason stays M4. In a pararepo it is that the move's spec is a
   job's. Two pieces go:
   - the close in step 2's change (`on_trunk and meta is None`, jig.py:17166-17172);
   - step 2 writing this repo's roadmap on trunk (jig.py:17201-17205). `jig merge` moves those
     items in the job's merge commit in any repo, as `items_follow_moves` already does.

   A receiver keeping its own roadmap gets its file as it does from a metarepo's job, in every
   repo: staged in the main checkout, unforwarded until the job merges, then forwarded by `jig
   staging resolve`.
2. **P2's answer comes from the job path, unchanged.**
   - Up: step 1's `meta: <meta> proposal <branch>`, in the job's own spec on trunk. The gate waits
     until the pin holds the proposal (`unreleased_proposals`), and `jig merge` keeps the spec.
   - Sideways, with a pointers branch: step 2 writes `meta: <meta> pointers <branch>` into the
     spec on the job's branch, as it does now, and `jig merge` keeps the spec.
   - Sideways, with nothing to propose: step 2 writes `- meta: none — <meta> names nothing of
     <me>/<path>[ § <s>]; it moved to <to>/<there>` into the spec on the job's branch. `jig merge`
     closes the spec, and P2 at the merge reads it from the job's side.

   P2 itself is unchanged. No P2 reads a spec its own commit deletes.
3. **rig offers a move's spec only when step 2 is next.**
   - A spec with a `- move:` record is listed under Waiting on, as waiting on `<to>`'s moved-from
     line for `<what>` (or on `<to>` being reached), until the receiver's trunk holds that line
     with its id numbered. One reader gives a move's state from its record and the receiver's
     trunk, and `jig move` and rig both call it.
   - A spec whose `## Buffer rows` lists rows (`jig propose --buffer`, `jig move-in`) is a
     proposal's record, not work. It never waits, so rig never offers it. `listed_rows` reads it.
4. **Down or sideways, step 1's state is its record's.**
   - A spec carrying the `- move:` line means step 1 is done, and step 2 waits on the receiver's
     trunk.
   - The reads of the receiver's staging folder and branch heads for step 1's state go, and so
     does the "dropped" state.
   - The plan says whether the file is still in `<to>`'s staging. When it isn't, the plan adds:
     "if `<to>` dropped it, delete `<spec>` on the owner's word, and run step 1 again".
   - With the spec gone, `move_records` finds no record, and step 1 sends the file again under
     the same name.
5. **Pointers move with the thing (N5).** `move_pointers` rewrites a pointer only when
   `pointer_parts` names this repo and `same_thing` matches the moved thing:
   - an entry's `<me>/.jig/decisions.md § <id>` becomes `<to>/.jig/decisions.md § <landed id>`;
   - a section's `<me>/<path> § <s>` becomes `<to>/<as> § <s>`;
   - a whole page's `<me>/<path>`, with any `§` part, becomes `<to>/<as>` with the same `§` part.

   Every other pointer into that page or log stays. With no pointer to rewrite and no item to
   move, no branch is made, and item 2's `meta: none` line answers P2.
6. **Text.**
   - `.jig/specs/moving-in-command.md`:
     - Part C item 10: "It stages the change in the checkout it runs in. In a metarepo's trunk
       checkout it is refused, because M4 puts the change in a job" becomes "It runs in the job
       opened from the move's spec, in any repo. In a trunk checkout it is refused, naming that
       job."
     - The "Otherwise, step 2 closes the move's spec" bullet becomes the close by `jig merge`,
       kept in a pararepo while it names a branch, plus the `meta: none` line for sideways with
       nothing to propose.
     - Item 11's "in step 2's change on its trunk, or by `jig merge` in a job" becomes "by `jig
       merge` in the job".
     - The 2026-11-23 Interpreted line on a pararepo keeping its own roadmap reads "`jig merge`
       does it in the job, as in a metarepo".
     - Part C's Done when runs step 2 of the up and sideways cases in L's job.
   - RULES.md, Metarepo and pararepos, Moving claims (around line 1596). Step 2 runs in a job
     opened from the move's spec in every repo, and is refused in a trunk checkout. `jig merge`
     closes the spec, keeping it in a pararepo while it names a metarepo branch. Down or
     sideways, step 1 is done once its spec records the move, and a drop is the owner's word:
     delete the spec, then run step 1 again. The pointer rewrite is the moved thing's. A sideways
     move with nothing to propose answers P2 with `meta: none`.
   - RULES.md, The board ("waiting") and Workflow (rig's items): a spec listing buffer rows never
     waits, and a move's spec waits on its receiver until step 2 is next.
   - `docs/metarepos.md` (Moving claims) and the hubnode skill's move line: step 2 in a job, in
     any repo.

### Done when
Smoke, `move` section, in its throwaway repos (`JIG_CONFIG`, `XDG_CONFIG_HOME` set). The fixture
gains a pararepo whose `contract_paths` cover its pages: L, or a new one.
- [ ] (up, a contract page: the reported B1) Step 1 moves `docs/u.md` up, and M merges the
  proposal.
  - On L's trunk checkout, step 2 `--apply` is refused, naming `jig open … --spec
    .jig/specs/move-docs-u-md.md`, and nothing is staged.
  - In the job opened from that spec, `--apply` stages the removal and the move line, and the
    commit passes. There, `git diff main -- .jig/specs/move-docs-u-md.md` is empty.
  - `jig gate` refuses, naming the proposal and the pin.
  - Once a release of M holding the proposal is pinned, the gate passes, and `jig merge` prints
    `kept .jig/specs/move-docs-u-md.md`.
  - Then `jig rig` doesn't list it, and `jig sync` prints `proposal propose/L-move-docs-u-md
    (.jig/specs/move-docs-u-md.md): released by`.
- [ ] (sideways, nothing to propose: B1) M names nothing of L's contract page `docs/n.md` and
  holds no item for it. After K lands it, step 2 in L's job writes `- meta: none — M names
  nothing of L/docs/n.md;` and the rest of the line into the spec. It makes no branch in M, and
  the commit passes. `jig merge` removes the spec in its merge commit, and `jig rig` doesn't
  list it.
- [ ] (sideways, pointers) The existing case, run in L's job:
  - the spec gains `- meta: M pointers propose/L-move-docs-l-md-pointers` on the branch;
  - `jig merge` prints `kept .jig/specs/move-docs-l-md.md`, and `jig rig` doesn't list it;
  - `jig sync` prints `pointers propose/L-move-docs-l-md-pointers (.jig/specs/move-docs-l-md.md):`.
- [ ] (rig, a waiting move: B2) Right after step 1 is committed, before the receiver lands it,
  `jig rig` lists the move's spec under Waiting on, naming the receiver, and not under Can start
  now. This holds in L for a sideways move and in M for a down move. Once the receiver's trunk
  holds the numbered moved-from line, rig lists it under Can start now.
- [ ] (rig, a finished move: B2) After each merge above, `jig rig` lists no move spec, and `jig
  rig --close` closes none and changes nothing.
- [ ] (records aren't work) In a pararepo, `jig rig` lists neither of these under Can start now
  or Waiting on: a `jig propose --buffer` spec committed on trunk, and `move-in.md` once `jig
  move-in` step 1 is committed.
- [ ] (a landing in progress: S3) K resolves the staged file in a job worktree and commits
  nothing. L's plan says step 1 is done and step 2 waits on K, and says nothing of "dropped".
  `--apply` says there is nothing to apply, and K's staging gains no file.
- [ ] (dropped, on the owner's word) K drops the staged file. L's plan still says step 1 is
  done, says the file isn't in K's staging, and names deleting the spec. Once the spec's
  deletion is committed, `--apply` sends the file again under the same spec name, and K's staging
  holds it.
- [ ] (pointers by the thing: N5) M cites `L/.jig/decisions.md § D-001` and `§ D-002`. L moves
  D-002 to K, which numbers it. The pointers proposal names `K/.jig/decisions.md § <its id>` for
  D-002 and leaves `L/.jig/decisions.md § D-001` as it was. A section moved sideways rewrites the
  pointers to that section only.
- [ ] `grep -c 'is done once this commits' plugin/templates/jig/jig.py` prints 0, and no
  output of step 2 says a spec stays until a release.
- [ ] `python3 .jig/jig.py queue -- bash tests/smoke.sh move moves movein pararepo metarepo
  roadmap rig close boundary staging decisions supersede removals pin_bump claims sync_buffer`
  passes. `claude plugin validate ./plugin` and `.jig/scripts/check.sh` pass.

### Out of scope
- O4, the warning on step 2's commit about an item its own proposal moves. It warns and doesn't
  refuse, and it is true of M's trunk until M merges the proposal. Silencing it would need the
  boundary check to read the proposal branch, a second reader for an optional finding. [seen]
- Closing a pararepo spec that names a metarepo branch once the pin holds it. `finished_specs`
  keeps every such spec for good (rig-and-versioning, a12af04), and `jig sync` reads them. The
  move's spec joins that rule as it is, by the owner's rule to reuse a path as it is. A close for
  all of them changes that rule, which isn't this job's.
- Not gating an up move's job on its release. Waiting for the pin is jig's rule for every
  pararepo job citing a proposal, and the move's job joins it.

### Touches
- `plugin/templates/jig/jig.py`:
  - `cmd_move`: the trunk refusal in any repo; step 1's state from its record down and sideways,
    with the staging and branch reads and "dropped" gone; the plan's line for a file not in the
    receiver's staging; the move's state as one reader, which rig calls too;
  - `move_step2`: the close and the trunk roadmap write go; `meta: none — …` when sideways makes
    no pointers branch;
  - `move_items_here`: the receiver's roadmap file as from a metarepo's job, in every repo;
  - `move_pointers`: rewrites by `pointer_parts` and `same_thing`, with the landed id for an entry;
  - `waiting_specs` (a spec listing buffer rows never waits) and `rig_state` (a move's spec
    waits on its receiver).
- `plugin/templates/jig/RULES.md`: The board (waiting), Workflow (rig's items), Metarepo and
  pararepos (Moving claims).
- `docs/metarepos.md` (Moving claims); `plugin/skills/hubnode/SKILL.md` (the move line).
- `.jig/specs/moving-in-command.md`: Part C items 10 and 11, the Interpreted line, Part C's Done
  when.
- `tests/smoke.sh`:
  - `sec_move`: the cases above. The existing up, sideways, Q and L cases that run step 2 on a
    pararepo's trunk move into jobs (`gjob`), and the `dropped` case takes the owner's word.
  - `sec_movein` or `sec_rig`: the records-aren't-work case.

### Alternatives considered
- **P2 reads a spec its commit deletes, at the base** (4e57127, reverted on the hubnode's
  word). Rejected because it lets any commit that deletes an old spec with a `meta:` line answer
  any contract change in it, where every P2 source today is tied to the change
  (jig.py:8307-8327). It would also leave rig offering the spec and nothing closing it. This
  reason is [seen].
- **Keep the trunk route: the spec stays, step 2 touches it so P2 reads it in this change, and a
  new close takes specs with no note.** Rejected because it is a second lifecycle for one kind of
  spec, with a close jig doesn't have, where the job path already does all three (`p5.sh`). The
  owner's rule is to reuse a path as it is. This reason is [seen].
- **The pointers proposal at step 1, so step 2 can close the spec** (4e57127). Rejected by that
  round's review: M could merge pointers to a page the receiver didn't hold yet. This reason is
  [seen].
- **Step 1 writes no spec in a pararepo.** Rejected because `jig sync`, `withdraw_proposal`, P2
  and the gate all read `meta:` lines from specs, and an up move needs one. This reason is
  [seen].
- **Read the receiver's worktrees too, to tell a landing in progress from a drop.** Rejected
  because it is still an inference from absence, the root Part A's bug named, and a landing can
  sit where `git worktree list` doesn't show it. This reason is [assumed] for the clone. The fix
  doesn't rest on it.
- **An `--again` flag to send the file again after a drop.** Rejected because deleting the record
  already makes `move_records` find none, and step 1 sends again. A flag is a new mechanism for
  the same word. This reason is [seen].
- **A `Build after` line to hold a move's spec until step 2 is next.** Not possible: `Build after`
  names a spec or job in this repo. This reason is [seen].

### Decisions
- A move's spec is a job's spec in every repo, in Part C item 9's own words. The pararepo trunk
  route goes. With it goes the Interpreted line letting a pararepo keeping its own roadmap edit it
  in step 2's change on trunk: `jig merge` does it in the job.
- The two hubnode rulings that fed c40ea6c were right in what they kept. P2 reads only answers
  tied to the change, and a pararepo spec naming a branch stays. Each was applied to the trunk
  route, which had no job to tie them to. On the job path both hold with no code special to
  moves.
- An up move's job merges once the pin holds its proposal, as any pararepo job citing a
  proposal does.
- A drop of a forwarded file is the owner's word, given by deleting the move's spec, as a
  withdrawal gives it for an up move. jig doesn't infer it.
- rig reads a move's state with `jig move`'s own reader. That is the one addition, where rig has
  no path for waiting on another repo.

## Roles
spec: tier 2, effort 2
bug: tier 2, effort 1
work: tier 2, effort 3
review: tier 2, effort 2
check: tier 3, effort 4
