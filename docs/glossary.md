# Glossary

The words jig uses, one heading each: what the word means, and what it doesn't.

## Trunk

The branch everything merges into, usually `main`. Only the hubnode commits on it. It isn't
a release: a release is a tag on trunk.

## Job

One piece of work in flight: a branch, its own git worktree, and a claim on the files it may
change. A job isn't a task list or a ticket. It opens on the board and closes when it merges.

## Board

The two files on trunk that say what's going on: `.jig/config.json` for the settings that
rarely change, and `.jig/jobs.json` for the open jobs. Only the hubnode edits them. The board
isn't a kanban view, and nobody ticks anything on it.

## Owns and shares

A job's two file lists. A file a job owns is one no other open job may change. A file it
shares, others may change too. They aren't permissions on the file system: a git hook checks
them at every commit.

## Hubnode

The owner's session, in the trunk checkout. It opens jobs, assigns each step, gates and merges.
It builds no feature itself. It isn't a daemon or a server: it's a chat you're having.

## Subnode

Every other session. A subnode takes one role on one job, works only in that job's worktree, and
reports back to the hubnode. It never commits on trunk, pushes or merges.

## Role

The kind of step a subnode takes: spec, bug, work, review or check. Each role runs at its own
tier and effort. A role isn't a person or a permission, and the hubnode's own steps (gate,
merge, release) belong to no role.

## Tier

A number standing for a model, from 1 (the strongest) down. `plugin/tiers.json` maps each
number to a model, so the rules never name one. A tier isn't a price or a quality score.

## Effort

A number standing for how hard a model thinks, from 0 (the most) to 4 (the least).
`plugin/tiers.json` maps each to an effort level. It isn't a time budget.

## Workflow

A fixed order of steps, such as Job (spec, work, review, handoff, gate, check, merge). Each
workflow says which role or node takes each step and whether it starts a new session. It
isn't a CI pipeline: people and sessions take the steps, and jig refuses one out of order.

## Spec

A short Markdown file, written before anything is built, saying what the task is and how
you'll know it's done. It isn't a design document. It names the files it touches, its done
checks, and the choices it made.

## Handoff

A mergeable chunk of a job, with a note naming the exact commit that was reviewed. A job can
hand off several times. A handoff isn't a merge: the hubnode still gates it.

## Gate

The hubnode's check that a handoff can merge. It confirms the note and the review, then sets up
a scratch checkout of that commit with trunk merged in, where the complete check runs. A gate
isn't the merge itself.

## Batch

Two or more gated jobs merged together, with one complete check on trunk afterward. A failure
is traced to the merge that caused it. A batch isn't a release.

## Workaround

A patch for a symptom when the cause isn't fixed yet. It gets a `WORKAROUND:` comment in
the code and a row in a ledger, or the commit is refused. It isn't a bug fix.

## Page contract

The shape every docs page keeps: a lead paragraph, sections named for what the system has,
then optional Talks to and Invariants sections. It isn't a style guide for prose.

## Decision log

One file per repo, `.jig/decisions.md`, holding every decision (who, when, what it replaced)
and every change line, grouped by release. It isn't a wiki. A changed mind is a new entry
that replaces the old one.

## Phase

A stage of a roadmap, in order, with an exit checklist. A phase has no dates. It isn't a
sprint.

## Scope

A named piece of a phase, written `<phase>/<scope>`. A spec takes one or more scopes, and a scope
is done when every spec taking it has landed. A scope isn't a ticket, and nobody marks it done.

## Staging

A folder, `.jig/staging/`, where a file written in another chat waits for a session in the repo
to land it or drop it. It's never committed, and nothing in it is decided yet.

## Inbox

A folder, `.jig/inbox/`, of messages to a repo's hubnode from sessions elsewhere. The hubnode
reads them; it answers only through the owner. It's never committed.

## Metarepo

A repo of docs only: the definitions, decisions and contracts that several product repos
share. It holds no code and copies nothing from them.

## Pararepo

A code, firmware or hardware repo that cites a metarepo at a released tag. It changes the
metarepo only through a proposal branch. It isn't a fork or a submodule.

## Rigger

A design session for one product repo, kept outside it. It holds the owner's running record
of the product and reaches the repo only through staging and the inbox. It never edits the repo.
