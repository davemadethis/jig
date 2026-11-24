# Commands

jig has two kinds of command. Skills are slash commands in Claude Code, like `/jig:review`. The
checker's commands run anywhere as `python3 .jig/jig.py <command>`, by hand or from any agent
tool. Most skills are thin wrappers around the checker. Every command below either opens a
[job](glossary.md#job), moves one along to its [gate](glossary.md#gate), or keeps the repo's
records straight.

Only the owner runs the owner-only skills. The model never starts one on its own, so type it
yourself. Each one changes the repo, tags a release, writes your repo list, speaks for a
[hubnode](glossary.md#hubnode), or files a report on jig.

## Setting a repo up

- `/jig:init` sets jig up in a new or small repo. It writes the `.jig/` folder and installs the git hooks. **Owner-only.**
- `/jig:survey` takes a read-only inventory of a repo against the jig shape, in the repo's own terms.
- `/jig:adopt` writes a staged plan for bringing an existing repo onto jig, for you to approve before anything moves. **Owner-only.**
- `/jig:update` brings a repo already on jig up to a newer plugin. It's a dry run first, and it asks before touching your files. **Owner-only.**
- `/jig:redocument` converts a repo's pages to the current [page contract](glossary.md#page-contract) in one supervised pass. **Owner-only.**
- `/jig:hardware` writes a circuit's page from a hardware definition you supply, and installs the skills it needs.

## Day to day

- `/jig:spec <task>` writes the [spec](glossary.md#spec) before anything is built.
- `/jig:bug <symptom>` looks into the cause before any fix exists.
- `/jig:work` builds a job's spec, hands it off, and fixes what review finds.
- `/jig:review` gives the diff a fresh-context review, once per [handoff](glossary.md#handoff).
- `/jig:check` runs the complete suite for a gate, a [batch](glossary.md#batch) or a release.
- `/jig:subnode` checks a session in as a [subnode](glossary.md#subnode): one [role](glossary.md#role) on one job.
- `/jig:retro` turns a repeated fix into a skill or a line of process, and sorts the ledgers.

## The hubnode's

- `/jig:hubnode` starts your session as the hubnode: it owns [trunk](glossary.md#trunk), the [board](glossary.md#board) and merges.
- `/jig:rig` shows what can start, what waits on what, and what waits on you, then asks one batch of decisions. `/jig:rig auto` acts without asking where it can.
- `/jig:decision-cards` puts pending decisions to you, each with a recommended option.

## Across chats

- `/jig:stage` sends a file from this chat to a repo's [staging](glossary.md#staging), or resolves what's staged there.
- `/jig:repos` lists, adds, renames or aliases the repos jig knows by name. **Owner-only.**
- `/jig:relay <repo> <text>` marks pasted text as that repo's hubnode talking, in another chat, and a reply is owed. **Owner-only.**
- `/jig:send` shows the reply for you to edit and send, then drops it in the repo's [inbox](glossary.md#inbox). **Owner-only.**
- `/jig:rigger <repo>` makes this chat the repo's [rigger](glossary.md#rigger). **Owner-only.**

## Release and feedback

- `/jig:release` builds and tags a version, the way this repo ships. The first time, it writes the release script with you. **Owner-only.**
- `/jig:feedback` reports a bug in jig itself. It looks into the cause the way `/jig:bug` does, and stages the report in the jig repo without patching your copy. **Owner-only.**
- `/jig:fix`, in the jig repo, turns staged feedback into specs.

## The checker

Setting up and checking:

- `python3 .jig/jig.py init` writes the board, the decision log and the roadmap's empty structure, and installs the hooks. A pararepo gets no roadmap: it plans from its metarepo's.
- `python3 .jig/jig.py install-hooks` rewrites the hooks.
- `python3 .jig/jig.py rules` runs the rules here, as the hook does.
- `python3 .jig/jig.py survey` inventories the repo against the jig shape.
- `python3 .jig/jig.py update` lists what's needed to reach the current layout. `--apply` does it.

Jobs, for the hubnode:

- `python3 .jig/jig.py open <name> --spec <path> --owns <files>` opens a job.
- `python3 .jig/jig.py share <job> <path>` adds a path to an open job's shares.
- `python3 .jig/jig.py reserve <job> <counter>` gives an open job another scarce number.
- `python3 .jig/jig.py consolidate` lists waiting specs whose files overlap, to settle before they open.
- `python3 .jig/jig.py mark <job> <state>` sets a job's state.
- `python3 .jig/jig.py gate <job>` checks a handoff can merge and sets up its scratch checkout.
- `python3 .jig/jig.py merge <job>` merges a gated job, on the owner's word.
- `python3 .jig/jig.py rig` prints the repo's picture.

Jobs, for anyone:

- `python3 .jig/jig.py status` lists the jobs, their states, and how far behind trunk each is.
- `python3 .jig/jig.py job` prints this branch's entry on the board.
- `python3 .jig/jig.py next` names each job's next step and who takes it.
- `python3 .jig/jig.py roles` prints each role's [tier](glossary.md#tier) and [effort](glossary.md#effort).
- `python3 .jig/jig.py flows` prints each [workflow](glossary.md#workflow)'s steps.
- `python3 .jig/jig.py sync` brings trunk into a job.
- `python3 .jig/jig.py reviewed` records that a commit had its review.
- `python3 .jig/jig.py checked` records that the complete check passed.
- `python3 .jig/jig.py handoff` writes the handoff note.
- `python3 .jig/jig.py queue -- <command>` runs a test or check in one of the machine's slots, so parallel jobs don't fight for cores.
- `python3 .jig/jig.py reading-list <files>` lists the pages to read before touching those files.

Records:

- `python3 .jig/jig.py decision <id>` prints a decision and what it replaced.
- `python3 .jig/jig.py roadmap` prints the [roadmap](glossary.md#roadmap)'s states, each phase with its type (Prototype, Pilot or Production). `--product`, `--phase`, `--type`, `--state` and `--owner` narrow what it prints, each repeatable, and `--view` prints that part as the view's Markdown. `--write` regenerates the whole view, and takes no filter. Run in the trunk checkout on a trunk with no roadmap, it commits the roadmap's empty structure first, as the other commands that read the roadmap do.
- `python3 .jig/jig.py staging` lists staged files. `resolve` lands one and `drop` deletes one.
- `python3 .jig/jig.py inbox` prints the hubnode's unread messages and marks them read.
- `python3 .jig/jig.py release` runs the repo's release and tags it.

Across repos:

- `python3 .jig/jig.py repos` lists, or adds to, where your repos live.
- `python3 .jig/jig.py rigger <repo>` sets up a rigger's folder for a repo.
- `python3 .jig/jig.py propose <spec> <slug>` opens a proposal branch on the [metarepo](glossary.md#metarepo).
- `python3 .jig/jig.py move-in --product <Name>` moves a pararepo's [roadmap](glossary.md#roadmap) into its metarepo's. It shows each step and its state. `--apply` does the next one.
- `python3 .jig/jig.py move <what> --to <repo>` moves a decision entry, a page or a section to another repo of its family, both ends. It shows each step and its state. `--apply` does the next one.
