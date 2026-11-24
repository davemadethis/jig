# 🔩 jig

AI coding agents are fast, and they drift. They skip the plan, fix the symptom, wave a review
through, and step on each other when two of them share a repo. A woodworker solves the same
problem with a jig: clamp the work in place once, and the cuts come out the same each time.

So that's what this is. A short written [spec](docs/glossary.md#spec) before building, a bug
looked into before it's fixed, and one review per [handoff](docs/glossary.md#handoff) from a
reader who never saw your reasoning. Parallel sessions each get a [job](docs/glossary.md#job)
with its own files, and a git hook refuses a commit outside them. The hooks run
[trunk](docs/glossary.md#trunk)'s copy of the rules, so no branch can weaken them. I built it
for prototyping software and firmware with Claude Code, but the checker runs fine without
Claude Code.

## 📦 Install

You need git, Python 3.10 or newer, and Claude Code. The repo half needs only git and Python.

```sh
claude plugin marketplace add davemadethis/jig
claude plugin install jig@davemadethis
```

To try it for one session without installing, clone this repo and run
`claude --plugin-dir ./jig/plugin`.

## 🧭 A first job

We'll walk one small job from start to finish, in a repo with a `src/app.py` and a `src/other.py`.

**1. Set up.** You run `/jig:init` in the repo. It writes a hidden `.jig/` folder (the checker,
the rulebook, the [board](docs/glossary.md#board), an empty [roadmap](docs/glossary.md#roadmap)
and an [ideas log](docs/glossary.md#ideas-log)) and installs the git hooks. Your root gets a
short `AGENTS.md`, a one-line `CLAUDE.md` and `ROADMAP.md`, the roadmap's view. Commit what it
wrote.

**2. Write the spec.** You run `/jig:spec greeting`, and describe the task. It writes
`.jig/specs/greeting.md`: what the task is, the files it touches, and how you'll know it's done.
You read it, fix what it got wrong, and commit it.

**3. Open the job.** Your session is the [hubnode](docs/glossary.md#hubnode): the one that owns
trunk, the board and every merge. It opens the job, which may change
only `src/app.py`:

```sh
python3 .jig/jig.py open greeting --spec .jig/specs/greeting.md --owns src/app.py
git add .jig/jobs.json && git commit -m "open greeting"
```

That makes a branch and a worktree at `.git/jig/worktrees/greeting`, and prints a kickoff
naming both. The board is committed on trunk, because the hooks read trunk's copy.

**4. Build it.** The hubnode starts a second session in that worktree with the kickoff. That's
a [subnode](docs/glossary.md#subnode), in the work [role](docs/glossary.md#role). Say it edits `src/app.py`, and also
strays into `src/other.py`. The commit is refused:

```
$ git commit -am "greet"
jig: R3 src/other.py is not job greeting's: ask the hubnode to add it to shares
```

The subnode puts `src/other.py` back and commits again. If the job really needs that file, the
hubnode adds it with `python3 .jig/jig.py share greeting src/other.py`.

**5. Review.** The hubnode starts a fresh session for `/jig:review`. It sees the diff, the spec
and the rules, and none of the conversation. The hubnode records the review in the job's
worktree. The record says the review role's [tier](docs/glossary.md#tier) and
[effort](docs/glossary.md#effort), and how many blocking findings it left:
`python3 .jig/jig.py reviewed --tier 2 --effort 2 --blocking 0`.

**6. Hand off.** The work subnode runs `python3 .jig/jig.py handoff`, which writes a note naming
the reviewed commit. The subnode fills in every heading of the note and commits it. That's the
[handoff](docs/glossary.md#handoff).

**7. [Gate](docs/glossary.md#gate).** The hubnode runs `python3 .jig/jig.py gate greeting`. It
sets up a scratch checkout of that commit with trunk merged in, and prints the complete check
to run there.

**8. Check.** The hubnode starts a check subnode, which runs that printed check in the scratch
checkout. When it passes, the subnode records it there, with the check role's tier and
effort:
`python3 .jig/jig.py checked --tier 3 --effort 4 --seconds <s>`. Then the hubnode runs
`python3 .jig/jig.py mark greeting gated` and commits `.jig/jobs.json` on trunk.

**9. Merge.** On your word, the hubnode runs `python3 .jig/jig.py merge greeting`. The job's
entry leaves the board in the merge commit, and its worktree and branch go away.

Every step above belongs to a [workflow](docs/glossary.md#workflow), and each subnode takes one
role in it. At any point, `python3 .jig/jig.py next` says what each job needs next and who
takes it.

## 📚 Read more

- [Jobs](docs/jobs.md): the board, owned files, the rules, handoff, gate and merge.
- [Workflows](docs/workflows.md): [nodes](docs/glossary.md#node), roles, workflows, and who takes each step.
- [Records](docs/records.md): pages, the [decision log](docs/glossary.md#decision-log), the ideas log, the [roadmap](docs/glossary.md#roadmap), [staging](docs/glossary.md#staging) and releases.
- [Metarepos](docs/metarepos.md): several repos sharing one set of decisions and one roadmap through a [metarepo](docs/glossary.md#metarepo), and moving a claim from one repo to another.
- [Commands](docs/commands.md): every skill and checker command.
- [Hooks](docs/hooks.md): what runs, when, and why it's safe.
- [Glossary](docs/glossary.md): every jig term, and what it isn't.

After init, `.jig/RULES.md` in your repo holds every rule the hooks enforce.

**On trust.** All but one of jig's plugin hooks run only in a repo that opted in, with a marker git
never clones. The session-start hook only reads and prints one line. [More](docs/hooks.md).

## 💬 Feedback and working on jig

This is a personal tool, built in the open. Issues and discussion are on GitHub. If jig
misbehaves in your repo, run `/jig:feedback`. It looks into the cause and stages a report in the
jig repo, without patching your copy.

To work on jig itself, start with `AGENTS.md`. This repo runs jig on itself: `.jig/` is the
installed release, and `plugin/` is the code you edit. `bash tests/smoke.sh` runs every rule
end to end in throwaway repos.
