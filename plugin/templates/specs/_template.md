# <task name>

Source: <who asked or reported, when; for a bug, the symptom in their words>
<!-- A line of its own here, `Scope: <phase>/<scope>, …`, naming the roadmap ids this task
     takes (`No phase/<id>` for an item). No id taken: no line. A spec takes only what it
     builds: a scope it builds only part of is split first, by a roadmap change on the owner's
     yes, and the spec takes the new scope holding the built part. The rest stays in the
     original scope, under its id, its text unchanged, and a wait on that id holds until the
     rest is built. -->

## Intent
One or two sentences. What should be true when this is done that isn't true now.

## Done when
- [ ] observable check 1 (a test, a command output, a thing on screen)
- [ ] observable check 2

## Out of scope
<!-- Work nothing will do, or work another named spec, job or repo does, each with why. Out of
     scope never defers: this section closes with the spec. Work worth building later goes
     onto the roadmap as a scope or No phase item on the owner's word, and stays there,
     unspecced, until a spec takes it. -->
- what this task deliberately does not touch

## Touches
- files / modules expected to change

## Alternatives considered
<!-- Required for any fix. Proof you looked one layer up. -->
- <sibling path or correction> — rejected because <reason> — reason is [seen|assumed]

## Decisions
- anything chosen during the work that someone would ask "why?" about later

## Roles
<!-- `python3 .jig/jig.py roles`'s output when this spec was written, as printed. The
     repo's settings, not this task's: never edit a role here. -->
